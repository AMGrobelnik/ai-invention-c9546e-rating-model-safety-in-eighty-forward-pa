#!/usr/bin/env python3
"""Per-member GPU work: axis fitting (S3), detection (S4), induction (S5).

Each member is loaded once, measured in BOTH roles of the same five axes, then
released.  ``detect_<key>.json`` and ``induce_<key>.json`` are written
atomically per member, so an interrupted run yields a complete subset rather
than a half-measured member.
"""

from __future__ import annotations

import gc
import json
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

import explib as EX
from lib import classify as CL
from lib import direction as DIR
from lib import dose as DOSE
from lib import models as MD
from lib.gen import steered_generate

DTYPE = torch.bfloat16
ENCODE_BATCH = 16
GEN_BATCH = 32
IND_BATCH = 78          # (prompt, contrast-level) rows decoded together


# ==========================================================================
# Loading
# ==========================================================================
def load_member(rec: dict):
    """Revision-pinned load in the archive's dtype."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    repo, rev = rec["repo"], rec.get("revision") or None

    class SM(MD.SteeredModel):
        def __init__(self):
            self.model_id = repo
            self.device = "cuda"
            kw = {"revision": rev} if rev else {}
            self.tok = AutoTokenizer.from_pretrained(repo, **kw)
            if self.tok.pad_token is None:
                self.tok.pad_token = self.tok.eos_token
            self.tok.padding_side = "left"
            self.model = AutoModelForCausalLM.from_pretrained(
                repo, dtype=DTYPE, device_map=None, **kw).to("cuda")
            self.model.eval()
            self.model.requires_grad_(False)
            self.n_layers = self.model.config.num_hidden_layers
            self.d_model = self.model.config.hidden_size
            self.state = MD.SteerState(
                alpha=torch.zeros(1, dtype=torch.float32, device="cuda"))
            self._handle = None
            self._hooked_layer = None

    return SM()


def layer_for(n_layers: int) -> int:
    """Pre-registered P2: L = round(0.25 * n_layers), clipped to [1, n_layers-1]."""
    return int(min(max(1, round(EX.LAYER_DEPTH * n_layers)), n_layers - 1))


# ==========================================================================
# S3 -- axes
# ==========================================================================
@torch.no_grad()
def _prompt_states(sm, texts, render, layer: int) -> np.ndarray:
    """Post-block residual at the LAST prompt token, layer `layer` -> (n, d)."""
    out = np.zeros((len(texts), sm.d_model), dtype=np.float32)
    for i, t in enumerate(texts):
        ids = sm.tok(render(t), return_tensors="pt",
                     add_special_tokens=False).input_ids.to(sm.device)
        o = sm.model(input_ids=ids, use_cache=False, output_hidden_states=True)
        out[i] = o.hidden_states[layer + 1][0, -1, :].float().cpu().numpy()
        del o
    return out


def fit_prompt_axis(sm, harmful, benign, render, layer: int) -> dict:
    """Axis E: harmful-vs-benign PROMPT contrast at the last prompt token."""
    sm.state.enabled = False
    nf = len(harmful) // 2
    h = _prompt_states(sm, harmful, render, layer)
    b = _prompt_states(sm, benign, render, layer)
    sm.state.enabled = True
    d = h[:nf].mean(0) - b[:nf].mean(0)
    raw = float(np.linalg.norm(d))
    u = (d / (raw + 1e-12)).astype(np.float32)
    p, q = h[nf:] @ u, b[nf:] @ u
    return {"direction": u, "raw_norm": raw, "heldout_auroc": EX.auroc(p, q),
            "cohens_d": EX.cohens_d(p, q)}


def build_axes(sm, render, layer: int) -> dict:
    """A/B/C/D/E at layer `layer`, all through the archived primitives."""
    sp = EX.axis_prompt_splits()
    fit, held = sp["fit"], sp["held"]
    out: dict[str, dict] = {}

    for name, pos, neg in (
        ("A_canned", DIR.REFUSAL_RESPONSES, DIR.COMPLY_RESPONSES),
        ("B_paraphrase", DIR.PARA_REFUSAL, DIR.PARA_COMPLY),
        ("C_stylistic", DIR.STYLE_FORMAL, DIR.STYLE_CASUAL),
    ):
        prof = DIR.fit_contrast_axis(sm, fit, held, render, pos, neg)
        out[name] = {"direction": prof["directions"][layer].astype(np.float32),
                     "raw_norm": float(prof["diff_norms"][layer]),
                     "heldout_auroc": float(prof["auroc"][layer]),
                     "cohens_d": float(prof["dprime"][layer])}
        if name == "A_canned":
            out["_norm_profile"] = [float(x) for x in prof["diff_norms"]]
            out["_auroc_profile"] = [float(x) for x in prof["auroc"]]
        del prof
        gc.collect()

    cs = EX.contrast_splits()
    out["E_prompt_contrast"] = fit_prompt_axis(sm, cs["harmful"], cs["benign"],
                                               render, layer)

    # D is the NORM-MATCHED random null: the direction is a unit random vector, and
    # its "contrast magnitude" is set to axis A's, so at any shared contrast level c
    # the injected vector alpha*NORM_L*d_hat has EXACTLY the same norm as A's. That
    # is what makes D a fair null for the magnitude-collapse rival: if a random
    # direction at A's own injected magnitude does not induce refusal, magnitude
    # alone is not what makes A work. (lib.direction.random_axis returns a unit
    # vector, so its own norm carries no contrast information.)
    rnd = DIR.random_axis(sm.d_model, sm.n_layers, seed=0)
    out["D_random0"] = {"direction": rnd[layer].astype(np.float32),
                        "raw_norm": float(out["A_canned"]["raw_norm"]),
                        "raw_norm_is_matched_to": "A_canned",
                        "unit_vector_norm": float(np.linalg.norm(rnd[layer])),
                        "heldout_auroc": None, "cohens_d": None}
    return out


# ==========================================================================
# S4 -- detection
# ==========================================================================
@torch.no_grad()
def generate_own_text(sm, render, prompts: list[dict], seeds: tuple,
                      max_new_tokens: int = 64) -> list[dict]:
    """Batched generation of the model's OWN text; ids are logged at gen time."""
    gens: list[dict] = []
    pad = sm.tok.pad_token_id if sm.tok.pad_token_id is not None else sm.tok.eos_token_id
    sm.tok.padding_side = "left"
    for seed in seeds:
        greedy = seed is None
        if not greedy:
            torch.manual_seed(int(seed))
        bs = GEN_BATCH
        i = 0
        while i < len(prompts):
            chunk = prompts[i:i + bs]
            texts = [render(p["text"]) for p in chunk]
            try:
                enc = sm.tok(texts, return_tensors="pt", padding=True,
                             add_special_tokens=False)
                enc = {k: v.to(sm.device) for k, v in enc.items()}
                out = sm.model.generate(
                    **enc, max_new_tokens=max_new_tokens,
                    do_sample=not greedy,
                    temperature=None if greedy else 0.7,
                    top_p=None if greedy else 1.0,
                    top_k=None if greedy else 0,
                    pad_token_id=pad)
            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                if bs <= 4:
                    raise
                bs = max(4, bs // 2)
                logger.warning(f"  OOM during generation -> batch {bs}")
                continue
            new = out[:, enc["input_ids"].shape[1]:]
            for p, row in zip(chunk, new):
                ids = [int(t) for t in row.tolist() if int(t) != pad]
                # trim at eos
                if sm.tok.eos_token_id is not None:
                    eos = int(sm.tok.eos_token_id)
                    if eos in ids:
                        ids = ids[:ids.index(eos)]
                gens.append({"uid": p["uid"], "stratum": p["stratum"],
                             "prompt": p["text"],
                             "seed": "greedy" if greedy else int(seed),
                             "gen_ids": ids,
                             "text": sm.tok.decode(ids, skip_special_tokens=True)})
            del out, enc, new
            i += bs
        EX.free_cuda()
    return gens


def exclusion_cascade(gens: list[dict]) -> tuple[list[dict], dict]:
    """The archived cascade, with FULL accounting reported at every rung."""
    acc = {"scanned": len(gens), "excl_dup": 0, "excl_nonfluent": 0,
           "excl_short": 0, "excl_degenerate": 0, "kept": 0}
    seen: set[tuple] = set()
    kept: list[dict] = []
    for g in gens:
        text = (g["text"] or "").strip()
        k = (g["prompt"], text)
        if k in seen:
            acc["excl_dup"] += 1
            continue
        seen.add(k)
        if len(g["gen_ids"]) < 8 or len(text) < 20:
            acc["excl_short"] += 1
            continue
        if not CL.fluency_ok(g["gen_ids"]):
            acc["excl_nonfluent"] += 1
            continue
        if CL.distinct_n(g["gen_ids"], 3) < 0.5:
            acc["excl_degenerate"] += 1
            continue
        g["text"] = text
        g["regex_refusal"] = bool(CL.REFUSAL_RE.match(text))
        kept.append(g)
    acc["kept"] = len(kept)
    return kept, acc


def balance_classes(items: list[dict], seed: int = 7) -> tuple[list[dict], dict]:
    """Subsample the majority class so AUROC is not read off a 95/5 split."""
    rng = np.random.default_rng(seed)
    ref = [it for it in items if it["regex_refusal"]]
    com = [it for it in items if not it["regex_refusal"]]
    info = {"n_refusal_pre": len(ref), "n_compliance_pre": len(com)}
    n = min(len(ref), len(com))
    if n == 0:
        info.update({"n_refusal": len(ref), "n_compliance": len(com),
                     "balanced": False})
        return items, info
    if len(ref) > n:
        ref = [ref[i] for i in rng.permutation(len(ref))[:n]]
    if len(com) > n:
        com = [com[i] for i in rng.permutation(len(com))[:n]]
    info.update({"n_refusal": len(ref), "n_compliance": len(com), "balanced": True})
    return ref + com, info


@torch.no_grad()
def encode_items(sm, render, items: list[dict], layer: int) -> tuple[np.ndarray, np.ndarray, dict]:
    """Re-encode prompt+completion by TOKEN-ID CONCATENATION and read layer L.

    The archived bug this guards against: building the scored sequence by STRING
    concatenation lets BPE merge the last prompt token with the first completion
    token, silently shifting the boundary (it corrupted up to 450/1028 archived
    items).  Concatenating ids is exact by construction; the number of items on
    which the two paths would have differed is counted and reported.
    """
    n = len(items)
    reps = np.zeros((n, sm.d_model), dtype=np.float32)
    ok = np.zeros(n, dtype=bool)
    n_merge_avoided = 0
    sm.state.enabled = False
    sm.remove_hook()
    pad = sm.tok.pad_token_id if sm.tok.pad_token_id is not None else 0
    t0 = time.time()
    bs = ENCODE_BATCH
    i = 0
    while i < n:
        chunk = items[i:i + bs]
        seqs, npres = [], []
        for it in chunk:
            pre = render(it["prompt"])
            ids_pre = sm.tok(pre, add_special_tokens=False).input_ids
            ids_gen = list(it["gen_ids"])
            joint = sm.tok(pre + it["text"], add_special_tokens=False).input_ids
            n_merge_avoided += int(joint[:len(ids_pre)] != list(ids_pre))
            seqs.append(list(ids_pre) + ids_gen)
            npres.append(len(ids_pre))
        maxlen = max(len(s) for s in seqs)
        # RIGHT padding so position n_pre is the first generated token in every row
        inp = torch.full((len(seqs), maxlen), pad, dtype=torch.long)
        att = torch.zeros((len(seqs), maxlen), dtype=torch.long)
        for r, s in enumerate(seqs):
            inp[r, :len(s)] = torch.tensor(s, dtype=torch.long)
            att[r, :len(s)] = 1
        try:
            o = sm.model(input_ids=inp.to(sm.device), attention_mask=att.to(sm.device),
                         use_cache=False, output_hidden_states=True)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if bs <= 1:
                raise
            bs = max(1, bs // 2)
            logger.warning(f"  OOM during encode -> batch {bs}")
            continue
        hs = o.hidden_states[layer + 1].float()
        for r, np_pre in enumerate(npres):
            reps[i + r] = hs[r, np_pre, :].cpu().numpy()
            ok[i + r] = True
        del o, hs
        i += bs
        if i % 320 == 0:
            logger.info(f"  encoded {i}/{n} ({time.time() - t0:.0f}s)")
    sm.state.enabled = True
    EX.free_cuda()
    return reps, ok, {"n_boundary_merge_avoided_by_id_concat": int(n_merge_avoided),
                      "encode_seconds": time.time() - t0,
                      "encode_batch_final": bs}


def run_detection(sm, render, layer: int, axes: dict, key: str,
                  seeds=(None, 1, 2, 3, 4), extra_seeds=(5, 6, 7, 8)) -> dict:
    """S4 end to end.  Escalates seeds/prompts if a class is under-powered."""
    prompts = EX.detection_prompts()
    core_uids = {p["uid"] for p in prompts if p["stratum"] == "harmful"}
    logger.info(f"[{key}] generating own text on {len(prompts)} prompts x {len(seeds)} seeds")
    gens = generate_own_text(sm, render, prompts, seeds)
    kept, acc = exclusion_cascade(gens)
    escalation = []

    def counts(lst):
        r = sum(1 for x in lst if x["regex_refusal"])
        return r, len(lst) - r

    n_ref, n_com = counts(kept)
    # rung 1: more sampled seeds on the harmful core only
    if min(n_ref, n_com) < EX.MIN_PER_CLASS:
        escalation.append("rung1_extra_seeds_on_harmful_core")
        harmful = [p for p in prompts if p["stratum"] == "harmful"]
        more = generate_own_text(sm, render, harmful, extra_seeds)
        gens += more
        kept, acc = exclusion_cascade(gens)
        n_ref, n_com = counts(kept)
    # rung 2: the plain_harmful rows beyond the core-80
    if min(n_ref, n_com) < EX.MIN_PER_CLASS:
        escalation.append("rung2_extra_harmful_prompts")
        extra = EX.extra_harmful_prompts(core_uids)[:200]
        more = generate_own_text(sm, render, extra, (None, 1))
        gens += more
        kept, acc = exclusion_cascade(gens)
        n_ref, n_com = counts(kept)

    powered = min(n_ref, n_com) >= EX.MIN_PER_CLASS
    if not powered:
        escalation.append("rung3_accept_UNPOWERED")

    items, bal = balance_classes(kept)
    # leakage assertion (T6a): no scored item text may be an axis fit string
    fitset = {s.strip() for s in (DIR.REFUSAL_RESPONSES + DIR.COMPLY_RESPONSES
                                  + DIR.PARA_REFUSAL + DIR.PARA_COMPLY
                                  + DIR.STYLE_FORMAL + DIR.STYLE_CASUAL)}
    # Leakage guard.  A scored item whose text IS an axis-fit string would let the
    # axis recognise its own training data, so such items are DROPPED and counted
    # rather than aborting the member: a model that happens to emit one of the
    # frozen strings verbatim is a curiosity about that model, not a broken run.
    # (Observed on reallexi/lexi-coder-v4.3, which reproduced 3 of them exactly.)
    leaked = [it for it in items if it["text"].strip() in fitset]
    n_leak = len(leaked)
    if n_leak:
        logger.warning(f"[{key}] dropping {n_leak} scored items that exactly match an "
                       f"axis-fit string")
        items = [it for it in items if it["text"].strip() not in fitset]
    fitp = set(EX.axis_prompt_splits()["fit"]) | set(EX.axis_prompt_splits()["held"])
    n_pleak = sum(1 for it in items if it["prompt"].strip() in fitp)

    reps, ok, enc_info = encode_items(sm, render, items, layer)
    items = [it for it, k in zip(items, ok) if k]
    reps = reps[ok]

    resid_norm = np.linalg.norm(reps, axis=1).astype(np.float32)
    proj, proj_cos = {}, {}
    for ax, rec in axes.items():
        if ax.startswith("_"):
            continue
        u = rec["direction"].astype(np.float32)
        proj[ax] = (reps @ u).astype(np.float32)
        # AMENDMENT-1 readout: cosine with the axis, i.e. the projection divided by
        # the residual-stream norm.  A raw projection is ||h|| * cos(angle), so ANY
        # direction inherits a refusal-vs-compliance difference in ||h||; that is
        # what made the matched RANDOM axis D read at AUROC 0.171 on the first
        # member and tripped the pre-registered sanity gate.  Dividing by ||h||
        # removes the shared magnitude channel and leaves only direction.
        proj_cos[ax] = (proj[ax] / np.maximum(resid_norm, 1e-6)).astype(np.float32)

    labels = np.array([it["regex_refusal"] for it in items], bool)
    strata = np.array([it["stratum"] for it in items])
    clusters = np.array([it["uid"] for it in items])
    stats = EX.detection_stats(proj, labels, strata, clusters)
    stats_cos = EX.detection_stats(proj_cos, labels, strata, clusters)

    # EMPIRICAL RANDOM NULL.  A single random direction is not a null
    # distribution: residual streams are strongly anisotropic, so one draw can
    # overlap the refusal signal by chance far more than an isotropic estimate
    # suggests (observed: a lone random axis reading at AUROC 0.70).  Twenty
    # fresh unit directions are projected through the SAME pipeline, and the axis
    # verdicts are read against the resulting spread rather than against a bare
    # 0.50.  This costs twenty dot products and no extra forward passes.
    stats["random_null"] = EX.random_null_distribution(
        reps, labels, strata, n_draws=20, seed=EX.BOOT_SEED)
    # the magnitude channel on its own, as a named baseline
    nrm_lo, nrm_hi = EX.boot_ci([EX.auroc(resid_norm[idx][labels[idx]],
                                          resid_norm[idx][~labels[idx]])
                                 for idx in EX.cluster_boot_indices(
                                     clusters, EX.N_BOOT, EX.BOOT_SEED)])
    stats["residual_norm_baseline"] = {
        "auroc": EX.auroc(resid_norm[labels], resid_norm[~labels]),
        "auroc_ci95": [nrm_lo, nrm_hi],
        "note": "AUROC of the residual-stream NORM alone, no direction involved. "
                "Any raw projection inherits this channel."}

    np.savez_compressed(EX.RESULTS / f"proj_{key}.npz",
                        labels=labels, strata=strata, clusters=clusters,
                        resid_norm=resid_norm,
                        **{f"proj_{a}": v for a, v in proj.items()},
                        **{f"cos_{a}": v for a, v in proj_cos.items()})
    (EX.RESULTS / f"proj_{key}_items.json").write_text(json.dumps(
        [{k: v for k, v in it.items() if k != "gen_ids"} for it in items]))

    return {"checkpoint": key, "powered": bool(powered),
            "n_refusal_pre_balance": n_ref, "n_compliance_pre_balance": n_com,
            "exclusion_cascade": acc, "balance": bal,
            "escalation_ladder": escalation,
            "leakage": {"n_text_overlap_dropped": n_leak, "n_prompt_overlap": n_pleak,
                        "dropped_texts": [it["text"][:120] for it in leaked[:5]]},
            "encode": enc_info, "detection": stats,
            "detection_norm_controlled": stats_cos}


# ==========================================================================
# S5 -- induction at matched contrast
# ==========================================================================
def run_induction(sm, render, layer: int, axes: dict, norm_l: float, key: str,
                  axis_names: tuple, seeds=(0, 1, 2), n_prompts: int = 12,
                  max_new_tokens: int = 48) -> dict:
    """Steering sweep reported in axis-contrast units c = alpha*NORM_L/||d_raw||."""
    bp = EX.benign_steer_prompts(n_prompts)
    texts = [p["text"] for p in bp]
    ts = CL.build_token_sets(sm.tok)
    clf = CL.RefusalClassifier(sm.tok, ts)
    banned = None
    out: dict[str, dict] = {}

    saved_dir, saved_norm = sm.state.direction, sm.state.norm_l
    for ax in axis_names:
        rec = axes.get(ax)
        if rec is None:
            continue
        raw = float(rec["raw_norm"])
        grid: dict[str, dict] = {}
        sm.state.direction = torch.tensor(rec["direction"], dtype=torch.float32,
                                          device=sm.device)
        sm.state.norm_l = float(norm_l)
        sm.install_hook(layer)
        # The steering hook indexes alpha PER ROW, so an entire contrast grid can be
        # decoded in one batch: rows are (prompt, c) pairs carrying their own alpha.
        # This collapses 13 sequential decodes per seed into a handful of chunks and
        # is what makes a 5-axis sweep affordable on every member.
        live = [c for c in EX.C_GRID
                if EX.alpha_for_contrast(c, raw, norm_l) <= EX.ALPHA_CAP]
        for c in EX.C_GRID:
            a = EX.alpha_for_contrast(c, raw, norm_l)
            grid[str(c)] = {"c": float(c), "alpha": float(a),
                            "capped": bool(a > EX.ALPHA_CAP),
                            "per_rollout": {}, "rate": None, "fluent": None,
                            "_ref": [], "_flu": []}
        rows = [(p, c) for c in live for p in bp]
        for s in seeds:
            for i in range(0, len(rows), IND_BATCH):
                chunk = rows[i:i + IND_BATCH]
                bg = steered_generate(
                    sm, clf, [p["text"] for p, _ in chunk], render,
                    alpha=[EX.alpha_for_contrast(c, raw, norm_l) for _, c in chunk],
                    max_new_tokens=max_new_tokens, temperature=0.7, seed=int(s),
                    banned=banned, record_r=False, stop_on_eos=True)
                for (p, c), toks in zip(chunk, bg.tokens):
                    cell = grid[str(c)]
                    r = int(bool(clf.opens_with_refusal(toks)))
                    cell["per_rollout"][f"{p['uid']}|{s}"] = r
                    cell["_ref"].append(r)
                    cell["_flu"].append(float(CL.distinct_n(toks, 3)))
                del bg
        sm.remove_hook()
        for c in EX.C_GRID:
            cell = grid[str(c)]
            ref, flu = cell.pop("_ref"), cell.pop("_flu")
            if not ref:
                continue
            cell["rate"] = float(np.mean(ref))
            cell["fluent"] = float(np.mean([x >= 0.5 for x in flu]))
            cell["mean_distinct3"] = float(np.mean(flu))
            cell["wilson_ci95"] = list(EX.wilson(int(sum(ref)), len(ref)))
            cell["n"] = len(ref)

        cs = [float(c) for c in EX.C_GRID if not grid[str(c)]["capped"]]
        rates = [grid[str(c)]["rate"] for c in cs]
        c50 = DOSE.nonparametric_alpha50(cs, rates) if len(cs) >= 2 else None
        imax = int(np.argmax(rates)) if rates else 0
        fl_collapse = next((c for c in cs if grid[str(c)]["fluent"] is not None
                            and grid[str(c)]["fluent"] < 0.5), None)
        out[ax] = {
            "raw_norm": raw, "NORM_L": float(norm_l), "grid": grid,
            "c_grid_uncapped": cs,
            "n_capped": sum(1 for c in EX.C_GRID if grid[str(c)]["capped"]),
            "c_50": c50, "alpha_50": (EX.alpha_for_contrast(c50, raw, norm_l)
                                      if c50 is not None else None),
            "max_rate": float(max(rates)) if rates else None,
            "c_at_max_rate": float(cs[imax]) if rates else None,
            "inverted_U": bool(rates and imax < len(rates) - 1
                               and rates[-1] < max(rates) - 0.10),
            "fluency_collapse_c": fl_collapse,
            "induction_works": bool(c50 is not None),
        }
        EX.free_cuda()
    sm.state.direction, sm.state.norm_l = saved_dir, saved_norm

    res = {"checkpoint": key, "layer": layer, "NORM_L": float(norm_l), "axes": out}
    if all(a in out for a in EX.AB):
        res["matched_contrast"] = EX.matched_contrast_delta(
            {c: v for c, v in out[EX.AB[0]]["grid"].items()},
            {c: v for c, v in out[EX.AB[1]]["grid"].items()})
    return res


# ==========================================================================
# Axis reproduction gate (archived checkpoints only)
# ==========================================================================
# Only axes built from an IDENTICAL construction can be compared to the archive.
#   A_canned          lib/direction.REFUSAL_RESPONSES vs COMPLY_RESPONSES -- same
#   E_prompt_contrast harmful-vs-benign last prompt token -- same
#   B_paraphrase      archive used gen_art_experiment_1/axes.select_paraphrase_pairs
#                     (8 dynamically selected pairs); here lib/direction.PARA_REFUSAL
#                     / PARA_COMPLY (24 frozen hand-written pairs) -- DIFFERENT
#   C_stylistic       archive used axes.FORMAL_RESPONSES / CASUAL_RESPONSES;
#                     here lib/direction.STYLE_FORMAL / STYLE_CASUAL -- DIFFERENT
#   D_random0         archive seeded 9000+i; here seed 0 -- DIFFERENT BY DESIGN
# The artifact plan names the lib/direction sets, so those are what is used; the
# gate is restricted to the comparable axes and the rest are reported, not scored.
COMPARABLE_AXES = ("A_canned", "E_prompt_contrast")
INCOMPARABLE_REASON = {
    "B_paraphrase": "archive fitted 8 dynamically selected paraphrase pairs "
                    "(axes.select_paraphrase_pairs); this run uses the 24 frozen "
                    "lib/direction.PARA_REFUSAL pairs named by the artifact plan",
    "C_stylistic": "archive used axes.FORMAL_RESPONSES/CASUAL_RESPONSES; this run "
                   "uses lib/direction.STYLE_FORMAL/STYLE_CASUAL",
    "D_random0": "different random seed by design (archive 9000, here 0); a matched "
                 "random axis is a null control, not a quantity to reproduce",
}


def axis_reproduction(key_archived: str | None, axes: dict) -> dict:
    if not key_archived:
        return {"applicable": False}
    out = {"applicable": True, "archived_key": key_archived, "cosines": {},
           "gated_axes": list(COMPARABLE_AXES),
           "incomparable_axes": INCOMPARABLE_REASON}
    for ax, rec in axes.items():
        if ax.startswith("_"):
            continue
        p = EX.ARCH_EVAL / f"results/axes/{key_archived}_{ax}.npy"
        if not p.exists():
            continue
        stored = np.load(p).astype(np.float32)
        cos = EX.cosine(rec["direction"], stored)
        gated = ax in COMPARABLE_AXES
        out["cosines"][ax] = {
            "cosine": cos, "gated": gated,
            "passes_0p999": bool(abs(cos) >= 0.999) if gated else None,
            "stop_and_diagnose": bool(abs(cos) < 0.95) if gated else False,
            "reason_not_gated": None if gated else INCOMPARABLE_REASON.get(ax)}
    vals = [abs(v["cosine"]) for a, v in out["cosines"].items()
            if v["gated"] and np.isfinite(v["cosine"])]
    out["min_abs_cosine"] = float(min(vals)) if vals else None
    out["all_pass_0p999"] = bool(vals and min(vals) >= 0.999)
    # the raw-norm agreement is the sharper check and is dtype-robust
    out["raw_norm_vs_archive"] = {}
    mp = EX.ITER2_EXP1 / f"results/model_{key_archived}.json"
    if mp.exists():
        stored_axes = EX.load_json(mp).get("axes", {})
        for ax in axes:
            if ax.startswith("_") or ax not in stored_axes:
                continue
            s = float(stored_axes[ax]["raw_norm"])
            g = float(axes[ax]["raw_norm"])
            out["raw_norm_vs_archive"][ax] = {
                "rederived": g, "archived": s,
                "rel_err": abs(g - s) / max(s, 1e-9),
                "gated": ax in COMPARABLE_AXES}
    return out


# ==========================================================================
# One member, end to end
# ==========================================================================
def run_member(rec: dict, *, do_induction: bool = True, detection_only: bool = False,
               induction_axes: tuple = EX.AXES_ALL,
               det_seeds=(None, 1, 2, 3, 4)) -> dict:
    key = rec["key"]
    t0 = time.time()
    logger.info(f"=== {key} :: {rec['repo']} ({rec['params_b']:.2f}B, "
                f"{rec['member_class']}, prio {rec['priority']})")
    sm = load_member(rec)
    # Renderer by MEMBER CLASS, not by "does the tokenizer ship a template".
    # Qwen3-*-Base tokenizers DO ship a chat template even though the base model
    # was never instruction-tuned to follow one, so "auto" silently rendered the
    # base checkpoints in ChatML -- which is both wrong on its own terms and a
    # departure from the archive (iter_2 MODEL_CFG pins base -> "plain"). It cost
    # the axis-reproduction gate: axis E fell to cosine 0.09-0.13 on the two base
    # checkpoints while every chat member reproduced at 0.9999.
    mode = "generic" if rec.get("member_class") == "base" else "auto"
    render, render_mode = MD.make_renderer(sm.tok, mode)
    layer = layer_for(sm.n_layers)
    logger.info(f"[{key}] n_layers={sm.n_layers} L={layer} "
                f"(depth {layer / sm.n_layers:.3f}) d_model={sm.d_model} render={render_mode}")

    axes = build_axes(sm, render, layer)
    repro = axis_reproduction(rec.get("archived_key"), axes)
    if repro.get("applicable"):
        logger.info(f"[{key}] axis reproduction min|cos|={repro['min_abs_cosine']}")

    onset = EX.refusal_onset_ids(rec.get("tokenizer_family") or "")
    para_gate = DIR.paraphrase_overlap_check(sm.tok, onset)

    norms = DIR.median_norms_all_layers(sm, EX.axis_prompt_splits()["fit"], render)
    norm_l = float(norms[layer])
    logger.info(f"[{key}] NORM_L={norm_l:.3f} raw norms=" +
                ", ".join(f"{a}={axes[a]['raw_norm']:.2f}" for a in EX.AXES_ALL
                          if a in axes))

    meta = {"checkpoint": key, "repo": rec["repo"], "revision": rec.get("revision"),
            "member_class": rec["member_class"], "lineage_id": rec["lineage_id"],
            "params_b": rec["params_b"], "role": rec["role"],
            "priority": rec["priority"],
            "breadth_b_reaches_half": rec.get("breadth_b_reaches_half", False),
            "archived_key": rec.get("archived_key"),
            "n_layers": int(sm.n_layers), "d_model": int(sm.d_model),
            "L": layer, "relative_depth": layer / sm.n_layers,
            "NORM_L": norm_l, "dtype": "bfloat16", "render": render_mode,
            "axis_raw_norms": {a: float(r["raw_norm"]) for a, r in axes.items()
                               if not a.startswith("_")},
            "axis_fit_heldout_auroc": {a: r.get("heldout_auroc") for a, r in axes.items()
                                       if not a.startswith("_")},
            "axis_reproduction": repro,
            "paraphrase_disjointness_gate": para_gate,
            "norm_profile_A": axes.get("_norm_profile")}

    adir = EX.RESULTS / "axes"
    adir.mkdir(parents=True, exist_ok=True)
    for ax, r in axes.items():
        if not ax.startswith("_"):
            np.save(adir / f"{key}_{ax}.npy", r["direction"].astype(np.float32))

    det = run_detection(sm, render, layer, axes, key, seeds=det_seeds)
    det.update(meta)
    EX.atomic_write_json(EX.RESULTS / f"detect_{key}.json", det)
    logger.info(f"[{key}] detection powered={det['powered']} "
                f"A={det['detection']['axes']['A_canned']['auroc']:.3f} "
                f"{det['detection']['axes']['A_canned']['verdict']}")

    ind = None
    if do_induction and not detection_only:
        ind = run_induction(sm, render, layer, axes, norm_l, key,
                            axis_names=tuple(a for a in induction_axes if a in axes))
        ind.update({k: meta[k] for k in ("repo", "member_class", "lineage_id",
                                         "params_b", "role", "archived_key",
                                         "breadth_b_reaches_half", "params_b")})
        EX.atomic_write_json(EX.RESULTS / f"induce_{key}.json", ind)
        a = ind["axes"].get("A_canned", {})
        logger.info(f"[{key}] induction A: c_50={a.get('c_50')} "
                    f"max_rate={a.get('max_rate')}")

    sm.close()
    del sm, axes
    EX.free_cuda()
    secs = time.time() - t0
    logger.info(f"[{key}] done in {secs:.0f}s")
    return {"key": key, "seconds": secs, "detect": det, "induce": ind}
