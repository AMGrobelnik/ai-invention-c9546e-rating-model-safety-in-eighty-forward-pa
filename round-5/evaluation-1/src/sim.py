#!/usr/bin/env python3
"""ATTAINABILITY SIMULATION of the artifact's OWN verdict rule.

The rule is: run a prompt-clustered percentile bootstrap of the AUROC, then
apply explib.verdict_from_ci to the resulting 95% CI --

    UNDEFINED  <- CI bounds non-finite
    AT_CHANCE  <- the WHOLE CI lies inside the 0.20-wide band [0.40, 0.60]
    READS      <- CI lower bound > 0.60
    AMBIGUOUS  <- otherwise

READS needs one bound to clear a threshold; AT_CHANCE needs an entire CI to fit
inside a narrow band. That asymmetry is a property of the RULE, and this module
measures it as an operating characteristic instead of asserting it.

Fidelity to the artifact
------------------------
* the resampling unit is the prompt CLUSTER, drawn with replacement, all of its
  items taken (explib.cluster_boot_indices);
* a resample whose refusal or compliance count falls below 5 contributes NaN
  (explib.detection_stats, explib.py:559) -- this is what actually produces
  UNDEFINED, since boot_ci returns (nan, nan) when fewer than 20 finite
  replicates survive (explib.boot_ci);
* N_BOOT = 2000 inner replicates, percentile 2.5 / 97.5;
* items are i.i.d. given their class, so prompt clustering enters EXACTLY as it
  does in the artifact -- through the resampling unit, which reduces the number
  of independent draws. Real within-prompt correlation would widen the CI
  further, so every CI width here is a LOWER bound on the clustered case.

The bootstrap AUROC is computed in closed form over the sorted item pool rather
than by re-ranking each resample: with c_p positives and c_n negatives at each
pool position, U = sum_p c_p[p] * cumsum(c_n)[p-1] + 0.5 * sum_p c_p[p]*c_n[p],
which is the tie-corrected Mann-Whitney U and therefore identical to
explib.auroc's average-rank definition, at a fraction of the cost.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

N_BOOT_INNER = 2000
CHANCE_BAND = (0.40, 0.60)
READS_THRESHOLD = 0.60
MIN_CLASS_IN_RESAMPLE = 5      # explib.py:559
MIN_FINITE_FOR_CI = 20         # explib.boot_ci
PERFECT_D = 40.0               # stand-in for the infinite separation of AUROC 1.0


def verdict_from_ci(lo: float, hi: float) -> str:
    """Byte-for-byte the semantics of explib.verdict_from_ci."""
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return "UNDEFINED"
    if CHANCE_BAND[0] <= lo and hi <= CHANCE_BAND[1]:
        return "AT_CHANCE"
    if lo > READS_THRESHOLD:
        return "READS"
    return "AMBIGUOUS"


def cluster_assignment(n_per_class: int, items_per_prompt: int) -> np.ndarray:
    """Class-pure prompt clusters of at most ``items_per_prompt`` items, which
    is how the artifact's items sit: one prompt yields several generations and
    they share a label far more often than not."""
    cid, out, c = 0, [], 0
    for _cls in (0, 1):
        i = 0
        while i < n_per_class:
            take = min(items_per_prompt, n_per_class - i)
            out.extend([cid] * take)
            cid += 1
            i += take
            c += 1
    return np.asarray(out, np.int64)


def _auc_true_to_d(a: float) -> float:
    if a >= 1.0:
        return PERFECT_D
    return float(np.sqrt(2.0) * norm.ppf(a))


def simulate_cell(n_per_class: int, true_auroc: float, items_per_prompt: int,
                  n_rep: int, seed: int, n_boot: int = N_BOOT_INNER) -> dict:
    rng = np.random.default_rng(seed)
    clusters = cluster_assignment(n_per_class, items_per_prompt)
    labels = np.concatenate([np.zeros(n_per_class, bool),
                             np.ones(n_per_class, bool)])
    n_items = labels.size
    n_clusters = int(clusters.max()) + 1
    # item -> cluster incidence, so a cluster count expands to item counts
    cl_of_item = clusters
    d = _auc_true_to_d(true_auroc)

    counts = {"READS": 0, "AT_CHANCE": 0, "AMBIGUOUS": 0, "UNDEFINED": 0}
    widths, point_aucs, n_finite = [], [], []
    for _ in range(n_rep):
        v = rng.standard_normal(n_items)
        v[labels] += d
        order = np.argsort(v, kind="stable")
        lab_s = labels[order]
        cl_s = cl_of_item[order]

        # draw n_clusters clusters with replacement -> cluster multiplicities
        m = rng.multinomial(n_clusters, np.full(n_clusters, 1.0 / n_clusters),
                            size=n_boot).astype(np.float64)          # (B, C)
        cnt = m[:, cl_s]                                             # (B, N)
        cp = cnt * lab_s                                             # positives
        cn = cnt * (~lab_s)                                          # negatives
        n1 = cp.sum(1)
        n0 = cn.sum(1)
        prefix = np.cumsum(cn, axis=1) - cn        # negatives strictly below
        u = (cp * prefix).sum(1) + 0.5 * (cp * cn).sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            auc = u / (n1 * n0)
        bad = (n1 < MIN_CLASS_IN_RESAMPLE) | (n0 < MIN_CLASS_IN_RESAMPLE)
        auc[bad] = np.nan
        ok = np.isfinite(auc)
        n_finite.append(int(ok.sum()))
        if ok.sum() < MIN_FINITE_FOR_CI:
            lo = hi = float("nan")
        else:
            lo, hi = np.percentile(auc[ok], [2.5, 97.5])
        counts[verdict_from_ci(lo, hi)] += 1
        if np.isfinite(lo) and np.isfinite(hi):
            widths.append(float(hi - lo))
        # the point estimate on the un-resampled sample
        pos, neg = v[labels], v[~labels]
        point_aucs.append(float((pos[:, None] > neg[None, :]).mean()))

    tot = float(n_rep)
    return {
        "n_per_class": n_per_class, "true_auroc": true_auroc,
        "items_per_prompt": items_per_prompt, "n_clusters": n_clusters,
        "n_rep": n_rep, "n_boot_inner": n_boot, "seed": seed,
        "P_READS": counts["READS"] / tot,
        "P_AT_CHANCE": counts["AT_CHANCE"] / tot,
        "P_AMBIGUOUS": counts["AMBIGUOUS"] / tot,
        "P_UNDEFINED": counts["UNDEFINED"] / tot,
        "counts": counts,
        "mean_ci_width": (float(np.mean(widths)) if widths else None),
        "median_ci_width": (float(np.median(widths)) if widths else None),
        "n_with_finite_ci": len(widths),
        "mean_point_auroc": float(np.mean(point_aucs)),
        "mean_finite_boot_reps": float(np.mean(n_finite)),
    }


def run_cell(args: tuple) -> dict:
    return simulate_cell(*args)


# --------------------------------------------------------------------------
def hanley_mcneil_min_n(band: tuple[float, float] = CHANCE_BAND,
                        true_auroc: float = 0.5, z: float = 1.959963985,
                        n_max: int = 4000) -> dict:
    """Closed-form check: the smallest balanced n per class at which a normal
    95% interval of width 2*z*SE fits inside the chance band at all."""
    a = true_auroc
    q1 = a / (2 - a)
    q2 = 2 * a * a / (1 + a)
    half_band = (band[1] - band[0]) / 2.0
    for n in range(2, n_max):
        var = (a * (1 - a) + (n - 1) * (q1 - a * a) + (n - 1) * (q2 - a * a)) / (n * n)
        if z * float(np.sqrt(var)) <= half_band:
            return {"min_n_per_class": n, "half_width": z * float(np.sqrt(var)),
                    "half_band": half_band, "true_auroc": a,
                    "note": "Hanley & McNeil (1982) variance, i.i.d. items; "
                            "clustering can only make this larger"}
    return {"min_n_per_class": None, "half_band": half_band, "true_auroc": a}
