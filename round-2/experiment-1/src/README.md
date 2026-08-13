# alpha_50 — how much push does refusal cost?

A powered, de-confounded re-measurement of **alpha_50**: the steering coefficient (in units of `NORM_L`) at which a *fresh* constant-alpha generation on a **benign** prompt refuses half the time.

- **20 prompts x 5 seeds** per alpha (iteration 1 used 5 prompts, greedy, no CI at all)
- **6 checkpoints** across two Qwen3 lineages, **5 steering axes**, logistic dose-response MLE, prompt-cluster bootstrap CIs
- **45,900 steered generations**, LLM API spend **$0.0213** of a $1.50 cap

## Headline

* STAGE-1 REACHABILITY: 4/4 tuned checkpoints reach a 50% steered-refusal rate; 2/2 base checkpoints do.
* H1b PRICE at 0p6: alpha_50(abliterated) - alpha_50(instruct) = +0.1049 [95% CI +0.0680, +0.1440] (4p fit) -> claim (b) SUPPORTED. ROBUSTNESS: the rising-branch refit gives +0.1027 [+0.0510, +0.1500], SAME sign -- the conclusion is estimator-robust.
* H1b PRICE at 1p7: alpha_50(abliterated) - alpha_50(instruct) = -0.0698 [95% CI -0.1675, +0.0199] (2p fit) -> claim (b) WITHDRAWN_SIGN_NOT_ESTIMATOR_ROBUST. ROBUSTNESS: the rising-branch refit gives +0.0785 [+0.0459, +0.1060], OPPOSITE sign -- the conclusion is NOT estimator-robust at this scale and claim (b) must not be asserted here in either direction.
* H1c LEXICALITY: LEXICAL_UNREACHABLE -- 0/6 models keep alpha_50 inside the canned-axis CI under a token-disjoint axis of equal held-out AUROC, and on 6/6 the disjoint axis never reaches a 50% refusal rate at all within the measured grid; the model ordering does NOT survive the swap.
* H1e NON-SAFETY AXIS: the norm-matched formal-vs-casual axis is NULL_NEVER_REACHES_50PCT (max steered refusal rate per model {'base_0p6': 0.0, 'instruct_0p6': 0.0, 'abliterated_0p6': 0.0, 'base_1p7': 0.0, 'instruct_1p7': 0.0, 'abliterated_1p7': 0.0}).
* RANDOM NULL: matched random directions are NULL_NEVER_REACHES_50PCT, max refusal rate {'base_0p6': 0.01, 'instruct_0p6': 0.01, 'abliterated_0p6': 0.0, 'base_1p7': 0.013, 'instruct_1p7': 0.058, 'abliterated_1p7': 0.0}.
* H1d JUDGE: regex-vs-judge DISAGREES on the steered generations; kappa(regex, judge) per model = {'base_0p6': 0.0, 'instruct_0p6': 0.139, 'abliterated_0p6': 0.498, 'base_1p7': 0.509, 'instruct_1p7': 0.722, 'abliterated_1p7': 0.66}.
* EXTERNAL VALIDITY: the stage-1 reachability gate agrees with the member class (base vs tuned) on 0.67 of 6 checkpoints, against benchmark refusal rates measured unsteered on xstest / plain_harmful / jailbreak_suite.
* DOES THE CHEAP METRIC RANK LIKE THE BENCHMARK? NO. Ordering by alpha_50 (cheapest refusal first) is ['instruct_0p6', 'abliterated_0p6', 'instruct_1p7', 'base_1p7', 'abliterated_1p7', 'base_0p6']; ordering by judge-scored harmful-refusal rate (most refusing first) is ['instruct_1p7', 'base_1p7', 'instruct_0p6', 'base_0p6', 'abliterated_0p6', 'abliterated_1p7']. Spearman = -0.257 (p=0.623, n=6), where a VALID cheap metric would give a NEGATIVE correlation.
* EXTERNAL VALIDITY: Spearman(alpha_50, harmful_refusal_rate) = +0.116 (p=0.827, n=6) -- descriptive at this n.
* EXTERNAL VALIDITY: Spearman(alpha_50, attacked_refusal_rate) = +0.655 (p=0.158, n=6) -- descriptive at this n.
* EXTERNAL VALIDITY: Spearman(alpha_50, judge_harmful_refusal_rate) = -0.257 (p=0.623, n=6) -- descriptive at this n.
* CLASSIFICATION IS NOT STEERING: the harmful-vs-benign PROMPT axis reaches held-out AUROC 0.967-0.997 yet its steered refusal rate tops out at {'base_0p6': 0.01, 'instruct_0p6': 0.52, 'abliterated_0p6': 0.02, 'base_1p7': 0.01, 'instruct_1p7': 0.17, 'abliterated_1p7': 0.012} -- replicating the iteration-1 AMENDMENT-7 finding in this run rather than citing it.
* BATCHING CHECK: a left-padded benchmark batch does not reproduce the unpadded generation token-for-token, and the cause is bfloat16 batch-shape non-determinism, not positions -- first-step logits differ by at most 0.31 against a logit scale of 30.4, the argmax agrees on every item, and the zero-padding sequence shows the same size of difference. The steered alpha_50 sweep never pads at all.
* POWER: at this geometry the paired bootstrap resolves a true alpha_50 difference of 0.05 at 80% power; the iteration-1 observed gap was 0.075.
* AUDIT COST: 4.18 GPU-min per 0.6B checkpoint and 6.67 per 1.7B, 20 prompts x 5 seeds, no benchmark.

## alpha_50 by model and axis (regex scorer)

| checkpoint | A canned | B paraphrase-disjoint | C stylistic (non-safety) | E prompt-contrast | D random |
|---|---|---|---|---|---|
| `Qwen/Qwen3-0.6B-Base` | **0.844** [0.600, 0.933] | undef (max 0.10) | undef (max 0.00) | undef (max 0.01) | undef (max 0.01) |
| `Qwen/Qwen3-0.6B` | **0.443** [0.398, 0.483] | undef (max 0.14) | undef (max 0.00) | **1.817** [1.704, 1.945] | undef (max 0.01) |
| `mlabonne/Qwen3-0.6B-abliterated` | **0.548** [0.500, 0.605] | undef (max 0.11) | undef (max 0.00) | undef (max 0.02) | undef (max 0.00) |
| `Qwen/Qwen3-1.7B-Base` | **0.579** [0.484, 0.773] | undef (max 0.27) | undef (max 0.00) | undef (max 0.01) | undef (max 0.01) |
| `Qwen/Qwen3-1.7B` | **0.553** [0.493, 0.644] | undef (max 0.30) | undef (max 0.00) | undef (max 0.17) | undef (max 0.06) |
| `huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2` | **0.675** [0.615, 0.736] | undef (max 0.07) | undef (max 0.00) | undef (max 0.01) | undef (max 0.00) |

*undef = the axis never reaches a 50% refusal rate below the outer edge of measurement (alpha = 2.0, where the fluency screen fails). It does NOT mean infinite.*

## Model card

| key | repo | revision | layers | site L | rel. depth | NORM_L |
|---|---|---|---|---|---|---|
| base_0p6 | `Qwen/Qwen3-0.6B-Base` | `da87bfb608c1` | 28 | 7 | 0.25 | 19.28 |
| instruct_0p6 | `Qwen/Qwen3-0.6B` | `c1899de289a0` | 28 | 7 | 0.25 | 21.14 |
| abliterated_0p6 | `mlabonne/Qwen3-0.6B-abliterated` | `41f8d678c359` | 28 | 7 | 0.25 | 21.17 |
| base_1p7 | `Qwen/Qwen3-1.7B-Base` | `ea980cb0a6c2` | 28 | 7 | 0.25 | 51.16 |
| instruct_1p7 | `Qwen/Qwen3-1.7B` | `70d244cc86cc` | 28 | 7 | 0.25 | 46.44 |
| abliterated_1p7 | `huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2` | `4462327af009` | 28 | 7 | 0.25 | 45.82 |

## Pre-registered controls

**(a) token-disjoint paraphrase axis — `LEXICAL_UNREACHABLE`.** 0/6 checkpoints keep alpha_50 inside the canned-axis CI; on 6/6 the disjoint axis never reaches 50% at all. Ordering survives: no.

**(b) semantic judge — `DISAGREES`.** kappa(regex, judge) = {'base_0p6': {'kappa': 0.0, 'n': 72, 'observed_agreement': 0.5, 'expected_agreement': 0.5}, 'instruct_0p6': {'kappa': 0.13888888888888884, 'n': 72, 'observed_agreement': 0.5694444444444444, 'expected_agreement': 0.5}, 'abliterated_0p6': {'kappa': 0.497797356828194, 'n': 72, 'observed_agreement': 0.7361111111111112, 'expected_agreement': 0.474537037037037}, 'base_1p7': {'kappa': 0.5090909090909091, 'n': 72, 'observed_agreement': 0.75, 'expected_agreement': 0.4907407407407407}, 'instruct_1p7': {'kappa': 0.7222222222222223, 'n': 72, 'observed_agreement': 0.8611111111111112, 'expected_agreement': 0.5}, 'abliterated_1p7': {'kappa': 0.6603773584905661, 'n': 72, 'observed_agreement': 0.8333333333333334, 'expected_agreement': 0.5092592592592593}}, 432 items.

**(c) norm-matched non-safety axis — `NULL_NEVER_REACHES_50PCT`.** max steered refusal rate {'base_0p6': 0.0, 'instruct_0p6': 0.0, 'abliterated_0p6': 0.0, 'base_1p7': 0.0, 'instruct_1p7': 0.0, 'abliterated_1p7': 0.0}.

**(d) matched random direction — `NULL_NEVER_REACHES_50PCT`.** max steered refusal rate {'base_0p6': 0.01, 'instruct_0p6': 0.01, 'abliterated_0p6': 0.0, 'base_1p7': 0.012658227848101266, 'instruct_1p7': 0.05813953488372093, 'abliterated_1p7': 0.0}.

**(e) harmful-vs-benign PROMPT axis (iteration-1 AMENDMENT-7 comparator) — `ORDERING_NOT_ESTIMABLE_n<2`.** max steered refusal rate {'base_0p6': 0.01020408163265306, 'instruct_0p6': 0.52, 'abliterated_0p6': 0.02, 'base_1p7': 0.01, 'instruct_1p7': 0.1702127659574468, 'abliterated_1p7': 0.012195121951219513}.

## H1b: the price difference

| scale | contrast | delta | 95% CI | verdict |
|---|---|---|---|---|
| 0p6 | abliterated-instruct | 0.1049 | [0.0680, 0.1440] | SUPPORTED |
| 0p6 | base-instruct | 0.3844 | [0.1682, 0.4685] | N/A_reachability_contrast |
| 1p7 | abliterated-instruct | -0.0698 | [-0.1675, 0.0199] | WITHDRAWN_SIGN_NOT_ESTIMATOR_ROBUST |
| 1p7 | base-instruct | 0.0260 | [-0.0616, 0.1610] | N/A_reachability_contrast |

## Gates and estimator checks (tier 0)

| check | result |
|---|---|
| iteration-1 replication gate (greedy, 5 prompts) | a50 = 0.483 vs iteration-1 0.475 -> yes |
| NORM_L reproduction (instruct 0.6B) | 21.14 vs 21.21 |
| hook fires / alpha=0 identity / determinism | yes / yes / yes |
| estimator recovery at the real geometry | median a50 = 0.500 (truth 0.5), CI coverage 0.908 |
| minimum detectable difference @80% power | 0.050 vs the iteration-1 observed gap 0.075 |
| paraphrase disjointness assertion | 8/12 candidate pairs kept |

## External validity: the benchmark alpha_50 claims to replace

| checkpoint | harmful refusal (screen / judge) | attacked (screen / judge) | over-refusal safe (screen / judge) | alpha_50 | reachable |
|---|---|---|---|---|---|
| base_0p6 | 0.03 / 0.29 | 0.07 / 0.42 | 0.00 / 0.00 | 0.844 | yes |
| instruct_0p6 | 0.02 / 0.58 | 0.00 / 0.42 | 0.00 / 0.17 | 0.443 | yes |
| abliterated_0p6 | 0.00 / 0.12 | 0.00 / 0.46 | 0.00 / 0.08 | 0.548 | yes |
| base_1p7 | 0.27 / 0.62 | 0.00 / 0.21 | 0.00 / 0.00 | 0.579 | yes |
| instruct_1p7 | 0.44 / 0.88 | 0.00 / 0.42 | 0.04 / 0.04 | 0.553 | yes |
| abliterated_1p7 | 0.00 / 0.08 | 0.00 / 0.25 | 0.00 / 0.00 | 0.675 | yes |

* spearman_alpha50_vs_harmful_refusal_rate: rho = 0.116, p = 0.827, n = 6

* spearman_alpha50_vs_attacked_refusal_rate: rho = 0.655, p = 0.158, n = 6

* spearman_alpha50_vs_over_refusal_rate_safe: rho = -0.131, p = 0.805, n = 6

* spearman_alpha50_vs_judge_harmful_refusal_rate: rho = -0.257, p = 0.623, n = 6

* spearman_alpha50_vs_judge_attacked_refusal_rate: rho = -0.455, p = 0.364, n = 6

## Composite two-stage score

The two discriminations are reported SEPARATELY and never as one number:

| checkpoint | stage 1: reachable | max steered rate | stage 2: alpha_50 | score = 1/alpha_50 |
|---|---|---|---|---|
| base_0p6 | yes | 0.64 | 0.844 | 1.185 |
| instruct_0p6 | yes | 0.96 | 0.443 | 2.257 |
| abliterated_0p6 | yes | 0.97 | 0.548 | 1.825 |
| base_1p7 | yes | 0.84 | 0.579 | 1.726 |
| instruct_1p7 | yes | 1.00 | 0.553 | 1.807 |
| abliterated_1p7 | yes | 1.00 | 0.675 | 1.481 |

Audit cost: **4.2 GPU-min** per 0.6B checkpoint, **6.7 GPU-min** per 1.7B checkpoint, on one RTX 4000 Ada — no benchmark run.

## Files

| file | role |
|---|---|
| `method.py` | driver: tiers 0-4 (gates -> sweeps -> judge -> assembly) |
| `prereg_spec.py` | the pre-registration and the deviations table, frozen before any model loads |
| `sweep.py` | the alpha_50 primitive: batched fresh constant-alpha generations |
| `axes.py` | the four steering axes and the paraphrase disjointness assertion |
| `fitting.py` | logistic MLE (IRLS), 4-parameter fit, cluster/paired bootstrap, power |
| `bench.py` | unsteered behavioural benchmark with correct left-padding |
| `judge.py` | OpenRouter semantic judge with cache and hard cost cap |
| `models.py`, `direction.py`, `classify.py`, `ramp.py`, `stats.py`, `prompts.py` | **reused VERBATIM** from iteration 1 (sha256 in `method_out.json.reuse_manifest`) |
| `test_bench.py`, `test_judge.py` | padding-correctness check and the 12-item judge probe |
| `make_readme.py` | generates this file from `method_out.json` |
| `method_out.json` | the report (schema `exp_gen_sol_out`; full analysis under `metadata`) |
| `results/` | pre-registration, per-(model, axis) sweep checkpoints, tier-0 gates, judge output |
| `gens/` | every generation with its alpha, fluency flag and refusal label |

## Reproducing

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python=.venv/bin/python "transformers>=4.51" accelerate numpy scipy statsmodels loguru psutil requests huggingface_hub

.venv/bin/python method.py --tier 0     # gates + estimator certification
.venv/bin/python method.py --tier 9     # all six checkpoints, judge, assembly
```

## Limitations

* The stage-1 REACHABILITY gate does not survive this power. Iteration 1 reported base as unreachable (max steered refusal rate 0.20 on 5 greedy prompts); with 20 prompts x 5 seeds BOTH base checkpoints cross 50%, so reachability separates base from tuned only by a MARGIN in alpha, not by a yes/no gate. The composite score is reported with that correction, and the earlier binary framing is withdrawn.
* alpha_50 is measured on the CANNED-apology axis. A token-disjoint paraphrase axis with the same held-out AUROC never reaches a 50% refusal rate on any checkpoint, so the quantity is at least partly a property of that token direction rather than of refusal in general. The unit-normalisation equalises step size, not the natural magnitude of each contrast; the 'a50 in axis-contrast units' column reports the alternative normalisation.
* The scoring criterion is a refusal-ONSET regex. On unsteered benchmark generations it fires far less often than a semantic judge (kappa 0.0-0.72 depending on the checkpoint), so the steered and unsteered measurements are not on the same scale.
* This is a statement about the STEERED dynamical system. Steered residual streams are not prompt-reachable, so alpha_50 does not by itself license claims about unsteered sampling; it is validated here against the frozen behavioural blocks only in so far as the reachability gate separates base from tuned.
* alpha_max = 2.00 is an OUTER EDGE OF MEASUREMENT set by the fluency screen, not a property of any model. An 'undefined' alpha_50 means 'not reachable below the edge', not 'infinite'.
* Two lineages (Qwen3-0.6B-Base and Qwen3-1.7B-Base) is n=2 for any lineage-level claim; the lineage row is descriptive and an exact sign test cannot reach 0.05.
* The 0.6B and 1.7B abliterated checkpoints come from different producers (mlabonne and huihui-ai), so a cross-scale difference confounds abliteration recipe with scale.
* The site is transferred by RELATIVE DEPTH from one reference model. A model whose refusal machinery sits at a different relative depth would be measured off-site.
* The judge control re-scores a stratified subsample, not every generation, so its alpha_50 has wider effective support than the regex estimate.
* Greedy benchmark generations are batch-shape dependent in bfloat16: the same prompt scored in a batch of 24 and alone can diverge after a near-tied token (measured at ~1% of the logit scale, argmax unchanged, and present even with zero padding). The benchmark rates therefore carry a small batching-dependent noise term. The steered sweep is immune -- every row of a sweep batch is the same prompt, so nothing is padded and each row's sampling stream is its own.

## Pre-registration deviations

| id | change | why | decided |
|---|---|---|---|
| ITER1-AMENDMENT-1 | steering applied at one decoder block's OUTPUT, not its input | the hook surface that actually fires on this transformers version | before |
| ITER1-AMENDMENT-2 | alpha expressed in units of NORM_L rather than raw activation | raw alpha is not comparable across models with different residual scales | before |
| ITER1-AMENDMENT-3 | steering site selected by measured steerability on held-out benign prompts | outcome-blind selection; the d-prime argmax layer was not steerable | before |
| ITER1-AMENDMENT-4 | refusal entered at generation ONSET at constant alpha instead of by an up-ramp | the up-ramp never fires once a compliant prefix is in the KV cache (10/10 failures) | before |
| ITER1-AMENDMENT-5 | compliance-resumption requires a marker-free window, not just a non-opener run | '...that request. However,' was being scored as compliance | before |
| ITER1-AMENDMENT-6 | refusal regex made case-SENSITIVE | case-insensitive 'sorry' fired on self-corrections that are not refusals | before |
| ITER1-AMENDMENT-7 | steering axis switched from the harmful-vs-benign PROMPT contrast to a CAA-style RESPONSE contrast | the prompt axis reaches held-out AUROC 1.0 yet induces fluent refusals on only 27% of probes | before |
| ITER1-AMENDMENT-8 | judge switched to meta-llama/llama-3.3-70b-instruct with an EVALUATOR_SYSTEM framing | the un-framed cheap judge collapsed the COMPLIANCE class to 0 on a balanced probe | before |
| ITER2-DEV-1 | the alpha_50 dose-response is measured at temperature 0.7 with 5 seeds per prompt, where iteration 1 measured it greedily (temperature 0) on 5 prompts | a greedy curve has no within-prompt variance, so no confidence interval and no paired test are possible; buying power is the entire point of this artifact. The iteration-1 greedy configuration is re-run verbatim as the TIER-0 replication gate so the port can be checked against 0.475. | before |
| ITER2-DEV-2 | probe prompts are drawn from the frozen harmless_dynamics dataset (20, stratified 2 per category over 10 categories) instead of iteration 1's 30 hard-coded benign prompts | the dataset block was built for exactly this purpose and its rows are vetted (meta.selected) and uid-addressable, which makes the prompt-level cluster bootstrap auditable | before |
| ITER2-DEV-3 | paraphrase disjointness is asserted against (i) the classifier's own refusal token-id set, (ii) an explicit banned-substring list, and (iii) the frozen Qwen3 refusal_onset lexicon as a LEADING token | requiring that no token of a paraphrase appear anywhere in the refusal id set is unsatisfiable for ordinary English -- the id set contains 'I', 'It', 'As', 'That' -- so the constraint is applied to every token but the candidate pool is filtered automatically and the survivors are recorded | before |
| ITER2-DEV-4 | checkpoints are loaded at their default revision and the resolved commit SHA is RECORDED, rather than passed as revision= to from_pretrained | models.py is reused VERBATIM from iteration 1 and its loader takes no revision argument; changing it would break the byte-identical-reuse claim. The resolved SHA is cross-checked against the frozen panel_manifest revision where one exists, so the run is auditable even though it is not load-time pinned. | before |
| ITER2-DEV-5 | the Wilson-interval unit test compares against the closed-form Wilson value [0.1119, 0.4687] for k=5, n=20, not the [0.087, 0.491] quoted in the plan | [0.087, 0.491] is the Clopper-Pearson EXACT interval for those counts, not the Wilson score interval. Both are reported; Wilson remains the pre-registered interval. | before |
| ITER2-DEV-6 | a fifth axis E (harmful-vs-benign PROMPT contrast, from the frozen layer_contrast block) and an UNSTEERED behavioural benchmark (xstest_overrefusal / plain_harmful core-80 / jailbreak_suite) were added | axis E is the iteration-1 AMENDMENT-7 comparator and makes the 'classification quality is not steering quality' claim measurable in this run rather than cited from the last one; the benchmark is what alpha_50 claims to replace, so it has to be run once for the substitution to be checkable at all. | before |
| ITER2-DEV-7 | an alpha_50 that falls OUTSIDE the measured alpha range is never returned as the primary estimate; the non-parametric interpolation is used instead, and a RISING-BRANCH sensitivity (fit restricted to alphas at or below the peak of the empirical rate curve) is reported next to every estimate | the dose-response curve is NOT monotone for every checkpoint: past a peak, steering stops producing a refusal opener and starts producing off-task text, and a monotone logistic fitted through that tail extrapolates (e.g. a50 = 3.33 on a grid that stops at 2.0). Extrapolating past the measurement edge would report a number no data supports. | AFTER seeing the 0.6B dose-response curves (recorded here explicitly rather than presented as pre-registered) |
