# Who Already Measured Steering Strength?

## Summary

Saturation-and-positioning dossier for the steering-strength-as-measurement lane. Deliverables: research_report.md (8 sections) and research_out.json carrying a 16-paper machine-readable F1-F5 table, four ready-to-paste paragraphs, and a 12-item consequences list. Every number is a verbatim quote with an [arXiv:ID section] anchor or marked NOT FOUND IN PRIMARY TEXT.

SATURATION VERDICT: (b) ADJACENT WORK EXISTS. Nearest neighbour is Logit-Gap Steering (arXiv:2506.24056, Palo Alto Networks, preprint): 'the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step' = 'the per-prompt safety margin that alignment provides'. Same conceptual object as alpha_50, different units. NOT identical: toxic prompts only (all 520 AdvBench), position-1 only (their own coverage 92.1% [89.4-94.2], residual on multi-token preambles), per-prompt. Residual that is ours: benign-only, generation-level, model-level, NORM_L-normalised, paired instruct-minus-abliterated. Withdraw any 'first scalar measuring refusal's operational margin' sentence.

BIGGEST CORRECTION: arXiv:2602.02712 (ICML 2026) is NOT a threat to the logistic fit - it is a theoretical endorsement. Theorem 3.6: target-concept probability 'is increasing in alpha'; Figure 4: increases 'with a sigmoidal shape'. The non-monotonic 'bump' of Theorem 3.3 is PER-TOKEN and for OFF-TARGET concepts; cross-entropy is locally quadratic (Thm 3.8). The real non-monotonicity threat is empirical coherence collapse (Rogue Scalpel, Falcon).

GALEONE SAYS MORE THAN ASSUMED. Two abstract sentences absent from the brief: they test and REJECT the cosine as a steerability predictor ('a signature of the dissociation, not a control dial') and propose a functional criterion - the steerable case is where the intervention direction also detects (format AUC~1 vs hallucination AUC~0.7). Our 0.69-AUROC axis that DOES steer is a counterexample; report as 'in tension with', not 'refutes'. Their detection axis is prompt/lm_head and intervention axis is lm_head-only, so our result is an EXTENSION (both our axes activation-derived), not a replication. Free gifts: 'alpha does not transfer across models (Gemma needs 15, Llama needs |1|, Qwen needs 5)' supports H1'''; '0/100 random directions' at matched norm validates our null design; format steering works at '0.6% of the activation norm'.

ROGUE SCALPEL DOES NOT WEAKEN THE NULL (author correction: Korznikov et al., NOT Kaminski). Identical calibration to ours - 'alpha = c*mu^(l)', c in {0.25...2.0} - so no conversion needed. Their effects live at 25-200% of activation norm vs 0.6% for a working intervention. 1-13% is a per-draw AVERAGE over 1,000 draws, not best-of-N. They never test random-induced REFUSAL on BENIGN prompts. No numeric lower floor exists in their text.

BEST UNPLANNED FIND: arXiv:2608.08159 shows a 'steerability emerges with scale' result is manufactured by raw units and dissolves under exactly our normalisation ('alpha = c||h||_l', 'h' = h + c||h||_l d_hat'), warning the trend 'depends jointly on raw units, the readout metric, and the operating point; correcting any one of these removes it'. NORM_L is now a requirement, not a convenience - but we must also state what we do about readout metric and operating point.

COMPETITOR NAMED: 'Has This Checkpoint Been Abliterated?' (arXiv:2607.01854) separates '57 public abliterations from 37 benign fine-tunes' at 'AUROC 0.95' on a '273-checkpoint registry' using activation refusal-gap + weight-recovery energy. It 'presumes an attested reference'; alpha_50 does not. No steering-strength abliteration metric exists.

VENUES VERIFIED: 2602.02712=ICML 2026, 2608.08383=COLM 2026, 2607.23519=AIES 2026, 2606.22686='Accepted at TrustNLP 2026 (ACL 2026)', 2605.09043=ACL 2026 SRW. Title changes flagged: 2509.13450, 2508.21448, 2605.09043, 2606.22686. All others preprints.

## Research Findings

SATURATION VERDICT: (b) ADJACENT WORK EXISTS.

The nearest neighbour to alpha_50 is Logit-Gap Steering [3,4], which defines "the difference between the top refusal-token logit and the top affirmative-token logit at the first decoding step" as "the per-prompt safety margin that alignment provides". That is the same conceptual object as alpha_50 - how much push before refusal loses the argmax - measured in logit units. It is NOT functionally identical: it is computed on toxic prompts (all 520 AdvBench prompts), at position 1 only (their own position-1 coverage is "92.1% [89.4-94.2]", with the residual on multi-token preambles), and it is per-prompt. What remains ours: benign-prompts-only measurement, generation-level rather than position-1 operationalisation, a model-level rather than prompt-level score, per-model NORM_L normalisation, and the paired instruct-minus-abliterated design.

Five findings change the paper beyond that verdict.

(1) The plan's "methodology threat" is the opposite of a threat [6,7]. arXiv:2602.02712 is ICML 2026 accepted, and its Theorem 3.6 states the target-concept probability increase "is increasing in alpha", with Figure 4 describing it as increasing "with a sigmoidal shape". The famous non-monotonicity is a per-token "bump" (Theorem 3.3) that applies to individual tokens and off-target concepts, plus a locally quadratic cross-entropy (Theorem 3.8). For the aggregate target-concept dose-response curve alpha_50 is fitted on, this paper is a theoretical argument that a logistic fit is the RIGHT functional form. The practically relevant non-monotonicity is instead empirical and comes from the Rogue Scalpel: "the relationship is non-monotonic for Falcon model: excessive coefficients degrade output coherence, producing nonsensical responses that we classify as safe" [9].

(2) Galeone et al. say more than the plan assumed, and part of it cuts against us [1,2]. They explicitly test and reject the reading that the cosine predicts steerability - "The cosine is a signature of the dissociation, not a control dial" - and propose a functional criterion instead: "The test is whether the intervention direction - the one that steers - also works as a detector. For format it does... For hallucination it does not (AUC ~ 0.7)". Our 0.69-AUROC response-contrast axis that DOES steer is a counterexample to that criterion. Report it as "in tension with", not "refutes", since it is a cross-behaviour, cross-model comparison. Their detection axis is prompt-activation-derived or lm_head-derived and their intervention axis is lm_head-only, so our result is an EXTENSION along a new dimension (both of our axes are activation-derived), not a replication.

(3) The Rogue Scalpel does not weaken our null, and the magnitude arithmetic is decisive [8,9]. Their calibration is identical to ours - "alpha = c*mu^(l)" where mu is "the average activation norm at layer l", with "c ... selected from (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)" - so no conversion assumption is needed. Their effects live at 25-200% of the activation norm. A purposeful, fully effective steering intervention operates at "0.6% of the activation norm" [2]. The 1-13% figure is a per-draw AVERAGE over "1,000 vectors of each type", not a best-of-N maximum. And they never test random-direction-induced REFUSAL on BENIGN prompts - their construct is harmful compliance on JailbreakBench prompts. Our null is untouched as a matter of construct and only needs magnitude scoping. No numeric lower no-effect floor exists in their text: c=0.25 is merely the smallest coefficient tested.

(4) The strongest methodological find was not on the plan's radar [10]. arXiv:2608.08159 shows a headline steering result ("steerability emerges with scale") is manufactured purely by raw activation units and dissolves under exactly our normalisation: "we express strength as a fraction of that norm, alpha = c||h||_l, which makes the intervention comparable across scales", with the injection "h' = h + c||h||_l d_hat". This converts NORM_L normalisation from a convenience into a citation-supported requirement. It also warns that the trend "depends jointly on raw units, the readout metric, and the operating point; correcting any one of these removes it" - so we must state what we do about the other two before presenting any alpha_50-vs-scale claim.

(5) The abliteration-metric lane has an incumbent that is NOT steering-based [11,16]. "Has This Checkpoint Been Abliterated?" [arXiv:2607.01854] combines "a reference-anchored activation refusal-gap and a weight-recovery energy of the base-to-candidate weight difference" to separate "57 public abliterations from 37 benign fine-tunes, merges, and instruction-tunes at AUROC 0.95" on a "273-checkpoint registry". It is our closest product competitor; our differentiator is that it "presumes an attested reference" and alpha_50 does not. Together with AMS and RAS/SafeVec, the lane is occupied by activation-geometry and weight-space methods - a steering-strength answer to "how abliterated is this checkpoint" does not exist in the searched literature.

CONFIDENCE AND LIMITATIONS. High confidence on everything read from primary full text via repeated fetch_grep (all Galeone numbers; the Logit-Gap definition, prompt dependence and position-1 scope; the Rogue Scalpel calibration, c-grid, 1,000-draw averaging and construct; arXiv:2602.02712 Theorems 3.3/3.6 and its ICML 2026 venue; arXiv:2608.08159's formulae). Medium confidence on secondary papers read at abstract level only - these are marked NOT FOUND IN PRIMARY TEXT where relevant and must be checked against PDFs before their numbers are quoted. Two known gaps: the Rogue Scalpel's OpenReview venue/decision was not fetched, and arXiv:2603.24543's +57%/-50% ASR figures are unverified here. Important caveat on the saturation check: scholarly mode (OpenAlex/Crossref) was largely useless on this topic - "steering coefficient threshold refusal" returned bovine-nutrition papers about steers, and "benchmark-free safety evaluation open-weight checkpoint" collided with immune-checkpoint oncology - so the arXiv API carried the saturation check. Non-arXiv venues (ACL Anthology-only, OpenReview-only workshops) are therefore under-sampled, and the verdict should be read as "no equivalent found on arXiv", which is weaker than "no equivalent exists".


## Sources

[1] [Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models (Galeone et al., arXiv:2606.24952)](https://arxiv.org/abs/2606.24952) — Abstract, authors, date, preprint status. Detection-intervention gap; the two abstract sentences absent from the planner brief (cosine does NOT predict steerability).

[2] [Galeone et al. full HTML text](https://arxiv.org/html/2606.24952v1) — All cosines, AUCs, four-model table, alpha non-transfer, matched-norm random controls, 0.6%-of-activation-norm magnitude, functional steerability criterion, limitations.

[3] [Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness (Li & Liu, arXiv:2506.24056)](https://arxiv.org/abs/2506.24056) — Verbatim abstract; the collision candidate. Definition of the refusal-affirmation logit gap as the per-prompt safety margin.

[4] [Logit-Gap Steering full HTML text v2](https://arxiv.org/html/2506.24056v2) — Palo Alto Networks affiliation; AdvBench n=520 dependence; median gap shifts per family; position-1 coverage 92.1%; token-list construction; benign/neutral contrast distributions.

[5] [Logit-Gap Steering full HTML text v1](https://arxiv.org/html/2506.24056v1) — Version comparison; section structure.

[6] [Towards Understanding Steering Strength (Taimeskhanov, Vaiter, Garreau, arXiv:2602.02712)](https://arxiv.org/abs/2602.02712) — ICML 2026 acceptance; abstract; eleven models.

[7] [Towards Understanding Steering Strength full HTML v2](https://arxiv.org/html/2602.02712v2) — Theorem 3.3 bump behaviour (per-token); Theorem 3.6 target-concept increasing with sigmoidal shape; Theorem 3.8 quadratic cross-entropy; adaptive-alpha remark.

[8] [The Rogue Scalpel: Activation Steering Compromises LLM Safety (Korznikov et al., arXiv:2509.22067)](https://arxiv.org/abs/2509.22067) — Correct author list (NOT Kaminski); abstract; v1/v2 dates; 0%->1-13% headline.

[9] [The Rogue Scalpel full HTML v2](https://arxiv.org/html/2509.22067v2) — alpha = c*mu^(l) calibration, c grid {0.25..2.0}, 1000-draw averaging, layer-16 peak, Falcon coherence-collapse non-monotonicity, JailbreakBench harmful-prompt construct, model roster 3B-70B.

[10] [When Is a Steerable Concept Representation Real? Measurement Confounds in a Cross-Family Audit (arXiv:2608.08159)](https://arxiv.org/html/2608.08159v1) — The residual-norm normalisation protocol alpha=c||h||_l and h'=h+c||h||_l*d_hat; held-out operating-point selection; demonstration that raw units manufacture a false scaling law.

[11] [arXiv API full-text search: abliterated](http://export.arxiv.org/api/query?search_query=all:%22abliterated%22) — Surfaced arXiv:2607.01854 (Has This Checkpoint Been Abliterated?), 2607.17427, 2608.08542; confirmed the abliteration-metric lane is activation-geometry/weight-space, not steering-strength.

[12] [arXiv API full-text search: steering strength](http://export.arxiv.org/api/query?search_query=all:%22steering+strength%22) — Surfaced arXiv:2606.11599 (When is Your LLM Steerable?), 2602.02712, 2606.07696 and others.

[13] [arXiv API abstract search: steerability](http://export.arxiv.org/api/query?search_query=abs:%22steerability%22) — Surfaced arXiv:2608.08159, 2607.13162, 2608.06578, 2607.23519.

[14] [arXiv API search: safety margin + language model](http://export.arxiv.org/api/query?search_query=abs:%22safety+margin%22+AND+abs:%22language+model%22) — Independently re-found arXiv:2506.24056 and surfaced arXiv:2602.04896 Steering Externalities; establishes 'safety margin' is a crowded term.

[15] [arXiv API batch abstract fetch (10 secondary papers)](http://export.arxiv.org/api/query?id_list=2606.11599,2607.13162,2608.06578,2608.08159,2602.04896,2606.07696,2607.23519,2511.00029,2604.08524,2608.08383) — Abstracts and comments fields for all secondary lane papers; COLM 2026 for 2608.08383, AIES 2026 for 2607.23519.

[16] [arXiv API batch fetch (venue/title verification)](http://export.arxiv.org/api/query?id_list=2606.22686,2509.13450,2508.21448,2603.24543,2602.02600,2605.09043,2607.01854) — Confirmed TrustNLP 2026 for 2606.22686, ACL 2026 SRW for 2605.09043, title changes for 2509.13450 / 2508.21448 / 2605.09043, Preprint status for 2602.02600, and the full 2607.01854 abstract.

[17] [arXiv API search: critical slowing down + language model](http://export.arxiv.org/api/query?search_query=all:%22critical+slowing+down%22+AND+all:%22language+model%22) — Zero results — supporting (footnote-level) evidence for the EWS scope claim.

[18] [arXiv API search: early warning signals in cs.CL](http://export.arxiv.org/api/query?search_query=all:%22early+warning+signals%22+AND+cat:cs.CL) — Nine papers, none computing an indicator suite on a model-internal generative time series; nearest neighbours identified.

[19] [arXiv API search: dose-response steering](http://export.arxiv.org/api/query?search_query=all:%22dose-response%22+AND+all:%22language+model%22+AND+all:%22steering%22) — Three papers, none defining a threshold steering coefficient.

[20] [arXiv API search: steering coefficient in cs.CL](http://export.arxiv.org/api/query?search_query=all:%22steering+coefficient%22+AND+cat:cs.CL) — Five papers, none a per-model threshold metric.

## Follow-up Questions

- What is The Rogue Scalpel's (arXiv:2509.22067) venue and review decision? Its OpenReview forum uXecy0nKiJ was attempted on 2026-08-12 and returns a browser-verification interstitial that requires an account; the paper must not be cited with a venue until that record is read by a logged-in reader.
- Do the +57%/-50% ASR swings of arXiv:2603.24543 have a magnitude regime attached? The figures themselves are now verified verbatim, but the steering coefficients at which they occur were not extracted, so it is not yet possible to place them on the same c = alpha/||h|| axis as the Rogue Scalpel's c in [0.25, 2.0].
- Does Fig. 2 (left) of arXiv:2509.22067 show a coefficient below which random steering has zero compliance effect? The text says effects appear at 'most steering coefficients' without enumerating the exceptions, so our null's lower magnitude bound is currently 'c=0.25 is the smallest tested', not 'the effect vanishes below 0.25'.

---
*Generated by AI Inventor Pipeline*
