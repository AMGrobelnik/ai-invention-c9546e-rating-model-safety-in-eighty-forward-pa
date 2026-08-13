#!/usr/bin/env python3
"""Render method_out.json as a compact markdown matrix for the write-up."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = ["check1_lexical", "check2_monotonicity", "check3_layer",
          "check4_jackknife", "check5_scorer"]
NAMES = {"check1_lexical": "1 lexical", "check2_monotonicity": "2 monotone",
         "check3_layer": "3 depth", "check4_jackknife": "4 jackknife",
         "check5_scorer": "5 scorer"}


def fmt(x, n=3):
    if x is None:
        return "--"
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, float):
        return f"{x:.{n}f}"
    if isinstance(x, list):
        return "[" + ", ".join(fmt(v, n) for v in x) + "]"
    return str(x)


def main() -> None:
    out = json.loads((HERE / "method_out.json").read_text())
    a = out["metadata"]["analysis"]
    m = a["matrix"]
    lines = ["# Discrimination matrix", "",
             f"**Verdict: {a['verdict']}**", "", a["verdict_line"], ""]
    if a.get("smoke_only"):
        lines += ["> SMOKE_ONLY -- fewer than 19 members completed; the numbers "
                  "below are not results.", ""]

    head = "| score | " + " | ".join(NAMES[c] for c in CHECKS) + \
           " | passed | rho (oriented) | 95% CI (lineage-clustered) | jackknife range | AUC |"
    lines += [head, "|" + "---|" * (len(CHECKS) + 6)]
    for k, row in m.items():
        cells = [row.get(c, {}).get("verdict", "--") for c in CHECKS]
        lines.append(
            f"| `{k}` | " + " | ".join(cells) +
            f" | {row.get('n_checks_passed')}/5 | {fmt(row.get('rho_oriented'))}"
            f" | {fmt(row.get('ci95'))} | {fmt(row.get('jackknife_range'))}"
            f" | {fmt(row.get('auc'))} |")

    lines += ["", "## Per-cell statistics", ""]
    for k, row in m.items():
        lines += [f"### `{k}`", ""]
        for c in CHECKS:
            cell = row.get(c, {})
            lines.append(f"- **{NAMES[c]} = {cell.get('verdict')}** "
                         f"(threshold {fmt(cell.get('threshold'))}): "
                         f"{cell.get('statistic') or cell.get('reason')}")
        lines += ["", f"  evidence: `{row.get(CHECKS[0], {}).get('evidence_pointer')}`",
                  ""]

    st = a["statistics"]
    lines += ["## Score columns against y_refusal", "",
              "| column | orientation | n | rho oriented | rho raw | 95% CI | "
              "exhaustive perm p | floor | AUC | rho / sqrt(0.75) |",
              "|" + "---|" * 10]
    for name, s in st.items():
        p = s.get("permutation", {})
        lines.append(
            f"| `{name}` | {s['orientation']:+d} | {s['n_defined']} | "
            f"{fmt(s['rho_oriented'])} | {fmt(s['rho_raw_unoriented'])} | "
            f"{fmt(s['ci95_lineage_clustered'])} | {fmt(p.get('p_permutation'), 4)} | "
            f"{fmt(p.get('p_min_achievable'), 5)} | "
            f"{fmt(s['auc_y_above_median'].get('auc'))} | "
            f"{fmt(s['rho_disattenuated_reliability_0.75'])} |")

    lines += ["", "## Sensitivity", "",
              "```json", json.dumps(a["discrimination_sensitivity"], indent=1), "```",
              "", "## Orientation sensitivity", "",
              f"any verdict depends on orientation: "
              f"{a['orientation_sensitivity']['any_verdict_depends_on_orientation']}",
              "", "```json",
              json.dumps(a["orientation_sensitivity"][
                  "rows_whose_verdict_depends_on_orientation"], indent=1), "```",
              "", "## Accounting", "", "```json",
              json.dumps(a["accounting"], indent=1), "```"]

    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))
    print(f"\nwrote RESULTS.md ({(HERE / 'RESULTS.md').stat().st_size} bytes)")


if __name__ == "__main__":
    sys.exit(main())
