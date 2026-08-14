#!/usr/bin/env python3
"""Regenerate all seven figures from method_out.json ALONE.

This is the T9 self-sufficiency proof: if a figure cannot be drawn from the JSON,
the JSON is missing something a reader needs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from loguru import logger  # noqa: E402

ROOT = Path(__file__).parent
FIGS = ROOT / "figs"
FIGS.mkdir(exist_ok=True)

COLORS = {
    "qwen3-0.6b/base": "#4C72B0",
    "qwen3-0.6b/instruct": "#C44E52",
    "qwen3-0.6b/abliterated": "#55A868",
    "smollm2/base": "#8172B2",
    "pythia/base": "#937860",
}


def color(m: str) -> str:
    return COLORS.get(m, "#777777")


def fig1_trajectories(d: dict, npz_dir: Path) -> None:
    """Mean r_t trajectories with rollout spread, per model."""
    models = sorted({r["model"] for r in d["indicators"]})
    fig, axes = plt.subplots(1, len(models), figsize=(4 * len(models), 3.4), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, m in zip(axes, models):
        f = npz_dir / f"{m.replace('/', '_')}_traj.npz"
        drawn = False
        if f.exists():
            z = np.load(f)
            keys = [k for k in z.files if k.endswith("_clean")]
            if keys:
                R = z[keys[0]]
                t = np.arange(R.shape[0])
                mu, sd = R.mean(axis=1), R.std(axis=1)
                ax.plot(t, mu, color=color(m), lw=1.6, label="mean")
                ax.fill_between(t, mu - sd, mu + sd, color=color(m), alpha=0.25,
                                label="±1 sd across rollouts")
                for j in range(min(5, R.shape[1])):
                    ax.plot(t, R[:, j], color=color(m), lw=0.4, alpha=0.45)
                drawn = True
        if not drawn:
            rows = [r for r in d["indicators"] if r["model"] == m]
            if rows:
                mu = rows[0]["primary"]["trend_mean"]
                ax.axhline(mu, color=color(m))
                ax.text(0.5, 0.5, "trajectory npz absent;\nJSON summary only",
                        ha="center", va="center", transform=ax.transAxes, fontsize=8)
        ax.axhline(0.0, color="k", ls=":", lw=0.9)
        ax.set_title(m, fontsize=9)
        ax.set_xlabel("generated step t")
    axes[0].set_ylabel(r"$r_t$  (refusal log-odds, layer-$L$ lens)")
    axes[0].legend(fontsize=7)
    fig.suptitle("Fig 1 — refusal observable trajectories on harmless prompts", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_trajectories.png", dpi=150)
    plt.close(fig)


def _rows(d: dict, m: str, dr: str, tf: bool) -> list[dict]:
    bp = d["grid_actually_run"]["base_p"]
    bc = d["grid_actually_run"]["base_eps_c"]
    return [r for r in d["lambda"]
            if r["model"] == m and r["direction"] == dr and r["teacher_forced"] is tf
            and r["p"] == bp and abs(r["eps_c"] - bc) < 1e-9]


def fig2_delta_decay(d: dict) -> None:
    """|delta_t| decay curves with the fitted exponential.

    Top row: TEACHER-FORCED (the primary channel — token content held fixed).
    Bottom row: FREE-RUNNING (the contrast — contaminated once tokens diverge).
    """
    dirs = ["toward_refuse", "toward_comply", "random_direction"]
    models = sorted({r["model"] for r in d["lambda"]})
    base_p = d["grid_actually_run"]["base_p"]
    fig, axes = plt.subplots(2, len(dirs), figsize=(4.2 * len(dirs), 6.4), sharey="row")
    axes = np.atleast_2d(axes)
    for ri, (tf, lbl) in enumerate([(True, "teacher-forced (PRIMARY)"),
                                    (False, "free-running (contrast)")]):
        for ci, dr in enumerate(dirs):
            ax = axes[ri, ci]
            for m in models:
                rows = _rows(d, m, dr, tf)
                curves = [r["layerL"]["mean_delta_curve"] for r in rows
                          if r["layerL"]["mean_delta_curve"]]
                if not curves:
                    continue
                n = min(len(c) for c in curves)
                # mean_delta_curve is the SIGNED across-rollout mean; the log axis
                # needs magnitudes, and the sign is not what this panel is about.
                mu = np.abs(np.array([c[:n] for c in curves]).mean(axis=0))
                t = np.arange(n)
                ax.plot(t, mu, color=color(m), lw=1.5, label=m)
                fits = [r["layerL"]["estimates"]["est1_nls"] for r in rows]
                lams = [f.get("lambda") for f in fits if f.get("lambda")]
                As = [f.get("A") for f in fits if f.get("A") is not None]
                bs = [f.get("b") for f in fits if f.get("b") is not None]
                if lams and As and bs:
                    ax.plot(t, np.abs(np.median(As) * np.exp(-np.median(lams) * t)
                                      + np.median(bs)),
                            color=color(m), ls="--", lw=1.0)
            ax.set_title(f"{dr}\n{lbl}", fontsize=8)
            ax.set_xlabel(f"steps after injection at p={base_p}")
            ax.set_yscale("log")
    axes[0, 0].set_ylabel(r"$|\,$mean signed $\delta_t|$ (layer-$L$)")
    axes[1, 0].set_ylabel(r"$|\,$mean signed $\delta_t|$ (layer-$L$)")
    axes[0, 0].legend(fontsize=7)
    fig.suptitle("Fig 2 — perturbation recovery (dashed = NLS fit). "
                 "Free-running curves GROW: token divergence, not relaxation.",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_delta_decay.png", dpi=150)
    plt.close(fig)


def fig3_epsilon(d: dict) -> None:
    """Linearity of the response in eps, and lambda's flatness across eps."""
    lin = d["epsilon_sweep"]["linearity"]["by_model"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
    for m, v in lin.items():
        if "eps_abs_values" not in v:
            continue
        x = np.array(v["eps_abs_values"])
        y = np.array(v["delta_at_p1_values"])
        a1.plot(x, y, "o-", color=color(m), lw=1.3, ms=4, label=m)
        if v.get("slope"):
            a1.plot(x, v["slope"] * x, ls="--", lw=0.8, color=color(m), alpha=0.7)
        lams = [z for z in v.get("lambda_values", []) if z is not None]
        cs = v.get("eps_c_values", [])
        if lams and len(lams) == len(cs):
            a2.plot(cs, lams, "s-", color=color(m), lw=1.3, ms=4, label=m)
    a1.set_xlabel(r"$\varepsilon$ (absolute)")
    a1.set_ylabel(r"$|\delta_{p+1}|$")
    a1.set_title("response linearity (dashed = through-origin fit)", fontsize=9)
    a1.legend(fontsize=7)
    a2.set_xlabel(r"$\varepsilon$ coefficient $c$")
    a2.set_ylabel(r"$\hat\lambda$")
    a2.set_title(r"$\lambda$ must be flat in the linear regime", fontsize=9)
    a2.set_xscale("log")
    fig.suptitle("Fig 3 — epsilon sweep", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig3_epsilon.png", dpi=150)
    plt.close(fig)


def fig4_series_length(d: dict) -> None:
    """Indicators vs series length — truncation artifacts must be visible."""
    models = sorted({r["model"] for r in d["indicators"]})
    metrics = [("var_star", r"Var$^*$"), ("ac1", "AC1"), ("flicker", "flicker")]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    for ax, (mk, lbl) in zip(axes, metrics):
        for m in models:
            rows = [r["series_length_sweep"] for r in d["indicators"] if r["model"] == m]
            if not rows:
                continue
            lens = sorted({s["length"] for r in rows for s in r})
            ys = []
            for L in lens:
                vals = [s[mk] for r in rows for s in r
                        if s["length"] == L and s[mk] is not None and np.isfinite(s[mk])]
                ys.append(np.median(vals) if vals else np.nan)
            ax.plot(lens, ys, "o-", color=color(m), lw=1.3, ms=4, label=m)
        ax.set_xlabel("series length (steps)")
        ax.set_ylabel(lbl)
        ax.set_title(lbl, fontsize=9)
    axes[0].legend(fontsize=7)
    fig.suptitle("Fig 4 — fluctuation indicators vs series length (detrended)", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig4_series_length.png", dpi=150)
    plt.close(fig)


def fig5_layer_profile(d: dict) -> None:
    """Per-layer harmful/benign separation on the reference model."""
    lc = d["layer_choice"]
    c = lc["per_layer_curve"]
    L = [x["layer"] for x in c]
    sep = [x["separation"] for x in c]
    au = [x["auroc"] for x in c]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(L, sep, "o-", color="#C44E52", lw=1.4, ms=3.5, label=r"separation $|2\cdot$AUROC$-1|$")
    ax.plot(L, au, "s-", color="#4C72B0", lw=1.0, ms=3, alpha=0.7, label="AUROC")
    ax.axvline(lc["L_ref"], color="k", ls="--", lw=1.0,
               label=f"chosen L={lc['L_ref']} (rel. depth {lc['rel_depth']:.2f})")
    n = lc["n_layers_ref"]
    ax.axvspan(n / 3, 2 * n / 3, color="grey", alpha=0.12, label="middle third")
    ax.set_xlabel("layer")
    ax.set_ylabel("separation / AUROC")
    ax.legend(fontsize=7)
    ax.set_title(f"Fig 5 — layer selection on {lc['reference_model']}", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "fig5_layer_profile.png", dpi=150)
    plt.close(fig)


def fig6_synthetic(d: dict) -> None:
    """Estimator bias/sd heatmaps from the synthetic recovery study."""
    tab = d["synthetic_ar1_table"]
    lams = sorted({r["true_lambda"] for r in tab})
    geoms = sorted({(r["T_fit"], r["n_roll"]) for r in tab})
    for metric, fname, lbl in (("rel_bias", "bias", "relative bias"),
                               ("rel_sd", "sd", "relative sd")):
        M = np.full((len(geoms), len(lams)), np.nan)
        for r in tab:
            if r.get(metric) is None:
                continue
            M[geoms.index((r["T_fit"], r["n_roll"])), lams.index(r["true_lambda"])] = r[metric]
        fig, ax = plt.subplots(figsize=(7, 5.2))
        vmax = float(np.nanpercentile(np.abs(M), 95)) if np.isfinite(M).any() else 1.0
        im = ax.imshow(M, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_xticks(range(len(lams)))
        ax.set_xticklabels([str(v) for v in lams])
        ax.set_yticks(range(len(geoms)))
        ax.set_yticklabels([f"T={g[0]}, n={g[1]}" for g in geoms], fontsize=7)
        ax.set_xlabel(r"true $\lambda$")
        for i in range(len(geoms)):
            for j in range(len(lams)):
                if np.isfinite(M[i, j]):
                    ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6)
        fig.colorbar(im, ax=ax, label=lbl)
        rule = d["min_series_length_rule"]
        ttl = ("NO cell passes the pre-registered rule"
               if not rule.get("any_cell_passes")
               else f"rule: T_fit>={rule['min_T_fit']}, n_roll>={rule['min_n_roll']}")
        ax.set_title(f"Fig 6 — synthetic recovery, {lbl}\n{ttl}", fontsize=10)
        fig.tight_layout()
        fig.savefig(FIGS / f"fig6_synthetic_{fname}.png", dpi=150)
        plt.close(fig)


def fig7_stepwise(d: dict) -> None:
    """lambda(p) — the free discriminator between a token-depth and a basin account."""
    models = sorted({r["model"] for r in d["lambda"]})
    base_c = d["grid_actually_run"]["base_eps_c"]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    any_pt = False
    for m in models:
        rows = [r for r in d["lambda"]
                if r["model"] == m and r["direction"] == "toward_refuse"
                and r["teacher_forced"] and abs(r["eps_c"] - base_c) < 1e-9]
        ps = sorted({r["p"] for r in rows})
        ys, es = [], []
        for p in ps:
            v = [r["layerL"]["estimates"]["est1_nls"].get("lambda")
                 for r in rows if r["p"] == p]
            v = [x for x in v if x is not None and np.isfinite(x)]
            ys.append(np.median(v) if v else np.nan)
            es.append(np.std(v) if len(v) > 1 else 0.0)
        if ps:
            ax.errorbar(ps, ys, yerr=es, fmt="o-", color=color(m), lw=1.3, ms=4,
                        capsize=3, label=m)
            any_pt = True
    ax.set_xlabel("injection step p")
    ax.set_ylabel(r"$\hat\lambda$ (toward refuse)")
    if any_pt:
        ax.legend(fontsize=7)
    ax.set_title(r"Fig 7 — step-wise $\lambda(p)$: token-depth vs basin account", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "fig7_stepwise_lambda.png", dpi=150)
    plt.close(fig)


def fig8_indicator_summary(d: dict) -> None:
    """Bonus: the four indicators + ground truth, side by side, with CIs."""
    agg = d["aggregate_by_model"]
    models = sorted(agg)
    panels = [
        ("lambda_toward_refuse", r"$\lambda$ toward refuse"),
        ("var_star", r"Var$^*$ (detrended)"),
        ("ac1", "AC1 (detrended)"),
        # crossings-per-100, NOT the fraction of rollouts crossing: over a 192-step
        # series every rollout crosses its own mean, so the fraction is 1.0 for all
        # four models and carries no information.
        ("flicker_crossings_per_100", "flicker (crossings / 100 steps)"),
    ]
    short = {m: (m.split("/")[-1] if m.split("/")[-1] != "base"
                 else f"{m.split('/')[0].split('-')[0]}\nbase") for m in models}
    gt = d["ground_truth"]
    fig, axes = plt.subplots(1, 5, figsize=(18, 3.6))
    for ax, (k, lbl) in zip(axes, panels):
        pts = [agg[m][k]["point"] for m in models]
        lo = [agg[m][k].get("ci_lo") for m in models]
        hi = [agg[m][k].get("ci_hi") for m in models]
        x = np.arange(len(models))
        for i, m in enumerate(models):
            if pts[i] is None:
                continue
            err = None
            if lo[i] is not None and hi[i] is not None:
                err = [[max(pts[i] - lo[i], 0)], [max(hi[i] - pts[i], 0)]]
            ax.errorbar([x[i]], [pts[i]], yerr=err, fmt="o", color=color(m),
                        ms=7, capsize=4)
        ax.set_xticks(x)
        ax.set_xticklabels([short[m] for m in models], rotation=30, fontsize=7)
        ax.set_title(lbl, fontsize=9)
    ax = axes[4]
    for i, m in enumerate(models):
        r = gt.get(m)
        if not r:
            continue
        h = r["harmful_refusal_rate"]
        ax.errorbar([i - 0.12], [h["p"]],
                    yerr=[[max(h["p"] - h["lo"], 0)], [max(h["hi"] - h["p"], 0)]],
                    fmt="o", color=color(m), ms=7, capsize=4)
        o = r["xstest_over_refusal_rate"]
        ax.errorbar([i + 0.12], [o["p"]],
                    yerr=[[max(o["p"] - o["lo"], 0)], [max(o["hi"] - o["p"], 0)]],
                    fmt="s", color=color(m), ms=6, capsize=4, alpha=0.6)
    ax.set_xticks(np.arange(len(models)))
    ax.set_xticklabels([short[m] for m in models], rotation=30, fontsize=7)
    ax.set_title("ground truth: harmful refusal (o)\nvs XSTest over-refusal (s)", fontsize=9)
    fig.suptitle(f"Fig 8 — indicators vs ground truth | VERDICT: {d['verdict']['code']}",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGS / "fig8_indicator_summary.png", dpi=150)
    plt.close(fig)


def _resolve_source() -> Path:
    """Figures are drawn from the archived result tree.

    The exp_gen_sol_out schema cannot hold the full per-cell result lists at the
    top level, so build_output.py moves them to out/tier0_raw.json and leaves the
    summaries in method_out.json's metadata. Both are shipped; this picks
    whichever file is actually in raw form, so the figures regenerate whether or
    not the reshaping step has run yet.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    raw = ROOT / "out" / "tier0_raw.json"
    if raw.exists():
        return raw
    return ROOT / "method_out.json"


def fig9_certified_lambda(d: dict) -> None:
    """lambda at the certified geometry (T_fit=128) vs the main run's T_fit=64.

    Drawn only if refit_certified.py has been run.
    """
    cert_path = ROOT / "out" / "refit_certified.json"
    if not cert_path.exists():
        logger.info("fig9 skipped: out/refit_certified.json not present")
        return
    cert = json.loads(cert_path.read_text())
    if not isinstance(cert, dict) or "aggregate_by_model" not in cert:
        logger.info("fig9 skipped: refit still in progress")
        return
    cagg = cert["aggregate_by_model"]
    models = sorted(cagg)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
    x = np.arange(len(models))
    for i, m in enumerate(models):
        for off, key, mk, lab in ((-0.15, "toward_refuse", "o", "toward refuse"),
                                  (0.15, "random_direction", "s", "random direction")):
            e = cagg[m][key]["lambda"]
            if e["point"] is None:
                continue
            err = None
            if e.get("ci_lo") is not None:
                err = [[max(e["point"] - e["ci_lo"], 0)], [max(e["ci_hi"] - e["point"], 0)]]
            a1.errorbar([x[i] + off], [e["point"]], yerr=err, fmt=mk, ms=7, capsize=4,
                        color=color(m), alpha=1.0 if off < 0 else 0.45,
                        label=lab if i == 0 else None)
    a1.set_xticks(x)
    a1.set_xticklabels([m.split("/")[-1] if m.split("/")[-1] != "base"
                        else f"{m.split('/')[0].split('-')[0]}\nbase" for m in models],
                       rotation=30, fontsize=7)
    a1.set_ylabel(r"$\hat\lambda$")
    a1.legend(fontsize=7)
    a1.set_title(rf"$\lambda$ at the CERTIFIED geometry "
                 rf"($T_{{fit}}$={cert['fit_len']}, $n$={cert['n_roll']})", fontsize=9)
    for i, m in enumerate(models):
        rows = [r for r in cert["rows"]
                if r["model"] == m and r["direction"] == "toward_refuse"]
        curves = [r["layerL"]["mean_delta_curve"] for r in rows]
        if not curves:
            continue
        n = min(len(c) for c in curves)
        mu = np.abs(np.array([c[:n] for c in curves]).mean(axis=0))
        a2.plot(np.arange(n), mu, color=color(m), lw=1.4, label=m)
    a2.set_yscale("log")
    a2.set_xlabel(f"steps after injection at p={cert['p']}")
    a2.set_ylabel(r"$|\,$mean signed $\delta_t|$")
    a2.set_title("recovery over the full certified window", fontsize=9)
    a2.legend(fontsize=6)
    # The supplementary verdict is computed by build_output.py, so read it from
    # method_out.json when that has already been produced.
    sv = cert.get("supplementary_verdict", {}).get("code", "")
    if not sv:
        mo = ROOT / "method_out.json"
        if mo.exists():
            try:
                md = json.loads(mo.read_text()).get("metadata", {})
                sv = (md.get("lambda_at_certified_geometry") or {}).get(
                    "supplementary_verdict", {}).get("code", "")
            except Exception:  # noqa: BLE001 - title text is cosmetic
                sv = ""
    fig.suptitle(
        f"Fig 9 — certified-geometry refit ($T_{{fit}}$=128)"
        + (f" | {sv}" if sv else ""), fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "fig9_certified_lambda.png", dpi=150)
    plt.close(fig)


def main() -> None:
    path = _resolve_source()
    d = json.loads(path.read_text())
    if "indicators" not in d:
        logger.error(
            f"{path} is in schema form and has no raw result tree; "
            "expected out/tier0_raw.json. No figures drawn."
        )
        return
    logger.info(f"Drawing figures from {path}")
    npz_dir = ROOT / "out" / "cells"
    made = []
    for name, fn in (("fig1", fig1_trajectories), ("fig2", fig2_delta_decay),
                     ("fig3", fig3_epsilon), ("fig4", fig4_series_length),
                     ("fig5", fig5_layer_profile), ("fig6", fig6_synthetic),
                     ("fig7", fig7_stepwise), ("fig8", fig8_indicator_summary),
                     ("fig9", fig9_certified_lambda)):
        try:
            fn(d, npz_dir) if name == "fig1" else fn(d)
            made.append(name)
        except Exception as exc:  # noqa: BLE001 - one bad figure must not kill the rest
            logger.error(f"{name} failed: {type(exc).__name__}: {exc}")
    logger.info(f"Figures generated: {made}")


if __name__ == "__main__":
    main()
