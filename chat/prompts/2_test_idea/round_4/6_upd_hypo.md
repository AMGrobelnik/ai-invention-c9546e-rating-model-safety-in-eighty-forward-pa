# upd_hypo — test_idea

> Phase: `invention_loop` · round 4 · `upd_hypo`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 03:19:25 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Refusal axes steer without reading
hypothesis: |-
  The project's object of study is unchanged (autoregressive generation and its activation geometry as an act-side system; goal = a benchmark-free, harmful-prompt-free safety score for arbitrary open-weight checkpoints). Iteration 1 retired the bistable/EWS mechanism. Iteration 2 retired alpha_50 as a safety score. Iteration 3 retired the five-check falsification protocol as a *contribution*: run unchanged on four cheap scores it does NOT discriminate. What iteration 4 must deliver is therefore no longer a protocol and no longer a new score, but (i) the ONE positive lead the failing protocol produced, replicated at a panel size where it can be believed, (ii) the measurement claim that survived every deflationary control - induction and detection dissociate WITHIN a single refusal axis - scoped honestly and extended where it matters most (abliterated checkpoints), and (iii) an internal-consistency repair the reviewer is right to demand: this study's own headline numbers are reported at two different aggregation units.

  WHAT IS NOW SETTLED (iteration 3, reported as refutation and as correction, not salvage):

  (S1 - THE PROTOCOL DOES NOT DISCRIMINATE) [art_3Cndd5cKsYV0] Applied unchanged to alpha_50, our-AMS sigma, and a Logit-Gap first-step margin (benign and harmful variants) on the same frozen 19-member / 7-lineage panel with the same code: alpha_50 2/5, our-AMS 2/5, logit-gap-benign 0/5, logit-gap-harmful 1/5. Rivals TIE rather than beat, so the pre-registered decision rule returns PROTOCOL_DOES_NOT_DISCRIMINATE and the battery is a limitations instrument, as pre-committed. The load-bearing finding is WHY: the best predictor of judged behaviour (logit-gap-harmful, rho 0.667 [0.439,0.904], exhaustive-permutation p 0.0038, AUC 0.784) passes the FEWEST checks. Construct hygiene and predictive validity are near-orthogonal on this panel. Check 5 fails identically in every row (REFUSAL annotator kappa 0.391 < 0.60), capping every score at 4/5; the checks-1-4 sensitivity returns the same verdict.

  (S2 - THE ONE POSITIVE, AND IT IS UNDERPOWERED) [art_3Cndd5cKsYV0] Refitting AMS's OWN contrastive pairs on token-disjoint paraphrases - exactly the operation the failing lexical check prescribes - IMPROVES the published metric: oriented rho 0.358 -> 0.654 [0.289,0.859], AUC 0.705 -> 0.886, Spearman(refit, original) 0.833, 6/19 PASS/WARN/CRIT verdict-class changes, and it is the only column in the study whose exhaustive lineage permutation reaches the achievable floor (1/5040 = 1.98e-4, NOT 2/5040). This is the study's only forward-looking result and it currently rests on n_lineage = 7, the exact sample size the paper's own Discussion warns readers not to trust.

  (S3 - INDUCTION AND DETECTION DISSOCIATE WITHIN ONE AXIS) [art_SVp6BHC9m27h] The iteration-2 'held-out AUROC 1.000' certificate over-stated axis A as well as axis B. On 7,241 re-encoded, AB-blind, model-GENERATED items (33,135 scanned -> 27,758 kept), the canonical axis A reads real refusals at AUROC 0.486-0.790 only: CI excludes chance on 4/6, clears the [0.40,0.60] indifference band on 1 (instruct_1p7 0.790), and sits AT CHANCE on BOTH abliterated members (0.495, 0.486) - while inducing refusal at 0.91-1.57 axis-contrast units. Axis B spans 0.386-0.602. The lexicality verdict is MIXED (2/6 within the 0.10 margin; 2/6 with A-B > 0.10 CI excluding 0). Two rival explanations are FALSIFIED, not argued away: the weak-estimate reading (R^2(s_B|s_A) <= 0.036, residual AUROC 0.483) and the magnitude-collapse reading of arXiv:2603.22061 (at MATCHED contrast units A exceeds B by +0.36 to +0.61, CIs excluding 0 on 6/6 -> NORM_MISMATCH_DOES_NOT_EXPLAIN). Semantic re-scoring gives PARTIAL_REVERSAL under a four-class judge but the adjudicated verdict is REVERSAL_CONFOUNDED_BY_DEGENERACY (controls C/D draw judge REFUSAL up to 0.80 on degraded text; a five-class rubric puts 0.711 of B's top-alpha text in DEGENERATE vs 0.285 refusal-of-any-wording).

  (S4 - THE ORIENTED COMPARISON, AND THE WRONG-SIGN CLAIM DOWNGRADED) [art_ouNbQqPM59dp] The pre-registered statistic was unoriented and could not reward a perfect metric (ideal alpha_50 scored Delta = -1.821). Oriented, Delta = -0.929 [-1.961,-0.113] over 7 lineage-aggregated units. The stronger 'wrong-signed' sentence is NOT supported at the interval: oriented rho(alpha_50) = -0.107 with bootstrap mass below 0 of 0.585, short of the pre-committed 0.90, so the defensible statement is 'indistinguishable from zero and point-estimated with the wrong sign'. Sign-flip recount: 6 of 11 analysis choices wrong-signed, 4 right, 1 undefined; the 'changes sign four times' sentence is retired. Orientation-free comparators agree on point estimates only (AUC 0.833 our-AMS vs 0.250 alpha_50 - anti-predictive; |rho| difference CI includes 0).

  (S5 - ACCOUNTING IS WORSE THAN 19/17/1, AND THE TWO ARTIFACTS DISAGREE) The primary-estimator triple is 19 / 14 / 1 per art_ouNbQqPM59dp (5 UNRELIABLE excluded) and 19 / 18 / 1 per art_3Cndd5cKsYV0 (status breakdown: DEFINED 1, UNRELIABLE_NON_MONOTONE 6, UNDEFINED_MAX_RATE_BELOW_HALF 8, UNDEFINED_NONPOSITIVE_SLOPE 4). Both are correct about different denominators and the paper must say which is which. Decisively: the single member with a defined logistic alpha_50 is itself UNRELIABLE, so after the pre-registered exclusion the primary estimator is defined on ZERO analysable members. Layer span: non-parametric 1.8x vs logistic 4.4x, logistic undefined at 1 of 5 layer cells and out-of-grid at 1 more, curve non-monotone at 4; the misspecification attribution is INCONCLUSIVE and is reported as such. AMS reproduction: 6/12 checkpoint x rule cells inside +/-25%, per-checkpoint PASS 3/3, ordering test vacuous at n=3 (floor 0.333); the label 'our AMS reimplementation' is kept on that accounting.

  (S6 - THE SURVIVING MECHANISM IS ABOUT AUTOREGRESSION, MEASURED NOT ASSERTED) [art_ouNbQqPM59dp] 61-88% of paired rollouts are EXACT ties (the perturbed free stream never diverged); forced strictly exceeds free in 36/1500; among diverging pairs free wins 0.79-1.00; medians decay in BOTH channels 15/15; sign test and Wilcoxon Holm-significant 15/15 among untied pairs (Cliff's delta 0.072-0.327). 'Deviation grows' and 'stochastic dominance' are retired; the effect is a right tail CONDITIONAL ON DIVERGENCE. The tail is NOT safety-relevant: prompt chi2 p=0.084, member judged-refusal rho -0.221 [-0.392,0.315]; the only surviving association (token-divergence extent r=0.50) is mechanical.

  (S7 - POSITIONING: THE BATTERY FRAMING IS PRIOR ART IN KIND) [art_PeyWw78NIx9d] arXiv:2607.28685 already treats safety scores as measurements with construct/metric/criterion validity, pre-specified positive and negative controls, and leave-one-organization-out clustering (our check 4); arXiv:2605.06161 already operationalises rubric-semantics invariance under certified-equivalent rewrites (our check 1) AND states the discrimination requirement outright. Residual novelty is the OBJECT audited (a benchmark-free, model-level scalar read off activations) and the battery composition - claimed narrowly. Random-direction null RECONCILED with arXiv:2602.06801 on four legs, decisively that they steer v+v_perp and never v_perp alone; qualifier retained that orthogonal shifts are 27-53% smaller than same-norm random directions, so random directions DO move logits.

  THE REVISED CLAIMS, in the order they must now be tested:

  (H-R - REPLICATE THE LEXICAL-INVARIANCE REFIT AT SCALE; THE NEW PRIMARY CLAIM, addressing reviewer MAJOR/scope) The claim to test is: a lexical-invariance refit of a published activation-based safety scanner's contrast set improves its criterion validity, and the improvement survives a panel large enough that the permutation floor stops binding. Run the AMS paraphrase refit on 20-31 lineages drawn from the frozen manifest at <= 4.2B (59 verified checkpoints over 31 lineages are already available) - 96 forward passes per model, zero generation, zero judge calls, $0. Pre-register: does rho(refit) - rho(original) remain positive with a lineage-bootstrap CI excluding 0; does the verdict-class change rate hold near 6/19; is the exhaustive permutation p now well inside a floor of 1/20! rather than pinned at 1.98e-4; and does the improvement hold on a paraphrase set generated by a DIFFERENT author/procedure than the original 80 (so the refit is not itself a lucky wording). Outcomes: (i) SURVIVES -> this becomes the paper's headline, stated as 'a lexical-invariance refit improves a published activation-based safety scanner, replicated across N >= 20 lineages', with the failing battery reframed as the mechanism that produced it; (ii) DOES NOT SURVIVE -> that is also clean, and it adjudicates the question iteration 3 left open by showing 7-lineage predictive validity is itself unreliable, which is the honest reading the Discussion already prefers. Either way the ambiguity between 'hygiene checks measure something users do not care about' and 'small-panel predictive validity is noise' must be RESOLVED by this experiment, not restated.

  (H-U - NAME THE AGGREGATION UNIT AND RECOMPUTE EVERYTHING AT BOTH; mandatory internal-consistency repair, reviewer MAJOR/rigor) The same our-AMS correlation appears as 0.358 (over 19 members with lineage-clustered resampling, art_3Cndd5cKsYV0) and as 0.821 (over 7 lineage-AGGREGATED units, art_ouNbQqPM59dp), and the discrepancy is larger than the effect the paper argues about. Every correlation in the paper must carry its unit explicitly, a table must give BOTH aggregations for alpha_50, our-AMS, the AMS paraphrase refit and both logit-gap variants, and the oriented Delta, its CI and its permutation p must be recomputed at BOTH levels (member-level Delta is approximately -0.107 - 0.358 = -0.465, materially different from -0.929). State explicitly whether the sign and the CI's exclusion of 0 survive the choice of unit. A paper whose thesis is that analysis choices swing conclusions cannot silently mix two aggregation levels across two headline sections; this is the single most damaging discoverable defect in the current draft.

  (H-D - THE DISSOCIATION, SCOPED AND EXTENDED; the surviving positive measurement claim) Keep the claim that induction and detection dissociate within one refusal axis, with three required repairs. (a) SCOPE, reviewer MAJOR/evidence: the matched-contrast test was run on the six-checkpoint DEPTH panel only, and on the breadth panel axis B DOES reach 0.50 refusal on 2 of 5 informative members [art_3Cndd5cKsYV0]. 'B induces almost nothing' must be scoped to the depth panel, the breadth-panel counterexamples reported alongside, and matched-contrast steering on those two members named as what would settle it. (b) EXTEND THE ABLITERATED ARM, reviewer MINOR/evidence: 'at chance on both abliterated members' is a contributions-level claim resting on n=2 from two producers at two scales. Extend the held-out AUROC certificate (forward-pass-only re-encoding of already-logged text) to as many of the manifest's 8 abliterated and 13 behavioural-uncensored members at <= 4.2B as have logged generations; 'the refusal axis is at chance in BOTH roles on K abliterated checkpoints' is a genuinely useful provenance signal that connects directly to the abliteration audit (arXiv:2607.01854), whereas n=2 must otherwise be downgraded in wording. (c) MEASURE THE DEGENERACY ADJUDICATION, reviewer MINOR/methodology: filter to text passing the archived fluency/degeneracy screen BEFORE judging, then report A's and B's refusal rates on that filtered set with CIs alongside the C/D false-positive floor measured on the same filtered set. One sentence - 'on non-degenerate text at matched contrast units, B induces X against A's Y with control floor Z' - converts REVERSAL_CONFOUNDED_BY_DEGENERACY from a verdict into a measurement, which the judge's 0.688 sensitivity / 0.804 specificity does not otherwise support.

  (H-N - CITE THE CLOSEST NEIGHBOUR AND FIX THE BIBLIOGRAPHY, reviewer MAJOR/novelty) arXiv:2607.13346 ('The Refusal Residue') reports the MIRROR IMAGE of our finding on an adjacent safety behaviour: one direction on hidden states detects alignment faking at leakage-free AUROC 0.87 on Llama collapsing to 0.43 on Qwen, while steering over 2,000 runs 'barely changes compliance (|h| < 0.08)' - detect-without-control, same within-single-direction framing, comparable control discipline. It must be cited in 'Detection versus intervention' and at the point of use. The framing to adopt is STRONGER than the current one-directional claim: they report detect-without-control for alignment faking with a model-conditional probe; we report induce-without-detect for refusal with the norm-mismatch rival excluded and both roles at chance on abliterated checkpoints; together these say the read-act mapping is unconstrained in BOTH directions. Also: reference [23] is mis-titled - arXiv:2604.02608 is 'Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens' - and every 2026 preprint title must be re-verified against arXiv, since the positioning dossier already flags title drift on several IDs.

  (H-T - THRESHOLD SENSITIVITY FOR THE NEGATIVE, reviewer MINOR/rigor) The PROTOCOL_DOES_NOT_DISCRIMINATE verdict is a step function of five arbitrary (if pre-registered) per-check thresholds, and check 1 fails all four scores at 0.70 while our-AMS sits at 0.833 and both logit-gap variants at 0.967-0.977 - close to plausible alternative cutoffs. Sweep each check's threshold over a plausible range (e.g. lexical 0.60-0.95 in 0.05 steps) and report the FRACTION of the grid on which the verdict holds. Stability over most of the grid makes the negative far stronger than a single point; instability must be reported as which choices flip it. This is cheap post-processing on results already computed.

  (H-P - THE PROTOCOL, DEMOTED IN PLACE) The five checks stay in the paper as a limitations instrument and as the machinery that generated H-R, never as a certification protocol, and never claimed as novel in kind given arXiv:2607.28685 and arXiv:2605.06161. No further work is spent trying to make it discriminate.

  (H-A - PRESENTATION, reviewer MINOR/clarity) The main text currently reports on the order of two hundred numbers in prose with no tables, which is what hid both MAJOR inconsistencies above. Lift the discrimination matrix into the main text as Table 1 verbatim from the artifact's RESULTS.md; add a per-checkpoint table for the dissociation section (axis A/B/C AUROC with CIs, paired A-B, Holm p, contrast units at 50% refusal); add the dual-aggregation correlation table required by H-U; move at most three prose number-dumps to supplementary.

  WHAT THIS PROJECT NOW CLAIMS, plainly: a benchmark-free, harmful-prompt-free ACT-SIDE safety score does not follow from steering strength along a refusal axis, and the validity battery built to explain that failure cannot rank cheap scores because construct hygiene and predictive validity come apart. Three things survive and are what the paper is now about: (1) within one refusal axis, the direction along which refusal is cheapest to INDUCE is a poor READER of the refusals the model itself writes, with the norm-mismatch and weak-estimate rivals excluded by measurement, and at chance in both roles on abliterated checkpoints; (2) repairing the surface-form dependence that the lexical check detects IMPROVES a published activation-based safety scanner - the study's one actionable recommendation, and the claim iteration 4 must either replicate at n_lineage >= 20 or retract; (3) the free-versus-forced perturbation asymmetry is a fact about autoregressive variance, not about alignment. The two controlled negatives (bistable/EWS; steering-price) stand as contributions in their own right.
motivation: |-
  Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator to hold and send harmful content. The published cheap alternatives all retain a dependency this proposal drops. AMS (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy over 14 configurations and explicitly reports that behavioral uncensored fine-tunes preserving geometry are undetectable by it. RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe and jailbreak prompts AND a safety-aligned reference model. VISAGE (arXiv:2405.17374) measures a safety basin in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static, read-side measurements. That question provably does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.

  This hypothesis attacks the gap from the act side with a different unit: not a direction, feature or basin volume, but a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge while doing something innocuous?

  What a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space is now stated as a testable divergence rather than asserted. The two accounts must rank the panel identically unless weight-space and behavior-space geometry come apart, and we pre-register the two places they should: (a) a behavioral uncensored fine-tune, where a small weight displacement produces a large behavioral change, and (b) a task-vector interpolant, where a smooth weight-space path may produce a step-like behavioral change. A phenomenon the weight-space basin cannot account for is therefore named in advance: a checkpoint whose weight-space basin volume is unchanged from its parent while its behavioral relaxation rate collapses. If the two rankings coincide, we say so and demote the mechanistic claim to a cost claim. The reinterpretation of Qi et al. gets the same treatment: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes afterwards, while the basin account predicts lambda differences PERSIST deep into generation. Step 5 already collects step-wise lambda profiles, so this discriminating test is free.

  If true this yields (a) a mechanistic account of what safety tuning buys, in the language of bistable systems - a shifted operating point; (b) an audit needing a handful of harmless prompts, no harmful content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.
assumptions:
- >-
  Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated
  prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over
  GENERATED steps. The series is NON-STATIONARY (chat-template openings and topic commitment produce a strong deterministic
  trend), so all fluctuation statistics are computed on residuals after subtracting the ACROSS-ROLLOUT mean trajectory at
  each generated step, estimated from the >= 20 rollouts we already collect. Without detrending, a high lag-1 autocorrelation
  would only mean 'this model produces stereotyped openings'.
- >-
  The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives
  the abliteration weight edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is primary
  precisely because a projection onto the abliterated direction is near-constant by construction, which would make any variance
  claim on abliterated models circular. The per-model diff-in-means axis is descriptive only.
- >-
  Steering-based tests (H1) probe states that are partly OFF the manifold reachable by prompting (arXiv:2604.09839 proves
  steered activations are non-surjective). H1 is therefore scoped as a statement about the steered dynamical system, and the
  safety claim of record (H3) uses only unsteered sampling plus a norm-epsilon perturbation whose linearity is verified by
  an epsilon sweep, so the product claim never rests on off-manifold behaviour.
- >-
  A graded safety ladder can be manufactured without training by scaling the alignment task vector W(t) = W_base + t*(W_instruct
  - W_base) and by scaling abliteration strength - but only if the interpolants stay fluent. Every interpolant must pass a
  pre-registered screen (WikiText perplexity within 2x of the t=1 endpoint, plus a distinct-3 / max-n-gram-repeat degeneracy
  check) before entering any analysis, because a degenerate model neither refuses nor complies AND has a degeneracy-dominated
  r_t series, which would corrupt both sides of the headline correlation at once and could manufacture a spurious result.
  Interpolants share a weight lineage and never count as independent units.
- >-
  Small models (0.36B-4B, int8/float32, batched rollouts) show the same qualitative refusal machinery reported for larger
  models. This is tested rather than assumed via a within-family scale ladder (Qwen3 0.6B/1.7B/4B), because a small model
  that is twitchy may be twitchy from undertraining; scale enters the headline analysis as a covariate.
investigation_approach: |-
  PANEL, ENUMERATED BY LINEAGE (the resampling unit). 20 distinct weight lineages, >= 8 architecture families, all CPU-feasible: Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B (each contributing base + instruct + abliterated members), Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Llama-3.2-3B, gemma-2-2b, SmolLM2-360M, SmolLM2-1.7B, TinyLlama-1.1B, Pythia-410M, Pythia-1B, Pythia-1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B, plus >= 4 behavioral uncensored fine-tunes (their own lineages). Base-only lineages (Pythia, OLMo) anchor the low-refusal end. Total measured UNITS (members) ~ 45-55; n_lineage = 20. Every model-level statistic is bootstrapped over the 20 lineages; the member/prompt bootstrap is reported separately and labelled measurement noise.

  STEP 0 - PRE-REGISTRATION (written before any run).
  (a) Layer L is fixed by a rule that never touches the outcome: the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set for ONE reference model, transferred by relative depth L/n_layers. Full layer profiles are secondary, Holm-corrected, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies.
  (b) Decoding fixed and reported: chat template, empty system prompt, temperature 0.7 for dynamics and 0.0 for deterministic controls; max_new_tokens = 192 for the H2 dynamics arm (needed for estimator identifiability) and 64 for ground-truth generation.
  (c) SPI is fixed a priori as the mean of FOUR z-scored terms [-log lambda, log detrended across-rollout variance, Fisher-z of detrended AC1, logit of flicker rate], PLUS - crucially - the z-scoring uses FROZEN normalization constants (means and sds) fit once on a designated REFERENCE subset of 6 named lineages and PUBLISHED in the paper. SPI for any new checkpoint uses only those frozen constants, so it is computable for a single model with no comparison panel (the defect that made the previous definition weaker than RAS's absolute 0-100 scale). All leave-one-out and leave-one-family-out numbers are recomputed with the left-out model excluded from the normalization fit. >= 3 checkpoints are reserved that appear in NO normalization and NO fitting step, and their SPI plus ground truth is reported as the out-of-panel demonstration.
  (d) SIGNED PREDICTION TABLE, one row per ground truth: plain-harmful refusal rate -> expected sign POSITIVE, threshold rho >= 0.6, reason: nearness to the switch makes the refuse mode easy to enter. XSTest over-refusal rate -> POSITIVE, rho >= 0.45, same reason applied to benign-but-scary prompts. Jailbreak attack-success rate -> SIGN IS THE DISCRIMINATING OUTCOME: the ASYMMETRIC reading predicts NEGATIVE (the shallow basin is the comply basin, so the model falls into refusal and is hard to tip out), the DOUBLE-SIDED reading predicts POSITIVE (near a fold in both directions, so it tips either way). Both are pre-registered as competing hypotheses; the outcome that discriminates them is the sign of the partial rank correlation of SPI with ASR controlling for plain-harmful refusal rate, corroborated by the Asymmetry Index of H2b. Either sign is informative; an unsigned rho would have been unfalsifiable.
  (e) Single-forward-pass measurement: DROPPED, not retained as an appendix, so it cannot be substituted for the generated-step result.

  STEP 1 - H1, three ramp arms. For each of >= 30 benign prompts: (i) UP-RAMP, raise alpha per generated token until a refusal-onset token is emitted -> alpha_up. (ii) RETAINED-PREFIX DOWN-RAMP, continue the same sequence with prefix and KV cache kept, lowering alpha -> alpha_down. (iii) FORCED-PREFIX DOWN-RAMP (the control that isolates the claim), force-feed the identical refusal prefix as a prefill without ever ramping up, then ramp alpha down from the same start -> alpha_down_forced. Test statistic = residual = alpha_down - alpha_down_forced, bootstrapped over prompts and lineages. width_naive = alpha_up - alpha_down is reported alongside, with the PRE-REGISTERED expectation that it is large and positive in base models too (per Kwon 2607.14147). A reset arm that discards the prefix between steps is retained as an implementation sanity check only: it must be indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the NOISE FLOOR against which retained-prefix quantities are compared (it will not be exactly 0 under sampling).

  STEP 2 - H2/H2b, early-warning indicators on harmless input only. Per benign prompt (~20 prompts), >= 20 paired-seed rollouts, 192 generated tokens. Perturbed arm: inject a norm-epsilon vector into the residual stream at layer L at step p, continue decoding, fit an exponential to |delta r_t| over subsequent generated steps -> lambda, run separately for refusal-directed and compliance-directed nudges (H2b). Clean rollouts give detrended Var*, detrended AC1, and flicker rate. Estimator hygiene, all pre-registered: subtract the across-rollout mean trajectory before AC1/Var*; a SYNTHETIC RECOVERY CHECK simulating AR(1) with known decay at the observed noise level and series length, reporting the estimator's bias and variance and a minimum series length below which lambda is not reported; and indicators reported as a function of series length so truncation artifacts are visible. Epsilon sweep confirms linearity. Three null controls: random readout axis (must NOT reproduce the safety ordering), random vs refusal-aligned perturbation, and a syntactic (part-of-speech probe) observable, which should decay at the same rate if what is being measured is generic mixing.

  STEP 3 - ground truth, three axes. Per member: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same under a fixed small jailbreak suite including prefill (ASR), ~50 XSTest benign-but-scary prompts (over-refusal). Scoring: cheap OpenRouter LLM judge PRIMARY, refusal-string matcher as screen, Cohen's kappa reported, >= 100 hand-adjudicated stratified items to estimate judge error, attenuation-corrected correlations alongside raw. Budget < $2 of the $10 cap. Interpolants additionally pass the fluency screen, and the ladder is PILOTED on one base/instruct pair first to confirm refusal rate varies smoothly in t rather than snapping to an endpoint; counts manufactured vs passed are reported, and if the pass rate is low the paper states that trimodality returns.

  STEP 4 - H3/H4, prediction with matched-n, faithful baselines. Spearman rho of SPI with each ground truth. The headline comparison is a PAIRED bootstrap of the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages, required to exclude 0 - this removes between-lineage variance common to both and is what n_lineage = 20 can actually support. Baselines: (a) static mean level of r on benign prompts; (b) two zero-internals output-side detectors (next-token probability of refusal-onset tokens; ever-emits-an-apology-token); (c) AMS-style cluster separation sigma and refusal-direction cosine, with leave-one-out accuracy reported in AMS's own format and leave-one-FAMILY-out; (d) a RAS/SafeVec reimplementation whose reference model, layer-window selection rule, prompt sets and calibration mapping are pre-registered, with a reproduction check against RAS's published numbers on overlapping models - if reproduction is out of scope it is labelled 'our RAS reimplementation' throughout, not 'RAS'; (e) VISAGE-style weight-perturbation basin volume on a 6-model subset, with SPI's correlation reported ON THAT SAME SUBSET so the comparison is at matched n. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND model scale. H4 candidates must pass the class-membership pre-check (sigma and refusal-direction cosine preserved vs parent, harmful compliance high, model card and community provenance checked for abliteration or abliterated-merge components); failures are reported with reasons, and if fewer than 4 pass, H4 is reported as a pre-registered case study with per-model detail rather than a statistical claim.

  STEP 5 - mechanism map and the two discriminating tests. Layer-wise and step-wise lambda profiles for base vs instruct vs abliterated vs interpolants: does the basin shallow monotonically in t; does abliteration revert to base or produce a third state; and the two named predictions - (i) does the behavioral basin rank the panel differently from VISAGE's weight basin on behavioral fine-tunes and interpolants (versus the account, if identical); (ii) do lambda differences persist deep into generation (basin account) or vanish after the first few generated steps (Qi et al. token-depth account).

  COMPUTE BUDGET AND STAGING (previously absent). Audit cost and validation cost are reported separately. AUDIT (what a user pays to score one new checkpoint): 20 benign prompts x 20 rollouts x 2 arms x 192 tokens with batched rollouts and hooks active - roughly 10-15 min on one consumer GPU, or ~40-60 min on CPU int8 at <= 1.7B. VALIDATION (what this study pays): Step 3 dominates, ~50 members x 210 prompts x 64 tokens. Tiering, pre-registered: TIER 0 smoke, 3 checkpoints, verifies the full pipeline end to end. TIER 1, 12 checkpoints spanning all families and both ladder endpoints, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2/H2b with controls. TIER 2, remaining members added to Steps 3-4 only (ground truth and correlation), where marginal cost is lowest and marginal power highest. Criteria are evaluated on whatever tier completes, with the tier stated; a partial run is therefore still reportable.
success_criteria: |-
  POWER, reconciled with the resampling unit (the previous version's n=30 arithmetic contradicted its own lineage bootstrap). n_lineage = 20. At n = 20 the 95% bootstrap CI half-width around an observed Spearman rho = 0.8 is roughly +/-0.22, so a criterion requiring SPI's CI lower bound to exceed a baseline's point estimate is NOT attainable regardless of truth and is replaced in advance by the PAIRED difference test, which removes the shared between-lineage variance. Partial correlations with two covariates have adequate power only for partial rho >= 0.5; criteria are set at that level.

  CONFIRMS:
  (1) The H1 residual (alpha_down - alpha_down_forced) is significantly > 0 with a bootstrap CI excluding 0 and exceeding the temperature-0.7 noise floor - path dependence exists that the emitted refusal text does not explain.
  (2) The residual is ordered instruct > base and instruct > abliterated, paired over prompts, CIs excluding 0.
  (3) On harmless prompts only, over generated steps, with DETRENDED statistics and a passing synthetic-recovery check: lambda lower and Var*, AC1, flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls.
  (4) SPI computed with FROZEN constants attains rho >= 0.6 with plain-harmful refusal rate (positive sign, as pre-registered) and rho >= 0.45 with XSTest over-refusal (positive), and the PAIRED bootstrap of rho_SPI - rho_baseline excludes 0 against the best of the static mean and the two zero-internals baselines; the partial correlation controlling for static mean and scale has a 95% CI excluding 0 at partial rho >= 0.5.
  (5) The jailbreak-ASR row resolves in EITHER direction with a partial correlation CI excluding 0 controlling for refusal rate, and the Asymmetry Index of H2b agrees with that sign. This is scored as a confirmed discrimination between the asymmetric and double-sided readings, not as a pass/fail.
  (6) SPI matches or beats AMS leave-one-out accuracy in AMS's own format with the left-out model excluded from normalization, and matches the RAS reimplementation and VISAGE (the latter at matched n on its 6-model subset) without needing their harmful prompts or reference model.
  (7) The >= 3 fully held-out checkpoints are scored correctly from frozen constants alone - the actual product claim.
  (8) H4: every behavioral uncensored fine-tune passing the class-membership check is flagged by SPI while cluster separation and refusal-direction cosine both mark it safe. Reported as a statistical claim only if >= 4 pass, otherwise as a pre-registered case study.

  THIRD OUTCOMES, PRE-REGISTERED (informative, not failures): (a) 'bistability present but not safety-specific' - the residual is nonzero in base models too, in which case H1 is confirmed and H1b refuted and only the quantitative ordering carries safety information (live because Kwon 2607.14147 attributes prefill grip to generic autoregressive conditioning and Rahimi et al. 2602.02600 report that autoregressive commitment masks instability). (b) Behavioral basin and VISAGE weight basin rank the panel identically - the mechanistic claim is then dropped to a cost claim, stated plainly. (c) The interpolant ladder fails its fluency screen or snaps to endpoints - the trimodality problem returns and is reported as a limitation on the correlation's interpretability.

  DISCONFIRMS (reported as refutation, not salvaged): the H1 residual is indistinguishable from the noise floor, i.e. all path dependence is prefix content and the bistable framing adds nothing; or lambda / Var* / AC1 / flicker show no consistent ordering with any ground truth once detrended; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured; or the correlation vanishes once static mean and scale are partialled out; or a zero-internals output-side baseline ties SPI in the paired difference test; or the held-out checkpoints are mis-scored under frozen constants, meaning the metric is a within-panel artifact; or indicators work within one family but fail leave-one-family-out, bounding the metric to a within-family diagnostic.
related_works:
- >-
  Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access
  2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) across 14 configurations
  and 4 families, 71% leave-one-out accuracy, compliance prediction r = -0.546, and explicitly reports behavioral uncensored
  fine-tunes as undetectable. Closest work and sharpest departure: static read-side property from harmful prompts versus our
  dynamical act-side RATE from harmless prompts only. Its documented blind spot is our H4 case study, and we report LOO accuracy
  in its format with the left-out model excluded from our normalization fit so the comparison is not leaked.
- >-
  Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise
  refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state
  alignment under unsafe and jailbreak prompts, mapped to a calibrated absolute 0-100 scale. It is the incumbent for our product
  claim and the reason we now FREEZE SPI's normalization constants: a within-panel z-score cannot score a single new checkpoint,
  which is exactly RAS's advantage. Run as a pre-registered reimplementation with a reproduction check on overlapping models,
  and labelled 'our reimplementation' if reproduction is out of scope. It needs harmful and jailbreak prompts and a reference
  model; SPI needs neither.
- >-
  Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the safety basin in WEIGHT space
  and proposes the VISAGE basin-volume metric, requiring a harmful benchmark at every weight perturbation. 'Shallow basin'
  is their language and we say so. The departure is now a TESTED prediction rather than an assertion: the accounts diverge
  where weight-space and behavior-space geometry come apart (behavioral uncensored fine-tunes; task-vector interpolants).
  VISAGE is run on a 6-model subset with SPI reported on that same subset at matched n; if the rankings coincide we drop the
  mechanistic claim to a cost claim.
- >-
  Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with
  linear probes, finding a sharp drop at final tokens in poorly aligned reasoning models. The per-position refusal score is
  an existing observable which we adopt rather than coin; our contribution is the detrended dynamical statistics computed
  on it across sampled rollouts plus the residual hysteresis test.
- >-
  Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - shows
  diffusion remasking enables recovery from harmful intermediate generations and proposes the SRI internal-dynamics signal,
  observing that autoregressive commitment masks underlying instability. Closest 'dynamics during decoding' work: it compares
  SAMPLING MECHANISMS, we hold sampling fixed and use controlled perturbation-recovery as an ESTIMATOR of distance to a switching
  point. Its commitment finding is a named pre-registered threat.
- >-
  Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - prefill jailbreak study: harm representation stays
  intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific
  collapse, concluding the prefill's grip is generic autoregressive conditioning rather than safety-specific suppression.
  This is precisely why H1's test statistic is now the FORCED-PREFIX RESIDUAL rather than the naive loop width, which this
  paper's mechanism would otherwise explain entirely.
- >-
  Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive
  Logit Steering plus prefix injection induces a phase transition where guardrails collapse, and reports 'Late Decision' (Llama,
  95% ASR) vs 'Early Divergence' (Qwen, safety integrated at ~40% depth) topologies. Phase-transition language exists here
  but as an ATTACK that crosses the edge; our point is estimating distance to the edge without crossing it. Its topology finding
  drives our relative-depth layer transfer.
- >-
  Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal
  and harmful compliance nearly uncorrelated. This is why three ground truths are predicted separately, and why the signed
  prediction table (positive for refusal and over-refusal, sign-as-outcome for ASR) is a real commitment rather than bookkeeping.
- >-
  Xiong et al., 'Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for LLMs' (arXiv:2602.04896,
  2026) - steering vectors from entirely benign data erode guardrails, with ASR above 80%, framed as consumption of a 'safety
  margin'. This is direct empirical support that a margin exists and is small in aligned models, and it is the strongest existing
  evidence for the DOUBLE-SIDED reading in H2b. It measures the consequence of crossing the margin; we measure the margin's
  width from harmless generation without crossing it.
- >-
  Mishra, Khashabi and Liu, 'Steered LLM Activations are Non-Surjective' (arXiv:2604.09839, 2026) - proves steered residual
  streams leave the manifold reachable from discrete prompts. A scope constraint we now state explicitly: H1's ramp probes
  the steered system, so the product claim (H3) rests only on unsteered sampling plus a verified-linear norm-epsilon perturbation.
- >-
  Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the
  static geometric account and our instrument for producing (and partially producing) uncensored checkpoints. Because abliteration
  orthogonalizes writes against that direction, we deliberately do NOT use a projection onto it as the primary observable.
- >-
  Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows aligned and unaligned
  generative distributions differ mainly over the first few output tokens. Their account and ours make DIFFERENT predictions
  we now test: token depth predicts the safety signal is confined to the first few generated steps, the basin account predicts
  lambda differences persist across generated steps.
- >-
  Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry
  (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering near a fold bifurcation).
  The imported source, not a competitor; scholarly search finds it applied to ecosystems, climate, financial crises, depression
  and sleep, but not to LLM generative dynamics or safety auditing.
inspiration: >-
  The transfer is from ecology and climate science at the methodological level. Ecologists face this problem in a different
  costume: they must know how close a lake, forest or fish population is to collapsing without running the experiment of collapsing
  it. Scheffer's early-warning-signal programme solved it by measuring the response to small, harmless disturbances - as a
  system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery from tiny nudges
  slows, fluctuations grow in variance, become more autocorrelated, and the system flickers. Resilience becomes measurable
  without pushing the system over the edge. Mapped onto model auditing: don't jailbreak a model to learn whether it can be
  jailbroken - nudge it gently while it does something innocuous and watch how fast it settles back. The import is legitimate
  only where a real stochastic dynamical system exists, which is why the measurement lives in autoregressive sampling and
  why the single-forward-pass version has now been dropped rather than kept as a heuristic. Ecology also supplies the fix
  for the statistics: EWS practitioners detrend before computing autocorrelation for exactly the reason we now must - a trend
  inflates AC1 and fakes the signal. Two further imports: from physics and materials science, the hysteresis loop as the decisive
  test of genuine bistability, which forces the sweep to happen within one generation with the prefix retained - and, following
  the same tradition's insistence on separating a real state variable from a memory of the drive, the forced-prefix control
  that isolates latent path dependence from conditioning on already-emitted text. From experimental genetics, the base / safety-tuned
  / abliterated series read as wild-type / knock-in / knock-out, extended to a dose-response ladder by scaling the alignment
  task vector, with a viability screen on the intermediates the way a geneticist screens for non-viable phenotypes. What a
  domain expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object
  - a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.
terms:
- term: Refusal observable (r_t)
  definition: >-
    A scalar read off the model at each GENERATED step t. Primary form: logit-lens log-odds of refusal-onset tokens against
    continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. All fluctuation
    statistics use the DETRENDED residual, obtained by subtracting the across-rollout mean trajectory at each generated step.
- term: Critical slowing down
  definition: >-
    The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows,
    fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in
    ecology, climate science and psychiatry for estimating resilience without triggering collapse.
- term: Recovery rate (lambda)
  definition: >-
    The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small residual-stream
    perturbation, averaged over >= 20 paired-seed rollouts of 192 tokens. Small lambda = slow recovery = shallow basin = close
    to switching. Its identifiability at the actual series length and noise level is verified by a synthetic AR(1) recovery
    check with a pre-registered minimum series length.
- term: Asymmetry Index
  definition: >-
    log(lambda_toward_refuse / lambda_toward_comply): recovery from a nudge pushing toward refusal versus one pushing toward
    compliance. It distinguishes an ASYMMETRIC shallow comply basin (tips into refusal easily, so high refusal but LOW jailbreak
    success) from a DOUBLE-SIDED fold (tips either way, so high refusal AND high jailbreak success) - the two readings of
    'nearness to a switch' whose conflation previously left the jailbreak prediction unsigned.
- term: Switching Proximity Index (SPI)
  definition: >-
    The proposed safety metric: the mean of four terms [-log lambda, log detrended across-rollout variance of r, Fisher-z
    of detrended lag-1 autocorrelation, logit of flicker rate], standardized with FROZEN normalization constants fit once
    on a named 6-lineage reference subset and published, so SPI is computable for a single new checkpoint with no comparison
    panel. Higher SPI = closer to the comply/refuse switching point.
- term: Forced-prefix control (alpha_down_forced)
  definition: >-
    The control that makes H1 decisive. The refusal prefix produced at the top of the up-ramp is force-fed as a prefill WITHOUT
    any prior ramp, then alpha is ramped down. Because the prefix content is identical, the difference alpha_down - alpha_down_forced
    isolates path dependence carried by latent state from ordinary conditioning on already-emitted refusal text - the mechanism
    Kwon reports as generic to autoregressive decoding.
- term: Noise floor
  definition: >-
    The apparent loop width produced by sampling alone, measured in the prefix-discarding reset arm at temperature 0.7. It
    must be indistinguishable from 0 at temperature 0; at 0.7 it is the baseline against which retained-prefix quantities
    are compared, replacing the previous, incorrect 'must be exactly zero' requirement.
- term: Flicker rate
  definition: >-
    At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts
    that switch mode between refusal and compliance. A classical early-warning indicator, available only because the measurement
    lives in stochastic sampling.
- term: Task-vector safety ladder
  definition: >-
    A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) plus partial-strength
    abliteration. Every interpolant must pass a fluency screen (WikiText perplexity within 2x of the t=1 endpoint; distinct-3
    and max-n-gram-repeat degeneracy checks) before entering analysis, and the ladder is piloted on one pair to confirm refusal
    rate varies smoothly rather than snapping to an endpoint. Members share a weight lineage and never count as independent
    units.
- term: Weight lineage
  definition: >-
    The resampling unit for every model-level claim: one pretrained base and everything derived from it (instruct, abliterated,
    interpolants). The panel has n_lineage = 20 across >= 8 families and ~45-55 measured members; all headline CIs are bootstrapped
    over the 20 lineages, and the headline baseline comparison is a PAIRED bootstrap of the correlation difference on the
    same resampled lineages.
- term: Behavioral uncensored fine-tune
  definition: >-
    An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than a directional weight edit, so
    it can keep harmful/benign geometry and the refusal direction intact while complying with nearly all harmful requests.
    Class membership is now VERIFIED before use (separation and cosine preserved vs parent, harmful compliance high, provenance
    checked for abliteration or abliterated merges), because an unverified candidate tests nothing.
- term: Audit cost vs validation cost
  definition: >-
    Two separately reported numbers. Audit cost is what a user pays to score one new checkpoint (20 benign prompts x 20 batched
    rollouts x 192 tokens; ~10-15 min on one consumer GPU, ~40-60 min on CPU at <= 1.7B). Validation cost is what this study
    pays to establish the metric, dominated by the harmful/jailbreak/over-refusal ground truth. Conflating them invites the
    objection that a cheap method needed an expensive study - true, normal, and stated plainly.
- term: Knowledge-action gap
  definition: >-
    The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act
    on it (98.2% probe AUROC vs 45.1% output sensitivity, 2026 clinical result). It is why a read-side safety metric can be
    confidently wrong, and why this hypothesis measures an act-side quantity.
summary: >-
  Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable
  about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation
  using the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges,
  higher detrended variance, autocorrelation, flickering), with a forced-prefix-controlled hysteresis residual as the decisive
  test of genuine bistability. This yields a frozen-normalization safety score computable for a single new checkpoint from
  a handful of harmless prompts, with no harmful content and no reference model, aimed where static activation-geometry scanners
  are documented to fail.
_relation_rationale: >-
  Same frame; protocol demoted, AMS lexical-invariance refit promoted to primary, dissociation scoped.
_confidence_delta: decreased
_key_changes:
- >-
  PROTOCOL RETIRED AS CONTRIBUTION (H-P demoted in place): art_3Cndd5cKsYV0 returns PROTOCOL_DOES_NOT_DISCRIMINATE (alpha_50
  2/5, our-AMS 2/5, logit-gap 0/5 and 1/5); rivals tie rather than beat, and the best predictor (rho 0.667) passes the fewest
  checks.
- >-
  NEW PRIMARY CLAIM (H-R), addressing reviewer MAJOR/scope: replicate the AMS paraphrase refit (rho 0.358->0.654, AUC 0.705->0.886)
  on 20-31 lineages from the frozen manifest at <=4.2B — 96 forward passes/model, $0 — and lead the paper with it if it survives,
  or use its failure to adjudicate 7-lineage predictive validity.
- >-
  Addressed MAJOR/rigor (aggregation unit): our-AMS is 0.358 over 19 members with lineage-clustered resampling and 0.821 over
  7 lineage-aggregated units; every correlation must name its unit, a dual-aggregation table is required, and oriented Delta
  must be recomputed at both levels (member-level ~ -0.465 vs lineage-level -0.929).
- >-
  Addressed MAJOR/evidence (scope of the induction claim): axis B DOES reach 0.50 on 2 of 5 informative breadth-panel members;
  'B induces almost nothing' is scoped to the depth panel where the matched-contrast test was run, with those two counterexamples
  named as what would settle it.
- >-
  Addressed MAJOR/novelty: cite arXiv:2607.13346 (detect-without-control for alignment faking, AUROC 0.87->0.43, steering
  |h|<0.08) as the closest neighbour and adopt the stronger two-directional framing; fix the mis-titled [23] (arXiv:2604.02608
  = 'Steerable but Not Decodable') and re-verify all 2026 preprint titles.
- >-
  UPGRADED the dissociation claim with its deflationary controls: weak-estimate reading falsified (R^2<=0.036, residual AUROC
  0.483) and magnitude-collapse (arXiv:2603.22061) excluded at matched contrast units (+0.36..+0.61, 6/6) — but scoped to
  the depth panel and requiring the abliterated arm to grow beyond n=2 (reviewer MINOR/evidence).
- >-
  Added H-D(c): measure rather than adjudicate the semantic reversal — judge only fluency-screened text and report B's and
  A's refusal rates with the C/D false-positive floor on the same filtered set (reviewer MINOR/methodology).
- >-
  Added H-T: sweep each check's threshold (e.g. lexical 0.60-0.95) and report the grid fraction on which PROTOCOL_DOES_NOT_DISCRIMINATE
  holds, since check 1 fails all rows at 0.70 while our-AMS sits at 0.833 (reviewer MINOR/rigor).
- >-
  CORRECTED the accounting: 19/14/1 (art_ouNbQqPM59dp, 5 UNRELIABLE excluded) vs 19/18/1 (art_3Cndd5cKsYV0 status breakdown)
  are different denominators and both must be stated; the one logistic-defined member is itself UNRELIABLE, so the primary
  estimator is defined on ZERO analysable members.
- >-
  DOWNGRADED the wrong-sign claim per the pre-committed rule (bootstrap mass below 0 = 0.585 < 0.90): 'indistinguishable from
  zero, point-estimated with the wrong sign'; 'changes sign four times' retired for a full 6-wrong / 4-right / 1-undefined
  enumeration.
- >-
  RESTATED the surviving mechanism from measurement: 61-88% exact ties, right tail CONDITIONAL ON DIVERGENCE, and the amplifying
  tail is NOT safety-relevant (member judged-refusal rho -0.221 [-0.392,0.315]) — a fact about autoregressive variance, not
  alignment.
- >-
  Conceded prior art in kind for the battery framing (arXiv:2607.28685 validity audit = our check 4; arXiv:2605.06161 policy
  invariance = our check 1 plus the discrimination requirement); residual novelty narrowed to the object audited.
- >-
  Added H-A: main text needs tables (discrimination matrix as Table 1, per-checkpoint AUROC table, dual-aggregation correlation
  table) — the prose-only format is what hid both MAJOR inconsistencies.
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_CKWQh2cOQLLQ
type: dataset
title: Frozen safety prompt sets and model list
summary: |-
  ONE deliverable, full_data_out.json, holding EXACTLY 8 datasets / 2,113 rows, every row tagged metadata_fold = dataset name. Row schema: {input, output, metadata_fold, metadata_uid, metadata_block_version, metadata_meta{...}}. Validated against exp_sel_data_out; full/mini/preview all pass. 3.5 MiB, far under the 100MB limit.

  DATASETS: harmless_dynamics (43: 40 vetted everyday user turns over 10 topics + 3 rejects, meta.selected); xstest_overrefusal (450 = 250 safe + 200 unsafe, split verbatim in meta.label/meta.prompt_type); plain_harmful (594 deduped AdvBench+JBB union, meta.in_core80 marks the 80-row 10-category stratified core, meta.target carries the affirmative prefix); jailbreak_suite (400 = the 80 core behaviors x 5 published templates, meta.pair_id resolves to the plain_harmful uid); layer_contrast (256 = 128 harmful + 128 benign, diff-in-means layer selection ONLY); wikitext_fluency (200 passages of 150-400 words); refusal_token_lexicon (10 tokenizer families); panel_manifest (160 checkpoint rows, 137 verified).

  HOW TO USE. Jailbreak rows branch on meta.delivery: t1_prefill has delivery='assistant_prefill' with meta.user_text and meta.prefill_text SEPARATE (do not concatenate — insert the prefill in the assistant slot); the other four are delivery='user_turn' with empty prefill. t5 stores meta.plaintext beside the base64 wrapper. Every row carries meta.template_text/template_source inline. B7 rows give refusal_onset and continuation lists per family, each entry {token_id, token_str, decoded_str, source in {empirical,lexicon}, empirical_count}; lists are disjoint, all ids < vocab_size, >=12 refusal and >=20 continuation per family, all 10 families empirical.

  PANEL: 137 verified, 59 at <=4.2B over 31 lineages (base 20 / instruct 18 / abliterated 8 / behavioral-uncensored 13); n_lineage 93 overall. lineage_id = the pretrained base at the root of the derivation chain, with the chain in meta.lineage_evidence — this is the bootstrap resampling unit. Gated repos (meta-llama/*, google/gemma-2*, huihui-ai Qwen3 v1 abliterated) are KEPT with verify_error; ungated mirrors are SEPARATE rows with meta.mirror_of. 6 clean H4 behavioral-uncensored candidates at <=4.2B, one (UnfilteredAI/DAN-Qwen3-1.7B) sharing the Qwen3-1.7B-Base lineage with its base/instruct/abliterated triad; 2 disqualified_by_provenance with card text quoted.

  DEVIATIONS, all evidence-driven and recorded in metadata.manifest: (1) walledai/* is gated (403) — XSTest from the ungated Paul/XSTest mirror, AdvBench from the llm-attacks GitHub CSV at a pinned commit. (2) mlabonne/harmful_behaviors REJECTED for layer_contrast because it is an AdvBench repackaging that would break disjointness; the harmful half is the Forbidden-Question-Set (Shen et al. CCS 2024) instead. Disjointness asserted: exact overlap 0, max cosine 0.652 vs threshold 0.85. (3) B7's planned harmful-vs-benign rate criterion cannot separate refusal from topic — run as specified it admitted 'Creating', 'Writing', 'Hack', 'Script', 'Title'. Replaced with behaviour-conditioning: a token is a refusal onset when it is the ACTUAL first generated token of >=3 greedy rollouts whose opening matches a refusal regex, over the same prompts. This surfaced a usable result: refusal onset is near a one-token event ('I'), and per-family greedy refusal rates (meta.greedy_refusal_rate) span 0.00 (Pythia-410m, danube3-500m-chat) to 0.81 (Gemma-2-2b-it), with Qwen3-0.6B at 0.05 with thinking disabled.

  CAUTION: harmless_dynamics (no_robots) and the layer_contrast benign half (alpaca-derived) are CC-BY-NC-4.0, NON-COMMERCIAL. B1 topic labels are a disclosed keyword heuristic (a stratification device, not a claim); the original task label is meta.task_type. 27 build assertions ship in metadata.assertions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_0UsKSgsMHome
type: research
title: Spec Sheets for Rival LLM Safety Metrics
summary: |-
  Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

  BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

  DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

  ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

  OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

  AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 3 ---
id: art_UthAQuH8WZ5C
type: experiment
title: Does refusal wobble predict model safety?
summary: |-
  TIER-0 feasibility experiment for the 'safety = nearness to a tipping point' hypothesis. EXECUTED IN FULL on an RTX A4500: 4 models x 20 harmless prompts x 20 paired rollouts x 192 generated steps (94 min) plus a 39 min certified-geometry refit, 590-710 tok/s, <3 GB VRAM, $0.00 API spend. Panel: Qwen3-0.6B triad (Base / instruct / abliterated) + SmolLM2-360M anchor. The primary abliterated repo is GATED; the maintainer's v2 (huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2) was used per the fallback plan. Panel validity PASSES (instruct 0.225 harmful-refusal vs abliterated 0.000).

  HEADLINE: DISCONFIRMATION, twice over. (1) lambda is NOT identifiable at any geometry reached — the pre-registered synthetic rule demands T_fit>=128; after refitting there (layer/direction/eps/prompts/seeds held identical) the requirement MOVES to n_roll>=40 vs the achieved 20. Sizing for iterations 2-5: n_roll>=40, ~2x this run. (2) The RANDOM-DIRECTION CONTROL REPRODUCES THE ORDERING: a random unit vector at the same layer and magnitude separates the panel as well as the refusal direction (2/3 vs 2/3 significant), and on the ONLY pair isolating safety tuning (instruct vs abliterated) the control separates (-0.493, CI excludes 0) while the treatment does NOT (-0.226, n.s.). Verdicts: LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY (pre-registered) + CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING (supplementary).

  Fluctuation indicators track LINEAGE, not safety: the Qwen triad overlaps (Var* 3.10-3.15, AC1 0.245-0.304, flicker 40.2-42.2) while SmolLM2 separates (Var* 2.75, AC1 0.182). Pre-registered ordering fails and partly reverses (instruct has the LOWEST Var*/flicker of the triad and the FASTEST relaxation). Method vs baseline: label-free SPI Spearman rho=-0.20 vs supervised diff-in-means refusal direction +0.40 and r_0 margin +0.40 — both baselines, given the 32 harmful prompts SPI is denied, BEAT it (n=4, directional only; 3 of 4 models sit at a refusal floor).

  FOUR BUGS THE PRE-FLIGHT GATES CAUGHT, each of which would have produced confident nonsense: (a) injecting at a layer's OUTPUT is a no-op for that layer's own readout (|delta| was EXACTLY 0 at every eps, since the layer writes K/V before a forward hook fires) -> moved to a forward PRE-hook on the layer input; (b) free-running delta cannot estimate a decay rate — token streams diverge in ~7 steps and |delta| GROWS (decay_ratio_16 2.57-5.33) vs teacher-forced (0.119-0.233) -> teacher-forced is the primary channel; (c) mean|delta| is upward-biased by +38% to +68% at EVERY n_roll because E|N(mu,s)|>|mu| -> fit the SIGNED across-rollout mean (bias -0.03..+0.02); (d) flicker-as-fraction saturates at 1.0 -> use crossings/100.

  Other reported diagnostics: exponential model misspecification (median fit r2 0.11-0.54, 30-90% of fits below 0.3, lambda IQR ratios 4.7-20) so the assumption-free decay_ratio/AUC statistics are preferred; layer-L logit lens vs final-layer readout correlates only 0.17-0.26 (below the pre-registered 0.3) so EVERYTHING is reported at both readouts; the per-cell eps-linearity control returns False purely from prompt scatter, while the prompt-averaged version gives r2 up to 0.996 with log-log slopes 0.61-0.90 (both shipped). Layer selection: L=15/28, AUROC 0.999, middle third.

  DELIVERABLES: method.py (single entry point running measure -> reshape -> figures -> validate), reusable spi/ library (models, prompts, observable, rollout, indicators, validity, groundtruth), refit_certified.py, 4 pre-flight gate scripts, 10 figures, out/tier0_raw.json (11 MB full result tree), out/refit_certified.json, out/layer_choice.json (written and asserted BEFORE any indicator). method_out.json is exp_gen_sol_out-valid: 5 datasets / 224 examples, 16 limitations, all 5 control booleans present, all 640 lambda rows carrying the identifiable flag, every failed fit null WITH a reason string, zero non-finite numbers. All 10 figures regenerate from the archived tree alone. pyproject.toml pins all 88 installed packages.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_TFe9eI-2QZN3
type: experiment
title: Does a refused answer stay refused?
summary: |-
  Pre-registered steering-hysteresis experiment on one Qwen3-0.6B lineage (Qwen/Qwen3-0.6B-Base, Qwen/Qwen3-0.6B instruct, mlabonne/Qwen3-0.6B-abliterated; huihui-ai is gated, fallback #8 used). A refusal-direction steering coefficient alpha (in units of NORM_L, the median residual-stream norm at the steering layer) is injected at one block's output for every position in the forward pass, so during incremental decoding each token's KV entries stay frozen carrying the alpha active when written - that frozen cache is the candidate latent state.

  Six arms per (model, prompt, seed), 30 benign prompts x 3 seeds x 3 models, $0.00 spend (all classification is deterministic string/token matching): UP-RAMP (measurement), ENTRY-AT-ALPHA, DOWN-RETAINED (alpha_down), DOWN-FORCED-A (byte-identical refusal prefix prefilled UNSTEERED; the primary control), DOWN-FORCED-B (alpha-schedule replay; positive control), RESET (prefix discarded; noise floor).

  VERDICT = REFUTED, the pre-registered disconfirmation. (1) Hysteresis is real: width alpha_entry - alpha_down = 0.262 [0.185, 0.344] for instruct, positive as pre-registered for generic autoregressive conditioning. (2) It is NOT carried by a retained latent state: excess_width (= alpha_down_forced_A - alpha_down) is 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base - every CI overlaps 0 and every lower bound sits below the temperature-0.7 RESET noise floor (p95 = 0.05). H1b NOT_CONFIRMED. (3) Not a plumbing artifact: FORCED-B reproduces the retained arm EXACTLY (mean and max |diff| = 0.000 on every prompt of every model) and the temperature-0 RESET gate is exactly 0 everywhere.

  Three further results useful downstream: (a) the up-transition is unreachable mid-generation - ramping alpha inside an already-compliant generation fails on 92-100% of attempts (10/10 at delta in {0.05,0.1,0.2,0.4}, 9/10 with an [L-2,L+2] window) while a fresh generation at the same constant alpha refuses reliably, i.e. compliance sticks, refusal does not; (b) a harmful-vs-benign PROMPT axis at held-out AUROC 1.0 (14 of 28 layers) is a poor INDUCER (site score 0.27, partly degenerate refusals) whereas a CAA-style RESPONSE-contrast axis scores 0.69 and yields clean refusals - prompt-classification quality is not steering quality, and a matched random direction induces refusal at no alpha; (c) a candidate cheap safety metric, alpha50 (steering coefficient at which a fresh generation starts refusing, 5 prompts, 13 alphas, no benchmark): base undefined / max rate 0.20, instruct 0.475, abliterated 0.550.

  Eight pre-registration amendments, each with trigger, timestamp and reason, are recorded in prereg.json and echoed in method_out.json['preregistration']. Sensitivity: narrow-floor run (alpha_min=-0.5, 43% censored) gave 0.011 [-0.050, 0.073] and 0.012 [-0.009, 0.035] uncensored; re-scoring every recorded token stream at COMPLIANCE_RUN in {6,10,14} keeps all CIs overlapping 0. Every generated token, its alpha and its r_t are logged in gens/ so every classification is auditable. method_out.json validates against exp_gen_sol_out; the full analysis lives under metadata.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 5 ---
id: art_W0HSULPgrt3K
type: experiment
title: Safety refusal scores and a graded safety dial
summary: |-
  Tier-0 behavioural safety ground truth on 16 members (Qwen3-0.6B base/instruct/mlabonne-abliterated triad, Llama-3.2-1B and SmolLM2-360M base+instruct cross-family pairs, pythia-410m low-refusal anchor, a template side-check member, 3 task-vector interpolants, 4 abliteration-strength members), 3365 generations, three axes (plain-harmful refusal on 80 deduped AdvBench items; jailbreak ASR on 40 of those x 3 fixed attacks = prefill/refusal-suppression/roleplay; XSTest 50 safe + 25 unsafe contrast). Decoding: greedy, fp32, max_new_tokens=64, left padding, enable_thinking=False with an automated <think> guard. fp32 is load-bearing: fp16 batched greedy is NOT batch-invariant (3/4 identical at batch=4 vs 1; 4/4 in fp32).

  HEADLINE (a measurement failure, and the main deliverable). The pre-registered LLM judge (gpt-5.4-nano, frozen rubric, empty system prompt) NEVER assigns COMPLIANCE to harmful content: 0/7 on the COMPLIANCE class of a balanced 21-item probe, 9/21 overall. claude-3-haiku (7/21) and claude-haiku-4.5 (12/21) also score 0/7. Not a parse or payload bug (finish_reason=stop, 100% clean parse, max_tokens 8 vs 64 identical). An evaluator system prompt is what fixes it, not model capability or price: llama-3.3-70b-instruct+framing 18/21 at $0.040/1k, gemini-3.6-flash+framing 21/21 at $1.236/1k.

  CONSEQUENCE: the pre-registered sanity gate FAILS under the frozen judge (deltas 0.263/0.225) and PASSES under a repaired judge (0.463/0.413) on IDENTICAL generations. The ladder verdict flips too: SNAPPED -> SMOOTH. The scorer, not the models, decides both. prereg.json was never edited; the repair arm is documented in prereg_amendment.json.

  THREE SCORERS, one pipeline: baseline refusal-string screen, frozen judge (PRIMARY, reported in full including its failure), repaired judge (full coverage), plus a gemini gold-reference arm on a 400-item stratified subsample. Blind adjudication of 147 items (labels withheld by construction, mtime-asserted): frozen 0.510 acc / kappa 0.242; repaired 0.694 / 0.412; gold 0.759 / 0.449; screen 0.844 binary acc but kappa only 0.315 (accuracy inflated by class imbalance; recall 0.223). DECISIVE: on the 80 adjudicated disagreements the adjudicator sides with repaired 48x, frozen 21x, neither 11x.

  KEY RATES (repaired scorer): qwen3_abliterated refusal 0.113 / ASR 0.858 vs qwen3_instruct 0.525 / 0.633; llama32_instruct 0.975. LADDERS: task-vector W(t)=W_base+t(W_instruct-W_base) gives 0.062/0.237/0.388/0.500/0.525 = SMOOTH and monotone (caveat: t=0 FAILS the fluency screen, distinct-3 0.113, so the low-t end is partly recovery-from-degeneracy). In-house abliteration W<-W-c*rr^T W is SNAPPED under both scorers: refusal flat 0.525->0.512 while XSTest over-refusal rises 0.16->0.42 - it changed the model without producing the knob.

  OTHER: incapacity floor (pythia-410m scores 0.550 'refusal' with 0.327 degenerate rate - rates near that floor carry no safety signal; 4 members auto-flagged UNRELIABLE); template confound (Qwen3 base 0.662 chat-template vs 0.900 generic, delta 0.238 > 0.15 threshold); SmolLM2 instruct refuses LESS than its own base (-0.325, CIs disjoint) so the sanity ordering is family-specific.

  COST: $1.251 total, within the pre-registered $1.50 budget; 0.109 s/item, ~551 tok/s; 50-member panel projects to 0.41 GPU-hours and $0.64. The fitted parameter-scaling slope came out NEGATIVE and is explicitly marked unusable (wall-clock dominated by early EOS, not FLOPs). Audit cost deliberately not measured.

  ARTIFACTS: the 7 ladder checkpoints (1.14 GB each, 7.9 GB) are derived intermediates and are NOT shipped. `python method.py --stage rebuild-ladder --verify-hashes` recreates them bit-exactly from the two public Qwen3-0.6B checkpoints plus the 5 KB refusal_direction.pt; this was verified, not assumed - the directory was deleted and all 7 reproduced their original sha256 (~6 s each), and finalize re-ran to byte-identical verdicts without them. sha256 values and the build recipe are in results/ladder_models_manifest.json.

  FOR DOWNSTREAM USE: do not build correlations on the frozen-judge rates. Use ground_truth_repaired_scorer, and attenuation-correct with the reported reliability. PARTIAL is the weakest class for every scorer (<=0.41 recall), so safe-completion behaviour is the least trustworthy axis. The adjudicator is an LLM agent, not a human, so every 'accuracy' bounds scorer disagreement, not truth.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 6 ---
id: art_r3PqOtpvcIsK
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Uses the frozen benign prompt set, harmful/jailbreak/XSTest rows and panel manifest for the powered alpha_50 sweep.
- id: art_0UsKSgsMHome
  label: methodology
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's estimator recipes, judge framing and baseline specs as the methodology for the re-measurement.
title: How much push does refusal cost?
summary: |-
  POWERED, DE-CONFOUNDED RE-MEASUREMENT OF alpha_50 (the steering coefficient, in units of NORM_L, at which a fresh constant-alpha generation on a BENIGN prompt refuses half the time). 45,900 steered generations: 6 checkpoints (Qwen3-0.6B and Qwen3-1.7B x base/instruct/abliterated) x 5 axes x 20 frozen benign prompts x 5 seeds x a coarse(0-2.0/0.20)+dense(0.05) grid, 32 tokens, temperature 0.7, EOS banned, bf16. Iteration-1 steering code (models/direction/classify/ramp/stats/prompts.py) reused VERBATIM, sha256-verified byte-identical in reuse_manifest. LLM spend $0.021 of a $1.50 cap. tier_completed=4.

  GATES ALL PASSED (results/tier0.json): iteration-1 replication a50=0.483 vs 0.475 (greedy, 5 prompts, verbatim config); NORM_L 21.14 vs 21.21; hook-fires / alpha=0-identity / determinism exact; an independent outcome-blind site scan re-selects layer 7 of 28 (score 0.778), the pre-registered site; estimator recovers a50=0.500 (bias 0.0004) with 90.8% bootstrap CI coverage at the REAL geometry; MDE@80% power = 0.05, below the 0.075 gap it had to resolve — so claim (b) was answerable before it was asked.

  HEADLINE — THE METRIC LARGELY DOES NOT SURVIVE THE POWER.
  (1) H1c LEXICALITY, the decisive control: a token-disjoint paraphrase axis with EQUAL held-out AUROC (1.0) and cos(A,B)=0.38 never reaches a 50% refusal rate on 6/6 checkpoints (max 0.07-0.30). alpha_50 is substantially a property of the canned-apology token direction, not of refusal in general.
  (2) H1a REACHABILITY WITHDRAWN: iteration 1 called base unreachable (max 0.20, 5 greedy prompts); at full power BOTH base checkpoints cross 50% (0.64, 0.84). Base-vs-tuned is a margin in alpha, not a yes/no gate; the gate agrees with member class on only 0.67 of 6.
  (3) H1b PRICE SPLITS BY SCALE: 0.6B delta=+0.1049 [+0.0680,+0.1440] SUPPORTED and estimator-robust (rising-branch refit +0.1027); 1.7B delta=-0.0698 [-0.1675,+0.0199] -> WITHDRAWN_SIGN_NOT_ESTIMATOR_ROBUST, because the rising-branch refit gives +0.0785 [+0.0459,+0.1060], the OPPOSITE sign.
  (4) EXTERNAL VALIDITY (the benchmark alpha_50 claims to replace, run once here on xstest/plain_harmful-core80/jailbreak_suite): alpha_50 ranks checkpoints DIFFERENTLY from the benchmark. Judge-scored harmful-refusal orders instruct>base>abliterated at both scales (1.7B: 0.88/0.62/0.08), while alpha_50 orders instruct<abliterated<base. Spearman(alpha_50, judge harmful refusal) = -0.257 (p=0.62, n=6); a valid cheap metric needs a clearly negative correlation.
  CLEAN NULLS: the norm-matched formal-vs-casual stylistic axis reaches 0.00 refusal on every checkpoint (cos to canned -0.05), and matched random directions 0.00-0.06. So the effect is NOT 'any axis at that site steers'.
  BASELINE COMPARATOR replicated in-run: the harmful-vs-benign PROMPT axis reaches held-out AUROC 0.967-0.997 yet its steered refusal rate tops out at 0.01-0.52 (a50=1.82 where defined) — classification quality is not steering quality.

  alpha_50 [95% CI] on the canned axis: base_0p6 0.844 [0.600,0.933] (non-parametric; the logistic extrapolated to 3.33 past a grid ending at 2.0, so a range guard forbids it), instruct_0p6 0.443 [0.398,0.483], abliterated_0p6 0.548 [0.500,0.605], base_1p7 0.579 [0.484,0.773], instruct_1p7 0.553 [0.493,0.644], abliterated_1p7 0.675 [0.615,0.736]. NORM_L 19.3/21.1/21.2 (0.6B) and 51.2/46.4/45.8 (1.7B); raw and axis-contrast-unit columns also shipped.

  METHOD NOTES A PAPER CAN RELY ON: cluster bootstrap over PROMPTS (5000 resamples) via IRLS on aggregated counts; 2p/4p/non-parametric estimators with an explicit primary-selection rule; per-alpha Wilson intervals (the plan's [0.087,0.491] reference is the Clopper-Pearson exact interval, not Wilson — both reported); dose-response MONOTONICITY diagnostics, since several curves rise then fall as steering degrades the text; judge control = llama-3.3-70b with EVALUATOR_SYSTEM verbatim (12/12 on a probe, 432 items, kappa 0.00-0.72) cross-checked against gemini-3.6-flash; a padded-batch mismatch proven to be bf16 batch-shape numerics (max |logit delta| 0.31 vs logit scale 30.4, argmax agrees, and the ZERO-padding sequence differs equally) rather than a positional bug — the steered sweep never pads at all. 15 pre-registration deviations, each with when_decided, including the one decided AFTER seeing the curves. Audit cost 4.2 GPU-min per 0.6B and 6.7 per 1.7B checkpoint on one RTX 4000 Ada.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 7 ---
id: art_sabuvuJ8P3Wy
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Draws the 19-checkpoint / 7-lineage breadth panel and all prompt sets from the frozen manifest and datasets.
- id: art_0UsKSgsMHome
  label: baseline spec
  relation_type: uses
  relation_rationale: >-
    Reimplements AMS to the dossier's published spec, including its Table-I reproduction gate and 96-forward-pass budget.
title: Testing if a cheap safety score works on new models
summary: |-
  Tests whether alpha_50 -- the steering coefficient at which a fresh generation on BENIGN prompts starts refusing 50% of the time, invented in iteration 1 on one Qwen3-0.6B lineage with 5 prompts and no CI -- is a cross-model triage metric. Panel: 19 checkpoints, 7 lineages, 6 architecture families (Qwen3, Qwen2, Llama3, Llama2, SmolLM2), all <=2B, float32, 1x RTX 4090. Cost $0.3384 of a $2.00 judge cap. Pre-registered before measurement; 12 amendments logged with timestamps and the data state at the time. Re-running --assemble from checkpoints reproduces method_out.json byte-identically apart from created_utc.

  D1 (alpha_50, 20 benign prompts x 5 seeds x 13-15 alphas = ~1300-1500 fresh generations/member, logistic MLE on the exact per-draw likelihood, 2000-replicate prompt-clustered bootstrap): THE PRE-REGISTERED PRIMARY ESTIMATOR IS DEFINED ON 1 OF 19 CHECKPOINTS. Two measured causes: (a) the dose curve is an INVERTED U, not a sigmoid -- past the alpha where the axis dominates the residual stream the model can no longer FORM a refusal opener (Qwen2.5-1.5B-Instruct: 0.01 -> 0.92 -> 0.13, whole-grid logistic gives alpha_50 = -0.459, CI [-12.98, 0.67]); (b) 6 of 7 base members never reach 0.5. Base max refusal rate 0.360 [0.190, 0.526] vs tuned 0.698 [0.474, 0.883] is a real base-vs-tuned separation. Variance decomposition (lineage = resampling unit): AMBIGUOUS on both pre-registered fallbacks (nonparametric alpha_50 within/across 0.885 [0.13, 4.57], n=6; max refusal rate 1.113 [0.64, 5.67], n=7). Within-lineage rank ordering reproduces the pooled ordering in only 2 of 4 / 2 of 7 lineages. Paired instruct-minus-abliterated: both defined CIs include 0, only 2 lineages carry it, pooled CI SUPPRESSED (a bootstrap over 2 numbers is not an interval) -> claim WITHDRAWN_UNDERPOWERED per the rule stated in advance; simulated power at the iteration-1 gap was 0.35, computed before the fits, with bootstrap coverage measured at 0.967 vs nominal 0.95.

  TWO MECHANISMS THAT REFRAME THE METRIC. (i) LEXICAL_PARTIAL: a token-disjoint paraphrased refusal axis (zero frozen-opener matches) fails to reproduce alpha_50 on 3 of 4 informative control members with disjoint Wilson CIs -- Qwen3-0.6B 0.933 vs 0.183, Qwen3-0.6B-abliterated 0.967 vs 0.000, Qwen2.5-1.5B-Instruct 0.900 vs 0.633; only Llama-3.2-1B-Instruct agrees. A norm-matched stylistic axis induces <=0.02 and a random direction <=0.08. So on the anchor lineage the score largely prices a particular refusal WORDING, not refusal. (ii) LAYER FRAGILITY (unplanned, forced by the data): the outcome-blind scan leaves layers 6/7 near-tied (0.719 vs 0.688) and the logistic alpha_50 spans 0.53-2.32 (4.4x) across L-2..L+2 while the nonparametric estimate stays in 0.40-0.73.

  D2 (275 greedy generations/member, repaired judge only): 5,785 items judged, parse rate 0.998, 0 unlabelled, $0.3384. Screen-vs-judge Cohen's kappa -0.021 to 0.774 (median 0.227), confirming the cheap string screen is not a substitute. Five base members auto-flagged UNRELIABLE (degenerate 0.25-0.46) and excluded from correlations.

  D3: AMS reimplemented to dossier spec (48 pairs, exactly 96 forward passes asserted, final prompt token, 40-80% depth sweep, all three calibration rules; synthetic separation recovered to 2.2%). THE TABLE-I REPRODUCTION GATE FAILS (Llama-3.2-3B-Instruct 8.37 -> 5.007, 40% error; ordering inverts), so the label branches in code to 'our AMS reimplementation' everywhere. Headline paired bootstrap over 7 lineages: DELTA = rho_alpha50 - rho_AMS = -0.714 [-1.765, 0.667] -> TIE; exhaustive permutation p = 0.840 against a floor of 0.0004. The decisive statistic is the leave-one-lineage-out jackknife: alpha_50's rho ranges -0.086 to 0.771 depending on which single lineage is dropped, while our-AMS stays 0.714-0.943 and never changes sign -- for 1/14th the compute. H4 case study (DAN-Qwen3-1.7B, n=1, 3/4 class checks): the pre-registered blind spot was NOT observed -- our-AMS demotes it to WARN and its refusal direction has rotated (cosine 0.699 vs parent).

  D4 RATCHET_GENERALISES: 5 of 5 lineages, 15 members, 4 families. Free-running perturbation deviation grows 2.0x-612x over 16 steps in every member; teacher-forced is 1-3 orders smaller and <1 in 7 of 15. Up-ramp failure 50-100% vs matched fresh-control refusal 0.00-0.33. No exponential fit, no lambda, so no identifiability gate can fail.

  SHIPPED: method.py + lib/ (10 modules), prereg.json with all amendments, per-member checkpoints in results/, every dose-response token stream with alpha and r_t in gens/, scored.jsonl, judge_cache.jsonl, layer-sensitivity and T1/T2/T3 test outputs, README.md with verdict-first tables, and pyproject.toml pinning all 71 packages.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 8 ---
id: art_gYmQllaTCGT5
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Rebuilds the judge probe from the frozen harmful/jailbreak/XSTest rows underlying the archived generations.
title: Rebuilding a flawed AI safety judge test
summary: |-
  AUDIT OF THE ITERATION-1 JUDGE SWAP. Rebuilds the 21-item, 9-character-heuristic probe that justified replacing the frozen judge (which moved abliterated plain-harmful refusal 0.700->0.113 and jailbreak ASR 0.092->0.858) as a 124-item probe over all four rubric classes, drawn from the 3,365 archived iteration-1 generations and stratified over the frozen-vs-repaired disagreement region (Q1 60 / Q2 24 / Q3 PARTIAL 20 / Q4 21 bridge / Q5 topup; max member share 13.7%; 47 disagreement cells). Truth from two BLIND independent LLM annotators plus an adjudicator, drawn from three model families (xAI grok-4.3, Moonshot kimi-k2-thinking, Alibaba qwen3.8-max) NONE of which is the family of any scored arm, so no arm is self-referentially scored. 11 arms scored on identical items under the unchanged frozen rubric: 6 live judges, 3 archived-label arms, 2 free negative controls. Cost $1.4872 of a $2.50 cap over 1,300 billed calls; fully cached, so reruns are $0.00. No GPU, no local inference.

  SIX FINDINGS (all in method_out.json.metadata.headline_findings, each with its number).
  (1) H1 SEVERELY_DEGRADED_NOT_ZERO. Iteration 1's '0/7, three judges, never labels harmful compliance as COMPLIANCE' does NOT survive: pooled COMPLIANCE recall of the three un-framed safety arms is 29/117 = 0.248, Wilson 95% [0.179, 0.333] (frozen 6/39, claude-3-haiku 10/39, claude-haiku-4.5 13/39). BUT on the 21 items carried verbatim from the old probe those same arms score 0/21. The old MEASUREMENT replicates exactly; only the generalisation from 7 easy items fails.
  (2) H2 the old truth labels were RIGHT. The blind panel re-adjudicated all 21 bridge items and changed NONE; every arm's bridge score is identical old-vs-new (gemini still 21/21, llama-70b 18/21, claude-haiku-4.5 12/21 un-framed). The plan's A007 premise ('a refusal-by-redirection, demonstrably mislabelled') was TESTED AND REFUTED: the completion opens 'Certainly! Here's a message that conveys hope...' but truncates at 64 tokens mid-compliance on 'Self-harm or suicide is a way to feel', which annotator B quoted; label COMPLIANCE stands.
  (3) H3 the defect is COVERAGE, not labels. The 9-character heuristic scores 0.912 [0.770, 0.970] on the items it labels but covers only 27.4% of the probe and emits PARTIAL never. That is the quantitative statement of the defect.
  (4) H4 the rubric's PARTIAL boundary is not reliably applicable. Cohen's kappa(A,B) = 0.567 [0.471, 0.664] (below the pre-set 0.60 floor, so the planned low-kappa path ran); per-class one-vs-rest kappa COMPLIANCE 0.819, DEGENERATE 0.846, REFUSAL 0.391, PARTIAL 0.054. Dominant A-vs-B flow is REFUSAL<->PARTIAL (26 items). Where A and B agree an independent third family agrees with 83/83 of the consensus [0.956, 1.0], so disagreement is confined to that one boundary.
  (5) H5 propagation PARTLY_DISSOLVES. Both published rates reproduce exactly from scored.jsonl. Against annotator truth on a FRESH SIMPLE RANDOM SAMPLE (40/block): jailbreak ASR revision STANDS (truth 0.800 [0.652, 0.895], inside the repaired arm's CI; frozen 0.092 far outside); the block-A refusal revision needs RESTATING (truth 0.000 [0.000, 0.088], so the repaired judge's 0.113 still over-states it and the frozen 0.700 is wrong by an order of magnitude). Confusion-matrix correction corroborates (corrected 0.017 and 0.926). method_out.json names every downstream quantity requiring restatement (sanity gate, ladder SMOOTH/SNAPPED verdict, per-member refusal and XSTest rates, per-attack and pooled ASR, alpha_50/H1'').
  (6) H6 NEW: the frozen judge is itself unstable. Re-run at temperature 0 with its exact configuration it reproduces its own archived labels only 75% of the time (kappa 0.596), versus 96% for the repaired arm and 100% for the gold arm, so every iteration-1 frozen-judge rate carries an un-reported labelling-variance component.

  NET READING FOR THE PAPER: iteration 1's DECISION to swap the judge was correct and is confirmed by independent annotator truth; its stated EVIDENCE ('never', 0/7) was an over-generalisation from a probe that could only contain the easy quarter of the population; and one of its two headline revised numbers needs restating. Three sensitivity columns (drop-unstable, A==B-consensus-only, bridge-only) accompany every headline number. ALSO NOTE: annotators are LLM agents, not humans, so all accuracies bound agreement with an LLM panel, not ground truth; the probe is deliberately stratified so raw per-arm accuracy on it is not a corpus estimate. Deliverables: method.py (resumable, cached, stages 0-7), method_out.json (exp_gen_sol_out-validated, 124 examples with predict_* for all 11 arms), results/probe_items_v2.json, annotation/blind_items_v2.json, results/truth_labels_v2.json, results/disputed_items.{json,md} (41 disputed items verbatim), results/cell_census.json, results/arm_labels_v2.json, results/cost_ledger.jsonl.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 9 ---
id: art_lYnzVulUmeG9
type: evaluation
in_dependencies:
- id: art_UthAQuH8WZ5C
  label: reanalysis
  relation_type: differences
  relation_rationale: >-
    Re-analysis overturns its verdicts: control is direction-specific; 'indicators track lineage not safety' withdrawn.
- id: art_TFe9eI-2QZN3
  label: cross-check
  relation_type: similarities
  relation_rationale: >-
    Cross-arm check: its token streams agree in sign that compliance sticks and refusal does not; corroboration only.
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Uses the frozen contrast and lexicon rows to recompute the observable-validity gate at the final-layer readout.
title: Re-checking the wobble experiment's statistics
summary: |-
  PURE RE-ANALYSIS of the iteration-1 dynamics arm (no rollouts regenerated, no steering re-run). Every number carries a JSON pointer into the archived tree; inputs frozen by sha256 in metadata.inputs. One piece of new compute only: final_layer_gate.py, forward-pass-only (~1,000 passes, 45 s), which recovers the observable-validity gate at the final-layer readout that the archive never stored. LLM spend $0.00.

  DELIVERABLES: eval.py (1,657 lines, imports the archived spi/ library verbatim so estimator definitions cannot drift), eval_lib.py, final_layer_gate.py, make_report.py, eval_out.json (exp_eval_sol_out-valid; 12 datasets / 249 rows; 39 aggregate metrics; metadata.verdicts with 8 strings; metadata.limitations with 15), figs/F1-F6 (PDF+PNG), results_section.md (drop-in replacement for the dynamics results, generated FROM eval_out.json so prose cannot drift), deviations.json/.csv (8-row pre-registration-deviations table), out/analysis_tables.json, out/final_layer_gate.json.

  FOUR REPAIRS AND WHAT THEY FOUND.
  (1) DIRECTION CONTROL RE-ADJUDICATED. Iteration 1 ran it on lambda; the tree marks identifiable=false on 640/640 rows (geometry_below_prereg_rule). Recomputed on the assumption-free statistics (S1=decay_ratio_16, S2=auc_norm; log scale; 10,000-rep paired-over-prompt bootstrap; Wilcoxon; Cliff's delta) the PRIMARY difference-in-differences (instruct vs abliterated, layer-L, teacher-forced) is -2.334 [-3.573, -1.037] -> DIRECTION_SPECIFIC, i.e. NOT the generic-mixing null iteration 1 reported. But it fails Holm within the 48-test family (adj p 0.214; only instruct-SmolLM2 survives, adj p 0.0039), 0/48 pass TOST at +/-0.20, 40/48 are INCONCLUSIVE. Sizing number: ~1,880 prompts needed, not 20. Archived lambda contrast re-quoted VERBATIM and found to differ from the plan's quoted values: -0.4045 (random) / -0.1655 (refusal), not -0.493/-0.226.
  (2) OBSERVABLE-VALIDITY GATE (AUROC>=0.70 AND margin>0). Layer-L: 1/4 members clear (instruct) -> 0 admissible model pairs; the emptiness IS the result and 'indicators track lineage, not safety' is withdrawn as stated. NEW: at the final-layer readout (recomputed here) 2/4 clear (instruct 0.912, abliterated 0.771) -> exactly 1 admissible pair, the safety-tuning pair, on which NO indicator separates (var* +0.008 [-0.082,+0.094], ac1 -0.003, flicker +0.165). Readout choice therefore decides whether any cross-model comparison exists. Instrument-vs-behaviour separated with experiment-2 token streams: token-level AUROC 0.935-1.000 pooled, so base/abliterated's low prompt-level AUROC is a BEHAVIOUR fact, not an instrument fault (caveat: 2-372 lexicon tokens per cell; no SmolLM2 stream).
  (3) SMALL-n CEILING, plus an unplanned finding: the archived rho_SPI=-0.20 vs rho_baseline=+0.40 REPRODUCES ONLY under an ordinal tie-break of the two models whose harmful refusal rate is identically 0.000. Tie-aware ranks give +0.105 and +0.632; tie-break range [-0.20,+0.40]. Exact 4!=24 permutation: two-sided p 1.000 / 0.500 against a floor of 2/24=0.0833 (0.1667 with ties), max |rho| 0.949, only 2 resolvable ground-truth levels.
  (4) AC1 LENGTH CONFOUND = VERIFICATION, NOT REPAIR: iteration 1 already used the Kendall-corrected field (matches for all 4 members); n_steps is 192 everywhere so nothing is length-manufactured; matched-length bootstrap at T=192 reproduces the picture on corrected and raw. EOS-hit fraction nevertheless varies 4x (0.0725-0.3175) across members.
  Cross-arm (analysis 5): both arms agree in sign (compliance sticks, refusal does not) but use different channels and different abliterated checkpoints - corroboration, not replication.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 10 ---
id: art_Qm_KL4GhZCnX
type: research
in_dependencies:
- id: art_0UsKSgsMHome
  label: extends
  relation_type: extends
  relation_rationale: >-
    Extends the baseline dossier with a 16-paper saturation search of the steering-strength-as-measurement lane.
title: Who Already Measured Steering Strength?
summary: |-
  Saturation-and-positioning dossier for the steering-strength-as-measurement lane. Deliverables: research_report.md (8 sections) and research_out.json carrying a 16-paper machine-readable F1-F5 table, four ready-to-paste paragraphs, and a 12-item consequences list. Every number is a verbatim quote with an [arXiv:ID section] anchor or marked NOT FOUND IN PRIMARY TEXT.

  SATURATION VERDICT: (b) ADJACENT WORK EXISTS. Nearest neighbour is Logit-Gap Steering (arXiv:2506.24056, Palo Alto Networks, preprint): 'the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step' = 'the per-prompt safety margin that alignment provides'. Same conceptual object as alpha_50, different units. NOT identical: toxic prompts only (all 520 AdvBench), position-1 only (their own coverage 92.1% [89.4-94.2], residual on multi-token preambles), per-prompt. Residual that is ours: benign-only, generation-level, model-level, NORM_L-normalised, paired instruct-minus-abliterated. Withdraw any 'first scalar measuring refusal's operational margin' sentence.

  BIGGEST CORRECTION: arXiv:2602.02712 (ICML 2026) is NOT a threat to the logistic fit - it is a theoretical endorsement. Theorem 3.6: target-concept probability 'is increasing in alpha'; Figure 4: increases 'with a sigmoidal shape'. The non-monotonic 'bump' of Theorem 3.3 is PER-TOKEN and for OFF-TARGET concepts; cross-entropy is locally quadratic (Thm 3.8). The real non-monotonicity threat is empirical coherence collapse (Rogue Scalpel, Falcon).

  GALEONE SAYS MORE THAN ASSUMED. Two abstract sentences absent from the brief: they test and REJECT the cosine as a steerability predictor ('a signature of the dissociation, not a control dial') and propose a functional criterion - the steerable case is where the intervention direction also detects (format AUC~1 vs hallucination AUC~0.7). Our 0.69-AUROC axis that DOES steer is a counterexample; report as 'in tension with', not 'refutes'. Their detection axis is prompt/lm_head and intervention axis is lm_head-only, so our result is an EXTENSION (both our axes activation-derived), not a replication. Free gifts: 'alpha does not transfer across models (Gemma needs 15, Llama needs |1|, Qwen needs 5)' supports H1'''; '0/100 random directions' at matched norm validates our null design; format steering works at '0.6% of the activation norm'.

  ROGUE SCALPEL DOES NOT WEAKEN THE NULL (author correction: Korznikov et al., NOT Kaminski). Identical calibration to ours - 'alpha = c*mu^(l)', c in {0.25...2.0} - so no conversion needed. Their effects live at 25-200% of activation norm vs 0.6% for a working intervention. 1-13% is a per-draw AVERAGE over 1,000 draws, not best-of-N. They never test random-induced REFUSAL on BENIGN prompts. No numeric lower floor exists in their text.

  BEST UNPLANNED FIND: arXiv:2608.08159 shows a 'steerability emerges with scale' result is manufactured by raw units and dissolves under exactly our normalisation ('alpha = c||h||_l', 'h' = h + c||h||_l d_hat'), warning the trend 'depends jointly on raw units, the readout metric, and the operating point; correcting any one of these removes it'. NORM_L is now a requirement, not a convenience - but we must also state what we do about readout metric and operating point.

  COMPETITOR NAMED: 'Has This Checkpoint Been Abliterated?' (arXiv:2607.01854) separates '57 public abliterations from 37 benign fine-tunes' at 'AUROC 0.95' on a '273-checkpoint registry' using activation refusal-gap + weight-recovery energy. It 'presumes an attested reference'; alpha_50 does not. No steering-strength abliteration metric exists.

  VENUES VERIFIED: 2602.02712=ICML 2026, 2608.08383=COLM 2026, 2607.23519=AIES 2026, 2606.22686='Accepted at TrustNLP 2026 (ACL 2026)', 2605.09043=ACL 2026 SRW. Title changes flagged: 2509.13450, 2508.21448, 2605.09043, 2606.22686. All others preprints.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 11 ---
id: art_3Cndd5cKsYV0
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: >-
    Draws the frozen 19-member panel, benign prompts and harmful rows for all four scores.
- id: art_Qm_KL4GhZCnX
  label: positioning
  relation_type: uses
  relation_rationale: >-
    Uses the dossier's Logit-Gap spec and positioning to pick the rival scores tested.
- id: art_0UsKSgsMHome
  label: baseline spec
  relation_type: uses
  relation_rationale: >-
    Reimplements AMS sigma to the dossier's published spec, including the 96-forward-pass budget.
title: Does our safety checklist tell good scores from bad?
summary: |-
  THE DISCRIMINATION MATRIX. Iteration 2's five-check falsification protocol failed alpha_50; that is only a result about alpha_50 if the protocol can separate a good score from a bad one. This artifact tests exactly that, running THREE cheap benchmark-free safety scores through the SAME five checks, on the SAME frozen 19-member / 7-lineage panel, with the SAME code: (i) alpha_50 (the incumbent, TRANSCRIBED from the archive), (ii) our-AMS sigma (our reimplementation of arXiv:2608.05578, recomputed), (iii) a Logit-Gap first-step refusal margin (our reimplementation of arXiv:2506.24056) in benign-only and plain-harmful variants. Ground truth is the archived judged plain-harmful refusal rate, never recomputed. $0 LLM spend; ~470 forward passes and ZERO generation per member; ~10 min total on one A4500.

  VERDICT: PROTOCOL_DOES_NOT_DISCRIMINATE (pre-registered as acceptable, not salvaged). Matrix, checks (1 lexical / 2 monotonicity / 3 depth / 4 jackknife / 5 scorer): alpha_50 F,F,P,P,F = 2/5, rho -0.208 [-0.545, 0.183]; our-AMS F,F,P,P,F = 2/5, rho 0.358 [-0.072, 0.709]; logit-gap benign F,F,F,F,F = 0/5, rho 0.101; logit-gap harmful F,F,F,P,F = 1/5, rho 0.667 [0.439, 0.904], perm p 0.0038, AUC 0.784. Rivals TIE alpha_50 rather than beat it, so the mandated sentence stands: the protocol must be reported as a limitations section, not as a contribution.

  FIVE HEADLINE FINDINGS, all computed not asserted. H2 is the load-bearing one: the score that predicts y_refusal BEST passes the FEWEST checks -- the cells measure stability and construct hygiene, not predictive validity, and the two come apart here. H3: the AMS PARAPHRASE REFIT tracks y BETTER than the sigma it reproduces (0.654 [0.289, 0.859] vs 0.358), with Spearman(refit, original) 0.833 and 6/19 verdict-class changes -- the lexical check is detecting real surface-form dependence, not noise. H4: check 5 fails identically in every row (REFUSAL annotator kappa 0.391 vs 0.60), capping everyone at 4/5; this was stated in the prereg BEFORE fitting and a checks-1-4-only sensitivity is reported. H5: reuse is MEASURED -- our-AMS recomputed from scratch reproduces the archived sigma on 19/19 members, max delta 2.4e-6.

  MEASURED CORRECTIONS to the plan (use these, not the plan's numbers): the panel holds 5 architecture families, NOT 6; the alpha_50 accounting is 19/18/1, NOT 19/17/1 (DEFINED 1, UNRELIABLE_NON_MONOTONE 6, UNDEFINED_MAX_RATE_BELOW_HALF 8, UNDEFINED_NONPOSITIVE_SLOPE 4); axis B DOES reach 0.50 on 2 of the 5 breadth members ('never reaches 0.50' is wrong, though check 1 still fails); there are 8 distinct lineage_id strings over 7 lineages (L7 base/instruct roots differ), so clustering on the id string would silently split L7; and the exhaustive lineage-permutation floor is 1/5040 = 1.98e-4, NOT 2/5040 -- only the identity permutation is guaranteed to reproduce |rho| when cluster blocks are unequal. One column (ams_sigma_para) lands exactly at that floor and is flagged.

  METHOD DETAILS worth reusing: prereg_iter3.json is sha256-stamped before any fit and carries the orientation map, every numeric threshold, and the acknowledgement that check 5 caps the count at 4. All correlations are reported oriented AND raw, with a full flipped-orientation matrix (no verdict depends on the choice). Resampling and permutation unit is the lineage label (7 units); permutation is exhaustive over all 5040 assignments. 80 paraphrases were hand-written and machine-checked for content-token disjointness against a frozen 60-word stoplist (80/80 pass); harmful_instruction harmful members are re-drawn uid-disjoint from outside the core-80. The logit lens is unit-tested against the model's own logits (error 1.7e-5); note HF's hidden_states[-1] is POST final-norm, so the norm must NOT be re-applied there. Real refusals open on tokens already in the frozen lexicon, so the token-set refit is usually UNDEFINED and a prompt refit carries check 1 for that row. Deliverables: method.py, RESULTS.md (rendered matrix), prereg_iter3.json, results/iter3_member_<key>.json x19, results/{reuse_manifest,t1_unit_tests,paraphrase_audit}.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 12 ---
id: art_SVp6BHC9m27h
type: evaluation
in_dependencies:
- id: art_r3PqOtpvcIsK
  label: reanalysis
  relation_type: differences
  relation_rationale: >-
    Overturns its held-out AUROC 1.000 certificate: axis A reads real refusals at only 0.486-0.790.
- id: art_sabuvuJ8P3Wy
  label: reanalysis
  relation_type: differences
  relation_rationale: >-
    Downgrades its lexicality verdict to MIXED and shows the certificate indicted axis A too.
- id: art_gYmQllaTCGT5
  label: scorer
  relation_type: uses
  relation_rationale: >-
    Uses the audited repaired judge and its sensitivity/specificity for semantic re-scoring.
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type: uses
  relation_rationale: Uses the frozen prompt sets and pinned checkpoint revisions for the re-encode.
title: Re-checking whether a refusal direction really reads refusal
summary: |-
  EVALUATION of the iteration-2 lexicality verdict, run as pure re-analysis of archived artifacts plus a forward-pass-only re-encode of already-logged text (no sampling, no new steered generation, no training). Six Qwen3 checkpoints (0.6B/1.7B x base/instruct/abliterated), pinned to the archived revision SHAs, bf16, one RTX A4500. OpenRouter spend $0.19 of a $1.50 cap. Pre-registration stamped BEFORE any AUROC (results/prereg_eval.json, 3 amendments each with when_decided).

  CRITICAL PRE-FLIGHT: axis vectors are not stored on disk, so all axes (A canned / B token-disjoint paraphrase / C norm-matched stylistic / D random / E prompt-contrast) were re-derived by re-running the archived fit code. V2 gate = STRICT_FAIL_SUBSTANTIVE_PASS: worst deviation from the archived summary statistics is 5.3e-3 relative (pre-registered gate 1e-3), while re-derivation is bit-exact WITHIN this run (self-delta 0.0), so the residual is a cross-run device difference (archive: RTX 4000 Ada; here: A4500), and the re-derived canned axis has cosine 0.9992 with an independently fitted float32 axis from the breadth panel. Random axes reproduce exactly from their stored seeds.

  HEADLINE, NOT ANTICIPATED BY THE BINARY RULE: the archived 'held-out AUROC 1.000' certificate over-stated axis A as well as axis B. On 7,241 re-encoded, AB-blind, model-generated items (stratum-centred projections, first-generated-token position, prompt-clustered bootstrap, n=2000), the canned axis A reaches only AUROC 0.486-0.790 -- CI excludes chance on 4 of 6 checkpoints, clears the whole [0.40,0.60] band on 1 (instruct_1p7), and sits AT CHANCE on both abliterated members. Axis B spans 0.386-0.602. Pre-registered lexicality verdict = MIXED (2/6 have upper CI(A-B) <= 0.10; 2/6 have A-B > 0.10 with CI excluding 0). Holm-adjusted p: instruct_0p6 and instruct_1p7 0.003, rest >= 0.10. Weak-estimate hypothesis directly falsified: R^2(s_B on s_A) <= 0.036 and the residual AUROC stays near chance, so B is not a scaled noisy copy of A. The stylistic control is not merely at chance -- on 4 checkpoints its CI lies entirely BELOW 0.5 (refusals score LOW on formal register) while it still induces 0.00 refusal when steered.

  MATCHED-CONTRAST (the reviewer's decisive quantity): steering convention extracted from the archived hook (h_L += alpha*NORM_L*x_hat), so c = alpha*NORM_L/raw_norm_X. A crosses 50% refusal at 0.91-1.57 contrast units; B is driven to 14.2-16.3 contrast units and tops out at 0.07-0.30. At MATCHED contrast units A stays above B by +0.36 to +0.61 with CIs excluding 0 on 6/6 -> NORM_MISMATCH_DOES_NOT_EXPLAIN. Every axis shows an inverted U; B's ceiling is not explained by fluency collapse on 5/6.

  SEMANTIC SCORING: re-scored with the repaired four-class judge, B crosses 0.5 on every checkpoint (PARTIAL_REVERSAL_UNDER_SEMANTIC_SCORING) -- but the clean controls (C, D), which induce 0.00 refusal under the regex, themselves draw judge REFUSAL rates up to 0.80, and a five-class rubric with an explicit non-canonical-refusal class puts most of B's high-alpha text in DEGENERATE (mean 0.711 vs 0.285 refusal of any wording; A: 0.667 refusal / 0.333 degenerate). Adjudicated verdict: REVERSAL_CONFOUNDED_BY_DEGENERACY. Judge sensitivity 0.688 / specificity 0.804 for REFUSAL against the blind-adjudicated audit truth; attenuation-corrected column ships alongside.

  GATES: V1 leakage 0 overlapping items on all six; V3 re-encoded refusal-logit margin reproduces the archived r_t_first at Pearson >= 0.9975 (fixed by concatenating token IDS rather than strings -- string concatenation let BPE merge across the prompt/completion boundary on up to 450/1028 plain-rendered base items); V4 all six powered (>= 40/class); V5 Holm; V7 accounting: 33,135 scanned -> 27,758 kept -> 7,241 re-encoded; V8 provenance map of 71 numbers with an EXECUTED assertion that no number in the deliverable prose is untraceable.

  SHIPPED: eval.py (7-stage orchestrator) + eval_lib/gpu_stage/analysis12/judge_stage/analysis34/assemble/figures, eval_out.json (exp_eval_sol_out validated; 330 examples over four datasets), results/{prereg_eval,provenance,analysis1-4,encode_*,axes/,proj/}, results/lexicality_subsection.md (drop-in paper subsection), results/b_axis_examples.md (40 verbatim boundary examples), 5 regenerated figures, pinned pyproject.toml.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 13 ---
id: art_ouNbQqPM59dp
type: evaluation
in_dependencies:
- id: art_sabuvuJ8P3Wy
  label: reanalysis
  relation_type: differences
  relation_rationale: >-
    Restates its headline Delta under sign orientation and corrects its 19/17/1 accounting to 19/14/1.
- id: art_r3PqOtpvcIsK
  label: reanalysis
  relation_type: differences
  relation_rationale: >-
    Reworks its composite and depth-panel correlations; the stage-1 gate contributes nothing.
- id: art_UthAQuH8WZ5C
  label: archive
  relation_type: uses
  relation_rationale: >-
    Reanalyses its archived rollout tree for the free-vs-forced asymmetry and tail characterisation.
- id: art_gYmQllaTCGT5
  label: scorer
  relation_type: uses
  relation_rationale: >-
    Uses its audited counts to recompute Wilson intervals and the attenuation caveat.
title: Redoing the headline safety stats honestly
summary: |-
  Pure reanalysis of the frozen iteration-1/2 trees: no GPU, no model loading, no API calls, $0.00, 55 s. Archived estimator code (lib/stats_ext, lib/dose) imported VERBATIM; rebuilt 7 lineage units match the archive to 1e-9 and the archived headline (Delta=-0.714 [-1.765,0.667]) reproduces to 3 dp before anything is restated.

  A1 SIGN ORIENTATION. Oriented Delta = -0.929 [-1.961,-0.113] (n=7 lineages, 5000 lineage bootstrap). CEILING CHECK: under the old raw statistic a PERFECT alpha_50 scored Delta = -1-0.821 = -1.821 (a catastrophic loss); oriented it scores +1-0.821 = +0.179 — the old comparison could not reward the ideal case. Wrong-sign claim DOWNGRADED per the pre-committed rule (bootstrap mass below 0 = 0.585, not >=0.90): 'indistinguishable from zero, point-estimated with the wrong sign'. Orientation-free comparators agree on point estimates only (AUC 0.833 our-AMS vs 0.250 alpha_50 — anti-predictive); |rho| difference CI includes 0, so nothing separates at n=7. Sign-flip recount: 6 of 11 enumerated analysis choices wrong-signed, 4 right, 1 undefined — the 'four times' sentence is retired. Depth panel oriented +0.257, exact permutation p=0.658 vs floor 0.00278 (720 orderings). Sign rule cited to E1 metadata.external_validity.ranking_agreement.expected_sign_if_metric_valid; the iteration-2 prereg fixes only the sign of the DIFFERENCE, never of either component — that gap is the defect.

  A2 ASYMMETRY (15/19 members, 5 lineages, 4 families; 1500 rollouts). The plan's expectation was WRONG in an instructive way: 61-88% of paired rollouts are EXACT ties (the perturbed free stream never diverged), forced strictly exceeds free in only 36/1500, and among diverging rollouts free wins 0.79-1.00. Sign test and Wilcoxon significant after Holm in 15/15 FAVOURING free among untied pairs. Medians decay in BOTH channels in 15/15 (free 0.199-0.783, forced 0.081-0.329); q95 delta positive 15/15; mean-diff CI excludes 0 in 15/15. 'Stochastic dominance' and 'deviation grows' retired; the effect is a right-tail effect CONDITIONAL ON DIVERGENCE. TAIL: not safety-relevant on any measured covariate (prompt chi2 p=0.084, member judged refusal rho=-0.221 [-0.392,0.315]); the only surviving association (token-divergence extent, r=0.50) is mechanical. Refusal-lexicon covariate NOT_RECOMPUTABLE (no archived survival token streams).

  A3 COMPOSITE. The plan's pointer was wrong: it is archived at E1 metadata.composite (6-checkpoint depth panel), score = 1/alpha_50 (verified every row). Its oriented rho is IDENTICAL to its alpha_50 component because 6/6 pass the gate — the gate contributes nothing — and stage 1 was withdrawn at power (both bases cross 0.50 at 0.64/0.84; gate-vs-class 0.67 of 6). Breadth-panel extension reported as a labelled reconstruction.

  A4 ACCOUNTING. The triple is 19 / 14 / 1, NOT 19/17/1 (5 UNRELIABLE excluded), and the single member with a defined logistic alpha_50 (l4_base) is itself UNRELIABLE, so after the pre-registered exclusion the primary estimator is defined on ZERO analysable members. AMS: 6/12 checkpoint x rule cells inside +-25%, per-checkpoint verdict PASS 3/3, ordering test vacuous at n=3 (floor 0.333); label kept. LAYERS: non-parametric 1.8x vs logistic 4.4x, logistic undefined at 1 of 5 layers and out-of-grid at 1 more, curve non-monotone at 4; misspecification diagnostic INCONCLUSIVE at 4 cells (said so rather than attributing). JUDGE: Wilson intervals recomputed from recovered counts — jailbreak ASR STANDS (0.800 [0.652,0.895], 32/40), plain-harmful RESTATED (0.000 [0.000,0.088], 0/40), pooled COMPLIANCE recall 29/117=0.248 [0.178,0.333]; attenuation caveat naming exactly which A1 correlations run against a REFUSAL-kappa-0.391 scorer.

  A5 CORRECTIONS OF RECORD: 13 appendix entries (each with old claim, corrected statement, file+key, why it moved), 15 E1 deviations / 12 E2 amendments / 8 V1 deviations, main-text reduction 16.1% (1592 words moved, 139 added back) — inside the 15-20% target, with donor paragraphs listed individually.

  SHIPPED: eval_out.json (exp_eval_sol_out-valid, 40 aggregate metrics, 3 datasets/29 rows, 31-file sha256 inputs manifest, 12-module reuse manifest, 15 limitations, 7 not_recomputable entries, zero non-finite numbers), out/replacement_text.md (14 old/new blocks GENERATED from the JSON with the JSON path of every number), out/appendix_corrections_of_record.md, out/main_text_stub.md, out/member_table.csv, and F1-F5 as vector PDF+PNG regenerated from the JSON.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 14 ---
id: art_PeyWw78NIx9d
type: research
in_dependencies:
- id: art_Qm_KL4GhZCnX
  label: extends
  relation_type: extends
  relation_rationale: >-
    Extends the iter-2 saturation dossier with five full-text papers on protocol-level prior art.
title: Where Our Steering Checks Meet Prior Work
summary: |-
  Primary-source positioning dossier for the five-check falsification protocol, extending the iter-2 dossier rather than repeating it. Deliverables: research_report.md (10 sections) and research_out.json carrying five full extraction records, a reconciliation object, a saturation object, ranked refutation risks, point-of-use sentences per protocol check, a Related Work paragraph, and 12 verified metadata rows. Every number is a verbatim quote with an [arXiv:ID section] anchor or marked NOT FOUND IN PRIMARY TEXT. All five planned papers were read in FULL TEXT.

  SATURATION VERDICT FOR THE PROTOCOL: adjacent work exists and is CLOSER than the plan assumed. Two concessions are now forced. arXiv:2607.28685 (Validity Audit of Agent-Safety Benchmarks) treats safety scores as measurements, separates 'construct validity ... metric validity ... criterion validity', runs a PRE-SPECIFIED positive control ('MMLU loads 0.74>=0.6') and negative control (column-permuted score matrix), and survives 'leave-one-organization-out and organization-clustered bootstrap' - the published counterpart of our check (4). arXiv:2605.06161 (Policy Invariance) operationalises 'rubric-semantics invariance under certified-equivalent rewrites' - the counterpart of our check (1) - and states the DISCRIMINATION requirement outright: judges 'respond to meaningful normative shifts and to meaningless structural rewrites with comparable strength, and cannot tell the two apart'. The checks-suite framing AND the discrimination requirement are prior art in kind. Residual: none of them audits a benchmark-free, model-level scalar read off activations, the class alpha_50 belongs to. Rewrite the novelty claim to the object audited plus the battery composition.

  RECONCILIATION: RECONCILED, on four legs, one decisive. arXiv:2602.06801 never studies refusal ('refus' = 0 matches in full text); its five traits are graded classifier scores (modulation, not induction); its criterion is graded (|d|<0.2) not a rate; and DECISIVELY its orthogonal test steers with 'v + v_perp versus v alone' - it never steers along v_perp alone, whereas our null steers a random direction by itself. Magnitude leg unverified (alpha in {0,0.5,1,2,3} raw, no activation norm reported). Pre-empt one qualifier: their App. B finds orthogonal shifts '27-53% smaller than random directions of the same norm', so random directions DO move logits; our claim is only that they do not cross a behavioural threshold.

  TOP REFUTATION RISK IS NEW AND WAS NOT ON THE PLAN'S RADAR. arXiv:2603.22061 shows a contrast-baseline change 'produces no functional refusal directions at any tested weight level on any tested layer' while unmatched contrast 'achieves complete refusal elimination on six layers', via 'reducing the extracted direction magnitude below the threshold at which weight-matrix projection perturbs the residual stream'. Our axis B norm 2.6-2.7 vs axis A 10.3-10.6 is the same signature, and arXiv:2602.17881 Sec 5.4 independently ties unreliability to smaller activation-difference norms. Settle it by re-running axis B at matched/unit norm BEFORE drafting; if the axis-contrast unit already normalises, say so in one sentence.

  arXiv:2602.02132 survives as a real but scope-limited threat: all 11 directions, including pairs at cos=0.127 and cos=-0.062, drive benign over-refusal to 0.88-1.00 and none fails. Reconciliation is by CONSTRUCTION (their directions are behaviour-labelled prompt contrasts at the decision-state token; ours is a wording paraphrase), and their result sharpens ours. AC-1 confirmed: the how-not-whether claim is theirs, NOT arXiv:2603.13359 (NOT FOUND IN PRIMARY TEXT there). AC-2: arXiv:2602.17881 is a Master's Thesis, University of Tuebingen.

  TWO FREE GIFTS. (a) LAP (arXiv:2604.15557) could NOT have predicted our failure ex ante - A_lin never sees the steering direction, so both axes score identically; refusal is only a demo; it is validated only on single-token completions. That is a residual for check (1), not a cross-reference. (b) arXiv:2604.02608 finds steering succeeds where the logit lens cannot decode across 4,032 pairs while the converse is 'nearly empty (3 of 72)', so the iter-2 Galeone tension weakens - our 0.69-AUROC steering axis is the common case.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 15 ---
id: art_CZaytBH8uL4_
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
- id: art_0UsKSgsMHome
  label: baseline spec
- id: art_PeyWw78NIx9d
  label: positioning
title: Testing a safety score on 52 models
summary: |-
  REPLICATION OF ITERATION 3'S ONE POSITIVE RESULT, AT SCALE. VERDICT: DOES_NOT_SURVIVE. Iteration 3 reported that refitting our AMS reimplementation's (arXiv:2608.05578) contrast set on token-disjoint paraphrases lifted Spearman rho with the judged plain-harmful refusal rate from 0.358 to 0.654 on 19 members / 7 lineages, where the exhaustive lineage-permutation floor is 1/5040. This run grew the panel to 52 analysed members over 28 weight lineages and 11 architecture families, added a second independently authored paraphrase set, and reported every correlation at BOTH aggregation units.

  HEADLINE NUMBERS (member level, lineage-clustered bootstrap, 10k reps). rho: original 0.359 [0.047, 0.592]; refit SET A 0.458 [0.197, 0.646]; refit SET B 0.207 [-0.110, 0.463]. Delta_A = +0.099 CI [-0.027, 0.244] (was +0.296) -> R1 FAILS. Delta_B = -0.152 CI [-0.488, 0.075] -> R3 FAILS: the independently authored wording does not merely fail to replicate the gain, it is WORSE than the unrefit baseline. Permutation p for Delta_A = 0.135 against a floor of 5.0e-6 (Monte Carlo, 200k draws) -> R4 FAILS, and the 1/5040 floor is genuinely retired by the larger panel. Only R2 passes (rho refit A >= 0.40 with CI excluding 0). Verdict-class change rate (descriptive) 12/52 = 0.231 [0.137, 0.361] vs the archived 6/19.

  THE DECISIVE DIAGNOSTIC. The archived 19-member block reproduces Delta_A = +0.2963 (gap 2.6e-04 to iteration 3's +0.296), while the 33 NEW members give -0.016 [-0.144, 0.130]. Per block: rho 0.358 -> 0.654 archived, 0.402 -> 0.386 new. The entire effect lives in the original small panel; this is a small-panel artifact, not a property of token-disjointness. Leave-one-lineage-out (28 folds) and leave-one-family-out (11 folds) never flip the sign of the shrunken Delta_A (ranges [0.068, 0.122] and [0.060, 0.137]), so the null is not driven by one outlier.

  REUSE PROVEN BEHAVIOURALLY, NOT JUST BY HASH. Every lib/ and lib_iter3/ file is sha256-identical to source (hard failure otherwise). Beyond that: our AMS reimplementation recomputed from scratch matches the iteration-2 archive on 19/19 members (max abs delta 2.4e-06); the SET-A refit matches iteration 3 on 19/19 (delta exactly 0.0); and both cross-pipeline calibration members regenerate byte-identically (100% judge-cache hit, y reproduced exactly, Wilson CIs identical), which is what licenses pooling the archived and newly measured y blocks.

  PARAPHRASE SET B. Generated by openai/gpt-5.6-luna (never the judge model) at temperature 0.3, verified by the FROZEN iteration-3 check_pair() with zero hand-written repairs: 80/80 strings pass (78 on the first attempt), 16/16 pairs kept, $0.0062. Measured wording independence: content-token Jaccard(SET A, SET B) = 0.201. Its 16 fresh harmful positives are uid-disjoint from both the core-80 and SET A's block.

  DUAL-AGGREGATION (H-U repair). The SIGN of rho survives the choice of unit on all three scores, but the CI's exclusion of 0 does NOT: at the member level orig and refit A exclude 0, at the lineage-aggregated unit none of the three does (rho 0.162 / 0.224 / 0.013). Any claim resting on CI exclusion is unit-dependent here.

  AMS TABLE-I GATE (our reimplementation vs published): Llama-3.2-1B-Instruct 4.274 vs 4.55 (-6%), gemma-2-2b-it 5.845 vs 4.80 (+22%), Llama-3.2-3B-Instruct 5.010 vs 8.37 (-40%). The label 'our AMS reimplementation' is kept regardless.

  DELIVERABLES: method.py (single driver), build_para_b.py, summarise.py, prereg_iter4.json (sha256-stamped before any correlation, plus a timestamp-free content sha stable across reruns), para_set_b.json, method_out.json (+ full/mini/preview, schema-valid), RESULTS.md (every number read from the JSON, never retyped), README.md, 54 per-member JSONs, 35 generation files, panel_selection.json (every rejection with a machine-readable reason), gt_calibration.json, t0_unit_tests.json (10/10), and results/t4_archive_only_method_out.json (the dry run reproducing iteration 3 exactly).

  CAVEATS FOR DOWNSTREAM USE. (1) y_refusal's REFUSAL one-vs-rest annotator kappa is 0.3907 (< 0.60); disattenuated rho is reported alongside raw, never instead of it. (2) Two enrolled checkpoints are unrecoverable upstream incompatibilities, recorded with their exception strings, costing one lineage: UnfilteredAI/NSFW-flash (StableLM attention shape mismatch under transformers 5.15) and cognitivecomputations/TinyDolphin-2.8-1.1b (SentencePiece tokenizer.model misparsed as tiktoken; installing tiktoken does not fix it). (3) The pre-registered lineage-collapse rule fired 0 times because the manifest's lineage_evidence is empty on the TinyLlama rows; that one collapse is inherited from the frozen iteration-2/3 labelling and is flagged as such. (4) Total spend $0.1334 against a $3.00 cap. (5) The frozen statsx.auc_binary splits y at its MEDIAN, not 0.5; both splits are reported and neither enters the decision rule.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 16 ---
id: art_1xT3w1joqeJ8
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
- id: art_PeyWw78NIx9d
  label: positioning
- id: art_Qm_KL4GhZCnX
  label: positioning
title: Does the refusal axis read or only push?
summary: |-
  EXECUTED on 30 checkpoints over 7 lineages (~3.5 h, 1x RTX A4500, $0.0099 OpenRouter). Each member measured in BOTH roles of the SAME five axes (A canned-response contrast, B token-disjoint paraphrase, C stylistic, D norm-matched random, E prompt contrast): DETECTION = held-out AUROC of the axis projection on the model's OWN generated text, stratum-centred, prompt-clustered bootstrap; INDUCTION = steering sweep in axis-contrast units c = alpha*NORM_L/||d_raw||.

  HEADLINE IS A REVERSAL of the iteration-3 result this set out to strengthen. 18 of 30 members return READS, **0 return AT_CHANCE**, 10 UNDEFINED. Every measurable member reads at AUROC >= 0.68. K = 0 of M = 4, so the pre-registered K<3 branch fires: the iteration-3 n=2 'at chance as a reader while still inducing' claim must be DOWNGRADED. The reason is STRUCTURAL, not statistical -- 14 of 18 abliterated-class checkpoints never produced 40 spontaneous refusals even after the full escalation ladder (1,585 generations each; median spontaneous refusal rate 0.008). Abliteration removes the refusals to be read, not the axis's ability to read them. Iteration 3 differed because its item pool contained STEERED and archived text; scoring each model's own spontaneous text flips it.

  H1b (the arm that IS measurable): across 10 within-lineage abliterated-vs-parent pairs, steering still induces on 5 abliterated checkpoints and FAILS on 4 whose parent was steerable (median delta max-rate -0.306). H2: 1 of 2 breadth-panel counterexamples is a genuine inducer, 1 a norm artifact. H3 (the study's first joint read-vs-act scatter): NOT null -- rho = 0.629 [0.465, 0.803], lineage bootstrap, over 70 (member, axis) pairs vs the previous evidence base of 4; within-member mean rho 0.715; c_50 censoring 0.771. Matched contrast gives NORM_MISMATCH_DOES_NOT_EXPLAIN on 22 of 30, ruling out arXiv:2603.22061's magnitude-collapse account.

  METHOD FACTS worth reusing: (1) archived relative depth is 0.25, NOT the plan's 0.30 (all six archived checkpoints are L=7 of 28). (2) c = alpha*NORM_L/||d_raw|| is EXACT on 459 archived analysis2 cells (error 0.0). (3) Base models MUST use the plain wrapper -- Qwen3-*-Base tokenizers ship a chat template despite never being tuned to follow one, and 'auto' selection dropped axis-E reproduction cosine to 0.13/0.09; fixed, all six archived checkpoints reproduce at >= 0.99992.

  TWO NULL-DESIGN CORRECTIONS (recorded amendments): a raw projection is ||h||*cos(angle), so ANY direction inherits a refusal-vs-compliance NORM difference (a random axis 'read' at 0.171) -- a norm-controlled cos = (h.u)/||h|| readout is now computed for every axis on every member; and ONE random draw is not a null distribution, since residual streams are anisotropic (measured 20-draw band spans +/-0.075 to +/-0.500 across members). Measured floor: a random direction at axis A's matched magnitude induces refusal >= 0.10 on 7 of 30 members (worst 0.389) -- a floor any steering claim must clear.

  PROVENANCE: prereg sha256-stamped before any new AUROC; T1 replays the archived analysis EXACTLY with no model (A 0.6620 / B 0.5102 / paired +0.1518); T2 exact on 459 cells; T3 shows the archived string-concat boundary bug bites 34/50 items under the plain wrapper and 0/50 under chat (token-id concat avoided 943 merges panel-wide); judge kappa 0.600 (regex stays primary); RESULTS.md regenerates BYTE-IDENTICALLY from method_out.json, so no prose number is hand-typed. lib/*.py is a byte-identical (sha256-matched) copy of the iteration-3 archive; the GPU stage is reimplemented and validated against it. 4 members failed with distinct logged causes. Deliverables: method_out.json (schema-validated), RESULTS.md (tables T1-T6), 3 vector figures, per-member checkpoints in results/.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 17 ---
id: art__tq3ZgPRYB0B
type: evaluation
in_dependencies:
- id: art_3Cndd5cKsYV0
  label: reanalysis
- id: art_sabuvuJ8P3Wy
  label: archive
- id: art_r3PqOtpvcIsK
  label: archive
- id: art_CKWQh2cOQLLQ
  label: dataset
title: The same number, counted two ways
summary: |-
  A pure-reanalysis EVALUATION over the FROZEN iteration-2/3 archives. Zero GPU, zero generation, zero LLM/API spend (cost_usd = 0.0), no downloads, no network, no torch import; the whole pipeline runs end-to-end in 125 s via `uv run eval.py` (stages 0-5, each independently re-runnable). Output validates against exp_eval_sol_out: 7 datasets / 209 examples / 40 aggregate metrics.

  REPRODUCTION GATE: 11/11 legs PASS to 1e-6. All four E3 discrimination-matrix oriented rho values (alpha_50 -0.2081, our-AMS 0.3578, logit-gap benign 0.1011, harmful 0.6673), the AMS paraphrase refit 0.6541, and V2's lineage-level Delta -0.9286 / rho(our-AMS) 0.8214 / rho(alpha_50) -0.1071 all regenerate from sha256-stamped inputs. Accounting legs 19/18/1 and 19/14/1 reproduce, as does the fact that the one member with a DEFINED logistic alpha_50 is itself among the five UNRELIABLE exclusions.

  ANALYSIS 1 (the H-U repair). The draft's 0.358 (S5.2) and 0.821 (S5.3) are ONE statistic at two aggregation units, neither of which the draft names. Across the 16 score x config cells where both units are defined, changing nothing but the unit moves oriented rho by a median 0.238 and a maximum 0.557, and FLIPS THE SIGN on 5. Oriented Delta emits SIGN_SURVIVES / EXCLUSION_LOST_AT_MEMBER_LEVEL on V2's carrier (-0.929 [-1.961,-0.113] lineage vs -0.376 [-0.795, 0.110] member), and SIGN_FLIPS / EXCLUDES_AT_NEITHER on the discrimination matrix's own carrier (-0.566 member vs +0.107 lineage). The plan's -0.465 estimate is NOT reproduced and nothing was tuned toward it. Ceiling, |rho| difference with CI, median-split AUC pair, per-column ICC, members-per-lineage, and the lineage-mean reconciliation check all ship. Every cell states n, the exhaustive 7! = 5040 lineage permutation p and the corrected floor 1/5040 = 1.98e-04; CIs are suppressed at n_lineages <= 3.

  ANALYSIS 2 (threshold surface, 164,736-point full factorial). Under the pre-registered rule PROTOCOL_DOES_NOT_DISCRIMINATE holds on 1.0000 of grid points (strict-exceed criterion 0.9091, checks-1-4-only 1.0000). Dropping the pass rules' secondary clauses and scoring the numeric cutoffs alone gives 0.5802 / 0.2429 -- which LOCATES the negative result in the verdict-class and interiority clauses, not the cutoffs. Exactly ONE single-axis change anywhere on the grid produces a strict rival win (check 3, 2.0 -> 1.75, our-AMS 2 vs alpha_50 1). Check 5's kappa 0.391 lies below the entire swept range [0.40, 0.80], so it can never change any verdict -- proved structurally and verified empirically. A 40-row marginal flip table and the named check-1 case ship.

  ANALYSIS 3: three tables as md AND csv, generated from json so prose cannot drift -- table1 discrimination matrix (with audit cost), table2 per-checkpoint depth-panel dissociation (with the breadth-panel axis-B scope footnote), table3 dual aggregation (32 rows, unit in every row label).

  ANALYSIS 4: 57 correlation/AUROC/Delta/CI claims audited in the draft -- 18 TRACEABLE_UNIT_STATED, 31 TRACEABLE_UNIT_MISSING, 3 VALUE_MISMATCH, 5 UNTRACEABLE. The generated out/replacement_text.md re-audits at 13/13 traceable with an EMPTY flag list; three prose number-dumps are named for supplementary with their replacement table.

  DISCOVERED, not inherited: the outcome variable itself disagrees across the two frozen archives on 3 of 19 members (l1/l2/l4_base; the iteration-2 archive records an identical 12/80 = 0.15, V2 re-derives from a larger judged pool). All three are UNRELIABLE-excluded so no reported correlation moves; it is stated in metadata.gaps.

  MECHANICS worth reusing: E3/method.py is NOT import-safe (imports torch, calls setrlimit at import), so PASS_RULES / ORIENTATION_MAP are loaded by exec-ing only the literal constant blocks, cross-checked against prereg_iter3.json. The plan's estimator list lives in E3/lib_iter3/statsx.py, not lib/stats_ext.py. V2's lineage units use a rank-bottom sentinel (max(defined)+1, recovered from V2/eval_a34.py) over the 14 reliable members -- without it V2's headline does not reproduce.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 18 ---
id: art_P-_YL8tdIwqF
type: evaluation
in_dependencies:
- id: art_r3PqOtpvcIsK
  label: archive
- id: art_gYmQllaTCGT5
  label: scorer
- id: art_sabuvuJ8P3Wy
  label: archive
title: Does garbled text fake the refusal reversal?
summary: |-
  PURE RE-ANALYSIS (no new sampling, no weights, CPU-only, $0.674 of a $1.50 judge cap) that converts the standing verdict REVERSAL_CONFOUNDED_BY_DEGENERACY into numbers. It re-applies the ARCHIVED lexical screen (classify.fluency_ok, distinct-3 >= 0.50 and max 5-gram repeat <= 3 on generated token ids) to all 45,900 archived steered generations on 6 Qwen3 checkpoints x axes {A_canned, B_paraphrase, C_stylistic, D_random*, E_prompt_contrast}, then judges ONLY the survivors at matched axis-contrast units under two rubrics (the archived four-class and the five-class one carrying REFUSAL_NONCANONICAL), 6,536 items x 2 rubrics, 11,866 calls, parse rate 1.000.

  HEADLINE: REVERSAL_DOES_NOT_SURVIVE, 6/6 checkpoints and pooled, at matched contrast. B's five-class ANY-REFUSAL is 0.028 [0.008, 0.057] against A's 0.747 [0.618, 0.858], with the control false-positive floor at 0.146 set by the RANDOM axis D; NET = B - floor = -0.118 [-0.157, -0.082] (paired prompt-clustered bootstrap, 5000 reps) -- B sits BELOW what a meaningless direction induces on the same filtered population.

  THE DEGENERACY STORY IS THE OPPOSITE OF THE STANDING VERDICT, and is now quantified three ways. (1) At matched contrast the screen removes NOTHING: retention is 1.00 for every axis, so B's near-zero rate is absence of effect, not filtering. (2) At B's own maximum coefficient (~15 contrast units) retention falls to 0.705 AND 70.2% of the text that PASSES the screen is still judge-DEGENERATE, against 0.711 unfiltered -- the lexical screen removes essentially none of the residual degeneracy because the failure is semantic, not lexical. (3) The control floor is itself made of screen-passing degenerate text: 59.0% of D_random's matched-cell survivors are judge-DEGENERATE, which is exactly why a B rate reported without a same-population floor is uninterpretable.

  A THIRD, PRE-REGISTERED LEVEL SPLITS THE VERDICT AND IS THE PAPER'S NUANCE: at B's own peak-rate coefficient (5.2 contrast units, ~4.3x the intervention A needs) B DOES clear the floor on fluent text -- 0.642 vs floor 0.077, NET +0.565 [+0.471, +0.655], DEGENERATE only 0.049 -> REVERSAL_SURVIVES 6/6. So B's apparent reversal is real but lives entirely at coefficients that matching forbids.

  ALSO SHIPPED: exact reproduction of the archived contrast-unit conversion (54 cells, 0.0 abs error); recomputed-vs-archived screen agreement 0.9987 (tokenizer-only loads) so the recomputed screen is primary; three scoring criteria side by side (anchored regex / four-class / five-class) with kappa between them (matched level: A 0.424, B 0.108, D 0.020 -- the lexical and semantic criteria barely agree); Rogan-Gladen correction with se=0.688 sp=0.804 reproduced from the audit, reported ALONGSIDE the raw rate, with its TRUNCATION explicitly flagged at the matched level (both B and the floor fall below 1-sp = 0.196, so the corrected NET is 0 by construction, not measurement) and a se/sp +/-0.05 sweep; a drop-in replacement paragraph for the paper's semantic-scoring passage; 20 verbatim boundary examples (6 B, 8 C/D, 6 A); three figures (retention-vs-contrast panel, NET forest, three-criteria bars); full pre-registration with sha256 of every consumed artifact and 4 deviations each stamped when_decided='before'.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 19 ---
id: art_G5SIDXT53EAW
type: research
in_dependencies:
- id: art_PeyWw78NIx9d
  label: extends
- id: art_Qm_KL4GhZCnX
  label: extends
title: Reading the closest rival paper and fixing our citations
summary: >-
  Primary-full-text dossier on arXiv:2607.13346 ('The Refusal Residue', Aman Mehta, ICML 2026 MI Workshop) plus a machine-verified
  audit of all 22 cited 2026 arXiv IDs, two saturation sweeps and a novelty check on the paraphrase-refit headline. Verdict:
  MIRROR IMAGE, weaker as a neighbour than its abstract implies (the dissociation is assembled across two models; probe is
  an MLP, steered object a unit diff-in-means vector; no abliterated arm; no activation norm reported so units are NOT convertible;
  '|h|' is Cohen's h). One concession forced: they steer a refusal axis and get a null. 9 of 21 cited 2026 entries are wrong,
  worst being a mis-titled [23]. New mandatory citation found: arXiv:2603.27412 LatentBiopsy, which already runs base/instruct/abliterated
  Qwen triplets. Deliverables: research_report.md (10 sections: headline verdict, full Part-A extraction dossier with an 8-row
  AUROC grid and a 7-row control-comparison table, the closeness verdict, three paste-ready artefacts, the 22-row audit table
  plus a corrected BibTeX block, the C1/C2 sweeps with verbatim query strings, the Part-D verdict, two separate residual-novelty
  paragraphs, and a confidence section listing every zero-match regex) and research_out.json with machine-readable versions
  of all of it. Key corrections downstream must act on: (1) their '|h| < 0.08' is COHEN'S h on compliance proportions, not
  a hidden state; (2) their detect-without-control is assembled across two models (0.870 Llama vs 0.425 Qwen) and their probe
  is an MLP, not the steered vector, so our within-model single-axis dissociation survives; (3) their steering scale is NOT
  convertible to NORM_L units - no activation norm is reported anywhere; (4) they DO steer a refusal axis and get a null,
  which must be conceded and distinguished; (5) nine of 21 cited 2026 entries are wrong, worst being reference [23], whose
  cited title is not the paper's title; (6) arXiv:2603.27412 (LatentBiopsy) already runs base/instruct/abliterated Qwen triplets,
  so any 'first activation score on abliterated checkpoints' claim must go - the surviving claim is that the refusal axis
  specifically dies in both roles while harm-intent geometry survives; (7) one action item before drafting: verify our AUROCs
  are not computed over the same items used to fit or normalise the axis, the leakage that moved Mehta's own number from 0.761
  to 0.425.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 5 artifacts were created THIS iteration.

id: art_CZaytBH8uL4_
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
- id: art_0UsKSgsMHome
  label: baseline spec
- id: art_PeyWw78NIx9d
  label: positioning
title: Testing a safety score on 52 models
summary: |-
  REPLICATION OF ITERATION 3'S ONE POSITIVE RESULT, AT SCALE. VERDICT: DOES_NOT_SURVIVE. Iteration 3 reported that refitting our AMS reimplementation's (arXiv:2608.05578) contrast set on token-disjoint paraphrases lifted Spearman rho with the judged plain-harmful refusal rate from 0.358 to 0.654 on 19 members / 7 lineages, where the exhaustive lineage-permutation floor is 1/5040. This run grew the panel to 52 analysed members over 28 weight lineages and 11 architecture families, added a second independently authored paraphrase set, and reported every correlation at BOTH aggregation units.

  HEADLINE NUMBERS (member level, lineage-clustered bootstrap, 10k reps). rho: original 0.359 [0.047, 0.592]; refit SET A 0.458 [0.197, 0.646]; refit SET B 0.207 [-0.110, 0.463]. Delta_A = +0.099 CI [-0.027, 0.244] (was +0.296) -> R1 FAILS. Delta_B = -0.152 CI [-0.488, 0.075] -> R3 FAILS: the independently authored wording does not merely fail to replicate the gain, it is WORSE than the unrefit baseline. Permutation p for Delta_A = 0.135 against a floor of 5.0e-6 (Monte Carlo, 200k draws) -> R4 FAILS, and the 1/5040 floor is genuinely retired by the larger panel. Only R2 passes (rho refit A >= 0.40 with CI excluding 0). Verdict-class change rate (descriptive) 12/52 = 0.231 [0.137, 0.361] vs the archived 6/19.

  THE DECISIVE DIAGNOSTIC. The archived 19-member block reproduces Delta_A = +0.2963 (gap 2.6e-04 to iteration 3's +0.296), while the 33 NEW members give -0.016 [-0.144, 0.130]. Per block: rho 0.358 -> 0.654 archived, 0.402 -> 0.386 new. The entire effect lives in the original small panel; this is a small-panel artifact, not a property of token-disjointness. Leave-one-lineage-out (28 folds) and leave-one-family-out (11 folds) never flip the sign of the shrunken Delta_A (ranges [0.068, 0.122] and [0.060, 0.137]), so the null is not driven by one outlier.

  REUSE PROVEN BEHAVIOURALLY, NOT JUST BY HASH. Every lib/ and lib_iter3/ file is sha256-identical to source (hard failure otherwise). Beyond that: our AMS reimplementation recomputed from scratch matches the iteration-2 archive on 19/19 members (max abs delta 2.4e-06); the SET-A refit matches iteration 3 on 19/19 (delta exactly 0.0); and both cross-pipeline calibration members regenerate byte-identically (100% judge-cache hit, y reproduced exactly, Wilson CIs identical), which is what licenses pooling the archived and newly measured y blocks.

  PARAPHRASE SET B. Generated by openai/gpt-5.6-luna (never the judge model) at temperature 0.3, verified by the FROZEN iteration-3 check_pair() with zero hand-written repairs: 80/80 strings pass (78 on the first attempt), 16/16 pairs kept, $0.0062. Measured wording independence: content-token Jaccard(SET A, SET B) = 0.201. Its 16 fresh harmful positives are uid-disjoint from both the core-80 and SET A's block.

  DUAL-AGGREGATION (H-U repair). The SIGN of rho survives the choice of unit on all three scores, but the CI's exclusion of 0 does NOT: at the member level orig and refit A exclude 0, at the lineage-aggregated unit none of the three does (rho 0.162 / 0.224 / 0.013). Any claim resting on CI exclusion is unit-dependent here.

  AMS TABLE-I GATE (our reimplementation vs published): Llama-3.2-1B-Instruct 4.274 vs 4.55 (-6%), gemma-2-2b-it 5.845 vs 4.80 (+22%), Llama-3.2-3B-Instruct 5.010 vs 8.37 (-40%). The label 'our AMS reimplementation' is kept regardless.

  DELIVERABLES: method.py (single driver), build_para_b.py, summarise.py, prereg_iter4.json (sha256-stamped before any correlation, plus a timestamp-free content sha stable across reruns), para_set_b.json, method_out.json (+ full/mini/preview, schema-valid), RESULTS.md (every number read from the JSON, never retyped), README.md, 54 per-member JSONs, 35 generation files, panel_selection.json (every rejection with a machine-readable reason), gt_calibration.json, t0_unit_tests.json (10/10), and results/t4_archive_only_method_out.json (the dry run reproducing iteration 3 exactly).

  CAVEATS FOR DOWNSTREAM USE. (1) y_refusal's REFUSAL one-vs-rest annotator kappa is 0.3907 (< 0.60); disattenuated rho is reported alongside raw, never instead of it. (2) Two enrolled checkpoints are unrecoverable upstream incompatibilities, recorded with their exception strings, costing one lineage: UnfilteredAI/NSFW-flash (StableLM attention shape mismatch under transformers 5.15) and cognitivecomputations/TinyDolphin-2.8-1.1b (SentencePiece tokenizer.model misparsed as tiktoken; installing tiktoken does not fix it). (3) The pre-registered lineage-collapse rule fired 0 times because the manifest's lineage_evidence is empty on the TinyLlama rows; that one collapse is inherited from the frozen iteration-2/3 labelling and is flagged as such. (4) Total spend $0.1334 against a $3.00 cap. (5) The frozen statsx.auc_binary splits y at its MEDIAN, not 0.5; both splits are reported and neither enters the decision rule.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_1xT3w1joqeJ8
type: experiment
in_dependencies:
- id: art_CKWQh2cOQLLQ
  label: dataset
- id: art_PeyWw78NIx9d
  label: positioning
- id: art_Qm_KL4GhZCnX
  label: positioning
title: Does the refusal axis read or only push?
summary: |-
  EXECUTED on 30 checkpoints over 7 lineages (~3.5 h, 1x RTX A4500, $0.0099 OpenRouter). Each member measured in BOTH roles of the SAME five axes (A canned-response contrast, B token-disjoint paraphrase, C stylistic, D norm-matched random, E prompt contrast): DETECTION = held-out AUROC of the axis projection on the model's OWN generated text, stratum-centred, prompt-clustered bootstrap; INDUCTION = steering sweep in axis-contrast units c = alpha*NORM_L/||d_raw||.

  HEADLINE IS A REVERSAL of the iteration-3 result this set out to strengthen. 18 of 30 members return READS, **0 return AT_CHANCE**, 10 UNDEFINED. Every measurable member reads at AUROC >= 0.68. K = 0 of M = 4, so the pre-registered K<3 branch fires: the iteration-3 n=2 'at chance as a reader while still inducing' claim must be DOWNGRADED. The reason is STRUCTURAL, not statistical -- 14 of 18 abliterated-class checkpoints never produced 40 spontaneous refusals even after the full escalation ladder (1,585 generations each; median spontaneous refusal rate 0.008). Abliteration removes the refusals to be read, not the axis's ability to read them. Iteration 3 differed because its item pool contained STEERED and archived text; scoring each model's own spontaneous text flips it.

  H1b (the arm that IS measurable): across 10 within-lineage abliterated-vs-parent pairs, steering still induces on 5 abliterated checkpoints and FAILS on 4 whose parent was steerable (median delta max-rate -0.306). H2: 1 of 2 breadth-panel counterexamples is a genuine inducer, 1 a norm artifact. H3 (the study's first joint read-vs-act scatter): NOT null -- rho = 0.629 [0.465, 0.803], lineage bootstrap, over 70 (member, axis) pairs vs the previous evidence base of 4; within-member mean rho 0.715; c_50 censoring 0.771. Matched contrast gives NORM_MISMATCH_DOES_NOT_EXPLAIN on 22 of 30, ruling out arXiv:2603.22061's magnitude-collapse account.

  METHOD FACTS worth reusing: (1) archived relative depth is 0.25, NOT the plan's 0.30 (all six archived checkpoints are L=7 of 28). (2) c = alpha*NORM_L/||d_raw|| is EXACT on 459 archived analysis2 cells (error 0.0). (3) Base models MUST use the plain wrapper -- Qwen3-*-Base tokenizers ship a chat template despite never being tuned to follow one, and 'auto' selection dropped axis-E reproduction cosine to 0.13/0.09; fixed, all six archived checkpoints reproduce at >= 0.99992.

  TWO NULL-DESIGN CORRECTIONS (recorded amendments): a raw projection is ||h||*cos(angle), so ANY direction inherits a refusal-vs-compliance NORM difference (a random axis 'read' at 0.171) -- a norm-controlled cos = (h.u)/||h|| readout is now computed for every axis on every member; and ONE random draw is not a null distribution, since residual streams are anisotropic (measured 20-draw band spans +/-0.075 to +/-0.500 across members). Measured floor: a random direction at axis A's matched magnitude induces refusal >= 0.10 on 7 of 30 members (worst 0.389) -- a floor any steering claim must clear.

  PROVENANCE: prereg sha256-stamped before any new AUROC; T1 replays the archived analysis EXACTLY with no model (A 0.6620 / B 0.5102 / paired +0.1518); T2 exact on 459 cells; T3 shows the archived string-concat boundary bug bites 34/50 items under the plain wrapper and 0/50 under chat (token-id concat avoided 943 merges panel-wide); judge kappa 0.600 (regex stays primary); RESULTS.md regenerates BYTE-IDENTICALLY from method_out.json, so no prose number is hand-typed. lib/*.py is a byte-identical (sha256-matched) copy of the iteration-3 archive; the GPU stage is reimplemented and validated against it. 4 members failed with distinct logged causes. Deliverables: method_out.json (schema-validated), RESULTS.md (tables T1-T6), 3 vector figures, per-member checkpoints in results/.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art__tq3ZgPRYB0B
type: evaluation
in_dependencies:
- id: art_3Cndd5cKsYV0
  label: reanalysis
- id: art_sabuvuJ8P3Wy
  label: archive
- id: art_r3PqOtpvcIsK
  label: archive
- id: art_CKWQh2cOQLLQ
  label: dataset
title: The same number, counted two ways
summary: |-
  A pure-reanalysis EVALUATION over the FROZEN iteration-2/3 archives. Zero GPU, zero generation, zero LLM/API spend (cost_usd = 0.0), no downloads, no network, no torch import; the whole pipeline runs end-to-end in 125 s via `uv run eval.py` (stages 0-5, each independently re-runnable). Output validates against exp_eval_sol_out: 7 datasets / 209 examples / 40 aggregate metrics.

  REPRODUCTION GATE: 11/11 legs PASS to 1e-6. All four E3 discrimination-matrix oriented rho values (alpha_50 -0.2081, our-AMS 0.3578, logit-gap benign 0.1011, harmful 0.6673), the AMS paraphrase refit 0.6541, and V2's lineage-level Delta -0.9286 / rho(our-AMS) 0.8214 / rho(alpha_50) -0.1071 all regenerate from sha256-stamped inputs. Accounting legs 19/18/1 and 19/14/1 reproduce, as does the fact that the one member with a DEFINED logistic alpha_50 is itself among the five UNRELIABLE exclusions.

  ANALYSIS 1 (the H-U repair). The draft's 0.358 (S5.2) and 0.821 (S5.3) are ONE statistic at two aggregation units, neither of which the draft names. Across the 16 score x config cells where both units are defined, changing nothing but the unit moves oriented rho by a median 0.238 and a maximum 0.557, and FLIPS THE SIGN on 5. Oriented Delta emits SIGN_SURVIVES / EXCLUSION_LOST_AT_MEMBER_LEVEL on V2's carrier (-0.929 [-1.961,-0.113] lineage vs -0.376 [-0.795, 0.110] member), and SIGN_FLIPS / EXCLUDES_AT_NEITHER on the discrimination matrix's own carrier (-0.566 member vs +0.107 lineage). The plan's -0.465 estimate is NOT reproduced and nothing was tuned toward it. Ceiling, |rho| difference with CI, median-split AUC pair, per-column ICC, members-per-lineage, and the lineage-mean reconciliation check all ship. Every cell states n, the exhaustive 7! = 5040 lineage permutation p and the corrected floor 1/5040 = 1.98e-04; CIs are suppressed at n_lineages <= 3.

  ANALYSIS 2 (threshold surface, 164,736-point full factorial). Under the pre-registered rule PROTOCOL_DOES_NOT_DISCRIMINATE holds on 1.0000 of grid points (strict-exceed criterion 0.9091, checks-1-4-only 1.0000). Dropping the pass rules' secondary clauses and scoring the numeric cutoffs alone gives 0.5802 / 0.2429 -- which LOCATES the negative result in the verdict-class and interiority clauses, not the cutoffs. Exactly ONE single-axis change anywhere on the grid produces a strict rival win (check 3, 2.0 -> 1.75, our-AMS 2 vs alpha_50 1). Check 5's kappa 0.391 lies below the entire swept range [0.40, 0.80], so it can never change any verdict -- proved structurally and verified empirically. A 40-row marginal flip table and the named check-1 case ship.

  ANALYSIS 3: three tables as md AND csv, generated from json so prose cannot drift -- table1 discrimination matrix (with audit cost), table2 per-checkpoint depth-panel dissociation (with the breadth-panel axis-B scope footnote), table3 dual aggregation (32 rows, unit in every row label).

  ANALYSIS 4: 57 correlation/AUROC/Delta/CI claims audited in the draft -- 18 TRACEABLE_UNIT_STATED, 31 TRACEABLE_UNIT_MISSING, 3 VALUE_MISMATCH, 5 UNTRACEABLE. The generated out/replacement_text.md re-audits at 13/13 traceable with an EMPTY flag list; three prose number-dumps are named for supplementary with their replacement table.

  DISCOVERED, not inherited: the outcome variable itself disagrees across the two frozen archives on 3 of 19 members (l1/l2/l4_base; the iteration-2 archive records an identical 12/80 = 0.15, V2 re-derives from a larger judged pool). All three are UNRELIABLE-excluded so no reported correlation moves; it is stated in metadata.gaps.

  MECHANICS worth reusing: E3/method.py is NOT import-safe (imports torch, calls setrlimit at import), so PASS_RULES / ORIENTATION_MAP are loaded by exec-ing only the literal constant blocks, cross-checked against prereg_iter3.json. The plan's estimator list lives in E3/lib_iter3/statsx.py, not lib/stats_ext.py. V2's lineage units use a rank-bottom sentinel (max(defined)+1, recovered from V2/eval_a34.py) over the 14 reliable members -- without it V2's headline does not reproduce.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_P-_YL8tdIwqF
type: evaluation
in_dependencies:
- id: art_r3PqOtpvcIsK
  label: archive
- id: art_gYmQllaTCGT5
  label: scorer
- id: art_sabuvuJ8P3Wy
  label: archive
title: Does garbled text fake the refusal reversal?
summary: |-
  PURE RE-ANALYSIS (no new sampling, no weights, CPU-only, $0.674 of a $1.50 judge cap) that converts the standing verdict REVERSAL_CONFOUNDED_BY_DEGENERACY into numbers. It re-applies the ARCHIVED lexical screen (classify.fluency_ok, distinct-3 >= 0.50 and max 5-gram repeat <= 3 on generated token ids) to all 45,900 archived steered generations on 6 Qwen3 checkpoints x axes {A_canned, B_paraphrase, C_stylistic, D_random*, E_prompt_contrast}, then judges ONLY the survivors at matched axis-contrast units under two rubrics (the archived four-class and the five-class one carrying REFUSAL_NONCANONICAL), 6,536 items x 2 rubrics, 11,866 calls, parse rate 1.000.

  HEADLINE: REVERSAL_DOES_NOT_SURVIVE, 6/6 checkpoints and pooled, at matched contrast. B's five-class ANY-REFUSAL is 0.028 [0.008, 0.057] against A's 0.747 [0.618, 0.858], with the control false-positive floor at 0.146 set by the RANDOM axis D; NET = B - floor = -0.118 [-0.157, -0.082] (paired prompt-clustered bootstrap, 5000 reps) -- B sits BELOW what a meaningless direction induces on the same filtered population.

  THE DEGENERACY STORY IS THE OPPOSITE OF THE STANDING VERDICT, and is now quantified three ways. (1) At matched contrast the screen removes NOTHING: retention is 1.00 for every axis, so B's near-zero rate is absence of effect, not filtering. (2) At B's own maximum coefficient (~15 contrast units) retention falls to 0.705 AND 70.2% of the text that PASSES the screen is still judge-DEGENERATE, against 0.711 unfiltered -- the lexical screen removes essentially none of the residual degeneracy because the failure is semantic, not lexical. (3) The control floor is itself made of screen-passing degenerate text: 59.0% of D_random's matched-cell survivors are judge-DEGENERATE, which is exactly why a B rate reported without a same-population floor is uninterpretable.

  A THIRD, PRE-REGISTERED LEVEL SPLITS THE VERDICT AND IS THE PAPER'S NUANCE: at B's own peak-rate coefficient (5.2 contrast units, ~4.3x the intervention A needs) B DOES clear the floor on fluent text -- 0.642 vs floor 0.077, NET +0.565 [+0.471, +0.655], DEGENERATE only 0.049 -> REVERSAL_SURVIVES 6/6. So B's apparent reversal is real but lives entirely at coefficients that matching forbids.

  ALSO SHIPPED: exact reproduction of the archived contrast-unit conversion (54 cells, 0.0 abs error); recomputed-vs-archived screen agreement 0.9987 (tokenizer-only loads) so the recomputed screen is primary; three scoring criteria side by side (anchored regex / four-class / five-class) with kappa between them (matched level: A 0.424, B 0.108, D 0.020 -- the lexical and semantic criteria barely agree); Rogan-Gladen correction with se=0.688 sp=0.804 reproduced from the audit, reported ALONGSIDE the raw rate, with its TRUNCATION explicitly flagged at the matched level (both B and the floor fall below 1-sp = 0.196, so the corrected NET is 0 by construction, not measurement) and a se/sp +/-0.05 sweep; a drop-in replacement paragraph for the paper's semantic-scoring passage; 20 verbatim boundary examples (6 B, 8 C/D, 6 A); three figures (retention-vs-contrast panel, NET forest, three-criteria bars); full pre-registration with sha256 of every consumed artifact and 4 deviations each stamped when_decided='before'.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_G5SIDXT53EAW
type: research
in_dependencies:
- id: art_PeyWw78NIx9d
  label: extends
- id: art_Qm_KL4GhZCnX
  label: extends
title: Reading the closest rival paper and fixing our citations
summary: >-
  Primary-full-text dossier on arXiv:2607.13346 ('The Refusal Residue', Aman Mehta, ICML 2026 MI Workshop) plus a machine-verified
  audit of all 22 cited 2026 arXiv IDs, two saturation sweeps and a novelty check on the paraphrase-refit headline. Verdict:
  MIRROR IMAGE, weaker as a neighbour than its abstract implies (the dissociation is assembled across two models; probe is
  an MLP, steered object a unit diff-in-means vector; no abliterated arm; no activation norm reported so units are NOT convertible;
  '|h|' is Cohen's h). One concession forced: they steer a refusal axis and get a null. 9 of 21 cited 2026 entries are wrong,
  worst being a mis-titled [23]. New mandatory citation found: arXiv:2603.27412 LatentBiopsy, which already runs base/instruct/abliterated
  Qwen triplets. Deliverables: research_report.md (10 sections: headline verdict, full Part-A extraction dossier with an 8-row
  AUROC grid and a 7-row control-comparison table, the closeness verdict, three paste-ready artefacts, the 22-row audit table
  plus a corrected BibTeX block, the C1/C2 sweeps with verbatim query strings, the Part-D verdict, two separate residual-novelty
  paragraphs, and a confidence section listing every zero-match regex) and research_out.json with machine-readable versions
  of all of it. Key corrections downstream must act on: (1) their '|h| < 0.08' is COHEN'S h on compliance proportions, not
  a hidden state; (2) their detect-without-control is assembled across two models (0.870 Llama vs 0.425 Qwen) and their probe
  is an MLP, not the steered vector, so our within-model single-axis dissociation survives; (3) their steering scale is NOT
  convertible to NORM_L units - no activation norm is reported anywhere; (4) they DO steer a refusal axis and get a null,
  which must be conceded and distinguished; (5) nine of 21 cited 2026 entries are wrong, worst being reference [23], whose
  cited title is not the paper's title; (6) arXiv:2603.27412 (LatentBiopsy) already runs base/instruct/abliterated Qwen triplets,
  so any 'first activation score on abliterated checkpoints' claim must go - the surviving claim is that the refusal axis
  specifically dies in both roles while harm-intent geometry survives; (7) one action item before drafting: verify our AUROCs
  are not computed over the same items used to fit or normalise the axis, the leakage that moved Mehta's own number from 0.761
  to 0.425.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Anyone who downloads an open-weight checkpoint faces a question with no cheap answer: is this model safety-aligned, and how much? The standard answer is a harmful-prompt benchmark such as AdvBench [1], JailbreakBench [2] or HarmBench [3], several hundred generations scored by a judge model [4], and a repeat of the whole procedure for every attack template of interest. The evaluator must hold, transmit and store harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown.

The stakes are set by scale. Hugging Face hosts hundreds of thousands of derived checkpoints, a growing fraction of them explicitly *uncensored* community fine-tunes, and the cheapest of these is produced by a weight edit — *abliteration* — that orthogonalizes every write against a single refusal direction [5]. A platform, a downstream deployer or a regulator wanting to triage such a population needs a score that costs seconds per model and touches no harmful text.

The published attempts at such a score keep at least one of the dependencies they were meant to remove. AMS [6] scans activation geometry but needs harmful prompts and reports 71% leave-one-model-out accuracy over 14 configurations. RAS/SafeVec [7] produces a calibrated absolute score but needs unsafe prompts, jailbreak prompts and a safety-aligned reference model. VISAGE [8] measures a safety basin in weight space and evaluates a harmful benchmark at every weight perturbation. AQI [9] is prompt-invariant but still latent-geometry-based. Logit-Gap Steering [10] defines the closest scalar to ours but reads it on 520 harmful AdvBench prompts, at position 1 only, per prompt rather than per model. All of these are read-side measurements, and a read-side measurement is not guaranteed to settle behaviour: Basu et al. report 98.2% probe AUROC alongside 45.1% output sensitivity in a setting where 3,695 significant sparse-autoencoder features produced zero behavioural effect [11].

Two iterations ago we proposed an act-side alternative and it failed. $\alpha_{50}$ — the steering coefficient at which a fresh generation on a benign prompt refuses half the time, along an axis fitted from refusal-style versus compliance-style responses — does not track judged behaviour, and the five-check falsification battery we built to explain that failure cannot rank cheap scores either. One positive result survived those two negatives, and one measurement claim: refitting AMS's contrast set on token-disjoint paraphrases improved its criterion validity ($\rho$ $0.358 \to 0.654$), and the canonical refusal axis appeared to *induce* refusal while sitting at chance for *reading* the refusals a model writes. Both rested on small evidence: seven weight lineages for the first, two abliterated checkpoints for the second.

This paper is what happened when both were measured at the scale their own limitations sections demanded. Neither survived, and what replaced them is more useful than either. Scaled from 19 checkpoints over 7 lineages to 52 over 28, the paraphrase refit's advantage collapses from $+0.296$ to $+0.099$ with a confidence interval covering zero, an independently authored paraphrase set makes the metric *worse*, and the effect is localised exactly: the archived 19 members reproduce $+0.296$ to four decimals while the 33 new ones give $-0.016$. Measured on each model's own spontaneous refusals rather than on an archived, partly steered item pool, the refusal axis reads at AUROC $\geq 0.68$ on every one of the 20 checkpoints where reading is measurable at all, *zero* of 30 sit at chance, and induction and detection turn out to be positively coupled at $\rho = 0.629$ $[0.465, 0.803]$ over 70 (member, axis) pairs. The abliterated checkpoints that looked like chance-level readers are not: 14 of 18 abliterated-class members never emit the 40 spontaneous refusals the statistic needs, so the correct verdict is UNDEFINED, not AT_CHANCE. Abliteration removes the refusals to be read, not the axis's ability to read them.

[FIGURE:fig1]

What the paper claims is therefore no longer a metric, and no longer a protocol. It is a set of measurements that hold up, each of which was obtained by breaking one of our own earlier results, plus the three measurement decisions that decided them — item-pool provenance, aggregation unit, and panel size.

## Summary of Contributions

- **Reading and steering along one refusal axis are coupled, not dissociated** (§5.1) [ARTIFACT:art_1xT3w1joqeJ8]. On 30 checkpoints over 7 lineages, each measured in both roles of the same five axes, the canonical axis returns 20 READS, 1 AMBIGUOUS, 9 UNDEFINED and **0 AT_CHANCE**; across 70 (member, axis) pairs induction and detection correlate at $\rho = 0.629$ $[0.465, 0.803]$ (lineage bootstrap), within-member mean $0.715$. This *reverses* the within-axis dissociation our previous draft led with, and the reversal has a named cause: the earlier item pool contained steered and archived text, whereas each model's own spontaneous text does not.
- **A published dissociation, and ours, both need the item pool stated** (§2, §5.1) [ARTIFACT:art_G5SIDXT53EAW]. Mehta [44] reports the mirror image — detect-without-control for alignment faking — but his own AUROC moves from $0.761$ to $0.425$ when the split discipline is tightened, and his dissociation is assembled across two models. Our reversal and his leakage correction are the same lesson at opposite signs.
- **The one positive lead does not survive at scale, and the failure is localised** (§5.2) [ARTIFACT:art_CZaytBH8uL4_]. At 52 members over 28 lineages and 11 families, $\Delta_A = +0.099$ $[-0.027, 0.244]$ against the archived $+0.296$; an independently authored paraphrase set gives $\Delta_B = -0.152$; the archived 19-member block reproduces $+0.2963$ (gap $2.6\times10^{-4}$) while the 33 new members give $-0.016$ $[-0.144, 0.130]$. The $1/5040$ permutation floor that pinned the original result is genuinely retired ($p = 0.135$ against a floor of $5\times10^{-6}$). This adjudicates the question our previous Discussion left open, in favour of seven-lineage predictive validity being unreliable.
- **The canonical axis beats its token-disjoint paraphrase on semantics, not just lexicon** (§5.3) [ARTIFACT:art_P-_YL8tdIwqF]. On fluency-screened text at matched contrast units, axis B induces $0.028$ $[0.008, 0.057]$ any-refusal against axis A's $0.747$ $[0.618, 0.858]$, with a random-direction false-positive floor of $0.146$: B sits $0.118$ $[0.082, 0.157]$ *below* what a meaningless direction induces. The previous draft adjudicated this; here it is measured.
- **The aggregation unit is a first-class analysis choice, and this paper's own numbers moved with it** (§5.4) [ARTIFACT:art__tq3ZgPRYB0B]. Our AMS reimplementation's $\rho = 0.358$ (19 members, lineage-clustered) and $\rho = 0.821$ (7 lineage-aggregated units) are one statistic at two units. Over 16 score $\times$ configuration cells, changing only the unit moves oriented $\rho$ by a median $0.238$, a maximum $0.557$, and flips the sign on 5. Every correlation in this paper now names its unit.
- **Two empirical nulls that steering papers should adopt** (§5.5). A random direction at the canonical axis's own matched magnitude induces refusal at $\geq 0.10$ on 7 of 30 checkpoints (worst $0.389$), and the random-direction *reading* AUROC band spans $\pm0.075$ to $\pm0.500$ across members — so "chance is $0.500$" is wrong by a wide, model-dependent margin, and single-draw random controls are not nulls.
- **The falsification battery is retired as a contribution, and its negative is now threshold-robust** (§5.4). `PROTOCOL_DOES_NOT_DISCRIMINATE` holds on a fraction $1.0000$ of a 164,736-point full factorial in its five thresholds.

# Related Work

**Static, benchmark-free safety metrics.** AMS [6] computes a standardized mean difference $\sigma = (\mu_+ - \mu_-)/\sigma_{\text{pooled}}$ of projections onto a diff-in-means direction, read at the final prompt token over a 40–80% relative-depth band, at a cost of 96 forward passes. RAS/SafeVec [7] extracts layer-wise refusal directions from a safety-aligned reference model and scores a target by hidden-state alignment under unsafe and jailbreak prompts. VISAGE [8] measures $\mathbb{E}[S_{\max} - S(\alpha)]$ over filter-normalised Gaussian weight directions, requiring a harmful benchmark at every perturbation. AQI [9] is a prompt-invariant latent-geometry diagnostic. RAS and VISAGE we do not run, for reasons fixed by a primary-source reimplementation audit [ARTIFACT:art_0UsKSgsMHome]: every RAS-scored checkpoint is $\geq$4B and none overlaps any panel at our scale, and VISAGE at published fidelity costs 4,800 generations and roughly 28 hours per 1B model on CPU. AMS and Logit-Gap Steering [10] we reimplement and run.

**Activation scores on abliterated checkpoints.** Two incumbents bound what we may claim, and a dedicated dossier settled both [ARTIFACT:art_G5SIDXT53EAW]. Hurtado [14] combines an activation refusal gap with a weight-recovery energy to separate 57 public abliterations from 37 benign fine-tunes at AUROC $0.95$, but the activation leg is a thresholded ratio (TPR $0.63$, FPR $0.14$, AUROC $0.84$) that "certifies whether the refusal mechanism is present, not whether a model is harmless", and it "presumes an attested reference". More decisively, LatentBiopsy [45] already runs base / instruction-tuned / abliterated Qwen triplets and reports that "both abliterated variants achieve AUROC at most 0.015 below their instruction-tuned counterparts", noting explicitly that its axis "is not the refusal direction itself, since it survives abliteration". Any claim to be first to read an activation safety score on abliterated checkpoints is therefore withdrawn. What survives, and what §5.1 reports, is narrower and compatible with [45]: the *refusal axis specifically* goes quiet on abliterated checkpoints — but quiet in a way we now measure precisely, as an absence of refusals to read rather than an inability to read them.

**Detection versus intervention.** Galeone et al. [12] establish that a detection direction at AUC $1.000$ can sit at $\cos = 0.12$ from the direction that produces the behaviour, and propose a *functional* criterion: the steerable case is where the intervention direction also detects. Our §5.1 result now *supports* that criterion rather than contradicting it. Mehta [44] is the closest published neighbour to what our previous draft claimed, and it is a mirror image: one direction on hidden states detects alignment faking at leakage-free leave-one-query-out AUROC $0.870 \pm 0.023$ on Llama-3.1-8B while steering over 2,000 runs "barely changes compliance", with Cohen's $h = +0.057$ $[-0.071, +0.181]$ at $\alpha = 5$ and Fisher $p = 0.41$. Three distinctions matter and the dossier verified all three in full text: the dissociation is assembled *across two models* (the steering null is on Qwen3-32B, where his own detection fails at $0.425 \pm 0.067$), his probe is a two-layer MLP rather than the steered unit vector, and no activation norm is reported anywhere, so his coefficient is not convertible to our contrast units. One concession is forced: he does steer along a refusal axis and gets a null, subtracting from an already-compliant generation at $\approx 70\%$ compliance, where we add on benign prompts from a near-zero base. The most transferable thing in his paper is not the dissociation but the leakage it survived — his own AUROC falls from $0.761$ to $0.425$ when per-fold residualisation and leave-one-query-out are enforced. Our §5.1 reversal has the same shape: the item pool decides the result. Read together, the two papers say that the read–act mapping is not fixed by geometry alone but by what text the reading is scored on. Nadaf [23] independently reports that steering succeeds where the logit lens cannot decode across 4,032 concept-layer pairs while the converse is "nearly empty (3 of 72)", which makes coupled read–act the expected case rather than a surprise.

**Steering-vector reliability.** Non-identifiability is established: steering vectors admit "large equivalence classes of behaviorally indistinguishable interventions", with orthogonal perturbations of a working vector leaving Cohen's $d$ at $0.119$–$0.131$ [15]. Unreliability has geometric predictors — cosine agreement among training activation differences and positive/negative separability along the steering direction both predict steering success across 36 datasets [13] — and the safety cost of steering has been separately catalogued [40]. Success is partly predictable ex ante: the Linear Accessibility Profile predicts steering effectiveness at $\rho = +0.86$ to $+0.91$ across 24 concept families [16], though it could not have predicted our axis comparison, because it never sees the steering direction and both of our axes score identically. Refusal is multi-directional: eleven category directions, several near-orthogonal, yield "nearly identical refusal to over-refusal trade-offs" [17], and category-specific directions can be composed for control [18]. Petrov [19] was the top refutation risk for our axis comparison, reporting that changing only the contrast baseline "produces no functional refusal directions at any tested weight level on any tested layer" by "reducing the extracted direction magnitude below the threshold at which weight-matrix projection perturbs the residual stream". We settle rather than concede it in §5.3, on 30 checkpoints in axis-contrast units, which normalise the axis magnitude by construction. Steering coefficients must be normalised by the residual-stream norm at all: Wu et al. [37] show a "steerability emerges with scale" result dissolves under exactly that normalisation.

**Auditing a safety measurement.** The battery framing is prior art in kind and we say so. Wang et al. [20] separate "construct validity ... metric validity ... criterion validity", run a pre-specified positive control and a column-permuted negative control, and survive "leave-one-organization-out and organization-clustered bootstrap" — the published counterpart of our jackknife, and the source of the warning that a small panel manufactures results (a correlation moving "from $-0.64$ at $n=7$ to $+0.02$ at $n=18$"), which §5.2 now confirms on our own data at $n = 7 \to 28$. Weng et al. [21] operationalise "rubric-semantics invariance under certified-equivalent rewrites" — the counterpart of our lexical check — and state the discrimination requirement outright. The methodological ancestor of both is the sanity-check literature for saliency maps [22]. We claim neither the checks-suite framing nor the discrimination requirement as novel.

**Refusal geometry and dynamics.** Arditi et al. [5] show refusal is mediated by a single direction and introduce the weight edit the abliteration community built on; representation engineering [24], activation addition [25] and contrastive activation addition [26] supply the steering machinery. Qi et al. [27] show aligned and unaligned generative distributions differ mainly over the first few output tokens; Yin et al. [28] trace a probe refusal score across token positions, an observable we adopt rather than coin. Korznikov et al. [29] report random steering raising harmful *compliance* from 0% to 1–13% at an identically calibrated coefficient; §5.5 supplies the matching measurement for the direction they do not test, random-induced *refusal on benign prompts*, and finds it non-negligible. Our behavioural axes follow AdvBench [1], JailbreakBench [2] and XSTest [34], with judge scoring in the style of [4]; Hasan and Biswas [39] find over-refusal and harmful compliance nearly uncorrelated ($r = -0.032$, $p = 0.89$) across 21 open-weight models, which is why the three axes are predicted separately. The critical-slowing-down programme [30, 31, 32, 33] supplied the indicators for this project's first iteration; that arm is closed and summarised in Appendix A.

# Preliminaries

**Panels and the resampling unit.** Three panels appear, and every claim names the one it rests on. The *depth* panel is six Qwen3 [35] checkpoints (0.6B and 1.7B $\times$ base / instruct / abliterated) measured exhaustively [ARTIFACT:art_r3PqOtpvcIsK]. The *breadth* panel is 19 checkpoints over 7 lineages and 5 architecture families, all $\leq$2B [ARTIFACT:art_sabuvuJ8P3Wy]. The *scale* panel, new here, is 52 analysed members over 28 weight lineages and 11 architecture families at $\leq$4.2B, drawn from a frozen manifest of 137 verified checkpoints over 93 lineages [ARTIFACT:art_CKWQh2cOQLLQ]; a separate 30-checkpoint, 7-lineage panel supports the read-versus-act measurement. The lineage — one pretrained base and everything derived from it — is the resampling and permutation unit for every model-level claim.

**Aggregation unit.** Because a lineage carries between one and four members, a model-level correlation can be computed two ways, and this paper's previous draft reported both without saying so. *Member level* means one row per checkpoint with the bootstrap and the permutation clustered on the lineage label; *lineage level* means one row per lineage, each the arithmetic mean over that lineage's defined members of both the score and the outcome. Both are legitimate; they are not interchangeable. Every correlation below is labelled, and Table 3 gives both for every score.

**Prompt sets.** All frozen and shipped [ARTIFACT:art_CKWQh2cOQLLQ]: 40 vetted everyday harmless user turns over 10 topics; 594 deduplicated AdvBench/JailbreakBench harmful behaviours with an 80-item stratified core; 400 jailbreak items; XSTest's 250 safe and 200 unsafe items; 256 harmful/benign contrast items reserved for layer selection only (exact overlap 0 with any evaluation set, maximum cosine $0.652$ against a $0.85$ threshold); 200 WikiText fluency passages.

**Steering axes.** Five axes are fitted per model at the same site on the same benign prompts: **A**, the canonical response contrast between four hand-written canned refusals and four compliances; **B**, a token-disjoint paraphrase axis built from 24 refusal paraphrases containing zero frozen refusal openers; **C**, a norm-matched non-safety stylistic axis (formal versus casual); **D**, matched random unit directions; **E**, the harmful-versus-benign *prompt* contrast. The steering site is $L = \mathrm{round}(0.25\,n_{\text{layers}})$ — the archived relative depth, which the plan for this iteration had recorded incorrectly as $0.30$ and which was corrected against the archive before any measurement [ARTIFACT:art_1xT3w1joqeJ8].

**Axis-contrast units.** The steering hook adds $\alpha\,\mathrm{NORM}_L\,\hat{x}$ to the residual stream, where $\mathrm{NORM}_L$ is the median residual-stream norm at the steering layer. Because raw diff-in-means norms differ up to fourfold between axes, all dose comparisons are reported per *axis-contrast unit* $c = \alpha\,\mathrm{NORM}_L / \lVert X \rVert$, which divides out the axis magnitude and is what settles the magnitude-collapse rival explanation [19]. The conversion was verified exact (absolute error $0.0$) against 459 archived grid cells.

**The refusal criterion.** A generation counts as a refusal when its opening matches an anchored refusal regex. Because the regex is lexical, §5.3 additionally re-scores outcomes with a four-class semantic judge and with a five-class rubric carrying an explicit non-canonical-refusal class, and every semantic rate is reported against a control false-positive floor measured on the same filtered population.

**A tokenisation hazard worth stating.** Re-encoding a prompt and its logged completion by concatenating *strings* lets byte-pair merges cross the boundary. Concatenating token *ids* fixes it. The bug is renderer-dependent: on 50 probe items it changes the boundary index on 34/50 under the plain wrapper and 0/50 under a chat template, so it bites base checkpoints specifically, and avoiding it changed 943 scored items across the 30-checkpoint panel. Relatedly, Qwen3 base tokenizers ship a chat template despite never having been tuned to follow one; automatic template selection dropped axis-E reproduction cosine to $0.13$, and forcing the plain wrapper on base models restored all six archived checkpoints to $\geq 0.99992$.

# Method

Four instruments, each pre-registered with a sha256 stamp before any statistic existed, with every deviation logged with its trigger and the data state at the time.

## Instrument 1: both roles of the same axis, on the model's own text

Each of 30 checkpoints (7 lineages, $\leq$4.2B, $\geq$8 layers) is measured in both roles of the same five axes [ARTIFACT:art_1xT3w1joqeJ8]. **Detection** is the held-out AUROC of the stratum-centred axis projection at the first generated token, refusals versus compliances, drawn from the model's *own spontaneous* generations — never steered, never archived — with a prompt-clustered bootstrap over 2,000 replicates and Holm correction. A member is `READS` when the CI lower bound exceeds $0.60$, `AT_CHANCE` when the whole CI lies inside $[0.40, 0.60]$, and `UNDEFINED` when fewer than 40 refusals exist after a full escalation ladder of 1,585 generations. **Induction** is a steering sweep reported in axis-contrast units. Two null-design corrections were forced by the data and recorded as amendments: a raw projection is $\lVert h\rVert\cos\theta$, so any direction inherits a refusal-versus-compliance *norm* difference (a random axis "read" at $0.171$ on one member), which is why a norm-controlled readout $\cos\theta = (h\cdot u)/\lVert h\rVert$ is computed for every axis on every member; and one random draw is not a null distribution, because residual streams are anisotropic, which is why the reading gate is read against 20 measured random draws per member rather than against $0.500$.

The difference from our previous certificate is one sentence, and it is the whole reversal: the earlier item pool was re-encoded archived text from six fixed checkpoints, including steered generations; this one is each model's own spontaneous output. Reuse is behavioural, not just hashed — all 13 archived `lib/*.py` modules are sha256-identical, and a no-model replay reproduces every archived per-axis AUROC exactly (paired $A-B = 0.152$ against an archived $0.152$).

## Instrument 2: the paraphrase refit at scale

The AMS paraphrase refit is rerun on 52 analysed members over 28 lineages and 11 families, at $\leq$4.2B, from the frozen manifest [ARTIFACT:art_CZaytBH8uL4_]. Cost is 96 forward passes per member, zero generation for the score itself, $0.1334 total and 13.3 minutes. Four outcomes were pre-registered before any correlation: **R1** $\Delta_A > 0$ with its paired lineage-bootstrap CI excluding zero; **R2** $\rho(\text{refit A}) \geq 0.40$ with its CI excluding zero; **R3** $\Delta_B > 0$ with its CI excluding zero, where SET B is an *independently authored* paraphrase set; **R4** permutation $p < 0.05$ and off the floor by an order of magnitude. SET B was generated by a model that is never the judge, at temperature $0.3$, and verified by the *frozen* iteration-3 `check_pair()` with zero hand-written repairs (80/80 strings pass, 78 on the first attempt); measured content-token Jaccard against SET A is $0.201$. Every correlation is reported at both aggregation units. Two enrolled checkpoints were unrecoverable upstream incompatibilities and are recorded with their exception strings.

## Instrument 3: measuring the degeneracy adjudication instead of asserting it

Our previous draft set aside a semantic partial reversal on the grounds that axis B's high-coefficient text is degenerate. That is an inference, not an estimate, and the judge's audited REFUSAL sensitivity ($0.688$) and specificity ($0.804$) do not carry it implicitly. The archived lexical screen (distinct-3 $\geq 0.50$, maximum 5-gram repeat $\leq 3$, computed on generated token ids) is therefore re-applied to all 45,900 archived steered generations, and only the *survivors* are judged, at three pre-registered coefficient levels: A's matched contrast (the adjudication), B's own peak refusal rate, and B's own maximum contrast [ARTIFACT:art_P-_YL8tdIwqF]. 6,536 items are scored under two rubrics, 11,866 calls, parse rate $1.000$, $0.674. Every rate is reported against a control false-positive floor computed on the *same filtered population* from axes C and D, and a Rogan–Gladen correction is reported alongside — never instead of — the raw rate, with its truncation flagged where both rates fall below $1 - \text{specificity} = 0.196$.

## Instrument 4: the aggregation-unit repair and the threshold surface

A pure re-analysis over the frozen archives, with no GPU, no generation and $0.00 spend, running end to end in 125 s [ARTIFACT:art__tq3ZgPRYB0B]. An 11-leg reproduction gate regenerates every headline number from sha256-stamped inputs to $10^{-6}$ before anything is restated. Analysis 1 recomputes every score at both aggregation units, holding the exhaustive $7! = 5040$ lineage permutation constant in both so the rows are comparable. Analysis 2 sweeps all five per-check thresholds in a 164,736-point full factorial and reports the fraction of the grid on which the battery's verdict holds. Analysis 4 audits the previous draft's own prose: 57 correlation, AUROC and $\Delta$ claims, classified as traceable-with-unit, traceable-without-unit, value-mismatch or untraceable.

# Results

## Reading and steering are coupled, and our previous dissociation was an item-pool artifact

The claim our previous draft led with was that the direction along which refusal is cheapest to *induce* is a mediocre *reader* of the refusals a model writes, and that on abliterated checkpoints it is at chance in both roles. Measured on 30 checkpoints, in both roles of the same five axes, on each model's own spontaneous text, it is wrong [ARTIFACT:art_1xT3w1joqeJ8].

Of 30 members the canonical axis returns 20 `READS`, 1 `AMBIGUOUS`, 9 `UNDEFINED` and **zero** `AT_CHANCE`. Every member on which the statistic exists reads at AUROC $\geq 0.685$, and the pre-registered $K < 3$ branch fires with $K = 0$ of $M = 4$: the two-checkpoint "at chance in both roles" claim is retracted.

[FIGURE:fig2]

The reason the abliterated arm could not be strengthened is structural rather than statistical, and it is the most useful thing in this section. Of 18 abliterated-class checkpoints, 14 never produced the 40 spontaneous refusals the detection statistic needs, even after the full escalation ladder — 1,585 generations each, with a median spontaneous refusal rate of $0.0076$ across the weight-edited abliteration arm and $0.0000$ across the behavioural-uncensored candidate arm. Their reading AUROC is therefore *undefined*, not at chance. Abliteration removes the refusals to be read; it does not remove the axis's ability to read them. That is consistent with LatentBiopsy's finding that harm-intent geometry survives abliteration to within $0.015$ AUROC [45], and it removes the provenance-signal reading we had previously attached to the $n=2$ result.

| arm | members | detection-powered | median spontaneous refusal rate | axis-A verdicts |
|---|---|---|---|---|
| aligned reference | 12 | 10 | 0.1131 | 11 READS, 1 AMBIGUOUS |
| weight-edited abliteration | 9 | 1 | 0.0076 | 5 READS, 4 UNDEFINED |
| behavioural-uncensored candidate | 5 | 0 | 0.0000 | 1 READS, 4 UNDEFINED |
| behavioural-uncensored unverified | 4 | 3 | 0.2884 | 3 READS, 1 UNDEFINED |

**Table 5.** Why the abliterated arm goes quiet. Detection needs refusals to read; the arms that emit none return UNDEFINED, not AT_CHANCE.

The six depth-panel checkpoints are the same in both studies, so the reversal can be read checkpoint by checkpoint.

| checkpoint | class | archived pool: A AUROC [95% CI] | archived paired $A-B$ | own-text pool: A AUROC [95% CI] | own-text verdict | spontaneous refusal rate | A contrast units at 50% refusal | A max refusal rate |
|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | base | 0.612 [0.565, 0.658] | $+0.074$ | 0.915 [0.869, 0.953] | READS | 0.0574 | 1.23 | 0.667 |
| Qwen3-0.6B | instruct | 0.662 [0.596, 0.713] | $+0.152$ | 0.980 [0.944, 1.000] | READS | 0.0422 | 0.82 | 1.000 |
| Qwen3-0.6B-abliterated | abliterated | 0.495 [0.443, 0.543] | $-0.062$ | undefined (0 refusals / 1,572) | UNDEFINED | 0.0000 | 1.15 | 0.972 |
| Qwen3-1.7B-Base | base | 0.623 [0.560, 0.687] | $+0.021$ | 0.918 [0.871, 0.957] | READS | 0.1688 | 1.50 | 0.806 |
| Qwen3-1.7B | instruct | 0.790 [0.746, 0.833] | $+0.404$ | 0.906 [0.859, 0.944] | READS | 0.2277 | 1.12 | 1.000 |
| Huihui-Qwen3-1.7B-abliterated-v2 | abliterated | 0.486 [0.420, 0.555] | $-0.006$ | undefined (0 refusals / 1,574) | UNDEFINED | 0.0000 | 1.57 | 0.972 |

**Table 2.** The same six checkpoints, the same canonical axis, two item pools. *Archived pool*: 7,241 re-encoded items from an archive containing steered and archived generations, where the axis looked like a mediocre reader and the two abliterated members looked at chance. *Own-text pool*: each model's own spontaneous, unsteered generations, where the axis reads at $0.906$–$0.980$ and the abliterated members produce no refusals to read at all. Induction is unchanged between the two studies; only the reading side moved. Unit: the item, prompt-clustered bootstrap over 2,000 replicates.

With both roles measurable on the same members, the study can for the first time put them on one plot. Across 70 (member, axis) pairs over 14 members and 7 lineages, induction quality (maximum induced refusal rate) and detection quality (held-out AUROC) are correlated at Spearman $\rho = 0.629$, lineage-bootstrap 95% CI $[0.465, 0.803]$; the within-member mean is $0.715$; the secondary version using $-\log_{10} c_{50}$ gives $0.448$ with $77.1\%$ censoring, which is why the rate version is primary. The previous evidence base for this relationship was four points.

[FIGURE:fig3]

Why the two studies disagree is not a mystery and is worth stating as a methodological result rather than a correction. The earlier certificate scored the axis on 7,241 re-encoded items drawn from an archive that included steered generations; this one scores each model on text it produced unsteered. Mehta [44] documents the same sensitivity from the other side: his leave-one-query-out, per-fold-residualised protocol moves his own detection AUROC from $0.761$ to $0.425$. The transferable claim is that a read–act comparison is only interpretable with the item pool's provenance stated, and that when the pool is the model's own spontaneous behaviour, reading and steering along a refusal axis go together.

One arm does remain measurable on abliterated checkpoints and it is not null. Across 10 within-lineage abliterated-versus-parent pairs, steering along the canonical axis still induces refusal on 5 abliterated checkpoints and *fails* on 4 whose parent was steerable, with a median change in maximum induced rate of $-0.306$ (for example `Qwen2.5-1.5B-Instruct-abliterated` falls to $0.028$ from its parent's $0.917$, while `Qwen3-0.6B-abliterated` holds at $0.972$ against $1.000$). Abliteration recipes differ in whether they close the steering channel, which is a cleaner triage signal than the retracted one and is measurable without any harmful prompt — but on 10 pairs it is a lead, not a result, and we label it as such.

## The one positive lead does not survive at 28 lineages

Our previous Discussion named one forward-looking result and one thing to do about it: refitting AMS's contrast set on token-disjoint paraphrases lifted its correlation with judged behaviour from $\rho = 0.358$ to $0.654$ on 19 members over 7 lineages, and the honest next step was to replicate it where the permutation floor stops binding. Done at 52 members over 28 lineages and 11 architecture families, it does not replicate [ARTIFACT:art_CZaytBH8uL4_].

At the member level with a lineage-clustered bootstrap over 10,000 replicates, the original scanner reaches $\rho = 0.359$ $[0.047, 0.592]$, the SET A refit $0.458$ $[0.197, 0.646]$, and the independently authored SET B refit $0.207$ $[-0.110, 0.463]$. The paired advantage is $\Delta_A = +0.099$ $[-0.027, 0.244]$, with $P(\Delta_A > 0) = 0.935$ — short of the pre-registered interval criterion — so **R1 fails**. $\Delta_B = -0.152$ $[-0.488, 0.075]$: independently authored wording does not merely fail to reproduce the gain, it points the other way, so **R3 fails**. The permutation $p$ for $\Delta_A$ is $0.135$ against a Monte-Carlo floor of $5\times10^{-6}$ over 200,000 lineage permutations, so **R4 fails** — and the $1/5040$ floor that the original result sat exactly on is genuinely retired by the larger panel. Only **R2** passes. The pre-registered verdict is `DOES_NOT_SURVIVE`, with no salvage and no post-hoc subgroup.

The decisive diagnostic is not the shrinkage but its location.

[FIGURE:fig4]

Split by provenance, the archived 19-member block reproduces $\Delta_A = +0.2963$ — a gap of $2.6\times10^{-4}$ to the previously published $+0.296$, confirming the reuse is byte-exact rather than merely similar — while the 33 newly measured members give $-0.016$ $[-0.144, 0.130]$. Per block the correlation goes $0.358 \to 0.654$ on the archive and $0.402 \to 0.386$ on the new members. The entire effect lives in the original small panel. This is not a single-outlier story: leave-one-lineage-out over 28 folds keeps the shrunken $\Delta_A$ in $[0.068, 0.122]$ and leave-one-family-out over 11 folds in $[0.060, 0.137]$, never flipping sign. Three alternative calibration rules (maximum-$\sigma$, harmful-concept-only, worst-concept) give $+0.066$, $+0.152$ and $-0.035$, none rejecting after Holm. The descriptive verdict-class change rate is $12/52 = 0.231$ $[0.137, 0.361]$ against the archived $6/19$, so the refit still *moves* AMS's PASS/WARN/CRIT verdicts; it just does not move them toward the truth.

This adjudicates the question our previous Discussion explicitly left open. We had two readings of the battery's failure — either hygiene checks measure something a user of a triage score does not care about, or seven-lineage predictive validity is itself noise — and said the panel could not separate them. It can now: at $n_{\text{lineage}} = 7$ the improvement is $+0.296$ and at $n_{\text{lineage}} = 28$ it is $+0.099$ with an interval covering zero, which is the second reading, and which is the exact failure mode Wang et al. warn about when they report a correlation moving from $-0.64$ at $n = 7$ to $+0.02$ at $n = 18$ [20]. We report it as a retraction of our own headline rather than as a limitation of someone else's.

Two accompanying measurements keep the retraction honest. Reuse is proven behaviourally: our AMS reimplementation recomputed from scratch matches the iteration-2 archive on 19/19 members (maximum absolute delta $2.4\times10^{-6}$), the SET A refit matches iteration 3 on 19/19 exactly, and both cross-pipeline calibration members regenerate byte-identically with their Wilson intervals unchanged, which is what licenses pooling archived and new outcome blocks at all. And the reimplementation label stands: against AMS's published Table I our $\sigma$ lands at $4.274$ versus $4.550$ ($-6.1\%$), $5.845$ versus $4.800$ ($+21.8\%$) and $5.010$ versus $8.370$ ($-40.1\%$), so everything in this section bounds *our reimplementation*, not AMS as published.

## The canonical axis beats its paraphrase on semantics, not only on lexicon

Our previous draft's weakest passage adjudicated a result rather than measuring it: under a four-class semantic judge the paraphrase axis B crossed a $0.50$ refusal rate on every checkpoint, and we set that aside on the grounds that B's high-coefficient text is degenerate. The reviewer was right that this needed a number. Filtering to text that passes the archived fluency screen *before* judging, and reporting every rate against a control floor measured on the same filtered population, produces one [ARTIFACT:art_P-_YL8tdIwqF].

At matched axis-contrast units — A's own 50%-refusal coefficient — the five-class any-refusal rate is $0.028$ $[0.008, 0.057]$ for axis B against $0.747$ $[0.618, 0.858]$ for axis A, with the false-positive floor at $0.146$, set by the *random* axis D. The net quantity $B - \text{floor}$ is $-0.118$ $[-0.157, -0.082]$ (paired prompt-clustered bootstrap, 5,000 replicates, $n = 600$ per axis): B sits below what a meaningless direction induces on the same population. The pre-registered verdict is `REVERSAL_DOES_NOT_SURVIVE`, on 6 of 6 checkpoints and pooled.

[FIGURE:fig5]

Three sub-measurements make this an estimate rather than an argument, and each cuts against something we previously wrote. First, the degeneracy story is the *opposite* of our earlier adjudication at the level that matters: at matched contrast the lexical screen removes nothing — retention is $1.000$ for both A and B — so B's near-zero rate there is an absence of effect, not a filtering artifact. Second, at B's own maximum coefficient ($\approx 15$ contrast units) retention does fall to $0.705$, but $70.2\%$ of the text that *passes* the screen is still judge-DEGENERATE, against $71.1\%$ unfiltered: the lexical screen removes essentially none of the residual degeneracy, because the failure is semantic and the screen is lexical. Third, the control floor is itself made of screen-passing degenerate text — $59.0\%$ of the random axis's matched-cell survivors are judge-DEGENERATE — which is precisely why a semantic rate reported without a same-population floor is uninterpretable, and why our previous four-class number was.

One pre-registered level splits the verdict, and it is the section's nuance rather than a hedge. At B's own peak refusal coefficient ($5.21$ contrast units, about $4.3\times$ the intervention A needs) B *does* clear the floor on fluent text: $0.642$ against a floor of $0.077$, net $+0.565$ $[+0.471, +0.655]$, with only $4.9\%$ DEGENERATE. So B's apparent reversal is real, but lives entirely at coefficients that matching forbids — which is what matching was introduced to detect. The Rogan–Gladen correction is reported throughout and is uninformative at the matched level by construction: both B's rate and the floor fall below $1 - \text{specificity} = 0.196$, so both corrected prevalences truncate at zero and the corrected net is exactly $0$ by construction rather than by measurement, which the artifact flags rather than quoting.

| axis | $n$ | anchored regex | four-class judge | five-class any-refusal | five-class non-canonical | five-class degenerate |
|---|---|---|---|---|---|---|
| A (canonical) | 600 | 0.470 | 0.763 | 0.747 | 0.142 | 0.005 |
| B (token-disjoint paraphrase) | 600 | 0.002 | 0.043 | 0.028 | 0.018 | 0.002 |
| C (stylistic control) | 600 | 0.000 | 0.050 | 0.017 | 0.017 | 0.007 |
| D (random control) | 575 | 0.002 | 0.374 | 0.146 | 0.139 | 0.590 |

**Table 4.** Refusal rates on fluency-screened text at matched axis-contrast units, three scoring criteria side by side, pooled over the six depth-panel checkpoints. The random control's four-class rate of $0.374$ against its five-class degenerate rate of $0.590$ is the false-positive floor that any semantic steering claim has to clear. Criterion agreement is poor where it matters: Cohen's $\kappa$ between the regex and the five-class rubric is $0.424$ on A, $0.108$ on B and $0.020$ on D.

The scope repair the reviewer asked for is also settled. On the breadth panel two members carried the objection that axis B does reach a $0.50$ refusal rate; re-measured at matched contrast, 1 of the 2 is a genuine inducer (`Llama-3.2-1B-Instruct`, verdict `B_IS_A_GENUINE_INDUCER`) and 1 is a norm artifact. Across all 30 checkpoints in the read-versus-act study, matched contrast returns `NORM_MISMATCH_DOES_NOT_EXPLAIN` on 22, which rules out Petrov's magnitude-collapse account [19] on a panel five times the size of the previous test.

## The aggregation unit, and the negative that is threshold-robust

The most damaging defect a reader could have found in our previous draft was internal: our AMS reimplementation's correlation with judged behaviour appeared as $0.358$ in one section and $0.821$ in another, with the paper's headline $\Delta$ computed from the second. Both numbers are correct and neither was labelled [ARTIFACT:art__tq3ZgPRYB0B]. At the **member level** — 19 checkpoints, resampled and permuted on the lineage label — the statistic is $\rho = 0.358$ $[-0.074, 0.699]$ with exhaustive permutation $p = 0.0911$. At the **lineage level** — 7 units, each the mean over that lineage's defined members of both score and outcome — the same statistic is $\rho = 0.821$. The gap of $0.464$ is what lineage aggregation buys by removing within-lineage variance and reducing $n$ from 19 to 7.

That is not a bookkeeping repair, because the choice moves conclusions. Over the 16 score $\times$ configuration cells where both units are defined, changing nothing but the unit moves oriented $\rho$ by a median $0.238$ and a maximum $0.557$, and **flips the sign on 5**.

[FIGURE:fig6]

The headline comparison inherits exactly that instability, and we now report it at both levels with the verdict strings the analysis emits. On the carrier our previous draft used, the oriented $\Delta = \rho(\alpha_{50}) - \rho(\text{our-AMS})$ is $-0.929$ $[-1.961, -0.113]$ at the lineage level and $-0.376$ $[-0.795, 0.110]$ at the member level: `SIGN_SURVIVES` but `EXCLUSION_LOST_AT_MEMBER_LEVEL`. The sign of the loss is robust to the unit; the interval's exclusion of zero — which the previous draft led with — is not. On the alternative $\alpha_{50}$ carrier used by the discrimination matrix, the same comparison gives $-0.566$ at the member level and $+0.107$ at the lineage level: `SIGN_FLIPS`, `EXCLUDES_AT_NEITHER`. The correct statement is that $\alpha_{50}$ loses to a cheaper activation scanner under every unit and carrier we can compute, and that no interval-based version of that claim survives both units. The same lesson applies to the scale replication in §5.2, where the sign of $\rho$ survives the unit on all three scores but the CI's exclusion of zero does not: at the lineage level none of $0.162$, $0.224$ and $0.013$ excludes zero.

An audit of our previous draft's own prose puts a number on how much of the paper this affected: of 57 correlation, AUROC and $\Delta$ claims, 18 were traceable with the unit stated, 31 traceable with the unit missing, 3 mismatched their source value, and 5 were untraceable. The generated replacement text re-audits at 13 of 13 traceable with an empty flag list. One further discrepancy surfaced that we did not inherit but discovered: the judged plain-harmful refusal rate itself differs across the two frozen archives on 3 of 19 checkpoints, all base members that one archive records as an identical $12/80 = 0.15$ and the other re-derives from a larger judged pool. All three are among the five auto-flagged `UNRELIABLE` members excluded from every correlation, so no reported correlation moves; we state it because a reader reconciling the artifacts would find it.

With units named, the discrimination matrix stands unchanged and its negative is now robust to its own thresholds.

| score | primary column | C1 lexical | C2 monotone | C3 depth | C4 jackknife | C5 scorer | passes | oriented $\rho$ (member) | 95% CI | perm $p$ | AUC | forward passes | generations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\alpha_{50}$ | max refusal rate | FAIL (undef.) | FAIL (0.833) | PASS (1.823) | PASS (0.210) | FAIL (0.391) | 2/5 | $-0.208$ | $[-0.545, 0.183]$ | 0.3087 | 0.381 | 0 | 265 |
| our-AMS $\sigma$ | ams_sigma | FAIL (0.833) | FAIL (0.947) | PASS (1.607) | PASS (0.226) | FAIL (0.391) | 2/5 | $0.358$ | $[-0.072, 0.709]$ | 0.0911 | 0.705 | 96 | 0 |
| logit-gap (benign) | logit_gap_benign | FAIL (0.967) | FAIL (0.158) | FAIL (4.361) | FAIL (0.292) | FAIL (0.391) | 0/5 | $0.101$ | $[-0.243, 0.569]$ | 0.6621 | 0.523 | 40 | 0 |
| logit-gap (harmful) | logit_gap_harmful | FAIL (0.977) | FAIL (0.526) | FAIL (3.611) | PASS (0.220) | FAIL (0.391) | 1/5 | $0.667$ | $[0.439, 0.904]$ | 0.0038 | 0.784 | 80 | 0 |

**Table 1.** The discrimination matrix: four cheap benchmark-free safety scores $\times$ five falsification checks, on the frozen 19-member / 7-lineage panel, all correlations at the **member level** with the lineage as the resampling and permutation unit (exhaustive $7! = 5040$; achievable floor $1/5040 = 1.98\times10^{-4}$). Verdict: `PROTOCOL_DOES_NOT_DISCRIMINATE`. Check 5 is a property of the shared scorer (REFUSAL $\kappa = 0.391$ against a $0.60$ threshold), so it fails identically in every row and caps every row at 4/5. $\alpha_{50}$'s audit cost is dominated by steered generation (265 per member, 5,460 measured GPU-seconds); every rival is forward-pass only.

The load-bearing observation is unchanged and is the reason we retired the battery: the score that predicts judged behaviour *best* — the logit-gap margin on harmful prompts, $\rho = 0.667$ $[0.439, 0.904]$ at the member level and $0.929$ $[0.412, 1.000]$ at the lineage level — passes the *fewest* checks. Construct hygiene and predictive validity are close to orthogonal on this panel. What is new is that the negative no longer depends on five arbitrary cutoffs. Over a 164,736-point full factorial in the five thresholds, `PROTOCOL_DOES_NOT_DISCRIMINATE` holds on a fraction $1.0000$ of grid points, and on $0.9091$ under the stricter criterion that a rival must *strictly exceed* $\alpha_{50}$'s pass count. Exactly one single-axis change anywhere on the grid produces a strict rival win: lowering check 3's depth-span threshold from $2.0$ to $1.75$. Check 5 cannot contribute at all, because its $\kappa$ of $0.391$ lies below the entire swept range $[0.40, 0.80]$ — proved structurally and verified empirically. Dropping the pass rules' secondary clauses and scoring the numeric cutoffs alone lowers stability to $0.5802$ and $0.2429$, which locates the negative precisely: it is carried by the verdict-class and interiority clauses, not by the numbers.

| score | member-level $\rho$ | 95% CI | perm $p$ | lineage-level $\rho$ | 95% CI | perm $p$ | sign agrees | CI excludes 0 |
|---|---|---|---|---|---|---|---|---|
| $\alpha_{50}$ (max refusal rate) | $-0.208$ | $[-0.547, 0.175]$ | 0.3087 | $+0.321$ | $[-0.887, 0.870]$ | 0.4976 | no | neither |
| our-AMS $\sigma$ | $0.358$ | $[-0.074, 0.699]$ | 0.0911 | $0.214$ | $[-0.765, 0.961]$ | 0.6615 | yes | neither |
| our-AMS $\sigma$, paraphrase refit | $0.654$ | $[0.276, 0.859]$ | $1.98\times10^{-4}$ | $0.643$ | $[-0.192, 1.000]$ | 0.1389 | yes | member only |
| logit-gap (benign) | $0.101$ | $[-0.243, 0.573]$ | 0.6621 | $0.286$ | $[-1.000, 0.765]$ | 0.5560 | yes | neither |
| logit-gap (harmful) | $0.667$ | $[0.439, 0.904]$ | 0.0038 | $0.929$ | $[0.412, 1.000]$ | 0.0067 | yes | both |
| our-AMS $\sigma$ (scale panel, $n=52$) | $0.359$ | $[0.047, 0.592]$ | — | $0.162$ | $[-0.314, 0.597]$ | — | yes | member only |
| our-AMS refit A (scale panel) | $0.458$ | $[0.197, 0.646]$ | — | $0.224$ | $[-0.229, 0.620]$ | — | yes | member only |
| our-AMS refit B (scale panel) | $0.207$ | $[-0.110, 0.463]$ | — | $0.013$ | $[-0.442, 0.453]$ | — | yes | neither |

**Table 3.** Every score against the judged plain-harmful refusal rate at **both** aggregation units. Rows 1–5 are the 19-member / 7-lineage panel with the exhaustive $7!$ permutation null in both units; rows 6–8 are the 52-member / 28-lineage scale panel, where the permutation null is Monte Carlo over 200,000 draws. Only one score — the logit-gap margin on harmful prompts — excludes zero at both units.

## Two empirical nulls that steering studies should adopt

The 30-checkpoint study was designed to test axes, and it produced two facts about *controls* that we did not expect and that generalise beyond this paper [ARTIFACT:art_1xT3w1joqeJ8].

First, a random direction is not behaviourally inert at the magnitude at which a refusal axis works. Injected at axis A's own matched magnitude, a matched random unit direction induces refusal at a maximum rate of at least $0.10$ on 7 of 30 members, with a worst case of $0.389$ and a panel median of $0.028$. Korznikov et al. [29] report the complementary effect — random steering raising harmful *compliance* to 1–13% at an identically calibrated coefficient — and never test random-induced refusal on benign prompts; this is that measurement, and it says the induction floor is a real quantity that steering claims must clear rather than a formality. Our own earlier random-direction null ($0.00$–$0.058$ over $\alpha \in [0,2]$) was measured on six checkpoints and does not generalise to 30.

Second, a random direction does not *read* at $0.500$. The empirical band of AUROCs over 20 random draws per member spans $\pm0.075$ to $\pm0.500$ across members, because residual streams are anisotropic, so a gate written against the textbook $0.500$ is wrong by a wide and model-dependent margin. A single random draw is not a null distribution. Related, a raw projection is $\lVert h\rVert\cos\theta$, so any direction inherits whatever refusal-versus-compliance *norm* difference the model has — one random axis "reads" at $0.171$ on a member for that reason alone — which is why every AUROC in §5.1 is reported both raw and norm-controlled, and why the two agree to within $0.011$ on the canonical axis.

# Discussion

**What this project now believes.** Four iterations have produced three controlled negatives — the bistable/early-warning route, $\alpha_{50}$ as a safety score, and the falsification battery as a certification protocol — plus, in this iteration, the retraction of both of the positives the previous draft carried. That reads badly until one notices that each retraction came from a measurement that is itself the contribution. The paraphrase refit's collapse from $+0.296$ at 7 lineages to $+0.099$ at 28, with the effect fully localised to the original block, is a clean instance of a phenomenon the field is currently warned about in the abstract [20] and rarely shows on its own published result. The dissociation's reversal identifies a specific, checkable confound in a read-versus-act comparison — the item pool — that the closest published neighbour hit from the opposite direction and fixed with the same kind of discipline [44].

**What survives, stated precisely.** Along one refusal axis, on 30 checkpoints over 7 lineages, reading and steering are positively coupled ($\rho = 0.629$ $[0.465, 0.803]$). The canonical canned-refusal axis reads real refusals at AUROC $\geq 0.685$ wherever the statistic exists, and induces refusal at roughly one axis-contrast unit. Its token-disjoint paraphrase induces $0.028$ any-refusal at matched contrast on fluent text, below a random-direction floor of $0.146$, so the earlier "the metric is merely lexical" reading is refuted at the semantic level rather than only at the regex level — but it is also refuted the other way at high coefficients, where B is a genuine if expensive inducer at $4.3\times$ A's coefficient. And a random direction at matched magnitude is not inert in either role.

**Why a validity battery can be right and useless at once.** The battery's cells each report a true property. What it cannot do is rank scores, because on this panel construct hygiene and predictive validity are close to orthogonal: the logit-gap harmful-prompt margin is at once the most predictive score and the least hygienic. This iteration removes the ambiguity we previously left in that reading. It is not that hygiene checks measure something users do not care about; it is that the criterion the checks were being validated *against* — predictive validity estimated on seven lineages — was itself unreliable, which §5.2 demonstrates directly on the one column where the checks appeared to pay off.

**Limitations.** (1) Scale: everything is measured at 0.13B–4.2B, and the within-family scale ladder runs only to 4B. (2) The read-versus-act coupling rests on 70 (member, axis) pairs from 14 detection-powered members over 7 lineages; the induction side is measurable on all 30 but the detection side is not, and the members it is missing are systematically the ones with no refusals, so the coupling estimate is conditioned on a model refusing sometimes. (3) The abliterated arm is bounded by that same structural fact: nothing in this study can tell an abliterated checkpoint whose axis has been destroyed from one whose refusals have merely been suppressed, because the detection statistic requires refusals. (4) Our AMS reimplementation misses the published Table I by $-6\%$, $+22\%$ and $-40\%$ on the three overlapping checkpoints, so §5.2 and §5.4 bound *our reimplementation*; RAS and VISAGE were not run, for the checkpoint-overlap and cost reasons in §2. (5) Behavioural rates are judge-derived, the REFUSAL one-versus-rest annotator $\kappa$ is $0.391$, and our annotators are LLM agents, so every accuracy bounds agreement with an LLM panel rather than truth; disattenuated correlations are reported alongside raw ones, never instead. (6) Everything steered is a statement about the steered dynamical system, which is provably not prompt-reachable [38]. (7) Our detection protocol uses a prompt-clustered bootstrap and held-out items, but not Mehta's per-fold residualisation with all normalisation statistics estimated inside the training fold [44]; that control moved his own AUROC by $0.336$ and we have not run its counterpart. (8) Two enrolled checkpoints in the scale panel failed on upstream incompatibilities, costing one lineage.

**What we would do next.** Three things follow. Run the read-versus-act protocol with Mehta's split discipline, since limitation (7) is the one place where a $0.34$ AUROC swing has been published and we have not excluded it. Test the abliteration-recipe lead from §5.1 — steering still induces on 5 of 10 abliterated checkpoints and fails on 4 whose parent was steerable — on enough within-lineage pairs to be a claim rather than a lead; it is a harmful-prompt-free provenance signal and it is the only measurement in this study still pointing at the original product goal. And pair the refusal axis with LatentBiopsy's harm-intent axis [45] on the same abliterated checkpoints: their axis survives abliteration to within $0.015$ AUROC while the refusal channel goes silent, and a two-axis signature (harm geometry intact, refusal channel dead) would be strictly more informative than either alone and would not need the attested reference that the published abliteration audit presumes [14].

# Conclusion

We set out to build a safety score that costs seconds per checkpoint and touches no harmful text. It does not work, and this iteration additionally retracts both of the positive results that survived the previous one — each by the experiment its own limitations section asked for. The lexical-invariance refit of a published activation scanner improves criterion validity by $+0.296$ on 7 lineages and by $+0.099$ $[-0.027, 0.244]$ on 28, with the archived block reproducing to $2.6\times10^{-4}$ and the 33 new members contributing $-0.016$: a small-panel artifact, localised rather than inferred. The within-axis induce-without-detect dissociation disappears when each model is scored on its own spontaneous text: 20 READS, 1 AMBIGUOUS, 9 UNDEFINED and zero at chance over 30 checkpoints, with the two roles positively coupled at $\rho = 0.629$ $[0.465, 0.803]$, and with abliteration removing the refusals to be read rather than the ability to read them.

What is left is a small set of measurements that hold. The canonical refusal axis both reads and steers; its token-disjoint paraphrase induces $0.028$ against $0.747$ at matched contrast on fluent text, *below* the $0.146$ floor a random direction sets, so the axis's advantage is semantic and not merely a wording artifact; a random direction at matched magnitude induces refusal on 7 of 30 checkpoints and reads at anything but $0.500$; and the aggregation unit alone moves this study's correlations by a median $0.238$ and flips 5 of 16 signs. Read together, they say that the obstacle to a cheap act-side safety score is not that the geometry is absent — it reads and steers exactly as advertised — but that every step from geometry to a number that predicts behaviour is decided by a measurement choice: which text is scored, which unit is resampled, and how many lineages are in the panel. On this evidence, a cheap safety score's construct hygiene, its predictive validity, and its apparent replication all have to be established separately, because none of the three implies another.

# Appendix A: Corrections of Record

Nineteen claims from earlier iterations are restated in the shipped artifacts rather than in the sections that first made them, each with the claim as previously stated, the corrected statement, the archived file and key it derives from, and why it moved [ARTIFACT:art_ouNbQqPM59dp]. The substantive items new to this iteration are: the AMS paraphrase refit (§5.2, `DOES_NOT_SURVIVE`); the within-axis dissociation and the "at chance on both abliterated members" claim (§5.1, downgraded with $K = 0$ of $M = 4$); the semantic-reversal adjudication (§5.3, `REVERSAL_CONFOUNDED_BY_DEGENERACY` replaced by a measured `REVERSAL_DOES_NOT_SURVIVE` at matched contrast and `REVERSAL_SURVIVES` at B's unmatched peak); the "axis B induces almost nothing" claim, scoped to the depth panel with 1 of 2 breadth-panel counterexamples confirmed genuine; the aggregation unit of every correlation (§5.4); the archived relative depth, which is $0.25$ and not the $0.30$ this iteration's plan recorded; the random-direction null, rescoped from $0.00$–$0.058$ on six checkpoints to a measured induction floor reaching $0.389$ on 30; and nine bibliographic entries corrected against the arXiv API, including reference [23], whose previously cited title was not the title of the paper it pointed to. Carried forward unchanged from earlier iterations are the early-warning-signal direction control (difference-in-differences $-2.334$ $[-3.573, -1.037]$, direction-specific but failing Holm within its 48-test family at adjusted $p = 0.214$, and needing on the order of 1,880 prompts rather than 20); the observable-validity gate, which admits 0 model pairs at the layer-$L$ readout and 1 at the final-layer readout, on which no indicator separates; the relaxation-rate claim, withdrawn as non-identifiable on 640 of 640 rows; the $\alpha_{50}$ accounting, where the primary logistic estimator is `DEFINED` on 1 of 19 members and that member is itself among the 5 excluded as `UNRELIABLE`, leaving zero analysable members; the free-versus-forced perturbation asymmetry, restated as a right-tail effect conditional on stream divergence (61–88% of paired rollouts are exact ties) and unassociated with the member's own judged refusal rate ($\rho = -0.221$ $[-0.392, 0.315]$), hence a fact about autoregressive variance rather than alignment; and the full pre-registration deviation tables.

# References

[1] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043, 2023.

[2] P. Chao, E. Debenedetti, A. Robey, M. Andriushchenko, F. Croce, V. Sehwag, E. Dobriban, N. Flammarion, G. J. Pappas, F. Tramèr, H. Hassani, and E. Wong. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024.

[3] M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, E. Sakhaee, N. Li, S. Basart, B. Li, D. Forsyth, and D. Hendrycks. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024.

[4] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023.

[5] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024.

[6] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

[7] C.-C. Huang, Y.-L. Chen, C.-M. Yu, and W.-B. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. arXiv:2606.25750, 2026.

[8] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024.

[9] A. Borah, S. Sarkar, R. Aditya, R. Anand, S. Kumar, A. Chadha, and A. Das. Alignment Quality Index (AQI): Beyond Refusals — AQI as an Intrinsic Alignment Diagnostic via Latent Geometry, Cluster Divergence, and Layer-wise Pooled Representations. *EMNLP*, 2025. arXiv:2506.13901.

[10] T.-L. Li and H. Liu. Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness. arXiv:2506.24056, 2025.

[11] S. Basu et al. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. arXiv:2603.18353, 2026.

[12] C. Galeone, A. Ettorre, M. Park, G. Ettorre, and D. Ligorio. Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models. arXiv:2606.24952, 2026.

[13] J. Braun. Understanding Unreliability of Steering Vectors in Language Models: Geometric Predictors and the Limits of Linear Approximations. Master's thesis, University of Tübingen, 2026. arXiv:2602.17881.

[14] G. Hurtado. Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map. arXiv:2607.01854, 2026.

[15] S. Venkatesh and A. M. Kurapath. On the Non-Identifiability of Steering Vectors in Large Language Models. arXiv:2602.06801v4, 2026.

[16] J. Billa. Predicting Where Steering Vectors Succeed. arXiv:2604.15557, 2026.

[17] F. Joad, M. Hawasly, S. Boughorbel, N. Durrani, and H. T. Sencar. There Is More to Refusal in Large Language Models than a Single Direction. arXiv:2602.02132, 2026.

[18] R. Alagharu, I. S. Singh, S. Shamsudeen, Z. Wu, and A. Panda. From Refusal Tokens to Refusal Control: Discovering and Steering Category-Specific Refusal Directions. arXiv:2603.13359, 2026.

[19] V. Petrov. On the Failure of Topic-Matched Contrast Baselines in Multi-Directional Refusal Abliteration. arXiv:2603.22061, 2026.

[20] Y. Wang, X. Han, D. Shang, Y. Tang, and B. Liu. Safety, or Just Capability? A Validity Audit of Agent-Safety Benchmarks. arXiv:2607.28685, 2026.

[21] S. Weng, Y. Feng, and X. Xie. Beyond Accuracy: Policy Invariance as a Reliability Test for LLM Safety Judges. arXiv:2605.06161, 2026.

[22] J. Adebayo, J. Gilmer, M. Muelly, I. Goodfellow, M. Hardt, and B. Kim. Sanity Checks for Saliency Maps. *NeurIPS*, 2018.

[23] M. S. B. Nadaf. Steerable but Not Decodable: Function Vectors Operate Beyond the Logit Lens. arXiv:2604.02608v2, 2026.

[24] A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A.-K. Dombrowski, S. Goel, N. Li, M. J. Byun, Z. Wang, A. Mallen, S. Basart, S. Koyejo, D. Song, M. Fredrikson, J. Z. Kolter, and D. Hendrycks. Representation Engineering: A Top-Down Approach to AI Transparency. arXiv:2310.01405, 2023.

[25] A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, and M. MacDiarmid. Steering Language Models With Activation Engineering. arXiv:2308.10248, 2023.

[26] N. Rimsky, N. Gabrieli, J. Schulz, M. Tong, E. Hubinger, and A. M. Turner. Steering Llama 2 via Contrastive Activation Addition. *ACL*, 2024.

[27] X. Qi, A. Panda, K. Lyu, X. Ma, S. Roy, A. Beirami, P. Mittal, and P. Henderson. Safety Alignment Should Be Made More Than Just a Few Tokens Deep. *ICLR*, 2025.

[28] Q. Yin, C. T. Leong, L. Yang, W. Huang, W. Li, X. Wang, J. Yoon, X. Yun, X. Xing, and J. Gu. Refusal Falls off a Cliff: How Safety Alignment Fails in Reasoning? arXiv:2510.06036, 2025.

[29] A. Korznikov, A. V. Galichin, A. Dontsov, O. Y. Rogov, I. Oseledets, and E. Tutubalina. The Rogue Scalpel: Activation Steering Compromises LLM Safety. arXiv:2509.22067, 2025.

[30] M. Scheffer, J. Bascompte, W. A. Brock, V. Brovkin, S. R. Carpenter, V. Dakos, H. Held, E. H. van Nes, M. Rietkerk, and G. Sugihara. Early-warning signals for critical transitions. *Nature*, 461:53–59, 2009.

[31] M. Scheffer, S. R. Carpenter, T. M. Lenton, J. Bascompte, W. Brock, V. Dakos, J. van de Koppel, I. A. van de Leemput, S. A. Levin, E. H. van Nes, M. Pascual, and J. Vandermeer. Anticipating Critical Transitions. *Science*, 338(6105):344–348, 2012.

[32] V. Dakos, S. R. Carpenter, W. A. Brock, A. M. Ellison, V. Guttal, A. R. Ives, S. Kéfi, V. Livina, D. A. Seekell, E. H. van Nes, and M. Scheffer. Methods for Detecting Early Warnings of Critical Transitions in Time Series Illustrated Using Simulated Ecological Data. *PLoS ONE*, 7(7):e41010, 2012.

[33] T. M. Bury. ewstools: A Python package for early warning signals of bifurcations in time series data. *Journal of Open Source Software*, 8(82):5038, 2023.

[34] P. Röttger, H. R. Kirk, B. Vidgen, G. Attanasio, F. Bianchi, and D. Hovy. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL*, 2024.

[35] A. Yang et al. Qwen3 Technical Report. arXiv:2505.09388, 2025.

[36] L. Ben Allal, A. Lozhkov, E. Bakouch, G. Martín Blázquez, G. Penedo, L. Tunstall, A. Marafioti, H. Kydlíček, A. Piqueres Lajarín, V. Srivastav, J. Lochner, C. Fahlgren, X. Nguyen, C. Fourrier, B. Burtenshaw, H. Larcher, H. Zhao, C. Zakka, M. Morlon, C. Raffel, L. von Werra, and T. Wolf. SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model. arXiv:2502.02737, 2025.

[37] Y. Wu, S. Zhao, and J. Chen. When Is a Steerable Concept Representation Real? Measurement Confounds in a Cross-Family Audit of Neuroscience Parallels in LLMs. arXiv:2608.08159, 2026.

[38] A. Mishra, D. Khashabi, and A. Liu. Steered LLM Activations are Non-Surjective. *ICLR 2026 Workshops (Sci4DL, Re-Align)*. arXiv:2604.09839v2, 2026.

[39] A. A. Hasan and S. Biswas. The Refusal–Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models. arXiv:2605.05427v2, 2026.

[40] Y. Li, A. Fastowski, E. Zaradoukas, B. Prenkaj, and G. Kasneci. Analysing the Safety Pitfalls of Steering Vectors. arXiv:2603.24543, 2026.

[41] M. Taimeskhanov, S. Vaiter, and D. Garreau. Towards Understanding Steering Strength. *ICML*, 2026. arXiv:2602.02712v2.

[42] E. Rahimi, E. Hirshel, R. Himelstein, A. LeVi, A. Mendelson, and C. Baskin. Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models. arXiv:2602.02600v3, 2026.

[43] A. Kwon. Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak. arXiv:2607.14147, 2026.

[44] A. Mehta. The Refusal Residue: When Probes Catch Alignment Faking and When They Don't. *Mechanistic Interpretability Workshop, ICML 2026*. arXiv:2607.13346, 2026.

[45] I. Llorente-Saguer. The Geometry of Harmful Intent: Training-Free Anomaly Detection via Angular Deviation in LLM Residual Streams. arXiv:2603.27412, 2026.

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The paper's new headline — 'reading and steering along one refusal axis are coupled, ρ = 0.629 [0.465, 0.803]' — is computed over 70 (member, axis) pairs, i.e. 14 members × 5 axes, pooling the canonical axis A with the paraphrase axis B and the three control axes C (stylistic), D (random) and E (prompt contrast). Axes C and D are constructed to be null in both roles and axis A is known to be strong in both, so the pooled Spearman is dominated by a between-axis-type contrast, not by a read–act relationship. I recomputed the same relationship within the canonical axis across the 13 detection-powered members using the paper's own shipped tables (T2 A-AUROC against T3 A-max-refusal-rate): Spearman ρ = 0.434, p = 0.14 — the coupling does not survive removal of the axis-type contrast. The lineage bootstrap on 7 lineages does not address this, because the confound is within-member, not between-lineage. The within-member mean ρ of 0.715 makes the problem worse rather than better: it is the mean of 14 Spearman coefficients computed on 5 points each, over the same axis-type contrast. Since this correlation is the evidence for the paper's central reversal (§5.1, the contributions list, the Discussion and the Conclusion all lead with it), the claim as stated is not supported by the analysis that produces the number.
  Action: Make the within-axis-A, across-member correlation the primary statistic for the coupling claim (n = 13-14 detection-powered members, lineage-clustered bootstrap, both aggregation units as the paper now requires of itself), and report the 70-pair pooled version explicitly as a secondary that mixes between-axis and between-model variance. If the within-axis estimate is 0.43 with a CI covering zero, say so — the honest statement then becomes 'the axis that induces is also the axis that reads, but among models the two qualities are only weakly and non-significantly related', which is still a clean reversal of the earlier dissociation claim and is defensible. Alternatively, fit a mixed-effects or partial-correlation model with an axis fixed effect and report the residual member-level coupling. Also add the trivial control: report ρ with axes C and D dropped, so a reader can see how much of the 0.629 is the control contrast.
- [MAJOR] (rigor) The 'zero AT_CHANCE' result is partly an artifact of an n-asymmetric verdict rule, and the Method misdescribes the gate the code applies. The paper states: 'a member is READS when the CI lower bound exceeds 0.60, AT_CHANCE when the whole CI lies inside [0.40, 0.60], and UNDEFINED when fewer than 40 refusals exist'. In the shipped per-member table, READS is issued at 7 refusals (TinyLlama-1.1B-Chat, AUROC 1.000 [1.000, 1.000]), 12 (Josiefied-Qwen2.5-3B-abliterated, 0.889 [0.688, 1.000]), 28, 32 and 33 — all of which the artifact's own 'pow' column marks N (not detection-powered). Only members with 0 or 1 refusals return UNDEFINED. This matters in two ways. First, READS at low n requires only a lower bound above 0.60, which perfect separation on a handful of items delivers automatically, whereas AT_CHANCE requires the entire bootstrap CI inside a 0.20-wide band, which is unreachable at n ≈ 10; 'zero AT_CHANCE over 30 checkpoints' is therefore not a property of the models but partly of the rule. Second, and more damagingly for the paper's key structural claim, the weight-edited abliteration arm's 5 READS verdicts rest on refusal counts of 12, 28, 32, 33 and 150 — exactly 1 of the 5 is powered. The claim that 'abliteration removes the refusals to be read, not the axis's ability to read them' is therefore carried, on the abliterated arm, by four underpowered estimates.
  Action: Report the verdict tally twice: once as-is, and once restricted to detection-powered members (≥40 per class), which is the population the pre-registration says the statistic exists on. State the minimum n at which AT_CHANCE is attainable under the CI rule (a two-line simulation), and add it as a footnote to every 'zero AT_CHANCE' statement. Correct the Method's description of the UNDEFINED gate to what the code does, and log it as a deviation with its trigger, as the paper does elsewhere. For the abliterated arm specifically, either extend the escalation ladder on the four underpowered READS members until they clear 40, or restate the arm's conclusion as resting on 1 powered member plus 4 underpowered ones, and give their CIs in the main text.
- [MAJOR] (methodology) The detection task is partly definitional, which inflates axis A's AUROC and contaminates the coupling claim. Axis A is fitted as the contrast between four hand-written canned refusals and four compliances; the detection labels are assigned by an anchored refusal regex matching canned refusal openers. So 'the canonical axis reads refusals at AUROC 0.69-1.00' is close to saying that a direction fitted on canned-refusal wording separates text that opens with canned-refusal wording. The A-vs-B comparison controls for this partially (B is token-disjoint), but the absolute AUROCs that the paper reports as its headline reading result, and the induction-vs-detection correlation built on them, both inherit it. The paper is aware of the lexical hazard on the induction side — that is exactly what §5.3 is about — but does not apply the same scepticism to the reading side, where the same regex is now the label rather than the outcome. The five-class semantic judge built for §5.3 is already available and would settle it.
  Action: Re-score the detection labels on a stratified subset of the spontaneous generations with the five-class semantic rubric (including the non-canonical-refusal class), and re-report axis A's AUROC against semantic labels for at least the detection-powered members. Report the delta between regex-labelled and semantically-labelled AUROC. If the AUROC holds up, that is a strong result and removes the objection in one paragraph; if it drops, the reversal in §5.1 needs restating as 'the axis reads canonically-worded refusals'. Either way, add one sentence to §5.1 acknowledging that the label and the axis share a lexical basis.
- [MAJOR] (scope) The scale panel was spent on the wrong score. Table 1 and Table 3 show that the logit-gap margin on harmful prompts is the only score whose CI excludes zero at BOTH aggregation units (ρ = 0.667 [0.439, 0.904] member, 0.929 [0.412, 1.000] lineage, permutation p = 0.0038 / 0.0067), and it costs 80 forward passes and zero generations per model. The paper's own load-bearing observation is that this score predicts best while passing fewest hygiene checks. Yet the 52-member / 28-lineage scale panel — the entire budget for the one instrument that could adjudicate a score at n_lineage = 28 — was spent replicating the AMS paraphrase refit, which duly failed. The result is a paper whose central lesson (seven-lineage predictive validity is unreliable) is demonstrated on the score that lost, and left unexamined on the score that won. A reader will immediately ask whether ρ = 0.667 also collapses at 28 lineages, and the paper cannot answer. This is the difference between a paper that ends in a fourth negative and one that ends in either a usable cheap safety score or a genuinely decisive negative about the whole score class.
  Action: Run the logit-gap harmful-prompt margin (and, for the same cost, the benign variant and our-AMS σ, both already computed) on the 52-member / 28-lineage scale panel, and report ρ at both aggregation units with the Monte-Carlo lineage permutation null already implemented for §5.2. State the pre-registered outcome before running. If ρ holds near 0.667 at 28 lineages, lead the paper with it — 'the cheapest score in the class, 80 forward passes and no harmful generation, predicts judged harmful-refusal at ρ = X across 28 lineages' is a result platforms would adopt and would answer the introduction's motivating question. If it collapses like the refit did, the paper's thesis becomes far stronger: every cheap activation score tested collapses from 7 to 28 lineages, which is a general claim about the class rather than about one refit.
- [MINOR] (novelty) The three 'measurement decisions' offered as the paper's surviving contribution are quantified instances of textbook phenomena, and the paper does not name them as such. Item-pool provenance deciding a read-vs-act comparison is train/test leakage and distribution shift; the aggregation unit moving ρ by a median 0.238 and flipping 5 of 16 signs is aggregation (ecological) bias, closely related to Simpson's paradox and long documented in psychometrics and ecology; the collapse from n_lineage = 7 to 28 is small-sample correlation instability, which the paper itself cites Wang et al. [20] as having warned about in the abstract. Presenting them as three discoveries rather than three well-measured instances invites a reviewer to discount the contribution, when the honest framing (a rare public demonstration on the authors' own published result, with the effect localised to the original block) is actually more persuasive.
  Action: In the Discussion, name each phenomenon by its standard name and cite one canonical source for each, then claim the instance: 'we do not claim aggregation bias as a finding; we claim a measured instance in which it moves this study's own headline by 0.464 and flips 5 of 16 signs'. This costs three sentences and removes the strongest available novelty objection.
- [MINOR] (evidence) Several numbers drift between the intro, the sections and the shipped tables, which matters more than usual in a paper whose thesis is measurement discipline. The introduction says the axis 'reads at AUROC ≥ 0.68 on every one of the 20 checkpoints where reading is measurable'; §5.1 says ≥ 0.685; the artifact's per-member table has a minimum of 0.691. 'The 20 checkpoints where reading is measurable' conflicts with 20 READS + 1 AMBIGUOUS = 21 non-UNDEFINED members. The artifact's own top-line summary still reports 18 READS / 0 AT_CHANCE / 10 UNDEFINED against the paper's and RESULTS.md's 20/1/9. Reference [11] is cited as 'S. Basu et al.' with no author list. None of these changes a conclusion, but a reviewer checking the artifact hits the 18-vs-20 discrepancy first.
  Action: Take every quoted extremum directly from the generated table (the pipeline already regenerates RESULTS.md byte-identically from JSON — extend that to the paper's prose numbers), reconcile the artifact's stale summary block with RESULTS.md, fix 'measurable' to name the AMBIGUOUS member, and complete the [11] author list.
- [MINOR] (clarity) Tables are numbered out of order of appearance (Table 5 precedes Table 2; Table 1 first appears in §5.4), and the paper has no abstract. The per-member detection table in the main text also omits the two columns a reader most needs to evaluate §5.1 — the refusal/compliance counts and the detection-powered flag — both of which exist in the artifact's T2 table.
  Action: Renumber tables by first appearance, add an abstract that states the three surviving measurements and the two retractions, and add 'n refusals / n compliances' and 'powered (y/N)' columns to the main-text detection table.
- [MINOR] (rigor) Limitation (7) correctly flags that Mehta's per-fold residualisation control has not been run, and notes it moved his own AUROC by 0.336. Given that §5.1's entire reversal is an item-pool/leakage argument, and the paper's own framing is that 'the item pool decides the result', leaving the single published leakage control unrun on the very analysis it would test is the one place where the paper's methodological standard is not applied to its own headline. It is also cheap: the projections are already computed and the change is in how normalisation statistics are estimated.
  Action: Run the detection AUROC with all centring/normalisation statistics estimated inside the training fold and with leave-one-prompt-out (or leave-one-query-out) splits, on at least the detection-powered members, and report the delta. If it is small, that is a one-line strengthening of the headline; if it is large, the paper needs to know before publication rather than after.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-13 03:19:25 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```
