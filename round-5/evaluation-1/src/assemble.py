#!/usr/bin/env python3
"""ASSEMBLE -- eval_out.json, the schema payload, and RESULTS.md.

RESULTS.md is rendered FROM eval_out.json so that it regenerates byte-identically
and no prose number is hand-typed, which is the discipline the upstream artifact
already applies to itself.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from common5 import ARMS, HERE, OUT, fmt, fmt_ci, fmt_p, jdump

VERDICT_ORDER = ["READS", "AMBIGUOUS", "AT_CHANCE", "UNDEFINED"]

SENTINEL = -1.0   # "this quantity does not exist for this row" -- never imputed


def num(v, default: float = SENTINEL) -> float:
    """Schema requires eval_* to be a number. A quantity that does not exist for
    a row (an UNDEFINED member has no AUROC) is written as the explicit sentinel
    -1.0, which is outside every real range here, rather than as a plausible
    finite value."""
    if v is None:
        return default
    try:
        f = float(v)
    except (TypeError, ValueError):
        return default
    return f if np.isfinite(f) else default


# --------------------------------------------------------------------------
def build_metrics_agg(s1, s2, s3) -> dict:
    P = s2["primary"]
    lad = s2["control_ladder"]
    dec = s2["confound"]["variance_decomposition"]
    rev = s2["reviewer_0p434_reproduction"]
    arm = s3["abliterated_arm"]
    ans = s3["attainability_simulation"]["extracted_answers"]
    ct_all, ct_pow = s3["tally_all_members"], s3["tally_detection_powered"]

    def g(d, *ks, default=None):
        for k in ks:
            if d is None:
                return default
            d = d.get(k) if isinstance(d, dict) else None
        return d if d is not None else default

    m = {
        # --- reproduction gate
        "gate_n_legs": s1["n_legs"],
        "gate_n_pass": s1["n_pass"],
        "gate_pass_fraction": s1["n_pass"] / s1["n_legs"],
        "gate_G1_pass": float(bool(s1["G1_pass"])),
        "gate_g4_n_item_level": s1["g4_levels"]["n_item_level"],
        "gate_g4_n_summary_level": s1["g4_levels"]["n_summary_level"],
        # --- H-C primary
        "within_axisA_member_rho": P["member"]["rho"],
        "within_axisA_member_ci_lo": P["member"]["ci95"][0],
        "within_axisA_member_ci_hi": P["member"]["ci95"][1],
        "within_axisA_member_ci_half_width": P["member"]["half_width"],
        "within_axisA_member_perm_p": P["member"]["p_permutation"],
        "within_axisA_n_members": P["member"]["n_points"],
        "within_axisA_n_lineages": P["member"]["n_clusters"],
        "within_axisA_lineage_rho": P["lineage"]["rho"],
        "within_axisA_lineage_ci_lo": P["lineage"]["ci95"][0],
        "within_axisA_lineage_ci_hi": P["lineage"]["ci95"][1],
        "perm_floor_1_over_5040": P["member"]["p_floor"],
        # --- pooled and ladder
        "pooled_70pair_rho": lad[0]["member"]["rho"],
        "pooled_70pair_ci_lo": lad[0]["member"]["ci95"][0],
        "pooled_70pair_ci_hi": lad[0]["member"]["ci95"][1],
        "pooled_70pair_lineage_rho": lad[0]["lineage"]["rho"],
        "ladder_minus_D_rho": lad[1]["member"]["rho"],
        "ladder_minus_C_rho": lad[2]["member"]["rho"],
        "ladder_minus_CD_rho": lad[3]["member"]["rho"],
        "ladder_ABE_only_rho": lad[4]["member"]["rho"],
        # --- confound
        "share_between_axis_type": dec["shares"]["between_axis_type"],
        "share_between_member": dec["shares"]["between_member"],
        "share_residual": dec["shares"]["residual"],
        "shares_sum": dec["shares_sum"],
        "partial_rho_controlling_axis": s2["confound"]["partial_controlling_axis"]["rho"],
        "partial_rho_controlling_member":
            s2["confound"]["partial_controlling_member"]["rho"],
        "residual_coupling_rho":
            s2["confound"]["residual_member_level_coupling"]["rho"],
        "mixedlm_beta_rx": s2["confound"]["mixedlm"].get("beta_rx"),
        "mixedlm_p_rx": s2["confound"]["mixedlm"].get("p_rx"),
        "within_member_mean_rho": s2["within_member"]["mean_rho"],
        # --- per axis
        "rho_axis_A": s2["per_axis"]["A_canned"]["member"]["rho"],
        "rho_axis_B": s2["per_axis"]["B_paraphrase"]["member"]["rho"],
        "rho_axis_C": s2["per_axis"]["C_stylistic"]["member"]["rho"],
        "rho_axis_D": s2["per_axis"]["D_random0"]["member"]["rho"],
        "rho_axis_E": s2["per_axis"]["E_prompt_contrast"]["member"]["rho"],
        # --- reviewer leg
        "reviewer_n13_rho": g(rev, "identified_rule", "rho"),
        "reviewer_n13_p": g(rev, "identified_rule", "p_asymptotic"),
        "n14_rho": rev["n14"]["rho"],
        "n14_p": rev["n14"]["p_asymptotic"],
        "reviewer_reproduced": float(bool(rev["reproduced"])),
        # --- secondary
        "secondary_c50_rho_sentinel": s2["secondary_c50"]["member"]["rho"],
        "secondary_c50_censoring_fraction": s2["secondary_c50"]["censoring_fraction"],
        # --- H-K tallies
        "tally_all_READS": ct_all["col_totals"]["READS"],
        "tally_all_AMBIGUOUS": ct_all["col_totals"]["AMBIGUOUS"],
        "tally_all_AT_CHANCE": ct_all["col_totals"]["AT_CHANCE"],
        "tally_all_UNDEFINED": ct_all["col_totals"]["UNDEFINED"],
        "tally_powered_n": ct_pow["grand_total"],
        "tally_powered_READS": ct_pow["col_totals"]["READS"],
        "tally_powered_AMBIGUOUS": ct_pow["col_totals"]["AMBIGUOUS"],
        "tally_powered_AT_CHANCE": ct_pow["col_totals"]["AT_CHANCE"],
        "tally_powered_UNDEFINED": ct_pow["col_totals"]["UNDEFINED"],
        # --- H-K simulation
        "sim_n_cells": s3["attainability_simulation"]["n_cells"],
        "sim_min_n_AT_CHANCE_k1":
            g(ans, "min_n_for_AT_CHANCE", "1", "min_n_with_any_AT_CHANCE",
              default=-1),
        "sim_min_n_AT_CHANCE_k4":
            g(ans, "min_n_for_AT_CHANCE", "4", "min_n_with_any_AT_CHANCE",
              default=-1),
        "sim_hanley_mcneil_min_n": ans["hanley_mcneil_closed_form"]["min_n_per_class"],
        "sim_P_AT_CHANCE_at_n40_k1":
            ans["pre_registered_gate_is_sufficient"][
                "P_AT_CHANCE_at_the_gate_true_auroc_0p50"]["1"],
        "sim_P_READS_at_chance_n10_k1": ans["P_READS_at_true_chance"]["1"]["10"],
        "sim_P_READS_at_chance_n40_k1": ans["P_READS_at_true_chance"]["1"]["40"],
        "sim_P_READS_perfect_n7_k1": ans["P_READS_under_perfect_separation"]["1"]["7"],
        "sim_P_READS_perfect_n33_k1": ans["P_READS_under_perfect_separation"]["1"]["33"],
        # --- deviation
        "n_UNDEFINED_members": s3["deviation_record"]["affected_members"]["n_UNDEFINED"],
        "n_unpowered_yet_READS":
            s3["deviation_record"]["affected_members"]["n_UNPOWERED_yet_READS"],
        # --- abliterated arm
        "abl_median_rate_weight_edited":
            arm["arm_medians"]["weight_edited_abliteration"],
        "abl_median_rate_aligned_reference": arm["arm_medians"]["aligned_reference"],
        "abl_median_rate_bu_candidate":
            arm["arm_medians"]["behavioural_uncensored_candidate"],
        "abl_mannwhitney_U": arm["mann_whitney"]["U"],
        "abl_mannwhitney_p": arm["mann_whitney"]["p_two_sided"],
        "abl_boot_delta_median": arm["lineage_clustered_bootstrap_median_difference"][
            "delta_median_point"],
        "abl_boot_ci_lo":
            arm["lineage_clustered_bootstrap_median_difference"]["ci95"][0],
        "abl_boot_ci_hi":
            arm["lineage_clustered_bootstrap_median_difference"]["ci95"][1],
        "abl_paired_n_pairs": arm["within_lineage_paired"]["n_pairs"],
        "abl_paired_n_lower": arm["within_lineage_paired"]["n_abliterated_lower"],
        "abl_paired_sign_p": arm["within_lineage_paired"]["sign_test"]["p_value"],
        "abl_claim_carried":
            float(bool(arm["structural_claim_carried_without_any_AUROC"])),
        "abl_n_READS_powered": arm["n_weight_edited_READS_powered"],
        "abl_n_READS_unpowered": arm["n_weight_edited_READS_unpowered"],
        # --- spend
        "llm_spend_usd": 0.0,
        "gpu_seconds": 0.0,
        "generation_calls": 0.0,
    }
    return {k: (float(v) if v is not None else float("nan")) for k, v in m.items()
            if v is not None and np.isfinite(float(v))}


# --------------------------------------------------------------------------
def build_datasets(s1, s2, s3) -> list[dict]:
    ds = []

    # 1. the reproduction gate, one example per leg
    ex = []
    for l in s1["legs"]:
        ex.append({
            "input": f"Reproduce: {l['leg']}",
            "output": str(l["target"]),
            "predict_recomputed": str(l["obtained"]),
            "metadata_level": l["level"],
            "metadata_status": l["status"],
            "metadata_note": l.get("note", ""),
            "eval_delta": num(l.get("delta"), 0.0),
            "eval_tolerance": num(l.get("tolerance"), 0.0),
            "eval_pass": 1.0 if l["status"] == "PASS" else 0.0,
        })
    ds.append({"dataset": "reproduction_gate", "examples": ex})

    # 2. the within-axis-A panel, one example per detection-powered member
    ex = []
    for r in s2["primary"]["members"]:
        ex.append({
            "input": (f"{r['checkpoint']} (lineage {r['lineage_id']}): "
                      f"does axis-A induction quality predict axis-A detection "
                      f"quality?"),
            "output": r["detection_verdict"],
            "predict_axisA_verdict": r["detection_verdict"],
            "metadata_lineage_id": r["lineage_id"],
            "metadata_c50_censored": r["A_c50"] is None,
            "eval_A_max_refusal_rate": num(r["A_max_rate"]),
            "eval_A_detection_auroc": num(r["A_auroc"]),
            "eval_A_c50": num(r["A_c50"]),
        })
    ds.append({"dataset": "within_axisA_coupling_panel", "examples": ex})

    # 3. the attainability surface, one example per simulated cell
    ex = []
    for c in s3["attainability_simulation"]["surface"]:
        ex.append({
            "input": (f"n per class = {c['n_per_class']}, true AUROC = "
                      f"{c['true_auroc']:.2f}, items per prompt = "
                      f"{c['items_per_prompt']}"),
            "output": "verdict probabilities under the shipped rule",
            "predict_modal_verdict": max(
                ("READS", "AT_CHANCE", "AMBIGUOUS", "UNDEFINED"),
                key=lambda v: c[f"P_{v}"]),
            "metadata_n_clusters": c["n_clusters"],
            "metadata_n_rep": c["n_rep"],
            "eval_n_per_class": float(c["n_per_class"]),
            "eval_true_auroc": float(c["true_auroc"]),
            "eval_items_per_prompt": float(c["items_per_prompt"]),
            "eval_P_READS": num(c["P_READS"]),
            "eval_P_AT_CHANCE": num(c["P_AT_CHANCE"]),
            "eval_P_AMBIGUOUS": num(c["P_AMBIGUOUS"]),
            "eval_P_UNDEFINED": num(c["P_UNDEFINED"]),
            "eval_mean_ci_width": num(c["mean_ci_width"]),
        })
    ds.append({"dataset": "verdict_rule_attainability_surface", "examples": ex})

    # 4. the abliterated-arm restatement, one example per member
    ex = []
    for t in s3["abliterated_arm"]["table"]:
        ex.append({
            "input": (f"{t['checkpoint']} (arm {t['arm']}, lineage "
                      f"{t['lineage_id']}): spontaneous refusal rate and axis-A "
                      f"verdict"),
            "output": t["A_verdict"],
            "predict_axisA_verdict": t["A_verdict"],
            "metadata_arm": t["arm"],
            "metadata_lineage_id": t["lineage_id"],
            "metadata_powered": t["powered"],
            "eval_spontaneous_refusal_rate": num(t["spontaneous_refusal_rate"]),
            "eval_wilson_lo": num(t["wilson95"][0]),
            "eval_wilson_hi": num(t["wilson95"][1]),
            "eval_n_refusal_of_scanned": num(t["n_refusal_of_scanned"]),
            "eval_n_scanned": num(t["n_scanned"]),
            "eval_A_auroc": num(t["A_auroc"]),
        })
    ds.append({"dataset": "abliterated_arm_refusal_rates", "examples": ex})

    return ds


# --------------------------------------------------------------------------
def render_results_md(doc: dict) -> str:
    a1, a2 = doc["analysis1"], doc["analysis2"]
    g = doc["reproduction_gate"]
    P, lad = a1["primary"], a1["control_ladder"]
    dec = a1["confound"]["variance_decomposition"]
    rev = a1["reviewer_0p434_reproduction"]
    arm = a2["abliterated_arm"]
    ans = a2["attainability_simulation"]["extracted_answers"]
    prov = doc["provenance"]
    L = []
    A = L.append

    A("# Recheck the read-versus-act coupling and the verdict rule")
    A("")
    A("Pure reanalysis of the frozen iteration-4 read-versus-act tree. "
      f"{prov['spend']['statement']} "
      f"Inputs: {prov['n_inputs']} files, each sha256-stamped; "
      f"{len(prov['missing'])} missing.")
    A("")
    A("## The short version")
    A("")
    A(f"**The read-act coupling is a between-axis-type contrast, not a "
      f"relationship among models.** Within the canonical axis A, across the "
      f"{P['member']['n_points']} detection-powered checkpoints, "
      f"rho = {fmt(P['member']['rho'])} {fmt_ci(P['member']['ci95'])} over "
      f"{P['member']['n_clusters']} lineage resampling units "
      f"(exhaustive permutation p = {fmt(P['member']['p_permutation'])}, floor "
      f"{fmt(P['member']['p_floor'], 5)}). The axis that induces is also the axis "
      f"that reads, but among models the two qualities are only weakly and "
      f"non-significantly related. A two-way decomposition of the shipped pooled "
      f"statistic attributes "
      f"{fmt(dec['shares']['between_axis_type'])} of it to between-axis-type "
      f"variation, {fmt(dec['shares']['between_member'])} to between members and "
      f"{fmt(dec['shares']['residual'])} to residual.")
    A("")
    A(f"**Pre-registered verdict: `{a1['verdict']['verdict']}`** "
      f"(all strings that fired: {', '.join(a1['verdict']['all_fired'])}).")
    A("")
    A(f"**The verdict rule is n-asymmetric and it is now measured.** "
      f"At a true AUROC of 0.500 the AT_CHANCE verdict is unreachable below "
      f"n = {ans['min_n_for_AT_CHANCE']['1']['min_n_with_any_AT_CHANCE']} items per "
      f"class; P(AT_CHANCE) at the pre-registered n = 40 gate is "
      f"{fmt(ans['pre_registered_gate_is_sufficient']['P_AT_CHANCE_at_the_gate_true_auroc_0p50']['1'])}. "
      f"Under perfect separation READS fires with probability "
      f"{fmt(ans['P_READS_under_perfect_separation']['1']['7'])} at n = 7.")
    A("")
    A(f"**The abliterated arm survives without any AUROC.** "
      f"Median spontaneous refusal rate "
      f"{fmt(arm['arm_medians']['weight_edited_abliteration'], 4)} in the "
      f"weight-edited arm against "
      f"{fmt(arm['arm_medians']['aligned_reference'], 4)} in the aligned reference "
      f"(exact Mann-Whitney p = {fmt_p(arm['mann_whitney']['p_two_sided'])}; "
      f"{arm['within_lineage_paired']['n_abliterated_lower']} of "
      f"{arm['within_lineage_paired']['n_pairs']} within-lineage pairs, sign test "
      f"p = {fmt_p(arm['within_lineage_paired']['sign_test']['p_value'])}).")
    A("")

    A("## R1 Reproduction gate")
    A("")
    A(f"{g['n_pass']} of {g['n_legs']} legs PASS at tolerance 1e-6 -> "
      f"**{g['gate_verdict']}**. G1 (the stop-the-line leg) "
      f"{'PASSES' if g['G1_pass'] else 'FAILS'}.")
    A("")
    A("| group | legs | pass | all pass |")
    A("|---|---|---|---|")
    for grp in sorted(g["by_group"]):
        b = g["by_group"][grp]
        A(f"| {grp} | {b['n']} | {b['n_pass']} | {'yes' if b['all_pass'] else 'NO'} |")
    A("")
    A("| leg | target | obtained | delta |")
    A("|---|---|---|---|")
    for l in g["legs"]:
        if l["leg"].startswith(("G1", "G2", "G3a", "G3b", "G6", "G7")):
            A(f"| {l['leg']} | {l['target']} | {l['obtained']} | "
              f"{fmt(l['delta'], 9) if l['delta'] is not None else '--'} |")
    A("")
    A(f"**The 18-versus-20 discrepancy, resolved.** "
      f"{g['verdict_tally_resolution']['diagnosis']} The stale figure is carried by: "
      + "; ".join(f"`{Path(p).name}`"
                  for p in g["verdict_tally_resolution"]["where_the_stale_one_lives"])
      + ".")
    A("")
    A(f"**Lineage bookkeeping.** {g['lineage_bookkeeping']['note']}")
    A("")

    A("## R2 The coupling without the axis-type contrast (H-C)")
    A("")
    A("Every quantity is given at BOTH aggregation units. CIs are "
      "lineage-clustered percentile bootstrap at 10,000 reps; the number of "
      "resampling units is printed beside each one; permutation p is exhaustive "
      "over all 5040 permutations of the 7 lineage labels, floor 1/5040 = "
      f"{fmt(P['member']['p_floor'], 5)}.")
    A("")
    A("| quantity | member unit | n / units | lineage unit | n / units | perm p |")
    A("|---|---|---|---|---|---|")

    def row(label, blk):
        m, l = blk["member"], blk["lineage"]
        return (f"| {label} | {fmt(m['rho'])} {fmt_ci(m['ci95'])} | "
                f"{m['n_points']} / {m['n_clusters']} | "
                f"{fmt(l['rho'])} {fmt_ci(l['ci95'])} | "
                f"{l['n_points']} / {l['n_clusters']} | "
                f"{fmt_p(m['p_permutation'])} |")

    A(row("**PRIMARY within-axis-A**", P))
    A(row("secondary, x = -log10 c_50 (rank_bottom sentinel)",
          {"member": a1["secondary_c50"]["member"],
           "lineage": a1["secondary_c50"]["lineage"]}))
    for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0",
               "E_prompt_contrast"):
        A(row(f"within axis {a1['per_axis'][ax]['short']} "
              f"({a1['per_axis'][ax]['by_construction'].split('(')[0].strip()})",
              a1["per_axis"][ax]))
    A("")
    A("### R2b Control ladder -- how much of the pooled figure is the control contrast")
    A("")
    A("| axis subset | pairs | member unit | lineage unit | perm p |")
    A("|---|---|---|---|---|")
    for b in lad:
        A(f"| {b['subset']} | {b['n_pairs']} | {fmt(b['member']['rho'])} "
          f"{fmt_ci(b['member']['ci95'])} | {fmt(b['lineage']['rho'])} "
          f"{fmt_ci(b['lineage']['ci95'])} | {fmt_p(b['member']['p_permutation'])} |")
    A("")
    A("### R2c Naming the confound")
    A("")
    A("| estimate | value | 95% CI | n |")
    A("|---|---|---|---|")
    for key, lab in (("partial_controlling_axis",
                      "partial Spearman, axis identity partialled out"),
                     ("partial_controlling_member",
                      "partial Spearman, member identity partialled out"),
                     ("residual_member_level_coupling",
                      "residual coupling, both main effects removed")):
        b = a1["confound"][key]
        A(f"| {lab} | {fmt(b['rho'])} | {fmt_ci(b['ci95'])} | {b['n_points']} |")
    mm = a1["confound"]["mixedlm"]
    A(f"| {mm['used'].split('--')[0].strip()} slope on ranks | "
      f"{fmt(mm.get('beta_rx'))} | {fmt_ci(mm.get('ci95_rx'))} | "
      f"{mm.get('n_obs')} |")
    A("")
    A("| variance component | share of the pooled rank cross-product |")
    A("|---|---|")
    for k, v in dec["shares"].items():
        A(f"| {k} | {fmt(v)} |")
    A(f"| **sum** | **{fmt(dec['shares_sum'])}** |")
    A("")
    A(f"The within-member mean of {a1['within_member']['n_coefficients']} "
      f"five-point coefficients is {fmt(a1['within_member']['mean_rho'])}. "
      f"{a1['within_member']['label']}")
    A("")
    A(f"**Reviewer recompute.** {rev['statement']}")
    A("")

    A("## R3 The verdict rule (H-K)")
    A("")
    A(a2["tally_markdown"])
    A("")
    A("### R3b Attainability of the verdicts, simulated on the artifact's own estimator")
    A("")
    A(f"{a2['attainability_simulation']['n_cells']} cells x "
      f"{a2['attainability_simulation']['grid']['n_replicates_per_cell']} replicates "
      f"x {a2['attainability_simulation']['grid']['n_boot_inner']} inner resamples "
      f"({a2['attainability_simulation']['wall_seconds']:.0f} s wall).")
    A("")
    A("| n per class | P(AT_CHANCE) at true AUROC 0.50 | P(READS) at true AUROC "
      "0.50 | mean CI width | P(READS) at true AUROC 1.00 |")
    A("|---|---|---|---|---|")
    k1 = ans["min_n_for_AT_CHANCE"]["1"]
    for n in ("5", "10", "20", "40", "80", "160"):
        pr1 = None
        for c in a2["attainability_simulation"]["surface"]:
            if (c["n_per_class"] == int(n) and c["items_per_prompt"] == 1
                    and abs(c["true_auroc"] - 1.0) < 1e-9):
                pr1 = c["P_READS"]
        A(f"| {n} | {fmt(k1['P_AT_CHANCE_by_n'][n])} | "
          f"{fmt(ans['P_READS_at_true_chance']['1'][n])} | "
          f"{fmt(k1['mean_ci_width_by_n'][n])} | {fmt(pr1)} |")
    A("")
    A("| shipped unpowered n per class | P(READS) under perfect separation |")
    A("|---|---|")
    for n, v in ans["P_READS_under_perfect_separation"]["1"].items():
        A(f"| {n} | {fmt(v)} |")
    A("")
    A(f"**Footnote for every 'zero AT_CHANCE' sentence.** "
      f"{a2['attainability_simulation']['footnote']}")
    A("")
    A("### R3c Gate deviation record")
    A("")
    dv = a2["deviation_record"]
    A(f"`{dv['id']}` -- {dv['trigger']}")
    A("")
    A(f"* **Method said:** {dv['what_the_method_said']}")
    A(f"* **Code does:** {dv['what_the_code_does']}")
    A(f"* **Code path:** `explib.py:{dv['code_path']['verdict']['lines']}`, "
      f"`explib.py:{dv['code_path']['resample_guard']['lines']}`, "
      f"`gpu_stage.py:{dv['code_path']['powered_flag']['lines']}`")
    A(f"* **Affected:** {dv['affected_members']['n_UNDEFINED']} UNDEFINED, "
      f"{dv['affected_members']['n_UNPOWERED_yet_READS']} unpowered yet READS")
    A("")
    A("| member | n ref / com | verdict | powered |")
    A("|---|---|---|---|")
    for m in dv["affected_members"]["UNPOWERED_yet_READS"]:
        A(f"| `{m['checkpoint']}` | {m['n_refusal']} / {m['n_compliance']} | "
          f"READS | N |")
    for m in dv["affected_members"]["UNDEFINED_verdict"]:
        A(f"| `{m['checkpoint']}` | {m['n_refusal']} / {m['n_compliance']} | "
          f"UNDEFINED | N |")
    A("")

    A("## R4 The abliterated arm, restated on refusal-rate evidence")
    A("")
    A("| member | n ref / com | spont. rate [Wilson 95%] | pow | A AUROC [CI] | "
      "verdict |")
    A("|---|---|---|---|---|---|")
    for t in arm["weight_edited"]:
        A(f"| `{t['checkpoint']}` | {t['n_refusal_scored']} / "
          f"{t['n_compliance_scored']} | {fmt(t['spontaneous_refusal_rate'], 4)} "
          f"[{fmt(t['wilson95'][0], 4)}, {fmt(t['wilson95'][1], 4)}] | "
          f"{'y' if t['powered'] else 'N'} | {fmt(t['A_auroc'])} "
          f"{fmt_ci(t['A_ci95'])} | {t['A_verdict']} |")
    A("")
    A("| test (no AUROC involved) | statistic | p | CI |")
    A("|---|---|---|---|")
    mw = arm["mann_whitney"]
    bs = arm["lineage_clustered_bootstrap_median_difference"]
    st = arm["within_lineage_paired"]["sign_test"]
    A(f"| Mann-Whitney U on member rates ({mw['n_weight_edited']} vs "
      f"{mw['n_aligned_reference']}), tie-corrected asymptotic | "
      f"U = {fmt(mw['U'], 1)} | {fmt_p(mw['p_two_sided'])} | -- |")
    A(f"| the same, EXHAUSTIVE permutation over all "
      f"{mw['n_permutations']:,} group assignments (valid under the "
      f"{mw['n_tied_values_across_arms']} value tied across the arms) | "
      f"U = {fmt(mw['U'], 1)} | "
      f"{fmt_p(mw['p_exhaustive_permutation'])} | floor "
      f"{fmt_p(mw['p_permutation_floor'])} |")
    A(f"| lineage-clustered bootstrap of the median difference "
      f"({bs['n_resampling_units']} units) | {fmt(bs['delta_median_point'], 4)} | "
      f"{fmt_p(bs['p_boot_two_sided'])} | {fmt_ci(bs['ci95'], 4)} |")
    A(f"| exact paired sign test, within-lineage pairs | {st['k']} of {st['n']} | "
      f"{fmt_p(st['p_value'])} | {fmt_ci(st['ci95_proportion'])} |")
    A("")
    A(f"Structural claim carried without any AUROC: "
      f"**{arm['structural_claim_carried_without_any_AUROC']}** -- "
      f"\"{arm['claim_text']}\".")
    A("")

    A("## R5 Prose audit")
    A("")
    pa = doc["replacement_text"]["audit"]
    A(f"{pa['n_pass']} of {pa['n_pointers']} numbers in the generated replacement "
      f"text resolve to a JSON pointer in this file and match it. "
      f"Banned salvage tokens found: {pa['banned_salvage_tokens_found'] or 'none'}. "
      f"Assertion passed: **{pa['assertion_passed']}**.")
    A("")
    A("## R6 Corrections to the artifact plan (measured, not assumed)")
    A("")
    for c in doc["plan_corrections"]:
        A(f"* **{c['item']}** -- plan said: {c['plan_said'].rstrip('.')}; "
          f"measured: {c['measured'].rstrip('.')}.")
    A("")
    A("## R7 Manifest")
    A("")
    A("| step | status |")
    A("|---|---|")
    for k, v in doc["completion_manifest"].items():
        A(f"| {k} | {v} |")
    A("")
    return "\n".join(L) + "\n"


def write_results_md(doc: dict) -> dict:
    txt = render_results_md(doc)
    p = HERE / "RESULTS.md"
    p.write_text(txt)
    again = render_results_md(doc)
    return {"path": str(p), "bytes": len(txt),
            "regenerates_byte_identically": bool(again == txt)}
