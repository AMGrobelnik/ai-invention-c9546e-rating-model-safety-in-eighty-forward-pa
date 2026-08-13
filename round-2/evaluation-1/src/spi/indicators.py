"""H2 early-warning indicators and the three lambda estimators.

Every fluctuation statistic is reported TWICE — detrended and raw — plus the
delta, so the size of the detrending effect is visible (pre-registered).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from loguru import logger
from scipy import optimize


# --------------------------------------------------------------------------- #
# Fluctuation indicators (no perturbation needed — these survive even if lambda
# turns out not to be identifiable).
# --------------------------------------------------------------------------- #

def detrend_across_rollouts(R: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """R: (T, n_roll) -> (residuals, trend). Trend is the across-rollout mean at
    each step, i.e. the deterministic step-index component of r_t."""
    trend = R.mean(axis=1)
    return R - trend[:, None], trend


def detrend_per_rollout_linear(R: np.ndarray) -> np.ndarray:
    """Robustness variant: remove a per-rollout linear trend in t."""
    T = R.shape[0]
    t = np.arange(T, dtype=np.float64)
    tc = t - t.mean()
    denom = float((tc**2).sum())
    if denom <= 0:
        return R - R.mean(axis=0, keepdims=True)
    slope = (tc[:, None] * (R - R.mean(axis=0, keepdims=True))).sum(axis=0) / denom
    return R - (R.mean(axis=0, keepdims=True) + slope[None, :] * tc[:, None])


def lag1_autocorr(x: np.ndarray) -> float:
    """Lag-1 autocorrelation of a single series."""
    x = np.asarray(x, dtype=np.float64)
    x = x[np.isfinite(x)]
    if x.size < 4:
        return float("nan")
    xc = x - x.mean()
    d = float((xc**2).sum())
    if d <= 1e-12:
        return float("nan")
    return float((xc[:-1] * xc[1:]).sum() / d)


def ac1_bias_corrected(x: np.ndarray) -> float:
    """Kendall small-sample bias correction: rho_c = rho + (1 + 3*rho)/T."""
    rho = lag1_autocorr(x)
    if not np.isfinite(rho):
        return float("nan")
    T = int(np.isfinite(x).sum())
    return float(rho + (1.0 + 3.0 * rho) / T)


def fisher_z(rho: float) -> float:
    if not np.isfinite(rho):
        return float("nan")
    rho = float(np.clip(rho, -0.999, 0.999))
    return float(np.arctanh(rho))


def flicker(R: np.ndarray, burn_in: int = 8, boundary: float = 0.0) -> dict[str, float]:
    """Fraction of rollouts crossing the r = boundary decision line at least once
    after burn_in, plus crossings per 100 steps."""
    X = R[burn_in:, :]
    if X.shape[0] < 2:
        return {"frac_rollouts_crossing": float("nan"), "crossings_per_100": float("nan")}
    sgn = np.sign(X - boundary)
    sgn[sgn == 0] = 1.0
    crossings = (sgn[1:] != sgn[:-1]).sum(axis=0)      # (n_roll,)
    steps = X.shape[0] - 1
    return {
        "frac_rollouts_crossing": float((crossings > 0).mean()),
        "crossings_per_100": float(crossings.mean() / steps * 100.0),
        "mean_crossings": float(crossings.mean()),
    }


def fluctuation_indicators(R: np.ndarray, burn_in: int = 8) -> dict[str, Any]:
    """All three perturbation-free indicators, detrended AND raw."""
    Rd, trend = detrend_across_rollouts(R)
    Rlin = detrend_per_rollout_linear(R)

    def pack(X: np.ndarray) -> dict[str, Any]:
        per_ac1 = [ac1_bias_corrected(X[:, j]) for j in range(X.shape[1])]
        per_ac1_raw = [lag1_autocorr(X[:, j]) for j in range(X.shape[1])]
        var_t = X.var(axis=1, ddof=1) if X.shape[1] > 1 else np.zeros(X.shape[0])
        # Crossings are counted on whatever series is passed in. For the RAW pack
        # that is r_t itself, so the boundary is the r=0 decision line (refusal and
        # continuation onset at equal log-odds). For the DETRENDED pack it is Rd,
        # whose zero is the across-rollout mean trajectory, so the statistic
        # becomes oscillation of a rollout about the central path. Both are
        # reported: on harmless prompts r_t sits well below 0, so the r=0 variant
        # is usually identically zero and would be a degenerate SPI term on its own.
        fl = flicker(X, burn_in=burn_in)
        return {
            "var_star": float(np.nanmean(var_t)),
            "var_star_sd_over_steps": float(np.nanstd(var_t)),
            "ac1": float(np.nanmean(per_ac1)),
            "ac1_uncorrected": float(np.nanmean(per_ac1_raw)),
            "ac1_per_rollout": [float(v) for v in per_ac1],
            "sd_overall": float(np.nanstd(X)),
            **{f"flicker_{k}": v for k, v in fl.items()},
        }

    det = pack(Rd)
    raw = pack(R)
    lin = pack(Rlin)
    det["flicker_boundary"] = "Rd = 0, i.e. the across-rollout mean trajectory"
    raw["flicker_boundary"] = "r_t = 0, the refusal/continuation log-odds parity line"
    return {
        "detrended": det,
        "raw": raw,
        "flicker_r0_is_degenerate": bool(
            raw["flicker_frac_rollouts_crossing"] == 0.0),
        "per_rollout_linear_detrend": lin,
        "delta_detrend_minus_raw": {
            "var_star": det["var_star"] - raw["var_star"],
            "ac1": det["ac1"] - raw["ac1"],
        },
        "trend_mean": float(np.nanmean(trend)),
        "trend_sd_over_steps": float(np.nanstd(trend)),
        "n_steps": int(R.shape[0]),
        "n_rollouts": int(R.shape[1]),
    }


# --------------------------------------------------------------------------- #
# lambda estimators
# --------------------------------------------------------------------------- #

def _exp_model(t: np.ndarray, A: float, lam: float, b: float) -> np.ndarray:
    return A * np.exp(-lam * t) + b


def fit_lambda_nls(d: np.ndarray, lam_bounds: tuple[float, float] = (1e-3, 2.0),
                   signed: bool = False) -> dict[str, Any]:
    """Estimator #1 (PRIMARY): robust NLS fit of delta_t = A*exp(-lam*t) + b.

    `signed=True` fits the SIGNED across-rollout mean deviation and lets A take
    either sign. That is the statistically correct target: mean_j |delta_{t,j}|
    is biased upward, because E|N(mu, sigma)| > |mu|, and — critically — the bias
    does NOT vanish as rollouts are added, since the average converges to E|X|
    rather than |E X|. Its tail therefore flattens onto a ~0.8*sigma floor whose
    curvature the free offset cannot absorb, which biases lambda upward. The
    signed mean is unbiased and its noise falls as sigma/sqrt(n_roll), so adding
    rollouts actually buys identifiability. `signed=False` reproduces the
    absolute-value statistic as the pre-registered secondary.
    """
    d = np.asarray(d, dtype=np.float64)
    t = np.arange(d.size, dtype=np.float64)
    ok = np.isfinite(d)
    if ok.sum() < 6:
        return {"lambda": None, "reason": "too_few_finite_points", "n": int(ok.sum())}
    t, d = t[ok], d[ok]
    tail = np.median(d[-max(3, d.size // 4):])
    b0 = float(tail)
    A0 = float(d[0] - tail)
    if signed:
        lo_A, hi_A = -np.inf, np.inf
        if abs(A0) < 1e-9:
            A0 = 1e-6
    else:
        lo_A, hi_A = 0.0, np.inf
        A0 = max(A0, 1e-6)
    try:
        popt, pcov = optimize.curve_fit(
            _exp_model, t, d,
            p0=[A0, 0.1, b0],
            bounds=([lo_A, lam_bounds[0], -np.inf], [hi_A, lam_bounds[1], np.inf]),
            loss="soft_l1", f_scale=max(float(np.std(d)), 1e-6), max_nfev=20000,
        )
    except Exception as exc:  # noqa: BLE001 - a failed fit must be null + reason
        return {"lambda": None, "reason": f"curve_fit_failed:{type(exc).__name__}"}
    A, lam, b = (float(v) for v in popt)
    pred = _exp_model(t, A, lam, b)
    ss_res = float(((d - pred) ** 2).sum())
    ss_tot = float(((d - d.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    se = float(np.sqrt(np.diag(pcov))[1]) if np.all(np.isfinite(pcov)) else float("nan")
    at_bound = lam <= lam_bounds[0] * 1.01 or lam >= lam_bounds[1] * 0.99
    return {
        "lambda": lam, "A": A, "b": b, "r2": r2, "se": se if np.isfinite(se) else None,
        "at_bound": bool(at_bound), "n": int(d.size), "reason": None,
    }


def fit_lambda_loglin(d: np.ndarray, floor: float) -> dict[str, Any]:
    """Estimator #2: OLS on log(|delta_t| + floor) vs t."""
    d = np.asarray(d, dtype=np.float64)
    t = np.arange(d.size, dtype=np.float64)
    ok = np.isfinite(d)
    if ok.sum() < 6:
        return {"lambda": None, "reason": "too_few_finite_points"}
    y = np.log(np.maximum(d[ok], 0.0) + max(floor, 1e-9))
    tt = t[ok]
    tc = tt - tt.mean()
    denom = float((tc**2).sum())
    if denom <= 0:
        return {"lambda": None, "reason": "degenerate_design"}
    slope = float((tc * (y - y.mean())).sum() / denom)
    pred = y.mean() + slope * tc
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(((y - pred) ** 2).sum()) / ss_tot if ss_tot > 0 else float("nan")
    return {"lambda": float(-slope), "r2": r2, "floor": float(floor), "reason": None}


def fit_lambda_ar1(d: np.ndarray) -> dict[str, Any]:
    """Estimator #3: AR(1) fit to delta_t; lambda = -log(phi)."""
    d = np.asarray(d, dtype=np.float64)
    d = d[np.isfinite(d)]
    if d.size < 6:
        return {"lambda": None, "reason": "too_few_finite_points"}
    x, y = d[:-1], d[1:]
    xc = x - x.mean()
    denom = float((xc**2).sum())
    if denom <= 1e-12:
        return {"lambda": None, "reason": "degenerate_series"}
    phi = float((xc * (y - y.mean())).sum() / denom)
    if phi <= 1e-6:
        return {"lambda": None, "phi": phi, "reason": "phi_nonpositive"}
    if phi >= 1.0:
        return {"lambda": 0.0, "phi": phi, "reason": "phi_ge_1_nonstationary"}
    return {"lambda": float(-np.log(phi)), "phi": phi, "reason": None}


def half_life_auc(d: np.ndarray) -> dict[str, Any]:
    """PRE-REGISTERED SUBSTITUTE for lambda if the rate fit is not identifiable.

    Area under |delta_t| over the fit window, normalised by |delta_1|. This is a
    monotone proxy for 1/lambda and is far more robust than an exponential rate.
    Also reports the empirical half-life (first step where |delta| falls below
    half of |delta_1|).
    """
    d = np.asarray(d, dtype=np.float64)
    d = d[np.isfinite(d)]
    if d.size < 3 or not np.isfinite(d[0]) or abs(d[0]) < 1e-12:
        return {"auc_norm": None, "half_life": None, "reason": "degenerate_delta0"}
    auc = float(d.sum() / d[0])
    below = np.flatnonzero(d < 0.5 * d[0])
    hl = float(below[0]) if below.size else float(d.size)
    return {"auc_norm": auc, "half_life": hl, "delta_0": float(d[0]), "reason": None}


def estimate_lambda_all(delta_signed: np.ndarray, clean_resid_sd: float,
                        fit_len: int = 64,
                        delta_abs: np.ndarray | None = None) -> dict[str, Any]:
    """All estimators, on the SIGNED mean deviation (primary) and on mean-|delta|.

    delta_signed: (T_post,) across-rollout mean of (r_pert - r_clean), from t=p+1.
    delta_abs:    (T_post,) across-rollout mean of |r_pert - r_clean| — the
                  pre-registered absolute-value statistic, kept as the secondary
                  so the effect of the bias correction is visible.
    """
    ds = np.asarray(delta_signed, dtype=np.float64)[:fit_len]
    floor = 0.05 * max(float(clean_resid_sd), 1e-9)
    est1 = fit_lambda_nls(ds, signed=True)
    est2 = fit_lambda_loglin(np.abs(ds), floor)
    est3 = fit_lambda_ar1(ds)
    lams = [e.get("lambda") for e in (est1, est2, est3)]
    lams = [float(v) for v in lams if v is not None and np.isfinite(v)]
    out = {
        "est1_nls": est1,
        "est2_loglin": est2,
        "est3_ar1": est3,
        "auc_substitute": half_life_auc(np.abs(ds)),
        "estimator_spread": float(np.max(lams) - np.min(lams)) if len(lams) > 1 else None,
        "estimator_agreement_ratio": (
            float(np.max(lams) / np.min(lams)) if len(lams) > 1 and min(lams) > 0 else None
        ),
        "fit_len": int(ds.size),
        "delta_floor": float(floor),
        "noise_floor_sd": float(clean_resid_sd),
        "statistic": "signed_across_rollout_mean",
    }
    if delta_abs is not None:
        da = np.asarray(delta_abs, dtype=np.float64)[:fit_len]
        out["abs_statistic_secondary"] = {
            "est1_nls": fit_lambda_nls(da, signed=False),
            "auc_substitute": half_life_auc(da),
            "note": "pre-registered mean-|delta| statistic; biased upward, see fit_lambda_nls",
        }
    return out


# --------------------------------------------------------------------------- #
# Bootstrap helpers
# --------------------------------------------------------------------------- #

def cluster_bootstrap_ci(values: list[float], n_reps: int = 5000, seed: int = 7,
                         stat: str = "median") -> dict[str, Any]:
    """Resample the CLUSTERS (prompts) with replacement."""
    v = np.asarray([x for x in values if x is not None and np.isfinite(x)], dtype=np.float64)
    if v.size == 0:
        return {"point": None, "ci_lo": None, "ci_hi": None, "n": 0}
    if v.size == 1:
        return {"point": float(v[0]), "ci_lo": None, "ci_hi": None, "n": 1}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(n_reps, v.size))
    draws = np.median(v[idx], axis=1) if stat == "median" else np.mean(v[idx], axis=1)
    point = float(np.median(v)) if stat == "median" else float(np.mean(v))
    return {
        "point": point,
        "ci_lo": float(np.percentile(draws, 2.5)),
        "ci_hi": float(np.percentile(draws, 97.5)),
        "n": int(v.size),
        "stat": stat,
        "n_reps": int(n_reps),
    }


def paired_bootstrap_diff(a: dict[str, float], b: dict[str, float],
                          n_reps: int = 5000, seed: int = 11) -> dict[str, Any]:
    """Paired-over-prompts bootstrap of (a - b). Keys are prompt ids."""
    keys = sorted(set(a) & set(b))
    d = np.asarray(
        [a[k] - b[k] for k in keys
         if a[k] is not None and b[k] is not None
         and np.isfinite(a[k]) and np.isfinite(b[k])],
        dtype=np.float64,
    )
    if d.size < 2:
        return {"diff": float(d[0]) if d.size == 1 else None,
                "ci_lo": None, "ci_hi": None, "n_pairs": int(d.size)}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(n_reps, d.size))
    draws = d[idx].mean(axis=1)
    lo, hi = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return {
        "diff": float(d.mean()), "ci_lo": lo, "ci_hi": hi,
        "n_pairs": int(d.size), "ci_excludes_zero": bool(lo > 0 or hi < 0),
    }


def wilson_ci(k: int, n: int, z: float = 1.96) -> dict[str, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return {"p": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    p = k / n
    den = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return {"p": float(p), "lo": float(max(0.0, centre - half)),
            "hi": float(min(1.0, centre + half)), "k": int(k), "n": int(n)}


def zscore(vals: list[float]) -> list[float]:
    v = np.asarray(vals, dtype=np.float64)
    m, s = np.nanmean(v), np.nanstd(v)
    if not np.isfinite(s) or s < 1e-12:
        logger.warning("zscore: near-zero spread; returning zeros")
        return [0.0] * len(vals)
    return [float(x) for x in (v - m) / s]


def safe_logit(p: float, eps: float = 1e-3) -> float:
    p = float(np.clip(p, eps, 1 - eps))
    return float(np.log(p / (1 - p)))
