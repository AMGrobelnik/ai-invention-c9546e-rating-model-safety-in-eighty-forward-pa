"""Monte-Carlo characterisation of the EWS estimators at the series lengths this
study will actually use (n = 64 and n = 192 generated steps).

Measures, for the lag-1 autocorrelation and the exponential recovery-rate fit:
  * bias and SD of the plain Yule-Walker/pandas r1 estimator
  * bias and SD after the +1/n and the +(1+3*rho)/n corrections
  * bias of lambda from the AR(1) conversion lambda = -ln(phi)
  * bias of lambda from a log-linear fit to an ensemble-mean recovery curve,
    including the noise-floor truncation effect
Deterministic: fixed seed.
"""
import numpy as np, json

RNG = np.random.default_rng(20260812)


def ar1(n, phi, sigma=1.0, rng=RNG):
    x = np.empty(n)
    x[0] = rng.normal(0, sigma / np.sqrt(max(1e-9, 1 - phi**2)))
    e = rng.normal(0, sigma, n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    return x


def r1(x):
    """pandas Series.autocorr(lag=1) == Pearson r of x[:-1] vs x[1:]."""
    a, b = x[:-1], x[1:]
    a = a - a.mean(); b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else np.nan


def ac1_study(ns=(64, 192), phis=(0.3, 0.6, 0.8, 0.9), reps=4000):
    out = []
    for n in ns:
        for phi in phis:
            r = np.array([r1(ar1(n, phi)) for _ in range(reps)])
            out.append(dict(
                n=n, phi=phi,
                raw_mean=float(r.mean()), raw_bias=float(r.mean() - phi),
                raw_sd=float(r.std(ddof=1)),
                corr_1overn_bias=float((r + 1.0 / n).mean() - phi),
                corr_marriott_bias=float((r + (1 + 3 * r) / n).mean() - phi),
            ))
    return out


def lambda_from_phi(ns=(64, 192), phis=(0.6, 0.8, 0.9), reps=4000):
    """lambda = -ln(phi); propagate the r1 bias through the conversion."""
    out = []
    for n in ns:
        for phi in phis:
            true_lam = -np.log(phi)
            r = np.array([r1(ar1(n, phi)) for _ in range(reps)])
            rc = np.clip(r + (1 + 3 * r) / n, 1e-6, 0.999999)
            lam_raw = -np.log(np.clip(r, 1e-6, 0.999999))
            lam_cor = -np.log(rc)
            out.append(dict(
                n=n, phi=phi, true_lambda=float(true_lam),
                lam_raw_mean=float(lam_raw.mean()),
                lam_raw_bias=float(lam_raw.mean() - true_lam),
                lam_corrected_mean=float(lam_cor.mean()),
                lam_corrected_bias=float(lam_cor.mean() - true_lam),
            ))
    return out


def recovery_fit(n_roll=32, lam=0.15, noise=0.05, amp=1.0, horizon=(8, 16, 32, 64),
                 reps=2000, rng=RNG):
    """Ensemble perturbation-recovery: d_t = amp*exp(-lam*t) + N(0, noise).

    Fit log-linear regression of log|mean deviation| on t over a fit window of
    length H. Demonstrates noise-floor truncation: once amp*exp(-lam*t) drops to
    ~noise/sqrt(n_roll), the fit saturates and lambda is UNDER-estimated.
    """
    out = []
    for H in horizon:
        t = np.arange(H)
        true = amp * np.exp(-lam * t)
        lams = []
        for _ in range(reps):
            d = true + rng.normal(0, noise, size=(n_roll, H)).mean(axis=0)
            y = np.abs(d)
            ok = y > 0
            if ok.sum() < 3:
                continue
            sl = np.polyfit(t[ok], np.log(y[ok]), 1)[0]
            lams.append(-sl)
        lams = np.array(lams)
        # step at which signal crosses the ensemble noise floor
        floor = noise / np.sqrt(n_roll)
        t_floor = float(np.log(amp / floor) / lam)
        out.append(dict(fit_window=H, true_lambda=lam,
                        est_mean=float(lams.mean()), bias=float(lams.mean() - lam),
                        sd=float(lams.std(ddof=1)), noise_floor=float(floor),
                        t_cross_floor=t_floor))
    return out


if __name__ == "__main__":
    res = dict(ac1=ac1_study(), lambda_from_phi=lambda_from_phi(),
               recovery_fit=recovery_fit())
    print(json.dumps(res, indent=2))
    with open("estimator_check.json", "w") as f:
        json.dump(res, f, indent=2)
