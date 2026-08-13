#!/usr/bin/env python3
"""Iteration-3 evaluation artifact: redo the headline statistics the honest way.

Pure reanalysis over the frozen iteration-1/iteration-2 result trees.
No GPU, no model loading, no API calls, $0.00 spend.

Outputs
  eval_out.json                       (exp_eval_sol_out schema)
  out/member_table.csv, lineage_units.csv
  out/replacement_text.md             (generated FROM eval_out.json)
  out/appendix_corrections_of_record.md, out/main_text_stub.md
  figs/                               (regenerated from the JSON)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from loguru import logger

Path("logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

import eval_a1  # noqa: E402
import eval_a2  # noqa: E402
import eval_a34  # noqa: E402
import eval_a5  # noqa: E402
import eval_step0  # noqa: E402
from eval_common import OUT, WS, finite, manifest  # noqa: E402
from eval_step0 import reuse_manifest  # noqa: E402

from lib import stats_ext  # noqa: E402

LIMITATIONS = [
    "This is a pure reanalysis. Every number inherits the sampling design, the panel "
    "composition and the judge of the archived iteration-1/iteration-2 runs; nothing was "
    "re-measured, so no design flaw in those runs can be repaired here, only stated.",
    "The breadth-panel correlations are computed on 7 lineage units. At n=7 no confidence "
    "interval on a Spearman rho is informative in the usual sense; the leave-one-lineage-out "
    "jackknife, not the CI, is the load-bearing stability statistic, and it is reported in full.",
    "The pre-registered primary logistic alpha_50 is defined on 1 of 19 members and that member "
    "is itself auto-flagged UNRELIABLE, so every logistic correlation on the breadth panel is "
    "undefined by construction and the headline rests entirely on the non-parametric fallback.",
    "The sign orientation is a convention. It is stated explicitly and defended from the "
    "pre-registered direction of each score, and two orientation-free comparators (|rho| and "
    "predictive AUC) are reported so a reader who disputes it can still read the ordering; but "
    "the primary oriented statistic is convention-dependent by construction.",
    "The judged behavioural axes come from a scorer whose one-vs-rest REFUSAL kappa is 0.391 and "
    "whose PARTIAL kappa is 0.054. Measurement error in the outcome attenuates every correlation "
    "in Analysis 1 toward zero; the attenuation is stated, not corrected away, because this "
    "design cannot identify a reliability model.",
    "The layer-sensitivity sweep was archived for exactly one member (l1_instruct), so the "
    "logistic-vs-non-parametric span contrast and its misspecification diagnostic are "
    "single-member facts. The diagnostic runs over 4 comparable layer cells and is reported as "
    "INCONCLUSIVE rather than as an attribution.",
    "The AMS reproduction gate has n=3 checkpoints. The ordering criterion cannot reach a "
    "permutation p below 0.333, so its failure carries essentially no evidential weight; this is "
    "stated rather than used.",
    "The free-vs-forced asymmetry is measured on 15 of 19 members (the four without an archived "
    "survival arm are listed under not_recomputable), 5 lineages and 4 families, at a single "
    "perturbation size (eps = 0.5 NORM_L), a single injection step and a 16-step horizon. "
    "Nothing here establishes that the effect survives other geometries.",
    "61-88% of paired survival rollouts are EXACT ties because the perturbed free-running stream "
    "never diverged from the clean stream. Every paired test therefore conditions on divergence, "
    "and the unconditional free>forced fraction (0.11-0.35) must not be read as a direction.",
    "The refusal-lexicon covariate of the amplifying tail is NOT_RECOMPUTABLE: the survival arm "
    "archived deviation trajectories but not token streams. The tail characterisation is "
    "therefore missing the one covariate most directly about safety content.",
    "The tokens-diverged covariate that DOES associate with amplification is close to mechanical "
    "(a rollout that never diverges cannot amplify), so it is reported as evidence about "
    "autoregressive variance rather than about safety.",
    "The two-stage composite was never written to the archive and is RECONSTRUCTED here from its "
    "stated definition. The reconstruction is deterministic and its rule is printed, but it is "
    "not a verbatim recovery of whatever was computed at the time.",
    "The main-text reduction accounting matches paragraphs by marker strings against the "
    "iteration-2 paper source. It is a mechanical proxy for editorial judgement and will miss "
    "material that discusses a corrected claim without naming any of its numbers.",
    "Annotator truth in the judge audit comes from an LLM panel, not from humans, so every "
    "propagation number bounds agreement with that panel rather than with ground truth.",
    "No multiplicity correction is applied across the analyses in this artifact as a whole. Holm "
    "is applied within the 15-member asymmetry family only; the Analysis-1 correlations are "
    "reported with exhaustive permutation p values and their achievable floors instead.",
]


def build_replacement_text(results: dict) -> str:
    """Generate out/replacement_text.md FROM the results dict (never hand-typed)."""
    L = ["# Replacement text (generated from eval_out.json)", "",
         "Each entry gives the OLD sentence, the NEW sentence, and the JSON path of every "
         "number in the new sentence. Generated by `eval.py :: build_replacement_text`; do not "
         "hand-edit.", ""]
    so = results["sign_orientation"]
    h = so["oriented_headline_delta"]["plain_harmful_refusal"]
    cc = so["ceiling_check"]

    def block(n, title, old, new, paths):
        L.extend([f"## R{n}. {title}", "",
                  f"**OLD.** {old}", "", f"**NEW.** {new}", "",
                  "**Numbers.**", ""])
        L.extend([f"- `{p}` = {v}" for p, v in paths.items()])
        L.append("")

    block(1, "The metric-vs-baseline headline",
          "Against our AMS reimplementation the paired bootstrap over 7 lineages is a tie "
          "(Delta rho = -0.714, 95% CI [-1.765, 0.667]).",
          f"Computed on SIGN-ORIENTED correlations -- the direction each score's own validity "
          f"theory predicts -- the breadth-panel comparison against the judged plain-harmful "
          f"refusal rate gives oriented rho = {h['rho_a']:.3f} for alpha_50 and "
          f"{h['rho_b']:.3f} for our-AMS, a paired difference of {h['delta']:.3f} "
          f"(95% CI [{h['ci_delta'][0]:.3f}, {h['ci_delta'][1]:.3f}], n = {h['n']} lineages, "
          f"{h['n_boot_valid']} valid resamples). The archived raw statistic reproduces to three "
          f"decimals before orientation is applied.",
          {"results.sign_orientation.oriented_headline_delta.plain_harmful_refusal.rho_a": h["rho_a"],
           "results.sign_orientation.oriented_headline_delta.plain_harmful_refusal.rho_b": h["rho_b"],
           "results.sign_orientation.oriented_headline_delta.plain_harmful_refusal.delta": h["delta"],
           "results.sign_orientation.oriented_headline_delta.plain_harmful_refusal.ci_delta": h["ci_delta"],
           "results.sign_orientation.regression_check_raw_headline.reproduces_to_3dp":
               so["regression_check_raw_headline"]["reproduces_to_3dp"]})

    old_c = cc["old_raw_statistic"]
    new_c = cc["corrected_oriented_statistic"]
    block(2, "The ceiling check (why the old statistic could not reward a perfect metric)",
          "Delta rho = -0.714 [-1.765, 0.667], reported as a TIE.",
          f"The raw statistic could not have rewarded a perfect metric: holding our-AMS at its "
          f"measured rho = {old_c['rho_ams_raw']:.4f}, an alpha_50 with the theoretically ideal "
          f"rho = -1 would have produced Delta = {old_c['arithmetic']}, a large negative number "
          f"scored as a catastrophic loss. Under the corrected oriented statistic the same ideal "
          f"case gives Delta = {new_c['arithmetic']}, so the comparison can now reward it.",
          {"results.sign_orientation.ceiling_check.old_raw_statistic.delta_if_alpha50_were_PERFECT":
               old_c["delta_if_alpha50_were_PERFECT"],
           "results.sign_orientation.ceiling_check.corrected_oriented_statistic.delta_if_alpha50_were_PERFECT":
               new_c["delta_if_alpha50_were_PERFECT"]})

    ws = so["wrong_sign_claim"]
    block(3, "How strongly alpha_50's correlation is wrong-signed",
          "alpha_50's correlation with judged behaviour ranges -0.086 to 0.771 under "
          "leave-one-lineage-out, i.e. it is unstable.",
          f"Under its own validity theory alpha_50's oriented breadth-panel correlation should be "
          f"positive; it is {ws['rho_alpha50_oriented']:.3f}, with the lineage bootstrap placing "
          f"{ws['p_true_oriented_rho_below_0']:.3f} of its mass below zero and the "
          f"leave-one-lineage-out jackknife spanning "
          f"[{ws['jackknife_oriented_range'][0]:.3f}, {ws['jackknife_oriented_range'][1]:.3f}] "
          f"with {ws['n_jackknife_folds_oriented_negative']} of 7 folds wrong-signed. "
          f"{ws['statement'].split('. ', 1)[1]}",
          {"results.sign_orientation.wrong_sign_claim.p_true_oriented_rho_below_0":
               ws["p_true_oriented_rho_below_0"],
           "results.sign_orientation.wrong_sign_claim.jackknife_oriented_range":
               ws["jackknife_oriented_range"],
           "results.sign_orientation.wrong_sign_claim.claim_strength": ws["claim_strength"]})

    ofc = so["orientation_free_comparators"]
    am = ofc["auc"]["median_split"]
    block(4, "Orientation-free comparators",
          "(no previous sentence: the comparison was reported only as a signed rho difference)",
          f"The ordering does not depend on the sign convention. On |rho| the difference is "
          f"{ofc['abs_rho']['plain_harmful_refusal']['abs_delta']:.3f} "
          f"(95% CI [{ofc['abs_rho']['plain_harmful_refusal']['ci_abs_delta'][0]:.3f}, "
          f"{ofc['abs_rho']['plain_harmful_refusal']['ci_abs_delta'][1]:.3f}]); as a predictor of "
          f"a median-split binarised safety label our-AMS reaches AUC "
          f"{am['ams_sigma']['auc']:.3f} (jackknife "
          f"[{am['ams_sigma']['jackknife_range'][0]:.3f}, "
          f"{am['ams_sigma']['jackknife_range'][1]:.3f}]) against "
          f"{am['alpha_50_nonparametric']['auc']:.3f} (jackknife "
          f"[{am['alpha_50_nonparametric']['jackknife_range'][0]:.3f}, "
          f"{am['alpha_50_nonparametric']['jackknife_range'][1]:.3f}]) for alpha_50. "
          f"{ofc['ordering_agreement']['statement']} "
          f"{ofc['ordering_agreement']['interval_caveat']} "
          f"{ofc['ordering_agreement']['note_alpha50_auc_below_chance']}",
          {"results.sign_orientation.orientation_free_comparators.abs_rho.plain_harmful_refusal.abs_delta":
               ofc["abs_rho"]["plain_harmful_refusal"]["abs_delta"],
           "results.sign_orientation.orientation_free_comparators.auc.median_split.ams_sigma.auc":
               am["ams_sigma"]["auc"],
           "results.sign_orientation.orientation_free_comparators.auc.median_split.alpha_50_nonparametric.auc":
               am["alpha_50_nonparametric"]["auc"],
           "results.sign_orientation.orientation_free_comparators.ordering_agreement.all_agree":
               ofc["ordering_agreement"]["all_agree"]})

    sf = so["sign_flip_recount"]
    block(5, "The sign-flip recount",
          sf["old_sentence"], sf["new_sentence"],
          {"results.sign_orientation.sign_flip_recount.n_choices_enumerated": sf["n_choices_enumerated"],
           "results.sign_orientation.sign_flip_recount.n_right_signed": sf["n_right_signed"],
           "results.sign_orientation.sign_flip_recount.n_wrong_signed": sf["n_wrong_signed"]})

    dp = so["depth_panel"]
    block(6, "The depth panel",
          "Spearman(alpha_50, judge harmful refusal) = -0.257 (p = 0.62, n = 6).",
          f"On the powered depth panel the oriented correlation is "
          f"{dp['oriented_rho']:.3f} (raw {dp['raw_rho']:.3f}), the only right-signed estimate in "
          f"the study, with an exact permutation p of "
          f"{dp['exact_permutation_oriented']['p_permutation']:.3f} against an achievable floor of "
          f"{dp['exact_permutation_oriented']['p_min_achievable']:.5f} over "
          f"{dp['exact_permutation_oriented']['n_permutations']} orderings at n = {dp['n']}.",
          {"results.sign_orientation.depth_panel.oriented_rho": dp["oriented_rho"],
           "results.sign_orientation.depth_panel.exact_permutation_oriented.p_permutation":
               dp["exact_permutation_oriented"]["p_permutation"],
           "results.sign_orientation.depth_panel.exact_permutation_oriented.p_min_achievable":
               dp["exact_permutation_oriented"]["p_min_achievable"]})

    a = results["asymmetry"]
    s = a["cross_member_summary"]
    block(7, "The free-running vs teacher-forced asymmetry",
          a["retired_claims"]["stochastic_dominance"]["old"] + " "
          + a["retired_claims"]["deviation_grows"]["old"],
          f"In {s['n_members']} of {s['n_members']} members across {s['n_lineages']} lineages and "
          f"{s['n_families']} families the paired mean-difference CI excludes zero, but the effect "
          f"is a right-tail effect conditional on stream divergence, not stochastic dominance: "
          f"{s['frac_exact_ties_range'][0]:.0%}-{s['frac_exact_ties_range'][1]:.0%} of paired "
          f"rollouts are exact ties in which the perturbed free-running stream never diverged, "
          f"the forced channel strictly exceeds the free channel in only "
          f"{s['n_forced_gt_free_total']} of {s['n_members'] * 100} rollouts, and among rollouts "
          f"that do diverge the free channel is larger in "
          f"{s['frac_free_gt_forced_given_divergence_range'][0]:.0%}-"
          f"{s['frac_free_gt_forced_given_divergence_range'][1]:.0%}. The typical rollout DECAYS "
          f"in both channels (median free {s['median_free_range'][0]:.2f}-"
          f"{s['median_free_range'][1]:.2f}, median forced {s['median_forced_range'][0]:.2f}-"
          f"{s['median_forced_range'][1]:.2f}), while the free channel's 95th percentile exceeds "
          f"the forced channel's in {s['n_members_q95_free_exceeds_forced']}/{s['n_members']} "
          f"members. Exact sign tests and Wilcoxon signed-rank tests are significant after Holm "
          f"in {s['n_sign_test_sig_holm']}/{s['n_members']} and "
          f"{s['n_wilcoxon_sig_holm']}/{s['n_members']} members respectively, all favouring the "
          f"free channel among untied pairs; Cliff's delta ranges "
          f"{s['cliffs_delta_range'][0]:.3f}-{s['cliffs_delta_range'][1]:.3f}.",
          {"results.asymmetry.cross_member_summary.n_mean_diff_ci_excludes_0": s["n_mean_diff_ci_excludes_0"],
           "results.asymmetry.cross_member_summary.frac_exact_ties_range": s["frac_exact_ties_range"],
           "results.asymmetry.cross_member_summary.frac_free_gt_forced_given_divergence_range":
               s["frac_free_gt_forced_given_divergence_range"],
           "results.asymmetry.cross_member_summary.median_free_range": s["median_free_range"],
           "results.asymmetry.cross_member_summary.median_forced_range": s["median_forced_range"],
           "results.asymmetry.cross_member_summary.n_sign_test_sig_holm": s["n_sign_test_sig_holm"]})

    t = results["tail_characterisation"]
    block(8, "What the amplifying tail is made of",
          "(no previous sentence: the tail was reported but never characterised)",
          f"Labelling a rollout amplifying when its free-running deviation ratio exceeds 1 "
          f"({t['n_amplifying_primary']} of {t['n_rollouts_total']} rollouts, "
          f"{t['amplification_rate_primary']:.1%}; "
          f"{t['amplification_rate_sensitivity']:.1%} under the sensitivity rule), amplification "
          f"is not associated with prompt identity (chi-square "
          f"{t['covariate_prompt_identity']['chi2']:.1f} on "
          f"{t['covariate_prompt_identity']['dof']} df, p = "
          f"{t['covariate_prompt_identity']['p']:.3f}, Cramer's V "
          f"{t['covariate_prompt_identity']['cramers_v']:.3f}) nor with the member's own judged "
          f"plain-harmful refusal rate (Spearman "
          f"{t['covariate_member_refusal_rate']['spearman_rho']:.3f}, lineage-bootstrap 95% CI "
          f"[{t['covariate_member_refusal_rate']['ci_lineage_bootstrap'][0]:.3f}, "
          f"{t['covariate_member_refusal_rate']['ci_lineage_bootstrap'][1]:.3f}], "
          f"n = {t['covariate_member_refusal_rate']['n_members']} members). {t['verdict']}",
          {"results.tail_characterisation.amplification_rate_primary": t["amplification_rate_primary"],
           "results.tail_characterisation.covariate_prompt_identity.p": t["covariate_prompt_identity"]["p"],
           "results.tail_characterisation.covariate_member_refusal_rate.spearman_rho":
               t["covariate_member_refusal_rate"]["spearman_rho"],
           "results.tail_characterisation.covariate_refusal_lexicon.status":
               t["covariate_refusal_lexicon"]["status"],
           "results.tail_characterisation.verdict": t["verdict"]})

    c = results["composite"]
    ph = c["oriented_correlations"]["plain_harmful_refusal"]
    block(9, "The deployment composite",
          "We propose a two-stage triage score: a reachability gate, then alpha_50 among the "
          "models that pass.",
          f"The composite is reported as a closed loop, not as a working product. Its oriented "
          f"correlation with the judged plain-harmful refusal rate is "
          f"{ph['composite']['rho_oriented']:.3f} against "
          f"{ph['component_alpha_50_nonparametric']['rho_oriented']:.3f} for its alpha_50 "
          f"component and {ph['component_our_AMS']['rho_oriented']:.3f} for our-AMS, so "
          f"composition has "
          + {"NO_EFFECT": "no effect", "HELPED": "a positive effect",
             "HURT": "a negative effect"}[c["did_composition_help"]]
          + ". On the 6-checkpoint depth panel where the composite was actually archived, its "
          f"oriented correlation with the judged harmful-refusal rate is "
          f"{c['archived_depth_panel']['oriented_correlations']['judge_harmful_refusal']['composite_rho_oriented']:.3f}, "
          f"identical to its alpha_50 component because all "
          f"{c['archived_depth_panel']['n_stage_1_pass']} of "
          f"{c['archived_depth_panel']['n']} checkpoints pass the gate, so the gate contributes "
          f"nothing. {c['stage_1_withdrawn_at_power']['statement']}",
          {"results.composite.oriented_correlations.plain_harmful_refusal.composite.rho_oriented":
               ph["composite"]["rho_oriented"],
           "results.composite.did_composition_help": c["did_composition_help"],
           "results.composite.stage_1_withdrawn_at_power.gate_vs_class_agreement":
               c["stage_1_withdrawn_at_power"]["gate_vs_class_agreement"]})

    acc = results["accounting"]
    block(10, "Panel accounting",
          "19 measured members, 17 analysed, 1 with a defined primary estimate.",
          acc["one_sentence_for_the_paper"] + " " + acc["sharpest_fact"]
          + (" " + acc["discrepancy"] if acc["discrepancy"] else ""),
          {"results.accounting.derived_triple": acc["derived_triple"],
           "results.accounting.n_unreliable_excluded": acc["n_unreliable_excluded"],
           "results.accounting.n_defined_logistic_after_exclusion":
               acc["n_defined_logistic_after_exclusion"]})

    ams = results["ams_reproduction"]
    block(11, "The AMS reproduction gate",
          "Our AMS reimplementation fails the Table-I reproduction gate, so the label 'our AMS "
          "reimplementation' is used everywhere.",
          ams["replacement_sentence"] + " " + ams["llama_1b_note"]["statement"],
          {"results.ams_reproduction.n_cells_within_25pct": ams["n_cells_within_25pct"],
           "results.ams_reproduction.per_checkpoint_criteria.n_verdict_measured_PASS":
               ams["per_checkpoint_criteria"]["n_verdict_measured_PASS"],
           "results.ams_reproduction.ordering_test_is_vacuous_at_n3.p_min_achievable":
               ams["ordering_test_is_vacuous_at_n3"]["p_min_achievable"]})

    ls = results["layer_sensitivity"]
    block(12, "Layer sensitivity",
          ls["headline_replacement"]["old"],
          ls["headline_replacement"]["new"] + " "
          + ls["misspecification_diagnostic"]["attribution_statement"] + " "
          + ls["coverage_caveat"] + ".",
          {"results.layer_sensitivity.per_member.l1_instruct.nonparametric_fold":
               ls["per_member"]["l1_instruct"]["nonparametric_fold"],
           "results.layer_sensitivity.per_member.l1_instruct.logistic_fold":
               ls["per_member"]["l1_instruct"]["logistic_fold"],
           "results.layer_sensitivity.misspecification_diagnostic.spearman_abs_gap_vs_non_monotonicity":
               ls["misspecification_diagnostic"]["spearman_abs_gap_vs_non_monotonicity"]})

    jp = results["judge_propagation"]
    pj = jp["propagation"]["abliterated_jailbreak_ASR"]
    pp = jp["propagation"]["abliterated_plain_harmful_refusal_rate"]
    block(13, "Judge propagation and the attenuation caveat",
          "The judge repair moved abliterated plain-harmful refusal 0.700 -> 0.113 and jailbreak "
          "ASR 0.092 -> 0.858.",
          f"Against blind annotator truth the jailbreak ASR revision STANDS (truth "
          f"{pj['archived_truth']:.3f}, Wilson 95% "
          f"[{pj['recomputed_wilson'][0]:.3f}, {pj['recomputed_wilson'][1]:.3f}], "
          f"k = {pj['recovered_k']}/{pj['recovered_n']}), while the plain-harmful refusal revision "
          f"must be RESTATED (truth {pp['archived_truth']:.3f}, Wilson 95% "
          f"[{pp['recomputed_wilson'][0]:.3f}, {pp['recomputed_wilson'][1]:.3f}], "
          f"k = {pp['recovered_k']}/{pp['recovered_n']}): the repaired judge still over-states it. "
          f"Pooled COMPLIANCE recall of the three un-framed safety arms is "
          f"{jp['pooled_compliance_recall']['k']}/{jp['pooled_compliance_recall']['n']} = "
          f"{jp['pooled_compliance_recall']['recall']:.3f} "
          f"[{jp['pooled_compliance_recall']['wilson_ci'][0]:.3f}, "
          f"{jp['pooled_compliance_recall']['wilson_ci'][1]:.3f}]. "
          f"{jp['attenuation_caveat']['statement']}",
          {"results.judge_propagation.propagation.abliterated_jailbreak_ASR.recomputed_wilson":
               pj["recomputed_wilson"],
           "results.judge_propagation.propagation.abliterated_plain_harmful_refusal_rate.recomputed_wilson":
               pp["recomputed_wilson"],
           "results.judge_propagation.pooled_compliance_recall.recall":
               jp["pooled_compliance_recall"]["recall"],
           "results.judge_propagation.attenuation_caveat.refusal_kappa":
               jp["attenuation_caveat"]["refusal_kappa"]})

    ra = results["corrections_of_record"]["reduction_accounting"]
    block(14, "Corrections of record (main-text stub)",
          "(corrections were stated inline across the results sections)",
          Path(OUT / "main_text_stub.md").read_text().split("\n\n", 1)[1].strip()
          + f" Moving the marker-matched material out of the main text removes "
            f"{ra['net_words_removed_from_main_text']} words of "
            f"{ra['main_text_total_words']} "
            f"({ra['achieved_reduction_vs_whole_main_text']:.1%} against a 15-20% target).",
          {"results.corrections_of_record.reduction_accounting.net_words_removed_from_main_text":
               ra["net_words_removed_from_main_text"],
           "results.corrections_of_record.reduction_accounting.achieved_reduction_vs_whole_main_text":
               ra["achieved_reduction_vs_whole_main_text"],
           "results.corrections_of_record.reduction_accounting.target_met": ra["target_met"]})
    return "\n".join(L)


def metrics_agg(results: dict) -> dict:
    so = results["sign_orientation"]
    h = so["oriented_headline_delta"]["plain_harmful_refusal"]
    s = results["asymmetry"]["cross_member_summary"]
    t = results["tail_characterisation"]
    ams = results["ams_reproduction"]
    ls = results["layer_sensitivity"]["per_member"]["l1_instruct"]
    jp = results["judge_propagation"]
    acc = results["accounting"]
    am = so["orientation_free_comparators"]["auc"]["median_split"]
    return {
        "oriented_rho_alpha50_vs_plain_harmful_refusal": h["rho_a"],
        "oriented_rho_ourAMS_vs_plain_harmful_refusal": h["rho_b"],
        "oriented_delta_alpha50_minus_ourAMS": h["delta"],
        "oriented_delta_ci_low": h["ci_delta"][0],
        "oriented_delta_ci_high": h["ci_delta"][1],
        "raw_delta_archived_reproduced": so["regression_check_raw_headline"]["recomputed"]["delta"],
        "ceiling_old_statistic_delta_for_perfect_alpha50":
            so["ceiling_check"]["old_raw_statistic"]["delta_if_alpha50_were_PERFECT"],
        "ceiling_oriented_statistic_delta_for_perfect_alpha50":
            so["ceiling_check"]["corrected_oriented_statistic"]["delta_if_alpha50_were_PERFECT"],
        "p_oriented_rho_alpha50_below_zero": so["wrong_sign_claim"]["p_true_oriented_rho_below_0"],
        "jackknife_oriented_rho_alpha50_min": so["wrong_sign_claim"]["jackknife_oriented_range"][0],
        "jackknife_oriented_rho_alpha50_max": so["wrong_sign_claim"]["jackknife_oriented_range"][1],
        "jackknife_oriented_rho_ourAMS_min": h["jackknife_rho_b_range"][0],
        "jackknife_oriented_rho_ourAMS_max": h["jackknife_rho_b_range"][1],
        "auc_ourAMS_median_split": am["ams_sigma"]["auc"],
        "auc_alpha50_median_split": am["alpha_50_nonparametric"]["auc"],
        "n_lineage_units": h["n"],
        "n_sign_flip_choices_wrong_signed": so["sign_flip_recount"]["n_wrong_signed"],
        "depth_panel_oriented_rho": so["depth_panel"]["oriented_rho"],
        "n_members_with_per_rollout_survival": results["asymmetry"]["n_members_with_per_rollout_data"],
        "n_members_mean_diff_ci_excludes_zero": s["n_mean_diff_ci_excludes_0"],
        "n_members_q95_free_exceeds_forced": s["n_members_q95_free_exceeds_forced"],
        "n_members_median_decays_both_channels": s["n_members_median_below_1_both_channels"],
        "frac_exact_ties_min": s["frac_exact_ties_range"][0],
        "frac_exact_ties_max": s["frac_exact_ties_range"][1],
        "amplification_rate_primary": t["amplification_rate_primary"],
        "tail_prompt_chi2_p": t["covariate_prompt_identity"]["p"],
        "tail_member_refusal_spearman": t["covariate_member_refusal_rate"]["spearman_rho"],
        "n_members_measured": acc["n_measured"],
        "n_members_unreliable_excluded": acc["n_unreliable_excluded"],
        "n_members_defined_logistic_alpha50": acc["n_with_defined_preregistered_logistic_alpha_50"],
        "n_members_defined_logistic_after_exclusion": acc["n_defined_logistic_after_exclusion"],
        "ams_cells_within_25pct": ams["n_cells_within_25pct"],
        "ams_checkpoints_verdict_pass": ams["per_checkpoint_criteria"]["n_verdict_measured_PASS"],
        "ams_ordering_permutation_floor": ams["ordering_test_is_vacuous_at_n3"]["p_min_achievable"],
        "layer_span_fold_logistic": ls["logistic_fold"],
        "layer_span_fold_nonparametric": ls["nonparametric_fold"],
        "judge_pooled_compliance_recall": jp["pooled_compliance_recall"]["recall"],
        "judge_refusal_kappa": jp["attenuation_caveat"]["refusal_kappa"],
        "main_text_reduction_fraction":
            results["corrections_of_record"]["reduction_accounting"][
                "achieved_reduction_vs_whole_main_text"],
        "cost_usd": 0.0,
    }


def datasets_block(results: dict, members: list[dict]) -> list[dict]:
    """Per-unit rows in the schema's examples format."""
    so = results["sign_orientation"]
    ex_members = []
    comp = {p["member_id"]: p for p in results["composite"]["per_member"]}
    asym = results["asymmetry"]["per_member"]
    for m in members:
        c = comp[m["member_id"]]
        a = asym.get(m["member_id"])
        row = {
            "input": (f"member {m['member_id']} ({m['repo']}, lineage {m['lineage']}, "
                      f"class {m['class']}, family {m['family']})"),
            "output": (f"judged plain-harmful refusal rate {m['plain_harmful_refusal']:.4f}, "
                       f"jailbreak ASR {m['jailbreak_asr']:.4f}, XSTest over-refusal "
                       f"{m['xstest_over_refusal']:.4f}"),
            "predict_alpha_50_nonparametric": ("undefined" if m["alpha_50_nonparametric"] is None
                                               else f"{m['alpha_50_nonparametric']:.6f}"),
            "predict_alpha_50_logistic": ("undefined" if m["alpha_50_logistic_guarded"] is None
                                          else f"{m['alpha_50_logistic_guarded']:.6f}"),
            "predict_our_ams_sigma": f"{m['ams_sigma']:.6f}",
            "predict_max_refusal_rate": f"{m['max_refusal_rate']:.6f}",
            "predict_composite_two_stage": f"{c['composite']:.6f}",
            "metadata_lineage": m["lineage"],
            "metadata_class": m["class"],
            "metadata_family": m["family"],
            "metadata_unreliable": m["unreliable"],
            "metadata_exclusion_reason": m["exclusion_reason"] or "retained",
            "metadata_alpha_50_logistic_status": m["alpha_50_logistic_status"],
            "metadata_stage_1_pass": c["stage_1_pass"],
            "eval_plain_harmful_refusal": m["plain_harmful_refusal"],
            "eval_jailbreak_asr": m["jailbreak_asr"],
            "eval_xstest_over_refusal": m["xstest_over_refusal"],
            "eval_degenerate_rate": m["degenerate_rate"],
            "eval_ams_sigma": m["ams_sigma"],
            "eval_max_refusal_rate": m["max_refusal_rate"],
            "eval_n_survival_rollouts": m["n_survival_rollouts"],
        }
        if a:
            row["eval_free_minus_forced_mean_diff"] = a["mean_diff"]["mean_diff"]
            row["eval_free_minus_forced_q95_delta"] = a["quantile_deltas"]["q95"]["delta"]
            row["eval_frac_exact_ties"] = a["paired_tests"]["frac_exact_ties"]
            row["eval_cliffs_delta_free_vs_forced"] = a["paired_tests"]["cliffs_delta"]
        ex_members.append(row)

    ex_lin = []
    for u in results["composite"]["lineage_units"]:
        lin = u["lineage"]
        ex_lin.append({
            "input": f"lineage {lin} (breadth-panel resampling unit)",
            "output": (f"judged plain-harmful refusal rate {u['plain_harmful_refusal']:.4f}"),
            "predict_alpha_50_nonparametric": f"{u['alpha_50_nonparametric']:.6f}",
            "predict_our_ams_sigma": f"{u['ams_sigma']:.6f}",
            "predict_composite_two_stage": f"{u['composite']:.6f}",
            "metadata_lineage": lin,
            "eval_plain_harmful_refusal": u["plain_harmful_refusal"],
            "eval_jailbreak_asr": u["jailbreak_asr"],
            "eval_xstest_over_refusal": u["xstest_over_refusal"],
            "eval_alpha_50_nonparametric": u["alpha_50_nonparametric"],
            "eval_ams_sigma": u["ams_sigma"],
            "eval_composite": u["composite"],
        })

    ex_ams = []
    for row in results["ams_reproduction"]["table_3x4"]:
        ex_ams.append({
            "input": f"AMS reproduction checkpoint {row['checkpoint']} ({row['repo']})",
            "output": f"published Table-I sigma {row['published']}",
            "predict_measured_depth_band": f"{row['measured']:.6f}",
            "predict_measured_harmful_only": f"{row['measured_harmful_only']:.6f}",
            "predict_measured_worst_concept": f"{row['measured_worst_concept']:.6f}",
            "predict_measured_best_layer": f"{row['measured_max']:.6f}",
            "metadata_dtype": row["dtype"],
            "metadata_verdict_measured": row["verdict_measured"],
            "eval_published": row["published"],
            "eval_relative_error_depth_band": row["measured_relative_error"],
            "eval_relative_error_harmful_only": row["measured_harmful_only_relative_error"],
            "eval_relative_error_worst_concept": row["measured_worst_concept_relative_error"],
            "eval_relative_error_best_layer": row["measured_max_relative_error"],
        })

    return [
        {"dataset": "breadth_panel_members_19", "examples": ex_members},
        {"dataset": "breadth_panel_lineage_units_7", "examples": ex_lin},
        {"dataset": "ams_reproduction_gate_3x4", "examples": ex_ams},
    ]


@logger.catch(reraise=True)
def main():
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    logger.info("STEP 0: freeze, inventory, member table")
    members, units = eval_step0.main()

    logger.info("ANALYSIS 1: sign-oriented comparison")
    a1 = eval_a1.run(units, members)

    logger.info("ANALYSIS 4: accounting, AMS, layer sensitivity, judge propagation")
    acc = eval_a34.accounting(members)
    ams = eval_a34.ams_reproduction()
    lay = eval_a34.layer_sensitivity()
    jud = eval_a34.judge_propagation(members)

    logger.info("ANALYSIS 2: asymmetry + tail characterisation")
    asym, tail = eval_a2.run(members)

    logger.info("ANALYSIS 3: the two-stage composite")
    comp = eval_a34.composite(members, units)

    results = {
        "sign_orientation": a1,
        "asymmetry": asym,
        "tail_characterisation": tail,
        "composite": comp,
        "accounting": acc,
        "ams_reproduction": ams,
        "layer_sensitivity": lay,
        "judge_propagation": jud,
    }

    logger.info("ANALYSIS 5: corrections of record")
    results["corrections_of_record"] = eval_a5.build(results)

    not_recomputable = [
        {"item": "refusal-lexicon content of the diverged free-running stream "
                 "(Analysis 2d covariate ii)",
         "reason": tail["covariate_refusal_lexicon"]["reason"]},
        {"item": "per-rollout survival data for l5_base, l5_instruct, l7_base, l7_instruct",
         "reason": "no survival arm was archived for these 4 of 19 members; the D4 ratchet arm "
                   "covered 15 members over 5 lineages. Not regenerated."},
        {"item": "E2/method_out.json :: metadata.composite (the key the plan pointed at)",
         "reason": "that key does not exist. The archived composite is at E1/method_out.json :: "
                   "metadata.composite and covers the 6-checkpoint DEPTH panel; it is reported "
                   "verbatim in results.composite.archived_depth_panel. Its extension to the "
                   "19-member breadth panel is a RECONSTRUCTION from the same two-stage rule, "
                   "labelled as such, not a recovery of an archived number."},
        {"item": "2-parameter and 4-parameter logistic alpha_50 per breadth-panel member",
         "reason": "the breadth panel fitted the 2-parameter logistic (reported here as "
                   "alpha_50_logistic, with its range guard) and the non-parametric estimator "
                   "only. The 4-parameter fit exists in the iteration-2 DEPTH panel (E1) and was "
                   "never run per member on the breadth panel, so the member table carries three "
                   "estimator columns rather than four."},
        {"item": "layer-sensitivity spans for the other 18 members",
         "reason": "E2/results/layersens_*.json exists for l1_instruct only."},
        {"item": "refusal-direction cosine for members other than the H4 case study",
         "reason": "only the H4 case-study member has an archived cosine to its parent; the "
                   "column is emitted as null elsewhere rather than imputed."},
        {"item": "a corrected (disattenuated) version of the Analysis-1 correlations",
         "reason": "correcting for the judge's REFUSAL kappa of 0.391 would require a "
                   "reliability model this design cannot identify; the attenuation is stated "
                   "instead."},
    ]

    out = {
        "metadata": {
            "evaluation_name": "iteration_3_honest_restatement",
            "description": ("Zero-GPU, zero-API reanalysis of the frozen iteration-1/2 result "
                            "trees: sign-oriented metric-vs-baseline comparison with a ceiling "
                            "check and orientation-free comparators; the free-vs-forced "
                            "asymmetry restated at the strength the per-rollout data carry, with "
                            "a tail characterisation; the two-stage composite reported as a "
                            "closed loop; panel accounting, per-checkpoint AMS reproduction, "
                            "dual-estimator layer sensitivity and judge-propagation "
                            "attenuation; and a corrections-of-record appendix."),
            "inputs_manifest": manifest(),
            "reuse_manifest": reuse_manifest(),
            "orientation_convention": a1["orientation_convention"],
            "seeds": {"lineage_bootstrap_seed": int(stats_ext.BOOT_SEED),
                      "rollout_bootstrap_seed": int(stats_ext.BOOT_SEED),
                      "cliffs_delta_seed": 12345,
                      "n_boot_lineage": 5000, "n_boot_rollout": 2000},
            "runtime_seconds": None,
            "cost_usd": 0.0,
            "compute": "CPU only; no GPU requested, no model loaded, no API call made",
            "results": results,
            "limitations": LIMITATIONS,
            "not_recomputable": not_recomputable,
        },
        "metrics_agg": metrics_agg(results),
        "datasets": datasets_block(results, members),
    }
    out["metadata"]["runtime_seconds"] = round(time.time() - t0, 2)
    out = finite(out)

    (OUT / "replacement_text.md").write_text(build_replacement_text(results))
    Path("eval_out.json").write_text(json.dumps(out, indent=1))
    logger.info(f"wrote eval_out.json ({Path('eval_out.json').stat().st_size / 1e6:.2f} MB) "
                f"in {out['metadata']['runtime_seconds']}s")
    return out


if __name__ == "__main__":
    main()
