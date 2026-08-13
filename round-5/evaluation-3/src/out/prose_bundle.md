# Replacement prose, generated from JSON pointers

Every number below is rendered from a sha256-frozen source at run time. Rendering twice is asserted byte-identical, the template is asserted free of bare numerals, and the claim ledger is asserted empty over this text.

## Introduction -- the reading result, with its population named

Measured on each model's own spontaneous refusals rather than on an archived, partly steered item pool, the canonical refusal axis returns 20 `READS`, 1 `AMBIGUOUS` and 9 `UNDEFINED` over the 30 checkpoints of the read-versus-act panel, and **zero** `AT_CHANCE`. Reading is *measurable* -- the axis-A AUROC and its bootstrap interval both exist -- on 21 of those members, which is the 20 `READS` members plus the one `AMBIGUOUS` member, `Llama_3p2_3B_Instruct` (AUROC 0.685, 282 refusals / 282 compliances, detection-powered y). Unit: the member. Over that population the minimum AUROC is 0.685 [0.597, 0.763], on `Llama_3p2_3B_Instruct`; over the `READS` members alone the minimum is 0.691, on `Llama_3p2_1B_Instruct`; over the detection-powered members alone it is 0.685, on `Llama_3p2_3B_Instruct`. The three minima belong to three different populations and the paper states which one it means every time it quotes one.

## §5.1 -- reading and steering, coupled

Across 70 (member, axis) pairs drawn from 14 detection-powered members over 7 lineages -- unit: the (member, axis) pair, with the bootstrap clustered on the lineage -- induction quality and detection quality correlate at Spearman 0.629 [0.465, 0.803]; the within-member mean is 0.715. The secondary version keyed on the steering coefficient gives 0.448 under 77.1\% censoring, which is why the rate version is primary.

The abliterated arm is structurally, not statistically, quiet. Of 18 abliterated-class checkpoints -- unit: the member -- 14 never reached the per-class count the statistic needs even after the full escalation ladder, so on the 4 that were powered the pre-registered hit count is 0. Induction remains measurable on every member: across 10 within-lineage abliterated-versus-parent pairs -- unit: the pair -- steering still induces on 5 and fails on 4, with a median change in maximum induced rate of -0.306.

## §5.2 -- the retraction, at the full lineage panel

At the **member level** -- 52 members over 28 lineages, one row per member with the bootstrap clustered on the lineage label -- the original scanner reaches 0.359 [0.047, 0.592], the SET A refit 0.458 [0.197, 0.646] and the independently authored SET B refit 0.207 [-0.110, 0.463]. The paired advantage is +0.099 [-0.027, 0.244] at the member level, against the archived +0.2963; SET B gives -0.152 [-0.488, 0.075]. The permutation p for the SET A advantage is 0.135 against a Monte-Carlo floor of 5.0e-06 -- unit: the lineage permutation -- so the floor that pinned the original result is retired. The verdict string is `DOES_NOT_SURVIVE`.

The shrinkage is localised, not diffuse. Split by provenance and read at the member level, the archived block reproduces +0.2963 -- a gap of 2.6e-04 to the previously published value, itself read from the frozen pre-registration -- while the newly measured members give -0.016 [-0.144, 0.130].

## §5.3 -- semantics at matched contrast, against a measured floor

At matched axis-contrast units, pooled over the depth panel and scored on fluency-screened text -- unit: the generated item -- the five-class any-refusal rate is 0.028 for axis B against 0.747 for axis A, with the random-direction false-positive floor at 0.146. The net quantity is -0.118 (paired prompt-clustered bootstrap, 95\% CI -0.157 to -0.082): axis B sits below what a meaningless direction induces on the same population. The verdict string is `REVERSAL_DOES_NOT_SURVIVE`, on 6 members and pooled. At matched contrast the lexical screen removes nothing -- retention is 1.000 for A and 1.000 for B -- while at B's own maximum coefficient retention falls to 0.705 and 70.2\% of the surviving text is still judge-degenerate against 71.1\% unfiltered. The control floor is itself made of screen-passing degenerate text: 59.0\% of the random axis's matched-cell survivors are judge-degenerate. At B's own peak coefficient B does clear the floor -- 0.642 against 0.077, net +0.565 -- which is the `REVERSAL_SURVIVES` branch, and it lives at coefficients matching forbids.

## §5.4 -- the aggregation unit, named on every row

Our AMS reimplementation's correlation with the judged plain-harmful refusal rate is 0.358 at the **member level** -- 19 members, resampled and permuted on the lineage label -- and 0.821 at the **lineage level**, 7 units each the mean over that lineage's defined members of both score and outcome. The gap of 0.464 is what lineage aggregation buys. Over the 16 score x configuration cells where both units are defined, changing nothing but the unit moves oriented rho by a median 0.238 and a maximum 0.557, and flips the sign on 5. The headline paired statistic inherits that: on the carrier the previous draft used it is -0.929 at the lineage level and -0.376 at the member level -- `SIGN_SURVIVES`, `EXCLUSION_LOST_AT_MEMBER_LEVEL`.

The battery's negative does not depend on its cutoffs. Over a 164,736-point full factorial in the five thresholds -- unit: the grid point -- `PROTOCOL_DOES_NOT_DISCRIMINATE` holds on a fraction 1.0000 of grid points, and on 0.9091 under the stricter strictly-exceed criterion. Scoring the numeric cutoffs alone lowers those to 0.5802 and 0.2429, which locates the negative in the verdict-class and interiority clauses rather than in the numbers.

## §5.5 -- the two empirical nulls

A matched random direction is not inert. Injected at the canonical axis's own matched magnitude it induces refusal at a maximum rate of at least the pre-registered threshold on 7 of 30 members -- unit: the member -- with a panel median of 0.028 and a worst case of 0.389. And a random direction does not *read* at the textbook chance value: over the 21 members where the band is measurable its half-width runs from 0.075 to 0.500 -- unit: the member -- so a gate written against the textbook value is wrong by a wide and model-dependent margin, and a single random draw is not a null distribution.
