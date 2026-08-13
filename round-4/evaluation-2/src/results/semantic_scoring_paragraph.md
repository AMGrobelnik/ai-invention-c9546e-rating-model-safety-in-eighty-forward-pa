# Drop-in replacement for the paper's semantic-scoring passage

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
