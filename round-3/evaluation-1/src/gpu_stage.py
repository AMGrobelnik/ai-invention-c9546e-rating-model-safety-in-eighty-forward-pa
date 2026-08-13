#!/usr/bin/env python3
"""GPU stage: axis re-derivation (V2), held-out item harvest, forward-pass-only
re-encode of archived text, projection onto every axis (V1/V3).

No sampling, no steered generation, no training.  Every model is pinned to the
revision_sha recorded in the EXP1 archive and loaded in the archive's dtype.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np
import psutil
from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import eval_lib as EL  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(HERE / "logs").mkdir(exist_ok=True)
logger.add(HERE / "logs/gpu_stage.log", rotation="30 MB", level="DEBUG")

# ---- resource limits -------------------------------------------------------
_avail = psutil.virtual_memory().available
RAM_BUDGET = int(min(16e9, _avail * 0.5))
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

MAX_ITEMS_PER_CKPT = 1400
MIN_COMPLETION_TOKENS = 8


# ===========================================================================
# Axis re-derivation
# ===========================================================================
def rederive_axes(key: str, sm, render, meta: dict, AX, DIR) -> dict:
    """Re-fit A/B/C/D/E with the archived code on the archived inputs."""
    L = int(meta["L"])
    prompts_doc = EL.load_json(EL.EXP1 / "results/prompts.json")
    splits = {"fit_benign": prompts_doc["axis_fit_prompts"],
              "held_benign": prompts_doc["axis_held_prompts"]}
    out: dict[str, dict] = {}

    # A: canned-apology response contrast at every layer (EXP1 uses the profile fit)
    prof = DIR.fit_response_direction(sm, splits, render)
    a_dir = prof["directions"][L].astype(np.float32)
    out["A_canned"] = {"direction": a_dir, "raw_norm": float(prof["diff_norms"][L]),
                       "heldout_auroc": float(prof["auroc"][L]),
                       "cohens_d": float(prof["dprime"][L])}
    out["_norm_profile"] = [float(x) for x in prof["diff_norms"]]
    out["_auroc_profile"] = [float(x) for x in prof["auroc"]]

    # B: paraphrase-disjoint pairs (re-selected with the archived selector)
    lex = _qwen_lexicon()
    lex_leading = {x["decoded_str"] for x in lex["refusal_onset"]}
    par = AX.select_paraphrase_pairs(sm.tok, lex_leading, n_want=8)
    out["B_paraphrase"] = AX.fit_contrast_axis(
        sm, splits["fit_benign"], splits["held_benign"], render,
        par["refusal"], par["comply"], L)
    out["_paraphrase_pairs"] = {"refusal": par["refusal"], "comply": par["comply"],
                                "n_pairs_kept": par["n_pairs_kept"]}

    # C: formal vs casual register
    out["C_stylistic"] = AX.fit_contrast_axis(
        sm, splits["fit_benign"], splits["held_benign"], render,
        AX.FORMAL_RESPONSES, AX.CASUAL_RESPONSES, L)

    # E: harmful-vs-benign last-prompt-token axis
    contrast = _contrast_splits()
    out["E_prompt_contrast"] = _fit_prompt_axis(
        sm, contrast["harmful"], contrast["benign"], render, L, DIR)

    # D: matched random directions with the archived seeds
    n_rand = 3 if meta["scale"] == "0p6" else 1
    for i in range(n_rand):
        out[f"D_random{i}"] = AX.random_axis(sm.d_model, seed=9000 + i)
    return out


def _fit_prompt_axis(sm, harmful, benign, render, layer, DIR) -> dict:
    """Verbatim copy of EXP1 method.fit_prompt_axis (axis E)."""
    sm.state.enabled = False
    nf = len(harmful) // 2
    h = DIR._states(sm, harmful, render, n_pos=1)[:, 0, layer, :]
    b = DIR._states(sm, benign, render, n_pos=1)[:, 0, layer, :]
    sm.state.enabled = True
    d = h[:nf].mean(0) - b[:nf].mean(0)
    raw = float(np.linalg.norm(d))
    u = (d / (raw + 1e-12)).astype(np.float32)
    p, q = h[nf:] @ u, b[nf:] @ u
    pooled = float(np.sqrt(0.5 * (p.var(ddof=1) + q.var(ddof=1))) + 1e-12)
    return {"direction": u, "raw_norm": raw, "heldout_auroc": float(DIR.auroc(p, q)),
            "cohens_d": float((p.mean() - q.mean()) / pooled)}


_BLOCKS_CACHE: dict | None = None


def _blocks() -> dict:
    global _BLOCKS_CACHE
    if _BLOCKS_CACHE is None:
        doc = EL.load_json(EL.DATASET)
        out: dict[str, list] = {}
        for ds in doc["datasets"]:
            for row in ds["examples"]:
                out.setdefault(row["metadata_fold"], []).append(row)
        _BLOCKS_CACHE = out
    return _BLOCKS_CACHE


def _contrast_splits(n_each: int = 48) -> dict:
    rows = sorted(_blocks()["layer_contrast"], key=lambda r: r["metadata_uid"])
    harmful = [r["input"] for r in rows if r["metadata_meta"]["polarity"] == "harmful"]
    benign = [r["input"] for r in rows if r["metadata_meta"]["polarity"] != "harmful"]
    n = min(n_each, len(harmful), len(benign))
    return {"harmful": harmful[:n], "benign": benign[:n], "n_each": n}


def _qwen_lexicon() -> dict:
    for r in _blocks()["refusal_token_lexicon"]:
        m = r["metadata_meta"]
        if m["tokenizer_family"].lower() == "qwen3":
            return m
    raise RuntimeError("no qwen3 row in refusal_token_lexicon")


def axis_reproduction_gate(key: str, axes: dict, meta: dict, AX) -> dict:
    """V2: re-derived raw_norm and pairwise cosines must match the archive."""
    checks, worst = [], 0.0
    for ax, rec in axes.items():
        if ax.startswith("_"):
            continue
        stored = meta["axes"].get(ax)
        if stored is None:
            continue
        rel = abs(rec["raw_norm"] - stored["raw_norm"]) / max(stored["raw_norm"], 1e-9)
        worst = max(worst, rel)
        checks.append({"axis": ax, "kind": "raw_norm", "rederived": rec["raw_norm"],
                       "stored": stored["raw_norm"], "rel_err": rel,
                       "passed": bool(rel < 1e-3)})
    for name, stored_cos in meta["axis_cosines"].items():
        k1, k2 = name[len("cos("):-1].split(",")
        if k1 not in axes or k2 not in axes:
            continue
        got = AX.cosine(axes[k1]["direction"], axes[k2]["direction"])
        err = abs(got - stored_cos)
        worst = max(worst, err)
        checks.append({"axis": name, "kind": "cosine", "rederived": float(got),
                       "stored": float(stored_cos), "abs_err": float(err),
                       "passed": bool(err < 1e-3)})
    return {"checkpoint": key, "n_checks": len(checks),
            "n_failed": sum(1 for c in checks if not c["passed"]),
            "worst_deviation": float(worst),
            "passed": all(c["passed"] for c in checks), "checks": checks}


# ===========================================================================
# Held-out item harvest
# ===========================================================================
def _prompt_lookup() -> dict:
    doc = EL.load_json(EL.EXP1 / "results/prompts.json")
    return {p["uid"]: p["text"] for p in doc["probe_prompts"]}


def _iter1_judge_index() -> dict:
    idx = {}
    p = EL.ITER1_GEN / "scored.jsonl"
    if p.exists():
        for r in EL.read_jsonl(p):
            lab = r.get("judge_repaired_label") or r.get("judge_label")
            idx[(r["member"], r["item_id"])] = lab
    return idx


def _exp2_judge_index() -> dict:
    idx = {}
    p = EL.EXP2 / "scored.jsonl"
    if p.exists():
        for r in EL.read_jsonl(p):
            idx[(r["member"], r["uid"], r.get("template", ""))] = r.get("judge_label")
    return idx


def _bench_judge_index() -> dict:
    """Semantic labels for EXP1 bench items, from results/judge.json."""
    idx = {}
    doc = EL.load_json(EL.EXP1 / "results/judge.json")
    for it in doc.get("bench_items", []) or []:
        if it.get("judge_label"):
            idx[(it["model"], it["uid"])] = it["judge_label"]
    return idx


def exp1_steered_judge_index() -> dict:
    """Already-paid semantic labels for EXP1 STEERED items (432 rows).

    Key: (model, prompt_uid, seed, round(alpha, 4)).
    """
    idx = {}
    doc = EL.load_json(EL.EXP1 / "results/judge.json")
    for it in doc.get("items", []) or []:
        if it.get("judge_label"):
            idx[(it["model"], it["prompt_uid"], int(it["seed"]),
                 round(float(it["alpha"]), 4))] = it["judge_label"]
    return idx


def banned_ids(tok):
    """Verbatim copy of EXP1 method.banned_ids (avoids importing method.py)."""
    import torch
    ids: set[int] = set()
    for t in (tok.eos_token_id, tok.pad_token_id):
        if isinstance(t, int):
            ids.add(t)
        elif isinstance(t, list):
            ids.update(int(x) for x in t)
    for s in ("<|im_end|>", "<|endoftext|>", "<|im_start|>", "<think>", "</think>"):
        try:
            i = tok.convert_tokens_to_ids(s)
            if isinstance(i, int) and i >= 0:
                ids.add(i)
        except Exception:  # noqa: BLE001
            pass
    return torch.tensor(sorted(ids), dtype=torch.long)


def harvest_items(key: str, CL) -> tuple[list[dict], dict]:
    """Build the AB-blind held-out pool.  Returns (items, accounting)."""
    plook = _prompt_lookup()
    acc = {"scanned": 0, "kept": 0, "excl_nonfluent": 0, "excl_short": 0,
           "excl_degenerate": 0, "excl_axis_fit_overlap": 0, "excl_dup": 0,
           "by_source": {}}
    items: list[dict] = []
    seen: set[tuple] = set()

    def add(rec):
        acc["scanned"] += 1
        text = (rec.get("text") or "").strip()
        if not text:
            acc["excl_short"] += 1
            return
        if len(EL.word_tokens(text)) < 4 or len(text) < 20:
            acc["excl_short"] += 1
            return
        if rec.get("fluent") is False:
            acc["excl_nonfluent"] += 1
            return
        if rec.get("judge_label") == "DEGENERATE":
            acc["excl_degenerate"] += 1
            return
        k = (rec["prompt"], text)
        if k in seen:
            acc["excl_dup"] += 1
            return
        seen.add(k)
        rec["regex_refusal"] = bool(CL.REFUSAL_RE.match(text))
        rec["text"] = text
        items.append(rec)
        acc["kept"] += 1
        acc["by_source"][rec["source"]] = acc["by_source"].get(rec["source"], 0) + 1

    # -- S1: EXP1 unsteered benchmark generations ---------------------------
    bj = _bench_judge_index()
    for r in EL.read_jsonl(EL.EXP1 / f"gens/bench_{key}.jsonl"):
        add({"source": "exp1_bench", "stratum": f"bench::{r['block']}",
             "cluster": r["uid"], "prompt": r["user_text"],
             "prefill": r.get("prefill", ""), "text": r.get("text", ""),
             "fluent": r.get("fluent"), "alpha": 0.0, "axis": None,
             "judge_label": bj.get((key, r["uid"])),
             "archive_refused": bool(r.get("refused"))})

    # -- S2: EXP1 steered generations, AB-blind (axes C/D/E) or alpha <= 0.10 -
    for f in sorted((EL.EXP1 / "gens").glob(f"{key}__*.jsonl")):
        axis = f.name.split("__")[1][:-len(".jsonl")]
        blind = axis not in EL.AB
        for r in EL.read_jsonl(f):
            alpha = float(r["alpha"])
            if not (blind or alpha <= 0.10):
                continue
            if r.get("n_tokens", 0) < MIN_COMPLETION_TOKENS:
                continue
            add({"source": "exp1_steered_blind" if blind else "exp1_steered_lowalpha",
                 "stratum": f"{axis}@{alpha:.2f}", "cluster": r["prompt_uid"],
                 "prompt": plook[r["prompt_uid"]], "prefill": "",
                 "text": r.get("text", ""), "fluent": r.get("fluent"),
                 "alpha": alpha, "axis": axis, "judge_label": None,
                 "archive_refused": bool(r["refused"]),
                 "r_t_first": r.get("r_t_first")})

    # -- S3: iteration-1 behavioural archive (0.6B lineage only) -------------
    inv = {v: k for k, v in EL.ITER1_MEMBER_MAP.items()}
    if key in inv:
        jidx = _iter1_judge_index()
        m1 = inv[key]
        for r in EL.read_jsonl(EL.ITER1_GEN / "generations.jsonl"):
            if r["member"] != m1:
                continue
            add({"source": "iter1_archive", "stratum": f"iter1::{r['block']}",
                 "cluster": r["item_id"], "prompt": r["prompt"],
                 "prefill": r.get("prefill") or "", "text": r.get("completion", ""),
                 "fluent": None, "alpha": 0.0, "axis": None,
                 "judge_label": jidx.get((m1, r["item_id"])),
                 "archive_refused": None})

    # -- S4: EXP2 breadth-panel behavioural generations ----------------------
    inv2 = {v: k for k, v in EL.EXP2_MEMBER_MAP.items()}
    if key in inv2:
        j2 = _exp2_judge_index()
        m2 = inv2[key]
        for f in sorted((EL.EXP2 / "gens").glob(f"behaviour_{m2}.jsonl")):
            for r in EL.read_jsonl(f):
                add({"source": "exp2_behaviour", "stratum": f"exp2::{r['block']}",
                     "cluster": r["uid"], "prompt": r["prompt"], "prefill": "",
                     "text": r.get("completion", ""), "fluent": None,
                     "alpha": 0.0, "axis": None,
                     "judge_label": j2.get((m2, r["uid"], r.get("template", ""))),
                     "archive_refused": None})

    for i, it in enumerate(items):
        it["item_id"] = f"{key}#{i:05d}"
    return items, acc


AXIS_FIT_STRINGS_CACHE: set[str] | None = None


def axis_fit_strings(axes: dict, AX, DIR) -> set[str]:
    """Every response string any axis was fitted on (the leakage reference set)."""
    s = set(DIR.REFUSAL_RESPONSES) | set(DIR.COMPLY_RESPONSES)
    s |= set(AX.CANNED_REFUSAL) | set(AX.CANNED_COMPLY)
    s |= set(AX.FORMAL_RESPONSES) | set(AX.CASUAL_RESPONSES)
    pp = axes.get("_paraphrase_pairs", {})
    s |= set(pp.get("refusal", [])) | set(pp.get("comply", []))
    for a, b in AX.PARAPHRASE_PAIRS:
        s.add(a)
        s.add(b)
    return {x.strip() for x in s}


def leakage_gate(items: list[dict], fit_strings: set[str]) -> dict:
    """V1: no held-out item text may be an axis fit string (exact match)."""
    hits = [it["item_id"] for it in items if it["text"].strip() in fit_strings]
    # also assert no held-out PROMPT is an axis fit prompt (the benign fit split)
    doc = EL.load_json(EL.EXP1 / "results/prompts.json")
    fitp = set(doc["axis_fit_prompts"]) | set(doc["axis_held_prompts"])
    pr_hits = [it["item_id"] for it in items if it["prompt"].strip() in fitp]
    return {"n_items": len(items), "n_text_overlap": len(hits),
            "n_prompt_overlap": len(pr_hits),
            "passed": len(hits) == 0,
            "note": ("axis fit responses are 8-16 fixed strings appended to 12 benign "
                     "fit prompts; the held-out pool is model-generated text on "
                     "different prompts"),
            "prompt_overlap_ids": pr_hits[:10]}


# ===========================================================================
# Re-encode + projection
# ===========================================================================
def balanced_subsample(items: list[dict], cap: int, seed: int = 7) -> list[dict]:
    """Keep every refusal-labelled item; subsample compliances to balance."""
    rng = np.random.default_rng(seed)

    def is_ref(it):
        lab = it.get("judge_label")
        if lab in ("REFUSAL", "COMPLIANCE", "PARTIAL"):
            return lab == "REFUSAL" or it["regex_refusal"]
        return it["regex_refusal"]

    ref_ids = {it["item_id"] for it in items if is_ref(it)}
    refs = [it for it in items if it["item_id"] in ref_ids]
    rest = [it for it in items if it["item_id"] not in ref_ids]
    n_rest = max(0, cap - len(refs))
    if len(rest) > n_rest:
        # stratified over source so no single source dominates the compliance class
        by_src: dict[str, list] = {}
        for it in rest:
            by_src.setdefault(it["source"], []).append(it)
        per = max(1, n_rest // max(1, len(by_src)))
        keep = []
        for src, lst in sorted(by_src.items()):
            idx = rng.permutation(len(lst))[:per]
            keep += [lst[i] for i in idx]
        rest = keep[:n_rest]
    out = refs[:cap] + rest
    return out


def encode_items(sm, render, items: list[dict], L: int, clf, ban) -> dict:
    """Forward pass over rendered prompt + logged completion; residual state at L."""
    import torch
    n = len(items)
    first = np.zeros((n, sm.d_model), dtype=np.float32)
    meanp = np.zeros((n, sm.d_model), dtype=np.float32)
    ok = np.zeros(n, dtype=bool)
    rt_re = np.full(n, np.nan, dtype=np.float32)
    n_merged = 0
    sm.state.enabled = False
    t0 = time.time()
    with torch.no_grad():
        for i, it in enumerate(items):
            pre = render(it["prompt"]) + (it.get("prefill") or "")
            ids_pre = sm.tok(pre, add_special_tokens=False).input_ids
            n_pre = len(ids_pre)
            # Concatenate TOKEN IDS, not strings: string concatenation lets BPE merge
            # the last prompt token with the first completion token on some items,
            # which silently shifts the boundary (measured: it moved the re-encoded
            # r_t by up to 3.3 nats on the plain-rendered base checkpoints).
            ids_gen = sm.tok(it["text"], add_special_tokens=False).input_ids
            if len(ids_gen) < 2:
                continue
            n_merged += int(sm.tok(pre + it["text"],
                                   add_special_tokens=False).input_ids[:n_pre] != ids_pre)
            ids = torch.tensor([ids_pre + ids_gen], dtype=torch.long, device=sm.device)
            o = sm.model(input_ids=ids, use_cache=False, output_hidden_states=True)
            hs = o.hidden_states[L + 1][0].float()          # (T, d)
            first[i] = hs[n_pre].cpu().numpy()
            meanp[i] = hs[n_pre:].mean(0).cpu().numpy()
            ok[i] = True
            if it["source"] == "exp1_steered_lowalpha" and it.get("alpha") == 0.0:
                lg = o.logits[0, n_pre - 1, :].float()
                if ban is not None and ban.numel():
                    lg[ban.to(lg.device)] = float("-inf")
                rt_re[i] = float(clf.r_t(lg.unsqueeze(0)))
            del o, hs
            if (i + 1) % 200 == 0:
                logger.info(f"  encoded {i + 1}/{n} ({time.time() - t0:.0f}s)")
    sm.state.enabled = True
    gc.collect()
    logger.info(f"  boundary-merge items avoided by id-concat: {n_merged}/{n}")
    return {"first": first, "mean": meanp, "ok": ok, "rt_reencoded": rt_re,
            "n_boundary_merge_avoided": int(n_merged)}


def run_checkpoint(key: str, args) -> dict:
    import torch
    AX, CL, DIR, MD = EL.import_exp1_modules()
    meta = EL.model_meta(key)
    cfg = EL.MODEL_CFG[key]
    logger.info(f"=== {key} :: {cfg['repo']} @ {meta['revision_sha'][:12]} L={meta['L']}")

    sm = _load(MD, cfg["repo"], meta["revision_sha"])
    render = EL.make_render(sm.tok, cfg["render"])

    t0 = time.time()
    axes = rederive_axes(key, sm, render, meta, AX, DIR)
    # F1 diagnostic, decided in advance: re-derive a SECOND time on the same GPU to
    # measure bf16 run-to-run nondeterminism, so the reproduction tolerance can be
    # read against the floor the hardware actually supports.
    axes2 = rederive_axes(key, sm, render, meta, AX, DIR)
    determinism = {}
    for ax in axes:
        if ax.startswith("_"):
            continue
        rel = abs(axes[ax]["raw_norm"] - axes2[ax]["raw_norm"]) / \
            max(axes[ax]["raw_norm"], 1e-9)
        determinism[ax] = {
            "rel_norm_delta_between_two_rederivations": float(rel),
            "cosine_between_two_rederivations":
                float(AX.cosine(axes[ax]["direction"], axes2[ax]["direction"])),
        }
    del axes2
    gate = axis_reproduction_gate(key, axes, meta, AX)
    gate["self_determinism"] = determinism
    gate["max_self_rel_delta"] = float(max(
        v["rel_norm_delta_between_two_rederivations"] for v in determinism.values()))
    logger.info(f"[{key}] V2 axis reproduction: passed={gate['passed']} "
                f"worst={gate['worst_deviation']:.2e} ({time.time() - t0:.0f}s)")

    adir = EL.RESULTS / "axes"
    adir.mkdir(parents=True, exist_ok=True)
    for ax, rec in axes.items():
        if not ax.startswith("_"):
            np.save(adir / f"{key}_{ax}.npy", rec["direction"].astype(np.float32))

    # cross-check against EXP2's independently-fitted canned axis, where present
    x2 = None
    inv2 = {v: k for k, v in EL.EXP2_MEMBER_MAP.items()}
    p2 = EL.EXP2 / f"results/axis_{inv2.get(key, 'none')}.npz"
    if p2.exists():
        z = np.load(p2)
        if z["v_resp"].shape[1] == sm.d_model:
            x2 = float(AX.cosine(axes["A_canned"]["direction"],
                                 z["v_resp"][int(meta["L"])].astype(np.float32)))

    items, acc = harvest_items(key, CL)
    fitset = axis_fit_strings(axes, AX, DIR)
    leak = leakage_gate(items, fitset)
    items = [it for it in items if it["text"].strip() not in fitset]
    items = balanced_subsample(items, args.max_items)
    logger.info(f"[{key}] harvested {acc['kept']} -> encoding {len(items)}")

    ts = CL.build_token_sets(sm.tok, meta.get("continuation_extra_ids"))
    clf = CL.RefusalClassifier(sm.tok, ts)
    ban = banned_ids(sm.tok)

    enc = encode_items(sm, render, items, int(meta["L"]), clf, ban)
    keep = enc["ok"]
    items = [it for it, k in zip(items, keep) if k]
    proj = {}
    for ax, rec in axes.items():
        if ax.startswith("_"):
            continue
        u = rec["direction"].astype(np.float32)
        proj[f"{ax}|first"] = (enc["first"][keep] @ u).astype(np.float32)
        proj[f"{ax}|mean"] = (enc["mean"][keep] @ u).astype(np.float32)

    npz = EL.RESULTS / "proj"
    npz.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npz / f"{key}.npz", rt_reencoded=enc["rt_reencoded"][keep],
                        **proj)
    (npz / f"{key}_items.json").write_text(json.dumps(items))

    out = {
        "checkpoint": key, "repo": cfg["repo"], "revision_sha": meta["revision_sha"],
        "L": int(meta["L"]), "NORM_L": float(meta["NORM_L"]),
        "d_model": int(meta["d_model"]), "n_layers": int(meta["n_layers"]),
        "dtype": "bfloat16", "render": cfg["render"],
        "axis_reproduction": gate,
        "cos_A_vs_exp2_independent_fit": x2,
        "axis_raw_norms": {a: float(r["raw_norm"]) for a, r in axes.items()
                           if not a.startswith("_")},
        "axis_heldout_auroc_stored_style": {
            a: (float(r["heldout_auroc"]) if r.get("heldout_auroc") is not None else None)
            for a, r in axes.items() if not a.startswith("_")},
        "harvest": acc, "leakage_gate": leak,
        "n_encoded": int(keep.sum()),
        "n_boundary_merge_avoided_by_id_concat": enc["n_boundary_merge_avoided"],
    }
    (EL.RESULTS / f"encode_{key}.json").write_text(json.dumps(out, indent=1))
    sm.close()
    del sm
    gc.collect()
    torch.cuda.empty_cache()
    return out


def _load(MD, repo: str, revision: str):
    """Load pinned to revision_sha in the archive's dtype (bf16)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    class SM(MD.SteeredModel):
        def __init__(self, model_id, rev):
            self.model_id = model_id
            self.device = "cuda"
            self.tok = AutoTokenizer.from_pretrained(model_id, revision=rev)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, revision=rev, dtype=torch.bfloat16, device_map=None).to("cuda")
            self.model.eval()
            self.model.requires_grad_(False)
            self.n_layers = self.model.config.num_hidden_layers
            self.d_model = self.model.config.hidden_size
            self.state = MD.SteerState(
                alpha=torch.zeros(1, dtype=torch.float32, device="cuda"))
            self._handle = None
            self._hooked_layer = None

    return SM(repo, revision)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoints", default="instruct_0p6")
    ap.add_argument("--max-items", type=int, default=MAX_ITEMS_PER_CKPT)
    args = ap.parse_args()
    keys = EL.CHECKPOINTS if args.checkpoints == "all" else args.checkpoints.split(",")
    EL.RESULTS.mkdir(exist_ok=True)
    for k in keys:
        t0 = time.time()
        try:
            run_checkpoint(k, args)
            logger.info(f"[{k}] done in {time.time() - t0:.0f}s")
        except Exception:
            logger.exception(f"[{k}] FAILED")
            raise


if __name__ == "__main__":
    main()
