#!/usr/bin/env python3
"""Regenerate every figure FROM eval_out.json, so no figure can disagree with it.

F1 forest of oriented rho (hand-written: the CIs are asymmetric and carry a
   jackknife-range whisker, which no catalogue type draws)
F2 ceiling-check bar          (generator: bar)
F3 per-member paired quantile deltas (generator: heatmap)
F4 AMS 3 x 4 reproduction heatmap    (generator: heatmap)
F5 layer-sensitivity dual estimator  (generator: line)
"""

from __future__ import annotations

import json
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
from loguru import logger

SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen")
GEN = SKILL / "scripts" / "chart_gen.py"
sys.path.insert(0, str(SKILL / "scripts"))

WS = Path(__file__).resolve().parent
FIGS = WS / "figs"
R = json.loads((WS / "eval_out.json").read_text())["metadata"]["results"]

AXIS_SHORT = {"plain_harmful_refusal": "plain-harmful refusal",
              "jailbreak_asr": "jailbreak ASR",
              "xstest_over_refusal": "XSTest over-refusal"}


def run_spec(spec: dict, name: str) -> None:
    out = FIGS / name
    p = subprocess.run([sys.executable, str(GEN), "--spec", "-", "--out", str(out)],
                       input=json.dumps(spec), text=True, capture_output=True)
    if p.returncode != 0:
        logger.error(f"{name} REFUSED: {p.stdout.strip()} {p.stderr.strip()}")
        raise SystemExit(f"figure {name} refused")
    logger.info(f"{name}: {p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'ok'}")


def fig1() -> None:
    """Forest of oriented rho per score per judged axis, with jackknife whiskers."""
    import matplotlib.pyplot as plt
    from chart_geometry import assert_text_is_legible
    from chart_style import (apply_house_style, PALETTE, assert_axis_names_are_unique,
                             clear_legends_of_data, fit_legends, fit_tick_labels, fit_titles,
                             literal, place_legend)

    head = R["sign_orientation"]["oriented_headline_delta"]
    rows = []
    for ax_key, short in AXIS_SHORT.items():
        h = head[ax_key]
        rows.append((f"our-AMS sigma / {short}", h["rho_b"], h["ci_rho_b"],
                     h["jackknife_rho_b_range"], 1))
        rows.append((f"alpha_50 (non-par.) / {short}", h["rho_a"], h["ci_rho_a"],
                     h["jackknife_rho_a_range"], 0))

    apply_house_style()
    with warnings.catch_warnings(record=True):
        fig, ax = plt.subplots(figsize=(7.6, 4.4), layout="constrained")
        y = np.arange(len(rows))
        seen = set()
        for i, (lab, v, ci, jk, grp) in enumerate(rows):
            col = PALETTE[grp]
            name = ["alpha_50 (non-parametric)", "our-AMS sigma"][grp]
            ax.plot([jk[0], jk[1]], [i + 0.20, i + 0.20], color=col, alpha=0.45, lw=6,
                    solid_capstyle="butt",
                    label=(literal("leave-one-lineage-out range")
                           if "jk" not in seen and grp == 0 else None))
            if grp == 0:
                seen.add("jk")
            ax.plot([ci[0], ci[1]], [i, i], color=col, lw=1.6)
            ax.plot([ci[0], ci[0], np.nan, ci[1], ci[1]],
                    [i - 0.12, i + 0.12, np.nan, i - 0.12, i + 0.12], color=col, lw=1.6)
            ax.plot([v], [i], "o", color=col, markersize=7,
                    label=literal(name) if name not in seen else None)
            seen.add(name)
        ax.axvline(0.0, color="#999999", linestyle="--", linewidth=1)
        ax.set_yticks(y, labels=[literal(r[0]) for r in rows])
        ax.invert_yaxis()
        ax.set_xlabel(literal("Sign-oriented Spearman rho"))
        ax.set_title(literal("Oriented correlation with judged behaviour (n=7 lineages; "
                             "bars 95% bootstrap, shading jackknife range)"))
        ax.grid(axis="x", visible=True)
        ax.grid(axis="y", visible=False)
        place_legend(ax, loc="best")
        fit_legends(fig)
        clear_legends_of_data(fig)
        fit_tick_labels(fig)
        fit_titles(fig)
        clear_legends_of_data(fig)
        assert_text_is_legible(fig)
        assert_axis_names_are_unique(fig)
        FIGS.mkdir(exist_ok=True)
        fig.savefig(FIGS / "f1_oriented_forest.pdf")
        fig.savefig(FIGS / "f1_oriented_forest.png", dpi=200)
        plt.close(fig)
    logger.info("f1_oriented_forest: written")


def fig2() -> None:
    cc = R["sign_orientation"]["ceiling_check"]
    o, c = cc["old_raw_statistic"], cc["corrected_oriented_statistic"]
    spec = {
        "type": "bar",
        "title": "What the comparison could ever have shown: measured vs ideal alpha_50",
        "xlabel": "Statistic used for the metric-vs-baseline comparison",
        "ylabel": "Delta = rho(alpha_50) - rho(our-AMS)",
        "aspect": "16:9",
        "categories": ["Old raw statistic", "Corrected sign-oriented statistic"],
        "series": [
            {"label": "measured alpha_50",
             "values": [o["delta_measured"], c["delta_measured"]]},
            {"label": "hypothetical PERFECT alpha_50",
             "values": [o["delta_if_alpha50_were_PERFECT"],
                        c["delta_if_alpha50_were_PERFECT"]]},
        ],
    }
    run_spec(spec, "f2_ceiling_check")


def fig3() -> None:
    pm = R["asymmetry"]["per_member"]
    members = sorted(pm)
    qs = ["q50", "q75", "q90", "q95"]
    matrix = [[float(np.log10(max(pm[m]["quantile_deltas"][q]["delta"], 1e-6))) for q in qs]
              for m in members]
    spec = {
        "type": "heatmap",
        "title": ("Free-running minus teacher-forced deviation ratio, by quantile "
                  "(all 60 cells positive; log scale)"),
        "xlabel": "Quantile of the per-rollout deviation ratio",
        "ylabel": "Panel member",
        "aspect": "4:3",
        "cbar_label": "log10(free - forced)",
        "row_labels": members,
        "col_labels": ["50th", "75th", "90th", "95th"],
        "matrix": matrix,
    }
    run_spec(spec, "f3_quantile_deltas")


def fig4() -> None:
    tab = R["ams_reproduction"]["table_3x4"]
    rules = ["measured", "measured_harmful_only", "measured_worst_concept", "measured_max"]
    names = ["depth band\n(primary)", "harmful only", "worst concept", "best layer"]
    matrix = [[row[f"{r}_relative_error"] for r in rules] for row in tab]
    rows = [f"{row['checkpoint']} (published {row['published']})" for row in tab]
    spec = {
        "type": "heatmap",
        "title": "AMS reproduction: relative error per checkpoint x calibration rule",
        "xlabel": "Calibration rule",
        "ylabel": "Checkpoint (published Table-I sigma)",
        "aspect": "16:9",
        "cbar_label": "|measured - published| / published",
        "row_labels": rows,
        "col_labels": names,
        "matrix": matrix,
    }
    run_spec(spec, "f4_ams_reproduction")


def fig5() -> None:
    ls = R["layer_sensitivity"]["per_member"]["l1_instruct"]
    rows = ls["rows"]
    x = [r["layer"] for r in rows]
    logi = [r["alpha_50_logistic"] for r in rows]
    npar = [r["alpha_50_nonparametric"] for r in rows]
    nonmono = [r["layer"] for r in rows if r["monotonicity"]["non_monotone"]]
    # a null in a line series is refused, so undefined logistic layers are dropped
    lx = [xx for xx, v in zip(x, logi) if v is not None]
    lv = [v for v in logi if v is not None]
    spec = {
        "type": "line",
        "title": (f"Layer sensitivity of alpha_50, l1_instruct (L={ls['selected_layer']}); "
                  f"dose curve non-monotone at layers {', '.join(str(v) for v in nonmono)}"),
        "xlabel": "Steering layer",
        "ylabel": "alpha_50 (units of NORM_L)",
        "aspect": "16:9",
        "series": [
            {"label": f"logistic ({ls['logistic_fold']:.1f}x; {len(x) - len(lx)}/{len(x)} undefined, "
                      f"{ls['n_layers_logistic_undefined_or_out_of_grid'] - (len(x) - len(lx))} "
                      f"out-of-grid)",
             "x": lx, "values": lv},
            {"label": f"non-parametric ({ls['nonparametric_fold']:.1f}x span)",
             "x": x, "values": npar},
        ],
    }
    run_spec(spec, "f5_layer_sensitivity")


def main():
    FIGS.mkdir(exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5):
        try:
            f()
        except SystemExit:
            raise
        except Exception:
            logger.exception(f"{f.__name__} failed")
            raise


if __name__ == "__main__":
    main()
