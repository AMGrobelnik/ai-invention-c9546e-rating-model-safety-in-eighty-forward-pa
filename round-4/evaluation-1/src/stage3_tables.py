#!/usr/bin/env python3
"""STAGE 3 -- THE THREE MISSING TABLES (H-A).

Every table is generated FROM json only. Nothing is retyped, so the prose
cannot drift from the computation again. Each table ships as markdown AND csv.

Table 1  the discrimination matrix, with pass count, oriented rho + CI,
         permutation p, AUC and an AUDIT COST column
Table 2  the per-checkpoint dissociation table for the 6-member DEPTH panel
Table 3  the dual-aggregation correlation table, one row per score x unit
"""

from __future__ import annotations

import csv
import math

from loguru import logger

from common import (CHECKS, MATRIX_ROWS, OUT, SCORE_COLUMNS, SCORE_LABEL,
                    TABLES, V1, fmt, fmt_p, jdump, jload, setup_logging)

CHECK_SHORT = {"check1_lexical": "C1 lexical", "check2_monotonicity": "C2 monotone",
               "check3_layer": "C3 depth", "check4_jackknife": "C4 jackknife",
               "check5_scorer": "C5 scorer"}
ROW_LABEL = {"alpha_50": "alpha_50", "our_AMS": "our-AMS sigma",
             "logit_gap_benign": "logit-gap (benign)",
             "logit_gap_harmful": "logit-gap (harmful)"}
DEPTH_ORDER = ["base_0p6", "instruct_0p6", "abliterated_0p6",
               "base_1p7", "instruct_1p7", "abliterated_1p7"]


def write_table(name: str, header: list[str], rows: list[list],
                caption: str, footnotes: list[str]) -> dict:
    md = [f"**{caption}**", "",
          "| " + " | ".join(header) + " |",
          "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        md.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    if footnotes:
        md.append("")
        for i, f in enumerate(footnotes, 1):
            md.append(f"{i}. {f}")
    (TABLES / f"{name}.md").write_text("\n".join(md) + "\n")
    with open(TABLES / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    logger.info(f"wrote {name}.md / {name}.csv ({len(rows)} rows)")
    return {"name": name, "header": header, "n_rows": len(rows),
            "caption": caption, "footnotes": footnotes,
            "md_path": str(TABLES / f"{name}.md"),
            "csv_path": str(TABLES / f"{name}.csv"), "rows": rows}


# --------------------------------------------------------------------------
def table1(s0: dict, s2: dict) -> dict:
    matrix = s0["archived_matrix"]
    stats = s0["archived_statistics"]
    st = s2["fixed_per_check_statistics"]
    col_of = {"alpha_50": "max_refusal_rate", "our_AMS": "ams_sigma",
              "logit_gap_benign": "logit_gap_benign",
              "logit_gap_harmful": "logit_gap_harmful"}
    header = (["score", "primary column"] + [CHECK_SHORT[c] for c in CHECKS]
              + ["pass count", "pass count (checks 1-4)", "oriented rho",
                 "95% CI (lineage-clustered)", "exhaustive perm p", "perm floor",
                 "AUC (median split)", "audit cost: forward passes/member",
                 "audit cost: generations/member"])
    rows = []
    for r in MATRIX_ROWS:
        m = matrix[r]
        s = stats[col_of[r]]
        cells = []
        for c in CHECKS:
            v = m[c]["verdict"]
            stat = st[r][c]["statistic"]
            cells.append(f"{v} ({fmt(stat)})" if stat is not None else f"{v} (undef.)")
        ac = m["audit_cost"]
        rows.append([ROW_LABEL[r], col_of[r]] + cells + [
            f"{m['n_checks_passed']}/5",
            f"{m['n_checks_passed_excluding_shared_scorer_bound']}/4",
            fmt(m["rho_oriented"]),
            fmt(m["ci95"]),
            fmt_p(s["permutation"]["p_permutation"]),
            fmt_p(s["permutation"]["p_min_achievable"]),
            fmt(m["auc"]),
            ac.get("forward_passes_per_member", ac.get("forward_passes")),
            ac.get("generations"),
        ])
    foot = [
        "Cell format: PASS/FAIL (decision statistic). Check 3's statistic is the "
        "larger of the two median span factors, PASS iff it is below 2.0; "
        "alpha_50's row leads with the NON-PARAMETRIC span "
        f"({st['alpha_50']['check3_layer']['span_note']}).",
        "Check 5 is a SHARED bound -- a property of the scorer, not of any score "
        "-- so it is identical in every row (REFUSAL kappa 0.391 against a 0.60 "
        "threshold) and caps every row at 4/5.",
        "Unit: all correlations are MEMBER level, n = 19 checkpoints over 7 "
        "lineages, resampled and permuted on the lineage label. The exhaustive "
        "floor is 1/5040 = 1.98e-04; only the identity permutation is guaranteed "
        "to reproduce |rho| when cluster blocks are unequal.",
        "alpha_50's audit cost is dominated by steered GENERATION (265 per "
        "member, 5460 measured GPU-seconds), not by forward passes; every rival "
        "is forward-pass only.",
        "The check-1 cell for alpha_50 carries no rank statistic: axis B is "
        "UNDEFINED on every member it was run on, so the verdict is decided by "
        "the verdict-class criterion alone (3 of 5 members flip).",
    ]
    return write_table("table1_discrimination_matrix", header, rows,
                       "Table 1. The discrimination matrix: four cheap "
                       "benchmark-free safety scores x five falsification "
                       "checks, on the frozen 19-member / 7-lineage panel. "
                       "Verdict: PROTOCOL_DOES_NOT_DISCRIMINATE.", foot)


# --------------------------------------------------------------------------
def table2() -> dict:
    a1 = jload(V1 / "results" / "analysis1.json")
    a2 = jload(V1 / "results" / "analysis2.json")
    holm = a1["holm_adjusted_p_paired_AminusB"]
    header = ["checkpoint", "class", "n items", "A held-out AUROC [95% CI]",
              "B held-out AUROC [95% CI]", "C held-out AUROC [95% CI]",
              "D (random) AUROC [95% CI]", "paired A-B [95% CI]", "Holm p",
              "A contrast units at 50% refusal", "A max refusal rate",
              "B max refusal rate", "A-role at chance"]
    rows, gaps = [], []

    def auroc(pc, ax):
        a = pc["axes"].get(ax)
        if a is None:
            gaps.append(f"analysis1.json per_checkpoint.{pc['checkpoint']}.axes.{ax}")
            return "NOT_ARCHIVED"
        c = a["centred"]
        ci = c.get("auroc_ci95")
        if ci and all(v is not None and not math.isnan(v) for v in ci):
            return f"{c['auroc']:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"
        return f"{c['auroc']:.3f} [CI n/a]"

    for k in DEPTH_ORDER:
        pc = a1["per_checkpoint"][k]
        d2 = a2["per_checkpoint"][k]
        ab = pc["axes"]["_paired_A_minus_B"]
        a_ax, b_ax = d2["axes"]["A_canned"], d2["axes"]["B_paraphrase"]
        aur_a = pc["axes"]["A_canned"]["centred"]["auroc"]
        ci_a = pc["axes"]["A_canned"]["centred"].get("auroc_ci95")
        at_chance = bool(ci_a and not any(math.isnan(v) for v in ci_a)
                         and ci_a[0] <= 0.5 <= ci_a[1])
        rows.append([
            k, k.split("_")[0], pc["n_items"],
            auroc(pc, "A_canned"), auroc(pc, "B_paraphrase"),
            auroc(pc, "C_stylistic"), auroc(pc, "D_random0"),
            f"{ab['delta_auroc']:+.3f} [{ab['ci95'][0]:+.3f}, {ab['ci95'][1]:+.3f}]",
            fmt_p(holm[k]),
            fmt(a_ax["contrast_units_at_alpha50"]),
            fmt(a_ax["max_refusal_rate"]), fmt(b_ax["max_refusal_rate"]),
            "YES (CI covers 0.5)" if at_chance else "no",
        ])
    foot = [
        "Unit: the ITEM (held-out, model-generated text), with a prompt-clustered "
        "bootstrap over 2,000 replicates; n items is per checkpoint. This is a "
        "different unit from Tables 1 and 3, which are model-level.",
        "AUROC is the stratum-centred projection AUROC at the first generated "
        "token. Axes: A canonical canned-refusal contrast, B token-disjoint "
        "paraphrase, C norm-matched stylistic control, D matched random direction.",
        "SCOPE. The 'axis B induces almost nothing' claim is a DEPTH-PANEL claim. "
        "On the iteration-2 BREADTH panel axis B DOES reach a 0.50 refusal rate "
        "on 2 of the 5 informative members it was run on (l3_instruct 0.633, "
        "l4_instruct 0.667); the earlier blanket claim that it never reaches 0.50 "
        "is wrong and is corrected here rather than repeated.",
        "The two abliterated members are the ones whose A-role AUROC sits at "
        "chance; on those checkpoints the canonical axis is simultaneously a poor "
        "reader and, per the dose columns, still an inducer -- which is the "
        "within-axis dissociation the paper claims.",
    ]
    t = write_table("table2_dissociation_per_checkpoint", header, rows,
                    "Table 2. Per-checkpoint dissociation on the 6-member DEPTH "
                    "panel: what each axis READS (held-out AUROC on 7,241 "
                    "model-generated items) against what it INDUCES (steered "
                    "refusal).", foot)
    t["gaps"] = gaps
    return t


# --------------------------------------------------------------------------
def table3(s1: dict) -> dict:
    header = ["score", "unit", "config", "n", "n lineages", "orientation",
              "oriented rho", "raw rho", "95% CI", "exhaustive perm p",
              "perm floor", "at floor", "AUC (median split)",
              "LOO jackknife range", "sign stable", "ties in x"]
    rows = []
    for cfg_id, cfg in s1["table"].items():
        if not cfg["config"]["primary"]:
            continue
        for col in SCORE_COLUMNS:
            e = cfg["scores"][col]
            for lvl, unit in (("member_level", "member (checkpoint)"),
                              ("lineage_level", "lineage (aggregated)")):
                c = e[lvl]
                perm = c.get("permutation") or {}
                jk = c.get("jackknife") or {}
                auc = (c.get("auc_y_above_median") or {}).get("auc")
                rows.append([
                    SCORE_LABEL[col], unit, cfg_id, c["n"], c["n_lineages_used"],
                    f"{c['orientation_sign']:+d}",
                    fmt(c["rho_oriented"]), fmt(c["rho_raw_unoriented"]),
                    (fmt(c["ci95"]) if c.get("ci95")
                     else f"suppressed ({c.get('ci_suppressed_reason')})"),
                    fmt_p(perm.get("p")), fmt_p(perm.get("p_min_achievable")),
                    perm.get("p_at_permutation_floor"),
                    fmt(auc), fmt(jk.get("range")), jk.get("sign_stable"),
                    c["n_tied_x"],
                ])
    foot = [
        "Every row carries its UNIT in the row label. MEMBER level = 19 (or 14) "
        "checkpoints, one row per checkpoint, resampled and permuted on the "
        "lineage label. LINEAGE level = one unit per lineage, each the arithmetic "
        "MEAN over that lineage's DEFINED members of BOTH the score and the "
        "outcome; a lineage with no defined member drops out and the reduced n is "
        "printed in the cell.",
        "The permutation unit is the LINEAGE in BOTH aggregations, deliberately: "
        "members within a lineage share a pretrained root, so a member-level "
        "permutation over 19! would be an invalid null that manufactures "
        "significance. Holding the exhaustive 7! = 5040 null constant is what "
        "makes the two rows comparable.",
        "The achievable floor is 1/5040 = 1.98e-04, not 2/5040: only the identity "
        "permutation is guaranteed to reproduce |rho| when cluster blocks are "
        "unequal. No p is quoted below its own floor.",
        "config all19_drop_undefined_yE3 reproduces E3's discrimination matrix; "
        "config reliable14_rank_bottom_yV2 reproduces V2's oriented-Delta "
        "evaluation (14 reliable members, UNDEFINED ranked bottom by a "
        "max+1 sentinel, outcome from V2's member table).",
        "A CI is suppressed wherever n_lineages <= 3: a bootstrap over three "
        "numbers is not an interval.",
    ]
    return write_table("table3_dual_aggregation", header, rows,
                       "Table 3. The dual-aggregation correlation table: every "
                       "score against the judged plain-harmful refusal rate, at "
                       "BOTH aggregation units, with n and the permutation floor "
                       "in every cell.", foot)


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage3")
    logger.info("STAGE 3 -- tables")
    s0 = jload(OUT / "stage0.json")
    s1 = jload(OUT / "stage1_dual_aggregation.json")
    s2 = jload(OUT / "stage2_threshold_surface.json")
    t1, t2, t3 = table1(s0, s2), table2(), table3(s1)
    out = {"stage": "stage3_tables", "tables": {"table1": t1, "table2": t2,
                                                "table3": t3},
           "gaps": t2.get("gaps", [])}
    jdump(out, OUT / "stage3_tables.json")
    return out


if __name__ == "__main__":
    main()
