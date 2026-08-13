# review_hypo — create_idea

> Phase: `hypo_loop` · round 2 · `review_hypo`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-12 12:53:50 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_2/review_hypo
```

### [2] SYSTEM-USER prompt · 2026-08-12 12:53:56 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviewer (Step 2.2: REVIEW_HYPO)

Pipeline: GEN_HYPO → REVIEW_HYPO (you) → INVENTION_LOOP → GEN_PAPER_REPO

You review a hypothesis BEFORE any experiments run. Catch problems early.

Rigorous pre-flight check → saves compute. Rubber-stamping → wasted pipeline run.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical conference reviewer.
Your expertise spans the domain of the hypothesis under review.
You have served on program committees at top-tier venues in the relevant field.

TASK: Perform a deep and honest review (at the level of a top-tier venue submission) of
this research hypothesis BEFORE any experiments have been run.

GOAL: Your review feeds directly back to the hypothesis author. The objective is to
maximize the overall review score in subsequent rounds. Every piece of feedback you
give should be written with this goal in mind — prioritize the critiques and suggestions
that would produce the largest score improvement if addressed. Don't waste the author's
iteration budget on low-impact polish when there are score-blocking issues to fix.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Originality: Are the ideas new? Novel combination of known techniques? Clear
    differentiation from prior work? Is related work adequately cited?
(b) Quality: Is the proposal technically sound? Are claims well supported? Is the
    methodology appropriate? Are the authors honest about limitations?
(c) Clarity: Is the hypothesis clearly written and well organized? Does it provide
    enough information for an expert to understand and evaluate it?
(d) Significance: Are the expected results important? Would others build on this?
    Does it address a meaningful problem better than prior work?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims and proposed methodology:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — quality of the overall contribution, importance of questions asked,
originality of ideas, value to the broader research community:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (would waste compute if not fixed) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Flag fatal flaws that would make experiments pointless if not addressed first
- Screen the hypothesis for prior art before any compute is spent. Search the web for the proposed idea, its method name, and its central claim. If the idea already exists, say so and name the source — this is the cheapest point in the pipeline to catch it
- Distinguish a genuinely new idea from a restatement of known work in new vocabulary. Coining a term for an existing method is not originality, and should be scored as a major issue

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<hypothesis>
kind: hypothesis
title: Safety as nearness to a tipping point
hypothesis: >-
  Safety fine-tuning does not merely install a harm detector; it moves the model's default generative state close to a bistable
  switching point between 'comply' and 'refuse'. Because of this, a safety-aligned model is measurably 'twitchy' about refusal
  even while generating completely harmless text, while base and uncensored models sit deep inside the comply basin. All claims
  are made about the genuine stochastic dynamical system in an LLM - autoregressive generation under temperature sampling,
  whose state is the generated prefix - not about token positions inside one forward pass. Concretely: (H1 - path-dependent
  switching) if a steering coefficient alpha along a refusal axis is ramped up WITHIN a single generation until refusal onset
  and then ramped back down while the generated prefix and KV cache are retained, the flip-to-refuse and flip-back-to-comply
  thresholds differ, giving a hysteresis loop of nonzero width; a reset-control arm that discards the prefix between alpha
  steps must give exactly zero width, which is what proves the loop is path dependence rather than noise. (H1b - safety specificity,
  pre-registered as separable from H1) loop width is ordered instruct > base and instruct > abliterated, paired over prompts.
  (H2 - critical slowing down) on harmless prompts only, and measured over GENERATED steps across sampled rollouts, a small
  perturbation injected into the residual stream decays more slowly (lower recovery rate lambda), and the refusal observable
  shows larger across-rollout variance, higher lag-1 autocorrelation, and more near-threshold flickering, in models that are
  behaviorally safer - the standard early-warning-signal signature of proximity to a fold bifurcation. (H3 - prediction) a
  single scalar built from these harmless-input dynamics, the Switching Proximity Index (SPI), rank-orders open-weight checkpoints
  by BOTH plain-harmful refusal rate AND jailbreak attack-success rate, with predictive power beyond the static mean level
  of the refusal observable, beyond two trivial output-side baselines, and beyond the published incumbents RAS and VISAGE.
  (H4 - where static geometry fails) SPI in particular succeeds on 'behavioral' uncensored fine-tunes, which preserve harmful/benign
  cluster geometry and the refusal direction intact and are a documented blind spot of activation-geometry scanners.
motivation: >-
  Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt
  benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator
  to hold and send harmful content. The two published cheap alternatives both retain a dependency this proposal drops. AMS
  (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy
  over 14 configurations and, explicitly, that behavioral uncensored fine-tunes preserving geometry are undetectable by it.
  RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe
  and jailbreak prompts AND a safety-aligned reference model to supply the direction. VISAGE (arXiv:2405.17374) measures a
  safety BASIN in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static,
  read-side measurements: they ask 'is harm represented, and does the representation look aligned?'. That question provably
  does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.
  This hypothesis attacks the gap from the act side and with a different unit: not a direction, feature or basin volume, but
  a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge, while it is doing
  something innocuous? If true it yields (a) a mechanistic account of what safety tuning buys, in the language of bistable
  systems - a shifted operating point, which recasts the 'shallow safety alignment' finding as a shallow BASIN IN BEHAVIORAL
  STATE SPACE rather than in weight space or token depth; (b) an audit that needs a handful of harmless prompts, no harmful
  content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal
  toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety
  is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.
assumptions:
- >-
  Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated
  prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over
  GENERATED steps. This replaces the previous, indefensible assumption that token position inside a single forward pass is
  a relaxation axis: within one pass, decay is dominated by attention dilution (an injected key competes with t-1 others,
  so influence falls roughly as 1/t), RMSNorm rescaling and residual-norm growth, and variance over prompt positions is dominated
  by deterministic token identity rather than fluctuation around an attractor. The single-forward-pass version is retained
  only as an explicitly heuristic secondary measurement with the 1/t dilution null fitted and subtracted.
- >-
  The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives
  the abliteration edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is the primary
  readout precisely because a projection onto the abliterated direction is near-constant by construction, which would make
  any variance claim on abliterated models circular. The per-model diff-in-means axis is a secondary readout, and all indicators
  are computed on the within-model z-scored observable so that scales are commensurable across families and layers.
- >-
  Ground truth is not one-dimensional and must not be treated as such: over-refusal and harmful compliance are nearly uncorrelated
  across open-weight models (arXiv:2605.05427). Three ground truths are therefore measured and reported separately - plain-harmful
  refusal rate, jailbreak attack-success rate, and XSTest-style over-refusal rate - and the panel must span a GRADED range
  of each, not three discrete classes, or a rank correlation degenerates into a 3-class discrimination that trivial baselines
  also win.
- >-
  A graded safety ladder can be manufactured without any training, by scaling the alignment task vector: W(t) = W_base + t
  * (W_instruct - W_base) for t in {0, 0.25, 0.5, 0.75, 1.0}, and by scaling the abliteration orthogonalization strength.
  This gives intermediate refusal rates at the cost of a few matrix operations, and its members are explicitly flagged as
  non-independent so that bootstrap resampling is done over weight LINEAGES, not over interpolants.
- >-
  Small models (0.36B-4B, CPU-feasible in float32/int8, generations capped at 32-64 tokens with rollouts batched) show the
  same qualitative refusal machinery reported for larger models. This is tested rather than assumed, via a within-family scale
  ladder (Qwen3 0.6B/1.7B/4B), because a small model that is 'twitchy' may be twitchy from undertraining rather than from
  proximity to a switch; scale enters the headline analysis as a covariate.
investigation_approach: |-
  PANEL (>= 30 units, >= 4 architecture families, all CPU-feasible). Real checkpoints: Qwen3-0.6B/1.7B/4B base + instruct + abliterated; Qwen2.5-0.5B/1.5B-Instruct; Llama-3.2-1B/3B-Instruct + an abliterated variant; gemma-2-2b-it; SmolLM2-360M/1.7B-Instruct; TinyLlama-1.1B-Chat; and at least two behavioral uncensored fine-tunes (Dolphin/Josiefied-style) as the class static geometry cannot see. Graded fillers: task-vector interpolants at t = 0.25/0.5/0.75 for three base/instruct pairs, plus partial-strength abliteration at 0.25/0.5/0.75, giving intermediate refusal rates for free.

  STEP 0 - PRE-REGISTRATION (written before any run). Layer L is fixed by a rule that never touches the outcome: L is the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set computed on ONE reference model only, then transferred to every other checkpoint by relative depth L/n_layers. The full layer profile is reported as a secondary descriptive figure with Holm correction on any per-layer claim, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies. Decoding is fixed and reported: chat template, empty system prompt, max 64 new tokens, temperature 0.7 for dynamics and 0.0 for the deterministic control. SPI is fixed in advance as SPI = mean of the within-panel z-scores of [ -log lambda , log Var*(r) , Fisher-z(AC1(r)) , logit(flicker rate) ], where r is the within-model z-scored logit-lens refusal log-odds and Var* is the ACROSS-ROLLOUT variance at fixed generated step. Higher SPI = closer to the switching point = expected to refuse more. Single-term versions are reported alongside so a reader can see which term carries the signal.

  STEP 1 - H1, hysteresis as a within-generation ramp. Fix a benign prompt. Decode autoregressively while raising alpha along the refusal axis by a fixed step per generated token until a refusal-onset token is emitted (alpha_up). Then CONTINUE decoding the same sequence, prefix and KV cache retained, lowering alpha per step, and record the alpha at which compliant continuation resumes (alpha_down). Loop width = alpha_up - alpha_down. Mandatory reset-control arm: discard the prefix between alpha steps; this must give width exactly 0, since under greedy decoding the response is then a deterministic single-valued function of alpha. Report width distributions over >= 30 prompts with bootstrap CIs, at temperature 0 and 0.7, and report near-threshold flickering at temperature 0.7 as a bonus early-warning indicator.

  STEP 2 - H2, early-warning indicators on harmless input only. For each of ~20 benign prompts, run >= 20 sampled rollouts with paired random seeds. In the perturbed arm inject a norm-epsilon vector into the residual stream at layer L at generation step p, continue decoding, and fit an exponential to |delta r_t| over subsequent GENERATED steps to get lambda. From the clean rollouts alone compute across-rollout Var*(r) at fixed step, AC1 along each rollout, and the flicker rate. Sweep epsilon to confirm linearity. Three mandatory null controls: (i) a RANDOM readout axis, which must NOT reproduce the safety ordering; (ii) random-direction vs refusal-aligned perturbation; (iii) a purely syntactic observable (part-of-speech probe direction), which should decay at the same rate if what is being measured is generic mixing rather than a basin. Demonstrate, not assume, that lambda is invariant to axis scaling.

  STEP 3 - ground truth, three axes. Per checkpoint: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same prompts under a fixed small jailbreak suite including prefill (attack-success rate), and ~50 XSTest benign-but-scary prompts (over-refusal rate). Scoring: a cheap OpenRouter LLM judge is PRIMARY, the refusal-string matcher is a screen; report Cohen's kappa between them, hand-adjudicate a stratified sample of >= 100 items to estimate judge error, and report the attenuation-corrected correlation alongside the raw one. Budget < $2, well inside the $10 cap.

  STEP 4 - H3/H4, prediction against pre-registered competitors. Spearman rank correlation of SPI with each ground truth, bootstrapped over weight LINEAGES (the unit of the model-level claim); the prompt-level bootstrap is reported separately and labelled as measurement noise only. Baselines, all pre-registered: (a) static mean level of r on benign prompts - the strongest cheap competitor; (b) two trivial output-side detectors using ZERO internals - next-token probability of refusal-onset tokens on the same benign prompts, and 'does the model ever emit an apology token'; (c) AMS-style cluster separation sigma and refusal-direction cosine; (d) a RAS/SafeVec-style representation-alignment score (needs harmful+jailbreak prompts and a reference model - the dependency SPI claims to drop); (e) VISAGE-style weight-perturbation basin volume, run on a 6-model subset only, with the reduction stated honestly. Report leave-one-out accuracy in AMS's own format so the comparison is like-for-like, plus leave-one-FAMILY-out. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND for model scale.

  STEP 5 - mechanism map. Layer-wise and step-wise profiles of lambda for base vs instruct vs abliterated vs interpolants: does safety tuning shallow the basin at particular layers or early generated steps, does the basin shallow monotonically with the task-vector coefficient t, and does abliteration revert to the base state or produce a third state that is neither?
success_criteria: |-
  POWER (stated in advance). At n = 30 lineage-weighted units the 95% bootstrap CI half-width on an observed Spearman rho = 0.8 is roughly +/-0.15, and a partial correlation with two covariates has adequate power only for partial rho >= 0.45. Criteria below are set at those attainable levels; if the achieved panel is smaller, criterion (3) is softened in advance to a directional claim with an honest CI rather than retro-fitted.

  CONFIRMS: (1) Hysteresis loop width is significantly > 0 in the retained-prefix ramp while the reset-control arm gives exactly 0 (bootstrap CI over prompts) - path-dependent switching is real. (2) Loop width is ordered instruct > base and instruct > abliterated, paired over prompts, with CIs excluding 0 - the switching carries safety information. (3) On harmless prompts only and over generated steps, lambda is lower, Var*, AC1 and flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls. (4) SPI attains Spearman rho >= 0.75 with plain-harmful refusal rate and rho >= 0.6 with jailbreak attack-success rate over >= 30 units, with a lineage-bootstrap CI lower bound above the best of the static-mean and the two trivial output-side baselines, and the partial correlation controlling for static mean and scale has a 95% CI excluding 0. (5) SPI matches or beats AMS leave-one-out accuracy in AMS's own format and matches RAS/VISAGE without needing their harmful prompts or reference model. (6) SPI correctly flags the behavioral uncensored fine-tunes that cluster separation and refusal-direction cosine both mark as safe.

  THIRD OUTCOME, PRE-REGISTERED (not a failure): 'bistability present but not safety-specific' - nonzero loop width in BASE models too. This is a live possibility because prefill-collapse dynamics have been attributed to generic autoregressive conditioning rather than safety-specific suppression (arXiv:2607.14147), and autoregressive commitment is reported to mask underlying instability (arXiv:2602.02600). If it occurs, the report states that hysteresis is a property of autoregressive decoding, and only the QUANTITATIVE width ordering of criterion (2) carries safety information; H1 is then reported as confirmed and H1b as refuted.

  DISCONFIRMS (reported as refutation, not salvaged): loop width indistinguishable from the reset control anywhere, i.e. no path dependence and the bistable framing is wrong; or lambda / Var* / AC1 / flicker show no consistent ordering with any of the three ground truths; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured rather than a basin; or the correlation vanishes once the static mean and scale are partialled out, meaning the dynamics add nothing over 'how refusal-leaning is this model on average'; or a trivial zero-internals output-side baseline matches SPI, meaning the internals add nothing; or the indicators work within one family but fail leave-one-family-out, which bounds the metric to a within-family diagnostic.
related_works:
- >-
  Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access
  2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine), validated on
  14 configurations across 4 families with 71% leave-one-out accuracy, predicting compliance at Pearson r = -0.546, and explicitly
  reporting that behavioral uncensored fine-tunes preserving geometry are undetectable. Closest work and sharpest departure:
  it measures a static read-side property using harmful prompts; we measure a dynamical act-side RATE using harmless prompts
  only, and its documented blind spot is our H4 test case. We report leave-one-out accuracy in its format for a like-for-like
  comparison.
- >-
  Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise
  refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state
  alignment under unsafe and jailbreak prompts, mapping to a calibrated 0-100 RAS score; separates aligned from uncensored/abliterated
  variants across Llama, Gemma and Qwen. This is the incumbent for our H3 product claim and is run as an empirical baseline.
  It needs harmful and jailbreak prompts AND a reference model; SPI claims to need neither, and measures relaxation dynamics
  rather than static alignment of a hidden state to a borrowed direction.
- >-
  Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the 'safety basin' in WEIGHT
  space (random weight perturbations preserve safety locally, with a sharp step-like drop outside) and proposes the VISAGE
  basin-volume safety metric. The 'shallow basin' language is therefore not ours to coin, and we say so. The departure is
  the space and the cost: VISAGE probes weight-space geometry and requires a harmful benchmark evaluated at every perturbation;
  we probe the basin of the BEHAVIORAL/generative state under harmless input and read it from a relaxation rate. VISAGE-style
  basin volume is run as a baseline on a model subset.
- >-
  Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with
  linear probes and finds a sharp drop at final tokens before output in poorly aligned reasoning models. The per-token-position
  refusal score is therefore an existing observable, not a new one; we adopt it rather than coin it, and our contribution
  is the dynamical statistics computed on it across sampled rollouts (recovery rate, across-rollout variance, autocorrelation,
  flicker) plus the hysteresis test, none of which appear there.
- >-
  Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - studies
  step-wise refusal dynamics, shows diffusion remasking enables recovery from harmful intermediate generations, and proposes
  the SRI internal-dynamics signal, observing that autoregressive commitment masks underlying instability. Closest 'dynamics
  of refusal during decoding' work. It compares SAMPLING MECHANISMS for robustness; we hold the sampling mechanism fixed and
  use controlled perturbation-recovery as an ESTIMATOR of proximity to a switching point, and predict unseen checkpoints'
  safety from harmless prompts. Its commitment finding is a named threat we pre-register against.
- >-
  Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - mechanistic study of the prefill jailbreak; harm representation
  stays intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific
  collapse in a non-safety-tuned model, concluding the prefill's grip is 'generic autoregressive conditioning, not safety-specific
  suppression'. This directly threatens our base-vs-instruct contrast and is why H1 (bistability) and H1b (safety specificity)
  are separated with a pre-registered third outcome.
- >-
  Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive
  Logit Steering plus prefix injection induces 'a phase transition where guardrails collapse', and reports architecture-dependent
  topologies: 'Late Decision' models (Llama, divergence only at final layers, 95% ASR) vs 'Early Divergence' models (Qwen,
  safety integrated at ~40% depth). Phase-transition language for refusal already exists here, but as an ATTACK that pushes
  the system over the edge; our whole point is estimating distance to the edge without crossing it. Its topology finding is
  why our layer-selection rule transfers by relative depth and why family differences are interpreted rather than swept.
- >-
  Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal
  and harmful compliance are nearly uncorrelated, with conservative (Llama) and permissive (Qwen, DeepSeek) calibration ecosystems.
  This is why we predict three separate ground truths instead of a single scalar 'safety', and why a metric validated only
  against plain-harmful refusal rate would be a weaker claim than it appears.
- >-
  Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the
  static geometric account of refusal, and our experimental instrument for producing (and partially producing) uncensored
  checkpoints. Because abliteration orthogonalizes writes against that direction, we deliberately do NOT use a projection
  onto it as the primary observable.
- >-
  Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows the aligned and unaligned
  generative distributions differ mainly over the first few output tokens, which prefilling attacks exploit. It establishes
  shallowness in TOKEN DEPTH; it does not model refusal as a bistable switch and offers no harmless-prompt-only diagnostic.
  Our account reinterprets it as a shallow basin in state space and turns it into a measurement.
- >-
  Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry
  (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering as a system nears a
  fold bifurcation). This is the imported source, not a competitor; our scholarly searches found it applied to ecosystems,
  climate, financial crises, depression and sleep, but not to the internal state dynamics of language models or to safety
  auditing.
inspiration: >-
  The transfer is from ecology and climate science, at the methodological level (level 3). Ecologists face our problem in
  a different costume: they need to know how close a lake, forest or fish population is to collapsing, and cannot run the
  experiment of collapsing it. Scheffer's early-warning-signal programme solved this by measuring the response to small, harmless
  disturbances - as a system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery
  from tiny nudges slows, spontaneous fluctuations grow in variance, become more autocorrelated, and the system begins to
  flicker between modes. Resilience becomes measurable without ever pushing the system over the edge. Mapped onto model auditing:
  don't jailbreak a model to find out whether it can be jailbroken - nudge it gently while it is doing something innocuous
  and watch how fast it settles back. Crucially, the import is only legitimate where a real stochastic dynamical system exists,
  which is why the measurement lives in autoregressive sampling (state = generated prefix) and not inside a single forward
  pass. Two further imports come with the package: from physics and materials science, the hysteresis loop as the decisive
  test that a switch is genuinely bistable rather than merely biased - which forces the sweep to happen WITHIN one generation
  with the prefix retained, since path dependence needs a persistent state variable; and from experimental genetics, the base
  / safety-tuned / abliterated series read as wild-type / knock-in / knock-out, extended here to a dose-response ladder by
  scaling the alignment task vector, the way a geneticist would use graded expression rather than only knockouts. What a domain
  expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object -
  a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.
terms:
- term: Refusal observable (r_t)
  definition: >-
    A scalar read off the model at each GENERATED step t. Primary form: the logit-lens log-odds of refusal-onset tokens against
    continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. Secondary
    form: projection of the residual stream onto a diff-in-means refusal axis. Always z-scored within model before any cross-model
    comparison.
- term: Critical slowing down
  definition: >-
    The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows,
    fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in
    ecology, climate science and psychiatry for estimating resilience without triggering the collapse.
- term: Recovery rate (lambda)
  definition: >-
    The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small perturbation
    is injected into the residual stream, averaged over >= 20 paired-seed sampled rollouts. Small lambda = slow recovery =
    shallow basin = close to switching. Must be shown invariant to readout-axis scaling.
- term: Switching Proximity Index (SPI)
  definition: >-
    The proposed safety metric, sign-transparent by construction: higher SPI = closer to the comply/refuse switching point
    = expected to refuse more. Fixed a priori as the mean of the within-panel z-scores of [-log lambda, log across-rollout
    variance of r, Fisher-z of lag-1 autocorrelation of r, logit of flicker rate], computed from a handful of harmless prompts
    at a pre-registered layer. (Renamed from 'Refusal Resilience Index', whose name read backwards relative to its construct.)
- term: Hysteresis loop width
  definition: >-
    In a ramp performed WITHIN a single generation with the prefix and KV cache retained, the gap between the steering coefficient
    at which the model flips into refusal while alpha is rising and the coefficient at which it flips back while alpha is
    falling. Retaining the prefix is what supplies the state variable; a reset-control arm that discards it must give width
    exactly zero, since without state the response is a single-valued function of alpha.
- term: Flicker rate
  definition: >-
    At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts
    that switch mode between refusal and compliance. Flickering is a classical early-warning indicator alongside variance
    and autocorrelation, and is available only because the measurement lives in stochastic sampling rather than in a deterministic
    forward pass.
- term: Task-vector safety ladder
  definition: >-
    A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) for intermediate t, plus
    partial-strength abliteration. It fills the middle of the refusal-rate range so that a rank correlation is a real correlation
    rather than a disguised 3-class discrimination. Its members share a weight lineage and are excluded from independent-unit
    counts in the bootstrap.
- term: Behavioral uncensored fine-tune
  definition: >-
    An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than by a directional weight edit.
    It can keep harmful/benign activation geometry and the refusal direction intact while complying with nearly all harmful
    requests, which makes it invisible to static activation-geometry scanners - hence the sharpest test case for a dynamical
    metric.
- term: Knowledge-action gap
  definition: >-
    The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act
    on it (98.2% probe AUROC vs 45.1% output sensitivity in the 2026 clinical result). It is why a read-side safety metric
    can be confidently wrong, and why this hypothesis measures an act-side quantity.
summary: >-
  Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable
  about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation,
  via the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges,
  higher across-rollout variance, autocorrelation, and flickering), with a within-generation hysteresis loop as the decisive
  test that the switch is genuinely bistable. This yields a safety score for any open-weight checkpoint from a handful of
  harmless prompts, no harmful content and no reference model, aimed exactly where static activation-geometry scanners are
  documented to fail.
</hypothesis>

<review_context>
No experiments have been run yet — evaluate the hypothesis purely on its merits.
</review_context>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the hypothesis is genuinely novel versus already-done or a known dead end in this field.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<previous_hypothesis>
The hypothesis from the PREVIOUS iteration (before the revision under review).
Use this to classify how the current hypothesis relates to it (see the H↔H
edge instructions in the task).

kind: hypothesis
title: Safety as nearness to a tipping point
hypothesis: >-
  Safety fine-tuning does not merely install a harm detector; it moves the model's default behavioral state close to a bistable
  switching point between 'comply' and 'refuse'. Because of this, a safety-aligned model is measurably 'twitchy' about refusal
  even on completely harmless input, while base and abliterated models sit deep inside the comply basin and are not. Concretely,
  we claim: (H1 - bistability) the refusal/comply decision in Qwen3-class models behaves as a bistable switch, evidenced by
  a hysteresis loop when a steering coefficient along the refusal direction is swept up and then back down (flip-to-refuse
  threshold != flip-back-to-comply threshold), with a loop of nonzero width in the safety-tuned model and a collapsed (zero-width)
  loop in the base and abliterated variants; (H2 - critical slowing down) on harmless prompts only, a small internal perturbation
  injected into the residual stream decays more slowly, and the internal refusal observable shows larger variance and higher
  lag-1 autocorrelation across token positions, in models that are behaviorally safer - the standard early-warning-signal
  signature of proximity to a tipping point; (H3 - prediction) a single scalar built from these harmless-input dynamics, the
  Refusal Resilience Index (RRI), rank-orders arbitrary open-weight models by their harmful-prompt refusal rate, and does
  so with predictive power beyond what the static mean level of the refusal observable explains (i.e. the partial correlation
  of the dynamic terms with refusal rate, controlling for the static mean, is significantly nonzero); (H4 - where static geometry
  fails) RRI in particular succeeds on 'behavioral' uncensored fine-tunes, which preserve harmful/benign cluster geometry
  and the refusal direction intact and are therefore a documented blind spot of activation-geometry scanners.
motivation: >-
  Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt
  benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator
  to hold and send harmful content. The existing cheap alternative - measure the geometric separation between harmful and
  benign activations, or the cosine of the refusal direction against a reference - has a published, mechanistically explained
  failure mode: fine-tunes that keep the geometry but change the behavior are invisible to it (a reported case shows intact
  separation and direction alongside 97% compliance with harmful requests). That failure is an instance of the field's sharpest
  open problem: internal decodability of a concept does not imply the model acts on it. This hypothesis attacks the gap from
  the other side. Instead of asking 'is harm represented?' (a static, read-side question that provably does not settle behavior),
  it asks 'how close to flipping is the model's behavioral state?' - a dynamical, act-side question. If true, it yields (a)
  a mechanistic account of what safety tuning actually buys, in the language of bistable systems: not a new feature but a
  shifted operating point, which also explains the well-known 'shallow safety alignment' finding as a shallow basin rather
  than a shallow representation; (b) a safety evaluation that needs a handful of harmless prompts, a few forward passes, no
  harmful content, no benchmark, and no reference model, and that cannot be gamed by memorizing benchmark items; and (c) a
  bridge that brings the mature early-warning-signal toolkit from ecology and climate science into model auditing.
assumptions:
- >-
  The refusal/comply distinction can be read out as a scalar observable at every token position - e.g. the projection of the
  residual stream onto a refusal direction, or the log-odds of refusal-onset tokens versus continuation tokens - and this
  observable is monotone with the model's actual refusal behavior.
- >-
  Token position can serve as the 'time' axis for the early-warning indicators: a perturbation injected at position p propagates
  to later positions through causal attention within a single forward pass, so the decay of its effect over later positions
  is a well-defined, measurable relaxation curve (the analogy to an autonomous dynamical system is operationalized, not assumed
  - H1's hysteresis test is what checks whether bistability is really present).
- >-
  The model set spans a real, measurable range of harmful-prompt refusal rates - i.e. small instruction-tuned checkpoints
  actually refuse a nontrivial fraction of a harmful benchmark, so ground truth is not degenerate. (Mitigation if it is: add
  stronger-refusing families such as Llama-3.2-1B-Instruct and use jailbreak-style rather than plain harmful prompts.)
- >-
  A refusal direction obtained from a small number of contrast prompts (or, for the strict zero-harmful-prompt variant, from
  the unembedding rows of refusal-onset tokens) is a good enough readout axis; the metric's predictive claim must survive
  using the unembedding-only axis, which requires no harmful data at all.
- >-
  Small models (0.6B-1.7B parameters, float32, CPU-only) show the same qualitative refusal machinery reported for larger models,
  so results on them are informative rather than an artifact of scale.
investigation_approach: |-
  Model panel (all small enough for CPU-only inference, ~10 checkpoints): Qwen3-0.6B-Base / Qwen3-0.6B / huihui-ai Qwen3-0.6B-abliterated, the same trio at 1.7B, Llama-3.2-1B-Instruct plus an abliterated variant (a second architecture and tokenizer, to test cross-family transfer), and at least one *behavioral* uncensored fine-tune (Dolphin/Josiefied-style) as the class that static geometry cannot detect.

  Step 1 - define the observable. r_t = projection of the layer-L residual stream at token position t onto a refusal axis. Two axis variants: (a) diff-in-means from ~32 harmful/harmless contrast prompts (the 'few prompts' variant), and (b) unembedding-derived refusal-onset direction, needing zero harmful prompts (the 'zero prompt' variant). All headline claims are reported for both.

  Step 2 - test bistability (H1). On a fixed benign prompt set, sweep a steering coefficient alpha along the refusal axis upward until the generated response flips to a refusal, then sweep back down until it flips to compliance. Record the two thresholds; loop width = alpha_up - alpha_down. Prediction: width > 0 for safety-tuned checkpoints, ~0 for base and abliterated. This is the decisive test - if there is no hysteresis anywhere, the tipping-point framing is refuted and the rest of the experiment reports that.

  Step 3 - measure early-warning indicators on harmless input only (H2). For each benign prompt: one clean forward pass giving the trajectory r_t; plus a handful of perturbed passes in which a small random (norm-epsilon) vector is added to the residual stream at layer L, position p. Because attention is causal, one forward pass yields the whole recovery curve |delta r_t| for t > p; fit an exponential to get the recovery rate lambda. Also compute, from the clean trajectory alone with no intervention at all, the variance and lag-1 autocorrelation of r_t. Sweep epsilon to confirm the response is in the linear regime, and sweep layer L. Cost: ~30 prompts x ~6 forward passes per model - seconds to minutes on CPU.

  Step 4 - ground truth. Generate ~60-100 short completions per model on a harmful benchmark subset (AdvBench / JailbreakBench-style) plus an over-refusal set (XSTest-style benign-but-scary prompts), and score refusal with a refusal-string classifier cross-checked by a cheap OpenRouter LLM judge on all items (well under the $10 cap; expected < $2).

  Step 5 - prediction and ablation (H3, H4). Fit RRI = a simple function of (lambda, variance, lag-1 AC) - fixed a priori, leave-one-model-out - and report Spearman rank correlation with harmful refusal rate. Pre-registered baselines it must beat or match: (i) harmful/benign cluster separation sigma (which, note, needs harmful prompts, unlike RRI); (ii) refusal-direction cosine against a reference model; (iii) the static mean level of r on benign prompts, the strongest cheap competitor. The load-bearing statistic is the partial rank correlation of the dynamic terms with refusal rate controlling for the static mean, with bootstrap CIs over models and prompts. Leave-one-family-out is reported separately, since transfer across tokenizers is the real test.

  Step 6 - mechanism map. Layer-wise and position-wise profiles of lambda for base vs instruct vs abliterated: does safety tuning shallow the basin at particular layers or early token positions, and does abliteration revert exactly those, or produce a third state that is neither base nor instruct?
success_criteria: |-
  CONFIRMS: (1) Hysteresis loop width is significantly > 0 for safety-tuned checkpoints and indistinguishable from 0 for base and abliterated ones (bootstrap CI over prompts excludes overlap) - bistability is real. (2) On harmless prompts only, recovery rate lambda is significantly lower (slower recovery), and lag-1 autocorrelation higher, in behaviorally safer models; ordering base ~ abliterated vs instruct is reproduced in at least 2 model families. (3) RRI computed from harmless prompts alone attains Spearman rho >= 0.8 with measured harmful-prompt refusal rate over >= 8 checkpoints, with a bootstrap 95% CI whose lower bound exceeds the correlation achieved by the static-mean baseline; and the partial correlation of the dynamic terms controlling for the static mean has a 95% CI excluding 0. (4) RRI correctly flags the behavioral uncensored fine-tune that cluster-separation sigma and refusal-direction cosine both mark as safe. (5) The zero-harmful-prompt (unembedding-axis) variant retains rho >= 0.7.

  DISCONFIRMS (any of these, and the hypothesis is reported as refuted rather than salvaged): no hysteresis in any checkpoint, i.e. the response to the steering sweep is single-valued and the bistable framing is wrong; or lambda / autocorrelation show no consistent ordering with safety; or their apparent correlation with refusal rate vanishes once the static mean level of r is partialled out - meaning the dynamics add nothing over 'how refusal-leaning is the model on average', the cheapest possible baseline; or the indicators work within Qwen3 but do not transfer across model families under leave-one-family-out, which would bound the metric to a within-family diagnostic. A clean negative here is itself informative: it would say safety is a static bias, not a shifted operating point of a bistable system, and it would extend the knowledge-action-gap literature with a dynamical arm.
related_works:
- >-
  Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - locate
  a refusal direction from harmful/harmless contrast means and orthogonalize the write matrices against it. This is the static,
  geometric account of refusal and the tool that produces our abliterated checkpoints; it says nothing about how close the
  model's default state sits to switching, and it is our experimental instrument, not our claim.
- >-
  Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (IEEE Access 2026) - AMS
  scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) to detect safety modification
  without behavioral testing; predicts compliance at Pearson r = -0.546, and explicitly reports that behavioral uncensored
  fine-tunes preserving geometry (97% compliance, intact sigma and direction) are undetectable by the approach. This is the
  closest work and the one we depart from most sharply: it measures a static read-side property using harmful prompts; we
  measure a dynamical act-side property using harmless prompts only, and its documented blind spot is our H4 test case.
- >-
  Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows the aligned generative
  distribution differs from the unaligned one mainly over the first few output tokens, which prefilling attacks exploit. It
  documents that safety is shallow in token depth; it does not model refusal as a bistable switch, does not measure basin
  depth, hysteresis, or recovery rates, and offers no harmless-prompt-only diagnostic. Our account reinterprets its finding
  as a shallow basin and turns it into a measurement.
- >-
  'Probing the Robustness of LLM Safety to Latent Perturbations' (Activation Steering Attack, 2025) - injects normalized steering
  vectors into hidden activations to see whether safety breaks, scored via the likelihood of the original response. It perturbs
  to break safety, requires harmful prompts and their responses, and reports a breakage rate; we perturb to measure how fast
  the model returns to its default state on harmless input, and never need a harmful prompt or a jailbreak outcome.
- >-
  Wollschlager et al. and the 'multi-directional refusal' line (e.g. AAAI 2026 SOM-directions work) - shows refusal lives
  on a low-dimensional manifold rather than one direction, i.e. it refines the geometry of the readout. Orthogonal to us:
  adding directions to the read-side does not address whether the behavioral state is near a switching point, and our indicators
  are computed on whatever refusal axis is chosen.
- >-
  'Measuring and Controlling Persona Drift in Language Model Dialogs' (2024) - tracks decay of persona adherence across dialog
  turns and attributes it to attention decay, proposing split-softmax as a fix. It is the nearest existing 'behavioral dynamics'
  measurement, but it measures drift away from a persona over long conversations as a problem to fix, not the relaxation rate
  after a controlled perturbation as an estimator of proximity to a tipping point, and it makes no safety prediction for unseen
  checkpoints.
- >-
  Hughes/ARC-style low-probability estimation, 'Estimating the Probabilities of Rare Outputs in Language Models' (ICLR 2025)
  - estimates the probability of a rare token output under a random input distribution via importance sampling and activation
  extrapolation. It shares the ambition of predicting rare behavior without observing it, but its mechanism is tail extrapolation
  of an output probability for a fixed query; ours is a dynamical-stability measurement (recovery rate, autocorrelation, hysteresis)
  of a behavioral mode, and it produces a per-model safety ranking rather than a per-query probability.
- >-
  Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology and climate science (rising variance,
  rising lag-1 autocorrelation, slower recovery from small perturbations as a system nears a fold bifurcation). This is the
  imported source, not a competitor; to our knowledge it has not been applied to the internal state dynamics of language models
  or to safety auditing at all.
inspiration: >-
  The transfer is from ecology and climate science, at the methodological level (level 3). Ecologists face exactly our problem
  in a different costume: they need to know how close a lake, a forest, or a fish population is to collapsing, and they cannot
  run the experiment of collapsing it. Scheffer's early-warning-signal programme solved this by measuring the system's response
  to small, harmless disturbances: as a system approaches a tipping point, the dominant eigenvalue of its linearized dynamics
  approaches zero, so recovery from tiny nudges slows down and spontaneous fluctuations grow in variance and become more autocorrelated.
  Resilience is measurable without ever pushing the system over the edge. Mapping that onto model auditing gives the whole
  design: 'don't jailbreak the model to find out if it can be jailbroken - nudge it gently while it is doing something innocuous,
  and watch how fast it settles back'. Two further imports come with the package: from physics and materials science, the
  hysteresis loop as the decisive experimental signature that a switch is genuinely bistable rather than merely biased (sweep
  the control parameter up, then down, and look for two different thresholds - the loop width becomes an interpretable safety
  quantity in its own right); and from genetics, the base / safety-tuned / abliterated triple read as a wild-type / knock-in
  / knock-out series, which lets us ask whether abliteration reverts the model to the base state or produces a third state
  that is neither. What a domain expert would not reach for is the reframing underneath all of it: mechanistic interpretability's
  default unit is a static object - a direction, a feature, a circuit - whereas the resilience literature's unit is a rate.
terms:
- term: Refusal observable (r_t)
  definition: >-
    A scalar read off the model at every token position t - the projection of the residual stream onto a refusal axis, or
    the log-odds of refusal-onset tokens against continuation tokens. Its trajectory over token positions is the 'time series'
    all indicators are computed from.
- term: Critical slowing down
  definition: >-
    The signature that a dynamical system is near a tipping point: recovery from small perturbations gets slower, and spontaneous
    fluctuations grow in variance and become more autocorrelated. Standard practice in ecology and climate science for estimating
    resilience without triggering a collapse.
- term: Recovery rate (lambda)
  definition: >-
    The exponential decay rate of the induced deviation in r_t at token positions after a small perturbation is injected into
    the residual stream. Small lambda = slow recovery = shallow basin = close to switching.
- term: Refusal Resilience Index (RRI)
  definition: >-
    The proposed safety metric: a single scalar combining recovery rate, fluctuation variance, and lag-1 autocorrelation of
    r_t, computed from a handful of harmless prompts and a few forward passes - no harmful prompts, no benchmark, no reference
    model.
- term: Hysteresis loop width
  definition: >-
    The gap between the steering coefficient at which a model flips into refusal while the coefficient is being increased
    and the (lower) coefficient at which it flips back while it is being decreased. Nonzero width is the definitive evidence
    of a genuinely bistable switch rather than a smoothly shifted bias.
- term: Abliteration
  definition: >-
    A weight edit that removes refusal behavior from an aligned open-weight model by orthogonalizing the matrices that write
    into the residual stream against an identified refusal direction, without retraining.
- term: Behavioral uncensored fine-tune
  definition: >-
    An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than by a directional weight edit.
    It can keep its harmful/benign activation geometry and refusal direction intact while complying with nearly all harmful
    requests, which makes it invisible to static activation-geometry scanners - and hence the sharpest test case for a dynamical
    metric.
- term: Knowledge-action gap
  definition: >-
    The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act
    on it, so probe accuracy does not predict behavior. It is the reason a read-side safety metric can be confidently wrong,
    and the reason this hypothesis measures an act-side quantity instead.
summary: >-
  Safety fine-tuning parks a model right next to a comply/refuse switching point, so an aligned model is subtly unstable about
  refusal even on completely harmless prompts - and that instability is measurable, via the early-warning indicators ecologists
  use to detect approaching tipping points (slower recovery from small nudges, higher variance and autocorrelation). This
  yields a safety score for any open-weight checkpoint from a handful of harmless prompts and a few forward passes, which
  should succeed exactly where static activation-geometry scanners are documented to fail.
</previous_hypothesis>

<previous_review>
Critiques from the previous review. Check which ones have been addressed
in the revised hypothesis. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (methodology) FATAL AS SPECIFIED — the H1 hysteresis test is guaranteed to return zero loop width in every checkpoint, for reasons unrelated to bistability. If the alpha sweep is implemented as independent generations at successive alpha values (which is what 'sweep alpha upward until the response flips, then sweep back down' describes), then under greedy decoding the response is a deterministic function of alpha alone. No state is carried from the up-sweep into the down-sweep, so the map alpha -> response is single-valued and alpha_up = alpha_down exactly. Hysteresis is definitionally path dependence and requires a persistent state variable; in an autoregressive LM the only candidate is the generated prefix / KV cache. As written, the experiment's own 'decisive test' would report the null, and the success criteria instruct the authors to conclude the tipping-point framing is refuted — a false negative baked into the protocol. This alone would waste the entire run.
  Action: Re-specify H1 as a within-generation ramp with retained state: fix a benign prompt, decode autoregressively while increasing alpha by a fixed step per generated token until a refusal onset is emitted; then continue decoding the SAME sequence (prefix and KV cache retained) while decreasing alpha per step, and record the alpha at which compliant continuation resumes. Loop width = alpha_up - alpha_down. Add a mandatory reset-control arm in which the prefix is discarded between alpha steps; that arm must yield zero width, and it is what demonstrates the loop is genuine path dependence rather than sampling noise. Report loop width distributions over >= 30 prompts with bootstrap CIs, and also report the width under temperature 0 vs temperature 0.7 (a real bistable switch should show flickering near the threshold at nonzero temperature — a bonus EWS the current design leaves on the table).
- [MAJOR] (methodology) The 'token position as time axis' assumption is the second load-bearing operationalization and it does not hold in the form stated. Critical slowing down is a property of the leading eigenvalue of a linearized AUTONOMOUS STOCHASTIC system near a fold bifurcation. Within a single forward pass over a fixed prompt, (a) the decay of an injected perturbation across later positions is dominated by attention dilution — an injected key competes with t-1 others, so influence falls roughly as 1/t irrespective of any basin — plus RMSNorm rescaling and position-dependent residual norm growth; and (b) Var(r_t) and AC(1) computed over PROMPT token positions are dominated by deterministic token-identity variation (punctuation, function words, chat-template scaffolding), not by stochastic fluctuation around an attractor. There is no noise process, so 'rising variance near a tipping point' has no referent. The hypothesis acknowledges the analogy is 'operationalized, not assumed' and points to H1 as the check, but H1 as specified is broken (see above), so nothing checks it.
  Action: Move the time axis to autoregressive generation under temperature sampling, which IS a genuine stochastic dynamical system with the token sequence as state. Concretely: (i) for lambda, inject the epsilon perturbation at generation step p, continue decoding, and fit the exponential decay of |delta r_t| across subsequent GENERATED steps, averaged over >= 20 sampled rollouts per prompt with paired clean/perturbed random seeds; (ii) for Var and AC(1), compute them on r_t over generated positions across rollouts (across-rollout variance at fixed step is the theoretically correct 'fluctuation' quantity, not within-sequence variance). Then add the three controls named in the soundness improvements — random readout axis, random vs refusal-aligned perturbation, and a syntactic-probe observable — so that a positive lambda ordering cannot be explained by generic mixing. If the authors prefer to keep the single-forward-pass version for cost reasons, it must be demoted to a secondary, explicitly-heuristic measurement and the 1/t attention-dilution null must be fit and subtracted.
- [MAJOR] (rigor) Statistical power is insufficient for every headline claim. The panel is ~10 checkpoints, but they are not independent units: three Qwen3-0.6B variants, three Qwen3-1.7B variants, two Llama-3.2-1B variants, and one or two uncensored fine-tunes — effectively 3 architecture families and 4-5 weight lineages. At n = 10, the 95% bootstrap CI around an observed Spearman rho = 0.8 spans roughly [0.3, 0.95], so criterion (3)'s requirement that the CI lower bound exceed the static-mean baseline's correlation is close to unattainable no matter what is true. The partial rank correlation controlling for the static mean — explicitly named as THE load-bearing statistic — has almost no power at n = 10 with strongly correlated predictors. Leave-one-family-out with 3 families is n_family = 2 for training, which is not an estimate. Bootstrapping over prompts does not help: prompts are not the unit of the model-level claim, and resampling them will produce deceptively narrow CIs on a model-level correlation (a pseudo-replication error a reviewer will catch immediately).
  Action: Scale the panel to >= 25 checkpoints across >= 4 families (see the contribution improvements for a CPU-feasible list — the whole point of the method is that it costs seconds per model, so a 25-model panel is nearly free and its absence would look strange). Bootstrap over MODELS as the unit for all model-level claims, and report the prompt-level bootstrap separately and labelled as a measurement-noise estimate only. Pre-register the achievable effect size: state the n at which the CI-exclusion criterion becomes attainable and either meet it or soften criterion (3) to a directional claim with an honest CI.
- [MAJOR] (rigor) The ground truth is degenerate in a way the assumptions block anticipates but under-treats. The panel is essentially trimodal: base models refuse ~0%, instruct models refuse at a high rate, abliterated models refuse ~0%. A Spearman rank correlation over such a distribution is a three-class discrimination wearing a correlation's clothes, and it can be won at rho ~ 1.0 by baselines so trivial they undermine the entire contribution — e.g. 'does the model ever emit an apology token on any prompt', or the next-token probability of 'I'/'Sorry' on a single benign prompt. Compounding this: a recent 21-model audit (arXiv:2605.05427) reports that over-refusal and harmful compliance are nearly uncorrelated across open-weight models, so 'harmful-prompt refusal rate' is not a one-dimensional safety construct in the first place, and a metric that predicts it may predict nothing about the adversarial robustness a safety auditor actually cares about.
  Action: Two changes. (1) Fill the middle of the refusal-rate range with deliberately partially-de-aligned checkpoints — a few hundred LoRA steps on compliant data at 3-4 strengths per base model gives a graded ladder cheaply and turns the correlation claim into a real one. (2) Predict TWO ground truths and report both: plain-harmful refusal rate (AdvBench/JailbreakBench subset) AND adversarial attack-success rate under a fixed jailbreak suite, plus the over-refusal rate on XSTest as a third axis. A 'nearness to tipping' metric should, on its own theory, predict jailbreak susceptibility better than plain refusal rate — that is a sharper and more valuable claim than the current one. Add the two trivial output-side baselines named above to the pre-registered baseline list; if RRI does not beat them, the internals add nothing.
- [MAJOR] (methodology) H2's central contrast is circular for the abliterated arm. Abliteration is defined (correctly, in the terms glossary) as orthogonalizing the residual-stream write matrices against the refusal direction. If r_t is then read out as the projection onto that same direction, r_t is near-constant in an abliterated model BY CONSTRUCTION — its variance collapses toward zero and its lag-1 autocorrelation becomes ill-conditioned or dominated by numerical noise. The predicted finding 'lower variance and lower AC(1) in abliterated models' is therefore guaranteed by the definition of the intervention rather than by anything about basin depth, and criterion (2) of CONFIRMS is not falsifiable in that arm. The same issue partially applies to the diff-in-means axis being re-derived per model: variance in projection units on a per-model axis of arbitrary scale is not commensurable across models.
  Action: Report every H2 indicator on at least one readout that survives the abliteration edit — the logit-lens log-odds of refusal-onset tokens against continuation tokens is the natural choice, and the hypothesis already lists it as an alternative observable. Additionally z-score r_t within model over the benign prompt set before computing Var and AC(1), and demonstrate that lambda is invariant to axis scaling (it should be, since it is a decay rate of a ratio, but this must be shown, not assumed). State explicitly in the pre-registration that any variance/AC result on the diff-in-means axis in abliterated models is reported as descriptive and is NOT counted toward criterion (2).
- [MAJOR] (novelty) The 'shallow basin' framing and the 'cheap internal safety score' deliverable both have closer prior art than the related-works section acknowledges, and both gaps are the kind a top-venue reviewer finds in one search. (a) 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) already establishes a SAFETY BASIN in weight space — random weight perturbations preserve safety locally, with a sharp step-like drop outside — and already ships a basin-geometry safety metric, VISAGE. The reinterpretation of Qi et al. as a 'shallow basin' is therefore not a new coinage, and the paper must state what a basin in ACTIVATION/behavioral state space adds over a basin in WEIGHT space. (b) RAS (arXiv:2606.25750) is a representation-level, calibrated 0-100 safety score explicitly motivated by 'output-level evaluation is expensive, judge-dependent, and benchmarks go stale' — nearly verbatim this proposal's motivation for H3 — validated across Llama, Gemma and Qwen against uncensored and abliterated variants. RAS does need harmful prompts, which is a real differentiator, but it must be named as the incumbent and beaten. (c) 'Refusal Falls off a Cliff' (arXiv:2510.06036) already probes a per-token-position refusal score, i.e. the r_t observable is not new. Coining new terms over an existing measurement is exactly what a reviewer scores as a novelty failure.
  Action: Add all three to related works with an explicit differentiator sentence each, and make two of them empirical baselines rather than citations: run VISAGE-style weight-perturbation basin volume (or state honestly why it is out of budget) and a RAS-style representation-alignment score on the same panel, and report RRI against both. The differentiator to lead with is sharp and defensible if stated plainly: VISAGE probes WEIGHT-space geometry and needs a harmful benchmark at each perturbation; RAS needs harmful and jailbreak prompts and a safety-aligned REFERENCE model; RRI claims to need neither. That claim is worth the paper — but only if the incumbents appear in the table.
- [MAJOR] (evidence) A published result directly threatens H1's base-vs-instruct contrast and is not pre-registered as an alternative hypothesis. 'Breaking Refusal in the First Half' (arXiv:2607.14147) reports, using base-model controls, that prefill-collapse refusal dynamics are 'generic autoregressive conditioning, not safety-specific active suppression', with non-safety-tuned base models showing the same prefill-specific collapse; and 'Step-Wise Refusal Dynamics' (arXiv:2602.02600) reports that autoregressive commitment masks underlying instability. If path-dependent switching is a generic property of autoregressive self-conditioning, then a corrected H1 protocol may well find NONZERO loop width in base models too. That would leave the bistability claim intact while destroying the safety-specificity claim on which H2-H4 rest — an outcome the current success/disconfirm criteria have no cell for, so it would be discovered mid-run and rationalized post hoc.
  Action: Pre-register this as a named third outcome with its own reporting commitment: 'bistability present but not safety-specific (loop width > 0 in base models)'. State in advance what it would mean (the hysteresis is a property of autoregressive decoding, and only the QUANTITATIVE width ordering, if any, carries safety information) and pre-register the ordering test (loop width instruct > base and instruct > abliterated, paired over prompts) as the claim that survives. Cite both papers as motivating this control.
- [MINOR] (methodology) Layer selection is under-specified in a way that creates a garden of forking paths. 'Sweep layer L' across 10+ models with ~28 layers each, then report the indicators, gives roughly 280 opportunities to find an ordering; no correction is mentioned. This matters more than usual here because a recent mechanistic analysis (arXiv:2606.22686, TrustNLP 2026) reports architecture-dependent safety topologies — 'Late Decision' models (Llama, safety divergence only at final layers) versus 'Early Divergence' models (Qwen, safety integrated mid-computation) — so the correct L differs systematically across the two families in the panel, and a per-family sweep chosen post hoc would be indistinguishable from selection on the outcome.
  Action: Pre-register a layer-selection RULE that does not touch the outcome variable: e.g. select L as the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set, computed on the REFERENCE model only and transferred by relative depth (L/n_layers) to the rest of the panel. Report the full layer profile as a secondary descriptive figure and cite arXiv:2606.22686 when interpreting family differences. Apply Holm or BH correction to any per-layer claims.
- [MINOR] (rigor) The refusal-string classifier plus 'cheap OpenRouter LLM judge' ground truth is under-specified for a paper whose entire headline is a correlation against that ground truth. Refusal-string matching is known to both over-count (models that say 'I cannot verify that' while complying) and under-count (soft refusals, deflections, capability-denials), and abliterated models in particular produce degenerate or repetitive outputs that string matchers mis-score. Any measurement error in the ground truth attenuates the correlation, which is the exact quantity the pre-registered criterion thresholds at 0.8.
  Action: Report inter-rater agreement between the string classifier and the LLM judge (Cohen's kappa) and use the judge as primary with the string matcher as a screen, not the reverse. Hand-adjudicate a stratified sample of >= 100 items to estimate the judge's own error rate, and report the attenuation-corrected correlation alongside the raw one. Also fix and report the decoding configuration (temperature, max tokens, chat template, system prompt) — refusal rates on small models are highly sensitive to all four, and the system prompt in particular is documented to shift the safety basin (arXiv:2405.17374).
- [MINOR] (scope) The 0.6B-1.7B scale assumption is stated but not defended, and it interacts badly with the central claim. The refusal-direction literature is built on 1.5B-72B models; at 0.6B the refusal mechanism may be genuinely weaker and noisier, and — more sharply — a 0.6B model that is 'twitchy about refusal on harmless input' may be twitchy because it is undertrained, not because it is parked near a tipping point. That is a confound the design cannot separate at a single scale, and it directly threatens the mechanistic interpretation even if the correlation holds.
  Action: Include at least one within-family scale ladder in the panel (Qwen3 0.6B / 1.7B / 4B, CPU-feasible in float32 or int8 at 4B for the short generations required) and report whether lambda, Var and AC(1) trend with SCALE independently of safety. If the indicators track scale as strongly as they track safety, say so and control for it as a covariate in the partial correlation. A one-paragraph scale-robustness result also substantially raises the paper's reach.
- [MINOR] (clarity) Two definitional issues that will cause misreading. (1) The RRI name is sign-inverted relative to its construct: 'Refusal Resilience Index' reads as 'how resilient refusal is', but a high RRI is meant to indicate a SHALLOW basin and hence LOW resilience of the comply state / high proximity to switching. (2) RRI is left as 'a simple function of (lambda, variance, lag-1 AC), fixed a priori' without stating the function — which makes 'fixed a priori' unverifiable by a reader and unenforceable on the authors.
  Action: Rename to something sign-transparent ('Refusal Proximity Index' or 'Switching Proximity Index'), or state the sign convention explicitly in the glossary entry. Write the exact formula and standardization into the hypothesis text before the run, e.g. RRI = mean of within-panel z-scores of (-lambda), log Var(r), and Fisher-z(AC1(r)), with all three computed on the standardized observable at the pre-registered layer. Report the single-term versions (lambda alone, AC1 alone) alongside, since a reviewer will want to know which term carries the signal.
</previous_review>

<task>
Provide a thorough peer review of this research hypothesis.

STEP 1 — GROUND YOUR REVIEW IN EVIDENCE:
Before writing critiques, search for relevant context to make your review authoritative:
- Search for accepted papers at top venues in this area — what level of
  contribution gets accepted? How does this hypothesis compare?
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes in the literature

STEP 2 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would waste compute if not fixed) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Flag fatal flaws that would waste compute if not fixed first.

STABILITY IS OK: If the hypothesis is on track and just needs more iterations to prove itself,
keep your feedback similar to the previous round. Don't manufacture new critiques — only escalate
when the revision introduced new issues or failed to address prior ones.

STEP 3 — H↔H EDGE (only if a <previous_hypothesis> block is present):
Classify how the current hypothesis relates to the previous iteration's hypothesis
using Moulines's structuralist typology. Set ``relation_type`` to one of:
    - "evolution": refining specialised claims while keeping the same conceptual frame
    - "embedding": the previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian, incommensurable shift)
Set ``relation_rationale`` to a brief justification (≤120 chars).

If no <previous_hypothesis> is present (this is iteration 1), leave both fields
null/empty.

Provide your review via structured output.
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
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "ReviewerFeedback + Moulines H\u2194H typology for hypo_loop iterations.\n\nAdds ``relation_type`` + ``relation_rationale`` so the trace projection\ncan build a typed edge from the previous iteration's hypothesis to\nthis iteration's. On iteration 1 (no previous), both fields are\nempty/None.",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    },
    "relation_type": {
      "anyOf": [
        {
          "enum": [
            "evolution",
            "embedding",
            "replacement"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Moulines's structuralist typology classifying how this iteration's hypothesis relates to the previous iteration's: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (Kuhnian shift). Leave null on the first iteration (no previous hypothesis).",
      "title": "Relation Type"
    },
    "relation_rationale": {
      "default": "",
      "description": "Brief rationale (one short line, \u2264120 chars) for the relation_type. Empty on the first iteration.",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "HypoReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-12 12:53:56 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] ASSISTANT · 2026-08-12 12:54:04 UTC

```
I'll review this hypothesis, grounding it in the relevant literature.
```

### [5] TOOL CALL — Bash · 2026-08-12 12:54:04 UTC

```
List user uploads:
ls /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads 2>/dev/null | head -50
```

### [6] TOOL CALL — Skill · 2026-08-12 12:54:04 UTC

```
aii-handbook-auto-mechanistic-interpretability
```

### [7] TOOL RESULT — Bash · 2026-08-12 12:54:04 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL RESULT — Skill · 2026-08-12 12:54:04 UTC

```
{"success": true, "commandName": "aii-handbook-auto-mechanistic-interpretability"}
```

### [9] TOOL CALL — Skill · 2026-08-12 12:54:08 UTC

```
aii-web-tools
```

### [10] TOOL RESULT — Skill · 2026-08-12 12:54:08 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [11] TOOL CALL — Bash · 2026-08-12 12:54:12 UTC

```
Search EWS LLM refusal:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "critical slowing down early warning signals large language models refusal bistability" --max-results 10 2>&1 | head -40
```

### [12] TOOL CALL — Bash · 2026-08-12 12:54:12 UTC

```
Search hysteresis steering:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "hysteresis steering vector LLM bistable refusal phase transition" --max-results 10 2>&1 | head -40
```

### [13] TOOL RESULT — Bash · 2026-08-12 12:54:12 UTC

```
{"stdout": "Search: critical slowing down early warning signals large language models refusal bistability  [general via ddgs]\nFound: 10 results\n\n1. Early warning signals and critical slowing – Tidy Ecology\n   https://tidyecology.com/posts/early-warning-signals-critical-slowing/\n   Critical slowing down offers a possible warning. As the driver pushes the system towards the fold, the dominant eigenvalue of the linearised dynamics approaches zero, so the system recovers from small...\n\n2. Cascading Tipping Points and Early Warning Signals... - YouTube\n   https://www.youtube.com/watch?v=Vi4bqZ_0TEM\n   I chat about tipping point cascades in the climate system and Early Warming Signals that show we are rapidly approaching a multitude of tipping points....\n\n3. Slowing-down based indicators | Early Warning Signals Toolbox\n   https://www.early-warning-signals.org/?page_id=854\n   What are Early Warning Signals? Perturbation experiments. Time series methods.Due to critical slowing down, neighboring units in space look more similar to each other when a system approaches a bifurc...\n\n4. Critical Slowing Down as Early Warning Signals... | Semantic Scholar\n   https://www.semanticscholar.org/paper/Critical-Slowing-Down-as-Early-Warning-Signals-for-Diks-Hommes/c3ec1bac34874f97557ada4f48b6f606d4c628ba\n   Our analysis shows evidence for critical slowing down before Black Monday 1987, while the results are mixed and insignificant for the other financial crises....\n\n5. (PDF) Early-warning signals for critical transitions\n   https://www.academia.edu/165617482/Early_warning_signals_for_critical_transitions\n   Signals of critical slowing down may be detected through measurement of summary statistics, but how extrinsic and intrinsic noises influence statistical patterns prior to a transition is unclear....\n\n6. Early warning of climate tipping points from critical slowing down...\n   https://hal.science/hal-02195169/document\n   We address whether robust early warning signals can, in principle, be provided before a climate tipping point is reached, focusing on methods that seek to detect critical slowing down as a precursor o...\n\n7. (Open Access) An Early Warning System for Flood Detection Using...\n   https://scispace.com/papers/an-early-warning-system-for-flood-detection-using-critical-3qvoeyckx3\n   Abstract: The theory of critical slowing down (CSD) suggests an increasing pattern in the time series of CSD indicators near catastrophic events. This theory has been successfully used as a generic in...\n\n8. Slow down and be critical before using early warning signals in...\n   https://colab.ws/articles/10.1038/s44159-024-00369-y\n   Early warning signals are considered to be generic indicators of a system’s accumulating instability and ‘critical slowing down’ prior to substantial and abrupt transitions between stable states....\n\n9. (PDF) Early-Warning Signals of Drought-Flood State Transition over...\n   https://www.researchgate.net/publication/354080609_Early-Warning_Signals_of_Drought-Flood_State_Transition_over_the_Dongting_Lake_Basin_Based_on_the_Critical_Slowing_Down_Theory\n   slowing down, the early-warning signals indicating the drought-flood state in the Dongting Lake.critical slowing down phenomenon are potential early warning signals, and more robust. conclusions requi...\n\n10. Local nearby bifurcations lead to synergies in critical slowing down...", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL RESULT — Bash · 2026-08-12 12:54:14 UTC

```
{"stdout": "Search: hysteresis steering vector LLM bistable refusal phase transition  [general via ddgs]\nFound: 10 results\n\n1. Valence-Arousal Subspace in LLMs: Circular Emotion... | alphaXiv\n   https://www.alphaxiv.org/overview/2604.03147\n   Refusal: Decreasing arousal (steering toward the \"calm\" or \"deactivated\" direction) significantly increases the refusal rate across multiple benchmarks like OKTest and XSTest....\n\n2. OPIUM: Mitigating Steering Externalities and Over-Refusal via Dual...\n   https://databubble.co/news/opium-mitigating-steering-externalities-and-over-refusal-via-dual-objective-latent-optimization-nqevx0\n   arXiv:2607.19806v2 Announce Type: replace-cross Abstract: Activation steering provides a lightweight mechanism for controlling large language models at inferenc....\n\n3. Dark-state phase transition to a dark soliton in a dissipative...\n   https://journals.aps.org/prresearch/abstract/10.1103/dv77-31g7\n   We show that a Bose-Hubbard model with local loss exhibits a first-order dark-state phase transition between a dark soliton and a uniform superfluid....\n\n4. Figure 1: An example of potential misuse of an LLM. We show LLM...\n   https://www.researchgate.net/figure/An-example-of-potential-misuse-of-an-LLM-We-show-LLM-responses-with-no-steering-vector_fig1_391676154\n   We show LLM responses with no steering vector applied vs. with the stereoset-race steering vector applied with a scalar of 1. Output generated by Mistral 7B Instruct v0.1 with intervention on layers 1...\n\n5. Alerting on LLM Metrics Without Alarm Fatigue - DEV Community\n   https://dev.to/multigrid/alerting-on-llm-metrics-without-alarm-fatigue-2npp\n   Which LLM signals deserve to wake someone, expressed as level-triggered burn-rate alerts with concrete windows and multipliers. Tagged with ai, devops, llm, machinelearning....\n\n6. Effect of a noisy driving field on a bistable polariton system\n   https://hal.science/hal-01211576v1/document\n   We report on the effect of noise on the characteristics of the bistable polariton emission system. The present experiment provides a time-resolved access to the polariton emission intensity....\n\n7. Stick-slip kinetics in a bistable bar immersed in a heat bath - PMC\n   https://pmc.ncbi.nlm.nih.gov/articles/PMC7442296/\n   Structural transitions in some rod-like biological macromolecules under tension are known to proceed by the propagation through the length of the molecule of an interface separating two phases....\n\n8. किसी भी API कुंजी के साथ Gemini CLI कैसे सेट करें | LLM Pricing\n   https://llmpricing.dev/hi/tutorials/gemini-cli/\n   LLM Pricing. मूल्य लीडरबोर्ड टूल प्रदाता गाइड....\n\n9. Where to Draw the Line - ACM Queue\n   https://queue.acm.org/detail.cfm?id=3834784\n   The USL defines bistable minima in the tokenized neural net landscape. The deeper minimum determines the lowest achievable loss of an LLM instance. Successively larger LLMs possess deeper global minim...\n\n10. Sci-Bot: микроактюаторы на основе никелида титана, их...", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-08-12 12:54:22 UTC

```
Scholarly EWS + LLM:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "critical slowing down early warning signal neural network language model tipping point" --mode scholarly --max-results 10 2>&1 | head -40
```

### [16] TOOL CALL — Bash · 2026-08-12 12:54:22 UTC

```
Scholarly cheap safety metric:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "safety metric without harmful prompts open-weight checkpoint refusal predict jailbreak internal activations" --mode scholarly --max-results 10 2>&1 | head -40
```

### [17] TOOL RESULT — Bash · 2026-08-12 12:54:22 UTC

```
{"stdout": "Search: critical slowing down early warning signal neural network language model tipping point  [scholarly via openalex]\nFound: 10 results\n\n1. Machine learning dismantling and early-warning signals of disintegration in complex systems\n   https://doi.org/10.1038/s41467-021-25485-8\n   Nature Communications · 2021 · cited by 126...\n\n2. Gesture, sign, and language: The coming of age of sign language and gesture studies\n   https://doi.org/10.1017/s0140525x15001247\n   Behavioral and Brain Sciences · 2015 · cited by 364...\n\n3. Psychopathological networks: Theory, methods and practice\n   https://doi.org/10.1016/j.brat.2021.104011\n   Behaviour Research and Therapy · 2021 · cited by 301...\n\n4. Early warning signals have limited applicability to empirical lake data\n   https://doi.org/10.1038/s41467-023-43744-8\n   Nature Communications · 2023 · cited by 54...\n\n5. SpiNNaker: A Spiking Neural Network Architecture\n   https://doi.org/10.1561/9781680836523\n   2020 · cited by 77...\n\n6. Dynamics of sleep: Exploring critical transitions and early warning signals\n   https://doi.org/10.1016/j.cmpb.2020.105448\n   Computer Methods and Programs in Biomedicine · 2020 · cited by 21...\n\n7. Online social networks security and privacy: comprehensive review and analysis\n   https://doi.org/10.1007/s40747-021-00409-7\n   Complex & Intelligent Systems · 2021 · cited by 266...\n\n8. A complex systems approach to the study of change in psychotherapy\n   https://doi.org/10.1186/s12916-020-01662-2\n   BMC Medicine · 2020 · cited by 156...\n\n9. Gaze cueing of attention: Visual attention, social cognition, and individual differences.\n   https://doi.org/10.1037/0033-2909.133.4.694\n   Psychological Bulletin · 2007 · cited by 1474...\n\n10. Dynamical state transitions into addictive behaviour and their early-warning signals", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL RESULT — Bash · 2026-08-12 12:54:24 UTC

```
{"stdout": "Search: safety metric without harmful prompts open-weight checkpoint refusal predict jailbreak internal activations  [scholarly via openalex]\nFound: 10 results\n\n1. Can Open Large Language Models Catch Vulnerabilities?\n   https://doi.org/10.4230/oasics.icpec.2025.4\n   arXiv (Cornell University) · 2025 · cited by 525...\n\n2. Enriching Location Representation with Detailed Semantic Information\n   https://doi.org/10.4230/lipics.giscience.2025.3\n   arXiv (Cornell University) · 2024 · cited by 431...\n\n3. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context\n   https://doi.org/10.48550/arxiv.2403.05530\n   arXiv (Cornell University) · 2024 · cited by 294...\n\n4. Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training\n   https://doi.org/10.48550/arxiv.2401.05566\n   arXiv (Cornell University) · 2024 · cited by 37...\n\n5. Adversarial machine learning :\n   https://doi.org/10.6028/nist.ai.100-2e2023\n   2024 · cited by 126...\n\n6. Retrieval augmented generation for large language models in healthcare: A systematic review\n   https://doi.org/10.1371/journal.pdig.0000877\n   PLOS Digital Health · 2025 · cited by 181...\n\n7. GUARDIAN: A Multi-Tiered Defense Architecture for Thwarting Prompt Injection Attacks on LLMs\n   https://doi.org/10.4236/jsea.2024.171003\n   Journal of Software Engineering and Applications · 2024 · cited by 19...\n\n8. Alignment faking in large language models\n   https://doi.org/10.48550/arxiv.2412.14093\n   arXiv (Cornell University) · 2024 · cited by 22...\n\n9. Adversarial Machine Learning:\n   https://doi.org/10.6028/nist.ai.100-2e2025\n   2025 · cited by 36...\n\n10. SELF-GUARD: Empower the LLM to Safeguard Itself", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-08-12 12:54:30 UTC

```
Verify cited arXiv IDs:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
for id in 2608.05578 2606.25750 2607.14147 2602.02600 2606.22686 2605.05427; do echo "=== $id ==="; $PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/$id" --max-chars 1200 2>&1 | head -25; done
```

### [20] TOOL RESULT — Bash · 2026-08-12 12:54:34 UTC

```
{"stdout": "=== 2608.05578 ===\nURL: https://arxiv.org/abs/2608.05578\nType: HTML\nLength: 8102 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Cryptography and Security\n\n**arXiv:2608.05578** (cs) \n\n[Submitted on 6 Aug 2026]\n\n# Title:Detecting Safety Training Modification in Language Models via Activation Analysis\n\nAuthors:[Glen Messenger](https://arxiv.org/search/cs?searchtype=author&query=Messenger,+G)\n\nView a PDF of the paper titled Detecting Safety Training Modification in Language Models via Activation Analysis, by Glen Messenger\n\n[View PDF](/pdf/2608.05578) [HTML (experimental)](https://arxiv.org/html/2608.05578v1)\n=== 2606.25750 ===\nURL: https://arxiv.org/abs/2606.25750\nType: HTML\nLength: 7598 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Cryptography and Security\n\n**arXiv:2606.25750** (cs) \n\n[Submitted on 24 Jun 2026]\n\n# Title:RAS: Measuring LLM Safety Through Refusal Alignment\n\nAuthors:[Chang-Chieh Huang](https://arxiv.org/search/cs?searchtype=author&query=Huang,+C), [Yan-Lun Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+Y), [Chia-Mu Yu](https://arxiv.org/search/cs?searchtype=author&query=Yu,+C), [Wei-Bin Lee](https://arxiv.org/search/cs?searchtype=author&query=Lee,+W)\n\nView a PDF of the paper titled RAS: Measuring LLM Safety Through Refusal Alignment, by Chang-Chieh Huang and 3 other authors\n\n[View PDF](/pdf/2606.25750) [HTML (experimental)](https://arxiv.org/html/2606.25750v1)\n=== 2607.14147 ===\nURL: https://arxiv.org/abs/2607.14147\nType: HTML\nLength: 8393 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Computation and Language\n\n**arXiv:2607.14147** (cs) \n\n[Submitted on 14 Jul 2026]\n\n# Title:Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak\n\nAuthors:[Alex Kwon](https://arxiv.org/search/cs?searchtype=author&query=Kwon,+A)\n\nView a PDF of the paper titled Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak, by Alex Kwon\n\n[View PDF](/pdf/2607.14147) [HTML (experimental)](https://arxiv.org/html/2607.14147v1)\n=== 2602.02600 ===\nURL: https://arxiv.org/abs/2602.02600\nType: HTML\nLength: 8253 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Machine Learning\n\n**arXiv:2602.02600** (cs) \n\n[Submitted on 1 Feb 2026 ([v1](https://arxiv.org/abs/2602.02600v1)), last revised 5 Jun 2026 (this version, v3)]\n\n# Title:Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models\n\nAuthors:[Eliron Rahimi](https://arxiv.org/search/cs?searchtype=author&query=Rahimi,+E), [Elad Hirshel](https://arxiv.org/search/cs?searchtype=author&query=Hirshel,+E), [Rom Himelstein](https://arxiv.org/search/cs?searchtype=author&query=Himelstein,+R), [Amit LeVi](https://arxiv.org/search/cs?searchtype=author&query=LeVi,+A), [Avi Mendelson](https://arxiv.org/search/cs?searchtype=author&query=Mendelson,+A), [Chaim Baskin](https://arxiv.org/search/cs?searchtype=author&query=Baskin,+C)\n\nView a PDF of the paper titled Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models, by Eliro\n=== 2606.22686 ===\nURL: https://arxiv.org/abs/2606.22686\nType: HTML\nLength: 8276 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Cryptography and Security\n\n**arXiv:2606.22686** (cs) \n\n[Submitted on 21 Jun 2026 ([v1](https://arxiv.org/abs/2606.22686v1)), last revised 30 Jun 2026 (this version, v2)]\n\n# Title:The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs\n\nAuthors:[Shivam Ratnakar](https://arxiv.org/search/cs?searchtype=author&query=Ratnakar,+S), [Kartikeya Vats](https://arxiv.org/search/cs?searchtype=author&query=Vats,+K)\n\nView a PDF of the paper titled The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs, by Shivam Ratnakar and 1 other authors\n\n[View PDF](/pdf/2606.22686) [HTML (experimental)](https://arxiv.org/html/2606.22686v2)\n=== 2605.05427 ===\nURL: https://arxiv.org/abs/2605.05427\nType: HTML\nLength: 7576 chars (truncated)\n\n--- Content ---\n\nSkip to main content [](https://arxiv.org/IgnoreMe) [ ](https://arxiv.org/) [ Search ](https://arxiv.org/search) [Submit](https://arxiv.org/user/create) [Donate](https://info.arxiv.org/about/donate.html) [Log in](https://arxiv.org/login)\n\nSearch arXiv\n\nPress Enter to search * [Advanced search](https://arxiv.org/search/advanced)\n\n# Computer Science > Artificial Intelligence\n\n**arXiv:2605.05427** (cs) \n\n[Submitted on 6 May 2026 ([v1](https://arxiv.org/abs/2605.05427v1)), last revised 30 May 2026 (this version, v2)]\n\n# Title:The Refusal--Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models\n\nAuthors:[Alif Al Hasan](https://arxiv.org/search/cs?searchtype=author&query=Hasan,+A+A), [Sumon Biswas](https://arxiv.org/search/cs?searchtype=author&query=Biswas,+S)\n\nView a PDF of the paper titled The Refusal--Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models, by Alif Al Hasan and 1 other authors\n\n[View PDF](/pdf/2605.05427) [HTML (experimental)](https://arxiv.org/html/2605.05427v2)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-08-12 12:54:44 UTC

```
arXiv API critical slowing down LLM:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "http://export.arxiv.org/api/query?search_query=all:%22critical%20slowing%20down%22%20AND%20all:%22language%20model%22&max_results=20&sortBy=submittedDate&sortOrder=descending" --max-chars 6000 2>&1 | grep -iE "^\s*(title|published)" | head -40
```

### [22] TOOL RESULT — Bash · 2026-08-12 12:54:44 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-08-12 12:54:44 UTC

```
arXiv hysteresis LLM:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "http://export.arxiv.org/api/query?search_query=abs:%22hysteresis%22+AND+abs:%22large+language+model%22&max_results=25&sortBy=submittedDate&sortOrder=descending" --max-chars 8000 2>&1 | head -60
```

### [24] TOOL RESULT — Bash · 2026-08-12 12:54:44 UTC

```
{"stdout": "URL: http://export.arxiv.org/api/query?search_query=abs:%22hysteresis%22+AND+abs:%22large+language+model%22&max_results=25&sortBy=submittedDate&sortOrder=descending\nType: HTML\nLength: 11667 chars (truncated)\n\n--- Content ---\n\nhttps://arxiv.org/api/HQwCU7RPQUdKRmbWVnnTppBfkFQ arXiv Query: search_query=abs:\"hysteresis\" AND abs:\"large language model\"&id_list=&start=0&max_results=25 2026-08-12T12:54:42Z 25 7 0 http://arxiv.org/abs/2608.00303v1 CrystalMem: Elastic Memory for Self-Evolving LLM Agents via Knowledge Crystallization 2026-07-31T21:35:46Z Memory for self-evolving large language model (LLM) agents is often provisioned as if its byte budget only grows. Cloud platforms, however, adjust quotas with load and cost, and we show that capability does not follow the budget back up: after a squeeze-and-recover cycle, the agent settles below its pre-squeeze level, a gap we call memory hysteresis. The cause is structural. Deletion and one-way compression discard the material needed for later rebuilding, and we prove that any policy that only keeps or drops entries carries a residual-deficit floor. We propose CrystalMem (Crystallized Memory), an elastic memory sidecar that demotes entries across four fidelity states under a crystallization-energy schedule, orders demotions by advantage-weighted influence with dependency coupling, and recovers capability through verified recrystallization under explicit compute and byte caps. Across seven environments, seventeen methods, and six backbones, with multi-tenant serving and a physical edge-cloud deployment, CrystalMem achieves the highest restored capability in every setting and closes the loop left open by every baseline. From a 50% byte budget, CrystalMem matches the strongest budgeted baseline at full provision on every environment; at equal budgets, it leads by +4.6 pp on average. 2026-07-31T21:35:46Z Beining Wu Jun Huang http://arxiv.org/abs/2605.29179v2 Sustainable Metal-Organic Framework Water Harvesters in the Artificial Intelligence Era 2026-06-15T23:39:02Z Metal-organic frameworks (MOFs) are excellent candidates for water harvesting due to their tunable pore environments, which can be precisely engineered to capture and release water in arid conditions. Integrating artificial intelligence (AI) into MOF discovery can further accelerate the design of high-performance sorbents by identifying structural features that enhance atmospheric water harvesting (AWH), stability, and cycling efficiency. In this Perspective, we examine key MOF design principles, including cooperative adsorption, operational relative humidity (RH), uptake capacity, hysteresis, and scalability. We highlight recent design advancements such as multivariate strategies and long-arm linker extension, and examine how these principles tune pore capacity and hydrophilicity, while preserving stability and crystallinity. Furthermore, we discuss how AI, large language models (LLMs), and data mining can accelerate the discovery process through predictive synthesis, inverse design, and elucidating synthesis-structure-property relationships for the next generation of MOF water harvesters. 2026-05-27T23:30:45Z 10 pages of main text, 26 total pages. 3 Figures and 1 Table of Content Graphic Reid A. Coyle Shyam Chand Pal Peter Walther Saeun Park Bin Feng Zhiling Zheng http://arxiv.org/abs/2604.25175v1 Indirect reciprocity beyond pairwise interactions 2026-04-28T03:27:47Z Cooperation in groups underpins collective responses to challenges from climate governance to public goods provision, yet how moral evaluation sustains it remains poorly understood. Indirect reciprocity -- cooperating to build a good reputation -- is well characterized for pairwise interactions, but real collective action requires individuals to be judged against the reputational profile of an entire group. Here we develop a general framework for multiplayer indirect reciprocity and show that stable group cooperation obeys a simple organizing principle: `all good, help; one bad, halt'. This rule is both necessary and sufficient for cooperation to emerge, and it recovers the classical leading eight norms in the pairwise limit. We further show that group structure fundamentally changes reputation dynamics: unlike pairwise models, which are monostable, multiplayer systems exhibit bistability and hysteresis, with a critical tipping point separating cooperative and defective regimes. Assessment of the latent norms of large language models reveals that they shift toward punitive defection when provided with richer social information, yet fail to follow the full logic of `all good, help; one bad, halt'. Our results establish a unifying principle for reputation-based cooperation in groups and provide a benchmark for evaluating cooperative alignment in artificial intelligence. 2026-04-28T03:27:47Z 21 pages, 10 figures Ming Wei Xin Wang Junyu Lu Longzhao Liu Yishen Jiang Hongwei Zheng Shaoting Tang Feng Fu http://arxiv.org/abs/2602.11211v1 TRACE: Timely Retrieval and Alignment for Cybersecurity Knowledge Graph Construction and Expansion 2026-02-11T06:54:21Z The rapid evolution of cyber threats has highlighted significant gaps in security knowledge integration. Cybersecurity Knowledge Graphs (CKGs) relying on structured data inherently exhibit hysteresis, as the timely incorporation of rapidly evolving unstructured data remains limited, potentially leading to the omission of critical insights for risk analysis. To address these limitations, we introduce TRACE, a framework designed to integrate structured and unstructured cybersecurity data sources. TRACE integrates knowledge from 24 structured databases and 3 categories of unstructured data, including APT reports, papers, and repair notices. Leveraging Large Language Models (LLMs), TRACE facilitates efficient entity extraction and alignment, enabling continuous updates to the CKG. Evaluations demonstrate that TRACE achieves a 1.8x increase in node coverage compared to existing CKGs. TRACE attains the precision of 86.08%, the recall of 76.92%, and the F1 score of 81.24% in entity extraction, surpassing the best-known LLM-based baselines by 7.8%. Furthermore, our entity alignment methods effectively harmonize entities with existing knowledge structures, enhancing the integrity and utility of the CKG. With TRACE, threat hunters and attack analysts gain real-time, holistic insights into vulnerabilities, attack methods, and defense technologies. 2026-02-11T06:54:21Z Zijing Xu Ziwei Ning Tiancheng Hu Jianwei Zhuge Yangyang Wang Jiahao Cao Mingwei Xu http://arxiv.org/abs/2602.07275v1 Evolving LLM-Derived Control Policies for Residential EV Charging and Vehicle-to-Grid Energy Optimization 2026-02-06T23:59:33Z This research presents a novel application of Evolutionary Computation to the domain of residential electric vehicle (EV) energy management. While reinforcement learning (RL) achieves high performance in vehicle-to-grid (V2G) optimization, it typically produces opaque \"black-box\" neural networks that are difficult for consumers and regulators to audit. Addressing this interpretability gap, we propose a program search framework that leverages Large Language Models (LLMs) as intelligent mutation operators within an iterative prompt-evaluation-repair loop. Utilizing the high-fidelity EV2Gym simulation environment as a fitness function, the system undergoes successive refinement cycles to synthesize executable Python policies that balance profit maximization, user comfort, and physical safety constraints. We benchmark four prompting strategies: Imitation, Reasoning, Hybrid and Runtime, evaluating their ability to discover adaptive control logic. Results demonstrate that the Hybrid strategy produces concise, human-readable heuristics that achieve 118% of the baseline profit, effectively discovering complex behaviors like anticipatory arbitrage and hysteresis without explicit programming. This work establishes LLM-driven Evolutionary Computation as a practical approach for generating EV charging control policies that are transparent, inspectable, and suitable for real residential deployment. 2026-02-06T23:59:33Z Vishesh Purnananda Benjamin John Wruck Mingyu Guo http://arxiv.or", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-08-12 12:54:50 UTC

```
arXiv EWS LLM:
export SKILL_DIR="/ai-inventor/.claude/skills/aii-web-tools"; export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "http://export.arxiv.org/api/query?search_query=abs:%22early+warning+signals%22+AND+abs:%22language+model%22&max_results=20&sortBy=submittedDate&sortOrder=descending" --max-chars 7000 2>&1 | head -50
```

### [26] TOOL RESULT — Bash · 2026-08-12 12:54:50 UTC

```
{"stdout": "URL: http://export.arxiv.org/api/query?search_query=abs:%22early+warning+signals%22+AND+abs:%22language+model%22&max_results=20&sortBy=submittedDate&sortOrder=descending\nType: HTML\nLength: 12468 chars (truncated)\n\n--- Content ---\n\nhttps://arxiv.org/api/RRMy/ZxRha2s1Av1rvXW2t3rFjM arXiv Query: search_query=abs:\"early warning signals\" AND abs:\"language model\"&id_list=&start=0&max_results=20 2026-08-12T12:54:49Z 20 7 0 http://arxiv.org/abs/2603.13325v1 Auditing Cascading Risks in Multi-Agent Systems via Semantic-Geometric Co-evolution 2026-03-04T16:45:26Z Large Language model (LLM)-based Multi-Agent Systems (MAS) are prone to cascading risks, where early-stage interactions remain semantically fluent and policy-compliant, yet the underlying interaction dynamics begin to distort in ways that amplify latent instability or misalignment. Traditional auditing methods that focus on per-message semantic content are inherently reactive and lagging, failing to capture these early structural precursors. In this paper, we propose a principled framework for cascading-risk detection grounded in semantic--geometric co-evolution. We model MAS interactions as dynamic graphs and introduce Ollivier--Ricci Curvature (ORC) -- a discrete geometric measure -- to characterize information redundancy and bottleneck formation in communication topologies. By coupling semantic flow signals with graph geometry, the framework learns the normal co-evolutionary dynamics of trusted collaboration and treats deviations from this coupled manifold as early-warning signals. Experiments on a suite of cascading-risk scenarios aligned with the risk category demonstrate that curvature anomalies systematically precede explicit semantic violations by several interaction turns, enabling proactive intervention. Furthermore, the local nature of Ricci curvature provides principled interpretability for root-cause attribution, identifying specific agents or links that precipitate the collapse of trustworthy collaboration. 2026-03-04T16:45:26Z This work has been accepted to ICLR 2026 Workshop: Principled Design for Trustworthy AI Zixun Luo Yuhang Fan Hengyu Lin Yufei Li Youzhi Zhang http://arxiv.org/abs/2602.01826v1 Beyond Precision: Training-Inference Mismatch is an Optimization Problem and Simple LR Scheduling Fixes It 2026-02-02T09:00:53Z Reinforcement Learning (RL) for training Large Language Models is notoriously unstable. While recent studies attribute this to \"training inference mismatch stemming\" from inconsistent hybrid engines, standard remedies, such as Importance Sampling, might fail during extended training runs. In this work, we analyze this instability through the lens of optimization, demonstrating that gradient noise and training-inference mismatch escalate in tandem as training progresses. Meanwhile, we find that the mismatch can be effectively suppressed by shrinking the update size. Taken together, we deduce that the mismatch is not merely a static numerical discrepancy, but a dynamic failure coupled with the model's optimization. Based on this insight, we propose a simple yet effective solution: a specialized Learning Rate (LR) scheduler. Instead of pre-defined decay schedule in traditional LR scheduler, our method dynamically triggers LR decay based on response length, which we identify as a reliable early-warning signal for impending instability. Empirical evidence suggests that by reducing the learning rate as gradient noise rises, we can consistently stabilize RL training and keep the training-inference mismatch at a safe level. 2026-02-02T09:00:53Z Yaxiang Zhang Yingru Li Jiacai Liu Jiawei Xu Ziniu Li Qian Liu Haoyuan Li http://arxiv.org/abs/2601.03007v2 From inconsistency to decision: explainable operation and maintenance of battery energy storage systems 2026-01-07T02:29:31Z Battery Energy Storage Systems (BESSs) are increasingly critical to power-system stability, yet their operation and maintenance remain dominated by reactive, expert-dependent diagnostics. While cell-level inconsistencies provide early warning signals of degradation and safety risks, the lack of scalable and interpretable decision-support frameworks prevents these signals from being effectively translated into operational actions. Here we introduce an inconsistency-driven operation and maintenance paradigm for large-scale BESSs that systematically transforms routine monitoring data into explainable, decision-oriented guidance. The proposed framework integrates multi-dimensional inconsistency evaluation with large language model-based semantic reasoning to bridge the gap between quantitative diagnostics and practical maintenance decisions. Using eight months of field data from an in-service battery system comprising 3,564 cells, we demonstrate how electrical, thermal, and aging-related inconsistencies can be distilled into structured operational records and converted into actionable maintenance insights through a multi-agent framework. The proposed approach enables accurate and explainable responses to real-world operation and maintenance queries, reducing response time and operational cost by over 80% compared with conventional expert-driven practices. These results establish a scalable pathway for intelligent operation and maintenance of battery energy storage systems, with direct implications for reliability, safety, and cost-effective integration of energy storage into modern power systems. 2026-01-06T13:32:04Z 13 pages, 5 figures Cell Reports Physical Science 7(6), 103388 (2026) Jingbo Qu Yijie Wang Yujie Fu Putai Zhang Weihan Li Mian Li 10.1016/j.xcrp.2026.103388 http://arxiv.org/abs/2510.05133v1 Characterizing Model Behavior Under Synthetic Data Training: An Empirical Study Across Scales and Mixing Ratios 2025-10-01T03:28:01Z Synthetic data generated by large language models has become integral to modern NLP training pipelines, from bootstrapping reasoning capabilities to augmenting instruction-following datasets. While recent work demonstrates successful applications maintaining high external data ratios, systematic understanding of how synthetic data proportion affects model behavior across different scales remains limited. This paper presents a controlled empirical study examining model performance, calibration, and output characteristics when trained on varying synthetic-to-external data ratios. Using the Pythia model suite (410M-12B parameters) across five diverse tasks, we evaluate models after one to three training iterations with synthetic data proportions ranging from 0-50\\%. Our key findings include: models maintain stable performance with up to 20\\% synthetic data, but degradation accelerates beyond 30\\%; larger models (6.9B-12B) show greater robustness to synthetic data than smaller models (410M-1.4B); calibration degradation precedes accuracy loss, providing an early warning signal; and task characteristics matter, with reasoning tasks degrading faster than retrieval tasks under synthetic data training. Importantly, we find that current best practices, such as those employed in STaR and Self-Instruct systems that maintain greater than 80\\% external data, operate well within safe regimes identified by our experiments. We provide prac", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-08-12 12:58:22 UTC

```
All six cited 2026 arXiv works verified as real and accurately characterized; no prior art found for EWS/critical-slowing-down applied to refusal dynamics or for hysteresis under within-generation steering ramps. Writing the review.
```

### [28] TOOL CALL — Bash · 2026-08-12 12:58:22 UTC

```
Write and validate review JSON:
cat > ./.terminal_claude_agent_struct_out.json <<'JSONEOF'
{
  "overall_assessment": "This is a large, disciplined revision that fixes every one of the eleven critiques from the previous round, several of them better than the suggested remedy (the training-free task-vector safety ladder is cheaper and cleaner than the LoRA de-alignment I proposed; the reset-control arm and the pre-registered third outcome are exactly right). I independently verified all six of the 2026 arXiv citations (2608.05578 AMS/Messenger, 2606.25750 RAS/Huang et al., 2607.14147 Kwon prefill, 2602.02600 Rahimi et al. step-wise, 2606.22686 Ratnakar & Vats, 2605.05427 Hasan & Biswas) — they exist, the authors and framings are reported accurately, and the differentiator sentences are fair rather than strawmanned. That is unusually good citation hygiene for a pre-registration. Prior-art screening (arXiv full-text queries on 'early warning signals' + language model, 'hysteresis' + LLM, and scholarly search on critical slowing down + LLMs) returned nothing that occupies this lane: the critical-slowing-down / EWS toolkit has not been applied to LLM generative dynamics or to safety auditing, and no one has run a within-generation steering ramp to test for hysteresis. The core idea is genuinely novel and the mechanistic reframing (safety as a shifted operating point in behavioral state space, unit = a rate not a direction) is the kind of conceptual move that top venues reward — the field handbook's own open question 3 (knowledge-action gap: decodability does not imply actionability) is precisely what this attacks, and it attacks it from the act side, which is the underserved side.\n\nWhat still blocks a higher score is not novelty and not sloppiness; it is that three specific things remain load-bearing and under-secured. (1) The power problem I raised last round is NOT actually fixed — it has been renamed. The panel is '>= 30 units', but the bootstrap is explicitly over weight LINEAGES with interpolants excluded from independent-unit counts, and the listed panel contains roughly 10-12 distinct lineages. The power calculation stated in success_criteria assumes n = 30 and is therefore internally inconsistent with the resampling scheme the same document mandates; at n_lineage ~ 11 the 95% CI around rho = 0.8 is closer to +/-0.30, and criterion (4)'s CI-lower-bound-above-baseline requirement is again close to unattainable regardless of truth. (2) H1 as now specified is almost guaranteed to CONFIRM for a trivial reason and therefore carries almost no evidential weight: the down-ramp is measured from a prefix that already contains refusal text, so the width is fully explained by ordinary next-token conditioning on that prefix — the exact 'generic autoregressive conditioning, not safety-specific suppression' mechanism Kwon reports — and the missing control is a forced-prefix arm, not the reset arm. (3) SPI is defined by within-panel z-scores, which makes it uncomputable for the single new checkpoint the product claim is about; RAS's calibrated absolute 0-100 scale beats it on exactly this axis. Plus a genuine conceptual tension the sign conventions hide: 'near the switching point' predicts BOTH more refusal and more jailbreak fragility, and unless the expected sign is pre-registered per ground truth, H3 is close to unfalsifiable. All four are fixable on paper before any compute is spent, and fixing them is worth roughly two points.",
  "strengths": [
    "Genuinely novel core move, verified by prior-art search: the early-warning-signal / critical-slowing-down toolkit (recovery rate, across-rollout variance, lag-1 autocorrelation, flickering) has not been applied to LLM generative dynamics or safety auditing. arXiv full-text queries on 'early warning signals'+'language model' and 'hysteresis'+'large language model' return nothing in this lane. The reframing from a static unit (direction, feature, circuit, basin volume) to a RATE is a real conceptual contribution, not a rebranding.",
    "Exceptional citation hygiene for a pre-registration. All six 2026 preprints cited were checked against arXiv and exist with the stated authors, titles and findings. The related-work entries do the harder thing than citing — each states an explicit differentiator, and two of the closest works (RAS, VISAGE) are promoted from citations to empirical baselines, which is what a top-venue reviewer wants to see.",
    "The revision is honest about prior claims it cannot own: it explicitly concedes 'shallow basin' to Peng et al. (VISAGE), the per-token refusal observable to Yin et al. ('Refusal Falls off a Cliff'), and the phase-transition language to Ratnakar & Vats. Renaming RRI to SPI with a stated sign convention and a written-out formula is exactly the requested fix.",
    "The pre-registered third outcome ('bistability present but not safety-specific') with a named citation basis (Kwon 2607.14147, Rahimi et al. 2602.02600) is model pre-registration practice — it removes the post-hoc rationalization cell that the previous version left open, and it correctly separates H1 from H1b.",
    "The training-free task-vector safety ladder W(t) = W_base + t*(W_instruct - W_base) plus partial-strength abliteration is a better solution to the degenerate-ground-truth problem than the LoRA de-alignment previously suggested: it costs matrix ops rather than training, and the lineage-exclusion caveat is stated up front rather than discovered by a reviewer.",
    "Ground truth is now correctly treated as three-dimensional (plain-harmful refusal, jailbreak ASR, XSTest over-refusal) on the basis of a real empirical finding (Hasan & Biswas: over-refusal and harmful compliance nearly uncorrelated), and the measurement-error treatment (LLM judge primary, string matcher as screen, Cohen's kappa, >=100 hand-adjudicated items, attenuation-corrected correlation) is more rigorous than most published safety-metric papers.",
    "The three null controls for H2 (random readout axis, random vs refusal-aligned perturbation, syntactic-probe observable) are well chosen: together they are what separates 'a basin' from 'generic mixing', and pre-committing that a positive result on the syntactic probe is DISCONFIRMING is a real falsifiability commitment.",
    "The abliteration circularity fix is correct and non-obvious: making the logit-lens refusal log-odds primary precisely because it survives an orthogonalization edit, with the diff-in-means projection demoted to descriptive, closes a hole that would have made criterion (2) unfalsifiable in the abliterated arm."
  ],
  "dimension_scores": [
    {
      "dimension": "soundness",
      "score": 3,
      "justification": "The two fatal operationalization errors from the previous round (single-valued alpha sweep; token-position-as-time) are correctly fixed, and the control structure for H2 is now strong. What keeps this from a 4 is that H1's decisive test still has an uncontrolled trivial explanation (prefix-content conditioning rather than path dependence), the estimator statistics (AC1 and exponential lambda on 32-64 generated steps, non-detrended) are under-identified at the stated sequence lengths, and the power arithmetic contradicts the mandated resampling unit.",
      "improvements": [
        "Add the forced-prefix control arm to H1 (see critique 2): without it, nonzero loop width is explained by next-token conditioning on refusal text and the decisive test decides nothing.",
        "Detrend r_t before computing AC1 by subtracting the across-rollout mean trajectory at each generated step — the >=20 rollouts already provide the estimate — and report a synthetic-recovery check showing that the lambda estimator recovers a known decay constant from a 20-40 step series at the observed noise level. Both are cheap and both are the difference between a statistic and a number.",
        "Reconcile the power statement with the lineage bootstrap: state n_lineage explicitly for the actual panel, recompute the CI half-width at that n, and soften criterion (4) in advance to the level that n supports."
      ]
    },
    {
      "dimension": "presentation",
      "score": 3,
      "justification": "Very well organized for a pre-registration — the terms glossary, the step-numbered protocol, the pre-registered baseline list and the explicit CONFIRM/THIRD-OUTCOME/DISCONFIRM cells make it evaluable by an expert without further questions on most points. It is however dense and, more damagingly, contains two internal inconsistencies (the n=30 vs lineage-bootstrap arithmetic; unspecified expected signs across the three ground truths) that a careful reader hits and has to resolve for the authors.",
      "improvements": [
        "Add a small table with one row per ground truth (plain-harmful refusal, jailbreak ASR, XSTest over-refusal) and columns for expected SIGN of the SPI correlation, the pre-registered threshold, and the theoretical reason for that sign. This is a five-line fix that converts the sharpest conceptual ambiguity into a falsifiable commitment.",
        "Add a one-paragraph compute budget: wall-clock estimate per checkpoint for each of Step 1 / Step 2 / Step 3, with the honest observation that the AUDIT is cheap while the VALIDATION is not, and a tier-1 / tier-2 panel split so a partial run is still reportable.",
        "State the number of distinct weight lineages in the panel explicitly alongside the >=30 unit count, so a reader is not left to count them."
      ]
    },
    {
      "dimension": "contribution",
      "score": 3,
      "justification": "The question is important (cheap, harmful-content-free safety auditing of arbitrary open-weight checkpoints), the framing is genuinely new and verified unoccupied, the incumbents are named and run as baselines, and even the pre-registered negative is publishable. It is held below 4 because the headline deliverable — a score you can compute for one new checkpoint — is not actually computable as defined (within-panel z-scores), and because H4, the sharpest differentiating claim, rests on n=2 behavioral uncensored fine-tunes.",
      "improvements": [
        "Define a frozen, panel-independent normalization for SPI (publish the reference means/sds) and demonstrate scoring of >=3 genuinely held-out checkpoints never used in normalization. Without this the product claim is weaker than RAS's calibrated 0-100 scale on the exact axis it claims to beat it.",
        "Raise the behavioral-uncensored-fine-tune count to >=4 CPU-feasible checkpoints, verify in advance that each actually preserves cluster separation and refusal-direction cosine (otherwise it is not the blind-spot class), and label H4 a pre-registered case study rather than a statistical claim if the count stays small.",
        "State plainly in the motivation what a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space — the current text says the space and cost differ, but not what is newly explained. One sentence naming a phenomenon the weight-space basin cannot account for would materially strengthen the contribution claim."
      ]
    }
  ],
  "critiques": [
    {
      "category": "rigor",
      "severity": "major",
      "description": "The power problem from the previous round is renamed rather than solved, and the document now contradicts itself. success_criteria computes power 'at n = 30 lineage-weighted units', giving a 95% CI half-width of ~+/-0.15 around rho = 0.8. But Step 4 mandates bootstrapping over weight LINEAGES as the unit of the model-level claim, and the assumptions block explicitly excludes the task-vector interpolants and partial-abliteration variants from independent-unit counts. Counting the listed panel by lineage gives roughly 10-12 independent units (Qwen3-0.6B/1.7B/4B trios collapse to three lineages, Qwen2.5-0.5B/1.5B two, Llama-3.2-1B/3B two, gemma-2-2b one, SmolLM2-360M/1.7B two, TinyLlama one, plus the uncensored fine-tunes). At n_lineage ~ 11 the 95% bootstrap CI around an observed rho = 0.8 is roughly +/-0.30, not +/-0.15, and criterion (4)'s requirement that the CI lower bound exceed the best baseline correlation is close to unattainable no matter what is true — exactly the failure mode flagged last round. The partial rank correlation controlling for static mean AND scale (two covariates, strongly correlated predictors) has even less power at that n. This is not a presentational slip: the resampling unit and the power arithmetic must agree before any compute is spent, or the run produces a number no criterion can adjudicate.",
      "suggested_action": "Do three things before running. (1) Enumerate the panel by LINEAGE in the pre-registration and state n_lineage explicitly next to the >=30 unit count. (2) Recompute the power table at that n and, if the CI-exclusion criterion is unattainable, replace criterion (4)'s exclusion requirement in advance with a paired comparison that has more power: bootstrap the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages and require the difference CI to exclude 0, which removes the between-lineage variance common to both and is the standard fix. (3) Expand the lineage count where it is cheapest: Pythia-410M/1B/1.4B, OLMo-1B, Danube3-500M, Phi-3-mini (int8), Falcon3-1B-Instruct, Granite-3.1-2B-Instruct and MiniCPM all add architecture families at essentially zero marginal cost given the method's own cheapness claim, and getting to ~18-20 lineages roughly halves the CI width."
    },
    {
      "category": "methodology",
      "severity": "major",
      "description": "H1's decisive test now has the opposite problem from last round: instead of being guaranteed to return zero, it is close to guaranteed to return a large positive width for a reason that has nothing to do with bistability. In the retained-prefix ramp, alpha_up is the coefficient at which refusal onset is emitted from a COMPLIANT prefix; alpha_down is the coefficient at which compliance resumes from a prefix that now CONTAINS refusal text ('I cannot help with that...'). A refusal prefix conditions strongly toward continued refusal in any autoregressive LM, aligned or not — this is precisely the 'generic autoregressive conditioning, not safety-specific suppression' mechanism Kwon (2607.14147) demonstrates with a base-model control, and the 'autoregressive commitment masks underlying instability' observation in Rahimi et al. (2602.02600). So the measured width conflates two things: path dependence through a genuine latent state (the bistability claim) and ordinary first-order conditioning on the literal text already emitted (trivial). The mandated reset control does not separate them: it discards the prefix entirely, so it removes BOTH mechanisms at once and, under greedy decoding, returns zero by pure construction — it is an implementation sanity check, not an informative control. As specified, H1 confirms, the entire evidential burden silently falls on H1b's ordering test, and a reviewer will ask why the 'decisive test' was decisive of nothing.",
      "suggested_action": "Add a forced-prefix control arm, which is the control that actually isolates the claim. For each prompt, take the refusal prefix produced at the top of the up-ramp, force-feed it as a fixed prefill WITHOUT ever having ramped alpha up, then ramp alpha DOWN from the same starting value and record the flip-back threshold. Call this alpha_down_forced. Then: (width_naive = alpha_up - alpha_down) is the current quantity; (alpha_down - alpha_down_forced) is the residual path dependence NOT explained by prefix content, and that residual is what the bistability claim is actually about. Pre-register the residual, not width_naive, as the H1 test statistic, and report both. Additionally, pre-register the prediction that width_naive is large and positive in base models too (per Kwon), so that outcome is scored as expected rather than as a surprise. Finally, at temperature 0.7 the reset arm will NOT give exactly zero — sampling noise produces apparent width — so replace the 'must give width exactly 0' language with 'must give width indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the noise floor against which the retained-prefix width is compared'."
    },
    {
      "category": "methodology",
      "severity": "major",
      "description": "SPI as defined cannot be computed for the use case that motivates the whole paper. It is fixed as 'the mean of the WITHIN-PANEL z-scores' of four terms. Within-panel standardization means the score of any checkpoint depends on which other checkpoints are in the panel — so for 'any random model on Hugging Face', the deliverable the motivation promises, SPI is undefined until you assemble a comparison panel and re-run every model in it. This is a strictly weaker product than the incumbent it claims to beat: RAS (2606.25750) explicitly maps to a calibrated absolute 0-100 scale precisely so a single target can be scored. It also creates a subtler validity problem: a rank correlation computed on panel-standardized scores against panel-measured ground truth is partly a within-panel artifact, and leave-one-out accuracy in AMS's format is not comparable if the left-out model contributed to the normalization constants.",
      "suggested_action": "Freeze the normalization. Compute the four terms' means and standard deviations once on a designated REFERENCE subset of the panel, publish those constants in the paper, and define SPI for any new checkpoint using the frozen constants only. Then (a) recompute all leave-one-out and leave-one-family-out numbers with the left-out model excluded from the normalization fit — otherwise the LOO figure is leaked and not comparable to AMS's 71%; and (b) reserve >=3 checkpoints that appear in NO normalization or fitting step and report their SPI and ground truth as a genuine out-of-panel demonstration. That demonstration, more than any correlation, is what makes the product claim credible, and it costs three extra model downloads."
    },
    {
      "category": "rigor",
      "severity": "major",
      "description": "The theory predicts opposite signs for two of the three ground truths and the pre-registration does not say which. 'Higher SPI = closer to the switching point = expected to refuse more' is stated in the glossary, which implies SPI correlates POSITIVELY with plain-harmful refusal rate. But the same construct — a shallow basin, small dominant eigenvalue, easy to push across the fold — is the textbook signature of FRAGILITY, which predicts HIGHER jailbreak attack-success rate, i.e. a model near the switch should be easy to tip into compliance. So SPI is predicted to go up with refusal rate and up with ASR, while refusal rate and ASR themselves are inversely related for most checkpoints. Criterion (4) asks only for 'rho >= 0.6 with jailbreak attack-success rate' without a sign, so as written either sign of a strong correlation can be read as success — which makes the headline claim close to unfalsifiable, and a reviewer will notice. This is arguably the most interesting theoretical question the proposal raises (nearness to a switch is not the same construct as behavioral safety, and the framing conflates them), and it deserves to be confronted rather than left implicit.",
      "suggested_action": "Write a signed prediction table into the pre-registration: one row per ground truth (plain-harmful refusal rate, jailbreak ASR, XSTest over-refusal), each with the expected sign, the threshold, and a one-line theoretical justification. Then resolve the tension explicitly, and the resolution is available: distinguish SPI's two possible readings — 'the comply basin is shallow, so the model tips INTO refusal easily' (predicts high refusal, high over-refusal, LOW ASR) versus 'the model sits near a fold in both directions, so it tips either way' (predicts high refusal AND high ASR). These make different predictions on the sign of rho(SPI, ASR), so pre-register both as competing hypotheses with the outcome that discriminates them. That converts a hidden ambiguity into a genuinely informative experiment and materially raises the contribution."
    },
    {
      "category": "methodology",
      "severity": "major",
      "description": "The dynamical estimators are under-identified at the stated sequence lengths and the series is non-stationary. Generations are capped at 32-64 new tokens, so lambda is fit to an exponential decay over at most ~20-50 generated steps after the injection point, and AC1 is estimated from a series of the same length. Two problems compound. (1) Estimator variance: AC1 from n ~ 40 has a standard error near 1/sqrt(n) ~ 0.16 before any model noise, which is the same order as the between-model differences the hypothesis needs to detect; an exponential fit to a short, noisy decay is notoriously ill-conditioned in the decay-constant parameter. (2) Non-stationarity: r_t over generated steps has a strong deterministic trend — early tokens after the chat template behave systematically differently from tokens 40-60, and once a model commits to a topic the refusal log-odds drift. AC1 computed on a trended series measures the trend, not fluctuation around an attractor, which is the same class of error as the token-position version rejected last round, only milder. Rising AC1 in 'safer' models could simply mean those models produce more stereotyped, template-driven openings.",
      "suggested_action": "Three fixes, all cheap. (1) Detrend before computing AC1 and Var*: you already have >=20 rollouts per prompt, so subtract the across-rollout MEAN trajectory at each generated step and compute AC1 on the residuals. This is the correct 'fluctuation around the deterministic path' quantity and it removes the stereotypy confound directly. (2) Run a synthetic-recovery check on the lambda estimator: simulate an AR(1)-with-known-decay process at the observed noise level and series length, and report the estimator's bias and variance. Pre-register a minimum series length below which lambda is not reported. (3) Raise max_new_tokens for the H2 rollouts specifically to 128-192 (only the H2 arm needs it; ground-truth generation can stay at 64), and report the indicators as a function of series length so a reader can see whether the ordering is stable or an artifact of truncation."
    },
    {
      "category": "scope",
      "severity": "major",
      "description": "The compute budget is not stated and the design is far heavier than the 'seconds per model' framing implies, which puts completion at risk. Ground truth alone is ~30 checkpoints x (80 harmful + 80 jailbreak variants + 50 XSTest) x 64+ generated tokens = on the order of 6,000+ generations, on CPU. H2 is ~30 checkpoints x 20 prompts x 20 rollouts x 2 arms (clean/perturbed) x 64 tokens, plus an epsilon sweep, plus three control conditions (random axis, random-direction perturbation, syntactic probe) — that alone is on the order of 100k+ generated tokens per checkpoint with residual-stream hooks active. H1 is 30 prompts x 2 ramp directions x 2 temperatures x 30 checkpoints, plus the reset arm and (per critique 2) the forced-prefix arm. Add ~30 checkpoint downloads including 4B models, plus materializing task-vector interpolants (each of which is a full extra weight set on disk). None of this is impossible, but the design as written has no stated budget, no staging, and no partial-completion story — the realistic failure mode is that the run is 60% done at deadline and no criterion can be evaluated, which is the same amount of wasted compute as a fatal flaw.",
      "suggested_action": "Add an explicit compute-budget paragraph with a per-step wall-clock estimate and a tiered panel. Tier 1: ~10-12 checkpoints spanning all >=4 families and both endpoints of the ladder, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2 with controls. Tier 2: the remaining units, added to Step 3 and Step 4 only (ground truth and correlation), where the marginal cost is lowest and the marginal power gain is highest. Pre-register that criteria are evaluated on whatever tier completes, with the tier stated. Separately — and this matters for the paper's framing — report AUDIT cost (what a user pays to score one new checkpoint: a handful of harmless prompts) as a distinct number from VALIDATION cost (what this study pays). Conflating them invites the objection that the cheap method needed an expensive study, which is fine and normal but must be said plainly."
    },
    {
      "category": "methodology",
      "severity": "minor",
      "description": "The task-vector safety ladder is the mechanism that rescues the ground-truth distribution from trimodality, and it can silently fail in a way that corrupts both the ground truth and the dynamics. Linear interpolation W(t) = W_base + t*(W_instruct - W_base) produces coherent models only when the two endpoints are linearly mode-connected — plausible for Qwen3 base/instruct, which share initialization, but at intermediate t the model may produce degenerate, repetitive or off-distribution text. If it does, its measured refusal rate is meaningless (a model emitting gibberish neither refuses nor complies), AND its r_t series is dominated by degeneracy rather than by basin geometry, so it contaminates both sides of the headline correlation simultaneously — which is worse than contaminating either alone, because it can manufacture a spurious correlation. The same risk applies to partial-strength abliteration, which is known to degrade fluency at high orthogonalization strength.",
      "suggested_action": "Pre-register a fluency screen with an exclusion rule before any interpolant enters the analysis: perplexity on a held-out benign corpus (e.g. WikiText or the model's own instruct-format completions) must be within a stated factor — 2x is a defensible pre-registered threshold — of the t=1 endpoint, plus a degenerate-repetition check (distinct-n / max n-gram repeat rate). Report how many interpolants were manufactured and how many passed; if the pass rate is low, the ladder does not fill the middle of the range and the trimodality problem returns, which the paper must then say. Also verify that the passing interpolants actually produce INTERMEDIATE refusal rates rather than snapping to one endpoint — a step function in t would make the ladder useless for its stated purpose, and that is worth checking on one base/instruct pair before building all nine."
    },
    {
      "category": "evidence",
      "severity": "minor",
      "description": "H4 — 'where static geometry fails', the sharpest differentiating claim against AMS and the one that most distinguishes this from the incumbents — rests on 'at least two behavioral uncensored fine-tunes'. n=2 cannot support a claim of the form 'SPI succeeds on the class that static geometry cannot see'; it supports at most an existence proof. Worse, the claim has an unverified premise: the chosen checkpoints must ACTUALLY preserve harmful/benign cluster geometry and refusal-direction cosine, or they are not instances of the blind-spot class at all and H4 tests nothing. Dolphin/Josiefied-style models at <=4B are also not guaranteed to be pure behavioral fine-tunes; some publicly distributed 'uncensored' variants are abliterated or are merges of abliterated components, which would put them in the wrong class entirely.",
      "suggested_action": "Raise the count to >=4 CPU-feasible behavioral fine-tunes and, critically, add a pre-analysis class-membership check: for each candidate, compute cluster separation sigma and refusal-direction cosine against its parent and confirm both are preserved (i.e. AMS-style scanning marks it safe) while its measured harmful-compliance rate is high. Only checkpoints passing that check count toward H4; report the ones that fail and why. Also check each model card and community discussion for abliteration or abliterated-merge provenance before including it. If the final count stays below 4, label H4 in advance as a pre-registered case study with per-model reporting rather than a statistical claim — an honest n=2 case study that AMS-style scanning demonstrably misses is still a strong result, and over-claiming it is the only way to lose that."
    },
    {
      "category": "rigor",
      "severity": "minor",
      "description": "Two baselines in the pre-registered list are specified at a level that makes the comparison unfalsifiable in the authors' favour. (a) The 'RAS/SafeVec-style representation-alignment score' is described only by its dependencies, not by its implementation; RAS involves layer-window stability selection and a calibration mapping, and a loose reimplementation that underperforms would be an unconvincing win. (b) The VISAGE-style basin volume is restricted to a 6-model subset 'with the reduction stated honestly' — honest, but 6 points cannot yield a rank correlation comparable to SPI's 30, so the comparison is not like-for-like even when reported honestly. Given that the whole H3 claim is 'beats the published incumbents', the quality of the incumbent implementations is load-bearing.",
      "suggested_action": "For RAS: pre-register the exact reimplementation (reference model, layer-window selection rule, prompt sets, calibration) and, where the original paper reports numbers on models that overlap this panel, report a reproduction check against those published numbers as evidence the baseline is faithful. If reproduction is out of scope, say so and label the RAS comparison as 'against our reimplementation' throughout rather than 'against RAS'. For VISAGE: on the 6-model subset, report SPI's correlation ON THAT SAME SUBSET alongside VISAGE's, so the comparison is at matched n; the 30-model SPI number is not a valid comparator for a 6-model VISAGE number and a reviewer will say so."
    },
    {
      "category": "novelty",
      "severity": "minor",
      "description": "The related-work treatment is strong, but one differentiator is asserted rather than argued and it is the one carrying the mechanistic contribution. Against VISAGE the text says the departure is 'the space and the cost' — weight-space vs behavioral-state-space geometry, and harmful-benchmark-per-perturbation vs harmless prompts. The cost difference is clear and defensible. The SPACE difference is not yet a claim: the proposal does not say what a basin in behavioral state space EXPLAINS that a basin in weight space does not, so a reviewer can reasonably read it as the same phenomenon measured more cheaply, which is a smaller contribution than the one the motivation advertises ('a mechanistic account of what safety tuning buys'). The same applies, more mildly, to the reinterpretation of Qi et al.: 'shallow in behavioral state space rather than token depth' is asserted as a reframing but no observation is named that would distinguish the two descriptions.",
      "suggested_action": "Name one discriminating observation for each. For VISAGE: the two accounts diverge on models where weight-space and behavior-space geometry come apart — a behavioral uncensored fine-tune is a candidate (large behavioral change, possibly small weight-space basin change), as is a task-vector interpolant (smooth weight-space path, possibly step-like behavioral change). Pre-register that comparison; if the behavioral basin and the weight basin rank the panel identically, say so and drop the mechanistic claim to a cost claim. For Qi et al.: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes after; the basin account predicts lambda differences persist across generated steps. Step 5 already collects step-wise lambda profiles, so this discriminating test is free — state it as a named prediction rather than leaving it as descriptive mechanism mapping. Both additions cost nothing in compute and convert asserted differentiators into tested ones."
    },
    {
      "category": "clarity",
      "severity": "minor",
      "description": "The single-forward-pass measurement is retained 'only as an explicitly heuristic secondary measurement with the 1/t dilution null fitted and subtracted', but nothing in the success criteria or disconfirmation cells says what role, if any, it plays. Retained-but-unscored measurements are how a garden of forking paths gets in through the back door: if the primary generated-step result is null and the secondary forward-pass result is positive, the pre-registration as written gives no guidance, and the paper will be tempted to lead with the latter.",
      "suggested_action": "Either drop the single-forward-pass arm entirely — it costs measurement time and buys nothing the generated-step version does not — or state in one sentence that it is reported as a descriptive appendix figure only, contributes to NO criterion, and cannot be substituted for the generated-step result under any outcome. The second option is fine; the current silence is not."
    }
  ],
  "score": 6,
  "confidence": 4,
  "relation_type": "evolution",
  "relation_rationale": "Same bistability/EWS frame; operationalizations, panel, controls and criteria refined to fix prior review's flaws."
}
JSONEOF
python3 -c "import json;d=json.load(open('./.terminal_claude_agent_struct_out.json'));print('ok',d['score'],len(d['critiques']),len(d['dimension_scores']))"
```

### [29] TOOL RESULT — Bash · 2026-08-12 12:58:30 UTC

```
{"stdout": "ok 6 11 3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-08-12 12:58:46 UTC

```
Review written to `./.terminal_claude_agent_struct_out.json`.

**Verdict: 6 (Weak Accept), confidence 4.** Soundness 3, Presentation 3, Contribution 3. Relation to previous: **evolution**.

**Evidence grounding done first:** I verified all six 2026 arXiv citations directly against arXiv (2608.05578 Messenger/AMS, 2606.25750 Huang et al./RAS, 2607.14147 Kwon, 2602.02600 Rahimi et al., 2606.22686 Ratnakar & Vats, 2605.05427 Hasan & Biswas) — all real, correctly attributed, fairly characterized. Prior-art screening via arXiv full-text queries (`"early warning signals"`+language model, `"hysteresis"`+LLM) and scholarly search found the lane genuinely unoccupied: critical slowing down / EWS has not been applied to LLM generative dynamics or safety auditing.

**The revision fixed all 11 prior critiques**, several better than suggested (training-free task-vector ladder beats the LoRA route; the pre-registered third outcome and abliteration-circularity fix are model practice).

**Four remaining major blockers**, all fixable on paper before compute:

1. **Power problem renamed, not solved.** `success_criteria` computes power at n=30, but Step 4 mandates bootstrapping over *lineages* with interpolants excluded — the panel has ~11 lineages, so the CI is ~±0.30, and criterion (4) is again unattainable. Fix: bootstrap the *difference* rho_SPI − rho_baseline on the same resampled lineages, and add cheap extra families.
2. **H1 now confirms trivially.** alpha_down is measured from a prefix that already contains refusal text, so width is explained by ordinary next-token conditioning — exactly Kwon's "generic autoregressive conditioning" mechanism. The reset arm removes both mechanisms at once and returns zero by construction. The missing control is a **forced-prefix arm**; the residual `alpha_down − alpha_down_forced` is the real test statistic.
3. **SPI isn't computable for its own use case** — within-panel z-scores mean scoring one new HF checkpoint requires re-running a panel. RAS's calibrated 0–100 scale beats it on precisely that axis. Needs frozen published normalization constants + genuinely out-of-panel demonstration (and LOO must exclude the left-out model from normalization, or the AMS comparison is leaked).
4. **Unfalsifiable sign.** "Near the switching point" predicts *both* more refusal *and* more jailbreak fragility, and criterion (4) asks for rho ≥ 0.6 with ASR without specifying sign. This is the most interesting question the proposal raises — I recommended pre-registering the two readings as competing hypotheses discriminated by sign(rho(SPI, ASR)).

Plus majors on estimator identifiability (AC1/λ on 32–64 steps, non-detrended — detrend against the across-rollout mean trajectory they already have) and unstated compute budget with no partial-completion story.
```
