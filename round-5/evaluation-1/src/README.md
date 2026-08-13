# Recheck the read-versus-act coupling and the verdict rule

Pure **reanalysis** of the frozen iteration-4 read-versus-act tree
(`iter_4/gen_art/gen_art_experiment_2`). **$0.00 LLM spend, zero GPU, zero
generation.** Every number comes from files already on disk; 174 inputs are
recorded in `eval_out.json` with size and sha256, and nothing is missing.

## What it decides

Two reviewer MAJORs.

**H-C — is the read-act coupling a relationship among models, or a contrast
between axis types?** The shipped positive was `rho = 0.629 [0.465, 0.803]` over
70 (member, axis) pairs. Axis A is strong in both roles by construction and axes
C and D are null in both roles by construction, so pooling axes measures the
difference between a fitted direction and a random one.

* Within axis A, across the 14 detection-powered checkpoints:
  **`rho = 0.547`, lineage-clustered 95% CI `[-0.031, 0.930]`** over 7 resampling
  units, exhaustive 5040-permutation `p = 0.149` (floor 1/5040 = 1.98e-4).
  Lineage unit `0.821 [0.348, 1.000]`; same sign.
* A **two-way variance decomposition** of the pooled statistic (balanced 14 × 5
  design, so the split is exact) attributes **0.896** of it to between-axis-type
  variation, 0.036 to between members, 0.069 residual — shares summing to 1.000.
* No single axis carries a within-axis coupling: A 0.547, B 0.148, C 0.397,
  D −0.038, E 0.416, every CI covering zero.
* Verdict (pre-registered, with numeric triggers):
  **`COUPLING_IS_AXIS_TYPE_CONTRAST`**, with **`UNDERPOWERED`** also firing
  (CI half-width 0.480 > 0.35). Both are true and both are reported.
* The reviewer's 13-member recompute is **reproduced exactly**: dropping
  `Llama_3p2_3B_Instruct`, the one member whose axis-A verdict is AMBIGUOUS,
  gives `rho = 0.434, p = 0.14`.

**H-K — is "zero AT_CHANCE over 30 checkpoints" evidence, or arithmetic?**

* **Double tally**, cross-tabulated by the four arms: 20 READS / 1 AMBIGUOUS /
  0 AT_CHANCE / 9 UNDEFINED over all 30 members; 13 / 1 / 0 / 0 over the 14
  detection-powered ones.
* **Attainability simulation** of the artifact's own prompt-clustered percentile
  bootstrap (141 cells × 2,000 replicates × 2,000 inner resamples, 453 s):
  at a true AUROC of 0.500 the AT_CHANCE verdict is **unreachable below n = 80**
  items per class and its probability at the pre-registered n = 40 gate is
  **0.000** (Hanley–McNeil closed form: n = 65). Under perfect separation READS
  fires with probability **1.000** at every one of the counts 7, 12, 28, 32, 33
  at which the shipped table issues it on unpowered members. The rule is *not*
  trigger-happy at true chance (P(READS | 0.500) = 0.017 at n = 5), so the
  asymmetry is one-sided: the null verdict is what cannot be returned.
* **Deviation record `DEV-ITER5-01`** with the exact code path: UNDEFINED fires
  only on non-finite CI bounds (`explib.py:486-494`), which come from the
  ≥ 5-per-class resample guard (`explib.py:555-563`); `MIN_PER_CLASS = 40`
  governs only the separate `powered` flag (`gpu_stage.py:342-345`). Seven
  members are unpowered yet READS, the smallest on 6 items per class.
* **The abliterated arm restated without any AUROC.** Its 5 READS rest on one
  powered member. The claim is carried instead by spontaneous refusal RATES:
  median 0.0076 (weight-edited) vs 0.1131 (aligned reference), Wilson intervals
  per member over ~1,585 generations; Mann-Whitney `U = 13.5`, tie-corrected
  asymptotic `p = 0.0044` and an exhaustive permutation over all 293,930 group
  assignments giving `p = 0.0026` (the arms share one rate, so scipy's exact
  Mann-Whitney null does not apply and its p is recorded but never quoted);
  lineage-clustered bootstrap of the median difference `−0.1055 [−0.2416,
  −0.0245]`; exact paired sign test over the 10 within-lineage
  abliterated-vs-parent pairs, 10 of 10, `p = 0.0020`. **"Abliteration removes
  the refusals, not the reader" survives the loss of every AUROC.**

## Validity

* **Reproduction gate: 169 of 169 legs PASS at tolerance 1e-6**, G1 (the
  stop-the-line leg) exact to 0.0e+00 — the pooled rho, its CI at the archived
  seed, the c_50 secondary and its censoring fraction, the within-member mean,
  all 30 per-member axis-A AUROCs/CIs/verdicts re-bootstrapped from the stored
  per-item projections (24 item-level, 6 summary-level where no `proj_*.npz`
  exists), the T1b arm table, the verdict tally, and the lineage bookkeeping.
* **The 18-vs-20 discrepancy is resolved in writing**: 18 + 0 + 10 = 28, two
  short of 30. The stale tally is carried by the iteration-4 `README.md` and its
  artifact summary; the correct one is 20 / 1 / 0 / 9.
* **The prose is generated, not typed.** Every number in
  `out/replacement_text.md` carries a JSON pointer into `eval_out.json`; the run
  ends with an executed assertion that resolves all **95 of 95** pointers and
  fails on any mismatch, plus a grep for the pre-registration's banned salvage
  tokens (none found).
* `RESULTS.md` is rendered from `eval_out.json` and double-rendered to confirm it
  regenerates byte-identically.
* Estimators are **imported, never retyped**: `frozen_src/explib.py` and
  `frozen_src/lib_iter3/statsx.py` are byte-identity-checked against their
  sources (19/19) at every run.

## Layout

| file | what |
|---|---|
| `eval.py` | orchestrator; runs every stage and writes `eval_out.json` |
| `prereg_iter5_eval.json` | the pre-registration, sha256 `b39c230e…`, written and hashed before any new statistic existed |
| `stage0_prereg.py` | provenance manifest (path + size + sha256) and the pre-registration |
| `stage1_gate.py` | the 7-group reproduction gate |
| `stage2_hc.py` | H-C: primary, secondary, per-axis, control ladder, confound decomposition, verdict |
| `stage3_hk.py` | H-K: double tally, simulation, deviation record, abliterated arm |
| `sim.py` | the attainability simulation (closed-form tie-corrected bootstrap AUROC, validated against `explib.auroc` to 1e-12) |
| `stage4_prose.py` | the replacement-text bundle and the pointer assertion |
| `assemble.py` | `eval_out.json` payload and `RESULTS.md` |
| `figures.py` | the three vector figures |
| `frozen_src/` | byte-identical copies of the imported estimator libraries |
| `RESULTS.md` | the rendered report |
| `out/replacement_text.md` | the six drop-in replacement sections |
| `figures/` | `fig1` within-axis vs pooled scatter, `fig2` control-ladder forest, `fig3` attainability heatmap (PDF + PNG) |

## Reproduce

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml   # every version pinned
.venv/bin/python eval.py
```

Roughly 100 s with `out/sim_raw.json` present; about 9 minutes on four cores if
the simulation surface has to be recomputed.

## Corrections to the artifact plan (measured, not assumed)

* Censored axis-A `c_50` among the powered members is **2 of 14**, not 7; the
  0.771 figure is the censoring fraction over all 70 pairs.
* The 6 members lacking per-item projections are the six `*_Instruct` /
  `*_Instruct_abliterated` checkpoints, not the ones the plan named;
  `BADMISTRAL_1p5B` and the fully-UNDEFINED members *do* have stored
  projections.
* The iteration-3 lineage-id-string trap does **not** recur: the 14 powered
  members carry exactly 7 distinct `lineage_id` strings, so the string is the
  cluster key and no merge map is needed.
* `MixedLM` does not converge on 70 points (the member random-effect variance
  sits on the zero boundary under L-BFGS); the pre-registered fallback ladder is
  logged, and the fit that does converge (`powell`) is the one reported.
