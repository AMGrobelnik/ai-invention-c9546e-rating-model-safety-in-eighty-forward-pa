#!/usr/bin/env python3
"""Shared helpers for the lexicality re-certification evaluation.

Pure re-analysis over archived iteration-1 / iteration-2 artifacts plus a
forward-pass-only re-encode of already-logged text.  Every archived code path
that defines an outcome (the refusal-onset regex, the axis fitting, the r_t
observable) is IMPORTED from the archive rather than re-implemented.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------
# Archive layout
# --------------------------------------------------------------------------
ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
EXP1 = ROOT / "iter_2/gen_art/gen_art_experiment_1"
EXP2 = ROOT / "iter_2/gen_art/gen_art_experiment_2"
AUDIT = ROOT / "iter_2/gen_art/gen_art_experiment_3"          # judge audit
ITER1_GEN = ROOT / "iter_1/gen_art/gen_art_experiment_3"      # 3,365 archived gens
DATASET = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGS = HERE / "figures"

CHECKPOINTS = [
    "instruct_0p6", "base_0p6", "abliterated_0p6",
    "instruct_1p7", "base_1p7", "abliterated_1p7",
]
AXES_MAIN = ["A_canned", "B_paraphrase", "C_stylistic", "D_random0", "E_prompt_contrast"]
AB = ("A_canned", "B_paraphrase")

# EXP1 model configuration (verbatim from EXP1 method.py MODELS)
MODEL_CFG = {
    "base_0p6": {"repo": "Qwen/Qwen3-0.6B-Base", "render": "plain"},
    "instruct_0p6": {"repo": "Qwen/Qwen3-0.6B", "render": "chatml"},
    "abliterated_0p6": {"repo": "mlabonne/Qwen3-0.6B-abliterated", "render": "chatml"},
    "base_1p7": {"repo": "Qwen/Qwen3-1.7B-Base", "render": "plain"},
    "instruct_1p7": {"repo": "Qwen/Qwen3-1.7B", "render": "chatml"},
    "abliterated_1p7": {"repo": "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2",
                        "render": "chatml"},
}
# iteration-1 archive member -> EXP1 checkpoint key (same repos, 0.6B anchor lineage)
ITER1_MEMBER_MAP = {
    "qwen3_base": "base_0p6",
    "qwen3_instruct": "instruct_0p6",
    "qwen3_abliterated": "abliterated_0p6",
}
# EXP2 breadth-panel member -> EXP1 checkpoint key (l1 = Qwen3-0.6B, l2 = Qwen3-1.7B)
EXP2_MEMBER_MAP = {
    "l1_base": "base_0p6", "l1_instruct": "instruct_0p6",
    "l1_abliterated": "abliterated_0p6",
    "l2_base": "base_1p7", "l2_instruct": "instruct_1p7",
}
# NOTE: EXP2 l2_abliterated is huihui-ai Qwen3-1.7B-abliterated-v2 == EXP1 abliterated_1p7
EXP2_MEMBER_MAP["l2_abliterated"] = "abliterated_1p7"

# Pre-registered constants
DELTA_MARGIN = 0.10
CHANCE_BAND = (0.40, 0.60)
MIN_PER_CLASS = 40
N_BOOT = 2000
BOOT_SEED = 20260812


# --------------------------------------------------------------------------
# Archive code import (verbatim reuse)
# --------------------------------------------------------------------------
def import_exp1_modules():
    """Import EXP1's classify / axes / direction / models modules verbatim."""
    if str(EXP1) not in sys.path:
        sys.path.insert(0, str(EXP1))
    import axes as AX          # noqa: N812
    import classify as CL      # noqa: N812
    import direction as DIR    # noqa: N812
    import models as MD        # noqa: N812
    return AX, CL, DIR, MD


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path):
    with open(p) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def load_json(p: Path):
    return json.loads(Path(p).read_text())


def model_meta(key: str) -> dict:
    return load_json(EXP1 / f"results/model_{key}.json")


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
try:                                     # fast tie-aware ranking (identical result)
    from scipy.stats import rankdata as _rankdata
except ImportError:                      # pragma: no cover
    _rankdata = None


def auroc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Rank AUROC with tie handling (identical to EXP1 direction.auroc)."""
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    n1, n0 = len(pos), len(neg)
    if n1 == 0 or n0 == 0:
        return float("nan")
    if _rankdata is not None:
        r = _rankdata(np.concatenate([pos, neg]), method="average")
        return float((r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
    x = np.concatenate([pos, neg])
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    ranks[order] = np.arange(1, len(x) + 1, dtype=float)
    sx = x[order]
    i = 0
    while i < len(sx):
        j = i
        while j + 1 < len(sx) and sx[j + 1] == sx[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = ranks[order[i:j + 1]].mean()
        i = j + 1
    n1, n0 = len(pos), len(neg)
    return float((ranks[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cohens_d(pos: np.ndarray, neg: np.ndarray) -> float:
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
    """Yield index arrays for a bootstrap that resamples CLUSTERS with replacement."""
    rng = np.random.default_rng(seed)
    uniq = np.unique(clusters)
    idx_by_c = {c: np.flatnonzero(clusters == c) for c in uniq}
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        yield np.concatenate([idx_by_c[c] for c in pick])


def boot_ci(vals: list[float], lo: float = 2.5, hi: float = 97.5):
    v = np.asarray([x for x in vals if np.isfinite(x)], dtype=float)
    if v.size < 20:
        return (float("nan"), float("nan"))
    return (float(np.percentile(v, lo)), float(np.percentile(v, hi)))


def boot_p_two_sided(vals: list[float], null: float = 0.0) -> float:
    """Bootstrap two-sided p for H0: statistic == null (percentile inversion)."""
    v = np.asarray([x for x in vals if np.isfinite(x)], dtype=float)
    if v.size < 20:
        return float("nan")
    frac = float(np.mean(v <= null))
    p = 2 * min(frac, 1 - frac)
    return float(min(1.0, max(1.0 / (v.size + 1), p)))


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = [(k, v) for k, v in pvals.items() if np.isfinite(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out, prev = {}, 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - i) * p))
        out[k] = adj
        prev = adj
    for k, v in pvals.items():
        out.setdefault(k, float("nan"))
    return out


def cohens_kappa(a: list, b: list) -> dict:
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


def pearson(x, y) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or x.std() < 1e-12 or y.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def ols_r2(x, y) -> dict:
    """Regress y on x (with intercept); return slope/intercept/R^2/residuals."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    X = np.stack([np.ones_like(x), x], axis=1)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    resid = y - pred
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / ss_tot if ss_tot > 0 else float("nan")
    return {"intercept": float(beta[0]), "slope": float(beta[1]),
            "r2": float(r2), "resid": resid}


# --------------------------------------------------------------------------
# Text statistics (degeneracy)
# --------------------------------------------------------------------------
def word_tokens(text: str) -> list[str]:
    return [w for w in text.replace("\n", " ").split(" ") if w]


def distinct_n_words(text: str, n: int = 3) -> float:
    w = word_tokens(text)
    if len(w) < n:
        return 1.0
    grams = [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]
    return len(set(grams)) / len(grams)


def max_ngram_repeat(text: str, n: int = 5) -> int:
    w = word_tokens(text)
    if len(w) < n:
        return 0
    from collections import Counter
    c = Counter(tuple(w[i:i + n]) for i in range(len(w) - n + 1))
    return int(max(c.values()))


def degeneracy_stats(text: str) -> dict:
    return {"distinct3": float(distinct_n_words(text, 3)),
            "max_rep5": int(max_ngram_repeat(text, 5)),
            "n_words": len(word_tokens(text))}


# --------------------------------------------------------------------------
# Rendering (verbatim conventions from EXP1 models.py)
# --------------------------------------------------------------------------
def make_render(tok, mode: str):
    from models import render_chatml, render_plain
    if mode == "plain":
        return render_plain
    return lambda t: render_chatml(tok, t)


def jp(rel: str, ptr: str) -> str:
    """Build a provenance pointer 'relative/path.json#/json/pointer'."""
    return f"{rel}#{ptr}"
