# Make every paper number check out

A $0, no-GPU, no-network reanalysis that builds a machine-readable claim ledger over every numeric claim in the iteration-4 draft, resolves each to a JSON pointer into a sha256-stamped source, and ships a regeneration harness that makes a hand-typed number structurally impossible under revision.

**Verdict: `NUMBER_DISCIPLINE_CLEAN_WITH_LOGGED_EXCEPTIONS`.**

## The ledger

911 numeric and verdict-string claims were extracted from 142 text surfaces across all four of the draft's number-bearing surfaces -- prose, markdown tables, figure captions and figure summaries -- plus the abstract. Flags before repair:

| flag | n |
|---|---|
| `MATCH` | 421 |
| `UNIT_MISSING` | 227 |
| `ROUNDING_OK` | 200 |
| `UNTRACEABLE` | 43 |
| `STALE_SOURCE` | 13 |
| `DIRECTIONAL_ROUNDING` | 7 |

After repair, the regenerated prose bundle and abstract skeleton audit at 150 claims with 0 flags. The residue on the ORIGINAL draft is 43 `UNTRACEABLE` rows, of which 15 are values attributed to cited literature rather than to any artifact of this project; each carries a search log naming what was searched.

The load-bearing number is `UNIT_MISSING` = 227: that many claims resolve to a source value while the sentence never says which aggregation unit produced it. On this paper's own evidence an unlabelled correlation is not merely imprecise -- changing only the unit moves oriented rho by a median 0.238 and flips 5 of 16 signs -- so it is ambiguous between two different estimands. Every sentence in the regenerated bundle names its unit inline, which is why the post-repair count is zero.

## The three drifts, resolved

**(a) The AUROC minimum is three numbers over three named populations, not one bound.** Over all members with a defined AUROC it is 0.685 (`Llama_3p2_3B_Instruct`, verdict AMBIGUOUS); over the READS members it is 0.691 (`Llama_3p2_1B_Instruct`); over the detection-powered members it is 0.685 (`Llama_3p2_3B_Instruct`). The draft's bare '>= 0.68' is none of them and is flagged DIRECTIONAL_ROUNDING on 7 sentences.

**(b) 'Measurable' is 21, not 20.** The tally is 20 READS + 1 AMBIGUOUS + 9 UNDEFINED over 30 members; the AMBIGUOUS member is named explicitly in the corrected sentence.

**(c) The stale 18/0/10 block is diagnosed, not guessed.** It is the panel state recorded in `backfill.log` before five base checkpoints were re-run under the plain wrapper, with the AMBIGUOUS class omitted -- which is why it sums to 28. See `out/corrected_summary_block.md` for the drop-in replacement and the file:line evidence.

## The regeneration harness

`out/render.py` resolves `{{ptr:ALIAS#/pointer|fmt}}` against a frozen sha256 registry. Six assertions execute on every run:

| assertion | result |
|---|---|
| rendering twice is byte-identical | True |
| unresolved placeholders | 0 |
| bare numerals in the template source | 0 |
| flags on the re-audited rendered text | 0 |
| mutation test (a perturbed source changes the output) | passed |
| the standalone `render.py` CLI reproduces the bundle byte for byte | True |

## Tables

`out/tables/table_detection_per_member.{md,csv}` -- 30 rows, each carrying the two columns the draft omitted: `n refusals / n compliances` and `powered (y/N)`. The computed powered count is 14. `out/tables/table_dual_aggregation.{md,csv}` -- 108 rows, the aggregation unit named in every row label. H-G status: `H_G_ROWS=ABSENT_AT_RUN_TIME`.

`out/table_numbering_map.json` renumbers by first appearance: Table 3 -> 1, Table 5 -> 2, Table 2 -> 3, Table 4 -> 4, Table 1 -> 5; bijection = True.

## Bibliography

45 entries parsed; 2 carry a truncation flag; reference [11] is completed to its full 8-author list from the audited BibTeX. All 9 corrections the citation audit found are re-asserted against the current draft: 9 APPLIED.

## Cost and runtime

`cost_usd = 0.0` (asserted). Wall clock 22 s, single process, no GPU, no network.

## Files

```
eval.py                       driver / assembler
stage0_ingest.py              sha256 manifest + the reproduction gate
stage1_ledger.py              the claim ledger and the three drifts
stage2_render.py              the regeneration harness + 5 assertions
stage3_tables.py              tables + the numbering map
stage5_bibliography.py        reference completion + re-assertion
ledgerlib.py                  claim extraction and pointer resolution
derived.py                    derived quantities (DERIVED_NOW_GENERATED)
prose_spec.py                 the prose and abstract TEMPLATES
out/render.py                 the template engine (standalone runnable)
out/ledger.csv                one row per claim
out/prose_bundle.md           drop-in rendered prose
out/abstract_skeleton.md      pointer-only abstract
out/corrected_summary_block.md
out/references_completed.md
out/tables/*.md, *.csv
out/cross_references_renumbered.md
out/_draft_paper_text.md          the draft under audit, as extracted
tests.py                      13 unit tests over the machinery
```
