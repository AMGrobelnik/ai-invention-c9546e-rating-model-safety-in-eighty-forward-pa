# review_hypo — create_idea

> Phase: `hypo_loop` · round 1 · `review_hypo`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `review_hypo` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-12 12:43:59 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_1/review_hypo
```

### [2] SYSTEM-USER prompt · 2026-08-12 12:44:05 UTC

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

STEP 3 — H↔H EDGE:
This is the first iteration — there is no previous hypothesis. Leave
``relation_type`` null and ``relation_rationale`` empty.

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

### [3] HUMAN-USER prompt · 2026-08-12 12:44:06 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] ASSISTANT · 2026-08-12 12:44:10 UTC

```
I'll ground this review in the literature before writing it.
```

### [5] TOOL CALL — Skill · 2026-08-12 12:44:10 UTC

```
aii-handbook-auto-mechanistic-interpretability
```

### [6] TOOL RESULT — Skill · 2026-08-12 12:44:10 UTC

```
{"success": true, "commandName": "aii-handbook-auto-mechanistic-interpretability"}
```

### [7] TOOL CALL — Bash · 2026-08-12 12:44:10 UTC

```
List user uploads:
ls -la /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads 2>/dev/null | head -50
```

### [8] TOOL RESULT — Bash · 2026-08-12 12:44:10 UTC

```
{"stdout": "total 1954\ndrwxr-xr-x 2 root root       1 Aug 12 12:34 .\ndrwxr-xr-x 7 root root 2000139 Aug 12 12:34 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-08-12 12:44:16 UTC

```
Read volatile.md:
cat /ai-inventor/.claude/skills/aii-handbook-auto-mechanistic-interpretability/volatile.md 2>/dev/null | head -200
```

### [10] TOOL RESULT — Bash · 2026-08-12 12:44:16 UTC

```
{"stdout": "# Volatile — aii-handbook-auto-mechanistic-interpretability   (fact half-life ≈ 3 months)\n\nThe Frontier tier decays fastest. Re-verify the primary source before relying on any of these in a\nnovelty verdict or a write-up. `as_of` = the source's own date, not the date you read this.\n\n## Lane-occupancy flags (novelty-critical — these read \"open\" to an unprimed searcher)\n\n- **Per-weight global interpretation is now OCCUPIED (thinly).** [\"whether a single weight can be understood globally across the full training distribution\"](https://arxiv.org/abs/2607.02964) — `as_of: 2026-07` · `applies-to: weight-sparse + dense transformers, 4 models` — [S2].\n  supersession: behavior-scoped circuit finding was the only framing → a global per-parameter framing now exists. re-verify: search \"per-weight / global weight interpretation transformer <year>\" before claiming it open.\n- **The AxBench \"SAEs are not competitive\" verdict is CONTESTED, not settled.** [\"Sparse Autoencoders can, in fact, perform close to on par with the reference LoRA performance on the AxBench benchmark, when features are selected and labelled with our supervised pipeline\"](https://arxiv.org/abs/2605.31183) — `as_of: 2026-05` · `applies-to: AxBench steering, supervised feature-selection pipelines` — [S25]. Unreviewed preprint; the raw-latent loss still stands.\n- **Attribution-patching unreliability is DIAGNOSED AND FIXED in-paper.** [\"the dominant error stems from the non-linearities in the downstream network rather than local curvature at the patched component\"](https://arxiv.org/abs/2606.09899) — `as_of: 2026-06` — [S19]. Proposing \"attribution patching may be unreliable\" as a finding re-treads this.\n\n## Point-in-time numbers (do not quote as current without re-fetching)\n\n- Attribution graphs give satisfying insight on [\"a quarter of the prompts we've tried\"](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) — `as_of: 2025-03` · `applies-to: Claude 3.5 Haiku + that replacement model` — [S11].\n- Knowledge–action gap: [\"SAE feature steering produced zero effect despite 3,695 significant features.\"](https://arxiv.org/abs/2603.18353) — `as_of: 2026-03` · `applies-to: Qwen 2.5 7B Instruct + Steerling-8B, clinical triage vignettes` — [S3]. One domain; treat as a strong existence proof, not a rate.\n- Weight-sparse interpretability ceiling: [\"scaling sparse models beyond tens of millions of nonzero parameters while preserving interpretability remains a challenge\"](https://arxiv.org/abs/2511.13653) — `as_of: 2025-11` — [S18]. re-verify: this is the number most likely to have moved.\n- MIB leaderboard verdict: [\"the supervised DAS method performs best, while SAE features are not better than neurons, i.e., non-featurized hidden vectors\"](https://arxiv.org/abs/2504.13151) — `as_of: 2025-04` · `applies-to: MIB causal-variable track` — [S10]. The leaderboard is explicitly still open [S22], so this ordering can change.\n\n## Peer-review status of load-bearing preprints (re-check for published versions)\n\n- **[S5] Non-Linear Representation Dilemma — PUBLISHED (NeurIPS 2025 Spotlight)** (`as_of: 2025-11`). The most stable anchor here; decays slowly.\n- **[S10] MIB — PUBLISHED (ICML 2025, PMLR v267)**; **[S22] BlackboxNLP 2025 — PUBLISHED (proceedings)**.\n- **[S3] Interpretability without actionability — arXiv preprint** (`as_of: 2026-03`); load-bearing for the knowledge-action gap. Search for a venue acceptance before citing as established.\n- **[S4] Variance analysis · [S23] Many Circuits, One Mechanism · [S19] When Attribution Patching Lies — arXiv preprints** (`as_of: 2025-10 / 2026-06 / 2026-06`); jointly load-bearing for the stability critique. Prefer published versions once they appear.\n- **[S25] SAE steering rebuttal · [S20] Steering-vector unreliability — unreviewed preprints, one/two authors.** Cite as contested positions, never as settled results.\n- **[S6] lab-team post · [S7] editorial critique · [S15] CEO essay — none peer-reviewed.** These are evidence of stated positions and decisions, not of technical facts.\n\n## Field-calendar items (stale within one cycle)\n\n- ICML 2026 Mechanistic Interpretability Workshop is the venue whose stated bar is quoted in the\n  taste section [S14] — `as_of: 2026`. Re-check the current year's CFP before treating the wording\n  as the field's standing norm.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Skill · 2026-08-12 12:44:20 UTC

```
aii-web-tools
```

### [12] TOOL RESULT — Skill · 2026-08-12 12:44:20 UTC

```
{"success": true, "commandName": "aii-web-tools"}
```

### [13] TOOL CALL — ToolSearch · 2026-08-12 12:44:20 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 3}
```

### [14] TOOL RESULT — ToolSearch · 2026-08-12 12:44:20 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 22}
```

### [15] TOOL CALL — WebSearch · 2026-08-12 12:44:24 UTC

```
critical slowing down early warning signals large language model refusal bistability
```

### [16] TOOL CALL — WebSearch · 2026-08-12 12:44:24 UTC

```
hysteresis activation steering refusal direction bistable switch LLM
```

### [17] TOOL RESULT — WebSearch · 2026-08-12 12:44:30 UTC

```
{"query": "critical slowing down early warning signals large language model refusal bistability", "results": [{"tool_use_id": "srvtoolu_01KFFBva4RSNUHK4JRrA7Tcj", "content": [{"title": "Critical Slowing Down in a Real Physical System", "url": "https://arxiv.org/pdf/2403.17973"}, {"title": "Early warning signal for interior crises in excitable systems", "url": "https://arxiv.org/pdf/1711.04594"}, {"title": "Exploring the role of the potential surface in the behaviour of early warning signals", "url": "https://www.medrxiv.org/content/10.1101/2022.08.12.22278717.full.pdf"}, {"title": "Evaluating the consequences: Impact of sex-selective harvesting on fish   population and identifying tipping points via life-history parameters", "url": "https://arxiv.org/pdf/2401.16255"}, {"title": "Overlapping Time Scales Obscure Early Warning Signals of the Second COVID-19 Wave", "url": "https://www.medrxiv.org/content/10.1101/2021.07.27.21261226.full.pdf"}, {"title": "Early Warning Signals in Ecological Time-Series", "url": "https://doi.org/10.3390/e28060628"}, {"title": "Overlapping timescales obscure early warning signals of the second COVID-19 wave", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8825995/"}, {"title": "Beyond I’m Sorry, I Can’t: Dissecting Large-Language-Model Refusal", "url": "https://arxiv.org/html/2509.09708v1"}, {"title": "Early warning of climate tipping points from critical slowing down: comparing methods to improve robustness | Philosophical Transactions of the Royal Society A | The Royal Society", "url": "https://royalsocietypublishing.org/rsta/article/370/1962/1185/114587/Early-warning-of-climate-tipping-points-from"}]}, "I found search results related to critical slowing down and early warning signals, as well as some work on LLM refusal, but the results don't appear to contain literature specifically connecting all of these concepts together (critical slowing down, early warning signals, large language model refusal, and bistability).\n\nHere's what the search results cover:\n\n**Critical Slowing Down and Early Warning Signals:**\n\nEarly warning signals (EWSs) arise from the theory of critical slowing down (CSD), where as a system approaches a critical transition caused by a zero-eigenvalue bifurcation it becomes slower to recover from small perturbations away from its steady state. Critical slowing down gives rise to three potential early-warning signals in the system's dynamics as it approaches a bifurcation: slower recovery from perturbations, increased autocorrelation, and raised variance.\n\n**Bistability and Flickering:**\n\nIn bistable systems near critical thresholds, stochastic fluctuations may occasionally drive the system across the separatrix into the alternative basin of attraction before returning, producing sporadic excursions visible as \"flickering\" between states, and as the potential barrier between attractors erodes, the frequency distribution may become detectably bimodal.\n\n**LLM Refusal:**\n\nThe search results include one paper on LLM refusal mechanisms, but it doesn't connect to the critical slowing down or bistability concepts.\n\nThe specific intersection of all these topics—applying critical slowing down theory to detect early warning signals of bifurcations in LLM refusal behavior that exhibits bistability—does not appear in these results. This may be a relatively novel or specialized research direction."], "durationSeconds": 7.967697533000003, "searchCount": 1}
```

### [18] TOOL RESULT — WebSearch · 2026-08-12 12:44:32 UTC

```
{"query": "hysteresis activation steering refusal direction bistable switch LLM", "results": [{"tool_use_id": "srvtoolu_01CM9CJkn94CE5EFWhBUr9tq", "content": [{"title": "AlphaSteer: Learning Refusal Steering with Principled Null-Space Constraint", "url": "https://arxiv.org/pdf/2506.07022"}, {"title": "Expert-Aware Refusal Steering", "url": "https://arxiv.org/pdf/2606.04160"}, {"title": "SafeSwitch: Steering Unsafe LLM Behavior via Internal Activation Signals", "url": "https://arxiv.org/html/2502.01042v5"}, {"title": "LLM Steering: From Prompting Tricks to Activation Control - DEV Community", "url": "https://dev.to/iamfaham/llm-steering-from-prompting-tricks-to-activation-control-33d0"}, {"title": "Published as a conference paper at ICLR 2025 PROGRAMMING REFUSAL WITH", "url": "https://proceedings.iclr.cc/paper_files/paper/2025/file/e2dd53601de57c773343a7cdf09fae1c-Paper-Conference.pdf"}, {"title": "Refusal in Language Models Is Mediated by a Single Direction Andy Arditi∗", "url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/f545448535dfde4f9786555403ab7c49-Paper-Conference.pdf"}, {"title": "Palette: A Modular, Controllable, and Efficient Framework for On-demand Authorized Safety Alignment Relaxation in LLMs", "url": "https://arxiv.org/pdf/2605.24154"}, {"title": "Steering Code LLMs with Activation Directions for Language and Library Control", "url": "https://arxiv.org/pdf/2603.23629"}, {"title": "Omni-Safety under Cross-Modality Conflict: Vulnerabilities, Dynamics Mechanisms and Efficient Alignment", "url": "https://arxiv.org/pdf/2602.10161"}]}, "I found several relevant research papers on activation steering and refusal control in LLMs. Here's a summary of the key findings:\n\n## Activation Steering and Refusal Behavior\n\nActivation steering focuses on how to control the behaviors of LLMs by injecting a direction vector into the activations of LLMs. Refusal behaviors have been encoded as linear directions within LLMs.\n\n## Refusal as a Linear Direction\n\nRefusal behavior in LLMs is mediated by a consistent direction in the residual stream latent space. By computing the difference in mean activations between harmful and harmless prompts, the harmless component is removed, isolating a direction that is unique to harmful inputs and refusal behavior.\n\n## Bistable Switch Behavior\n\nA condition vector can represent certain activation patterns induced by the prompt during inference, and a similarity calculation between this condition vector and the model's activation effectively serves as a switch, determining whether to apply the refusal vector. This provides a form of conditional, context-dependent control over refusal behavior.\n\n## Applications and Recent Work\n\nRecent research includes methods like SafeSwitch, which monitors internal states and activates the refusal head upon unsafe generations are predicted, enhancing model safety and maintaining utility. Additionally, current methods adopt two main paradigms: vector calibration and conditional steering.\n\nThe research demonstrates that hysteresis-like effects and bistable switching mechanisms can be achieved through careful control of activation steering directions during inference."], "durationSeconds": 9.456831121000002, "searchCount": 1}
```

### [19] TOOL CALL — WebSearch · 2026-08-12 12:44:42 UTC

```
"safety basin" LLM safety landscape VISAGE metric fine-tuning perturbation NeurIPS
```

### [20] TOOL CALL — WebSearch · 2026-08-12 12:44:42 UTC

```
predict LLM refusal rate without harmful benchmark internal activations cheap safety metric open-weight checkpoint
```

### [21] TOOL RESULT — WebSearch · 2026-08-12 12:44:46 UTC

```
{"query": "\"safety basin\" LLM safety landscape VISAGE metric fine-tuning perturbation NeurIPS", "results": [{"tool_use_id": "srvtoolu_01Mt7MhGnHaPcz7qMN5mvGvG", "content": [{"title": "NeurIPS Poster Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models", "url": "https://neurips.cc/virtual/2024/poster/95896"}, {"title": "VISAGE safety metric : Measuring Risks in finetuning LLMs | by SACHIN KUMAR | Medium", "url": "https://medium.com/@techsachin/visage-safety-metric-measuring-risks-in-finetuning-llms-0ccbdceafbb5"}, {"title": "Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models for NeurIPS 2024 - IBM Research", "url": "https://research.ibm.com/publications/navigating-the-safety-landscape-measuring-risks-in-finetuning-large-language-models"}, {"title": "Curvature-Aware Safety Restoration In LLMs Fine-Tuning", "url": "https://arxiv.org/pdf/2511.18039"}, {"title": "Navigating the Safety Landscape: Measuring Risks in", "url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/ada93fa6643735f294be51dc31eebbd4-Paper-Conference.pdf"}, {"title": "Navigating the Safety Landscape: Measuring Risks in", "url": "https://arxiv.org/pdf/2405.17374"}, {"title": "Navigating the safety landscape | Proceedings of the 38th International Conference on Neural Information Processing Systems", "url": "https://dl.acm.org/doi/10.5555/3737916.3740948"}, {"title": "Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models — Anthony Peng", "url": "https://shengyun-peng.github.io/papers/llm-safety-landscape"}, {"title": "Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models | OpenReview", "url": "https://openreview.net/forum?id=GZnsqBwHAG&noteId=YTphump4UQ"}, {"title": "[2405.17374] Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models", "url": "https://arxiv.org/abs/2405.17374"}]}, "Based on the search results, here's what I found about this research topic:\n\n## Safety Basin and VISAGE Metric\n\nA new phenomenon termed \"safety basin\" has been discovered in the model parameter space of popular open-source LLMs, where random perturbations to model weights maintain the safety level of the original aligned model within its local neighborhood. However, outside this local region, safety is fully compromised, exhibiting a sharp, step-like drop.\n\nThis safety basin contrasts sharply with the LLM capability landscape, where model performance peaks at the origin and gradually declines as random perturbation increases.\n\n## VISAGE Safety Metric\n\nThe discovery inspired the proposal of a new VISAGE safety metric that measures the safety in LLM finetuning by probing its safety landscape. VISAGE is the acronym for volumetric index for safety alignment guided by explanation.\n\n## Key Findings\n\nThe safety basin is evident in both 1D and 2D safety landscape of LLaMA2, LLaMA3, Vicuna, and Mistral across various random directions and different safety benchmarks.\n\nLLM safety landscape also highlights the system prompt's critical role in protecting a model, and that such protection transfers to its perturbed variants within the safety basin.\n\nThis research was presented at NeurIPS 2024."], "durationSeconds": 6.517092091000006, "searchCount": 1}
```

### [22] TOOL RESULT — WebSearch · 2026-08-12 12:44:50 UTC

```
{"query": "predict LLM refusal rate without harmful benchmark internal activations cheap safety metric open-weight checkpoint", "results": [{"tool_use_id": "srvtoolu_01KMvGKbgUiu7j11SxUh6h12", "content": [{"title": "SafeSwitch: Steering Unsafe LLM Behavior via Internal Activation Signals", "url": "https://arxiv.org/html/2502.01042"}, {"title": "RefusalBench: LLM Refusal Misranking in Bio Research", "url": "https://www.emergentmind.com/papers/2605.21545"}, {"title": "From hallucinations to hazards: benchmarking LLMs for hazard analysis in safety-critical systems - ScienceDirect", "url": "https://www.sciencedirect.com/science/article/pii/S0925753525002814"}, {"title": "RAS: Measuring LLM Safety Through Refusal Alignment", "url": "https://arxiv.org/html/2606.25750"}, {"title": "SafeConstellations: Mitigating Over-Refusals in LLMs Through Task-Aware Representation Steering", "url": "https://arxiv.org/html/2508.11290v4"}, {"title": "Guiding Giants: Lightweight Controllers for Weighted Activation Steering in LLMs", "url": "https://arxiv.org/pdf/2505.20309"}, {"title": "The Refusal--Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models", "url": "https://arxiv.org/pdf/2605.05427"}, {"title": "Expert Personas Improve LLM Alignment but Damage Accuracy: Bootstrapping Intent-Based Persona Routing with PRISM", "url": "https://arxiv.org/pdf/2603.18507"}, {"title": "The Refusal–Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models", "url": "https://arxiv.org/html/2605.05427"}]}, "I found several relevant research papers on this topic. Here are the key findings from the search results:\n\n## Internal Activation-Based Safety Metrics\n\nOne approach uses representation-level refusal alignment to create a metric called RAS (Refusal Alignment Score), which maps representation-level refusal alignment to a calibrated 0–100 safety score. This research asks whether safety can be evaluated earlier, at the representation level, rather than through expensive output-level evaluation.\n\n## Why Internal Activations Matter\n\nOutput-level evaluation is expensive because each prompt requires generation and often a second judge model, the result depends on decoding parameters and refusal templates, and benchmarks can become stale as models are trained against known question banks. Output-level safety is a late-stage behavioral signal that measures whether a model ultimately refuses or complies, but does not reveal whether the model internally recognizes a request as unsafe.\n\n## Research on Refusal Behavior\n\nOne study found that LLMs integrated with a safety method demonstrate approximately an 80% reduction in harmful outputs on safety benchmarks including SORRY-Bench and TrustLLM. Additionally, across 21 evaluated open-weight models, over-refusal and harmful compliance are nearly uncorrelated, meaning a model's refusal rate provides essentially no information about its adversarial vulnerability.\n\nThe research suggests that predicting LLM refusal rates through internal activation analysis offers a potentially cheaper, more efficient alternative to running full harmful benchmarks while providing insights into whether models genuinely understand safety-related concepts."], "durationSeconds": 8.577737916999999, "searchCount": 1}
```

### [23] TOOL CALL — WebSearch · 2026-08-12 12:45:24 UTC

```
Messenger "Detecting Safety Training Modification in Language Models via Activation Analysis" IEEE Access
```

### [24] TOOL CALL — WebSearch · 2026-08-12 12:45:24 UTC

```
"critical slowing down" OR "early warning signals" applied to neural network transformer internal dynamics tipping point 2025 2026
```

### [25] TOOL RESULT — WebSearch · 2026-08-12 12:45:30 UTC

```
{"query": "Messenger \"Detecting Safety Training Modification in Language Models via Activation Analysis\" IEEE Access", "results": [{"tool_use_id": "srvtoolu_01Cdq2L5TiRp8DBN3ALrp8ux", "content": [{"title": "Detecting Safety Training Modification in Language Models via Activation Analysis", "url": "https://arxiv.org/html/2608.05578"}, {"title": "Detecting Safety Training Modification in Language Models ...", "url": "https://arxiv.org/pdf/2608.05578"}, {"title": "[2608.05578] Detecting Safety Training Modification in Language Models via Activation Analysis", "url": "https://arxiv.org/abs/2608.05578"}, {"title": "Anti abuse", "url": "https://research.google/research-areas/anti-abuse/"}, {"title": "Steering MoE LLMs via Expert (De)Activation", "url": "https://arxiv.org/html/2509.09660v1"}, {"title": "Data Augmentation for Messenger Phishing Detection Using Large Language Models | IEEE Conference Publication | IEEE Xplore", "url": "https://ieeexplore.ieee.org/document/10879623"}, {"title": "Steering Awareness: Detecting Activation Steering from Within", "url": "https://arxiv.org/pdf/2511.21399"}, {"title": "GAVEL: Towards Rule-Based Safety Through Activation Monitoring", "url": "https://arxiv.org/pdf/2601.19768"}, {"title": "Model-Editing-Based Jailbreak against Safety-aligned Large Language   Models", "url": "https://arxiv.org/pdf/2412.08201"}]}, "I found the research paper you're looking for. Here are the key details:\n\n**Title:** \"Detecting Safety Training Modification in Language Models via Activation Analysis\"\n\n**Author:** Glen Messenger from Google Cloud, Google LLC\n\n**Publication:** IEEE Access, vol. 14, pp. 91723–91737, 2026, doi:10.1109/ACCESS.2026.3704057\n\n**Overview:** The paper introduces AMS (Activation-based Model Scanner), a tool that detects modifications to safety training in language models by measuring the geometric structure of safety-relevant concepts in activation space. Safety training creates measurable separation between harmful and benign content classes; certain safety modifications collapse or rotate this structure, while others leave it intact.\n\n**Validation:** The research validates AMS across 14 model configurations spanning 4 architecture families (Llama, Gemma, Qwen, Mistral) and four safety-modification categories (instruction-tuned, base, abliterated, uncensored fine-tunes), with leave-one-out cross-validation achieving 71% accuracy.\n\nThe paper is available on arXiv and IEEE Access."], "durationSeconds": 6.780647765000001, "searchCount": 1}
```

### [26] TOOL RESULT — WebSearch · 2026-08-12 12:45:32 UTC

```
{"query": "\"critical slowing down\" OR \"early warning signals\" applied to neural network transformer internal dynamics tipping point 2025 2026", "results": [{"tool_use_id": "srvtoolu_01E6Mya8HLvGeCb9HYTAPd5v", "content": [{"title": "Identifying early-warning signals of critical transitions with strong noise by dynamical network markers | Scientific Reports", "url": "https://www.nature.com/articles/srep17501"}, {"title": "Baseline-referenced spatial early warning signals for tipping points on heterogeneous networks", "url": "https://arxiv.org/html/2608.06608"}, {"title": "Critical Slowing Down in a Real Physical System", "url": "https://arxiv.org/pdf/2403.17973"}, {"title": "(PDF) Deep learning for early warning signals of tipping points", "url": "https://www.researchgate.net/publication/354718209_Deep_learning_for_early_warning_signals_of_tipping_points"}, {"title": "Choosing observables that capture critical slowing down before tipping points: A Fokker-Planck operator approach | Phys. Rev. E", "url": "https://journals.aps.org/pre/abstract/10.1103/l2v2-xndy"}, {"title": "Robustness and resilience of dynamical networks in biology and epidemiology", "url": "https://arxiv.org/pdf/2512.01462"}, {"title": "Ultra-Early Prediction of Tipping Points: Integrating Dynamical Measures with Reservoir Computing", "url": "https://arxiv.org/pdf/2603.14944"}, {"title": "Anticipating Tipping Points for Disordered Traffic: Critical Slowing   Down on the Onset of Congestion", "url": "https://arxiv.org/pdf/2401.09364"}, {"title": "Early Warnings for Multistage Transitions in Dynamics on Networks", "url": "https://arxiv.org/pdf/2208.08961"}, {"title": "Detecting and distinguishing tipping points using spectral early warning signals", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7536046/"}]}, "Based on the search results, I found relevant research on critical slowing down and early warning signals, with some specific findings about transformers and neural networks. Here are the key findings:\n\n## Critical Slowing Down and Early Warning Signals\n\nMany early warning signals are based on critical slowing down: as a dynamical system approaches a bifurcation, its recovery from small perturbations becomes slower. Critical slowing down results in predictable signatures in time series data, including increasing variance and autocorrelation, and it is these signatures that are used to construct early warning signals.\n\n## Transformers and Tipping Point Prediction\n\nA particularly relevant finding concerns transformer architectures' ability to detect tipping points. When testing if transformers can capture catastrophic collapse (which occurs when a bifurcation parameter crosses a critical threshold), models trained on trajectories in normal parameter regimes and tested on parameters in an unseen regime with system collapse show that transformers, across configurations, consistently fail to capture collapse, while reservoir computing reliably predicts the transitions. This surprising finding raises questions about the generalization ability of transformers to dynamical systems, a topic warranting future research.\n\n## Current Research Approaches\n\nCritical slowing down is an avenue for predicting tipping points in real-world systems, which is a decrease in the relaxation rate after perturbations prior to a tipping point that can be measured by statistical early warning signals in the autocovariance of observational time series.\n\nThe research suggests this is an active and evolving field, with ongoing efforts to improve detection methods and understanding of how different machine learning architectures perform for tipping point prediction."], "durationSeconds": 7.9864146489999985, "searchCount": 1}
```

### [27] TOOL CALL — WebFetch · 2026-08-12 12:45:42 UTC

```
URL: https://arxiv.org/abs/2606.25750
Prompt: Summarize: what is RAS? How is the refusal alignment score computed, does it need harmful prompts, how many models evaluated, what correlation with behavioral refusal rate is reported?
```

### [28] TOOL CALL — WebSearch · 2026-08-12 12:45:42 UTC

```
LLM refusal "phase transition" OR "tipping point" OR "bifurcation" internal representation safety 2026
```

### [29] TOOL RESULT — WebFetch · 2026-08-12 12:45:46 UTC

```
{"bytes": 41478, "code": 200, "codeText": "OK", "result": "# RAS: Refusal Alignment Score Summary\n\n**What is RAS?**\nRAS (Refusal Alignment Score) is a white-box safety evaluation metric for large language models that measures safety through internal representations rather than generated outputs. It produces a calibrated 0-100 safety score.\n\n**How is it Computed?**\nThe methodology involves three steps: extracting layer-wise refusal directions from a safety-aligned reference model, identifying stable layer windows where safe and unsafe behaviors are distinguishable, and scoring target models by measuring \"whether its hidden states align with these refusal directions under unsafe and jailbreak prompts.\"\n\n**Does it Need Harmful Prompts?**\nYes. The approach requires unsafe and jailbreak prompts to evaluate alignment in the target model's hidden states.\n\n**Models Evaluated?**\nThe paper tested across three model families: Llama, Gemma, and Qwen, comparing aligned models against uncensored and abliterated variants.\n\n**Correlation with Behavioral Refusal?**\nThe abstract indicates RAS \"tracks output-level attack success rate\" and is \"substantially faster than judge-based evaluation,\" suggesting positive correlation with behavioral refusal metrics, though specific correlation coefficients aren't detailed in this excerpt.", "durationMs": 4767, "url": "https://arxiv.org/abs/2606.25750"}
```

### [30] TOOL RESULT — WebSearch · 2026-08-12 12:45:50 UTC

```
{"query": "LLM refusal \"phase transition\" OR \"tipping point\" OR \"bifurcation\" internal representation safety 2026", "results": [{"tool_use_id": "srvtoolu_01AG7h8xTzC66LuVpX627i4Q", "content": [{"title": "The Geometry of Refusal: Linear Instability in Safety-Aligned LLMsAccepted at TrustNLP 2026, the Sixth Workshop on Trustworthy Natural Language Processing, co-located with ACL 2026.", "url": "https://arxiv.org/html/2606.22686v1"}, {"title": "The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs", "url": "https://arxiv.org/html/2606.22686"}, {"title": "[2606.22686] The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs", "url": "https://arxiv.org/abs/2606.22686"}, {"title": "Instruction Tuning-Based Refusal", "url": "https://www.emergentmind.com/topics/instruction-tuning-based-refusal"}, {"title": "Rebuilding LLMs Safety Mechanism via Probabilistically ...", "url": "https://aclanthology.org/2025.findings-emnlp.956.pdf"}, {"title": "Over-Refusal and Representation Subspaces: A Mechanistic Analysis of Task-Conditioned Refusal in Aligned LLMs", "url": "https://arxiv.org/pdf/2603.27518"}, {"title": "SafeConstellations: Mitigating Over-Refusals in LLMs Through Task-Aware Representation Steering", "url": "https://arxiv.org/pdf/2508.11290"}, {"title": "SteeringSafety: A Systematic Safety Evaluation Framework of Representation Steering in LLMs", "url": "https://arxiv.org/pdf/2509.13450"}, {"title": "SafeConstellations: Mitigating Over-Refusals in LLMs Through Task-Aware Representation Steering", "url": "https://arxiv.org/html/2508.11290v4"}]}, "Based on the search results, I found highly relevant recent research on LLM refusal, phase transitions, and internal representations:\n\n## Key Findings\n\n**Phase Transition in Refusal Mechanisms:**\n\nA recent paper accepted at TrustNLP 2026 demonstrates that when coupled with prefix injection to bypass initial refusal reflexes, a method called Contrastive Logit Steering induces a phase transition where guardrails collapse.\n\n**Internal Representation Analysis:**\n\nResearchers are investigating whether safety compliance is a deep semantic decision or a manipulable linear feature. The mechanistic analysis reveals two distinct safety topologies: \"Late Decision\" models (Llama) where safety divergence occurs only at the final layers, and \"Early Divergence\" models (Qwen) that integrate safety mid-computation and prove substantially more robust.\n\n**Safety as a Linear Feature:**\n\nResearch shows that malicious queries and benign instructions form distinct clusters, demonstrating that safety is encoded as a linear feature in the activation space. Contrastive Logit Steering achieves 95% attack success rate on Llama-3.1 by isolating and removing a \"Refusal Vector\" via simple arithmetic.\n\n**Broader 2026 Research:**\n\nRecent research analyzes mechanistic methods, exploring how internal model representations influence safety behaviors, with representation and latent space steering demonstrating that targeted modifications to activation patterns can dynamically adjust model outputs without retraining or prompt modification."], "durationSeconds": 8.010683293000008, "searchCount": 1}
```

### [31] TOOL CALL — WebSearch · 2026-08-12 12:45:58 UTC

```
"refusal cliff" OR "commitment" autoregressive first tokens refusal self-reinforcing prefill hysteresis path dependence generation
```

### [32] TOOL RESULT — WebSearch · 2026-08-12 12:46:06 UTC

```
{"query": "\"refusal cliff\" OR \"commitment\" autoregressive first tokens refusal self-reinforcing prefill hysteresis path dependence generation", "results": [{"tool_use_id": "srvtoolu_01SFUUhU4TETSH7x78giogNc", "content": [{"title": "Breaking Refusal in the First Half", "url": "https://arxiv.org/pdf/2607.14147"}, {"title": "Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models", "url": "https://arxiv.org/html/2602.02600v3"}, {"title": "Breaking Refusal in the First Half A Mechanistic Study of the Prefill JailbreakCode, data, and the full reproducible experiment ledger: https://github.com/collapseindex/breaking-refusal", "url": "https://arxiv.org/html/2607.14147v1"}, {"title": "Refusal Falls off a Cliff: How Safety Alignment Fails in Reasoning?", "url": "https://arxiv.org/pdf/2510.06036"}, {"title": "Refusal-Aware Instruction Tuning", "url": "https://www.emergentmind.com/topics/refusal-aware-instruction-tuning"}]}, "Here are the search results for your query about \"refusal cliff,\" commitment, autoregressive generation, and related concepts in LLM refusal mechanisms:\n\n## Key Research Findings:\n\n**Refusal Cliff Phenomenon:**\nResearch has identified a \"refusal cliff\" in reasoning models, where hidden states can be probed to estimate a \"refusal score\" at each token position.\n\n**Early Token Commitment in Refusal:**\nSafety alignment appears to be \"shallow\" in token depth, with the refusal decision carried by the first few output tokens, and attacks that get past them tend to succeed. Research has localized the failure to an early multi-token window rather than just a first-token count.\n\n**Autoregressive Conditioning vs. Active Suppression:**\nStudies using base-model controls identify the refusal mechanism as generic autoregressive conditioning, not safety-specific active suppression, with non-safety-tuned base models showing the same prefill-specific collapse. An early window of the response (the first half) restores as much as the whole, while the second half is nearly inert.\n\n**Path Dependence in Generation:**\nIn autoregressive generation, tokens are committed once generated, and harmful tokens can be committed even when the model has high entropy. Autoregressive models expose only the final, committed trajectory, masking the underlying instability entirely.\n\n**Self-Reinforcing Dynamics:**\nRecovery during sampling occurs when harmful tokens generated in earlier steps do not persist to the final response, which requires both that harmful tokens are not committed in earlier steps and that later steps generate harmless tokens instead."], "durationSeconds": 9.610360461999997, "searchCount": 1}
```

### [33] ASSISTANT · 2026-08-12 12:49:18 UTC

```
I have enough grounding. Writing the review.
```

### [34] TOOL CALL — Write · 2026-08-12 12:49:18 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_1/review_hypo/.terminal_claude_agent_struct_out.json

{
  "overall_assessment": "This is one of the more imaginative hypotheses I have reviewed at the pre-flight stage. The core move — replace the field's default static unit (a direction, a feature, a cluster separation) with a *rate*, and import the ecology/climate early-warning-signal (EWS) toolkit to estimate proximity to a comply/refuse tipping point — is a real reframing, not a relabeling, and it is aimed squarely at a documented blind spot (behavioral uncensored fine-tunes that AMS-style activation-geometry scanners cannot see; Messenger, arXiv:2608.05578 / IEEE Access 14:91723-91737, 2026, which I verified — AMS reports 71% leave-one-out accuracy over 14 configs and 4 families). The proposal is unusually well-engineered as a *falsifiable* object: it pre-registers a decisive test (H1 hysteresis), pre-registers the strongest cheap competitor (static mean of r), pre-registers the load-bearing statistic (partial rank correlation controlling for that mean), and pre-registers a clean negative. That is exactly the ICML MI workshop bar ('specific falsifiable hypotheses, and how the evidence provided does and does not support them'). I want this run.\n\nBut as written it would very likely burn its compute for reasons that have nothing to do with whether the underlying idea is true. Two construct-validity problems are close to fatal and must be fixed BEFORE any GPU/CPU time is spent:\n\n(1) **The hysteresis protocol as specified is guaranteed to return zero loop width, by construction, in every checkpoint.** If alpha is swept by running independent generations at alpha = 0, 0.1, 0.2, ..., then back down, the model's response is a deterministic (under greedy decoding) function of alpha alone. There is no state carried from the up-sweep into the down-sweep, so response(alpha) is single-valued and alpha_up = alpha_down identically. Hysteresis requires path dependence, i.e. a state variable that persists across the sweep. In an autoregressive LM the *only* such state is the generated prefix + KV cache. So H1 is only well-posed if alpha is ramped up and back down WITHIN a single generation, with the prefix retained. As written, the 'decisive test' would return a trivially null result that the authors' own success criteria would (incorrectly) read as refuting the tipping-point framing. This is the single highest-impact fix in the review.\n\n(2) **'Token position as time' is not a relaxation axis of an autonomous dynamical system, and CSD theory does not license the indicators over it.** Critical slowing down is a statement about the leading eigenvalue of a linearized *autonomous stochastic* system near a fold. Within one forward pass over a fixed prompt, the decay of an injected perturbation across later positions is dominated by attention dilution (an injected key is one of t keys; influence falls roughly as 1/t regardless of any basin), by RMSNorm rescaling, and by residual-norm growth with depth/position — none of which are the dominant eigenvalue of a comply/refuse dynamics. Worse, the variance and lag-1 autocorrelation of r_t across *prompt* token positions are dominated by token identity (punctuation, function words, chat-template scaffolding), i.e. by deterministic content, not by fluctuations around an attractor. The good news: the fix is the same as for (1). Autoregressive generation with temperature sampling IS a genuine stochastic dynamical system whose state is the sequence; measuring lambda, Var, and AC(1) over *generated* positions across sampled rollouts is theoretically defensible and empirically much more likely to show the predicted ordering.\n\nBeyond those, three further issues would each independently sink the headline claim: an n-problem (n approximately 10 checkpoints, effectively 3-4 independent families, cannot support a rho >= 0.8 claim with a CI that excludes a strong baseline, let alone a partial correlation or leave-one-family-out at n_family = 2-3), a degenerate-ground-truth problem (a trimodal base/instruct/abliterated panel turns a 'rank correlation' into a 3-class classification any trivial detector wins), and a circularity in H2's key contrast (abliteration orthogonalizes writes against the refusal direction, so r_t in an abliterated model is near-constant by construction; low variance and degenerate AC(1) there are an artifact of the readout being surgically destroyed, not evidence about basin depth).\n\nRelated work is well chosen but has real gaps that a reviewer at a top venue will find immediately: RAS (arXiv:2606.25750) is a representation-level, calibrated 0-100 safety score explicitly motivated by 'output-level evaluation is expensive' — that is the same product H3 promises and it is uncited; 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) already frames safety as a *basin* and ships VISAGE, a basin-volume safety metric — the 'shallow basin' language here is not new and must be positioned against it; 'Refusal Falls off a Cliff' (arXiv:2510.06036) already probes a per-token-position refusal score; 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion LMs' (arXiv:2602.02600) already studies commitment/path-dependence in refusal generation and observes that autoregressive decoding 'masks the underlying instability'; and 'Breaking Refusal in the First Half' (arXiv:2607.14147) reports, with base-model controls, that prefill-collapse dynamics are 'generic autoregressive conditioning, not safety-specific active suppression' — which is a pre-registered threat to H1's base-vs-instruct contrast that must be confronted, not discovered mid-run.\n\nMy verdict: the idea deserves the compute, but not this protocol. With the sweep moved inside generation, the time axis moved to sampled rollouts, the panel widened to 25-30 checkpoints with graded ground truth, and the abliteration confound handled by a model-independent readout, this becomes a strong paper whether it confirms or refutes. Without those, a null result will be uninterpretable and a positive result will be unpublishable.",
  "strengths": [
    "Genuinely novel reframing, not new vocabulary for an old method. The field's default unit is a static object (direction, feature, circuit); this proposes a rate, and imports a mature, well-validated toolkit (Scheffer-style EWS: slowed recovery, rising variance, rising lag-1 autocorrelation) that my searches confirm has not been applied to LLM internal state dynamics or safety auditing. The physics import (hysteresis as the decisive test that a switch is bistable rather than merely biased) is the right instinct and is what separates this from a vague 'safety is fragile' claim.",
    "Pre-registered falsifiability at a level rarely seen in pre-flight proposals. H1 is named as decisive; the DISCONFIRMS block commits in advance to reporting refutation rather than salvaging; and — most importantly — the authors identify the *strongest cheap competitor* themselves (the static mean level of r on benign prompts) and make the load-bearing statistic a partial correlation controlling for it. That is precisely the discipline the MI literature is currently faulted for lacking, and it is worth real credit.",
    "The target is a real, documented gap, correctly identified. AMS (Messenger 2026) genuinely reports that behavioral uncensored fine-tunes preserve cluster separation and refusal direction while complying with harmful requests; H4 aims at exactly that blind spot, and does so from the act-side rather than the read-side. This connects cleanly to the sharpest 2026 negative result in interpretability — the knowledge-action gap — and the motivation section makes that connection correctly rather than decoratively.",
    "The deliverable, if it works, is operationally valuable and cheap: a per-checkpoint safety score from a handful of harmless prompts, no harmful content held or transmitted, no reference model, no benchmark to memorize and game. The zero-harmful-prompt (unembedding-axis) variant is a good, honest hardening of that claim, and reporting all headline results under both axis variants is the right call.",
    "The base / safety-tuned / abliterated triple read as a wild-type / knock-in / knock-out series is a clean experimental-genetics framing, and Step 6's question — does abliteration revert to base or produce a third state? — is a genuinely interesting, publishable sub-result even if H3 fails.",
    "Costing and feasibility are realistic and honest (CPU-only, small models, <$2 judge spend), and the assumptions block is unusually candid, including a stated mitigation for degenerate ground truth."
  ],
  "dimension_scores": [
    {
      "dimension": "soundness",
      "score": 2,
      "justification": "The framing is coherent and the statistical plan is thoughtfully pre-registered, but two load-bearing operationalizations do not survive scrutiny: the hysteresis sweep as described has no state variable and is therefore single-valued by construction, and token-position-within-one-forward-pass is not the relaxation axis of an autonomous dynamical system that CSD theory requires. Add a severe power deficit (n approximately 10, effectively 3-4 independent families) against a headline claim that needs a bootstrap CI to exclude a strong baseline, a trimodal ground truth that makes the rank correlation nearly vacuous, and a confound that makes H2's abliterated arm circular, and the current design cannot deliver an interpretable verdict either way. All of these are fixable pre-flight, which is why this is a 2 and not a 1.",
      "improvements": [
        "Redefine the H1 sweep as a within-generation ramp: hold one benign prompt, generate autoregressively while raising alpha per step until a refusal onset token appears, then lower alpha per step while RETAINING the generated prefix and KV cache, and record the alpha at which the model returns to compliant continuation. Loop width = alpha_up - alpha_down is then well-posed because the prefix is the state variable. Include a shuffled-control arm (reset the prefix between steps) which must give zero width — that control is what proves the loop is path dependence and not noise.",
        "Move the H2 time axis from prompt-token position inside one forward pass to autoregressive generation steps under temperature sampling. Inject the epsilon perturbation at generation step p, continue decoding, and fit the exponential decay of |delta r_t| over subsequent GENERATED steps, averaged over >= 20 rollouts per prompt. Compute Var(r_t) and AC(1) on the sampled rollout trajectories. This makes the dynamical-system analogy defensible rather than metaphorical, and it is the only version of the measurement a physics- or ecology-literate reviewer will accept.",
        "Add the three null controls that make lambda interpretable: (i) a random-direction readout axis instead of the refusal axis — lambda on a random axis must NOT show the safety ordering; (ii) a random-vector perturbation vs a refusal-axis-aligned perturbation; (iii) an attention-dilution baseline, i.e. lambda measured on a purely syntactic observable (e.g. projection onto a part-of-speech probe direction), which should decay at the same rate if what you are measuring is generic mixing rather than a basin.",
        "Fix the abliteration circularity. Abliteration orthogonalizes the write matrices against the refusal direction, so r_t is near-constant in abliterated models by construction and its variance/AC(1) are degenerate for trivial reasons. Either (a) report all indicators on a readout axis that is NOT the abliterated direction (e.g. the logit-lens log-odds of refusal-onset tokens, which survives the edit), or (b) z-score r_t within model before computing Var and AC(1) and state explicitly that the variance claim is scale-free, or preferably both. Without this, criterion (2) of CONFIRMS is unfalsifiable.",
        "Make r_t commensurable across models. A per-model diff-in-means axis has arbitrary scale and the residual stream norm differs by an order of magnitude across families and layers. Standardize r_t (unit-norm axis, and z-scored r within model over the benign prompt set) before any cross-model comparison, and report that lambda is invariant to that normalization.",
        "Report an explicit power analysis in the plan. At n = 10 the 95% bootstrap CI on an observed Spearman rho = 0.8 spans roughly [0.3, 0.95]; a partial correlation at n = 10 with one covariate has almost no power; leave-one-family-out at 3 families is n = 2. State the n needed for the pre-registered CI-exclusion criterion to be attainable and scale the panel to it."
      ]
    },
    {
      "dimension": "presentation",
      "score": 3,
      "justification": "Exceptionally clear and well organized for a pre-flight hypothesis: four numbered sub-claims, an explicit decisive test, a terms glossary, pre-registered baselines, and a genuinely honest DISCONFIRMS block. The related-works entries are substantive rather than perfunctory — each states what the prior work does and where this departs. Deductions are for gaps in prior-art coverage (several close works uncited) and for a few places where the metaphor is asserted where a definition is needed.",
      "improvements": [
        "Cite and position against the five works my searches surfaced that are missing: RAS (arXiv:2606.25750, representation-level calibrated safety score, same product claim as H3); 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374, which already introduces the safety BASIN and the VISAGE basin-volume metric — the 'shallow basin' language is not new); 'Refusal Falls off a Cliff' (arXiv:2510.06036, per-token-position refusal score probing); 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion LMs' (arXiv:2602.02600, commitment and path-dependence in refusal decoding); and 'Breaking Refusal in the First Half' (arXiv:2607.14147, base-model controls attributing prefill collapse to generic autoregressive conditioning). One sentence each on the departure is enough, but their absence is currently the most visible reviewer-facing weakness after the two design flaws.",
        "Give RRI an explicit, fixed formula in the hypothesis text rather than 'a simple function of (lambda, variance, lag-1 AC)'. State the exact combination and the exact standardization, and state it BEFORE the run. 'Fixed a priori' is only credible if the reader can see the fixed thing. A defensible default: RRI = mean of the within-panel z-scores of (-lambda), log Var, and Fisher-z(AC1).",
        "Fix the naming asymmetry: 'Refusal Resilience Index' reads as 'how resilient refusal is', but the construct is the opposite — a HIGH RRI is meant to indicate a SHALLOW basin, i.e. LOW resilience of the comply state. Rename (e.g. 'Refusal Proximity Index') or state the sign convention in the definition; as written it will be misread in every table caption.",
        "State the layer/position selection protocol as a pre-registration, not a sweep. 'Sweep layer L' plus 'report the best' is a garden of forking paths across a 10-model panel. Fix L by a stated rule (e.g. the layer maximizing harmful/benign separation on a held-out contrast set of the REFERENCE model only) and report the full layer profile as secondary."
      ]
    },
    {
      "dimension": "contribution",
      "score": 3,
      "justification": "High-ceiling and genuinely original in framing. A confirmed result gives a mechanistic account of safety tuning in the language of bistable systems plus a cheap, ungameable, harmful-content-free auditing metric that works where the published static scanner is documented to fail; a clean negative ('safety is a static bias, not a shifted operating point') is itself a publishable extension of the knowledge-action-gap literature with a dynamical arm. The ceiling is capped, though, by the model panel (0.6B-1.7B, 2-3 families, smaller than the 14-config/4-family panel of the AMS work it aims to beat) and by the risk that H1's contrast is explained by generic autoregressive conditioning rather than anything safety-specific.",
      "improvements": [
        "Widen the panel to >= 25 checkpoints spanning a GRADED range of refusal rates, not three discrete classes. Candidates that remain CPU-feasible: Qwen2.5-0.5B/1.5B-Instruct, SmolLM2-360M/1.7B-Instruct, Llama-3.2-1B/3B-Instruct, gemma-2-2b-it, TinyLlama-1.1B-Chat, Phi-3-mini, plus their abliterated and Dolphin/Josiefied-style uncensored variants, plus deliberately partially-de-aligned checkpoints (a few hundred steps of LoRA on compliant data, several strengths) to fill the middle of the range. Without intermediate refusal rates, a Spearman rho over a trimodal panel is a 3-class discrimination that a one-line 'does it ever emit an apology token' baseline will also win at rho ~ 1, which makes criterion (3) uninformative even if it passes.",
        "Beat AMS on AMS's own terms, or say why not. AMS validates on 14 configs across 4 families with leave-one-out at 71%. Reporting a metric on 10 checkpoints across 2-3 families cannot claim to supersede it. Add at least a fourth family (Gemma or Mistral) and report the same leave-one-out accuracy figure alongside the rank correlation so the comparison is like-for-like.",
        "Pre-register the base-model confound as a named alternative hypothesis, citing arXiv:2607.14147. If hysteresis loop width is nonzero in BASE models too, the bistability finding survives but the SAFETY-specificity claim does not. Decide in advance which of H1's two halves you are willing to lose, and state what a nonzero base-model loop width would mean. Discovering this mid-run is what turns a clean negative into an ambiguous one.",
        "Add a jailbreak-robustness arm to the ground truth, or narrow the claim. A recent large audit (arXiv:2605.05427, 21 open-weight models) reports over-refusal and harmful compliance are nearly uncorrelated — so 'harmful-prompt refusal rate' is not a scalar safety construct. Either predict two separate ground truths (plain-harmful refusal rate AND adversarial/jailbreak attack-success rate) and report RRI's correlation with each, or state up front that the claim is scoped to plain-harmful refusal only. Predicting jailbreak robustness would be a substantially stronger contribution and is more naturally what a 'nearness to tipping' metric should predict.",
        "Add the cheapest possible baseline to the pre-registered list, beyond the static mean: a pure output-side detector using ZERO internals — e.g. the model's next-token probability of refusal-onset tokens ('I', 'Sorry', 'I cannot') on the same handful of benign prompts. If that trivial baseline matches RRI, the internals add nothing, and this is the baseline a reviewer will ask for first."
      ]
    }
  ],
  "critiques": [
    {
      "category": "methodology",
      "severity": "major",
      "description": "FATAL AS SPECIFIED — the H1 hysteresis test is guaranteed to return zero loop width in every checkpoint, for reasons unrelated to bistability. If the alpha sweep is implemented as independent generations at successive alpha values (which is what 'sweep alpha upward until the response flips, then sweep back down' describes), then under greedy decoding the response is a deterministic function of alpha alone. No state is carried from the up-sweep into the down-sweep, so the map alpha -> response is single-valued and alpha_up = alpha_down exactly. Hysteresis is definitionally path dependence and requires a persistent state variable; in an autoregressive LM the only candidate is the generated prefix / KV cache. As written, the experiment's own 'decisive test' would report the null, and the success criteria instruct the authors to conclude the tipping-point framing is refuted — a false negative baked into the protocol. This alone would waste the entire run.",
      "suggested_action": "Re-specify H1 as a within-generation ramp with retained state: fix a benign prompt, decode autoregressively while increasing alpha by a fixed step per generated token until a refusal onset is emitted; then continue decoding the SAME sequence (prefix and KV cache retained) while decreasing alpha per step, and record the alpha at which compliant continuation resumes. Loop width = alpha_up - alpha_down. Add a mandatory reset-control arm in which the prefix is discarded between alpha steps; that arm must yield zero width, and it is what demonstrates the loop is genuine path dependence rather than sampling noise. Report loop width distributions over >= 30 prompts with bootstrap CIs, and also report the width under temperature 0 vs temperature 0.7 (a real bistable switch should show flickering near the threshold at nonzero temperature — a bonus EWS the current design leaves on the table)."
    },
    {
      "category": "methodology",
      "severity": "major",
      "description": "The 'token position as time axis' assumption is the second load-bearing operationalization and it does not hold in the form stated. Critical slowing down is a property of the leading eigenvalue of a linearized AUTONOMOUS STOCHASTIC system near a fold bifurcation. Within a single forward pass over a fixed prompt, (a) the decay of an injected perturbation across later positions is dominated by attention dilution — an injected key competes with t-1 others, so influence falls roughly as 1/t irrespective of any basin — plus RMSNorm rescaling and position-dependent residual norm growth; and (b) Var(r_t) and AC(1) computed over PROMPT token positions are dominated by deterministic token-identity variation (punctuation, function words, chat-template scaffolding), not by stochastic fluctuation around an attractor. There is no noise process, so 'rising variance near a tipping point' has no referent. The hypothesis acknowledges the analogy is 'operationalized, not assumed' and points to H1 as the check, but H1 as specified is broken (see above), so nothing checks it.",
      "suggested_action": "Move the time axis to autoregressive generation under temperature sampling, which IS a genuine stochastic dynamical system with the token sequence as state. Concretely: (i) for lambda, inject the epsilon perturbation at generation step p, continue decoding, and fit the exponential decay of |delta r_t| across subsequent GENERATED steps, averaged over >= 20 sampled rollouts per prompt with paired clean/perturbed random seeds; (ii) for Var and AC(1), compute them on r_t over generated positions across rollouts (across-rollout variance at fixed step is the theoretically correct 'fluctuation' quantity, not within-sequence variance). Then add the three controls named in the soundness improvements — random readout axis, random vs refusal-aligned perturbation, and a syntactic-probe observable — so that a positive lambda ordering cannot be explained by generic mixing. If the authors prefer to keep the single-forward-pass version for cost reasons, it must be demoted to a secondary, explicitly-heuristic measurement and the 1/t attention-dilution null must be fit and subtracted."
    },
    {
      "category": "rigor",
      "severity": "major",
      "description": "Statistical power is insufficient for every headline claim. The panel is ~10 checkpoints, but they are not independent units: three Qwen3-0.6B variants, three Qwen3-1.7B variants, two Llama-3.2-1B variants, and one or two uncensored fine-tunes — effectively 3 architecture families and 4-5 weight lineages. At n = 10, the 95% bootstrap CI around an observed Spearman rho = 0.8 spans roughly [0.3, 0.95], so criterion (3)'s requirement that the CI lower bound exceed the static-mean baseline's correlation is close to unattainable no matter what is true. The partial rank correlation controlling for the static mean — explicitly named as THE load-bearing statistic — has almost no power at n = 10 with strongly correlated predictors. Leave-one-family-out with 3 families is n_family = 2 for training, which is not an estimate. Bootstrapping over prompts does not help: prompts are not the unit of the model-level claim, and resampling them will produce deceptively narrow CIs on a model-level correlation (a pseudo-replication error a reviewer will catch immediately).",
      "suggested_action": "Scale the panel to >= 25 checkpoints across >= 4 families (see the contribution improvements for a CPU-feasible list — the whole point of the method is that it costs seconds per model, so a 25-model panel is nearly free and its absence would look strange). Bootstrap over MODELS as the unit for all model-level claims, and report the prompt-level bootstrap separately and labelled as a measurement-noise estimate only. Pre-register the achievable effect size: state the n at which the CI-exclusion criterion becomes attainable and either meet it or soften criterion (3) to a directional claim with an honest CI."
    },
    {
      "category": "rigor",
      "severity": "major",
      "description": "The ground truth is degenerate in a way the assumptions block anticipates but under-treats. The panel is essentially trimodal: base models refuse ~0%, instruct models refuse at a high rate, abliterated models refuse ~0%. A Spearman rank correlation over such a distribution is a three-class discrimination wearing a correlation's clothes, and it can be won at rho ~ 1.0 by baselines so trivial they undermine the entire contribution — e.g. 'does the model ever emit an apology token on any prompt', or the next-token probability of 'I'/'Sorry' on a single benign prompt. Compounding this: a recent 21-model audit (arXiv:2605.05427) reports that over-refusal and harmful compliance are nearly uncorrelated across open-weight models, so 'harmful-prompt refusal rate' is not a one-dimensional safety construct in the first place, and a metric that predicts it may predict nothing about the adversarial robustness a safety auditor actually cares about.",
      "suggested_action": "Two changes. (1) Fill the middle of the refusal-rate range with deliberately partially-de-aligned checkpoints — a few hundred LoRA steps on compliant data at 3-4 strengths per base model gives a graded ladder cheaply and turns the correlation claim into a real one. (2) Predict TWO ground truths and report both: plain-harmful refusal rate (AdvBench/JailbreakBench subset) AND adversarial attack-success rate under a fixed jailbreak suite, plus the over-refusal rate on XSTest as a third axis. A 'nearness to tipping' metric should, on its own theory, predict jailbreak susceptibility better than plain refusal rate — that is a sharper and more valuable claim than the current one. Add the two trivial output-side baselines named above to the pre-registered baseline list; if RRI does not beat them, the internals add nothing."
    },
    {
      "category": "methodology",
      "severity": "major",
      "description": "H2's central contrast is circular for the abliterated arm. Abliteration is defined (correctly, in the terms glossary) as orthogonalizing the residual-stream write matrices against the refusal direction. If r_t is then read out as the projection onto that same direction, r_t is near-constant in an abliterated model BY CONSTRUCTION — its variance collapses toward zero and its lag-1 autocorrelation becomes ill-conditioned or dominated by numerical noise. The predicted finding 'lower variance and lower AC(1) in abliterated models' is therefore guaranteed by the definition of the intervention rather than by anything about basin depth, and criterion (2) of CONFIRMS is not falsifiable in that arm. The same issue partially applies to the diff-in-means axis being re-derived per model: variance in projection units on a per-model axis of arbitrary scale is not commensurable across models.",
      "suggested_action": "Report every H2 indicator on at least one readout that survives the abliteration edit — the logit-lens log-odds of refusal-onset tokens against continuation tokens is the natural choice, and the hypothesis already lists it as an alternative observable. Additionally z-score r_t within model over the benign prompt set before computing Var and AC(1), and demonstrate that lambda is invariant to axis scaling (it should be, since it is a decay rate of a ratio, but this must be shown, not assumed). State explicitly in the pre-registration that any variance/AC result on the diff-in-means axis in abliterated models is reported as descriptive and is NOT counted toward criterion (2)."
    },
    {
      "category": "novelty",
      "severity": "major",
      "description": "The 'shallow basin' framing and the 'cheap internal safety score' deliverable both have closer prior art than the related-works section acknowledges, and both gaps are the kind a top-venue reviewer finds in one search. (a) 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) already establishes a SAFETY BASIN in weight space — random weight perturbations preserve safety locally, with a sharp step-like drop outside — and already ships a basin-geometry safety metric, VISAGE. The reinterpretation of Qi et al. as a 'shallow basin' is therefore not a new coinage, and the paper must state what a basin in ACTIVATION/behavioral state space adds over a basin in WEIGHT space. (b) RAS (arXiv:2606.25750) is a representation-level, calibrated 0-100 safety score explicitly motivated by 'output-level evaluation is expensive, judge-dependent, and benchmarks go stale' — nearly verbatim this proposal's motivation for H3 — validated across Llama, Gemma and Qwen against uncensored and abliterated variants. RAS does need harmful prompts, which is a real differentiator, but it must be named as the incumbent and beaten. (c) 'Refusal Falls off a Cliff' (arXiv:2510.06036) already probes a per-token-position refusal score, i.e. the r_t observable is not new. Coining new terms over an existing measurement is exactly what a reviewer scores as a novelty failure.",
      "suggested_action": "Add all three to related works with an explicit differentiator sentence each, and make two of them empirical baselines rather than citations: run VISAGE-style weight-perturbation basin volume (or state honestly why it is out of budget) and a RAS-style representation-alignment score on the same panel, and report RRI against both. The differentiator to lead with is sharp and defensible if stated plainly: VISAGE probes WEIGHT-space geometry and needs a harmful benchmark at each perturbation; RAS needs harmful and jailbreak prompts and a safety-aligned REFERENCE model; RRI claims to need neither. That claim is worth the paper — but only if the incumbents appear in the table."
    },
    {
      "category": "evidence",
      "severity": "major",
      "description": "A published result directly threatens H1's base-vs-instruct contrast and is not pre-registered as an alternative hypothesis. 'Breaking Refusal in the First Half' (arXiv:2607.14147) reports, using base-model controls, that prefill-collapse refusal dynamics are 'generic autoregressive conditioning, not safety-specific active suppression', with non-safety-tuned base models showing the same prefill-specific collapse; and 'Step-Wise Refusal Dynamics' (arXiv:2602.02600) reports that autoregressive commitment masks underlying instability. If path-dependent switching is a generic property of autoregressive self-conditioning, then a corrected H1 protocol may well find NONZERO loop width in base models too. That would leave the bistability claim intact while destroying the safety-specificity claim on which H2-H4 rest — an outcome the current success/disconfirm criteria have no cell for, so it would be discovered mid-run and rationalized post hoc.",
      "suggested_action": "Pre-register this as a named third outcome with its own reporting commitment: 'bistability present but not safety-specific (loop width > 0 in base models)'. State in advance what it would mean (the hysteresis is a property of autoregressive decoding, and only the QUANTITATIVE width ordering, if any, carries safety information) and pre-register the ordering test (loop width instruct > base and instruct > abliterated, paired over prompts) as the claim that survives. Cite both papers as motivating this control."
    },
    {
      "category": "methodology",
      "severity": "minor",
      "description": "Layer selection is under-specified in a way that creates a garden of forking paths. 'Sweep layer L' across 10+ models with ~28 layers each, then report the indicators, gives roughly 280 opportunities to find an ordering; no correction is mentioned. This matters more than usual here because a recent mechanistic analysis (arXiv:2606.22686, TrustNLP 2026) reports architecture-dependent safety topologies — 'Late Decision' models (Llama, safety divergence only at final layers) versus 'Early Divergence' models (Qwen, safety integrated mid-computation) — so the correct L differs systematically across the two families in the panel, and a per-family sweep chosen post hoc would be indistinguishable from selection on the outcome.",
      "suggested_action": "Pre-register a layer-selection RULE that does not touch the outcome variable: e.g. select L as the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set, computed on the REFERENCE model only and transferred by relative depth (L/n_layers) to the rest of the panel. Report the full layer profile as a secondary descriptive figure and cite arXiv:2606.22686 when interpreting family differences. Apply Holm or BH correction to any per-layer claims."
    },
    {
      "category": "rigor",
      "severity": "minor",
      "description": "The refusal-string classifier plus 'cheap OpenRouter LLM judge' ground truth is under-specified for a paper whose entire headline is a correlation against that ground truth. Refusal-string matching is known to both over-count (models that say 'I cannot verify that' while complying) and under-count (soft refusals, deflections, capability-denials), and abliterated models in particular produce degenerate or repetitive outputs that string matchers mis-score. Any measurement error in the ground truth attenuates the correlation, which is the exact quantity the pre-registered criterion thresholds at 0.8.",
      "suggested_action": "Report inter-rater agreement between the string classifier and the LLM judge (Cohen's kappa) and use the judge as primary with the string matcher as a screen, not the reverse. Hand-adjudicate a stratified sample of >= 100 items to estimate the judge's own error rate, and report the attenuation-corrected correlation alongside the raw one. Also fix and report the decoding configuration (temperature, max tokens, chat template, system prompt) — refusal rates on small models are highly sensitive to all four, and the system prompt in particular is documented to shift the safety basin (arXiv:2405.17374)."
    },
    {
      "category": "scope",
      "severity": "minor",
      "description": "The 0.6B-1.7B scale assumption is stated but not defended, and it interacts badly with the central claim. The refusal-direction literature is built on 1.5B-72B models; at 0.6B the refusal mechanism may be genuinely weaker and noisier, and — more sharply — a 0.6B model that is 'twitchy about refusal on harmless input' may be twitchy because it is undertrained, not because it is parked near a tipping point. That is a confound the design cannot separate at a single scale, and it directly threatens the mechanistic interpretation even if the correlation holds.",
      "suggested_action": "Include at least one within-family scale ladder in the panel (Qwen3 0.6B / 1.7B / 4B, CPU-feasible in float32 or int8 at 4B for the short generations required) and report whether lambda, Var and AC(1) trend with SCALE independently of safety. If the indicators track scale as strongly as they track safety, say so and control for it as a covariate in the partial correlation. A one-paragraph scale-robustness result also substantially raises the paper's reach."
    },
    {
      "category": "clarity",
      "severity": "minor",
      "description": "Two definitional issues that will cause misreading. (1) The RRI name is sign-inverted relative to its construct: 'Refusal Resilience Index' reads as 'how resilient refusal is', but a high RRI is meant to indicate a SHALLOW basin and hence LOW resilience of the comply state / high proximity to switching. (2) RRI is left as 'a simple function of (lambda, variance, lag-1 AC), fixed a priori' without stating the function — which makes 'fixed a priori' unverifiable by a reader and unenforceable on the authors.",
      "suggested_action": "Rename to something sign-transparent ('Refusal Proximity Index' or 'Switching Proximity Index'), or state the sign convention explicitly in the glossary entry. Write the exact formula and standardization into the hypothesis text before the run, e.g. RRI = mean of within-panel z-scores of (-lambda), log Var(r), and Fisher-z(AC1(r)), with all three computed on the standardized observable at the pre-registered layer. Report the single-term versions (lambda alone, AC1 alone) alongside, since a reviewer will want to know which term carries the signal."
    }
  ],
  "score": 5,
  "confidence": 4,
  "relation_type": null,
  "relation_rationale": ""
}
```

### [35] TOOL RESULT — Write · 2026-08-12 12:49:18 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_1/review_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"overall_assessment\": \"This is one of the more imaginative hypotheses I have reviewed at the pre-flight stage. The core move — replace the field's default static unit (a direction, a feature, a cluster separation) with a *rate*, and import the ecology/climate early-warning-signal (EWS) toolkit to estimate proximity to a comply/refuse tipping point — is a real reframing, not a relabeling, and it is aimed squarely at a documented blind spot (behavioral uncensored fine-tunes that AMS-style activation-geometry scanners cannot see; Messenger, arXiv:2608.05578 / IEEE Access 14:91723-91737, 2026, which I verified — AMS reports 71% leave-one-out accuracy over 14 configs and 4 families). The proposal is unusually well-engineered as a *falsifiable* object: it pre-registers a decisive test (H1 hysteresis), pre-registers the strongest cheap competitor (static mean of r), pre-registers the load-bearing statistic (partial rank correlation controlling for that mean), and pre-registers a clean negative. That is exactly the ICML MI workshop bar ('specific falsifiable hypotheses, and how the evidence provided does and does not support them'). I want this run.\\n\\nBut as written it would very likely burn its compute for reasons that have nothing to do with whether the underlying idea is true. Two construct-validity problems are close to fatal and must be fixed BEFORE any GPU/CPU time is spent:\\n\\n(1) **The hysteresis protocol as specified is guaranteed to return zero loop width, by construction, in every checkpoint.** If alpha is swept by running independent generations at alpha = 0, 0.1, 0.2, ..., then back down, the model's response is a deterministic (under greedy decoding) function of alpha alone. There is no state carried from the up-sweep into the down-sweep, so response(alpha) is single-valued and alpha_up = alpha_down identically. Hysteresis requires path dependence, i.e. a state variable that persists across the sweep. In an autoregressive LM the *only* such state is the generated prefix + KV cache. So H1 is only well-posed if alpha is ramped up and back down WITHIN a single generation, with the prefix retained. As written, the 'decisive test' would return a trivially null result that the authors' own success criteria would (incorrectly) read as refuting the tipping-point framing. This is the single highest-impact fix in the review.\\n\\n(2) **'Token position as time' is not a relaxation axis of an autonomous dynamical system, and CSD theory does not license the indicators over it.** Critical slowing down is a statement about the leading eigenvalue of a linearized *autonomous stochastic* system near a fold. Within one forward pass over a fixed prompt, the decay of an injected perturbation across later positions is dominated by attention dilution (an injected key is one of t keys; influence falls roughly as 1/t regardless of any basin), by RMSNorm rescaling, and by residual-norm growth with depth/position — none of which are the dominant eigenvalue of a comply/refuse dynamics. Worse, the variance and lag-1 autocorrelation of r_t across *prompt* token positions are dominated by token identity (punctuation, function words, chat-template scaffolding), i.e. by deterministic content, not by fluctuations around an attractor. The good news: the fix is the same as for (1). Autoregressive generation with temperature sampling IS a genuine stochastic dynamical system whose state is the sequence; measuring lambda, Var, and AC(1) over *generated* positions across sampled rollouts is theoretically defensible and empirically much more likely to show the predicted ordering.\\n\\nBeyond those, three further issues would each independently sink the headline claim: an n-problem (n approximately 10 checkpoints, effectively 3-4 independent families, cannot support a rho >= 0.8 claim with a CI that excludes a strong baseline, let alone a partial correlation or leave-one-family-out at n_family = 2-3), a degenerate-ground-truth problem (a trimodal base/instruct/abliterated panel turns a 'rank correlation' into a 3-class classification any trivial detector wins), and a circularity in H2's key contrast (abliteration orthogonalizes writes against the refusal direction, so r_t in an abliterated model is near-constant by construction; low variance and degenerate AC(1) there are an artifact of the readout being surgically destroyed, not evidence about basin depth).\\n\\nRelated work is well chosen but has real gaps that a reviewer at a top venue will find immediately: RAS (arXiv:2606.25750) is a representation-level, calibrated 0-100 safety score explicitly motivated by 'output-level evaluation is expensive' — that is the same product H3 promises and it is uncited; 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) already frames safety as a *basin* and ships VISAGE, a basin-volume safety metric — the 'shallow basin' language here is not new and must be positioned against it; 'Refusal Falls off a Cliff' (arXiv:2510.06036) already probes a per-token-position refusal score; 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion LMs' (arXiv:2602.02600) already studies commitment/path-dependence in refusal generation and observes that autoregressive decoding 'masks the underlying instability'; and 'Breaking Refusal in the First Half' (arXiv:2607.14147) reports, with base-model controls, that prefill-collapse dynamics are 'generic autoregressive conditioning, not safety-specific active suppression' — which is a pre-registered threat to H1's base-vs-instruct contrast that must be confronted, not discovered mid-run.\\n\\nMy verdict: the idea deserves the compute, but not this protocol. With the sweep moved inside generation, the time axis moved to sampled rollouts, the panel widened to 25-30 checkpoints with graded ground truth, and the abliteration confound handled by a model-independent readout, this becomes a strong paper whether it confirms or refutes. Without those, a null result will be uninterpretable and a positive result will be unpublishable.\",\n  \"strengths\": [\n    \"Genuinely novel reframing, not new vocabulary for an old method. The field's default unit is a static object (direction, feature, circuit); this proposes a rate, and imports a mature, well-validated toolkit (Scheffer-style EWS: slowed recovery, rising variance, rising lag-1 autocorrelation) that my searches confirm has not been applied to LLM internal state dynamics or safety auditing. The physics import (hysteresis as the decisive test that a switch is bistable rather than merely biased) is the right instinct and is what separates this from a vague 'safety is fragile' claim.\",\n    \"Pre-registered falsifiability at a level rarely seen in pre-flight proposals. H1 is named as decisive; the DISCONFIRMS block commits in advance to reporting refutation rather than salvaging; and — most importantly — the authors identify the *strongest cheap competitor* themselves (the static mean level of r on benign prompts) and make the load-bearing statistic a partial correlation controlling for it. That is precisely the discipline the MI literature is currently faulted for lacking, and it is worth real credit.\",\n    \"The target is a real, documented gap, correctly identified. AMS (Messenger 2026) genuinely reports that behavioral uncensored fine-tunes preserve cluster separation and refusal direction while complying with harmful requests; H4 aims at exactly that blind spot, and does so from the act-side rather than the read-side. This connects cleanly to the sharpest 2026 negative result in interpretability — the knowledge-action gap — and the motivation section makes that connection correctly rather than decoratively.\",\n    \"The deliverable, if it works, is operationally valuable and cheap: a per-checkpoint safety score from a handful of harmless prompts, no harmful content held or transmitted, no reference model, no benchmark to memorize and game. The zero-harmful-prompt (unembedding-axis) variant is a good, honest hardening of that claim, and reporting all headline results under both axis variants is the right call.\",\n    \"The base / safety-tuned / abliterated triple read as a wild-type / knock-in / knock-out series is a clean experimental-genetics framing, and Step 6's question — does abliteration revert to base or produce a third state? — is a genuinely interesting, publishable sub-result even if H3 fails.\",\n    \"Costing and feasibility are realistic and honest (CPU-only, small models, <$2 judge spend), and the assumptions block is unusually candid, including a stated mitigation for degenerate ground truth.\"\n  ],\n  \"dimension_scores\": [\n    {\n      \"dimension\": \"soundness\",\n      \"score\": 2,\n      \"justification\": \"The framing is coherent and the statistical plan is thoughtfully pre-registered, but two load-bearing operationalizations do not survive scrutiny: the hysteresis sweep as described has no state variable and is therefore single-valued by construction, and token-position-within-one-forward-pass is not the relaxation axis of an autonomous dynamical system that CSD theory requires. Add a severe power deficit (n approximately 10, effectively 3-4 independent families) against a headline claim that needs a bootstrap CI to exclude a strong baseline, a trimodal ground truth that makes the rank correlation nearly vacuous, and a confound that makes H2's abliterated arm circular, and the current design cannot deliver an interpretable verdict either way. All of these are fixable pre-flight, which is why this is a 2 and not a 1.\",\n      \"improvements\": [\n        \"Redefine the H1 sweep as a within-generation ramp: hold one benign prompt, generate autoregressively while raising alpha per step until a refusal onset token appears, then lower alpha per step while RETAINING the generated prefix and KV cache, and record the alpha at which the model returns to compliant continuation. Loop width = alpha_up - alpha_down is then well-posed because the prefix is the state variable. Include a shuffled-control arm (reset the prefix between steps) which must give zero width — that control is what proves the loop is path dependence and not noise.\",\n        \"Move the H2 time axis from prompt-token position inside one forward pass to autoregressive generation steps under temperature sampling. Inject the epsilon perturbation at generation step p, continue decoding, and fit the exponential decay of |delta r_t| over subsequent GENERATED steps, averaged over >= 20 rollouts per prompt. Compute Var(r_t) and AC(1) on the sampled rollout trajectories. This makes the dynamical-system analogy defensible rather than metaphorical, and it is the only version of the measurement a physics- or ecology-literate reviewer will accept.\",\n        \"Add the three null controls that make lambda interpretable: (i) a random-direction readout axis instead of the refusal axis — lambda on a random axis must NOT show the safety ordering; (ii) a random-vector perturbation vs a refusal-axis-aligned perturbation; (iii) an attention-dilution baseline, i.e. lambda measured on a purely syntactic observable (e.g. projection onto a part-of-speech probe direction), which should decay at the same rate if what you are measuring is generic mixing rather than a basin.\",\n        \"Fix the abliteration circularity. Abliteration orthogonalizes the write matrices against the refusal direction, so r_t is near-constant in abliterated models by construction and its variance/AC(1) are degenerate for trivial reasons. Either (a) report all indicators on a readout axis that is NOT the abliterated direction (e.g. the logit-lens log-odds of refusal-onset tokens, which survives the edit), or (b) z-score r_t within model before computing Var and AC(1) and state explicitly that the variance claim is scale-free, or preferably both. Without this, criterion (2) of CONFIRMS is unfalsifiable.\",\n        \"Make r_t commensurable across models. A per-model diff-in-means axis has arbitrary scale and the residual stream norm differs by an order of magnitude across families and layers. Standardize r_t (unit-norm axis, and z-scored r within model over the benign prompt set) before any cross-model comparison, and report that lambda is invariant to that normalization.\",\n        \"Report an explicit power analysis in the plan. At n = 10 the 95% bootstrap CI on an observed Spearman rho = 0.8 spans roughly [0.3, 0.95]; a partial correlation at n = 10 with one covariate has almost no power; leave-one-family-out at 3 families is n = 2. State the n needed for the pre-registered CI-exclusion criterion to be attainable and scale the panel to it.\"\n      ]\n    },\n    {\n      \"dimension\": \"presentation\",\n      \"score\": 3,\n      \"justification\": \"Exceptionally clear and well organized for a pre-flight hypothesis: four numbered sub-claims, an explicit decisive test, a terms glossary, pre-registered baselines, and a genuinely honest DISCONFIRMS block. The related-works entries are substantive rather than perfunctory — each states what the prior work does and where this departs. Deductions are for gaps in prior-art coverage (several close works uncited) and for a few places where the metaphor is asserted where a definition is needed.\",\n      \"improvements\": [\n        \"Cite and position against the five works my searches surfaced that are missing: RAS (arXiv:2606.25750, representation-level calibrated safety score, same product claim as H3); 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374, which already introduces the safety BASIN and the VISAGE basin-volume metric — the 'shallow basin' language is not new); 'Refusal Falls off a Cliff' (arXiv:2510.06036, per-token-position refusal score probing); 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion LMs' (arXiv:2602.02600, commitment and path-dependence in refusal decoding); and 'Breaking Refusal in the First Half' (arXiv:2607.14147, base-model controls attributing prefill collapse to generic autoregressive conditioning). One sentence each on the departure is enough, but their absence is currently the most visible reviewer-facing weakness after the two design flaws.\",\n        \"Give RRI an explicit, fixed formula in the hypothesis text rather than 'a simple function of (lambda, variance, lag-1 AC)'. State the exact combination and the exact standardization, and state it BEFORE the run. 'Fixed a priori' is only credible if the reader can see the fixed thing. A defensible default: RRI = mean of the within-panel z-scores of (-lambda), log Var, and Fisher-z(AC1).\",\n        \"Fix the naming asymmetry: 'Refusal Resilience Index' reads as 'how resilient refusal is', but the construct is the opposite — a HIGH RRI is meant to indicate a SHALLOW basin, i.e. LOW resilience of the comply state. Rename (e.g. 'Refusal Proximity Index') or state the sign convention in the definition; as written it will be misread in every table caption.\",\n        \"State the layer/position selection protocol as a pre-registration, not a sweep. 'Sweep layer L' plus 'report the best' is a garden of forking paths across a 10-model panel. Fix L by a stated rule (e.g. the layer maximizing harmful/benign separation on a held-out contrast set of the REFERENCE model only) and report the full layer profile as secondary.\"\n      ]\n    },\n    {\n      \"dimension\": \"contribution\",\n      \"score\": 3,\n      \"justification\": \"High-ceiling and genuinely original in framing. A confirmed result gives a mechanistic account of safety tuning in the language of bistable systems plus a cheap, ungameable, harmful-content-free auditing metric that works where the published static scanner is documented to fail; a clean negative ('safety is a static bias, not a shifted operating point') is itself a publishable extension of the knowledge-action-gap literature with a dynamical arm. The ceiling is capped, though, by the model panel (0.6B-1.7B, 2-3 families, smaller than the 14-config/4-family panel of the AMS work it aims to beat) and by the risk that H1's contrast is explained by generic autoregressive conditioning rather than anything safety-specific.\",\n      \"improvements\": [\n        \"Widen the panel to >= 25 checkpoints spanning a GRADED range of refusal rates, not three discrete classes. Candidates that remain CPU-feasible: Qwen2.5-0.5B/1.5B-Instruct, SmolLM2-360M/1.7B-Instruct, Llama-3.2-1B/3B-Instruct, gemma-2-2b-it, TinyLlama-1.1B-Chat, Phi-3-mini, plus their abliterated and Dolphin/Josiefied-style uncensored variants, plus deliberately partially-de-aligned checkpoints (a few hundred steps of LoRA on compliant data, several strengths) to fill the middle of the range. Without intermediate refusal rates, a Spearman rho over a trimodal panel is a 3-class discrimination that a one-line 'does it ever emit an apology token' baseline will also win at rho ~ 1, which makes criterion (3) uninformative even if it passes.\",\n        \"Beat AMS on AMS's own terms, or say why not. AMS validates on 14 configs across 4 families with leave-one-out at 71%. Reporting a metric on 10 checkpoints across 2-3 families cannot claim to supersede it. Add at least a fourth family (Gemma or Mistral) and report the same leave-one-out accuracy figure alongside the rank correlation so the comparison is like-for-like.\",\n        \"Pre-register the base-model confound as a named alternative hypothesis, citing arXiv:2607.14147. If hysteresis loop width is nonzero in BASE models too, the bistability finding survives but the SAFETY-specificity claim does not. Decide in advance which of H1's two halves you are willing to lose, and state what a nonzero base-model loop width would mean. Discovering this mid-run is what turns a clean negative into an ambiguous one.\",\n        \"Add a jailbreak-robustness arm to the ground truth, or narrow the claim. A recent large audit (arXiv:2605.05427, 21 open-weight models) reports over-refusal and harmful compliance are nearly uncorrelated — so 'harmful-prompt refusal rate' is not a scalar safety construct. Either predict two separate ground truths (plain-harmful refusal rate AND adversarial/jailbreak attack-success rate) and report RRI's correlation with each, or state up front that the claim is scoped to plain-harmful refusal only. Predicting jailbreak robustness would be a substantially stronger contribution and is more naturally what a 'nearness to tipping' metric should predict.\",\n        \"Add the cheapest possible baseline to the pre-registered list, beyond the static mean: a pure output-side detector using ZERO internals — e.g. the model's next-token probability of refusal-onset tokens ('I', 'Sorry', 'I cannot') on the same handful of benign prompts. If that trivial baseline matches RRI, the internals add nothing, and this is the baseline a reviewer will ask for first.\"\n      ]\n    }\n  ],\n  \"critiques\": [\n    {\n      \"category\": \"methodology\",\n      \"severity\": \"major\",\n      \"description\": \"FATAL AS SPECIFIED — the H1 hysteresis test is guaranteed to return zero loop width in every checkpoint, for reasons unrelated to bistability. If the alpha sweep is implemented as independent generations at successive alpha values (which is what 'sweep alpha upward until the response flips, then sweep back down' describes), then under greedy decoding the response is a deterministic function of alpha alone. No state is carried from the up-sweep into the down-sweep, so the map alpha -> response is single-valued and alpha_up = alpha_down exactly. Hysteresis is definitionally path dependence and requires a persistent state variable; in an autoregressive LM the only candidate is the generated prefix / KV cache. As written, the experiment's own 'decisive test' would report the null, and the success criteria instruct the authors to conclude the tipping-point framing is refuted — a false negative baked into the protocol. This alone would waste the entire run.\",\n      \"suggested_action\": \"Re-specify H1 as a within-generation ramp with retained state: fix a benign prompt, decode autoregressively while increasing alpha by a fixed step per generated token until a refusal onset is emitted; then continue decoding the SAME sequence (prefix and KV cache retained) while decreasing alpha per step, and record the alpha at which compliant continuation resumes. Loop width = alpha_up - alpha_down. Add a mandatory reset-control arm in which the prefix is discarded between alpha steps; that arm must yield zero width, and it is what demonstrates the loop is genuine path dependence rather than sampling noise. Report loop width distributions over >= 30 prompts with bootstrap CIs, and also report the width under temperature 0 vs temperature 0.7 (a real bistable switch should show flickering near the threshold at nonzero temperature — a bonus EWS the current design leaves on the table).\"\n    },\n    {\n      \"category\": \"methodology\",\n      \"severity\": \"major\",\n      \"description\": \"The 'token position as time axis' assumption is the second load-bearing operationalization and it does not hold in the form stated. Critical slowing down is a property of the leading eigenvalue of a linearized AUTONOMOUS STOCHASTIC system near a fold bifurcation. Within a single forward pass over a fixed prompt, (a) the decay of an injected perturbation across later positions is dominated by attention dilution — an injected key competes with t-1 others, so influence falls roughly as 1/t irrespective of any basin — plus RMSNorm rescaling and position-dependent residual norm growth; and (b) Var(r_t) and AC(1) computed over PROMPT token positions are dominated by deterministic token-identity variation (punctuation, function words, chat-template scaffolding), not by stochastic fluctuation around an attractor. There is no noise process, so 'rising variance near a tipping point' has no referent. The hypothesis acknowledges the analogy is 'operationalized, not assumed' and points to H1 as the check, but H1 as specified is broken (see above), so nothing checks it.\",\n      \"suggested_action\": \"Move the time axis to autoregressive generation under temperature sampling, which IS a genuine stochastic dynamical system with the token sequence as state. Concretely: (i) for lambda, inject the epsilon perturbation at generation step p, continue decoding, and fit the exponential decay of |delta r_t| across subsequent GENERATED steps, averaged over >= 20 sampled rollouts per prompt with paired clean/perturbed random seeds; (ii) for Var and AC(1), compute them on r_t over generated positions across rollouts (across-rollout variance at fixed step is the theoretically correct 'fluctuation' quantity, not within-sequence variance). Then add the three controls named in the soundness improvements — random readout axis, random vs refusal-aligned perturbation, and a syntactic-probe observable — so that a positive lambda ordering cannot be explained by generic mixing. If the authors prefer to keep the single-forward-pass version for cost reasons, it must be demoted to a secondary, explicitly-heuristic measurement and the 1/t attention-dilution null must be fit and subtracted.\"\n    },\n    {\n      \"category\": \"rigor\",\n      \"severity\": \"major\",\n      \"description\": \"Statistical power is insufficient for every headline claim. The panel is ~10 checkpoints, but they are not independent units: three Qwen3-0.6B variants, three Qwen3-1.7B variants, two Llama-3.2-1B variants, and one or two uncensored fine-tunes — effectively 3 architecture families and 4-5 weight lineages. At n = 10, the 95% bootstrap CI around an observed Spearman rho = 0.8 spans roughly [0.3, 0.95], so criterion (3)'s requirement that the CI lower bound exceed the static-mean baseline's correlation is close to unattainable no matter what is true. The partial rank correlation controlling for the static mean — explicitly named as THE load-bearing statistic — has almost no power at n = 10 with strongly correlated predictors. Leave-one-family-out with 3 families is n_family = 2 for training, which is not an estimate. Bootstrapping over prompts does not help: prompts are not the unit of the model-level claim, and resampling them will produce deceptively narrow CIs on a model-level correlation (a pseudo-replication error a reviewer will catch immediately).\",\n      \"suggested_action\": \"Scale the panel to >= 25 checkpoints across >= 4 families (see the contribution improvements for a CPU-feasible list — the whole point of the method is that it costs seconds per model, so a 25-model panel is nearly free and its absence would look strange). Bootstrap over MODELS as the unit for all model-level claims, and report the prompt-level bootstrap separately and labelled as a measurement-noise estimate only. Pre-register the achievable effect size: state the n at which the CI-exclusion criterion becomes attainable and either meet it or soften criterion (3) to a directional claim with an honest CI.\"\n    },\n    {\n      \"category\": \"rigor\",\n      \"severity\": \"major\",\n      \"description\": \"The ground truth is degenerate in a way the assumptions block anticipates but under-treats. The panel is essentially trimodal: base models refuse ~0%, instruct models refuse at a high rate, abliterated models refuse ~0%. A Spearman rank correlation over such a distribution is a three-class discrimination wearing a correlation's clothes, and it can be won at rho ~ 1.0 by baselines so trivial they undermine the entire contribution — e.g. 'does the model ever emit an apology token on any prompt', or the next-token probability of 'I'/'Sorry' on a single benign prompt. Compounding this: a recent 21-model audit (arXiv:2605.05427) reports that over-refusal and harmful compliance are nearly uncorrelated across open-weight models, so 'harmful-prompt refusal rate' is not a one-dimensional safety construct in the first place, and a metric that predicts it may predict nothing about the adversarial robustness a safety auditor actually cares about.\",\n      \"suggested_action\": \"Two changes. (1) Fill the middle of the refusal-rate range with deliberately partially-de-aligned checkpoints — a few hundred LoRA steps on compliant data at 3-4 strengths per base model gives a graded ladder cheaply and turns the correlation claim into a real one. (2) Predict TWO ground truths and report both: plain-harmful refusal rate (AdvBench/JailbreakBench subset) AND adversarial attack-success rate under a fixed jailbreak suite, plus the over-refusal rate on XSTest as a third axis. A 'nearness to tipping' metric should, on its own theory, predict jailbreak susceptibility better than plain refusal rate — that is a sharper and more valuable claim than the current one. Add the two trivial output-side baselines named above to the pre-registered baseline list; if RRI does not beat them, the internals add nothing.\"\n    },\n    {\n      \"category\": \"methodology\",\n      \"severity\": \"major\",\n      \"description\": \"H2's central contrast is circular for the abliterated arm. Abliteration is defined (correctly, in the terms glossary) as orthogonalizing the residual-stream write matrices against the refusal direction. If r_t is then read out as the projection onto that same direction, r_t is near-constant in an abliterated model BY CONSTRUCTION — its variance collapses toward zero and its lag-1 autocorrelation becomes ill-conditioned or dominated by numerical noise. The predicted finding 'lower variance and lower AC(1) in abliterated models' is therefore guaranteed by the definition of the intervention rather than by anything about basin depth, and criterion (2) of CONFIRMS is not falsifiable in that arm. The same issue partially applies to the diff-in-means axis being re-derived per model: variance in projection units on a per-model axis of arbitrary scale is not commensurable across models.\",\n      \"suggested_action\": \"Report every H2 indicator on at least one readout that survives the abliteration edit — the logit-lens log-odds of refusal-onset tokens against continuation tokens is the natural choice, and the hypothesis already lists it as an alternative observable. Additionally z-score r_t within model over the benign prompt set before computing Var and AC(1), and demonstrate that lambda is invariant to axis scaling (it should be, since it is a decay rate of a ratio, but this must be shown, not assumed). State explicitly in the pre-registration that any variance/AC result on the diff-in-means axis in abliterated models is reported as descriptive and is NOT counted toward criterion (2).\"\n    },\n    {\n      \"category\": \"novelty\",\n      \"severity\": \"major\",\n      \"description\": \"The 'shallow basin' framing and the 'cheap internal safety score' deliverable both have closer prior art than the related-works section acknowledges, and both gaps are the kind a top-venue reviewer finds in one search. (a) 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) already establishes a SAFETY BASIN in weight space — random weight perturbations preserve safety locally, with a sharp step-like drop outside — and already ships a basin-geometry safety metric, VISAGE. The reinterpretation of Qi et al. as a 'shallow basin' is therefore not a new coinage, and the paper must state what a basin in ACTIVATION/behavioral state space adds over a basin in WEIGHT space. (b) RAS (arXiv:2606.25750) is a representation-level, calibrated 0-100 safety score explicitly motivated by 'output-level evaluation is expensive, judge-dependent, and benchmarks go stale' — nearly verbatim this proposal's motivation for H3 — validated across Llama, Gemma and Qwen against uncensored and abliterated variants. RAS does need harmful prompts, which is a real differentiator, but it must be named as the incumbent and beaten. (c) 'Refusal Falls off a Cliff' (arXiv:2510.06036) already probes a per-token-position refusal score, i.e. the r_t observable is not new. Coining new terms over an existing measurement is exactly what a reviewer scores as a novelty failure.\",\n      \"suggested_action\": \"Add all three to related works with an explicit differentiator sentence each, and make two of them empirical baselines rather than citations: run VISAGE-style weight-perturbation basin volume (or state honestly why it is out of budget) and a RAS-style representation-alignment score on the same panel, and report RRI against both. The differentiator to lead with is sharp and defensible if stated plainly: VISAGE probes WEIGHT-space geometry and needs a harmful benchmark at each perturbation; RAS needs harmful and jailbreak prompts and a safety-aligned REFERENCE model; RRI claims to need neither. That claim is worth the paper — but only if the incumbents appear in the table.\"\n    },\n    {\n      \"category\": \"evidence\",\n      \"severity\": \"major\",\n      \"description\": \"A published result directly threatens H1's base-vs-instruct contrast and is not pre-registered as an alternative hypothesis. 'Breaking Refusal in the First Half' (arXiv:2607.14147) reports, using base-model controls, that prefill-collapse refusal dynamics are 'generic autoregressive conditioning, not safety-specific active suppression', with non-safety-tuned base models showing the same prefill-specific collapse; and 'Step-Wise Refusal Dynamics' (arXiv:2602.02600) reports that autoregressive commitment masks underlying instability. If path-dependent switching is a generic property of autoregressive self-conditioning, then a corrected H1 protocol may well find NONZERO loop width in base models too. That would leave the bistability claim intact while destroying the safety-specificity claim on which H2-H4 rest — an outcome the current success/disconfirm criteria have no cell for, so it would be discovered mid-run and rationalized post hoc.\",\n      \"suggested_action\": \"Pre-register this as a named third outcome with its own reporting commitment: 'bistability present but not safety-specific (loop width > 0 in base models)'. State in advance what it would mean (the hysteresis is a property of autoregressive decoding, and only the QUANTITATIVE width ordering, if any, carries safety information) and pre-register the ordering test (loop width instruct > base and instruct > abliterated, paired over prompts) as the claim that survives. Cite both papers as motivating this control.\"\n    },\n    {\n      \"category\": \"methodology\",\n      \"severity\": \"minor\",\n      \"description\": \"Layer selection is under-specified in a way that creates a garden of forking paths. 'Sweep layer L' across 10+ models with ~28 layers each, then report the indicators, gives roughly 280 opportunities to find an ordering; no correction is mentioned. This matters more than usual here because a recent mechanistic analysis (arXiv:2606.22686, TrustNLP 2026) reports architecture-dependent safety topologies — 'Late Decision' models (Llama, safety divergence only at final layers) versus 'Early Divergence' models (Qwen, safety integrated mid-computation) — so the correct L differs systematically across the two families in the panel, and a per-family sweep chosen post hoc would be indistinguishable from selection on the outcome.\",\n      \"suggested_action\": \"Pre-register a layer-selection RULE that does not touch the outcome variable: e.g. select L as the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set, computed on the REFERENCE model only and transferred by relative depth (L/n_layers) to the rest of the panel. Report the full layer profile as a secondary descriptive figure and cite arXiv:2606.22686 when interpreting family differences. Apply Holm or BH correction to any per-layer claims.\"\n    },\n    {\n      \"category\": \"rigor\",\n      \"severity\": \"minor\",\n      \"description\": \"The refusal-string classifier plus 'cheap OpenRouter LLM judge' ground truth is under-specified for a paper whose entire headline is a correlation against that ground truth. Refusal-string matching is known to both over-count (models that say 'I cannot verify that' while complying) and under-count (soft refusals, deflections, capability-denials), and abliterated models in particular produce degenerate or repetitive outputs that string matchers mis-score. Any measurement error in the ground truth attenuates the correlation, which is the exact quantity the pre-registered criterion thresholds at 0.8.\",\n      \"suggested_action\": \"Report inter-rater agreement between the string classifier and the LLM judge (Cohen's kappa) and use the judge as primary with the string matcher as a screen, not the reverse. Hand-adjudicate a stratified sample of >= 100 items to estimate the judge's own error rate, and report the attenuation-corrected correlation alongside the raw one. Also fix and report the decoding configuration (temperature, max tokens, chat template, system prompt) — refusal rates on small models are highly sensitive to all four, and the system prompt in particular is documented to shift the safety basin (arXiv:2405.17374).\"\n    },\n    {\n      \"category\": \"scope\",\n      \"severity\": \"minor\",\n      \"description\": \"The 0.6B-1.7B scale assumption is stated but not defended, and it interacts badly with the central claim. The refusal-direction literature is built on 1.5B-72B models; at 0.6B the refusal mechanism may be genuinely weaker and noisier, and — more sharply — a 0.6B model that is 'twitchy about refusal on harmless input' may be twitchy because it is undertrained, not because it is parked near a tipping point. That is a confound the design cannot separate at a single scale, and it directly threatens the mechanistic interpretation even if the correlation holds.\",\n      \"suggested_action\": \"Include at least one within-family scale ladder in the panel (Qwen3 0.6B / 1.7B / 4B, CPU-feasible in float32 or int8 at 4B for the short generations required) and report whether lambda, Var and AC(1) trend with SCALE independently of safety. If the indicators track scale as strongly as they track safety, say so and control for it as a covariate in the partial correlation. A one-paragraph scale-robustness result also substantially raises the paper's reach.\"\n    },\n    {\n      \"category\": \"clarity\",\n      \"severity\": \"minor\",\n      \"description\": \"Two definitional issues that will cause misreading. (1) The RRI name is sign-inverted relative to its construct: 'Refusal Resilience Index' reads as 'how resilient refusal is', but a high RRI is meant to indicate a SHALLOW basin and hence LOW resilience of the comply state / high proximity to switching. (2) RRI is left as 'a simple function of (lambda, variance, lag-1 AC), fixed a priori' without stating the function — which makes 'fixed a priori' unverifiable by a reader and unenforceable on the authors.\",\n      \"suggested_action\": \"Rename to something sign-transparent ('Refusal Proximity Index' or 'Switching Proximity Index'), or state the sign convention explicitly in the glossary entry. Write the exact formula and standardization into the hypothesis text before the run, e.g. RRI = mean of within-panel z-scores of (-lambda), log Var(r), and Fisher-z(AC1(r)), with all three computed on the standardized observable at the pre-registered layer. Report the single-term versions (lambda alone, AC1 alone) alongside, since a reviewer will want to know which term carries the signal.\"\n    }\n  ],\n  \"score\": 5,\n  \"confidence\": 4,\n  \"relation_type\": null,\n  \"relation_rationale\": \"\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [36] TOOL CALL — Bash · 2026-08-12 12:49:24 UTC

```
Validate output JSON:
python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
print(d['score'],d['confidence'],len(d['critiques']),len(d['strengths']),[(x['dimension'],x['score']) for x in d['dimension_scores']])
print(len(d['relation_rationale']))"
```

### [37] TOOL RESULT — Bash · 2026-08-12 12:49:24 UTC

```
{"stdout": "5 4 11 6 [('soundness', 2), ('presentation', 3), ('contribution', 3)]\n0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-08-12 12:49:36 UTC

```
Review written to `.terminal_claude_agent_struct_out.json` — **score 5/10** (borderline accept), confidence 4; soundness 2, presentation 3, contribution 3.

**The two flaws that would waste the run if not fixed first:**

1. **H1's hysteresis test returns zero loop width by construction.** If alpha is swept as independent generations, `response(alpha)` is deterministic and single-valued — no state carries from the up-sweep to the down-sweep, so `alpha_up == alpha_down` identically. The "decisive test" would return a guaranteed null that the success criteria misread as refutation. Fix: ramp alpha *within* one generation, retaining prefix + KV cache (the only state variable an autoregressive LM has), with a prefix-reset control arm that must give zero width.

2. **Token position within one forward pass is not a CSD relaxation axis.** Perturbation decay across later positions is dominated by attention dilution (~1/t), RMSNorm, and residual-norm growth; and Var/AC(1) over prompt positions are dominated by token identity, not fluctuation around an attractor — there is no noise process, so "rising variance" has no referent. Same fix: move the time axis to sampled autoregressive rollouts, which *is* a genuine stochastic dynamical system.

**Other major issues:** n≈10 checkpoints across effectively 3 families cannot support the pre-registered CI-exclusion or the partial correlation (bootstrapping over prompts would be pseudo-replication); trimodal ground truth makes the rank correlation winnable by a trivial "does it ever emit *Sorry*" baseline; H2's abliterated arm is circular (abliteration destroys the readout axis, so low variance is definitional).

**Prior art the author must confront** (verified by search, all uncited): VISAGE / "Navigating the Safety Landscape" (NeurIPS 2024) already frames safety as a *basin*; RAS (arXiv:2606.25750) is a representation-level cheap safety score with the same motivation; "Refusal Falls off a Cliff" already probes per-position refusal scores; and "Breaking Refusal in the First Half" attributes prefill-collapse dynamics to *generic autoregressive conditioning, not safety-specific suppression* — a pre-registered threat to H1's base-vs-instruct contrast. The AMS paper it targets (Messenger, IEEE Access 2026) checks out, and its 14-config/4-family panel is larger than the one proposed here.
```
