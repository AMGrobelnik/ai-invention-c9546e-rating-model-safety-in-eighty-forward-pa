**Table 1. The discrimination matrix: four cheap benchmark-free safety scores x five falsification checks, on the frozen 19-member / 7-lineage panel. Verdict: PROTOCOL_DOES_NOT_DISCRIMINATE.**

| score | primary column | C1 lexical | C2 monotone | C3 depth | C4 jackknife | C5 scorer | pass count | pass count (checks 1-4) | oriented rho | 95% CI (lineage-clustered) | exhaustive perm p | perm floor | AUC (median split) | audit cost: forward passes/member | audit cost: generations/member |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| alpha_50 | max_refusal_rate | FAIL (undef.) | FAIL (0.833) | PASS (1.823) | PASS (0.210) | FAIL (0.391) | 2/5 | 2/4 | -0.208 | [-0.545, 0.183] | 0.3087 | 1.98e-04 | 0.381 | 0 | 265 |
| our-AMS sigma | ams_sigma | FAIL (0.833) | FAIL (0.947) | PASS (1.607) | PASS (0.226) | FAIL (0.391) | 2/5 | 2/4 | 0.358 | [-0.072, 0.709] | 0.0911 | 1.98e-04 | 0.705 | 96 | 0 |
| logit-gap (benign) | logit_gap_benign | FAIL (0.967) | FAIL (0.158) | FAIL (4.361) | FAIL (0.292) | FAIL (0.391) | 0/5 | 0/4 | 0.101 | [-0.243, 0.569] | 0.6621 | 1.98e-04 | 0.523 | 40 | 0 |
| logit-gap (harmful) | logit_gap_harmful | FAIL (0.977) | FAIL (0.526) | FAIL (3.611) | PASS (0.220) | FAIL (0.391) | 1/5 | 1/4 | 0.667 | [0.439, 0.904] | 0.0038 | 1.98e-04 | 0.784 | 80 | 0 |

1. Cell format: PASS/FAIL (decision statistic). Check 3's statistic is the larger of the two median span factors, PASS iff it is below 2.0; alpha_50's row leads with the NON-PARAMETRIC span (non-parametric span led, as pre-registered; the logistic spans are 4.380 / 4.380).
2. Check 5 is a SHARED bound -- a property of the scorer, not of any score -- so it is identical in every row (REFUSAL kappa 0.391 against a 0.60 threshold) and caps every row at 4/5.
3. Unit: all correlations are MEMBER level, n = 19 checkpoints over 7 lineages, resampled and permuted on the lineage label. The exhaustive floor is 1/5040 = 1.98e-04; only the identity permutation is guaranteed to reproduce |rho| when cluster blocks are unequal.
4. alpha_50's audit cost is dominated by steered GENERATION (265 per member, 5460 measured GPU-seconds), not by forward passes; every rival is forward-pass only.
5. The check-1 cell for alpha_50 carries no rank statistic: axis B is UNDEFINED on every member it was run on, so the verdict is decided by the verdict-class criterion alone (3 of 5 members flip).
