# Dynamics arm — results (iteration-2 re-analysis)

*Drop-in replacement for the iteration-1 dynamics results. This section reports a pure re-analysis of the archived tree: no rollouts were regenerated and no steering was re-run. Every number carries a JSON pointer into `gen_art_experiment_1/out/tier0_raw.json` (sha256 `77af6eb6c1124a1c…`) or into the artifacts named beside it. Total spend for this section: $0.00.*

## 1. The direction control, re-adjudicated on assumption-free statistics

The load-bearing control for the whole early-warning arm asks whether a random unit vector, injected at the same layer with the same magnitude, separates the panel as well as the refusal direction does. Iteration 1 adjudicated that control on the decay rate λ. Its own tree marks every one of the 640 archived λ rows `identifiable = false` with reason `geometry_below_prereg_rule` (`tier0_raw.json:lambda[*].identifiable`; achieved T_fit = 64 and n_roll = 20 against a pre-registered rule of T_fit ≥ 128, which after the certified refit moves to n_roll ≥ 40). We therefore re-run the control on the two statistics the same tree nominates as assumption-free and stores per row: S1, the 16-step decay ratio (`layerL.decay_ratio_16`), and S2, the deviation AUC normalised by |δ₁| (`layerL.estimates.auc_substitute.auc_norm`). Both are ratios, so all contrasts are computed in logs and bootstrapped over the 20 prompts (10,000 replicates, percentile CI). The primary cell throughout is ε_c = 0.1, p = 16, teacher-forced — the archive also contains an ε sweep and an injection-step sweep inside the same 640 rows, and those rows are excluded from every contrast.

**Per-model contrast (random − refusal, log S1, layer-L, teacher-forced):**

| member | median S1 random | median S1 refusal | log-ratio [95% CI] | Wilcoxon p |
|---|---|---|---|---|
| base | 0.088 | 0.155 | -0.954 [-2.153, +0.168] | 0.1429 |
| instruct | 0.231 | 0.119 | +1.208 [+0.304, +2.208] | 0.0296 |
| abliterated | 0.101 | 0.188 | -1.126 [-2.246, +0.027] | 0.0897 |
| SmolLM2-360M | 0.034 | 0.231 | -2.170 [-2.866, -1.490] | 0.0000 |

The direction matters, but not in one direction: on `instruct` the random axis decays *more slowly* than the refusal axis (+1.208 [+0.304, +2.208]), while on the other three members it decays *faster*. That heterogeneity is exactly what the difference-in-differences is designed to test: DiD(prompt) = [log S_A(refuse) − log S_B(refuse)] − [log S_A(random) − log S_B(random)]. If the between-model separation were generic mixing, the DiD would sit at zero.

**Difference-in-differences, all six pairs (S1, layer-L, teacher-forced):**

| pair | DiD [95% CI] | verdict | Wilcoxon p | Holm p |
|---|---|---|---|---|
| base − instruct | +2.162 [+0.764, +3.606] | DIRECTION_SPECIFIC | 0.0153 | 0.658 |
| base − abliterated | -0.172 [-1.518, +1.355] | INCONCLUSIVE | 0.5706 | 1.000 |
| base − SmolLM2-360M | -1.216 [-2.641, +0.215] | INCONCLUSIVE | 0.1140 | 1.000 |
| instruct − abliterated **(primary)** | -2.334 [-3.573, -1.037] | DIRECTION_SPECIFIC | 0.0049 | 0.214 |
| instruct − SmolLM2-360M | -3.378 [-4.665, -2.176] | DIRECTION_SPECIFIC | 0.0001 | 0.004 |
| abliterated − SmolLM2-360M | -1.045 [-2.588, +0.489] | INCONCLUSIVE | 0.3118 | 1.000 |

On the pre-designated primary pair — instruct vs abliterated, the only pair that isolates safety tuning while holding the pretrained base fixed — the DiD is -2.334 [-3.573, -1.037] log units, a 95% CI that excludes zero, so the verdict is **DIRECTION_SPECIFIC**: the between-model separation is *not* reproduced by the random axis. It does not survive Holm correction within the 48-test family (adjusted p = 0.214), and only 8 of 48 tests in that family have a CI excluding zero — of which instruct − SmolLM2 (-3.378 [-4.665, -2.176], Holm p = 0.0039) is the only one that does survive. The same primary pair gives -1.642 [-2.445, -0.858] on S2 — same sign, CI still excluding zero — and -0.210 [-1.300, +0.903] at the final-layer readout, where the sign agrees but the CI includes zero. The honest summary is that the direction contrast is not the null the λ-based control reported, but neither is it robust to multiplicity or to the choice of readout.

**Equivalence, not absence of evidence.** We pre-registered a margin of ±0.20 log units (≈20% multiplicative, far below the free-running-versus-teacher-forced contrast the same tree treats as a real effect, see §5). 0 of 48 DiD tests pass the two-one-sided-test at that margin and 40 land INCONCLUSIVE. At the observed spread, a ±0.20 equivalence claim at 80% power would need on the order of 1880 prompts rather than 20 — that is the concrete sizing number this re-analysis hands to the next iteration, and it is why the honest label for most of this table is INCONCLUSIVE rather than 'no effect'.

### 1b. λ as a labelled consistency check only

For the record, the archived λ-based control on the primary pair reads -0.404 [-0.784, -0.029] for the random direction (`tier0_raw.json:ordering_tests['qwen3-0.6b/instruct_minus_qwen3-0.6b/abliterated']['lambda_random_dir']`, CI excludes zero) against -0.165 [-0.529, +0.160] for the refusal direction (`…['lambda_refuse']`, CI includes zero). Both numbers rest on the same non-identifiable estimator: at the layer-L readout the median single-exponential fit r² is 0.17–0.54 across members, 30–90% of fits fall below r² = 0.3, 35% of SmolLM2 fits terminate at the optimiser bound, the per-prompt λ inter-quartile ratio across the 20 rollouts runs 8.8–13.2, and the three-estimator agreement ratio has a median in the thousands (1304–4230). Both arms of the λ control are equally non-identifiable, so their asymmetry is a comparison between two equally noisy estimators and cannot carry the control's weight. We report it as a consistency check and adjudicate the control on §1.

## 2. The observable-validity gate

Var*, AC1 and flicker computed on a scalar that does not track refusal are statistics about a meaningless series, so the observable must be validated before any indicator is compared. We pre-register the weakest defensible gate — harmful-vs-benign AUROC ≥ 0.70 **and** margin > 0 (harmful must score *higher*) — and read it off `tier0_raw.json:per_model_meta[m].observable_sanity`, the block fitted on the 128 harmful + 128 benign `layer_contrast` rows.

| member | AUROC [95% CI] | margin | gate |
|---|---|---|---|
| base | 0.414 [0.344, 0.484] | -0.153 | fail |
| instruct | 0.793 [0.738, 0.848] | +0.706 | **PASS** |
| abliterated | 0.480 [0.410, 0.551] | +0.026 | fail |
| SmolLM2-360M | 0.633 [0.565, 0.701] | +0.110 | fail |

Only **1 of 4** members clears, and the consequence is arithmetic: the cross-model fluctuation-indicator comparison has **0 admissible model pairs**. The sensitivity curve does not rescue it — at a threshold of 0.60 two members clear (one pair), at 0.65–0.75 one member clears (zero pairs), at 0.80 none do. The emptiness is the result. The iteration-1 sentence *'indicators track lineage, not safety'* is therefore restated as: on the only member whose observable is a validated refusal readout (instruct, AUROC 0.793, margin +0.706) no cross-model contrast is available; the Qwen-triad overlap (Var* 3.10–3.15, AC1 0.245–0.304, flicker 40.2–42.2) and the SmolLM2 separation are contrasts between series at least one of which is not a validated refusal signal. The full ordering table is retained in `eval_out.json:datasets[ordering_tests_gate_labelled]` with an ADMISSIBLE / NOT ADMISSIBLE label attached to every row.

**Instrument or behaviour?** A low harmful-vs-benign AUROC has two readings — a broken instrument, or a model that genuinely does not treat harmful prompts differently — and the base and abliterated harmful refusal rates (0.025 and 0.000) make the second live. We separate them with a behaviour-independent check: within experiment 2's logged token streams, where actual refusal text is present by construction, we score every logged token as refusal-lexicon or continuation-lexicon using the Qwen3 family list from the frozen dataset and take the AUROC of the logged r_t within each member.

| member (experiment 2) | token-level AUROC [95% CI] | n refusal / n cont | mean r_t refusal / continuation | reading |
|---|---|---|---|---|
| abliterated | 0.935 [0.909, 0.960] | 227 / 95 | +1.53 / -3.83 | instrument works |
| base | 1.000 [1.000, 1.000] | 58 / 2 | +3.13 / -4.10 | instrument works |
| base_plaintemplate | 1.000 [1.000, 1.000] | 12 / 1 | +1.43 / -4.66 | instrument works |
| instruct | 0.950 [0.931, 0.969] | 372 / 72 | +2.34 / -1.91 | instrument works |

r_t rises sharply on real refusal text in every member tested (0.935–1.000 pooled over all four arms; the lowest single-arm value anywhere is 0.752), so the low *prompt-level* AUROC in base and abliterated is a behaviour fact, not an instrument fault. Two caveats are load bearing: the lexicon-matched token counts are small (2–372 per cell, and one member reaches a degenerate 1.000), and experiment 2 covers only the Qwen3 lineage, so SmolLM2-360M's 0.633 cannot be attributed either way. The abliterated member also differs between the arms (huihui-ai v2 in experiment 1, mlabonne in experiment 2) and the two rows are never merged.

**Final-layer readout.** Because the two readouts correlate only 0.17–0.26, the choice of readout is a live analytic degree of freedom, so we evaluate the gate at both. The final-layer column was recomputed with the single forward-pass job this artifact permits (each checkpoint at its pinned revision, the same 256 `layer_contrast` rows, the same refusal-vs-continuation log-odds contrast, no sampling and no steering):

| member | final-layer AUROC [95% CI] | margin | gate |
|---|---|---|---|
| base | 0.588 [0.518, 0.657] | +0.496 | fail |
| instruct | 0.912 [0.875, 0.949] | +6.479 | **PASS** |
| abliterated | 0.771 [0.714, 0.829] | +3.688 | **PASS** |
| SmolLM2-360M | 0.356 [0.288, 0.423] | -0.293 | fail |

This is a substantive finding in its own right: **which readout is chosen decides whether any cross-model comparison exists at all**. At the final layer 2 of 4 members clear (instruct, abliterated), yielding exactly 1 admissible pair — and it is the instruct-vs-abliterated pair, the only one that isolates safety tuning. On that single admissible pair, none of the three indicators separates: var_star +0.008 [-0.082, +0.094]; ac1 -0.003 [-0.023, +0.013]; flicker +0.165 [-0.613, +1.011] — all three CIs include zero. Iteration 1 did not report the readout choice as a degree of freedom, and with a lens-vs-final correlation of only 0.17–0.26 it is a material one.

## 3. The n = 4 rank comparison is uninformative by construction

Iteration 1 compared a label-free SPI against two supervised baselines by Spearman rank correlation with the ground-truth harmful refusal rate over four checkpoints, reporting ρ_SPI = −0.20 against ρ_diff-in-means = +0.40 and ρ_r0-margin = +0.40. Two things need saying in the same breath.

First, **the archived contrast is a tie-break artifact**. Two of the four models have an identical ground-truth harmful refusal rate of 0.000 (abliterated and SmolLM2-360M). Under tie-aware average ranks the same data give ρ_SPI = +0.105, ρ_diff-in-means = +0.632 and ρ_r0-margin = +0.316; the archived −0.20/+0.40 pair is reproduced exactly only under an *ordinal* rank that breaks that tie by array order (recomputed ordinal value -0.20). The two admissible tie-breaks bracket ρ_SPI in [-0.20, +0.40]. The sign of the headline comparison is decided by an arbitrary ordering of two models that the ground truth cannot distinguish.

Second, **no n = 4 ranking could have been significant**. With four models there are 4! = 24 orderings; enumerating them exactly gives a smallest attainable one-sided p of 1/24 = 0.0417 and a two-sided floor of 2/24 = 0.0833 in an untied design, rising to 0.1667 once the observed ties are honoured, which also cap |ρ| at 0.949. The observed values sit at exact two-sided p = 1.000 (SPI) and 0.500 (diff-in-means): indistinguishable from chance, and unable to be otherwise. The ground truth compounds it — only 2 of 4 levels are resolvable once the Wilson intervals on k/40 refusals are drawn, since 3 models sit at or below 0.025.

*Recommended wording.* For the abstract: **with four checkpoints, three of which sit at a refusal floor, no rank comparison between SPI and the supervised baselines is informative; the comparison is deferred to the ≥ 20-lineage panel.** For the appendix, keep the numbers with the exact p, the tie-break range and the 1/24 floor stated in the same sentence.

## 4. The AC1 length control: a verification, not a repair

The Kendall small-sample correction ρ_c = ρ + (1 + 3ρ)/T contributes 0.0090 at T = 192 and 0.0271 at T = 64 — the same order as the ~0.04–0.11 cross-model AC1 gaps being interpreted — so which field iteration 1 reported matters. It reported the corrected one: the per-model `aggregate_by_model[m].ac1.point` matches the median of `indicators[*].primary.detrended.ac1` exactly for all four members, and differs from the median of `ac1_uncorrected` by a constant ≈0.009. This is a verification, not a repair, and the paper should not imply otherwise.

Series lengths are equal by construction — `n_steps` is 192 for every model and every prompt at both readouts — so no part of the AC1 gap is manufactured by unequal T. What is *not* equal is EOS truncation: the fraction of rollouts hitting EOS runs 0.0725 (base) to 0.3175 (instruct), a four-fold difference across members whose series are nevertheless all length 192, so post-EOS steps enter the indicators on unequal footing. That is a limitation of the design, not of the correction.

The archived `series_length_sweep` makes a matched-length re-report free. AC1 is strongly length dependent — it swings by +0.019 to +0.173 between T = 16 and T = 192 depending on the member — which is precisely why a length-matched comparison is required. At the largest common length (T = 192) the paired model-pair bootstrap reproduces the iteration-1 picture on both the corrected and the raw field: the instruct-vs-abliterated AC1 difference is -0.003 [-0.022, +0.014] (corrected) and -0.004 [-0.022, +0.012] (raw) — both overlapping zero — while every SmolLM2 contrast separates on both fields. 17 of 24 matched-length pair × indicator tests have a CI excluding zero. The length-manufactured component of the cross-model gap is therefore measured at ≈0.009 (the constant correction term), against gaps of 0.047–0.110. The same table cannot be produced at the final-layer readout: `series_length_sweep` is archived only for layer-L.

## 5. Cross-arm asymmetry, on matched statistics

The surviving mechanism claim from iteration 1 — perturbations grow when the token stream is free to diverge and shrink when it is held fixed — now rests on the same statistics as the retracted one. At the layer-L readout, log S1(free-running) − log S1(teacher-forced) is +1.958 [+1.001, +2.885] to +3.438 [+2.444, +4.671] across members, with every CI excluding zero: median S1 is 2.53–5.32 free-running against 0.119–0.231 teacher-forced. The steering arm reports the same sign through a different channel: ramping the refusal coefficient inside an already-compliant generation fails on 92–100% of attempts (Wilson CIs in `eval_out.json:datasets[cross_arm_asymmetry]`) while a fresh generation at the same constant α refuses reliably (α₅₀ = 0.475 instruct, 0.55 abliterated). Compliance sticks; refusal does not. The two arms use different perturbation channels and different abliterated checkpoints, so this is corroboration and not replication — and the r_t scales are comparable (both log-odds, per-member 5th–95th percentiles spanning roughly −12 to +8 on the experiment-2 streams).

## What changed relative to iteration 1

1. The random-direction control is no longer adjudicated on λ. λ is reported as a labelled consistency check with `identifiable = false` (640/640 rows) and its misspecification diagnostics printed in the same table row.
2. The verdict `CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING` is withdrawn as stated. On assumption-free statistics the primary pair's difference-in-differences excludes zero (DIRECTION_SPECIFIC before multiplicity correction, INCONCLUSIVE after); most pairs are INCONCLUSIVE, and none is equivalent at ±0.20.
3. 'Fluctuation indicators track lineage, not safety' is withdrawn as stated: at AUROC ≥ 0.70 and margin > 0, one of four members clears the observable-validity gate at the layer-L readout and zero model pairs are admissible; at the final-layer readout 2 clear and the single admissible pair shows no indicator separation at all.
4. The claim that a low harmful-vs-benign AUROC indicts the observable is replaced by an instrument-versus-behaviour separation: the instrument works within-member on real refusal text; base and abliterated simply do not refuse.
5. ρ_SPI = −0.20 vs ρ_baseline = +0.40 is retired. The pair is reproduced only under an arbitrary tie-break between two models with identical ground truth, and the exact n = 4 permutation floor makes any such comparison uninformative by construction.
6. The AC1 headline is confirmed to have used the Kendall-corrected field, and the corrected/raw and matched-length tables are now published side by side rather than asserted to be equivalent.
7. Every cross-model indicator statement now carries an ADMISSIBLE / NOT ADMISSIBLE gate label, and every number carries a JSON pointer into the archived tree.

### Sizing numbers handed to the next iteration

- **Prompts**: ≈1880 prompts (not 20) for a ±0.20-log-unit equivalence claim on the direction contrast at 80% power.
- **Members**: 1 of 4 clear the observable-validity gate at layer-L and 2 of 4 at the final layer; a cross-model indicator claim needs at least two, so the panel must be selected on validated observables — and the readout fixed in advance — not on lineage availability.
- **Lineages**: n = 4 cannot beat an exact two-sided p floor of 0.083; escaping it needs the ≥ 20-lineage panel, and the ground truth must resolve more than 2 levels.
- **Rollouts**: λ remains non-identifiable at T_fit = 64, n_roll = 20; the certified refit moves the requirement to n_roll ≥ 40.
