#!/usr/bin/env python3
"""Figures: (1) retention vs axis-contrast units per axis, one panel per
checkpoint; (2) forest plot of NET = B - control floor with paired
prompt-clustered 95% CIs; (3) the three scoring criteria side by side."""

from __future__ import annotations

import json
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
from loguru import logger

import eval_lib2 as L

HERE = Path(__file__).resolve().parent
SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen")
GEN = SKILL / "scripts/chart_gen.py"
FIGS = HERE / "figures"
FIGS.mkdir(exist_ok=True)

AXIS_LABEL = {"A_canned": "A canned-refusal", "B_paraphrase": "B paraphrase",
              "C_stylistic": "C stylistic", "D_random0": "D random"}


def _run(spec: dict, name: str) -> None:
    out = FIGS / name
    p = subprocess.run([sys.executable, str(GEN), "--spec", "-", "--out", str(out)],
                       input=json.dumps(spec), capture_output=True, text=True)
    if p.returncode != 0:
        logger.error(f"{name} REFUSED: {p.stdout}\n{p.stderr}")
        raise SystemExit(f"figure {name} refused")
    logger.info(f"  wrote {out}.pdf/.png")


def fig_retention() -> None:
    curves = L.load_json(L.RESULTS / "retention_curves.json")["curves"]
    panels = []
    for m in L.CHECKPOINTS:
        series = []
        for ax in L.AXES_CORE:
            g = curves[m].get(ax)
            if not g:
                continue
            pts = [c for c in g["grid"] if c["contrast_units"] > 0]
            series.append({"label": AXIS_LABEL[ax],
                           "x": [c["contrast_units"] for c in pts],
                           "values": [c["retention"] for c in pts]})
        panel = {"type": "line", "title": m, "logx": True,
                 "xlabel": "axis-contrast units", "series": series}
        if len(panels) % 3 == 0:          # y-label on the left column only
            panel["ylabel"] = "screen retention"
        panels.append(panel)
    _run({"type": "panel", "ncols": 3, "aspect": "16:9",
          "title": "Fraction of steered generations surviving the frozen "
                   "degeneracy screen",
          "panels": panels}, "fig_retention_vs_contrast")


def fig_rates() -> None:
    r = L.load_json(L.RESULTS / "rates_filtered.json")["rates"]["pooled"]["matched"]
    cats = [AXIS_LABEL[a] for a in L.AXES_CORE if a in r]
    crit = [("regex_anchored", "anchored regex"),
            ("judge4_strict", "judge 4-class REFUSAL"),
            ("judge5_any_refusal", "judge 5-class ANY-REFUSAL"),
            ("judge5_degenerate", "judge 5-class DEGENERATE")]
    series = []
    for key, lab in crit:
        vals, errs = [], []
        for a in L.AXES_CORE:
            if a not in r:
                continue
            b = r[a][key]
            vals.append(b["rate"])
            lo, hi = b["ci95_prompt_clustered"]
            errs.append(max(0.0, (hi - lo) / 2))
        series.append({"label": lab, "values": vals, "errors": errs})
    _run({"type": "bar", "title": "Rates on the screen-passing set at matched "
                                  "contrast units (pooled over 6 checkpoints)",
          "xlabel": "steering axis", "ylabel": "rate",
          "aspect": "16:9", "categories": cats, "series": series},
         "fig_rates_three_criteria")


def fig_forest() -> None:
    """Hand-written: the bootstrap percentile intervals are ASYMMETRIC, which the
    forest renderer's single `errors` magnitude cannot express."""
    sys.path.insert(0, str(SKILL / "scripts"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from chart_geometry import assert_text_is_legible
    from chart_style import (PALETTE, apply_house_style,  # noqa: N811
                             assert_axis_names_are_unique, clear_legends_of_data,
                             fit_legends, fit_tick_labels, fit_titles, literal,
                             place_legend)

    net = L.load_json(L.RESULTS / "net_and_correction.json")["net"]
    rows = []
    for m in L.CHECKPOINTS:
        nb = net["per_member"][m]["matched"]
        rows.append((m, nb["NET_B_minus_floor"],
                     nb["rogan_gladen"]["primary"]["NET_corrected"]))
    nb = net["pooled"]["matched"]
    rows.append(("POOLED", nb["NET_B_minus_floor"],
                 nb["rogan_gladen"]["primary"]["NET_corrected"]))

    apply_house_style()
    with warnings.catch_warnings(record=True):
        fig, ax = plt.subplots(figsize=(7, 4.2), layout="constrained")
        y = np.arange(len(rows))
        for off, (key, lab, col) in enumerate([(1, "raw NET", PALETTE[0]),
                                               (2, "Rogan-Gladen corrected", PALETTE[1])]):
            v = np.array([r[key]["point"] for r in rows])
            lo = np.array([r[key]["ci95"][0] for r in rows])
            hi = np.array([r[key]["ci95"][1] for r in rows])
            ax.errorbar(v, y + (off - 0.5) * 0.22,
                        xerr=np.vstack([np.maximum(0, v - lo), np.maximum(0, hi - v)]),
                        fmt="o", color=col, ecolor="#333333", elinewidth=1.2,
                        capsize=3, markersize=6, label=literal(lab), linestyle="none")
        ax.axvline(0.0, color="#999999", linestyle="--", linewidth=1)
        ax.set_yticks(y, labels=[literal(r[0]) for r in rows])
        ax.invert_yaxis()
        ax.set_xlabel(literal("NET = B minus control floor (95% CI)"))
        ax.set_title(literal("Does the paraphrase axis induce refusal above the "
                             "control floor at matched contrast?"))
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
        fig.savefig(FIGS / "fig_net_forest.pdf")
        fig.savefig(FIGS / "fig_net_forest.png", dpi=200)
        plt.close(fig)
    logger.info(f"  wrote {FIGS / 'fig_net_forest'}.pdf/.png")


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    fig_retention()
    fig_rates()
    fig_forest()


if __name__ == "__main__":
    main()
