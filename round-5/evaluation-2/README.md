# Is the refusal axis reading meaning or wording?

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_Y-oGSm04Tcar`

## Layman Summary

Re-checks whether an AI safety detector really recognises refusals or just the phrase 'I cannot', and whether its score is inflated by how the numbers were normalised.

## Full Summary

PURE RE-ANALYSIS of the frozen iter-4 read-vs-act tree (art_1xT3w1joqeJ8): no weights loaded, no generation, no steering, no training. 93 s on 4 CPUs, $0.0277 of a $2.00 hard cap (513 billed calls, 147 warm-cache hits, 0 errors; reruns are $0.00 from results/judge_cache_5class_local.jsonl).

GATE FIRST. R0 regenerates every archived per-member AUROC, its prompt-clustered CI, the within-stratum and per-stratum AUROCs and the paired A-B delta from proj_<KEY>.npz alone, using explib.centre_by_stratum / explib.detection_stats IMPORTED from the archive: 667/667 cells at max|delta| = 0.0, and lib/classify.REFUSAL_RE re-derives the stored labels array byte-identically on all 24 members. DEVIATION (pre-registered fallback): 6 of 30 archived members have a detect json but no proj npz (the archived gpu_stage dumps projections AFTER the detection stats; those six were scored by an earlier pass, mtimes 01:27 vs 02:30) and 3 of them are POWERED, so POWERED-and-available = 11 of 14.

PART 1 (H-L) VERDICT: READS_CANONICAL_WORDING_ONLY, member AND lineage unit. 660 stratified items (regex label x stratum x projection tertile, middle tertile 2x, IPW back to the item population) re-labelled with the five-class rubric loaded verbatim from RE3/judge_stage.py through ARCH/judge.py. Swapping the label barely moves the pooled AUROC (0.834 [0.736,0.923] regex -> 0.821 [0.752,0.866] semantic; paired DELTA_L -0.013 [-0.067,+0.030] member / -0.024 [-0.066,+0.018] lineage; kappa +0.789 [+0.699,+0.879]), but the SPLIT is decisive: canonically-worded refusals 0.897 [0.864,0.922] vs REFUSAL_NONCANONICAL 0.611 [0.542,0.686], which does not clear the members' own 20-draw random READING band (mean upper edge 0.750 -- chance is NOT 0.500 here).

NEW MEASURED CAVEAT the paper must carry: the rubric's CANONICAL/NON-CANONICAL split is NOT the regex's split. 54 of 267 items (20.2%) that open with a frozen refusal opener are still called REFUSAL_NONCANONICAL by the judge, and the drift is member-dependent (0/27 Qwen3-1.7B-Base, 17/25 Llama-3.2-3B-Instruct). Taking the rubric class as 'refusals the regex missed' over-counts 83 vs 38. On the sharper subset (semantic refusal AND regex non-refusal) the pre-registered floor of 40 is not met at n=38, so the reportable claim is the pre-registered fallback: weighted corpus prevalence 0.0546 [0.0412,0.0686] -- about 1 scored item in 18 is a refusal the regex of record calls a compliance.

PART 2 (H-X) VERDICT: LEAKAGE_CONTROL_SMALL_DELTA, both units. Four normalisation protocols on identical items/axes (archived whole-pool centring; fold-internal centring LOPO; fold-internal centre+scale = Mehta's full residualisation; leaky whole-pool z-score), on axes A, B and the norm-matched random D, under BOTH label sets. Axis A DELTA_X = -0.0205 [-0.0352,-0.0071] (centring alone +0.0009; leaky z -0.0205), an order of magnitude short of arXiv:2607.13346's -0.336 on its own data; under semantic labels -0.0397 [-0.0763,-0.0047]. CONTROL ON THE CONTROL holds: the same protocol moves random axis D by only -0.0020 [-0.0084,+0.0032] and axis B by -0.0023, so the axis-A movement is not pure normalisation. 0 fallback folds anywhere. Leakage precondition RE-ASSERTED not inherited: exact axis-fit-string text overlap = 0 on every member (fit strings re-parsed from lib/direction.py), recomputed n_prompt_overlap matches the archive on every member, and a drop-those-items sensitivity column bounds it.

ALSO SHIPPED: PARTIAL treated three ways (as refusal / as compliance / dropped-primary); judge-error attenuation from the audited 124-item probe of the SAME judge configuration (art_gYmQllaTCGT5 arm2_repaired, sensitivity 0.688 / specificity 0.923 strict); Holm-adjusted per-member p; a rank-normalised pooled AUROC; both aggregation units with both verdict strings everywhere (H-U). DELIVERABLES: eval_out.json (+full/mini/preview, exp_eval_sol_out-validated, 660 examples with both criteria, axis score and IPW weight, and a paper_numbers block every quoted number is read from), results/section_5_1_paragraph.md (f-string-generated, regenerates byte-identically), results/noncanonical_examples.md (20 verbatim boundary cases), results/prereg_eval.json (sha256-stamped before any new AUROC), r0_gate.json, sampling_frame.json, labels5.json, cost_ledger.jsonl and two vector figures.

## Dependencies

- `art_1xT3w1joqeJ8` — reanalysis
- `art_gYmQllaTCGT5` — scorer
- `art_CKWQh2cOQLLQ` — dataset

## Output Files

- `eval.py`
- `full_eval_out.json`
- `mini_eval_out.json`
- `preview_eval_out.json`

## Demo Files

- **eval.py** — Evaluation script with metrics computation

---
*Generated by AI Inventor Pipeline*
