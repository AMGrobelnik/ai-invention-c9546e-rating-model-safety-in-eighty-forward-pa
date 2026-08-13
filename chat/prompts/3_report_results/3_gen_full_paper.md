# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 06:49:10 UTC

````
<research_methodology>
Write like an experienced academic. Reviewers judge both the science and the writing.

- Claims must be proportional to evidence. Choose verbs carefully — "demonstrate," "observe," and "hypothesize" mean different things.
- Every result needs: what was measured, on what data, the numbers, and what they mean.
- Methodology must be specific enough to reproduce. Related work must be organized by theme, not a literature dump.
- State limitations honestly. Avoid both overclaiming and excessive hedging.
</research_methodology>

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

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: Rating Model Safety in Eighty Forward Passes
abstract: >-
  Deciding whether an open-weight checkpoint is safety-aligned normally costs hundreds of harmful generations plus a judge
  model, per checkpoint. Cheap activation-based alternatives exist, but every one we could locate in primary text is validated
  on four or fewer architecture families, and none resamples on the weight lineage -- the unit at which checkpoints derived
  from a common base are not independent. We ask whether any member of this class predicts behaviour once the panel is large
  enough to say. On 52 checkpoints over 28 weight lineages and 11 families, the first-decoding-step logit-gap margin -- 80
  forward passes, no generation, no judge, no benchmark run, no reference model -- predicts the judged plain-harmful refusal
  rate at Spearman rho = 0.694 [0.495, 0.822] with the lineage as the resampling unit, and 0.564 [0.140, 0.826] with members
  aggregated within lineage. It transfers across provenance blocks (0.667 on 19 archived members versus 0.668 on 33 new ones),
  is not a parameter-count proxy (partial rho 0.676), and beats our reimplementation of the closest published activation scanner
  by +0.421 [0.169, 0.684]. The margin is read on harmful prompts, so it is not harmful-prompt-free; the benign variant collapses
  to 0.129. The same panel retracts two of our own earlier results: a paraphrase refit of that scanner falls from +0.296 at
  7 lineages to +0.099 [-0.027, 0.244] at 28, localised to the block that produced it, and a claimed read-versus-act coupling
  of 0.629 is 89.6% a between-axis-type contrast by exact decomposition, its within-axis value being 0.547 with an interval
  covering zero. The difference between a cheap safety score that works and one that does not is invisible at seven lineages
  and legible at twenty-eight.
paper_text: |
  # Introduction

  Anyone who downloads an open-weight checkpoint faces a question with no cheap answer: is this model safety-aligned, and how much? The standard answer is a harmful-prompt benchmark such as AdvBench [1], JailbreakBench [2] or HarmBench [3], several hundred generations scored by a judge model [4], and a repeat of the whole procedure for every attack template of interest. The evaluator must hold, transmit and store harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown.

  The stakes are set by scale. Hugging Face hosts hundreds of thousands of derived checkpoints, a growing fraction of them explicitly *uncensored* community fine-tunes, and the cheapest of these is produced by a weight edit — *abliteration* — that orthogonalizes every write against a single refusal direction [5]. A platform, a downstream deployer or a regulator wanting to triage such a population needs a score that costs seconds per model.

  The published attempts at such a score are validated on panels far too small to support them, and the panel size is the part nobody reports. AMS [6] scans activation geometry over 14 configurations from 4 architecture families and reports Pearson $r = -0.546$ ($p = 0.043$) against behavioural compliance — its directly comparable rank statistic is $\rho = -0.423$ at $p = 0.13$, which is not significant. RAS/SafeVec [7] needs unsafe prompts, jailbreak prompts and a safety-aligned reference model, and reports no correlation coefficient, no $n$ and no resampling unit. VISAGE [8] evaluates a harmful benchmark at every weight perturbation. AQI [9] claims correlation with external judges with no locatable $n$ or coefficient. The one audit that exceeds 20 checkpoints — 273 of them — scores a *binary* uncensored label and presumes an attested reference model plus a full weight download [14]. Of the five model-level internal safety scores we could locate in primary text, five validate at four or fewer architecture families, four at fourteen or fewer checkpoints, and **zero** resample on the weight lineage \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-5/research-1}}. Whether any member of this class predicts behaviour once the panel is large enough to say has, until now, not been tested by anyone.

  This paper tests it, and one score passes. On a frozen panel of 52 checkpoints over 28 weight lineages and 11 architecture families, the first-decoding-step logit-gap margin read on harmful prompts — 80 forward passes, zero generations, zero judge calls, zero benchmark runs, zero reference models per checkpoint — predicts the judged plain-harmful refusal rate at Spearman $\rho = 0.694$ $[0.495, 0.822]$ with the lineage as the resampling unit, and $0.564$ $[0.140, 0.826]$ when members are first aggregated within lineage. It is not a small-panel artifact: split by provenance, the 19 archived members give $\rho = 0.667$ and the 33 newly measured ones $\rho = 0.668$, a difference of $-0.0004$. It survives a partial correlation on $\log_{10}$ parameter count ($0.676$), 28 leave-one-lineage-out folds ($[0.661, 0.726]$) and 11 leave-one-family-out folds ($[0.650, 0.772]$) without a sign change, and it beats our reimplementation of the closest published activation scanner by $+0.421$ $[0.169, 0.684]$ on the same resampled lineages.

  The honesty statement that must travel with that number, and that we put in the abstract rather than a footnote, is what the score does *not* remove. It reads the margin on harmful prompts, so it is not harmful-prompt-free; the benign-prompt variant collapses to $\rho = 0.129$ $[-0.168, 0.436]$. What it removes is everything downstream of the forward pass: no generation, no judge, no benchmark, no reference model.

  [FIGURE:fig1]

  The same panel is what retires the rest of this project's programme, and we report those retractions as results rather than as limitations. Two iterations ago we proposed an act-side score — $\alpha_{50}$, the steering coefficient at which a fresh generation on a benign prompt refuses half the time — and it failed. The five-check falsification battery built to explain that failure could not rank cheap scores either. One positive lead survived, a paraphrase refit of AMS's contrast set that lifted criterion validity from $\rho = 0.358$ to $0.654$ on 7 lineages; measured on the same 28-lineage panel it collapses to $\Delta_A = +0.099$ $[-0.027, 0.244]$, with the effect localised entirely to the original 19-member block. Two scores, one panel, opposite outcomes: that contrast is what makes the panel informative rather than merely large.

  The previous draft of this paper additionally claimed that reading and steering along one refusal axis are strongly coupled, at $\rho = 0.629$ over 70 (member, axis) pairs. A reviewer identified that statistic as dominated by a between-axis-type contrast, and re-analysis confirms it: an exact two-way decomposition attributes $0.896$ of the pooled coefficient to variation between axis types \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-5/evaluation-1}}. The correct primary statistic — within the canonical axis, across models — is $\rho = 0.547$ with a lineage-clustered interval of $[-0.031, 0.930]$ that covers zero. We report the weaker claim.

  ## Summary of Contributions

  - **A cheap safety score that survives a fourfold panel increase** (§5.1) \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-5/experiment-1}}. The first-decoding-step logit-gap harmful margin predicts judged plain-harmful refusal at $\rho = 0.694$ $[0.495, 0.822]$ (member unit, lineage-clustered bootstrap) and $0.564$ $[0.140, 0.826]$ (lineage unit) over 52 members / 28 lineages / 11 families, with a Monte-Carlo lineage-permutation $p$ at the $5\times10^{-6}$ design floor. The archived-19 vs new-33 block split gives $0.667$ vs $0.668$. Cost: 80 forward passes, 0 generations, median 20.0 s per checkpoint including download.
  - **The first model-level criterion validation in this class that resamples on the weight lineage** (§2, §5.1) . Zero of five published model-level internal safety scores do; the widest published family axis is four, against our eleven. We claim neither the scalar (it is Li and Liu's [10]) nor the largest checkpoint panel (Hurtado's [14]) — only the conjunction.
  - **A companion negative that makes the positive interpretable** (§5.2) \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-4/experiment-1}}. On the identical panel the AMS paraphrase refit gives $\Delta_A = +0.099$ $[-0.027, 0.244]$ against an archived $+0.296$, an independently authored paraphrase set gives $-0.152$, and the effect is localised: the archived 19 reproduce $+0.2963$ to $2.6\times10^{-4}$ while the 33 new members give $-0.016$. Panel size is not a nuisance parameter in this lane; it decides which of two same-cost scores you would ship.
  - **The read-versus-act coupling, re-estimated without the axis-type confound** (§5.3) . Within the canonical axis across 14 detection-powered members: $\rho = 0.547$ $[-0.031, 0.930]$, exhaustive permutation $p = 0.149$; lineage unit $0.821$ $[0.348, 1.000]$. The pooled $0.629$ is demoted to a secondary and decomposed: $0.896$ between axis type, $0.036$ between members, $0.069$ residual. Verdict: `COUPLING_IS_AXIS_TYPE_CONTRAST` and `UNDERPOWERED`, both firing.
  - **The verdict rule is $n$-asymmetric, and we quantify by how much** (§5.3). Simulating the study's own bootstrap over 141 cells, `AT_CHANCE` is unreachable below 40 items per class ($P = 0.000$ at the pre-registered gate; Hanley–McNeil closed form $n = 65$; first attainable at $n = 80$), while `READS` fires with probability $1.000$ under perfect separation at $n = 7$. The tally is now reported twice — 20/1/0/9 over all 30 members, 13/1/0/0 over the 14 powered ones — and the abliterated-arm claim is re-carried on refusal *rates* (exhaustive permutation $p = 0.0026$; paired sign test 10/10, $p = 0.0020$), needing no AUROC at all.
  - **The detection label and the axis share a lexical basis, and the consequence is measured** (§5.3) [ARTIFACT:art_Y-oGSm04Tcar]. Re-labelling 660 stratified items with a five-class semantic rubric barely moves the pooled AUROC ($0.834 \to 0.821$, paired $-0.013$ $[-0.067, +0.030]$), but splits it: $0.897$ $[0.864, 0.922]$ on canonically-worded refusals against $0.611$ $[0.542, 0.686]$ on non-canonical ones, which does not clear the members' own random-direction reading band. Verdict: `READS_CANONICAL_WORDING_ONLY`.
  - **The one published leakage control, run on our own headline** (§5.3). Re-estimating every centring and scaling statistic inside the training fold under leave-one-prompt-out moves axis-A AUROC by $-0.0205$ $[-0.0352, -0.0071]$, against the $-0.336$ the same control produced on its author's data [44]; the control on the control moves random axis D by $-0.0020$.
  - **Three named measurement pathologies, each measured on our own published numbers** (§6) . Item-pool provenance is leakage type [L3.3] in Kapoor and Narayanan's taxonomy [46]; the aggregation unit moving $\rho$ from $0.358$ to $0.821$ is ecological correlation in Robinson's sense [47]; the $7\to28$ lineage collapse is small-sample correlation instability, and Schönbrodt and Perugini's own table puts our $n = 28$ six to nine times below the point of stability [49, 50]. We claim the instances, not the phenomena.

  # Related Work

  **Static, benchmark-free safety metrics, and how they are validated.** AMS [6] computes a standardized mean difference of projections onto a diff-in-means direction at 96 forward passes per model. RAS/SafeVec [7] extracts layer-wise refusal directions from a safety-aligned reference model and scores a target by hidden-state alignment. VISAGE [8] measures a weight-space safety basin, requiring a harmful benchmark at every perturbation. AQI [9] is a prompt-invariant latent-geometry diagnostic. RAS and VISAGE we do not run, for reasons fixed by a primary-source reimplementation audit \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-1/research-1}}: every RAS-scored checkpoint is $\geq$4B and none overlaps any panel at our scale, and VISAGE at published fidelity costs 4,800 generations and roughly 28 hours per 1B model on CPU. AMS and Logit-Gap Steering [10] we reimplement and run.

  What is uniform across these papers is the thinness of the validation panel, and a dossier read all five in primary text to establish it . AMS validates at 14 configurations over 4 families; RAS states a qualitative correlation with attack success rate across 3 families with no coefficient, $n$ or resampling unit; AQI's abstract claims correlation with external judges with neither $n$ nor coefficient locatable; Logit-Gap Steering validates a *per-prompt* margin against its own attack's success rate across suffix strategies, with family-clustered inference at $n = 3$; Hurtado's abliteration audit [14] exceeds 20 checkpoints at 273 but against a binary label, with an attested reference and full weight access. Not one resamples on the weight lineage — the unit at which the statistical dependence actually lives, since one pretrained base and its derivatives are not independent observations. That is the gap §5.1 fills, and it is a gap in *validation practice*, not in scalar design.

  **The scalar we validate is not ours.** Logit-Gap Steering [10] defines the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step as "the per-prompt safety margin that alignment provides", and reports that the aligned model's gap exceeds the base model's on 97.5–99.8% of toxic prompts, with position-1 accounting for 92–99% of the refusal decision depending on family. A full-text extraction confirms that no cross-model margin-versus-behaviour correlation exists anywhere in that paper: all 28 correlation matches are token-level, suffix-level, or cited from elsewhere . One estimand difference must be declared: their affirmative token is selected *per prompt* as the highest-logit one, making their gap an attack-relevant minimum, whereas our fixed-lexicon maximum is a different quantity. Xu and Sheng [51] use refusal vectors as a provenance fingerprint over 76 offspring models, identifying the base family at 100% accuracy — model identity, not safety behaviour, which is the cleanest available contrast to what we predict.

  **Detection versus intervention.** Galeone et al. [12] establish that a detection direction at AUC $1.000$ can sit at $\cos = 0.12$ from the direction that produces the behaviour, and propose a *functional* criterion: the steerable case is where the intervention direction also detects. Mehta [44] is the closest published neighbour to the read-versus-act claim our previous draft led with, and it is a mirror image: one direction detects alignment faking at leave-one-query-out AUROC $0.87$ on Llama-3.1-8B while steering over 2,000 runs "barely changes compliance" (Cohen's $h = +0.057$, Fisher $p = 0.41$). Three distinctions were verified in full text \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-4/research-1}}: his dissociation is assembled *across two models* (the steering null is on Qwen3-32B, where his own detection falls to $0.43$), his probe is a two-layer MLP rather than the steered unit vector, and no activation norm is reported, so his coefficient is not convertible to our contrast units. One concession is forced: he does steer a refusal axis and get a null. The most transferable thing in his paper is not the dissociation but the leakage control it survived — his own AUROC falls from $0.761$ to $0.43$ under per-fold residualisation and leave-one-query-out, and it reaches $0.63$ on a control condition where the effect cannot exist. We run that control on our own headline in §5.3. Nadaf [23] independently reports that steering succeeds where the logit lens cannot decode across 4,032 concept-layer pairs while the converse is "nearly empty (3 of 72)", which makes coupled read–act the expected case.

  **Activation scores on abliterated checkpoints.** Two incumbents bound what we may claim . Hurtado [14] separates 57 public abliterations from 37 benign fine-tunes at AUROC $0.95$, but the activation leg is a thresholded ratio (AUROC $0.84$) that "certifies whether the refusal mechanism is present, not whether a model is harmless", and it "presumes an attested reference". Llorente-Saguer [45] already runs base / instruction-tuned / abliterated Qwen triplets and reports that "both abliterated variants achieve AUROC at most 0.015 below their instruction-tuned counterparts", noting that its axis "is not the refusal direction itself, since it survives abliteration". Any claim to be first to read an activation safety score on abliterated checkpoints is therefore withdrawn. What survives, and what §5.3 reports, is narrower and compatible: the *refusal axis specifically* goes quiet on abliterated checkpoints, because the refusals it would read are gone.

  **Steering-vector reliability.** Non-identifiability is established: steering vectors admit "large equivalence classes of behaviorally indistinguishable interventions" [15]. Unreliability has geometric predictors across 36 datasets [13], and the safety cost of steering has been catalogued [40]. Success is partly predictable ex ante at $\rho = +0.86$ to $+0.91$ across 24 concept families [16], though the Linear Accessibility Profile could not have predicted our axis comparison, because it never sees the steering direction and both of our axes score identically. Refusal is multi-directional: eleven category directions, several near-orthogonal, yield "nearly identical refusal to over-refusal trade-offs" [17], and category-specific directions can be composed for control [18]. Petrov [19] was the top refutation risk for our axis comparison, reporting that changing only the contrast baseline "produces no functional refusal directions at any tested weight level on any tested layer" by "reducing the extracted direction magnitude below the threshold at which weight-matrix projection perturbs the residual stream"; §5.4 settles it on 30 checkpoints in axis-contrast units, which normalise the axis magnitude by construction. Wu et al. [37] show a "steerability emerges with scale" result dissolves under exactly that normalisation.

  **Auditing a safety measurement, and the pathologies we name.** The battery framing is prior art in kind and we say so. Wang et al. [20] separate "construct validity ... metric validity ... criterion validity", run pre-specified positive and negative controls, and survive "leave-one-organization-out and organization-clustered bootstrap"; they are also the source of the field-local warning that a small panel manufactures results — a correlation moving "from $-0.64$ at $n=7$ to $+0.02$ at $n=18$", with "a quarter of random size-7 subsets" showing $|\rho| \geq 0.5$ despite a near-zero full-panel value. Weng et al. [21] operationalise rubric-semantics invariance under certified-equivalent rewrites and state the discrimination requirement outright. The methodological ancestor of both is the sanity-check literature for saliency maps [22]. Outside machine learning, the three phenomena §6 names have canonical statements: Kapoor and Narayanan's leakage taxonomy [46], whose type [L3.3] *sampling bias in test distribution* is our item-pool case exactly; Robinson's demonstration that an ecological correlation can differ in sign from its individual counterpart [47], extended by Openshaw's modifiable-areal-unit literature [48]; and Schönbrodt and Perugini's point-of-stability analysis [49, 50]. Simpson's note [52] names the paradox but its setting is categorical contingency tables, so Robinson is the closer analogue.

  **Refusal geometry and dynamics.** Arditi et al. [5] show refusal is mediated by a single direction and introduce the weight edit the abliteration community built on; representation engineering [24], activation addition [25] and contrastive activation addition [26] supply the steering machinery. Qi et al. [27] show aligned and unaligned generative distributions differ mainly over the first few output tokens; Yin et al. [28] trace a probe refusal score across token positions, an observable we adopt rather than coin. Korznikov et al. [29] report random steering raising harmful *compliance* from 0% to 1–13% at an identically calibrated coefficient; §5.6 supplies the matching measurement for the direction they do not test. Our behavioural axes follow AdvBench [1], JailbreakBench [2] and XSTest [34], with judge scoring in the style of [4]; Hasan and Biswas [39] find over-refusal and harmful compliance nearly uncorrelated ($r = -0.032$, $p = 0.89$) across 21 open-weight models, which is why the three axes are predicted separately. The critical-slowing-down programme [30, 31, 32, 33] supplied the indicators for this project's first iteration; that arm is closed and summarised in Appendix A.

  # Preliminaries

  **Panels and the resampling unit.** Three panels appear, and every claim names the one it rests on. The *depth* panel is six Qwen3 [35] checkpoints (0.6B and 1.7B $\times$ base / instruct / abliterated) measured exhaustively \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-2/experiment-1}}. The *read-versus-act* panel is 30 checkpoints over 7 lineages, each measured in both roles of five axes \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-4/experiment-2}}. The *scale* panel is 52 analysed members over 28 weight lineages and 11 architecture families at $\leq$4.2B, drawn from a frozen manifest of 137 verified checkpoints over 93 lineages \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-1/dataset-1}}, and split for diagnostic purposes into the 19 members archived from iteration 2 and the 33 measured afresh. The *lineage* — one pretrained base and everything derived from it — is the resampling and permutation unit for every model-level claim.

  **Aggregation unit.** Because a lineage carries between one and four members, a model-level correlation can be computed two ways. *Member level* means one row per checkpoint with the bootstrap and the permutation clustered on the lineage label; *lineage level* means one row per lineage, each the arithmetic mean over that lineage's defined members of both the score and the outcome. Both are legitimate; they are not interchangeable, and §5.5 measures how far apart they are. Every correlation below is labelled and Table 6 gives both for every score.

  **Prompt sets.** All frozen and shipped : 40 vetted everyday harmless user turns over 10 topics; 594 deduplicated AdvBench/JailbreakBench harmful behaviours with an 80-item stratified core; 400 jailbreak items; XSTest's 250 safe and 200 unsafe items; 256 harmful/benign contrast items reserved for layer selection only (exact overlap 0 with any evaluation set, maximum cosine $0.652$ against a $0.85$ threshold); 200 WikiText fluency passages.

  **The four scores.** All are read from forward passes only. **Logit-gap harmful** is the difference between the maximum logit over a per-tokenizer-family empirical refusal-onset lexicon and the maximum over a continuation lexicon, at the first decoding step, averaged over the frozen 80-item harmful core — 80 forward passes. **Logit-gap benign** is the same quantity on 40 harmless prompts. **Our-AMS $\sigma$** is our reimplementation of [6] — $(\mu_+ - \mu_-)/\sigma_{\text{pooled}}$ on the diff-in-means direction, final prompt token, 40–80% relative-depth sweep, 96 forward passes. **$\alpha_{50}$**, retained only as this project's retired incumbent, is the steering coefficient at which a fresh benign-prompt generation refuses half the time; it costs 265 generations per member.

  The refusal-onset lexicon is *empirical*, derived per tokenizer family from tokens that actually open refusals under greedy decoding, and it is never back-filled across families: five scale-panel members whose family has no lexicon entry receive NULL primary columns with reason `MISSING_FAMILY_LEXICON`, and a clearly labelled union-of-all-families secondary column is reported beside the null rather than substituted for it.

  **Steering axes.** Five axes are fitted per model at the same site on the same benign prompts: **A**, the canonical response contrast between four hand-written canned refusals and four compliances; **B**, a token-disjoint paraphrase axis built from 24 refusal paraphrases containing zero frozen refusal openers; **C**, a norm-matched non-safety stylistic axis (formal versus casual); **D**, matched random unit directions; **E**, the harmful-versus-benign *prompt* contrast. The steering site is $L = \mathrm{round}(0.25\,n_{\text{layers}})$.

  **Axis-contrast units.** The steering hook adds $\alpha\,\mathrm{NORM}_L\,\hat{x}$ to the residual stream, where $\mathrm{NORM}_L$ is the median residual-stream norm at the steering layer. Because raw diff-in-means norms differ up to fourfold between axes, all dose comparisons are reported per *axis-contrast unit* $c = \alpha\,\mathrm{NORM}_L / \lVert X \rVert$, which divides out the axis magnitude and is what settles the magnitude-collapse rival explanation [19]. The conversion was verified exact (absolute error $0.0$) against 459 archived grid cells.

  **The refusal criterion.** A generation counts as a refusal when its opening matches an anchored refusal regex. Because the regex is lexical, §5.3 and §5.4 additionally re-score with a four-class semantic judge and with a five-class rubric carrying an explicit non-canonical-refusal class, and every semantic rate is reported against a control false-positive floor measured on the same filtered population.

  **A tokenisation hazard worth stating.** Re-encoding a prompt and its logged completion by concatenating *strings* lets byte-pair merges cross the boundary; concatenating token *ids* fixes it. The bug is renderer-dependent: on 50 probe items it changes the boundary index on 34/50 under the plain wrapper and 0/50 under a chat template, so it bites base checkpoints specifically. Relatedly, Qwen3 base tokenizers ship a chat template despite never having been tuned to follow one; automatic template selection dropped axis-E reproduction cosine to $0.13$, and forcing the plain wrapper on base models restored all six archived checkpoints to $\geq 0.99992$.

  # Method

  Five instruments, each pre-registered with a sha256 stamp before any statistic existed, with every deviation logged with its trigger and the data state at the time.

  ## Instrument 1: the scale-panel test of the score that won

  The reviewer of our previous draft identified the decisive scoping error: the 52-member panel had been spent replicating the score that *lost* the discrimination matrix, leaving the score that won — the logit-gap harmful margin, the only one whose confidence interval excluded zero at both aggregation units — untested at $n_{\text{lineage}} = 28$. This instrument runs it .

  Four outcomes were pre-registered, verbatim, before any correlation: `HOLDS` requires $\rho \geq 0.50$ **and** a CI excluding zero at *both* units; `HOLDS_AT_MEMBER_UNIT_ONLY` is pre-committed as *not a win* — "this is the same unit-dependence iteration 4 documented and must not be written as one"; `COLLAPSES` converts the paper's claim into a general statement about the score class; `REPLAY_FAILED` halts the analysis entirely. The gate order is enforced by the driver: byte-identity of 17 reused library files, 14 offline apparatus assertions, constant extraction by `ast` (the iteration-3 driver calls `setrlimit` at module scope and cannot be imported), panel and ground-truth identity, a T0-REPLAY reproducing iteration 3's $0.6673$ $[0.439, 0.904]$ / $0.929$ to four decimals, and only then the pre-registration stamp. Ground truth is the archived judged plain-harmful refusal rate, reused rather than re-judged, so LLM spend is $0.00 and the outcome variable cannot drift.

  Three secondary analyses were registered in advance rather than chosen after: the archived-19 versus new-33 block split, which is the diagnostic that localised the paraphrase refit's failure; a partial Spearman controlling for $\log_{10}$ parameter count, because the obvious rival explanation is that any activation score is a capability proxy; and both leave-one-lineage-out and leave-one-family-out jackknives.

  ## Instrument 2: the paraphrase refit at scale

  The AMS paraphrase refit is rerun on the identical 52 members , with four pre-registered outcomes: **R1** $\Delta_A > 0$ with its paired lineage-bootstrap CI excluding zero; **R2** $\rho(\text{refit A}) \geq 0.40$ with its CI excluding zero; **R3** $\Delta_B > 0$ where SET B is an *independently authored* paraphrase set; **R4** permutation $p < 0.05$ and off the floor by an order of magnitude. SET B was generated by a model that is never the judge, at temperature $0.3$, and verified by the *frozen* iteration-3 `check_pair()` with zero hand-written repairs (80/80 strings pass, 78 on the first attempt); measured content-token Jaccard against SET A is $0.201$.

  ## Instrument 3: the read-versus-act re-analysis

  A pure re-analysis of the frozen 30-checkpoint tree, with estimators imported rather than retyped and a 169-leg reproduction gate that passes at $10^{-6}$, with the pooled coefficient and its interval reproducing at the archived seed to $0.0$ . Three repairs are made.

  *The coupling statistic.* The primary estimand becomes the within-axis-A, across-member correlation over the 14 detection-powered members, at both aggregation units, with the lineage-clustered bootstrap and an exhaustive $7! = 5040$ permutation. The pooled 70-pair figure is retained only as a labelled secondary and is decomposed: because the design is a balanced $14 \times 5$, a two-way decomposition of the rank cross-product is *exact and orthogonal*, so the share attributable to axis type is a measurement rather than an argument. A control ladder (drop the two by-construction null axes), a rank-residualised partial correlation, and a mixed-effects slope on ranks are all reported.

  *The verdict rule.* Rather than assert that the rule is asymmetric, we simulate the study's own prompt-clustered percentile bootstrap over a $141$-cell grid of true AUROC $\times$ items per class, 2,000 replicates per cell with 2,000 inner resamples, and report the attainability surface of each verdict. A closed-form Hanley–McNeil check accompanies it. The tally is then reported twice: as shipped over all 30 members, and restricted to the 14 members the pre-registration says the statistic exists on.

  *The abliterated arm.* The structural claim is re-carried on spontaneous refusal *rates*, which involve no AUROC: a two-sided Mann–Whitney U on member-level rates, an exhaustive permutation over all $293{,}930$ group assignments (the arms share one tied rate, so `scipy`'s exact method is invalid here and its value is recorded but never quoted), a lineage-clustered bootstrap of the median difference, and a paired within-lineage sign test.

  ## Instrument 4: breaking the label–axis lexical circularity, and the leakage control

  Axis A is fitted on canned refusals and the detection label is a canned-refusal regex, so part of any shared AUROC is definitional. Instrument 4 re-labels 660 stratified items — stratified by regex label $\times$ stratum $\times$ projection tertile, with the middle tertile double-sampled and inverse-probability weights back to the item population — using the five-class semantic rubric already built for the degeneracy adjudication, loaded verbatim from the archived judge stage [ARTIFACT:art_Y-oGSm04Tcar]. A reproduction gate regenerates 667 archived cells from stored projections at $\max|\Delta| = 0.0$ first.

  The same instrument runs the one published leakage control [44]: four normalisation protocols on identical items and axes — the archived whole-pool centring, fold-internal centring under leave-one-prompt-out, fold-internal centre-and-scale (Mehta's full residualisation), and a deliberately leaky whole-pool z-score — on axes A, B and the norm-matched random axis D, under both label sets. Axis D is the control on the control: a normalisation artifact would move it too. The leakage precondition is re-asserted rather than inherited, with axis-fit strings re-parsed from the archived fitting code and exact text overlap recomputed per member.

  ## Instrument 5: the aggregation-unit repair, the threshold surface, and the claim ledger

  A pure re-analysis over the frozen archives with no GPU and no spend \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-4/evaluation-1}}: an 11-leg reproduction gate, every score recomputed at both aggregation units with the exhaustive permutation held constant, and a 164,736-point full factorial in the falsification battery's five thresholds.

  A second instrument audits the paper's own prose \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-5/evaluation-3}}. Every numeric and verdict-string claim on every number-bearing surface — prose, tables, figure captions, figure summaries, abstract — is resolved against a two-tier pointer index over the shipped JSON (an unfiltered index over 152,118 numeric leaves resolves almost any two-decimal number to *something*, producing false matches, so only 51,178 reportable summary-statistic pointers may resolve a claim). 911 claims over 142 surfaces were audited; the regenerated text re-audits at 150 claims with zero flags, byte-identically across two runs, under a lint forbidding bare numerals and a mutation test confirming the pointers are live.

  # Results

  ## A cheap score that survives a fourfold increase in panel size

  The pre-registered verdict is `HOLDS`, and it is the first positive result in this project . On 52 members over 28 lineages and 11 families, the first-decoding-step logit-gap harmful margin predicts the judged plain-harmful refusal rate at $\rho = 0.694$ $[0.495, 0.822]$ at the member unit with a lineage-clustered bootstrap over 10,000 replicates, and $\rho = 0.564$ $[0.140, 0.826]$ at the lineage-aggregated unit. Both criteria of the pre-registered rule — $\rho \geq 0.50$ and a CI excluding zero — are satisfied at both units. The Monte-Carlo lineage-permutation $p$ sits at the design floor of $5\times10^{-6}$ over 200,000 draws, and we quote the floor beside it rather than a smaller number the design cannot express.

  [FIGURE:fig2]

  | score | fwd passes | generations | $\rho$ member [95% CI] | $\rho$ lineage [95% CI] | perm $p$ (floor) | LOLO range | LOFO range | AUC |
  |---|---|---|---|---|---|---|---|---|
  | logit-gap harmful | 80 | 0 | $0.694$ $[0.495, 0.822]$ | $0.564$ $[0.140, 0.826]$ | $5.0\times10^{-6}$ ($5.0\times10^{-6}$) | $[0.661, 0.726]$ | $[0.650, 0.772]$ | 0.806 |
  | logit-gap harmful, union lexicon | 80 | 0 | $0.579$ $[0.281, 0.746]$ | $0.482$ $[0.086, 0.760]$ | $4.0\times10^{-5}$ | $[0.532, 0.611]$ | $[0.520, 0.724]$ | 0.750 |
  | our-AMS $\sigma$ | 96 | 0 | $0.359$ $[0.047, 0.592]$ | $0.162$ $[-0.314, 0.597]$ | $0.00988$ | $[0.289, 0.389]$ | $[0.289, 0.467]$ | 0.534 |
  | logit-gap benign | 40 | 0 | $0.129$ $[-0.168, 0.436]$ | $0.103$ $[-0.355, 0.499]$ | $0.43631$ | $[0.009, 0.184]$ | $[0.089, 0.177]$ | 0.654 |

  **Table 1.** The scale-panel result: four benchmark-free scores against the judged plain-harmful refusal rate on 52 members / 28 lineages / 11 families, at both aggregation units. All $\rho$ are oriented (higher = safer) using the orientation map extracted from the iteration-3 driver. LOLO = leave-one-lineage-out (28 folds); LOFO = leave-one-family-out (11 folds); both are sign-stable in every fold for every score.

  Four things make this more than a large correlation.

  *It is not the small panel again.* The decisive diagnostic is the one that localised the paraphrase refit's failure, pre-registered here before any correlation: split the panel by provenance and ask whether the effect lives only in the block that produced it. It does not. The 19 archived members give $\rho = 0.6673$ and the 33 newly measured members $\rho = 0.6677$, a paired difference of $-0.0004$ $[-0.308, 0.380]$. The score transfers intact to 21 lineages it was never developed on.

  [FIGURE:fig3]

  *It is not parameter count.* The partial Spearman controlling for $\log_{10}$ parameter count is $0.676$ $[0.475, 0.814]$, essentially unchanged, and the score's own correlation with $\log_{10}$ parameters is $0.092$. The contrast with our-AMS $\sigma$ is instructive: that score correlates with size at $0.458$ and its partial drops from $0.359$ to $0.243$ $[-0.096, 0.507]$, an interval that covers zero. A reader entitled to suspect that any activation-derived score is a capability proxy gets a direct answer for both.

  *It is not one lineage or one family.* Leave-one-lineage-out over 28 folds spans $[0.661, 0.726]$ and leave-one-family-out over 11 folds spans $[0.650, 0.772]$, sign-stable throughout. For comparison, the incumbent $\alpha_{50}$'s jackknife on the seven-lineage panel ranged from $-0.086$ to $0.771$ depending on which single lineage was dropped.

  *It beats the anchor.* Paired on the same resampled lineages, logit-gap harmful minus our-AMS $\sigma$ is $+0.421$ $[0.169, 0.684]$ with $P(\Delta > 0) = 1.000$, verdict `SCORE_BETTER`. Our-AMS $\sigma$ itself reproduces the iteration-4 archived value on 49 of 52 members (maximum $|\Delta| = 0.0275$), and recomputing the 19 archived members from the models leaves the ranks *identical* (Spearman between iteration-3 and iteration-5 margins $= 1.000$, zero rank positions moved), so no Spearman statistic in this section is affected by the small numeric drift on three Llama members.

  **The harmful regime is load-bearing, which is why the product claim is narrowed rather than advertised.** The benign-prompt variant of the identical statistic collapses to $\rho = 0.129$ $[-0.168, 0.436]$, and the paired harmful-versus-benign difference is $+0.565$ $[0.205, 0.873]$. The score therefore reads the margin *on harmful prompts*. It is not harmful-prompt-free. What it removes is everything downstream of the forward pass — no generation, no judge, no benchmark, no reference model — and that sentence ships verbatim in the artifact rather than being written for the paper. The audit cost is 80 forward passes and 0 generations per checkpoint, with a median of 20.0 s (p90 36.7 s, maximum 70.1 s) per member on one RTX A4500 *including model download*; the forward-pass count is the hardware-independent figure and the seconds are not.

  Three plan assumptions were measured false and are recorded as deviations rather than quietly repaired. The five `UNRELIABLE`-flagged members the plan instructed us to exclude *do not exist* anywhere in the iteration-4 archive — neither the per-member table nor any per-member JSON carries such a field, and the string appears only inside verdict prose — so that exclusion set was not invented, and the with/without sensitivity was replaced by the block split and the missing-lexicon sensitivity, which are measurable. 51 of 52 rows carry a pinned revision SHA, not 52. And five members have no empirical refusal-onset lexicon for their tokenizer family; their primary columns are NULL, never back-filled, with the union-of-all-families secondary column ($\rho = 0.579$) reported beside them. Dropping those five leaves the primary $\rho$ at $0.694$ exactly, since they never entered it.

  **What we do and do not claim.** We do not claim the scalar: the first-decoding-step refusal-affirmation margin is Li and Liu's [10], who establish it as a per-prompt safety margin and validate it against their own attack's success rate across suffix strategies, not across models. We do not claim to be first on abliterated checkpoints [45], nor the largest checkpoint panel [14]. What is ours is the conjunction none of them has: a model-level criterion validation of a first-decoding-step margin against a *graded* judged refusal rate, with no attested reference model and no weight access, over 11 architecture families, with inference clustered on the weight lineage — which zero of the five located model-level scores currently use . The closest published attempt at exactly this validation, AMS, reports Pearson $r = -0.546$ ($p = 0.043$) over 14 configurations from 4 families, and its directly comparable rank statistic is $\rho = -0.423$ at $p = 0.13$.

  ## The companion negative: the paraphrase refit does not survive the same panel

  The value of the previous subsection depends on a second score having been run through the identical apparatus and having failed, and one was . Our previous draft's one forward-looking result was that refitting AMS's contrast set on token-disjoint paraphrases lifted its correlation with judged behaviour from $\rho = 0.358$ to $0.654$ on 19 members over 7 lineages. On the same 52 members over 28 lineages it does not replicate.

  At the member level the original scanner reaches $\rho = 0.359$ $[0.047, 0.592]$, the SET A refit $0.458$ $[0.197, 0.646]$, and the independently authored SET B refit $0.207$ $[-0.110, 0.463]$. The paired advantage is $\Delta_A = +0.099$ $[-0.027, 0.244]$ with $P(\Delta_A > 0) = 0.935$, short of the pre-registered interval criterion, so **R1 fails**. $\Delta_B = -0.152$ $[-0.488, 0.075]$: independently authored wording does not merely fail to reproduce the gain, it points the other way, so **R3 fails**. The permutation $p$ is $0.135$ against a floor of $5\times10^{-6}$, so **R4 fails**, and the $1/5040$ floor the original result sat exactly on is retired by the larger panel. Only **R2** passes. The verdict is `DOES_NOT_SURVIVE`, with no salvage and no post-hoc subgroup.

  The location of the failure is what makes it useful. The archived 19-member block reproduces $\Delta_A = +0.2963$ — a gap of $2.6\times10^{-4}$ to the previously published $+0.296$, confirming the reuse is byte-exact rather than merely similar — while the 33 newly measured members give $-0.016$ $[-0.144, 0.130]$. Per block the correlation goes $0.358 \to 0.654$ on the archive and $0.402 \to 0.386$ on the new members. This is not a single-outlier story: leave-one-lineage-out over 28 folds keeps the shrunken $\Delta_A$ in $[0.068, 0.122]$ and leave-one-family-out over 11 folds in $[0.060, 0.137]$, never flipping sign. Three alternative calibration rules give $+0.066$, $+0.152$ and $-0.035$, none rejecting after Holm. The refit still *moves* AMS's PASS/WARN/CRIT verdict class on $12/52 = 0.231$ $[0.137, 0.361]$ of members; it just does not move them toward the truth.

  | score | archived-19 $\rho$ | new-33 $\rho$ | block difference [95% CI] |
  |---|---|---|---|
  | logit-gap harmful | $0.667$ $[0.439, 0.904]$ | $0.668$ $[0.365, 0.851]$ | $-0.0004$ $[-0.308, 0.380]$ |
  | our-AMS $\sigma$ | $0.358$ $[-0.072, 0.709]$ | $0.402$ $[-0.048, 0.679]$ | $-0.044$ $[-0.557, 0.514]$ |
  | AMS paraphrase refit, $\Delta_A$ | $+0.2963$ | $-0.016$ $[-0.144, 0.130]$ | — |

  **Table 2.** The provenance block split, the diagnostic that separates a transferable score from a small-panel artifact. Two scores of nearly identical cost, one panel, opposite outcomes. The refit's entire advantage lives in the 19 members that produced it; the logit-gap margin's does not.

  Read together, §5.1 and §5.2 say something neither says alone. It is not that cheap activation-derived scores are all illusory, which is the conclusion a reader would have drawn from the previous draft; nor that they are all fine. It is that at seven lineages the two are indistinguishable, and at twenty-eight they are not. That is the practical content of the small-sample-instability warning [20], stated in the one currency a practitioner cares about: which of two same-cost scores you would ship.

  ## Reading versus steering: the coupling re-estimated, the verdict rule audited, the label broken

  Our previous draft led §5 with the claim that reading and steering along one refusal axis are positively coupled at $\rho = 0.629$ $[0.465, 0.803]$ over 70 (member, axis) pairs. The reviewer's objection was that the 70 pairs are 14 members $\times$ 5 axes, that axis A is strong in both roles *by construction* and axes C and D null in both roles *by construction*, and that the pooled Spearman therefore measures a between-axis-type contrast. Re-analysis confirms the objection and quantifies it .

  **The primary statistic is now the within-axis, across-member one, and it does not resolve.** Within axis A across the 14 detection-powered members, $\rho = 0.547$ with a lineage-clustered 95% CI of $[-0.031, 0.930]$ over 7 resampling units and an exhaustive $5040$-permutation $p = 0.149$ against an attainable floor of $1.98\times10^{-4}$. Aggregating members within lineage first leaves the sign unchanged at $\rho = 0.821$ $[0.348, 1.000]$. The defensible sentence is therefore: *the axis that induces is also the axis that reads, but among models the two qualities are only weakly and non-significantly related.* That remains a clean reversal of the induce-without-detect dissociation our earlier work claimed; it is not a demonstration of coupling strength, and the previous draft wrote it as one.

  **The confound is measured, not conceded.** Because the design is a balanced $14 \times 5$, a two-way decomposition of the pooled rank cross-product is exact and orthogonal. It attributes $0.896$ of the pooled coefficient to between-axis-type variation, against $0.036$ between members and $0.069$ residual, the three shares summing to $1.000$. Removing the axis main effect by rank-residualisation drops the association to $\rho = 0.234$ $[-0.059, 0.397]$; removing both the axis and the member main effects leaves $0.126$ $[-0.240, 0.366]$; a mixed-effects slope on ranks gives $0.192$ $[-0.075, 0.458]$. The trivial control the reviewer asked for is reported: dropping the two by-construction null axes moves the pooled coefficient from $0.629$ to $0.545$ $[0.284, 0.726]$ over 42 pairs. Within each single axis taken alone the coefficients are A $0.547$, B $0.148$, C $0.397$, D $-0.038$ and E $0.416$ — every one with an interval covering zero. No single axis carries a within-axis coupling on this panel.

  [FIGURE:fig4]

  The reviewer's own recompute over thirteen members is reproduced exactly rather than paraphrased: dropping `Llama-3.2-3B-Instruct`, the one member whose axis-A verdict is `AMBIGUOUS` rather than `READS`, gives $\rho = 0.434$, $p = 0.14$, against this analysis's 14-member $\rho = 0.547$, $p = 0.04$. Both of those $p$-values are the asymptotic Spearman value, which treats the 14 checkpoints as independent; the lineage-clustered interval covers zero at either $n$. The pre-registered verdict is `COUPLING_IS_AXIS_TYPE_CONTRAST` with `UNDERPOWERED` also firing — the within-axis interval's half-width is $0.480$, so at 7 lineages this panel could not have resolved a coupling of the size it estimates even if one is there. Both statements are true at once and the paper carries both. The within-member mean of $0.715$ is demoted rather than defended: it is the mean of 14 coefficients computed over the *same* axis-type contrast on five points each, two of which are controls, so being larger than the pooled figure makes it weaker evidence, not stronger.

  **The verdict rule is $n$-asymmetric, and the Method previously misdescribed the gate.** The reviewer observed that `READS` was issued at 7, 12, 28, 32 and 33 refusals — counts the artifact's own `powered` column marks as not detection-powered — while only members with 0 or 1 refusals returned `UNDEFINED`, which is not the "fewer than 40 refusals" rule the Method described. Both halves are correct and are now fixed at the source. The code path is quoted in the deviation record `DEV-ITER5-01`: `verdict_from_ci` returns `UNDEFINED` if and only if the bootstrap CI bounds are non-finite, which happens because a $\geq$5-per-class resample guard discards enough replicates when one class holds 0–1 items; `MIN_PER_CLASS = 40` governs a *separate* `powered` flag the verdict never consults. The corrected Method sentence appears in §4 above.

  The asymmetry is then quantified rather than asserted, by simulating the study's own prompt-clustered percentile bootstrap over 141 cells at 2,000 replicates each with 2,000 inner resamples. At a true AUROC of $0.500$, `AT_CHANCE` — which requires an entire 95% CI to fit inside the $0.20$-wide band $[0.40, 0.60]$ — is unreachable until $n = 80$ items per class: $P(\text{AT\_CHANCE}) = 0.000$ at the pre-registered $n = 40$ gate, and the Hanley–McNeil closed form puts the i.i.d. threshold at $n = 65$. Under perfect separation `READS` fires with probability $1.000$ at every one of $n = 7, 12, 28, 32, 33$. The asymmetry is *one-sided*, which matters for how the result should be read: the false-`READS` rate at true chance is only $0.005$ at $n = 10$ and $0.001$ at $n = 40$, so `READS` is not noise-driven — it is the *null* verdict that cannot be returned. Every "zero `AT_CHANCE`" sentence in this paper carries that footnote.

  Accordingly the tally is reported twice. Over all 30 members the axis-A verdicts are 20 `READS`, 1 `AMBIGUOUS`, 0 `AT_CHANCE` and 9 `UNDEFINED`; restricted to the 14 detection-powered members they are 13, 1, 0 and 0. Reading is *measurable* — the AUROC and its interval both exist — on 21 members, not 20: the twenty `READS` members plus `Llama-3.2-3B-Instruct`. The minimum axis-A AUROC is $0.685$ over the 21 members with a defined AUROC and $0.691$ over the 20 `READS` members; the bare form "$\geq 0.68$" that appeared in our previous draft belongs to neither population and is retired .

  **The abliterated arm no longer rests on underpowered AUROCs.** The reviewer's sharpest structural point was that the weight-edited arm's five `READS` verdicts rest on counts of 12, 28, 32, 33 and 150, exactly one of which is powered. That is correct, and the claim does not need them. Abliteration removing the refusals to be read rather than the ability to read them is carried instead by spontaneous refusal *rates*, which involve no AUROC: a median of $0.0076$ in the weight-edited arm and $0.0000$ in the behavioural-uncensored candidate arm against $0.1131$ in the aligned reference, over roughly 1,585 generations per member. A two-sided Mann–Whitney U separates the weight-edited arm from the aligned reference ($U = 13.5$, tie-corrected asymptotic $p = 0.0044$, 9 versus 12 members); because the arms share one tied rate, `scipy`'s exact method is invalid here and an exhaustive permutation over all $293{,}930$ group assignments is reported in its place, giving $p = 0.0026$. A lineage-clustered bootstrap of the median difference over 9 lineages gives $-0.1055$ $[-0.2416, -0.0245]$, and over the 10 within-lineage abliterated-versus-parent pairs the abliterated member has the lower rate in 10 of 10 (exact paired sign test $p = 0.0020$, median paired difference $-0.1669$). The four underpowered AUROCs are cited as illustration only.

  | member | arm | $n$ ref / com | spont. refusal rate | powered | axis-A AUROC [95% CI] | verdict |
  |---|---|---|---|---|---|---|
  | `Qwen3-1.7B-Base` | aligned reference | 146 / 146 | 0.1688 | y | $0.918$ $[0.871, 0.957]$ | READS |
  | `Qwen3-1.7B` | aligned reference | 197 / 197 | 0.2277 | y | $0.906$ $[0.859, 0.944]$ | READS |
  | `Qwen2.5-1.5B-Instruct` | aligned reference | 348 / 348 | 0.4023 | y | $0.763$ $[0.709, 0.812]$ | READS |
  | `Llama-3.2-1B-Instruct` | aligned reference | 172 / 172 | 0.1988 | y | $0.691$ $[0.603, 0.773]$ | READS |
  | `Llama-3.2-3B-Instruct` | aligned reference | 282 / 282 | 0.3260 | y | $0.685$ $[0.597, 0.763]$ | AMBIGUOUS |
  | `Llama-3.2-3B-Instruct-abliterated` | weight-edited abliteration | 150 / 150 | 0.1734 | y | $0.718$ $[0.628, 0.802]$ | READS |
  | `Josiefied-Qwen3-4B-...-gabliterated-v2` | weight-edited abliteration | 32 / 32 | 0.0202 | N | $0.998$ $[0.989, 1.000]$ | READS |
  | `Josiefied-Qwen2.5-3B-...-abliterated-v1` | weight-edited abliteration | 12 / 12 | 0.0076 | N | $0.889$ $[0.688, 1.000]$ | READS |
  | `Qwen3-0.6B-abliterated` | weight-edited abliteration | 0 / 1572 | 0.0000 | N | — | UNDEFINED |
  | `Huihui-Qwen3-1.7B-abliterated-v2` | weight-edited abliteration | 0 / 1574 | 0.0000 | N | — | UNDEFINED |
  | `TinyLlama-1.1B-Chat-v1.0` | aligned reference | 7 / 7 | 0.0044 | N | $1.000$ $[1.000, 1.000]$ | READS |
  | `Mia-001` | behavioural-uncensored candidate | 0 / 1242 | 0.0000 | N | — | UNDEFINED |

  **Table 3.** Twelve of the thirty per-member detection rows, chosen to show the whole operating range; the full 30-row table with norm-controlled readouts ships with the artifact. The two columns the previous draft omitted — refusal/compliance counts and the `powered` flag — are what let a reader see that `TinyLlama-1.1B-Chat-v1.0` reads at AUROC $1.000$ on seven items and that the entire weight-edited arm has one powered member. Panel totals: 14 powered of 30; 20 READS, 1 AMBIGUOUS, 0 AT_CHANCE, 9 UNDEFINED.

  **The label and the axis share a lexical basis, and the AUROC mostly survives it.** Axis A is the diff-in-means of hand-written canned refusals against canned compliances, and the label of record is an anchored regex over canned-refusal openers, so part of any shared AUROC is definitional. We measure it [ARTIFACT:art_Y-oGSm04Tcar]. Re-labelling 660 stratified items with the five-class semantic rubric moves the pooled axis-A AUROC from $0.834$ $[0.736, 0.923]$ under the regex label to $0.821$ $[0.752, 0.866]$ under the semantic one — a paired difference of $-0.013$ $[-0.067, +0.030]$ at the member level and $-0.024$ $[-0.066, +0.018]$ at the lineage level, with the two criteria agreeing at Cohen's $\kappa = +0.789$ $[+0.699, +0.879]$.

  The deciding split is not the swap but the stratum. On canonically-worded refusals the axis separates at $0.897$ $[0.864, 0.922]$; on the genuine refusals the regex misses (`REFUSAL_NONCANONICAL`) it reaches only $0.611$ $[0.542, 0.686]$, which does not clear these members' own 20-draw random reading band, whose upper edge averages $0.750$. The pre-registered verdict is `READS_CANONICAL_WORDING_ONLY` at both units. A caveat we did not expect and must carry: the rubric's canonical/non-canonical split is *not* the regex's split — 54 of 267 items (20.2%) that open with a frozen refusal opener are still called `REFUSAL_NONCANONICAL` by the judge, and the drift is member-dependent (0/27 on `Qwen3-1.7B-Base`, 17/25 on `Llama-3.2-3B-Instruct`). Taking the rubric class as "refusals the regex missed" over-counts 83 against 38. On the sharper subset — semantic refusal *and* regex non-refusal — the pre-registered floor of 40 is not met at $n = 38$, so the reportable claim is the pre-registered fallback: weighted corpus prevalence $0.0546$ $[0.0412, 0.0686]$, roughly one scored item in eighteen is a refusal the regex of record calls a compliance.

  [FIGURE:fig5]

  **The one published leakage control, run on our own headline.** Our thesis is that the item pool decides the result, and the single published control that tests exactly this had not been applied to the analysis it would test. It has now. Re-estimating every centring and scaling statistic inside the training fold under leave-one-prompt-out moves axis-A AUROC by $-0.0205$ $[-0.0352, -0.0071]$ (centring alone: $+0.0009$; the deliberately leaky whole-pool z-score: $-0.0205$), and $-0.0397$ $[-0.0763, -0.0047]$ under semantic labels — an order of magnitude short of the $-0.336$ the same control produced on its author's own data [44]. The control on the control holds: the identical protocol moves the norm-matched random axis D by only $-0.0020$ $[-0.0084, +0.0032]$ and axis B by $-0.0023$, so the axis-A movement is not pure normalisation. Zero fallback folds occurred anywhere, and text overlap between the scored items and the axis-fit strings is exactly zero on every member, re-asserted here rather than inherited. Verdict: `LEAKAGE_CONTROL_SMALL_DELTA`.

  ## The canonical axis beats its paraphrase on semantics, not only on lexicon

  An earlier draft of this work adjudicated rather than measured a semantic partial reversal: under a four-class judge the token-disjoint paraphrase axis B crossed a $0.50$ refusal rate on every checkpoint, and we set that aside on the grounds that B's high-coefficient text is degenerate. Filtering to text that passes the archived fluency screen *before* judging, and reporting every rate against a control floor measured on the same filtered population, replaces the argument with an estimate [ARTIFACT:art_P-_YL8tdIwqF].

  At matched axis-contrast units — axis A's own 50%-refusal coefficient — the five-class any-refusal rate is $0.028$ $[0.008, 0.057]$ for axis B against $0.747$ $[0.618, 0.858]$ for axis A, with the false-positive floor at $0.146$ set by the *random* axis D. The net quantity $B - \text{floor}$ is $-0.118$ $[-0.157, -0.082]$ (paired prompt-clustered bootstrap, 5,000 replicates, $n = 600$ per axis): B sits below what a meaningless direction induces on the same population. The verdict is `REVERSAL_DOES_NOT_SURVIVE`, on 6 of 6 checkpoints and pooled.

  [FIGURE:fig6]

  Three sub-measurements make this an estimate rather than an argument, and each cuts against something previously written. At matched contrast the lexical screen removes *nothing* — retention is $1.000$ for both A and B — so B's near-zero rate there is an absence of effect, not a filtering artifact, which inverts our earlier degeneracy story at the level that matters. At B's own maximum coefficient ($\approx 15$ contrast units) retention does fall to $0.705$, but $70.2\%$ of the text that *passes* the screen is still judge-`DEGENERATE`, against $71.1\%$ unfiltered: the lexical screen removes essentially none of the residual degeneracy, because the failure is semantic and the screen is lexical. And the control floor is itself made of screen-passing degenerate text — $59.0\%$ of the random axis's matched-cell survivors are judge-`DEGENERATE` — which is precisely why a semantic rate reported without a same-population floor is uninterpretable.

  One pre-registered level splits the verdict, and it is the section's nuance rather than a hedge. At B's own peak refusal coefficient ($5.21$ contrast units, about $4.3\times$ the intervention A needs) B *does* clear the floor on fluent text: $0.642$ against a floor of $0.077$, net $+0.565$ $[+0.471, +0.655]$, with only $4.9\%$ `DEGENERATE`. B's apparent reversal is real, but lives entirely at coefficients that matching forbids — which is what matching was introduced to detect. The Rogan–Gladen correction is reported throughout and is uninformative at the matched level by construction: both B's rate and the floor fall below $1 - \text{specificity} = 0.196$, so both corrected prevalences truncate at zero and the corrected net is exactly $0$ by construction rather than by measurement, which the artifact flags rather than quoting.

  | axis | $n$ | anchored regex | four-class judge | five-class any-refusal | five-class non-canonical | five-class degenerate |
  |---|---|---|---|---|---|---|
  | A (canonical) | 600 | 0.470 | 0.763 | 0.747 | 0.142 | 0.005 |
  | B (token-disjoint paraphrase) | 600 | 0.002 | 0.043 | 0.028 | 0.018 | 0.002 |
  | C (stylistic control) | 600 | 0.000 | 0.050 | 0.017 | 0.017 | 0.007 |
  | D (random control) | 575 | 0.002 | 0.374 | 0.146 | 0.139 | 0.590 |

  **Table 4.** Refusal rates on fluency-screened text at matched axis-contrast units, three scoring criteria side by side, pooled over the six depth-panel checkpoints. The random control's four-class rate of $0.374$ against its five-class degenerate rate of $0.590$ is the false-positive floor any semantic steering claim has to clear. Criterion agreement is poor where it matters: Cohen's $\kappa$ between the regex and the five-class rubric is $0.424$ on A, $0.108$ on B and $0.020$ on D.

  Across all 30 read-versus-act checkpoints, matched contrast returns `NORM_MISMATCH_DOES_NOT_EXPLAIN` on 22, which rules out Petrov's magnitude-collapse account [19] on a panel five times the size of the previous test. On the two breadth-panel members that carried the objection that axis B does reach a $0.50$ refusal rate, re-measurement at matched contrast finds 1 of 2 a genuine inducer (`Llama-3.2-1B-Instruct`) and 1 a norm artifact.

  ## The aggregation unit, and a negative that is robust to its own thresholds

  The most damaging defect a reader could have found in an earlier draft was internal: our AMS reimplementation's correlation with judged behaviour appeared as $0.358$ in one section and $0.821$ in another, with a headline $\Delta$ computed from the second. Both numbers are correct and neither was labelled . At the **member level** — 19 checkpoints, resampled and permuted on the lineage label — the statistic is $\rho = 0.358$ $[-0.074, 0.699]$ with exhaustive permutation $p = 0.0911$. At the **lineage level** — 7 units, each the mean over that lineage's defined members of both score and outcome — the same statistic is $\rho = 0.821$. The gap of $0.464$ is what lineage aggregation buys by removing within-lineage variance and reducing $n$ from 19 to 7.

  That is not a bookkeeping repair, because the choice moves conclusions. Over the 16 score $\times$ configuration cells where both units are defined, changing nothing but the unit moves oriented $\rho$ by a median $0.238$ and a maximum $0.557$, and **flips the sign on 5**. The headline comparison inherits exactly that instability: on the carrier an earlier draft used, the oriented $\Delta = \rho(\alpha_{50}) - \rho(\text{our-AMS})$ is $-0.929$ $[-1.961, -0.113]$ at the lineage level and $-0.376$ $[-0.795, 0.110]$ at the member level — `SIGN_SURVIVES` but `EXCLUSION_LOST_AT_MEMBER_LEVEL`; on the discrimination matrix's own carrier it gives $-0.566$ member and $+0.107$ lineage — `SIGN_FLIPS`, `EXCLUDES_AT_NEITHER`. The correct statement is that $\alpha_{50}$ loses to a cheaper activation scanner under every unit and carrier we can compute, and that no interval-based version of that claim survives both units. §5.1's headline is reported at both units for the same reason, and it is one of the few rows in this study that clears zero at both.

  | score | member-level $\rho$ | 95% CI | lineage-level $\rho$ | 95% CI | CI excludes 0 |
  |---|---|---|---|---|---|
  | $\alpha_{50}$ (max refusal rate), 19/7 | $-0.208$ | $[-0.547, 0.175]$ | $+0.321$ | $[-0.887, 0.870]$ | neither |
  | our-AMS $\sigma$, 19/7 | $0.358$ | $[-0.074, 0.699]$ | $0.214$ | $[-0.765, 0.961]$ | neither |
  | our-AMS $\sigma$, paraphrase refit, 19/7 | $0.654$ | $[0.276, 0.859]$ | $0.643$ | $[-0.192, 1.000]$ | member only |
  | logit-gap (benign), 19/7 | $0.101$ | $[-0.243, 0.573]$ | $0.286$ | $[-1.000, 0.765]$ | neither |
  | logit-gap (harmful), 19/7 | $0.667$ | $[0.439, 0.904]$ | $0.929$ | $[0.412, 1.000]$ | **both** |
  | our-AMS $\sigma$, scale panel 52/28 | $0.359$ | $[0.047, 0.592]$ | $0.162$ | $[-0.314, 0.597]$ | member only |
  | our-AMS refit A, scale panel 52/28 | $0.458$ | $[0.197, 0.646]$ | $0.224$ | $[-0.229, 0.620]$ | member only |
  | our-AMS refit B, scale panel 52/28 | $0.207$ | $[-0.110, 0.463]$ | $0.013$ | $[-0.442, 0.453]$ | neither |
  | logit-gap (benign), scale panel 52/28 | $0.129$ | $[-0.168, 0.436]$ | $0.103$ | $[-0.355, 0.499]$ | neither |
  | **logit-gap (harmful), scale panel 52/28** | $\mathbf{0.694}$ | $[0.495, 0.822]$ | $\mathbf{0.564}$ | $[0.140, 0.826]$ | **both** |

  **Table 5.** Every score against the judged plain-harmful refusal rate at **both** aggregation units. Rows 1–5 are the 19-member / 7-lineage panel with the exhaustive $7!$ permutation null in both units; rows 6–10 are the 52-member / 28-lineage scale panel with a Monte-Carlo null over 200,000 draws. The logit-gap harmful margin is the only score that excludes zero at both units on both panels.

  With units named, the discrimination matrix stands unchanged and its negative is now robust to its own thresholds.

  | score | primary column | C1 lexical | C2 monotone | C3 depth | C4 jackknife | C5 scorer | passes | oriented $\rho$ (member) | 95% CI | perm $p$ | fwd passes | generations |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | $\alpha_{50}$ | max refusal rate | FAIL | FAIL | PASS | PASS | FAIL | 2/5 | $-0.208$ | $[-0.545, 0.183]$ | 0.3087 | 0 | 265 |
  | our-AMS $\sigma$ | ams_sigma | FAIL | FAIL | PASS | PASS | FAIL | 2/5 | $0.358$ | $[-0.072, 0.709]$ | 0.0911 | 96 | 0 |
  | logit-gap (benign) | logit_gap_benign | FAIL | FAIL | FAIL | FAIL | FAIL | 0/5 | $0.101$ | $[-0.243, 0.569]$ | 0.6621 | 40 | 0 |
  | logit-gap (harmful) | logit_gap_harmful | FAIL | FAIL | FAIL | PASS | FAIL | 1/5 | $0.667$ | $[0.439, 0.904]$ | 0.0038 | 80 | 0 |

  **Table 6.** The discrimination matrix: four cheap benchmark-free safety scores $\times$ five falsification checks, on the frozen 19-member / 7-lineage panel, all correlations at the **member level** with the lineage as the resampling and permutation unit (exhaustive $7! = 5040$; achievable floor $1.98\times10^{-4}$). Verdict: `PROTOCOL_DOES_NOT_DISCRIMINATE`. Check 5 is a property of the shared scorer (REFUSAL $\kappa = 0.391$ against a $0.60$ threshold), so it fails identically in every row and caps every row at 4/5.

  The load-bearing observation is unchanged, and §5.1 sharpens it into something more uncomfortable than we could previously say: the score that predicts judged behaviour *best* passes the *fewest* checks, and it is now also the score that survives a fourfold panel increase while the score the checks favoured does not. Construct hygiene and predictive validity are close to orthogonal on this panel, and the checks pointed the wrong way. What is new is that the negative no longer depends on five arbitrary cutoffs. Over a 164,736-point full factorial in the five thresholds, `PROTOCOL_DOES_NOT_DISCRIMINATE` holds on a fraction $1.0000$ of grid points, and on $0.9091$ under the stricter criterion that a rival must *strictly exceed* $\alpha_{50}$'s pass count. Exactly one single-axis change anywhere on the grid produces a strict rival win: lowering check 3's depth-span threshold from $2.0$ to $1.75$. Check 5 cannot contribute at all, because its $\kappa$ of $0.391$ lies below the entire swept range $[0.40, 0.80]$ — proved structurally and verified empirically. Dropping the pass rules' secondary clauses and scoring the numeric cutoffs alone lowers stability to $0.5802$ and $0.2429$, which locates the negative precisely: it is carried by the verdict-class and interiority clauses, not by the numbers.

  ## Two empirical nulls that steering studies should adopt

  The 30-checkpoint study was designed to test axes, and it produced two facts about *controls* that generalise beyond this paper .

  First, a random direction is not behaviourally inert at the magnitude at which a refusal axis works. Injected at axis A's own matched magnitude, a matched random unit direction induces refusal at a maximum rate of at least $0.10$ on 7 of 30 members, with a worst case of $0.389$ and a panel median of $0.028$. Korznikov et al. [29] report the complementary effect — random steering raising harmful *compliance* to 1–13% at an identically calibrated coefficient — and never test random-induced refusal on benign prompts; this is that measurement, and it says the induction floor is a real quantity that steering claims must clear. Our own earlier random-direction null ($0.00$–$0.058$) was measured on six checkpoints and does not generalise to 30.

  Second, a random direction does not *read* at $0.500$. The empirical band of AUROCs over 20 random draws per member spans $\pm0.075$ to $\pm0.500$ across members, because residual streams are anisotropic, so a gate written against the textbook $0.500$ is wrong by a wide and model-dependent margin. A single random draw is not a null distribution. Relatedly, a raw projection is $\lVert h\rVert\cos\theta$, so any direction inherits whatever refusal-versus-compliance *norm* difference the model has — one random axis "reads" at $0.171$ on a member for that reason alone — which is why every AUROC in §5.3 is reported both raw and norm-controlled, and why the two agree to within $0.011$ on the canonical axis.

  # Discussion

  **What a platform could do with this.** The practical output of five iterations is one score and one protocol for trusting it. The score is 80 forward passes on a frozen 80-item harmful core, no generation, no judge, no benchmark, no reference model, roughly 20 s per checkpoint including download at $\leq$4B; it ranks checkpoints by judged harmful-refusal rate at $\rho \approx 0.69$ across 28 lineages and 11 families. It is a triage instrument, not a certificate: $\rho = 0.69$ leaves ample room for individual checkpoints to be mis-ranked, and the score reads harmful prompts, so an operator still has to hold 80 harmful strings — they just never generate from them, never send them to a judge, and never need a reference model. Against the honest alternative — a few hundred generations plus a judge per checkpoint — that is roughly three orders of magnitude cheaper per model and removes the one operational requirement (an attested reference) that the published abliteration audit needs [14].

  **Three named pathologies, and the instances we claim.** Three of this paper's surviving results are measured instances of long-named methodological phenomena rather than new phenomena, and presenting them as discoveries would invite the correct objection . We name each and claim only the instance.

  *Item-pool provenance is leakage.* Kapoor and Narayanan's taxonomy names our case directly as [L3.3] *sampling bias in test distribution* — "choosing a non-representative subset of the dataset for evaluation ... the test set is no longer representative of the general population about which claims are made" — with [L1.2] covering the statistics-estimated-on-everything half [46]. We claim the measured instance: on the six depth-panel checkpoints the *same* refusal axis moves from AUROC $0.486$–$0.790$ when scored on an archived pool containing steered text to $0.906$–$0.980$ when scored on each model's own spontaneous text, with induction unchanged, so a read-versus-act conclusion was decided entirely by which items the score was evaluated on. The field-local precedent is exact: Mehta's probe falls from $0.761$ to $0.43$ under leave-one-query-out with per-fold residualisation and scores $0.63$ on a control condition where the effect cannot exist [44].

  *The aggregation unit is ecological correlation.* Robinson showed in 1950 that the same relationship computed at different levels of aggregation need not agree in sign: nativity against illiteracy is $+.118$ individually, $-.526$ over 48 states and $-.619$ over 9 divisions [47]. Openshaw's modifiable-areal-unit literature separates the scale problem from the aggregation problem and reports that for a six-zone aggregation of 99 Iowa counties "the range of possible correlations is between $-.99$ and $+.99$" [48]. Simpson's note [52] names the paradox but its setting is categorical contingency tables, so Robinson is the closer analogue. We do not claim aggregation bias as a finding; we claim a measured instance in which it moves this study's own headline by $0.464$ and flips 5 of 16 signs.

  *The $7\to28$ collapse is small-sample correlation instability, and we are still below stability.* Schönbrodt and Perugini define the point of stability and conclude that "in typical scenarios the sample size should approach 250 for stable estimates"; their Table 1 puts the critical $n$ at $252$, $238$, $212$ and $181$ for true $\rho$ of $.1$–$.4$ even at the most permissive corridor they report [49, 50]. We claim the instance against ourselves: quadrupling the panel from 7 to 28 lineages moves our own previously published $\Delta_A$ from $+0.296$ to $+0.099$ with an interval covering zero, localised so that the archived block reproduces to $2.6\times10^{-4}$ while the new members give $-0.016$. And we state the uncomfortable corollary deliberately: $n = 28$ is still six to nine times below the point of stability for this effect-size band, so §5.1's $\rho = 0.694$ is a direction of travel under a fourfold increase, not a settled value. The reference class this belongs to is small: of five published model-level internal safety scores, none resamples on the weight lineage and none exceeds four architecture families.

  **Why a validity battery can be right and useless at once.** The battery's cells each report a true property. What it cannot do is rank scores, because on this panel construct hygiene and predictive validity are close to orthogonal — the logit-gap harmful margin is at once the most predictive score, the least hygienic, and the only one that survives at 28 lineages. Had we ranked by the checks, we would have shipped the paraphrase refit and discarded the score that works. That is a stronger statement than the previous draft's, which could only say the checks failed to discriminate; it now says they discriminated, in the wrong direction, on the one question a user cares about.

  **Limitations.** (1) Scale: everything is measured at 0.13B–4.2B, and the within-family scale ladder runs only to 4B; nothing here licenses extrapolation to frontier checkpoints. (2) $n = 28$ lineages remains far below the point of stability (above), and the lineage-level interval on the headline, $[0.140, 0.826]$, is wide. (3) The score is not harmful-prompt-free, and the benign variant collapses to $0.129$; any claim that this is a content-free audit is false. (4) The read-versus-act coupling is unresolved: $0.547$ with a CI covering zero on 14 powered members from 7 lineages, and the members it is missing are systematically the ones with no refusals, so the estimate is conditioned on a model refusing sometimes. (5) The refusal axis reads canonically-worded refusals at $0.897$ and non-canonical ones at $0.611$, within the random reading band, so "the axis reads refusals" is true only of the wording it was fitted on. (6) Nothing here distinguishes an abliterated checkpoint whose axis has been destroyed from one whose refusals have merely been suppressed, because the detection statistic requires refusals. (7) Our AMS reimplementation misses the published Table I by $-6\%$, $+22\%$ and $-40\%$ on the three overlapping checkpoints, so every AMS comparison bounds *our reimplementation*; RAS and VISAGE were not run, for the checkpoint-overlap and cost reasons in §2. (8) Behavioural rates are judge-derived with a REFUSAL one-versus-rest annotator $\kappa$ of $0.391$, and our annotators are LLM agents, so every accuracy bounds agreement with an LLM panel rather than truth; disattenuated correlations are reported alongside raw ones, never instead. (9) Our fixed-lexicon maximum margin is a different estimand from Li and Liu's per-prompt highest-logit affirmative token [10], and five members' tokenizer families have no empirical lexicon at all. (10) Everything steered is a statement about the steered dynamical system, which is provably not prompt-reachable [38].

  **What we would do next.** Three things follow, in cost order. Extend the panel toward the point of stability — the score costs 80 forward passes, so 250 lineages is a weekend of compute rather than a research programme, and it is the only way to convert a direction of travel into a value. Test whether the margin can be gamed: it is read at one token position from a fixed lexicon, which is exactly the surface a fine-tune could be tuned against, and the honest version of a triage score has to survive an adversary who knows it. And pair the refusal axis with a harm-intent axis [45] on the same abliterated checkpoints, since their axis survives abliteration to within $0.015$ AUROC while the refusal channel goes silent; a two-axis signature — harm geometry intact, refusal channel dead — would be strictly more informative than either alone and would not need the attested reference the published abliteration audit presumes [14].

  # Conclusion

  We set out to build a safety score that costs seconds per checkpoint and touches no harmful text. The second half is not achievable by any route we found; the first half is. On 52 checkpoints over 28 weight lineages and 11 architecture families, a first-decoding-step logit-gap margin costing 80 forward passes, zero generations, zero judge calls and no reference model predicts the judged plain-harmful refusal rate at $\rho = 0.694$ $[0.495, 0.822]$ at the member unit and $0.564$ $[0.140, 0.826]$ at the lineage unit, transfers between provenance blocks at $0.667$ versus $0.668$, survives a partial correlation on parameter count at $0.676$, and beats our reimplementation of the closest published activation scanner by $+0.421$ $[0.169, 0.684]$. It reads harmful prompts, so what it saves is generation, judging, benchmarking and the reference model — not the harmful content itself.

  The same panel retires the alternatives. The lexical-invariance refit of that scanner improves criterion validity by $+0.296$ on 7 lineages and by $+0.099$ $[-0.027, 0.244]$ on 28, with the archived block reproducing to $2.6\times10^{-4}$ and the 33 new members contributing $-0.016$. The act-side score this project began with, $\alpha_{50}$, loses to a cheaper forward-pass scanner under every unit and carrier we can compute. The five-check battery built to explain that failure not only fails to rank scores but ranks them backwards: it favoured the refit that collapsed and penalised the margin that held.

  What is left is a score a platform could run tomorrow, and a measurement discipline that is the reason to believe it: three named pathologies — leakage through item-pool provenance, ecological correlation through the aggregation unit, and small-sample instability through panel size — each quantified on this project's own previously published numbers, with the effect localised to the block that produced it. The reference class this score joins validates at four or fewer architecture families and never resamples on the weight lineage. On that evidence the useful claim is not that we found the right scalar; Li and Liu defined it. It is that the difference between a cheap safety score that works and one that does not is invisible at seven lineages and legible at twenty-eight — and that twenty-eight is still not enough.

  # Appendix A: Corrections of Record

  Twenty-six claims from earlier iterations are restated in the shipped artifacts rather than in the sections that first made them, each with the claim as previously stated, the corrected statement, the archived file and key it derives from, and why it moved \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/tree/main/round-3/evaluation-2}}. The substantive items new to this iteration are: the read-versus-act coupling coefficient, demoted from a pooled $0.629$ to a within-axis $0.547$ with an interval covering zero, with the $0.896$ between-axis-type variance share as the reason; the Method's description of the `UNDEFINED` detection gate, which fires on a non-finite bootstrap interval at $\leq 1$ refusal and not at the "fewer than 40 refusals" rule the Method stated, logged as deviation `DEV-ITER5-01` with the three code paths quoted; the axis-A verdict tally, now reported twice (20/1/0/9 over 30 members; 13/1/0/0 over the 14 powered ones) with an attainability footnote establishing that `AT_CHANCE` is unreachable below $n = 80$ per class; the reading claim, narrowed to `READS_CANONICAL_WORDING_ONLY` ($0.897$ canonical versus $0.611$ non-canonical against a random band edge of $0.750$); the abliterated-arm claim, re-carried on refusal rates rather than on four underpowered AUROCs; the minimum axis-A AUROC, which is $0.685$ over the 21 members with a defined AUROC and $0.691$ over the 20 `READS` members, with the bare "$\geq 0.68$" retired; the count of members on which reading is measurable, which is 21 and not 20; a stale top-line summary of 18 `READS` / 0 `AT_CHANCE` / 10 `UNDEFINED`, diagnosed exactly as an intermediate log state with the `AMBIGUOUS` class dropped, which is why it sums to 28; and reference [11], completed to its full eight-author list. Carried forward unchanged: the AMS paraphrase refit (`DOES_NOT_SURVIVE`); the semantic-reversal adjudication (`REVERSAL_DOES_NOT_SURVIVE` at matched contrast, `REVERSAL_SURVIVES` at B's unmatched peak); the archived relative depth of $0.25$; the random-direction null, rescoped to a measured induction floor reaching $0.389$ on 30 checkpoints; the early-warning-signal arm, closed with a direction-specific difference-in-differences of $-2.334$ $[-3.573, -1.037]$ that fails Holm within its 48-test family and would need on the order of 1,880 prompts; the observable-validity gate, which admits 0 model pairs at the layer-$L$ readout and 1 at the final-layer readout; the relaxation-rate claim, withdrawn as non-identifiable on 640 of 640 rows; the $\alpha_{50}$ accounting, where the primary logistic estimator is `DEFINED` on 1 of 19 members and that member is itself excluded; and nine bibliographic corrections against the arXiv API, including reference [45], whose title is *The Geometry of Harmful Intent*.

  # References

  [1] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043, 2023.

  [2] P. Chao, E. Debenedetti, A. Robey, M. Andriushchenko, F. Croce, V. Sehwag, E. Dobriban, N. Flammarion, G. J. Pappas, F. Tramèr, H. Hassani, and E. Wong. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024.

  [3] M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, E. Sakhaee, N. Li, S. Basart, B. Li, D. Forsyth, and D. Hendrycks. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024.

  [4] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023.

  [5] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024.

  [6] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

  [7] C. Huang, Y. Chen, C. Yu, and W. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. arXiv:2606.25750, 2026.

  [8] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024.

  [9] A. Borah, S. Sarkar, R. Aditya, R. Anand, S. Kumar, A. Chadha, and A. Das. Alignment Quality Index (AQI): Beyond Refusals — AQI as an Intrinsic Alignment Diagnostic via Latent Geometry, Cluster Divergence, and Layer-wise Pooled Representations. *EMNLP*, 2025. arXiv:2506.13901.

  [10] T.-L. Li and H. Liu. Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness. arXiv:2506.24056, 2025.

  [11] S. Basu, S. Y. Patel, P. Sheth, B. Muralidharan, N. Elamaran, A. Kinra, J. Morgan, and R. Batniji. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. arXiv:2603.18353, 2026.

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

  [46] S. Kapoor and A. Narayanan. Leakage and the Reproducibility Crisis in Machine-Learning-Based Science. *Patterns*, 4(9):100804, 2023.

  [47] W. S. Robinson. Ecological Correlations and the Behavior of Individuals. *American Sociological Review*, 15(3):351–357, 1950.

  [48] S. Openshaw. *The Modifiable Areal Unit Problem*. Concepts and Techniques in Modern Geography (CATMOG) 38, Geo Books, Norwich, 1984.

  [49] F. D. Schönbrodt and M. Perugini. At What Sample Size Do Correlations Stabilize? *Journal of Research in Personality*, 47(5):609–612, 2013.

  [50] F. D. Schönbrodt and M. Perugini. Corrigendum to "At What Sample Size Do Correlations Stabilize?" *Journal of Research in Personality*, 74:194, 2018.

  [51] Z. Xu and V. S. Sheng. A Behavioral Fingerprint for Large Language Models: Provenance Tracking via Refusal Vectors. arXiv:2602.09434, 2026.

  [52] E. H. Simpson. The Interpretation of Interaction in Contingency Tables. *Journal of the Royal Statistical Society: Series B (Methodological)*, 13(2):238–241, 1951.
summary: >-
  On a frozen panel of 52 open-weight checkpoints spanning 28 weight lineages and 11 architecture families, the first-decoding-step
  logit-gap margin -- 80 forward passes, no generation, no judge, no benchmark and no reference model -- predicts judged plain-harmful
  refusal rate at Spearman rho = 0.694 [0.495, 0.822] (member unit) and 0.564 [0.140, 0.826] (lineage unit), transfers across
  provenance blocks (0.667 vs 0.668), is not a parameter-count proxy (partial 0.676), and beats a reimplemented activation
  scanner by +0.421 [0.169, 0.684]. The same panel retracts two of the authors' earlier positives: an AMS paraphrase refit
  collapses from +0.296 at 7 lineages to +0.099 [-0.027, 0.244] at 28 with the effect localised to the original block, and
  a claimed read-versus-act coupling of 0.629 is shown by an exact variance decomposition to be 89.6% a between-axis-type
  contrast (within-axis 0.547, CI covering zero). The paper additionally quantifies an n-asymmetric verdict rule, breaks a
  label-axis lexical circularity (READS_CANONICAL_WORDING_ONLY), runs the one published leakage control on its own headline
  (-0.0205), and names the three measurement pathologies involved as instances rather than discoveries.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
figure_type: concept
title: Two ways to score a checkpoint's safety
caption: >-
  The audit this paper validates, against the audit it replaces. The benchmark path (top) requires holding harmful prompts,
  generating from them, and paying a judge, per checkpoint. The forward-pass path (bottom) reads the refusal-versus-affirmation
  logit margin at the first decoding step over a frozen 80-item harmful core: 80 forward passes, no generation, no judge,
  no benchmark run and no reference model. Validation is where the contribution lies: the resampling unit is the weight lineage,
  not the checkpoint.
image_gen_detailed_description: >-
  Horizontal two-lane flow diagram, left to right, clean sans-serif, white background, no 3D. TOP LANE labelled 'Benchmark
  audit (what it replaces)' in muted grey-red: five boxes connected by right arrows -- 'Harmful prompt set (AdvBench / JailbreakBench)'
  (grey), 'Generate ~300 completions' (grey), 'LLM judge scores each' (grey), 'Refusal rate' (grey), 'Cost: hundreds of generations
  + judge spend per checkpoint' as a small annotation box in red-grey. BOTTOM LANE labelled 'Forward-pass audit (this paper)'
  in blue-green: five boxes -- 'Frozen 80-item harmful core' (light blue), 'One forward pass per prompt' (blue), 'First-decoding-step
  logits' (blue), 'margin = max logit(refusal-onset tokens) - max logit(continuation tokens)' shown as a wide formula box
  (dark blue), 'Model-level score: mean over 80 prompts' (green). Annotation box under the bottom lane in green: '80 forward
  passes, 0 generations, 0 judge calls, 0 reference models; median 20.0 s per checkpoint'. To the RIGHT of both lanes, a single
  tall validation box in orange, receiving an arrow from the green box, labelled 'Validation: 52 checkpoints / 28 weight lineages
  / 11 families; bootstrap and permutation clustered on the LINEAGE' with three bullet lines inside: 'rho = 0.694 [0.495,
  0.822] (member unit)', 'rho = 0.564 [0.140, 0.826] (lineage unit)', 'archived-19 0.667 vs new-33 0.668'. A small grey caveat
  strip along the bottom edge spanning the whole figure: 'The margin is read ON HARMFUL PROMPTS - not harmful-prompt-free.'
  Do not draw model internals or transformer blocks.
aspect_ratio: '21:9'
summary: >-
  Hero diagram contrasting the benchmark audit with the 80-forward-pass logit-gap audit, and naming the lineage-clustered
  validation panel.
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
figure_type: data
title: Which cheap score predicts behaviour at 28 lineages
caption: >-
  Spearman correlation of four benchmark-free scores with the judged plain-harmful refusal rate on the 52-member / 28-lineage
  / 11-family scale panel, at both aggregation units. Bars are 95\% lineage-clustered bootstrap intervals over 10,000 replicates.
  Only the logit-gap harmful margin clears zero at both units; the benign-prompt variant of the same statistic does not clear
  zero at either.
image_gen_detailed_description: >-
  Horizontal forest plot (point estimate with 95% confidence interval whiskers), two series distinguished by colour and marker.
  X-axis: 'Spearman rho with judged plain-harmful refusal rate', range -0.45 to 1.00, with a bold vertical reference line
  at 0.00 and a dashed vertical line at 0.50 labelled 'pre-registered threshold'. Y-axis categories, top to bottom: 'logit-gap
  harmful (80 fwd passes)', 'logit-gap harmful, union lexicon (80)', 'our-AMS sigma (96)', 'logit-gap benign (40)'. Series
  1 'member unit (n=52, lineage-clustered)' in dark blue: values 0.694 [0.495, 0.822]; 0.579 [0.281, 0.746]; 0.359 [0.047,
  0.592]; 0.129 [-0.168, 0.436]. Series 2 'lineage unit (n=28)' in orange: values 0.564 [0.140, 0.826]; 0.482 [0.086, 0.760];
  0.162 [-0.314, 0.597]; 0.103 [-0.355, 0.499]. Sans-serif, white background, light horizontal gridlines only.
aspect_ratio: '16:9'
summary: >-
  Forest plot showing the logit-gap harmful margin is the only score excluding zero at both aggregation units on the 28-lineage
  panel.
figure_path: figures/fig2_v0.pdf

--- Item 3 ---
id: fig3
figure_type: data
title: Does the effect live only in the old models?
caption: >-
  The provenance block split, the diagnostic that separates a transferable score from a small-panel artifact. The logit-gap
  harmful margin gives 0.667 on the 19 archived members and 0.668 on the 33 newly measured ones, a difference of $-0.0004$.
  The AMS paraphrase refit's advantage, by contrast, is entirely inside the block that produced it: $+0.2963$ archived against
  $-0.016$ new.
image_gen_detailed_description: >-
  Grouped bar chart, two panels side by side sharing a y-axis style but with different y-quantities, each panel labelled.
  LEFT PANEL title 'Correlation with judged refusal rate (Spearman rho)'. Categories on x-axis: 'logit-gap harmful', 'our-AMS
  sigma'. Two bars per category: 'archived 19 members (7 lineages)' in dark blue and 'new 33 members (18-22 lineages)' in
  light green. Values: logit-gap harmful archived 0.667, new 0.668; our-AMS sigma archived 0.358, new 0.402. Y-axis range
  0.0 to 0.8, label 'Spearman rho'. RIGHT PANEL title 'AMS paraphrase refit: paired advantage Delta_A'. Categories on x-axis:
  'archived 19 members', 'new 33 members'. Single series, bars coloured dark blue (archived) and light green (new). Values:
  0.2963 and -0.016. Y-axis range -0.10 to 0.35, label 'Delta_A (refit minus original)', with a bold horizontal reference
  line at 0.00. Annotate the right panel's new-33 bar with the text 'CI [-0.144, 0.130]'. Annotate the left panel with a small
  text label 'block difference -0.0004 [-0.308, 0.380]'. Sans-serif, white background.
aspect_ratio: '16:9'
summary: >-
  Two-panel bar chart: the surviving score transfers across provenance blocks while the retracted refit does not.
figure_path: figures/fig3_v0.pdf

--- Item 4 ---
id: fig4
figure_type: data
title: How much of the coupling was the control axes
caption: >-
  The read-versus-act coupling under seven estimators of the same relationship. The pooled 70-pair coefficient our previous
  draft led with (top) mixes between-axis and between-model variance; an exact two-way decomposition on the balanced 14$\times$5
  design attributes 0.896 of it to between-axis-type variation, 0.036 to between-member variation and 0.069 to residual. The
  primary estimand -- within the canonical axis, across the 14 detection-powered members -- has an interval covering zero
  at the member unit.
image_gen_detailed_description: >-
  Horizontal forest plot with point estimates and 95% confidence interval whiskers, single series in dark blue except where
  noted. X-axis 'Spearman rho (induction quality vs detection quality)', range -0.30 to 1.05, bold vertical reference line
  at 0.00. Y-axis rows, top to bottom, with the top two rows shaded light grey to mark them SECONDARY: 'POOLED, all 5 axes,
  70 pairs (secondary)' 0.629 [0.465, 0.803]; 'POOLED, control axes C and D dropped, 42 pairs (secondary)' 0.545 [0.284, 0.726];
  then unshaded PRIMARY rows: 'WITHIN axis A, member unit, n=14' 0.547 [-0.031, 0.930]; 'WITHIN axis A, lineage unit, n=7'
  0.821 [0.348, 1.000]; 'partial, axis main effect removed' 0.234 [-0.059, 0.397]; 'partial, axis + member effects removed'
  0.126 [-0.240, 0.366]; 'mixed-effects slope on ranks' 0.192 [-0.075, 0.458]. Add an inset stacked horizontal bar in the
  lower right corner titled 'Variance decomposition of the pooled statistic' with three segments labelled with their values:
  'between axis type 0.896' (red), 'between member 0.036' (blue), 'residual 0.069' (grey), summing to 1.000. Sans-serif, white
  background.
aspect_ratio: '16:9'
summary: >-
  Forest plot plus variance decomposition showing the previously headline coupling coefficient is 89.6% a between-axis-type
  contrast.
figure_path: figures/fig4_v0.pdf

--- Item 5 ---
id: fig5
figure_type: data
title: The axis reads canned refusals, not all refusals
caption: >-
  Axis-A detection AUROC under regex versus semantic labels, and split by refusal wording. Swapping the label barely moves
  the pooled value ($-0.013$ paired), but the axis separates canonically-worded refusals at 0.897 and the genuine refusals
  the regex misses at only 0.611 -- inside the members' own random-direction reading band, whose upper edge averages 0.750.
  The verdict is \texttt{READS\_CANONICAL\_WORDING\_ONLY}.
image_gen_detailed_description: >-
  Vertical bar chart with 95% confidence-interval error bars, four bars. X-axis categories, left to right: 'pooled, regex
  label' (grey-blue), 'pooled, semantic label' (blue), 'canonically-worded refusals' (green), 'REFUSAL_NONCANONICAL (regex
  misses)' (red). Values with intervals: 0.834 [0.736, 0.923]; 0.821 [0.752, 0.866]; 0.897 [0.864, 0.922]; 0.611 [0.542, 0.686].
  Y-axis 'axis-A detection AUROC', range 0.45 to 1.00. Draw TWO horizontal reference lines spanning the plot: a dashed grey
  line at 0.500 labelled 'textbook chance', and a solid orange line at 0.750 labelled 'measured random-direction reading band,
  mean upper edge'. Annotate the gap between the two pooled bars with 'paired delta -0.013 [-0.067, +0.030]'. Sans-serif,
  white background, light horizontal gridlines.
aspect_ratio: '4:3'
summary: >-
  Bar chart showing the refusal axis reads canonically-worded refusals well and non-canonical ones no better than a random
  direction.
figure_path: figures/fig5_v0.pdf

--- Item 6 ---
id: fig6
figure_type: data
title: Refusal induced by each steering direction
caption: >-
  Five-class any-refusal rate on fluency-screened text at matched axis-contrast units, with the random-direction false-positive
  floor drawn as a reference line. The token-disjoint paraphrase axis B induces 0.028 against the canonical axis A's 0.747
  and sits 0.118 [0.082, 0.157] BELOW what a meaningless direction induces on the same filtered population, so the canonical
  axis's advantage is semantic rather than a wording artifact. The inset shows the one pre-registered level at which B does
  clear its floor -- its own peak coefficient, 4.3$\times$ the dose A requires.
image_gen_detailed_description: >-
  Main panel: vertical bar chart with 95% paired prompt-clustered bootstrap error bars. X-axis categories: 'A canonical (n=600)'
  dark blue, 'B token-disjoint paraphrase (n=600)' light blue, 'C stylistic control (n=600)' grey, 'D random control (n=575)'
  red. Values: 0.747 [0.618, 0.858]; 0.028 [0.008, 0.057]; 0.017; 0.146. Y-axis 'five-class any-refusal rate at matched axis-contrast
  units', range 0.0 to 0.95. Horizontal dashed red reference line at 0.146 labelled 'random-direction false-positive floor'.
  Annotate bar B with 'net vs floor = -0.118 [-0.157, -0.082]'. INSET panel in the upper right, small, titled 'axis B at its
  OWN peak coefficient (5.21 contrast units, 4.3x A)': two bars, 'B refusal rate' 0.642 (light blue) and 'floor at that level'
  0.077 (red), y-axis 0 to 0.8, annotated 'net +0.565 [+0.471, +0.655]'. Sans-serif, white background.
aspect_ratio: '4:3'
summary: >-
  Bar chart of matched-contrast refusal rates by steering axis against a measured random-direction floor, with an inset showing
  where the paraphrase axis does work.
figure_path: figures/fig6_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH, prints at 93% and keeps its text above 10 pt. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where the hero ENDS UP is decided by its [FIGURE:] marker in
paper_text, which is already placed near the end of the Introduction — preserve it.
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-13 06:49:10 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-08-13 06:49:16 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated vector PDFs and JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-08-13 06:49:16 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
