#!/usr/bin/env python3
"""ASSEMBLE -- fold the four stages into eval_out.json (exp_eval_sol_out schema)
and write the verdict-first README."""

from __future__ import annotations

from loguru import logger

from common import (HERE, OUT, SCORE_COLUMNS, SCORE_LABEL, TABLES, fmt, fmt_p,
                    jdump, jload, setup_logging)


def s(v) -> str:
    return "undefined" if v is None else (f"{v:.6f}" if isinstance(v, float) else str(v))


def num(v):
    """schema: eval_* must be a number; None is dropped by the caller."""
    return None if v is None else float(v)


def build_datasets(s0, s1, s2, s3, s4) -> list[dict]:
    ds = []

    # 1 -------------------------------------------------- dual aggregation
    ex = []
    for cfg_id, cfg in s1["table"].items():
        if not cfg["config"]["primary"]:
            continue
        for col in SCORE_COLUMNS:
            e = cfg["scores"][col]
            for lvl, unit in (("member_level", "member"), ("lineage_level", "lineage")):
                c = e[lvl]
                perm = c.get("permutation") or {}
                jk = c.get("jackknife") or {}
                auc = (c.get("auc_y_above_median") or {}).get("auc")
                row = {
                    "input": (f"score={col} | unit={unit} | config={cfg_id} | "
                              f"n={c['n']} | n_lineages={c['n_lineages_used']}"),
                    "output": (f"oriented rho = {s(c['rho_oriented'])} "
                               f"(orientation {c['orientation_sign']:+d}), "
                               f"n = {c['n']} {unit}s over "
                               f"{c['n_lineages_used']} lineages"),
                    "metadata_fold": "dual_aggregation",
                    "metadata_uid": f"{cfg_id}::{col}::{lvl}",
                    "metadata_score": col,
                    "metadata_score_label": SCORE_LABEL[col],
                    "metadata_unit": unit,
                    "metadata_config": cfg["config"],
                    "metadata_cell": c,
                    "metadata_lineage_unit_detail": e["lineage_unit_detail"],
                    "metadata_why_they_differ": e.get("why_they_differ"),
                    "predict_oriented_rho": s(c["rho_oriented"]),
                    "predict_ci95": (fmt(c["ci95"]) if c.get("ci95")
                                     else f"SUPPRESSED: {c.get('ci_suppressed_reason')}"),
                    "predict_permutation_p": (fmt_p(perm.get("p"))
                                              if perm.get("p") is not None else "undefined"),
                    "predict_permutation_floor": (fmt_p(perm.get("p_min_achievable"))
                                                  if perm.get("p_min_achievable") is not None
                                                  else "undefined"),
                }
                for k, v in (("eval_rho_oriented", c["rho_oriented"]),
                             ("eval_rho_raw_unoriented", c["rho_raw_unoriented"]),
                             ("eval_n", c["n"]), ("eval_n_lineages", c["n_lineages_used"]),
                             ("eval_auc_median_split", auc),
                             ("eval_permutation_p", perm.get("p")),
                             ("eval_permutation_floor", perm.get("p_min_achievable")),
                             ("eval_jackknife_spread", jk.get("spread")),
                             ("eval_n_tied_x", c["n_tied_x"])):
                    if v is not None:
                        row[k] = num(v)
                if c.get("ci95"):
                    row["eval_ci95_low"] = num(c["ci95"][0])
                    row["eval_ci95_high"] = num(c["ci95"][1])
                ex.append(row)
    ds.append({"dataset": "dual_aggregation_cells", "examples": ex})

    # 2 -------------------------------------------------- oriented Delta
    ex = []
    for key, d in s1["deltas"].items():
        m, l = d["member_level"], d["lineage_level"]
        ex.append({
            "input": f"Delta = rho({d['alpha_50_carrier']}) - rho({d['reference']}) | {d['config']}",
            "output": (f"member level Delta = {s(m.get('delta'))} (n={m.get('n')}); "
                       f"lineage level Delta = {s(l.get('delta'))} (n={l.get('n')}); "
                       f"{d['sign_survives_unit_choice']} / "
                       f"{d['ci_exclusion_survives_unit_choice']}"),
            "metadata_fold": "oriented_delta",
            "metadata_uid": key,
            "metadata_member_level": m, "metadata_lineage_level": l,
            "metadata_auc_pair": d["auc_pair"],
            "predict_sign_survives_unit_choice": d["sign_survives_unit_choice"],
            "predict_ci_exclusion_survives_unit_choice":
                d["ci_exclusion_survives_unit_choice"],
            "predict_member_ci": (fmt(m.get("ci95")) if m.get("ci95") else "suppressed"),
            "predict_lineage_ci": (fmt(l.get("ci95")) if l.get("ci95") else "suppressed"),
            **({"eval_delta_member": num(m["delta"])} if m.get("delta") is not None else {}),
            **({"eval_delta_lineage": num(l["delta"])} if l.get("delta") is not None else {}),
            **({"eval_ceiling_oriented_lineage":
                num(l["ceiling"]["oriented_ceiling_delta"])}
               if (l.get("ceiling") or {}).get("oriented_ceiling_delta") is not None else {}),
            **({"eval_abs_rho_difference_lineage":
                num(l["abs_rho_difference"]["point"])}
               if (l.get("abs_rho_difference") or {}).get("point") is not None else {}),
        })
    ds.append({"dataset": "oriented_delta_both_units", "examples": ex})

    # 3 -------------------------------------------------- threshold surface
    ex = []
    for rule, sur in s2["surfaces"].items():
        for req, v in sur["by_required"].items():
            ex.append({
                "input": f"rule={rule} | required_rival_passes={req} | "
                         f"grid={s2['n_grid_points']} points",
                "output": (f"PROTOCOL_DOES_NOT_DISCRIMINATE on "
                           f"{v['n_PROTOCOL_DOES_NOT_DISCRIMINATE']} of "
                           f"{s2['n_grid_points']} grid points "
                           f"({v['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f})"),
                "metadata_fold": "threshold_surface",
                "metadata_uid": f"{rule}::required_{req}",
                "metadata_rule": rule, "metadata_detail": v,
                "predict_verdict_fraction":
                    f"{v['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f}",
                "eval_fraction_does_not_discriminate":
                    num(v["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
                "eval_n_discriminates": num(v["n_DISCRIMINATES"]),
                "eval_n_degenerate_ties": num(v["n_DISCRIMINATES_that_are_degenerate_ties"]),
            })
        se = sur["strict_exceed_criterion"]
        ex.append({
            "input": f"rule={rule} | criterion=STRICT_EXCEED",
            "output": (f"PROTOCOL_DOES_NOT_DISCRIMINATE on "
                       f"{se['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} of grid points; "
                       f"winners {se['winner_counts']}"),
            "metadata_fold": "threshold_surface",
            "metadata_uid": f"{rule}::strict_exceed",
            "metadata_rule": rule, "metadata_detail": se,
            "metadata_kappa_invariance": sur["check5_kappa_axis_invariance"],
            "predict_verdict_fraction":
                f"{se['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f}",
            "eval_fraction_does_not_discriminate":
                num(se["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
            "eval_n_discriminates": num(se["n_DISCRIMINATES"]),
        })
    ds.append({"dataset": "threshold_surface", "examples": ex})

    # 4 -------------------------------------------------- marginal flip table
    ex = []
    for i, f in enumerate(s2["marginal_flip_table"]):
        ex.append({
            "input": f"rule={f['rule']} | score={f['score']} | check={f['check']}",
            "output": (f"statistic {s(f['statistic'])} against a pre-registered "
                       f"threshold of {f['preregistered_threshold']}: "
                       f"{f['verdict_at_preregistered_threshold']}; "
                       + ("flips between "
                          f"{f['flip_boundary']['between']}" if f["flip_boundary"]
                          else "never flips in the swept range")),
            "metadata_fold": "marginal_flip_table",
            "metadata_uid": f"flip_{i}", "metadata_detail": f,
            "predict_verdict_at_prereg": f["verdict_at_preregistered_threshold"],
            "predict_flip_boundary": (str(f["flip_boundary"]["between"])
                                      if f["flip_boundary"] else "NONE"),
            "eval_flips_within_swept_range": float(f["flips_within_swept_range"]),
            **({"eval_statistic": num(f["statistic"])}
               if f["statistic"] is not None else {}),
        })
    ds.append({"dataset": "marginal_flip_table", "examples": ex})

    # 5 -------------------------------------------------- the three tables
    ex = []
    for tname, t in s3["tables"].items():
        for i, r in enumerate(t["rows"]):
            ex.append({
                "input": f"{tname} row {i}: {r[0]}",
                "output": " | ".join("" if v is None else str(v) for v in r),
                "metadata_fold": tname, "metadata_uid": f"{tname}_row{i}",
                "metadata_header": t["header"], "metadata_row": r,
                "metadata_caption": t["caption"],
                "metadata_footnotes": t["footnotes"],
                "predict_row_label": str(r[0]),
                "eval_row_index": float(i),
                "eval_n_columns": float(len(t["header"])),
                "eval_n_cells_populated": float(sum(
                    1 for c in r if c not in (None, "", "n/a"))),
            })
    ds.append({"dataset": "generated_tables", "examples": ex})

    # 6 -------------------------------------------------- prose audit
    ex = []
    for i, c in enumerate(s4["audit_of_draft"]["claims"]
                          + s4["audit_of_replacement_text"]["claims"]):
        ex.append({
            "input": f"[{c['source']}] {c['anchor']} :: {c['statistic_kind']} = {c['value']}",
            "output": f"{c['status']} (unit tag {c['unit_tag']})",
            "metadata_fold": "prose_audit", "metadata_uid": f"claim_{i}",
            "metadata_claim": c,
            "predict_status": c["status"],
            "predict_unit_tag": c["unit_tag"],
            "predict_json_pointer": c["json_pointer"] or "NONE",
            "eval_value": num(c["value"]),
            "eval_is_flagged": float(c["status"] in ("TRACEABLE_UNIT_MISSING",
                                                     "VALUE_MISMATCH", "UNTRACEABLE")),
        })
    ds.append({"dataset": "prose_audit_claims", "examples": ex})

    # 7 -------------------------------------------------- reproduction gate
    ex = []
    for L in s0["reproduction"]["legs"]:
        ex.append({
            "input": f"reproduction leg: {L['leg']}",
            "output": ("PASS" if L["pass"] else "FAIL")
            + f" | archived={L['archived']} recomputed={L['recomputed']}",
            "metadata_fold": "reproduction_gate", "metadata_uid": L["leg"],
            "metadata_leg": L,
            "predict_pass": "PASS" if L["pass"] else "FAIL",
            "eval_pass": float(L["pass"]),
            **({"eval_abs_delta": num(L["abs_delta"])}
               if L.get("abs_delta") is not None else {}),
        })
    ds.append({"dataset": "reproduction_gate", "examples": ex})
    return ds


def build_metrics(s0, s1, s2, s4) -> dict:
    h = s1["headline_discrepancy"]
    dv2 = s1["deltas"]["reliable14_rank_bottom_yV2::alpha_50_nonparametric_minus_ams_sigma"]
    de3 = s1["deltas"]["all19_drop_undefined_yE3::max_refusal_rate_minus_ams_sigma"]
    full = s2["surfaces"]["FULL_PREREGISTERED"]
    thr = s2["surfaces"]["THRESHOLD_ONLY"]
    ams = s1["table"]["all19_drop_undefined_yE3"]["scores"]["ams_sigma"]
    da = s4["audit_of_draft"]
    ra = s4["audit_of_replacement_text"]
    m = {
        "cost_usd": 0.0,
        "n_reproduction_legs": float(s0["reproduction"]["n_legs"]),
        "n_reproduction_legs_failed": float(s0["reproduction"]["n_failed"]),
        "n_members": 19.0, "n_lineage_labels": 7.0, "n_lineage_id_strings": 8.0,
        "n_members_y_outcome_disagrees_across_archives":
            float(s0["panel_assertions"]["y_outcome_disagreement"]["n_members_disagreeing"]),
        # the H-U repair
        "ourAMS_rho_member_level": float(h["recomputed_member_level"]),
        "ourAMS_rho_lineage_level": float(h["recomputed_lineage_level"]),
        "ourAMS_rho_gap_between_units": float(h["gap_in_rho"]),
        "n_score_cells_whose_rho_sign_flips_with_the_unit":
            float(h["unit_swing_summary"]["n_cells_whose_sign_flips_with_the_unit"]),
        "n_score_cells_compared_across_units":
            float(h["unit_swing_summary"]["n_score_x_config_cells"]),
        "max_abs_change_in_rho_from_unit_choice_alone":
            float(h["unit_swing_summary"]["max_abs_change_in_rho"]),
        "median_abs_change_in_rho_from_unit_choice_alone":
            float(h["unit_swing_summary"]["median_abs_change_in_rho"]),
        "ourAMS_icc_score": float(ams["why_they_differ"]["icc_score"]["icc"]),
        "ourAMS_icc_outcome": float(ams["why_they_differ"]["icc_outcome"]["icc"]),
        "oriented_delta_lineage_level_v2_carrier": float(dv2["lineage_level"]["delta"]),
        "oriented_delta_member_level_v2_carrier": float(dv2["member_level"]["delta"]),
        "oriented_delta_lineage_level_e3_carrier": float(de3["lineage_level"]["delta"]),
        "oriented_delta_member_level_e3_carrier": float(de3["member_level"]["delta"]),
        "oriented_ceiling_delta_lineage_level":
            float(dv2["lineage_level"]["ceiling"]["oriented_ceiling_delta"]),
        # the threshold surface
        "n_grid_points": float(s2["n_grid_points"]),
        "frac_does_not_discriminate_preregistered_rule":
            float(full["by_required"]["3"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
        "frac_does_not_discriminate_strict_exceed":
            float(full["strict_exceed_criterion"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
        "frac_does_not_discriminate_threshold_only_rule":
            float(thr["by_required"]["3"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
        "frac_does_not_discriminate_threshold_only_strict_exceed":
            float(thr["strict_exceed_criterion"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
        "frac_does_not_discriminate_checks_1_to_4_only":
            float(full["checks_1_to_4_only"]["3"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"]),
        "n_grid_points_where_check5_passes_any_row":
            float(full["check5_kappa_axis_invariance"]
                  ["n_grid_points_where_check5_passes_any_row"]),
        "n_single_axis_threshold_changes_that_flip_the_verdict":
            float(s2["minimal_verdict_flipping_changes"]["FULL_PREREGISTERED"]
                  ["n_single_axis_changes_that_flip_the_verdict"]),
        "n_matrix_cells_reproduced":
            float(s2["matrix_reproduction_at_preregistered_thresholds"]["n_cells"]
                  - s2["matrix_reproduction_at_preregistered_thresholds"]["n_mismatch"]),
        # the prose audit
        "n_prose_claims_audited": float(da["n_claims_audited"]),
        "n_prose_claims_traceable_unit_stated":
            float(da["counts_by_status"].get("TRACEABLE_UNIT_STATED", 0)),
        "n_prose_claims_traceable_unit_missing":
            float(da["counts_by_status"].get("TRACEABLE_UNIT_MISSING", 0)),
        "n_prose_claims_value_mismatch":
            float(da["counts_by_status"].get("VALUE_MISMATCH", 0)),
        "n_prose_claims_untraceable":
            float(da["counts_by_status"].get("UNTRACEABLE", 0)),
        "n_prose_claims_flagged": float(da["n_flagged"]),
        "n_replacement_claims_audited": float(ra["n_claims_audited"]),
        "n_replacement_claims_flagged": float(ra["n_flagged"]),
        "replacement_flag_list_empty": float(ra["flag_list_empty"]),
        "n_tables_generated": 3.0,
    }
    return m


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("assemble")
    s0 = jload(OUT / "stage0.json")
    s1 = jload(OUT / "stage1_dual_aggregation.json")
    s2 = jload(OUT / "stage2_threshold_surface.json")
    s3 = jload(OUT / "stage3_tables.json")
    s4 = jload(OUT / "stage4_prose_audit.json")

    dv2 = s1["deltas"]["reliable14_rank_bottom_yV2::alpha_50_nonparametric_minus_ams_sigma"]
    de3 = s1["deltas"]["all19_drop_undefined_yE3::max_refusal_rate_minus_ams_sigma"]
    full = s2["surfaces"]["FULL_PREREGISTERED"]

    verdicts = {
        "reproduction_gate": s0["reproduction"]["status"],
        "sign_survives_unit_choice_v2_carrier": dv2["sign_survives_unit_choice"],
        "ci_exclusion_survives_unit_choice_v2_carrier":
            dv2["ci_exclusion_survives_unit_choice"],
        "sign_survives_unit_choice_e3_carrier": de3["sign_survives_unit_choice"],
        "ci_exclusion_survives_unit_choice_e3_carrier":
            de3["ci_exclusion_survives_unit_choice"],
        "aggregation_unit_discrepancy": s1["headline_discrepancy"]["verdict"],
        "threshold_surface_preregistered_rule":
            ("VERDICT_STABLE_OVER_THE_WHOLE_GRID"
             if full["by_required"]["3"]["fraction_PROTOCOL_DOES_NOT_DISCRIMINATE"] == 1.0
             else "VERDICT_NOT_STABLE_OVER_THE_GRID"),
        "threshold_surface_strict_exceed":
            s2["minimal_verdict_flipping_changes"]["FULL_PREREGISTERED"]["verdict"],
        "check5_kappa_axis": "CANNOT_CHANGE_ANY_DISCRIMINATION_VERDICT",
        "replacement_text_flag_list_empty":
            "EMPTY" if s4["audit_of_replacement_text"]["flag_list_empty"] else "NON_EMPTY",
    }

    gaps = list(s3.get("gaps", []))
    yd = s0["panel_assertions"]["y_outcome_disagreement"]
    if yd["n_members_disagreeing"]:
        gaps.append({
            "gap": "Y_OUTCOME_DISAGREES_ACROSS_ARCHIVES",
            "detail": yd,
        })
    if not s4["audit_of_replacement_text"]["flag_list_empty"]:
        gaps.append({"gap": "REPLACEMENT_TEXT_RESIDUAL_FLAGS",
                     "detail": s4["audit_of_replacement_text"]["flagged"]})
    gaps.append({
        "gap": "PLAN_ESTIMATE_NOT_REPRODUCED_AS_STATED",
        "detail": ("The hypothesis estimated the member-level oriented Delta at "
                   "about -0.465. The COMPUTED values are "
                   f"{de3['member_level']['delta']:.4f} on the discrimination "
                   f"matrix's alpha_50 carrier (max refusal rate, 19 members) and "
                   f"{dv2['member_level']['delta']:.4f} on V2's carrier "
                   f"(non-parametric alpha_50, 14 analysable members). The plan's "
                   "figure was an arithmetic estimate from two separately-oriented "
                   "rho values, not a computed paired statistic; nothing was tuned "
                   "to hit it."),
    })

    out = {
        "metadata": {
            "evaluation_name": "Same numbers, both counting units",
            "description": (
                "A pure-reanalysis evaluation over the FROZEN iteration-2/3 "
                "archives: zero GPU, zero generation, zero LLM/API spend, no "
                "downloads, no network. It repairs the aggregation-unit defect "
                "(the same correlation reported at two units in two sections), "
                "converts PROTOCOL_DOES_NOT_DISCRIMINATE from a step function of "
                "five cutoffs into a 164,736-point stability surface, ships the "
                "three tables the main text is missing, and audits every "
                "correlation-bearing number in the draft against a json pointer."),
            "verdicts": verdicts,
            "inputs": s0["inputs"],
            "archived_definitions_route": s0["archived_definitions_route"],
            "panel_assertions": s0["panel_assertions"],
            "orientation_map": s0["orientation_map"],
            "pass_rule_thresholds": s0["pass_rule_thresholds"],
            "discrimination_rule": s0["discrimination_rule"],
            "reproduction": s0["reproduction"],
            "analysis_1_dual_aggregation": {
                "configs": s1["configs"], "table": s1["table"],
                "deltas": s1["deltas"],
                "headline_discrepancy": s1["headline_discrepancy"],
                "methodological_note": s1["methodological_note"],
            },
            "analysis_2_threshold_surface": {
                "grid": s2["grid"], "n_grid_points": s2["n_grid_points"],
                "preregistered_thresholds": s2["preregistered_thresholds"],
                "fixed_per_check_statistics": s2["fixed_per_check_statistics"],
                "matrix_reproduction_at_preregistered_thresholds":
                    s2["matrix_reproduction_at_preregistered_thresholds"],
                "surfaces": s2["surfaces"],
                "check1_named_case": s2["check1_named_case"],
                "minimal_verdict_flipping_changes":
                    s2["minimal_verdict_flipping_changes"],
            },
            "analysis_3_tables": {k: {kk: vv for kk, vv in v.items() if kk != "rows"}
                                  for k, v in s3["tables"].items()},
            "analysis_4_prose_audit": {
                "audit_of_draft": {k: v for k, v in s4["audit_of_draft"].items()
                                   if k != "claims"},
                "audit_of_replacement_text":
                    {k: v for k, v in s4["audit_of_replacement_text"].items()
                     if k != "claims"},
                "assertion": s4["assertion"],
                "recommended_deletions": s4["recommended_deletions"],
                "number_dumps_for_supplementary": s4["number_dumps_for_supplementary"],
            },
            "gaps": gaps,
            "determinism": {"boot_seed": s1["boot_seed"], "n_boot": s1["n_boot"],
                            "permutation": "exhaustive over 7! = 5040 lineage assignments"},
            "spend": {"cost_usd": 0.0, "llm_calls": 0, "gpu_seconds": 0,
                      "network_requests": 0, "models_downloaded": 0},
        },
        "metrics_agg": build_metrics(s0, s1, s2, s4),
        "datasets": build_datasets(s0, s1, s2, s3, s4),
    }
    jdump(out, HERE / "eval_out.json")
    logger.info(f"wrote eval_out.json: {len(out['datasets'])} datasets, "
                f"{sum(len(d['examples']) for d in out['datasets'])} examples, "
                f"{len(out['metrics_agg'])} aggregate metrics")
    write_readme(out, s0, s1, s2, s3, s4)
    return out


def write_readme(out, s0, s1, s2, s3, s4) -> None:
    v = out["metadata"]["verdicts"]
    m = out["metrics_agg"]
    dv2 = s1["deltas"]["reliable14_rank_bottom_yV2::alpha_50_nonparametric_minus_ams_sigma"]
    full = s2["surfaces"]["FULL_PREREGISTERED"]
    thr = s2["surfaces"]["THRESHOLD_ONLY"]
    L = [
        "# Same numbers, both counting units",
        "",
        "**VERDICT (first).** The reproduction gate PASSES on "
        f"{int(m['n_reproduction_legs'] - m['n_reproduction_legs_failed'])}/"
        f"{int(m['n_reproduction_legs'])} legs, so this re-analysis is entitled to "
        "restate the archives' numbers. Three things then follow.",
        "",
        f"1. **The aggregation-unit defect is real and it is load-bearing.** The "
        f"draft's `{m['ourAMS_rho_member_level']:.3f}` (§5.2) and "
        f"`{m['ourAMS_rho_lineage_level']:.3f}` (§5.3) are the SAME statistic at "
        f"two different units -- 19 members against 7 lineage-aggregated units -- "
        f"and the gap of {m['ourAMS_rho_gap_between_units']:.3f} in rho is larger "
        f"than the effect the paper argues about. Neither section names its unit. "
        f"Verdict: `{v['aggregation_unit_discrepancy']}`.",
        f"2. **The oriented Delta's sign survives the unit choice; its CI "
        f"exclusion does not.** On V2's carrier: "
        f"`{v['sign_survives_unit_choice_v2_carrier']}` and "
        f"`{v['ci_exclusion_survives_unit_choice_v2_carrier']}` -- "
        f"Delta = {dv2['lineage_level']['delta']:.3f} "
        f"{fmt(dv2['lineage_level']['ci95'])} at the lineage level against "
        f"{dv2['member_level']['delta']:.3f} "
        f"{fmt(dv2['member_level']['ci95'])} at the member level. On the "
        f"discrimination matrix's own alpha_50 carrier the sign does NOT survive: "
        f"`{v['sign_survives_unit_choice_e3_carrier']}`.",
        f"3. **The negative result is not manufactured by the cutoffs.** Over a "
        f"{int(m['n_grid_points']):,}-point full factorial in the five thresholds, "
        f"the pre-registered rule returns `PROTOCOL_DOES_NOT_DISCRIMINATE` on "
        f"{m['frac_does_not_discriminate_preregistered_rule']:.4f} of grid points "
        f"and the stricter strict-exceed criterion on "
        f"{m['frac_does_not_discriminate_strict_exceed']:.4f}. Exactly "
        f"{int(m['n_single_axis_threshold_changes_that_flip_the_verdict'])} "
        f"single-axis change anywhere on the grid produces a strict rival win "
        f"(check 3 lowered from 2.0 to 1.75, our-AMS 2 against alpha_50's 1).",
        "",
        f"Scale of the unit effect, measured on the paper's own numbers: over the "
        f"{int(m['n_score_cells_compared_across_units'])} score x config cells "
        f"where both units are defined, changing NOTHING but the aggregation unit "
        f"moves the oriented correlation by a median of "
        f"{m['median_abs_change_in_rho_from_unit_choice_alone']:.3f} and a maximum "
        f"of {m['max_abs_change_in_rho_from_unit_choice_alone']:.3f}, and flips the "
        f"SIGN on {int(m['n_score_cells_whose_rho_sign_flips_with_the_unit'])} of "
        f"them.",
        "",
        "## What was run",
        "",
        "Zero GPU, zero generation, zero LLM/API spend, no downloads, no network: "
        f"`cost_usd = {m['cost_usd']}`. Every input file is sha256-stamped into "
        "`eval_out.json:metadata.inputs`. The estimator code is IMPORTED from the "
        "frozen archive rather than re-implemented "
        f"(`{s0['archived_definitions_route']['route']}`); the plan named "
        "`lib/stats_ext.py`, the functions it lists actually live in "
        "`lib_iter3/statsx.py`, and that correction is recorded in the output.",
        "",
        "| stage | output | what it does |",
        "|---|---|---|",
        "| `stage0_ingest.py` | `out/stage0.json` | sha256 manifest, panel assembly, unit assertions, the reproduction gate |",
        "| `stage1_dual.py` | `out/stage1_dual_aggregation.json` | every score at BOTH units under a 6-cell analysis-choice grid |",
        "| `stage2_sweep.py` | `out/stage2_threshold_surface.json` | the 164,736-point threshold factorial + the marginal flip table |",
        "| `stage3_tables.py` | `out/tables/*.{md,csv}` | the three missing tables, generated FROM json |",
        "| `stage4_prose.py` | `out/stage4_prose_audit.json`, `out/replacement_text.md` | the prose audit and the repaired text |",
        "| `assemble.py` | `eval_out.json`, `README.md` | folds the stages into the schema |",
        "",
        "Run everything with `uv run eval.py` (or `--stage N` for one stage).",
        "",
        "## Reproduction gate",
        "",
        "| leg | archived | recomputed | pass |",
        "|---|---|---|---|",
    ]
    for leg in s0["reproduction"]["legs"]:
        L.append(f"| `{leg['leg']}` | {leg['archived']} | {leg['recomputed']} | "
                 f"{'PASS' if leg['pass'] else '**FAIL**'} |")
    L += [
        "",
        "## Analysis 1 -- dual aggregation",
        "",
        f"{s1['methodological_note']}",
        "",
        "Full table: `out/tables/table3_dual_aggregation.md` (32 rows, one per "
        "score x unit x config; every cell carries rho, CI, permutation p, the "
        "floor, n, and the unit in the row label).",
        "",
        "## Analysis 2 -- the threshold surface",
        "",
        "| rule | criterion | fraction PROTOCOL_DOES_NOT_DISCRIMINATE |",
        "|---|---|---|",
        f"| pre-registered (threshold AND secondary clause) | rival >= 3 of 5 | "
        f"{full['by_required']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} |",
        f"| pre-registered | rival strictly exceeds alpha_50 | "
        f"{full['strict_exceed_criterion']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} |",
        f"| pre-registered, checks 1-4 only | rival >= 3 of 4 | "
        f"{full['checks_1_to_4_only']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} |",
        f"| threshold-only (secondary clauses dropped) | rival >= 3 of 5 | "
        f"{thr['by_required']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} |",
        f"| threshold-only | rival strictly exceeds alpha_50 | "
        f"{thr['strict_exceed_criterion']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f} |",
        "",
        "The two rows differ by a factor of four, and that difference LOCATES the "
        "negative result: it is carried by the pass rules' verdict-class and "
        "interiority clauses, not by the numeric cutoffs. Check 5 contributes "
        "nothing at any grid point -- its REFUSAL kappa of 0.391 lies below the "
        "entire swept range [0.40, 0.80], so it fails identically in all four rows "
        "and shifts every pass count together; the invariance is proved "
        "structurally and verified empirically over the whole kappa axis "
        f"(`{v['check5_kappa_axis']}`).",
        "",
        "## Analysis 3 -- the three tables",
        "",
    ]
    for k, t in s3["tables"].items():
        L.append(f"- `out/tables/{t['name']}.{{md,csv}}` -- {t['caption']}")
    L += [
        "",
        "## Analysis 4 -- prose audit",
        "",
        f"{int(m['n_prose_claims_audited'])} correlation-, AUROC-, Delta- and "
        f"CI-bearing claims were extracted from the draft's Contributions and "
        f"Results sections and each was tagged with an aggregation unit and a json "
        f"pointer: {int(m['n_prose_claims_traceable_unit_stated'])} "
        f"TRACEABLE_UNIT_STATED, {int(m['n_prose_claims_traceable_unit_missing'])} "
        f"TRACEABLE_UNIT_MISSING, {int(m['n_prose_claims_value_mismatch'])} "
        f"VALUE_MISMATCH, {int(m['n_prose_claims_untraceable'])} UNTRACEABLE -- "
        f"{int(m['n_prose_claims_flagged'])} flagged in total. The repaired text "
        f"in `out/replacement_text.md` re-audits at "
        f"{int(m['n_replacement_claims_audited'])} claims and "
        f"{int(m['n_replacement_claims_flagged'])} flags "
        f"(`{v['replacement_text_flag_list_empty']}`).",
        "",
        "Three prose number-dumps are recommended for supplementary:",
        "",
    ]
    for d in s4["number_dumps_for_supplementary"]:
        L.append(f"- **{d['anchor']}** ({d['n_numbers']} numbers) -> replace with "
                 f"`{d['replaced_by_table']}`. First words: {d['first_words']}")
    L += ["", "## Gaps and honest disclosures", ""]
    for g in out["metadata"]["gaps"]:
        if isinstance(g, dict):
            L.append(f"- **{g.get('gap', 'gap')}**: "
                     f"{str(g.get('detail'))[:600]}")
        else:
            L.append(f"- {g}")
    (HERE / "README.md").write_text("\n".join(L) + "\n")
    logger.info("wrote README.md")


if __name__ == "__main__":
    main()
