# Make every paper number check out

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_Xx1VPyGi4nAT`

## Layman Summary

Checks every number in the paper draft against the files that produced it, explains the three places the numbers disagreed, and rebuilds the prose so no number can ever be typed by hand again.

## Full Summary

VERDICT: NUMBER_DISCIPLINE_CLEAN_WITH_LOGGED_EXCEPTIONS. 23 s on CPU, $0.00 LLM spend (cost_usd == 0.0 asserted), no GPU, no network. 28 input files sha256-stamped (declared deps plus UNDECLARED_BUT_STAMPED evaluation/paper artifacts); the 8-leg ingest gate reproduces every archived headline to full float repr and PASSED.

THE CLAIM LEDGER (eval_out.json:metadata.claim_ledger + out/ledger.csv). 911 numeric and verdict-string claims over 142 surfaces; audited on all four number-bearing surfaces (prose, tables, figure captions, figure summaries) plus the abstract. Flags BEFORE repair: MATCH 421 / ROUNDING_OK 200 / UNIT_MISSING 227 / UNTRACEABLE 43 / STALE_SOURCE 13 / DIRECTIONAL_ROUNDING 7 / VALUE_MISMATCH 0. AFTER repair the regenerated prose bundle + abstract skeleton re-audit at 150 claims with 0 flags. UNIT_MISSING = 227 is the load-bearing number: that many claims resolve to a source value while the sentence never names its aggregation unit, and on this paper's own evidence the unit moves oriented rho by a median 0.238 and flips 5 of 16 signs.

METHOD CORRECTION worth reusing: an unfiltered index over 152,118 numeric leaves resolves almost any 2-decimal number to SOMETHING, producing false MATCHes. A two-tier index is required - 51,178 'reportable' summary-statistic pointers resolve claims, the rest only populate an UNTRACEABLE's search log - plus gating on semantic key-compatibility and per-token type.

THE THREE DRIFTS, resolved by naming POPULATIONS. (a) min axis-A AUROC = 0.6845 over all members with a defined AUROC (Llama_3p2_3B_Instruct, AMBIGUOUS, 282/282, powered y), 0.6908 over READS members (Llama_3p2_1B_Instruct, 172/172), 0.6845 over powered-and-defined; the bare '>= 0.68' matches none and is flagged DIRECTIONAL_ROUNDING on 7 sentences. (b) 'measurable' is 21, not 20 (20 READS + 1 AMBIGUOUS + 9 UNDEFINED over 30; 14 powered, NOT the plan's expected 13). (c) The stale 18/0/10 is diagnosed exactly, not guessed: it is backfill.log's panel state (18 READS / 2 AMBIGUOUS / 10 UNDEFINED over 30) with the AMBIGUOUS class dropped - which is why it sums to 28 - before rerun_base.log re-ran five base checkpoints under the plain wrapper, moving Qwen2p5_0p5B AMBIGUOUS->READS and Qwen3_0p6B_Base UNDEFINED->READS. A grep for a writer finds report.py:428 emitting RESULTS.md and ZERO writers for README.md (line 16) or the registered summary: one generated tally, one hand-typed stale one, no second live code path. BONUS DEFECT for H-K: the code's UNDEFINED gate is a non-finite bootstrap CI (fires at <= 1 refusal, explib.verdict_from_ci), NOT the Method's '< 40 refusals' (that rule drives the separate `powered` flag, gpu_stage.py:343) - which is why members with 6-33 refusals carry READS while unpowered.

REGENERATION HARNESS (out/render.py, standalone-runnable). Template {{ptr:ALIAS#/rfc6901|fmt}} over a frozen sha256 registry. SIX executed assertions, all pass: byte-identical twice; 0 unresolved placeholders; 0 bare numerals under a NO_BARE_NUMERAL lint with 12 itemised allow-list entries; 0 flags on the re-audited rendered text; mutation test passed (perturbing a source value changes the output, so pointers are live); the standalone CLI reproduces the bundle byte for byte. Deterministic across two full reruns (runtime excluded).

TABLES + BIB. out/tables/table_detection_per_member.{md,csv}: 30 rows carrying the two omitted columns 'n refusals / n compliances' and 'powered (y/N)', plus norm-controlled cos and induction, with a totals footer. table_dual_aggregation.{md,csv}: 108 rows, unit named in every row label, incl. the 52-member scale panel; H_G_ROWS=ABSENT_AT_RUN_TIME (iter_5 experiment workspaces empty), so a schema-stable stub with exact row labels and pointer names ships instead - no value forecast. Numbering by first appearance: Table 3->1, 5->2, 2->3, 4->4, 1->5, bijection asserted, 0 dangling refs. Bibliography: 45 entries parsed, [11] completed to its full 8-author list from the audited BibTeX; all 9 citation-audit corrections re-asserted APPLIED (0 web lookups).

LOGGED EXCEPTIONS (4): 43 UNTRACEABLE on the ORIGINAL draft (15 external-literature values from cited works, 28 internal - each with a search log); 13 STALE_SOURCE sentences owned by H-K; 7 DIRECTIONAL_ROUNDING; H-G absent. 4 claims became DERIVED_NOW_GENERATED via auditable derivation functions (the 2.6e-4 reproduction gap, the AMS Table-I percentage deltas, the verdict-tally sums, the random-null reading band 0.075-0.500).

DELIVERABLES: eval.py + full/mini/preview_eval_out.json (all schema-valid), out/{ledger.csv, render.py, prose_template.md, prose_bundle.md, abstract_template.md, abstract_skeleton.md, corrected_summary_block.md, references_completed.md, cross_references_renumbered.md, table_numbering_map.json, derived.json, stage*.json, tables/}, tests.py (13/13), README.md rendered from JSON. GEN_PAPER_TEXT can paste out/prose_bundle.md and out/abstract_skeleton.md directly, and re-run out/render.py after any source refresh.

## Dependencies

- `art_1xT3w1joqeJ8` — archive
- `art_CZaytBH8uL4_` — archive
- `art_3Cndd5cKsYV0` — tables
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
