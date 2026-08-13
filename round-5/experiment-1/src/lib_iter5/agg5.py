#!/usr/bin/env python3
"""Aggregation units, block split and the pre-emptive controls.

Everything that iteration 3/4 already implemented is CALLED from
`lib_iter3/statsx.py` (byte-identical reuse); only the pieces that iteration 5
adds live here:

  * `collapse_to_lineage`  -- the LINEAGE aggregation unit. Iteration 4's
    lineage-aggregated column collapses each lineage to the MEAN of its members'
    score and the MEAN of its members' y; that rule is reproduced here and
    verified against iteration 4's published lineage-unit numbers.
  * `bootstrap_rho_units`  -- a plain n=K bootstrap over already-collapsed units.
  * `block_delta_rho`      -- rho(block A) - rho(block B) with a CI from a
    bootstrap that resamples lineages WITHIN each block and differences the two
    rhos on the SAME draw (the construction `statsx.paired_rho_delta_clustered`
    uses for its paired delta).
  * `partial_spearman`     -- Spearman partial correlation controlling for a
    third variable, with a lineage-clustered bootstrap CI.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata, spearmanr

from lib_iter3 import statsx as sx

BOOT_SEED = sx.BOOT_SEED
N_BOOT = sx.N_BOOT


def _finite_idx(*vectors) -> list[int]:
    n = len(vectors[0])
    keep = []
    for i in range(n):
        vals = [v[i] for v in vectors]
        if any(v is None for v in vals):
            continue
        try:
            if all(np.isfinite(float(v)) for v in vals):
                keep.append(i)
        except (TypeError, ValueError):
            continue
    return keep


def _rho(a: np.ndarray, b: np.ndarray) -> float | None:
    if a.size < 3 or np.allclose(a, a[0]) or np.allclose(b, b[0]):
        return None
    r = spearmanr(a, b).statistic
    return None if (r is None or not np.isfinite(r)) else float(r)


# --------------------------------------------------------------------------
# LINEAGE aggregation unit
# --------------------------------------------------------------------------
def collapse_to_lineage(x, y, lineages, rule: str = "mean") -> dict:
    """Collapse members to one point per lineage.

    `rule` is 'mean' -- the rule iteration 4 used, verified in this run's T0d
    replay against iteration 3's published lineage-unit rho of 0.929.
    """
    if rule not in ("mean", "median"):
        raise ValueError(f"unknown collapse rule {rule!r}")
    agg = np.mean if rule == "mean" else np.median
    idx = _finite_idx(x, y)
    groups: dict[str, list[int]] = {}
    for i in idx:
        groups.setdefault(lineages[i], []).append(i)
    order = sorted(groups)
    return {
        "lineages": order,
        "x": [float(agg([float(x[i]) for i in groups[L]])) for L in order],
        "y": [float(agg([float(y[i]) for i in groups[L]])) for L in order],
        "n_members_per_lineage": {L: len(groups[L]) for L in order},
        "rule": rule,
        "n_units": len(order),
        "n_members_used": len(idx),
    }


def bootstrap_rho_units(x, y, n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """Plain bootstrap over already-collapsed units (the LINEAGE unit)."""
    idx = _finite_idx(x, y)
    a = np.array([float(x[i]) for i in idx])
    b = np.array([float(y[i]) for i in idx])
    point = _rho(a, b)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        pick = rng.integers(0, a.size, size=a.size)
        r = _rho(a[pick], b[pick])
        if r is not None:
            boot.append(r)
    ci = ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
          if len(boot) >= 50 else None)
    p_asym = float(spearmanr(a, b).pvalue) if point is not None else None
    return {"rho": point, "n": int(a.size), "n_lineages": int(a.size),
            "ci95_unit_bootstrap": ci, "n_boot_valid": len(boot),
            "p_asymptotic": p_asym,
            "resampling_unit": "lineage (already collapsed; unit = row)"}


# --------------------------------------------------------------------------
# The block split: archived-19 vs new-33
# --------------------------------------------------------------------------
def block_delta_rho(x, y, lineages, blocks, block_a: str, block_b: str,
                    n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """rho(block_a) - rho(block_b) with a within-block lineage bootstrap.

    Each draw resamples the lineages of block A and the lineages of block B
    independently (with replacement, preserving each block's lineage count) and
    differences the two rhos computed on THAT draw, so the CI carries the
    covariance the two blocks share through nothing but the estimator itself.
    """
    idx = _finite_idx(x, y)
    a_all = np.array([float(x[i]) for i in idx])
    b_all = np.array([float(y[i]) for i in idx])
    blk = [blocks[i] for i in idx]
    lin = [lineages[i] for i in idx]

    def _block_pos(name):
        return [j for j, v in enumerate(blk) if v == name]

    pos_a, pos_b = _block_pos(block_a), _block_pos(block_b)
    rho_a = _rho(a_all[pos_a], b_all[pos_a]) if len(pos_a) >= 3 else None
    rho_b = _rho(a_all[pos_b], b_all[pos_b]) if len(pos_b) >= 3 else None
    delta = (rho_a - rho_b) if (rho_a is not None and rho_b is not None) else None

    def _by_lin(pos):
        d: dict[str, list[int]] = {}
        for j in pos:
            d.setdefault(lin[j], []).append(j)
        return d, sorted(d)

    la, ua = _by_lin(pos_a)
    lb, ub = _by_lin(pos_b)
    rng = np.random.default_rng(seed)
    boot = []
    if delta is not None and ua and ub:
        for _ in range(n_boot):
            sa: list[int] = []
            for k in rng.integers(0, len(ua), size=len(ua)):
                sa.extend(la[ua[k]])
            sb: list[int] = []
            for k in rng.integers(0, len(ub), size=len(ub)):
                sb.extend(lb[ub[k]])
            if len(sa) < 3 or len(sb) < 3:
                continue
            r1 = _rho(a_all[sa], b_all[sa])
            r2 = _rho(a_all[sb], b_all[sb])
            if r1 is not None and r2 is not None:
                boot.append(r1 - r2)
    ci = ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
          if len(boot) >= 50 else None)
    return {
        "block_a": block_a, "block_b": block_b,
        "n_a": len(pos_a), "n_b": len(pos_b),
        "n_lineages_a": len(ua), "n_lineages_b": len(ub),
        "rho_a": rho_a, "rho_b": rho_b, "delta": delta, "ci95": ci,
        "prob_delta_gt_0": float(np.mean(np.asarray(boot) > 0)) if boot else None,
        "n_boot_valid": len(boot),
        "verdict": (None if delta is None or ci is None else
                    ("A_HIGHER" if ci[0] > 0 else
                     ("B_HIGHER" if ci[1] < 0 else "TIE_CI_INCLUDES_0"))),
    }


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------
def partial_spearman(x, y, z, lineages=None, n_boot: int = N_BOOT,
                     seed: int = BOOT_SEED) -> dict:
    """Spearman partial correlation of (x, y) controlling for z.

    Ranks are taken once on the FULL analysed set, then x and y are residualised
    on z by ordinary least squares and the residuals correlated (Pearson of the
    rank residuals = the standard Spearman partial). When `lineages` is given a
    lineage-clustered bootstrap CI is added; the ranks are recomputed inside each
    draw so the statistic resampled is the one reported.
    """
    idx = _finite_idx(x, y, z)
    if len(idx) < 5:
        return {"partial_rho": None, "n": len(idx)}
    a = np.array([float(x[i]) for i in idx])
    b = np.array([float(y[i]) for i in idx])
    c = np.array([float(z[i]) for i in idx])

    def _pr(a_, b_, c_) -> float | None:
        if a_.size < 5:
            return None
        ra, rb, rc = rankdata(a_), rankdata(b_), rankdata(c_)
        if np.allclose(rc, rc[0]):
            return _rho(a_, b_)
        design = np.column_stack([np.ones_like(rc), rc])
        try:
            ea = ra - design @ np.linalg.lstsq(design, ra, rcond=None)[0]
            eb = rb - design @ np.linalg.lstsq(design, rb, rcond=None)[0]
        except np.linalg.LinAlgError:
            return None
        sa, sb_ = ea.std(), eb.std()
        if sa < 1e-12 or sb_ < 1e-12:
            return None
        v = float(np.corrcoef(ea, eb)[0, 1])
        return v if np.isfinite(v) else None

    point = _pr(a, b, c)
    out = {"partial_rho": point, "n": int(a.size),
           "rho_unadjusted": _rho(a, b),
           "rho_x_vs_control": _rho(a, c), "rho_y_vs_control": _rho(b, c),
           "control": "log10(param_count)"}
    if lineages is not None and point is not None:
        lin = [lineages[i] for i in idx]
        by: dict[str, list[int]] = {}
        for j, L in enumerate(lin):
            by.setdefault(L, []).append(j)
        uniq = sorted(by)
        rng = np.random.default_rng(seed)
        boot = []
        for _ in range(n_boot):
            sel: list[int] = []
            for k in rng.integers(0, len(uniq), size=len(uniq)):
                sel.extend(by[uniq[k]])
            if len(sel) < 5:
                continue
            r = _pr(a[sel], b[sel], c[sel])
            if r is not None:
                boot.append(r)
        out["ci95_lineage_clustered"] = (
            [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
            if len(boot) >= 50 else None)
        out["n_boot_valid"] = len(boot)
        out["n_lineages"] = len(uniq)
    return out


def subset(vectors: dict, keep: list[int]) -> dict:
    return {k: [v[i] for i in keep] for k, v in vectors.items()}
