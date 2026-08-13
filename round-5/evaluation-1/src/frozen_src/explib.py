#!/usr/bin/env python3
"""Shared primitives for the read-versus-act experiment.

Every outcome-defining code path (refusal regex, axis fitting, the steering
hook, the non-parametric alpha_50 interpolator) is IMPORTED from ``lib/``, which
is a byte-identical copy of the iteration-3 ``gen_art_experiment_1/lib``.  What
lives here is only the new plumbing: panel resolution off the frozen manifest,
the token-id-concatenation re-encoder, the stratum-centred detection statistics
and the axis-contrast-unit induction sweep.
"""

from __future__ import annotations

import gc
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
DATA = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
ARCH_EXP = ROOT / "iter_3/gen_art/gen_art_experiment_1"
ARCH_EVAL = ROOT / "iter_3/gen_art/gen_art_evaluation_1"
ITER2_EXP1 = ROOT / "iter_2/gen_art/gen_art_experiment_1"
RESULTS = HERE / "results"
FIGS = HERE / "figures"

# --------------------------------------------------------------------------
# Pre-registered constants (mirrored into results/prereg.json by method.py)
# --------------------------------------------------------------------------
CHANCE_BAND = (0.40, 0.60)
READS_THRESHOLD = 0.60
MIN_PER_CLASS = 40
N_BOOT = 2000
BOOT_SEED = 20260812
# The archive selected its layer with an outcome-blind site scan; the achieved
# relative depth was EXACTLY 0.25 on all six archived checkpoints (verified in
# iter_2/.../results/model_*.json).  The artifact plan asserted 0.30; 0.25 is
# what the archive actually used, so 0.25 is what is pre-registered here and the
# discrepancy is reported rather than silently resolved.
LAYER_DEPTH = 0.25
ALPHA_CAP = 4.0
C_GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0]
AXES_ALL = ["A_canned", "B_paraphrase", "C_stylistic", "D_random0", "E_prompt_contrast"]
AB = ("A_canned", "B_paraphrase")
MAX_PARAMS_B = 4.2


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def load_json(p: Path):
    return json.loads(Path(p).read_text())


def atomic_write_json(p: Path, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=_jdefault))
    tmp.replace(p)


def _jdefault(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    raise TypeError(f"not JSON serialisable: {type(o)}")


# ==========================================================================
# Frozen dataset blocks
# ==========================================================================
_BLOCKS: dict | None = None


def blocks() -> dict:
    """All 8 frozen datasets, keyed by metadata_fold."""
    global _BLOCKS
    if _BLOCKS is None:
        doc = load_json(DATA)
        out: dict[str, list] = {}
        for ds in doc["datasets"]:
            for row in ds["examples"]:
                out.setdefault(row["metadata_fold"], []).append(row)
        for k in out:
            out[k].sort(key=lambda r: r["metadata_uid"])
        _BLOCKS = out
    return _BLOCKS


def axis_prompt_splits() -> dict:
    """The archived benign axis-fit / axis-held prompt splits, verbatim.

    Reusing the exact strings is what makes the axis-reproduction gate on the
    six archived checkpoints meaningful.
    """
    doc = load_json(ITER2_EXP1 / "results/prompts.json")
    return {"fit": list(doc["axis_fit_prompts"]),
            "held": list(doc["axis_held_prompts"]),
            "probe": [p["text"] for p in doc["probe_prompts"]]}


def detection_prompts() -> list[dict]:
    """The behavioural prompt pool the model's OWN text is generated on.

    43 harmless_dynamics + the 80-row stratified harmful core + 50 XSTest safe
    prompts.  Three strata, used for the stratum-centring in S4.5.
    """
    b = blocks()
    out = []
    for r in b["harmless_dynamics"]:
        out.append({"uid": r["metadata_uid"], "text": r["input"], "stratum": "harmless"})
    for r in b["plain_harmful"]:
        if r["metadata_meta"].get("in_core80"):
            out.append({"uid": r["metadata_uid"], "text": r["input"], "stratum": "harmful"})
    safe = [r for r in b["xstest_overrefusal"]
            if r["metadata_meta"].get("prompt_type") == "safe"
            or r["metadata_meta"].get("label") == "safe"]
    for r in safe[:50]:
        out.append({"uid": r["metadata_uid"], "text": r["input"], "stratum": "xstest"})
    return out


def extra_harmful_prompts(exclude_uids: set[str]) -> list[dict]:
    """The 514 plain_harmful rows outside the core-80 (escalation ladder rung 2)."""
    return [{"uid": r["metadata_uid"], "text": r["input"], "stratum": "harmful"}
            for r in blocks()["plain_harmful"] if r["metadata_uid"] not in exclude_uids]


def benign_steer_prompts(n: int = 12) -> list[dict]:
    """Benign prompts for the induction sweep: the archived probe set.

    These are the SAME 20 probe prompts the archive dosed on, so the induction
    numbers are directly comparable; the first 12 by frozen order are used.
    """
    doc = load_json(ITER2_EXP1 / "results/prompts.json")
    return [{"uid": p["uid"], "text": p["text"]} for p in doc["probe_prompts"][:n]]


def contrast_splits(n_each: int = 48) -> dict:
    """Harmful / benign halves of layer_contrast (axis E), archived convention."""
    rows = blocks()["layer_contrast"]
    harmful = [r["input"] for r in rows if r["metadata_meta"]["polarity"] == "harmful"]
    benign = [r["input"] for r in rows if r["metadata_meta"]["polarity"] != "harmful"]
    n = min(n_each, len(harmful), len(benign))
    return {"harmful": harmful[:n], "benign": benign[:n], "n_each": n}


def refusal_onset_ids(tokenizer_family: str) -> list[int]:
    """Frozen B7 refusal-onset ids for a tokenizer family (paraphrase gate)."""
    fam = (tokenizer_family or "").lower()
    best = None
    for r in blocks()["refusal_token_lexicon"]:
        m = r["metadata_meta"]
        f = m["tokenizer_family"].lower()
        if f == fam:
            best = m
            break
        if best is None and f == "qwen3":
            best = m
    if best is None:
        return []
    return [int(x["token_id"]) for x in best["refusal_onset"]]


# ==========================================================================
# Panel resolution off the frozen manifest
# ==========================================================================
# The iteration-1/2/3 anchor abliterated member is NOT a manifest row (it was
# frozen into lib/panel.py before the manifest was built).  It is carried here
# explicitly so the one checkpoint on which the phenomenon is already known can
# act as the reproduction control (test T5).
ANCHOR_ROWS = [
    {"repo": "mlabonne/Qwen3-0.6B-abliterated", "revision": None,
     "member_class": "abliterated", "lineage_id": "Qwen/Qwen3-0.6B-Base",
     "params_b": 0.60, "n_layers": 28, "gated": False,
     "source": "lib/panel.py (iteration-1 anchor, not a manifest row)",
     "archived_key": "abliterated_0p6"},
]

# Manifest repo -> the archived evaluation checkpoint key it corresponds to.
# Only these six have archived axes to reproduce against.
ARCHIVED_KEY_BY_REPO = {
    "Qwen/Qwen3-0.6B-Base": "base_0p6",
    "Qwen/Qwen3-0.6B": "instruct_0p6",
    "mlabonne/Qwen3-0.6B-abliterated": "abliterated_0p6",
    "Qwen/Qwen3-1.7B-Base": "base_1p7",
    "Qwen/Qwen3-1.7B": "instruct_1p7",
    "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2": "abliterated_1p7",
}

# The two BREADTH-panel members on which the archived paraphrase axis B DOES
# reach a 0.50 refusal rate (iteration-3 method_out.json,
# metadata.analysis.matrix.alpha_50.check1_lexical.detail: l3_instruct 0.633,
# l4_instruct 0.667).  They are the scope objection and are mandatory.
BREADTH_B_REACHES_HALF = {
    "unsloth/Llama-3.2-1B-Instruct": {"member": "l3_instruct", "archived_B_max_rate": 0.6333333333333333},
    "Qwen/Qwen2.5-1.5B-Instruct": {"member": "l4_instruct", "archived_B_max_rate": 0.6666666666666666},
}


def _key_for(repo: str) -> str:
    return repo.split("/")[-1].replace(".", "p").replace("-", "_")


def resolve_panel() -> dict:
    """Build the run panel from the frozen panel_manifest.

    Priority order (the pre-registered load screen):
      1  the two breadth-panel members on which axis B reaches 0.50
      2  abliterated-class members whose lineage already has a parent queued
      3  remaining abliterated-class members, smallest first
      4  remaining in-lineage parents (one instruct + one base per lineage)
    """
    rows = blocks()["panel_manifest"]
    recs = []
    for r in rows:
        m = r["metadata_meta"]
        pc = m.get("param_count")
        if not pc:
            continue
        recs.append({
            "repo": m["hf_repo_id"], "revision": r["output"] or m.get("revision"),
            "member_class": m["member_class"], "lineage_id": m["lineage_id"],
            "params_b": pc / 1e9, "n_layers": m.get("n_layers"),
            "gated": bool(m.get("gated")), "verified": bool(m.get("verified")),
            "mirror_of": m.get("mirror_of") or "", "h4_status": m.get("h4_status"),
            "architecture": m.get("architecture"),
            "tokenizer_family": m.get("tokenizer_family"),
            "has_chat_template": bool(m.get("has_chat_template")),
            "source": "panel_manifest",
        })

    def eligible(x):
        return (x["verified"] and not x["gated"] and x["params_b"] <= MAX_PARAMS_B
                and x["n_layers"] and x["n_layers"] >= 8)

    small = [x for x in recs if eligible(x)]
    by_repo = {x["repo"]: x for x in small}

    abl_cls = ("abliterated", "behavioral_uncensored")
    cand_abl = [x for x in small if x["member_class"] in abl_cls]
    # the anchor is not a manifest row; splice it in
    for a in ANCHOR_ROWS:
        if a["repo"] not in by_repo:
            rec = dict(a)
            rec.update({"verified": True, "h4_status": "anchor", "mirror_of": "",
                        "architecture": "Qwen3ForCausalLM", "tokenizer_family": "Qwen3",
                        "has_chat_template": True})
            cand_abl.append(rec)
            by_repo[rec["repo"]] = rec

    abl_lineages = {x["lineage_id"] for x in cand_abl}
    parents = [x for x in small if x["member_class"] in ("base", "instruct")
               and x["lineage_id"] in abl_lineages]
    # one instruct + one base per lineage, preferring the smallest (cheapest load)
    chosen_parents: dict[tuple[str, str], dict] = {}
    for x in sorted(parents, key=lambda z: (z["lineage_id"], z["member_class"], z["params_b"])):
        k = (x["lineage_id"], x["member_class"])
        if k not in chosen_parents:
            chosen_parents[k] = x
    parent_list = list(chosen_parents.values())

    # breadth-panel members: mandatory even if their lineage has no abliterated kin
    breadth = []
    for repo in BREADTH_B_REACHES_HALF:
        rec = by_repo.get(repo) or next((x for x in recs if x["repo"] == repo), None)
        if rec is not None:
            breadth.append(rec)

    queued: dict[str, dict] = {}

    def enqueue(rec, prio, role):
        if rec["repo"] in queued:
            queued[rec["repo"]]["priority"] = min(queued[rec["repo"]]["priority"], prio)
            return
        out = dict(rec)
        out.update({"priority": prio, "role": role, "key": _key_for(rec["repo"]),
                    "archived_key": ARCHIVED_KEY_BY_REPO.get(rec["repo"]),
                    "breadth_b_reaches_half": rec["repo"] in BREADTH_B_REACHES_HALF})
        queued[rec["repo"]] = out

    for rec in breadth:
        enqueue(rec, 1, "breadth_panel_parent")
    have_parent_lineage = {r["lineage_id"] for r in breadth}
    for rec in sorted(cand_abl, key=lambda z: z["params_b"]):
        if rec["lineage_id"] in have_parent_lineage:
            enqueue(rec, 2, "abliterated_class")
    # Within priority 3 the WEIGHT-EDITED abliterations come first (they are the
    # class the headline is about), then behavioural-uncensored checkpoints the
    # manifest flagged h4_status='candidate', then the rest.  The ratchet drops
    # from the bottom, so this ordering decides what a short run still answers.
    def p3_rank(z):
        cls = 0 if z["member_class"] == "abliterated" else (
            1 if z.get("h4_status") == "candidate" else 2)
        return (cls, z["params_b"])

    for rec in sorted(cand_abl, key=p3_rank):
        enqueue(rec, 3, "abliterated_class")
    for rec in sorted(parent_list, key=lambda z: (z["params_b"])):
        enqueue(rec, 4, "in_lineage_parent")

    def order(z):
        return (z["priority"],
                p3_rank(z) if z["priority"] == 3 else (0, z["params_b"]))

    panel = sorted(queued.values(), key=order)
    skipped = [{"repo": x["repo"], "reason":
                ("gated" if x["gated"] else
                 "unverified" if not x["verified"] else
                 f"params_b={x['params_b']:.2f}>{MAX_PARAMS_B}" if x["params_b"] > MAX_PARAMS_B
                 else "n_layers missing or <8"),
                "member_class": x["member_class"], "params_b": x["params_b"]}
               for x in recs if not eligible(x) and x["member_class"] in abl_cls]
    return {"panel": panel, "skipped_candidates": skipped,
            "n_abliterated_class_queued": sum(1 for x in panel
                                              if x["member_class"] in abl_cls),
            "n_parents_queued": sum(1 for x in panel
                                    if x["member_class"] in ("base", "instruct")),
            "layer_depth_rule": LAYER_DEPTH, "max_params_b": MAX_PARAMS_B}


# ==========================================================================
# Statistics
# ==========================================================================
def auroc(pos, neg) -> float:
    from scipy.stats import rankdata
    pos = np.asarray(pos, float)
    neg = np.asarray(neg, float)
    n1, n0 = len(pos), len(neg)
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(np.concatenate([pos, neg]), method="average")
    return float((r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cohens_d(pos, neg) -> float:
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) < 2 or len(neg) < 2:
        return float("nan")
    pooled = math.sqrt(0.5 * (pos.var(ddof=1) + neg.var(ddof=1))) + 1e-12
    return float((pos.mean() - neg.mean()) / pooled)


def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def cluster_boot_indices(clusters: np.ndarray, n_boot: int, seed: int):
    """Index arrays for a bootstrap resampling CLUSTERS (prompts) with replacement."""
    rng = np.random.default_rng(seed)
    uniq = np.unique(clusters)
    idx_by_c = {c: np.flatnonzero(clusters == c) for c in uniq}
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        yield np.concatenate([idx_by_c[c] for c in pick])


def boot_ci(vals, lo=2.5, hi=97.5):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if v.size < 20:
        return (float("nan"), float("nan"))
    return (float(np.percentile(v, lo)), float(np.percentile(v, hi)))


def boot_p_two_sided(vals, null: float = 0.0) -> float:
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    if v.size < 20:
        return float("nan")
    frac = float(np.mean(v <= null))
    p = 2 * min(frac, 1 - frac)
    return float(min(1.0, max(1.0 / (v.size + 1), p)))


def holm(pvals: dict) -> dict:
    items = [(k, v) for k, v in pvals.items() if np.isfinite(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out, prev = {}, 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - i) * p))
        out[k] = adj
        prev = adj
    for k in pvals:
        out.setdefault(k, float("nan"))
    return out


def spearman(x, y) -> float:
    from scipy.stats import rankdata
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return float("nan")
    rx, ry = rankdata(x[ok]), rankdata(y[ok])
    if rx.std() < 1e-12 or ry.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def cohens_kappa(a, b) -> dict:
    a, b = list(a), list(b)
    n = len(a)
    if n == 0:
        return {"kappa": float("nan"), "n": 0}
    cats = sorted(set(a) | set(b))
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    exp = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    k = (obs - exp) / (1 - exp) if abs(1 - exp) > 1e-12 else 0.0
    return {"kappa": float(k), "n": n, "observed_agreement": float(obs),
            "expected_agreement": float(exp)}


def cosine(a, b) -> float:
    a, b = np.asarray(a, float).ravel(), np.asarray(b, float).ravel()
    if a.shape != b.shape:
        return float("nan")
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def random_null_distribution(reps: np.ndarray, labels: np.ndarray,
                             strata: np.ndarray, n_draws: int = 20,
                             seed: int = BOOT_SEED) -> dict:
    """AUROC a RANDOM unit direction achieves, over `n_draws` fresh draws.

    A residual stream is strongly anisotropic, so the isotropic intuition that a
    random direction reads at 0.50 is wrong in practice: a single draw can land
    well away from chance.  This is the empirical null the axis verdicts should
    be read against, and it costs `n_draws` dot products and no forward passes.
    Both the raw-projection and the norm-controlled (cosine) readouts are drawn.
    """
    labels = np.asarray(labels, bool)
    if labels.sum() < 2 or (~labels).sum() < 2:
        return {"n_draws": 0, "undefined": True}
    rng = np.random.default_rng(seed)
    d = reps.shape[1]
    nrm = np.maximum(np.linalg.norm(reps, axis=1), 1e-6)
    a_proj, a_cos = [], []
    for _ in range(n_draws):
        u = rng.normal(size=d).astype(np.float32)
        u /= np.linalg.norm(u) + 1e-12
        p = centre_by_stratum(reps @ u, strata)
        c = centre_by_stratum((reps @ u) / nrm, strata)
        a_proj.append(auroc(p[labels], p[~labels]))
        a_cos.append(auroc(c[labels], c[~labels]))

    def summarise(vals):
        v = np.asarray(vals, float)
        dev = np.abs(v - 0.5)
        return {"mean": float(v.mean()), "sd": float(v.std(ddof=1)),
                "min": float(v.min()), "max": float(v.max()),
                "p2p5": float(np.percentile(v, 2.5)),
                "p97p5": float(np.percentile(v, 97.5)),
                "max_abs_deviation_from_half": float(dev.max()),
                "p95_abs_deviation_from_half": float(np.percentile(dev, 95))}

    return {"n_draws": n_draws, "undefined": False,
            "projection": summarise(a_proj), "norm_controlled": summarise(a_cos),
            "aurocs_projection": [float(x) for x in a_proj],
            "note": "AUROC achieved by RANDOM unit directions through the identical "
                    "pipeline. An axis only demonstrates a directional finding if it "
                    "sits outside this spread."}


def verdict_from_ci(lo: float, hi: float) -> str:
    """Pre-registered P4: AT_CHANCE / READS / AMBIGUOUS."""
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return "UNDEFINED"
    if CHANCE_BAND[0] <= lo and hi <= CHANCE_BAND[1]:
        return "AT_CHANCE"
    if lo > READS_THRESHOLD:
        return "READS"
    return "AMBIGUOUS"


# ==========================================================================
# Detection statistics: stratum-centred, prompt-clustered
# ==========================================================================
def centre_by_stratum(s: np.ndarray, strata: np.ndarray) -> np.ndarray:
    """Archived convention (analysis12._centre_by_stratum), verbatim semantics."""
    out = np.asarray(s, float).copy()
    for st in np.unique(strata):
        m = strata == st
        if m.sum() >= 2:
            out[m] -= out[m].mean()
        else:
            out[m] -= out.mean()
    return out


def detection_stats(proj: dict, labels: np.ndarray, strata: np.ndarray,
                    clusters: np.ndarray, n_boot: int = N_BOOT,
                    seed: int = BOOT_SEED, centred: dict | None = None) -> dict:
    """AUROC per axis with a prompt-clustered bootstrap and a paired A-B contrast.

    ``proj``    : {axis: (n,) projections onto the unit axis}
    ``labels``  : bool, True = refusal
    ``strata``  : per-item stratum name (harmless / harmful / xstest)
    ``clusters``: per-item prompt uid (the bootstrap resampling unit)

    Stratum-centring subtracts the per-stratum mean projection before pooling, so
    a prompt-topic offset cannot inflate AUROC.  Raw (uncentred) AUROC is
    reported alongside, never as the primary.
    """
    labels = np.asarray(labels, bool)
    axes = sorted(proj)
    if centred is None:
        centred = {ax: centre_by_stratum(proj[ax], strata) for ax in axes}
    else:
        centred = {ax: np.asarray(centred[ax], float) for ax in axes}

    out = {"n_items": int(labels.size), "n_refusal": int(labels.sum()),
           "n_compliance": int((~labels).sum()),
           "n_prompts": int(len(np.unique(clusters))), "axes": {}}

    # Stratum composition: if refusals live almost entirely in one stratum and
    # compliances in another, a pooled AUROC can be driven by prompt topic rather
    # than by refusal.  Centring removes the mean offset but not that separation,
    # so a WITHIN-stratum AUROC is computed as well and the imbalance is reported.
    comp, usable = {}, []
    for s in np.unique(strata):
        m = strata == s
        nr, nc = int((labels & m).sum()), int(((~labels) & m).sum())
        comp[str(s)] = {"n_refusal": nr, "n_compliance": nc, "n": int(m.sum())}
        if nr >= 5 and nc >= 5:
            usable.append(s)
    out["stratum_composition"] = comp
    out["strata_with_both_classes"] = [str(s) for s in usable]
    nr_tot, nc_tot = int(labels.sum()), int((~labels).sum())
    out["class_stratum_separation"] = float(max(
        max(v["n_refusal"] / max(nr_tot, 1) for v in comp.values()),
        max(v["n_compliance"] / max(nc_tot, 1) for v in comp.values())))

    boot_idx = list(cluster_boot_indices(clusters, n_boot, seed))
    boot_auc: dict[str, list] = {ax: [] for ax in axes}
    for idx in boot_idx:
        yb = labels[idx]
        if yb.sum() < 5 or (~yb).sum() < 5:
            for ax in axes:
                boot_auc[ax].append(float("nan"))
            continue
        for ax in axes:
            vb = centred[ax][idx]
            boot_auc[ax].append(auroc(vb[yb], vb[~yb]))

    for ax in axes:
        v = centred[ax]
        a = auroc(v[labels], v[~labels])
        lo, hi = boot_ci(boot_auc[ax])
        raw = np.asarray(proj[ax], float)
        ws, wn = [], []
        for s in usable:
            m = strata == s
            ws.append(auroc(v[m & labels], v[m & ~labels]))
            wn.append(int(m.sum()))
        within = (float(np.average(ws, weights=wn)) if ws else float("nan"))
        out["axes"][ax] = {
            "auroc": a, "auroc_ci95": [lo, hi],
            "verdict": verdict_from_ci(lo, hi),
            "cohens_d": cohens_d(v[labels], v[~labels]),
            "auroc_raw_uncentred": auroc(raw[labels], raw[~labels]),
            "auroc_within_stratum": within,
            "auroc_per_stratum": {str(s): x for s, x in zip(usable, ws)},
            "mean_diff_projection_units": float(v[labels].mean() - v[~labels].mean()),
        }

    # paired A - B on the SAME resampled prompts
    if all(ax in centred for ax in AB):
        a_ax, b_ax = AB
        obs = out["axes"][a_ax]["auroc"] - out["axes"][b_ax]["auroc"]
        diffs = [x - y for x, y in zip(boot_auc[a_ax], boot_auc[b_ax])
                 if np.isfinite(x) and np.isfinite(y)]
        lo, hi = boot_ci(diffs)
        out["paired_A_minus_B"] = {
            "delta": float(obs), "ci95": [lo, hi],
            "p_boot": boot_p_two_sided(diffs, 0.0), "n_boot_effective": len(diffs)}
    return out


# ==========================================================================
# Induction: contrast units and the matched-contrast paired advantage
# ==========================================================================
def alpha_for_contrast(c: float, raw_norm: float, norm_l: float) -> float:
    """alpha = c * ||d_raw|| / NORM_L.

    Inverse of the archived contrast-unit definition c = alpha * NORM_L /
    ||d_raw||, which reproduces analysis2.json exactly (instruct_0p6, axis A:
    alpha 0.5, NORM_L 21.1353, ||d_raw|| 10.6322 -> c = 0.99393, archived
    0.9939255730665065).
    """
    return float(c * raw_norm / max(norm_l, 1e-12))


def contrast_units(alpha: float, raw_norm: float, norm_l: float) -> float:
    return float(alpha * norm_l / max(raw_norm, 1e-12))


def matched_contrast_delta(grid_a: dict, grid_b: dict, n_boot: int = N_BOOT,
                           seed: int = BOOT_SEED) -> dict:
    """Paired A-minus-B refusal-rate advantage at MATCHED contrast units.

    ``grid_x`` maps str(c) -> {"per_rollout": {(prompt,seed) -> 0/1}, "capped":
    bool, "fluent": float}.  Only c values where BOTH axes are uncapped and
    fluent enter the average, so the norm-mismatch rival (arXiv:2603.22061)
    cannot explain a surviving gap: the injected vector carries the same norm
    relative to each axis's own contrast magnitude.
    """
    shared = [c for c in grid_a if c in grid_b
              and not grid_a[c]["capped"] and not grid_b[c]["capped"]
              and grid_a[c]["fluent"] >= 0.5 and grid_b[c]["fluent"] >= 0.5
              and float(c) > 0]
    shared.sort(key=float)
    if not shared:
        return {"verdict": "INCONCLUSIVE", "reason": "no shared uncapped fluent c",
                "n_shared_c": 0, "shared_c": []}

    # per-rollout keys are "prompt|seed"; cluster on prompt
    keys = sorted(set(grid_a[shared[0]]["per_rollout"]))
    prompts = np.array([k.split("|")[0] for k in keys])
    per_c = {}
    for c in shared:
        ra = np.array([grid_a[c]["per_rollout"].get(k, np.nan) for k in keys], float)
        rb = np.array([grid_b[c]["per_rollout"].get(k, np.nan) for k in keys], float)
        per_c[c] = (ra, rb)

    def stat(idx):
        ds = [np.nanmean(per_c[c][0][idx] - per_c[c][1][idx]) for c in shared]
        return float(np.nanmean(ds))

    obs = stat(np.arange(len(keys)))
    boots = [stat(idx) for idx in cluster_boot_indices(prompts, n_boot, seed)]
    lo, hi = boot_ci(boots)

    # delta at the c where A first reaches 0.50
    c_at_half, delta_at_half = None, None
    for c in shared:
        if np.nanmean(per_c[c][0]) >= 0.5:
            c_at_half = float(c)
            delta_at_half = float(np.nanmean(per_c[c][0] - per_c[c][1]))
            break

    b_rates = [float(np.nanmean(per_c[c][1])) for c in shared]
    b_reaches_half = bool(max(b_rates) >= 0.5) if b_rates else False
    if np.isfinite(lo) and lo > 0:
        verdict = "NORM_MISMATCH_DOES_NOT_EXPLAIN"
    elif b_reaches_half and np.isfinite(lo) and lo <= 0 <= hi:
        verdict = "B_IS_A_GENUINE_INDUCER"
    else:
        verdict = "INCONCLUSIVE"
    return {"verdict": verdict, "mean_delta": obs, "ci95": [lo, hi],
            "p_boot": boot_p_two_sided(boots, 0.0),
            "n_shared_c": len(shared), "shared_c": [float(c) for c in shared],
            "c_where_A_first_reaches_half": c_at_half,
            "delta_at_that_c": delta_at_half,
            "B_max_rate_over_shared_c": float(max(b_rates)) if b_rates else None,
            "B_reaches_half_at_matched_contrast": b_reaches_half}


def free_cuda():
    import torch
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


class Ratchet:
    """Wall-clock ratchet: stop launching new members at the deadline."""

    def __init__(self, budget_min: float):
        self.t0 = time.time()
        self.budget = budget_min * 60.0
        self.per_member: list[float] = []

    def elapsed(self) -> float:
        return time.time() - self.t0

    def remaining(self) -> float:
        return self.budget - self.elapsed()

    def record(self, secs: float) -> None:
        self.per_member.append(float(secs))

    def can_start(self, est: float | None = None) -> bool:
        if est is None:
            est = float(np.median(self.per_member)) if self.per_member else 600.0
        return self.remaining() > est * 1.15

    def report(self) -> dict:
        return {"elapsed_s": self.elapsed(), "budget_s": self.budget,
                "remaining_s": self.remaining(),
                "median_member_s": float(np.median(self.per_member))
                if self.per_member else None,
                "n_members_done": len(self.per_member)}
