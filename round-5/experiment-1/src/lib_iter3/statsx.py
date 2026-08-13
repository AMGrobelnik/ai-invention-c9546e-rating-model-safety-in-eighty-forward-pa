#!/usr/bin/env python3
"""Sign-oriented, lineage-clustered statistics for the discrimination matrix.

Everything here operates on ORIENTED scores (higher = safer) with the raw
unoriented form reported alongside. The resampling / permutation unit is the
LINEAGE, never the member.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import rankdata, spearmanr

BOOT_SEED = 20260812
N_BOOT = 10000

# reliability of the judged outcome, used for the disattenuation factor
JUDGE_SELF_AGREEMENT_FROZEN = 0.75  # iteration-2 experiment-3, arm1_frozen
JUDGE_SELF_AGREEMENT_REPAIRED = 0.9597  # arm2_repaired: the judge that produced y


def orient(values, sign: int) -> list[float | None]:
    return [None if v is None else sign * float(v) for v in values]


def _clean(x, y) -> tuple[np.ndarray, np.ndarray, list[int]]:
    idx = [i for i, (a, b) in enumerate(zip(x, y))
           if a is not None and b is not None
           and np.isfinite(float(a)) and np.isfinite(float(b))]
    return (np.array([float(x[i]) for i in idx]),
            np.array([float(y[i]) for i in idx]), idx)


def _rho(a: np.ndarray, b: np.ndarray) -> float | None:
    if a.size < 3 or np.allclose(a, a[0]) or np.allclose(b, b[0]):
        return None
    r = spearmanr(a, b).statistic
    return None if (r is None or not np.isfinite(r)) else float(r)


def spearman_basic(x, y) -> dict:
    a, b, idx = _clean(x, y)
    if a.size < 3:
        return {"rho": None, "p_asymptotic": None, "n": int(a.size)}
    rho = _rho(a, b)
    p = float(spearmanr(a, b).pvalue) if rho is not None else None
    return {"rho": rho, "p_asymptotic": p, "n": int(a.size)}


# --------------------------------------------------------------------------
# Lineage-clustered bootstrap
# --------------------------------------------------------------------------
def clustered_bootstrap_rho(x, y, lineages, n_boot: int = N_BOOT,
                            seed: int = BOOT_SEED) -> dict:
    """Resample LINEAGE IDs with replacement, take ALL members of each draw."""
    a, b, idx = _clean(x, y)
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    by_lin = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    point = _rho(a, b)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(uniq), size=len(uniq))
        sel: list[int] = []
        for k in pick:
            sel.extend(by_lin[uniq[k]])
        if len(sel) < 3:
            continue
        r = _rho(a[sel], b[sel])
        if r is not None:
            boot.append(r)
    ci = ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
          if len(boot) >= 50 else None)
    return {"rho": point, "n": int(a.size), "n_lineages": len(uniq),
            "ci95_lineage_clustered": ci, "n_boot_valid": len(boot),
            "resampling_unit": "lineage label (L1..L7)"}


# --------------------------------------------------------------------------
# Exhaustive permutation over LINEAGE label assignments
# --------------------------------------------------------------------------
def lineage_permutation_p(x, y, lineages, max_exact_factorial: int = 40320,
                          n_random: int = 100000, seed: int = BOOT_SEED) -> dict:
    """Permute which lineage's y-block is paired with which lineage's x-block.

    With unequal lineage sizes a permutation pi maps lineage L (size n_L) onto
    lineage pi(L) (size m); member j of L is paired with member (j mod m) of
    pi(L). This is deterministic, exhaustively enumerable over |lineages|!, and
    keeps the CLUSTER, not the member, as the exchangeable unit. The identity
    permutation is included and always reproduces |rho|, so the attainable floor
    is 1/K, not the 2/K that a reversal-symmetric permutation set would give.
    """
    a, b, idx = _clean(x, y)
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    n_l = len(uniq)
    blocks = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    rho = _rho(a, b)
    if rho is None or n_l < 3:
        return {"rho": rho, "n_lineages": n_l, "p_permutation": None,
                "p_min_achievable": None, "exhaustive": False}
    ra = rankdata(a)
    rb = rankdata(b)

    def _perm_rho(perm) -> float | None:
        yy = np.empty_like(rb)
        for src_i, L in enumerate(uniq):
            tgt = blocks[uniq[perm[src_i]]]
            for j, member in enumerate(blocks[L]):
                yy[member] = rb[tgt[j % len(tgt)]]
        return _rho(ra, yy)

    nfac = math.factorial(n_l)
    if nfac <= max_exact_factorial:
        cnt = 0
        for perm in itertools.permutations(range(n_l)):
            r = _perm_rho(perm)
            if r is not None and abs(r) >= abs(rho) - 1e-12:
                cnt += 1
        # The identity permutation is always counted (it reproduces rho exactly),
        # so the smallest attainable count is 1 and the floor is 1/nfac. The
        # conventional 2/nfac assumes the permutation set is symmetric under
        # reversal, which a CLUSTER permutation with unequal block sizes does not
        # guarantee; both are reported so no p is ever quoted below its floor.
        return {"rho": rho, "n_lineages": n_l, "p_permutation": cnt / nfac,
                "p_min_achievable": 1.0 / nfac,
                "p_min_two_sided_symmetric_reference": 2.0 / nfac,
                "floor_note": "identity permutation always counted -> floor 1/nfac; "
                              "2/nfac would require reversal symmetry, which unequal "
                              "lineage block sizes do not provide",
                "exhaustive": True,
                "n_permutations": nfac, "n_extreme": cnt}
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_random):
        r = _perm_rho(list(rng.permutation(n_l)))
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            cnt += 1
    return {"rho": rho, "n_lineages": n_l, "p_permutation": (cnt + 1) / (n_random + 1),
            "p_min_achievable": 1.0 / (n_random + 1), "exhaustive": False,
            "n_permutations": n_random, "n_extreme": cnt}


# --------------------------------------------------------------------------
# Leave-one-lineage-out jackknife
# --------------------------------------------------------------------------
def loo_lineage_jackknife(x, y, lineages) -> dict:
    a, b, idx = _clean(x, y)
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    folds = []
    for L in uniq:
        keep = [j for j, v in enumerate(lin) if v != L]
        r = _rho(a[keep], b[keep]) if len(keep) >= 3 else None
        folds.append({"dropped_lineage": L, "n_remaining": len(keep), "rho": r})
    vals = [f["rho"] for f in folds if f["rho"] is not None]
    signs = {int(np.sign(v)) for v in vals if abs(v) > 1e-12}
    return {
        "n_folds": len(uniq), "folds": folds,
        "rho_full": _rho(a, b),
        "range": [float(min(vals)), float(max(vals))] if vals else None,
        "spread": float(max(vals) - min(vals)) if vals else None,
        "sign_stable": (len(signs) <= 1) if vals else None,
        "n_valid_folds": len(vals),
    }


# --------------------------------------------------------------------------
# Paired bootstrap of (rho_score - rho_reference) on the SAME lineage draws
# --------------------------------------------------------------------------
def paired_rho_delta_clustered(score, reference, y, lineages,
                               n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    idx = [i for i in range(len(y))
           if score[i] is not None and reference[i] is not None and y[i] is not None]
    if len(idx) < 3:
        return {"n": len(idx), "delta": None, "ci95": None,
                "rho_score": None, "rho_reference": None}
    a = np.array([float(score[i]) for i in idx])
    c = np.array([float(reference[i]) for i in idx])
    b = np.array([float(y[i]) for i in idx])
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    by_lin = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    ra, rc = _rho(a, b), _rho(c, b)
    delta = (ra - rc) if (ra is not None and rc is not None) else None
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(uniq), size=len(uniq))
        sel: list[int] = []
        for k in pick:
            sel.extend(by_lin[uniq[k]])
        if len(sel) < 3:
            continue
        r1, r2 = _rho(a[sel], b[sel]), _rho(c[sel], b[sel])
        if r1 is not None and r2 is not None:
            boot.append(r1 - r2)
    ci = ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
          if len(boot) >= 50 else None)
    return {
        "n": len(idx), "n_lineages": len(uniq),
        "rho_score": ra, "rho_reference": rc, "delta": delta, "ci95": ci,
        "prob_delta_gt_0": float(np.mean(np.asarray(boot) > 0)) if boot else None,
        "n_boot_valid": len(boot),
        "verdict": (None if delta is None or ci is None else
                    ("SCORE_BETTER" if ci[0] > 0 else
                     ("REFERENCE_BETTER" if ci[1] < 0 else "TIE_CI_INCLUDES_0"))),
    }


# --------------------------------------------------------------------------
# Sign-free companion: AUC of the oriented score for y >= median(y)
# --------------------------------------------------------------------------
def auc_binary(score, y) -> dict:
    a, b, _ = _clean(score, y)
    if a.size < 4:
        return {"auc": None, "n": int(a.size)}
    med = float(np.median(b))
    lab = (b >= med).astype(int)
    if lab.sum() in (0, lab.size):
        return {"auc": None, "n": int(a.size), "note": "degenerate split"}
    r = rankdata(a)
    n1 = int(lab.sum())
    n0 = int(lab.size - n1)
    auc = (r[lab == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    return {"auc": float(auc), "n": int(a.size), "n_pos": n1, "n_neg": n0,
            "threshold": med, "outcome": "y_refusal >= median"}


def disattenuate(rho: float | None, reliability: float) -> float | None:
    if rho is None or reliability <= 0:
        return None
    return float(rho / math.sqrt(reliability))


def spearman_pair(x, y) -> dict:
    """Plain Spearman used for CHECK 1 (refit vs original)."""
    return spearman_basic(x, y)


def monotone_rho(xs, ys) -> float | None:
    a, b, _ = _clean(xs, ys)
    return _rho(a, b)


def span_factor(values) -> float | None:
    v = [float(x) for x in values if x is not None and np.isfinite(float(x))]
    if len(v) < 2:
        return None
    lo, hi = min(v), max(v)
    if abs(lo) < 1e-9:
        return None
    if lo <= 0 < hi or hi <= 0:
        # a sign change makes max/min meaningless; report the ratio of absolute
        # magnitudes so the row is still comparable, flagged by the caller
        return float(max(abs(lo), abs(hi)) / max(min(abs(lo), abs(hi)), 1e-9))
    return float(hi / lo)
