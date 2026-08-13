# gen_hypo_1 — create_idea

> Phase: `hypo_loop` · round 3 · `gen_hypo`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_hypo_1` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-12 12:58:51 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_3/gen_hypo/claude_agent
```

### [2] SYSTEM-USER prompt · 2026-08-12 12:58:57 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis generator (Step 2.1: GEN_HYPO — UNSEEDED mode)

Pipeline: GEN_HYPO (you) → INVENTION_LOOP → GEN_PAPER_REPO

You received a AII prompt. No external seeds — generate a novel hypothesis from your own reasoning and web research.

Your hypothesis will enter the invention loop (propose → execute → narrate) → the results become a paper + GitHub repo.
It MUST be GENUINELY NOVEL (validated against related work) and FEASIBLE TO TEST (within computational/data/tooling constraints provided).
Vague or incremental hypothesis → wasted computation across the entire pipeline.
</your_role>
</ai_inventor_context>

<strategic_mindset>
You are competing with human researchers.

YOUR ADVANTAGE: Breadth across many fields (information theory, ecology, economics, physics, cognitive science, program synthesis, etc.). No single human has this breadth.

HUMAN ADVANTAGE: Deep expertise in their specific field — they know every paper, every failed attempt, every subtle reason "obvious" ideas don't work.

HOW TO WIN: Don't create variants within their field — they'll always recognize those. Find unexpected connections ACROSS fields no single expert would think of.

NOVELTY BAR: An expert should say "I never thought of approaching it THAT way" — not "that's like paper X with a twist." If your idea lives in a crowded neighborhood of similar approaches, it's NOT novel enough.

NO TIME PRESSURE: Exploring 5-6 directions and abandoning all is a SUCCESSFUL process. Settling for a mediocre idea because you already spent so long researching it is a FAILED process.
</strategic_mindset>

<principles>
1. NOVEL - genuinely new mechanism/principle, not incremental. If you have to argue why it's different, it's NOT novel enough.
2. FEASIBLE - testable within the provided compute, data, and tooling
3. CROSS-FIELD - leverage connections across distant domains
4. RIGOROUS - consider what evidence would support OR refute it
5. PRECISE - clear language, no unnecessary jargon
</principles>

<common_mistakes_to_avoid>
Critical pitfalls from past runs. EXPLICITLY CHECK FOR EACH ONE.

**1. Incremental Recombination Disguised as Novelty**
"Apply known method X to known domain Y" is engineering, not conceptual novelty. Your idea needs a new mechanism/principle/insight — not just a new pairing of existing things.
CHECK: If describable as "A but with B" where A and B both exist, it's recombination. What is the genuinely new IDEA?

**2. Ignoring Resource Constraints**
Every hypothesis MUST be testable with available compute, data, and tools.
CHECK: "Can this be implemented with the specific resources listed? What exact data/compute/tools do I need, and are they available?"

**3. Shallow Search Leading to False Novelty**
The same concept often exists under different terminology, in different fields, or framed differently. Searching only your own phrasing and concluding novelty is the MOST dangerous mistake.

CHECK — For every promising hypothesis:
a) Search 5-6 semantically different phrasings within the field
b) Strip to the CORE MECHANISM and search 8-10 unrelated fields (e.g., "MDL-based complexity selection" → search neural architecture search, program synthesis, Bayesian model selection) — the same principle often exists under different names
c) Search for failed/negative results ("limitations", "does not improve")
d) Search in plain English without jargon
If a paper does the same thing under a different name, it's NOT novel.

**4. Rationalizing Overlapping Prior Work**
When you find similar work, do NOT rationalize minor differences as novelty. Two common traps:

FRAMEWORK PORTING: "Nobody did this in MY framework" — if the core mechanism exists in any context (different algorithm, different ensemble type, different field), porting it is engineering, not novelty.

GAP-FILLING: Papers A, B, C each cover variants → you propose the missing combination. An expert would say "obviously someone will do that eventually."

CHECK: Strip your idea to its core mechanism. Search if that mechanism exists ANYWHERE — any framework, any field, any algorithm family. If yes, ABANDON. Don't salvage by narrowing scope or listing "critical differences."

**5. Anchoring Bias**
Once invested in a direction, you'll unconsciously downplay overlap and inflate minor differences into "key differentiators." This feels like thoroughness but is actually defensiveness.

WARNING SIGNS: listing "critical differences" instead of reconsidering; reluctance to "waste" prior search effort; refining the SAME idea instead of exploring different ones; differentiators about context/framework rather than core mechanism.

CHECK: If you found even 1 paper with a similar core mechanism, ABANDON. The best hypotheses rarely come from your first direction. Each abandonment is progress.

**6. Relying on Search Snippets Without Fetching**
Search snippets are NOT enough to assess overlap or understand an approach. The actual mechanism and limitations are only in the full text.
CHECK: FETCH and read any potentially relevant result. Don't assess novelty from titles and snippets alone.

**7. Same-Neighborhood Pivoting**
Replacing one idea with a variant in the same conceptual space is NOT a genuine pivot. If all your directions are "[different adjective] + [same core concept]", you haven't actually explored.

CHECK: Would a single expert in that subfield have thought of ALL your directions? If yes, bring in a mechanism or framing from a completely unrelated field. That's where genuine novelty lives.
</common_mistakes_to_avoid>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

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

<task_preview>
You will generate 1 novel groundbreaking research hypothesis in the AII prompt provided in the accompanying user message.
</task_preview>

<YOUR_AII_PROMPT>
Your AII prompt — the research prompt to invent within — is provided as a SEPARATE user message in this turn, immediately following this one. Treat that message as the definition of what to generate a hypothesis for.
</YOUR_AII_PROMPT>

<hypothesis_inspiration>
<YOUR_INSPIRATION>
Human researchers overspecialize — they know their domain deeply but lack breadth to see when other fields have already solved analogous problems. Your advantage is breadth. Only propose a cross-domain transfer if it concretely outperforms existing approaches in this domain. Avoid handwavy analogies — if the imported method is vaguer or weaker than what domain experts already use, it's not worth proposing.

Explore cross-domain inspiration at three levels, from abstract to concrete. At each level, consider both established and recent developments — with slight priority for newer work, which tends to leverage more powerful tools and be less widely known.

1. CONCEPTUAL: Borrow high-level ideas, framings, or design philosophies from distant fields.
   What mental model or approach from another domain suggests a novel angle on this problem?

2. PROCEDURAL: Adapt specific problem-solving processes from other domains.
   What workflow, iterative strategy, or pipeline used elsewhere could restructure how this problem is attacked?

3. METHODOLOGICAL: Import concrete methods directly from other fields with minimal modification.
   What algorithm, formula, or technique from a different domain applies here as-is or with adaptation?

Cast wide — draw from ANY field, not just these examples: ecology, economics, physics, linguistics, game theory, control theory, materials science, cognitive science, epidemiology. The best hypotheses often come from Level 2-3 transfers that experts in the field would never encounter.
</YOUR_INSPIRATION>
</hypothesis_inspiration>

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

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, open problems, dead ends, and what counts as a genuinely novel contribution — read it BEFORE brainstorming and during the novelty check.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<YOUR_TASK>
Generate 1 novel groundbreaking research hypothesis in the AII prompt that is feasible with the above constraints.

<web_research_process>
Read and STRICTLY follow these skills: aii-web-tools.

1. DIVERGE: Brainstorm 5-7 diverse directions WITHOUT searching.
   Think across fields — what techniques from unrelated domains (ecology, economics, physics,
   linguistics, game theory, etc.) could inspire a novel mechanism? What assumptions does the field
   take for granted? Diversity matters more than depth here.

2. SEARCH: Web search for a high-level overview of each direction.
   What similar approaches exist? Is this genuinely novel or incremental? Remember: snippets
   are NOT enough for detailed understanding — treat search as discovery only.

3. FETCH & READ: MUST fetch any potentially relevant URL — you cannot assess novelty from
   snippets alone. Use the aii-web-tools skill:
   - fetch a page for high-level understanding of HTML pages
   - fetch_grep for exact details, methodology, or PDFs
   Prioritize recent papers closest to your idea. If you find significant overlap, PIVOT.

4. ADVERSARIAL NOVELTY CHECK: Actively try to DISPROVE novelty. Most important step.
   Run the FULL search checklist from <common_mistakes_to_avoid> mistake 3 — within-field
   rephrasings, cross-field core-mechanism search, failed/negative results, plain English.
   Ask: "Is the core insight of your hypothesis new, or known things in a new wrapper?"
   "Would an expert find this genuinely surprising?"
   MANDATORY SELF-CHECK: State the core mechanism in one sentence. Does it exist in ANY
   algorithm, framework, or field? If yes — even in a different framework — ABANDON.

5. FEASIBILITY CHECK: Verify your hypothesis is testable with provided resources. What specific data/compute/tools
   needed? All available within constraints?

6. ABANDON or PROCEED:
   ABANDON if: 2+ similar papers exist; you need to argue "critical differences"; core mechanism
   exists in any context.
   Abandoning is progress — go back to step 1 in a genuinely DIFFERENT direction (not a variant).
   PROCEED only if novelty is SELF-EVIDENT — an expert would immediately see it's new without
   explanation.

7. ITERATE: Expect to repeat steps 1-6 multiple times. The first few directions will likely be
   non-novel. This is normal. Don't settle for your first idea just because you've invested time.

<CRITICAL>We want SCIENTIFIC novelty (new mechanism, principle, or insight — the contribution is
knowledge), NOT application novelty (known methods applied to a new domain — the contribution is a
product). If an expert would say "clever engineering but known science," keep searching.
Hypothesis must be feasible within available resources.</CRITICAL>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>
</web_research_process>

Prioritize simplicity. Use concise, approachable language. The explanation should be fully self-contained.
</YOUR_TASK>

<previous_hypothesis>
Your hypothesis from the previous iteration. The reviewer evaluated it below.

hypothesis_id: gen_hypo_1
model: claude-opus-5
is_seeded: false
seeds: []
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
</previous_hypothesis>

<previous_review_feedback>
A reviewer evaluated your previous hypothesis and provided the feedback below.

IMPORTANT: Do NOT generate a completely new hypothesis. Take the previous hypothesis above and
REVISE it to address the feedback. Keep what works, fix what was criticized.

You MUST address ALL the critiques. Do NOT repeat the same mistakes.

kind: reviewer_feedback
id: review_hypo_3437847eb1bc
overall_assessment: |-
  This is a large, disciplined revision that fixes every one of the eleven critiques from the previous round, several of them better than the suggested remedy (the training-free task-vector safety ladder is cheaper and cleaner than the LoRA de-alignment I proposed; the reset-control arm and the pre-registered third outcome are exactly right). I independently verified all six of the 2026 arXiv citations (2608.05578 AMS/Messenger, 2606.25750 RAS/Huang et al., 2607.14147 Kwon prefill, 2602.02600 Rahimi et al. step-wise, 2606.22686 Ratnakar & Vats, 2605.05427 Hasan & Biswas) — they exist, the authors and framings are reported accurately, and the differentiator sentences are fair rather than strawmanned. That is unusually good citation hygiene for a pre-registration. Prior-art screening (arXiv full-text queries on 'early warning signals' + language model, 'hysteresis' + LLM, and scholarly search on critical slowing down + LLMs) returned nothing that occupies this lane: the critical-slowing-down / EWS toolkit has not been applied to LLM generative dynamics or to safety auditing, and no one has run a within-generation steering ramp to test for hysteresis. The core idea is genuinely novel and the mechanistic reframing (safety as a shifted operating point in behavioral state space, unit = a rate not a direction) is the kind of conceptual move that top venues reward — the field handbook's own open question 3 (knowledge-action gap: decodability does not imply actionability) is precisely what this attacks, and it attacks it from the act side, which is the underserved side.

  What still blocks a higher score is not novelty and not sloppiness; it is that three specific things remain load-bearing and under-secured. (1) The power problem I raised last round is NOT actually fixed — it has been renamed. The panel is '>= 30 units', but the bootstrap is explicitly over weight LINEAGES with interpolants excluded from independent-unit counts, and the listed panel contains roughly 10-12 distinct lineages. The power calculation stated in success_criteria assumes n = 30 and is therefore internally inconsistent with the resampling scheme the same document mandates; at n_lineage ~ 11 the 95% CI around rho = 0.8 is closer to +/-0.30, and criterion (4)'s CI-lower-bound-above-baseline requirement is again close to unattainable regardless of truth. (2) H1 as now specified is almost guaranteed to CONFIRM for a trivial reason and therefore carries almost no evidential weight: the down-ramp is measured from a prefix that already contains refusal text, so the width is fully explained by ordinary next-token conditioning on that prefix — the exact 'generic autoregressive conditioning, not safety-specific suppression' mechanism Kwon reports — and the missing control is a forced-prefix arm, not the reset arm. (3) SPI is defined by within-panel z-scores, which makes it uncomputable for the single new checkpoint the product claim is about; RAS's calibrated absolute 0-100 scale beats it on exactly this axis. Plus a genuine conceptual tension the sign conventions hide: 'near the switching point' predicts BOTH more refusal and more jailbreak fragility, and unless the expected sign is pre-registered per ground truth, H3 is close to unfalsifiable. All four are fixable on paper before any compute is spent, and fixing them is worth roughly two points.
strengths:
- >-
  Genuinely novel core move, verified by prior-art search: the early-warning-signal / critical-slowing-down toolkit (recovery
  rate, across-rollout variance, lag-1 autocorrelation, flickering) has not been applied to LLM generative dynamics or safety
  auditing. arXiv full-text queries on 'early warning signals'+'language model' and 'hysteresis'+'large language model' return
  nothing in this lane. The reframing from a static unit (direction, feature, circuit, basin volume) to a RATE is a real conceptual
  contribution, not a rebranding.
- >-
  Exceptional citation hygiene for a pre-registration. All six 2026 preprints cited were checked against arXiv and exist with
  the stated authors, titles and findings. The related-work entries do the harder thing than citing — each states an explicit
  differentiator, and two of the closest works (RAS, VISAGE) are promoted from citations to empirical baselines, which is
  what a top-venue reviewer wants to see.
- >-
  The revision is honest about prior claims it cannot own: it explicitly concedes 'shallow basin' to Peng et al. (VISAGE),
  the per-token refusal observable to Yin et al. ('Refusal Falls off a Cliff'), and the phase-transition language to Ratnakar
  & Vats. Renaming RRI to SPI with a stated sign convention and a written-out formula is exactly the requested fix.
- >-
  The pre-registered third outcome ('bistability present but not safety-specific') with a named citation basis (Kwon 2607.14147,
  Rahimi et al. 2602.02600) is model pre-registration practice — it removes the post-hoc rationalization cell that the previous
  version left open, and it correctly separates H1 from H1b.
- >-
  The training-free task-vector safety ladder W(t) = W_base + t*(W_instruct - W_base) plus partial-strength abliteration is
  a better solution to the degenerate-ground-truth problem than the LoRA de-alignment previously suggested: it costs matrix
  ops rather than training, and the lineage-exclusion caveat is stated up front rather than discovered by a reviewer.
- >-
  Ground truth is now correctly treated as three-dimensional (plain-harmful refusal, jailbreak ASR, XSTest over-refusal) on
  the basis of a real empirical finding (Hasan & Biswas: over-refusal and harmful compliance nearly uncorrelated), and the
  measurement-error treatment (LLM judge primary, string matcher as screen, Cohen's kappa, >=100 hand-adjudicated items, attenuation-corrected
  correlation) is more rigorous than most published safety-metric papers.
- >-
  The three null controls for H2 (random readout axis, random vs refusal-aligned perturbation, syntactic-probe observable)
  are well chosen: together they are what separates 'a basin' from 'generic mixing', and pre-committing that a positive result
  on the syntactic probe is DISCONFIRMING is a real falsifiability commitment.
- >-
  The abliteration circularity fix is correct and non-obvious: making the logit-lens refusal log-odds primary precisely because
  it survives an orthogonalization edit, with the diff-in-means projection demoted to descriptive, closes a hole that would
  have made criterion (2) unfalsifiable in the abliterated arm.
dimension_scores:
- dimension: soundness
  score: 3
  justification: >-
    The two fatal operationalization errors from the previous round (single-valued alpha sweep; token-position-as-time) are
    correctly fixed, and the control structure for H2 is now strong. What keeps this from a 4 is that H1's decisive test still
    has an uncontrolled trivial explanation (prefix-content conditioning rather than path dependence), the estimator statistics
    (AC1 and exponential lambda on 32-64 generated steps, non-detrended) are under-identified at the stated sequence lengths,
    and the power arithmetic contradicts the mandated resampling unit.
  improvements:
  - >-
    Add the forced-prefix control arm to H1 (see critique 2): without it, nonzero loop width is explained by next-token conditioning
    on refusal text and the decisive test decides nothing.
  - >-
    Detrend r_t before computing AC1 by subtracting the across-rollout mean trajectory at each generated step — the >=20 rollouts
    already provide the estimate — and report a synthetic-recovery check showing that the lambda estimator recovers a known
    decay constant from a 20-40 step series at the observed noise level. Both are cheap and both are the difference between
    a statistic and a number.
  - >-
    Reconcile the power statement with the lineage bootstrap: state n_lineage explicitly for the actual panel, recompute the
    CI half-width at that n, and soften criterion (4) in advance to the level that n supports.
- dimension: presentation
  score: 3
  justification: >-
    Very well organized for a pre-registration — the terms glossary, the step-numbered protocol, the pre-registered baseline
    list and the explicit CONFIRM/THIRD-OUTCOME/DISCONFIRM cells make it evaluable by an expert without further questions
    on most points. It is however dense and, more damagingly, contains two internal inconsistencies (the n=30 vs lineage-bootstrap
    arithmetic; unspecified expected signs across the three ground truths) that a careful reader hits and has to resolve for
    the authors.
  improvements:
  - >-
    Add a small table with one row per ground truth (plain-harmful refusal, jailbreak ASR, XSTest over-refusal) and columns
    for expected SIGN of the SPI correlation, the pre-registered threshold, and the theoretical reason for that sign. This
    is a five-line fix that converts the sharpest conceptual ambiguity into a falsifiable commitment.
  - >-
    Add a one-paragraph compute budget: wall-clock estimate per checkpoint for each of Step 1 / Step 2 / Step 3, with the
    honest observation that the AUDIT is cheap while the VALIDATION is not, and a tier-1 / tier-2 panel split so a partial
    run is still reportable.
  - >-
    State the number of distinct weight lineages in the panel explicitly alongside the >=30 unit count, so a reader is not
    left to count them.
- dimension: contribution
  score: 3
  justification: >-
    The question is important (cheap, harmful-content-free safety auditing of arbitrary open-weight checkpoints), the framing
    is genuinely new and verified unoccupied, the incumbents are named and run as baselines, and even the pre-registered negative
    is publishable. It is held below 4 because the headline deliverable — a score you can compute for one new checkpoint —
    is not actually computable as defined (within-panel z-scores), and because H4, the sharpest differentiating claim, rests
    on n=2 behavioral uncensored fine-tunes.
  improvements:
  - >-
    Define a frozen, panel-independent normalization for SPI (publish the reference means/sds) and demonstrate scoring of
    >=3 genuinely held-out checkpoints never used in normalization. Without this the product claim is weaker than RAS's calibrated
    0-100 scale on the exact axis it claims to beat it.
  - >-
    Raise the behavioral-uncensored-fine-tune count to >=4 CPU-feasible checkpoints, verify in advance that each actually
    preserves cluster separation and refusal-direction cosine (otherwise it is not the blind-spot class), and label H4 a pre-registered
    case study rather than a statistical claim if the count stays small.
  - >-
    State plainly in the motivation what a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space — the
    current text says the space and cost differ, but not what is newly explained. One sentence naming a phenomenon the weight-space
    basin cannot account for would materially strengthen the contribution claim.
critiques:
- id: ''
  category: rigor
  severity: major
  description: >-
    The power problem from the previous round is renamed rather than solved, and the document now contradicts itself. success_criteria
    computes power 'at n = 30 lineage-weighted units', giving a 95% CI half-width of ~+/-0.15 around rho = 0.8. But Step 4
    mandates bootstrapping over weight LINEAGES as the unit of the model-level claim, and the assumptions block explicitly
    excludes the task-vector interpolants and partial-abliteration variants from independent-unit counts. Counting the listed
    panel by lineage gives roughly 10-12 independent units (Qwen3-0.6B/1.7B/4B trios collapse to three lineages, Qwen2.5-0.5B/1.5B
    two, Llama-3.2-1B/3B two, gemma-2-2b one, SmolLM2-360M/1.7B two, TinyLlama one, plus the uncensored fine-tunes). At n_lineage
    ~ 11 the 95% bootstrap CI around an observed rho = 0.8 is roughly +/-0.30, not +/-0.15, and criterion (4)'s requirement
    that the CI lower bound exceed the best baseline correlation is close to unattainable no matter what is true — exactly
    the failure mode flagged last round. The partial rank correlation controlling for static mean AND scale (two covariates,
    strongly correlated predictors) has even less power at that n. This is not a presentational slip: the resampling unit
    and the power arithmetic must agree before any compute is spent, or the run produces a number no criterion can adjudicate.
  suggested_action: >-
    Do three things before running. (1) Enumerate the panel by LINEAGE in the pre-registration and state n_lineage explicitly
    next to the >=30 unit count. (2) Recompute the power table at that n and, if the CI-exclusion criterion is unattainable,
    replace criterion (4)'s exclusion requirement in advance with a paired comparison that has more power: bootstrap the DIFFERENCE
    (rho_SPI - rho_baseline) on the SAME resampled lineages and require the difference CI to exclude 0, which removes the
    between-lineage variance common to both and is the standard fix. (3) Expand the lineage count where it is cheapest: Pythia-410M/1B/1.4B,
    OLMo-1B, Danube3-500M, Phi-3-mini (int8), Falcon3-1B-Instruct, Granite-3.1-2B-Instruct and MiniCPM all add architecture
    families at essentially zero marginal cost given the method's own cheapness claim, and getting to ~18-20 lineages roughly
    halves the CI width.
- id: ''
  category: methodology
  severity: major
  description: >-
    H1's decisive test now has the opposite problem from last round: instead of being guaranteed to return zero, it is close
    to guaranteed to return a large positive width for a reason that has nothing to do with bistability. In the retained-prefix
    ramp, alpha_up is the coefficient at which refusal onset is emitted from a COMPLIANT prefix; alpha_down is the coefficient
    at which compliance resumes from a prefix that now CONTAINS refusal text ('I cannot help with that...'). A refusal prefix
    conditions strongly toward continued refusal in any autoregressive LM, aligned or not — this is precisely the 'generic
    autoregressive conditioning, not safety-specific suppression' mechanism Kwon (2607.14147) demonstrates with a base-model
    control, and the 'autoregressive commitment masks underlying instability' observation in Rahimi et al. (2602.02600). So
    the measured width conflates two things: path dependence through a genuine latent state (the bistability claim) and ordinary
    first-order conditioning on the literal text already emitted (trivial). The mandated reset control does not separate them:
    it discards the prefix entirely, so it removes BOTH mechanisms at once and, under greedy decoding, returns zero by pure
    construction — it is an implementation sanity check, not an informative control. As specified, H1 confirms, the entire
    evidential burden silently falls on H1b's ordering test, and a reviewer will ask why the 'decisive test' was decisive
    of nothing.
  suggested_action: >-
    Add a forced-prefix control arm, which is the control that actually isolates the claim. For each prompt, take the refusal
    prefix produced at the top of the up-ramp, force-feed it as a fixed prefill WITHOUT ever having ramped alpha up, then
    ramp alpha DOWN from the same starting value and record the flip-back threshold. Call this alpha_down_forced. Then: (width_naive
    = alpha_up - alpha_down) is the current quantity; (alpha_down - alpha_down_forced) is the residual path dependence NOT
    explained by prefix content, and that residual is what the bistability claim is actually about. Pre-register the residual,
    not width_naive, as the H1 test statistic, and report both. Additionally, pre-register the prediction that width_naive
    is large and positive in base models too (per Kwon), so that outcome is scored as expected rather than as a surprise.
    Finally, at temperature 0.7 the reset arm will NOT give exactly zero — sampling noise produces apparent width — so replace
    the 'must give width exactly 0' language with 'must give width indistinguishable from 0 at temperature 0, and its temperature-0.7
    width is the noise floor against which the retained-prefix width is compared'.
- id: ''
  category: methodology
  severity: major
  description: >-
    SPI as defined cannot be computed for the use case that motivates the whole paper. It is fixed as 'the mean of the WITHIN-PANEL
    z-scores' of four terms. Within-panel standardization means the score of any checkpoint depends on which other checkpoints
    are in the panel — so for 'any random model on Hugging Face', the deliverable the motivation promises, SPI is undefined
    until you assemble a comparison panel and re-run every model in it. This is a strictly weaker product than the incumbent
    it claims to beat: RAS (2606.25750) explicitly maps to a calibrated absolute 0-100 scale precisely so a single target
    can be scored. It also creates a subtler validity problem: a rank correlation computed on panel-standardized scores against
    panel-measured ground truth is partly a within-panel artifact, and leave-one-out accuracy in AMS's format is not comparable
    if the left-out model contributed to the normalization constants.
  suggested_action: >-
    Freeze the normalization. Compute the four terms' means and standard deviations once on a designated REFERENCE subset
    of the panel, publish those constants in the paper, and define SPI for any new checkpoint using the frozen constants only.
    Then (a) recompute all leave-one-out and leave-one-family-out numbers with the left-out model excluded from the normalization
    fit — otherwise the LOO figure is leaked and not comparable to AMS's 71%; and (b) reserve >=3 checkpoints that appear
    in NO normalization or fitting step and report their SPI and ground truth as a genuine out-of-panel demonstration. That
    demonstration, more than any correlation, is what makes the product claim credible, and it costs three extra model downloads.
- id: ''
  category: rigor
  severity: major
  description: >-
    The theory predicts opposite signs for two of the three ground truths and the pre-registration does not say which. 'Higher
    SPI = closer to the switching point = expected to refuse more' is stated in the glossary, which implies SPI correlates
    POSITIVELY with plain-harmful refusal rate. But the same construct — a shallow basin, small dominant eigenvalue, easy
    to push across the fold — is the textbook signature of FRAGILITY, which predicts HIGHER jailbreak attack-success rate,
    i.e. a model near the switch should be easy to tip into compliance. So SPI is predicted to go up with refusal rate and
    up with ASR, while refusal rate and ASR themselves are inversely related for most checkpoints. Criterion (4) asks only
    for 'rho >= 0.6 with jailbreak attack-success rate' without a sign, so as written either sign of a strong correlation
    can be read as success — which makes the headline claim close to unfalsifiable, and a reviewer will notice. This is arguably
    the most interesting theoretical question the proposal raises (nearness to a switch is not the same construct as behavioral
    safety, and the framing conflates them), and it deserves to be confronted rather than left implicit.
  suggested_action: >-
    Write a signed prediction table into the pre-registration: one row per ground truth (plain-harmful refusal rate, jailbreak
    ASR, XSTest over-refusal), each with the expected sign, the threshold, and a one-line theoretical justification. Then
    resolve the tension explicitly, and the resolution is available: distinguish SPI's two possible readings — 'the comply
    basin is shallow, so the model tips INTO refusal easily' (predicts high refusal, high over-refusal, LOW ASR) versus 'the
    model sits near a fold in both directions, so it tips either way' (predicts high refusal AND high ASR). These make different
    predictions on the sign of rho(SPI, ASR), so pre-register both as competing hypotheses with the outcome that discriminates
    them. That converts a hidden ambiguity into a genuinely informative experiment and materially raises the contribution.
- id: ''
  category: methodology
  severity: major
  description: >-
    The dynamical estimators are under-identified at the stated sequence lengths and the series is non-stationary. Generations
    are capped at 32-64 new tokens, so lambda is fit to an exponential decay over at most ~20-50 generated steps after the
    injection point, and AC1 is estimated from a series of the same length. Two problems compound. (1) Estimator variance:
    AC1 from n ~ 40 has a standard error near 1/sqrt(n) ~ 0.16 before any model noise, which is the same order as the between-model
    differences the hypothesis needs to detect; an exponential fit to a short, noisy decay is notoriously ill-conditioned
    in the decay-constant parameter. (2) Non-stationarity: r_t over generated steps has a strong deterministic trend — early
    tokens after the chat template behave systematically differently from tokens 40-60, and once a model commits to a topic
    the refusal log-odds drift. AC1 computed on a trended series measures the trend, not fluctuation around an attractor,
    which is the same class of error as the token-position version rejected last round, only milder. Rising AC1 in 'safer'
    models could simply mean those models produce more stereotyped, template-driven openings.
  suggested_action: >-
    Three fixes, all cheap. (1) Detrend before computing AC1 and Var*: you already have >=20 rollouts per prompt, so subtract
    the across-rollout MEAN trajectory at each generated step and compute AC1 on the residuals. This is the correct 'fluctuation
    around the deterministic path' quantity and it removes the stereotypy confound directly. (2) Run a synthetic-recovery
    check on the lambda estimator: simulate an AR(1)-with-known-decay process at the observed noise level and series length,
    and report the estimator's bias and variance. Pre-register a minimum series length below which lambda is not reported.
    (3) Raise max_new_tokens for the H2 rollouts specifically to 128-192 (only the H2 arm needs it; ground-truth generation
    can stay at 64), and report the indicators as a function of series length so a reader can see whether the ordering is
    stable or an artifact of truncation.
- id: ''
  category: scope
  severity: major
  description: >-
    The compute budget is not stated and the design is far heavier than the 'seconds per model' framing implies, which puts
    completion at risk. Ground truth alone is ~30 checkpoints x (80 harmful + 80 jailbreak variants + 50 XSTest) x 64+ generated
    tokens = on the order of 6,000+ generations, on CPU. H2 is ~30 checkpoints x 20 prompts x 20 rollouts x 2 arms (clean/perturbed)
    x 64 tokens, plus an epsilon sweep, plus three control conditions (random axis, random-direction perturbation, syntactic
    probe) — that alone is on the order of 100k+ generated tokens per checkpoint with residual-stream hooks active. H1 is
    30 prompts x 2 ramp directions x 2 temperatures x 30 checkpoints, plus the reset arm and (per critique 2) the forced-prefix
    arm. Add ~30 checkpoint downloads including 4B models, plus materializing task-vector interpolants (each of which is a
    full extra weight set on disk). None of this is impossible, but the design as written has no stated budget, no staging,
    and no partial-completion story — the realistic failure mode is that the run is 60% done at deadline and no criterion
    can be evaluated, which is the same amount of wasted compute as a fatal flaw.
  suggested_action: >-
    Add an explicit compute-budget paragraph with a per-step wall-clock estimate and a tiered panel. Tier 1: ~10-12 checkpoints
    spanning all >=4 families and both endpoints of the ladder, run through ALL of Steps 1-5, sufficient on its own to report
    H1/H1b/H2 with controls. Tier 2: the remaining units, added to Step 3 and Step 4 only (ground truth and correlation),
    where the marginal cost is lowest and the marginal power gain is highest. Pre-register that criteria are evaluated on
    whatever tier completes, with the tier stated. Separately — and this matters for the paper's framing — report AUDIT cost
    (what a user pays to score one new checkpoint: a handful of harmless prompts) as a distinct number from VALIDATION cost
    (what this study pays). Conflating them invites the objection that the cheap method needed an expensive study, which is
    fine and normal but must be said plainly.
- id: ''
  category: methodology
  severity: minor
  description: >-
    The task-vector safety ladder is the mechanism that rescues the ground-truth distribution from trimodality, and it can
    silently fail in a way that corrupts both the ground truth and the dynamics. Linear interpolation W(t) = W_base + t*(W_instruct
    - W_base) produces coherent models only when the two endpoints are linearly mode-connected — plausible for Qwen3 base/instruct,
    which share initialization, but at intermediate t the model may produce degenerate, repetitive or off-distribution text.
    If it does, its measured refusal rate is meaningless (a model emitting gibberish neither refuses nor complies), AND its
    r_t series is dominated by degeneracy rather than by basin geometry, so it contaminates both sides of the headline correlation
    simultaneously — which is worse than contaminating either alone, because it can manufacture a spurious correlation. The
    same risk applies to partial-strength abliteration, which is known to degrade fluency at high orthogonalization strength.
  suggested_action: >-
    Pre-register a fluency screen with an exclusion rule before any interpolant enters the analysis: perplexity on a held-out
    benign corpus (e.g. WikiText or the model's own instruct-format completions) must be within a stated factor — 2x is a
    defensible pre-registered threshold — of the t=1 endpoint, plus a degenerate-repetition check (distinct-n / max n-gram
    repeat rate). Report how many interpolants were manufactured and how many passed; if the pass rate is low, the ladder
    does not fill the middle of the range and the trimodality problem returns, which the paper must then say. Also verify
    that the passing interpolants actually produce INTERMEDIATE refusal rates rather than snapping to one endpoint — a step
    function in t would make the ladder useless for its stated purpose, and that is worth checking on one base/instruct pair
    before building all nine.
- id: ''
  category: evidence
  severity: minor
  description: >-
    H4 — 'where static geometry fails', the sharpest differentiating claim against AMS and the one that most distinguishes
    this from the incumbents — rests on 'at least two behavioral uncensored fine-tunes'. n=2 cannot support a claim of the
    form 'SPI succeeds on the class that static geometry cannot see'; it supports at most an existence proof. Worse, the claim
    has an unverified premise: the chosen checkpoints must ACTUALLY preserve harmful/benign cluster geometry and refusal-direction
    cosine, or they are not instances of the blind-spot class at all and H4 tests nothing. Dolphin/Josiefied-style models
    at <=4B are also not guaranteed to be pure behavioral fine-tunes; some publicly distributed 'uncensored' variants are
    abliterated or are merges of abliterated components, which would put them in the wrong class entirely.
  suggested_action: >-
    Raise the count to >=4 CPU-feasible behavioral fine-tunes and, critically, add a pre-analysis class-membership check:
    for each candidate, compute cluster separation sigma and refusal-direction cosine against its parent and confirm both
    are preserved (i.e. AMS-style scanning marks it safe) while its measured harmful-compliance rate is high. Only checkpoints
    passing that check count toward H4; report the ones that fail and why. Also check each model card and community discussion
    for abliteration or abliterated-merge provenance before including it. If the final count stays below 4, label H4 in advance
    as a pre-registered case study with per-model reporting rather than a statistical claim — an honest n=2 case study that
    AMS-style scanning demonstrably misses is still a strong result, and over-claiming it is the only way to lose that.
- id: ''
  category: rigor
  severity: minor
  description: >-
    Two baselines in the pre-registered list are specified at a level that makes the comparison unfalsifiable in the authors'
    favour. (a) The 'RAS/SafeVec-style representation-alignment score' is described only by its dependencies, not by its implementation;
    RAS involves layer-window stability selection and a calibration mapping, and a loose reimplementation that underperforms
    would be an unconvincing win. (b) The VISAGE-style basin volume is restricted to a 6-model subset 'with the reduction
    stated honestly' — honest, but 6 points cannot yield a rank correlation comparable to SPI's 30, so the comparison is not
    like-for-like even when reported honestly. Given that the whole H3 claim is 'beats the published incumbents', the quality
    of the incumbent implementations is load-bearing.
  suggested_action: >-
    For RAS: pre-register the exact reimplementation (reference model, layer-window selection rule, prompt sets, calibration)
    and, where the original paper reports numbers on models that overlap this panel, report a reproduction check against those
    published numbers as evidence the baseline is faithful. If reproduction is out of scope, say so and label the RAS comparison
    as 'against our reimplementation' throughout rather than 'against RAS'. For VISAGE: on the 6-model subset, report SPI's
    correlation ON THAT SAME SUBSET alongside VISAGE's, so the comparison is at matched n; the 30-model SPI number is not
    a valid comparator for a 6-model VISAGE number and a reviewer will say so.
- id: ''
  category: novelty
  severity: minor
  description: >-
    The related-work treatment is strong, but one differentiator is asserted rather than argued and it is the one carrying
    the mechanistic contribution. Against VISAGE the text says the departure is 'the space and the cost' — weight-space vs
    behavioral-state-space geometry, and harmful-benchmark-per-perturbation vs harmless prompts. The cost difference is clear
    and defensible. The SPACE difference is not yet a claim: the proposal does not say what a basin in behavioral state space
    EXPLAINS that a basin in weight space does not, so a reviewer can reasonably read it as the same phenomenon measured more
    cheaply, which is a smaller contribution than the one the motivation advertises ('a mechanistic account of what safety
    tuning buys'). The same applies, more mildly, to the reinterpretation of Qi et al.: 'shallow in behavioral state space
    rather than token depth' is asserted as a reframing but no observation is named that would distinguish the two descriptions.
  suggested_action: >-
    Name one discriminating observation for each. For VISAGE: the two accounts diverge on models where weight-space and behavior-space
    geometry come apart — a behavioral uncensored fine-tune is a candidate (large behavioral change, possibly small weight-space
    basin change), as is a task-vector interpolant (smooth weight-space path, possibly step-like behavioral change). Pre-register
    that comparison; if the behavioral basin and the weight basin rank the panel identically, say so and drop the mechanistic
    claim to a cost claim. For Qi et al.: the token-depth account predicts the safety signal is concentrated in the first
    few GENERATED steps and vanishes after; the basin account predicts lambda differences persist across generated steps.
    Step 5 already collects step-wise lambda profiles, so this discriminating test is free — state it as a named prediction
    rather than leaving it as descriptive mechanism mapping. Both additions cost nothing in compute and convert asserted differentiators
    into tested ones.
- id: ''
  category: clarity
  severity: minor
  description: >-
    The single-forward-pass measurement is retained 'only as an explicitly heuristic secondary measurement with the 1/t dilution
    null fitted and subtracted', but nothing in the success criteria or disconfirmation cells says what role, if any, it plays.
    Retained-but-unscored measurements are how a garden of forking paths gets in through the back door: if the primary generated-step
    result is null and the secondary forward-pass result is positive, the pre-registration as written gives no guidance, and
    the paper will be tempted to lead with the latter.
  suggested_action: >-
    Either drop the single-forward-pass arm entirely — it costs measurement time and buys nothing the generated-step version
    does not — or state in one sentence that it is reported as a descriptive appendix figure only, contributes to NO criterion,
    and cannot be substituted for the generated-step result under any outcome. The second option is fine; the current silence
    is not.
score: 6
confidence: 4
relation_type: evolution
relation_rationale: >-
  Same bistability/EWS frame; operationalizations, panel, controls and criteria refined to fix prior review's flaws.
</previous_review_feedback><user_data>
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
    "TermDefinition": {
      "description": "A technical term and its definition.",
      "properties": {
        "term": {
          "description": "The technical term",
          "title": "Term",
          "type": "string"
        },
        "definition": {
          "description": "Clear definition of the term",
          "title": "Definition",
          "type": "string"
        }
      },
      "required": [
        "term",
        "definition"
      ],
      "title": "TermDefinition",
      "type": "object"
    }
  },
  "description": "A research hypothesis with validation approach.",
  "properties": {
    "title": {
      "description": "Hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); name the idea, not a status.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "The core hypothesis statement",
      "title": "Hypothesis",
      "type": "string"
    },
    "motivation": {
      "description": "Why this hypothesis matters - significance and impact",
      "title": "Motivation",
      "type": "string"
    },
    "assumptions": {
      "description": "Key assumptions that must hold for this hypothesis (2-5 items)",
      "items": {
        "type": "string"
      },
      "title": "Assumptions",
      "type": "array"
    },
    "investigation_approach": {
      "description": "High-level approach to investigating this hypothesis",
      "title": "Investigation Approach",
      "type": "string"
    },
    "success_criteria": {
      "description": "What outcomes would confirm or disconfirm this hypothesis?",
      "title": "Success Criteria",
      "type": "string"
    },
    "related_works": {
      "description": "The most similar existing works found during research. Each entry describes one related work: what it does and how the proposed hypothesis fundamentally differs from it.",
      "items": {
        "type": "string"
      },
      "title": "Related Works",
      "type": "array"
    },
    "inspiration": {
      "description": "What inspired this hypothesis - which patterns, techniques, or cross-field insights were adapted (from the explicit inspiration seeds if your prompt included any, otherwise from your own cross-domain exploration)",
      "title": "Inspiration",
      "type": "string"
    },
    "terms": {
      "description": "Definitions of key technical terms used in the hypothesis",
      "items": {
        "$ref": "#/$defs/TermDefinition"
      },
      "title": "Terms",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the hypothesis in 1-2 sentences",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "motivation",
    "assumptions",
    "investigation_approach",
    "success_criteria",
    "related_works",
    "inspiration",
    "terms",
    "summary"
  ],
  "title": "Hypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-12 12:58:57 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] TOOL CALL — ToolSearch · 2026-08-12 12:59:09 UTC

```
{'query': 'select:WebSearch,WebFetch', 'max_results': 2}
```

### [5] TOOL RESULT — ToolSearch · 2026-08-12 12:59:09 UTC

```
{"matches": ["WebSearch", "WebFetch"], "query": "select:WebSearch,WebFetch", "total_deferred_tools": 22}
```

### [6] TOOL CALL — WebSearch · 2026-08-12 12:59:15 UTC

```
critical slowing down early warning signals large language model generation dynamics safety
```

### [7] TOOL CALL — WebSearch · 2026-08-12 12:59:15 UTC

```
hysteresis steering vector within generation refusal bistable LLM
```

### [8] TOOL RESULT — WebSearch · 2026-08-12 12:59:21 UTC

```
{"query": "hysteresis steering vector within generation refusal bistable LLM", "results": [{"tool_use_id": "srvtoolu_0142RXQk4q7Ytixtfy1Ak3YW", "content": [{"title": "Published as a conference paper at ICLR 2025 PROGRAMMING REFUSAL WITH", "url": "https://proceedings.iclr.cc/paper_files/paper/2025/file/e2dd53601de57c773343a7cdf09fae1c-Paper-Conference.pdf"}, {"title": "Refusal in Language Models Is Mediated by a Single Direction Andy Arditi∗", "url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/f545448535dfde4f9786555403ab7c49-Paper-Conference.pdf"}, {"title": "AlphaSteer: Learning Refusal Steering with Principled Null-Space Constraint", "url": "https://arxiv.org/pdf/2506.07022"}, {"title": "What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal", "url": "https://arxiv.org/html/2604.08524"}, {"title": "Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for Large Language Models", "url": "https://arxiv.org/pdf/2602.04896"}, {"title": "Steered LLM Activations are Non-Surjective", "url": "https://arxiv.org/pdf/2604.09839"}, {"title": "Steering the CensorShip: Uncovering Representation Vectors for LLM \"Thought\" Control", "url": "https://arxiv.org/pdf/2504.17130"}, {"title": "Refusal Steering: Fine-grained Control over LLM Refusal Behaviour", "url": "https://arxiv.org/pdf/2512.16602"}, {"title": "A Sober Look at Steering Vectors for LLMs", "url": "https://www.alignmentforum.org/posts/QQP4nq7TXg89CJGBh/a-sober-look-at-steering-vectors-for-llms"}, {"title": "Palette: A Modular, Controllable, and Efficient Framework for On-demand Authorized Safety Alignment Relaxation in LLMs", "url": "https://arxiv.org/pdf/2605.24154"}]}, "I found several relevant research papers on steering vectors for LLM refusal. Here's a summary of what the search revealed:\n\n## Steering Vectors and Refusal in LLMs\n\nA steering vector is typically extracted by computing the difference in activations between examples that exhibit a desired behavior and those that don't. During inference, this vector is added to the model's hidden states at a chosen layer, scaled by a hyperparameter, and the model completes generation using these modified activations.\n\n### Key Findings on Refusal Steering\n\nWhile activation steering has shown promise in altering LLM behavior such as removing or inducing refusal behavior, a key limitation is the inability to condition when and what to refuse, as adding a \"refusal vector\" increases refusal rates indiscriminately across all inputs.\n\nThe difference-in-means method computes steering vectors as the difference in activation mean between two sets of prompts with contrasting concepts, such as \"refusal\" and \"non-refusal\".\n\n### Mechanistic Studies\n\nRecent research has also examined how these steering vectors work mechanistically. Refusal steering interacts with attention primarily through the OV circuit.\n\nThe search results include several recent papers (2025-2026) addressing challenges like maintaining utility while controlling refusal behavior, and developing more sophisticated steering methods with better control mechanisms."], "durationSeconds": 7.554339042, "searchCount": 1}
```

### [9] TOOL RESULT — WebSearch · 2026-08-12 12:59:21 UTC

```
{"query": "critical slowing down early warning signals large language model generation dynamics safety", "results": [{"tool_use_id": "srvtoolu_01NryKJXEJ21WukuoEYzmsJN", "content": [{"title": "Critical Slowing Down in a Real Physical System", "url": "https://arxiv.org/pdf/2403.17973"}, {"title": "Early warning signals for loss of control in complex systems | PNAS", "url": "https://www.pnas.org/doi/10.1073/pnas.2608847123"}, {"title": "Probing the Safety Response Boundary of Large Language Models via Unsafe Decoding Path Generation WARNING: This paper contains model outputs which are offensive in nature.", "url": "https://arxiv.org/html/2408.10668v3"}, {"title": "Overlapping Time Scales Obscure Early Warning Signals of the Second COVID-19 Wave", "url": "https://www.medrxiv.org/content/10.1101/2021.07.27.21261226.full.pdf"}, {"title": "Entropy Collapse: A Universal Failure Mode of Intelligent Systems", "url": "https://arxiv.org/pdf/2512.12381"}, {"title": "Overlapping timescales obscure early warning signals of the second COVID-19 wave", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8825995/"}, {"title": "Identifying early-warning signals of critical transitions with strong noise by dynamical network markers | Scientific Reports", "url": "https://www.nature.com/articles/srep17501"}, {"title": "Detecting critical slowing down in high-dimensional epidemiological systems", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7082051/"}, {"title": "System Identification near a Hopf Bifurcation via the Noise-Induced   Dynamics in the Fixed-Point Regime", "url": "https://arxiv.org/pdf/2101.06828"}]}, "Based on the search results, here's what I found regarding critical slowing down, early warning signals, large language models, generation dynamics, and safety:\n\n## Critical Slowing Down and Early Warning Signals\n\nCritical slowing down describes the phenomenon that many systems, as they approach their critical point, return more slowly to their equilibrium after small external perturbations, resulting in an increase in statistics such as the local autocorrelation coefficient and variance. This phenomenon has been shown to occur in the climate, biology, and other complex nonlinear systems approaching criticality.\n\n## Application to Complex Systems\n\nLow-dimensional epidemiological models predict that epidemic transitions are preceded by critical slowing down, which has raised the possibility of anticipating disease emergence using CSD-based early-warning signals, which are statistical moments estimated from time series data. These indicators could apply across a wider class of controlled systems including reactors, aircraft, and self-driving cars.\n\n## LLM Safety and Generation Dynamics\n\nThe search results include research on safety alignment techniques such as SFT or RLHF, where models can still exhibit vulnerabilities in their early token generation, which can be exploited to elicit toxic responses. Additionally, language models trained on recursively generated data lose output diversity.\n\nHowever, the search results don't contain specific research directly connecting critical slowing down theory to large language model generation dynamics or safety. The results suggest these are emerging areas of investigation rather than well-established intersections."], "durationSeconds": 7.589655601000002, "searchCount": 1}
```

### [10] TOOL CALL — WebFetch · 2026-08-12 12:59:29 UTC

```
URL: https://arxiv.org/pdf/2602.04896
Prompt: What is the core claim, method, and main finding? Does it measure hysteresis, recovery rates, variance, autocorrelation, or bistability? Authors and title exactly.
```

### [11] TOOL CALL — WebFetch · 2026-08-12 12:59:29 UTC

```
URL: https://arxiv.org/abs/2604.09839
Prompt: Exact title, authors, core claim and method. Does it involve ramping steering coefficients, hysteresis, or path dependence?
```

### [12] TOOL RESULT — WebFetch [ERROR] · 2026-08-12 12:59:29 UTC

```
Error: maxContentLength size of 10485760 exceeded
```

### [13] TOOL RESULT — WebFetch · 2026-08-12 12:59:33 UTC

```
{"bytes": 41444, "code": 200, "codeText": "OK", "result": "# Paper Summary\n\n**Title:** \"Steered LLM Activations are Non-Surjective\"\n\n**Authors:** Aayush Mishra, Daniel Khashabi, Anqi Liu\n\n**Core Claim:** The researchers argue that \"activation steering pushes the residual stream off the manifold of states reachable from discrete prompts.\" Their fundamental assertion is that steered behaviors cannot be reproduced through natural prompting, establishing a formal separation between white-box steering and black-box prompting capabilities.\n\n**Method:** The work frames the question as a mathematical surjectivity problem—examining whether every steered activation has a corresponding preimage achievable through the model's standard forward pass. Under practical assumptions, they prove this theoretically and validate findings empirically across three major language models.\n\n**Regarding Your Specific Questions:** The abstract and available metadata do not mention ramping steering coefficients, hysteresis, or path dependence. The paper focuses on the fundamental non-surjectivity property rather than dynamic steering coefficient manipulations or temporal effects.", "durationMs": 4241, "url": "https://arxiv.org/abs/2604.09839"}
```

### [14] TOOL CALL — WebFetch · 2026-08-12 12:59:43 UTC

```
URL: https://arxiv.org/abs/2602.04896
Prompt: Exact title, authors, core finding. Does benign steering increase jailbreak risk, and by what mechanism?
```

### [15] TOOL RESULT — WebFetch · 2026-08-12 12:59:43 UTC

```
{"bytes": 42271, "code": 200, "codeText": "OK", "result": "# Paper Summary\n\n**Title:** \"Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for Large Language Models\"\n\n**Authors:** Chen Xiong, Zhiyuan He, Pin-Yu Chen, Ching-Yun Ko, Tsung-Yi Ho\n\n## Core Finding\n\nYes, benign steering demonstrably increases jailbreak vulnerability. The researchers discovered that \"steering vectors derived from entirely benign datasets...inadvertently erode safety guardrails,\" with attack success rates exceeding 80% on standard benchmarks.\n\n## Mechanism\n\nThe paper identifies \"Steering Externalities\"—an unintended consequence where activation steering vectors optimized for legitimate purposes (compliance, JSON formatting, etc.) systematically weaken the model's safety alignment. These interventions act as \"a force multiplier, creating new vulnerabilities to jailbreaks\" by bypassing existing safety mechanisms.\n\nThe critical insight is that inference-time utility improvements erode what researchers call the \"safety margin,\" making models more susceptible to black-box attacks despite being developed through benign alignment techniques.\n\nThis represents a significant deployment vulnerability: developers can inadvertently compromise safety while pursuing legitimate performance enhancements.", "durationMs": 4779, "url": "https://arxiv.org/abs/2602.04896"}
```

### [16] ASSISTANT · 2026-08-12 13:02:55 UTC

```
Prior-art lane still clear; two new relevant papers found (non-surjectivity of steering; steering externalities/safety margin) which I'll fold in. Writing the revised hypothesis.
```

### [17] TOOL CALL — Write · 2026-08-12 13:02:55 UTC

```
File: /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_3/gen_hypo/claude_agent/.terminal_claude_agent_struct_out.json

{
  "title": "Safety as nearness to a tipping point",
  "hypothesis": "Safety fine-tuning does not merely install a harm detector; it moves the model's default generative state close to a bistable switching point between 'comply' and 'refuse'. Because of this, a safety-aligned model is measurably 'twitchy' about refusal even while generating completely harmless text, while base and uncensored models sit deep inside the comply basin. All claims concern the genuine stochastic dynamical system in an LLM - autoregressive generation under temperature sampling, whose state is the generated prefix plus KV cache - measured over GENERATED steps. The single-forward-pass version of the measurement is DROPPED entirely (it contributed to no criterion and its decay was dominated by 1/t attention dilution). Concretely:\n\n(H1 - path dependence beyond prefix content) Ramping a steering coefficient alpha along a refusal axis WITHIN one generation until refusal onset (alpha_up) and then ramping back down with the prefix and KV cache retained gives a flip-back threshold alpha_down. The pre-registered H1 test statistic is NOT the naive width alpha_up - alpha_down, which ordinary conditioning on already-emitted refusal text explains and which we predict IN ADVANCE to be large and positive even in base models. It is the RESIDUAL alpha_down - alpha_down_forced, where alpha_down_forced is measured after force-feeding the identical refusal prefix as a prefill WITHOUT ever ramping alpha up. The residual is the part of the path dependence that the literal emitted text cannot explain, i.e. the part attributable to a persistent latent state.\n\n(H1b - safety specificity, separable from H1) The residual is ordered instruct > base and instruct > abliterated, paired over prompts.\n\n(H2 - critical slowing down) On harmless prompts only, over generated steps and across sampled rollouts, a small residual-stream perturbation decays more slowly (lower recovery rate lambda) and the DETRENDED refusal observable shows larger across-rollout variance, higher lag-1 autocorrelation, and more near-threshold flickering, in models that are behaviorally safer - the early-warning-signal signature of proximity to a fold bifurcation.\n\n(H2b - which side the fold is on) Recovery is measured separately for a nudge TOWARD refusal and a nudge TOWARD compliance, giving lambda_toward_refuse and lambda_toward_comply. Their log ratio (the Asymmetry Index) discriminates two competing readings of 'nearness to a switch': ASYMMETRIC (the comply basin is shallow, the model tips into refusal easily - predicts high refusal, high over-refusal, LOWER jailbreak success) versus DOUBLE-SIDED (the model sits near a fold in both directions - predicts high refusal AND high jailbreak success).\n\n(H3 - prediction, with signs pre-registered per ground truth) A scalar computed from harmless-input dynamics with FROZEN, published normalization constants - the Switching Proximity Index (SPI) - rank-orders unseen open-weight checkpoints on three separately measured ground truths with pre-registered signs: positive with plain-harmful refusal rate, positive with XSTest over-refusal rate, and with the sign on jailbreak attack-success rate left as the discriminating outcome between the two readings above. SPI must beat the static mean level of the refusal observable, two zero-internals output-side baselines, and reimplementations of AMS, RAS and VISAGE, by a PAIRED bootstrap of the correlation difference over weight lineages.\n\n(H4 - where static geometry fails, pre-registered as a case study) SPI flags behavioral uncensored fine-tunes that pass an explicit class-membership check (cluster separation and refusal-direction cosine preserved, harmful compliance high, no abliteration in provenance) and are therefore a documented blind spot of activation-geometry scanners.",
  "motivation": "Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator to hold and send harmful content. The published cheap alternatives all retain a dependency this proposal drops. AMS (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy over 14 configurations and explicitly reports that behavioral uncensored fine-tunes preserving geometry are undetectable by it. RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe and jailbreak prompts AND a safety-aligned reference model. VISAGE (arXiv:2405.17374) measures a safety basin in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static, read-side measurements. That question provably does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.\n\nThis hypothesis attacks the gap from the act side with a different unit: not a direction, feature or basin volume, but a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge while doing something innocuous?\n\nWhat a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space is now stated as a testable divergence rather than asserted. The two accounts must rank the panel identically unless weight-space and behavior-space geometry come apart, and we pre-register the two places they should: (a) a behavioral uncensored fine-tune, where a small weight displacement produces a large behavioral change, and (b) a task-vector interpolant, where a smooth weight-space path may produce a step-like behavioral change. A phenomenon the weight-space basin cannot account for is therefore named in advance: a checkpoint whose weight-space basin volume is unchanged from its parent while its behavioral relaxation rate collapses. If the two rankings coincide, we say so and demote the mechanistic claim to a cost claim. The reinterpretation of Qi et al. gets the same treatment: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes afterwards, while the basin account predicts lambda differences PERSIST deep into generation. Step 5 already collects step-wise lambda profiles, so this discriminating test is free.\n\nIf true this yields (a) a mechanistic account of what safety tuning buys, in the language of bistable systems - a shifted operating point; (b) an audit needing a handful of harmless prompts, no harmful content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.",
  "assumptions": [
    "Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over GENERATED steps. The series is NON-STATIONARY (chat-template openings and topic commitment produce a strong deterministic trend), so all fluctuation statistics are computed on residuals after subtracting the ACROSS-ROLLOUT mean trajectory at each generated step, estimated from the >= 20 rollouts we already collect. Without detrending, a high lag-1 autocorrelation would only mean 'this model produces stereotyped openings'.",
    "The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives the abliteration weight edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is primary precisely because a projection onto the abliterated direction is near-constant by construction, which would make any variance claim on abliterated models circular. The per-model diff-in-means axis is descriptive only.",
    "Steering-based tests (H1) probe states that are partly OFF the manifold reachable by prompting (arXiv:2604.09839 proves steered activations are non-surjective). H1 is therefore scoped as a statement about the steered dynamical system, and the safety claim of record (H3) uses only unsteered sampling plus a norm-epsilon perturbation whose linearity is verified by an epsilon sweep, so the product claim never rests on off-manifold behaviour.",
    "A graded safety ladder can be manufactured without training by scaling the alignment task vector W(t) = W_base + t*(W_instruct - W_base) and by scaling abliteration strength - but only if the interpolants stay fluent. Every interpolant must pass a pre-registered screen (WikiText perplexity within 2x of the t=1 endpoint, plus a distinct-3 / max-n-gram-repeat degeneracy check) before entering any analysis, because a degenerate model neither refuses nor complies AND has a degeneracy-dominated r_t series, which would corrupt both sides of the headline correlation at once and could manufacture a spurious result. Interpolants share a weight lineage and never count as independent units.",
    "Small models (0.36B-4B, int8/float32, batched rollouts) show the same qualitative refusal machinery reported for larger models. This is tested rather than assumed via a within-family scale ladder (Qwen3 0.6B/1.7B/4B), because a small model that is twitchy may be twitchy from undertraining; scale enters the headline analysis as a covariate."
  ],
  "investigation_approach": "PANEL, ENUMERATED BY LINEAGE (the resampling unit). 20 distinct weight lineages, >= 8 architecture families, all CPU-feasible: Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B (each contributing base + instruct + abliterated members), Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Llama-3.2-3B, gemma-2-2b, SmolLM2-360M, SmolLM2-1.7B, TinyLlama-1.1B, Pythia-410M, Pythia-1B, Pythia-1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B, plus >= 4 behavioral uncensored fine-tunes (their own lineages). Base-only lineages (Pythia, OLMo) anchor the low-refusal end. Total measured UNITS (members) ~ 45-55; n_lineage = 20. Every model-level statistic is bootstrapped over the 20 lineages; the member/prompt bootstrap is reported separately and labelled measurement noise.\n\nSTEP 0 - PRE-REGISTRATION (written before any run).\n(a) Layer L is fixed by a rule that never touches the outcome: the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set for ONE reference model, transferred by relative depth L/n_layers. Full layer profiles are secondary, Holm-corrected, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies.\n(b) Decoding fixed and reported: chat template, empty system prompt, temperature 0.7 for dynamics and 0.0 for deterministic controls; max_new_tokens = 192 for the H2 dynamics arm (needed for estimator identifiability) and 64 for ground-truth generation.\n(c) SPI is fixed a priori as the mean of FOUR z-scored terms [-log lambda, log detrended across-rollout variance, Fisher-z of detrended AC1, logit of flicker rate], PLUS - crucially - the z-scoring uses FROZEN normalization constants (means and sds) fit once on a designated REFERENCE subset of 6 named lineages and PUBLISHED in the paper. SPI for any new checkpoint uses only those frozen constants, so it is computable for a single model with no comparison panel (the defect that made the previous definition weaker than RAS's absolute 0-100 scale). All leave-one-out and leave-one-family-out numbers are recomputed with the left-out model excluded from the normalization fit. >= 3 checkpoints are reserved that appear in NO normalization and NO fitting step, and their SPI plus ground truth is reported as the out-of-panel demonstration.\n(d) SIGNED PREDICTION TABLE, one row per ground truth: plain-harmful refusal rate -> expected sign POSITIVE, threshold rho >= 0.6, reason: nearness to the switch makes the refuse mode easy to enter. XSTest over-refusal rate -> POSITIVE, rho >= 0.45, same reason applied to benign-but-scary prompts. Jailbreak attack-success rate -> SIGN IS THE DISCRIMINATING OUTCOME: the ASYMMETRIC reading predicts NEGATIVE (the shallow basin is the comply basin, so the model falls into refusal and is hard to tip out), the DOUBLE-SIDED reading predicts POSITIVE (near a fold in both directions, so it tips either way). Both are pre-registered as competing hypotheses; the outcome that discriminates them is the sign of the partial rank correlation of SPI with ASR controlling for plain-harmful refusal rate, corroborated by the Asymmetry Index of H2b. Either sign is informative; an unsigned rho would have been unfalsifiable.\n(e) Single-forward-pass measurement: DROPPED, not retained as an appendix, so it cannot be substituted for the generated-step result.\n\nSTEP 1 - H1, three ramp arms. For each of >= 30 benign prompts: (i) UP-RAMP, raise alpha per generated token until a refusal-onset token is emitted -> alpha_up. (ii) RETAINED-PREFIX DOWN-RAMP, continue the same sequence with prefix and KV cache kept, lowering alpha -> alpha_down. (iii) FORCED-PREFIX DOWN-RAMP (the control that isolates the claim), force-feed the identical refusal prefix as a prefill without ever ramping up, then ramp alpha down from the same start -> alpha_down_forced. Test statistic = residual = alpha_down - alpha_down_forced, bootstrapped over prompts and lineages. width_naive = alpha_up - alpha_down is reported alongside, with the PRE-REGISTERED expectation that it is large and positive in base models too (per Kwon 2607.14147). A reset arm that discards the prefix between steps is retained as an implementation sanity check only: it must be indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the NOISE FLOOR against which retained-prefix quantities are compared (it will not be exactly 0 under sampling).\n\nSTEP 2 - H2/H2b, early-warning indicators on harmless input only. Per benign prompt (~20 prompts), >= 20 paired-seed rollouts, 192 generated tokens. Perturbed arm: inject a norm-epsilon vector into the residual stream at layer L at step p, continue decoding, fit an exponential to |delta r_t| over subsequent generated steps -> lambda, run separately for refusal-directed and compliance-directed nudges (H2b). Clean rollouts give detrended Var*, detrended AC1, and flicker rate. Estimator hygiene, all pre-registered: subtract the across-rollout mean trajectory before AC1/Var*; a SYNTHETIC RECOVERY CHECK simulating AR(1) with known decay at the observed noise level and series length, reporting the estimator's bias and variance and a minimum series length below which lambda is not reported; and indicators reported as a function of series length so truncation artifacts are visible. Epsilon sweep confirms linearity. Three null controls: random readout axis (must NOT reproduce the safety ordering), random vs refusal-aligned perturbation, and a syntactic (part-of-speech probe) observable, which should decay at the same rate if what is being measured is generic mixing.\n\nSTEP 3 - ground truth, three axes. Per member: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same under a fixed small jailbreak suite including prefill (ASR), ~50 XSTest benign-but-scary prompts (over-refusal). Scoring: cheap OpenRouter LLM judge PRIMARY, refusal-string matcher as screen, Cohen's kappa reported, >= 100 hand-adjudicated stratified items to estimate judge error, attenuation-corrected correlations alongside raw. Budget < $2 of the $10 cap. Interpolants additionally pass the fluency screen, and the ladder is PILOTED on one base/instruct pair first to confirm refusal rate varies smoothly in t rather than snapping to an endpoint; counts manufactured vs passed are reported, and if the pass rate is low the paper states that trimodality returns.\n\nSTEP 4 - H3/H4, prediction with matched-n, faithful baselines. Spearman rho of SPI with each ground truth. The headline comparison is a PAIRED bootstrap of the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages, required to exclude 0 - this removes between-lineage variance common to both and is what n_lineage = 20 can actually support. Baselines: (a) static mean level of r on benign prompts; (b) two zero-internals output-side detectors (next-token probability of refusal-onset tokens; ever-emits-an-apology-token); (c) AMS-style cluster separation sigma and refusal-direction cosine, with leave-one-out accuracy reported in AMS's own format and leave-one-FAMILY-out; (d) a RAS/SafeVec reimplementation whose reference model, layer-window selection rule, prompt sets and calibration mapping are pre-registered, with a reproduction check against RAS's published numbers on overlapping models - if reproduction is out of scope it is labelled 'our RAS reimplementation' throughout, not 'RAS'; (e) VISAGE-style weight-perturbation basin volume on a 6-model subset, with SPI's correlation reported ON THAT SAME SUBSET so the comparison is at matched n. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND model scale. H4 candidates must pass the class-membership pre-check (sigma and refusal-direction cosine preserved vs parent, harmful compliance high, model card and community provenance checked for abliteration or abliterated-merge components); failures are reported with reasons, and if fewer than 4 pass, H4 is reported as a pre-registered case study with per-model detail rather than a statistical claim.\n\nSTEP 5 - mechanism map and the two discriminating tests. Layer-wise and step-wise lambda profiles for base vs instruct vs abliterated vs interpolants: does the basin shallow monotonically in t; does abliteration revert to base or produce a third state; and the two named predictions - (i) does the behavioral basin rank the panel differently from VISAGE's weight basin on behavioral fine-tunes and interpolants (versus the account, if identical); (ii) do lambda differences persist deep into generation (basin account) or vanish after the first few generated steps (Qi et al. token-depth account).\n\nCOMPUTE BUDGET AND STAGING (previously absent). Audit cost and validation cost are reported separately. AUDIT (what a user pays to score one new checkpoint): 20 benign prompts x 20 rollouts x 2 arms x 192 tokens with batched rollouts and hooks active - roughly 10-15 min on one consumer GPU, or ~40-60 min on CPU int8 at <= 1.7B. VALIDATION (what this study pays): Step 3 dominates, ~50 members x 210 prompts x 64 tokens. Tiering, pre-registered: TIER 0 smoke, 3 checkpoints, verifies the full pipeline end to end. TIER 1, 12 checkpoints spanning all families and both ladder endpoints, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2/H2b with controls. TIER 2, remaining members added to Steps 3-4 only (ground truth and correlation), where marginal cost is lowest and marginal power highest. Criteria are evaluated on whatever tier completes, with the tier stated; a partial run is therefore still reportable.",
  "success_criteria": "POWER, reconciled with the resampling unit (the previous version's n=30 arithmetic contradicted its own lineage bootstrap). n_lineage = 20. At n = 20 the 95% bootstrap CI half-width around an observed Spearman rho = 0.8 is roughly +/-0.22, so a criterion requiring SPI's CI lower bound to exceed a baseline's point estimate is NOT attainable regardless of truth and is replaced in advance by the PAIRED difference test, which removes the shared between-lineage variance. Partial correlations with two covariates have adequate power only for partial rho >= 0.5; criteria are set at that level.\n\nCONFIRMS:\n(1) The H1 residual (alpha_down - alpha_down_forced) is significantly > 0 with a bootstrap CI excluding 0 and exceeding the temperature-0.7 noise floor - path dependence exists that the emitted refusal text does not explain.\n(2) The residual is ordered instruct > base and instruct > abliterated, paired over prompts, CIs excluding 0.\n(3) On harmless prompts only, over generated steps, with DETRENDED statistics and a passing synthetic-recovery check: lambda lower and Var*, AC1, flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls.\n(4) SPI computed with FROZEN constants attains rho >= 0.6 with plain-harmful refusal rate (positive sign, as pre-registered) and rho >= 0.45 with XSTest over-refusal (positive), and the PAIRED bootstrap of rho_SPI - rho_baseline excludes 0 against the best of the static mean and the two zero-internals baselines; the partial correlation controlling for static mean and scale has a 95% CI excluding 0 at partial rho >= 0.5.\n(5) The jailbreak-ASR row resolves in EITHER direction with a partial correlation CI excluding 0 controlling for refusal rate, and the Asymmetry Index of H2b agrees with that sign. This is scored as a confirmed discrimination between the asymmetric and double-sided readings, not as a pass/fail.\n(6) SPI matches or beats AMS leave-one-out accuracy in AMS's own format with the left-out model excluded from normalization, and matches the RAS reimplementation and VISAGE (the latter at matched n on its 6-model subset) without needing their harmful prompts or reference model.\n(7) The >= 3 fully held-out checkpoints are scored correctly from frozen constants alone - the actual product claim.\n(8) H4: every behavioral uncensored fine-tune passing the class-membership check is flagged by SPI while cluster separation and refusal-direction cosine both mark it safe. Reported as a statistical claim only if >= 4 pass, otherwise as a pre-registered case study.\n\nTHIRD OUTCOMES, PRE-REGISTERED (informative, not failures): (a) 'bistability present but not safety-specific' - the residual is nonzero in base models too, in which case H1 is confirmed and H1b refuted and only the quantitative ordering carries safety information (live because Kwon 2607.14147 attributes prefill grip to generic autoregressive conditioning and Rahimi et al. 2602.02600 report that autoregressive commitment masks instability). (b) Behavioral basin and VISAGE weight basin rank the panel identically - the mechanistic claim is then dropped to a cost claim, stated plainly. (c) The interpolant ladder fails its fluency screen or snaps to endpoints - the trimodality problem returns and is reported as a limitation on the correlation's interpretability.\n\nDISCONFIRMS (reported as refutation, not salvaged): the H1 residual is indistinguishable from the noise floor, i.e. all path dependence is prefix content and the bistable framing adds nothing; or lambda / Var* / AC1 / flicker show no consistent ordering with any ground truth once detrended; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured; or the correlation vanishes once static mean and scale are partialled out; or a zero-internals output-side baseline ties SPI in the paired difference test; or the held-out checkpoints are mis-scored under frozen constants, meaning the metric is a within-panel artifact; or indicators work within one family but fail leave-one-family-out, bounding the metric to a within-family diagnostic.",
  "related_works": [
    "Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access 2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) across 14 configurations and 4 families, 71% leave-one-out accuracy, compliance prediction r = -0.546, and explicitly reports behavioral uncensored fine-tunes as undetectable. Closest work and sharpest departure: static read-side property from harmful prompts versus our dynamical act-side RATE from harmless prompts only. Its documented blind spot is our H4 case study, and we report LOO accuracy in its format with the left-out model excluded from our normalization fit so the comparison is not leaked.",
    "Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state alignment under unsafe and jailbreak prompts, mapped to a calibrated absolute 0-100 scale. It is the incumbent for our product claim and the reason we now FREEZE SPI's normalization constants: a within-panel z-score cannot score a single new checkpoint, which is exactly RAS's advantage. Run as a pre-registered reimplementation with a reproduction check on overlapping models, and labelled 'our reimplementation' if reproduction is out of scope. It needs harmful and jailbreak prompts and a reference model; SPI needs neither.",
    "Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the safety basin in WEIGHT space and proposes the VISAGE basin-volume metric, requiring a harmful benchmark at every weight perturbation. 'Shallow basin' is their language and we say so. The departure is now a TESTED prediction rather than an assertion: the accounts diverge where weight-space and behavior-space geometry come apart (behavioral uncensored fine-tunes; task-vector interpolants). VISAGE is run on a 6-model subset with SPI reported on that same subset at matched n; if the rankings coincide we drop the mechanistic claim to a cost claim.",
    "Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with linear probes, finding a sharp drop at final tokens in poorly aligned reasoning models. The per-position refusal score is an existing observable which we adopt rather than coin; our contribution is the detrended dynamical statistics computed on it across sampled rollouts plus the residual hysteresis test.",
    "Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - shows diffusion remasking enables recovery from harmful intermediate generations and proposes the SRI internal-dynamics signal, observing that autoregressive commitment masks underlying instability. Closest 'dynamics during decoding' work: it compares SAMPLING MECHANISMS, we hold sampling fixed and use controlled perturbation-recovery as an ESTIMATOR of distance to a switching point. Its commitment finding is a named pre-registered threat.",
    "Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - prefill jailbreak study: harm representation stays intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific collapse, concluding the prefill's grip is generic autoregressive conditioning rather than safety-specific suppression. This is precisely why H1's test statistic is now the FORCED-PREFIX RESIDUAL rather than the naive loop width, which this paper's mechanism would otherwise explain entirely.",
    "Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive Logit Steering plus prefix injection induces a phase transition where guardrails collapse, and reports 'Late Decision' (Llama, 95% ASR) vs 'Early Divergence' (Qwen, safety integrated at ~40% depth) topologies. Phase-transition language exists here but as an ATTACK that crosses the edge; our point is estimating distance to the edge without crossing it. Its topology finding drives our relative-depth layer transfer.",
    "Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal and harmful compliance nearly uncorrelated. This is why three ground truths are predicted separately, and why the signed prediction table (positive for refusal and over-refusal, sign-as-outcome for ASR) is a real commitment rather than bookkeeping.",
    "Xiong et al., 'Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for LLMs' (arXiv:2602.04896, 2026) - steering vectors from entirely benign data erode guardrails, with ASR above 80%, framed as consumption of a 'safety margin'. This is direct empirical support that a margin exists and is small in aligned models, and it is the strongest existing evidence for the DOUBLE-SIDED reading in H2b. It measures the consequence of crossing the margin; we measure the margin's width from harmless generation without crossing it.",
    "Mishra, Khashabi and Liu, 'Steered LLM Activations are Non-Surjective' (arXiv:2604.09839, 2026) - proves steered residual streams leave the manifold reachable from discrete prompts. A scope constraint we now state explicitly: H1's ramp probes the steered system, so the product claim (H3) rests only on unsteered sampling plus a verified-linear norm-epsilon perturbation.",
    "Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the static geometric account and our instrument for producing (and partially producing) uncensored checkpoints. Because abliteration orthogonalizes writes against that direction, we deliberately do NOT use a projection onto it as the primary observable.",
    "Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows aligned and unaligned generative distributions differ mainly over the first few output tokens. Their account and ours make DIFFERENT predictions we now test: token depth predicts the safety signal is confined to the first few generated steps, the basin account predicts lambda differences persist across generated steps.",
    "Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering near a fold bifurcation). The imported source, not a competitor; scholarly search finds it applied to ecosystems, climate, financial crises, depression and sleep, but not to LLM generative dynamics or safety auditing."
  ],
  "inspiration": "The transfer is from ecology and climate science at the methodological level. Ecologists face this problem in a different costume: they must know how close a lake, forest or fish population is to collapsing without running the experiment of collapsing it. Scheffer's early-warning-signal programme solved it by measuring the response to small, harmless disturbances - as a system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery from tiny nudges slows, fluctuations grow in variance, become more autocorrelated, and the system flickers. Resilience becomes measurable without pushing the system over the edge. Mapped onto model auditing: don't jailbreak a model to learn whether it can be jailbroken - nudge it gently while it does something innocuous and watch how fast it settles back. The import is legitimate only where a real stochastic dynamical system exists, which is why the measurement lives in autoregressive sampling and why the single-forward-pass version has now been dropped rather than kept as a heuristic. Ecology also supplies the fix for the statistics: EWS practitioners detrend before computing autocorrelation for exactly the reason we now must - a trend inflates AC1 and fakes the signal. Two further imports: from physics and materials science, the hysteresis loop as the decisive test of genuine bistability, which forces the sweep to happen within one generation with the prefix retained - and, following the same tradition's insistence on separating a real state variable from a memory of the drive, the forced-prefix control that isolates latent path dependence from conditioning on already-emitted text. From experimental genetics, the base / safety-tuned / abliterated series read as wild-type / knock-in / knock-out, extended to a dose-response ladder by scaling the alignment task vector, with a viability screen on the intermediates the way a geneticist screens for non-viable phenotypes. What a domain expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object - a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.",
  "terms": [
    {
      "term": "Refusal observable (r_t)",
      "definition": "A scalar read off the model at each GENERATED step t. Primary form: logit-lens log-odds of refusal-onset tokens against continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. All fluctuation statistics use the DETRENDED residual, obtained by subtracting the across-rollout mean trajectory at each generated step."
    },
    {
      "term": "Critical slowing down",
      "definition": "The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows, fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in ecology, climate science and psychiatry for estimating resilience without triggering collapse."
    },
    {
      "term": "Recovery rate (lambda)",
      "definition": "The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small residual-stream perturbation, averaged over >= 20 paired-seed rollouts of 192 tokens. Small lambda = slow recovery = shallow basin = close to switching. Its identifiability at the actual series length and noise level is verified by a synthetic AR(1) recovery check with a pre-registered minimum series length."
    },
    {
      "term": "Asymmetry Index",
      "definition": "log(lambda_toward_refuse / lambda_toward_comply): recovery from a nudge pushing toward refusal versus one pushing toward compliance. It distinguishes an ASYMMETRIC shallow comply basin (tips into refusal easily, so high refusal but LOW jailbreak success) from a DOUBLE-SIDED fold (tips either way, so high refusal AND high jailbreak success) - the two readings of 'nearness to a switch' whose conflation previously left the jailbreak prediction unsigned."
    },
    {
      "term": "Switching Proximity Index (SPI)",
      "definition": "The proposed safety metric: the mean of four terms [-log lambda, log detrended across-rollout variance of r, Fisher-z of detrended lag-1 autocorrelation, logit of flicker rate], standardized with FROZEN normalization constants fit once on a named 6-lineage reference subset and published, so SPI is computable for a single new checkpoint with no comparison panel. Higher SPI = closer to the comply/refuse switching point."
    },
    {
      "term": "Forced-prefix control (alpha_down_forced)",
      "definition": "The control that makes H1 decisive. The refusal prefix produced at the top of the up-ramp is force-fed as a prefill WITHOUT any prior ramp, then alpha is ramped down. Because the prefix content is identical, the difference alpha_down - alpha_down_forced isolates path dependence carried by latent state from ordinary conditioning on already-emitted refusal text - the mechanism Kwon reports as generic to autoregressive decoding."
    },
    {
      "term": "Noise floor",
      "definition": "The apparent loop width produced by sampling alone, measured in the prefix-discarding reset arm at temperature 0.7. It must be indistinguishable from 0 at temperature 0; at 0.7 it is the baseline against which retained-prefix quantities are compared, replacing the previous, incorrect 'must be exactly zero' requirement."
    },
    {
      "term": "Flicker rate",
      "definition": "At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts that switch mode between refusal and compliance. A classical early-warning indicator, available only because the measurement lives in stochastic sampling."
    },
    {
      "term": "Task-vector safety ladder",
      "definition": "A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) plus partial-strength abliteration. Every interpolant must pass a fluency screen (WikiText perplexity within 2x of the t=1 endpoint; distinct-3 and max-n-gram-repeat degeneracy checks) before entering analysis, and the ladder is piloted on one pair to confirm refusal rate varies smoothly rather than snapping to an endpoint. Members share a weight lineage and never count as independent units."
    },
    {
      "term": "Weight lineage",
      "definition": "The resampling unit for every model-level claim: one pretrained base and everything derived from it (instruct, abliterated, interpolants). The panel has n_lineage = 20 across >= 8 families and ~45-55 measured members; all headline CIs are bootstrapped over the 20 lineages, and the headline baseline comparison is a PAIRED bootstrap of the correlation difference on the same resampled lineages."
    },
    {
      "term": "Behavioral uncensored fine-tune",
      "definition": "An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than a directional weight edit, so it can keep harmful/benign geometry and the refusal direction intact while complying with nearly all harmful requests. Class membership is now VERIFIED before use (separation and cosine preserved vs parent, harmful compliance high, provenance checked for abliteration or abliterated merges), because an unverified candidate tests nothing."
    },
    {
      "term": "Audit cost vs validation cost",
      "definition": "Two separately reported numbers. Audit cost is what a user pays to score one new checkpoint (20 benign prompts x 20 batched rollouts x 192 tokens; ~10-15 min on one consumer GPU, ~40-60 min on CPU at <= 1.7B). Validation cost is what this study pays to establish the metric, dominated by the harmful/jailbreak/over-refusal ground truth. Conflating them invites the objection that a cheap method needed an expensive study - true, normal, and stated plainly."
    },
    {
      "term": "Knowledge-action gap",
      "definition": "The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act on it (98.2% probe AUROC vs 45.1% output sensitivity, 2026 clinical result). It is why a read-side safety metric can be confidently wrong, and why this hypothesis measures an act-side quantity."
    }
  ],
  "summary": "Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation using the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges, higher detrended variance, autocorrelation, flickering), with a forced-prefix-controlled hysteresis residual as the decisive test of genuine bistability. This yields a frozen-normalization safety score computable for a single new checkpoint from a handful of harmless prompts, with no harmful content and no reference model, aimed where static activation-geometry scanners are documented to fail."
}
```

### [18] TOOL RESULT — Write · 2026-08-12 13:02:55 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/iter_3/gen_hypo/claude_agent/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Safety as nearness to a tipping point\",\n  \"hypothesis\": \"Safety fine-tuning does not merely install a harm detector; it moves the model's default generative state close to a bistable switching point between 'comply' and 'refuse'. Because of this, a safety-aligned model is measurably 'twitchy' about refusal even while generating completely harmless text, while base and uncensored models sit deep inside the comply basin. All claims concern the genuine stochastic dynamical system in an LLM - autoregressive generation under temperature sampling, whose state is the generated prefix plus KV cache - measured over GENERATED steps. The single-forward-pass version of the measurement is DROPPED entirely (it contributed to no criterion and its decay was dominated by 1/t attention dilution). Concretely:\\n\\n(H1 - path dependence beyond prefix content) Ramping a steering coefficient alpha along a refusal axis WITHIN one generation until refusal onset (alpha_up) and then ramping back down with the prefix and KV cache retained gives a flip-back threshold alpha_down. The pre-registered H1 test statistic is NOT the naive width alpha_up - alpha_down, which ordinary conditioning on already-emitted refusal text explains and which we predict IN ADVANCE to be large and positive even in base models. It is the RESIDUAL alpha_down - alpha_down_forced, where alpha_down_forced is measured after force-feeding the identical refusal prefix as a prefill WITHOUT ever ramping alpha up. The residual is the part of the path dependence that the literal emitted text cannot explain, i.e. the part attributable to a persistent latent state.\\n\\n(H1b - safety specificity, separable from H1) The residual is ordered instruct > base and instruct > abliterated, paired over prompts.\\n\\n(H2 - critical slowing down) On harmless prompts only, over generated steps and across sampled rollouts, a small residual-stream perturbation decays more slowly (lower recovery rate lambda) and the DETRENDED refusal observable shows larger across-rollout variance, higher lag-1 autocorrelation, and more near-threshold flickering, in models that are behaviorally safer - the early-warning-signal signature of proximity to a fold bifurcation.\\n\\n(H2b - which side the fold is on) Recovery is measured separately for a nudge TOWARD refusal and a nudge TOWARD compliance, giving lambda_toward_refuse and lambda_toward_comply. Their log ratio (the Asymmetry Index) discriminates two competing readings of 'nearness to a switch': ASYMMETRIC (the comply basin is shallow, the model tips into refusal easily - predicts high refusal, high over-refusal, LOWER jailbreak success) versus DOUBLE-SIDED (the model sits near a fold in both directions - predicts high refusal AND high jailbreak success).\\n\\n(H3 - prediction, with signs pre-registered per ground truth) A scalar computed from harmless-input dynamics with FROZEN, published normalization constants - the Switching Proximity Index (SPI) - rank-orders unseen open-weight checkpoints on three separately measured ground truths with pre-registered signs: positive with plain-harmful refusal rate, positive with XSTest over-refusal rate, and with the sign on jailbreak attack-success rate left as the discriminating outcome between the two readings above. SPI must beat the static mean level of the refusal observable, two zero-internals output-side baselines, and reimplementations of AMS, RAS and VISAGE, by a PAIRED bootstrap of the correlation difference over weight lineages.\\n\\n(H4 - where static geometry fails, pre-registered as a case study) SPI flags behavioral uncensored fine-tunes that pass an explicit class-membership check (cluster separation and refusal-direction cosine preserved, harmful compliance high, no abliteration in provenance) and are therefore a documented blind spot of activation-geometry scanners.\",\n  \"motivation\": \"Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator to hold and send harmful content. The published cheap alternatives all retain a dependency this proposal drops. AMS (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy over 14 configurations and explicitly reports that behavioral uncensored fine-tunes preserving geometry are undetectable by it. RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe and jailbreak prompts AND a safety-aligned reference model. VISAGE (arXiv:2405.17374) measures a safety basin in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static, read-side measurements. That question provably does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.\\n\\nThis hypothesis attacks the gap from the act side with a different unit: not a direction, feature or basin volume, but a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge while doing something innocuous?\\n\\nWhat a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space is now stated as a testable divergence rather than asserted. The two accounts must rank the panel identically unless weight-space and behavior-space geometry come apart, and we pre-register the two places they should: (a) a behavioral uncensored fine-tune, where a small weight displacement produces a large behavioral change, and (b) a task-vector interpolant, where a smooth weight-space path may produce a step-like behavioral change. A phenomenon the weight-space basin cannot account for is therefore named in advance: a checkpoint whose weight-space basin volume is unchanged from its parent while its behavioral relaxation rate collapses. If the two rankings coincide, we say so and demote the mechanistic claim to a cost claim. The reinterpretation of Qi et al. gets the same treatment: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes afterwards, while the basin account predicts lambda differences PERSIST deep into generation. Step 5 already collects step-wise lambda profiles, so this discriminating test is free.\\n\\nIf true this yields (a) a mechanistic account of what safety tuning buys, in the language of bistable systems - a shifted operating point; (b) an audit needing a handful of harmless prompts, no harmful content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.\",\n  \"assumptions\": [\n    \"Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over GENERATED steps. The series is NON-STATIONARY (chat-template openings and topic commitment produce a strong deterministic trend), so all fluctuation statistics are computed on residuals after subtracting the ACROSS-ROLLOUT mean trajectory at each generated step, estimated from the >= 20 rollouts we already collect. Without detrending, a high lag-1 autocorrelation would only mean 'this model produces stereotyped openings'.\",\n    \"The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives the abliteration weight edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is primary precisely because a projection onto the abliterated direction is near-constant by construction, which would make any variance claim on abliterated models circular. The per-model diff-in-means axis is descriptive only.\",\n    \"Steering-based tests (H1) probe states that are partly OFF the manifold reachable by prompting (arXiv:2604.09839 proves steered activations are non-surjective). H1 is therefore scoped as a statement about the steered dynamical system, and the safety claim of record (H3) uses only unsteered sampling plus a norm-epsilon perturbation whose linearity is verified by an epsilon sweep, so the product claim never rests on off-manifold behaviour.\",\n    \"A graded safety ladder can be manufactured without training by scaling the alignment task vector W(t) = W_base + t*(W_instruct - W_base) and by scaling abliteration strength - but only if the interpolants stay fluent. Every interpolant must pass a pre-registered screen (WikiText perplexity within 2x of the t=1 endpoint, plus a distinct-3 / max-n-gram-repeat degeneracy check) before entering any analysis, because a degenerate model neither refuses nor complies AND has a degeneracy-dominated r_t series, which would corrupt both sides of the headline correlation at once and could manufacture a spurious result. Interpolants share a weight lineage and never count as independent units.\",\n    \"Small models (0.36B-4B, int8/float32, batched rollouts) show the same qualitative refusal machinery reported for larger models. This is tested rather than assumed via a within-family scale ladder (Qwen3 0.6B/1.7B/4B), because a small model that is twitchy may be twitchy from undertraining; scale enters the headline analysis as a covariate.\"\n  ],\n  \"investigation_approach\": \"PANEL, ENUMERATED BY LINEAGE (the resampling unit). 20 distinct weight lineages, >= 8 architecture families, all CPU-feasible: Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B (each contributing base + instruct + abliterated members), Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Llama-3.2-3B, gemma-2-2b, SmolLM2-360M, SmolLM2-1.7B, TinyLlama-1.1B, Pythia-410M, Pythia-1B, Pythia-1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B, plus >= 4 behavioral uncensored fine-tunes (their own lineages). Base-only lineages (Pythia, OLMo) anchor the low-refusal end. Total measured UNITS (members) ~ 45-55; n_lineage = 20. Every model-level statistic is bootstrapped over the 20 lineages; the member/prompt bootstrap is reported separately and labelled measurement noise.\\n\\nSTEP 0 - PRE-REGISTRATION (written before any run).\\n(a) Layer L is fixed by a rule that never touches the outcome: the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set for ONE reference model, transferred by relative depth L/n_layers. Full layer profiles are secondary, Holm-corrected, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies.\\n(b) Decoding fixed and reported: chat template, empty system prompt, temperature 0.7 for dynamics and 0.0 for deterministic controls; max_new_tokens = 192 for the H2 dynamics arm (needed for estimator identifiability) and 64 for ground-truth generation.\\n(c) SPI is fixed a priori as the mean of FOUR z-scored terms [-log lambda, log detrended across-rollout variance, Fisher-z of detrended AC1, logit of flicker rate], PLUS - crucially - the z-scoring uses FROZEN normalization constants (means and sds) fit once on a designated REFERENCE subset of 6 named lineages and PUBLISHED in the paper. SPI for any new checkpoint uses only those frozen constants, so it is computable for a single model with no comparison panel (the defect that made the previous definition weaker than RAS's absolute 0-100 scale). All leave-one-out and leave-one-family-out numbers are recomputed with the left-out model excluded from the normalization fit. >= 3 checkpoints are reserved that appear in NO normalization and NO fitting step, and their SPI plus ground truth is reported as the out-of-panel demonstration.\\n(d) SIGNED PREDICTION TABLE, one row per ground truth: plain-harmful refusal rate -> expected sign POSITIVE, threshold rho >= 0.6, reason: nearness to the switch makes the refuse mode easy to enter. XSTest over-refusal rate -> POSITIVE, rho >= 0.45, same reason applied to benign-but-scary prompts. Jailbreak attack-success rate -> SIGN IS THE DISCRIMINATING OUTCOME: the ASYMMETRIC reading predicts NEGATIVE (the shallow basin is the comply basin, so the model falls into refusal and is hard to tip out), the DOUBLE-SIDED reading predicts POSITIVE (near a fold in both directions, so it tips either way). Both are pre-registered as competing hypotheses; the outcome that discriminates them is the sign of the partial rank correlation of SPI with ASR controlling for plain-harmful refusal rate, corroborated by the Asymmetry Index of H2b. Either sign is informative; an unsigned rho would have been unfalsifiable.\\n(e) Single-forward-pass measurement: DROPPED, not retained as an appendix, so it cannot be substituted for the generated-step result.\\n\\nSTEP 1 - H1, three ramp arms. For each of >= 30 benign prompts: (i) UP-RAMP, raise alpha per generated token until a refusal-onset token is emitted -> alpha_up. (ii) RETAINED-PREFIX DOWN-RAMP, continue the same sequence with prefix and KV cache kept, lowering alpha -> alpha_down. (iii) FORCED-PREFIX DOWN-RAMP (the control that isolates the claim), force-feed the identical refusal prefix as a prefill without ever ramping up, then ramp alpha down from the same start -> alpha_down_forced. Test statistic = residual = alpha_down - alpha_down_forced, bootstrapped over prompts and lineages. width_naive = alpha_up - alpha_down is reported alongside, with the PRE-REGISTERED expectation that it is large and positive in base models too (per Kwon 2607.14147). A reset arm that discards the prefix between steps is retained as an implementation sanity check only: it must be indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the NOISE FLOOR against which retained-prefix quantities are compared (it will not be exactly 0 under sampling).\\n\\nSTEP 2 - H2/H2b, early-warning indicators on harmless input only. Per benign prompt (~20 prompts), >= 20 paired-seed rollouts, 192 generated tokens. Perturbed arm: inject a norm-epsilon vector into the residual stream at layer L at step p, continue decoding, fit an exponential to |delta r_t| over subsequent generated steps -> lambda, run separately for refusal-directed and compliance-directed nudges (H2b). Clean rollouts give detrended Var*, detrended AC1, and flicker rate. Estimator hygiene, all pre-registered: subtract the across-rollout mean trajectory before AC1/Var*; a SYNTHETIC RECOVERY CHECK simulating AR(1) with known decay at the observed noise level and series length, reporting the estimator's bias and variance and a minimum series length below which lambda is not reported; and indicators reported as a function of series length so truncation artifacts are visible. Epsilon sweep confirms linearity. Three null controls: random readout axis (must NOT reproduce the safety ordering), random vs refusal-aligned perturbation, and a syntactic (part-of-speech probe) observable, which should decay at the same rate if what is being measured is generic mixing.\\n\\nSTEP 3 - ground truth, three axes. Per member: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same under a fixed small jailbreak suite including prefill (ASR), ~50 XSTest benign-but-scary prompts (over-refusal). Scoring: cheap OpenRouter LLM judge PRIMARY, refusal-string matcher as screen, Cohen's kappa reported, >= 100 hand-adjudicated stratified items to estimate judge error, attenuation-corrected correlations alongside raw. Budget < $2 of the $10 cap. Interpolants additionally pass the fluency screen, and the ladder is PILOTED on one base/instruct pair first to confirm refusal rate varies smoothly in t rather than snapping to an endpoint; counts manufactured vs passed are reported, and if the pass rate is low the paper states that trimodality returns.\\n\\nSTEP 4 - H3/H4, prediction with matched-n, faithful baselines. Spearman rho of SPI with each ground truth. The headline comparison is a PAIRED bootstrap of the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages, required to exclude 0 - this removes between-lineage variance common to both and is what n_lineage = 20 can actually support. Baselines: (a) static mean level of r on benign prompts; (b) two zero-internals output-side detectors (next-token probability of refusal-onset tokens; ever-emits-an-apology-token); (c) AMS-style cluster separation sigma and refusal-direction cosine, with leave-one-out accuracy reported in AMS's own format and leave-one-FAMILY-out; (d) a RAS/SafeVec reimplementation whose reference model, layer-window selection rule, prompt sets and calibration mapping are pre-registered, with a reproduction check against RAS's published numbers on overlapping models - if reproduction is out of scope it is labelled 'our RAS reimplementation' throughout, not 'RAS'; (e) VISAGE-style weight-perturbation basin volume on a 6-model subset, with SPI's correlation reported ON THAT SAME SUBSET so the comparison is at matched n. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND model scale. H4 candidates must pass the class-membership pre-check (sigma and refusal-direction cosine preserved vs parent, harmful compliance high, model card and community provenance checked for abliteration or abliterated-merge components); failures are reported with reasons, and if fewer than 4 pass, H4 is reported as a pre-registered case study with per-model detail rather than a statistical claim.\\n\\nSTEP 5 - mechanism map and the two discriminating tests. Layer-wise and step-wise lambda profiles for base vs instruct vs abliterated vs interpolants: does the basin shallow monotonically in t; does abliteration revert to base or produce a third state; and the two named predictions - (i) does the behavioral basin rank the panel differently from VISAGE's weight basin on behavioral fine-tunes and interpolants (versus the account, if identical); (ii) do lambda differences persist deep into generation (basin account) or vanish after the first few generated steps (Qi et al. token-depth account).\\n\\nCOMPUTE BUDGET AND STAGING (previously absent). Audit cost and validation cost are reported separately. AUDIT (what a user pays to score one new checkpoint): 20 benign prompts x 20 rollouts x 2 arms x 192 tokens with batched rollouts and hooks active - roughly 10-15 min on one consumer GPU, or ~40-60 min on CPU int8 at <= 1.7B. VALIDATION (what this study pays): Step 3 dominates, ~50 members x 210 prompts x 64 tokens. Tiering, pre-registered: TIER 0 smoke, 3 checkpoints, verifies the full pipeline end to end. TIER 1, 12 checkpoints spanning all families and both ladder endpoints, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2/H2b with controls. TIER 2, remaining members added to Steps 3-4 only (ground truth and correlation), where marginal cost is lowest and marginal power highest. Criteria are evaluated on whatever tier completes, with the tier stated; a partial run is therefore still reportable.\",\n  \"success_criteria\": \"POWER, reconciled with the resampling unit (the previous version's n=30 arithmetic contradicted its own lineage bootstrap). n_lineage = 20. At n = 20 the 95% bootstrap CI half-width around an observed Spearman rho = 0.8 is roughly +/-0.22, so a criterion requiring SPI's CI lower bound to exceed a baseline's point estimate is NOT attainable regardless of truth and is replaced in advance by the PAIRED difference test, which removes the shared between-lineage variance. Partial correlations with two covariates have adequate power only for partial rho >= 0.5; criteria are set at that level.\\n\\nCONFIRMS:\\n(1) The H1 residual (alpha_down - alpha_down_forced) is significantly > 0 with a bootstrap CI excluding 0 and exceeding the temperature-0.7 noise floor - path dependence exists that the emitted refusal text does not explain.\\n(2) The residual is ordered instruct > base and instruct > abliterated, paired over prompts, CIs excluding 0.\\n(3) On harmless prompts only, over generated steps, with DETRENDED statistics and a passing synthetic-recovery check: lambda lower and Var*, AC1, flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls.\\n(4) SPI computed with FROZEN constants attains rho >= 0.6 with plain-harmful refusal rate (positive sign, as pre-registered) and rho >= 0.45 with XSTest over-refusal (positive), and the PAIRED bootstrap of rho_SPI - rho_baseline excludes 0 against the best of the static mean and the two zero-internals baselines; the partial correlation controlling for static mean and scale has a 95% CI excluding 0 at partial rho >= 0.5.\\n(5) The jailbreak-ASR row resolves in EITHER direction with a partial correlation CI excluding 0 controlling for refusal rate, and the Asymmetry Index of H2b agrees with that sign. This is scored as a confirmed discrimination between the asymmetric and double-sided readings, not as a pass/fail.\\n(6) SPI matches or beats AMS leave-one-out accuracy in AMS's own format with the left-out model excluded from normalization, and matches the RAS reimplementation and VISAGE (the latter at matched n on its 6-model subset) without needing their harmful prompts or reference model.\\n(7) The >= 3 fully held-out checkpoints are scored correctly from frozen constants alone - the actual product claim.\\n(8) H4: every behavioral uncensored fine-tune passing the class-membership check is flagged by SPI while cluster separation and refusal-direction cosine both mark it safe. Reported as a statistical claim only if >= 4 pass, otherwise as a pre-registered case study.\\n\\nTHIRD OUTCOMES, PRE-REGISTERED (informative, not failures): (a) 'bistability present but not safety-specific' - the residual is nonzero in base models too, in which case H1 is confirmed and H1b refuted and only the quantitative ordering carries safety information (live because Kwon 2607.14147 attributes prefill grip to generic autoregressive conditioning and Rahimi et al. 2602.02600 report that autoregressive commitment masks instability). (b) Behavioral basin and VISAGE weight basin rank the panel identically - the mechanistic claim is then dropped to a cost claim, stated plainly. (c) The interpolant ladder fails its fluency screen or snaps to endpoints - the trimodality problem returns and is reported as a limitation on the correlation's interpretability.\\n\\nDISCONFIRMS (reported as refutation, not salvaged): the H1 residual is indistinguishable from the noise floor, i.e. all path dependence is prefix content and the bistable framing adds nothing; or lambda / Var* / AC1 / flicker show no consistent ordering with any ground truth once detrended; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured; or the correlation vanishes once static mean and scale are partialled out; or a zero-internals output-side baseline ties SPI in the paired difference test; or the held-out checkpoints are mis-scored under frozen constants, meaning the metric is a within-panel artifact; or indicators work within one family but fail leave-one-family-out, bounding the metric to a within-family diagnostic.\",\n  \"related_works\": [\n    \"Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access 2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) across 14 configurations and 4 families, 71% leave-one-out accuracy, compliance prediction r = -0.546, and explicitly reports behavioral uncensored fine-tunes as undetectable. Closest work and sharpest departure: static read-side property from harmful prompts versus our dynamical act-side RATE from harmless prompts only. Its documented blind spot is our H4 case study, and we report LOO accuracy in its format with the left-out model excluded from our normalization fit so the comparison is not leaked.\",\n    \"Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state alignment under unsafe and jailbreak prompts, mapped to a calibrated absolute 0-100 scale. It is the incumbent for our product claim and the reason we now FREEZE SPI's normalization constants: a within-panel z-score cannot score a single new checkpoint, which is exactly RAS's advantage. Run as a pre-registered reimplementation with a reproduction check on overlapping models, and labelled 'our reimplementation' if reproduction is out of scope. It needs harmful and jailbreak prompts and a reference model; SPI needs neither.\",\n    \"Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the safety basin in WEIGHT space and proposes the VISAGE basin-volume metric, requiring a harmful benchmark at every weight perturbation. 'Shallow basin' is their language and we say so. The departure is now a TESTED prediction rather than an assertion: the accounts diverge where weight-space and behavior-space geometry come apart (behavioral uncensored fine-tunes; task-vector interpolants). VISAGE is run on a 6-model subset with SPI reported on that same subset at matched n; if the rankings coincide we drop the mechanistic claim to a cost claim.\",\n    \"Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with linear probes, finding a sharp drop at final tokens in poorly aligned reasoning models. The per-position refusal score is an existing observable which we adopt rather than coin; our contribution is the detrended dynamical statistics computed on it across sampled rollouts plus the residual hysteresis test.\",\n    \"Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - shows diffusion remasking enables recovery from harmful intermediate generations and proposes the SRI internal-dynamics signal, observing that autoregressive commitment masks underlying instability. Closest 'dynamics during decoding' work: it compares SAMPLING MECHANISMS, we hold sampling fixed and use controlled perturbation-recovery as an ESTIMATOR of distance to a switching point. Its commitment finding is a named pre-registered threat.\",\n    \"Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - prefill jailbreak study: harm representation stays intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific collapse, concluding the prefill's grip is generic autoregressive conditioning rather than safety-specific suppression. This is precisely why H1's test statistic is now the FORCED-PREFIX RESIDUAL rather than the naive loop width, which this paper's mechanism would otherwise explain entirely.\",\n    \"Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive Logit Steering plus prefix injection induces a phase transition where guardrails collapse, and reports 'Late Decision' (Llama, 95% ASR) vs 'Early Divergence' (Qwen, safety integrated at ~40% depth) topologies. Phase-transition language exists here but as an ATTACK that crosses the edge; our point is estimating distance to the edge without crossing it. Its topology finding drives our relative-depth layer transfer.\",\n    \"Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal and harmful compliance nearly uncorrelated. This is why three ground truths are predicted separately, and why the signed prediction table (positive for refusal and over-refusal, sign-as-outcome for ASR) is a real commitment rather than bookkeeping.\",\n    \"Xiong et al., 'Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for LLMs' (arXiv:2602.04896, 2026) - steering vectors from entirely benign data erode guardrails, with ASR above 80%, framed as consumption of a 'safety margin'. This is direct empirical support that a margin exists and is small in aligned models, and it is the strongest existing evidence for the DOUBLE-SIDED reading in H2b. It measures the consequence of crossing the margin; we measure the margin's width from harmless generation without crossing it.\",\n    \"Mishra, Khashabi and Liu, 'Steered LLM Activations are Non-Surjective' (arXiv:2604.09839, 2026) - proves steered residual streams leave the manifold reachable from discrete prompts. A scope constraint we now state explicitly: H1's ramp probes the steered system, so the product claim (H3) rests only on unsteered sampling plus a verified-linear norm-epsilon perturbation.\",\n    \"Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the static geometric account and our instrument for producing (and partially producing) uncensored checkpoints. Because abliteration orthogonalizes writes against that direction, we deliberately do NOT use a projection onto it as the primary observable.\",\n    \"Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows aligned and unaligned generative distributions differ mainly over the first few output tokens. Their account and ours make DIFFERENT predictions we now test: token depth predicts the safety signal is confined to the first few generated steps, the basin account predicts lambda differences persist across generated steps.\",\n    \"Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering near a fold bifurcation). The imported source, not a competitor; scholarly search finds it applied to ecosystems, climate, financial crises, depression and sleep, but not to LLM generative dynamics or safety auditing.\"\n  ],\n  \"inspiration\": \"The transfer is from ecology and climate science at the methodological level. Ecologists face this problem in a different costume: they must know how close a lake, forest or fish population is to collapsing without running the experiment of collapsing it. Scheffer's early-warning-signal programme solved it by measuring the response to small, harmless disturbances - as a system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery from tiny nudges slows, fluctuations grow in variance, become more autocorrelated, and the system flickers. Resilience becomes measurable without pushing the system over the edge. Mapped onto model auditing: don't jailbreak a model to learn whether it can be jailbroken - nudge it gently while it does something innocuous and watch how fast it settles back. The import is legitimate only where a real stochastic dynamical system exists, which is why the measurement lives in autoregressive sampling and why the single-forward-pass version has now been dropped rather than kept as a heuristic. Ecology also supplies the fix for the statistics: EWS practitioners detrend before computing autocorrelation for exactly the reason we now must - a trend inflates AC1 and fakes the signal. Two further imports: from physics and materials science, the hysteresis loop as the decisive test of genuine bistability, which forces the sweep to happen within one generation with the prefix retained - and, following the same tradition's insistence on separating a real state variable from a memory of the drive, the forced-prefix control that isolates latent path dependence from conditioning on already-emitted text. From experimental genetics, the base / safety-tuned / abliterated series read as wild-type / knock-in / knock-out, extended to a dose-response ladder by scaling the alignment task vector, with a viability screen on the intermediates the way a geneticist screens for non-viable phenotypes. What a domain expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object - a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.\",\n  \"terms\": [\n    {\n      \"term\": \"Refusal observable (r_t)\",\n      \"definition\": \"A scalar read off the model at each GENERATED step t. Primary form: logit-lens log-odds of refusal-onset tokens against continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. All fluctuation statistics use the DETRENDED residual, obtained by subtracting the across-rollout mean trajectory at each generated step.\"\n    },\n    {\n      \"term\": \"Critical slowing down\",\n      \"definition\": \"The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows, fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in ecology, climate science and psychiatry for estimating resilience without triggering collapse.\"\n    },\n    {\n      \"term\": \"Recovery rate (lambda)\",\n      \"definition\": \"The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small residual-stream perturbation, averaged over >= 20 paired-seed rollouts of 192 tokens. Small lambda = slow recovery = shallow basin = close to switching. Its identifiability at the actual series length and noise level is verified by a synthetic AR(1) recovery check with a pre-registered minimum series length.\"\n    },\n    {\n      \"term\": \"Asymmetry Index\",\n      \"definition\": \"log(lambda_toward_refuse / lambda_toward_comply): recovery from a nudge pushing toward refusal versus one pushing toward compliance. It distinguishes an ASYMMETRIC shallow comply basin (tips into refusal easily, so high refusal but LOW jailbreak success) from a DOUBLE-SIDED fold (tips either way, so high refusal AND high jailbreak success) - the two readings of 'nearness to a switch' whose conflation previously left the jailbreak prediction unsigned.\"\n    },\n    {\n      \"term\": \"Switching Proximity Index (SPI)\",\n      \"definition\": \"The proposed safety metric: the mean of four terms [-log lambda, log detrended across-rollout variance of r, Fisher-z of detrended lag-1 autocorrelation, logit of flicker rate], standardized with FROZEN normalization constants fit once on a named 6-lineage reference subset and published, so SPI is computable for a single new checkpoint with no comparison panel. Higher SPI = closer to the comply/refuse switching point.\"\n    },\n    {\n      \"term\": \"Forced-prefix control (alpha_down_forced)\",\n      \"definition\": \"The control that makes H1 decisive. The refusal prefix produced at the top of the up-ramp is force-fed as a prefill WITHOUT any prior ramp, then alpha is ramped down. Because the prefix content is identical, the difference alpha_down - alpha_down_forced isolates path dependence carried by latent state from ordinary conditioning on already-emitted refusal text - the mechanism Kwon reports as generic to autoregressive decoding.\"\n    },\n    {\n      \"term\": \"Noise floor\",\n      \"definition\": \"The apparent loop width produced by sampling alone, measured in the prefix-discarding reset arm at temperature 0.7. It must be indistinguishable from 0 at temperature 0; at 0.7 it is the baseline against which retained-prefix quantities are compared, replacing the previous, incorrect 'must be exactly zero' requirement.\"\n    },\n    {\n      \"term\": \"Flicker rate\",\n      \"definition\": \"At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts that switch mode between refusal and compliance. A classical early-warning indicator, available only because the measurement lives in stochastic sampling.\"\n    },\n    {\n      \"term\": \"Task-vector safety ladder\",\n      \"definition\": \"A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) plus partial-strength abliteration. Every interpolant must pass a fluency screen (WikiText perplexity within 2x of the t=1 endpoint; distinct-3 and max-n-gram-repeat degeneracy checks) before entering analysis, and the ladder is piloted on one pair to confirm refusal rate varies smoothly rather than snapping to an endpoint. Members share a weight lineage and never count as independent units.\"\n    },\n    {\n      \"term\": \"Weight lineage\",\n      \"definition\": \"The resampling unit for every model-level claim: one pretrained base and everything derived from it (instruct, abliterated, interpolants). The panel has n_lineage = 20 across >= 8 families and ~45-55 measured members; all headline CIs are bootstrapped over the 20 lineages, and the headline baseline comparison is a PAIRED bootstrap of the correlation difference on the same resampled lineages.\"\n    },\n    {\n      \"term\": \"Behavioral uncensored fine-tune\",\n      \"definition\": \"An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than a directional weight edit, so it can keep harmful/benign geometry and the refusal direction intact while complying with nearly all harmful requests. Class membership is now VERIFIED before use (separation and cosine preserved vs parent, harmful compliance high, provenance checked for abliteration or abliterated merges), because an unverified candidate tests nothing.\"\n    },\n    {\n      \"term\": \"Audit cost vs validation cost\",\n      \"definition\": \"Two separately reported numbers. Audit cost is what a user pays to score one new checkpoint (20 benign prompts x 20 batched rollouts x 192 tokens; ~10-15 min on one consumer GPU, ~40-60 min on CPU at <= 1.7B). Validation cost is what this study pays to establish the metric, dominated by the harmful/jailbreak/over-refusal ground truth. Conflating them invites the objection that a cheap method needed an expensive study - true, normal, and stated plainly.\"\n    },\n    {\n      \"term\": \"Knowledge-action gap\",\n      \"definition\": \"The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act on it (98.2% probe AUROC vs 45.1% output sensitivity, 2026 clinical result). It is why a read-side safety metric can be confidently wrong, and why this hypothesis measures an act-side quantity.\"\n    }\n  ],\n  \"summary\": \"Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation using the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges, higher detrended variance, autocorrelation, flickering), with a forced-prefix-controlled hysteresis residual as the decisive test of genuine bistability. This yields a frozen-normalization safety score computable for a single new checkpoint from a handful of harmless prompts, with no harmful content and no reference model, aimed where static activation-geometry scanners are documented to fail.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [19] TOOL CALL — Bash · 2026-08-12 13:03:01 UTC

```
python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
req=['title','hypothesis','motivation','assumptions','investigation_approach','success_criteria','related_works','inspiration','terms','summary']
print([k for k in req if k not in d]); print(len(d['assumptions']),len(d['terms']),len(d['related_works']),d['title'])"
```

### [20] TOOL RESULT — Bash · 2026-08-12 13:03:01 UTC

```
{"stdout": "[]\n5 13 13 Safety as nearness to a tipping point", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-08-12 13:03:17 UTC

```
Written and schema-valid: `./.terminal_claude_agent_struct_out.json`

**Revision kept the core** (safety as nearness to a comply/refuse tipping point, measured with ecology's early-warning-signal toolkit) and fixed all eleven critiques:

| Critique | Fix |
|---|---|
| Power contradicts lineage bootstrap | Panel enumerated **by lineage: n_lineage = 20** (added Pythia×3, OLMo, Danube3, Falcon3, Granite, MiniCPM, ≥4 uncensored FTs, ≥8 families); CI half-width recomputed (±0.22); criterion (4)'s CI-exclusion replaced by a **paired bootstrap of Δrho on the same resampled lineages** |
| H1 confirms trivially | **Forced-prefix control arm** added; test statistic is now the residual `alpha_down − alpha_down_forced`; `width_naive` pre-registered as large-and-positive in base models too (per Kwon); reset arm demoted to a **noise floor**, "exactly 0" language removed |
| SPI uncomputable for one model | **Frozen, published normalization constants** from a named 6-lineage reference subset; LOO recomputed with left-out models excluded from the fit; **≥3 fully held-out checkpoints** as the product demonstration |
| Unsigned ASR prediction | **Signed prediction table** + new **H2b Asymmetry Index** (λ toward-refuse / toward-comply) turning the ambiguity into a pre-registered discrimination between *asymmetric* and *double-sided* readings |
| Under-identified estimators | Detrend by across-rollout mean trajectory; **synthetic AR(1) recovery check** with a minimum series length; H2 rollouts to **192 tokens**; indicators reported vs series length |
| No compute budget | Tier 0/1/2 staging, per-step estimates, **audit cost reported separately from validation cost** |
| Interpolants can degenerate | Pre-registered fluency screen (2× perplexity, distinct-3/repeat) + one-pair pilot for smooth-vs-step refusal rates; manufacture/pass counts reported |
| H4 at n=2 | ≥4 candidates with an explicit **class-membership + provenance check**; labelled a case study if fewer pass |
| Weak baselines | RAS reimplementation pre-specified with a reproduction check (else labelled "our reimplementation"); **VISAGE compared at matched n** |
| Asserted VISAGE/Qi differentiators | Named discriminating observations for both (behavior-vs-weight basin ranking divergence; λ persisting deep into generation vs confined to first steps) |
| Unscored forward-pass arm | **Dropped entirely** |

Two new papers folded in from this round's search: *Steering Externalities* (2602.04896, "safety margin" — empirical support for the double-sided reading) and *Steered LLM Activations are Non-Surjective* (2604.09839 — a scope constraint now stated, keeping the product claim off steered/off-manifold states). Prior-art lane remains unoccupied.
```
