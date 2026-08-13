#!/usr/bin/env python3
"""Statistics beyond the iteration-1 toolkit: Wilson CIs, the within-vs-across
lineage variance decomposition, exhaustive permutation p-values for Spearman at
small n, and the headline paired bootstrap of (rho_alpha50 - rho_AMS)."""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import rankdata, spearmanr

BOOT_SEED = 20260812


def wilson_ci(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def rate_block(labels, positive) -> dict:
    n = len(labels)
    k = sum(1 for x in labels if x == positive)
    lo, hi = wilson_ci(k, n)
    return {"n": n, "k": k, "rate": (k / n) if n else None, "ci": [lo, hi]}


def cohens_kappa(a, b) -> float | None:
    a = np.asarray(a, dtype=bool)
    b = np.asarray(b, dtype=bool)
    if a.size == 0 or a.size != b.size:
        return None
    po = float((a == b).mean())
    pe = float(a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()))
    if abs(1 - pe) < 1e-12:
        return None
    return (po - pe) / (1 - pe)


# --------------------------------------------------------------------------
# H1''' -- the triage premise
# --------------------------------------------------------------------------
def variance_decomposition(table: list[dict], value_key: str = "value",
                           n_boot: int = 2000, seed: int = BOOT_SEED) -> dict:
    """table rows: {lineage, level, value}.

    sigma^2_within  = mean over lineages of the within-lineage variance across levels
    sigma^2_across  = mean over levels of the across-lineage variance at that level
    ratio           = within / across   ( > 1  => the metric TRANSFERS: a lineage's
                      safety levels are further apart than two lineages at the same
                      level, which is what a triage user needs )
    Bootstrap resamples LINEAGES, the pre-registered resampling unit.
    """
    rows = [r for r in table if r.get(value_key) is not None]
    lineages = sorted({r["lineage"] for r in rows})
    levels = sorted({r["level"] for r in rows})

    def _stats(sub):
        by_lin: dict[str, list[float]] = {}
        by_lev: dict[str, list[float]] = {}
        for r in sub:
            by_lin.setdefault(r["lineage"], []).append(float(r[value_key]))
            by_lev.setdefault(r["level"], []).append(float(r[value_key]))
        w = [np.var(v, ddof=1) for v in by_lin.values() if len(v) > 1]
        a = [np.var(v, ddof=1) for v in by_lev.values() if len(v) > 1]
        if not w or not a:
            return None, None, None
        wm, am = float(np.mean(w)), float(np.mean(a))
        return wm, am, (wm / am if am > 1e-12 else None)

    within, across, ratio = _stats(rows)
    boot = []
    rng = np.random.default_rng(seed)
    if lineages:
        for _ in range(n_boot):
            pick = rng.choice(len(lineages), size=len(lineages), replace=True)
            sub = []
            for j, li in enumerate(pick):
                for r in rows:
                    if r["lineage"] == lineages[li]:
                        rr = dict(r)
                        rr["lineage"] = f"{r['lineage']}#{j}"
                        sub.append(rr)
            _, _, rt = _stats(sub)
            if rt is not None and np.isfinite(rt):
                boot.append(rt)
    ci = (
        [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
        if len(boot) >= 50 else None
    )
    if ratio is None or ci is None:
        label = "UNDERPOWERED"
    elif ci[0] > 1.0:
        label = "TRANSFERS"
    elif ci[1] < 1.0:
        label = "DOES_NOT_TRANSFER"
    else:
        label = "AMBIGUOUS"
    return {
        "n_lineages": len(lineages), "n_levels": len(levels), "n_members": len(rows),
        "sigma2_within_lineage": within, "sigma2_across_lineage": across,
        "ratio_within_over_across": ratio, "ratio_ci": ci, "n_boot_valid": len(boot),
        "verdict": label,
    }


def rank_consistency(table: list[dict], value_key: str = "value") -> dict:
    """Does the within-lineage ORDERING of levels match the pooled ordering?

    This is what a triage user actually needs: 'does instruct always sit
    below/above its abliterated sibling?'.
    """
    rows = [r for r in table if r.get(value_key) is not None]
    by_level: dict[str, list[float]] = {}
    for r in rows:
        by_level.setdefault(r["level"], []).append(float(r[value_key]))
    pooled_order = sorted(by_level, key=lambda k: np.mean(by_level[k]))
    pooled_rank = {lv: i for i, lv in enumerate(pooled_order)}

    by_lin: dict[str, list[dict]] = {}
    for r in rows:
        by_lin.setdefault(r["lineage"], []).append(r)
    matches, checked, detail = 0, 0, {}
    for lin, rs in sorted(by_lin.items()):
        if len(rs) < 2:
            detail[lin] = "single_member"
            continue
        local = sorted(rs, key=lambda r: float(r[value_key]))
        local_levels = [r["level"] for r in local]
        expect = sorted(local_levels, key=lambda lv: pooled_rank[lv])
        ok = local_levels == expect
        checked += 1
        matches += int(ok)
        detail[lin] = {"observed_order": local_levels, "pooled_order": expect, "match": ok}
    return {
        "pooled_level_order_low_to_high": pooled_order,
        "n_lineages_checked": checked,
        "n_matching": matches,
        "fraction_matching": (matches / checked) if checked else None,
        "per_lineage": detail,
    }


# --------------------------------------------------------------------------
# D3 -- the headline comparison
# --------------------------------------------------------------------------
def _spearman(x, y) -> float | None:
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.size < 3 or np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return None
    return float(spearmanr(x, y).statistic)


def spearman_with_permutation(x, y, max_exact: int = 40320) -> dict:
    """Spearman rho with an EXHAUSTIVE permutation p when n! is small enough, so
    the small-n ceiling on the achievable p is visible rather than hidden."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = x.size
    rho = _spearman(x, y)
    if rho is None:
        return {"rho": None, "n": int(n), "p_permutation": None, "p_min_achievable": None,
                "exhaustive": False}
    nfac = math.factorial(n)
    rx = rankdata(x)
    ry = rankdata(y)
    if nfac <= max_exact:
        cnt = 0
        for perm in itertools.permutations(range(n)):
            r = _spearman(rx, ry[list(perm)])
            if r is not None and abs(r) >= abs(rho) - 1e-12:
                cnt += 1
        return {"rho": rho, "n": int(n), "p_permutation": cnt / nfac,
                "p_min_achievable": 2.0 / nfac, "exhaustive": True, "n_permutations": nfac}
    rng = np.random.default_rng(BOOT_SEED)
    reps = 20000
    cnt = 0
    for _ in range(reps):
        r = _spearman(rx, rng.permutation(ry))
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            cnt += 1
    return {"rho": rho, "n": int(n), "p_permutation": (cnt + 1) / (reps + 1),
            "p_min_achievable": 1.0 / (reps + 1), "exhaustive": False, "n_permutations": reps}


def paired_rho_delta(units: list[dict], key_a: str, key_b: str, key_y: str,
                     n_boot: int = 5000, seed: int = BOOT_SEED) -> dict:
    """DELTA = Spearman(a, y) - Spearman(b, y), PAIRED bootstrap over the SAME
    resampled units (lineages). Sign convention: DELTA > 0 means alpha_50
    (key_a) tracks behaviour better than AMS (key_b)."""
    rows = [u for u in units if u.get(key_a) is not None and u.get(key_b) is not None
            and u.get(key_y) is not None]
    if len(rows) < 3:
        return {"n": len(rows), "delta": None, "ci": None, "rho_a": None, "rho_b": None}
    a = np.array([u[key_a] for u in rows], dtype=float)
    b = np.array([u[key_b] for u in rows], dtype=float)
    y = np.array([u[key_y] for u in rows], dtype=float)
    ra, rb = _spearman(a, y), _spearman(b, y)
    delta = (ra - rb) if (ra is not None and rb is not None) else None
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(rows), size=len(rows))
        r1, r2 = _spearman(a[idx], y[idx]), _spearman(b[idx], y[idx])
        if r1 is not None and r2 is not None:
            boot.append(r1 - r2)
    ci = (
        [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
        if len(boot) >= 50 else None
    )
    # Leave-one-unit-out jackknife: with n this small a single lineage can move
    # rho across most of its range, and the reader must be able to see that.
    jack = []
    for i in range(len(rows)):
        m = [j for j in range(len(rows)) if j != i]
        r1, r2 = _spearman(a[m], y[m]), _spearman(b[m], y[m])
        jack.append({"dropped": rows[i].get("lineage", i), "rho_a": r1, "rho_b": r2,
                     "delta": (r1 - r2) if (r1 is not None and r2 is not None) else None})
    ja = [j["rho_a"] for j in jack if j["rho_a"] is not None]
    jb = [j["rho_b"] for j in jack if j["rho_b"] is not None]
    return {
        "n": len(rows), "rho_a": ra, "rho_b": rb, "delta": delta, "ci": ci,
        "jackknife": jack,
        "jackknife_rho_a_range": [min(ja), max(ja)] if ja else None,
        "jackknife_rho_b_range": [min(jb), max(jb)] if jb else None,
        "n_boot_valid": len(boot),
        "frac_positive": float(np.mean(np.asarray(boot) > 0)) if boot else None,
        "perm_a": spearman_with_permutation(a, y),
        "perm_b": spearman_with_permutation(b, y),
        "winner": (
            None if delta is None or ci is None
            else ("alpha_50" if ci[0] > 0 else ("AMS" if ci[1] < 0 else "TIE_CI_INCLUDES_0"))
        ),
    }


def bootstrap_mean(values, n_boot: int = 5000, seed: int = BOOT_SEED) -> dict:
    v = np.asarray([x for x in values if x is not None and np.isfinite(x)], dtype=float)
    if v.size == 0:
        return {"n": 0, "mean": None, "ci": None}
    rng = np.random.default_rng(seed)
    m = v[rng.integers(0, v.size, size=(n_boot, v.size))].mean(axis=1)
    return {
        "n": int(v.size), "mean": float(v.mean()),
        "sd": float(v.std(ddof=1)) if v.size > 1 else 0.0,
        "median": float(np.median(v)),
        "ci": [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))],
    }


def bootstrap_paired(values_a, values_b, n_boot: int = 5000, seed: int = BOOT_SEED) -> dict:
    pairs = [(a, b) for a, b in zip(values_a, values_b)
             if a is not None and b is not None and np.isfinite(a) and np.isfinite(b)]
    if len(pairs) < 2:
        return {"n": len(pairs), "mean_diff": None, "ci": None}
    d = np.array([a - b for a, b in pairs], dtype=float)
    rng = np.random.default_rng(seed)
    m = d[rng.integers(0, d.size, size=(n_boot, d.size))].mean(axis=1)
    return {
        "n": int(d.size), "mean_diff": float(d.mean()),
        "ci": [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))],
        "frac_positive": float((d > 0).mean()),
    }
