# Does garbled text fake the refusal reversal?

**POOLED VERDICT (matched contrast): REVERSAL_DOES_NOT_SURVIVE**

> NET = -0.118, CI [-0.157, -0.082] does not exclude 0 above it

Pure re-analysis of 45,900 archived steered generations. No new sampling, no model weights loaded, no GPU. Judge spend $0.6736 of the $1.50 cap.

## The one sentence

On non-degenerate text at matched axis-contrast units, the paraphrase axis B
induces 0.028 refusal (five-class ANY-REFUSAL, 95% CI
[0.008, 0.057], prompt-clustered, n = 600)
against the canned axis A's 0.747 [0.618, 0.858]
(n = 600), with the C/D control false-positive floor at 0.146
(floor set by D_random0); the net quantity B minus floor is
-0.118 with a prompt-clustered 95% CI of
[-0.157, -0.082], which
excludes 0 BELOW it -- B sits under the floor a meaningless direction sets.
Correcting for the audited judge's REFUSAL sensitivity
0.688 and specificity 0.804
(Rogan-Gladen; Youden denominator 0.492, which roughly
doubles the interval) moves the net to +0.000
[+0.000, +0.000],
reported alongside and never instead of the raw figure.
The retention caveat is the measurement that replaces the old adjective, and it
cuts the opposite way from the standing verdict: at the matched coefficient the
screen removes nothing at all -- 100.0% of B's generations survive it
against 100.0% of A's -- so B's near-zero rate there is NOT a degeneracy
artefact, it is simply the absence of an effect. Degeneracy only becomes the
story at B's own maximum coefficient, where retention falls to 70.5%
and, crucially, 70.2% of the text that DOES pass the
lexical screen is still labelled DEGENERATE by the five-class judge, against
71.1% on the unfiltered archive sample -- the
screen removes essentially none of the residual degeneracy
(+1%),
because it is a lexical filter and the failure is semantic. Between those two
regimes lies B's inverted-U peak, where B does clear the floor on fluent text
(0.642 against a floor of 0.077, NET +0.565
[+0.471, +0.655], DEGENERATE
4.9%) -- but only at 5.2 contrast units, about
4.3x the intervention A needs, which is precisely the
comparison matching was introduced to forbid.
Verdict (pre-registered, stamped before any label existed):
**REVERSAL_DOES_NOT_SURVIVE** at matched contrast,
**REVERSAL_DOES_NOT_SURVIVE** at B's maximum
coefficient, and **REVERSAL_SURVIVES** at B's own
peak-rate coefficient
(NET = -0.118, CI [-0.157, -0.082] does not exclude 0 above it).
The Rogan-Gladen correction is reported alongside but is uninformative at the
matched level: both B's rate and the floor fall below 1 - specificity = 0.196,
so both corrected prevalences TRUNCATE at 0 (flagged in
`results/net_and_correction.json`) and the corrected NET is exactly 0 by
construction rather than by measurement. The raw NET is therefore the primary
figure at that level.


## The three pre-registered comparison levels (pooled)

The matched level is the adjudication; the other two are the pre-registered 'B at its best' readings, carried so neither can be picked post hoc. They do not agree, and that disagreement IS the finding: B's apparent reversal lives entirely at coefficients matching forbids.

| level | B alpha (mean cu) | rate_B | rate_A | floor Z (from) | NET [CI] | DEGEN(B) | retention B | verdict |
|---|---|---|---|---|---|---|---|---|
| matched contrast (adjudication) | 0.20 (1.50) | 0.028 | 0.747 | 0.146 (D) | -0.118 [-0.157, -0.082] | 0.002 | 1.000 | REVERSAL_DOES_NOT_SURVIVE |
| B at its own peak refusal rate | 0.70 (5.21) | 0.642 | 0.987 | 0.077 (D) | +0.565 [+0.471, +0.655] | 0.049 | 0.958 | REVERSAL_SURVIVES |
| B at its own max contrast | 2.00 (14.98) | 0.296 | 0.531 | 0.054 (C) | +0.242 [+0.193, +0.282] | 0.702 | 0.705 | REVERSAL_DOES_NOT_SURVIVE |

**The control floor is itself made of degenerate text that passed the lexical screen.** At the matched level the floor is set by the random axis D at 0.146, and 59.0% of D's screen-passing text is labelled DEGENERATE by the five-class judge. A B rate reported without this same-population floor would be uninterpretable -- which is the check the original over-reading lacked.

## Per-member verdict at matched contrast units

| member | target cu | B alpha (cu) | ret_B | ret_A | n_B | rate_B | rate_A | floor Z | NET [CI] | corrected NET [CI] | surviving DEGEN(B) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instruct_0p6 | 0.91 | 0.20 (1.63) | 1.00 | 1.00 | 100 | 0.070 | 0.780 | 0.384 (D) | -0.314 [-0.450, -0.170] | -0.383 [-0.588, -0.198] | 0.000 | REVERSAL_DOES_NOT_SURVIVE |
| base_0p6 | 1.57 | 0.20 (1.42) | 1.00 | 1.00 | 100 | 0.060 | 0.950 | 0.061 (D) | -0.001 [-0.080, +0.060] | +0.000 [+0.000, +0.000] | 0.000 | REVERSAL_DOES_NOT_SURVIVE |
| abliterated_0p6 | 1.12 | 0.20 (1.63) | 1.00 | 1.00 | 100 | 0.010 | 0.750 | 0.061 (D) | -0.051 [-0.111, -0.011] | +0.000 [+0.000, +0.000] | 0.000 | REVERSAL_DOES_NOT_SURVIVE |
| instruct_1p7 | 1.14 | 0.20 (1.44) | 1.00 | 1.00 | 100 | 0.000 | 0.630 | 0.063 (D) | -0.063 [-0.117, -0.020] | +0.000 [+0.000, +0.000] | 0.010 | REVERSAL_DOES_NOT_SURVIVE |
| base_1p7 | 1.21 | 0.20 (1.42) | 1.00 | 1.00 | 100 | 0.030 | 0.700 | 0.158 (D) | -0.128 [-0.212, -0.046] | +0.000 [-0.105, +0.000] | 0.000 | REVERSAL_DOES_NOT_SURVIVE |
| abliterated_1p7 | 1.33 | 0.20 (1.45) | 1.00 | 1.00 | 100 | 0.000 | 0.670 | 0.146 (D) | -0.146 [-0.227, -0.068] | +0.000 [-0.064, +0.000] | 0.000 | REVERSAL_DOES_NOT_SURVIVE |

## Retention: the judge-free headline

Fraction of steered generations surviving the frozen lexical screen (`classify.fluency_ok`, recomputed on re-tokenised text; agreement with the archived flag 0.9987, primary screen = recomputed).

| member | A @matched | B @matched | B @max alpha | delta_retention B-A @matched [CI] |
|---|---|---|---|---|
| instruct_0p6 | 1.000 | 1.000 | 0.670 | +0.000 [+0.000, +0.000] |
| base_0p6 | 1.000 | 1.000 | 0.890 | +0.000 [+0.000, +0.000] |
| abliterated_0p6 | 1.000 | 1.000 | 0.550 | +0.000 [+0.000, +0.000] |
| instruct_1p7 | 1.000 | 1.000 | 0.670 | +0.000 [+0.000, +0.000] |
| base_1p7 | 1.000 | 1.000 | 0.960 | +0.000 [+0.000, +0.000] |
| abliterated_1p7 | 1.000 | 1.000 | 0.490 | +0.000 [+0.000, +0.000] |

## Rates on the filtered set, three criteria side by side (pooled, matched level)

| axis | n | regex | judge4 STRICT | judge4 INCL | judge5 ANY | judge5 NONCANON | judge5 DEGEN |
|---|---|---|---|---|---|---|---|
| A_canned | 600 | 0.470 | 0.763 | 0.770 | 0.747 | 0.142 | 0.005 |
| B_paraphrase | 600 | 0.002 | 0.043 | 0.043 | 0.028 | 0.018 | 0.002 |
| C_stylistic | 600 | 0.000 | 0.050 | 0.050 | 0.017 | 0.017 | 0.007 |
| D_random0 | 575 | 0.002 | 0.374 | 0.374 | 0.146 | 0.139 | 0.590 |

## Confusion-matrix correction

Archived judge REFUSAL sensitivity 0.688 / specificity 0.804 (n=124, Youden 0.492).

Assumptions (all load-bearing):

- (i) se/sp are TRANSPORTED from the AUD probe population -- which was deliberately STRATIFIED over the frozen-vs-repaired disagreement region, so they are NOT corpus estimates -- to steered, screen-passing text;
- (ii) they are treated as class-conditional constants independent of axis and steering coefficient;
- (iii) judge errors are assumed independent across items.
- The Youden denominator se+sp-1 = 0.492 roughly DOUBLES the CI width, so a corrected NET is materially less powered than the raw one.

**The correction TRUNCATES at the matched level and must be read as such.** Both B's observed rate (0.028) and the floor (0.146) fall below 1 - specificity = 0.196, so Rogan-Gladen maps both to 0 and the corrected NET is 0 by construction, not by measurement. The raw NET is the primary figure at that level; the correction is informative at the two higher-coefficient levels, where B's rate clears 0.196.

Sensitivity of the pooled matched NET to se/sp +/- 0.05:

| variant | se | sp | corrected B | truncated? | corrected NET | CI | excludes 0 |
|---|---|---|---|---|---|---|---|
| primary | 0.688 | 0.804 | 0.000 | YES | +0.000 | [+0.000, +0.000] | False |
| se_plus_0.05 | 0.738 | 0.804 | 0.000 | YES | +0.000 | [+0.000, +0.000] | False |
| se_minus_0.05 | 0.637 | 0.804 | 0.000 | YES | +0.000 | [+0.000, +0.000] | False |
| sp_plus_0.05 | 0.688 | 0.854 | 0.000 | YES | -0.001 | [-0.064, +0.000] | False |
| sp_minus_0.05 | 0.688 | 0.754 | 0.000 | YES | +0.000 | [+0.000, +0.000] | False |

At the two higher levels, where truncation does not bite on B:

| level | corrected B | corrected floor | corrected NET | CI | excludes 0 |
|---|---|---|---|---|---|
| own_peak_rate | 0.907 | 0.000 (truncated: YES) | +0.907 | [+0.715, +1.000] | True |
| own_max_contrast | 0.203 | 0.000 (truncated: YES) | +0.203 | [+0.123, +0.280] | True |

## Lexical vs semantic: how far apart the criteria are

Cohen's kappa between the anchored refusal-onset regex (the criterion alpha_50 was measured with) and the five-class judge's ANY-REFUSAL, on the same screen-passing items.

| level | axis | n | kappa(regex, judge5) | regex miss / judge hit | regex hit / judge miss | noncanonical share of judged refusals |
|---|---|---|---|---|---|---|
| matched | A_canned | 600 | +0.424 | 0.287 | 0.010 | 0.190 |
| matched | B_paraphrase | 600 | +0.108 | 0.027 | 0.000 | 0.647 |
| matched | C_stylistic | 600 | +0.000 | 0.017 | 0.000 | 1.000 |
| matched | D_random0 | 575 | +0.020 | 0.144 | 0.000 | 0.952 |
| own_peak_rate | A_canned | 599 | +0.037 | 0.095 | 0.010 | 0.049 |
| own_peak_rate | B_paraphrase | 575 | +0.143 | 0.492 | 0.017 | 0.447 |
| own_peak_rate | C_stylistic | 600 | +0.000 | 0.007 | 0.000 | 1.000 |
| own_peak_rate | D_random0 | 547 | +0.201 | 0.066 | 0.009 | 0.810 |
| own_max_contrast | A_canned | 482 | +0.302 | 0.336 | 0.025 | 0.418 |
| own_max_contrast | B_paraphrase | 423 | +0.000 | 0.296 | 0.000 | 0.984 |
| own_max_contrast | C_stylistic | 577 | +0.000 | 0.054 | 0.000 | 1.000 |
| own_max_contrast | D_random0 | 457 | +0.102 | 0.037 | 0.000 | 0.889 |

## Files

- `results/prereg_eval.json` -- decision rule + screen + hashes, stamped before any label existed
- `results/provenance.json` -- every headline number -> source file and JSON pointer
- `results/retention_curves.json` -- retention per (member, axis, alpha)
- `results/matched_cells.json` -- matched-contrast cell selection
- `results/rates_filtered.json` -- all rates, all criteria, all CIs
- `results/net_and_correction.json` -- NET, paired CIs, Rogan-Gladen
- `results/verdict.json` -- per-member and pooled verdicts
- `results/semantic_scoring_paragraph.md` -- drop-in paper paragraph
- `results/boundary_examples.md` -- 20 verbatim filtered examples
- `results/cost_ledger.jsonl` -- judge spend
- `results/judged_pool.json` -- every judged item with both labels
- `eval_out.json` -- schema-validated evaluation output (`exp_eval_sol_out`), 6,536 judged examples
- `figures/fig_retention_vs_contrast.pdf` -- retention against axis-contrast units, one panel per checkpoint
- `figures/fig_net_forest.pdf` -- NET with paired CIs, raw and corrected, per checkpoint and pooled
- `figures/fig_rates_three_criteria.pdf` -- the three scoring criteria side by side at the matched level
- `eval.py` / `eval_lib2.py` / `figures.py` -- the analysis (`uv run eval.py`; `--no-judge` reuses the cached labels and is free)

## Reproducing

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r <(uv pip compile pyproject.toml)
.venv/bin/python eval.py            # judging is cache-first
.venv/bin/python eval.py --no-judge # analysis only, $0
.venv/bin/python figures.py
```
