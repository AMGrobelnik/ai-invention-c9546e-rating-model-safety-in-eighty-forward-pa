# Spec Sheets for Rival LLM Safety Metrics

## Summary

Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.

## Research Findings

# Spec dossier for four rival safety metrics, the refusal observable, the EWS toolkit, and a full citation audit

The complete artifact is `research_report.md` (six sections, ~1,300 lines, every number
anchored). This is the synthesis.

## 1. The novelty question, answered first because it is the most consequential

**No prior work applies early-warning signals / critical slowing down to LLM generative
dynamics.** arXiv's own abstract-field search returns **zero** results for
`"critical slowing down" AND "language model"` [20]; the cs.LG sweep returns only
lattice-QCD and diffusion-sampling work [21], and the scholarly sweeps return the
ecology/depression EWS canon with no LLM application.

Two qualifications must nonetheless be written into the paper, because a reviewer will
find them:

- **arXiv:2605.09043** (ACL 2026 SRW) applies critical-slowing-down signatures - variance
  rise before a saddle-node bifurcation, with hysteresis - to **conversation derailment
  in human dialogue corpora** (CGA-Wiki N=652; CGA-CMV N=1,169), with effect sizes
  d=0.20-0.36 [18]. It is CSD on *text-level dialogue*, not on model internals, and it
  uses **variance** rather than the slowing-down indicators proper (AC1, recovery rate).
  Distinct, but adjacent enough that omitting it looks like a failed search.
- **AQI (arXiv:2506.13901)** is a **fifth competitor the hypothesis does not cite** [19]:
  a prompt-invariant intrinsic alignment diagnostic via latent geometry, explicitly
  pitched as "beyond refusals" and motivated by alignment faking. It occupies our exact
  product niche and must appear in related work.

## 2. The four baselines are now reimplementable

**AMS** [1] is fully specified. Its statistic is a Cohen's-d-like standardised mean
difference of projections onto the diff-in-means direction, `sigma = (mu+ - mu-)/sigma_pooled`,
read at the **final prompt token**, layer chosen by a sweep over the **40-80% relative-depth
band** - a relative-depth rule that transfers to our small models. Total cost is
**96 forward passes, 10-40 s on an A100**, so it is CPU-easy (~3-8 min per 1B model).
Crucially, **three checkpoints in our panel appear in AMS Table I** - Llama-3.2-3B-Instruct
(8.37), gemma-2-2b-it (4.80), Llama-3.2-1B-Instruct (4.55) - giving us a genuine validation
gate for our reimplementation. The 71% figure is **10/14 under leave-one-model-out**, and
**both** calibration rules (sigma_harmful only; worst-concept minimum) give identically 71%.

**The H4 quote is real and carries no hedge**, verbatim: *"This class of modification is
currently undetectable by activation-only probing of mid-residual-stream representations;
we treat it as the principal limitation of the approach."* [1]. Preserve the scope
qualifier "activation-only ... mid-residual-stream" - it is exactly what makes a
logit-space, generation-time observable non-trivial. Two headline numbers verified
(r=-0.546, p=0.043), plus one the hypothesis omits and should not: the **Spearman
rho=-0.423 is not significant** (p=0.13).

**RAS/SafeVec** [2] is fully specified including **every published calibration constant**
(tau=0.8, q=0.9, lambda=0.5, w_u=w_j=0.5, sigmoid centre c=0.75, steepness beta=5.0).
That sets the bar for our own FROZEN SPI constants: RAS publishes all of its, so we must
publish all of ours. But **the overlap between RAS-published models and our panel is
EMPTY** - RAS reports only Llama-3.1-8B, Gemma-3-4B and Qwen2.5-7B families, all >=4B,
none in our panel. **We must write "our RAS reimplementation" throughout and state
explicitly that no published RAS score exists for any model we evaluate.** Two further
findings: RAS is judge-free only at *target-scoring* time - its calibration **requires ASR**,
hence generation and a judge; and its speed-up claim is **internally inconsistent** (216.88x
in text, 210.13x in Table 2 - mean-of-ratios versus ratio-of-means).

**VISAGE** [3] is `E[S_max - S(alpha)]` over `alpha ~ U(-0.5, 0.5)` along filter-normalised
Gaussian weight directions, with **3 directions x 20 steps x 80 AdvBench prompts**. The
cost arithmetic is decisive: **4,800 generations per model, ~614k forward passes,
~28 hours per 1B model on 4 vCPU - infeasible**. The dossier specifies a reduced but
faithful variant (2 directions x 9 alpha-steps x 32 prompts x 48 new tokens ~ 1.3 h/model)
with an explicit table of what each reduction costs in fidelity - chiefly the ability to
resolve *basin width*, since the step-like drop is localised and a coarse grid can straddle it.

**Qi et al.** resolves to **arXiv:2406.05946** [4]. The per-position KL values in their
Figure 1 are not stated numerically in the text, so I did **not** invent them. What is
firmly pinned is the authors' own operationalisation of shallow depth: their regularizer
uses **beta_t = 2 for t <= 5 and beta_t = 0.1 for t > 5**, with an appendix ablation
defending "the first 5 tokens". **k = 5** is therefore a design decision the authors made
and defended, not a number read off a plot.

## 3. The discriminating test, pre-registered

Both accounts predict a base-vs-instruct difference in the step-wise lambda profile; they
differ in *where it lives*. The token-depth account says the aligned/unaligned difference
is spent in the first ~5 tokens and decays; the basin account says lambda is a property of
the dynamical system and persists. Hence:

> **PR-1.** Delta-lambda(t) must remain significantly non-zero (bootstrap 95% CI excluding 0)
> for **t > 15 = 3 x Qi's k=5**, evaluated over generated steps 16 through 48. If Delta-lambda dies for all
> t > 15, the token-depth account suffices and the basin framing has not earned its keep -
> report that as a negative result rather than moving the cut. Conservative replicate at t > 20.

15 is chosen as the largest cut that clears Qi's decay length by a comfortable multiple
while staying inside our estimator's reliable range - because, as section 4 shows, the
recovery fit itself degrades past ~t=31 at representative noise levels.

## 4. The estimator toolkit, with measured rather than remembered corrections

The EWS recipes are grounded in the Scheffer lineage - *Early-warning signals for critical
transitions*, Nature 461, doi:10.1038/nature08227 [22] - operationalised through Dakos et al.
2012 [15] and the `ewstools` source [16], which gave the de-facto community defaults read
from code: **Gaussian detrend with
bandwidth = 20% of series length** (`sigma = (0.25/0.675) x bw_num`, mirroring R's
`ksmooth`), **rolling window = 25%**, lag 1, Kendall tau as the trend statistic. Notably,
**ewstools applies no small-sample bias correction to AC1 at all** [16].

The *direction* of the bias is documented: Krone, Wichers & Hamaker report that r1 is biased
for small samples, especially for positive autocorrelation, and that closed-form estimators
are biased and/or high-variance for T<=50 [17]. But I could not confirm the analytic
`-(1+3rho)/n` attribution in a primary source, so rather than paraphrase it from memory I
**measured it** (`estimator_check.py`, 4,000 reps/cell,
fixed seed). The results decide a design constraint:

| n | rho | raw AC1 bias | raw SD | bias after +(1+3r)/n |
|---|---|---|---|---|
| 64 | 0.9 | **-0.0638** | 0.077 | **-0.0090** |
| 192 | 0.9 | -0.0195 | 0.036 | **-0.0005** |

The correction is *empirically* correct even though the citation is unconfirmed, and the
confound the plan anticipated is real and quantified: **a 192->64 difference in effective
series length alone manufactures a spurious AC1 gap of ~0.04, with the same sign as "less
critical slowing down"**. Mitigation is mandatory and threefold - apply the correction,
truncate to a common length before comparison, and report effective length as a covariate.

Two further measured hazards. **The AR(1)->lambda conversion is convex, so the downward
bias in phi becomes an upward bias in lambda: at n=64, phi=0.9, uncorrected lambda is
inflated by 75%** - precisely in the slow-recovery regime that critical slowing down
predicts. And **noise-floor truncation is severe and one-sided**: extending the recovery
fit window past the point where the ensemble-mean deviation crosses the noise floor
under-estimates lambda by **40%** (measured: true 0.150, fitted 0.0896 at window 64 with
the floor crossed at t~31.5). The dossier gives a stopping rule and a hard floor of
n_min = 64 below which lambda is not reportable.

For false positives, Dakos et al. supply a directly reusable null: **best-fit ARMA
surrogates of the detrended residuals, 1,000 draws, observed Kendall tau compared to the
surrogate distribution** [15]. Our ensemble detrending (subtracting the across-rollout mean
trajectory) is **not** discussed in that literature - flagged as an adaptation, defended on
the grounds that it eliminates the bandwidth hyperparameter that Dakos Fig. 10 shows is
exactly where EWS conclusions are fragile, with the ewstools-default Gaussian detrend
retained as a mandatory robustness check.

## 5. The refusal observable is adopted, not coined

Yin et al. [5] define the **refusal score as a linear probe's predicted probability**,
traced across token positions - and the critical prompt-vs-generated question resolves in
our favour: **the positions are generated tokens** (the thinking chain), with the cliff at
the final tokens before output. So our r_t is a legitimate adoption; what is new is the
*dynamical statistics* computed on it, in ordinary autoregressive generation rather than a
reasoning chain. Arditi et al. [6] contribute the *behavioural* screen (binary substring
matching, not a continuous readout) and, in Figure 9, direct precedent for reading refusal
onset off the next-token distribution. The verbatim 12-entry refusal-substring list was
transcribed from source code [7]; note AMS restricts matching to the **first 250
characters**, which is the better protocol and should be adopted with attribution [1].

The **abliteration-invariance argument** is grounded: Arditi's edit is applied "across all
layers and all token positions ... prevents the model from ever representing this direction
in its residual stream" [6], and AMS measures the cosine falling to 0.30 [1]. So a
projection-onto-direction observable is driven toward a constant by construction - but
honestly caveated, since AMS's rotation-without-collapse class leaves cosine at 0.83.

A **tokenizer hazard** is flagged with a runtime resolution recipe: leading-space variants
are different token IDs in every BPE vocabulary, so the refusal-onset set must be resolved
per tokenizer at runtime and the resolved surface forms logged, never hard-coded as IDs.

## 6. Citation audit: all 16 anchors resolve; the missing one is found

**Every arXiv ID in the hypothesis resolves with matching title and authors. None was
fabricated; no author was misattributed.** Beyond metadata, the specific attributed claims
were checked, and the two most load-bearing both survive:

- **Kwon (2607.14147)** [8] - *both* H1 claims verbatim, including the base-model control
  (64%->25% harmful content vs a matched control's 64%, replicated at 7B). H1's
  forced-prefix-residual rationale needs no rewriting.
- **Ratnakar & Vats (2606.22686)** [11] - both topology names and the depth figure
  verbatim: Llama-3.1 "Late Decision" identical for 95% of layers; Qwen-2.5 "Early
  Divergence" at "~40% depth". Step 0(a)'s relative-depth rule is anchored.

**The unanchored knowledge-action-gap result is found: arXiv:2603.18353** (Basu et al.)
[14], with both quoted numbers verbatim - **98.2% probe AUROC vs 45.1% output sensitivity**,
a 53-pp gap over 400 physician-adjudicated vignettes - plus the SAE detail (**zero effect
despite 3,695 significant features**). Hasan & Biswas [12] yielded the exact figure the
hypothesis asserted without one: **r = -0.032, p = 0.89**. Mishra et al. [9] do *prove*
non-surjectivity, with the qualifier "under practical assumptions" that must be preserved.
Xiong et al. [13] verify H2b's strongest support: benign-derived steering vectors drive ASR
"to over 80% on standard benchmarks" and the paper frames this explicitly as erosion of the
"safety margin", which is what licenses the double-sided reading rather than a one-way one.

Only two claims need rewriting, both minor: the **ICLR 2025 "Oral"** designation is not
verifiable from the arXiv record, and any single-number citation of RAS's speed-up should
become "~210x (Table 2; the text states 216.88x)".

## 7. The recommendation the plan did not anticipate

**SRI (arXiv:2602.02600) should be promoted from a citation to a baseline** [10]. It is a
per-generated-step scalar bounded between 0 and 1, built from mean-pooled last-layer activations with
harmful/harmless prototype anchors and a cosine-distance log-ratio through a sigmoid -
structurally the nearest existing rival to our r_t. It differs in three statable ways
(activation-distance vs logit space; requires labelled anchor sets; reports a
threshold-crossing count rather than CSD statistics), and it runs on hidden states we are
already extracting, so the marginal cost is two anchor forward passes plus O(d) per step.
Omitting it is the most likely "why no comparison to X" review comment.

## Confidence and limitations

**High confidence** on: the four method specs (all read from primary full text, formulas
transcribed with section anchors); the empty RAS overlap and non-empty AMS overlap; the
H4 quote; Qi's k=5; the measured estimator biases (my own deterministic simulation); and
the citation audit verdicts.

**Explicitly incomplete, stated rather than papered over**: Qi's Figure-1 per-position KL
values are not in the text (mitigated by recommending we measure the curve ourselves -
it is two teacher-forced passes, ~10-25 min/model); the `-(1+3rho)/n` *attribution* is
unconfirmed though the correction is validated by simulation; the AdvBench/Zou verbatim
list was not retrieved (the JailbreakBench list is transcribed and suffices); RAS's prompt
sizes, layer thresholds and per-family constants are simply not published, so RAS is not
reproducible end-to-end; Yin et al.'s exact probe layer is unstated; and Hartigan's dip
test is not present in Dakos et al. 2012.

What would change these conclusions: locating the ICLR/OpenReview record for Qi et al.;
retrieving Qi's Figure-1 underlying data; or finding an EWS-on-LLM paper indexed outside
arXiv abstracts (a full-text rather than abstract search would be the next check).

## Sources

[1] [Messenger, Detecting Safety Training Modification in Language Models via Activation Analysis (AMS)](https://arxiv.org/abs/2608.05578) — AMS full spec: separation = (mu+ - mu-)/sigma_pooled on diff-in-means direction, final-token hidden state, 40-80% depth sweep, 16 contrastive pairs x 3 concepts, PASS>3.5/WARN 2.0-3.5/CRIT<2.0, 96 forward passes in 10-40s on A100. Verified 71% LOOCV (10/14, both rules), r=-0.546 p=0.043, Spearman rho=-0.423 n.s., 14-model table, four-class taxonomy, and the verbatim H4 'undetectable by activation-only probing' quote. Venue confirmed IEEE Access 14:91723-91737, doi:10.1109/ACCESS.2026.3704057.

[2] [Huang, Chen, Yu, Lee, RAS: Measuring LLM Safety Through Refusal Alignment (SafeVec)](https://arxiv.org/pdf/2606.25750) — Full five-stage SafeVec spec with every published calibration constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0); layer windows Llama 22-30 / Gemma 27-29 / Qwen 22-26; reference models Llama-3.1-8B-Instruct, gemma-3-4b-it, Qwen2.5-7B-Instruct; Table 1 raw scores + ASR for 8 Llama checkpoints; runtime table (210.13x table average vs 216.88x in text). Established the EMPTY overlap with our panel.

[3] [Peng, Chen, Hull, Chau, Navigating the Safety Landscape (VISAGE), NeurIPS 2024](https://arxiv.org/pdf/2405.17374) — VISAGE = E[S_max - S] over alpha~U(-0.5,0.5); filter-normalised Gaussian directions (Eq.2); 20 interpolation steps per axis; 3 random directions (stability test used 8); Adv-80 AdvBench prompts scored by refusal-keyword ASR; top-p=0, temp=1; published VISAGE 77.37-90.40 and Adv-520 ASRs. Supplied the cost arithmetic (4,800 generations/model full).

[4] [Qi et al., Safety Alignment Should Be Made More Than Just a Few Tokens Deep](https://arxiv.org/pdf/2406.05946) — ID verified for the by-name-only citation. Per-token KL between aligned and base model on Harmful HEx-PHI (330 instructions); operational shallow depth pinned at k=5 tokens via beta_1=0.5, beta_t=2 for 2<=t<=5, beta_t=0.1 for t>5; data augmentation samples k~Uniform[1,100]. Basis for the pre-registered step-15 discriminating cut.

[5] [Yin et al., Refusal Falls off a Cliff: How Safety Alignment Fails in Reasoning?](https://arxiv.org/pdf/2510.06036) — Refusal score = linear probe's predicted probability of refusal, traced across token positions in the reasoning chain; resolved the critical prompt-vs-generated question in our favour (positions are GENERATED thinking tokens, cliff at final tokens before output). Establishes our r_t as adopted rather than coined.

[6] [Arditi et al., Refusal in Language Models Is Mediated by a Single Direction, NeurIPS 2024](https://arxiv.org/pdf/2406.11717) — refusal_score is binary substring matching (not continuous); orthogonalisation applied at all layers and all token positions - the abliteration-invariance argument; Figure 9 top-10 next-token probabilities for Gemma 2B IT across harmful vs harmless is prior art for a logit-space refusal-onset readout.

[7] [Arditi et al. refusal_direction repo - evaluate_jailbreak.py](https://raw.githubusercontent.com/andyrdt/refusal_direction/main/pipeline/submodules/evaluate_jailbreak.py) — Verbatim 12-entry _test_prefixes_jailbreakbench refusal-substring list plus substring_matching_judge_fn (case-insensitive, whole-completion match) and the LlamaGuard2 <15-word length filter. Directly reusable for the Step-3 string screen.

[8] [Kwon, Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak](https://arxiv.org/abs/2607.14147) — Verified BOTH load-bearing H1 claims verbatim: probe reads harm 0.91-0.98 while behavioural refusal drops to chance; and the base-model control (64% to 25% harmful content vs matched control's 64%, replicated at 7B) showing the prefill grip is generic autoregressive conditioning.

[9] [Mishra, Khashabi, Liu, Steered LLM Activations are Non-Surjective](https://arxiv.org/pdf/2604.09839) — Confirmed the paper PROVES (not merely demonstrates) non-surjectivity - 'Under practical assumptions, we prove that activation steering pushes the residual stream off the manifold' - with the assumption qualifier that must be preserved. ICLR 2026 Workshops.

[10] [Rahimi et al., Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models (SRI)](https://arxiv.org/pdf/2602.02600) — Full SRI definition: mean-pooled last-layer activations phi_t, harmful/harmless prototype anchors, cosine-distance log-ratio through a sigmoid to give sigma_t in [0,1] per generated step; plus Internal Recovery Rate Def.1. Verified the autoregressive-commitment claim verbatim. Basis for recommending SRI as a baseline.

[11] [Ratnakar, Vats, The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs](https://arxiv.org/pdf/2606.22686) — Verified both topology names and the depth figure verbatim: Llama-3.1 'Late Decision' processes harmful and safe queries identically for 95% of layers (95% ASR in ~1s); Qwen-2.5 'Early Divergence' integrates safety at ~40% depth. Anchors the relative-depth layer-transfer rule. TrustNLP 2026 @ ACL.

[12] [Hasan, Biswas, The Refusal-Compliance Tradeoff](https://arxiv.org/pdf/2605.05427) — Verified the 21-model audit and recovered the exact correlation the hypothesis asserted without a number: over-refusal and harmful compliance are nearly uncorrelated, r = -0.032, p = 0.89 (OR-Bench, Llama-70B judge). Also judge-instability data (ORR agreement r=0.990 vs HCR r=0.356).

[13] [Xiong et al., Steering Externalities](https://arxiv.org/abs/2602.04896) — Verified >80% ASR from benign-derived steering vectors and the explicit 'erodes the safety margin' framing supporting H2b's double-sided reading.

[14] [Basu et al., Interpretability without actionability: mechanistic methods cannot correct language model errors](https://arxiv.org/abs/2603.18353) — FOUND the previously unanchored knowledge-action-gap citation. Verified both numbers verbatim: 98.2% probe AUROC vs 45.1% output sensitivity (53-pp gap) on 400 physician-adjudicated clinical vignettes (144 hazards, 256 benign); SAE feature steering produced zero effect despite 3,695 significant features. Model: Qwen 2.5 7B Instruct.

[15] [Dakos et al. 2012, Methods for Detecting Early Warnings of Critical Transitions in Time Series, PLoS ONE 7(7):e41010](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0041010) — The EWS methods paper. Supplied: the three equivalent AC1 estimators (ACF rho_1, conditional-least-squares AR(1) alpha_1, return rate 1/alpha_1 or 1-alpha_1); Gaussian-filter detrending with rolling windows of half the series length; DFA requiring >100 points; conditional-heteroskedasticity recipe at 10% windows; BDS test as a false-positive guard; Kendall tau as the trend statistic; and the surrogate null procedure (best-fit ARMA on residuals, 1000 surrogates, P from the tau distribution).

[16] [ewstools source (Bury), JOSS doi:10.21105/joss.05038](https://raw.githubusercontent.com/ThomasMBury/ewstools/main/ewstools/core.py) — De-facto community defaults, read from code rather than prose: detrend(method='Gaussian', bandwidth=0.2) with sigma=(0.25/0.675)*bw_num mirroring R ksmooth/earlywarnings; rolling_window=0.25; lag=1; Kendall tau via corrwith. Also established that ewstools applies NO small-sample bias correction to AC1.

[17] [Krone, Wichers, Hamaker, A comparative simulation study of AR(1) estimators in short time series](https://pmc.ncbi.nlm.nih.gov/articles/PMC5227053/) — Documents that r1 is biased for small samples, especially for positive autocorrelation, and that closed-form estimators are biased and/or high-variance for T<=50; catalogues the bias-corrected r1 variants. Grounds the direction of the AC1 bias that our simulation then quantified.

[18] [Litchiowong, Phase Transitions in Affective Meaning Divergence, ACL 2026 SRW](https://arxiv.org/abs/2605.09043) — The closest prior art found: critical-slowing-down signatures (variance rise, saddle-node bifurcation, hysteresis) applied to conversation derailment on CGA-Wiki (N=652) and CGA-CMV (N=1,169). Text-level human dialogue, not model internals - narrows but does not defeat our novelty claim.

[19] [Borah et al., Alignment Quality Index (AQI)](https://arxiv.org/abs/2506.13901) — A fifth competitor in our product niche that the hypothesis does not cite: prompt-invariant intrinsic alignment diagnostic via latent geometry and cluster divergence, explicitly motivated by the failure of refusal rates and alignment faking. Must appear in related work.

[20] [arXiv API abstract search: 'critical slowing down' AND 'language model'](http://export.arxiv.org/api/query?search_query=abs:%22critical%20slowing%20down%22%20AND%20abs:%22language%20model%22) — Returned ZERO results - the primary novelty evidence that no prior work applies critical slowing down to language-model dynamics. Companion queries over cs.CL and cs.LG returned only the dialogue paper and lattice-QCD/diffusion-sampling work.

[21] [Del Bono, Biroli, Charbonneau, Gabrie, The critical slowing down in diffusion models](https://arxiv.org/abs/2605.12597) — Checked as a possible novelty collision: it concerns score-model training and sampling near criticality in the O(n) model of statistical field theory, not generation dynamics or safety. Not a collision.

[22] [Scheffer et al. 2009, Early-warning signals for critical transitions, Nature 461](https://www.nature.com/articles/nature08227) — Confirmed title and DOI 10.1038/nature08227 for the lineage citation.

## Follow-up Questions

- Qi et al.'s Figure 1 per-token KL curve is not transcribed numerically in the text - should the experiment reproduce that curve on our own base/instruct pairs (two teacher-forced forward passes per pair, ~10-25 min per model on CPU) so the pre-registered step-15 cut is self-contained rather than importing a decay length measured on 7B Llama-2/Gemma into a panel of sub-4B models with different tokenizers?
- RAS's calibration requires ASR (hence generation and a judge) and its per-family constants b_a, alpha_a and gamma_a are unpublished - is the paper's own documented fallback path (gamma_a=1, b_a from the 0.9-quantile branch specified for empty high-risk sets, with our abliterated/base variants as anchors) an acceptable reimplementation, or does the RAS comparison need to be reframed as rank-correlation-only to avoid depending on unpublished constants?
- Given that arXiv:2605.09043 already applies critical-slowing-down signatures to conversation derailment using variance, does our contribution need to demonstrate that AC1 and recovery rate (the slowing-down indicators proper) carry signal that variance alone does not - i.e. should a variance-only ablation become a required control rather than an optional one?

---
*Generated by AI Inventor Pipeline*
