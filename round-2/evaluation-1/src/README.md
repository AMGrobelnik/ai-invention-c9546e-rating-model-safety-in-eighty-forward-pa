# Re-checking the wobble experiment's statistics

Pure **re-analysis** of the iteration-1 refusal-wobble dynamics arm. No rollouts were
regenerated and no steering was re-run. The single piece of new compute is a
forward-pass-only job (`final_layer_gate.py`, ~1,000 forward passes, ~45 s on the GPU)
that recovers the observable-validity gate at the final-layer readout, which the archive
did not store. LLM API spend: **$0.00**.

## Run it

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python numpy pandas scipy matplotlib loguru psutil
.venv/bin/python eval.py          # analyses + eval_out.json + figs/
.venv/bin/python make_report.py   # results_section.md + deviations.{json,csv}
```

`final_layer_gate.py` needs torch/transformers and is optional; `eval.py` picks up
`out/final_layer_gate.json` if it exists and otherwise reports the final-layer arm of the
gate as *not recoverable without new compute*:

```bash
<iter_1>/gen_art_experiment_1/.venv/bin/python final_layer_gate.py
```

## Deliverables

| file | what it is |
|---|---|
| `eval_out.json` | `exp_eval_sol_out`-valid. 12 datasets / 249 rows, every row carrying its source JSON pointer; `metadata.verdicts` (8 strings), `metadata.limitations` (15), `metadata.inputs` (sha256 manifest of every input). |
| `mini_eval_out.json`, `preview_eval_out.json`, `full_eval_out.json` | size variants from the aii-json skill. |
| `results_section.md` | drop-in replacement for the dynamics arm's results, generated from `eval_out.json` so the prose cannot drift from the numbers. |
| `deviations.json` / `deviations.csv` | machine-readable pre-registration-deviations table (analysis / what iteration 1 said / what this says / why / pointer). |
| `figs/F1…F6.{pdf,png}` | forest plot of the direction contrast + DiD with the equivalence margin; the validity gate at both readouts paired with the token-level instrument check; the exact n=4 permutation null; AC1/Var*/flicker vs series length; λ diagnostics; the cross-arm asymmetry table. |
| `out/analysis_tables.json` | every intermediate table, unflattened. |
| `out/final_layer_gate.json` | the forward-pass job's output. |
| `spi/` | the iteration-1 estimator library, copied verbatim and imported rather than reimplemented, so definitions cannot drift. |

## Headline results

1. **The direction control, re-adjudicated.** Iteration 1 ran it on λ, which its own tree
   marks `identifiable=false` on 640/640 rows. Recomputed on the assumption-free
   statistics (16-step decay ratio, normalised deviation AUC), the primary pair's
   difference-in-differences is **−2.334 [−3.573, −1.037]** log units — *not* the null the
   λ-based control reported — but it does not survive Holm correction across the 48-test
   family (adjusted p = 0.214) and 0/48 tests pass equivalence at ±0.20. Sizing number for
   the next iteration: ≈1,880 prompts, not 20.
2. **The observable-validity gate empties the cross-model table.** At AUROC ≥ 0.70 and
   margin > 0, **1 of 4** members clears at the layer-L readout → **0 admissible model
   pairs**. At the final layer (recomputed here) **2 of 4** clear → 1 admissible pair, and
   on it no indicator separates. Which readout you pick decides whether the comparison
   exists at all.
3. **The n=4 rank comparison is a tie-break artifact *and* uninformative by construction.**
   The archived ρ_SPI = −0.20 vs ρ_baseline = +0.40 reproduces only under an ordinal rank
   that breaks the tie between the two models whose harmful refusal rate is identically
   0.000; tie-aware ranks give +0.105 and +0.632. Either way the exact 4! = 24 permutation
   floor puts the smallest attainable two-sided p at 0.083 (0.167 with the observed ties).
4. **The AC1 length control is a verification, not a repair.** Iteration 1 already reported
   the Kendall-corrected field, all series are length 192, and the matched-length re-report
   at T = 192 reproduces the picture on both the corrected and the raw field.
