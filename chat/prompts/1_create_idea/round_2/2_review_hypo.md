# review_hypo — create_idea

> Phase: `hypo_loop` · round 2 · `review_hypo`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-12 12:53:56 UTC

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

### [2] HUMAN-USER prompt · 2026-08-12 12:53:56 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-handbook-auto-mechanistic-interpretability · 2026-08-12 12:54:04 UTC

The agent loaded the **aii-handbook-auto-mechanistic-interpretability** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-handbook-auto-mechanistic-interpretability
description: "Verified field handbook for mechanistic-interpretability research. ALWAYS read before ANY mechanistic-interpretability research work — ideation/novelty assessment, study planning, experiment/eval design, write-up, or review; do NOT do any of these from priors alone (the field's core validity assumptions were contested through H1-2026 and several obvious-looking directions are saturated). Triggers: mechanistic interpretability, mech interp, circuits, circuit discovery, activation patching, attribution patching, causal abstraction, causal scrubbing, interchange interventions, sparse autoencoder, transcoder, attribution graph, steering vector, activation steering, probing, auto-interp, model diffing, CoT faithfulness, monitorability, weight-sparse transformers, MIB, BlackboxNLP. NOT for: post-hoc XAI on tabular or vision pipelines (SHAP/LIME/saliency), prompt engineering, generic capability evaluation, or training and finetuning work with no interpretability question."
---

<!-- GENERATED by amg-handbook-forge — DRAFT for expert review. generated: 2026-07-27 · next_check:
     2026-10-27 (volatile.md half-life ≈ 3 months). ✓x=exec · [Sn]=cited · ⚠️=candidate.
     Row fails → `STALE: <what>` in place. -->

# Mechanistic interpretability — field handbook

## Overview

Scope: the FIELD of mechanistic interpretability — what a mechanistic claim is, how it is
validated, and where the frontier sits mid-2026. The star is the SUBSTRATE below: a dated,
source-anchored map with an explicit do-not-redo list. The only lens is open questions.
This is the SOLE interpretability handbook: SAE-era decomposition
primitives are covered here as one thread of six rather than in a separate deep-dive.

## Organizing principles (how the field reasons)

- The field defines itself by **goal, not method**: understand computational mechanisms "in order
  to accomplish concrete scientific and engineering goals" [S1].
- Its own venue prints a **two-track evidence bar**: either "specific falsifiable hypotheses, and
  how the evidence provided does and does not support them", or "clear practical benefits over
  well-implemented baselines" [S14].
- One methodological critique reframes findings as **statistical estimates, not properties**: the
  causal effect of a component is "a volatile random variable rather than a fixed property" [S4].
- **Structure is not mechanism.** Discovery algorithms "sample from an equivalence class of valid
  subgraphs rather than recovering a unique mechanism" [S23].
- **Causal abstraction is vacuous without an encoding assumption**: with unrestricted alignment maps,
  "any neural network can be mapped to any algorithm" [S5].
- The artifact a reader gets is a **hypothesis about the model, not a description of it** —
  attribution graphs (Anthropic) run on a replacement model and give satisfying insight on about
  "a quarter of the prompts" [S11].

## Frontier (recency-weighted)

**Validity & stability of the method itself** *(weight-capped — the loudest thread)*

- Circuit discovery is unstable under small perturbations: "small perturbations in input data
  or hyperparameters yield vastly different circuits" [S4] (2025-10, rev 2026-05).
- Phantom specialization: across 75 circuits in five Pythia models, structural differences showed
  "apparent specialization but do not correspond to functional differences" [S23] (2026-06).
- The workhorse approximation was diagnosed — attribution patching's "dominant error stems from the
  non-linearities in the downstream network rather than local curvature at the patched component",
  with a correction in the same paper [S19] (2026-06).

**Intrinsic interpretability (train-for-interpretability)**

- Weight-sparse transformers yield understandable circuits, but "making weights sparser trades off
  capability for interpretability", and "scaling sparse models beyond tens of millions of nonzero
  parameters while preserving interpretability remains a challenge" [S18] (2025-11).
- The newest entrant flips the unit from behavior to parameter, asking "whether a single weight can
  be understood globally across the full training distribution" [S2] (2026-07, four models only).

**Evaluation & standardization**

- MIB is a standardized method-comparison benchmark: on causal variable localization "the supervised DAS method
  performs best, while SAE features are not better than neurons" [S10] (ICML 2025), extended to a
  community shared task whose framing admission stands — "measuring progress in MI remains
  challenging" [S22] (BlackboxNLP 2025).
- Randomized baselines invalidate the auto-interp proxy: SAEs on randomly initialized transformers
  score similarly to trained ones [S9] (2025-01, rev 2026-01).

**Decomposition primitives (the SAE era, and after)**

- The sparsity objective is itself a distorting inductive bias: feature absorption "is caused by
  optimizing for sparsity in SAEs whenever the underlying features form a hierarchy", so
  "SAE latents may be inherently unreliable classifiers" [S30] (NeurIPS 2025 Oral).
- The single latent is not a canonical unit — SAE stitching shows dictionaries are incomplete and
  meta-SAEs show they are "not atomic" [S33] (ICLR 2025); seed-unstable latents concentrate in
  "reproducible lower-rank subspaces", i.e. basis ambiguity rather than noise [S35] (2026-06).
- The raw-latent verdict a reviewer will cite: on steering "prompting outperforms all existing
  methods" and on detection difference-in-means wins — "SAEs are not competitive" [S31] (2025-01);
  contested, but only by an unreviewed supervised-pipeline rebuttal [S25].
- Proxy metrics are the field's own named weak point: "gains on proxy metrics do not reliably
  translate to better practical performance" [S32] (ICML 2025).
- Model diffing has a known-bad default: the crosscoder L1 loss "can misattribute concepts as unique
  to the fine-tuned model, when they really exist in both models"; the same paper ships the BatchTopK
  fix [S34] (NeurIPS 2025).
- The flagship open fleet has already moved past SAE-only — Gemma Scope 2 ships "transcoders,
  cross-layer transcoders, and crosscoders" alongside SAEs [S36] (2025-12).

**Reasoning-trace interpretability**

- Faithfulness and monitorability come apart: "models can appear faithful yet remain hard to
  monitor when they leave out key factors" [S12] (2025-10).
- The dominant unfaithfulness metric is contested — it "confuses unfaithfulness with
  incompleteness", and "the absence of hint words alone does not prove unfaithfulness" [S13]
  (2025-12, rev 2026-05).

**Applied / safety-facing interpretability**

- Persona vectors (Anthropic) predict and pre-empt training-induced trait shifts, and "flag training data that
  will produce undesirable personality changes" [S16] (2025-07) — the clearest applied win.
- A blinded audit protocol exists: three of four teams "successfully uncovered the model's hidden
  objective", SAEs among the techniques used [S17] (2025-03).
- Counter-current, and the sharpest 2026 negative result — internal decodability far exceeded output
  behaviour: "Linear probes discriminated hazardous from benign cases with 98.2% AUROC, yet the
  model's output sensitivity was only 45.1%, a 53-percentage-point knowledge-action gap." SAE
  feature steering "produced zero effect despite 3,695 significant features", and steering was
  "indistinguishable from random perturbation" [S3] (2026-03; 400 physician-adjudicated vignettes,
  one clinical domain).

**Field strategy & meta-science**

- A frontier lab publicly narrowed its bet — "We have been disappointed by the amount of progress
  made by ambitious mech interp work, from both us and others", and "We made a decision to
  deprioritise SAE research as a result, not because we thought the technique was useless" [S6]
  (2025-12). One team's decision, not a field verdict.
- Results are not yet comparable across papers: two studies reached "conflicting conclusions for the
  same behavior", a third found both "partially correct but incomparable" [S8] (2026-04).

## Recent (~1–2 yr, compressed) · Durable core

- The field's own review concedes "there are many open problems in the field that require solutions
  before many scientific and practical benefits can be realized" [S1] (2025-01), and the LRM sub-map
  names the same gaps [S24]. The two framings a reviewer will invoke: "the returns from
  interpretability have been roughly nonexistent" [S7] (2025-05), against "We are thus in a race
  between interpretability and model intelligence." [S15] (2025-04) — a stated goal, not a result.
- Durable: activation patching remains the gold-standard causal metric faster methods approximate [S19];
  attribution graphs remain the scaling story, with their stated ceiling [S11].

## ⛔ Already crowded — go ELSEWHERE (do-not-redo)

The blank space is NOT in these lanes; each is saturated through H1-2026:

- **Circuit-discovery methods and their corrections.** Attribution patching, its error diagnosis and
  second-order fix [S19], structural-vs-functional decoupling [S23], and an eight-method community
  bake-off [S22] are all published.
- **Auto-interp / agentic feature explanation.** Both the agentic pipeline [S21] and the
  randomized-baseline invalidation of its metrics [S9] already exist.
- **Activation steering and its reliability diagnostics.** Per-sample unreliability and the
  linear-approximation limit are characterized [S20]; the AxBench verdict
  already has a published rebuttal [S25].
- **CoT faithfulness / monitorability metrics.** The measurement wave [S12] and the
  metric-invalidating counter-wave [S13] have both landed.
- **Benchmarking MI methods against each other.** MIB [S10] plus its shared-task extension [S22]
  own this; a new leaderboard re-treads it.
- **Developmental / training-dynamics interpretability.** Feature evolution is already tracked
  across pre-training snapshots with crosscoders [S28] (ICLR 2026).
- **Training-data attribution as an interpretability method.** Already explicitly bridged to MI and
  causally validated on Pythia [S26].
- **Multimodal / vision-language mechanistic interpretability.** Has its own survey and taxonomy
  since 2025-02 [S27].
- **Mechanistic interpretability of RL-trained reasoning models.** Occupied through 2026 — temporal
  sparse autoencoders already track feature dynamics across RLVR training [S29].
- **Sparse-dictionary decomposition of activations.** The most-worked lane in the field: SAE features
  are "not better than neurons" on MIB [S10], the auto-interp metrics used to defend them fail a
  randomized baseline [S9], absorption is traced to the objective itself [S30], canonical-unit claims
  are refuted [S33], and the raw-latent steering/detection verdict plus its rebuttal are both
  published [S31] [S25].

> **Standing directive — this list is necessarily INCOMPLETE.** Map-silence means *not-yet-checked*,
> NOT *open*. Before committing to any direction this map does not explicitly flag as crowded, run
> a fresh, dated saturation search and confirm the space is actually unoccupied. (Measured in this forge's own
> A/B runs: a live-searching baseline beats a static handbook precisely on the crowded lanes a
> map omits.)

## Open questions the field hasn't answered

*(the whole lens — the reader answers in their own way)*

1. If exact single-input causal scores are volatile random variables [S4] and structurally distinct
   circuits implement one computation [S23], **what object is circuit discovery actually estimating,
   and at what granularity is a "mechanism" even well-defined?** The field's standard output — one
   circuit, one figure — presupposes an answer it has not given.
2. Causal abstraction is vacuous without a constraint on how models encode information [S5]. What
   would make such an encoding assumption testable independently of the claim it licenses?
3. Near-perfect internal decodability coexists with a large knowledge-action gap and steering
   indistinguishable from random perturbation [S3]. What would have to hold for "we understand it"
   to imply "we can change it" — and is that implication load-bearing for the field's stated
   goals [S1]?
4. Two verdicts clash: the returns are "roughly nonexistent" [S7], yet the same window produced
   deployed applied results [S16] [S17]. On what measure are both true, and which should a paper
   report?
5. Two studies reached conflicting conclusions on one behavior and a third found both partially
   right but incomparable [S8]. What makes two mechanistic findings comparable at all, and can that
   be settled without a standard the field does not yet have?
6. Interpretability is bought at a stated capability cost with a scaling ceiling [S18], while
   auto-interp scores fail to separate trained from random networks [S9]. What is the exchange rate
   between understandability and capability, and who should be willing to pay it?

## What counts as DEEP here (taste)

| Naive move | Expert judgment/move | Why (failure prevented) | tier | src |
|---|---|---|---|---|
| Ship a new circuit/feature method that improves a proxy metric on one task. | The rewarded move meets the venue's own bar: state "specific falsifiable hypotheses, and how the evidence provided does and does not support them", or show "clear practical benefits over well-implemented baselines". Recognition signal: a NeurIPS 2025 **Spotlight** went to a result proving the field's own framework vacuous when generalized [S5]. | problematizes-nothing — proxy-metric progress reads incremental in 2026 | L·A | [S14] [S5] |
| Treat a high auto-interpretability or reconstruction score as evidence that real features were recovered. | **Buried (2025-01, rev 2026-01):** the same scores appear on randomly initialized transformers [S9]. Reopening condition, stated there: routine randomized baselines plus targeted measures of feature abstractness. | wrong-result — the metric does not discriminate the thing it is used to claim | L | [S9] |
| Report one circuit, from one extraction, one seed, one input distribution, as *the* mechanism. | **Buried (2025-10 → 2026-06):** effects are volatile random variables [S4]; structure-to-function is many-to-one [S23]. Reopening condition: edge-level evaluation plus cross-condition transfer tests. | wrong-result — a single-draw circuit is an unreported sample from an equivalence class | L | [S4] [S23] |

> **Science-vs-application, as this field draws it:** unusually, it prints BOTH bars in one
> sentence [S14] — a falsifiable mechanistic claim, or a demonstrated practical benefit over strong
> baselines. What clears neither is a method with a better proxy score and no falsifiable
> hypothesis attached [S9] [S22].

## Critical rules (execution · eval · validity)

| Naive move | Expert judgment/move | Why (failure prevented) | tier | src |
|---|---|---|---|---|
| Report a circuit from one seed/hyperparameter/input set. | Designing the run: sample across seeds, hyperparameters and input distributions; report the distribution and stability metrics, not the modal circuit. | wrong-result — single-config circuits are unstable | L | [S4] |
| Read structural difference between two circuits as two mechanisms. | Before claiming distinct mechanisms: run edge-level evaluation and cross-condition transfer; source-level evaluation inflates apparent faithfulness. | wrong-result — phantom specialization | L | [S23] |
| Use attribution patching scores as ground truth at scale. | When approximating: screen with a reliability score and correct the leading term; expect downstream non-linearity, not local curvature, to dominate the error. | wrong-result — the evidence for the circuit is itself mis-specified | L | [S19] |
| Validate an interpretation with a freely-parameterized alignment map. | Stating the claim: fix and declare the map class, and make the encoding assumption explicit — unconstrained maps hit 100% interchange-intervention accuracy on randomly initialized models. | wrong-result — a perfect fit that means nothing | L | [S5] |
| Use a raw SAE latent as a classifier or steering target. | Choosing the unit: benchmark against difference-in-means and a prompting ceiling before claiming a latent works; expect absorption to make single latents unreliable where features are hierarchical. | wrong-result — the raw-latent verdict is the field's default prior | L | [S31] [S30] |
| Read a crosscoder model-diff at face value. | Diffing two models: use BatchTopK rather than L1 and presence-test any "unique to the fine-tune" latent — the artifact is a property of the loss. | wrong-result — the loss fabricates unique-to-finetune latents | L | [S34] |
| Score SAE/dictionary features against nothing. | Choosing the comparison: benchmark against non-featurized hidden vectors (neurons) and supervised DAS on MIB's tracks. | wrong-result — featurization may add zero | L | [S10] |
| Report auto-interp scores as the validity evidence. | Reporting: add a randomized-transformer arm; treat aggregate auto-interp as a proxy, never as recovery evidence. | wrong-result — untrained networks pass | L | [S9] |
| Claim a steering result from a mean effect at one coefficient. | Reporting steering: give the per-sample distribution and the behaviors where it fails; effect sizes "vary across samples and are unreliable for many target behaviors". | wrong-result — the mean hides the failure regime | L | [S20] |
| Call a CoT unfaithful because it omits a hint that changed the answer. | Judging traces: separate unfaithfulness from incompleteness, and pair hint-based metrics with causal mediation. | wrong-result — the metric over-reports | L | [S13] [S12] |
| Claim interpretability *enables* correction because the information is decodable. | Closing the loop: measure output-level correction AND collateral disruption of already-correct cases, against a random-perturbation control. | wrong-result — decodability ≠ actionability | L | [S3] |

## Decision guide

- **Which primitive for which question:** components and their interactions → circuit localization
  (attribution / mask optimization lead on MIB); an interpretable variable inside a hidden vector →
  causal variable localization (supervised DAS leads; SAE features do not beat neurons) [S10].
- **Post-hoc vs trained-for-interpretability:** post-hoc buys you the deployed model; weight-sparse
  training buys understandability at a capability cost and stops scaling in the tens of millions of
  nonzero parameters [S18].
- **Auditing claims:** in the reference blinded protocol, three of four teams succeeded, leaning on
  several technique families together rather than interpretability alone [S17].
- **Weighing sources:** most 2026 frontier results here are unreviewed preprints; the peer-reviewed
  anchors are [S5] (NeurIPS 2025 Spotlight), [S10] (ICML 2025), [S22] (BlackboxNLP 2025).

## Ground rules (known-lane — terse)

- Activation patching = the gold-standard causal metric; attribution patching = its first-order,
  gradient-based approximation, adopted for cost [S19].
- A "circuit" is a subgraph claimed to explain a behavior on a sub-distribution; the contrasting
  framing asks instead whether a single weight can be understood globally [S2].
- Attribution graphs are computed on a replacement model that "incompletely and imperfectly
  captures the original", so they yield hypotheses, not conclusions [S11].
- Interchange-intervention accuracy is a fit statistic, meaningful only relative to a declared map
  class [S5].
- Monitorability ≠ faithfulness: a trace can be faithful and still omit factors a monitor needs [S12].

## Reference documentation

- **[volatile.md](volatile.md)** — dated frontier numbers, lane-occupancy flags, and per-source
  review status. Re-check this FIRST before any novelty verdict or write-up.

## Candidate lane  ⚠️ (expert to resolve — NOT verified)

- ⚠️ **The crowded list is still not exhaustive.** Every lane flagged here has now been
  saturation-checked and ALL came back occupied (all are listed above). No flagged lane remains open.
  **Treat any lane this map does not mention as unchecked, not open, and search before committing —
  the measured base rate for unchecked lanes in this forge is 11/11 occupied.**
- ⚠️ **The actionability negative result [S3] is one clinical domain, one model family.** It is the
  strongest published statement of the knowledge-action gap, but generalization beyond triage
  vignettes is unverified. Confirm/refute: a replication in a non-clinical task with the same
  four-method comparison.
- ⚠️ **No peer-reviewed field-wide SURVEY was fetched** (a 2026 ACM Computing Surveys entry exists
  but was access-gated), and nothing independently confirms other labs made the same call as [S6].
  Individual claims are well-anchored — seven sources here are peer-reviewed — but a field-wide
  "the field holds X" statement still lacks a survey to rest on.
```

### [4] SKILL-INPUT — aii-web-tools · 2026-08-12 12:54:08 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: free-first web search (general or scholarly, Serper fallback), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
