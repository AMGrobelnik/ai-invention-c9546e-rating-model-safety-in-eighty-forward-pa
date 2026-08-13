# Does the paraphrase axis really read refusal?

**MIXED** — 2/6 powered checkpoints have upper CI(A-B) <= 0.1; 2/6 have A-B > 0.1 with CI excluding 0; 4/6 have both null axes at chance

**The unanticipated finding, and the one that matters most:** the archived certificate over-stated axis A as well as axis B. On the models' own generated text the canned axis reaches AUROC 0.486-0.790 (archived certificate: 1.000 for every axis), its CI excludes chance on 4 of 6 powered checkpoints, and on both abliterated members it is at chance. The steering-strength metric the paper defines is built on that axis.

**Matched contrast: NORM_MISMATCH_DOES_NOT_EXPLAIN** — 6/6 checkpoints keep A materially above B at matched contrast units (lower CI of the paired difference > 0)

**Semantic dose: PARTIAL_REVERSAL_UNDER_SEMANTIC_SCORING**

Re-analysis only: no new sampling, no new steered generation, no training. The single piece of GPU work is a forward pass over text that was already logged, to read the residual stream at the steering site.

## What this replaces

Iteration 2's lexicality control was certified by 'equal held-out AUROC 1.000' on eight hand-written strings. A, B and C all saturate there, so that number certifies nothing. Here the certificate is computed on the models' own generated refusals and compliances, in a pool that is blind to both axes.

Across the six checkpoints 33,135 archived generations were scanned, 27,758 survived the pre-registered exclusions (3,647 duplicate (prompt, text) pairs, 1,115 failing the archived fluency screen, 130 too short, 485 judged DEGENERATE), and 7,241 were re-encoded after balancing the classes; 0 overlapped any axis fit response.

## Held-out behavioural certification (Analysis 1)

| checkpoint | n refusal | n compliance | AUROC A [95% CI] | AUROC B [95% CI] | AUROC C | AUROC D | paired A-B [95% CI] | powered |
|---|---|---|---|---|---|---|---|---|
| instruct_0p6 | 382 | 1010 | 0.662 [0.596, 0.713] | 0.510 [0.465, 0.557] | 0.421 | 0.473 | +0.152 [+0.083, +0.210] | yes |
| base_0p6 | 138 | 887 | 0.612 [0.565, 0.658] | 0.538 [0.478, 0.595] | 0.389 | 0.529 | +0.074 [+0.011, +0.141] | yes |
| abliterated_0p6 | 125 | 1228 | 0.495 [0.443, 0.543] | 0.557 [0.505, 0.609] | 0.561 | 0.498 | -0.062 [-0.132, +0.009] | yes |
| instruct_1p7 | 308 | 842 | 0.790 [0.746, 0.833] | 0.386 [0.322, 0.454] | 0.313 | 0.479 | +0.404 [+0.324, +0.484] | yes |
| base_1p7 | 132 | 924 | 0.623 [0.560, 0.687] | 0.602 [0.543, 0.660] | 0.299 | 0.483 | +0.021 [-0.087, +0.132] | yes |
| abliterated_1p7 | 70 | 1119 | 0.486 [0.420, 0.555] | 0.492 [0.412, 0.568] | 0.488 | 0.491 | -0.006 [-0.107, +0.099] | yes |

Underpowered (fewer than 40 items in one class, excluded from the verdict count by the pre-registered rule): none.

## Axis-contrast-unit dose (Analysis 2)

| checkpoint | axis | raw norm | alpha_50 | contrast units @ 50% | max contrast units | max refusal rate | inverted U | fluency collapse alpha |
|---|---|---|---|---|---|---|---|---|
| instruct_0p6 | A_canned | 10.63 | 0.459 | 0.91 | 4.0 | 0.96 | yes | none |
| instruct_0p6 | B_paraphrase | 2.59 | n/a (never crosses) | n/a | 16.3 | 0.14 | yes | none |
| instruct_0p6 | C_stylistic | 7.64 | n/a (never crosses) | n/a | 5.5 | 0.00 | no | none |
| instruct_0p6 | D_random0 | 33.14 | n/a (never crosses) | n/a | 1.3 | 0.01 | no | none |
| instruct_0p6 | E_prompt_contrast | 2.62 | 1.592 | 12.83 | 16.1 | 0.52 | yes | none |
| base_0p6 | A_canned | 10.34 | 0.844 | 1.57 | 3.7 | 0.64 | yes | none |
| base_0p6 | B_paraphrase | 2.72 | n/a (never crosses) | n/a | 14.2 | 0.10 | yes | none |
| base_0p6 | C_stylistic | 8.30 | n/a (never crosses) | n/a | 4.6 | 0.00 | no | none |
| base_0p6 | D_random0 | 33.14 | n/a (never crosses) | n/a | 1.2 | 0.01 | no | none |
| base_0p6 | E_prompt_contrast | 5.16 | n/a (never crosses) | n/a | 7.5 | 0.01 | no | none |
| abliterated_0p6 | A_canned | 10.64 | 0.564 | 1.12 | 4.0 | 0.97 | yes | none |
| abliterated_0p6 | B_paraphrase | 2.59 | n/a (never crosses) | n/a | 16.3 | 0.09 | yes | none |
| abliterated_0p6 | C_stylistic | 7.64 | n/a (never crosses) | n/a | 5.5 | 0.00 | no | none |
| abliterated_0p6 | D_random0 | 33.14 | n/a (never crosses) | n/a | 1.3 | 0.00 | no | none |
| abliterated_0p6 | E_prompt_contrast | 2.62 | n/a (never crosses) | n/a | 16.2 | 0.02 | no | none |
| instruct_1p7 | A_canned | 22.95 | 0.562 | 1.14 | 4.0 | 1.00 | yes | none |
| instruct_1p7 | B_paraphrase | 6.46 | n/a (never crosses) | n/a | 14.4 | 0.30 | yes | none |
| instruct_1p7 | C_stylistic | 18.97 | n/a (never crosses) | n/a | 4.9 | 0.00 | no | none |
| instruct_1p7 | D_random0 | 46.61 | n/a (never crosses) | n/a | 2.0 | 0.07 | yes | none |
| instruct_1p7 | E_prompt_contrast | 8.37 | n/a (never crosses) | n/a | 11.1 | 0.16 | yes | 2.0 |
| base_1p7 | A_canned | 24.06 | 0.571 | 1.21 | 4.3 | 0.84 | yes | none |
| base_1p7 | B_paraphrase | 7.22 | n/a (never crosses) | n/a | 14.2 | 0.27 | yes | none |
| base_1p7 | C_stylistic | 22.17 | n/a (never crosses) | n/a | 4.6 | 0.00 | no | none |
| base_1p7 | D_random0 | 46.61 | n/a (never crosses) | n/a | 2.2 | 0.01 | no | none |
| base_1p7 | E_prompt_contrast | 21.16 | n/a (never crosses) | n/a | 4.8 | 0.01 | no | none |
| abliterated_1p7 | A_canned | 22.41 | 0.652 | 1.33 | 4.1 | 1.00 | yes | none |
| abliterated_1p7 | B_paraphrase | 6.30 | n/a (never crosses) | n/a | 14.5 | 0.07 | yes | 2.0 |
| abliterated_1p7 | C_stylistic | 18.60 | n/a (never crosses) | n/a | 4.9 | 0.00 | no | none |
| abliterated_1p7 | D_random0 | 46.61 | n/a (never crosses) | n/a | 2.0 | 0.03 | no | none |
| abliterated_1p7 | E_prompt_contrast | 7.94 | n/a (never crosses) | n/a | 11.5 | 0.01 | no | 2.0 |

## Pre-registration, gates and cost

- Pre-registration stamped before any AUROC existed; 3 amendments appended with `when_decided` and the data state at the time (counting universe over POWERED checkpoints; the axis-reproduction tolerance reported at both the strict and the determinism-calibrated reading; the null-axis judge floor added after seeing the control curves).
- V1 leakage: 0 held-out items overlap any axis fit response, on every checkpoint.
- V2 axis reproduction: STRICT FAIL / SUBSTANTIVE PASS — the archived vectors are not stored, so they are re-derived; deviation from the archived summary statistics reaches 5.3e-03 relative, above the pre-registered 1e-3, while the re-derivation is bit-exact within this run and the re-derived canned axis has cosine 0.9992 with an independently fitted float32 axis from the breadth panel.
- V3 observable reproduction: the re-encoded refusal-logit margin reproduces the archived `r_t_first` at Pearson 0.9975 or better on all six checkpoints.
- OpenRouter spend: $0.1900 of a $1.50 cap (cache-first sampler; every archived judge cache was seeded first).

## Files

- `eval_out.json` — schema-validated evaluation output (all four analyses)
- `results/prereg_eval.json` — pre-registration, stamped before any AUROC
- `results/provenance.json` — every headline number to its archived JSON pointer
- `results/lexicality_subsection.md` — drop-in replacement paper subsection
- `results/b_axis_examples.md` — verbatim boundary examples
- `results/analysis{1,2,3,4}.json`, `results/encode_*.json`, `results/axes/*.npy`
- `figures/` — regenerated from the analysis output only

## Reproduce

```bash
python prereg.py                       # stamp the pre-registration
python gpu_stage.py --checkpoints all  # axis re-derivation + re-encode (GPU)
python analysis12.py                   # Analyses 1 and 2
python judge_stage.py --checkpoints all  # Analyses 3/4 judging (OpenRouter)
python analysis34.py                   # Analyses 3 and 4
python assemble.py && python figures.py
```