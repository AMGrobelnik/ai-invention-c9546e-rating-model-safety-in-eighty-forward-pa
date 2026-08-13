#!/usr/bin/env python3
"""Dual-aggregation helpers and the permutation test for a rho DIFFERENCE.

The paper-wide H-U repair requires every correlation at BOTH aggregation units:
MEMBER level with a lineage-clustered resample, and LINEAGE-AGGREGATED units.
`aggregate_by_lineage` produces the second unit; the clustered estimators in
lib_iter3.statsx then serve both (at the aggregated unit each row IS its own
cluster, so the same code path gives the ordinary unit bootstrap).

`lineage_permutation_p_delta` is the STEP-3(c) statistic: a permutation p for
Delta = rho(score, y) - rho(reference, y). Permuting a single rho would be the
wrong null here -- Delta is a difference between two rhos sharing the SAME y, so
the permutation must move the y-blocks and recompute BOTH rhos on every draw.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import rankdata, spearmanr

BOOT_SEED = 20260812


def _rho(a: np.ndarray, b: np.ndarray) -> float | None:
    if a.size < 3 or np.allclose(a, a[0]) or np.allclose(b, b[0]):
        return None
    r = spearmanr(a, b).statistic
    return None if (r is None or not np.isfinite(r)) else float(r)


def aggregate_by_lineage(values: dict[str, list], y: list, lineages: list) -> dict:
    """Per-lineage MEAN of every named score column and of y.

    Rows where y or the score is missing are dropped from that column's mean; a
    lineage contributes a unit only when at least one member survives.
    """
    labels = sorted({L for L, yy in zip(lineages, y) if yy is not None})
    out: dict[str, list] = {k: [] for k in values}
    ys: list[float] = []
    ns: list[int] = []
    keep_labels: list[str] = []
    for L in labels:
        idx = [i for i, (lab, yy) in enumerate(zip(lineages, y))
               if lab == L and yy is not None]
        if not idx:
            continue
        keep_labels.append(L)
        ns.append(len(idx))
        ys.append(float(np.mean([float(y[i]) for i in idx])))
        for k, col in values.items():
            vals = [float(col[i]) for i in idx
                    if col[i] is not None and np.isfinite(float(col[i]))]
            out[k].append(float(np.mean(vals)) if vals else None)
    return {"labels": keep_labels, "y": ys, "scores": out, "n_members": ns,
            "n_units": len(keep_labels)}


def lineage_permutation_p_delta(score, reference, y, lineages,
                                max_exact_factorial: int = 40320,
                                n_random: int = 200000,
                                seed: int = BOOT_SEED) -> dict:
    """Permutation p for Delta = rho(score, y) - rho(reference, y).

    Lineage blocks of y are permuted onto lineage blocks of the scores exactly as
    lib_iter3.statsx.lineage_permutation_p does (member j of L pairs with member
    j mod m of pi(L)), so the exchangeable unit is the CLUSTER. The identity
    permutation is always included and always reproduces Delta, so the attainable
    floor is 1/K (exhaustive) or 1/(n_random+1) (Monte Carlo), never 0.
    """
    idx = [i for i in range(len(y))
           if score[i] is not None and reference[i] is not None and y[i] is not None
           and np.isfinite(float(score[i])) and np.isfinite(float(reference[i]))]
    if len(idx) < 3:
        return {"delta": None, "p_permutation": None, "n": len(idx)}
    a = np.array([float(score[i]) for i in idx])
    c = np.array([float(reference[i]) for i in idx])
    b = np.array([float(y[i]) for i in idx])
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    n_l = len(uniq)
    blocks = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    ra, rc, rb = rankdata(a), rankdata(c), rankdata(b)
    d0a, d0c = _rho(ra, rb), _rho(rc, rb)
    if d0a is None or d0c is None or n_l < 3:
        return {"delta": None, "p_permutation": None, "n": len(idx),
                "n_lineages": n_l}
    delta = d0a - d0c

    def _perm_delta(perm) -> float | None:
        yy = np.empty_like(rb)
        for src_i, L in enumerate(uniq):
            tgt = blocks[uniq[perm[src_i]]]
            for j, member in enumerate(blocks[L]):
                yy[member] = rb[tgt[j % len(tgt)]]
        r1, r2 = _rho(ra, yy), _rho(rc, yy)
        return None if (r1 is None or r2 is None) else r1 - r2

    nfac = math.factorial(n_l)
    if nfac <= max_exact_factorial:
        cnt = 0
        for perm in itertools.permutations(range(n_l)):
            d = _perm_delta(perm)
            if d is not None and abs(d) >= abs(delta) - 1e-12:
                cnt += 1
        return {"delta": delta, "n": len(idx), "n_lineages": n_l,
                "p_permutation": cnt / nfac, "p_min_achievable": 1.0 / nfac,
                "exhaustive": True, "n_permutations": nfac, "n_extreme": cnt,
                "resolution_note": f"exhaustive over {nfac} lineage permutations; "
                                   f"floor {1.0 / nfac:.3e}"}
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_random):
        d = _perm_delta(list(rng.permutation(n_l)))
        if d is not None and abs(d) >= abs(delta) - 1e-12:
            cnt += 1
    p = (cnt + 1) / (n_random + 1)
    return {"delta": delta, "n": len(idx), "n_lineages": n_l,
            "p_permutation": p, "p_min_achievable": 1.0 / (n_random + 1),
            "exhaustive": False, "n_permutations": n_random, "n_extreme": cnt,
            "resolution_note": (f"Monte Carlo over {n_random} lineage permutations "
                                f"plus the identity; floor {1.0 / (n_random + 1):.3e}; "
                                f"n_lineages! = {nfac:.3e} is too large to enumerate")}


def wilson_ci(k: int, n: int, z: float = 1.959963985) -> list[float]:
    if n <= 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [max(0.0, (c - h) / d), min(1.0, (c + h) / d)]


def ci_overlap(a: list[float] | None, b: list[float] | None) -> bool | None:
    if not a or not b:
        return None
    return not (a[1] < b[0] or b[1] < a[0])


def holm(pvals: dict[str, float | None]) -> dict[str, dict]:
    """Holm-Bonferroni over a named family; None p-values are passed through."""
    items = [(k, v) for k, v in pvals.items() if v is not None]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, dict] = {k: {"p_raw": v, "p_holm": None, "reject_at_0.05": None}
                            for k, v in pvals.items()}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - i) * p))
        running = adj
        out[k] = {"p_raw": p, "p_holm": adj, "reject_at_0.05": adj < 0.05}
    return out
