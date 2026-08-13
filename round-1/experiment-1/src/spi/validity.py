"""Estimator-identifiability checks — the make-or-break arm of this artifact.

The central question is NOT "is lambda ordered as predicted" but "is lambda
recoverable at all from a real 0.6B model's generated-step series at achievable
length and noise level". Stage H answers it with a synthetic recovery study that
mirrors the real pipeline exactly: per-rollout differences with the OBSERVED
noise sd, averaged as |delta|, fed to the SAME estimator.
"""

from __future__ import annotations

import multiprocessing as mp
from typing import Any

import numpy as np
from loguru import logger

from .indicators import fit_lambda_nls, half_life_auc

# Pre-registered acceptance rule for a (T_fit, n_roll) cell.
BIAS_TOL = 0.20   # |bias| < 0.20 * true_lambda
SD_TOL = 0.50     # sd < 0.50 * true_lambda


def simulate_delta_curve(true_lambda: float, amp: float, noise_sd: float,
                         T_fit: int, n_roll: int, rng: np.random.Generator
                         ) -> tuple[np.ndarray, np.ndarray]:
    """One replicate of the curves the real estimator consumes: (signed, abs).

    Per rollout the deviation is a decaying signal plus independent noise. The
    signed across-rollout mean is what the primary estimator fits; the
    absolute-value mean is simulated alongside so the study measures the bias
    that statistic carries rather than assuming it.
    """
    t = np.arange(T_fit, dtype=np.float64)
    signal = amp * np.exp(-true_lambda * t)
    noise = rng.normal(0.0, noise_sd, size=(T_fit, n_roll))
    per_rollout = signal[:, None] + noise
    return per_rollout.mean(axis=1), np.abs(per_rollout).mean(axis=1)


def _cell_worker(args: tuple) -> dict[str, Any]:
    true_lambda, amp, noise_sd, T_fit, n_roll, n_reps, seed = args
    rng = np.random.default_rng(seed)
    lams: list[float] = []
    lams_abs: list[float] = []
    aucs: list[float] = []
    n_fail = 0
    n_bound = 0
    for _ in range(n_reps):
        ds, da = simulate_delta_curve(true_lambda, amp, noise_sd, T_fit, n_roll, rng)
        fit = fit_lambda_nls(ds, signed=True)
        fit_a = fit_lambda_nls(da, signed=False)
        if fit_a.get("lambda") is not None:
            lams_abs.append(float(fit_a["lambda"]))
        if fit.get("lambda") is None:
            n_fail += 1
            continue
        if fit.get("at_bound"):
            n_bound += 1
        lams.append(float(fit["lambda"]))
        a = half_life_auc(np.abs(ds))
        if a.get("auc_norm") is not None:
            aucs.append(float(a["auc_norm"]))
    arr = np.asarray(lams, dtype=np.float64)
    arr_abs = np.asarray(lams_abs, dtype=np.float64)
    if arr.size < 10:
        return {
            "true_lambda": true_lambda, "T_fit": T_fit, "n_roll": n_roll,
            "n_ok": int(arr.size), "n_fail": n_fail, "bias": None, "sd": None,
            "passes": False, "reason": "insufficient_successful_fits",
        }
    bias = float(arr.mean() - true_lambda)
    sd = float(arr.std(ddof=1))
    # Bootstrap-percentile coverage of the true value across replicates.
    lo, hi = np.percentile(arr, [2.5, 97.5])
    passes = abs(bias) < BIAS_TOL * true_lambda and sd < SD_TOL * true_lambda
    return {
        "true_lambda": float(true_lambda), "T_fit": int(T_fit), "n_roll": int(n_roll),
        "amp": float(amp), "noise_sd": float(noise_sd),
        "n_ok": int(arr.size), "n_fail": int(n_fail), "n_at_bound": int(n_bound),
        "mean_est": float(arr.mean()), "median_est": float(np.median(arr)),
        "bias": bias, "rel_bias": float(bias / true_lambda), "sd": sd,
        "rel_sd": float(sd / true_lambda),
        "pct_2_5": float(lo), "pct_97_5": float(hi),
        "covers_truth": bool(lo <= true_lambda <= hi),
        "auc_mean": float(np.mean(aucs)) if aucs else None,
        "auc_sd": float(np.std(aucs, ddof=1)) if len(aucs) > 1 else None,
        # The pre-registered mean-|delta| statistic, measured side by side so the
        # size of its upward bias is a reported number, not an assertion.
        "abs_statistic_rel_bias": (
            float((arr_abs.mean() - true_lambda) / true_lambda) if arr_abs.size >= 10 else None),
        "abs_statistic_rel_sd": (
            float(arr_abs.std(ddof=1) / true_lambda) if arr_abs.size >= 10 else None),
        "passes": bool(passes), "reason": None,
    }


def synthetic_ar1_study(noise_sd: float, amp: float, *,
                        lambdas: tuple[float, ...] = (0.02, 0.05, 0.1, 0.2, 0.5, 1.0),
                        T_fits: tuple[int, ...] = (16, 32, 64, 128),
                        n_rolls: tuple[int, ...] = (4, 12, 20, 40),
                        n_reps: int = 500, seed: int = 4242,
                        n_workers: int = 16) -> dict[str, Any]:
    """Full grid. Returns the table plus the derived minimum-geometry rule."""
    jobs = []
    s = seed
    for lam in lambdas:
        for T_fit in T_fits:
            for n_roll in n_rolls:
                jobs.append((lam, amp, noise_sd, T_fit, n_roll, n_reps, s))
                s += 1
    logger.info(
        f"Synthetic AR(1) study: {len(jobs)} cells x {n_reps} reps "
        f"(noise_sd={noise_sd:.4f}, amp={amp:.4f}) on {n_workers} workers"
    )
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=n_workers) as pool:
        rows = pool.map(_cell_worker, jobs, chunksize=1)

    rule = derive_min_geometry(rows, lambdas)
    logger.info(f"Minimum-geometry rule: {rule}")
    return {"table": rows, "rule": rule, "n_reps": n_reps,
            "noise_sd": float(noise_sd), "amp": float(amp),
            "bias_tol": BIAS_TOL, "sd_tol": SD_TOL}


def derive_min_geometry(rows: list[dict[str, Any]],
                        lambdas: tuple[float, ...]) -> dict[str, Any]:
    """Smallest (T_fit, n_roll) cell passing the rule across the WHOLE lambda range.

    If no cell passes, that is the artifact's headline finding and is reported
    as such — never dressed up.
    """
    by_geom: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for r in rows:
        by_geom.setdefault((r["T_fit"], r["n_roll"]), []).append(r)
    passing = []
    for (T_fit, n_roll), cells in by_geom.items():
        if len(cells) < len(lambdas):
            continue
        if all(c["passes"] for c in cells):
            passing.append((T_fit, n_roll))
    # Per-lambda relaxation: which lambdas are recoverable at the largest geometry.
    largest = max(by_geom, key=lambda k: (k[0], k[1]))
    per_lambda = {
        str(c["true_lambda"]): bool(c["passes"]) for c in by_geom[largest]
    }
    if not passing:
        return {
            "any_cell_passes": False,
            "min_T_fit": None, "min_n_roll": None,
            "per_lambda_at_largest_geometry": per_lambda,
            "largest_geometry": {"T_fit": largest[0], "n_roll": largest[1]},
            "note": (
                "NO (T_fit, n_roll) cell meets |bias| < 0.2*lambda AND sd < 0.5*lambda "
                "across the full lambda range. Under the pre-registered rule, lambda is "
                "reported with identifiable=false and the AUC/half-life substitute "
                "becomes the headline recovery statistic."
            ),
        }
    passing.sort(key=lambda k: (k[0], k[1]))
    T_min, n_min = passing[0]
    return {
        "any_cell_passes": True, "min_T_fit": int(T_min), "min_n_roll": int(n_min),
        "n_passing_cells": len(passing),
        "per_lambda_at_largest_geometry": per_lambda,
        "largest_geometry": {"T_fit": largest[0], "n_roll": largest[1]},
        "note": (
            f"lambda is reported as identifiable only at T_fit >= {T_min} and "
            f"n_roll >= {n_min} (pre-registered rule)."
        ),
    }


def is_identifiable(rule: dict[str, Any], T_fit: int, n_roll: int) -> bool:
    """Apply the pre-registered rule to a real measurement's geometry."""
    if not rule.get("any_cell_passes"):
        return False
    return T_fit >= int(rule["min_T_fit"]) and n_roll >= int(rule["min_n_roll"])


def estimator_unit_tests() -> dict[str, Any]:
    """T5 correctness gate — run BEFORE the study, on placeholder inputs.

    (a) noiseless exponentials must be recovered within 2%;
    (b) pure noise must NOT yield a confident number.
    """
    out: dict[str, Any] = {"noiseless": [], "pure_noise": []}
    for lam in (0.05, 0.1, 0.3, 0.8):
        t = np.arange(64, dtype=np.float64)
        d = 1.0 * np.exp(-lam * t) + 0.0
        fit = fit_lambda_nls(d)
        est = fit.get("lambda")
        rel = abs(est - lam) / lam if est is not None else None
        out["noiseless"].append({
            "true": lam, "est": est, "rel_err": rel,
            "within_2pct": bool(rel is not None and rel < 0.02),
        })
    rng = np.random.default_rng(0)
    for i in range(20):
        d = np.abs(rng.normal(0.0, 1.0, size=64))
        fit = fit_lambda_nls(d)
        out["pure_noise"].append({
            "lambda": fit.get("lambda"), "r2": fit.get("r2"),
            "at_bound": fit.get("at_bound"), "reason": fit.get("reason"),
        })
    out["noiseless_all_pass"] = all(x["within_2pct"] for x in out["noiseless"])
    r2s = [x["r2"] for x in out["pure_noise"] if x["r2"] is not None]
    out["pure_noise_median_r2"] = float(np.median(r2s)) if r2s else None
    out["pure_noise_flagged_rate"] = float(
        np.mean([bool(x["at_bound"]) or x["lambda"] is None or (x["r2"] or 0) < 0.2
                 for x in out["pure_noise"]])
    )
    logger.info(
        f"Estimator unit tests: noiseless_all_pass={out['noiseless_all_pass']} "
        f"pure_noise_median_r2={out['pure_noise_median_r2']} "
        f"flagged_rate={out['pure_noise_flagged_rate']}"
    )
    return out
