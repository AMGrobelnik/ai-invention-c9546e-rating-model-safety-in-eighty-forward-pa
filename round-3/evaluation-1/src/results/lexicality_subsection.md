## Lexicality, re-certified on held-out behaviour

**Held-out certification verdict: MIXED** (pre-registered branch). 2/6 powered checkpoints have upper CI(A-B) <= 0.1; 2/6 have A-B > 0.1 with CI excluding 0; 4/6 have both null axes at chance.

**Matched-contrast verdict: NORM_MISMATCH_DOES_NOT_EXPLAIN.** 6/6 checkpoints keep A materially above B at matched contrast units (lower CI of the paired difference > 0).

**Semantic-dose verdict: PARTIAL_REVERSAL_UNDER_SEMANTIC_SCORING**, adjudicated to REVERSAL_CONFOUNDED_BY_DEGENERACY.

The finding the binary rule did not anticipate, and the one that matters most: the vacuous certificate over-stated axis A as well as axis B. On held-out behaviour the canned axis is a mediocre refusal reader and on the two abliterated checkpoints it is at chance -- while the steering asymmetry it was invoked to explain survives every deflationary test applied here.

### Why the previous certificate was vacuous

Iteration 2 certified the token-disjoint paraphrase axis B as an equally good refusal direction by held-out AUROC 1.000 on eight hand-written response strings. Axes A, B and C all score 1.000 there, so the statistic has no discriminating power: it cannot separate *B is a refusal direction* from *B is a weak, noisy estimate of A*. This subsection replaces it with a certificate computed on text the models themselves produced, on prompts no axis was fitted on, and -- critically -- on text that neither A-steering nor B-steering produced, so neither axis is scored on its own effect.

Across the six checkpoints 33,135 archived generations were scanned, 27,758 survived the pre-registered exclusions (3,647 duplicate (prompt, text) pairs, 1,115 failing the archived fluency screen, 130 too short, 485 judged DEGENERATE), and 7,241 were re-encoded after balancing the classes; 0 overlapped any axis fit response.

### Held-out behavioural AUROC

| checkpoint | n refusal | n compliance | AUROC A [95% CI] | AUROC B [95% CI] | AUROC C | AUROC D | paired A-B [95% CI] | powered |
|---|---|---|---|---|---|---|---|---|
| instruct_0p6 | 382 | 1010 | 0.662 [0.596, 0.713] | 0.510 [0.465, 0.557] | 0.421 | 0.473 | +0.152 [+0.083, +0.210] | yes |
| base_0p6 | 138 | 887 | 0.612 [0.565, 0.658] | 0.538 [0.478, 0.595] | 0.389 | 0.529 | +0.074 [+0.011, +0.141] | yes |
| abliterated_0p6 | 125 | 1228 | 0.495 [0.443, 0.543] | 0.557 [0.505, 0.609] | 0.561 | 0.498 | -0.062 [-0.132, +0.009] | yes |
| instruct_1p7 | 308 | 842 | 0.790 [0.746, 0.833] | 0.386 [0.322, 0.454] | 0.313 | 0.479 | +0.404 [+0.324, +0.484] | yes |
| base_1p7 | 132 | 924 | 0.623 [0.560, 0.687] | 0.602 [0.543, 0.660] | 0.299 | 0.483 | +0.021 [-0.087, +0.132] | yes |
| abliterated_1p7 | 70 | 1119 | 0.486 [0.420, 0.555] | 0.492 [0.412, 0.568] | 0.488 | 0.491 | -0.006 [-0.107, +0.099] | yes |

On the reference checkpoint the canned axis A reaches AUROC 0.662 and the paraphrase axis B 0.510, a paired difference of 0.152 (95% CI [+0.083, +0.210]) against a pre-registered indifference margin of 0.10. The two axes have cosine 0.376 and diff-in-means norms 10.62 (A) versus 2.589 (B), a ratio of 4.10, so the 'B is just a weaker estimate of A' hypothesis is quantified rather than waved away. Its direct test is the residual: regressing s_B on s_A across held-out items gives R^2 = 0.006 and the residual still separates refusals from compliances at AUROC 0.483; a purely scaled noisy copy of A would leave nothing there.

### The certificate also over-stated axis A

The archived certificate gave A, B and C held-out AUROC 1.000 alike. On the models' own generated text the CANNED axis itself reaches only 0.486-0.790. Its 95% CI excludes chance on 4 of 6 powered checkpoints (instruct_0p6, base_0p6, instruct_1p7, base_1p7) and clears the whole pre-registered chance band on only 1 (instruct_1p7); on both abliterated members it sits at chance. Axis B's own range is 0.386-0.602. The vacuous certificate therefore over-stated the canned axis as well as the paraphrase axis: on held-out behaviour neither axis is the clean refusal reader that 1.000 implied. That is the most consequential correction in this re-analysis, because the paper's steering-strength metric is defined on axis A. The norm-matched stylistic control is also not merely at chance: on 4 checkpoints its CI lies entirely BELOW 0.5, i.e. refusals score LOW on the formal-register axis. It reads refusal text in the opposite direction while still inducing 0.00 refusal when steered, which is the dissociation this control was built to show. The random direction is at chance everywhere.

### The axis-contrast-unit dose, and whether norm mismatch explains B

Steering adds `alpha * NORM_L * x_hat` to the residual stream at layer L (extracted from the archived hook, not assumed), so one AXIS-CONTRAST UNIT is `c = alpha * NORM_L / raw_norm_X`. In those units axis A crosses 50% refusal at 0.91-1.57 contrast units, while axis B is driven to as much as 16.3 contrast units at the grid maximum alpha = 2.0 and still tops out at a refusal rate of 0.30. **The norm deficit therefore does not explain B's failure**: at MATCHED contrast units the paired refusal-rate difference A - B is 0.456 (NORM_MISMATCH_DOES_NOT_EXPLAIN; instruct_0p6: +0.504 [+0.444, +0.560] over 22 matched contrast levels; base_0p6: +0.360 [+0.292, +0.435] over 22 matched contrast levels; abliterated_0p6: +0.403 [+0.353, +0.452] over 22 matched contrast levels; instruct_1p7: +0.499 [+0.435, +0.553] over 22 matched contrast levels; base_1p7: +0.358 [+0.316, +0.397] over 23 matched contrast levels; abliterated_1p7: +0.610 [+0.553, +0.656] over 22 matched contrast levels).

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

### Semantic scoring of the outcome, and why the apparent reversal is not clean

The archived `refused` flag is an onset regex, so a lexical axis was being scored by a lexical outcome measure. Re-scored with the repaired four-class judge, axis B's refusal rate on the judged subsample rises from at most 0.45 under the regex (0.30 on the full grid) to as much as 1.00, and crosses 0.5 on every checkpoint, which taken at face value is a **PARTIAL_REVERSAL_UNDER_SEMANTIC_SCORING**. Two measurements say it should not be read as a clean one. First, the clean control axes -- the norm-matched stylistic axis and the random direction, which induce 0.00 refusal under the regex -- themselves receive judge REFUSAL rates as high as 0.80 at their top alphas, so there is a large false-positive floor on degraded text. Second, the five-class rubric applied to the SAME alpha region, which offers an explicit non-canonical-refusal class, assigns most of that text to DEGENERATE instead. The adjudicated reading is **REVERSAL_CONFOUNDED_BY_DEGENERACY**. The audited judge has sensitivity 0.688 and specificity 0.804 for REFUSAL against blind-adjudicated truth, so an attenuation-corrected column ships beside the raw judge rate and REFUSAL/PARTIAL is named as the unreliable boundary.

### What B's high-alpha text actually is

Classified with REFUSAL split into canonical and non-canonical wording, B's top-three-alpha text is 0.270 non-canonical refusal, 0.285 refusal of any wording and 0.711 degenerate, against 0.667 refusal and 0.333 degenerate for A at its own top three alphas. So B does induce SOME refusal the onset regex cannot see -- that part of the headline needs restating -- but the dominant effect of driving B hard is incoherence, not refusal, while A at its own top alphas is dominated by refusal. Boundary examples are published verbatim in `results/b_axis_examples.md`.

### Validity

Axis vectors are not stored in the archive, so all four axes were re-derived by re-running the archived fit code at the archived layer and revision SHA. They reproduce the archived values to within 5.3e-03 relative on the stored norms and cosines, so the pre-registered 1e-3 gate FAILS on a minority of quantities and is reported as a strict failure rather than waved through. It is not run-to-run noise inside this evaluation: re-deriving every axis twice on the same GPU reproduces it bit-for-bit (largest relative movement 0.0e+00), so the residual is a cross-RUN difference between the archive's device and ours: same code, same weights, same revision SHA, bf16 on a different GPU. Three facts bound its consequence -- the stored pairwise cosines reproduce to about 1e-3, the random axes reproduce EXACTLY from their stored seeds, and the re-derived canned axis has cosine 0.9992 with the independently fitted float32 axis from the breadth-panel experiment. Zero held-out items overlap any axis fit response (leakage gate), and the re-encoded refusal-logit margin reproduces the archived r_t_first at Pearson 0.9975 or better on every checkpoint. Token IDS are concatenated rather than strings when the prompt and its logged completion are re-encoded: string concatenation lets BPE merge across the boundary, which on the plain-rendered base checkpoints affected a large share of items and broke this gate outright.