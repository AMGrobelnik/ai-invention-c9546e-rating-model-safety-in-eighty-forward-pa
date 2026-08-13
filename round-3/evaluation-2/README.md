# Redoing the headline safety stats honestly

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_ouNbQqPM59dp`

## Layman Summary

Recomputes the previous experiments' headline statistics correctly from archived files only, showing several published claims were stated in a form that could not have been right.

## Full Summary

Pure reanalysis of the frozen iteration-1/2 trees: no GPU, no model loading, no API calls, $0.00, 55 s. Archived estimator code (lib/stats_ext, lib/dose) imported VERBATIM; rebuilt 7 lineage units match the archive to 1e-9 and the archived headline (Delta=-0.714 [-1.765,0.667]) reproduces to 3 dp before anything is restated.

A1 SIGN ORIENTATION. Oriented Delta = -0.929 [-1.961,-0.113] (n=7 lineages, 5000 lineage bootstrap). CEILING CHECK: under the old raw statistic a PERFECT alpha_50 scored Delta = -1-0.821 = -1.821 (a catastrophic loss); oriented it scores +1-0.821 = +0.179 — the old comparison could not reward the ideal case. Wrong-sign claim DOWNGRADED per the pre-committed rule (bootstrap mass below 0 = 0.585, not >=0.90): 'indistinguishable from zero, point-estimated with the wrong sign'. Orientation-free comparators agree on point estimates only (AUC 0.833 our-AMS vs 0.250 alpha_50 — anti-predictive); |rho| difference CI includes 0, so nothing separates at n=7. Sign-flip recount: 6 of 11 enumerated analysis choices wrong-signed, 4 right, 1 undefined — the 'four times' sentence is retired. Depth panel oriented +0.257, exact permutation p=0.658 vs floor 0.00278 (720 orderings). Sign rule cited to E1 metadata.external_validity.ranking_agreement.expected_sign_if_metric_valid; the iteration-2 prereg fixes only the sign of the DIFFERENCE, never of either component — that gap is the defect.

A2 ASYMMETRY (15/19 members, 5 lineages, 4 families; 1500 rollouts). The plan's expectation was WRONG in an instructive way: 61-88% of paired rollouts are EXACT ties (the perturbed free stream never diverged), forced strictly exceeds free in only 36/1500, and among diverging rollouts free wins 0.79-1.00. Sign test and Wilcoxon significant after Holm in 15/15 FAVOURING free among untied pairs. Medians decay in BOTH channels in 15/15 (free 0.199-0.783, forced 0.081-0.329); q95 delta positive 15/15; mean-diff CI excludes 0 in 15/15. 'Stochastic dominance' and 'deviation grows' retired; the effect is a right-tail effect CONDITIONAL ON DIVERGENCE. TAIL: not safety-relevant on any measured covariate (prompt chi2 p=0.084, member judged refusal rho=-0.221 [-0.392,0.315]); the only surviving association (token-divergence extent, r=0.50) is mechanical. Refusal-lexicon covariate NOT_RECOMPUTABLE (no archived survival token streams).

A3 COMPOSITE. The plan's pointer was wrong: it is archived at E1 metadata.composite (6-checkpoint depth panel), score = 1/alpha_50 (verified every row). Its oriented rho is IDENTICAL to its alpha_50 component because 6/6 pass the gate — the gate contributes nothing — and stage 1 was withdrawn at power (both bases cross 0.50 at 0.64/0.84; gate-vs-class 0.67 of 6). Breadth-panel extension reported as a labelled reconstruction.

A4 ACCOUNTING. The triple is 19 / 14 / 1, NOT 19/17/1 (5 UNRELIABLE excluded), and the single member with a defined logistic alpha_50 (l4_base) is itself UNRELIABLE, so after the pre-registered exclusion the primary estimator is defined on ZERO analysable members. AMS: 6/12 checkpoint x rule cells inside +-25%, per-checkpoint verdict PASS 3/3, ordering test vacuous at n=3 (floor 0.333); label kept. LAYERS: non-parametric 1.8x vs logistic 4.4x, logistic undefined at 1 of 5 layers and out-of-grid at 1 more, curve non-monotone at 4; misspecification diagnostic INCONCLUSIVE at 4 cells (said so rather than attributing). JUDGE: Wilson intervals recomputed from recovered counts — jailbreak ASR STANDS (0.800 [0.652,0.895], 32/40), plain-harmful RESTATED (0.000 [0.000,0.088], 0/40), pooled COMPLIANCE recall 29/117=0.248 [0.178,0.333]; attenuation caveat naming exactly which A1 correlations run against a REFUSAL-kappa-0.391 scorer.

A5 CORRECTIONS OF RECORD: 13 appendix entries (each with old claim, corrected statement, file+key, why it moved), 15 E1 deviations / 12 E2 amendments / 8 V1 deviations, main-text reduction 16.1% (1592 words moved, 139 added back) — inside the 15-20% target, with donor paragraphs listed individually.

SHIPPED: eval_out.json (exp_eval_sol_out-valid, 40 aggregate metrics, 3 datasets/29 rows, 31-file sha256 inputs manifest, 12-module reuse manifest, 15 limitations, 7 not_recomputable entries, zero non-finite numbers), out/replacement_text.md (14 old/new blocks GENERATED from the JSON with the JSON path of every number), out/appendix_corrections_of_record.md, out/main_text_stub.md, out/member_table.csv, and F1-F5 as vector PDF+PNG regenerated from the JSON.

## Dependencies

- `art_sabuvuJ8P3Wy` — reanalysis
- `art_r3PqOtpvcIsK` — reanalysis
- `art_UthAQuH8WZ5C` — archive
- `art_gYmQllaTCGT5` — scorer

## Output Files

- `eval.py`
- `full_eval_out.json`
- `mini_eval_out.json`
- `preview_eval_out.json`

## Demo Files

- **eval.py** — Evaluation script with metrics computation

---
*Generated by AI Inventor Pipeline*
