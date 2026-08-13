**Table 2. Per-checkpoint dissociation on the 6-member DEPTH panel: what each axis READS (held-out AUROC on 7,241 model-generated items) against what it INDUCES (steered refusal).**

| checkpoint | class | n items | A held-out AUROC [95% CI] | B held-out AUROC [95% CI] | C held-out AUROC [95% CI] | D (random) AUROC [95% CI] | paired A-B [95% CI] | Holm p | A contrast units at 50% refusal | A max refusal rate | B max refusal rate | A-role at chance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base_0p6 | base | 1028 | 0.612 [0.565, 0.658] | 0.538 [0.478, 0.595] | 0.389 [0.339, 0.439] | 0.529 [0.480, 0.579] | +0.074 [+0.011, +0.141] | 0.1000 | 1.574 | 0.640 | 0.100 | no |
| instruct_0p6 | instruct | 1431 | 0.662 [0.596, 0.713] | 0.510 [0.465, 0.557] | 0.421 [0.381, 0.469] | 0.473 [0.423, 0.527] | +0.152 [+0.083, +0.210] | 0.0030 | 0.913 | 0.960 | 0.140 | no |
| abliterated_0p6 | abliterated | 1354 | 0.495 [0.443, 0.543] | 0.557 [0.505, 0.609] | 0.561 [0.510, 0.613] | 0.498 [0.438, 0.561] | -0.062 [-0.132, +0.009] | 0.2370 | 1.122 | 0.970 | 0.090 | YES (CI covers 0.5) |
| base_1p7 | base | 1061 | 0.623 [0.560, 0.687] | 0.602 [0.543, 0.660] | 0.299 [0.251, 0.346] | 0.483 [0.422, 0.543] | +0.021 [-0.087, +0.132] | 1.0000 | 1.215 | 0.840 | 0.270 | no |
| instruct_1p7 | instruct | 1171 | 0.790 [0.746, 0.833] | 0.386 [0.322, 0.454] | 0.313 [0.262, 0.361] | 0.479 [0.417, 0.547] | +0.404 [+0.324, +0.484] | 0.0030 | 1.136 | 1.000 | 0.300 | no |
| abliterated_1p7 | abliterated | 1196 | 0.486 [0.420, 0.555] | 0.492 [0.412, 0.568] | 0.488 [0.423, 0.553] | 0.491 [0.413, 0.567] | -0.006 [-0.107, +0.099] | 1.0000 | 1.334 | 1.000 | 0.070 | YES (CI covers 0.5) |

1. Unit: the ITEM (held-out, model-generated text), with a prompt-clustered bootstrap over 2,000 replicates; n items is per checkpoint. This is a different unit from Tables 1 and 3, which are model-level.
2. AUROC is the stratum-centred projection AUROC at the first generated token. Axes: A canonical canned-refusal contrast, B token-disjoint paraphrase, C norm-matched stylistic control, D matched random direction.
3. SCOPE. The 'axis B induces almost nothing' claim is a DEPTH-PANEL claim. On the iteration-2 BREADTH panel axis B DOES reach a 0.50 refusal rate on 2 of the 5 informative members it was run on (l3_instruct 0.633, l4_instruct 0.667); the earlier blanket claim that it never reaches 0.50 is wrong and is corrected here rather than repeated.
4. The two abliterated members are the ones whose A-role AUROC sits at chance; on those checkpoints the canonical axis is simultaneously a poor reader and, per the dose columns, still an inducer -- which is the within-axis dissociation the paper claims.
