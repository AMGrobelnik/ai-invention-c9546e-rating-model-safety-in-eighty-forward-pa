#!/usr/bin/env python3
"""Bootstrap, paired tests, censoring sensitivity, agreement statistics."""

from __future__ import annotations

import numpy as np

N_BOOT = 10000
BOOT_SEED = 20260812


def _rng() -> np.random.Generator:
    return np.random.default_rng(BOOT_SEED)


def bootstrap_mean(values: list[float], n_boot: int = N_BOOT) -> dict:
    v = np.asarray([x for x in values if x is not None and np.isfinite(x)], dtype=float)
    if v.size == 0:
        return {"n": 0, "mean": None, "ci_low": None, "ci_high": None, "sd": None}
    rng = _rng()
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    means = v[idx].mean(axis=1)
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "sd": float(v.std(ddof=1)) if v.size > 1 else 0.0,
        "ci_low": float(np.percentile(means, 2.5)),
        "ci_high": float(np.percentile(means, 97.5)),
    }


def bootstrap_paired_diff(a: dict, b: dict, n_boot: int = N_BOOT) -> dict:
    """a, b: prompt_id -> value. Paired bootstrap over the shared prompt set."""
    keys = sorted(set(a) & set(b))
    keys = [k for k in keys if a[k] is not None and b[k] is not None]
    if len(keys) < 2:
        return {"n": len(keys), "mean": None, "ci_low": None, "ci_high": None}
    d = np.array([a[k] - b[k] for k in keys], dtype=float)
    rng = _rng()
    idx = rng.integers(0, d.size, size=(n_boot, d.size))
    means = d[idx].mean(axis=1)
    return {
        "n": int(d.size),
        "mean": float(d.mean()),
        "ci_low": float(np.percentile(means, 2.5)),
        "ci_high": float(np.percentile(means, 97.5)),
        "frac_positive": float((d > 0).mean()),
    }


def percentile(values: list[float], q: float) -> float | None:
    v = np.asarray([x for x in values if x is not None and np.isfinite(x)], dtype=float)
    if v.size == 0:
        return None
    return float(np.percentile(v, q))


def spearman(x: list[float], y: list[float]) -> dict:
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 3:
        return {"rho": None, "p": None, "n": len(pairs)}
    from scipy.stats import spearmanr

    a = np.array([p[0] for p in pairs], dtype=float)
    b = np.array([p[1] for p in pairs], dtype=float)
    if np.allclose(a, a[0]) or np.allclose(b, b[0]):
        return {"rho": None, "p": None, "n": len(pairs)}
    r = spearmanr(a, b)
    return {"rho": float(r.statistic), "p": float(r.pvalue), "n": len(pairs)}


def cohen_kappa(a: list[bool], b: list[bool]) -> dict:
    if not a or len(a) != len(b):
        return {"kappa": None, "n": 0}
    a_arr = np.asarray(a, dtype=bool)
    b_arr = np.asarray(b, dtype=bool)
    n = a_arr.size
    po = float((a_arr == b_arr).mean())
    pa1, pb1 = a_arr.mean(), b_arr.mean()
    pe = float(pa1 * pb1 + (1 - pa1) * (1 - pb1))
    if abs(1 - pe) < 1e-12:
        return {"kappa": None, "n": int(n), "observed_agreement": po}
    return {
        "kappa": float((po - pe) / (1 - pe)),
        "n": int(n),
        "observed_agreement": po,
        "expected_agreement": pe,
    }


def censoring_sensitivity(per_prompt: list[dict]) -> dict:
    """Primary (alpha_min substitution, already baked into the values) vs
    complete-case (drop prompts where any down-ramp hit the floor)."""
    key = "excess_width" if per_prompt and "excess_width" in per_prompt[0] else "residual"
    prim = [p[key] for p in per_prompt if p[key] is not None]
    cc = [
        p[key]
        for p in per_prompt
        if p[key] is not None and not p.get("censored", False)
    ]
    n_cens = sum(1 for p in per_prompt if p.get("censored", False))
    return {
        "n_prompts": len(per_prompt),
        "n_censored": n_cens,
        "frac_censored": (n_cens / len(per_prompt)) if per_prompt else None,
        "primary_alpha_min_substitution": bootstrap_mean(prim),
        "complete_case": bootstrap_mean(cc),
    }
