# A cheap safety score that survives more models

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** experiment  
**ID:** `art_Vag73M9ysCVF`

## Layman Summary

Tests whether a safety score costing 80 quick model reads and zero text generation still predicts which AI models refuse harmful requests when the model panel grows from 19 to 52 checkpoints.

## Full Summary

VERDICT: HOLDS -- the first positive result in this run. The first-decoding-step logit-gap margin read on HARMFUL prompts (our reimplementation of arXiv:2506.24056; 80 forward passes, ZERO generations, zero judge calls, zero benchmark runs, zero reference models per checkpoint) predicts the judged plain-harmful refusal rate at rho 0.694 [0.495, 0.822] at the MEMBER unit (lineage-clustered bootstrap, 10,000 reps, seed 20260812) and 0.564 [0.140, 0.826] at the LINEAGE-AGGREGATED unit, on the SAME frozen 52-member / 28-lineage / 11-family panel that retired the AMS paraphrase refit in iteration 4. 52/52 members scored, zero failures, 14,792 forward passes, 0 generations, $0.00 LLM spend.

THE DECISIVE DIAGNOSTIC PASSES. The pre-registered archived-19 vs new-33 block split gives rho 0.6673 vs 0.6677, delta -0.0004 [-0.308, 0.380]. Unlike the paraphrase refit, whose advantage was carried entirely by the archived block, this score transfers intact to 21 lineages it was never fitted on. It is not a small-panel correlation artefact.

IT SURVIVES EVERY PRE-EMPTIVE CONTROL. Partial Spearman controlling for log10(param_count) is 0.676 [0.475, 0.814] and rho(score, log10 params) is only 0.092, so the prediction is NOT parameter count. Leave-one-lineage-out (28 folds) spans [0.661, 0.726] and leave-one-family-out (11 folds) [0.650, 0.772], sign-stable in every fold. AUC 0.806. Monte-Carlo lineage-permutation p sits at the 5.0e-6 floor (200,000 draws; floor quoted beside every p). Disattenuated at kappa 0.3907 alongside -- never instead of -- the raw value.

IT BEATS THE ANCHOR. Paired on the same resampled lineages, logit_gap_harmful minus our_ams_sigma = +0.421 [0.169, 0.684], SCORE_BETTER. our-AMS sigma itself scores 0.359 member / 0.162 lineage and reproduces iteration 4's archived value on 49/52 members (max |delta| 0.0275, on two L3 Llama members plus one).

THE HARMFUL REGIME IS LOAD-BEARING, WHICH IS WHY THE HONESTY STATEMENT IS MANDATORY. The benign-regime variant COLLAPSES to 0.129 [-0.168, 0.436], and harmful-vs-benign paired delta is +0.565 [0.205, 0.873]. The saving is 'no generation, no judge, no benchmark, no reference model' -- it is NOT harmful-prompt-free, and that sentence ships verbatim in RESULTS.md and in method_out.json's 'framing' field.

GATES, ALL GREEN AND ALL ORDERED BEFORE ANY CORRELATION. Byte-identity reuse manifest over 17 lib/ + lib_iter3/ files plus 46 hashed archived inputs; 14 offline apparatus assertions; ORIENTATION_MAP recovered from iteration 3's driver by ast (never imported -- it calls setrlimit at module scope); panel identity 52/28/11 and 19/33 with both calibration members reproducing 0.250 and 0.900; T0-REPLAY reproducing iteration 3's 0.6673 [0.439, 0.904] / 0.929 to 4 decimals; a timestamp-free pre-registration content sha stable across invocations. Recomputing the 19 archived members from the models gives IDENTICAL RANKS (Spearman(iter3, iter5) = 1.000, 0 positions moved), so every Spearman statistic is unchanged by the small numeric drift on 3 members.

THREE PLAN ASSUMPTIONS WERE MEASURED FALSE AND ARE RECORDED AS PRE-REGISTERED DEVIATIONS: (1) the plan's five UNRELIABLE-flagged members DO NOT EXIST anywhere in iteration 4's archive, so that exclusion set was not invented; (2) 51 of 52 rows carry a revision SHA, not 52 (l1_abliterated has no panel_manifest row, hence also no manifest tokenizer family and no param_count); (3) five members have no empirical refusal-onset lexicon for their tokenizer family -- their primary columns are NULL with reason MISSING_FAMILY_LEXICON, never back-filled, and the pre-registered union-of-all-families SECONDARY column (rho 0.579 member) ships beside them.

Audit cost: 80 forward passes and 0 generations to score one new checkpoint; median 20.0 s / p90 36.7 s / max 70.1 s per member for all four scores including download on one RTX A4500. Deliverables: method.py (--tier t0/smoke/t2/archive/full, resumable by per-member file existence), lib_iter5/ (ast constant extraction, revision-pinned loader, aggregation and block-split statistics), prereg_iter5.json, 58 result files including per-member JSONs and the archive-only analysis, and summarise.py which renders RESULTS.md deterministically with every number read from method_out.json rather than retyped.

## Dependencies

- `art_CKWQh2cOQLLQ` — dataset
- `art_0UsKSgsMHome` — baseline spec
- `art_Qm_KL4GhZCnX` — positioning

## Output Files

- `method.py`
- `full_method_out.json`
- `mini_method_out.json`
- `preview_method_out.json`

## Demo Files

- **method.py** — Research methodology implementation

---
*Generated by AI Inventor Pipeline*
