# gen_plan_experiment_2 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-12 23:08:16 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<hypothesis>
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter4_dir2
type: experiment
objective: >-
  EXTEND THE DISSOCIATION TO A REAL ABLITERATED PANEL AND SCOPE IT HONESTLY. Turn 'at chance in both roles on both abliterated
  members' (n=2, two producers, two scales) into a measured statement over K >= 6 abliterated / behavioural-uncensored checkpoints,
  and settle the reviewer's scope objection by running the matched-contrast induction test on the breadth-panel members where
  axis B DOES reach 0.50.
approach: >-
  Read the archived iteration-3 evaluation workspace directly from disk (it is not a permitted dependency type for an experiment).
  Reuse the archived axis-fitting, steering-hook and re-encoding code verbatim from 3_invention_loop/iter_3/gen_art/gen_art_evaluation_1
  (eval_lib, gpu_stage, axes/, proj/) and the iteration-2 steering modules, sha256-verified. PANEL: all abliterated (8) and
  behavioural-uncensored (13) members at <= 4.2B from the frozen manifest that load ungated, PLUS their parent base/instruct
  members where available so each abliterated member has an in-lineage reference, PLUS the two breadth-panel members on which
  axis B reaches 0.50 refusal. Report loads/skips explicitly; target K >= 6 abliterated-class members and state the achieved
  K. TWO MEASUREMENTS PER MEMBER, on the same five axes as the archive (A canned response contrast, B token-disjoint paraphrase,
  C norm-matched stylistic, D matched random, E prompt contrast), all re-derived with the archived fit code at the archived
  relative depth and pinned revision SHAs. (1) DETECTION: generate the model's OWN refusals and compliances (frozen benign
  prompts plus the plain-harmful core-80, greedy and temperature-0.7, max_new_tokens 64, batched), apply the archived exclusion
  cascade (duplicate prompt/text pairs, fluency screen, min length, degenerate) with the full scanned -> kept -> encoded accounting
  reported, class-balance, re-encode with token-ID concatenation (NOT string concatenation -- the archived bug that corrupted
  up to 450/1028 items), take stratum-centred projections at the first generated token, and report per-axis AUROC with prompt-clustered
  bootstrap CIs (2000 reps), the paired A-B difference with Holm correction, and the [0.40,0.60] indifference-band verdict.
  Assert zero overlap between axis-fit text and scored text. (2) INDUCTION: a coarse steering sweep on frozen benign prompts
  (>= 10 prompts x >= 3 seeds x a coefficient grid spanning at least 0 to the archived maxima), reporting refusal rate versus
  AXIS-CONTRAST UNITS (c = alpha*NORM_L/||X||) for every axis, the contrast units at 50% refusal where defined, and the matched-contrast
  paired A-minus-B advantage with CIs -- the decisive quantity, and the one that settles the breadth-panel counterexamples.
  HEADLINE OUTPUTS: (i) 'the canonical refusal axis is at chance in BOTH roles on K of M abliterated checkpoints' with the
  exact K/M and per-member CIs, or the honest weaker statement if K is small; (ii) a scoped restatement of the induction claim
  -- depth panel versus breadth panel -- with the two B-reaches-0.50 members measured at matched contrast units so the paper
  reports whether they are genuine counterexamples or norm artifacts; (iii) a joint read-versus-act scatter over ALL measured
  (member, axis) pairs, which is the first time this study has more than four points and directly answers the Discussion's
  own 'is any pair of induction and detection quality on the same axis related?' question -- report the correlation with a
  lineage bootstrap and state plainly if it is null. Budget: GPU only, judge calls capped at $1.50 with cumulative cost logged;
  use the deterministic anchored refusal regex as the primary criterion and the repaired judge only on a stratified subsample,
  reporting kappa.
depends_on:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type:
  relation_rationale:
- id: art_PeyWw78NIx9d
  label: positioning
  relation_type:
  relation_rationale:
- id: art_Qm_KL4GhZCnX
  label: positioning
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Dependency 2 ---
id: art_Qm_KL4GhZCnX
type: research
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
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 3 ---
id: art_PeyWw78NIx9d
type: research
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
out_dependency_files:
  file_list:
  - research_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-12 23:08:16 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```
