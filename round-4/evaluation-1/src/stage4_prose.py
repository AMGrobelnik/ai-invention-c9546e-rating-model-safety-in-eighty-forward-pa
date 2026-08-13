#!/usr/bin/env python3
"""STAGE 4 -- PROSE AUDIT.

Every correlation-, AUROC-, Delta- or CI-bearing numeric claim in the draft's
Contributions and Results sections is extracted, tagged with its aggregation
unit and with a JSON pointer that reproduces it, and given a status. The
repaired replacement text is then generated FROM the json and audited again.
"""

from __future__ import annotations

import re

from loguru import logger

from common import (DRAFT, OUT, SCORE_LABEL, V1, fmt, fmt_p, jdump, jload,
                    setup_logging)

UNIT_PATTERNS = {
    "member": [r"\b19 checkpoints?\b", r"\bper checkpoint\b", r"\bmember level\b",
               r"\b19[- ]member\b", r"\bacross 19\b", r"\bcheckpoint level\b",
               r"\bof 19\b", r"\b19 members?\b", r"\bmember-level\b"],
    "lineage": [r"\blineage level\b", r"\blineage-level\b", r"\b7 lineages\b",
                r"\bn = 7\b", r"\bseven lineages\b", r"\blineage units?\b",
                r"\bover the same 7\b", r"\b7 lineage\b"],
    "item": [r"\bheld-out items?\b", r"\b7,241\b", r"\bper item\b", r"\bitem level\b",
             r"\bmodel-generated items\b", r"\bacross held-out items\b"],
    "prompt": [r"\bper prompt\b", r"\bprompt level\b", r"\bprompt-clustered\b",
               r"\b\d+ prompts\b"],
    "depth_panel_checkpoint": [r"\b6 checkpoints?\b", r"\bsix depth-panel\b",
                               r"\bdepth panel\b", r"\bdepth-panel\b",
                               r"\bof 6\b", r"\b6 of 6\b", r"\bn = 6\b"],
}

# statistic kinds we audit
STAT_PATTERNS = [
    ("correlation", r"\\rho\s*(?:=|\$?\s*)\s*\$?\s*([+-]?\d*\.\d+)"),
    ("correlation", r"Spearman\s+\$?([+-]?\d*\.\d+)\$?"),
    ("correlation", r"rank\s+\$?\\rho\$?\s*=\s*\$?([+-]?\d*\.\d+)"),
    ("AUROC", r"AUROC\s*\$?([+-]?\d*\.\d+)"),
    ("AUC", r"\bAUC\s*(?:is\s*|=\s*|of\s*)?\$?([+-]?\d*\.\d+)"),
    ("Delta", r"\\Delta\s*=\s*\$?\s*([+-]?\d*\.\d+)"),
]
CI_PATTERN = r"\$?\[([+-]?\d*\.\d+),\s*([+-]?\d*\.\d+)\]\$?"
RANGE_PATTERN = r"\$?([+-]?\d*\.\d+)\$?\s*--\s*\$?([+-]?\d*\.\d+)\$?"


# --------------------------------------------------------------------------
def build_value_index(s0, s1, s2, tables) -> dict:
    """value (rounded to 3dp) -> list of {pointer, unit, what}."""
    idx: dict[float, list[dict]] = {}

    def add(v, pointer, unit, what):
        if v is None:
            return
        try:
            k = round(float(v), 3)
        except (TypeError, ValueError):
            return
        idx.setdefault(k, []).append({"pointer": pointer, "unit": unit, "what": what})

    for cfg_id, cfg in s1["table"].items():
        if not cfg["config"]["primary"]:
            continue
        for col, e in cfg["scores"].items():
            for lvl, unit in (("member_level", "member"), ("lineage_level", "lineage")):
                c = e[lvl]
                base = f"eval_out.json:analysis_1_dual_aggregation.table.{cfg_id}.scores.{col}.{lvl}"
                add(c["rho_oriented"], base + ".rho_oriented", unit,
                    f"oriented rho of {SCORE_LABEL.get(col, col)}")
                add(c["rho_raw_unoriented"], base + ".rho_raw_unoriented", unit,
                    f"raw rho of {SCORE_LABEL.get(col, col)}")
                for i, side in enumerate(("low", "high")):
                    if c.get("ci95"):
                        add(c["ci95"][i], base + f".ci95[{i}]", unit, f"CI {side}")
                auc = (c.get("auc_y_above_median") or {}).get("auc")
                add(auc, base + ".auc_y_above_median.auc", unit,
                    f"median-split AUC of {SCORE_LABEL.get(col, col)}")
                perm = c.get("permutation") or {}
                add(perm.get("p"), base + ".permutation.p", unit, "exhaustive permutation p")
                add(perm.get("p_min_achievable"), base + ".permutation.p_min_achievable",
                    unit, "permutation floor")
                jk = c.get("jackknife") or {}
                if jk.get("range"):
                    add(jk["range"][0], base + ".jackknife.range[0]", unit, "jackknife min")
                    add(jk["range"][1], base + ".jackknife.range[1]", unit, "jackknife max")

    for key, d in s1["deltas"].items():
        for lvl, unit in (("member_level", "member"), ("lineage_level", "lineage")):
            c = d[lvl]
            base = f"eval_out.json:analysis_1_dual_aggregation.deltas.{key}.{lvl}"
            add(c.get("delta"), base + ".delta", unit, "oriented Delta")
            add(c.get("rho_score"), base + ".rho_score", unit, "rho of the alpha_50 carrier")
            add(c.get("rho_reference"), base + ".rho_reference", unit, "rho of our-AMS")
            if c.get("ci95"):
                add(c["ci95"][0], base + ".ci95[0]", unit, "Delta CI low")
                add(c["ci95"][1], base + ".ci95[1]", unit, "Delta CI high")
            add((c.get("ceiling") or {}).get("oriented_ceiling_delta"),
                base + ".ceiling.oriented_ceiling_delta", unit, "oriented ceiling Delta")
            add((c.get("abs_rho_difference") or {}).get("point"),
                base + ".abs_rho_difference.point", unit, "|rho| difference")

    # archived E3 matrix (member level) and its statistics
    for row, m in s0["archived_matrix"].items():
        base = f"iter_3/gen_art/gen_art_experiment_1/full_method_out.json:metadata.analysis.matrix.{row}"
        add(m["rho_oriented"], base + ".rho_oriented", "member", f"{row} oriented rho")
        add(m["auc"], base + ".auc", "member", f"{row} AUC")
        if m.get("ci95"):
            add(m["ci95"][0], base + ".ci95[0]", "member", f"{row} CI low")
            add(m["ci95"][1], base + ".ci95[1]", "member", f"{row} CI high")
    for col, s in s0["archived_statistics"].items():
        base = f"iter_3/gen_art/gen_art_experiment_1/full_method_out.json:metadata.analysis.statistics.{col}"
        add(s["rho_oriented"], base + ".rho_oriented", "member", f"{col} oriented rho")
        add((s.get("auc_y_above_median") or {}).get("auc"),
            base + ".auc_y_above_median.auc", "member", f"{col} AUC")
        add(s["permutation"].get("p_permutation"), base + ".permutation.p_permutation",
            "member", f"{col} permutation p")
        add(s["permutation"].get("p_min_achievable"),
            base + ".permutation.p_min_achievable", "member", "permutation floor")
        if s.get("ci95_lineage_clustered"):
            add(s["ci95_lineage_clustered"][0], base + ".ci95_lineage_clustered[0]",
                "member", f"{col} CI low")
            add(s["ci95_lineage_clustered"][1], base + ".ci95_lineage_clustered[1]",
                "member", f"{col} CI high")

    # V1 depth-panel AUROCs (item unit)
    a1 = jload(V1 / "results" / "analysis1.json")
    for k, pc in a1["per_checkpoint"].items():
        for ax, a in pc["axes"].items():
            if not isinstance(a, dict) or "centred" not in a:
                continue
            base = (f"iter_3/gen_art/gen_art_evaluation_1/results/analysis1.json:"
                    f"per_checkpoint.{k}.axes.{ax}.centred")
            add(a["centred"]["auroc"], base + ".auroc", "item",
                f"{ax} held-out AUROC on {k}")
        ab = pc["axes"].get("_paired_A_minus_B")
        if ab:
            base = (f"iter_3/gen_art/gen_art_evaluation_1/results/analysis1.json:"
                    f"per_checkpoint.{k}.axes._paired_A_minus_B")
            add(ab["delta_auroc"], base + ".delta_auroc", "item", f"paired A-B on {k}")
            add(ab["ci95"][0], base + ".ci95[0]", "item", "paired A-B CI low")
            add(ab["ci95"][1], base + ".ci95[1]", "item", "paired A-B CI high")

    # V1's dose summaries (depth-panel checkpoint unit) and headline metrics
    a2 = jload(V1 / "results" / "analysis2.json")
    for k, pc in a2["per_checkpoint"].items():
        for ax, a in pc["axes"].items():
            base = (f"iter_3/gen_art/gen_art_evaluation_1/results/analysis2.json:"
                    f"per_checkpoint.{k}.axes.{ax}")
            for field, what in (("contrast_units_at_alpha50", "contrast units at 50% refusal"),
                                ("max_refusal_rate", "max steered refusal rate"),
                                ("max_contrast_units_reached", "max contrast units reached"),
                                ("alpha_50_nonparametric", "non-parametric alpha_50")):
                add(a.get(field), base + f".{field}", "depth_panel_checkpoint",
                    f"{ax} {what} on {k}")
        mc = pc.get("matched_contrast", {})
        for ax, a in mc.items():
            base = (f"iter_3/gen_art/gen_art_evaluation_1/results/analysis2.json:"
                    f"per_checkpoint.{k}.matched_contrast.{ax}")
            add(a.get("mean_paired_diff_A_minus_other"), base + ".mean_paired_diff_A_minus_other",
                "depth_panel_checkpoint", "matched-contrast paired advantage")
            if a.get("ci95"):
                add(a["ci95"][0], base + ".ci95[0]", "depth_panel_checkpoint", "CI low")
                add(a["ci95"][1], base + ".ci95[1]", "depth_panel_checkpoint", "CI high")
    for name, v in jload(V1 / "eval_out.json")["metrics_agg"].items():
        add(v, f"iter_3/gen_art/gen_art_evaluation_1/eval_out.json:metrics_agg.{name}",
            "depth_panel_checkpoint", name)
    # V2's archived evaluation (lineage unit unless its own name says otherwise)
    v2 = jload(__import__("common").V2 / "full_eval_out.json")
    for name, v in v2["metrics_agg"].items():
        add(v, f"iter_3/gen_art/gen_art_evaluation_2/eval_out.json:metrics_agg.{name}",
            "lineage", name)

    # the threshold surface
    for rule, s in s2["surfaces"].items():
        base = f"eval_out.json:analysis_2_threshold_surface.surfaces.{rule}"
        for req, v in s["by_required"].items():
            add(v["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"],
                base + f".by_required.{req}.fraction_PROTOCOL_DOES_NOT_DISCRIMINATE",
                "grid point", "fraction of the threshold grid")
        add(s["strict_exceed_criterion"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"],
            base + ".strict_exceed_criterion.fraction_PROTOCOL_DOES_NOT_DISCRIMINATE",
            "grid point", "fraction of the threshold grid, strict-exceed criterion")
    return idx


# --------------------------------------------------------------------------
def split_sentences(par: str) -> list[str]:
    parts = re.split(r"(?<=[.;])\s+(?=[A-Z`$*\\(])", par)
    return [p.strip() for p in parts if p.strip()]


def target_sections(text: str, all_sections: bool = False) -> list[tuple[str, str]]:
    """(anchor, paragraph) for the Contributions and Results sections."""
    out, cur_h1, cur_h2 = [], None, None
    for block in text.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):
            cur_h1, cur_h2 = b[2:].strip(), None
            continue
        if b.startswith("## "):
            cur_h2 = b[3:].strip()
            continue
        if all_sections or cur_h1 in ("Results",) or cur_h2 == "Summary of Contributions":
            anchor = f"{cur_h1 or '?'} / {cur_h2 or '(lead)'}"
            out.append((anchor, b))
    return out


def audit_text(text: str, index: dict, source_label: str,
               all_sections: bool = False) -> dict:
    claims = []
    for anchor, par in target_sections(text, all_sections=all_sections):
        for sent in split_sentences(par):
            found: list[tuple[str, str]] = []
            for kind, pat in STAT_PATTERNS:
                for m in re.finditer(pat, sent):
                    found.append((kind, m.group(1)))
            # a CI or an en-dash range only counts when the sentence already
            # carries one of the audited statistics
            if found:
                for m in re.finditer(CI_PATTERN, sent):
                    tail = sent[m.end():m.end() + 40].lower()
                    if "indifference band" in tail or "margin" in tail:
                        continue  # a pre-registered decision band, not an estimate
                    found.append(("CI", m.group(1)))
                    found.append(("CI", m.group(2)))
                for m in re.finditer(RANGE_PATTERN, sent):
                    found.append(("range", m.group(1)))
                    found.append(("range", m.group(2)))
            if not found:
                continue
            units = [u for u, pats in UNIT_PATTERNS.items()
                     if any(re.search(p, sent, flags=re.I) for p in pats)]
            for kind, raw in found:
                v = float(raw)
                hits = index.get(round(v, 3), [])
                if hits:
                    status = ("TRACEABLE_UNIT_STATED" if units
                              else "TRACEABLE_UNIT_MISSING")
                    ptr = hits[0]["pointer"]
                    ptr_unit = hits[0]["unit"]
                    what = hits[0]["what"]
                else:
                    near = [k for k in index
                            if abs(k - round(v, 3)) <= 0.002 and k != round(v, 3)]
                    status = "VALUE_MISMATCH" if near else "UNTRACEABLE"
                    ptr = (index[near[0]][0]["pointer"] if near else None)
                    ptr_unit = (index[near[0]][0]["unit"] if near else None)
                    what = (index[near[0]][0]["what"] if near else None)
                claims.append({
                    "source": source_label, "anchor": anchor,
                    "sentence": sent[:600], "statistic_kind": kind, "value": v,
                    "unit_tag": (units[0] if len(units) == 1 else
                                 ("MULTIPLE:" + "+".join(units) if units
                                  else "UNSPECIFIED")),
                    "json_pointer": ptr, "pointer_unit": ptr_unit,
                    "pointer_describes": what, "status": status,
                })
    counts: dict[str, int] = {}
    for c in claims:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    flagged = [c for c in claims
               if c["status"] in ("TRACEABLE_UNIT_MISSING", "VALUE_MISMATCH",
                                  "UNTRACEABLE")]
    return {"source": source_label, "n_claims_audited": len(claims),
            "counts_by_status": counts, "claims": claims,
            "flagged": flagged, "n_flagged": len(flagged),
            "flag_list_empty": len(flagged) == 0}


# --------------------------------------------------------------------------
def number_dumps(text: str) -> list[dict]:
    """The three prose paragraphs with the highest raw number count, each mapped
    to the table that should replace it."""
    rows = []
    for anchor, par in target_sections(text):
        nums = re.findall(r"[+-]?\d+\.\d+", par)
        rows.append({"anchor": anchor, "n_numbers": len(nums),
                     "first_words": " ".join(par.split()[:14]) + " ..."})
    rows.sort(key=lambda r: -r["n_numbers"])
    mapping = [
        ("battery", "table1_discrimination_matrix"),
        ("axis", "table2_dissociation_per_checkpoint"),
        ("oriented", "table3_dual_aggregation"),
    ]
    top = rows[:3]
    for i, r in enumerate(top):
        low = (r["anchor"] + " " + r["first_words"]).lower()
        r["replaced_by_table"] = next(
            (t for k, t in mapping if k in low),
            ["table1_discrimination_matrix", "table3_dual_aggregation",
             "table2_dissociation_per_checkpoint"][i])
        r["recommendation"] = "MOVE_TO_SUPPLEMENTARY_AND_CITE_THE_TABLE"
    return top


# --------------------------------------------------------------------------
def replacement_text(s1, s2, s0) -> str:
    """Paste-ready prose generated FROM the json, with the unit named inline."""
    d_v2 = s1["deltas"]["reliable14_rank_bottom_yV2::alpha_50_nonparametric_minus_ams_sigma"]
    d_e3 = s1["deltas"]["all19_drop_undefined_yE3::max_refusal_rate_minus_ams_sigma"]
    h = s1["headline_discrepancy"]
    ams_m = s1["table"]["all19_drop_undefined_yE3"]["scores"]["ams_sigma"]["member_level"]
    ams_l = s1["table"]["reliable14_rank_bottom_yV2"]["scores"]["ams_sigma"]["lineage_level"]
    full = s2["surfaces"]["FULL_PREREGISTERED"]
    thr = s2["surfaces"]["THRESHOLD_ONLY"]
    L = []
    L.append("# Replacement text (generated from eval_out.json; do not retype)\n")
    L.append("## §5.2 / §5.3 -- the aggregation unit, stated inline\n")
    L.append(
        f"At the **member level** -- 19 checkpoints, one row per checkpoint, "
        f"resampled and permuted on the lineage label -- our AMS reimplementation's "
        f"oriented Spearman correlation with the judged plain-harmful refusal rate "
        f"is $\\rho = {fmt(ams_m['rho_oriented'])}$ ${fmt(ams_m['ci95'])}$, with "
        f"exhaustive permutation $p = {fmt_p(ams_m['permutation']['p'])}$ against an "
        f"achievable floor of {fmt_p(ams_m['permutation']['p_min_achievable'])}. "
        f"At the **lineage level** -- 7 lineage units, each the arithmetic mean over "
        f"that lineage's defined members of both the score and the outcome, so "
        f"n = 7 lineages -- the same statistic is "
        f"$\\rho = {fmt(ams_l['rho_oriented'])}$. "
        f"These are one statistic at two aggregation units, not two results: the "
        f"gap of {fmt(h['gap_in_rho'])} is what lineage aggregation buys by "
        f"removing the within-lineage variance and reducing n from 19 to 7, and "
        f"every correlation in this paper is now reported with its unit named.\n")
    L.append("## §5.3 -- the oriented Delta, at both units\n")
    L.append(
        f"Recomputed on sign-oriented correlations over the 7 lineages, the paired "
        f"statistic at the **lineage level** is "
        f"$\\Delta = {fmt(d_v2['lineage_level']['delta'])}$ "
        f"${fmt(d_v2['lineage_level']['ci95'])}$. "
        f"At the **member level**, over the same 14 analysable checkpoints with the "
        f"bootstrap clustered on the lineage, it is "
        f"$\\Delta = {fmt(d_v2['member_level']['delta'])}$ "
        f"${fmt(d_v2['member_level']['ci95'])}$. "
        f"The verdict strings the analysis emits are "
        f"`{d_v2['sign_survives_unit_choice']}` and "
        f"`{d_v2['ci_exclusion_survives_unit_choice']}`: the sign of the loss is "
        f"robust to the aggregation unit, but the interval's exclusion of zero -- "
        f"which is what the previous draft led with -- is not, and holds only at "
        f"the lineage level. "
        f"Under the alternative $\\alpha_{{50}}$ carrier used by the discrimination "
        f"matrix, the maximum refusal rate over all 19 checkpoints, the same "
        f"comparison gives $\\Delta = {fmt(d_e3['member_level']['delta'])}$ at the "
        f"member level. "
        f"Aggregated to 7 lineages it gives "
        f"$\\Delta = {fmt(d_e3['lineage_level']['delta'])}$ at the lineage level, "
        f"so on that carrier the verdict strings are "
        f"`{d_e3['sign_survives_unit_choice']}` and "
        f"`{d_e3['ci_exclusion_survives_unit_choice']}`. "
        f"The ceiling is reported beside the observed value: over the same 7 "
        f"lineages an ideal $\\alpha_{{50}}$ would have scored "
        f"$\\Delta = {fmt(d_v2['lineage_level']['ceiling']['oriented_ceiling_delta'])}$ "
        f"at the lineage level.\n")
    L.append("## §5.2 -- the negative result, as a function of the thresholds\n")
    L.append(
        f"The verdict `PROTOCOL_DOES_NOT_DISCRIMINATE` is not an artefact of the "
        f"five chosen cutoffs. Over a {s2['n_grid_points']:,}-point full factorial "
        f"in the five thresholds (unit: grid point), the pre-registered rule "
        f"returns `PROTOCOL_DOES_NOT_DISCRIMINATE` on a fraction "
        f"{fmt(full['by_required']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE'], 4)} "
        f"of grid points, and under the stricter criterion that a rival must "
        f"*strictly exceed* $\\alpha_{{50}}$'s pass count on "
        f"{fmt(full['strict_exceed_criterion']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE'], 4)}. "
        f"The single-axis exception is check 3: lowering the depth-span threshold "
        f"from 2.0 to 1.75 makes our-AMS pass 2 checks against $\\alpha_{{50}}$'s 1, "
        f"the only single-threshold change anywhere on the grid that produces a "
        f"strict rival win. Dropping the pass rules' secondary clauses and scoring "
        f"the numeric thresholds alone -- a deliberately generous relaxation -- "
        f"lowers the stability to "
        f"{fmt(thr['by_required']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE'], 4)} "
        f"and {fmt(thr['strict_exceed_criterion']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE'], 4)} "
        f"respectively, which locates the negative result precisely: it is carried "
        f"by the pass rules' verdict-class and interiority clauses, not by the "
        f"numeric cutoffs. Check 5 cannot contribute at all: its statistic, a "
        f"REFUSAL $\\kappa$ of 0.391, lies below the entire swept range "
        f"$[0.40, 0.80]$, so it fails identically in all four rows at every grid "
        f"point and shifts all four pass counts together -- an invariance that is "
        f"proved structurally and verified empirically over the whole $\\kappa$ "
        f"axis.\n")
    L.append("## §3 -- the outcome variable itself\n")
    yd = s0["panel_assertions"]["y_outcome_disagreement"]
    L.append(
        f"One accounting item this re-analysis discovered rather than inherited: "
        f"the judged plain-harmful refusal rate is not identical across the two "
        f"frozen archives. It agrees on {yd['n_members_agreeing']} of the 19 "
        f"checkpoints and differs on {yd['n_members_disagreeing']}, all of them "
        f"base members that the iteration-2 archive records with an identical "
        f"12/80 = 0.15 and that the later evaluation re-derives from a larger "
        f"judged pool. All three are among the five auto-flagged `UNRELIABLE` "
        f"members excluded from every correlation, so no reported correlation "
        f"moves; the discrepancy is stated because a reader reconciling the two "
        f"artifacts would otherwise find it themselves.\n")
    return "\n".join(L)


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage4")
    logger.info("STAGE 4 -- prose audit")
    s0 = jload(OUT / "stage0.json")
    s1 = jload(OUT / "stage1_dual_aggregation.json")
    s2 = jload(OUT / "stage2_threshold_surface.json")
    s3 = jload(OUT / "stage3_tables.json")
    index = build_value_index(s0, s1, s2, s3)
    logger.info(f"value index: {len(index)} distinct values")

    draft = DRAFT.read_text()
    before = audit_text(draft, index, "iter_3 paper_body.md")
    logger.info(f"draft: {before['n_claims_audited']} claims, "
                f"{before['counts_by_status']}")

    rep = replacement_text(s1, s2, s0)
    (OUT / "replacement_text.md").write_text(rep)
    after = audit_text(rep, index, "out/replacement_text.md", all_sections=True)
    logger.info(f"replacement: {after['n_claims_audited']} claims, "
                f"{after['counts_by_status']}")

    out = {
        "stage": "stage4_prose_audit",
        "audit_of_draft": before,
        "audit_of_replacement_text": after,
        "assertion": {
            "claim": "the REPAIRED replacement text has an empty flag list",
            "holds": after["flag_list_empty"],
            "residual_flags": after["flagged"],
            "policy": ("a non-empty residual list is shipped rather than raised; "
                       "an untraceable claim is recommended for deletion from the "
                       "main text, not silently kept"),
        },
        "recommended_deletions": [
            {"sentence": c["sentence"], "value": c["value"], "anchor": c["anchor"],
             "reason": "no archived json pointer reproduces this number"}
            for c in before["flagged"] if c["status"] == "UNTRACEABLE"][:20],
        "number_dumps_for_supplementary": number_dumps(draft),
        "replacement_text_path": str(OUT / "replacement_text.md"),
    }
    jdump(out, OUT / "stage4_prose_audit.json")
    logger.info(f"wrote {OUT / 'stage4_prose_audit.json'}")
    return out


if __name__ == "__main__":
    main()
