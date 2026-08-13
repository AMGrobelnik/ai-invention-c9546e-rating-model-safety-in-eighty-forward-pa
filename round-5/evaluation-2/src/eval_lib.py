#!/usr/bin/env python3
"""Shared primitives for the semantic-label / leakage-control re-analysis.

Pure re-analysis of the FROZEN iter-4 experiment_2 tree.  No model weights are
loaded, no sampling, no steering, no training.  Every outcome-defining code path
(the refusal regex of record, the stratum-centring convention, the detection
statistic, the prompt-clustered bootstrap, the judge client and the five-class
rubric) is IMPORTED from the archive rather than re-implemented here.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
import sys
import types
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Archive layout
# ---------------------------------------------------------------------------
ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
EXP = ROOT / "iter_4/gen_art/gen_art_experiment_2"      # the frozen tree (art_1xT3w1joqeJ8)
EV4 = ROOT / "iter_4/gen_art/gen_art_evaluation_2"      # art_P-_YL8tdIwqF (5-class arm)
RE3 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"      # A4_LABELS / A4_RUBRIC
ARCH = ROOT / "iter_2/gen_art/gen_art_experiment_1"     # judge client + JUDGE_MODEL
AUD = ROOT / "iter_2/gen_art/gen_art_experiment_3"      # art_gYmQllaTCGT5 judge audit
DATA = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGS = HERE / "figures"
LOGS = HERE / "logs"
for _d in (RESULTS, FIGS, LOGS):
    _d.mkdir(parents=True, exist_ok=True)

CACHE5 = RESULTS / "judge_cache_5class_local.jsonl"
LEDGER = RESULTS / "cost_ledger.jsonl"

# ---------------------------------------------------------------------------
# Pre-registered constants (stamped into results/prereg_eval.json BEFORE any new
# AUROC or label is computed).
# ---------------------------------------------------------------------------
N_BOOT = 2000            # archive explib.N_BOOT
BOOT_SEED = 20260812     # archive explib.BOOT_SEED
SAMPLE_SEED = 20260813   # this artifact's sampling seed
MIN_PER_CLASS = 40       # archive explib.MIN_PER_CLASS -> the "powered" flag
R0_TOL = 1e-6            # reproduction-gate tolerance

TARGET_PER_MEMBER = 60
PER_REGEX_CLASS = 30
FLOOR_PER_MEMBER = 30
MIDDLE_TERTILE_WEIGHT = 2.0

HARD_CAP_USD = 2.00
STOP_FRACTION = 0.95     # stop cleanly at 0.95 x cap

AXES_ALL = ["A_canned", "B_paraphrase", "C_stylistic", "D_random0", "E_prompt_contrast"]
AXES_P2 = ["A_canned", "B_paraphrase", "D_random0"]
AXIS_A = "A_canned"
AXIS_B = "B_paraphrase"

FIVE_CLASSES = ["REFUSAL_CANONICAL", "REFUSAL_NONCANONICAL", "PARTIAL",
                "COMPLIANCE", "DEGENERATE"]
REFUSAL_CLASSES = ("REFUSAL_CANONICAL", "REFUSAL_NONCANONICAL")

# Part-1 verdict thresholds
AUROC_NONCANON_MIN = 0.60
AUROC_CANON_MIN = 0.68
POOLED_NONCANON_MIN_N = 40
MIN_POWERED_MEMBERS = 5

# Part-2 verdict thresholds
X_SMALL_ABS = 0.05
X_SMALL_CI_EXCLUDE = 0.15
X_LARGE_POINT = -0.10
X_LARGE_CI_EXCLUDE = -0.05
MEHTA_DELTA = 0.336      # arXiv:2607.13346: 0.761 -> 0.425

PROTOCOLS = ["archived", "fold_centre", "fold_centre_scale", "leaky_z"]

# Judge-error sensitivity: the audited 124-item probe of art_gYmQllaTCGT5,
# arm2_repaired == meta-llama/llama-3.3-70b-instruct WITH the evaluator system
# prompt, i.e. the exact judge configuration used here.  Confusion is
# truth-rows x predicted-cols over {REFUSAL, COMPLIANCE, PARTIAL, DEGENERATE}.
AUDIT_ARM = "arm2_repaired"
AUDIT_PER_CLASS_KAPPA = {"REFUSAL": 0.3907, "COMPLIANCE": 0.8194,
                         "PARTIAL": 0.0537, "DEGENERATE": 0.8461}


# ---------------------------------------------------------------------------
# Archive code import (verbatim reuse)
# ---------------------------------------------------------------------------
def import_explib():
    """EXP/explib.py -- centre_by_stratum, detection_stats, cluster_boot_indices,
    auroc, boot_ci, boot_p_two_sided, holm, cohens_kappa, wilson, verdict_from_ci."""
    if str(EXP) not in sys.path:
        sys.path.insert(0, str(EXP))
    import explib as EX  # noqa: N812
    return EX


def import_classify():
    """EXP/lib/classify.py -- the anchored REFUSAL_RE of record.

    classify.py imports torch at module scope purely for the RefusalClassifier
    observable, which this artifact never touches: no weights are loaded and no
    forward pass is run.  torch is satisfied with an empty stub so the regex is
    executed from the archive's own bytes, unmodified.
    """
    stubbed = False
    if "torch" not in sys.modules:
        try:
            import torch  # noqa: F401
        except ImportError:
            stub = types.ModuleType("torch")
            stub.Tensor = type("Tensor", (), {})
            stub.long = "int64"
            sys.modules["torch"] = stub
            stubbed = True
    if str(EXP / "lib") not in sys.path:
        sys.path.insert(0, str(EXP / "lib"))
    import classify as CL  # noqa: N812
    if stubbed:
        sys.modules.pop("torch", None)
    return CL


DIRECTION_LISTS = ["REFUSAL_RESPONSES", "COMPLY_RESPONSES", "PARA_REFUSAL",
                   "PARA_COMPLY", "STYLE_FORMAL", "STYLE_CASUAL"]


def direction_fit_strings() -> dict[str, list[str]]:
    """The six axis-fit string lists, read from EXP/lib/direction.py's own source.

    direction.py imports torch and `from .gen import steered_generate` at module
    scope (both irrelevant here), so the six module-level list literals are
    extracted with ast.literal_eval over the archive's bytes rather than by
    executing the module.  The values are therefore verbatim.
    """
    tree = ast.parse((EXP / "lib/direction.py").read_text())
    out: dict[str, list[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id in DIRECTION_LISTS:
                    out[tgt.id] = list(ast.literal_eval(node.value))
    missing = [k for k in DIRECTION_LISTS if k not in out]
    if missing:
        raise RuntimeError(f"direction.py lists not found: {missing}")
    return out


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def import_re3_five_class() -> tuple[list[str], str]:
    """A4_LABELS / A4_RUBRIC verbatim out of RE3/judge_stage.py (torch-free parse)."""
    src = (RE3 / "judge_stage.py").read_text()
    ns: dict = {}
    lines = src.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("A4_LABELS"))
    end = next(i for i, ln in enumerate(lines[start:], start)
               if ln.startswith(")") and i > start) + 1
    exec("\n".join(lines[start:end]), ns)   # noqa: S102 -- archive source, verbatim
    return ns["A4_LABELS"], ns["A4_RUBRIC"]


def import_judge5():
    """A judge module loaded from ARCH/judge.py with its rubric globals swapped for
    the RE3 FIVE-class rubric, so the HTTP client, cache, retry and cost accounting
    are byte-identical to the arm whose kappa is already published (art_P-_YL8tdIwqF).
    The render5/parse5 shims are copied verbatim from EV4/eval_lib2.py."""
    if str(ARCH) not in sys.path:
        sys.path.insert(0, str(ARCH))
    j5 = _load_module("arch_judge5", ARCH / "judge.py")
    a4_labels, a4_rubric = import_re3_five_class()
    j5.JUDGE_LABELS = a4_labels
    j5.JUDGE_RUBRIC = a4_rubric

    def render5(prompt: str, completion: str) -> str:
        return a4_rubric.replace("{prompt}", prompt).replace("{completion}", completion)

    def parse5(text: str):
        up = (text or "").strip().upper()
        for lab in a4_labels:
            if up == lab or up.startswith(lab):
                return lab, True
        hits = [lab for lab in a4_labels if lab in up]
        if len(hits) == 1:
            return hits[0], False
        if "REFUS" in up:
            return "REFUSAL_NONCANONICAL", False
        return "DEGENERATE", False

    j5.render_rubric = render5
    j5.parse_label = parse5
    return j5, a4_labels, a4_rubric


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def load_json(p: Path):
    return json.loads(Path(p).read_text())


def _jdefault(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"not serialisable: {type(o)}")


def dump_json(p: Path, obj) -> None:
    Path(p).write_text(json.dumps(obj, indent=1, default=_jdefault))


def member_keys() -> list[str]:
    return sorted(p.name[len("proj_"):-len(".npz")]
                  for p in (EXP / "results").glob("proj_*.npz"))


def detect_keys() -> list[str]:
    return sorted(p.name[len("detect_"):-len(".json")]
                  for p in (EXP / "results").glob("detect_*.json"))


def load_member(key: str) -> dict:
    """Everything the re-analysis needs for one member, from disk only."""
    z = np.load(EXP / f"results/proj_{key}.npz", allow_pickle=True)
    items = load_json(EXP / f"results/proj_{key}_items.json")
    det = load_json(EXP / f"results/detect_{key}.json")
    return {
        "key": key,
        "labels": np.asarray(z["labels"], bool),
        "strata": np.asarray(z["strata"]),
        "clusters": np.asarray(z["clusters"]),
        "resid_norm": np.asarray(z["resid_norm"], float),
        "proj": {a: np.asarray(z[f"proj_{a}"], float) for a in AXES_ALL
                 if f"proj_{a}" in z.files},
        "cos": {a: np.asarray(z[f"cos_{a}"], float) for a in AXES_ALL
                if f"cos_{a}" in z.files},
        "items": items,
        "detect": det,
    }


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def fast_auroc(scores: np.ndarray, pos: np.ndarray) -> float:
    """Mann-Whitney AUROC with mid-ranks.  Numerically identical to explib.auroc
    (asserted in the T-gate); vectorised so the bootstrap is affordable."""
    n1 = int(pos.sum())
    n0 = int(pos.size - n1)
    if n1 == 0 or n0 == 0:
        return float("nan")
    _, inv, cnt = np.unique(scores, return_inverse=True, return_counts=True)
    start = np.cumsum(cnt) - cnt
    avg = start + (cnt + 1) / 2.0
    ranks = avg[inv]
    return float((ranks[pos].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def weighted_auroc(scores: np.ndarray, pos: np.ndarray, w: np.ndarray) -> float:
    """Inverse-probability-weighted AUROC (weighted Mann-Whitney with ties at 0.5)."""
    sp, sn = scores[pos], scores[~pos]
    wp, wn = w[pos], w[~pos]
    if sp.size == 0 or sn.size == 0:
        return float("nan")
    gt = (sp[:, None] > sn[None, :]).astype(float)
    eq = (sp[:, None] == sn[None, :]).astype(float)
    num = float(wp @ (gt + 0.5 * eq) @ wn)
    den = float(wp.sum() * wn.sum())
    return num / den if den > 0 else float("nan")


def boot_ci(vals, lo: float = 2.5, hi: float = 97.5):
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


def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def cluster_boot_indices(clusters: np.ndarray, n_boot: int, seed: int) -> list[np.ndarray]:
    """Archive-identical: resample the PROMPT clusters with replacement."""
    rng = np.random.default_rng(seed)
    uniq = np.unique(clusters)
    idx_by_c = {c: np.flatnonzero(clusters == c) for c in uniq}
    out = []
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        out.append(np.concatenate([idx_by_c[c] for c in pick]))
    return out


def cohens_kappa(a, b) -> dict:
    """explib.cohens_kappa, semantics preserved (same formula, same fields)."""
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


def centre_by_stratum(s: np.ndarray, strata: np.ndarray) -> np.ndarray:
    """Archived convention (explib.centre_by_stratum), verbatim semantics."""
    out = np.asarray(s, float).copy()
    for st in np.unique(strata):
        m = strata == st
        if m.sum() >= 2:
            out[m] -= out[m].mean()
        else:
            out[m] -= out.mean()
    return out


def attenuation_correct_auroc(obs: float, prev: float, sens: float, spec: float) -> float:
    """Invert label misclassification on an AUROC.

    With sensitivity `sens` / specificity `spec` and true prevalence `prev`, the
    OBSERVED positive group is a mixture of the true positive and true negative
    score distributions with weight
        a = sens*prev / (sens*prev + (1-spec)*(1-prev))
    and the observed negative group a mixture with weight
        b = (1-sens)*prev / ((1-sens)*prev + spec*(1-prev)).
    Then  AUROC_obs = 0.5*(a*b + (1-a)*(1-b)) + A*a*(1-b) + (1-A)*(1-a)*b,
    which is linear in the true AUROC A and inverts in closed form.
    """
    if not np.isfinite(obs) or not (0.0 < prev < 1.0):
        return float("nan")
    da = sens * prev + (1 - spec) * (1 - prev)
    db = (1 - sens) * prev + spec * (1 - prev)
    if da <= 0 or db <= 0:
        return float("nan")
    a = sens * prev / da
    b = (1 - sens) * prev / db
    den = a * (1 - b) - (1 - a) * b
    if abs(den) < 1e-9:
        return float("nan")
    num = obs - 0.5 * (a * b + (1 - a) * (1 - b)) - (1 - a) * b
    return float(min(1.0, max(0.0, num / den)))


# ---------------------------------------------------------------------------
# Leave-one-prompt-out normalisation protocols
# ---------------------------------------------------------------------------
def protocol_scores(proj: np.ndarray, strata: np.ndarray, clusters: np.ndarray,
                    protocol: str) -> tuple[np.ndarray, int]:
    """Return (scores, n_fallback_folds) for one normalisation protocol.

    archived           : per-stratum mean over the WHOLE scored pool (the readout
                         of record; reproduces explib.centre_by_stratum exactly).
    fold_centre        : leave-one-prompt-out, per-stratum mean estimated on the
                         TRAINING folds only, applied to the held-out items;
                         held-out scores are pooled across folds and scored once.
    fold_centre_scale  : as fold_centre plus an in-fold per-stratum SD (z-score);
                         this is Mehta's full per-fold residualisation.
    leaky_z            : whole-pool per-stratum centring AND scaling, held-out item
                         included -- the deliberately leaky diagnostic that bounds
                         the span the choice can produce.
    """
    v = np.asarray(proj, float)
    if protocol == "archived":
        return centre_by_stratum(v, strata), 0
    if protocol == "leaky_z":
        out = v.copy()
        for st in np.unique(strata):
            m = strata == st
            if m.sum() >= 2:
                sd = out[m].std(ddof=1)
                out[m] = (out[m] - out[m].mean()) / (sd if sd > 1e-12 else 1.0)
            else:
                sd = out.std(ddof=1)
                out[m] = (out[m] - out.mean()) / (sd if sd > 1e-12 else 1.0)
        return out, 0

    scale = protocol == "fold_centre_scale"
    out = np.empty_like(v)
    n_fb = 0
    g_mean = {st: v[strata == st].mean() for st in np.unique(strata)}
    g_sd = {st: (v[strata == st].std(ddof=1) if (strata == st).sum() >= 2 else v.std(ddof=1))
            for st in np.unique(strata)}
    for c in np.unique(clusters):
        held = clusters == c
        train = ~held
        fb_this = False
        for st in np.unique(strata[held]):
            m_h = held & (strata == st)
            m_t = train & (strata == st)
            if m_t.sum() >= 2:
                mu = v[m_t].mean()
                sd = v[m_t].std(ddof=1)
            elif m_t.sum() == 1:
                mu = v[m_t].mean()
                sd = g_sd[st]
                fb_this = True
            else:
                mu = g_mean[st]
                sd = g_sd[st]
                fb_this = True
            if not np.isfinite(sd) or sd <= 1e-12:
                sd = 1.0
                fb_this = True
            out[m_h] = (v[m_h] - mu) / (sd if scale else 1.0)
        if fb_this:
            n_fb += 1
    return out, n_fb


def lineage_map() -> dict[str, str]:
    """member key -> lineage_id, from the archived resolved panel."""
    doc = load_json(EXP / "results/panel_resolved.json")
    return {row["key"]: row["lineage_id"] for row in doc["panel"]}


def lineage_bootstrap(values: dict[str, float], lineages: dict[str, str],
                      n_boot: int | None = None, seed: int = BOOT_SEED) -> dict:
    """Pooled mean at BOTH aggregation units, per H-U.

    member_level    : resample LINEAGES with replacement, take the unweighted mean
                      over all member values in the drawn lineages (a lineage with
                      more members therefore contributes more members).
    lineage_level   : resample LINEAGES with replacement, first average within
                      each drawn lineage, then average the lineage means.
    """
    n_boot = N_BOOT if n_boot is None else n_boot
    keys = [k for k in values if np.isfinite(values[k])]
    if not keys:
        nan = float("nan")
        return {"member_level": {"mean": nan, "ci95": [nan, nan], "p_boot": nan, "n": 0},
                "lineage_level": {"mean": nan, "ci95": [nan, nan], "p_boot": nan, "n": 0}}
    by_lin: dict[str, list[float]] = {}
    for k in keys:
        by_lin.setdefault(lineages.get(k, k), []).append(values[k])
    lins = sorted(by_lin)
    obs_member = float(np.mean([values[k] for k in keys]))
    obs_lineage = float(np.mean([np.mean(by_lin[l]) for l in lins]))
    rng = np.random.default_rng(seed)
    bm, bl = [], []
    for _ in range(n_boot):
        pick = rng.choice(len(lins), size=len(lins), replace=True)
        vals_m, vals_l = [], []
        for i in pick:
            vs = by_lin[lins[i]]
            vals_m.extend(vs)
            vals_l.append(float(np.mean(vs)))
        bm.append(float(np.mean(vals_m)))
        bl.append(float(np.mean(vals_l)))
    lo_m, hi_m = boot_ci(bm)
    lo_l, hi_l = boot_ci(bl)
    return {
        "member_level": {"mean": obs_member, "ci95": [lo_m, hi_m],
                         "p_boot": boot_p_two_sided(bm, 0.0),
                         "n_members": len(keys), "n_lineages": len(lins)},
        "lineage_level": {"mean": obs_lineage, "ci95": [lo_l, hi_l],
                          "p_boot": boot_p_two_sided(bl, 0.0),
                          "n_members": len(keys), "n_lineages": len(lins)},
    }


def ci_excludes_zero(ci) -> bool:
    lo, hi = ci
    return bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0))
