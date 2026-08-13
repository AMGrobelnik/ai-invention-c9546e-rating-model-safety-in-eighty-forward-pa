# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 5 · `gen_plan`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 03:26:55 UTC

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
title: Cheap safety scores die at panel scale
hypothesis: |-
  The project's object of study is unchanged (autoregressive generation and its activation geometry as an act-side system; goal = a benchmark-free, harmful-prompt-free safety score for arbitrary open-weight checkpoints). Iteration 1 retired the bistable/EWS mechanism. Iteration 2 retired alpha_50 as a safety score. Iteration 3 retired the five-check falsification protocol as a contribution. Iteration 4 retired BOTH of the positives iteration 3 carried forward: the AMS paraphrase refit does not survive at 28 lineages, and the within-axis induce-without-detect dissociation does not survive when each model is scored on its own spontaneous text. What iteration 5 must deliver is (i) the one test the scale panel should have run and did not - the SAME 28-lineage replication applied to the score that actually WON the discrimination matrix (the logit-gap harmful-prompt margin), which converts a fourth negative about one refit into either a usable cheap score or a general claim about the whole class of cheap activation scores; (ii) three targeted repairs to the read-versus-act reversal that the reviewer showed is currently carried by a confounded statistic, an n-asymmetric verdict rule, and a partly definitional label; and (iii) the honest reframing of the surviving 'measurement decisions' as measured instances of named, textbook phenomena rather than as discoveries.

  WHAT IS NOW SETTLED (iteration 4, reported as retraction and correction, not salvage):

  (S1 - THE PARAPHRASE REFIT DOES NOT SURVIVE AT SCALE, AND THE FAILURE IS LOCALISED) [art_CZaytBH8uL4_] At 52 analysed members over 28 lineages and 11 families (up from 19/7), member-level lineage-clustered bootstrap: rho original 0.359 [0.047,0.592], refit SET A 0.458 [0.197,0.646], refit SET B 0.207 [-0.110,0.463]. Delta_A = +0.099 [-0.027,0.244] (was +0.296), P(Delta_A>0)=0.935 -> R1 FAILS. An INDEPENDENTLY AUTHORED paraphrase set (Jaccard 0.201 against SET A, generated by a non-judge model, verified by the FROZEN iteration-3 check_pair(), 80/80 pass) gives Delta_B = -0.152 [-0.488,0.075] -> R3 FAILS. Permutation p = 0.135 against a Monte-Carlo floor of 5e-6 over 200,000 lineage permutations -> R4 FAILS, and the 1/5040 floor the original result sat exactly on is genuinely retired. Only R2 passes. DECISIVE DIAGNOSTIC: the archived 19-member block reproduces Delta_A = +0.2963 (gap 2.6e-4, so reuse is byte-exact) while the 33 NEW members give -0.016 [-0.144,0.130]; per block rho goes 0.358->0.654 archived and 0.402->0.386 new. Leave-one-lineage-out (28 folds, [0.068,0.122]) and leave-one-family-out (11 folds, [0.060,0.137]) never flip the sign, so it is not one outlier. Verdict-class change rate 12/52 = 0.231 [0.137,0.361]: the refit still MOVES AMS's PASS/WARN/CRIT verdicts, it just does not move them toward the truth. This adjudicates the ambiguity iteration 3 left open in favour of 'seven-lineage predictive validity is itself unreliable' - the exact failure mode arXiv:2607.28685 documents (a correlation moving from -0.64 at n=7 to +0.02 at n=18).

  (S2 - THE DISSOCIATION REVERSES; ABLITERATION REMOVES THE REFUSALS, NOT THE READER) [art_1xT3w1joqeJ8] On 30 checkpoints over 7 lineages, each measured in BOTH roles of the same five axes, with detection scored on each model's OWN spontaneous unsteered generations: 20 READS, 1 AMBIGUOUS, 9 UNDEFINED, ZERO AT_CHANCE; the pre-registered K<3 branch fires at K=0 of M=4, so the iteration-3 'at chance in both roles on both abliterated members' claim is RETRACTED. The cause is structural: 14 of 18 abliterated-class members never produced the 40 spontaneous refusals the statistic needs even after the full escalation ladder (1,585 generations each; median spontaneous refusal rate 0.0076 in the weight-edited arm and 0.0000 in the behavioural-uncensored arm). Iteration 3 differed because its item pool contained STEERED and archived text. On the six depth-panel checkpoints the same axis goes from AUROC 0.486-0.790 (archived pool) to 0.906-0.980 (own-text pool) with induction unchanged. Matched contrast returns NORM_MISMATCH_DOES_NOT_EXPLAIN on 22 of 30, retiring arXiv:2603.22061's magnitude-collapse rival on a panel five times the previous size. TWO NULL-DESIGN CORRECTIONS that generalise: a random direction at axis A's matched magnitude induces refusal >= 0.10 on 7 of 30 members (worst 0.389), and the 20-draw random READING band spans +/-0.075 to +/-0.500 across members, so 'chance is 0.500' and 'one random draw is a null' are both wrong.

  (S3 - THE COUPLING STATISTIC IS CONFOUNDED BY AXIS TYPE; REVIEWER MAJOR/evidence, CONCEDED) The headline rho = 0.629 [0.465,0.803] is computed over 70 (member, axis) pairs = 14 members x 5 axes, pooling axis A (strong in both roles by construction) with C and D (null in both roles by construction). That pooled Spearman is dominated by a BETWEEN-AXIS-TYPE contrast, not a read-act relationship, and the lineage bootstrap cannot fix it because the confound is within-member. The reviewer recomputed the within-axis-A, across-member version from this study's own shipped tables (T2 A-AUROC vs T3 A-max-refusal-rate over 13 detection-powered members): rho = 0.434, p = 0.14. The within-member mean of 0.715 is worse, not better - it is the mean of 14 coefficients on 5 points each, over the same contrast. The defensible statement is now: the axis that induces is also the axis that reads, but AMONG MODELS the two qualities are only weakly and non-significantly related. This is still a clean reversal of the dissociation claim; it is not a demonstration of coupling strength.

  (S4 - THE VERDICT RULE IS n-ASYMMETRIC AND THE METHOD MISDESCRIBES IT; REVIEWER MAJOR/rigor, CONCEDED) READS requires only a CI lower bound above 0.60, which perfect separation on a handful of items delivers automatically; AT_CHANCE requires the whole bootstrap CI inside a 0.20-wide band, which is unreachable at n ~ 10. In the shipped per-member table READS is issued at 7, 12, 28, 32 and 33 refusals - all marked NOT detection-powered by the artifact's own 'pow' column - while only members with 0 or 1 refusals return UNDEFINED, which is NOT the '<40 refusals' gate the Method describes. Consequently 'zero AT_CHANCE over 30 checkpoints' is partly a property of the rule, and the weight-edited abliteration arm's 5 READS rest on counts of 12/28/32/33/150 - exactly ONE powered member.

  (S5 - THE DETECTION TASK IS PARTLY DEFINITIONAL; REVIEWER MAJOR/methodology, CONCEDED) Axis A is fitted on hand-written canned refusals versus compliances, and the detection LABEL is an anchored regex matching canned refusal openers. 'The canonical axis reads refusals at AUROC 0.69-1.00' therefore comes close to saying that a direction fitted on canned-refusal wording separates text opening with canned-refusal wording. The A-vs-B comparison controls this only partially. The scepticism iteration 4 applied to the INDUCTION side (S6) was not applied to the READING side, where the same regex became the label.

  (S6 - THE PARAPHRASE AXIS LOSES ON SEMANTICS, NOT ONLY LEXICON, AND THE DEGENERACY STORY INVERTS) [art_P-_YL8tdIwqF] On fluency-screened text at matched axis-contrast units, five-class any-refusal is 0.028 [0.008,0.057] for axis B against 0.747 [0.618,0.858] for axis A, with the random-axis-D false-positive floor at 0.146; NET = B - floor = -0.118 [-0.157,-0.082] -> REVERSAL_DOES_NOT_SURVIVE 6/6 and pooled. Three sub-measurements each cut against something previously written: at matched contrast the lexical screen removes NOTHING (retention 1.000), so B's near-zero rate is absence of effect and not filtering; at B's maximum coefficient retention falls to 0.705 but 70.2% of SCREEN-PASSING text is still judge-DEGENERATE against 71.1% unfiltered, so the lexical screen removes essentially none of the residual degeneracy because the failure is semantic; and 59.0% of the control floor's own survivors are judge-DEGENERATE, which is why a semantic rate without a same-population floor is uninterpretable. NUANCE, pre-registered: at B's OWN peak coefficient (5.21 contrast units, ~4.3x what A needs) B clears the floor on fluent text at 0.642 vs 0.077, NET +0.565 [+0.471,+0.655], DEGENERATE 0.049 -> REVERSAL_SURVIVES 6/6. B's reversal is real but lives entirely at coefficients that matching forbids. Rogan-Gladen truncates at the matched level by construction (both rates below 1-specificity = 0.196) and is flagged rather than quoted.

  (S7 - THE AGGREGATION-UNIT REPAIR IS DONE AND THE PROTOCOL NEGATIVE IS THRESHOLD-ROBUST) [art__tq3ZgPRYB0B] 11/11 reproduction legs pass to 1e-6. Across 16 score x config cells where both units are defined, changing NOTHING but the unit moves oriented rho by a median 0.238 and a maximum 0.557 and FLIPS THE SIGN on 5. The oriented Delta emits SIGN_SURVIVES / EXCLUSION_LOST_AT_MEMBER_LEVEL on one carrier (-0.929 [-1.961,-0.113] lineage vs -0.376 [-0.795,0.110] member) and SIGN_FLIPS / EXCLUDES_AT_NEITHER on the other (-0.566 member vs +0.107 lineage); the plan's -0.465 estimate was NOT reproduced and nothing was tuned toward it. PROTOCOL_DOES_NOT_DISCRIMINATE holds on 1.0000 of a 164,736-point full factorial (0.9091 strict-exceed, 1.0000 checks-1-4); dropping the pass rules' secondary clauses and scoring numeric cutoffs alone gives 0.5802/0.2429, which LOCATES the negative in the verdict-class and interiority clauses rather than the cutoffs; check 5's kappa 0.391 lies below the entire swept range so it can never flip anything. A prose audit found 57 claims: 18 traceable-with-unit, 31 traceable-without-unit, 3 value-mismatch, 5 untraceable. Discovered, not inherited: the outcome variable itself disagrees across the two frozen archives on 3 of 19 members (all UNRELIABLE-excluded, so nothing moves).

  (S8 - POSITIONING: THE MIRROR PAPER IS WEAKER THAN ITS ABSTRACT, AND THE BIBLIOGRAPHY WAS BROKEN) [art_G5SIDXT53EAW] arXiv:2607.13346 is a MIRROR IMAGE but a weaker neighbour: its dissociation is assembled ACROSS TWO MODELS (detection 0.870 Llama, 0.425 Qwen), its probe is a two-layer MLP rather than the steered vector, '|h|<0.08' is COHEN'S h on compliance proportions, no activation norm is reported so its coefficient is NOT convertible to our contrast units, and there is no abliterated arm. One concession is forced: it DOES steer a refusal axis and get a null. The most transferable thing in it is the leakage control that moved its own AUROC from 0.761 to 0.425 - which we have not run. arXiv:2603.27412 (LatentBiopsy) already runs base/instruct/abliterated Qwen triplets and reports abliterated AUROC within 0.015 of instruction-tuned, so any 'first activation score on abliterated checkpoints' claim is withdrawn; what survives is that the REFUSAL axis specifically goes quiet while harm-intent geometry does not. 9 of 21 cited 2026 entries were wrong, worst being a mis-titled [23].

  THE REVISED CLAIMS, in the order they must now be tested:

  (H-G - RUN THE SCALE PANEL ON THE SCORE THAT WON; THE NEW PRIMARY CLAIM, reviewer MAJOR/scope) The scale panel was spent on the losing score. The logit-gap harmful-prompt margin is the ONLY score whose CI excludes zero at BOTH aggregation units (rho 0.667 [0.439,0.904] member, p 0.0038; 0.929 [0.412,1.000] lineage, p 0.0067), and it costs 80 forward passes and ZERO generations per model. The claim to test is: does a first-decoding-step logit-gap margin predict judged plain-harmful refusal rate at n_lineage = 28, or does it collapse the way the paraphrase refit did? Run it - together with the benign variant and our-AMS sigma, both already implemented and free at the same cost - on the SAME 52-member / 28-lineage / 11-family scale panel, with the SAME Monte-Carlo lineage permutation null and BOTH aggregation units, reusing the frozen y_refusal block whose byte-identical regeneration is already proven. PRE-REGISTER BEFORE RUNNING: (a) rho(logit-gap-harmful) >= 0.50 at the member level with a lineage-clustered CI excluding 0; (b) the same at the lineage-aggregated unit; (c) permutation p well off the 5e-6 floor; (d) the archived-19 vs new-33 block split reported as the decisive diagnostic exactly as in S1, since that is what localised the refit's failure; (e) a pre-committed statement of what a partial result means (member-only exclusion = the same unit-dependence S7 documents, not a win). OUTCOMES: (i) HOLDS -> lead the paper with it: 'the cheapest score in the class - 80 forward passes, no harmful generation, no reference model - predicts judged harmful refusal at rho = X across 28 lineages and 11 families', which answers the introduction's motivating question and is the first thing in four iterations a platform could adopt. Note honestly that this score is NOT harmful-prompt-free (it reads the margin on harmful prompts), so the product claim narrows from 'no harmful content' to 'no generation, no judge, no benchmark, no reference model' - a real but smaller saving that must be stated in the abstract rather than buried. (ii) COLLAPSES -> the paper's thesis becomes strictly stronger and general: EVERY cheap activation-derived safety score tested collapses from 7 to 28 lineages, which is a claim about the score class rather than about one refit, and it retires the small-panel literature's implicit licence in this lane. Either outcome is the paper's headline; the current fourth-negative-about-one-refit framing is not.

  (H-C - RE-ESTIMATE THE READ-ACT COUPLING WITHOUT THE AXIS-TYPE CONTRAST; mandatory, reviewer MAJOR/evidence) Make the WITHIN-AXIS-A, ACROSS-MEMBER correlation the primary statistic (n = 13-14 detection-powered members, lineage-clustered bootstrap, BOTH aggregation units, as this paper now requires of itself), and demote the 70-pair pooled rho = 0.629 to an explicitly labelled secondary that mixes between-axis and between-model variance. Report the trivial control - rho with axes C and D dropped - so a reader can see how much of 0.629 is the control contrast. Also fit a partial correlation or mixed-effects model with an axis fixed effect and report the residual member-level coupling. If the within-axis estimate is ~0.43 with a CI covering zero, SAY SO: 'the axis that induces is also the axis that reads, but among models the two qualities are only weakly and non-significantly related' is still a clean reversal of the dissociation and is defensible; the current sentence is not.

  (H-K - REPORT THE VERDICT TALLY TWICE AND FIX THE GATE'S DESCRIPTION; mandatory, reviewer MAJOR/rigor) Report the READS/AMBIGUOUS/AT_CHANCE/UNDEFINED tally (a) as-is and (b) restricted to detection-powered members (>= 40 per class), which is the population the pre-registration says the statistic exists on. State, from a two-line simulation, the minimum n at which AT_CHANCE is ATTAINABLE under the CI rule, and attach it as a footnote to every 'zero AT_CHANCE' sentence. Correct the Method to describe the gate the code actually applies (UNDEFINED fires at 0-1 refusals, not at <40) and log it as a deviation with its trigger, as this project does elsewhere. For the abliterated arm specifically, either extend the escalation ladder on the four underpowered READS members until they clear 40, or restate the arm as resting on ONE powered member plus four underpowered ones with their CIs in the main text. The structural claim ('abliteration removes the refusals to be read, not the ability to read them') is likely to survive - the median spontaneous refusal rate of 0.0076 carries it independently of any AUROC - but it must be carried by the refusal-rate evidence, not by four underpowered AUROCs.

  (H-L - BREAK THE LABEL-AXIS LEXICAL CIRCULARITY; mandatory, reviewer MAJOR/methodology) Re-score the detection LABELS on a stratified subset of the spontaneous generations with the five-class semantic rubric already built for S6 (including the non-canonical-refusal class), and re-report axis A's AUROC against SEMANTIC labels for at least the detection-powered members, with the delta to the regex-labelled AUROC. If it holds, the objection dies in one paragraph and the reading result gets stronger; if it drops, restate the reversal as 'the axis reads CANONICALLY-WORDED refusals'. Either way add one sentence acknowledging that the label and the axis share a lexical basis - the same scepticism S6 applied to induction, applied to detection.

  (H-X - RUN THE ONE PUBLISHED LEAKAGE CONTROL ON OUR OWN HEADLINE; reviewer MINOR/rigor, but load-bearing given the paper's own framing) The paper's thesis is that the item pool decides the result; the single published control that tests exactly this - arXiv:2607.13346's per-fold residualisation with ALL centring/normalisation statistics estimated inside the training fold, under leave-one-prompt-out / leave-one-query-out splits - is the one place our standard is not applied to our own headline, and it moved that author's AUROC by 0.336. The projections are already computed; the change is only in where the normalisation statistics come from. Run it on at least the detection-powered members and report the delta. Small delta = a one-line strengthening; large delta = something we must know before publication.

  (H-N - NAME THE PHENOMENA, THEN CLAIM THE INSTANCE; reviewer MINOR/novelty) The three surviving 'measurement decisions' are quantified instances of textbook phenomena and must be named as such: item-pool provenance deciding a read-vs-act comparison is train/test leakage and distribution shift; the aggregation unit moving rho by a median 0.238 and flipping 5 of 16 signs is aggregation (ecological) bias, a relative of Simpson's paradox, long documented in psychometrics and ecology; the collapse from n_lineage 7 to 28 is small-sample correlation instability, which we already cite arXiv:2607.28685 as warning about. Cite one canonical source each, then claim the instance: 'we do not claim aggregation bias as a finding; we claim a measured instance in which it moves this study's own headline by 0.464 and flips 5 of 16 signs'. Three sentences, and it removes the strongest available novelty objection - the honest framing (a rare public demonstration on the authors' OWN published result, with the effect localised to the original block) is more persuasive than the discovery framing.

  (H-U - AGGREGATION UNIT, DONE AND KEPT) Every correlation names its unit; Table 3 gives both for every score; the oriented Delta is reported at both with its verdict strings. This repair is COMPLETE [art__tq3ZgPRYB0B] and must be extended verbatim to whatever H-G produces. No further work.

  (H-P - THE PROTOCOL, DEMOTED IN PLACE, NOW WITH A THRESHOLD SURFACE) The five checks stay as a limitations instrument and as the machinery that produced the (retracted) refit lead, never as a certification protocol, never claimed novel in kind given arXiv:2607.28685 and arXiv:2605.06161. Its negative is now threshold-robust on 1.0000 of a 164,736-point grid and located in the verdict-class/interiority clauses. No further work.

  (H-A - PRESENTATION AND NUMBER DISCIPLINE; reviewer MINOR/clarity and MINOR/evidence) Add an ABSTRACT stating the surviving measurements and the retractions. Renumber tables by first appearance (Table 5 currently precedes Table 2; Table 1 first appears in section 5.4). Add 'n refusals / n compliances' and 'powered (y/N)' columns to the main-text detection table - the two columns a reader most needs to evaluate the reversal and both already in the artifact's T2. Extend the byte-identical-regeneration discipline from RESULTS.md to the PAPER'S PROSE NUMBERS: the AUROC minimum is quoted as >= 0.68 in the intro, >= 0.685 in section 5.1 and is 0.691 in the table; '20 checkpoints where reading is measurable' conflicts with 20 READS + 1 AMBIGUOUS; the artifact's stale top-line summary still says 18/0/10 against RESULTS.md's 20/1/9. Reconcile the stale summary block, and complete reference [11]'s author list. In a paper whose thesis is measurement discipline, a reader who checks the artifact hits the 18-vs-20 discrepancy first.

  WHAT THIS PROJECT NOW CLAIMS, plainly: a benchmark-free, harmful-prompt-free ACT-SIDE safety score does not follow from steering strength along a refusal axis; the validity battery built to explain that failure cannot rank cheap scores because construct hygiene and predictive validity come apart; and BOTH positives the previous draft carried have been retracted by the experiments their own limitations sections demanded. What survives is (1) reading and steering along one refusal axis are not dissociated - the axis reads the model's own spontaneous refusals wherever refusals exist, zero of 30 members sit at chance, and abliteration removes the refusals rather than the reader - with the strength of the read-act coupling still to be estimated without the axis-type confound (H-C) and the label circularity broken (H-L); (2) the canonical axis's advantage over its token-disjoint paraphrase is SEMANTIC at matched contrast (0.028 against 0.747, below a 0.146 random floor) and reverses only at 4.3x the coefficient matching allows; (3) a random direction is inert in NEITHER role - it induces refusal on 7 of 30 checkpoints at matched magnitude and reads anywhere in a +/-0.075 to +/-0.500 band - so single-draw random controls and a 0.500 chance line are both unsafe; and (4) three named measurement pathologies, each measured on this study's own published numbers. The three controlled negatives (bistable/EWS; steering-price alpha_50; the protocol) stand as contributions in their own right. Whether the class of cheap activation scores contains ANY member that predicts behaviour at 28 lineages is the one open question, and H-G is the experiment that settles it.
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
  Same frame; both iter-3 positives retracted at scale, scale panel repointed at the winning logit-gap score.
_confidence_delta: decreased
_key_changes:
- >-
  PARAPHRASE REFIT RETRACTED (S1) [art_CZaytBH8uL4_]: at 52 members / 28 lineages Delta_A = +0.099 [-0.027,0.244] (was +0.296),
  independently authored SET B gives -0.152, perm p 0.135 vs floor 5e-6; archived-19 block reproduces +0.2963 while new-33
  give -0.016, so the effect is a localised small-panel artifact, not a property of token-disjointness.
- >-
  DISSOCIATION REVERSED (S2) [art_1xT3w1joqeJ8]: 20 READS / 1 AMBIGUOUS / 9 UNDEFINED / ZERO AT_CHANCE over 30 checkpoints
  on each model's own spontaneous text; K=0 of M=4 retracts the n=2 'at chance in both roles'; 14 of 18 abliterated members
  emit <40 refusals (median rate 0.0076), so abliteration removes the refusals, not the reader.
- >-
  NEW PRIMARY CLAIM (H-G), addressing reviewer MAJOR/scope: run the logit-gap harmful-prompt margin (plus benign variant and
  our-AMS sigma, free at the same cost) on the SAME 52-member / 28-lineage scale panel with the Monte-Carlo permutation null
  and both units — it is the only score excluding 0 at both units (0.667 member / 0.929 lineage) and costs 80 forward passes;
  either it becomes the paper's adoptable headline or every cheap activation score collapses 7->28, a claim about the class.
- >-
  CONCEDED reviewer MAJOR/evidence (S3, H-C): rho = 0.629 over 70 (member, axis) pairs is dominated by a between-axis-type
  contrast (A strong by construction, C/D null by construction); the reviewer's within-axis-A recompute gives 0.434, p 0.14.
  Within-axis-A across members becomes PRIMARY, the pooled version an explicitly labelled secondary, plus a C/D-dropped control
  and an axis-fixed-effect partial.
- >-
  CONCEDED reviewer MAJOR/rigor (S4, H-K): the verdict rule is n-asymmetric (READS issued at 7/12/28/32/33 refusals, all unpowered;
  UNDEFINED fires at 0-1, not <40 as the Method says). Tally must be reported twice (as-is and powered-only), with the minimum
  n at which AT_CHANCE is attainable footnoted, the gate description corrected as a logged deviation, and the abliterated
  arm restated as 1 powered + 4 underpowered.
- >-
  CONCEDED reviewer MAJOR/methodology (S5, H-L): axis A is fitted on canned-refusal wording and the detection LABEL is a canned-refusal
  regex, so the reading AUROC is partly definitional; re-score labels with the existing five-class semantic rubric on powered
  members and report the delta.
- >-
  ADDED H-X (reviewer MINOR/rigor, promoted as load-bearing): run arXiv:2607.13346's per-fold residualisation + leave-one-query-out
  on our own detection headline — the one published leakage control, worth 0.336 AUROC on its author's own data, left unrun
  on the very analysis it tests.
- >-
  DEGENERACY ADJUDICATION MEASURED (S6) [art_P-_YL8tdIwqF]: REVERSAL_DOES_NOT_SURVIVE 6/6 at matched contrast (B 0.028 vs
  A 0.747, random floor 0.146, NET -0.118); the screen removes NOTHING at matched contrast and ~none of the residual degeneracy
  at B's peak (70.2% of screen-passing text still judge-DEGENERATE); B survives only at 4.3x A's coefficient.
- >-
  AGGREGATION REPAIR COMPLETE (S7, H-U) [art__tq3ZgPRYB0B]: unit moves oriented rho by median 0.238 / max 0.557 and flips
  5 of 16 signs; SIGN_SURVIVES/EXCLUSION_LOST_AT_MEMBER_LEVEL on one carrier, SIGN_FLIPS on the other; protocol negative holds
  on 1.0000 of a 164,736-point grid, located in the verdict-class clauses not the cutoffs.
- >-
  POSITIONING TIGHTENED (S8) [art_G5SIDXT53EAW]: 2607.13346 is a weaker mirror (cross-model dissociation, MLP probe, Cohen's
  h, units not convertible, it DOES steer a refusal axis and get a null); LatentBiopsy 2603.27412 kills any 'first on abliterated
  checkpoints' claim; 9 of 21 2026 citations were wrong.
- >-
  ADDED H-N (reviewer MINOR/novelty): name leakage/distribution shift, aggregation (ecological) bias and small-sample correlation
  instability by their standard names with canonical citations, then claim the measured INSTANCE on our own published numbers
  rather than the phenomenon.
- >-
  ADDED H-A (reviewer MINOR/clarity + MINOR/evidence): add an abstract, renumber tables by first appearance, add refusal/compliance
  counts and a powered flag to the detection table, extend byte-identical regeneration to the paper's prose numbers (0.68
  vs 0.685 vs 0.691; 20 vs 21 measurable; artifact's stale 18/0/10 vs 20/1/9), complete reference [11].
- >-
  PRODUCT CLAIM NARROWED IN ADVANCE: if H-G's logit-gap score holds, it is NOT harmful-prompt-free (it reads the margin on
  harmful prompts), so the saving must be stated as 'no generation, no judge, no benchmark, no reference model' in the abstract
  rather than buried.
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

id: experiment_iter5_dir1
type: experiment
objective: >-
  H-G, THE NEW PRIMARY CLAIM. Run the first-decoding-step logit-gap harmful-prompt margin — the ONLY score in the discrimination
  matrix whose CI excludes zero at both aggregation units, costing 80 forward passes and ZERO generations per model — on the
  SAME 52-member / 28-lineage / 11-family scale panel that retired the AMS paraphrase refit, together with the benign variant
  and our-AMS sigma (free at the same cost, already implemented). Settle whether ANY cheap activation-derived safety score
  predicts judged plain-harmful refusal rate at n_lineage = 28, or whether the whole class collapses from 7 to 28 lineages.
approach: >-
  REUSE, NOT REBUILD. Read the iteration-3 and iteration-4 experiment trees directly from disk (experiment trees are not permitted
  dependency types, so read the workspace paths): 3_invention_loop/iter_3/gen_art/gen_art_experiment_1 (the logit-gap implementation
  and its unit test against the model's own logits at error 1.7e-5, the ORIENTATION_MAP, lib_iter3/statsx.py estimators) and
  3_invention_loop/iter_4/gen_art/gen_art_experiment_1 (the 52-member panel_selection.json, the frozen y_refusal block, gt_calibration.json,
  the Monte-Carlo lineage permutation with 200,000 draws, the dual-aggregation reporting, the sha256 reuse manifest discipline).
  Every reused file must be sha256-verified byte-identical with a hard failure otherwise, exactly as art_CZaytBH8uL4_ did,
  and the run must include a T0 replay leg that reproduces the archived 19-member logit-gap-harmful rho = 0.6673 EXACTLY before
  any new correlation is computed — if that leg fails, stop and report it. NOTE the known pitfall recorded in art__tq3ZgPRYB0B:
  iter-3 method.py is NOT import-safe (imports torch, calls setrlimit at import), so load its constant blocks by exec-ing
  only the literal constant sections and cross-check against prereg_iter3.json; note also that HF hidden_states[-1] is POST
  final-norm so the norm must not be re-applied. PANEL: the same 52 analysed members / 28 lineages / 11 families, at the same
  pinned revision SHAs, with the same lineage label as the resampling and permutation unit and the same two known-unrecoverable
  checkpoints excluded with their exception strings. The outcome variable y is the FROZEN judged plain-harmful refusal rate
  block whose byte-identical regeneration art_CZaytBH8uL4_ already proved (100% judge-cache hit, Wilson CIs identical) — do
  NOT re-judge; assert regeneration and reuse. If any member's y is missing, collect it with the same instrument (greedy,
  max_new_tokens=64, frozen plain-harmful core-80, repaired judge with EVALUATOR_SYSTEM verbatim, judge_cache reused) under
  a HARD $2.00 cap with cumulative cost logged after every call and graceful degradation to whatever n_lineage completes.
  SCORES, each 0 generations: (i) logit-gap harmful (80 forward passes, the margin between the top refusal-onset-token logit
  and the top affirmative/continuation-token logit at the FIRST decoding step, using the frozen per-tokenizer-family refusal_onset
  / continuation token lists from the dataset artifact — 10 families are covered there; log and report any panel family with
  no empirical lexicon entry rather than silently falling back); (ii) logit-gap benign (40 forward passes, frozen harmless
  prompts); (iii) our-AMS sigma (96 forward passes) as the anchor that ties this run to art_CZaytBH8uL4_'s numbers on the
  identical panel. PRE-REGISTER, sha256-stamped before ANY correlation is computed, with a timestamp-free content sha stable
  across reruns: (a) rho(logit-gap-harmful) >= 0.50 at the MEMBER level with a lineage-clustered bootstrap (10,000 reps) CI
  excluding 0; (b) the same at the LINEAGE-aggregated unit; (c) Monte-Carlo lineage permutation p well off the 5e-6 floor
  over 200,000 draws, with the floor stated; (d) the archived-19 vs new-33 BLOCK SPLIT reported as the decisive diagnostic
  exactly as in the refit study, since block localisation is what identified the refit's failure as a small-panel artifact
  — report per-block rho and the between-block difference with a CI; (e) leave-one-lineage-out (28 folds) and leave-one-family-out
  (11 folds) ranges; (f) a PRE-COMMITTED statement of what a partial result means — member-level exclusion with lineage-level
  failure is the SAME unit-dependence art__tq3ZgPRYB0B documents and is NOT a win, and must be reported as HOLDS_AT_MEMBER_UNIT_ONLY.
  Emit one of HOLDS / HOLDS_AT_MEMBER_UNIT_ONLY / COLLAPSES as a verdict string with the pre-registered rule quoted verbatim
  beside it. ALSO REPORT, because they cost nothing and pre-empt the obvious objections: the score's own scale/parameter-count
  partial correlation (is it just model size?), its correlation with the fraction of UNRELIABLE-flagged degenerate members,
  the 5 UNRELIABLE exclusions applied identically to iteration 4, both raw and disattenuated correlations given the REFUSAL
  kappa 0.3907, and the audit cost per member in measured forward passes and wall-clock seconds. HONESTY REQUIREMENT for the
  write-up: this score reads the margin ON HARMFUL PROMPTS, so if it holds the saving must be stated as 'no generation, no
  judge, no benchmark, no reference model' — never as harmful-prompt-free. DELIVERABLES: method.py with a single driver, prereg_iter5.json,
  per-member JSONs, a RESULTS.md whose every number is read from the JSON (never retyped, byte-identical regeneration asserted),
  and the three-score x two-unit table ready to paste into Table 3.
depends_on:
- id: art_CKWQh2cOQLLQ
  label: dataset
  relation_type:
  relation_rationale:
- id: art_0UsKSgsMHome
  label: baseline spec
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

--- Dependency 3 ---
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

### [2] HUMAN-USER prompt · 2026-08-13 03:26:55 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```
