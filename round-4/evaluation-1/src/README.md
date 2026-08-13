# Same numbers, both counting units

**VERDICT (first).** The reproduction gate PASSES on 11/11 legs, so this re-analysis is entitled to restate the archives' numbers. Three things then follow.

1. **The aggregation-unit defect is real and it is load-bearing.** The draft's `0.358` (§5.2) and `0.821` (§5.3) are the SAME statistic at two different units -- 19 members against 7 lineage-aggregated units -- and the gap of 0.464 in rho is larger than the effect the paper argues about. Neither section names its unit. Verdict: `SAME_STATISTIC_TWO_UNITS_BOTH_CORRECT_NEITHER_LABELLED`.
2. **The oriented Delta's sign survives the unit choice; its CI exclusion does not.** On V2's carrier: `SIGN_SURVIVES` and `EXCLUSION_LOST_AT_MEMBER_LEVEL` -- Delta = -0.929 [-1.961, -0.113] at the lineage level against -0.376 [-0.795, 0.110] at the member level. On the discrimination matrix's own alpha_50 carrier the sign does NOT survive: `SIGN_FLIPS`.
3. **The negative result is not manufactured by the cutoffs.** Over a 164,736-point full factorial in the five thresholds, the pre-registered rule returns `PROTOCOL_DOES_NOT_DISCRIMINATE` on 1.0000 of grid points and the stricter strict-exceed criterion on 0.9091. Exactly 1 single-axis change anywhere on the grid produces a strict rival win (check 3 lowered from 2.0 to 1.75, our-AMS 2 against alpha_50's 1).

Scale of the unit effect, measured on the paper's own numbers: over the 16 score x config cells where both units are defined, changing NOTHING but the aggregation unit moves the oriented correlation by a median of 0.238 and a maximum of 0.557, and flips the SIGN on 5 of them.

## What was run

Zero GPU, zero generation, zero LLM/API spend, no downloads, no network: `cost_usd = 0.0`. Every input file is sha256-stamped into `eval_out.json:metadata.inputs`. The estimator code is IMPORTED from the frozen archive rather than re-implemented (`EXEC_OF_LITERAL_CONSTANT_BLOCKS`); the plan named `lib/stats_ext.py`, the functions it lists actually live in `lib_iter3/statsx.py`, and that correction is recorded in the output.

| stage | output | what it does |
|---|---|---|
| `stage0_ingest.py` | `out/stage0.json` | sha256 manifest, panel assembly, unit assertions, the reproduction gate |
| `stage1_dual.py` | `out/stage1_dual_aggregation.json` | every score at BOTH units under a 6-cell analysis-choice grid |
| `stage2_sweep.py` | `out/stage2_threshold_surface.json` | the 164,736-point threshold factorial + the marginal flip table |
| `stage3_tables.py` | `out/tables/*.{md,csv}` | the three missing tables, generated FROM json |
| `stage4_prose.py` | `out/stage4_prose_audit.json`, `out/replacement_text.md` | the prose audit and the repaired text |
| `assemble.py` | `eval_out.json`, `README.md` | folds the stages into the schema |

Run everything with `uv run eval.py` (or `--stage N` for one stage).

## Reproduction gate

| leg | archived | recomputed | pass |
|---|---|---|---|
| `e3_rho_oriented_alpha_50_row` | -0.2080952098456918 | -0.2080952098456918 | PASS |
| `e3_rho_oriented_our_AMS_row` | 0.3578030619574787 | 0.3578030619574787 | PASS |
| `e3_rho_oriented_logit_gap_benign_row` | 0.10109914527054066 | 0.10109914527054066 | PASS |
| `e3_rho_oriented_logit_gap_harmful_row` | 0.6672543587855684 | 0.6672543587855684 | PASS |
| `e3_rho_oriented_ams_paraphrase_refit` | 0.6540675137502804 | 0.6540675137502804 | PASS |
| `v2_lineage_rho_alpha50` | -0.10714285714285716 | -0.10714285714285716 | PASS |
| `v2_lineage_rho_ourAMS` | 0.8214285714285715 | 0.8214285714285715 | PASS |
| `v2_lineage_oriented_delta` | -0.9285714285714287 | -0.9285714285714287 | PASS |
| `e3_alpha50_status_breakdown_19_18_1` | {'DEFINED': 1, 'UNRELIABLE_NON_MONOTONE': 6, 'UNDEFINED_MAX_RATE_BELOW_HALF': 8, 'UNDEFINED_NONPOSITIVE_SLOPE': 4} | {'UNRELIABLE_NON_MONOTONE': 6, 'UNDEFINED_MAX_RATE_BELOW_HALF': 8, 'UNDEFINED_NONPOSITIVE_SLOPE': 4, 'DEFINED': 1} | PASS |
| `v2_accounting_19_14_1` | {'n_members': 19, 'n_analysable': 14, 'n_unreliable_excluded': 5} | {'n_members': 19, 'n_analysable': 14, 'n_unreliable_excluded': 5} | PASS |
| `defined_logistic_member_is_itself_unreliable` | True | True | PASS |

## Analysis 1 -- dual aggregation

Lineage aggregation replaces each lineage's members by their mean, which removes the within-lineage variance and reduces n from 19 members to 7 lineage units. For our-AMS sigma the intraclass correlation is 0.016 (between-lineage variance 0.0179 against within-lineage 1.0671); for the judged outcome it is 0.000. The member-level and lineage-level correlations are therefore estimands of different quantities rather than a contradiction: the first asks whether a checkpoint's score tracks that checkpoint's behaviour, the second whether a lineage's average score tracks that lineage's average behaviour. The unequal lineage sizes ({'L1': 3, 'L2': 4, 'L3': 3, 'L4': 3, 'L5': 2, 'L6': 2, 'L7': 2}) are also why only the identity permutation is guaranteed to reproduce |rho|, so the exhaustive floor is 1/5040 and not 2/5040. A paper whose thesis is that analysis choices swing conclusions must name the unit at every correlation it reports.

Full table: `out/tables/table3_dual_aggregation.md` (32 rows, one per score x unit x config; every cell carries rho, CI, permutation p, the floor, n, and the unit in the row label).

## Analysis 2 -- the threshold surface

| rule | criterion | fraction PROTOCOL_DOES_NOT_DISCRIMINATE |
|---|---|---|
| pre-registered (threshold AND secondary clause) | rival >= 3 of 5 | 1.000000 |
| pre-registered | rival strictly exceeds alpha_50 | 0.909091 |
| pre-registered, checks 1-4 only | rival >= 3 of 4 | 1.000000 |
| threshold-only (secondary clauses dropped) | rival >= 3 of 5 | 0.580201 |
| threshold-only | rival strictly exceeds alpha_50 | 0.242898 |

The two rows differ by a factor of four, and that difference LOCATES the negative result: it is carried by the pass rules' verdict-class and interiority clauses, not by the numeric cutoffs. Check 5 contributes nothing at any grid point -- its REFUSAL kappa of 0.391 lies below the entire swept range [0.40, 0.80], so it fails identically in all four rows and shifts every pass count together; the invariance is proved structurally and verified empirically over the whole kappa axis (`CANNOT_CHANGE_ANY_DISCRIMINATION_VERDICT`).

## Analysis 3 -- the three tables

- `out/tables/table1_discrimination_matrix.{md,csv}` -- Table 1. The discrimination matrix: four cheap benchmark-free safety scores x five falsification checks, on the frozen 19-member / 7-lineage panel. Verdict: PROTOCOL_DOES_NOT_DISCRIMINATE.
- `out/tables/table2_dissociation_per_checkpoint.{md,csv}` -- Table 2. Per-checkpoint dissociation on the 6-member DEPTH panel: what each axis READS (held-out AUROC on 7,241 model-generated items) against what it INDUCES (steered refusal).
- `out/tables/table3_dual_aggregation.{md,csv}` -- Table 3. The dual-aggregation correlation table: every score against the judged plain-harmful refusal rate, at BOTH aggregation units, with n and the permutation floor in every cell.

## Analysis 4 -- prose audit

57 correlation-, AUROC-, Delta- and CI-bearing claims were extracted from the draft's Contributions and Results sections and each was tagged with an aggregation unit and a json pointer: 18 TRACEABLE_UNIT_STATED, 31 TRACEABLE_UNIT_MISSING, 3 VALUE_MISMATCH, 5 UNTRACEABLE -- 39 flagged in total. The repaired text in `out/replacement_text.md` re-audits at 13 claims and 0 flags (`EMPTY`).

Three prose number-dumps are recommended for supplementary:

- **Introduction / Summary of Contributions** (30 numbers) -> replace with `table2_dissociation_per_checkpoint`. First words: - **Induction and detection dissociate within a single axis** (§5.1). On 7,241 held-out, model-generated ...
- **Results / Scorer validity bounds everything above** (25 numbers) -> replace with `table3_dual_aggregation`. First words: Three quantities bound every rate in this paper. Cohen's $\kappa(A,B) = 0.567$ $[0.471, 0.664]$, ...
- **Results / The falsification battery does not discriminate, and the reason is the finding** (17 numbers) -> replace with `table1_discrimination_matrix`. First words: Two of the individual cells deserve their measured statement rather than the flat version ...

## Gaps and honest disclosures

- **Y_OUTCOME_DISAGREES_ACROSS_ARCHIVES**: {'n_members_disagreeing': 3, 'n_members_agreeing': 16, 'all_disagreeing_are_unreliable': True, 'detail': [{'member_id': 'l1_base', 'level': 'base', 'y_e3_transcribed_archive': 0.15, 'y_v2_member_table': 0.19375, 'abs_delta': 0.04375000000000001, 'unreliable': True, 'n_judged_v2': 355}, {'member_id': 'l4_base', 'level': 'base', 'y_e3_transcribed_archive': 0.15, 'y_v2_member_table': 0.175, 'abs_delta': 0.024999999999999994, 'unreliable': True, 'n_judged_v2': 355}, {'member_id': 'l2_base', 'level': 'base', 'y_e3_transcribed_archive': 0.15, 'y_v2_member_table': 0.38125, 'abs_delta': 0.231249999999
- **PLAN_ESTIMATE_NOT_REPRODUCED_AS_STATED**: The hypothesis estimated the member-level oriented Delta at about -0.465. The COMPUTED values are -0.5659 on the discrimination matrix's alpha_50 carrier (max refusal rate, 19 members) and -0.3755 on V2's carrier (non-parametric alpha_50, 14 analysable members). The plan's figure was an arithmetic estimate from two separately-oriented rho values, not a computed paired statistic; nothing was tuned to hit it.
