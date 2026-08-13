#!/usr/bin/env python3
"""Figures, regenerated FROM the analysis JSON only (never from a running model).

  (a) per-member forest plot of the canonical axis's detection AUROC, with the
      pre-registered [0.40, 0.60] indifference band drawn
  (b) refusal rate versus axis-contrast units, axis A vs axis B
  (c) the joint read-versus-act scatter, coloured by member class
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from loguru import logger

import explib as EX

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen")
GEN = SKILL / "scripts/chart_gen.py"
PY = str(EX.HERE / ".venv/bin/python")

SHORT = {"abliterated": "abl", "behavioral_uncensored": "unc",
         "instruct": "inst", "base": "base"}


def short_name(key: str, n: int = 26) -> str:
    return key if len(key) <= n else key[:n - 1] + "…"


def render(spec: dict, out: str) -> bool:
    EX.FIGS.mkdir(parents=True, exist_ok=True)
    p = EX.FIGS / f"{out}_spec.json"
    p.write_text(json.dumps(spec, indent=1))
    r = subprocess.run([PY, str(GEN), "--spec", str(p), "--out", str(EX.FIGS / out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        logger.error(f"{out}: {r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        return False
    logger.info(f"wrote figures/{out}.pdf + .png")
    return True


# ==========================================================================
def fig_forest(R) -> dict:
    h1 = R["h1_abliterated_arm"]
    # Only members with a DEFINED AUROC can be drawn. An unpowered member has too
    # few spontaneous refusals for the statistic to exist at all, and a NaN would
    # render as a silent gap that reads as zero -- so they are excluded here and
    # the count of exclusions is put in the title rather than left implicit.
    rows = [r for r in h1["per_member"]
            if r["A_auroc"] is not None and np.isfinite(r["A_auroc"])
            and r.get("A_ci95") and all(np.isfinite(x) for x in r["A_ci95"])]
    n_excl = len(h1["per_member"]) - len(rows)
    rows.sort(key=lambda r: (r["member_class"], -r["A_auroc"]))
    return {
        "type": "forest",
        "title": (f"Does the canonical refusal axis READ its own model's refusals? "
                  f"({n_excl} members omitted: too few spontaneous refusals)"),
        "xlabel": "held-out AUROC on the model's own text (chance = 0.50)",
        "ylabel": "checkpoint",
        "width_in": 7.0, "aspect": "4:3",
        "null_line": 0.5,
        "categories": [f"{short_name(r['checkpoint'], 22)} ({SHORT.get(r['member_class'], '?')})"
                       for r in rows],
        "series": [{
            # `errors` is a symmetric half-width by construction in this renderer.
            # The bootstrap interval is a percentile interval and so is slightly
            # asymmetric; the EXACT bounds are in table T2 of RESULTS.md, and the
            # worst asymmetry across the panel is recorded in figures_status.json.
            "values": [r["A_auroc"] for r in rows],
            "errors": [max(0.0, ((r["A_ci95"] or [np.nan, np.nan])[1]
                                 - (r["A_ci95"] or [np.nan, np.nan])[0]) / 2.0)
                       for r in rows],
        }],
    }


def fig_dose() -> dict:
    """Refusal rate vs contrast units, A and B, one panel per member."""
    panels = []
    for p in sorted(EX.RESULTS.glob("induce_*.json")):
        d = EX.load_json(p)
        series = []
        for ax, lab in ((("A_canned"), "A canned"), (("B_paraphrase"), "B paraphrase"),
                        (("D_random0"), "D matched random")):
            rec = d["axes"].get(ax)
            if not rec:
                continue
            cs = rec["c_grid_uncapped"]
            ys = [rec["grid"][str(c)]["rate"] for c in cs]
            if not cs or any(y is None for y in ys):
                continue
            series.append({"label": lab, "x": [float(c) for c in cs],
                           "values": [float(y) for y in ys]})
        if len(series) >= 2:
            panels.append({"type": "line", "title": short_name(d["checkpoint"], 14),
                           "xlabel": "contrast units c", "ylabel": "refusal rate",
                           "ylim": [0.0, 1.02], "series": series})
    panels = panels[:6]
    if not panels:
        return {}
    return {"type": "panel",
            "title": "Refusal rate versus axis-contrast units (matched injection norm)",
            "ncols": 3 if len(panels) >= 3 else len(panels),
            "panels": panels}


def fig_joint(R) -> dict:
    h3 = R["h3_joint_scatter"]
    pts = R.get("joint_scatter_points", [])
    if len(pts) < 4:
        return {}
    by_level: dict[str, list] = {}
    for p in pts:
        by_level.setdefault(p["level"], []).append(p)
    series = []
    for lvl in sorted(by_level):
        sub = by_level[lvl]
        series.append({"label": SHORT.get(lvl, lvl),
                       "x": [float(p["max_refusal_rate"]) for p in sub],
                       "values": [float(p["detection_auroc"]) for p in sub]})
    rho = h3.get("rho_primary")
    lo, hi = h3.get("ci95_lineage_bootstrap", [np.nan, np.nan])
    return {"type": "scatter",
            "title": (f"Reading versus pushing: rho = {rho:.2f} "
                      f"[{lo:.2f}, {hi:.2f}] over {h3['n_pairs']} (member, axis) pairs"),
            "xlabel": "induction quality: max refusal rate over the contrast grid",
            "ylabel": "detection quality: held-out AUROC",
            "width_in": 7.0, "aspect": "4:3",
            "fit": False, "series": series}


def main():
    mo = EX.load_json(EX.HERE / "method_out.json")
    R = mo["metadata"]["results"]
    ok = {}
    ok["fig_a_detection_forest"] = render(fig_forest(R), "fig_a_detection_forest")
    d = fig_dose()
    ok["fig_b_dose_contrast_units"] = render(d, "fig_b_dose_contrast_units") if d else False
    j = fig_joint(R)
    ok["fig_c_joint_read_vs_act"] = render(j, "fig_c_joint_read_vs_act") if j else False
    EX.atomic_write_json(EX.FIGS / "figures_status.json", ok)
    logger.info(f"figures: {sum(ok.values())}/{len(ok)} rendered")


if __name__ == "__main__":
    main()
