# Redo the headline stats the honest way

Pure reanalysis of the frozen iteration-1 / iteration-2 result trees.
**No GPU, no model loading, no API call, $0.00 spend, 55 s wall-clock.**
Every number is recomputed from files already on disk; anything that could not be
recomputed is listed under `metadata.not_recomputable` with the reason, and nothing
was re-measured.

## Verdict first

| Claim | Old statement | What the archive actually supports |
|---|---|---|
| Metric vs baseline | `Delta rho = -0.714 [-1.765, 0.667]`, a TIE | On **sign-oriented** correlations `Delta = -0.929 [-1.961, -0.113]`, an our-AMS win. The archived raw value reproduces to 3 dp first. |
| Could the old statistic ever have rewarded a perfect metric? | never asked | **No.** A perfect alpha_50 (rho = -1) scored `Delta = -1 - 0.821 = -1.821`, a catastrophic loss. Oriented, the same ideal case scores `+1 - 0.821 = +0.179`. |
| How wrong is alpha_50's sign? | "unstable, -0.086 to 0.771" | Oriented rho `-0.107`; the lineage bootstrap puts **0.585** of its mass below zero, so the strong "wrong-signed" claim is **downgraded** to "indistinguishable from zero and point-estimated with the wrong sign", per the pre-committed rule. |
| Does the conclusion depend on the convention? | not tested | No, on point estimates: oriented rho, \|rho\| and AUC all favour our-AMS (AUC 0.833 vs **0.250**, i.e. alpha_50 is anti-predictive). But no comparator separates them at n=7 — the \|rho\| CI includes 0. |
| "changes sign four times" | 4 | **6 of 11** enumerated analysis choices are wrong-signed, 4 right-signed, 1 undefined. Old count retired. |
| Free vs teacher-forced | "stochastic dominance; deviation grows" | Both retired. 61-88% of paired rollouts are **exact ties** (the perturbed stream never diverged); forced strictly exceeds free in **36 of 1500**; among diverging rollouts free wins 79-100%. The median rollout **decays in both channels** (15/15). Sign test and Wilcoxon significant after Holm in 15/15, favouring free among untied pairs. |
| What is the amplifying tail? | never characterised | **Not safety-relevant on any measured covariate**: prompt identity p = 0.084, member judged refusal rate rho = -0.221 [-0.392, 0.315]. The one surviving association (token-divergence extent) is mechanical. The refusal-lexicon covariate is NOT_RECOMPUTABLE. |
| The composite | "a two-stage triage score" | Archived at `E1 :: metadata.composite` (not E2). Its correlation is **identical to its alpha_50 component** because 6 of 6 checkpoints pass the gate, and stage 1 was **withdrawn at power** (both bases cross 0.50 at 0.64/0.84). Reported as a closed loop. |
| Panel accounting | "19 / 17 / 1" | **19 / 14 / 1.** 5 members are auto-flagged UNRELIABLE, and the single member with a defined logistic alpha_50 (`l4_base`) is one of them — so after the pre-registered exclusion the primary estimator is defined on **0** analysable members. |
| AMS reproduction | "the reimplementation fails" | Fails the two **aggregate** criteria (6/12 cells inside ±25%; ordering) while **passing the per-checkpoint verdict on 3/3**, and the ordering test **cannot reach p < 0.333 at n = 3**. Label "our AMS reimplementation" kept. |
| Layer sensitivity | "4.4x" | **1.8x non-parametric** vs 4.4x logistic, with the logistic undefined at 1 of 5 layers, out-of-grid at 1 more, and the dose curve non-monotone at 4. Misspecification diagnostic **INCONCLUSIVE at 4 cells**. |
| Judge propagation | both revisions settled | Jailbreak ASR **STANDS** (truth 0.800 [0.652, 0.895], 32/40); plain-harmful refusal **RESTATED** (truth 0.000 [0.000, 0.088], 0/40). Wilson intervals recomputed from recovered counts, all reproduce. |

## Reproduction checks that had to pass first

- Rebuilt lineage units match the archived ones to `1e-9` on all 7 x 7 cells.
- `Delta = -0.714`, CI `[-1.765, 0.667]` reproduced to 3 dp through `lib.stats_ext.paired_rho_delta`, imported **verbatim** from the archive.
- The judged axes recomputed from `scored.jsonl` match the archived per-member aggregation exactly.
- The archived composite score is verified to be `1 / alpha_50` on every row.

## Layout

```
eval.py            entry point: runs step 0 + analyses 1-5, writes eval_out.json
eval_common.py     paths, manifest/sha256, shared statistics
eval_step0.py      freeze + inventory + the 19-member table + 7 lineage units
eval_a1.py         Analysis 1: orientation, ceiling check, comparators, recount
eval_a2.py         Analysis 2: asymmetry at true strength + tail characterisation
eval_a34.py        Analyses 3 & 4: composite, accounting, AMS, layers, judge
eval_a5.py         Analysis 5: corrections-of-record appendix + reduction accounting
make_figs.py       regenerates every figure FROM eval_out.json
out/               member_table.csv, lineage_units.csv, replacement_text.md,
                   appendix_corrections_of_record.md, main_text_stub.md
figs/              F1-F5 as vector PDF + PNG
```

Run: `.venv/bin/python eval.py && .venv/bin/python make_figs.py`

## Figures

| | |
|---|---|
| F1 | oriented rho per score per judged axis, lineage-bootstrap CI + jackknife range |
| F2 | the ceiling check: measured vs hypothetically perfect alpha_50, old vs corrected statistic |
| F3 | per-member free-minus-forced deviation-ratio deltas at the 50/75/90/95th percentiles |
| F4 | the AMS 3 x 4 reproduction grid, relative error per checkpoint x calibration rule |
| F5 | layer sensitivity, logistic vs non-parametric across L-2..L+2 |

## What the paper step should paste

`out/replacement_text.md` — 14 blocks, each with the OLD sentence, the NEW sentence and
the JSON path of every number in it. It is **generated** by `eval.py`, not hand-typed, so
it cannot drift from `eval_out.json`. `out/main_text_stub.md` and
`out/appendix_corrections_of_record.md` implement the 16.1% main-text reduction
(1,592 words moved, 139 added back, against a 15-20% target); the donor paragraphs are
listed individually with their disposition in
`results.corrections_of_record.reduction_accounting.donor_paragraphs`.
