#!/usr/bin/env python3
"""alpha_50: logistic dose-response on Bernoulli refusal draws, with a
prompt-clustered bootstrap CI and every pre-registered guardrail.

The fit is MLE on the EXACT per-draw log-likelihood (not on aggregated rates),
so a prompt contributing 5 seeds at 13 alphas contributes 65 Bernoulli terms.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2

BOOT_SEED = 20260812


def _nll(params, alpha, y):
    b0, b1 = params
    z = b0 + b1 * alpha
    # numerically stable binary cross entropy
    return float(np.sum(np.logaddexp(0.0, z) - y * z))


def _grad(params, alpha, y):
    b0, b1 = params
    z = b0 + b1 * alpha
    p = 1.0 / (1.0 + np.exp(-z))
    r = p - y
    return np.array([r.sum(), float((r * alpha).sum())])


def fit_logistic(alpha: np.ndarray, y: np.ndarray) -> dict:
    """MLE logistic fit. Returns b0, b1, alpha_50 (None when undefined)."""
    alpha = np.asarray(alpha, dtype=float)
    y = np.asarray(y, dtype=float)
    if y.size == 0 or np.allclose(y, y[0]):
        return {"b0": None, "b1": None, "alpha_50": None, "reason": "degenerate_outcome"}
    best = None
    for init in ((0.0, 1.0), (-2.0, 4.0), (-5.0, 10.0), (2.0, -1.0)):
        try:
            res = minimize(
                _nll, np.array(init, dtype=float), args=(alpha, y), jac=_grad,
                method="L-BFGS-B", options={"maxiter": 500},
            )
        except (ValueError, FloatingPointError):
            continue
        if res.success or np.isfinite(res.fun):
            if best is None or res.fun < best.fun:
                best = res
    if best is None:
        return {"b0": None, "b1": None, "alpha_50": None, "reason": "fit_failed"}
    b0, b1 = float(best.x[0]), float(best.x[1])
    return {"b0": b0, "b1": b1, "nll": float(best.fun),
            "alpha_50": (-b0 / b1) if b1 > 1e-6 else None,
            "reason": "" if b1 > 1e-6 else "nonpositive_slope"}


def nonparametric_alpha50(grid: list[float], rates: list[float]) -> float | None:
    """Linear interpolation between the grid points bracketing the 0.5 crossing.

    Reported alongside the logistic estimate whenever the curve is step-like.
    """
    g = np.asarray(grid, dtype=float)
    r = np.asarray(rates, dtype=float)
    order = np.argsort(g)
    g, r = g[order], r[order]
    for i in range(len(g) - 1):
        if r[i] < 0.5 <= r[i + 1]:
            if r[i + 1] == r[i]:
                return float(g[i])
            return float(g[i] + (0.5 - r[i]) * (g[i + 1] - g[i]) / (r[i + 1] - r[i]))
    if r[0] >= 0.5:
        return float(g[0])
    return None


def hosmer_lemeshow(grid, rates, counts, b0, b1) -> dict:
    """Grid-wise goodness of fit: a step-like curve shows up as a large residual
    rather than being smoothed over by the logistic."""
    if b0 is None or b1 is None:
        return {"chi2": None, "df": None, "p": None, "max_abs_residual": None}
    g = np.asarray(grid, dtype=float)
    obs = np.asarray(rates, dtype=float) * np.asarray(counts, dtype=float)
    n = np.asarray(counts, dtype=float)
    p = 1.0 / (1.0 + np.exp(-(b0 + b1 * g)))
    exp = p * n
    denom = np.clip(exp * (1 - p), 1e-9, None)
    stat = float(np.sum((obs - exp) ** 2 / denom))
    df = max(1, len(g) - 2)
    return {
        "chi2": stat, "df": int(df), "p": float(chi2.sf(stat, df)),
        "max_abs_residual": float(np.max(np.abs(np.asarray(rates) - p))),
        "fitted_rates": [float(x) for x in p],
    }


class DoseData:
    """Bernoulli draws indexed by (prompt, alpha), ready for cluster resampling.

    draws[prompt_index] -> (alpha_vector, y_vector) for all seeds and alphas.
    """

    def __init__(self, n_prompts: int):
        self.n_prompts = n_prompts
        self.alpha: list[list[float]] = [[] for _ in range(n_prompts)]
        self.y: list[list[int]] = [[] for _ in range(n_prompts)]

    def add(self, prompt_idx: int, alpha: float, refused: bool) -> None:
        self.alpha[prompt_idx].append(float(alpha))
        self.y[prompt_idx].append(int(bool(refused)))

    def arrays(self) -> tuple[list[np.ndarray], list[np.ndarray]]:
        return (
            [np.asarray(a, dtype=float) for a in self.alpha],
            [np.asarray(v, dtype=float) for v in self.y],
        )

    def flat(self) -> tuple[np.ndarray, np.ndarray]:
        a, y = self.arrays()
        return np.concatenate(a) if a else np.array([]), np.concatenate(y) if y else np.array([])

    def rates_by_alpha(self) -> dict[float, tuple[float, int]]:
        acc: dict[float, list[int]] = {}
        for a_list, y_list in zip(self.alpha, self.y):
            for a, y in zip(a_list, y_list):
                acc.setdefault(round(a, 6), []).append(y)
        return {a: (float(np.mean(v)), len(v)) for a, v in sorted(acc.items())}

    def to_json(self) -> dict:
        return {"n_prompts": self.n_prompts, "alpha": self.alpha, "y": self.y}

    @staticmethod
    def from_json(d: dict) -> "DoseData":
        dd = DoseData(int(d["n_prompts"]))
        dd.alpha = [list(map(float, x)) for x in d["alpha"]]
        dd.y = [list(map(int, x)) for x in d["y"]]
        return dd


def analyse_dose(dd: DoseData, n_boot: int = 2000, seed: int = BOOT_SEED,
                 undefined_frac_threshold: float = 0.20) -> dict:
    """Point fit + prompt-clustered bootstrap CI + every pre-registered guardrail."""
    a_all, y_all = dd.flat()
    if a_all.size == 0:
        return {"status": "NO_DATA"}
    rates = dd.rates_by_alpha()
    grid = sorted(rates)
    rate_vec = [rates[g][0] for g in grid]
    counts = [rates[g][1] for g in grid]
    max_rate = float(max(rate_vec))

    point = fit_logistic(a_all, y_all)
    hl = hosmer_lemeshow(grid, rate_vec, counts, point.get("b0"), point.get("b1"))
    np_a50 = nonparametric_alpha50(grid, rate_vec)

    status = "DEFINED"
    if max_rate < 0.5:
        status = "UNDEFINED_MAX_RATE_BELOW_HALF"
    elif point["alpha_50"] is None:
        status = "UNDEFINED_NONPOSITIVE_SLOPE"
    elif point["alpha_50"] > max(grid) * 1.5 or point["alpha_50"] < min(grid) - 1.0:
        status = "UNDEFINED_OUT_OF_RANGE"

    alphas_p, ys_p = dd.arrays()
    rng = np.random.default_rng(seed)
    boot_a50, boot_b1 = [], []
    n_undef = 0
    idx_pool = np.arange(dd.n_prompts)
    for _ in range(n_boot):
        idx = rng.choice(idx_pool, size=dd.n_prompts, replace=True)
        aa = np.concatenate([alphas_p[i] for i in idx])
        yy = np.concatenate([ys_p[i] for i in idx])
        f = fit_logistic(aa, yy)
        if f["alpha_50"] is None or not np.isfinite(f["alpha_50"]):
            n_undef += 1
            continue
        boot_a50.append(f["alpha_50"])
        boot_b1.append(f["b1"])
    frac_undef = n_undef / max(1, n_boot)

    out = {
        "status": status,
        "b0": point.get("b0"),
        "b1": point.get("b1"),
        "alpha_50": point.get("alpha_50") if status == "DEFINED" else None,
        "alpha_50_raw_fit": point.get("alpha_50"),
        "alpha_50_nonparametric": np_a50,
        "max_refusal_rate": max_rate,
        "alpha_grid": grid,
        "refusal_rates": rate_vec,
        "n_draws_per_alpha": counts,
        "fit_residual": hl,
        "bootstrap": {
            "n_boot": n_boot,
            "n_valid": len(boot_a50),
            "frac_undefined": frac_undef,
            "unstable": frac_undef > undefined_frac_threshold,
            "alpha_50_ci": (
                [float(np.percentile(boot_a50, 2.5)), float(np.percentile(boot_a50, 97.5))]
                if len(boot_a50) >= 50 else None
            ),
            "alpha_50_median": float(np.median(boot_a50)) if boot_a50 else None,
            "b1_ci": (
                [float(np.percentile(boot_b1, 2.5)), float(np.percentile(boot_b1, 97.5))]
                if len(boot_b1) >= 50 else None
            ),
        },
    }
    if out["bootstrap"]["unstable"] and status == "DEFINED":
        out["status"] = "UNSTABLE"
    return out


def paired_alpha50_diff(dd_a: DoseData, dd_b: DoseData, n_boot: int = 2000,
                        seed: int = BOOT_SEED) -> dict:
    """Paired cluster bootstrap of alpha_50(A) - alpha_50(B).

    ONE prompt resample is drawn and BOTH members are refitted on it, so the
    difference is paired on the prompt set exactly as pre-registered.
    """
    n = min(dd_a.n_prompts, dd_b.n_prompts)
    aa, ya = dd_a.arrays()
    ab, yb = dd_b.arrays()
    pa = fit_logistic(*dd_a.flat())
    pb = fit_logistic(*dd_b.flat())
    point = (
        pa["alpha_50"] - pb["alpha_50"]
        if pa["alpha_50"] is not None and pb["alpha_50"] is not None else None
    )
    rng = np.random.default_rng(seed)
    diffs = []
    n_undef = 0
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        fa = fit_logistic(np.concatenate([aa[i] for i in idx]), np.concatenate([ya[i] for i in idx]))
        fb = fit_logistic(np.concatenate([ab[i] for i in idx]), np.concatenate([yb[i] for i in idx]))
        if fa["alpha_50"] is None or fb["alpha_50"] is None:
            n_undef += 1
            continue
        diffs.append(fa["alpha_50"] - fb["alpha_50"])
    if len(diffs) < 50:
        return {"diff": point, "ci": None, "n_valid": len(diffs),
                "frac_undefined": n_undef / max(1, n_boot)}
    return {
        "diff": point,
        "ci": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "median": float(np.median(diffs)),
        "frac_positive": float(np.mean(np.asarray(diffs) > 0)),
        "n_valid": len(diffs),
        "frac_undefined": n_undef / max(1, n_boot),
    }


def monotonicity(grid, rates, drop_threshold: float = 0.20) -> dict:
    """Detect the inverted-U dose curve the pre-registration anticipated.

    Steering past the point where the axis dominates the residual stream
    destroys the model's ability to FORM a refusal opener at all, so the
    refusal rate rises and then falls. A logistic fitted across the whole grid
    then reports a meaningless alpha_50 (measured: Qwen2.5-1.5B-Instruct,
    rates 0.01 -> 0.92 -> 0.13, logistic alpha_50 = -0.459 with CI
    [-12.98, 0.67]). This function makes that visible instead of smoothing it.
    """
    g = list(map(float, grid))
    r = list(map(float, rates))
    if not r:
        return {"non_monotone": None}
    i_max = int(np.argmax(r))
    drop = float(r[i_max] - r[-1])
    return {
        "max_rate": float(r[i_max]),
        "alpha_at_max_rate": g[i_max],
        "rate_at_largest_alpha": float(r[-1]),
        "drop_from_peak_to_largest_alpha": drop,
        "non_monotone": bool(drop > drop_threshold),
        "drop_threshold": drop_threshold,
    }
