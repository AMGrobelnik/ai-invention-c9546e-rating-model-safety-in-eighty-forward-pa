# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 3 · `gen_art`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-12 21:53:17 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Conduct thorough, unbiased research on the given topic.
Adapt your investigation approach based on the research question and domain.
</task>

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

<critical_requirements>
1. SOURCE DIVERSITY - Consult MANY sources (10+), not just the first few results
2. AVOID SELECTION BIAS - Actively seek contradicting viewpoints, not just confirming ones
3. TRIANGULATE - Cross-reference claims across multiple independent sources
4. ACKNOWLEDGE UNCERTAINTY - Be honest about confidence levels and limitations
5. SYNTHESIZE - Produce a coherent answer that accounts for conflicting evidence
</critical_requirements>

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

NOTE: a previous attempt at the task below was interrupted before it finished, and you are a FRESH session that does not remember it.

Any partial work the previous attempt wrote is on disk under /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1 — inspect that directory and REUSE whatever usable work is already there; do NOT start over from scratch if you can build on it. Then carry the task through to completion.

----- ORIGINAL TASK BELOW -----

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1/file.py`, `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_3/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for prior work and the field's landscape to ground your research.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<context>
<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>
</context>

<artifact_plan>
id: gen_plan_research_1_idx4
type: research
title: Where Our Steering Checks Meet Prior Work
summary: >-
  A primary-source positioning dossier for the five-check falsification protocol against the 2026 steering-vector reliability
  literature (arXiv:2602.06801, 2602.17881, 2604.15557, 2603.13359, 2602.02132), plus a targeted saturation check for published
  reliability-audit protocols for benchmark-free safety scores, a metadata verification pass over the already-pinned lane,
  and three ready-to-paste paragraphs: Related Work, the random-direction-null vs orthogonal-equivalence reconciliation, and
  the residual novelty statement. All five target papers were confirmed to exist during planning; one is a thesis, and the
  D/E role assignment in the direction is mis-attributed and must be corrected.
runpod_compute_profile: cpu_light
question: >-
  Given the 2026 steering-vector reliability literature, what exactly is left that is ours in the five-check falsification
  protocol and in the wording-not-behaviour result; and can our clean norm-matched random-direction null (0.00-0.058 refusal
  induction over alpha in [0,2] NORM_L units on benign prompts) be reconciled with the published orthogonal-equivalence finding
  by target and magnitude scope, or does it genuinely conflict?
research_plan: |-
  ## 0. Setup, ground rules, and what planning already established

  Load the `aii-web-tools` skill first (search / fetch / fetch_grep). Also read the dependency artifact at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/gen_art/gen_art_research_1/research_out.json` (and `research_report.md` if present) BEFORE any search — it already contains verified venue metadata, verbatim quotes and F1-F5 rows for 16 papers in the already-pinned lane, and this dossier EXTENDS it rather than redoing it. Do not re-extract anything that dossier already has an anchored quote for; cite it and move on.

  EVIDENCE RULE (non-negotiable, inherited from the prior dossier): every claim in the deliverable is either (a) a verbatim quote of <= 40 words with an `[arXiv:ID section/figure/table]` anchor, or (b) explicitly marked `NOT FOUND IN PRIMARY TEXT`. Never paraphrase an abstract and present it as a paper's finding. Abstract-only facts must be labelled `[arXiv:ID abstract]`. If only the abstract is reachable (no HTML, PDF extraction fails), say so per-paper in a `access` field rather than silently downgrading.

  NO CODE, NO DOWNLOADS. This is a pure web-research artifact. Budget 3h; target ~2h of extraction and ~45min of writing. $0 LLM spend (no OpenRouter calls needed).

  FACTS ALREADY VERIFIED DURING PLANNING (use them, but re-confirm titles/authors from the abs page in one fetch each, since the bibliography must not carry an error):
  - arXiv:2602.06801 — "On the Non-Identifiability of Steering Vectors in Large Language Models", Sohan Venkatesh and Ashish Mahendran Kurapath. Abstract asserts many behaviourally equivalent interventions exist "including orthogonal perturbations that achieve comparable effectiveness", equivalence-class dimensionality measured via covariance matrices, and that "non-identifiability is a robust geometric property that persists across diverse prompt distributions".
  - arXiv:2602.17881 — "Understanding Unreliability of Steering Vectors in Language Models: Geometric Predictors and the Limits of Linear Approximations", Joschka Braun. **This appears to be a THESIS, not a conference paper.** Verify the degree/institution/year on the abs page and cite it as a thesis; a mis-typed bibliography entry here is exactly the error class this artifact exists to prevent.
  - arXiv:2604.15557 — "Predicting Where Steering Vectors Succeed", Jayadev Billa (single author). Introduces the Linear Accessibility Profile (LAP) and metric A_lin from the logit lens; 24 binary concept families, five models Pythia-2.8B..Llama-8B; peak A_lin correlation with steering success +0.86 to +0.91, layer-selection prediction +0.63 to +0.92; a "three-regime framework"; middle-layer heuristic reported ineffective.
  - arXiv:2603.13359 — "From Refusal Tokens to Refusal Control: Discovering and Steering Category-Specific Refusal Directions", Alagharu, Singh, Shamsudeen, Wu, Panda. Llama-3-8B variant emitting categorical refusal tokens; separable category-aligned residual-stream directions; "a learned low-rank combination that mixes these category directions in a whitened, orthonormal steering basis"; reduces over-refusal while keeping harmful refusal; transfers across variants.
  - arXiv:2602.02132 — "There Is More to Refusal in Large Language Models than a Single Direction", Joad, Hawasly, Boughorbel, Durrani, Sencar. Eleven refusal categories (safety, incomplete requests, anthropomorphization, over-refusal) "correspond to geometrically distinct directions in activation space"; yet steering along any refusal direction gives similar refusal/over-refusal tradeoffs, acting as "a shared one-dimensional control knob"; different directions determine **how** a model refuses rather than **whether** it refuses.

  **CORRECTION THE EXECUTOR MUST MAKE (do not silently inherit the direction's framing):** the artifact direction attributes the "category-specific directions change HOW not WHETHER a model refuses" claim to arXiv:2603.13359. From the abstracts, that claim belongs to **arXiv:2602.02132**; 2603.13359 is a control/steering method paper (category tokens -> low-rank mixed steering basis) whose headline is over-refusal reduction. Verify this against both full texts, then state the corrected attribution explicitly in the dossier (a `attribution_corrections` field) so the paper's citation of record is right. This swap changes which paper is the nearest neighbour of our wording-not-behaviour headline — see step 4.

  ## 1. Per-paper extraction protocol (papers A-E)

  For each paper run the same three-stage loop, and run the five papers' stage-1 fetches in PARALLEL:
  1. `fetch` `https://arxiv.org/abs/<ID>` -> title, author list in order, submission date, version count, any comment field naming a venue or thesis.
  2. `fetch` the full text: try `https://arxiv.org/pdf/<ID>` first, then `https://www.alphaxiv.org/overview/<ID>` or `https://ar5iv.labs.arxiv.org/html/<ID>` as fallbacks. Record which worked in an `access` field.
  3. `fetch_grep` the full text with the paper-specific regexes below to pull exact numbers and method sentences. Always request context so the surrounding sentence is captured for the quote.

  Use this per-paper record schema (one object per paper in `research_out.json`):
  `{id, title, authors, venue_or_status, access, claim_extracted[], quotes[{text, anchor}], models, layers, behaviours, magnitude_regime{raw_units, normalised_units_if_stated, conversion_note}, panel_size, headline_numbers[], bears_on_which_protocol_check, relation_to_us (one of: THREAT / STRENGTHENING_CROSS_REFERENCE / ORTHOGONAL / RECONCILABLE_BY_SCOPE), point_of_use_sentence, not_found[]}`

  ### (A) arXiv:2602.06801 — non-identifiability / orthogonal equivalence. THE reconciliation target.
  Extract, in this priority order:
  - The exact formal statement of the equivalence class (definition/theorem/proposition environment) — quote it, with the anchor.
  - The ORTHOGONAL-perturbation efficacy numbers: what fraction of orthogonal directions were behaviourally equivalent, at what effect size, with what tolerance for "comparable effectiveness". Grep: `orthogonal`, `equivalen`, `effect size`, `Cohen`, `comparable`, `steering strength|coefficient|magnitude|\\alpha|lambda|scale`, `norm`, `dimension(ality)? of the equivalence`.
  - Panel: which MODELS, which LAYERS, which TARGET BEHAVIOURS (is refusal among them? is any target measured on BENIGN prompts?). Grep: `Llama|Qwen|Gemma|Pythia|Mistral`, `layer`, `refus|sycophan|corrigib|truthful|hallucin|CAA|Anthropic`.
  - The MAGNITUDE REGIME in units comparable to ours: do they report multiples of the activation norm (`c*||h||`), raw coefficient values, or normalised units? Grep for `\\|h\\||norm of the activation|fraction of the norm|relative norm|coefficient of` and `%` near `norm`. If they give only raw coefficients on named models, record that and mark the conversion `NOT DERIVABLE FROM PRIMARY TEXT` — do NOT invent a conversion.
  - Whether they evaluate INDUCTION of a behaviour that is absent by default, or MODULATION of a behaviour already present. This distinction is the load-bearing half of our reconciliation.

  ### (B) arXiv:2602.17881 — geometric predictors of unreliability. The published counterpart of our protocol check (3).
  Extract: the exact geometric quantities (cosine similarity between training activations; positive/negative separation along the steering direction; directional distinctness of vectors trained on prompt variants), the panel (models, behaviours, n datasets), and the ACCURACY/CORRELATION with which each predicts unreliability (grep `r =|rho|Spearman|Pearson|AUROC|accuracy|correlat`). Then answer the direction's specific question: **does the work already PRESCRIBE a layer-span or layer-sensitivity diagnostic?** Grep `layer sweep|across layers|layer selection|layer span|best layer|layer-wise`. If yes, quote it and state precisely what our check (3) adds (our claim: a metric-level span statistic — the ratio of the estimate across L-2..L+2 for BOTH estimators, 4.4x logistic vs 1.8x non-parametric — used as a PASS/FAIL gate on a downstream SCORE, versus their per-vector reliability prediction). If no, say `NOT FOUND IN PRIMARY TEXT` and note that our check is then not anticipated there.

  ### (C) arXiv:2604.15557 — LAP / A_lin, predicting where steering succeeds.
  Extract the A_lin definition verbatim (it is logit-lens based; our r_t observable is also logit-lens based — note that overlap explicitly), the three regimes with their boundaries, the panel, and the correlation numbers (+0.86..+0.91, +0.63..+0.92 — confirm against the text, do not trust the abstract). Then answer the decisive question: **would LAP have predicted alpha_50's failure ex ante?** Concretely: does LAP score a DIRECTION/CONCEPT or a LAYER; is refusal among the 24 concept families; do they report an A_lin value or regime for refusal; and does the framework predict that a semantically-equivalent but lexically-disjoint axis would fall in a different regime from the canned axis? If it would have predicted the failure, write it up as a STRENGTHENING cross-reference ("an independent, published ex-ante predictor agrees with our post-hoc check") and draft that sentence. If it is silent on refusal or scores only layers, say so plainly — a cross-reference we cannot substantiate is worse than none.

  ### (D) arXiv:2603.13359 — category-specific refusal control.
  Extract the exact claim and the evidence table (over-refusal reduction and harmful-refusal retention numbers, transfer results, the whitened orthonormal basis construction). Determine whether they anywhere claim direction choice changes refusal STYLE rather than incidence — if that claim is absent here, record `NOT FOUND IN PRIMARY TEXT` and move the positioning weight onto (E), per the attribution correction in step 0.

  ### (E) arXiv:2602.02132 — more to refusal than a single direction. **HIGHEST-RISK PAPER; do this one most carefully.**
  This is simultaneously the nearest published neighbour of our wording-not-behaviour headline AND a potential direct threat to it. Their "steering along any refusal direction produces similar refusal-to-over-refusal tradeoffs / a shared one-dimensional control knob" is, read naively, the OPPOSITE of our finding that a token-disjoint paraphrase axis B never reaches 50% refusal on 6/6 checkpoints. Extract, with quotes:
  - Exactly HOW the eleven category directions were built (diff-in-means? on what contrast pairs? prompt-only or full-generation activations?), on which models/layers.
  - The exact evidence for "shared one-dimensional control knob": is it a refusal-rate-vs-over-refusal CURVE per direction, and do all directions actually REACH high refusal, or are the curves merely parallel/rescaled? Grep `knob|trade-?off|Pareto|refusal rate|over-?refusal|sweep|coefficient|\\alpha`. Record the maximum induced refusal rate per direction if reported.
  - Whether any of their directions FAILS to induce refusal at achievable magnitudes, and whether they report per-direction vector NORMS (our A/B norms are 10.3-10.6 vs 2.6-2.7).
  - Whether their prompt set is HARMFUL or BENIGN. Our claim is about INDUCING refusal on BENIGN prompts; if their knob is measured on prompts where refusal is already partly present, the tension dissolves by target.
  - What multi-dimensionality they establish, and whether it undermines our "the axis is forced" argument (i.e. that a dose must be defined on the axis that actually carries the behaviour).
  Then classify the relation in `relation_to_us` with a written justification, and produce BOTH: a sentence for the case where scope reconciles the tension, and an explicit `refutation_risk` entry stating what in their result would, if it holds on benign-prompt induction at matched norm, downgrade our lexicality headline. Do not soften this. A named live threat in the dossier is worth more than a smooth paragraph.

  ## 2. The reconciliation paragraph (the direction's central deliverable)

  Write ~200-300 words reconciling arXiv:2602.06801's orthogonal-equivalence with our norm-matched random-direction null (refusal induction 0.00-0.058 over alpha in [0,2] NORM_L units on BENIGN prompts; axis C stylistic null 0.00). Structure it on exactly three axes, each with numbers from BOTH sides:
  1. **Target.** Ours = INDUCING refusal where the default behaviour is compliance, on benign prompts. Theirs = <fill from extraction>. If theirs is modulation of an already-expressed behaviour, or a non-refusal concept, say so with the quote.
  2. **Magnitude regime.** Ours = alpha in [0,2] in NORM_L units (multiples of the layer-L activation norm), which the prior dossier notes is the same calibration as Rogue Scalpel's `alpha = c*mu^(l)`, c in {0.25..2.0}; and the prior dossier's find that a working format intervention lives at 0.6% of the activation norm while random-direction effects live at 25-200%. Theirs = <fill>; if not convertible, say `NOT DERIVABLE FROM PRIMARY TEXT` and reconcile on target alone, stating that the magnitude leg is unverified.
  3. **Criterion.** Ours = a hard behavioural threshold (a 50% refusal RATE), not a graded effect. "Comparable effectiveness" in an equivalence-class sense can hold on a graded effect measure while every member still sits below a 50% rate threshold — check whether their effectiveness measure is graded or thresholded and quote it.
  Close with two explicit sentences: **what our null DOES claim** ("norm-matched random directions do not induce refusal on benign prompts at alpha <= 2 NORM_L, so the axis-A effect is not 'any direction steers'") and **what it does NOT claim** ("it is not a claim that the refusal axis is unique or identifiable; 2602.06801's equivalence class is compatible with our null and we do not contest it").
  **If the reconciliation does NOT hold** — e.g. their orthogonal perturbations induce refusal on benign prompts at alpha <= 2 NORM_L — write that plainly as a `reconciliation_verdict: CONFLICT` with the offending numbers, and draft the paragraph the paper would then need, which concedes the null is weaker than presented. This outcome must reach the paper; do not bury it.

  ## 3. (F) Saturation check: published falsification protocols for benchmark-free / activation-based safety SCORES

  Scholarly mode (`mode=scholarly`) plus general mode, at least 10 distinct queries, reporting HITS not a zero-hit claim. Run in parallel batches:
  - "falsification protocol interpretability metric"; "validity checklist alignment metric"; "reliability audit activation-based safety score"; "benchmark-free safety evaluation language model"; "sanity checks saliency" (the Adebayo-style precedent — the closest methodological ancestor and it MUST be cited if the protocol is framed as a checks-suite); "sanity checks for interpretability methods"; "construct validity NLP evaluation metric"; "metric validation protocol LLM safety audit"; "do steering vectors generalize evaluation protocol"; "leave-one-out stability interpretability metric jackknife"; "paraphrase invariance probe evaluation".
  For each hit, record id/title/venue/year and a one-line statement of what it prescribes. Then answer explicitly: **does an equivalent checks-suite already exist?** If yes, identify precisely the residual — our candidate residual is (i) the checks are applied to a benchmark-free SAFETY SCORE rather than to an explanation or a steering method, and (ii) the protocol is required to DISCRIMINATE (pass our-AMS, fail alpha_50) rather than only to condemn. Verify that framing is not itself standard practice (grep the strongest hit for `discriminat|control metric|positive control|negative control`). Note that a positive/negative-control requirement on a metrics checklist would be the sharpest possible prior art — search for it deliberately, do not hope to miss it.

  ## 4. Positioning sentence for the wording-not-behaviour headline

  After (D)/(E) are extracted, write the careful contrast sentence the direction asks for, in the corrected attribution:
  - Theirs (arXiv:2602.02132, and 2603.13359 for the control side): among directions that ALL carry refusal, the choice of direction changes HOW/WHICH refusals occur, with a shared tradeoff curve.
  - Ours: a LEXICALLY DISJOINT, SEMANTICALLY EQUIVALENT axis of comparable detection quality cannot induce refusal AT ALL at achievable magnitude (A crosses at 0.88-1.57 axis-contrast units; B reaches ~16 contrast units at the grid maximum and never crosses), so a steering-STRENGTH metric built on the canned axis prices the WORDING, not the behaviour.
  - State the precondition honestly: this contrast only survives if H-L re-certifies axis B against the models' own generated refusals; until then the sentence must be written in the provisional form. Draft BOTH forms — the confirmed-lexicality sentence and the downgraded "axis-estimation fragility" sentence — so the paper can drop in whichever H-L returns.

  ## 5. (G) Cross-check of the already-pinned lane + metadata verification

  For Logit-Gap (2506.24056), Galeone (2606.24952), Taimeskhanov (2602.02712), Wu (2608.08159), abliteration audit (2607.01854): re-read the prior dossier's rows and ask ONE question of each — does any claim change now that the framing is a DISCRIMINATING PROTOCOL rather than a steering-strength metric? Expected live items to check: (a) Wu 2608.08159's warning that a trend "depends jointly on raw units, the readout metric, and the operating point" now applies to the protocol's check (3) as well as to NORM_L — state what we do about readout metric and operating point; (b) Galeone's functional criterion (the steerable case is where the intervention direction also DETECTS) is a published relative of our protocol check (1), and our 0.69-AUROC axis that does steer is a counterexample — restate as "in tension with", never "refutes"; (c) the abliteration audit's AUROC 0.95 with an attested reference is the competitor our protocol must be positioned against on the reference-free axis. Only re-fetch a paper if the new framing raises a question the prior dossier's quotes cannot answer.
  Metadata: for all FIVE new entries verify authors (exact order and spelling), title, year, and venue-or-preprint-or-thesis from the arXiv abs page comment field, plus one corroborating source (Semantic Scholar or the venue site) where a venue is claimed. Flag any title change between versions. Explicitly record 2602.17881's status (thesis + institution) — the prior dossier already caught one author mis-attribution (Rogue Scalpel = Korznikov et al., not Kaminski), so treat metadata as error-prone by default.

  ## 6. Deliverables

  **`research_report.md`**, sections in this order:
  1. Executive summary + saturation verdict for the PROTOCOL specifically (adjacent work exists / equivalent exists / none found), in one paragraph.
  2. Attribution corrections (the D/E swap; anything else found).
  3. Per-paper dossiers A-E, each with verbatim quotes + anchors, the extraction schema fields, and a `relation_to_us` verdict with justification.
  4. The reconciliation paragraph (ready to paste), with its `reconciliation_verdict`.
  5. Ready-to-paste "Steering-vector reliability" Related Work paragraph (150-220 words, every sentence citable, no claim without an anchor).
  6. Point-of-use citation sentences, one per protocol check: (1) lexical disjointness -> Galeone functional criterion + 2602.02132; (2) monotonicity/in-grid guard -> 2602.02712 Thm 3.6 + coherence-collapse cites; (3) layer/depth sensitivity -> 2602.17881 + 2604.15557; (4) leave-one-lineage-out jackknife -> 2602.17881 + whatever step 3 surfaces; (5) scorer validity/kappa -> step 3 hits. Plus sentences for the lexicality discussion and the random-null discussion.
  7. Residual novelty statement, ONE paragraph, written after all the above is granted: what remains ours. It must name what we concede (steering fragility is known; non-identifiability is known; layer sensitivity is known; ex-ante predictors exist).
  8. Refutation risks and open threats, ranked, with the 2602.02132 knob result first if it survives extraction as a threat.
  9. Bibliography table: id, title, authors, year, venue/status, verified-by URL.

  **`research_out.json`**: `{answer: <the residual-novelty statement plus saturation verdict, ~300 words>, sources: [{id, url, title, authors, venue_or_status, access, relation_to_us, key_quotes:[{text, anchor}]}], follow_up_questions: [...]}` plus top-level keys `papers` (the five extraction records), `reconciliation` `{verdict, paragraph, target_axis, magnitude_axis, criterion_axis, unverified_legs[]}`, `saturation_F` `{hits[], verdict, residual}`, `pinned_lane_updates[]`, `attribution_corrections[]`, `point_of_use_sentences` (keyed by protocol check), `related_work_paragraph`, `refutation_risks[]`, `metadata_verification[]`.
  Run the `aii-json` skill to validate, and `aii-file-size-limit` if the JSON is large.

  ## 7. Failure scenarios and how to handle them
  - **PDF/HTML unreachable for a paper.** Fall back in order: arxiv abs -> alphaxiv -> ar5iv -> Semantic Scholar abstract -> huggingface papers page. Record `access` and mark every downstream field abstract-only. Never upgrade an abstract sentence to a "section 4 finding".
  - **A number named in the direction is not in the text** (e.g. specific orthogonal-efficacy figures). Write `NOT FOUND IN PRIMARY TEXT` in `not_found[]` and, where it matters, say which claim of ours is therefore unsupported by that citation.
  - **The magnitude regimes are not convertible.** Say so; reconcile on target and criterion only; label the magnitude leg `UNVERIFIED` in the reconciliation object. Do not manufacture a conversion factor.
  - **(E) turns out to be a genuine threat.** Do not soften. Produce the `refutation_risk` entry, quantify what evidence would settle it (a benign-prompt induction sweep on their category directions at matched norm), and add it as the top `follow_up_question` — this is exactly the kind of finding this artifact exists to surface before the paper is written.
  - **Step 3 finds an equivalent published protocol.** Then H-P's novelty claim shrinks to the discrimination requirement and the safety-score application. Say so explicitly and rewrite the residual-novelty paragraph accordingly rather than defending the original framing.
  - **Time pressure.** Priority order if the 3h runs short: (A) reconciliation > (E) threat assessment > (F) saturation > (B)/(C) > (D) > (G) metadata. The reconciliation paragraph and the (E) verdict are the two things the paper cannot be written without.
explanation: >-
  Iteration 3's primary claim (H-P) is that the five-check falsification protocol DISCRIMINATES between benchmark-free safety
  scores rather than merely describing alpha_50's death. That claim is only publishable if it is not a rediscovery of the
  2026 steering-vector reliability literature, which independently established non-identifiability (2602.06801), geometric
  predictors of steering unreliability (2602.17881), ex-ante prediction of where steering succeeds (2604.15557), and multi-directionality
  of refusal (2602.02132, 2603.13359). Without this dossier the paper risks two specific, fatal errors: (i) presenting checks
  (1) and (3) as novel when published counterparts prescribe them, and (ii) presenting a clean norm-matched random-direction
  null that a reviewer reads as contradicted by a published orthogonal-equivalence result. Both are addressed here by extracting
  exact scope (target behaviour, magnitude regime in comparable units, induction-vs-modulation, thresholded-vs-graded criterion)
  from primary text rather than abstracts. The dossier also front-loads the sharpest live threat to the surviving headline:
  2602.02132's report that steering along ANY refusal direction acts as a shared one-dimensional control knob is, on its face,
  in tension with our finding that a token-disjoint paraphrase axis never induces refusal — and whether that tension dissolves
  by target and magnitude scope, or survives as a refutation, must be known before the paper is drafted, not after review.
  Finally it fixes a mis-attribution already visible in the direction (the HOW-not-WHETHER claim belongs to 2602.02132, not
  2603.13359) and verifies that one target is a thesis rather than a paper, so the bibliography does not carry an error into
  the record.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-12 21:53:17 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-web-tools · 2026-08-12 21:53:23 UTC

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

### [4] SYSTEM-USER prompt · 2026-08-12 22:09:56 UTC

```
<verification_failed>
Your research output failed verification (attempt 1/10).
</verification_failed>

<schema_errors>
JSON SCHEMA ERRORS:
  - research_out.json: Source 0 missing 'summary'
  - research_out.json: Source 1 missing 'summary'
  - research_out.json: Source 2 missing 'summary'
  - research_out.json: Source 3 missing 'summary'
  - research_out.json: Source 4 missing 'summary'

Fix: research_out.json must have:
     {
       "answer": "comprehensive answer with [1], [2] citations",
       "sources": [{"index": 1, "url": "...", "title": "...", "summary": "..."}],
       "follow_up_questions": ["Question 1?", "Question 2?"],
       "summary": "what was found"
     }

     Each citation [N] in answer MUST match a source with that index.
</schema_errors>

<content_warnings>
CONTENT ISSUES:
  - research_out.json: Sources with uncited indices: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

Fix: Ensure answer is comprehensive, has proper citations, and all sources are cited.
</content_warnings>

<task>
FIX ISSUES:
1. Output valid research_out.json with all required fields
2. Ensure every factual claim has a numbered citation [1], [2], etc.
3. Ensure every source has a matching citation in the answer
</task>
```
