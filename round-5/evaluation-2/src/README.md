# Is the refusal axis reading meaning or wording?

Pure re-analysis of the FROZEN iteration-4 read-vs-act tree
(`iter_4/gen_art/gen_art_experiment_2`, art_1xT3w1joqeJ8). **No model weights are
loaded, no text is generated, no steering is applied, no model is trained.**
Everything is arithmetic over the archived `results/proj_<KEY>.npz`,
`proj_<KEY>_items.json` and `detect_<KEY>.json`, plus $0.0277 of OpenRouter
judging against a $2.00 hard cap.

Run: `uv run eval.py` (93 s wall, 4 CPUs, no GPU) then `uv run figures.py`.

## The two questions

**Part 1 (H-L) — is the detection result partly definitional?** Axis A is the
diff-in-means of hand-written canned refusals against canned compliances, and the
detection label of record is `lib/classify.REFUSAL_RE`, an anchored regex over
canned-refusal openers. Those two objects share a lexical basis. A stratified
subset of the SAME stored spontaneous generations was re-labelled with the
five-class semantic rubric of `iter_3/.../judge_stage.py` (which carries an
explicit `REFUSAL_NONCANONICAL` class) and axis A's AUROC was recomputed against
semantic labels, paired against the regex AUROC **on the identical items**.

**Part 2 (H-X) — how much of the AUROC is the normalisation?** The archived
readout subtracts a per-stratum mean estimated on the WHOLE scored pool, which
lets information from the held-out item into its own normalisation. The one
published control (arXiv:2607.13346, worth 0.761 → 0.425 on its author's data)
re-estimates every centring/scaling statistic inside the training fold under
leave-one-prompt-out. Four protocols were run on the identical items and axes:
`archived`, `fold_centre`, `fold_centre_scale` (Mehta's full residualisation) and
a deliberately leaky whole-pool z-score, on axes A, B and the norm-matched random
axis D, under BOTH the regex and the semantic labels.

## Headline numbers

| quantity | value |
|---|---|
| reproduction gate R0 | **667 / 667 cells, max abs delta 0.0**, regex labels byte-identical to the stored `labels` array on all 24 members |
| members: detect json / projections / POWERED and available | 30 / 24 / **11** |
| kappa(regex, semantic any-refusal), pooled | **+0.789 [+0.699, +0.879]** |
| AUROC axis A, regex label → semantic label | 0.834 [0.736, 0.923] → 0.821 [0.752, 0.866] |
| DELTA_L (paired, same items), member / lineage unit | **−0.013 [−0.067, +0.030]** / −0.024 [−0.066, +0.018] |
| AUROC on canonically-worded refusals | **0.897 [0.864, 0.922]** |
| AUROC on `REFUSAL_NONCANONICAL` | **0.611 [0.542, 0.686]** |
| mean 20-draw random READING band upper edge | **0.750** (chance is NOT 0.500 here) |
| n `REFUSAL_NONCANONICAL` / n the regex actually missed | 83 / **38** (29 of them non-canonical) |
| weighted corpus prevalence of regex-missed refusals | **0.0546 [0.0412, 0.0686]** |
| DELTA_X, axis A, fold-internal centre+scale | **−0.0205 [−0.0352, −0.0071]** (Mehta: −0.336) |
| same protocol on the random axis D / axis B | −0.0020 [−0.0084, +0.0032] / −0.0023 |
| judge cost | **$0.0277** cumulative of a $2.00 hard cap (513 billed calls, 147 warm-cache hits, 0 errors); reruns are $0.00 |

**PART 1 VERDICT: `READS_CANONICAL_WORDING_ONLY`** (member level and lineage
level agree). Swapping the label barely moves the pooled AUROC, but the split is
decisive: the axis separates canonically-worded refusals from compliances at
0.897 while non-canonically-worded ones sit at 0.611, whose CI does not clear the
members' own measured random band (0.750). The honest restatement is that axis A
reads canonically-worded refusals.

**Secondary, sharper subset** (the refusals the regex ACTUALLY missed, rather
than the rubric's own non-canonical class): `UNDERPOWERED` at n = 38 against the
pre-registered floor of 40. The pre-registered fallback applies — the reportable
claim is the weighted corpus prevalence, 0.0546 [0.0412, 0.0686], i.e. about one
scored item in eighteen is a refusal the regex of record calls a compliance.

**PART 2 VERDICT: `LEAKAGE_CONTROL_SMALL_DELTA`** (both units). Applying the
published control to our own headline costs 0.02 AUROC, two orders of magnitude
short of the 0.336 it produced on its author's data, and the control on the
control holds: the same protocol moves the norm-matched random axis D by only
0.0020, so the axis-A movement is not a pure normalisation artefact. Under the
semantic labels the same protocol gives −0.0397 [−0.0763, −0.0047] — still small.
Text overlap between scored items and axis-fit strings is **zero on every
member**, re-asserted here rather than inherited, and the separate non-zero
prompt-level overlap is bounded by a drop-those-items sensitivity column.

## Things worth knowing before reusing this

- **The rubric's CANONICAL/NON-CANONICAL split is not the regex's split.** Of the
  items both criteria call refusals, 54 of 267 (20.2%) open with a frozen refusal
  opener and are still labelled `REFUSAL_NONCANONICAL` by the judge — and the
  drift is strongly member-dependent (0/27 on Qwen3-1.7B-Base, 17/25 on
  Llama-3.2-3B-Instruct). That is
  why `n_semantic_refusal_regex_missed` is reported beside
  `n_refusal_noncanonical`; taking the rubric class as "refusals the regex
  missed" over-counts by more than 2x here (83 vs 38). Per-member rubric-drift
  statistics are in `part1.per_member.*.rubric_drift`.
- **6 of the 30 archived members have a `detect_<KEY>.json` but no
  `proj_<KEY>.npz`** — the archived `gpu_stage` writes the projections AFTER the
  detection statistics and those six were scored by an earlier pass of the same
  run (file mtimes 01:27 vs 02:30). Three of them are POWERED. The
  pre-registered fallback was applied: the re-analysis is restricted to the 24
  members with projections and the missing ones are listed with their archived
  numbers in `metadata.powered_set`.
- **The subset is deliberately boundary-heavy** (regex label x stratum x
  projection tertile, middle tertile at 2x), so raw per-arm accuracy on it is NOT
  a corpus estimate. Every corpus-level quantity is inverse-probability-weighted
  back to the member's item population and both weighted and unweighted numbers
  are reported.
- **`PARTIAL` and `DEGENERATE` are excluded from the primary semantic AUROC.**
  All three PARTIAL treatments (as refusal / as compliance / dropped) ship as a
  sensitivity column, because the audited probe measured the REFUSAL↔PARTIAL
  boundary as the one place LLM annotators themselves disagree (per-class kappa
  0.391 / 0.054).
- **Judge-error attenuation** uses the FOUR-class audited confusion of the same
  judge configuration (`art_gYmQllaTCGT5`, `arm2_repaired`, sensitivity 0.688 /
  specificity 0.923 strict). The audit predates the five-class rubric, so the
  correction is an approximation reported alongside the raw number, never in
  place of it.
- Every pooled quantity is reported at **both aggregation units** with both
  verdict strings (H-U); the bootstrap resampling unit is the lineage in both
  cases and the units differ only in whether members are averaged within lineage
  first.

## Deliverables

| file | what |
|---|---|
| `eval_out.json` (+ `full_`/`mini_`/`preview_`) | schema-validated (`exp_eval_sol_out`); 660 re-labelled examples with both criteria, the axis score and the IPW weight; `metadata.paper_numbers` is the block every quoted number is read from |
| `results/section_5_1_paragraph.md` | drop-in replacement paragraph, generated from `eval_out.json` by f-string substitution — no hand-typed numbers, regenerable byte-identically |
| `results/noncanonical_examples.md` | 20 verbatim boundary examples the regex missed, with prompt, full generated text, both verdicts, projection and percentile in the compliance distribution |
| `results/prereg_eval.json` | every threshold and verdict rule, sha256-stamped before any new AUROC or label |
| `results/r0_gate.json` | the per-member reproduction table |
| `results/sampling_frame.json`, `results/labels5.json` | the frame (cells, weights) and the five-class labels |
| `results/cost_ledger.jsonl`, `results/judge_cache_5class_local.jsonl` | cost discipline and the warm cache (a rerun is $0.00) |
| `figures/fig1_dumbbell_regex_vs_semantic.pdf` | per-member paired AUROC, regex vs semantic label, with CIs and the random band |
| `figures/fig2_protocols_by_axis.pdf` | per-member AUROC across the four normalisation protocols for axes A, B, D |
