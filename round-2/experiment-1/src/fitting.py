#!/usr/bin/env python3
"""Dose-response estimation of alpha_50 and its uncertainty.

Three estimators on the SAME Bernoulli draws:
  * 2-parameter logistic  P = sigmoid(b0 + b1 * alpha),         a50 = -b0/b1
  * 4-parameter logistic  P = c + (d - c) * sigmoid(b1*(a-a50)) with free floor/ceiling
  * non-parametric        linear interpolation of the empirical rate at 0.5

Uncertainty: CLUSTER bootstrap over PROMPTS (all seeds of a drawn prompt travel
together), and a PAIRED cluster bootstrap for between-model differences (the same
prompt indices are drawn for both models and both are refit).
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize

BOOT_SEED = 20260812
N_BOOT = 5000


# ---------------------------------------------------------------------------
# Binomial interval
# ---------------------------------------------------------------------------
def wilson_ci(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


# ---------------------------------------------------------------------------
# Likelihoods
# ---------------------------------------------------------------------------
def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 0.5 * (1.0 + np.tanh(0.5 * np.clip(x, -60.0, 60.0)))


def _nll_2p(theta: np.ndarray, a: np.ndarray, y: np.ndarray, l2: float) -> float:
    p = np.clip(_sigmoid(theta[0] + theta[1] * a), 1e-9, 1 - 1e-9)
    nll = -float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return nll + l2 * float(np.dot(theta, theta))


def _nll_4p(theta: np.ndarray, ua: np.ndarray, k: np.ndarray, n: np.ndarray) -> float:
    c = _sigmoid(np.array([theta[0]]))[0]
    d = _sigmoid(np.array([theta[1]]))[0]
    b1, a50 = theta[2], theta[3]
    lo, hi = min(c, d), max(c, d)
    p = np.clip(lo + (hi - lo) * _sigmoid(b1 * (ua - a50)), 1e-9, 1 - 1e-9)
    return -float(np.sum(k * np.log(p) + (n - k) * np.log(1 - p)))


def aggregate(a: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bernoulli draws -> per-alpha (successes, trials).  The binomial likelihood
    on the aggregate is IDENTICAL to the Bernoulli likelihood up to a constant,
    so nothing is lost and the fit becomes ~1000x cheaper."""
    ua, inv = np.unique(np.round(a, 6), return_inverse=True)
    k = np.bincount(inv, weights=y, minlength=ua.size)
    n = np.bincount(inv, minlength=ua.size).astype(float)
    return ua, k, n


def irls_2p(alphas: np.ndarray, k: np.ndarray, n: np.ndarray, l2: float = 1e-3,
            max_iter: int = 60, tol: float = 1e-10) -> tuple[float, float, bool]:
    """Newton/IRLS for ridge-penalised binomial logistic on aggregated counts.

    The ridge term is the separation guard (a Firth-style stand-in): with a
    perfectly separated grid the unpenalised slope diverges, and the penalty
    keeps b1 finite while leaving a50 = -b0/b1 essentially unbiased.
    """
    X = np.column_stack([np.ones_like(alphas), alphas])
    beta = np.zeros(2)
    pen = np.diag([l2, l2])
    for _ in range(max_iter):
        eta = X @ beta
        p = _sigmoid(eta)
        w = n * p * (1 - p) + 1e-12
        grad = X.T @ (k - n * p) - 2.0 * pen @ beta
        H = (X * w[:, None]).T @ X + 2.0 * pen
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            return float(beta[0]), float(beta[1]), False
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            return float(beta[0]), float(beta[1]), True
    return float(beta[0]), float(beta[1]), True


def fit_2p(a: np.ndarray, y: np.ndarray, l2: float = 1e-3) -> dict:
    """Ridge-penalised logistic MLE (IRLS on aggregated counts)."""
    if a.size == 0 or len(np.unique(y)) < 2:
        return {"defined": False, "reason": "no variation in outcome", "a50": None}
    ua, k, n = aggregate(a, y)
    b0, b1, ok = irls_2p(ua, k, n, l2)
    if not ok or not np.isfinite(b0) or not np.isfinite(b1):
        return {"defined": False, "reason": "IRLS did not converge", "a50": None}
    if b1 <= 1e-6:
        return {"defined": False, "reason": "slope not positive", "a50": None,
                "b0": b0, "b1": b1}
    p = np.clip(_sigmoid(b0 + b1 * ua), 1e-9, 1 - 1e-9)
    nll = -float(np.sum(k * np.log(p) + (n - k) * np.log(1 - p)))
    return {"defined": True, "a50": float(-b0 / b1), "b0": b0, "b1": b1,
            "nll": nll, "l2_penalty": l2, "n_alphas": int(ua.size)}


def fit_4p(a: np.ndarray, y: np.ndarray, warm: list[float] | None = None) -> dict:
    if a.size == 0 or len(np.unique(y)) < 2:
        return {"defined": False, "reason": "no variation in outcome", "a50": None}
    ua, k, n = aggregate(a, y)
    amid = float(np.median(a))
    starts = ([-4.0, 4.0, 8.0, amid], [-2.0, 2.0, 4.0, 0.5], [-6.0, 3.0, 12.0, 0.6])
    if warm is not None:
        starts = (list(warm),)  # bootstrap: one warm-started restart is enough
    best = None
    for start in starts:
        try:
            r = minimize(
                _nll_4p, np.array(start, dtype=float), args=(ua, k, n),
                method="Nelder-Mead",
                options={"maxiter": 4000, "maxfev": 4000, "xatol": 1e-7, "fatol": 1e-9},
            )
        except (ValueError, FloatingPointError):
            continue
        if best is None or r.fun < best.fun:
            best = r
    if best is None:
        return {"defined": False, "reason": "optimiser failed", "a50": None}
    c = float(_sigmoid(np.array([best.x[0]]))[0])
    d = float(_sigmoid(np.array([best.x[1]]))[0])
    lo, hi = min(c, d), max(c, d)
    b1, a50_mid = float(best.x[2]), float(best.x[3])
    if b1 <= 1e-6 or hi <= 0.5 or lo >= 0.5:
        # the curve never crosses the ABSOLUTE 0.5 level
        return {"defined": False, "reason": "curve does not cross 0.5",
                "floor": lo, "ceiling": hi, "b1": b1, "a50_midpoint": a50_mid,
                "a50": None}
    # alpha at which the 4p curve equals 0.5 in absolute probability
    frac = (0.5 - lo) / (hi - lo)
    a50 = a50_mid + math.log(frac / (1 - frac)) / b1
    return {"defined": True, "a50": float(a50), "floor": lo, "ceiling": hi,
            "b1": b1, "a50_midpoint": a50_mid, "nll": float(best.fun)}


def nonparametric_a50(alphas: np.ndarray, rates: np.ndarray, target: float = 0.5):
    """Linear interpolation of the empirical rate curve at `target`."""
    order = np.argsort(alphas)
    a, r = np.asarray(alphas)[order], np.asarray(rates)[order]
    for i in range(1, len(a)):
        if r[i - 1] < target <= r[i]:
            if r[i] == r[i - 1]:
                return float(a[i])
            f = (target - r[i - 1]) / (r[i] - r[i - 1])
            return float(a[i - 1] + f * (a[i] - a[i - 1]))
    return None


# ---------------------------------------------------------------------------
# The estimate for one (model, axis, scorer)
# ---------------------------------------------------------------------------
def summarise_draws(rows: list[dict]) -> dict:
    """rows: {prompt_uid, seed, alpha, refused(bool), fluent(bool)}."""
    by_alpha: dict[float, list[int]] = {}
    for r in rows:
        by_alpha.setdefault(round(float(r["alpha"]), 6), []).append(int(bool(r["refused"])))
    alphas = sorted(by_alpha)
    out = []
    for a in alphas:
        v = by_alpha[a]
        k, n = int(sum(v)), len(v)
        lo, hi = wilson_ci(k, n)
        out.append({"alpha": a, "n": n, "k": k, "rate": k / n if n else None,
                    "wilson_lo": lo, "wilson_hi": hi})
    return {"per_alpha": out, "max_rate": max((r["rate"] for r in out), default=0.0)}


def estimate_a50(rows: list[dict]) -> dict:
    """Full point estimate + all three estimators. `rows` must already be
    fluency-filtered and censorship-filtered."""
    a = np.array([float(r["alpha"]) for r in rows], dtype=float)
    y = np.array([1.0 if r["refused"] else 0.0 for r in rows], dtype=float)
    summ = summarise_draws(rows)
    curve_a = np.array([p["alpha"] for p in summ["per_alpha"]], dtype=float)
    curve_r = np.array([p["rate"] for p in summ["per_alpha"]], dtype=float)
    crosses = bool(summ["max_rate"] >= 0.5)
    f2, f4 = fit_2p(a, y), fit_4p(a, y)
    npar = nonparametric_a50(curve_a, curve_r)
    return {
        "n_draws": int(a.size),
        "max_rate": float(summ["max_rate"]),
        "observed_crossing": crosses,
        "alpha_min_measured": float(curve_a.min()) if curve_a.size else None,
        "alpha_max_measured": float(curve_a.max()) if curve_a.size else None,
        "fit_2p": f2,
        "fit_4p": f4,
        "nonparametric_a50": npar,
        "per_alpha": summ["per_alpha"],
    }


def pick_primary(est: dict) -> tuple[float | None, str]:
    """2p is primary when the empirical curve reaches ~1.0; the 4p fit (free
    floor/ceiling) becomes primary when the ceiling is materially below 1.

    HARD RULE: an alpha_50 outside the MEASURED alpha range is an extrapolation
    beyond the outer edge of measurement and is never returned as the primary
    estimate. When the parametric fits extrapolate, the non-parametric
    interpolation of the empirical curve (which is inside the range by
    construction) is used instead, and the estimator name records it.
    """
    if not est["observed_crossing"]:
        return None, "undefined_no_crossing"
    hi = est.get("alpha_max_measured")
    lo = est.get("alpha_min_measured")

    def in_range(v) -> bool:
        return (v is not None and np.isfinite(v)
                and (lo is None or v >= lo - 1e-9) and (hi is None or v <= hi + 1e-9))

    f4, f2 = est["fit_4p"], est["fit_2p"]
    cands: list[tuple[float | None, str]] = []
    if f4.get("defined") and f4.get("ceiling", 1.0) < 0.9:
        cands.append((f4["a50"], "4p"))
        if f2.get("defined"):
            cands.append((f2["a50"], "2p"))
    else:
        if f2.get("defined"):
            cands.append((f2["a50"], "2p"))
        if f4.get("defined"):
            cands.append((f4["a50"], "4p"))
    for v, name in cands:
        if in_range(v):
            return v, name
    if est["nonparametric_a50"] is not None:
        return est["nonparametric_a50"], "nonparametric_after_extrapolating_fit"
    return None, "undefined_fit_failed"


# ---------------------------------------------------------------------------
# Cluster bootstrap
# ---------------------------------------------------------------------------
def _warm_start(rows: list[dict]) -> list[float] | None:
    """Full-sample 4p parameters, used to warm-start every bootstrap refit."""
    a = np.array([float(r["alpha"]) for r in rows])
    y = np.array([1.0 if r["refused"] else 0.0 for r in rows])
    f = fit_4p(a, y)
    if not f.get("defined"):
        return None
    lo, hi = max(min(f["floor"], 0.999), 1e-4), max(min(f["ceiling"], 0.999), 1e-4)
    logit = lambda p: float(np.log(p / (1 - p)))  # noqa: E731
    return [logit(lo), logit(hi), f["b1"], f["a50_midpoint"]]


class ClusterCounts:
    """Per-prompt success/trial counts on a shared alpha grid.

    A cluster bootstrap draw is then a row-sum of a resampled count matrix, so
    5000 refits cost a handful of vectorised Newton steps rather than 5000
    Nelder-Mead runs.
    """

    def __init__(self, rows: list[dict], grid: np.ndarray | None = None):
        self.uids = sorted({r["prompt_uid"] for r in rows})
        alphas = np.unique(np.round([float(r["alpha"]) for r in rows], 6))
        self.grid = alphas if grid is None else grid
        gi = {a: i for i, a in enumerate(self.grid)}
        self.K = np.zeros((len(self.uids), self.grid.size))
        self.N = np.zeros((len(self.uids), self.grid.size))
        ui = {u: i for i, u in enumerate(self.uids)}
        for r in rows:
            j = gi.get(round(float(r["alpha"]), 6))
            if j is None:
                continue
            i = ui[r["prompt_uid"]]
            self.N[i, j] += 1.0
            self.K[i, j] += 1.0 if r["refused"] else 0.0

    def total(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.grid, self.K.sum(0), self.N.sum(0)

    def draw(self, idx: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.grid, self.K[idx].sum(0), self.N[idx].sum(0)


def rising_branch(rows: list[dict]) -> list[dict]:
    """Trim the draws to alphas at or below the PEAK of the empirical rate curve.

    Beyond the peak the refusal rate falls again: steering that strong stops
    producing a refusal opener and starts producing off-task text, so a
    monotone dose-response model is misspecified there.  Fitting the rising
    branch is the sensitivity analysis for that.  (Decided AFTER seeing the
    curves; recorded as a deviation.)
    """
    by: dict[float, list[int]] = {}
    for r in rows:
        by.setdefault(round(float(r["alpha"]), 6), []).append(int(bool(r["refused"])))
    if not by:
        return rows
    alphas = sorted(by)
    rates = [sum(by[a]) / len(by[a]) for a in alphas]
    a_peak = alphas[int(np.argmax(rates))]
    return [r for r in rows if round(float(r["alpha"]), 6) <= a_peak + 1e-9]


def _a50_from_counts(grid: np.ndarray, k: np.ndarray, n: np.ndarray,
                     mode: str, warm: list[float] | None = None) -> float | None:
    m = n > 0
    if m.sum() < 2:
        return None
    if mode == "np":
        return nonparametric_a50(grid[m], k[m] / n[m])
    if mode == "4p":
        # the 4p path needs draw-shaped input; reconstruct it from the counts
        a_arr = np.repeat(grid[m], n[m].astype(int))
        y_arr = np.concatenate([
            np.concatenate([np.ones(int(round(k[i]))),
                            np.zeros(int(round(n[i] - k[i])))])
            for i in np.where(m)[0]])
        f = fit_4p(a_arr, y_arr, warm=warm)
        return f["a50"] if f.get("defined") else None
    b0, b1, ok = irls_2p(grid[m], k[m], n[m])
    if not ok or b1 <= 1e-6 or not np.isfinite(b0) or not np.isfinite(b1):
        return None
    return float(-b0 / b1)


def bootstrap_a50(rows: list[dict], mode: str = "2p", n_boot: int = N_BOOT,
                  seed: int = BOOT_SEED) -> dict:
    cc = ClusterCounts(rows)
    if len(cc.uids) < 2:
        return {"n_prompts": len(cc.uids), "ci_lo": None, "ci_hi": None, "n_ok": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(cc.uids), size=(n_boot, len(cc.uids)))
    vals = []
    warm = _warm_start(rows) if mode == "4p" else None
    for row in idx:
        g, k, n = cc.draw(row)
        v = _a50_from_counts(g, k, n, mode, warm)
        if v is not None and np.isfinite(v):
            vals.append(v)
    if len(vals) < 20:
        return {"n_prompts": len(cc.uids), "ci_lo": None, "ci_hi": None,
                "n_ok": len(vals), "n_boot": n_boot}
    v = np.array(vals)
    return {
        "n_prompts": len(cc.uids),
        "n_boot": n_boot,
        "n_ok": len(vals),
        "boot_median": float(np.median(v)),
        "ci_lo": float(np.percentile(v, 2.5)),
        "ci_hi": float(np.percentile(v, 97.5)),
        "sd": float(v.std(ddof=1)),
    }


def paired_bootstrap_diff(rows_a: list[dict], rows_b: list[dict], mode: str = "2p",
                          n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """CI of a50(A) - a50(B) resampling the SAME prompt indices for both."""
    grid = np.unique(np.round(
        [float(r["alpha"]) for r in rows_a] + [float(r["alpha"]) for r in rows_b], 6))
    ca, cb = ClusterCounts(rows_a, grid), ClusterCounts(rows_b, grid)
    shared = sorted(set(ca.uids) & set(cb.uids))
    if len(shared) < 2:
        return {"n_prompts": len(shared), "delta": None, "ci_lo": None, "ci_hi": None}
    ia = np.array([ca.uids.index(u) for u in shared])
    ib = np.array([cb.uids.index(u) for u in shared])
    wa = _warm_start(rows_a) if mode == "4p" else None
    wb = _warm_start(rows_b) if mode == "4p" else None
    pa = _a50_from_counts(*ca.draw(ia), mode, wa)
    pb = _a50_from_counts(*cb.draw(ib), mode, wb)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(shared), size=(n_boot, len(shared)))
    diffs = []
    for row in idx:
        va = _a50_from_counts(*ca.draw(ia[row]), mode, wa)
        vb = _a50_from_counts(*cb.draw(ib[row]), mode, wb)
        if va is not None and vb is not None and np.isfinite(va) and np.isfinite(vb):
            diffs.append(float(va - vb))
    if len(diffs) < 20:
        return {"n_prompts": len(shared), "delta": None, "ci_lo": None,
                "ci_hi": None, "n_ok": len(diffs)}
    d = np.array(diffs)
    lo, hi = float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))
    return {
        "n_prompts": len(shared),
        "n_boot": n_boot,
        "n_ok": len(diffs),
        "delta": (float(pa - pb) if pa is not None and pb is not None else None),
        "a50_a": pa, "a50_b": pb,
        "boot_median_delta": float(np.median(d)),
        "ci_lo": lo, "ci_hi": hi,
        "overlaps_zero": bool(lo <= 0.0 <= hi),
        "frac_positive": float((d > 0).mean()),
    }


# ---------------------------------------------------------------------------
# D1 / D2: estimator certification and power, at the REAL geometry
# ---------------------------------------------------------------------------
def simulate_rows(alphas: list[float], n_prompts: int, n_seeds: int, a50: float,
                  slope: float, rng: np.random.Generator,
                  prompt_sd: float = 0.0) -> list[dict]:
    rows = []
    offs = rng.normal(0.0, prompt_sd, size=n_prompts) if prompt_sd > 0 else np.zeros(n_prompts)
    for p in range(n_prompts):
        for s in range(n_seeds):
            for a in alphas:
                pr = float(_sigmoid(np.array([slope * (a - a50 - offs[p])]))[0])
                rows.append({"prompt_uid": f"p{p}", "seed": s, "alpha": a,
                             "refused": bool(rng.random() < pr)})
    return rows


def synthetic_recovery(alphas: list[float], n_prompts: int, n_seeds: int,
                       a50_true: float = 0.5, slope: float = 8.0,
                       n_rep: int = 500, n_boot: int = 400, seed: int = 7) -> dict:
    """D1: does the estimator recover a known a50 at the ACTUAL geometry, and do
    its bootstrap CIs cover the truth at the nominal 95%?"""
    rng = np.random.default_rng(seed)
    ests, covered = [], []
    for i in range(n_rep):
        rows = simulate_rows(alphas, n_prompts, n_seeds, a50_true, slope, rng)
        a = np.array([r["alpha"] for r in rows]); y = np.array([float(r["refused"]) for r in rows])
        f = fit_2p(a, y)
        if not f["defined"]:
            continue
        ests.append(f["a50"])
        if i < 120:  # CI coverage on a subset (bootstrap is the expensive part)
            b = bootstrap_a50(rows, mode="2p", n_boot=n_boot, seed=1000 + i)
            if b.get("ci_lo") is not None:
                covered.append(bool(b["ci_lo"] <= a50_true <= b["ci_hi"]))
    e = np.array(ests)
    return {
        "a50_true": a50_true, "slope": slope, "n_rep": int(e.size),
        "median_a50": float(np.median(e)) if e.size else None,
        "bias": float(np.median(e) - a50_true) if e.size else None,
        "sd_a50": float(e.std(ddof=1)) if e.size > 1 else None,
        "iqr": [float(np.percentile(e, 25)), float(np.percentile(e, 75))] if e.size else None,
        "ci_coverage": float(np.mean(covered)) if covered else None,
        "n_coverage_rep": len(covered),
        "pass_median_within_0p02": bool(e.size and abs(np.median(e) - a50_true) <= 0.02),
        "pass_coverage_90_to_99": bool(covered and 0.90 <= float(np.mean(covered)) <= 0.995),
    }


def _power_at(delta: float, alphas: list[float], n_prompts: int, n_seeds: int,
              slope: float, n_rep: int, n_boot: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_rep):
        ra = simulate_rows(alphas, n_prompts, n_seeds, 0.5 + delta, slope, rng)
        rb = simulate_rows(alphas, n_prompts, n_seeds, 0.5, slope, rng)
        d = paired_bootstrap_diff(ra, rb, mode="2p", n_boot=n_boot,
                                  seed=int(rng.integers(1_000_000_000)))
        if d.get("ci_lo") is not None and not d["overlaps_zero"]:
            hits += 1
    return hits / max(n_rep, 1)


def power_curve(alphas: list[float], n_prompts: int, n_seeds: int, slope: float = 8.0,
                deltas: tuple[float, ...] = (0.025, 0.05, 0.075, 0.10, 0.15, 0.20),
                n_rep: int = 60, n_boot: int = 200, seed: int = 11) -> dict:
    """D2: minimum detectable difference of the paired bootstrap at 80% power."""
    out = []
    for i, d in enumerate(deltas):
        p = _power_at(d, alphas, n_prompts, n_seeds, slope, n_rep, n_boot, seed + 97 * i)
        out.append({"delta": d, "power": p, "n_rep": n_rep})
    mde = next((r["delta"] for r in out if r["power"] >= 0.80), None)
    return {"curve": out, "mde_80pct": mde, "slope_assumed": slope,
            "n_prompts": n_prompts, "n_seeds": n_seeds, "n_alphas": len(alphas)}


# ---------------------------------------------------------------------------
# Agreement
# ---------------------------------------------------------------------------
def cohen_kappa(a: list[bool], b: list[bool]) -> dict:
    if not a or len(a) != len(b):
        return {"kappa": None, "n": 0}
    x, y = np.asarray(a, dtype=bool), np.asarray(b, dtype=bool)
    po = float((x == y).mean())
    pe = float(x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean()))
    if abs(1 - pe) < 1e-12:
        return {"kappa": None, "n": int(x.size), "observed_agreement": po,
                "note": "degenerate: one rater is constant"}
    return {"kappa": float((po - pe) / (1 - pe)), "n": int(x.size),
            "observed_agreement": po, "expected_agreement": pe}
