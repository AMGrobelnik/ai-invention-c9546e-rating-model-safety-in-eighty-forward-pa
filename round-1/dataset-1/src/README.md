# Frozen prompt corpus and verified model-panel manifest

One deliverable — `full_data_out.json` — holding **exactly 8 datasets / 2,113 rows**. Every
row carries `metadata_fold` = its dataset name, so a downstream artifact slices with a single
filter. Schema: `{input, output, metadata_fold, metadata_uid, metadata_block_version,
metadata_meta{...}}`.

`full_data_out.json` (3.5 MiB) + `mini_data_out.json` + `preview_data_out.json`, all three
validated against `exp_sel_data_out`.

## The 8 datasets

| dataset | rows | source (pinned) | licence |
|---|---:|---|---|
| `harmless_dynamics` | 43 | no_robots + dolly-15k, GPU-vetted | CC-BY-NC-4.0 / CC-BY-SA-3.0 |
| `xstest_overrefusal` | 450 | `Paul/XSTest` (XSTest v2, 250 safe + 200 unsafe) | CC-BY-4.0 |
| `plain_harmful` | 594 | JBB-Behaviors + AdvBench, deduped union | MIT |
| `jailbreak_suite` | 400 | 80 behaviors × 5 published templates | mixed |
| `layer_contrast` | 256 | 128 forbidden-question + 128 harmless-alpaca | MIT / CC-BY-NC-4.0 |
| `wikitext_fluency` | 200 | WikiText-2-raw-v1 test, 150–400-word passages | CC-BY-SA-3.0 |
| `refusal_token_lexicon` | 10 | per-tokenizer-family token id lists | n/a |
| `panel_manifest` | 160 | verified HF checkpoints | per-row |

**The plan's four extra resources are not ninth datasets, so they are folded into their
parents rather than dropped.** Each is one boolean filter away:

| resource | where it lives now |
|---|---|
| B3b widened pool | `plain_harmful` rows with `meta.in_core80 == false` (80 of 594 are the stratified core the jailbreak suite pairs against) |
| jailbreak template sidecar | `meta.template_text` / `meta.prefill_template` / `meta.template_source` on every `jailbreak_suite` row, plus the whole table once at `metadata.manifest.jailbreak_suite.templates` |
| B1 vetting rejects | `harmless_dynamics` rows with `meta.selected == false` and `meta.reject_reasons` (40 selected, 3 rejected) |
| `_manifest` | `metadata.manifest`, keyed by dataset — per-dataset source repo, revision SHA, licence, row count, retrieval timestamp and sha256, plus `metadata.assertions` with all 27 results |

**Frozen, not nominally frozen.** Every dataset records its source's resolved revision SHA (or
pinned git commit, for AdvBench) and a sha256 over its serialized rows, in `metadata.manifest`.
`data.py` reads only the local copies in `temp/datasets/` — no network — so re-running it
reproduces byte-identical datasets. Nothing is synthesized: the sole generation step is
mechanical instantiation of published jailbreak templates over real behaviors.

## Decisions worth knowing

**`walledai/*` is gated.** XSTest, AdvBench, HarmBench and StrongREJECT all 403 there with the
available token. XSTest comes from the ungated `Paul/XSTest` mirror (450 rows, split and 10
prompt types intact); AdvBench from the authoritative `llm-attacks/llm-attacks` GitHub CSV at
a pinned commit. Recorded in `_manifest`, not silently substituted.

**`mlabonne/harmful_behaviors` is deliberately NOT the layer-contrast harmful half.** It is an
AdvBench repackaging, so using it would break disjointness from `plain_harmful`. The harmful
half comes instead from the Forbidden-Question-Set (Shen et al., CCS 2024), independently
constructed over 13 OpenAI-policy scenarios. Disjointness is asserted at build time, not
assumed: exact overlap 0, max TF-IDF cosine **0.650** against XSTest ∪ plain_harmful ∪ pool,
threshold 0.85.

**`t1_prefill` is not concatenated into the user turn.** Prefill rows carry
`meta.delivery='assistant_prefill'` with `meta.user_text` and `meta.prefill_text` separate, so
the executor inserts the prefill in the assistant slot. Every other template is
`delivery='user_turn'` with an empty prefill; `t5` stores the plaintext beside the base64
wrapper. The suite is asserted to be a complete 80 × 5 grid.

**B1 needed a filter the plan did not name.** Inspecting the preview showed `no_robots` "Chat"
rows are frequently *persona/system definitions* ("Olivia is a helpful chatbot that…"), not
user turns. 717 such rows were being admitted. B1 now additionally requires each prompt to be
a question or an imperative and rejects persona prompts and first-person emotional disclosure
(717 + 490 + 4 dropped, all counted in the manifest). The 10 topical categories the plan asks
for are *assigned* — the source corpora carry task-type labels only — by a disclosed keyword
vote with two overrides; the original task label is kept as `meta.task_type`. Treat the topic
label as the stratification device it is, not as a claim about the prompt. Result: 40 rows,
10 topics, 4 each, from 200 candidates of which 197 survived vetting (Qwen3-0.6B, 3 rollouts
× 64 tokens).

**B7's membership criterion was changed from the one specified, on evidence.** The planned
criterion — count ≥ 5 on harmful prompts with harmful/benign rate ratio ≥ 3 — cannot separate
refusal from topic, because the harmful and benign prompt sets differ in both. Run as
specified it admitted `Creating`, `Writing`, `Hack`, `Script` and `Title` as "refusal-onset"
tokens: AdvBench topic words, not refusals. The shipped lists instead condition on the
rollout's own behaviour — a token is a refusal onset when it is the *actual first generated
token* of ≥ 3 greedy rollouts whose opening matches a refusal regex, over the same 200 harmful
+ 40 harmless prompts. Topic is matched by construction. The old criterion's statistics are
retained per token as diagnostics, and `n_rate_criterion_only` counts what it would have
wrongly admitted. All 10 families are empirical, disjoint, in-vocab, and clear the ≥12 / ≥20
floors.

That change surfaced a result worth carrying forward: **refusal onset is close to a one-token
event.** On safety-aligned instruct models the first generated token of a refusal is `I` in
essentially every case (Gemma-2-2b-it 195/240 refusing rollouts, Falcon3-1B 190, Llama-3.2-1B
172, Qwen2.5-0.5B 177, Granite-3.1-2b 146). Per-family greedy refusal rates ship as
`meta.greedy_refusal_rate` and span 0.00 (Pythia-410m, danube3-500m-chat) to 0.81 (Gemma),
with Qwen3-0.6B at 0.05 with thinking disabled — itself a datum.

## Panel

160 candidate rows, **137 verified**, of which **59 at ≤ 4.2B params over 31 weight lineages**
(base 20 / instruct 18 / abliterated 8 / behavioral-uncensored 13) — the ≥18 lineage floor is
met with room. Verified = `model_info` returned, `config.json` and the tokenizer downloaded
and loaded by `AutoConfig`/`AutoTokenizer`, repo not gated-without-access. **Weights are never
downloaded for verification.** Failed candidates are kept with `verify_error` filled in —
`meta-llama/*`, `google/gemma-2*` and the v1 `huihui-ai/Qwen3-*-abliterated` repos are gated
here, and ungated mirrors are added as *separate* rows with `meta.mirror_of` set rather than
silently swapped in.

`lineage_id` is the pretrained base at the root of the derivation chain, with the chain
recorded in `meta.lineage_evidence`. It is the bootstrap resampling unit for every downstream
claim, so it is derived, not guessed.

**H4 class membership.** Discovery over 10 queries, then a model-card grep for
`abliterat|orthogonaliz|refusal direction|ablation|failspy|mergekit`. 2 models are
`disqualified_by_provenance` with the matching card text quoted. 6 clean behavioural-uncensored
candidates survive at ≤ 4.2B, one of which — `UnfilteredAI/DAN-Qwen3-1.7B` — shares the
`Qwen/Qwen3-1.7B-Base` lineage with the base/instruct/abliterated triad, exactly the
within-lineage contrast H4 needs. A name matching "uncensored"/"lexi"/"dolphin" is *not*
sufficient: candidacy also requires a causal-LM architecture and an explicit uncensored /
no-refusal / compliance claim in the card; rows failing either are `not_applicable` with the
reason recorded.

## Pipeline

Run in this order; each stage writes to `temp/` and the next reads it.

```
uv run preview_candidates.py   # sweep 25 candidate datasets (metadata, size, columns)
uv run select_datasets.py      # KEEP/DISCARD + download the 15 kept sources at pinned revisions
uv run panel.py                # B8: seeded + discovery model-panel verification  -> temp/panel_rows.json
uv run data.py                 # build everything                                 -> temp/b1_candidates.json (+ fails on stale vetting)
uv run vet.py                  # B1 GPU vetting                                   -> temp/b1_vetted.json
uv run data.py                 # rebuild                                          -> full_data_out.json
uv run harvest_tokens.py       # B7 GPU token harvest                             -> temp/b7_tokens.json
uv run data.py                 # final build
```

`data.py` deliberately refuses to build when `temp/b1_vetted.json` does not match the
candidate pool it just constructed — a stale vetting table would silently ship unvetted
prompts, so the recovery path is an error, not a warning. It also asserts that the set of
emitted datasets equals the declared eight.

`pyproject.toml` pins all 95 installed packages to exact versions (`uv pip freeze`). Note the
cu124 torch index: the host driver is CUDA 12.4 and the default PyPI wheel fails at import
with `undefined symbol: ncclCommResume`, so `uv run` must not resolve torch from PyPI.

`temp/dataset_selection.json` records all 15 kept sources with why-kept and used-for, and 12
discarded with reasons; raw copies live in `temp/datasets/`.

All 27 build assertions pass — row floors (whole-dataset and subset), exactly-8-datasets, B5
disjointness, B4 pair/template resolution, inlined template text and grid completeness, B7
vocab bounds and disjointness, B8 revision/lineage, B1 topic spread, B2 split preservation, B3
core-80 stratification, B5 balance, and no duplicate uid anywhere. They ship in
`metadata.assertions`.

**Licence note:** `harmless_dynamics` (no_robots) and the `layer_contrast` benign half
(alpaca-derived) are **CC-BY-NC-4.0, non-commercial**. Recorded explicitly in `_manifest`.
