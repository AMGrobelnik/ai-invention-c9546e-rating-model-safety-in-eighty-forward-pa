#!/usr/bin/env python3
"""Regenerate every figure from the analysis output only (never hand-typed numbers)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_lib as EL  # noqa: E402

SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py")
PY = str(HERE / ".venv/bin/python")
FIGS = HERE / "figures"
SPECS = FIGS / "specs"

AXIS_LABEL = {"A_canned": "A canned refusal", "B_paraphrase": "B paraphrase (disjoint)",
              "C_stylistic": "C stylistic (norm-matched)", "D_random0": "D random",
              "E_prompt_contrast": "E prompt contrast"}


def render(spec: dict, name: str) -> bool:
    SPECS.mkdir(parents=True, exist_ok=True)
    p = SPECS / f"{name}.json"
    p.write_text(json.dumps(spec, indent=1))
    r = subprocess.run([PY, str(SKILL), "--spec", str(p), "--out", str(FIGS / name)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        logger.error(f"{name}: {r.stdout[-800:]}\n{r.stderr[-800:]}")
        return False
    logger.info(f"wrote figures/{name}.pdf")
    return True


def fig1_forest(a1: dict) -> None:
    cats, vals, errs = [], [], []
    for k, v in a1["per_checkpoint"].items():
        for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0"):
            r = v["axes"].get(ax)
            if not r:
                continue
            c = r["centred"]
            lo, hi = c["auroc_ci95"]
            cats.append(f"{k} · {AXIS_LABEL[ax].split(' ')[0]}")
            vals.append(float(c["auroc"]))
            errs.append(float(max(abs(hi - c["auroc"]), abs(c["auroc"] - lo))))
    render({"type": "forest", "null_line": 0.5,
            "title": "Held-out behavioural AUROC by axis and checkpoint "
                     "(prompt-clustered bootstrap)",
            "xlabel": "AUROC: refusal vs compliance in AB-blind generated text",
            "aspect": "3:4", "width_in": 6.5,
            "categories": cats,
            "series": [{"values": vals, "errors": errs}]}, "fig1_heldout_auroc_forest")


def fig2_contrast_dose(a2: dict) -> None:
    panels = []
    for k, v in a2["per_checkpoint"].items():
        series = []
        for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0",
                   "E_prompt_contrast"):
            r = v["axes"].get(ax)
            if not r:
                continue
            g = r["grid"]
            xs = [g[a]["contrast_units"] for a in sorted(g, key=float)]
            ys = [g[a]["rate"] for a in sorted(g, key=float)]
            series.append({"label": AXIS_LABEL[ax], "x": xs, "values": ys})
        panels.append({"type": "line", "title": k, "xlabel": "axis-contrast units",
                       "ylabel": "refusal rate", "series": series})
    render({"type": "panel", "ncols": 3, "panel_labels": True, "aspect": "16:9",
            "title": "Dose response in AXIS-CONTRAST UNITS "
                     "(c = alpha x NORM_L / axis diff-in-means norm)",
            "panels": panels}, "fig2_contrast_unit_dose")


def fig3_matched(a2: dict) -> None:
    cats, vals, errs = [], [], []
    for k, v in a2["per_checkpoint"].items():
        for other in ("B_paraphrase", "C_stylistic", "D_random0"):
            m = v["matched_contrast"].get(other)
            if not m or not m.get("n_matched_levels"):
                continue
            d = m["mean_paired_diff_A_minus_other"]
            lo, hi = m["ci95"]
            cats.append(f"{k} · A−{other.split('_')[0]}")
            vals.append(float(d))
            errs.append(float(max(abs(hi - d), abs(d - lo))))
    render({"type": "forest", "null_line": 0.0,
            "title": "Refusal-rate difference at MATCHED axis-contrast units",
            "xlabel": "mean paired difference (axis A − other axis)",
            "aspect": "3:4", "width_in": 6.5, "categories": cats,
            "series": [{"values": vals, "errors": errs}]}, "fig3_matched_contrast")


def fig4_judge_overlay(a3: dict) -> None:
    panels = []
    for kk, v in sorted(a3["per_checkpoint_axis"].items()):
        if v["axis"] not in ("A_canned", "B_paraphrase"):
            continue
        g = v["grid"]
        xs = [float(a) for a in sorted(g, key=float)]
        panels.append({
            "type": "line", "title": f"{v['checkpoint']} · {v['axis'].split('_')[0]}",
            "xlabel": "alpha", "ylabel": "refusal rate",
            "series": [
                {"label": "onset regex", "x": xs,
                 "values": [g[a]["rate_regex"] for a in sorted(g, key=float)]},
                {"label": "semantic judge", "x": xs,
                 "values": [g[a]["rate_judge_strict"] for a in sorted(g, key=float)]},
                {"label": "judge incl. PARTIAL", "x": xs,
                 "values": [g[a]["rate_judge_incl_partial"] for a in sorted(g, key=float)]},
            ]})
    render({"type": "panel", "ncols": 4, "panel_labels": True, "aspect": "16:9",
            "width_in": 13,
            "title": "Dose response under the onset regex vs the semantic judge "
                     "(alpha in NORM_L units)",
            "panels": panels}, "fig4_regex_vs_judge")


def fig5_b_classes(a4: dict) -> None:
    labels = ["REFUSAL_CANONICAL", "REFUSAL_NONCANONICAL", "PARTIAL", "COMPLIANCE",
              "DEGENERATE"]
    cats, series = [], {lab: [] for lab in labels}
    for kk, v in sorted(a4["per_checkpoint_axis"].items()):
        if v["axis"] != "B_paraphrase":
            continue
        for a in sorted(v["by_alpha"], key=float):
            cats.append(f"{v['checkpoint']}\n{float(a):.2f}")
            cnt = v["by_alpha"][a]["counts"]
            for lab in labels:
                series[lab].append(float(cnt.get(lab, 0)))
    render({"type": "stacked_pct", "title": "What axis-B steering actually produces at "
                                            "its top three alphas",
            "xlabel": "checkpoint / alpha", "aspect": "16:9", "annotate": False,
            "categories": cats,
            "series": [{"label": lab, "values": series[lab]} for lab in labels]},
           "fig5_b_text_classes")


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    FIGS.mkdir(exist_ok=True)
    a1 = EL.load_json(EL.RESULTS / "analysis1.json")
    a2 = EL.load_json(EL.RESULTS / "analysis2.json")
    fig1_forest(a1)
    fig2_contrast_dose(a2)
    fig3_matched(a2)
    if (EL.RESULTS / "analysis3.json").exists():
        fig4_judge_overlay(EL.load_json(EL.RESULTS / "analysis3.json"))
    if (EL.RESULTS / "analysis4.json").exists():
        fig5_b_classes(EL.load_json(EL.RESULTS / "analysis4.json"))


if __name__ == "__main__":
    main()
