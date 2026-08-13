#!/usr/bin/env python3
"""Vector figures, rendered from eval_out.json so they cannot disagree with it.

fig1  the within-axis-A scatter beside the pooled 70-pair scatter -- the visual
      statement of the confound
fig2  the control ladder as a forest plot of rho by axis subset, at BOTH units
fig3  the attainability surface as a heatmap of P(AT_CHANCE) over n x true AUROC
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

from common5 import AXIS_SHORT, FIGS, HERE, jdump, setup_logging

SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py")
PY = str(HERE / ".venv/bin/python")


def render(spec: dict, out: Path) -> dict:
    p = FIGS / f"{out.name}_spec.json"
    jdump(p, spec)
    r = subprocess.run([PY, str(SKILL), "--spec", str(p), "--out", str(out)],
                       capture_output=True, text=True)
    ok = (out.with_suffix(".pdf").exists() and out.with_suffix(".png").exists())
    if not ok:
        logger.error(f"{out.name}: {r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    else:
        logger.info(f"{out.name}: pdf + png written")
    return {"figure": out.name, "spec": str(p), "ok": bool(ok),
            "pdf": str(out.with_suffix(".pdf")), "png": str(out.with_suffix(".png")),
            "stderr_tail": r.stderr[-400:] if not ok else ""}


# --------------------------------------------------------------------------
def fig1(doc: dict) -> dict:
    a1 = doc["metadata"]["analysis1"]
    P = a1["primary"]
    pts = doc["metadata"]["analysis1"]["control_ladder"][0]
    members = P["members"]
    # pooled scatter needs all 70 pairs -- read them straight off the frozen tree
    from common5 import R4, jload
    allp = jload(R4 / "method_out.json")["metadata"]["results"][
        "joint_scatter_points"]

    left = {
        "type": "scatter", "fit": True,
        "title": (f"Within axis A, across {P['member']['n_points']} models: "
                  f"rho = {P['member']['rho']:.3f}"),
        "xlabel": "axis-A maximum induced refusal rate",
        "ylabel": "axis-A held-out detection AUROC",
        "series": [{"label": "detection-powered checkpoint",
                    "x": [m["A_max_rate"] for m in members],
                    "values": [m["A_auroc"] for m in members]}],
    }
    by_axis: dict[str, dict] = {}
    for p in allp:
        s = by_axis.setdefault(AXIS_SHORT[p["axis"]], {"x": [], "values": []})
        s["x"].append(p["max_refusal_rate"])
        s["values"].append(p["detection_auroc"])
    right = {
        "type": "scatter", "fit": False,
        "title": (f"Pooled over all 5 axes ({pts['n_pairs']} pairs): "
                  f"rho = {pts['member']['rho']:.3f}"),
        "xlabel": "maximum induced refusal rate",
        "ylabel": "held-out detection AUROC",
        "series": [{"label": f"axis {k}", **v} for k, v in sorted(by_axis.items())],
    }
    spec = {"type": "panel", "ncols": 2, "panel_labels": True, "aspect": "16:9",
            "title": "Within one axis versus pooled across axes",
            "panels": [left, right]}
    return render(spec, FIGS / "fig1_within_axis_vs_pooled")


def fig2(doc: dict) -> dict:
    """Hand-written: the built-in `forest` renderer takes ONE series and
    SYMMETRIC error bars, and these CIs are neither -- a bootstrap percentile
    interval is asymmetric and both aggregation units must appear side by side.
    Drawing it by hand keeps the interval honest; the house style is applied
    through the skill's own helpers."""
    import warnings

    sys.path.insert(0, str(SKILL.parent))
    import matplotlib.pyplot as plt                                   # noqa: E402
    import numpy as np                                                # noqa: E402
    from chart_geometry import assert_text_is_legible                 # noqa: E402
    from chart_style import (PALETTE, apply_house_style,              # noqa: E402
                             assert_axis_names_are_unique,
                             assert_legends_clear_of_data,
                             assert_series_are_distinguishable,
                             clear_legends_of_data, fit_legends,
                             fit_tick_labels, fit_titles, place_legend)

    a1 = doc["metadata"]["analysis1"]
    rows = [("within axis A only (PRIMARY)", a1["primary"])]
    rows += [(b["subset"], b) for b in a1["control_ladder"]]
    labs = [f"{n}\n({r.get('n_pairs', r['member']['n_points'])} points)"
            for n, r in rows]

    apply_house_style()
    with warnings.catch_warnings(record=True):
        fig, ax = plt.subplots(figsize=(7.6, 4.6), layout="constrained")
        y = np.arange(len(rows))[::-1]
        for j, (unit, off, mk) in enumerate((("member", +0.16, "o"),
                                             ("lineage", -0.16, "s"))):
            v = np.array([r[unit]["rho"] for _, r in rows], float)
            lo = np.array([r[unit]["ci95"][0] for _, r in rows], float)
            hi = np.array([r[unit]["ci95"][1] for _, r in rows], float)
            ax.errorbar(v, y + off, xerr=np.vstack([v - lo, hi - v]), fmt=mk,
                        color=PALETTE[j], ecolor=PALETTE[j], elinewidth=1.3,
                        capsize=3, markersize=6, linestyle="none",
                        label=f"{unit} unit")
        ax.axvline(0.0, color="#999999", linestyle="--", linewidth=1)
        ax.set_xlim(-1.55, 1.06)   # room at the top left for the legend
        ax.set_yticks(y, labels=labs)
        ax.set_xlabel("Spearman rho (induction vs detection)")
        ax.set_title("Control ladder: rho by axis subset, both units")
        ax.grid(axis="x", visible=True)
        ax.grid(axis="y", visible=False)
        place_legend(ax, loc="upper left")
        fit_legends(fig)
        clear_legends_of_data(fig)
        fit_tick_labels(fig)
        fit_titles(fig)
        clear_legends_of_data(fig)
        assert_text_is_legible(fig)
        assert_legends_clear_of_data(fig)
        assert_series_are_distinguishable(fig)
        assert_axis_names_are_unique(fig)
        out = FIGS / "fig2_control_ladder_forest"
        fig.savefig(out.with_suffix(".pdf"))
        fig.savefig(out.with_suffix(".png"), dpi=200)
        plt.close(fig)
    logger.info("fig2_control_ladder_forest: pdf + png written (hand-drawn)")
    return {"figure": out.name, "spec": "hand-written matplotlib (asymmetric CI, "
                                        "two aggregation units)", "ok": True,
            "pdf": str(out.with_suffix(".pdf")), "png": str(out.with_suffix(".png")),
            "stderr_tail": ""}


def fig3(doc: dict) -> dict:
    surf = doc["metadata"]["analysis2"]["attainability_simulation"]["surface"]
    ns = [5, 10, 20, 40, 80, 160]
    aurocs = [0.50, 0.55, 0.60, 0.69, 0.75, 0.90, 1.00]
    panels = []
    for k in (1, 4):
        M = []
        for a in aurocs:
            row = []
            for n in ns:
                hit = [c for c in surf if c["n_per_class"] == n
                       and abs(c["true_auroc"] - a) < 1e-9
                       and c["items_per_prompt"] == k]
                row.append(hit[0]["P_AT_CHANCE"] if hit else 0.0)
            M.append(row)
        panels.append({
            "type": "heatmap",
            "title": f"{k} item per prompt" if k == 1 else f"{k} items per prompt",
            "xlabel": "items per class (n)", "ylabel": "true AUROC",
            "cbar_label": "P(AT_CHANCE)",
            "row_labels": [f"{a:.2f}" for a in aurocs],
            "col_labels": [str(n) for n in ns],
            "matrix": M,
        })
    spec = {"type": "panel", "ncols": 2, "panel_labels": True, "aspect": "16:9",
            "title": "Attainability of the AT_CHANCE verdict",
            "panels": panels}
    return render(spec, FIGS / "fig3_attainability_surface")


def main(doc: dict | None = None) -> dict:
    setup_logging("figures")
    if doc is None:
        doc = json.loads((HERE / "eval_out.json").read_text())
    out = [fig1(doc), fig2(doc), fig3(doc)]
    jdump(FIGS / "figures_manifest.json", {"figures": out,
                                           "n_ok": sum(f["ok"] for f in out)})
    logger.info(f"{sum(f['ok'] for f in out)}/{len(out)} figures rendered")
    return {"figures": out}


if __name__ == "__main__":
    sys.exit(0 if all(f["ok"] for f in main()["figures"]) else 1)
