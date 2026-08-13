# review_paper — test_idea

> Phase: `invention_loop` · round 5 · `review_paper`
> Run: `run_CbJDs3opF7E_` — Rating Model Safety in Eighty Forward Passes
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 05:17:14 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An adversarial paper reviewer (Step 3.5: REVIEW_PAPER in the invention loop)

You received a paper draft written by a DIFFERENT model. Review it with fresh eyes.
Provide constructive but rigorous critique that will improve the next iteration.

Specific critiques → better paper. Vague praise → no improvement.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical conference reviewer.
Your expertise spans the domain of the paper under review.
You have served on program committees at top-tier venues in the relevant field.

TASK: Perform a deep and honest review (at the level of a top-tier venue submission) of the paper.

FIGURES: The paper contains figure specifications with captions and descriptions but the
actual images have not been generated yet. Assume each figure shows exactly what its
caption describes — do not penalize for missing images.

ARTIFACTS: The paper references code artifacts via [ARTIFACT:id] markers. The correct
URLs to the artifact folders will be added later — do not penalize for missing links.

GOAL: Your review feeds directly back to the paper author. The objective is to maximize
the overall review score in subsequent rounds. Every piece of feedback you give should
be written with this goal in mind — prioritize the critiques and suggestions that would
produce the largest score improvement if addressed. Don't waste the author's iteration
budget on low-impact polish when there are score-blocking issues to fix.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Originality: Are the tasks or methods new? Novel combination of known techniques?
    Clear differentiation from prior work? Is related work adequately cited?
(b) Quality: Is the submission technically sound? Are claims well supported by theoretical
    analysis or experimental results? Is the methodology appropriate? Is this a complete
    piece of work? Are the authors honest about limitations?
(c) Clarity: Is the submission clearly written and well organized? Does it provide enough
    information for an expert to reproduce its results?
(d) Significance: Are the results important? Would others build on them? Does it address
    a meaningful problem better than prior work? Does it advance the state of the art?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims, experimental and research methodology,
and whether central claims are adequately supported with evidence:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — quality of the overall contribution, importance of questions asked,
originality of ideas and execution, value to the broader research community:
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
- Distinguish major issues (would cause rejection) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Check if figures are well-specified and would effectively communicate the results
- Verify that claims are supported by the artifacts described
- Screen for unattributed reuse. Search the web for the paper's distinctive phrasings, its central claim, and any method name it coins. If wording, a derivation, or a result appears in prior work, say so and name the source. Treat close paraphrase of a source's argument without citation the same as verbatim reuse
- Check that any prior work the paper builds on is cited at the point it is used, not only in a related-work list. An uncited source that the work depends on is a major issue, not a presentation nit
- Check the cited sources exist and say what they are claimed to say. Flag any reference you cannot verify, and any retracted or predatory-venue source

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

<paper>
# Introduction

Anyone who downloads an open-weight checkpoint faces a question with no cheap answer: is this model safety-aligned, and how much? The standard answer is a harmful-prompt benchmark such as AdvBench [1], JailbreakBench [2] or HarmBench [3], several hundred generations scored by a judge model [4], and a repeat of the whole procedure for every attack template of interest. The evaluator must hold, transmit and store harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown.

The stakes are set by scale. Hugging Face hosts hundreds of thousands of derived checkpoints, a growing fraction of them explicitly *uncensored* community fine-tunes, and the cheapest of these is produced by a weight edit — *abliteration* — that orthogonalizes every write against a single refusal direction [5]. A platform, a downstream deployer or a regulator wanting to triage such a population needs a score that costs seconds per model.

The published attempts at such a score are validated on panels far too small to support them, and the panel size is the part nobody reports. AMS [6] scans activation geometry over 14 configurations from 4 architecture families and reports Pearson $r = -0.546$ ($p = 0.043$) against behavioural compliance — its directly comparable rank statistic is $\rho = -0.423$ at $p = 0.13$, which is not significant. RAS/SafeVec [7] needs unsafe prompts, jailbreak prompts and a safety-aligned reference model, and reports no correlation coefficient, no $n$ and no resampling unit. VISAGE [8] evaluates a harmful benchmark at every weight perturbation. AQI [9] claims correlation with external judges with no locatable $n$ or coefficient. The one audit that exceeds 20 checkpoints — 273 of them — scores a *binary* uncensored label and presumes an attested reference model plus a full weight download [14]. Of the five model-level internal safety scores we could locate in primary text, five validate at four or fewer architecture families, four at fourteen or fewer checkpoints, and **zero** resample on the weight lineage [ARTIFACT:art_9sXeYgowURMn]. Whether any member of this class predicts behaviour once the panel is large enough to say has, until now, not been tested by anyone.

This paper tests it, and one score passes. On a frozen panel of 52 checkpoints over 28 weight lineages and 11 architecture families, the first-decoding-step logit-gap margin read on harmful prompts — 80 forward passes, zero generations, zero judge calls, zero benchmark runs, zero reference models per checkpoint — predicts the judged plain-harmful refusal rate at Spearman $\rho = 0.694$ $[0.495, 0.822]$ with the lineage as the resampling unit, and $0.564$ $[0.140, 0.826]$ when members are first aggregated within lineage. It is not a small-panel artifact: split by provenance, the 19 archived members give $\rho = 0.667$ and the 33 newly measured ones $\rho = 0.668$, a difference of $-0.0004$. It survives a partial correlation on $\log_{10}$ parameter count ($0.676$), 28 leave-one-lineage-out folds ($[0.661, 0.726]$) and 11 leave-one-family-out folds ($[0.650, 0.772]$) without a sign change, and it beats our reimplementation of the closest published activation scanner by $+0.421$ $[0.169, 0.684]$ on the same resampled lineages.

The honesty statement that must travel with that number, and that we put in the abstract rather than a footnote, is what the score does *not* remove. It reads the margin on harmful prompts, so it is not harmful-prompt-free; the benign-prompt variant collapses to $\rho = 0.129$ $[-0.168, 0.436]$. What it removes is everything downstream of the forward pass: no generation, no judge, no benchmark, no reference model.

[FIGURE:fig1]

The same panel is what retires the rest of this project's programme, and we report those retractions as results rather than as limitations. Two iterations ago we proposed an act-side score — $\alpha_{50}$, the steering coefficient at which a fresh generation on a benign prompt refuses half the time — and it failed. The five-check falsification battery built to explain that failure could not rank cheap scores either. One positive lead survived, a paraphrase refit of AMS's contrast set that lifted criterion validity from $\rho = 0.358$ to $0.654$ on 7 lineages; measured on the same 28-lineage panel it collapses to $\Delta_A = +0.099$ $[-0.027, 0.244]$, with the effect localised entirely to the original 19-member block. Two scores, one panel, opposite outcomes: that contrast is what makes the panel informative rather than merely large.

The previous draft of this paper additionally claimed that reading and steering along one refusal axis are strongly coupled, at $\rho = 0.629$ over 70 (member, axis) pairs. A reviewer identified that statistic as dominated by a between-axis-type contrast, and re-analysis confirms it: an exact two-way decomposition attributes $0.896$ of the pooled coefficient to variation between axis types [ARTIFACT:art_3Nid1IyvhfIG]. The correct primary statistic — within the canonical axis, across models — is $\rho = 0.547$ with a lineage-clustered interval of $[-0.031, 0.930]$ that covers zero. We report the weaker claim.

## Summary of Contributions

- **A cheap safety score that survives a fourfold panel increase** (§5.1) [ARTIFACT:art_Vag73M9ysCVF]. The first-decoding-step logit-gap harmful margin predicts judged plain-harmful refusal at $\rho = 0.694$ $[0.495, 0.822]$ (member unit, lineage-clustered bootstrap) and $0.564$ $[0.140, 0.826]$ (lineage unit) over 52 members / 28 lineages / 11 families, with a Monte-Carlo lineage-permutation $p$ at the $5\times10^{-6}$ design floor. The archived-19 vs new-33 block split gives $0.667$ vs $0.668$. Cost: 80 forward passes, 0 generations, median 20.0 s per checkpoint including download.
- **The first model-level criterion validation in this class that resamples on the weight lineage** (§2, §5.1) [ARTIFACT:art_9sXeYgowURMn]. Zero of five published model-level internal safety scores do; the widest published family axis is four, against our eleven. We claim neither the scalar (it is Li and Liu's [10]) nor the largest checkpoint panel (Hurtado's [14]) — only the conjunction.
- **A companion negative that makes the positive interpretable** (§5.2) [ARTIFACT:art_CZaytBH8uL4_]. On the identical panel the AMS paraphrase refit gives $\Delta_A = +0.099$ $[-0.027, 0.244]$ against an archived $+0.296$, an independently authored paraphrase set gives $-0.152$, and the effect is localised: the archived 19 reproduce $+0.2963$ to $2.6\times10^{-4}$ while the 33 new members give $-0.016$. Panel size is not a nuisance parameter in this lane; it decides which of two same-cost scores you would ship.
- **The read-versus-act coupling, re-estimated without the axis-type confound** (§5.3) [ARTIFACT:art_3Nid1IyvhfIG]. Within the canonical axis across 14 detection-powered members: $\rho = 0.547$ $[-0.031, 0.930]$, exhaustive permutation $p = 0.149$; lineage unit $0.821$ $[0.348, 1.000]$. The pooled $0.629$ is demoted to a secondary and decomposed: $0.896$ between axis type, $0.036$ between members, $0.069$ residual. Verdict: `COUPLING_IS_AXIS_TYPE_CONTRAST` and `UNDERPOWERED`, both firing.
- **The verdict rule is $n$-asymmetric, and we quantify by how much** (§5.3). Simulating the study's own bootstrap over 141 cells, `AT_CHANCE` is unreachable below 40 items per class ($P = 0.000$ at the pre-registered gate; Hanley–McNeil closed form $n = 65$; first attainable at $n = 80$), while `READS` fires with probability $1.000$ under perfect separation at $n = 7$. The tally is now reported twice — 20/1/0/9 over all 30 members, 13/1/0/0 over the 14 powered ones — and the abliterated-arm claim is re-carried on refusal *rates* (exhaustive permutation $p = 0.0026$; paired sign test 10/10, $p = 0.0020$), needing no AUROC at all.
- **The detection label and the axis share a lexical basis, and the consequence is measured** (§5.3) [ARTIFACT:art_Y-oGSm04Tcar]. Re-labelling 660 stratified items with a five-class semantic rubric barely moves the pooled AUROC ($0.834 \to 0.821$, paired $-0.013$ $[-0.067, +0.030]$), but splits it: $0.897$ $[0.864, 0.922]$ on canonically-worded refusals against $0.611$ $[0.542, 0.686]$ on non-canonical ones, which does not clear the members' own random-direction reading band. Verdict: `READS_CANONICAL_WORDING_ONLY`.
- **The one published leakage control, run on our own headline** (§5.3). Re-estimating every centring and scaling statistic inside the training fold under leave-one-prompt-out moves axis-A AUROC by $-0.0205$ $[-0.0352, -0.0071]$, against the $-0.336$ the same control produced on its author's data [44]; the control on the control moves random axis D by $-0.0020$.
- **Three named measurement pathologies, each measured on our own published numbers** (§6) [ARTIFACT:art_9sXeYgowURMn]. Item-pool provenance is leakage type [L3.3] in Kapoor and Narayanan's taxonomy [46]; the aggregation unit moving $\rho$ from $0.358$ to $0.821$ is ecological correlation in Robinson's sense [47]; the $7\to28$ lineage collapse is small-sample correlation instability, and Schönbrodt and Perugini's own table puts our $n = 28$ six to nine times below the point of stability [49, 50]. We claim the instances, not the phenomena.

# Related Work

**Static, benchmark-free safety metrics, and how they are validated.** AMS [6] computes a standardized mean difference of projections onto a diff-in-means direction at 96 forward passes per model. RAS/SafeVec [7] extracts layer-wise refusal directions from a safety-aligned reference model and scores a target by hidden-state alignment. VISAGE [8] measures a weight-space safety basin, requiring a harmful benchmark at every perturbation. AQI [9] is a prompt-invariant latent-geometry diagnostic. RAS and VISAGE we do not run, for reasons fixed by a primary-source reimplementation audit [ARTIFACT:art_0UsKSgsMHome]: every RAS-scored checkpoint is $\geq$4B and none overlaps any panel at our scale, and VISAGE at published fidelity costs 4,800 generations and roughly 28 hours per 1B model on CPU. AMS and Logit-Gap Steering [10] we reimplement and run.

What is uniform across these papers is the thinness of the validation panel, and a dossier read all five in primary text to establish it [ARTIFACT:art_9sXeYgowURMn]. AMS validates at 14 configurations over 4 families; RAS states a qualitative correlation with attack success rate across 3 families with no coefficient, $n$ or resampling unit; AQI's abstract claims correlation with external judges with neither $n$ nor coefficient locatable; Logit-Gap Steering validates a *per-prompt* margin against its own attack's success rate across suffix strategies, with family-clustered inference at $n = 3$; Hurtado's abliteration audit [14] exceeds 20 checkpoints at 273 but against a binary label, with an attested reference and full weight access. Not one resamples on the weight lineage — the unit at which the statistical dependence actually lives, since one pretrained base and its derivatives are not independent observations. That is the gap §5.1 fills, and it is a gap in *validation practice*, not in scalar design.

**The scalar we validate is not ours.** Logit-Gap Steering [10] defines the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step as "the per-prompt safety margin that alignment provides", and reports that the aligned model's gap exceeds the base model's on 97.5–99.8% of toxic prompts, with position-1 accounting for 92–99% of the refusal decision depending on family. A full-text extraction confirms that no cross-model margin-versus-behaviour correlation exists anywhere in that paper: all 28 correlation matches are token-level, suffix-level, or cited from elsewhere [ARTIFACT:art_9sXeYgowURMn]. One estimand difference must be declared: their affirmative token is selected *per prompt* as the highest-logit one, making their gap an attack-relevant minimum, whereas our fixed-lexicon maximum is a different quantity. Xu and Sheng [51] use refusal vectors as a provenance fingerprint over 76 offspring models, identifying the base family at 100% accuracy — model identity, not safety behaviour, which is the cleanest available contrast to what we predict.

**Detection versus intervention.** Galeone et al. [12] establish that a detection direction at AUC $1.000$ can sit at $\cos = 0.12$ from the direction that produces the behaviour, and propose a *functional* criterion: the steerable case is where the intervention direction also detects. Mehta [44] is the closest published neighbour to the read-versus-act claim our previous draft led with, and it is a mirror image: one direction detects alignment faking at leave-one-query-out AUROC $0.87$ on Llama-3.1-8B while steering over 2,000 runs "barely changes compliance" (Cohen's $h = +0.057$, Fisher $p = 0.41$). Three distinctions were verified in full text [ARTIFACT:art_G5SIDXT53EAW]: his dissociation is assembled *across two models* (the steering null is on Qwen3-32B, where his own detection falls to $0.43$), his probe is a two-layer MLP rather than the steered unit vector, and no activation norm is reported, so his coefficient is not convertible to our contrast units. One concession is forced: he does steer a refusal axis and get a null. The most transferable thing in his paper is not the dissociation but the leakage control it survived — his own AUROC falls from $0.761$ to $0.43$ under per-fold residualisation and leave-one-query-out, and it reaches $0.63$ on a control condition where the effect cannot exist. We run that control on our own headline in §5.3. Nadaf [23] independently reports that steering succeeds where the logit lens cannot decode across 4,032 concept-layer pairs while the converse is "nearly empty (3 of 72)", which makes coupled read–act the expected case.

**Activation scores on abliterated checkpoints.** Two incumbents bound what we may claim [ARTIFACT:art_G5SIDXT53EAW]. Hurtado [14] separates 57 public abliterations from 37 benign fine-tunes at AUROC $0.95$, but the activation leg is a thresholded ratio (AUROC $0.84$) that "certifies whether the refusal mechanism is present, not whether a model is harmless", and it "presumes an attested reference". Llorente-Saguer [45] already runs base / instruction-tuned / abliterated Qwen triplets and reports that "both abliterated variants achieve AUROC at most 0.015 below their instruction-tuned counterparts", noting that its axis "is not the refusal direction itself, since it survives abliteration". Any claim to be first to read an activation safety score on abliterated checkpoints is therefore withdrawn. What survives, and what §5.3 reports, is narrower and compatible: the *refusal axis specifically* goes quiet on abliterated checkpoints, because the refusals it would read are gone.

**Steering-vector reliability.** Non-identifiability is established: steering vectors admit "large equivalence classes of behaviorally indistinguishable interventions" [15]. Unreliability has geometric predictors across 36 datasets [13], and the safety cost of steering has been catalogued [40]. Success is partly predictable ex ante at $\rho = +0.86$ to $+0.91$ across 24 concept families [16], though the Linear Accessibility Profile could not have predicted our axis comparison, because it never sees the steering direction and both of our axes score identically. Refusal is multi-directional: eleven category directions, several near-orthogonal, yield "nearly identical refusal to over-refusal trade-offs" [17], and category-specific directions can be composed for control [18]. Petrov [19] was the top refutation risk for our axis comparison, reporting that changing only the contrast baseline "produces no functional refusal directions at any tested weight level on any tested layer" by "reducing the extracted direction magnitude below the threshold at which weight-matrix projection perturbs the residual stream"; §5.4 settles it on 30 checkpoints in axis-contrast units, which normalise the axis magnitude by construction. Wu et al. [37] show a "steerability emerges with scale" result dissolves under exactly that normalisation.

**Auditing a safety measurement, and the pathologies we name.** The battery framing is prior art in kind and we say so. Wang et al. [20] separate "construct validity ... metric validity ... criterion validity", run pre-specified positive and negative controls, and survive "leave-one-organization-out and organization-clustered bootstrap"; they are also the source of the field-local warning that a small panel manufactures results — a correlation moving "from $-0.64$ at $n=7$ to $+0.02$ at $n=18$", with "a quarter of random size-7 subsets" showing $|\rho| \geq 0.5$ despite a near-zero full-panel value. Weng et al. [21] operationalise rubric-semantics invariance under certified-equivalent rewrites and state the discrimination requirement outright. The methodological ancestor of both is the sanity-check literature for saliency maps [22]. Outside machine learning, the three phenomena §6 names have canonical statements: Kapoor and Narayanan's leakage taxonomy [46], whose type [L3.3] *sampling bias in test distribution* is our item-pool case exactly; Robinson's demonstration that an ecological correlation can differ in sign from its individual counterpart [47], extended by Openshaw's modifiable-areal-unit literature [48]; and Schönbrodt and Perugini's point-of-stability analysis [49, 50]. Simpson's note [52] names the paradox but its setting is categorical contingency tables, so Robinson is the closer analogue.

**Refusal geometry and dynamics.** Arditi et al. [5] show refusal is mediated by a single direction and introduce the weight edit the abliteration community built on; representation engineering [24], activation addition [25] and contrastive activation addition [26] supply the steering machinery. Qi et al. [27] show aligned and unaligned generative distributions differ mainly over the first few output tokens; Yin et al. [28] trace a probe refusal score across token positions, an observable we adopt rather than coin. Korznikov et al. [29] report random steering raising harmful *compliance* from 0% to 1–13% at an identically calibrated coefficient; §5.6 supplies the matching measurement for the direction they do not test. Our behavioural axes follow AdvBench [1], JailbreakBench [2] and XSTest [34], with judge scoring in the style of [4]; Hasan and Biswas [39] find over-refusal and harmful compliance nearly uncorrelated ($r = -0.032$, $p = 0.89$) across 21 open-weight models, which is why the three axes are predicted separately. The critical-slowing-down programme [30, 31, 32, 33] supplied the indicators for this project's first iteration; that arm is closed and summarised in Appendix A.

# Preliminaries

**Panels and the resampling unit.** Three panels appear, and every claim names the one it rests on. The *depth* panel is six Qwen3 [35] checkpoints (0.6B and 1.7B $\times$ base / instruct / abliterated) measured exhaustively [ARTIFACT:art_r3PqOtpvcIsK]. The *read-versus-act* panel is 30 checkpoints over 7 lineages, each measured in both roles of five axes [ARTIFACT:art_1xT3w1joqeJ8]. The *scale* panel is 52 analysed members over 28 weight lineages and 11 architecture families at $\leq$4.2B, drawn from a frozen manifest of 137 verified checkpoints over 93 lineages [ARTIFACT:art_CKWQh2cOQLLQ], and split for diagnostic purposes into the 19 members archived from iteration 2 and the 33 measured afresh. The *lineage* — one pretrained base and everything derived from it — is the resampling and permutation unit for every model-level claim.

**Aggregation unit.** Because a lineage carries between one and four members, a model-level correlation can be computed two ways. *Member level* means one row per checkpoint with the bootstrap and the permutation clustered on the lineage label; *lineage level* means one row per lineage, each the arithmetic mean over that lineage's defined members of both the score and the outcome. Both are legitimate; they are not interchangeable, and §5.5 measures how far apart they are. Every correlation below is labelled and Table 6 gives both for every score.

**Prompt sets.** All frozen and shipped [ARTIFACT:art_CKWQh2cOQLLQ]: 40 vetted everyday harmless user turns over 10 topics; 594 deduplicated AdvBench/JailbreakBench harmful behaviours with an 80-item stratified core; 400 jailbreak items; XSTest's 250 safe and 200 unsafe items; 256 harmful/benign contrast items reserved for layer selection only (exact overlap 0 with any evaluation set, maximum cosine $0.652$ against a $0.85$ threshold); 200 WikiText fluency passages.

**The four scores.** All are read from forward passes only. **Logit-gap harmful** is the difference between the maximum logit over a per-tokenizer-family empirical refusal-onset lexicon and the maximum over a continuation lexicon, at the first decoding step, averaged over the frozen 80-item harmful core — 80 forward passes. **Logit-gap benign** is the same quantity on 40 harmless prompts. **Our-AMS $\sigma$** is our reimplementation of [6] — $(\mu_+ - \mu_-)/\sigma_{\text{pooled}}$ on the diff-in-means direction, final prompt token, 40–80% relative-depth sweep, 96 forward passes. **$\alpha_{50}$**, retained only as this project's retired incumbent, is the steering coefficient at which a fresh benign-prompt generation refuses half the time; it costs 265 generations per member.

The refusal-onset lexicon is *empirical*, derived per tokenizer family from tokens that actually open refusals under greedy decoding, and it is never back-filled across families: five scale-panel members whose family has no lexicon entry receive NULL primary columns with reason `MISSING_FAMILY_LEXICON`, and a clearly labelled union-of-all-families secondary column is reported beside the null rather than substituted for it.

**Steering axes.** Five axes are fitted per model at the same site on the same benign prompts: **A**, the canonical response contrast between four hand-written canned refusals and four compliances; **B**, a token-disjoint paraphrase axis built from 24 refusal paraphrases containing zero frozen refusal openers; **C**, a norm-matched non-safety stylistic axis (formal versus casual); **D**, matched random unit directions; **E**, the harmful-versus-benign *prompt* contrast. The steering site is $L = \mathrm{round}(0.25\,n_{\text{layers}})$.

**Axis-contrast units.** The steering hook adds $\alpha\,\mathrm{NORM}_L\,\hat{x}$ to the residual stream, where $\mathrm{NORM}_L$ is the median residual-stream norm at the steering layer. Because raw diff-in-means norms differ up to fourfold between axes, all dose comparisons are reported per *axis-contrast unit* $c = \alpha\,\mathrm{NORM}_L / \lVert X \rVert$, which divides out the axis magnitude and is what settles the magnitude-collapse rival explanation [19]. The conversion was verified exact (absolute error $0.0$) against 459 archived grid cells.

**The refusal criterion.** A generation counts as a refusal when its opening matches an anchored refusal regex. Because the regex is lexical, §5.3 and §5.4 additionally re-score with a four-class semantic judge and with a five-class rubric carrying an explicit non-canonical-refusal class, and every semantic rate is reported against a control false-positive floor measured on the same filtered population.

**A tokenisation hazard worth stating.** Re-encoding a prompt and its logged completion by concatenating *strings* lets byte-pair merges cross the boundary; concatenating token *ids* fixes it. The bug is renderer-dependent: on 50 probe items it changes the boundary index on 34/50 under the plain wrapper and 0/50 under a chat template, so it bites base checkpoints specifically. Relatedly, Qwen3 base tokenizers ship a chat template despite never having been tuned to follow one; automatic template selection dropped axis-E reproduction cosine to $0.13$, and forcing the plain wrapper on base models restored all six archived checkpoints to $\geq 0.99992$.

# Method

Five instruments, each pre-registered with a sha256 stamp before any statistic existed, with every deviation logged with its trigger and the data state at the time.

## Instrument 1: the scale-panel test of the score that won

The reviewer of our previous draft identified the decisive scoping error: the 52-member panel had been spent replicating the score that *lost* the discrimination matrix, leaving the score that won — the logit-gap harmful margin, the only one whose confidence interval excluded zero at both aggregation units — untested at $n_{\text{lineage}} = 28$. This instrument runs it [ARTIFACT:art_Vag73M9ysCVF].

Four outcomes were pre-registered, verbatim, before any correlation: `HOLDS` requires $\rho \geq 0.50$ **and** a CI excluding zero at *both* units; `HOLDS_AT_MEMBER_UNIT_ONLY` is pre-committed as *not a win* — "this is the same unit-dependence iteration 4 documented and must not be written as one"; `COLLAPSES` converts the paper's claim into a general statement about the score class; `REPLAY_FAILED` halts the analysis entirely. The gate order is enforced by the driver: byte-identity of 17 reused library files, 14 offline apparatus assertions, constant extraction by `ast` (the iteration-3 driver calls `setrlimit` at module scope and cannot be imported), panel and ground-truth identity, a T0-REPLAY reproducing iteration 3's $0.6673$ $[0.439, 0.904]$ / $0.929$ to four decimals, and only then the pre-registration stamp. Ground truth is the archived judged plain-harmful refusal rate, reused rather than re-judged, so LLM spend is $0.00 and the outcome variable cannot drift.

Three secondary analyses were registered in advance rather than chosen after: the archived-19 versus new-33 block split, which is the diagnostic that localised the paraphrase refit's failure; a partial Spearman controlling for $\log_{10}$ parameter count, because the obvious rival explanation is that any activation score is a capability proxy; and both leave-one-lineage-out and leave-one-family-out jackknives.

## Instrument 2: the paraphrase refit at scale

The AMS paraphrase refit is rerun on the identical 52 members [ARTIFACT:art_CZaytBH8uL4_], with four pre-registered outcomes: **R1** $\Delta_A > 0$ with its paired lineage-bootstrap CI excluding zero; **R2** $\rho(\text{refit A}) \geq 0.40$ with its CI excluding zero; **R3** $\Delta_B > 0$ where SET B is an *independently authored* paraphrase set; **R4** permutation $p < 0.05$ and off the floor by an order of magnitude. SET B was generated by a model that is never the judge, at temperature $0.3$, and verified by the *frozen* iteration-3 `check_pair()` with zero hand-written repairs (80/80 strings pass, 78 on the first attempt); measured content-token Jaccard against SET A is $0.201$.

## Instrument 3: the read-versus-act re-analysis

A pure re-analysis of the frozen 30-checkpoint tree, with estimators imported rather than retyped and a 169-leg reproduction gate that passes at $10^{-6}$, with the pooled coefficient and its interval reproducing at the archived seed to $0.0$ [ARTIFACT:art_3Nid1IyvhfIG]. Three repairs are made.

*The coupling statistic.* The primary estimand becomes the within-axis-A, across-member correlation over the 14 detection-powered members, at both aggregation units, with the lineage-clustered bootstrap and an exhaustive $7! = 5040$ permutation. The pooled 70-pair figure is retained only as a labelled secondary and is decomposed: because the design is a balanced $14 \times 5$, a two-way decomposition of the rank cross-product is *exact and orthogonal*, so the share attributable to axis type is a measurement rather than an argument. A control ladder (drop the two by-construction null axes), a rank-residualised partial correlation, and a mixed-effects slope on ranks are all reported.

*The verdict rule.* Rather than assert that the rule is asymmetric, we simulate the study's own prompt-clustered percentile bootstrap over a $141$-cell grid of true AUROC $\times$ items per class, 2,000 replicates per cell with 2,000 inner resamples, and report the attainability surface of each verdict. A closed-form Hanley–McNeil check accompanies it. The tally is then reported twice: as shipped over all 30 members, and restricted to the 14 members the pre-registration says the statistic exists on.

*The abliterated arm.* The structural claim is re-carried on spontaneous refusal *rates*, which involve no AUROC: a two-sided Mann–Whitney U on member-level rates, an exhaustive permutation over all $293{,}930$ group assignments (the arms share one tied rate, so `scipy`'s exact method is invalid here and its value is recorded but never quoted), a lineage-clustered bootstrap of the median difference, and a paired within-lineage sign test.

## Instrument 4: breaking the label–axis lexical circularity, and the leakage control

Axis A is fitted on canned refusals and the detection label is a canned-refusal regex, so part of any shared AUROC is definitional. Instrument 4 re-labels 660 stratified items — stratified by regex label $\times$ stratum $\times$ projection tertile, with the middle tertile double-sampled and inverse-probability weights back to the item population — using the five-class semantic rubric already built for the degeneracy adjudication, loaded verbatim from the archived judge stage [ARTIFACT:art_Y-oGSm04Tcar]. A reproduction gate regenerates 667 archived cells from stored projections at $\max|\Delta| = 0.0$ first.

The same instrument runs the one published leakage control [44]: four normalisation protocols on identical items and axes — the archived whole-pool centring, fold-internal centring under leave-one-prompt-out, fold-internal centre-and-scale (Mehta's full residualisation), and a deliberately leaky whole-pool z-score — on axes A, B and the norm-matched random axis D, under both label sets. Axis D is the control on the control: a normalisation artifact would move it too. The leakage precondition is re-asserted rather than inherited, with axis-fit strings re-parsed from the archived fitting code and exact text overlap recomputed per member.

## Instrument 5: the aggregation-unit repair, the threshold surface, and the claim ledger

A pure re-analysis over the frozen archives with no GPU and no spend [ARTIFACT:art__tq3ZgPRYB0B]: an 11-leg reproduction gate, every score recomputed at both aggregation units with the exhaustive permutation held constant, and a 164,736-point full factorial in the falsification battery's five thresholds.

A second instrument audits the paper's own prose [ARTIFACT:art_Xx1VPyGi4nAT]. Every numeric and verdict-string claim on every number-bearing surface — prose, tables, figure captions, figure summaries, abstract — is resolved against a two-tier pointer index over the shipped JSON (an unfiltered index over 152,118 numeric leaves resolves almost any two-decimal number to *something*, producing false matches, so only 51,178 reportable summary-statistic pointers may resolve a claim). 911 claims over 142 surfaces were audited; the regenerated text re-audits at 150 claims with zero flags, byte-identically across two runs, under a lint forbidding bare numerals and a mutation test confirming the pointers are live.

# Results

## A cheap score that survives a fourfold increase in panel size

The pre-registered verdict is `HOLDS`, and it is the first positive result in this project [ARTIFACT:art_Vag73M9ysCVF]. On 52 members over 28 lineages and 11 families, the first-decoding-step logit-gap harmful margin predicts the judged plain-harmful refusal rate at $\rho = 0.694$ $[0.495, 0.822]$ at the member unit with a lineage-clustered bootstrap over 10,000 replicates, and $\rho = 0.564$ $[0.140, 0.826]$ at the lineage-aggregated unit. Both criteria of the pre-registered rule — $\rho \geq 0.50$ and a CI excluding zero — are satisfied at both units. The Monte-Carlo lineage-permutation $p$ sits at the design floor of $5\times10^{-6}$ over 200,000 draws, and we quote the floor beside it rather than a smaller number the design cannot express.

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

**What we do and do not claim.** We do not claim the scalar: the first-decoding-step refusal-affirmation margin is Li and Liu's [10], who establish it as a per-prompt safety margin and validate it against their own attack's success rate across suffix strategies, not across models. We do not claim to be first on abliterated checkpoints [45], nor the largest checkpoint panel [14]. What is ours is the conjunction none of them has: a model-level criterion validation of a first-decoding-step margin against a *graded* judged refusal rate, with no attested reference model and no weight access, over 11 architecture families, with inference clustered on the weight lineage — which zero of the five located model-level scores currently use [ARTIFACT:art_9sXeYgowURMn]. The closest published attempt at exactly this validation, AMS, reports Pearson $r = -0.546$ ($p = 0.043$) over 14 configurations from 4 families, and its directly comparable rank statistic is $\rho = -0.423$ at $p = 0.13$.

## The companion negative: the paraphrase refit does not survive the same panel

The value of the previous subsection depends on a second score having been run through the identical apparatus and having failed, and one was [ARTIFACT:art_CZaytBH8uL4_]. Our previous draft's one forward-looking result was that refitting AMS's contrast set on token-disjoint paraphrases lifted its correlation with judged behaviour from $\rho = 0.358$ to $0.654$ on 19 members over 7 lineages. On the same 52 members over 28 lineages it does not replicate.

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

Our previous draft led §5 with the claim that reading and steering along one refusal axis are positively coupled at $\rho = 0.629$ $[0.465, 0.803]$ over 70 (member, axis) pairs. The reviewer's objection was that the 70 pairs are 14 members $\times$ 5 axes, that axis A is strong in both roles *by construction* and axes C and D null in both roles *by construction*, and that the pooled Spearman therefore measures a between-axis-type contrast. Re-analysis confirms the objection and quantifies it [ARTIFACT:art_3Nid1IyvhfIG].

**The primary statistic is now the within-axis, across-member one, and it does not resolve.** Within axis A across the 14 detection-powered members, $\rho = 0.547$ with a lineage-clustered 95% CI of $[-0.031, 0.930]$ over 7 resampling units and an exhaustive $5040$-permutation $p = 0.149$ against an attainable floor of $1.98\times10^{-4}$. Aggregating members within lineage first leaves the sign unchanged at $\rho = 0.821$ $[0.348, 1.000]$. The defensible sentence is therefore: *the axis that induces is also the axis that reads, but among models the two qualities are only weakly and non-significantly related.* That remains a clean reversal of the induce-without-detect dissociation our earlier work claimed; it is not a demonstration of coupling strength, and the previous draft wrote it as one.

**The confound is measured, not conceded.** Because the design is a balanced $14 \times 5$, a two-way decomposition of the pooled rank cross-product is exact and orthogonal. It attributes $0.896$ of the pooled coefficient to between-axis-type variation, against $0.036$ between members and $0.069$ residual, the three shares summing to $1.000$. Removing the axis main effect by rank-residualisation drops the association to $\rho = 0.234$ $[-0.059, 0.397]$; removing both the axis and the member main effects leaves $0.126$ $[-0.240, 0.366]$; a mixed-effects slope on ranks gives $0.192$ $[-0.075, 0.458]$. The trivial control the reviewer asked for is reported: dropping the two by-construction null axes moves the pooled coefficient from $0.629$ to $0.545$ $[0.284, 0.726]$ over 42 pairs. Within each single axis taken alone the coefficients are A $0.547$, B $0.148$, C $0.397$, D $-0.038$ and E $0.416$ — every one with an interval covering zero. No single axis carries a within-axis coupling on this panel.

[FIGURE:fig4]

The reviewer's own recompute over thirteen members is reproduced exactly rather than paraphrased: dropping `Llama-3.2-3B-Instruct`, the one member whose axis-A verdict is `AMBIGUOUS` rather than `READS`, gives $\rho = 0.434$, $p = 0.14$, against this analysis's 14-member $\rho = 0.547$, $p = 0.04$. Both of those $p$-values are the asymptotic Spearman value, which treats the 14 checkpoints as independent; the lineage-clustered interval covers zero at either $n$. The pre-registered verdict is `COUPLING_IS_AXIS_TYPE_CONTRAST` with `UNDERPOWERED` also firing — the within-axis interval's half-width is $0.480$, so at 7 lineages this panel could not have resolved a coupling of the size it estimates even if one is there. Both statements are true at once and the paper carries both. The within-member mean of $0.715$ is demoted rather than defended: it is the mean of 14 coefficients computed over the *same* axis-type contrast on five points each, two of which are controls, so being larger than the pooled figure makes it weaker evidence, not stronger.

**The verdict rule is $n$-asymmetric, and the Method previously misdescribed the gate.** The reviewer observed that `READS` was issued at 7, 12, 28, 32 and 33 refusals — counts the artifact's own `powered` column marks as not detection-powered — while only members with 0 or 1 refusals returned `UNDEFINED`, which is not the "fewer than 40 refusals" rule the Method described. Both halves are correct and are now fixed at the source. The code path is quoted in the deviation record `DEV-ITER5-01`: `verdict_from_ci` returns `UNDEFINED` if and only if the bootstrap CI bounds are non-finite, which happens because a $\geq$5-per-class resample guard discards enough replicates when one class holds 0–1 items; `MIN_PER_CLASS = 40` governs a *separate* `powered` flag the verdict never consults. The corrected Method sentence appears in §4 above.

The asymmetry is then quantified rather than asserted, by simulating the study's own prompt-clustered percentile bootstrap over 141 cells at 2,000 replicates each with 2,000 inner resamples. At a true AUROC of $0.500$, `AT_CHANCE` — which requires an entire 95% CI to fit inside the $0.20$-wide band $[0.40, 0.60]$ — is unreachable until $n = 80$ items per class: $P(\text{AT\_CHANCE}) = 0.000$ at the pre-registered $n = 40$ gate, and the Hanley–McNeil closed form puts the i.i.d. threshold at $n = 65$. Under perfect separation `READS` fires with probability $1.000$ at every one of $n = 7, 12, 28, 32, 33$. The asymmetry is *one-sided*, which matters for how the result should be read: the false-`READS` rate at true chance is only $0.005$ at $n = 10$ and $0.001$ at $n = 40$, so `READS` is not noise-driven — it is the *null* verdict that cannot be returned. Every "zero `AT_CHANCE`" sentence in this paper carries that footnote.

Accordingly the tally is reported twice. Over all 30 members the axis-A verdicts are 20 `READS`, 1 `AMBIGUOUS`, 0 `AT_CHANCE` and 9 `UNDEFINED`; restricted to the 14 detection-powered members they are 13, 1, 0 and 0. Reading is *measurable* — the AUROC and its interval both exist — on 21 members, not 20: the twenty `READS` members plus `Llama-3.2-3B-Instruct`. The minimum axis-A AUROC is $0.685$ over the 21 members with a defined AUROC and $0.691$ over the 20 `READS` members; the bare form "$\geq 0.68$" that appeared in our previous draft belongs to neither population and is retired [ARTIFACT:art_Xx1VPyGi4nAT].

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

The most damaging defect a reader could have found in an earlier draft was internal: our AMS reimplementation's correlation with judged behaviour appeared as $0.358$ in one section and $0.821$ in another, with a headline $\Delta$ computed from the second. Both numbers are correct and neither was labelled [ARTIFACT:art__tq3ZgPRYB0B]. At the **member level** — 19 checkpoints, resampled and permuted on the lineage label — the statistic is $\rho = 0.358$ $[-0.074, 0.699]$ with exhaustive permutation $p = 0.0911$. At the **lineage level** — 7 units, each the mean over that lineage's defined members of both score and outcome — the same statistic is $\rho = 0.821$. The gap of $0.464$ is what lineage aggregation buys by removing within-lineage variance and reducing $n$ from 19 to 7.

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

The 30-checkpoint study was designed to test axes, and it produced two facts about *controls* that generalise beyond this paper [ARTIFACT:art_1xT3w1joqeJ8].

First, a random direction is not behaviourally inert at the magnitude at which a refusal axis works. Injected at axis A's own matched magnitude, a matched random unit direction induces refusal at a maximum rate of at least $0.10$ on 7 of 30 members, with a worst case of $0.389$ and a panel median of $0.028$. Korznikov et al. [29] report the complementary effect — random steering raising harmful *compliance* to 1–13% at an identically calibrated coefficient — and never test random-induced refusal on benign prompts; this is that measurement, and it says the induction floor is a real quantity that steering claims must clear. Our own earlier random-direction null ($0.00$–$0.058$) was measured on six checkpoints and does not generalise to 30.

Second, a random direction does not *read* at $0.500$. The empirical band of AUROCs over 20 random draws per member spans $\pm0.075$ to $\pm0.500$ across members, because residual streams are anisotropic, so a gate written against the textbook $0.500$ is wrong by a wide and model-dependent margin. A single random draw is not a null distribution. Relatedly, a raw projection is $\lVert h\rVert\cos\theta$, so any direction inherits whatever refusal-versus-compliance *norm* difference the model has — one random axis "reads" at $0.171$ on a member for that reason alone — which is why every AUROC in §5.3 is reported both raw and norm-controlled, and why the two agree to within $0.011$ on the canonical axis.

# Discussion

**What a platform could do with this.** The practical output of five iterations is one score and one protocol for trusting it. The score is 80 forward passes on a frozen 80-item harmful core, no generation, no judge, no benchmark, no reference model, roughly 20 s per checkpoint including download at $\leq$4B; it ranks checkpoints by judged harmful-refusal rate at $\rho \approx 0.69$ across 28 lineages and 11 families. It is a triage instrument, not a certificate: $\rho = 0.69$ leaves ample room for individual checkpoints to be mis-ranked, and the score reads harmful prompts, so an operator still has to hold 80 harmful strings — they just never generate from them, never send them to a judge, and never need a reference model. Against the honest alternative — a few hundred generations plus a judge per checkpoint — that is roughly three orders of magnitude cheaper per model and removes the one operational requirement (an attested reference) that the published abliteration audit needs [14].

**Three named pathologies, and the instances we claim.** Three of this paper's surviving results are measured instances of long-named methodological phenomena rather than new phenomena, and presenting them as discoveries would invite the correct objection [ARTIFACT:art_9sXeYgowURMn]. We name each and claim only the instance.

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

Twenty-six claims from earlier iterations are restated in the shipped artifacts rather than in the sections that first made them, each with the claim as previously stated, the corrected statement, the archived file and key it derives from, and why it moved [ARTIFACT:art_ouNbQqPM59dp]. The substantive items new to this iteration are: the read-versus-act coupling coefficient, demoted from a pooled $0.629$ to a within-axis $0.547$ with an interval covering zero, with the $0.896$ between-axis-type variance share as the reason; the Method's description of the `UNDEFINED` detection gate, which fires on a non-finite bootstrap interval at $\leq 1$ refusal and not at the "fewer than 40 refusals" rule the Method stated, logged as deviation `DEV-ITER5-01` with the three code paths quoted; the axis-A verdict tally, now reported twice (20/1/0/9 over 30 members; 13/1/0/0 over the 14 powered ones) with an attainability footnote establishing that `AT_CHANCE` is unreachable below $n = 80$ per class; the reading claim, narrowed to `READS_CANONICAL_WORDING_ONLY` ($0.897$ canonical versus $0.611$ non-canonical against a random band edge of $0.750$); the abliterated-arm claim, re-carried on refusal rates rather than on four underpowered AUROCs; the minimum axis-A AUROC, which is $0.685$ over the 21 members with a defined AUROC and $0.691$ over the 20 `READS` members, with the bare "$\geq 0.68$" retired; the count of members on which reading is measurable, which is 21 and not 20; a stale top-line summary of 18 `READS` / 0 `AT_CHANCE` / 10 `UNDEFINED`, diagnosed exactly as an intermediate log state with the `AMBIGUOUS` class dropped, which is why it sums to 28; and reference [11], completed to its full eight-author list. Carried forward unchanged: the AMS paraphrase refit (`DOES_NOT_SURVIVE`); the semantic-reversal adjudication (`REVERSAL_DOES_NOT_SURVIVE` at matched contrast, `REVERSAL_SURVIVES` at B's unmatched peak); the archived relative depth of $0.25$; the random-direction null, rescoped to a measured induction floor reaching $0.389$ on 30 checkpoints; the early-warning-signal arm, closed with a direction-specific difference-in-differences of $-2.334$ $[-3.573, -1.037]$ that fails Holm within its 48-test family and would need on the order of 1,880 prompts; the observable-validity gate, which admits 0 model pairs at the layer-$L$ readout and 1 at the final-layer readout; the relaxation-rate claim, withdrawn as non-identifiable on 640 of 640 rows; the $\alpha_{50}$ accounting, where the primary logistic estimator is `DEFINED` on 1 of 19 members and that member is itself excluded; and nine bibliographic corrections against the arXiv API, including reference [45], whose title is *The Geometry of Harmful Intent*.

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

</paper>

<supplementary_materials>
The authors' code, data, and experimental artifacts. You may read these to verify
claims made in the paper — check if the code matches the described methodology,
if the results are reproducible, and if the data supports the conclusions.

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

--- Item 20 ---
id: art_Vag73M9ysCVF
type: experiment
title: A cheap safety score that survives more models
summary: |-
  VERDICT: HOLDS -- the first positive result in this run. The first-decoding-step logit-gap margin read on HARMFUL prompts (our reimplementation of arXiv:2506.24056; 80 forward passes, ZERO generations, zero judge calls, zero benchmark runs, zero reference models per checkpoint) predicts the judged plain-harmful refusal rate at rho 0.694 [0.495, 0.822] at the MEMBER unit (lineage-clustered bootstrap, 10,000 reps, seed 20260812) and 0.564 [0.140, 0.826] at the LINEAGE-AGGREGATED unit, on the SAME frozen 52-member / 28-lineage / 11-family panel that retired the AMS paraphrase refit in iteration 4. 52/52 members scored, zero failures, 14,792 forward passes, 0 generations, $0.00 LLM spend.

  THE DECISIVE DIAGNOSTIC PASSES. The pre-registered archived-19 vs new-33 block split gives rho 0.6673 vs 0.6677, delta -0.0004 [-0.308, 0.380]. Unlike the paraphrase refit, whose advantage was carried entirely by the archived block, this score transfers intact to 21 lineages it was never fitted on. It is not a small-panel correlation artefact.

  IT SURVIVES EVERY PRE-EMPTIVE CONTROL. Partial Spearman controlling for log10(param_count) is 0.676 [0.475, 0.814] and rho(score, log10 params) is only 0.092, so the prediction is NOT parameter count. Leave-one-lineage-out (28 folds) spans [0.661, 0.726] and leave-one-family-out (11 folds) [0.650, 0.772], sign-stable in every fold. AUC 0.806. Monte-Carlo lineage-permutation p sits at the 5.0e-6 floor (200,000 draws; floor quoted beside every p). Disattenuated at kappa 0.3907 alongside -- never instead of -- the raw value.

  IT BEATS THE ANCHOR. Paired on the same resampled lineages, logit_gap_harmful minus our_ams_sigma = +0.421 [0.169, 0.684], SCORE_BETTER. our-AMS sigma itself scores 0.359 member / 0.162 lineage and reproduces iteration 4's archived value on 49/52 members (max |delta| 0.0275, on two L3 Llama members plus one).

  THE HARMFUL REGIME IS LOAD-BEARING, WHICH IS WHY THE HONESTY STATEMENT IS MANDATORY. The benign-regime variant COLLAPSES to 0.129 [-0.168, 0.436], and harmful-vs-benign paired delta is +0.565 [0.205, 0.873]. The saving is 'no generation, no judge, no benchmark, no reference model' -- it is NOT harmful-prompt-free, and that sentence ships verbatim in RESULTS.md and in method_out.json's 'framing' field.

  GATES, ALL GREEN AND ALL ORDERED BEFORE ANY CORRELATION. Byte-identity reuse manifest over 17 lib/ + lib_iter3/ files plus 46 hashed archived inputs; 14 offline apparatus assertions; ORIENTATION_MAP recovered from iteration 3's driver by ast (never imported -- it calls setrlimit at module scope); panel identity 52/28/11 and 19/33 with both calibration members reproducing 0.250 and 0.900; T0-REPLAY reproducing iteration 3's 0.6673 [0.439, 0.904] / 0.929 to 4 decimals; a timestamp-free pre-registration content sha stable across invocations. Recomputing the 19 archived members from the models gives IDENTICAL RANKS (Spearman(iter3, iter5) = 1.000, 0 positions moved), so every Spearman statistic is unchanged by the small numeric drift on 3 members.

  THREE PLAN ASSUMPTIONS WERE MEASURED FALSE AND ARE RECORDED AS PRE-REGISTERED DEVIATIONS: (1) the plan's five UNRELIABLE-flagged members DO NOT EXIST anywhere in iteration 4's archive, so that exclusion set was not invented; (2) 51 of 52 rows carry a revision SHA, not 52 (l1_abliterated has no panel_manifest row, hence also no manifest tokenizer family and no param_count); (3) five members have no empirical refusal-onset lexicon for their tokenizer family -- their primary columns are NULL with reason MISSING_FAMILY_LEXICON, never back-filled, and the pre-registered union-of-all-families SECONDARY column (rho 0.579 member) ships beside them.

  Audit cost: 80 forward passes and 0 generations to score one new checkpoint; median 20.0 s / p90 36.7 s / max 70.1 s per member for all four scores including download on one RTX A4500. Deliverables: method.py (--tier t0/smoke/t2/archive/full, resumable by per-member file existence), lib_iter5/ (ast constant extraction, revision-pinned loader, aggregation and block-split statistics), prereg_iter5.json, 58 result files including per-member JSONs and the archive-only analysis, and summarise.py which renders RESULTS.md deterministically with every number read from method_out.json rather than retyped.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_5/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 21 ---
id: art_3Nid1IyvhfIG
type: evaluation
title: Rechecking the read-versus-act coupling
summary: |-
  PURE REANALYSIS of the frozen iteration-4 read-vs-act tree. $0.00 LLM spend, zero GPU, zero generation; 90 s wall (plus a one-off 453 s simulation, cached in out/sim_raw.json). 174 inputs sha256-stamped, 0 missing. Estimators IMPORTED not retyped (frozen_src/explib.py + lib_iter3/statsx.py, byte-identity 19/19 every run).

  REPRODUCTION GATE: 169/169 legs PASS at 1e-6; G1 (pooled rho 0.629 and its CI at the archived seed) exact to 0.0e+00. G4 re-bootstrapped all 30 per-member axis-A AUROCs/CIs/verdicts from stored projections (24 item-level, 6 summary-level where no proj_*.npz exists).

  H-C VERDICT: COUPLING_IS_AXIS_TYPE_CONTRAST + UNDERPOWERED (both fire, both reported). Within axis A across the 14 powered members rho = 0.547, lineage-clustered CI [-0.031, 0.930] over 7 units, exhaustive 5040-perm p = 0.149 (floor 1.98e-4); lineage unit 0.821 [0.348, 1.000], same sign. An EXACT two-way variance decomposition (balanced 14x5, so orthogonal) attributes 0.896 of the pooled statistic to between-axis-type, 0.036 between-member, 0.069 residual, shares summing to 1.000. Partial rho controlling axis 0.234 [-0.059, 0.397]; both main effects removed 0.126 [-0.240, 0.366]; MixedLM slope on ranks 0.192 [-0.075, 0.458]. NO single axis carries a within-axis coupling (A .547 B .148 C .397 D -.038 E .416, every CI covering 0). Control ladder: 0.629 -> 0.545 [0.284, 0.726] on A+B+E only. The reviewer's 0.434/p=0.14 is REPRODUCED EXACTLY by dropping Llama_3p2_3B_Instruct, the one AMBIGUOUS member; n=14 gives 0.547/p=0.04, but that asymptotic p ignores lineage clustering and the clustered CI covers zero at either n. The within-member mean 0.715 is demoted: same contrast, 14 times, so weaker evidence not stronger.

  H-K: powered-only tally 13 READS / 1 AMBIGUOUS / 0 AT_CHANCE / 0 UNDEFINED of 14; all-30 tally 20/1/0/9, both cross-tabbed by arm with totals asserted. Attainability simulation of the artifact's OWN prompt-clustered bootstrap (141 cells x 2000 replicates x 2000 inner resamples): at true AUROC 0.500 AT_CHANCE is UNREACHABLE below n = 80 per class and P = 0.000 at the pre-registered n = 40 gate (Hanley-McNeil closed form n = 65); P(READS) = 1.000 under perfect separation at every one of n = 7, 12, 28, 32, 33. But P(READS | true 0.500) is only 0.017 at n=5 -- the asymmetry is ONE-SIDED: READS is not noise-driven, the NULL verdict is what cannot be returned. Deviation DEV-ITER5-01 quotes the code: UNDEFINED fires only on non-finite CI bounds (explib.py:486-494) via the >=5-per-class resample guard (explib.py:555-563); MIN_PER_CLASS=40 governs only the separate `powered` flag (gpu_stage.py:342-345). 7 members unpowered yet READS, smallest 6/class.

  ABLITERATED ARM SURVIVES WITHOUT ANY AUROC: median rate 0.0076 vs 0.1131; Mann-Whitney U=13.5, tie-corrected asymptotic p=0.0044 PLUS an exhaustive permutation over all 293,930 assignments p=0.0026 -- the arms share one rate, so scipy method='exact' is INVALID here and its 0.0033 is recorded but never quoted; lineage-clustered bootstrap of the median difference -0.1055 [-0.2416, -0.0245]; paired sign test 10/10, p=0.0020.

  MEASURED CORRECTIONS to the plan: the stale tally is 18+0+10 = 28, two short of 30 (correct 20/1/0/9), carried by iter-4 README.md and its artifact summary, NOT RESULTS.md; censored axis-A c_50 among powered members is 2 of 14 not 7 (0.771 is over all 70 PAIRS); the 6 members lacking proj_*.npz are the *_Instruct/*_Instruct_abliterated six, not BADMISTRAL or the UNDEFINED members; the iteration-3 8-strings-7-lineages trap does NOT recur (exactly 7 distinct lineage_id strings); MixedLM fails under lbfgs (LinAlgError, variance on the zero boundary) and powell converges.

  DELIVERABLES: eval_out.json (schema-validated, 84 aggregate metrics, 4 datasets: gate 169 legs / coupling panel 14 / simulation surface 141 cells / abliterated rates 30), out/replacement_text.md with six drop-in sections whose 97/97 JSON pointers all resolve and zero banned salvage tokens appear, RESULTS.md rendered from the JSON and confirmed byte-identical on re-render, prereg_iter5_eval.json (sha256 b39c230e..., written and hashed before any new statistic), and 3 vector figures (within-axis vs pooled scatter, control-ladder forest at both units, attainability heatmap).

  REUSABLE: bootstrap AUROC in closed form over the sorted item pool (U = sum cp*cumsum(cn) + 0.5*sum cp*cn from cluster multiplicities) is exactly equal to explib.auroc's average-rank definition to 1e-12 and ~50x faster than re-ranking each resample -- that is what made the simulation feasible on 4 cores.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 22 ---
id: art_Y-oGSm04Tcar
type: evaluation
title: Is the refusal axis reading meaning or wording?
summary: |-
  PURE RE-ANALYSIS of the frozen iter-4 read-vs-act tree (art_1xT3w1joqeJ8): no weights loaded, no generation, no steering, no training. 93 s on 4 CPUs, $0.0277 of a $2.00 hard cap (513 billed calls, 147 warm-cache hits, 0 errors; reruns are $0.00 from results/judge_cache_5class_local.jsonl).

  GATE FIRST. R0 regenerates every archived per-member AUROC, its prompt-clustered CI, the within-stratum and per-stratum AUROCs and the paired A-B delta from proj_<KEY>.npz alone, using explib.centre_by_stratum / explib.detection_stats IMPORTED from the archive: 667/667 cells at max|delta| = 0.0, and lib/classify.REFUSAL_RE re-derives the stored labels array byte-identically on all 24 members. DEVIATION (pre-registered fallback): 6 of 30 archived members have a detect json but no proj npz (the archived gpu_stage dumps projections AFTER the detection stats; those six were scored by an earlier pass, mtimes 01:27 vs 02:30) and 3 of them are POWERED, so POWERED-and-available = 11 of 14.

  PART 1 (H-L) VERDICT: READS_CANONICAL_WORDING_ONLY, member AND lineage unit. 660 stratified items (regex label x stratum x projection tertile, middle tertile 2x, IPW back to the item population) re-labelled with the five-class rubric loaded verbatim from RE3/judge_stage.py through ARCH/judge.py. Swapping the label barely moves the pooled AUROC (0.834 [0.736,0.923] regex -> 0.821 [0.752,0.866] semantic; paired DELTA_L -0.013 [-0.067,+0.030] member / -0.024 [-0.066,+0.018] lineage; kappa +0.789 [+0.699,+0.879]), but the SPLIT is decisive: canonically-worded refusals 0.897 [0.864,0.922] vs REFUSAL_NONCANONICAL 0.611 [0.542,0.686], which does not clear the members' own 20-draw random READING band (mean upper edge 0.750 -- chance is NOT 0.500 here).

  NEW MEASURED CAVEAT the paper must carry: the rubric's CANONICAL/NON-CANONICAL split is NOT the regex's split. 54 of 267 items (20.2%) that open with a frozen refusal opener are still called REFUSAL_NONCANONICAL by the judge, and the drift is member-dependent (0/27 Qwen3-1.7B-Base, 17/25 Llama-3.2-3B-Instruct). Taking the rubric class as 'refusals the regex missed' over-counts 83 vs 38. On the sharper subset (semantic refusal AND regex non-refusal) the pre-registered floor of 40 is not met at n=38, so the reportable claim is the pre-registered fallback: weighted corpus prevalence 0.0546 [0.0412,0.0686] -- about 1 scored item in 18 is a refusal the regex of record calls a compliance.

  PART 2 (H-X) VERDICT: LEAKAGE_CONTROL_SMALL_DELTA, both units. Four normalisation protocols on identical items/axes (archived whole-pool centring; fold-internal centring LOPO; fold-internal centre+scale = Mehta's full residualisation; leaky whole-pool z-score), on axes A, B and the norm-matched random D, under BOTH label sets. Axis A DELTA_X = -0.0205 [-0.0352,-0.0071] (centring alone +0.0009; leaky z -0.0205), an order of magnitude short of arXiv:2607.13346's -0.336 on its own data; under semantic labels -0.0397 [-0.0763,-0.0047]. CONTROL ON THE CONTROL holds: the same protocol moves random axis D by only -0.0020 [-0.0084,+0.0032] and axis B by -0.0023, so the axis-A movement is not pure normalisation. 0 fallback folds anywhere. Leakage precondition RE-ASSERTED not inherited: exact axis-fit-string text overlap = 0 on every member (fit strings re-parsed from lib/direction.py), recomputed n_prompt_overlap matches the archive on every member, and a drop-those-items sensitivity column bounds it.

  ALSO SHIPPED: PARTIAL treated three ways (as refusal / as compliance / dropped-primary); judge-error attenuation from the audited 124-item probe of the SAME judge configuration (art_gYmQllaTCGT5 arm2_repaired, sensitivity 0.688 / specificity 0.923 strict); Holm-adjusted per-member p; a rank-normalised pooled AUROC; both aggregation units with both verdict strings everywhere (H-U). DELIVERABLES: eval_out.json (+full/mini/preview, exp_eval_sol_out-validated, 660 examples with both criteria, axis score and IPW weight, and a paper_numbers block every quoted number is read from), results/section_5_1_paragraph.md (f-string-generated, regenerates byte-identically), results/noncanonical_examples.md (20 verbatim boundary cases), results/prereg_eval.json (sha256-stamped before any new AUROC), r0_gate.json, sampling_frame.json, labels5.json, cost_ledger.jsonl and two vector figures.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_5/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 23 ---
id: art_Xx1VPyGi4nAT
type: evaluation
title: Make every paper number check out
summary: |-
  VERDICT: NUMBER_DISCIPLINE_CLEAN_WITH_LOGGED_EXCEPTIONS. 23 s on CPU, $0.00 LLM spend (cost_usd == 0.0 asserted), no GPU, no network. 28 input files sha256-stamped (declared deps plus UNDECLARED_BUT_STAMPED evaluation/paper artifacts); the 8-leg ingest gate reproduces every archived headline to full float repr and PASSED.

  THE CLAIM LEDGER (eval_out.json:metadata.claim_ledger + out/ledger.csv). 911 numeric and verdict-string claims over 142 surfaces; audited on all four number-bearing surfaces (prose, tables, figure captions, figure summaries) plus the abstract. Flags BEFORE repair: MATCH 421 / ROUNDING_OK 200 / UNIT_MISSING 227 / UNTRACEABLE 43 / STALE_SOURCE 13 / DIRECTIONAL_ROUNDING 7 / VALUE_MISMATCH 0. AFTER repair the regenerated prose bundle + abstract skeleton re-audit at 150 claims with 0 flags. UNIT_MISSING = 227 is the load-bearing number: that many claims resolve to a source value while the sentence never names its aggregation unit, and on this paper's own evidence the unit moves oriented rho by a median 0.238 and flips 5 of 16 signs.

  METHOD CORRECTION worth reusing: an unfiltered index over 152,118 numeric leaves resolves almost any 2-decimal number to SOMETHING, producing false MATCHes. A two-tier index is required - 51,178 'reportable' summary-statistic pointers resolve claims, the rest only populate an UNTRACEABLE's search log - plus gating on semantic key-compatibility and per-token type.

  THE THREE DRIFTS, resolved by naming POPULATIONS. (a) min axis-A AUROC = 0.6845 over all members with a defined AUROC (Llama_3p2_3B_Instruct, AMBIGUOUS, 282/282, powered y), 0.6908 over READS members (Llama_3p2_1B_Instruct, 172/172), 0.6845 over powered-and-defined; the bare '>= 0.68' matches none and is flagged DIRECTIONAL_ROUNDING on 7 sentences. (b) 'measurable' is 21, not 20 (20 READS + 1 AMBIGUOUS + 9 UNDEFINED over 30; 14 powered, NOT the plan's expected 13). (c) The stale 18/0/10 is diagnosed exactly, not guessed: it is backfill.log's panel state (18 READS / 2 AMBIGUOUS / 10 UNDEFINED over 30) with the AMBIGUOUS class dropped - which is why it sums to 28 - before rerun_base.log re-ran five base checkpoints under the plain wrapper, moving Qwen2p5_0p5B AMBIGUOUS->READS and Qwen3_0p6B_Base UNDEFINED->READS. A grep for a writer finds report.py:428 emitting RESULTS.md and ZERO writers for README.md (line 16) or the registered summary: one generated tally, one hand-typed stale one, no second live code path. BONUS DEFECT for H-K: the code's UNDEFINED gate is a non-finite bootstrap CI (fires at <= 1 refusal, explib.verdict_from_ci), NOT the Method's '< 40 refusals' (that rule drives the separate `powered` flag, gpu_stage.py:343) - which is why members with 6-33 refusals carry READS while unpowered.

  REGENERATION HARNESS (out/render.py, standalone-runnable). Template {{ptr:ALIAS#/rfc6901|fmt}} over a frozen sha256 registry. SIX executed assertions, all pass: byte-identical twice; 0 unresolved placeholders; 0 bare numerals under a NO_BARE_NUMERAL lint with 12 itemised allow-list entries; 0 flags on the re-audited rendered text; mutation test passed (perturbing a source value changes the output, so pointers are live); the standalone CLI reproduces the bundle byte for byte. Deterministic across two full reruns (runtime excluded).

  TABLES + BIB. out/tables/table_detection_per_member.{md,csv}: 30 rows carrying the two omitted columns 'n refusals / n compliances' and 'powered (y/N)', plus norm-controlled cos and induction, with a totals footer. table_dual_aggregation.{md,csv}: 108 rows, unit named in every row label, incl. the 52-member scale panel; H_G_ROWS=ABSENT_AT_RUN_TIME (iter_5 experiment workspaces empty), so a schema-stable stub with exact row labels and pointer names ships instead - no value forecast. Numbering by first appearance: Table 3->1, 5->2, 2->3, 4->4, 1->5, bijection asserted, 0 dangling refs. Bibliography: 45 entries parsed, [11] completed to its full 8-author list from the audited BibTeX; all 9 citation-audit corrections re-asserted APPLIED (0 web lookups).

  LOGGED EXCEPTIONS (4): 43 UNTRACEABLE on the ORIGINAL draft (15 external-literature values from cited works, 28 internal - each with a search log); 13 STALE_SOURCE sentences owned by H-K; 7 DIRECTIONAL_ROUNDING; H-G absent. 4 claims became DERIVED_NOW_GENERATED via auditable derivation functions (the 2.6e-4 reproduction gap, the AMS Table-I percentage deltas, the verdict-tally sums, the random-null reading band 0.075-0.500).

  DELIVERABLES: eval.py + full/mini/preview_eval_out.json (all schema-valid), out/{ledger.csv, render.py, prose_template.md, prose_bundle.md, abstract_template.md, abstract_skeleton.md, corrected_summary_block.md, references_completed.md, cross_references_renumbered.md, table_numbering_map.json, derived.json, stage*.json, tables/}, tests.py (13/13), README.md rendered from JSON. GEN_PAPER_TEXT can paste out/prose_bundle.md and out/abstract_skeleton.md directly, and re-run out/render.py after any source refresh.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_5/gen_art/gen_art_evaluation_3
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 24 ---
id: art_9sXeYgowURMn
type: research
title: Naming the measurement pathologies, placing the headline
summary: |-
  Primary-full-text dossier for iteration 5. Deliverables: research_report.md (S0-S10) and research_out.json carrying the three ready-to-paste Discussion passages, a 7-row neighbour table, two branch-specific residual-novelty paragraphs, a 25-row query log, and a 16-entry BibTeX block. Every number is a verbatim quote with an anchor or is marked NOT FOUND / NOT OBTAINED / INHERITED.

  THREE FRONT-MATTER RESOLUTIONS. (1) The 2506.24056 coverage conflict is NOT a version drift: 97.5-99.8% (fraction of toxic prompts where the ALIGNED gap exceeds the BASE gap) and 92.1% [89.4-94.2] (Qwen2.5-0.5B's position-1 decision census; Llama 98.8%, gemma 96.0%) are BOTH in v2 and measure different things. Cite 92-99% for position-1 validity, 97.5-99.8% for 'alignment widens the gap'. (2) The 0.464 blocker is RESOLVED from the shipped table, no placeholder needed: ourAMS rho = 0.358 (19 members) vs 0.821 (7 lineages), gap = 0.4636; the -0.929/-0.376 pair (diff 0.553) is a DIFFERENT quantity (oriented Delta, v2 carrier); median 0.238 / max 0.557 / 5-of-16 sign flips is a third. The drafter must name which pair of cells. (3) HURTADO VERDICT: H-G's novelty survives, but the plan's assumed distinction is WRONG - Hurtado's labels come from a behavioural oracle (Qwen3Guard), not a provenance tag, and his rho is explicitly 'one scalar per model'. The four surviving residuals are: attested reference required and spoofable; BINARY label vs graded refusal rate; 4 families vs 11; full weight download required. H-G may NOT claim 'first model-level cheap safety score validated against behaviour'.

  LOGIT-GAP FULLY EXTRACTED (v2, full text). NO cross-model margin-vs-behaviour correlation exists - all 28 correlation matches inspected; every one is token-level, suffix-level, or cited from Bai et al. The abstract's co-variation is 'across suffix strategies' and is self-labelled an internal consistency check. Token lists recovered verbatim. CRITICAL CAVEAT NOT PREVIOUSLY RECORDED: their affirmative token is chosen PER PROMPT as the highest-logit one, making their gap an attack-relevant MINIMUM; a fixed-list max is a different estimand and must be declared.

  CANONICAL SOURCES PINNED AND QUOTED. Leakage = Kapoor & Narayanan L3.3 Sampling bias in test distribution (exact label; L1.2 for the statistics half). Aggregation = Robinson 1950, with the sign flip read out of the paper: nativity x illiteracy is +.118 individual, -.526 (48 states), -.619 (9 divisions) - do NOT use the trio recalled in the plan. Openshaw CATMOG 38 supplies the scale/aggregation definitions and the devastating 'for a 6 region aggregation of the 99 Iowa counties the range of possible correlations is between -.99 and +.99'. Simpson 1951 verified (and Semantic Scholar's 'A. Simpson' is WRONG; the byline is E. H. Simpson). Small-sample = Schoenbrodt & Perugini 2013 with full Table 1: POS_crit at w=.10/80% is 252/238/212/181 for rho=.1/.2/.3/.4, so n=28 is 6.5-9x below stability - state this DELIBERATELY. NEW FIND: a 2018 CORRIGENDUM exists (DOI 10.1016/j.jrp.2018.02.010) and must be cited alongside.

  CORRECTIONS TO OUR RECORDS. Mehta's LOQO figures are 0.43/0.87 in primary text, NOT 0.425/0.870 - quote two decimals. His 0.761 IS verified verbatim, as is the sharper control (AUROC 0.63 on a condition where the effect cannot exist). arXiv:2607.28685's -0.64@n=7 -> +0.02@n=18 is CONFIRMED plus a previously unrecorded and stronger clause: 'a quarter of random size-7 subsets show |rho| >= 0.5'. AMS verified at 14 configs / 4 families / Pearson -0.546 (p=0.043) - but its SPEARMAN is -0.423 at p=0.13, which is the directly comparable statistic and is not significant. NEW NEIGHBOUR: arXiv:2602.09434 (Xu & Sheng), refusal vectors over 76 offspring models at 100% base-family identification - outcome is MODEL IDENTITY, the clean provenance-vs-behaviour distinction the plan expected from Hurtado. arXiv:2603.27412's real title is 'The Geometry of Harmful Intent', not 'LatentBiopsy'.

  SATURATION: the 13 scholarly-mode zeros are NOT credible (OpenAlex returned oncology and climate models); the claim is carried by arXiv-scoped search plus five harvested related-work sections. C1: no work validates such a score against judged behaviour at >=20 lineages or >=10 families; family-axis maximum anywhere is 4. C2: one direct hit only. TALLY for the COLLAPSES branch: 5 of 5 located model-level scores validate at <=4 families, 4 of 5 at <=14 checkpoints, and 0 of 5 use lineage-clustered resampling - lead with that last count.

  NOT RESOLVED: iter-4 references numbered 11 and 23 (the numbered bibliography is in no readable workspace); Moreno-Torres full text (six routes failed, so NO quotation from it exists and it should be demoted to a citation without a quote).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_5/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</supplementary_materials>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the paper's contribution is genuinely novel versus already-done or a known dead end in this field.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<previous_review>
Your review from the previous iteration. Check which critiques have been addressed
in the revised paper. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

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
</previous_review>

<task>
Review this paper as you would for a top-tier venue submission.

STEP 1 — READ THE PAPER: Read it carefully. Note claims, methodology, and results.

STEP 2 — CHECK THE CODE: Read the supplementary materials to verify the paper's claims.
Do the experiments match what's described? Are there discrepancies between code and paper?

STEP 3 — SEARCH THE LITERATURE: Ground your review in evidence.
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes
- What level of contribution gets accepted at top venues in this area?

STEP 4 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would cause rejection) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Provide your review via structured output.
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
  "description": "Adversarial review of the paper draft.\n\nID format: review_it{iteration}__{model}",
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
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "ReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-13 05:17:14 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-web-tools · 2026-08-13 05:18:20 UTC

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
