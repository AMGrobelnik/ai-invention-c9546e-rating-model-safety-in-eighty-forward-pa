#!/usr/bin/env python3
"""Shared statistics helpers for the wobble re-analysis.

Everything here is either a thin wrapper around the ARCHIVED spi/ library
(imported verbatim so estimator definitions cannot drift) or a small,
self-contained addition (TOST, exact permutation, Cliff's delta, AUROC CIs).
"""

from __future__ import annotations

import hashlib
import itertools
import math
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy import stats

from spi.indicators import paired_bootstrap_diff, wilson_ci  # noqa: F401  (re-export)

BOOT_REPS = 10_000
BOOT_SEED = 20260812


# --------------------------------------------------------------------------- #
# provenance
# --------------------------------------------------------------------------- #

def sha256_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_of_tree(root: Path, pattern: str = "**/*.jsonl") -> dict[str, Any]:
    """Content-independent but reproducible fingerprint of a file tree:
    hash over the sorted (relative path, size) list plus the file count."""
    files = sorted(root.glob(pattern))
    h = hashlib.sha256()
    total = 0
    for f in files:
        n = f.stat().st_size
        total += n
        h.update(f"{f.relative_to(root)}:{n}\n".encode())
    return {"root": str(root), "n_files": len(files),
            "total_bytes": total, "sha256_of_name_size_index": h.hexdigest()}


# --------------------------------------------------------------------------- #
# paired statistics over prompts
# --------------------------------------------------------------------------- #

def _clean_pairs(a: dict[str, float], b: dict[str, float]) -> tuple[np.ndarray, list[str]]:
    keys = sorted(set(a) & set(b))
    ok = [k for k in keys
          if a[k] is not None and b[k] is not None
          and np.isfinite(a[k]) and np.isfinite(b[k])]
    return np.asarray([a[k] - b[k] for k in ok], dtype=np.float64), ok


def bootstrap_mean(d: np.ndarray, *, n_reps: int = BOOT_REPS, seed: int = BOOT_SEED,
                   alpha: float = 0.05) -> dict[str, Any]:
    """Percentile bootstrap of the mean of a vector of paired differences."""
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)
    if d.size < 2:
        return {"diff": float(d[0]) if d.size == 1 else None, "ci_lo": None,
                "ci_hi": None, "n_pairs": int(d.size), "ci_excludes_zero": None,
                "sd": None, "boot_p_two_sided": None}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(n_reps, d.size))
    draws = d[idx].mean(axis=1)
    lo = float(np.percentile(draws, 100 * alpha / 2))
    hi = float(np.percentile(draws, 100 * (1 - alpha / 2)))
    # two-sided bootstrap p: 2 * min(frac of draws <= 0, frac >= 0)
    frac_le = float((draws <= 0).mean())
    frac_ge = float((draws >= 0).mean())
    p = float(min(1.0, 2.0 * min(frac_le, frac_ge)))
    return {"diff": float(d.mean()), "ci_lo": lo, "ci_hi": hi,
            "n_pairs": int(d.size), "ci_excludes_zero": bool(lo > 0 or hi < 0),
            "sd": float(d.std(ddof=1)), "boot_p_two_sided": p,
            "n_reps": int(n_reps), "alpha": float(alpha)}


def bootstrap_ci_level(d: np.ndarray, *, level: float, n_reps: int = BOOT_REPS,
                       seed: int = BOOT_SEED + 1) -> tuple[float | None, float | None]:
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)
    if d.size < 2:
        return None, None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(n_reps, d.size))
    draws = d[idx].mean(axis=1)
    a = (1.0 - level) / 2.0
    return float(np.percentile(draws, 100 * a)), float(np.percentile(draws, 100 * (1 - a)))


def wilcoxon_signed_rank(d: np.ndarray) -> dict[str, Any]:
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)
    nz = d[d != 0]
    if nz.size < 3:
        return {"stat": None, "p": None, "n": int(nz.size), "mode": "too_few"}
    mode = "exact" if nz.size <= 25 else "approx"
    try:
        res = stats.wilcoxon(nz, alternative="two-sided", mode=mode)
    except TypeError:  # scipy >= 1.13 renamed the kwarg
        res = stats.wilcoxon(nz, alternative="two-sided", method=mode)
    return {"stat": float(res.statistic), "p": float(res.pvalue),
            "n": int(nz.size), "mode": mode}


def cliffs_delta(x: Sequence[float], y: Sequence[float]) -> float:
    """Cliff's delta of x vs y (unpaired form, used as a distribution-free
    effect size companion to the paired bootstrap)."""
    a = np.asarray([v for v in x if np.isfinite(v)], dtype=np.float64)
    b = np.asarray([v for v in y if np.isfinite(v)], dtype=np.float64)
    if a.size == 0 or b.size == 0:
        return float("nan")
    gt = float((a[:, None] > b[None, :]).sum())
    lt = float((a[:, None] < b[None, :]).sum())
    return (gt - lt) / (a.size * b.size)


def paired_cliffs_delta(d: np.ndarray) -> float:
    """Paired sign-based effect size: P(d>0) - P(d<0)."""
    d = np.asarray([v for v in d if np.isfinite(v)], dtype=np.float64)
    if d.size == 0:
        return float("nan")
    return float((d > 0).mean() - (d < 0).mean())


def tost(d: np.ndarray, margin: float) -> dict[str, Any]:
    """Two-one-sided-tests for equivalence of the mean of d to 0 within
    +/- margin. Returns both the parametric TOST p and the bootstrap 90% CI
    (the CI-inclusion rule is the operational verdict)."""
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=np.float64)
    out: dict[str, Any] = {"margin": float(margin), "n": int(d.size)}
    if d.size < 3:
        out.update({"p_tost": None, "ci90_lo": None, "ci90_hi": None,
                    "equivalent": None})
        return out
    m = float(d.mean())
    se = float(d.std(ddof=1) / math.sqrt(d.size))
    df = d.size - 1
    if se <= 0:
        p_lo = p_hi = 0.0
    else:
        p_lo = float(stats.t.sf((m + margin) / se, df))       # H0: mu <= -margin
        p_hi = float(stats.t.cdf((m - margin) / se, df))      # H0: mu >= +margin
    lo90, hi90 = bootstrap_ci_level(d, level=0.90)
    out.update({
        "mean": m, "se": se, "df": int(df),
        "p_tost": float(max(p_lo, p_hi)), "p_lower": p_lo, "p_upper": p_hi,
        "ci90_lo": lo90, "ci90_hi": hi90,
        "equivalent": bool(lo90 is not None and lo90 > -margin and hi90 < margin),
    })
    return out


def tost_sample_size(sd: float, margin: float, *, alpha: float = 0.05,
                     power: float = 0.80) -> int | None:
    """n per (paired) sample for a TOST at `margin` with true effect 0."""
    if not np.isfinite(sd) or sd <= 0 or margin <= 0:
        return None
    z_a = stats.norm.ppf(1 - alpha)
    z_b = stats.norm.ppf(1 - (1 - power) / 2)
    return int(math.ceil(((z_a + z_b) ** 2) * (sd ** 2) / (margin ** 2)))


def holm(pvals: dict[str, float]) -> dict[str, float]:
    """Holm-Bonferroni step-down adjusted p-values."""
    items = [(k, v) for k, v in pvals.items() if v is not None and np.isfinite(v)]
    m = len(items)
    items.sort(key=lambda kv: kv[1])
    adj: dict[str, float] = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        val = min(1.0, (m - i) * p)
        running = max(running, val)
        adj[k] = float(running)
    for k, v in pvals.items():
        if k not in adj:
            adj[k] = float("nan")
    return adj


# --------------------------------------------------------------------------- #
# AUROC
# --------------------------------------------------------------------------- #

def auroc_mannwhitney(pos: Sequence[float], neg: Sequence[float]) -> dict[str, Any]:
    a = np.asarray([v for v in pos if np.isfinite(v)], dtype=np.float64)
    b = np.asarray([v for v in neg if np.isfinite(v)], dtype=np.float64)
    if a.size == 0 or b.size == 0:
        return {"auroc": None, "n_pos": int(a.size), "n_neg": int(b.size),
                "ci_lo": None, "ci_hi": None, "p": None}
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    auc = float(u / (a.size * b.size))
    ci = auroc_hanley_ci(auc, a.size, b.size)
    return {"auroc": auc, "n_pos": int(a.size), "n_neg": int(b.size),
            "ci_lo": ci["lo"], "ci_hi": ci["hi"], "se": ci["se"], "p": float(p)}


def auroc_hanley_ci(auc: float, n_pos: int, n_neg: int, z: float = 1.96) -> dict[str, float]:
    """Hanley & McNeil (1982) standard error and normal CI for an AUROC."""
    if not np.isfinite(auc) or n_pos <= 0 or n_neg <= 0:
        return {"se": float("nan"), "lo": float("nan"), "hi": float("nan")}
    q1 = auc / (2 - auc)
    q2 = 2 * auc ** 2 / (1 + auc)
    var = (auc * (1 - auc)
           + (n_pos - 1) * (q1 - auc ** 2)
           + (n_neg - 1) * (q2 - auc ** 2)) / (n_pos * n_neg)
    se = float(math.sqrt(max(var, 0.0)))
    return {"se": se, "lo": float(max(0.0, auc - z * se)),
            "hi": float(min(1.0, auc + z * se))}


# --------------------------------------------------------------------------- #
# exact permutation Spearman for tiny n
# --------------------------------------------------------------------------- #

def exact_spearman_permutation(x: Sequence[float], y: Sequence[float]) -> dict[str, Any]:
    """Enumerate every assignment of the x-ranks to the y-ranks (n! of them) and
    return the exact null distribution of Spearman rho, plus exact p-values.

    Tie-aware: ranks are computed with 'average' tie handling, and DISTINCT
    attainable rho values are enumerated (with their multiplicities) rather
    than assuming n! distinct values."""
    xr = stats.rankdata(np.asarray(x, dtype=np.float64), method="average")
    yr = stats.rankdata(np.asarray(y, dtype=np.float64), method="average")
    n = len(xr)
    obs = float(stats.spearmanr(xr, yr).statistic)
    rhos: list[float] = []
    for perm in itertools.permutations(range(n)):
        rhos.append(float(stats.spearmanr(xr[list(perm)], yr).statistic))
    arr = np.asarray(rhos, dtype=np.float64)
    n_perm = arr.size
    tol = 1e-9
    p_greater = float((arr >= obs - tol).mean())
    p_less = float((arr <= obs + tol).mean())
    p_two = float(min(1.0, (np.abs(arr) >= abs(obs) - tol).mean()))
    uniq = sorted({round(v, 10) for v in arr if np.isfinite(v)})
    finite = arr[np.isfinite(arr)]
    return {
        "rho_observed": obs,
        "n_permutations": int(n_perm),
        "n_distinct_rho": int(len(uniq)),
        "p_one_sided_greater": p_greater,
        "p_one_sided_less": p_less,
        "p_two_sided": p_two,
        "min_attainable_one_sided_p": float(1.0 / n_perm),
        "min_attainable_two_sided_p": float(
            (np.abs(finite) >= np.abs(finite).max() - tol).mean()) if finite.size else None,
        "max_attainable_abs_rho": float(np.abs(finite).max()) if finite.size else None,
        "null_rho_values": [float(v) for v in uniq],
    }


def n_resolvable_levels(rates: dict[str, dict[str, float]]) -> dict[str, Any]:
    """Greedy chain-count of ground-truth levels whose Wilson CIs do not overlap.
    `rates` maps model -> {'p':..., 'lo':..., 'hi':...}."""
    items = sorted(rates.items(), key=lambda kv: kv[1]["p"])
    groups: list[list[str]] = []
    for name, r in items:
        placed = False
        for g in groups:
            if all(not (rates[o]["hi"] < r["lo"] or r["hi"] < rates[o]["lo"]) for o in g):
                g.append(name)
                placed = True
                break
        if not placed:
            groups.append([name])
    return {"n_levels": len(groups), "groups": groups,
            "detail": {k: dict(v) for k, v in rates.items()}}
