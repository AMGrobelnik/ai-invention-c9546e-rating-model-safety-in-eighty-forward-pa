# Rechecking the read-versus-act coupling

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_3Nid1IyvhfIG`

## Layman Summary

Re-analyses the previous experiment's own saved numbers and finds its headline correlation mostly compares two kinds of measurement direction rather than two qualities of the models.

## Full Summary

PURE REANALYSIS of the frozen iteration-4 read-vs-act tree. $0.00 LLM spend, zero GPU, zero generation; 90 s wall (plus a one-off 453 s simulation, cached in out/sim_raw.json). 174 inputs sha256-stamped, 0 missing. Estimators IMPORTED not retyped (frozen_src/explib.py + lib_iter3/statsx.py, byte-identity 19/19 every run).

REPRODUCTION GATE: 169/169 legs PASS at 1e-6; G1 (pooled rho 0.629 and its CI at the archived seed) exact to 0.0e+00. G4 re-bootstrapped all 30 per-member axis-A AUROCs/CIs/verdicts from stored projections (24 item-level, 6 summary-level where no proj_*.npz exists).

H-C VERDICT: COUPLING_IS_AXIS_TYPE_CONTRAST + UNDERPOWERED (both fire, both reported). Within axis A across the 14 powered members rho = 0.547, lineage-clustered CI [-0.031, 0.930] over 7 units, exhaustive 5040-perm p = 0.149 (floor 1.98e-4); lineage unit 0.821 [0.348, 1.000], same sign. An EXACT two-way variance decomposition (balanced 14x5, so orthogonal) attributes 0.896 of the pooled statistic to between-axis-type, 0.036 between-member, 0.069 residual, shares summing to 1.000. Partial rho controlling axis 0.234 [-0.059, 0.397]; both main effects removed 0.126 [-0.240, 0.366]; MixedLM slope on ranks 0.192 [-0.075, 0.458]. NO single axis carries a within-axis coupling (A .547 B .148 C .397 D -.038 E .416, every CI covering 0). Control ladder: 0.629 -> 0.545 [0.284, 0.726] on A+B+E only. The reviewer's 0.434/p=0.14 is REPRODUCED EXACTLY by dropping Llama_3p2_3B_Instruct, the one AMBIGUOUS member; n=14 gives 0.547/p=0.04, but that asymptotic p ignores lineage clustering and the clustered CI covers zero at either n. The within-member mean 0.715 is demoted: same contrast, 14 times, so weaker evidence not stronger.

H-K: powered-only tally 13 READS / 1 AMBIGUOUS / 0 AT_CHANCE / 0 UNDEFINED of 14; all-30 tally 20/1/0/9, both cross-tabbed by arm with totals asserted. Attainability simulation of the artifact's OWN prompt-clustered bootstrap (141 cells x 2000 replicates x 2000 inner resamples): at true AUROC 0.500 AT_CHANCE is UNREACHABLE below n = 80 per class and P = 0.000 at the pre-registered n = 40 gate (Hanley-McNeil closed form n = 65); P(READS) = 1.000 under perfect separation at every one of n = 7, 12, 28, 32, 33. But P(READS | true 0.500) is only 0.017 at n=5 -- the asymmetry is ONE-SIDED: READS is not noise-driven, the NULL verdict is what cannot be returned. Deviation DEV-ITER5-01 quotes the code: UNDEFINED fires only on non-finite CI bounds (explib.py:486-494) via the >=5-per-class resample guard (explib.py:555-563); MIN_PER_CLASS=40 governs only the separate `powered` flag (gpu_stage.py:342-345). 7 members unpowered yet READS, smallest 6/class.

ABLITERATED ARM SURVIVES WITHOUT ANY AUROC: median rate 0.0076 vs 0.1131; Mann-Whitney U=13.5, tie-corrected asymptotic p=0.0044 PLUS an exhaustive permutation over all 293,930 assignments p=0.0026 -- the arms share one rate, so scipy method='exact' is INVALID here and its 0.0033 is recorded but never quoted; lineage-clustered bootstrap of the median difference -0.1055 [-0.2416, -0.0245]; paired sign test 10/10, p=0.0020.

MEASURED CORRECTIONS to the plan: the stale tally is 18+0+10 = 28, two short of 30 (correct 20/1/0/9), carried by iter-4 README.md and its artifact summary, NOT RESULTS.md; censored axis-A c_50 among powered members is 2 of 14 not 7 (0.771 is over all 70 PAIRS); the 6 members lacking proj_*.npz are the *_Instruct/*_Instruct_abliterated six, not BADMISTRAL or the UNDEFINED members; the iteration-3 8-strings-7-lineages trap does NOT recur (exactly 7 distinct lineage_id strings); MixedLM fails under lbfgs (LinAlgError, variance on the zero boundary) and powell converges.

DELIVERABLES: eval_out.json (schema-validated, 84 aggregate metrics, 4 datasets: gate 169 legs / coupling panel 14 / simulation surface 141 cells / abliterated rates 30), out/replacement_text.md with six drop-in sections whose 97/97 JSON pointers all resolve and zero banned salvage tokens appear, RESULTS.md rendered from the JSON and confirmed byte-identical on re-render, prereg_iter5_eval.json (sha256 b39c230e..., written and hashed before any new statistic), and 3 vector figures (within-axis vs pooled scatter, control-ladder forest at both units, attainability heatmap).

REUSABLE: bootstrap AUROC in closed form over the sorted item pool (U = sum cp*cumsum(cn) + 0.5*sum cp*cn from cluster multiplicities) is exactly equal to explib.auroc's average-rank definition to 1e-12 and ~50x faster than re-ranking each resample -- that is what made the simulation feasible on 4 cores.

## Dependencies

- `art_1xT3w1joqeJ8` — reanalysis
- `art_3Cndd5cKsYV0` — estimators
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
