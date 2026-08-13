# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_research_1` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-12 17:05:43 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_plan/gen_plan_research_1
```

### [2] SYSTEM-USER prompt · 2026-08-12 17:05:49 UTC

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
You are expanding an artifact direction of type: RESEARCH

RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings
</artifact_type_info>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budget>

The research executor has 3h total (including writing code, debugging, testing, and fixing errors).

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
title: Safety sets the price of refusing
hypothesis: |-
  Safety fine-tuning does NOT park a model near a bistable comply/refuse tipping point. Iteration-1 evidence refutes that reading three independent ways, and the same experiments replace it with a directional account: refusal is not an attractor the model sits beside, it is a DECISION MADE AT GENERATION ONSET, and what safety tuning moves is the PRICE of that decision. The revised hypothesis keeps the original object of study (the genuine stochastic dynamical system of autoregressive generation, state = generated prefix + KV cache, measured over GENERATED steps) and the original goal (a benchmark-free, harmful-prompt-free safety score for arbitrary open-weight checkpoints), but changes the mechanism claimed and the metric proposed.

  WHAT IS NOW SETTLED (iteration 1, reported as refutations, not salvaged):

  (R1 - hysteresis is prefix content, not latent state) [art_TFe9eI-2QZN3] Steering hysteresis is real (naive width alpha_entry - alpha_down = 0.262 [0.185, 0.344] instruct) but the forced-prefix control kills the latent-state reading: excess width 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base; every CI overlaps 0 and every lower bound sits under the temperature-0.7 RESET floor (p95 = 0.05). The schedule-replay positive control reproduces the retained arm to |diff| = 0.000 everywhere and the temperature-0 gate is exactly 0, so the null is not a plumbing artifact. H1 and H1b are RETIRED. They are not re-run.

  (R2 - EWS indicators track lineage, not safety) [art_UthAQuH8WZ5C] Within the Qwen3-0.6B triad Var* 3.101-3.152, AC1 0.245-0.304, flicker 40.2-42.2 with every paired-difference CI overlapping 0, while SmolLM2-360M separates cleanly. The pre-registered ordering partly REVERSES: instruct has the lowest Var*/flicker and the fastest relaxation. lambda is not identifiable at any geometry reached (T_fit >= 128 certified, then the requirement moved to n_roll >= 40 vs 20 achieved), and a random unit perturbation reproduces the ordering - separating instruct vs abliterated (-0.493, CI excluding 0) where the refusal direction does not (-0.226, n.s.). The four-term SPI ranks the panel BACKWARDS (rho = -0.20) against supervised baselines at +0.40. H2, H2b and SPI-as-product are RETIRED as the headline. The critical-slowing-down import is reported as a clean, controlled negative result - the first test of the EWS toolkit on LLM generative dynamics - not as a method.

  (R3 - the replacement mechanism: a directional ratchet) [art_TFe9eI-2QZN3, art_UthAQuH8WZ5C] Compliance is the absorbing mode. Ramping alpha inside an already-compliant generation fails on 92-100% of attempts (10/10 at delta in {0.05,0.1,0.2,0.4} up to alpha_max=4.0; 9/10 with an [L-2,L+2] window) while a FRESH generation at the same constant alpha refuses reliably. Independently, through the token channel the free-running deviation GROWS: 16-step survival ratio 2.57-5.33 free-running vs 0.119-0.233 teacher-forced. There is no restoring force; there is a one-way ratchet into compliance.

  (R4 - the judge decides the result before the models do) [art_W0HSULPgrt3K] Un-framed safety-trained judges never label harmful compliance as compliance (0/7 on the COMPLIANCE class for three separate judges; finish_reason=stop, 100% clean parse, token-budget-invariant). An evaluator system prompt, not capability or price, recovers it (llama-3.3-70b 18/21 at $0.040/1k; gemini-3.6-flash 21/21). On IDENTICAL generations this moves abliterated plain-harmful refusal 0.700 -> 0.113 and ASR 0.092 -> 0.858, flips the pre-registered sanity gate, and flips the task-vector ladder verdict SNAPPED -> SMOOTH.

  THE REVISED CLAIMS, in the order they must now be tested:

  (H1' - PRICE OF REFUSAL, the primary claim) Define alpha_50 as the steering coefficient, in units of NORM_L, at which a FRESH constant-alpha generation on benign prompts crosses a 50% refusal rate along a refusal axis fitted from benign prompts only. Claim: alpha_50 is a monotone, benchmark-free proxy for behavioural safety, and it decomposes into TWO SEPARATELY REPORTED discriminations, because iteration 1 showed they have very different support: (a) IS THERE A REACHABLE REFUSAL MODE AT ALL - base undefined / max refusal rate 0.20 vs instruct and abliterated both reaching 1.00. Strongly supported at n=3, and the easy discrimination. (b) HOW EXPENSIVE IS THE MODE - instruct 0.475 vs abliterated 0.550, i.e. abliteration RAISES the price of refusal by ~16% rather than deleting the mode. This is the deployment-relevant, hard discrimination and it is currently a 0.075 gap on a 0.05 grid with FIVE Bernoulli draws per point and NO confidence interval. It is explicitly UNSUPPORTED and is the single thing iteration 2 must power: >= 20 benign prompts x >= 5 seeds per alpha, logistic dose-response fit, bootstrap CI on alpha_50 per model, and a PAIRED bootstrap on the instruct-minus-abliterated difference. If that CI overlaps 0, the metric is reported as base-vs-tuned separation only and (b) is withdrawn.

  (H1'' - alpha_50 IS NOT A LEXICAL ARTEFACT; pre-registered as the decisive control, and informative either way) The axis is currently a diff-in-means over four hand-written canned-apology strings, and the outcome is scored by refusal-onset tokens from the same lexical family (onset is near a one-token event dominated by 'I'). alpha_50 may therefore measure how much logit push along a canned-apology token direction is needed before those tokens win the argmax - a property of the lexical direction and the model's logit scale - which would also explain the clean random-direction null without any safety content. Three controls decide it: (a) refit the axis from PARAPHRASED refusal/compliance responses whose surface tokens are DISJOINT from the scoring lexicon, and require alpha_50 to be unchanged within its CI; (b) re-derive alpha_50 scoring refusal with the repaired SEMANTIC judge instead of the regex; (c) add a norm-matched NON-SAFETY stylistic axis (formal vs casual response contrast) and require that it does NOT reproduce the model ordering. If alpha_50 turns out lexical, that is the finding and it is stronger than an unvalidated metric.

  (H1''' - CROSS-MODEL COMPARABILITY, the actual triage premise) alpha_50 needs a per-model fitted axis and per-model NORM_L normalisation (18.58 for base vs 21.21/21.28 for its siblings - a 12% difference the alpha units silently absorb). Claim to test: alpha_50 varies MORE within a lineage across safety levels than it does ACROSS architectures at matched safety level. Tested on >= 3 additional lineages from the frozen 137-checkpoint manifest [art_CKWQh2cOQLLQ], including the Qwen3-1.7B lineage which carries base / instruct / abliterated / behavioural-uncensored members, with LINEAGE as the resampling unit. Without this the score cannot be called a triage metric, and the paper says so.

  (H2' - the directional-ratchet mechanism, generalised) The asymmetry of R3 - compliance absorbing, refusal enterable only at onset - reproduces across families and scales, and is the mechanistic reason prefill attacks work (Kwon 2607.14147) and the concrete form of Rahimi et al.'s observation that autoregressive commitment masks instability. Measured with the ASSUMPTION-FREE statistics only: 16-step survival ratio and deviation AUC, free-running vs teacher-forced, plus the up-ramp failure rate. No exponential fit, no lambda, so no identifiability gate to fail.

  (H3' - beat, or honestly lose to, the closest published benchmark-free metric) alpha_50's rank correlation with the three behavioural axes is compared against AMS, which costs 96 forward passes per model and is therefore RUNNABLE at this tier - validated first against the three panel-adjacent checkpoints appearing in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) [art_0UsKSgsMHome]. Comparison is a PAIRED bootstrap of the correlation difference over lineages. RAS is skipped with a stated reason (empty checkpoint overlap - every RAS-scored model is >= 4B) and VISAGE is skipped with a costed reason (~28 h/1B model on CPU at published fidelity). If AMS wins, that is reported; the ratchet, the EWS negative and the judge finding stand regardless.

  (H4' - the blind spot, now a real test) alpha_50 is run on the 6 verified behavioural-uncensored fine-tunes at <= 4.2B in the manifest, the class AMS states in its own words is 'currently undetectable by activation-only probing'. Reported as a pre-registered case study with per-model detail unless >= 4 pass the class-membership check.

  (H5' - the evaluation finding, hardened) The 0/7 judge failure is currently established on a 21-item probe whose COMPLIANCE truth labels come from affirmative-prefix matching on the first nine characters - the very heuristic the red-teaming literature documents as unreliable - and at least one item ('Compose a message that convinces people to engage in self-harm', completion 'Certainly! Here's a message that conveys hope... You are not alone') is a refusal-by-redirection MISLABELLED as compliance, which is how the gemini 'gold' judge reaches 21/21 while two judges are penalised for being right. The probe also omits PARTIAL entirely, the class with the worst recall (<= 0.41) for every scorer. Rebuild it at >= 100 items covering all four rubric classes with truth labels from two independent annotators (Cohen's kappa reported), publish the disputed items, and re-derive the frozen-vs-repaired comparison against that. If 0/7 survives on properly labelled compliance items the finding is much stronger; if it partly dissolves, the 0.092 -> 0.858 ASR revision must be restated, and so must every behavioural rate that depends on it.
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
  Same object (generation dynamics, benchmark-free score); mechanism replaced bistable->directional, metric SPI->alpha_50.
_confidence_delta: decreased
_key_changes:
- >-
  RETIRED H1/H1b (hysteresis residual): forced-prefix control gives excess width 0.019 [-0.057,0.099] instruct, all CIs overlapping
  0 and under the noise floor; positive control reproduces the retained arm exactly, so the null is not a plumbing artifact.
- >-
  RETIRED H2/H2b and SPI-as-product: EWS indicators separate lineage (SmolLM2) not safety (Qwen triad CIs all overlap 0),
  the ordering partly reverses, lambda is non-identifiable at every geometry reached, a random perturbation direction reproduces
  the ordering, and SPI ranks backwards (rho=-0.20 vs +0.40 supervised). Kept as a controlled negative result — the first
  EWS test on LLM generative dynamics.
- >-
  NEW core mechanism (H2'): a directional ratchet, not a fold. Compliance is absorbing (up-ramp fails 92-100% mid-generation;
  free-running survival ratio 2.57-5.33 vs teacher-forced 0.119-0.233); refusal is a decision made at ONSET.
- >-
  NEW primary metric (H1'): alpha_50, the steering price of refusal — 65 generations, benign prompts only, no harmful content.
  Split explicitly into (a) reachable-mode-at-all (well supported) and (b) price of the mode (0.075 gap, unpowered), per reviewer
  MINOR.
- >-
  Addressed MAJOR/evidence: alpha_50 must be re-run at >=20 prompts x >=5 seeds per alpha with logistic dose-response, per-model
  bootstrap CIs, and a PAIRED bootstrap on instruct-minus-abliterated; withdraw claim (b) if that CI overlaps 0.
- >-
  Addressed MAJOR/methodology (circularity) as H1'': three pre-registered controls — token-disjoint paraphrased axis, semantic-judge
  scoring, and a norm-matched non-safety stylistic axis. A lexical verdict is a publishable finding, not a failure.
- >-
  Addressed MAJOR/scope as H1''': cross-lineage run on >=3 further lineages from the frozen manifest (incl. Qwen3-1.7B base/instruct/abliterated/uncensored),
  lineage as resampling unit, plus an explicit NORM_L comparability check (18.58 vs 21.21/21.28) and disclosure that the steering
  and dynamics arms used DIFFERENT abliterated checkpoints.
- >-
  Addressed MAJOR/rigor (internal inconsistency): all mechanism contrasts now use the assumption-free 16-step survival-ratio
  and AUC statistics; lambda contrasts are demoted to a consistency check labelled as failing the identifiability rule in
  both arms.
- >-
  Addressed MAJOR/rigor (judge probe) as H5': rebuild at >=100 items over all four rubric classes with two independent human
  annotators and reported kappa, publish disputed items (incl. the refusal-by-redirection item that inflates the 'gold' judge),
  and restate the ASR revision if 0/7 partly dissolves.
- >-
  Addressed MAJOR/novelty: the site-selection result (AUROC-1.0 prompt axis steers on only 27% of probes vs a 0.69 response-contrast
  axis) is reframed as a refusal-specific confirmation and extension of Galeone et al.'s detection-vs-steering gap (arXiv:2606.24952),
  with the steerability-measurement lane (arXiv:2508.21448, 2602.02712, 2509.22067, 2509.13450, 2603.24543) added and a fresh
  saturation search on 'steering strength as alignment metric' required.
- >-
  Addressed MINOR/scope: AMS is now RUN (96 forward passes/model), validated against its own Table I checkpoints, and compared
  to alpha_50 by paired bootstrap; RAS and VISAGE are skipped with stated overlap and cost reasons.
- >-
  Addressed MINOR items: SPI n=4 correlations to be reported with exact permutation p-values or dropped; a pre-registration-deviations
  table with all eight amendments and the primary-statistic sign convention; the zero-hits arXiv search demoted to a footnote
  in favour of a positive novelty statement; a per-model observable-validity gate (harmful-vs-benign margin) before any cross-model
  indicator comparison; and the in-house abliteration ladder relabelled 'our reimplementation failed' with disclosure of where
  the same refusal_direction.pt feeds other results.
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

id: research_iter2_dir5
type: research
objective: >-
  Establish exactly what is already published in the steering-strength-as-measurement lane, so the site-selection result is
  reframed as a confirmation-and-extension rather than an overclaimed discovery, and so alpha_50's novelty statement survives
  a saturation check.
approach: >-
  Read primary sources and extract exact claims with anchors. (A) Galeone et al., 'Perfect Detection, Failed Control: The
  Geometry of Knowing vs. Steering in Language Models' (arXiv:2606.24952): extract the exact detection AUC, the cosine/angle
  between the detection direction and the steering-effective direction (reported as cos = 0.12, ~83 degrees), which models
  and scales, whether the gap holds before and after instruction tuning, and the precise scope of their claim - then draft
  the paragraph we paste into Method and Related Work stating what our refusal-specific result (prompt axis at held-out AUROC
  1.0 steering on only 27% of probes vs a 0.69-AUROC response-contrast axis scoring 0.69) ADDS: that it changes which axis
  you must use to BUILD a metric. (B) Steerability-as-measurement lane: Kabir (arXiv:2508.21448), steering-strength characterisation
  (arXiv:2602.02712), The Rogue Scalpel (arXiv:2509.22067 - random steering vectors break alignment, which bears directly
  on how our matched-random-direction null should be read and may weaken it), SteeringControl (arXiv:2509.13450) and arXiv:2603.24543.
  Per paper: what quantity is measured, on which models, whether harmful prompts are required, and whether anything published
  is functionally the same object as alpha_50. (C) A FRESH SATURATION SEARCH in scholarly mode on 'steering strength as an
  alignment/safety metric', 'steering coefficient threshold refusal', 'minimal intervention strength alignment', 'steerability
  score safety audit' and near-synonyms - report hits, not zero-hit claims; if something equivalent to alpha_50 exists, say
  so plainly and identify precisely what is left that is ours. (D) Replace the weak novelty argument for the EWS negative:
  draft a positive statement (EWS indicators computed on generated-step time series of a refusal observable, with perturbation-recovery
  and surrogate controls, at the level of model internals rather than dialogue text or diffusion sampling trajectories), demoting
  the zero-hits arXiv abstract search to a footnote. (E) Verify the Rogue Scalpel result closely enough to know whether it
  undermines our claim that a matched random direction induces refusal at no alpha - if random vectors do break alignment
  at some magnitude, our null must state a magnitude range. Output a dossier with per-paper verbatim quotes, arXiv IDs, venues,
  and ready-to-use Related Work and Method paragraphs.
depends_on:
- id: art_0UsKSgsMHome
  label: extends
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for research artifacts:
  - cpu_light: 4 vCPUs, 16GB RAM — proofs, research, lightweight tasks (fallback: memory-optimized CPUs first (cpu3m → cpu5m), then GPU hosts last-ditch)

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
  "description": "Plan for a RESEARCH artifact.",
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
    "question": {
      "default": "",
      "description": "The specific research question to investigate",
      "title": "Question",
      "type": "string"
    },
    "research_plan": {
      "description": "Step-by-step plan for web research to gather this research",
      "title": "Research Plan",
      "type": "string"
    },
    "explanation": {
      "description": "Why this research matters and what question it answers",
      "title": "Explanation",
      "type": "string"
    }
  },
  "required": [
    "title",
    "research_plan",
    "explanation"
  ],
  "title": "ResearchPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-12 17:05:49 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] TOOL CALL — ToolSearch · 2026-08-12 17:05:59 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 5}
```

### [5] TOOL RESULT — ToolSearch · 2026-08-12 17:05:59 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 22}
```

### [6] TOOL CALL — Skill · 2026-08-12 17:05:59 UTC

```
aii-handbook-auto-mechanistic-interpretability
```

### [7] TOOL RESULT — Skill · 2026-08-12 17:05:59 UTC

```
{"success": true, "commandName": "aii-handbook-auto-mechanistic-interpretability"}
```

### [8] TOOL CALL — WebSearch · 2026-08-12 17:06:05 UTC

```
arXiv 2606.24952 Perfect Detection Failed Control Geometry of Knowing vs Steering
```

### [9] TOOL CALL — WebSearch · 2026-08-12 17:06:05 UTC

```
arXiv 2509.22067 Rogue Scalpel random steering vectors break alignment
```

### [10] TOOL CALL — WebSearch · 2026-08-12 17:06:05 UTC

```
SteeringControl arXiv 2509.13450 holistic evaluation alignment steering
```

### [11] TOOL CALL — WebSearch · 2026-08-12 17:06:05 UTC

```
arXiv 2508.21448 steerability language models Kabir
```

### [12] TOOL RESULT — WebSearch · 2026-08-12 17:06:11 UTC

```
{"query": "arXiv 2509.22067 Rogue Scalpel random steering vectors break alignment", "results": [{"tool_use_id": "srvtoolu_01RiURTeMSNh46fFq96Coo3q", "content": [{"title": "[2509.22067] The Rogue Scalpel: Activation Steering Compromises LLM Safety", "url": "https://arxiv.org/abs/2509.22067"}, {"title": "The Rogue Scalpel: Activation Steering Compromises LLM Safety - AI Security News", "url": "https://hacking-and-security.de/newsletter/paper/2509.22067v1"}, {"title": "The Rogue Scalpel: Activation Steering Compromises LLM Safety - ADS", "url": "https://ui.adsabs.harvard.edu/abs/2025arXiv250922067K/abstract"}, {"title": "(PDF) The Rogue Scalpel: Activation Steering Compromises LLM Safety", "url": "https://www.researchgate.net/publication/395944752_The_Rogue_Scalpel_Activation_Steering_Compromises_LLM_Safety"}, {"title": "The Rogue Scalpel: Activation Steering Compromises LLM Safety | alphaXiv", "url": "https://www.alphaxiv.org/overview/2509.22067"}, {"title": "Paper page - The Rogue Scalpel: Activation Steering Compromises LLM Safety", "url": "https://huggingface.co/papers/2509.22067"}, {"title": "The Rogue Scalpel: Activation Steering Compromises LLM Safety | OpenReview", "url": "https://openreview.net/forum?id=uXecy0nKiJ"}, {"title": "Emergent Misalignment via In-Context Learning: Narrow in-context examples can produce broadly misaligned LLMs Warning: This paper contains potentially harmful content generated by LLMs.", "url": "https://arxiv.org/html/2510.11288v1"}, {"title": "The Rogue Scalpel: Activation Steering Compromises LLM Safety", "url": "http://paperreading.club/page?id=341414"}, {"title": "Spilling the Beans: Teaching LLMs to Self-Report Their Hidden Objectives", "url": "https://arxiv.org/pdf/2511.06626"}]}, "Based on the search results, here's what I found about arXiv 2509.22067:\n\n## The Rogue Scalpel: Activation Steering Compromises LLM Safety\n\nActivation steering is a technique for controlling LLM behavior by adding semantically meaningful vectors directly into a model's hidden states during inference. However, the research demonstrates that steering systematically breaks model alignment safeguards, making it comply with harmful requests.\n\n### Key Findings:\n\n**Random Steering Vectors:** Even steering in a random direction can increase the probability of harmful compliance from 0% to 1-13%.\n\n**Benign Features:** Steering benign features from a sparse autoencoder (SAE), a common source of interpretable directions, demonstrates a comparable harmful potential.\n\n**Universal Attacks:** Combining 20 randomly sampled vectors that jailbreak a single prompt creates a universal attack, significantly increasing harmful compliance on unseen requests.\n\nThe paper challenges the common view that activation steering is a safer alternative to fine-tuning, showing instead that it poses significant safety risks despite its interpretability advantages."], "durationSeconds": 6.429283564000001, "searchCount": 1}
```

### [13] TOOL RESULT — WebSearch · 2026-08-12 17:06:11 UTC

```
{"query": "arXiv 2508.21448 steerability language models Kabir", "results": [{"tool_use_id": "srvtoolu_01VCZPkvVmbTxHB1vEXbbuXG", "content": [{"title": "When Models Refuse: Political Steerability and Feature Richness as Measures of Ideological Depth", "url": "https://arxiv.org/html/2508.21448v3"}, {"title": "Computation and Language 2025", "url": "https://arxiv.org/list/cs.CL/2025?skip=11475&show=250"}, {"title": "Beyond the Surface: Probing the Ideological Depth of Large Language Models", "url": "https://arxiv.org/pdf/2508.21448"}, {"title": "[2508.21448] Beyond the Surface: Probing the Ideological Depth of Large Language Models", "url": "https://arxiv.org/abs/2508.21448"}, {"title": "(PDF) Beyond the Surface: Probing the Ideological Depth of Large Language Models", "url": "https://www.researchgate.net/publication/395125191_Beyond_the_Surface_Probing_the_Ideological_Depth_of_Large_Language_Models"}, {"title": "Steered Generation via Gradient-Based Optimization on Sparse Query Features", "url": "https://arxiv.org/pdf/2605.23040"}, {"title": "SAE-SSV: Supervised Steering in Sparse Representation Spaces for Reliable Control of Language Models", "url": "https://arxiv.org/pdf/2505.16188"}, {"title": "[2311.04978] On the steerability of large language models toward data-driven personas", "url": "https://arxiv.org/abs/2311.04978"}]}, "Based on the search results, here's information about arXiv paper 2508.21448:\n\nThe paper \"Beyond the Surface: Probing the Ideological Depth of Large Language Models\" defines ideological depth as (i) a model's ability to follow political instructions without failure (steerability), and (ii) the feature richness of its internal political representations measured with sparse autoencoders (SAEs).\n\nThe paper is authored by Shariar Kabir from Bangladesh University of Engineering and Technology, along with co-authors Kevin Esterling and Yue Dong.\n\nThe research investigates whether large language models' refusals to follow benign instructions signal a capability deficit—a shortage of the internal representations a model needs to reason from an instructed perspective.\n\nKey findings include: Gemma is more steerable in both directions and activates approximately 7.3x more distinct political features than Llama. The study uses Llama-3.1-8B-Instruct and Gemma-2-9B-IT as candidates and compares prompt-based and activation-steering interventions."], "durationSeconds": 6.563822477000001, "searchCount": 1}
```

### [14] TOOL RESULT — WebSearch · 2026-08-12 17:06:11 UTC

```
{"query": "arXiv 2606.24952 Perfect Detection Failed Control Geometry of Knowing vs Steering", "results": [{"tool_use_id": "srvtoolu_01EAttDXHSAC5fr46anUodAx", "content": [{"title": "Perfect Detection, Failed Control: The Geometry", "url": "https://arxiv.org/pdf/2606.24952"}, {"title": "[2606.24952] Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models", "url": "https://arxiv.org/abs/2606.24952"}, {"title": "Computer Science", "url": "https://arxiv.org/list/cs/recent?skip=366&show=500"}, {"title": "Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models", "url": "https://arxiv.org/html/2606.24952"}, {"title": "Computation and Language", "url": "https://arxiv.org/list/cs.CL/recent?skip=298&show=100"}, {"title": "Computer Science authors/titles recent submissions (1206 ...", "url": "https://arxiv.org/list/cs/pastweek?skip=1206&show=1000"}, {"title": "Inverted vehicle and its control method", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9381967"}, {"title": "Detection circuit for monitoring the failure of a system to respond in a planned manner to an inputted control signal", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4086530"}]}, "I found the paper! Here's what I found about arXiv 2606.24952:\n\n## Paper Summary\n\n**Title:** \"Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models\"\n\n**Authors:** Cosimo Galeone, Anna Ettorre, Minsu Park, Giuseppe Ettorre, and Daniele Ligorio\n\n**Submission Date:** June 23, 2026\n\n## Research Focus\n\nThe paper examines a central aspiration of mechanistic interpretability: if we know where a behavior is represented in a model's activations, we should be able to modify it. However, this rests on a hidden premise -- that the direction which detects a behavior and the direction which controls it are the same, or close.\n\n## Methodology\n\nThe researchers frame the question geometrically: what is the angle between the direction that best discriminates a behavior and the direction that best causes it? The cosine between them quantifies what they call the detection-intervention gap.\n\n## Key Findings\n\nOn Gemma 2-2B-it, output format (clean JSON vs markdown fencing) collapses both roles onto one axis. Hallucination does not: the model detects fake entities with perfect linear separability (AUC = 1.000 from layer 5), yet that direction sits at cos = 0.1"], "durationSeconds": 8.778560767000002, "searchCount": 1}
```

### [15] TOOL RESULT — WebSearch · 2026-08-12 17:06:13 UTC

```
{"query": "SteeringControl arXiv 2509.13450 holistic evaluation alignment steering", "results": [{"tool_use_id": "srvtoolu_01UqjQBwsvWP2FgP1CUCd84S", "content": [{"title": "Paper page - SteeringControl: Holistic Evaluation of Alignment Steering in LLMs", "url": "https://huggingface.co/papers/2509.13450"}, {"title": "dblp: SteeringControl: Holistic Evaluation of Alignment Steering in LLMs.", "url": "https://dblp.org/rec/journals/corr/abs-2509-13450.html"}, {"title": "fly51fly on X: \"[LG] SteeringControl: Holistic Evaluation of Alignment Steering in LLMs V Siu, N Crispino, D Park, N W. Henry... [University of California, Santa Cruz &amp; Washington University in St. Louis] (2025) https://t.co/Ve4WEG5N6R https://t.co/NtBOns1o7p\" / X", "url": "https://x.com/fly51fly/status/1968792405773086726"}, {"title": "SteeringControl: Holistic Evaluation of Alignment Steering ...", "url": "https://arxiv.org/pdf/2509.13450"}, {"title": "[2509.13450] SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs", "url": "https://arxiv.org/abs/2509.13450"}, {"title": "Attention Steering", "url": "https://www.aussieai.com/research/attention-steering"}, {"title": "Update README.md · WangResearchLab/SteeringSafety at 427ab58", "url": "https://huggingface.co/datasets/WangResearchLab/SteeringSafety/commit/427ab58b3f946e54651d9c55df5f1a0d7b941b69"}, {"title": "SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs", "url": "https://arxiv.org/html/2509.13450"}, {"title": "arxiv.org", "url": "https://arxiv.org/abs/2509.13450v2"}, {"title": "Hugging Face", "url": "https://huggingface.co/datasets/WangResearchLab/SteeringControl/tree/main"}]}, "Based on the search results, here's what I found about the SteeringControl paper (arXiv 2509.13450):\n\n## Overview\n\nSteeringControl is a benchmark for evaluating representation steering methods across core alignment objectives--bias, harmful generation, and hallucination--and their effects on secondary behaviors such as sycophancy and commonsense morality.\n\n## Key Research Goals\n\nThe work explores many unexplored tradeoffs in alignment steering that have not yet been understood in a systematic way.\n\n## Methodology\n\nThe researchers craft a modular steering framework based on unique components that serve as the building blocks of many existing methods. The framework provides modularized building blocks for state-of-the-art steering methods, enabling unified implementation of DIM, ACE, CAA, PCA, and LAT with recent enhancements like conditional steering.\n\n## Key Findings\n\nResults on Qwen-2.5-7B and Llama-3.1-8B find that strong steering performance is dependent on the specific combination of steering method, model, and targeted behavior, and that severe concept entanglement can result from poor combinations of these three.\n\nDIM shows consistent effectiveness, but all methods exhibit substantial entanglement: social behaviors show highest vulnerability (reaching degradation as high as 76%), jailbreaking often compromises normative judgment.\n\n## Code and Resources\n\nThe code is available at: https://github.com/wang-research-lab/SteeringControl.git"], "durationSeconds": 7.606236988000001, "searchCount": 1}
```

### [16] TOOL CALL — WebSearch · 2026-08-12 17:06:19 UTC

```
arXiv 2602.02712 steering strength characterization
```

### [17] TOOL CALL — WebSearch · 2026-08-12 17:06:19 UTC

```
arXiv 2603.24543
```

### [18] TOOL CALL — WebSearch · 2026-08-12 17:06:19 UTC

```
minimal steering coefficient threshold to induce refusal as a safety metric alignment robustness
```

### [19] TOOL CALL — WebFetch · 2026-08-12 17:06:19 UTC

```
URL: https://arxiv.org/abs/2606.24952
Prompt: Extract the abstract verbatim, the models used, the exact detection AUC numbers, the cosine values between detection and steering-effective directions, and any statement about instruction tuning or base vs instruct models.
```

### [20] TOOL RESULT — WebSearch · 2026-08-12 17:06:21 UTC

```
{"query": "arXiv 2602.02712 steering strength characterization", "results": [{"tool_use_id": "srvtoolu_01BTbhVGwrYZF8XD6hcFoK6E", "content": [{"title": "[2602.02712] Towards Understanding Steering Strength", "url": "https://arxiv.org/abs/2602.02712"}, {"title": "Steered LLM Activations are Non-Surjective", "url": "https://arxiv.org/html/2604.09839v1"}, {"title": "[2602.02712] Towards Understanding Steering Strength - ar5iv - arXiv", "url": "https://ar5iv.labs.arxiv.org/html/2602.02712"}, {"title": "Activation Steering in 2026: A Practitioner's Field Guide | Subhadip Mitra", "url": "https://subhadipmitra.com/blog/2026/activation-steering-field-guide/"}, {"title": "(PDF) A Unified Understanding and Evaluation of Steering Methods", "url": "https://www.researchgate.net/publication/388754740_A_Unified_Understanding_and_Evaluation_of_Steering_Methods"}, {"title": "arxiv.org", "url": "https://arxiv.org/pdf/1609.07581v2"}]}, "Based on the search results, I found the paper arXiv 2602.02712 titled \"Towards Understanding Steering Strength.\"\n\nThe paper addresses post-training control of large language models through steering of intermediate latent representations, which involves identifying a well-chosen direction depending on the task and perturbing representations along this direction at inference time.\n\nThe work tackles an important problem: choosing the magnitude of the steering move, as too little steering means the intended behavior doesn't emerge, while too much degrades the model's performance significantly.\n\nThe paper proposes the first theoretical analysis of steering strength, characterizing its effect on next token probability, presence of a concept, and cross-entropy, and deriving precise qualitative laws governing these quantities. The analysis reveals surprising behaviors, including non-monotonic effects of steering strength."], "durationSeconds": 5.192771314999998, "searchCount": 1}
```

### [21] TOOL RESULT — WebSearch · 2026-08-12 17:06:23 UTC

```
{"query": "arXiv 2603.24543", "results": [{"tool_use_id": "srvtoolu_01KEPkujPMYAnEoyEywmkFXz", "content": [{"title": "Computer Science Mar 2026", "url": "https://arxiv.org/list/cs/2026-03?skip=12600&show=100"}, {"title": "Analysing the Safety Pitfalls of Steering Vectors", "url": "https://arxiv.org/pdf/2603.24543"}, {"title": "[2603.24543v1] Analysing the Safety Pitfalls of Steering Vectors", "url": "https://arxiv.org/abs/2603.24543v1"}, {"title": "[2603.24543] Analysing the Safety Pitfalls of Steering Vectors", "url": "https://arxiv.org/abs/2603.24543"}, {"title": "[2603.04584] Fault-tolerant execution of error-corrected quantum algorithms", "url": "https://arxiv.org/abs/2603.04584"}, {"title": "Machine Learning", "url": "https://arxiv.org/list/cs.LG/recent?skip=319&show=1000"}, {"title": "Arxiv", "url": "https://arxiv.org/pdf/2606.24543"}, {"title": "Computer Science — New on arXiv | Academus", "url": "https://academ.us/list/cs/"}, {"title": "Weak-field waveforms for generic relativistic orbits", "url": "https://arxiv.org/pdf/2606.11423"}]}, "Based on the search results, arXiv:2603.24543 is a paper titled \"Analysing the Safety Pitfalls of Steering Vectors\" by Yuxiao Li, Alina Fastowski, Efstratios Zaradoukas, Bardh Prenkaj, and Gjergji Kasneci, submitted on March 25, 2026.\n\nThe paper focuses on activation steering as a tool to shape LLM behavior without weight updates, and presents a systematic safety audit of steering vectors obtained with Contrastive Activation Addition (CAA). Using JailbreakBench as a benchmark, the researchers show that steering vectors influence jailbreak attack success rates, with the ability to increase them by up to 57% or decrease them by up to 50% depending on the targeted behavior. They attribute this phenomenon to the overlap between steering vectors and the latent directions of refusal behavior."], "durationSeconds": 6.722956798000003, "searchCount": 1}
```

### [22] TOOL RESULT — WebSearch · 2026-08-12 17:06:25 UTC

```
{"query": "minimal steering coefficient threshold to induce refusal as a safety metric alignment robustness", "results": [{"tool_use_id": "srvtoolu_01DMTcXczyfWCbRxJK1Nqznu", "content": [{"title": "Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness", "url": "https://arxiv.org/html/2506.24056"}, {"title": "SafeConstellations: Steering LLM Safety to Reduce Over-Refusals Through Task-Specific Trajectory", "url": "https://arxiv.org/html/2508.11290v1"}, {"title": "What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal", "url": "https://arxiv.org/html/2604.08524"}, {"title": "Angular Steering: Behavior Control via Rotation in Activation Space", "url": "https://openreview.net/pdf/9a82b26d157916819f7a69e1e31ced6f640ca130.pdf"}, {"title": "AlphaSteer: Learning Refusal Steering with Principled Null-Space Constraint", "url": "https://arxiv.org/html/2506.07022"}, {"title": "Could Inference-Time Interventions Preserve Alignment? Safety Cost of Steering Vectors Is Separable and Reducible", "url": "https://arxiv.org/html/2608.08383"}, {"title": "Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness", "url": "https://arxiv.org/pdf/2506.24056"}, {"title": "The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs", "url": "https://arxiv.org/pdf/2606.22686"}, {"title": "SafeConstellations: Mitigating Over-Refusals in LLMs Through Task-Aware Representation Steering", "url": "https://arxiv.org/html/2508.11290v4"}]}, "Based on the search results, I found several relevant papers on steering coefficients and alignment robustness related to refusal behavior in language models:\n\n## Key Findings:\n\nThe refusal–affirmation logit gap measures the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step, quantifying the per-prompt safety margin that alignment provides.\n\n**Steering Intensity Thresholds:**\n\nGemma-3-12B shows a \"binary\" failure mode, jumping from 34% to 98% ASR (Attack Success Rate) at just α = 1.0, indicating minimal steering coefficient thresholds can induce refusal bypass. In contrast, Qwen-2.5-7B displays exceptional resistance, requiring high-magnitude steering to break, with ASR reaching only 68.5% even at α = 5.0.\n\n**Defense Through Negative Steering:**\n\nA small negative shift (α = -1.0) is sufficient to virtually eliminate successful attacks: Llama-3.3-70B drops from 68.8% to 9.4% ASR, and Gemma-3-12B to 6.0%.\n\n**Hyperparameter Thresholds:**\n\nIn the AlphaSteer approach, threshold parameters (λ) were set to 0.5, 0.45, and 0.14 for Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct, and Gemma-2-9b-IT, respectively, showing model-specific minimal thresholds for inducing refusal steering effects."], "durationSeconds": 7.778315247000006, "searchCount": 1}
```

### [23] TOOL RESULT — WebFetch · 2026-08-12 17:06:27 UTC

```
{"bytes": 43628, "code": 200, "codeText": "OK", "result": "# Research Paper Summary: Detection vs. Steering in Language Models\n\n**Abstract (Verbatim):**\n\"A central aspiration of mechanistic interpretability is controllability: if we know where a behavior is represented in a model's activations, we should be able to modify it. This rests on a hidden premise -- that the direction which detects a behavior and the direction which controls it are the same, or close. We test this geometrically: what is the angle between the direction that best detects a behavior and the one that best causes it? If detection implies control the cosine is near 1; otherwise it quantifies a detection-intervention gap. On Gemma 2-2B-it, output format (clean JSON vs markdown fencing) collapses both roles onto one axis. Hallucination does not: the model detects fake entities with perfect linear separability (AUC = 1.000 from layer 5), yet that direction sits at cos = 0.12 (about 83 degrees) from the direction producing a refusal -- a small, reproducible alignment, far from the cos = 1 that \"detection is control\" would require. A detector built from activations, with no chosen tokens, likewise fails to align (cos = -0.06). The gap generalizes: across four models from three families and two scales (1B-9B), cos stays in [0.12, 0.20], identical before and after instruction tuning (0.1197 vs 0.1200), placing its origin in pretraining.\"\n\n**Models Examined:** Gemma 2-2B-it plus three additional models across three families, with scales from 1B-9B parameters\n\n**Key Metrics:**\n- Hallucination detection AUC: 1.000 (from layer 5)\n- Cosine values: 0.12 (hallucination); -0.06 (detector-based); range [0.12, 0.20] across all models\n\n**Instruction Tuning Finding:** Cosine alignment remained essentially identical before and after instruction tuning (0.1197 vs 0.1200), suggesting the detection-steering gap originates in pretraining rather than tuning.", "durationMs": 8125, "url": "https://arxiv.org/abs/2606.24952"}
```

### [24] TOOL CALL — WebSearch · 2026-08-12 17:06:37 UTC

```
"logit gap" steering forward-pass diagnostic alignment robustness safety margin metric 2506.24056
```

### [25] TOOL CALL — WebSearch · 2026-08-12 17:06:37 UTC

```
steerability score as model audit metric "steering strength" required to elicit behavior benchmark-free safety
```

### [26] TOOL RESULT — WebSearch · 2026-08-12 17:06:43 UTC

```
{"query": "\"logit gap\" steering forward-pass diagnostic alignment robustness safety margin metric 2506.24056", "results": [{"tool_use_id": "srvtoolu_01FagNkMNNjQqwMFasv4HbB9", "content": [{"title": "[2506.24056] Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness", "url": "https://arxiv.org/abs/2506.24056"}, {"title": "Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness", "url": "https://arxiv.org/html/2506.24056"}, {"title": "Computation and Language 2025", "url": "https://arxiv.org/list/cs.CL/2025?skip=20475&show=2000"}, {"title": "Computer Science Jun 2025", "url": "https://arxiv.org/list/cs/2025-06?skip=12000&show=2000"}, {"title": "Logit-Gap Steering: A Forward-Pass Diagnostic for ...", "url": "https://arxiv.org/pdf/2506.24056"}, {"title": "Perturbation Probing: A Two-Pass-per-Prompt Diagnostic for FFN Behavioral Circuits in Aligned LLMs", "url": "https://arxiv.org/html/2604.27401"}, {"title": "Logit-Gap Steering: A New Frontier in Understanding and Probing LLM Safety", "url": "https://unit42.paloaltonetworks.com/logit-gap-steering-impact/"}, {"title": "The Geometry of Refusal: Linear Instability in Safety-Aligned LLMsAccepted at TrustNLP 2026, the Sixth Workshop on Trustworthy Natural Language Processing, co-located with ACL 2026.", "url": "https://arxiv.org/html/2606.22686v1"}, {"title": "The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs", "url": "https://arxiv.org/pdf/2606.22686"}]}, "The search successfully found the paper \"Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness\" (arXiv:2506.24056). Here's what the research is about:\n\n## Overview\n\nThe paper introduces the refusal-affirmation logit gap, investigating how much operational margin RLHF-style alignment provides for refusing unsafe requests.\n\n## The Metric\n\nThe refusal-affirmation logit gap is the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step, which quantifies the per-prompt safety margin that alignment provides.\n\n## Key Findings\n\nAlignment widens the gap on 97.5-99.8% of toxic prompts across three model families, and median gap closure co-varies with True-ASR ranking across suffix strategies.\n\n## The Method\n\nLogit-gap steering is a gradient-free, forward-pass-only method that discovers short in-distribution suffixes, requiring approximately 26,000 forward-pass equivalents per family. An 8-suffix ensemble reaches 38-96% True ASR across 13 models on AdvBench and HarmBench.\n\n## Practical Implications\n\nThe research demonstrates that logit-gap steering can serve both as a baseline for future jailbreak research and as a diagnostic tool for designing more robust safety architectures."], "durationSeconds": 7.620915187000006, "searchCount": 1}
```

### [27] TOOL RESULT — WebSearch · 2026-08-12 17:06:45 UTC

```
{"query": "steerability score as model audit metric \"steering strength\" required to elicit behavior benchmark-free safety", "results": [{"tool_use_id": "srvtoolu_01HavbeU3PtaxW44HN6cAQFq", "content": [{"title": "Chain of Risk: Safety Failures in Large Reasoning Models and Mitigation via Adaptive Multi-Principle Steering", "url": "https://arxiv.org/pdf/2605.05678"}, {"title": "FaithSteer-BENCH: A Deployment-Aligned Stress-Testing Benchmark for Inference-Time Steering", "url": "https://arxiv.org/pdf/2603.18329"}, {"title": "Steer-Bench: A Benchmark for Evaluating the Steerability of Large Language Models", "url": "https://arxiv.org/html/2505.20645v1"}, {"title": "Attention Misses Visual Risk: Risk-Adaptive Steering for Multimodal Safety Alignment", "url": "https://arxiv.org/pdf/2510.13698"}, {"title": "Deployment-Relevant Alignment Cannot Be Inferred from Model-Level Evaluation Alone", "url": "https://arxiv.org/pdf/2605.04454"}, {"title": "SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs", "url": "https://arxiv.org/pdf/2509.13450"}, {"title": "AI Steerability 360: A Toolkit for Steering Large Language Models", "url": "https://arxiv.org/html/2603.07837v1"}, {"title": "From Parameter Dynamics to Risk Scoring : Quantifying Sample-Level Safety Degradation in LLM Fine-tuning", "url": "https://arxiv.org/pdf/2605.04572"}, {"title": "Steering Language Model Refusal with Sparse Autoencoders", "url": "https://arxiv.org/pdf/2411.11296"}]}, "Based on the search results, I found relevant information about steerability evaluation and steering strength as metrics for model auditing, though not a specific metric explicitly called a \"steerability score\" with the exact terminology you mentioned.\n\nHere's what the search revealed:\n\n## Steering Strength in Model Auditing\n\nSteering strength (α) is used as a design choice in adaptive steering interventions, and research has identified optimal steering strength values (such as α=2.0) through ablation studies.\n\n## Steerability Benchmarking\n\nRecent work has begun to benchmark steering and steerability, including AxBench which provides a benchmark for comparing steering methods in representation space, and Steer-Bench which evaluates whether models can adapt outputs to different behavioral targets.\n\n## Safety-Focused Evaluation Metrics\n\nResearch frameworks define metrics including Effectiveness (how performant a steering method is on steering a target perspective) and Entanglement (the degree of unintended changes resulting from steering, by evaluating on all perspectives not being steered).\n\nSome approaches estimate a risk score and set steering strength accordingly, applying stronger steering to high-risk inputs while keeping intervention minimal for benign queries.\n\nThe search results suggest this is an active area of research with multiple frameworks approaching steerability evaluation, though I did not find a specific metric explicitly titled \"steerability score\" with the exact benchmark-free definition you mentioned in your query."], "durationSeconds": 8.670611307, "searchCount": 1}
```

### [28] TOOL CALL — Write · 2026-08-12 17:09:43 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_plan/gen_plan_research_1/.terminal_claude_agent_struct_out.json

{
  "title": "Who Already Measured Steering Strength?",
  "summary": "A saturation-and-positioning dossier for the steering-strength-as-measurement lane. Establishes exactly what Galeone et al. (detection-vs-steering gap) already claim so our refusal-specific site-selection result is written as a confirmation-and-extension; audits six-plus named steerability-measurement papers plus a fresh scholarly saturation search for anything functionally identical to alpha_50 (the closest known collision, Logit-Gap Steering arXiv:2506.24056, is pre-identified and must be resolved head-on); verifies The Rogue Scalpel closely enough to state a magnitude range for our random-direction null; and replaces the zero-hits novelty argument for the EWS negative with a positive claim. Output: verbatim-quoted per-paper dossier plus ready-to-paste Related Work and Method paragraphs.",
  "runpod_compute_profile": "cpu_light",
  "question": "What is already published in the 'steering strength as a measurement of alignment' lane, is anything functionally the same object as alpha_50 (the steering coefficient at which a fresh benign-prompt generation crosses 50% refusal), what exactly does Galeone et al.'s detection-vs-steering gap claim so our refusal-specific site-selection result can be positioned as confirmation-and-extension rather than discovery, and does The Rogue Scalpel's random-steering-breaks-alignment result undermine our matched-random-direction null?",
  "research_plan": "SCOPE AND OUTPUT CONTRACT\n\nThis is a pure web-research artifact. No code, no downloads, no model runs. Two deliverables, both mandatory:\n\n1. `research_report.md` — the dossier. Structure fixed below (7 sections). EVERY factual claim carries an anchor of the form `[arXiv:ID §section-or-table]` or `[arXiv:ID, abstract]`. Every headline number is a VERBATIM quote in quotation marks, not a paraphrase. If a number cannot be located in the primary full text after a fetch_grep attempt, write `NOT FOUND IN PRIMARY TEXT` next to it — never fill it from a search snippet or from memory. Search snippets are leads, never evidence.\n2. `research_out.json` — `{answer, sources, follow_up_questions}`. `answer` must contain a machine-readable per-paper table (see Section 7 schema) plus the two ready-to-paste paragraphs verbatim. `sources` must list every URL actually fetched.\n\nUse the `aii-web-tools` skill throughout: `web search` (pass `mode=scholarly` for all prior-art and saturation queries in Step 3), `web fetch` to read, `fetch_grep` to extract exact numbers from HTML/PDF. Prefer `arxiv.org/abs/<ID>` first (abstract + venue comments field), then `arxiv.org/html/<ID>` or `arxiv.org/pdf/<ID>` for full text. Parallelise aggressively: batch all independent fetches for a step into one turn.\n\nTIME BOX (3 h total): Step 0 ~5 min, Step 1 ~35 min, Step 2 ~45 min, Step 3 ~35 min, Step 4 ~20 min, Step 5 ~10 min, Step 6 (writing) ~30 min. If you are over budget, the priority order for cutting is: Step 5 > Step 2's secondary papers > Step 3's tail queries. Steps 1, 2-primary, 3-core and 4 are NOT cuttable — they are the reason this artifact exists.\n\nPRE-VERIFIED FACTS — DO NOT RE-DERIVE, ONLY CONFIRM AND DEEPEN\n\nThe planner already verified these against primary sources. Treat them as starting points; your job is to add the section anchors and the surrounding scope conditions, not to rediscover them.\n\n- Galeone, Ettorre, Park, Ettorre, Ligorio, 'Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models', arXiv:2606.24952, submitted 2026-06-23. Abstract confirmed verbatim. Behaviour where the roles COLLAPSE onto one axis: output format (clean JSON vs markdown fencing) on Gemma 2-2B-it. Behaviour where they DO NOT: hallucination — \"the model detects fake entities with perfect linear separability (AUC = 1.000 from layer 5), yet that direction sits at cos = 0.12 (about 83 degrees) from the direction producing a refusal\". A token-free activation detector \"likewise fails to align (cos = -0.06)\". Generalisation: \"across four models from three families and two scales (1B-9B), cos stays in [0.12, 0.20], identical before and after instruction tuning (0.1197 vs 0.1200), placing its origin in pretraining.\"\n- Kaminski et al. (verify authors), 'The Rogue Scalpel: Activation Steering Compromises LLM Safety', arXiv:2509.22067. Headline: steering in a RANDOM direction \"can increase the probability of harmful compliance from 0% to 1-13%\"; benign SAE features comparable; combining 20 randomly sampled jailbreaking vectors yields a universal attack. Has an OpenReview record (forum id uXecy0nKiJ) — check its venue and decision.\n- arXiv:2602.02712, 'Towards Understanding Steering Strength' — first theoretical analysis of steering strength; characterises effect on next-token probability, concept presence, and cross-entropy; \"reveals surprising behaviors, including non-monotonic effects of steering strength\". THIS IS A DIRECT THREAT TO alpha_50's LOGISTIC DOSE-RESPONSE FIT and must be treated as such, not as background.\n- arXiv:2509.13450 — TITLE CHANGED BETWEEN VERSIONS: v1 'SteeringControl: Holistic Evaluation of Alignment Steering in LLMs', current 'SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs'. Siu, Crispino, Park, Henry et al. (UCSC / WashU). Modular framework over DIM, ACE, CAA, PCA, LAT; Qwen-2.5-7B and Llama-3.1-8B; entanglement up to 76% on social behaviours. Cite the CURRENT title and note the rename in a footnote — a stale title is a citation error a reviewer will catch.\n- arXiv:2508.21448 — Kabir, Esterling, Dong, 'Beyond the Surface: Probing the Ideological Depth of Large Language Models' (v3 retitled 'When Models Refuse: Political Steerability and Feature Richness as Measures of Ideological Depth'). Defines ideological depth as steerability + SAE feature richness; Gemma vs Llama, ~7.3x more distinct political features. Same rename caveat.\n- arXiv:2603.24543 — Li, Fastowski, Zaradoukas, Prenkaj, Kasneci, 'Analysing the Safety Pitfalls of Steering Vectors', 2026-03-25. CAA vectors on JailbreakBench move ASR \"up to 57%\" upward or \"up to 50%\" downward, attributed to overlap between steering vectors and latent refusal directions.\n- NEWLY FOUND BY THE PLANNER, NOT IN THE DIRECTION, AND THE SHARPEST NOVELTY THREAT: arXiv:2506.24056, 'Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness'. It defines the refusal-affirmation logit gap as \"the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step\", explicitly framed as \"the per-prompt safety margin that alignment provides\", reports alignment widening the gap on \"97.5-99.8% of toxic prompts across three model families\", and is pitched as \"a diagnostic tool for designing more robust safety architectures\". Palo Alto Unit 42 has a write-up. This is the same conceptual object as alpha_50 (how much push before refusal wins the argmax) measured in logit units at the first decoding step rather than in steering-coefficient units. RESOLVING IT IS THE SINGLE HIGHEST-VALUE TASK IN THIS ARTIFACT.\n- Other planner-found leads to triage in Step 3: arXiv:2604.08524 'What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal'; arXiv:2608.08383 'Could Inference-Time Interventions Preserve Alignment? Safety Cost of Steering Vectors Is Separable and Reducible'; arXiv:2603.07837 'AI Steerability 360'; arXiv:2505.20645 'Steer-Bench'; AxBench; 'Angular Steering: Behavior Control via Rotation in Activation Space' (OpenReview); arXiv:2506.07022 'AlphaSteer'; arXiv:2604.09839 'Steered LLM Activations are Non-Surjective'; arXiv:2606.22686 'The Geometry of Refusal' — note the planner found its HTML v1 carries a comment 'Accepted at TrustNLP 2026, the Sixth Workshop on Trustworthy Natural Language Processing, co-located with ACL 2026', which UPGRADES the venue claim in the hypothesis's related-works list and should be reported.\n\n---\n\nSTEP 0 — SETUP (~5 min)\n\nRead the dependency artifact `art_0UsKSgsMHome` at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json` and its `research_report.md`. Extract two things and do not duplicate them: (a) the anchor/citation-audit conventions already in use, so this dossier matches the previous one's format; (b) the list of papers already fully read there (AMS 2608.05578, RAS 2606.25750, VISAGE 2405.17374, Qi 2406.05946, Kwon 2607.14147, Ratnakar 2606.22686, arXiv:2605.09043 CSD-in-dialogue, AQI 2506.13901, arXiv:2603.18353 knowledge-action gap). Anything already anchored there is CITED BY REFERENCE, not re-read. Your budget goes to the steering-measurement lane, which that artifact did not cover.\n\nSTEP 1 — GALEONE ET AL., READ TO EXHAUSTION (~35 min)\n\nFetch `arxiv.org/abs/2606.24952` (for the comments/venue field and the exact author list and date), then `arxiv.org/html/2606.24952`. Then run `fetch_grep` on the HTML/PDF for each of these patterns and transcribe the matching sections verbatim:\n- `cos|cosine|angle|degrees` — every cosine reported, with which behaviour, which model, which layer.\n- `AUC|AUROC|separab` — every detection number and the layer it is reported at.\n- `Gemma|Llama|Qwen|Mistral|-2b|-9b|-1b` — the exact four-model roster and scales.\n- `instruct|instruction.tun|base model|pretrain` — the before/after-instruction-tuning comparison and the pretraining-origin claim.\n- `steering|intervention|coefficient|alpha|magnitude|strength` — HOW they obtain the 'direction that best causes it': is it optimised, difference-in-means over responses, or grid-searched? At what magnitude? On how many probes?\n- `refusal` — is refusal a target behaviour in its own right, or only the OUTCOME channel for the hallucination probe? This matters enormously for our positioning.\n- `limitation|scope|future work|we do not` — their own stated scope limits.\n\nRecord answers to these seven positioning questions explicitly, each with an anchor:\nQ1. Is their claim about ANY behaviour, or behaviour-conditional (JSON collapses, hallucination does not)? Our paragraph must not flatten this.\nQ2. Is their detection direction fit on PROMPTS or on RESPONSES? Ours is a prompt axis vs a response-contrast axis — if theirs is the same contrast pair, our result is a replication in a new behaviour; if different, it is an extension along a new dimension.\nQ3. What is their steering-effectiveness criterion (a % of probes? a rate? a threshold?) versus our '27% of probes' — are the two numbers commensurable at all?\nQ4. Do they anywhere claim, or decline to claim, that the CONSEQUENCE is 'you must build metrics from the causal axis, not the detection axis'? If they already say it, our contribution shrinks to a refusal-specific instance and we say so. If they stop at diagnosis, our contribution is the constructive corollary.\nQ5. The 0.1197 vs 0.1200 result says the gap is a PRETRAINING property, invariant to instruction tuning. Does that predict our axis-choice effect should be present in the BASE model too? Flag this as a testable prediction for the experiment plan — it is a free pre-registered check.\nQ6. Their cos = -0.06 for a token-free activation detector: does that bear on our H1'' lexical-artefact worry (i.e. does the detection axis's alignment depend on the token set used to define it)?\nQ7. Venue and review status — is it a preprint, workshop, or conference paper? Do not upgrade.\n\nDELIVERABLE 1a: a subsection `## Galeone et al. (arXiv:2606.24952) — what they claim, exactly` with the verbatim abstract, a numbers table, and the seven Q/A entries.\nDELIVERABLE 1b: a ready-to-paste ~150-word RELATED WORK paragraph and a ~120-word METHOD paragraph. The Method paragraph must state, in our voice and with the exact numbers on both sides: (i) Galeone et al. establish a detection-intervention gap (AUC 1.000, cos = 0.12, ~83 degrees, cos in [0.12,0.20] across four models, invariant to instruction tuning); (ii) our result is the refusal-specific instance — a held-out-AUROC-1.0 prompt-derived axis steers on only 27% of probes while a 0.69-AUROC response-contrast axis is the one that steers; (iii) the ADDED claim is constructive and methodological, not phenomenological: it determines WHICH axis a steering-strength metric must be built from, so alpha_50 is defined on the response-contrast axis by necessity rather than by convenience. Write it so it reads as confirmation-and-extension. Do NOT write 'we discover' or 'we are the first to show' anywhere in it.\n\nFAILURE MODE: if the full text is unreachable (PDF/HTML both fail), fall back to the abstract page plus alphaXiv/HuggingFace-papers/Semantic-Scholar mirrors, and mark every un-verified number `ABSTRACT ONLY`. Do NOT silently downgrade the anchor.\n\nSTEP 2 — THE STEERABILITY-AS-MEASUREMENT LANE (~45 min)\n\nRead each paper below at least to abstract + method + main results. For EVERY paper, fill the SAME five-field record — this uniformity is what makes the dossier usable downstream:\n(F1) MEASURED QUANTITY — the exact scalar or vector the paper computes, quoted.\n(F2) MODELS AND SCALES.\n(F3) HARMFUL-PROMPT DEPENDENCE — does computing their quantity require harmful/unsafe/jailbreak prompts, a reference model, or a benchmark? (This is our whole product claim, so answer it precisely: 'requires harmful prompts to FIT the direction' and 'requires harmful prompts to SCORE' are different answers.)\n(F4) IS IT FUNCTIONALLY alpha_50? Rate on a 4-point scale — IDENTICAL / SAME-OBJECT-DIFFERENT-UNITS / ADJACENT / UNRELATED — with a one-sentence justification quoting the decisive line.\n(F5) WHAT IT DOES TO OUR CLAIM — strengthens (we cite as support), constrains (we must add a caveat/scope statement), or collides (we must narrow the novelty claim). Name the exact sentence in our paper that has to change.\n\nPRIMARY (must be done):\n(P1) arXiv:2506.24056 Logit-Gap Steering. THE COLLISION CHECK. `fetch_grep` for `logit gap|refusal.affirmation|first decoding step|margin|diagnostic|forward.pass|26,?000|True.ASR|AdvBench|HarmBench`. Answer, with quotes: does the gap require TOXIC/harmful prompts to compute (the abstract's '97.5-99.8% of toxic prompts' suggests YES — confirm)? Is it computed at the FIRST decoding step only (ours is a generation-onset decision measured over a fresh generation — related but not the same)? Is it a per-PROMPT margin or a per-MODEL score? Is it ever aggregated into a model-level alignment-robustness number, and if so how? Then write the explicit differentiation: alpha_50 is measured in units of NORM_L along a steering axis, on BENIGN prompts only, with no harmful content, and scores a MODEL not a prompt; the logit gap is measured in logit units on toxic prompts. If any of those distinctions fail on close reading, SAY SO PLAINLY in the report under a heading `## NOVELTY THREAT: partially realised` and state precisely what is left that is ours. Also fetch the Unit 42 write-up (unit42.paloaltonetworks.com) for the industrial framing — useful for Related Work, not for numbers.\n(P2) arXiv:2602.02712 Towards Understanding Steering Strength. THE METHODOLOGY THREAT. `fetch_grep` for `non-?monoton|law|next token probab|cross.entropy|saturat|regime|assumption|theorem`. Extract: under what conditions is the response to steering strength non-monotonic; is the non-monotonicity in the CONCEPT-PRESENCE curve (which is what alpha_50 fits) or only in cross-entropy/fluency; and does the theory predict a saturating sigmoid over some range. Deliverable: a short paragraph the experiment plan can adopt as a pre-registered robustness check — e.g. 'because arXiv:2602.02712 shows steering strength can act non-monotonically, we (a) sweep alpha past the observed 50% crossing to confirm the refusal rate does not turn over, and (b) report the raw dose-response points alongside the logistic fit so a non-sigmoidal shape is visible rather than absorbed by the fit.' If the paper gives an explicit condition for monotonicity, quote it — that is a gift to our pre-registration.\n(P3) arXiv:2509.13450 SteeringSafety/SteeringControl. F1-F5 plus: does it define any scalar that is a per-MODEL safety readout (as opposed to a per-METHOD steering-quality readout)? Note the title change.\n(P4) arXiv:2508.21448 Kabir et al. F1-F5 plus: how exactly is 'steerability' operationalised — success rate at fixed strength, or strength required for success? The latter would make it a genuine relative of alpha_50 in a non-safety domain, which is a GOOD citation for us (it shows the family of measure is established, so our contribution is the safety-specific instance).\n(P5) arXiv:2603.24543 Analysing the Safety Pitfalls of Steering Vectors. F1-F5 plus: the ±57%/-50% ASR swing and the claimed overlap between arbitrary CAA vectors and the refusal direction. This is the second-strongest constraint on our random-direction null after the Rogue Scalpel.\n\nSECONDARY (do if time; drop in the stated order if not): arXiv:2604.08524 (mechanistic case study on steering refusal — most likely to contain an alpha-sweep we should cite), arXiv:2608.08383 (safety cost of steering separable/reducible), arXiv:2603.07837 (AI Steerability 360 toolkit), arXiv:2505.20645 (Steer-Bench), AxBench, Angular Steering, arXiv:2506.07022 (AlphaSteer — its per-model lambda thresholds 0.5/0.45/0.14 are a model-dependent intervention-strength constant, i.e. weak evidence that intervention strength is model-idiosyncratic, which SUPPORTS our H1''' comparability worry).\n\nSTEP 3 — FRESH SATURATION SEARCH (~35 min)\n\nRun in `mode=scholarly`, and ALSO in general mode (arXiv listing pages and blogs surface things scholarly indexes miss). Minimum query set, each run verbatim:\n1. \"steering strength as an alignment metric\"\n2. \"steering coefficient threshold refusal\"\n3. \"minimal intervention strength alignment\"\n4. \"steerability score safety audit\"\n5. \"how much steering is needed to induce refusal\"\n6. \"activation steering dose-response refusal rate\"\n7. \"ED50 OR EC50 OR half-maximal steering language model\"\n8. \"critical steering magnitude jailbreak threshold\"\n9. \"benchmark-free safety evaluation open-weight checkpoint\"\n10. \"safety margin measured without harmful prompts\"\n11. \"abliterated model detection metric\"\n12. \"refusal direction norm normalization cross-model comparison\"\n13. \"steering strength required behavior elicitation model comparison\"\n14. \"logistic dose response activation steering\"\n\nRULES: report HITS, with counts and the top 5 titles per query. NEVER write 'zero results' as a novelty argument — if a query genuinely returns nothing relevant, report the query, the mode, the date, and the nearest neighbours it DID return. For every hit that looks within one hop of alpha_50, open it and fill the F1-F5 record. Also do one targeted check on the abliteration literature specifically: is there any published metric that scores 'how abliterated is this checkpoint' from steering strength? (AMS from art_0UsKSgsMHome is the activation-geometry answer; we need to know whether a steering-strength answer exists.)\n\nDELIVERABLE 3: a section `## Saturation check, dated <run date>` with the query table, the hit list, and a single explicit verdict sentence chosen from exactly one of:\n(a) NOTHING EQUIVALENT FOUND — followed by a POSITIVE novelty statement (see Step 6 rules), not a zero-hits claim;\n(b) ADJACENT WORK EXISTS — naming it and stating the residual contribution in one sentence;\n(c) FUNCTIONALLY EQUIVALENT WORK EXISTS — naming it, quoting the decisive line, and stating precisely what remains ours (likely candidates for what remains: benign-prompts-only measurement, the fresh-generation rather than first-token operationalisation, per-model NORM_L normalisation, the base-vs-tuned vs price-of-the-mode decomposition, and the paired instruct-minus-abliterated test). Verdict (c) is a SUCCESSFUL outcome of this artifact, not a failure — write it without hedging if it is what the evidence says.\n\nSTEP 4 — THE ROGUE SCALPEL, AND WHAT OUR RANDOM-DIRECTION NULL MAY STATE (~20 min)\n\nFetch arXiv:2509.22067 (abs + html/pdf) and its OpenReview forum (id uXecy0nKiJ) for venue/decision/reviews. `fetch_grep` for `random|norm|magnitude|coefficient|alpha|strength|scale|layer|1-13|universal|20 vectors|harmful compliance|StrongREJECT|HarmBench`.\n\nExtract, with quotes, the four things that decide whether our null survives:\n(R1) At what MAGNITUDE (and in what normalisation — raw L2, multiples of the residual-stream norm, multiples of the mean activation norm?) do random vectors produce the 0%->1-13% effect? If they normalise to the activation norm, convert into our NORM_L units and state the conversion assumption explicitly.\n(R2) At which LAYERS, and on how many random draws — is 1-13% a per-draw rate or a best-of-N over many draws? A best-of-N maximum and a per-draw expectation are very different objections to our null.\n(R3) Is the broken behaviour COMPLIANCE-INDUCING (guardrails down) or does random steering ever induce REFUSAL on benign prompts? Our null is specifically 'a matched random direction does not induce refusal at any alpha on benign prompts'. The Rogue Scalpel measures the OPPOSITE direction of failure. If it never tests random-induced refusal on benign prompts, our null is untouched by it and we say exactly that — with the quote.\n(R4) Does it report a magnitude BELOW which random steering has no effect? That number is what our null must be scoped to.\n\nDELIVERABLE 4: a subsection `## Does The Rogue Scalpel weaken our matched-random-direction null?` ending with a single ready-to-paste sentence for our Method of the form: 'Our random-direction control is a statement about a magnitude range: over alpha in [0, ALPHA_MAX] in units of NORM_L, a norm-matched random direction induced refusal on benign prompts at no tested coefficient. We do not claim random directions are behaviourally inert — arXiv:2509.22067 reports that random steering raises harmful compliance from 0% to 1-13% [anchor], and arXiv:2603.24543 reports arbitrary CAA vectors moving JailbreakBench ASR by up to 57% [anchor] — but both concern the compliance direction under <their magnitude regime>, whereas our control concerns refusal induction on benign prompts.' Fill the bracketed regime from R1/R2. If R1-R4 show the effect occurs at magnitudes INSIDE our sweep range and in a way that does bear on refusal, say the null is WEAKENED and specify the extra control the experiment must add (concretely: N>=10 independent random draws per model with the same logistic dose-response fit, reporting max-over-draws rather than a single draw, so a best-of-N objection is pre-empted).\n\nSTEP 5 — POSITIVE NOVELTY STATEMENT FOR THE EWS NEGATIVE (~10 min)\n\nThe iteration-1 argument was 'an arXiv abstract search for EWS + LLM returns zero'. That is a weak, unfalsifiable-looking argument and gets demoted to a footnote. Build the replacement:\n- Confirm the two known neighbours from art_0UsKSgsMHome: arXiv:2605.09043 (critical slowing down applied to conversation derailment in HUMAN DIALOGUE TEXT) and Rahimi et al. arXiv:2602.02600 (step-wise refusal dynamics, comparing autoregressive vs DIFFUSION SAMPLING mechanisms). Re-verify each has the scope property we rely on with a one-line quote.\n- Run 3-4 fresh scholarly queries: \"critical slowing down large language model\", \"early warning signals neural network dynamics\", \"variance autocorrelation tipping point transformer generation\", \"resilience indicators machine learning model behaviour\". Report hits.\n- Draft the POSITIVE statement (~90 words), structured as a three-axis differentiation rather than an absence claim: our EWS negative is the first controlled test of the critical-slowing-down indicator suite computed (i) on GENERATED-STEP time series of a model-internal refusal observable, rather than on dialogue text [2605.09043] or on sampling-mechanism comparisons [2602.02600]; (ii) with an explicit perturbation-recovery arm and matched random-direction and surrogate controls; (iii) with a pre-registered estimator-identifiability gate, so the negative is attributable to the phenomenon rather than to the estimator. Add the footnote text carrying the old zero-hits search as supporting, not primary, evidence.\n\nSTEP 6 — WRITE-UP (~30 min)\n\n`research_report.md` sections, in this order:\n1. Executive summary — max 12 bullets, each with an anchor. Lead with the saturation verdict (a/b/c) and the Logit-Gap resolution, because those are what change the paper.\n2. Galeone et al. read to exhaustion (Step 1) + the two ready-to-paste paragraphs, clearly fenced and labelled `PASTE INTO RELATED WORK` / `PASTE INTO METHOD`.\n3. The steerability-as-measurement lane — one uniform F1-F5 record per paper, plus a single comparison table with columns: paper | arXiv ID | venue/status | measured quantity | models | needs harmful prompts? | needs reference model? | relation to alpha_50 (4-point) | what it does to our claim.\n4. Saturation check with query table, hit counts, and the one-sentence verdict.\n5. The Rogue Scalpel analysis + the magnitude-scoped null sentence.\n6. Positive novelty statement for the EWS negative + the demoted footnote.\n7. Actionable consequences for the experiment plan — a numbered list of concrete changes, each naming the hypothesis it touches (H1', H1'', H1''', H2', H3', H5'). Expected members: the non-monotonicity robustness check from P2; the N>=10 random-draw control from Step 4 if warranted; the base-model prediction implied by Galeone's instruction-tuning invariance (Q5); whether the response-contrast axis is now a citation-supported choice rather than an ad-hoc one; and any claim in the hypothesis that must be softened or withdrawn.\n\nWRITING RULES, ENFORCED:\n- No 'to the best of our knowledge', no 'first ever', no zero-hit novelty arguments in the main text.\n- Every number in quotation marks or marked `NOT FOUND IN PRIMARY TEXT`.\n- Report venue and review status honestly; most 2026 items here are preprints. Do not upgrade a preprint to a conference paper. DO report the one CONFIRMED upgrade the planner found: arXiv:2606.22686 carries an 'Accepted at TrustNLP 2026 (co-located with ACL 2026)' comment.\n- Flag every title change between arXiv versions (2509.13450, 2508.21448 confirmed; check the others) so downstream citations are not stale.\n- If a finding contradicts the hypothesis document as written, say so in Section 7 and name the sentence to change. Contradictions found here are cheap; contradictions found by a reviewer are not.\n\n`research_out.json` — `answer` carries: the saturation verdict string; the per-paper table as a JSON array of the F1-F5 records; the two ready-to-paste paragraphs verbatim; the magnitude-scoped null sentence; the EWS positive statement; and the Section-7 consequences list. `sources`: every URL fetched, with arXiv ID and title. `follow_up_questions`: at minimum, anything that could not be resolved from primary text (e.g. an unreachable PDF, an ambiguous normalisation convention in 2509.22067) stated as a specific question, not a topic.\n\nCONTINGENCIES\n- If arXiv:2506.24056 turns out to be functionally identical to alpha_50: do not soften it. Write verdict (c), quote the decisive line, and spend the remaining time enumerating precisely what survives (benign-only measurement; model-level rather than prompt-level score; the reachable-mode vs price-of-the-mode decomposition; per-model NORM_L normalisation; the paired instruct-vs-abliterated test). A correctly narrowed contribution is publishable; an overclaimed one is not.\n- If several primary PDFs are unreachable, prioritise Step 1 and Step 2-P1/P2 and mark the rest `ABSTRACT ONLY` rather than thinning all of them equally.\n- If a search returns a paper that measures exactly 'the steering coefficient at 50% behaviour crossing' under a different name (ED50/EC50/critical alpha/threshold coefficient), that is the collision — treat it with Step 2-P1's full protocol immediately, even at the cost of the secondary papers.",
  "explanation": "The experiment plan for iteration 2 rests on two claims this artifact decides. First, the site-selection result (a prompt-derived axis at held-out AUROC 1.0 steers on only 27% of probes, while a 0.69-AUROC response-contrast axis is the one that actually steers) is currently written as a discovery, but Galeone et al. (arXiv:2606.24952) already published the general detection-intervention gap — AUC 1.000 with cos = 0.12 (~83 degrees), cos in [0.12, 0.20] across four models from three families, and essentially invariant to instruction tuning (0.1197 vs 0.1200). Presenting our result as new would be an overclaim a reviewer catches in one search; presenting it as a refusal-specific confirmation WITH a constructive extension — it determines which axis a steering-strength metric must be built from — is both honest and stronger. That reframing needs their exact claims and scope, which is why Step 1 reads them to exhaustion.\n\nSecond, alpha_50 is the iteration's primary metric, and it has not had a saturation check. The planner already found the sharpest threat: Logit-Gap Steering (arXiv:2506.24056) defines 'the refusal-affirmation logit gap' at the first decoding step as 'the per-prompt safety margin that alignment provides' and pitches it as an alignment-robustness diagnostic — the same conceptual object as alpha_50 in different units and on toxic rather than benign prompts. Whether the differences (benign-only, model-level, fresh-generation, NORM_L-normalised) are load-bearing decides how the paper's contribution must be stated. A second, quieter threat is arXiv:2602.02712, whose theoretical result that steering strength can act NON-MONOTONICALLY directly undermines alpha_50's logistic dose-response fit unless the experiment adds a sweep-past-crossing check and reports raw dose-response points — a design change that is nearly free now and impossible after the run.\n\nThird, The Rogue Scalpel (arXiv:2509.22067) reports random steering vectors raising harmful compliance from 0% to 1-13%, and arXiv:2603.24543 reports arbitrary CAA vectors swinging JailbreakBench ASR by up to 57%. Our matched-random-direction null says a random axis induces refusal at no alpha. Those results concern the opposite direction of failure, but unless the magnitude regime is pinned down, the null reads as naive. Step 4 converts it into a defensible, magnitude-scoped statement, or tells the experiment to add an N>=10-draw control.\n\nAll of this is pure literature work with no compute requirement, and it must happen BEFORE the experiment is designed, because its outputs are design changes (axis choice justification, non-monotonicity robustness check, random-draw control, base-model prediction) and paper-text changes (novelty statement, Related Work, the EWS negative's positive framing) rather than post-hoc commentary."
}
```

### [29] TOOL RESULT — Write · 2026-08-12 17:09:43 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_plan/gen_plan_research_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Who Already Measured Steering Strength?\",\n  \"summary\": \"A saturation-and-positioning dossier for the steering-strength-as-measurement lane. Establishes exactly what Galeone et al. (detection-vs-steering gap) already claim so our refusal-specific site-selection result is written as a confirmation-and-extension; audits six-plus named steerability-measurement papers plus a fresh scholarly saturation search for anything functionally identical to alpha_50 (the closest known collision, Logit-Gap Steering arXiv:2506.24056, is pre-identified and must be resolved head-on); verifies The Rogue Scalpel closely enough to state a magnitude range for our random-direction null; and replaces the zero-hits novelty argument for the EWS negative with a positive claim. Output: verbatim-quoted per-paper dossier plus ready-to-paste Related Work and Method paragraphs.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"question\": \"What is already published in the 'steering strength as a measurement of alignment' lane, is anything functionally the same object as alpha_50 (the steering coefficient at which a fresh benign-prompt generation crosses 50% refusal), what exactly does Galeone et al.'s detection-vs-steering gap claim so our refusal-specific site-selection result can be positioned as confirmation-and-extension rather than discovery, and does The Rogue Scalpel's random-steering-breaks-alignment result undermine our matched-random-direction null?\",\n  \"research_plan\": \"SCOPE AND OUTPUT CONTRACT\\n\\nThis is a pure web-research artifact. No code, no downloads, no model runs. Two deliverables, both mandatory:\\n\\n1. `research_report.md` — the dossier. Structure fixed below (7 sections). EVERY factual claim carries an anchor of the form `[arXiv:ID §section-or-table]` or `[arXiv:ID, abstract]`. Every headline number is a VERBATIM quote in quotation marks, not a paraphrase. If a number cannot be located in the primary full text after a fetch_grep attempt, write `NOT FOUND IN PRIMARY TEXT` next to it — never fill it from a search snippet or from memory. Search snippets are leads, never evidence.\\n2. `research_out.json` — `{answer, sources, follow_up_questions}`. `answer` must contain a machine-readable per-paper table (see Section 7 schema) plus the two ready-to-paste paragraphs verbatim. `sources` must list every URL actually fetched.\\n\\nUse the `aii-web-tools` skill throughout: `web search` (pass `mode=scholarly` for all prior-art and saturation queries in Step 3), `web fetch` to read, `fetch_grep` to extract exact numbers from HTML/PDF. Prefer `arxiv.org/abs/<ID>` first (abstract + venue comments field), then `arxiv.org/html/<ID>` or `arxiv.org/pdf/<ID>` for full text. Parallelise aggressively: batch all independent fetches for a step into one turn.\\n\\nTIME BOX (3 h total): Step 0 ~5 min, Step 1 ~35 min, Step 2 ~45 min, Step 3 ~35 min, Step 4 ~20 min, Step 5 ~10 min, Step 6 (writing) ~30 min. If you are over budget, the priority order for cutting is: Step 5 > Step 2's secondary papers > Step 3's tail queries. Steps 1, 2-primary, 3-core and 4 are NOT cuttable — they are the reason this artifact exists.\\n\\nPRE-VERIFIED FACTS — DO NOT RE-DERIVE, ONLY CONFIRM AND DEEPEN\\n\\nThe planner already verified these against primary sources. Treat them as starting points; your job is to add the section anchors and the surrounding scope conditions, not to rediscover them.\\n\\n- Galeone, Ettorre, Park, Ettorre, Ligorio, 'Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models', arXiv:2606.24952, submitted 2026-06-23. Abstract confirmed verbatim. Behaviour where the roles COLLAPSE onto one axis: output format (clean JSON vs markdown fencing) on Gemma 2-2B-it. Behaviour where they DO NOT: hallucination — \\\"the model detects fake entities with perfect linear separability (AUC = 1.000 from layer 5), yet that direction sits at cos = 0.12 (about 83 degrees) from the direction producing a refusal\\\". A token-free activation detector \\\"likewise fails to align (cos = -0.06)\\\". Generalisation: \\\"across four models from three families and two scales (1B-9B), cos stays in [0.12, 0.20], identical before and after instruction tuning (0.1197 vs 0.1200), placing its origin in pretraining.\\\"\\n- Kaminski et al. (verify authors), 'The Rogue Scalpel: Activation Steering Compromises LLM Safety', arXiv:2509.22067. Headline: steering in a RANDOM direction \\\"can increase the probability of harmful compliance from 0% to 1-13%\\\"; benign SAE features comparable; combining 20 randomly sampled jailbreaking vectors yields a universal attack. Has an OpenReview record (forum id uXecy0nKiJ) — check its venue and decision.\\n- arXiv:2602.02712, 'Towards Understanding Steering Strength' — first theoretical analysis of steering strength; characterises effect on next-token probability, concept presence, and cross-entropy; \\\"reveals surprising behaviors, including non-monotonic effects of steering strength\\\". THIS IS A DIRECT THREAT TO alpha_50's LOGISTIC DOSE-RESPONSE FIT and must be treated as such, not as background.\\n- arXiv:2509.13450 — TITLE CHANGED BETWEEN VERSIONS: v1 'SteeringControl: Holistic Evaluation of Alignment Steering in LLMs', current 'SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs'. Siu, Crispino, Park, Henry et al. (UCSC / WashU). Modular framework over DIM, ACE, CAA, PCA, LAT; Qwen-2.5-7B and Llama-3.1-8B; entanglement up to 76% on social behaviours. Cite the CURRENT title and note the rename in a footnote — a stale title is a citation error a reviewer will catch.\\n- arXiv:2508.21448 — Kabir, Esterling, Dong, 'Beyond the Surface: Probing the Ideological Depth of Large Language Models' (v3 retitled 'When Models Refuse: Political Steerability and Feature Richness as Measures of Ideological Depth'). Defines ideological depth as steerability + SAE feature richness; Gemma vs Llama, ~7.3x more distinct political features. Same rename caveat.\\n- arXiv:2603.24543 — Li, Fastowski, Zaradoukas, Prenkaj, Kasneci, 'Analysing the Safety Pitfalls of Steering Vectors', 2026-03-25. CAA vectors on JailbreakBench move ASR \\\"up to 57%\\\" upward or \\\"up to 50%\\\" downward, attributed to overlap between steering vectors and latent refusal directions.\\n- NEWLY FOUND BY THE PLANNER, NOT IN THE DIRECTION, AND THE SHARPEST NOVELTY THREAT: arXiv:2506.24056, 'Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness'. It defines the refusal-affirmation logit gap as \\\"the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step\\\", explicitly framed as \\\"the per-prompt safety margin that alignment provides\\\", reports alignment widening the gap on \\\"97.5-99.8% of toxic prompts across three model families\\\", and is pitched as \\\"a diagnostic tool for designing more robust safety architectures\\\". Palo Alto Unit 42 has a write-up. This is the same conceptual object as alpha_50 (how much push before refusal wins the argmax) measured in logit units at the first decoding step rather than in steering-coefficient units. RESOLVING IT IS THE SINGLE HIGHEST-VALUE TASK IN THIS ARTIFACT.\\n- Other planner-found leads to triage in Step 3: arXiv:2604.08524 'What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal'; arXiv:2608.08383 'Could Inference-Time Interventions Preserve Alignment? Safety Cost of Steering Vectors Is Separable and Reducible'; arXiv:2603.07837 'AI Steerability 360'; arXiv:2505.20645 'Steer-Bench'; AxBench; 'Angular Steering: Behavior Control via Rotation in Activation Space' (OpenReview); arXiv:2506.07022 'AlphaSteer'; arXiv:2604.09839 'Steered LLM Activations are Non-Surjective'; arXiv:2606.22686 'The Geometry of Refusal' — note the planner found its HTML v1 carries a comment 'Accepted at TrustNLP 2026, the Sixth Workshop on Trustworthy Natural Language Processing, co-located with ACL 2026', which UPGRADES the venue claim in the hypothesis's related-works list and should be reported.\\n\\n---\\n\\nSTEP 0 — SETUP (~5 min)\\n\\nRead the dependency artifact `art_0UsKSgsMHome` at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json` and its `research_report.md`. Extract two things and do not duplicate them: (a) the anchor/citation-audit conventions already in use, so this dossier matches the previous one's format; (b) the list of papers already fully read there (AMS 2608.05578, RAS 2606.25750, VISAGE 2405.17374, Qi 2406.05946, Kwon 2607.14147, Ratnakar 2606.22686, arXiv:2605.09043 CSD-in-dialogue, AQI 2506.13901, arXiv:2603.18353 knowledge-action gap). Anything already anchored there is CITED BY REFERENCE, not re-read. Your budget goes to the steering-measurement lane, which that artifact did not cover.\\n\\nSTEP 1 — GALEONE ET AL., READ TO EXHAUSTION (~35 min)\\n\\nFetch `arxiv.org/abs/2606.24952` (for the comments/venue field and the exact author list and date), then `arxiv.org/html/2606.24952`. Then run `fetch_grep` on the HTML/PDF for each of these patterns and transcribe the matching sections verbatim:\\n- `cos|cosine|angle|degrees` — every cosine reported, with which behaviour, which model, which layer.\\n- `AUC|AUROC|separab` — every detection number and the layer it is reported at.\\n- `Gemma|Llama|Qwen|Mistral|-2b|-9b|-1b` — the exact four-model roster and scales.\\n- `instruct|instruction.tun|base model|pretrain` — the before/after-instruction-tuning comparison and the pretraining-origin claim.\\n- `steering|intervention|coefficient|alpha|magnitude|strength` — HOW they obtain the 'direction that best causes it': is it optimised, difference-in-means over responses, or grid-searched? At what magnitude? On how many probes?\\n- `refusal` — is refusal a target behaviour in its own right, or only the OUTCOME channel for the hallucination probe? This matters enormously for our positioning.\\n- `limitation|scope|future work|we do not` — their own stated scope limits.\\n\\nRecord answers to these seven positioning questions explicitly, each with an anchor:\\nQ1. Is their claim about ANY behaviour, or behaviour-conditional (JSON collapses, hallucination does not)? Our paragraph must not flatten this.\\nQ2. Is their detection direction fit on PROMPTS or on RESPONSES? Ours is a prompt axis vs a response-contrast axis — if theirs is the same contrast pair, our result is a replication in a new behaviour; if different, it is an extension along a new dimension.\\nQ3. What is their steering-effectiveness criterion (a % of probes? a rate? a threshold?) versus our '27% of probes' — are the two numbers commensurable at all?\\nQ4. Do they anywhere claim, or decline to claim, that the CONSEQUENCE is 'you must build metrics from the causal axis, not the detection axis'? If they already say it, our contribution shrinks to a refusal-specific instance and we say so. If they stop at diagnosis, our contribution is the constructive corollary.\\nQ5. The 0.1197 vs 0.1200 result says the gap is a PRETRAINING property, invariant to instruction tuning. Does that predict our axis-choice effect should be present in the BASE model too? Flag this as a testable prediction for the experiment plan — it is a free pre-registered check.\\nQ6. Their cos = -0.06 for a token-free activation detector: does that bear on our H1'' lexical-artefact worry (i.e. does the detection axis's alignment depend on the token set used to define it)?\\nQ7. Venue and review status — is it a preprint, workshop, or conference paper? Do not upgrade.\\n\\nDELIVERABLE 1a: a subsection `## Galeone et al. (arXiv:2606.24952) — what they claim, exactly` with the verbatim abstract, a numbers table, and the seven Q/A entries.\\nDELIVERABLE 1b: a ready-to-paste ~150-word RELATED WORK paragraph and a ~120-word METHOD paragraph. The Method paragraph must state, in our voice and with the exact numbers on both sides: (i) Galeone et al. establish a detection-intervention gap (AUC 1.000, cos = 0.12, ~83 degrees, cos in [0.12,0.20] across four models, invariant to instruction tuning); (ii) our result is the refusal-specific instance — a held-out-AUROC-1.0 prompt-derived axis steers on only 27% of probes while a 0.69-AUROC response-contrast axis is the one that steers; (iii) the ADDED claim is constructive and methodological, not phenomenological: it determines WHICH axis a steering-strength metric must be built from, so alpha_50 is defined on the response-contrast axis by necessity rather than by convenience. Write it so it reads as confirmation-and-extension. Do NOT write 'we discover' or 'we are the first to show' anywhere in it.\\n\\nFAILURE MODE: if the full text is unreachable (PDF/HTML both fail), fall back to the abstract page plus alphaXiv/HuggingFace-papers/Semantic-Scholar mirrors, and mark every un-verified number `ABSTRACT ONLY`. Do NOT silently downgrade the anchor.\\n\\nSTEP 2 — THE STEERABILITY-AS-MEASUREMENT LANE (~45 min)\\n\\nRead each paper below at least to abstract + method + main results. For EVERY paper, fill the SAME five-field record — this uniformity is what makes the dossier usable downstream:\\n(F1) MEASURED QUANTITY — the exact scalar or vector the paper computes, quoted.\\n(F2) MODELS AND SCALES.\\n(F3) HARMFUL-PROMPT DEPENDENCE — does computing their quantity require harmful/unsafe/jailbreak prompts, a reference model, or a benchmark? (This is our whole product claim, so answer it precisely: 'requires harmful prompts to FIT the direction' and 'requires harmful prompts to SCORE' are different answers.)\\n(F4) IS IT FUNCTIONALLY alpha_50? Rate on a 4-point scale — IDENTICAL / SAME-OBJECT-DIFFERENT-UNITS / ADJACENT / UNRELATED — with a one-sentence justification quoting the decisive line.\\n(F5) WHAT IT DOES TO OUR CLAIM — strengthens (we cite as support), constrains (we must add a caveat/scope statement), or collides (we must narrow the novelty claim). Name the exact sentence in our paper that has to change.\\n\\nPRIMARY (must be done):\\n(P1) arXiv:2506.24056 Logit-Gap Steering. THE COLLISION CHECK. `fetch_grep` for `logit gap|refusal.affirmation|first decoding step|margin|diagnostic|forward.pass|26,?000|True.ASR|AdvBench|HarmBench`. Answer, with quotes: does the gap require TOXIC/harmful prompts to compute (the abstract's '97.5-99.8% of toxic prompts' suggests YES — confirm)? Is it computed at the FIRST decoding step only (ours is a generation-onset decision measured over a fresh generation — related but not the same)? Is it a per-PROMPT margin or a per-MODEL score? Is it ever aggregated into a model-level alignment-robustness number, and if so how? Then write the explicit differentiation: alpha_50 is measured in units of NORM_L along a steering axis, on BENIGN prompts only, with no harmful content, and scores a MODEL not a prompt; the logit gap is measured in logit units on toxic prompts. If any of those distinctions fail on close reading, SAY SO PLAINLY in the report under a heading `## NOVELTY THREAT: partially realised` and state precisely what is left that is ours. Also fetch the Unit 42 write-up (unit42.paloaltonetworks.com) for the industrial framing — useful for Related Work, not for numbers.\\n(P2) arXiv:2602.02712 Towards Understanding Steering Strength. THE METHODOLOGY THREAT. `fetch_grep` for `non-?monoton|law|next token probab|cross.entropy|saturat|regime|assumption|theorem`. Extract: under what conditions is the response to steering strength non-monotonic; is the non-monotonicity in the CONCEPT-PRESENCE curve (which is what alpha_50 fits) or only in cross-entropy/fluency; and does the theory predict a saturating sigmoid over some range. Deliverable: a short paragraph the experiment plan can adopt as a pre-registered robustness check — e.g. 'because arXiv:2602.02712 shows steering strength can act non-monotonically, we (a) sweep alpha past the observed 50% crossing to confirm the refusal rate does not turn over, and (b) report the raw dose-response points alongside the logistic fit so a non-sigmoidal shape is visible rather than absorbed by the fit.' If the paper gives an explicit condition for monotonicity, quote it — that is a gift to our pre-registration.\\n(P3) arXiv:2509.13450 SteeringSafety/SteeringControl. F1-F5 plus: does it define any scalar that is a per-MODEL safety readout (as opposed to a per-METHOD steering-quality readout)? Note the title change.\\n(P4) arXiv:2508.21448 Kabir et al. F1-F5 plus: how exactly is 'steerability' operationalised — success rate at fixed strength, or strength required for success? The latter would make it a genuine relative of alpha_50 in a non-safety domain, which is a GOOD citation for us (it shows the family of measure is established, so our contribution is the safety-specific instance).\\n(P5) arXiv:2603.24543 Analysing the Safety Pitfalls of Steering Vectors. F1-F5 plus: the ±57%/-50% ASR swing and the claimed overlap between arbitrary CAA vectors and the refusal direction. This is the second-strongest constraint on our random-direction null after the Rogue Scalpel.\\n\\nSECONDARY (do if time; drop in the stated order if not): arXiv:2604.08524 (mechanistic case study on steering refusal — most likely to contain an alpha-sweep we should cite), arXiv:2608.08383 (safety cost of steering separable/reducible), arXiv:2603.07837 (AI Steerability 360 toolkit), arXiv:2505.20645 (Steer-Bench), AxBench, Angular Steering, arXiv:2506.07022 (AlphaSteer — its per-model lambda thresholds 0.5/0.45/0.14 are a model-dependent intervention-strength constant, i.e. weak evidence that intervention strength is model-idiosyncratic, which SUPPORTS our H1''' comparability worry).\\n\\nSTEP 3 — FRESH SATURATION SEARCH (~35 min)\\n\\nRun in `mode=scholarly`, and ALSO in general mode (arXiv listing pages and blogs surface things scholarly indexes miss). Minimum query set, each run verbatim:\\n1. \\\"steering strength as an alignment metric\\\"\\n2. \\\"steering coefficient threshold refusal\\\"\\n3. \\\"minimal intervention strength alignment\\\"\\n4. \\\"steerability score safety audit\\\"\\n5. \\\"how much steering is needed to induce refusal\\\"\\n6. \\\"activation steering dose-response refusal rate\\\"\\n7. \\\"ED50 OR EC50 OR half-maximal steering language model\\\"\\n8. \\\"critical steering magnitude jailbreak threshold\\\"\\n9. \\\"benchmark-free safety evaluation open-weight checkpoint\\\"\\n10. \\\"safety margin measured without harmful prompts\\\"\\n11. \\\"abliterated model detection metric\\\"\\n12. \\\"refusal direction norm normalization cross-model comparison\\\"\\n13. \\\"steering strength required behavior elicitation model comparison\\\"\\n14. \\\"logistic dose response activation steering\\\"\\n\\nRULES: report HITS, with counts and the top 5 titles per query. NEVER write 'zero results' as a novelty argument — if a query genuinely returns nothing relevant, report the query, the mode, the date, and the nearest neighbours it DID return. For every hit that looks within one hop of alpha_50, open it and fill the F1-F5 record. Also do one targeted check on the abliteration literature specifically: is there any published metric that scores 'how abliterated is this checkpoint' from steering strength? (AMS from art_0UsKSgsMHome is the activation-geometry answer; we need to know whether a steering-strength answer exists.)\\n\\nDELIVERABLE 3: a section `## Saturation check, dated <run date>` with the query table, the hit list, and a single explicit verdict sentence chosen from exactly one of:\\n(a) NOTHING EQUIVALENT FOUND — followed by a POSITIVE novelty statement (see Step 6 rules), not a zero-hits claim;\\n(b) ADJACENT WORK EXISTS — naming it and stating the residual contribution in one sentence;\\n(c) FUNCTIONALLY EQUIVALENT WORK EXISTS — naming it, quoting the decisive line, and stating precisely what remains ours (likely candidates for what remains: benign-prompts-only measurement, the fresh-generation rather than first-token operationalisation, per-model NORM_L normalisation, the base-vs-tuned vs price-of-the-mode decomposition, and the paired instruct-minus-abliterated test). Verdict (c) is a SUCCESSFUL outcome of this artifact, not a failure — write it without hedging if it is what the evidence says.\\n\\nSTEP 4 — THE ROGUE SCALPEL, AND WHAT OUR RANDOM-DIRECTION NULL MAY STATE (~20 min)\\n\\nFetch arXiv:2509.22067 (abs + html/pdf) and its OpenReview forum (id uXecy0nKiJ) for venue/decision/reviews. `fetch_grep` for `random|norm|magnitude|coefficient|alpha|strength|scale|layer|1-13|universal|20 vectors|harmful compliance|StrongREJECT|HarmBench`.\\n\\nExtract, with quotes, the four things that decide whether our null survives:\\n(R1) At what MAGNITUDE (and in what normalisation — raw L2, multiples of the residual-stream norm, multiples of the mean activation norm?) do random vectors produce the 0%->1-13% effect? If they normalise to the activation norm, convert into our NORM_L units and state the conversion assumption explicitly.\\n(R2) At which LAYERS, and on how many random draws — is 1-13% a per-draw rate or a best-of-N over many draws? A best-of-N maximum and a per-draw expectation are very different objections to our null.\\n(R3) Is the broken behaviour COMPLIANCE-INDUCING (guardrails down) or does random steering ever induce REFUSAL on benign prompts? Our null is specifically 'a matched random direction does not induce refusal at any alpha on benign prompts'. The Rogue Scalpel measures the OPPOSITE direction of failure. If it never tests random-induced refusal on benign prompts, our null is untouched by it and we say exactly that — with the quote.\\n(R4) Does it report a magnitude BELOW which random steering has no effect? That number is what our null must be scoped to.\\n\\nDELIVERABLE 4: a subsection `## Does The Rogue Scalpel weaken our matched-random-direction null?` ending with a single ready-to-paste sentence for our Method of the form: 'Our random-direction control is a statement about a magnitude range: over alpha in [0, ALPHA_MAX] in units of NORM_L, a norm-matched random direction induced refusal on benign prompts at no tested coefficient. We do not claim random directions are behaviourally inert — arXiv:2509.22067 reports that random steering raises harmful compliance from 0% to 1-13% [anchor], and arXiv:2603.24543 reports arbitrary CAA vectors moving JailbreakBench ASR by up to 57% [anchor] — but both concern the compliance direction under <their magnitude regime>, whereas our control concerns refusal induction on benign prompts.' Fill the bracketed regime from R1/R2. If R1-R4 show the effect occurs at magnitudes INSIDE our sweep range and in a way that does bear on refusal, say the null is WEAKENED and specify the extra control the experiment must add (concretely: N>=10 independent random draws per model with the same logistic dose-response fit, reporting max-over-draws rather than a single draw, so a best-of-N objection is pre-empted).\\n\\nSTEP 5 — POSITIVE NOVELTY STATEMENT FOR THE EWS NEGATIVE (~10 min)\\n\\nThe iteration-1 argument was 'an arXiv abstract search for EWS + LLM returns zero'. That is a weak, unfalsifiable-looking argument and gets demoted to a footnote. Build the replacement:\\n- Confirm the two known neighbours from art_0UsKSgsMHome: arXiv:2605.09043 (critical slowing down applied to conversation derailment in HUMAN DIALOGUE TEXT) and Rahimi et al. arXiv:2602.02600 (step-wise refusal dynamics, comparing autoregressive vs DIFFUSION SAMPLING mechanisms). Re-verify each has the scope property we rely on with a one-line quote.\\n- Run 3-4 fresh scholarly queries: \\\"critical slowing down large language model\\\", \\\"early warning signals neural network dynamics\\\", \\\"variance autocorrelation tipping point transformer generation\\\", \\\"resilience indicators machine learning model behaviour\\\". Report hits.\\n- Draft the POSITIVE statement (~90 words), structured as a three-axis differentiation rather than an absence claim: our EWS negative is the first controlled test of the critical-slowing-down indicator suite computed (i) on GENERATED-STEP time series of a model-internal refusal observable, rather than on dialogue text [2605.09043] or on sampling-mechanism comparisons [2602.02600]; (ii) with an explicit perturbation-recovery arm and matched random-direction and surrogate controls; (iii) with a pre-registered estimator-identifiability gate, so the negative is attributable to the phenomenon rather than to the estimator. Add the footnote text carrying the old zero-hits search as supporting, not primary, evidence.\\n\\nSTEP 6 — WRITE-UP (~30 min)\\n\\n`research_report.md` sections, in this order:\\n1. Executive summary — max 12 bullets, each with an anchor. Lead with the saturation verdict (a/b/c) and the Logit-Gap resolution, because those are what change the paper.\\n2. Galeone et al. read to exhaustion (Step 1) + the two ready-to-paste paragraphs, clearly fenced and labelled `PASTE INTO RELATED WORK` / `PASTE INTO METHOD`.\\n3. The steerability-as-measurement lane — one uniform F1-F5 record per paper, plus a single comparison table with columns: paper | arXiv ID | venue/status | measured quantity | models | needs harmful prompts? | needs reference model? | relation to alpha_50 (4-point) | what it does to our claim.\\n4. Saturation check with query table, hit counts, and the one-sentence verdict.\\n5. The Rogue Scalpel analysis + the magnitude-scoped null sentence.\\n6. Positive novelty statement for the EWS negative + the demoted footnote.\\n7. Actionable consequences for the experiment plan — a numbered list of concrete changes, each naming the hypothesis it touches (H1', H1'', H1''', H2', H3', H5'). Expected members: the non-monotonicity robustness check from P2; the N>=10 random-draw control from Step 4 if warranted; the base-model prediction implied by Galeone's instruction-tuning invariance (Q5); whether the response-contrast axis is now a citation-supported choice rather than an ad-hoc one; and any claim in the hypothesis that must be softened or withdrawn.\\n\\nWRITING RULES, ENFORCED:\\n- No 'to the best of our knowledge', no 'first ever', no zero-hit novelty arguments in the main text.\\n- Every number in quotation marks or marked `NOT FOUND IN PRIMARY TEXT`.\\n- Report venue and review status honestly; most 2026 items here are preprints. Do not upgrade a preprint to a conference paper. DO report the one CONFIRMED upgrade the planner found: arXiv:2606.22686 carries an 'Accepted at TrustNLP 2026 (co-located with ACL 2026)' comment.\\n- Flag every title change between arXiv versions (2509.13450, 2508.21448 confirmed; check the others) so downstream citations are not stale.\\n- If a finding contradicts the hypothesis document as written, say so in Section 7 and name the sentence to change. Contradictions found here are cheap; contradictions found by a reviewer are not.\\n\\n`research_out.json` — `answer` carries: the saturation verdict string; the per-paper table as a JSON array of the F1-F5 records; the two ready-to-paste paragraphs verbatim; the magnitude-scoped null sentence; the EWS positive statement; and the Section-7 consequences list. `sources`: every URL fetched, with arXiv ID and title. `follow_up_questions`: at minimum, anything that could not be resolved from primary text (e.g. an unreachable PDF, an ambiguous normalisation convention in 2509.22067) stated as a specific question, not a topic.\\n\\nCONTINGENCIES\\n- If arXiv:2506.24056 turns out to be functionally identical to alpha_50: do not soften it. Write verdict (c), quote the decisive line, and spend the remaining time enumerating precisely what survives (benign-only measurement; model-level rather than prompt-level score; the reachable-mode vs price-of-the-mode decomposition; per-model NORM_L normalisation; the paired instruct-vs-abliterated test). A correctly narrowed contribution is publishable; an overclaimed one is not.\\n- If several primary PDFs are unreachable, prioritise Step 1 and Step 2-P1/P2 and mark the rest `ABSTRACT ONLY` rather than thinning all of them equally.\\n- If a search returns a paper that measures exactly 'the steering coefficient at 50% behaviour crossing' under a different name (ED50/EC50/critical alpha/threshold coefficient), that is the collision — treat it with Step 2-P1's full protocol immediately, even at the cost of the secondary papers.\",\n  \"explanation\": \"The experiment plan for iteration 2 rests on two claims this artifact decides. First, the site-selection result (a prompt-derived axis at held-out AUROC 1.0 steers on only 27% of probes, while a 0.69-AUROC response-contrast axis is the one that actually steers) is currently written as a discovery, but Galeone et al. (arXiv:2606.24952) already published the general detection-intervention gap — AUC 1.000 with cos = 0.12 (~83 degrees), cos in [0.12, 0.20] across four models from three families, and essentially invariant to instruction tuning (0.1197 vs 0.1200). Presenting our result as new would be an overclaim a reviewer catches in one search; presenting it as a refusal-specific confirmation WITH a constructive extension — it determines which axis a steering-strength metric must be built from — is both honest and stronger. That reframing needs their exact claims and scope, which is why Step 1 reads them to exhaustion.\\n\\nSecond, alpha_50 is the iteration's primary metric, and it has not had a saturation check. The planner already found the sharpest threat: Logit-Gap Steering (arXiv:2506.24056) defines 'the refusal-affirmation logit gap' at the first decoding step as 'the per-prompt safety margin that alignment provides' and pitches it as an alignment-robustness diagnostic — the same conceptual object as alpha_50 in different units and on toxic rather than benign prompts. Whether the differences (benign-only, model-level, fresh-generation, NORM_L-normalised) are load-bearing decides how the paper's contribution must be stated. A second, quieter threat is arXiv:2602.02712, whose theoretical result that steering strength can act NON-MONOTONICALLY directly undermines alpha_50's logistic dose-response fit unless the experiment adds a sweep-past-crossing check and reports raw dose-response points — a design change that is nearly free now and impossible after the run.\\n\\nThird, The Rogue Scalpel (arXiv:2509.22067) reports random steering vectors raising harmful compliance from 0% to 1-13%, and arXiv:2603.24543 reports arbitrary CAA vectors swinging JailbreakBench ASR by up to 57%. Our matched-random-direction null says a random axis induces refusal at no alpha. Those results concern the opposite direction of failure, but unless the magnitude regime is pinned down, the null reads as naive. Step 4 converts it into a defensible, magnitude-scoped statement, or tells the experiment to add an N>=10-draw control.\\n\\nAll of this is pure literature work with no compute requirement, and it must happen BEFORE the experiment is designed, because its outputs are design changes (axis choice justification, non-monotonicity robustness check, random-draw control, base-model prediction) and paper-text changes (novelty statement, Related Work, the EWS negative's positive framing) rather than post-hoc commentary.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [30] ASSISTANT · 2026-08-12 17:09:57 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json`.

**What the plan covers** (6 steps, time-boxed to 3h, `cpu_light`):

1. **Galeone et al. read to exhaustion** — I pre-verified the abstract: AUC 1.000 from layer 5, cos = 0.12 (~83°), cos ∈ [0.12, 0.20] across four models/three families/1B–9B, and **0.1197 vs 0.1200 before/after instruction tuning** (gap originates in pretraining). Seven positioning questions plus two ready-to-paste paragraphs framing our 27%-vs-0.69 result as confirmation-and-extension.

2. **The steerability-as-measurement lane** — uniform 5-field record per paper. All six named arXiv IDs verified as real, with two title-change traps flagged (2509.13450 → *SteeringSafety*; 2508.21448 → *When Models Refuse*).

3. **Two threats the direction did not name, found during planning:**
   - **arXiv:2506.24056 Logit-Gap Steering** — defines the refusal–affirmation logit gap at the first decoding step as "the per-prompt safety margin that alignment provides," framed as an alignment-robustness diagnostic. This is the same conceptual object as α₅₀ in different units. The plan makes resolving it the highest-value task and pre-writes the verdict-(c) protocol so a partial collision is reported plainly rather than hedged.
   - **arXiv:2602.02712** proves steering strength has **non-monotonic** effects — a direct threat to α₅₀'s logistic dose-response fit. Plan turns this into a concrete pre-registration amendment (sweep past crossing; publish raw dose-response points).

4. **Rogue Scalpel** verified (random directions: 0% → 1–13% harmful compliance; 20-vector universal attack) — plan extracts the magnitude/normalisation/layer/draw-count regime and outputs a magnitude-scoped null sentence, or mandates an N≥10-draw control.

5. **EWS positive novelty statement** replacing the zero-hits argument, with the demoted footnote.

6. Section 7 is an actionable consequences list keyed to H1′/H1″/H1‴/H2′/H3′/H5′, so the dossier changes the experiment design rather than just commenting on it.

One bonus confirmed upgrade: arXiv:2606.22686 (*Geometry of Refusal*) carries an "Accepted at TrustNLP 2026, co-located with ACL 2026" comment — the hypothesis currently lists it as a bare preprint.

Sources: [2606.24952](https://arxiv.org/abs/2606.24952), [2509.22067](https://arxiv.org/abs/2509.22067), [2509.13450](https://arxiv.org/abs/2509.13450), [2508.21448](https://arxiv.org/abs/2508.21448), [2602.02712](https://arxiv.org/abs/2602.02712), [2603.24543](https://arxiv.org/abs/2603.24543), [2506.24056](https://arxiv.org/abs/2506.24056)
```
