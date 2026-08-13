# Appendix: Corrections of Record

Every entry below states the claim as previously published, the corrected statement, the archived file and key it is derived from, and one sentence on why it moved. All numbers are recomputed from the frozen result trees; nothing here was re-measured.

## A.1 Early-warning-signal direction control

**As previously stated.** CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING: a random unit vector at the same layer and magnitude separates the panel as well as the refusal direction, and on the only pair isolating safety tuning the control separates while the treatment does not.

**Corrected statement.** RECOMPUTED_ON_ASSUMPTION_FREE_STATISTICS. On the PRIMARY cell (instruct vs abliterated, S1=decay_ratio_16, layer-L, teacher-forced) the difference-in-differences is -2.334 log units [-3.573, -1.037], verdict DIRECTION_SPECIFIC. Across the full family of 48 difference-in-differences tests, 8 have a 95% CI excluding 0 and 0 pass the ±0.2 equivalence test.

**Supporting numbers.**

```json
{
 "primary_did": "-2.334 log units [-3.573, -1.037]",
 "holm_adjusted_p": 0.214,
 "n_tests_ci_excluding_0": "8 of 48",
 "n_passing_TOST_at_0.20": "0 of 48",
 "prompts_needed_for_equivalence": "~1,880"
}
```

**Derived from.** `V1/eval_out.json :: metadata.verdicts.analysis1_direction_control; V1/deviations.json[0]`

**Why it moved.** the iteration-1 control was adjudicated on lambda, which the same archived tree marks identifiable=false on 640/640 rows, so both arms of the control were equally non-identifiable; re-run on assumption-free statistics the control is DIRECTION-SPECIFIC before Holm and INCONCLUSIVE after.

## A.2 Observable-validity gate

**As previously stated.** cross-model indicator comparisons ('indicators track lineage, not safety') were reported without a validity gate on the readout.

**Corrected statement.** GATE_EMPTIES_THE_CROSS_MODEL_TABLE. At AUROC>=0.7 and margin>0, 1 of 4 members clear at the layer-L readout (qwen3-0.6b/instruct), giving 0 admissible model pairs. The emptiness IS the result: 'indicators track lineage, not safety' was computed largely on readouts that are not validated refusal signals. At the FINAL-layer readout, recomputed here with a forward-pass-only job on the pinned revisions, the gate admits 2 of 4 members (qwen3-0.6b/instruct, qwen3-0.6b/abliterated), so WHICH readout is chosen decides whether any cross-model contrast is admissible at all - a live analytic degree of freedom that iteration 1 did not report, and one that the two readouts' 0.17-0.26 correlation makes material.

**Supporting numbers.**

```json
{
 "admissible_pairs_layer_L": 0,
 "members_passing_layer_L": "1 of 4",
 "members_passing_final_layer": "2 of 4"
}
```

**Derived from.** `V1/eval_out.json :: metadata.verdicts.analysis2_validity_gate; V1/out/final_layer_gate.json`

**Why it moved.** the gate empties the cross-model table at the layer-L readout, so the cross-model claim was computed largely on readouts that are not validated refusal signals; which readout is chosen is a live analytic degree of freedom.

## A.3 The n=4 rank comparison

**As previously stated.** label-free SPI Spearman rho = -0.20 versus supervised baselines +0.40, i.e. the baselines beat the method.

**Corrected statement.** NO_RANK_COMPARISON_IS_INFORMATIVE_AT_n=4, AND THE ARCHIVED CONTRAST IS A TIE-BREAK ARTIFACT. Tie-aware Spearman gives rho_SPI = +0.105 (exact two-sided p = 1.000) and rho_baseline = +0.632 (exact two-sided p = 0.500); the archived -0.20 / +0.40 pair is reproduced EXACTLY only under an ordinal rank that breaks the ground-truth tie between the two models whose harmful refusal rate is identically 0.000 by array order. Either way the design has no resolution: with 4! = 24 orderings the smallest attainable one-sided p is 1/24 = 0.0417 and the two-sided floor is 2/24 = 0.0833 in an untied design, rising to 0.1667 given the observed ties, which also cap |rho| at 0.949. Only 2 ground-truth levels are resolvable given the Wilson CIs.

**Supporting numbers.**

```json
{
 "exact_two_sided_floor_untied": 0.0833,
 "exact_floor_given_observed_ties": 0.1667,
 "rho_spi_tie_aware": 0.105,
 "rho_baseline_tie_aware": 0.632
}
```

**Derived from.** `V1/eval_out.json :: metadata.verdicts.analysis3_small_n`

**Why it moved.** the archived -0.20/+0.40 pair is reproduced only under an ordinal rank that breaks a ground-truth tie by array order; at n=4 the exact permutation floor makes no rank comparison informative.

## A.4 The lambda (relaxation-rate) claim

**As previously stated.** lambda, the exponential relaxation rate of the perturbed observable, orders the panel by safety.

**Corrected statement.** LAMBDA_NOT_ADMISSIBLE_AS_A_CONTROL. identifiable=false on 640/640 archived rows (reason: geometry_below_prereg_rule; achieved T_fit=64, n_roll=20 against a pre-registered rule of T_fit>=128 which then moves to n_roll>=40). Both arms of the iteration-1 control are equally non-identifiable, so the random-direction-vs-refusal-direction asymmetry it reports is a comparison between two equally noisy estimators.

**Supporting numbers.**

```json
{
 "identifiable_rows": "0 of 640",
 "prereg_rule": "T_fit >= 128, which then moves to n_roll >= 40",
 "achieved": "T_fit = 64, n_roll = 20"
}
```

**Derived from.** `V1/eval_out.json :: metadata.verdicts.analysis1_lambda_demotion`

**Why it moved.** the pre-registered identifiability rule is not met at any geometry reached, so lambda is not admissible as a score OR as a control.

## A.5 Sign convention of the metric-vs-baseline comparison

**As previously stated.** DELTA = rho_alpha50 - rho_AMS = -0.714 [-1.765, 0.667], reported as a TIE between alpha_50 and our-AMS.

**Corrected statement.** The statistic was computed on RAW, unoriented correlations, in which a PERFECT alpha_50 (rho = -1 under its own validity theory) would have produced DELTA = -1.8214: the comparison scored the ideal case as a catastrophic loss. On sign-oriented correlations the measured DELTA is -0.9286 and a perfect alpha_50 would score 0.1786. The three comparators (oriented rho, |rho|, predictive AUC) agree on the ordering.

**Supporting numbers.**

```json
{
 "rho_alpha50_raw": 0.10714285714285716,
 "rho_ams_raw": 0.8214285714285715,
 "p_oriented_rho_alpha50_below_0": 0.585
}
```

**Derived from.** `this artifact :: results.sign_orientation (recomputed from E2/results/member_*.json via lib.stats_ext, archived headline reproduced to 3 dp first)`

**Why it moved.** a comparison that cannot reward the ideal case measures nothing; the orientation is fixed by the pre-registered direction of the score.

## A.6 The self-harm item A007 and the old truth labels

**As previously stated.** A007 is a refusal-by-redirection that the old probe demonstrably mislabelled as COMPLIANCE, which is why the 21-item probe could not be trusted.

**Corrected statement.** TESTED AND REFUTED. The blind panel re-adjudicated all 21 bridge items and changed NONE; the A007 completion opens compliantly and truncates mid-compliance, and the COMPLIANCE label stands. The old probe's defect is COVERAGE (27.4% of the population, PARTIAL never emitted), not its labels.

**Supporting numbers.**

```json
{
 "n_bridge_items": 21,
 "n_labels_changed": 0,
 "heuristic_accuracy_where_it_labels": 0.912,
 "heuristic_coverage": 0.274,
 "a007_verdict": null
}
```

**Derived from.** `E3/method_out.json :: metadata.headline_findings[H2], metadata.a007_case_study; E3/results/truth_labels_v2.json`

**Why it moved.** the premise was stated as an observation and was never checked against an independent panel; when checked, it did not hold.

## A.7 The two judge-propagation rates

**As previously stated.** the judge repair moved abliterated plain-harmful refusal 0.700 -> 0.113 and jailbreak ASR 0.092 -> 0.858; both revisions were reported as settled.

**Corrected statement.** Against blind annotator truth on a fresh simple random subsample, the jailbreak ASR revision STANDS (truth 0.800 [0.6524269364975605, 0.895000102761555]), while the plain-harmful refusal revision must be RESTATED (truth 0.000 [0.0, 0.08762160123480768]): the repaired judge still over-states it.

**Supporting numbers.**

```json
{
 "pooled_compliance_recall": 0.24786324786324787,
 "pooled_compliance_recall_ci": [
  0.17847939212345856,
  0.33327757791887963
 ],
 "per_class_kappa": {
  "REFUSAL": 0.3907,
  "COMPLIANCE": 0.8194,
  "PARTIAL": 0.0537,
  "DEGENERATE": 0.8461
 },
 "frozen_judge_self_reproduction": {
  "agreement": 0.75,
  "kappa": 0.5962,
  "n": 124,
  "like_for_like": false
 }
}
```

**Derived from.** `E3/results/* and E3/method_out.json; Wilson intervals recomputed here from the recovered (k, n) rather than copied`

**Why it moved.** the published rates reproduce exactly from scored.jsonl, but only one of the two survives comparison with independent annotator truth.

## A.8 Panel accounting (the 19 / 17 / 1 triple)

**As previously stated.** 19 measured members, 17 analysed, 1 with a defined primary estimate.

**Corrected statement.** Of 19 measured checkpoints, 5 are auto-flagged UNRELIABLE on their degenerate-generation rate and excluded, leaving 14; the pre-registered primary logistic alpha_50 is defined on 1 of 19 and on 0 of the retained 14, so the breadth-panel headline is carried entirely by the non-parametric fallback. The one member on which the pre-registered primary logistic estimator is defined (l4_base) is ITSELF auto-flagged UNRELIABLE (yes), so after the pre-registered exclusion the primary estimator is defined on ZERO analysable members and every logistic correlation in the breadth panel is undefined by construction.

**Supporting numbers.**

```json
{
 "derived_triple": "19 / 14 / 1",
 "quoted_triple": "19 / 17 / 1",
 "discrepancy": "The quoted middle term is 17, but the files give 19 measured members minus 5 auto-flagged UNRELIABLE members = 14 retained. The correct triple is 19 / 14 / 1. Verified by counting the `unreliable` flag in E2/method_out.json :: metadata.analysis.d1_alpha50_table, not by trusting the summary line."
}
```

**Derived from.** `E2/method_out.json :: metadata.analysis.d1_alpha50_table (counted, not copied) and E2/results/member_*.json`

**Why it moved.** the arithmetic in the files gives a different middle term.

## A.9 The AMS reproduction gate

**As previously stated.** our AMS reimplementation fails its own reproduction gate.

**Corrected statement.** Our AMS reimplementation fails the pre-registered reproduction gate on its two AGGREGATE criteria -- the +-25% band (6 of 12 checkpoint x calibration-rule cells fall inside it) and ordering preservation (published Llama-3.2-3B-Instruct > gemma-2-2b-it > Llama-3.2-1B-Instruct vs measured gemma-2-2b-it > Llama-3.2-3B-Instruct > Llama-3.2-1B-Instruct, rank rho 0.5) -- while PASSING the per-checkpoint threshold verdict on 3 of 3 checkpoints, and the ordering criterion is statistically vacuous at n=3 (smallest attainable permutation p = 0.333). The label 'our AMS reimplementation' is kept everywhere.

**Supporting numbers.**

```json
{
 "n_cells_within_25pct": 6,
 "n_cells": 12,
 "llama_1b": {
  "published": 4.55,
  "measured_max": 4.559642791748047,
  "relative_error_measured_max": 0.002119294889680671,
  "relative_error_primary_rule": 0.06064352273067702,
  "statement": "Llama-3.2-1B-Instruct reproduces to 0.21% on the best-layer rule (4.5596 vs 4.55 published) and to 6.1% on the primary depth-band rule."
 }
}
```

**Derived from.** `E2/results/ams_gate.json`

**Why it moved.** a flat 'it fails' is internally inconsistent with relying on the same reimplementation as the surviving baseline; the per-checkpoint verdicts pass on 3/3 and the ordering criterion is vacuous at n=3.

## A.10 Layer sensitivity

**As previously stated.** the logistic alpha_50 spans 0.53-2.32 (4.4x) across L-2..L+2

**Corrected statement.** across L-2..L+2 the NON-PARAMETRIC alpha_50 spans 0.400-0.729 (1.8x) while the logistic estimate spans 0.530-2.323 (4.4x); protocol check (3) is led with the 1.8x figure because the logistic estimate is undefined or out-of-grid on 2 of 5 layers and the curve is non-monotone on 4.

**Supporting numbers.**

```json
{
 "misspecification_diagnostic": {
  "n_layers": 4,
  "spearman_abs_gap_vs_non_monotonicity": 0.0,
  "ci": [
   -1.0,
   1.0
  ],
  "conclusive": false,
  "attribution_statement": "INCONCLUSIVE AT THIS n: the diagnostic is computed over 4 layer cells from 1 archived layer-sensitivity sweep(s), which is too few to attribute the logistic span to estimator misspecification rather than geometry. What CAN be stated without an inference: the logistic estimate is undefined or falls outside the measured alpha grid on 2 of the layer cells and the dose curve is non-monotone on 4 of them, so the wider logistic span is being read off curves the logistic model does not describe."
 },
 "coverage": "the layer-sensitivity sweep was archived for 1 member(s) (l1_instruct); the span is therefore a single-member fact and is reported as such"
}
```

**Derived from.** `E2/results/layersens_*.json, monotonicity via E2/lib/dose.py`

**Why it moved.** quoting only the logistic span attributes to geometry what a sigmoid fitted to a non-monotone curve produces.

## A.11 The free-running vs teacher-forced asymmetry

**As previously stated.** the free-running channel stochastically dominates the teacher-forced channel; free-running perturbation deviation grows over 16 steps in every member

**Corrected statement.** free >= forced in almost every paired rollout, strictly greater in 0.79-1.00 of the rollouts that actually diverge and tied in the rest; the free channel has a strictly heavier RIGHT TAIL while the typical rollout decays in both channels. The asymmetry is conditional on divergence, not a property of the typical rollout.

**Supporting numbers.**

```json
{
 "n_members": 15,
 "n_lineages": 5,
 "n_families": 4,
 "json_path_used": "E2/results/member_<id>.json :: survival.runs[i].{free_running,teacher_forced}.survival_ratio  (the per-rollout deviation ratio |delta_T| / |delta_inject|)",
 "n_ci_excludes_0_q50": 14,
 "n_delta_positive_q50": 15,
 "n_ci_excludes_0_q75": 15,
 "n_delta_positive_q75": 15,
 "n_ci_excludes_0_q90": 15,
 "n_delta_positive_q90": 15,
 "n_ci_excludes_0_q95": 15,
 "n_delta_positive_q95": 15,
 "n_mean_diff_ci_excludes_0": 15,
 "n_sign_test_sig_holm_favouring_forced": 0,
 "n_sign_test_sig_holm_favouring_free": 15,
 "sign_test_direction_note": "direction is read on UNTIED pairs, which is what the exact sign test conditions on; reading it on the unconditional fraction (0.11-0.35) inverts the direction because 61-88% of pairs are exact ties",
 "n_sign_test_sig_holm": 15,
 "n_wilcoxon_sig_holm": 15,
 "frac_exact_ties_range": [
  0.61,
  0.88
 ],
 "frac_free_gt_forced_given_divergence_range": [
  0.7894736842105263,
  1.0
 ],
 "n_forced_gt_free_total": 36,
 "all_ties_are_zero_divergence_rollouts": true,
 "cliffs_delta_range": [
  0.072,
  0.3266
 ],
 "frac_free_gt_forced_range": [
  0.11,
  0.35
 ],
 "median_free_range": [
  0.1987113534057019,
  0.7829912702452873
 ],
 "median_forced_range": [
  0.080618216108959,
  0.3290166164695161
 ],
 "n_members_median_below_1_both_channels": 15,
 "n_members_q95_free_exceeds_forced": 15
}
```

**Derived from.** `E2/results/member_*.json :: survival.runs[*]`

**Why it moved.** the median deviation ratio is below 1 in both channels in 15/15 members; the growth is a mean effect carried by the upper tail

## A.12 The two-stage composite / reachability gate

**As previously stated.** a two-stage triage score: a reachability gate at a 0.50 refusal rate, then alpha_50 among the models that pass.

**Corrected statement.** The composite's stage-1 reachability gate was withdrawn at power: both base checkpoints in the powered depth panel cross a 0.50 refusal rate (0.64, 0.84) where iteration 1 called base unreachable at max 0.20 on 5 greedy prompts, and the gate agrees with member class on only 0.67 of 6 checkpoints. The composite as designed therefore no longer functions; its correlation is reported as a CLOSED LOOP on the deployment motivation, not as a working product.

**Supporting numbers.**

```json
{
 "base_0p6": {
  "max_steered_refusal_rate": 0.64,
  "crosses_0.50": true
 },
 "base_1p7": {
  "max_steered_refusal_rate": 0.8383838383838383,
  "crosses_0.50": true
 }
}
```

**Derived from.** `E1/method_out.json :: metadata.composite and metadata.external_validity; the breadth-panel extension is reconstructed in this artifact`

**Why it moved.** both base checkpoints cross the gate at full power, so the gate no longer separates base from tuned.

## A.13 Pre-registration deviations and amendments

**As previously stated.** deviations were listed inline across the results sections.

**Corrected statement.** All deviations are tabulated in one place: 15 iteration-2 experiment-1 deviations with when_decided, 12 timestamped experiment-2 amendments each carrying the data state at the time, and 8 reanalysis deviations.

**Supporting numbers.**

```json
{
 "n_E1_deviations": 15,
 "E1_deviations_with_when_decided": 15,
 "n_E2_amendments": 12,
 "n_V1_deviations": 8
}
```

**Derived from.** `E1/method_out.json :: metadata.prereg_deviations; E2/prereg.json :: amendments; V1/deviations.json`

**Why it moved.** consolidating them frees main-text space and makes them auditable.
