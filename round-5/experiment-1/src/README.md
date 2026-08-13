# Does the cheapest safety score survive?

Iteration 3 ran a five-score discrimination matrix against the judged
plain-harmful refusal rate on 19 checkpoints over 7 weight lineages. Exactly one
score had a lineage-clustered CI excluding zero at **both** aggregation units:
the **first-decoding-step logit-gap margin read on harmful prompts** — our
reimplementation of arXiv:2506.24056 — at rho 0.667 [0.439, 0.904] member and
0.929 [0.412, 1.000] lineage, for **80 forward passes and zero generations** per
model.

Iteration 4 then grew the panel to 52 members / 28 lineages / 11 architecture
families and used it to retire the AMS paraphrase refit. This artifact re-runs
the cheapest score on **that same frozen panel**, alongside its benign-regime
variant and our AMS reimplementation's sigma (both free at the same forward-pass
cost; sigma is the anchor that proves the panel really is the same panel).

Three verdicts were pre-registered and all three are publishable:
`HOLDS`, `HOLDS_AT_MEMBER_UNIT_ONLY`, `COLLAPSES` — plus `REPLAY_FAILED`, the
stop branch. The measured verdict, the pre-registration hashes and every number
behind them are in `RESULTS.md` and `method_out.json`.

## Measured outcome: **HOLDS**

All numbers below are quoted from `method_out.json`; `RESULTS.md` is rendered
from it and is the authority.

* 52/52 members scored, 28 lineages, 11 families, **0 generations**, 14,792
  forward passes, **$0.00** of LLM spend.
* `logit_gap_harmful`: rho **0.694** [0.495, 0.822] at the member unit,
  **0.564** [0.140, 0.826] at the lineage unit; Monte-Carlo lineage-permutation
  p at the 5.0e-6 floor; AUC 0.806; leave-one-lineage-out [0.661, 0.726] and
  leave-one-family-out [0.650, 0.772], sign-stable in every fold.
* **The decisive diagnostic passes.** archived-19 rho 0.667 vs new-33 rho 0.668,
  delta −0.0004. This is *not* the small-panel artefact the paraphrase refit
  turned out to be — the score transfers intact to 21 lineages it was never
  fitted on.
* **It is not parameter count.** Partial rho controlling for log10(params) is
  0.676 [0.475, 0.814]; rho(score, log10 params) is only 0.092.
* **It beats the anchor.** Paired on the same resampled lineages,
  `logit_gap_harmful` − `our_ams_sigma` = +0.421 [0.169, 0.684], `SCORE_BETTER`.
* **The harmful regime is load-bearing, and that is why the honesty statement is
  mandatory.** The benign-regime variant collapses to rho 0.129 [−0.168, 0.436].
  The saving is no generation, no judge, no benchmark, no reference model — it is
  NOT harmful-prompt-free.
* Reproduction is exact where it must be: the T0-REPLAY reproduces iteration 3's
  0.6673 [0.439, 0.904] / 0.929 to 4 decimals, and recomputing the 19 archived
  members from the models gives **identical ranks** (Spearman(iter3, iter5) =
  1.000, 0 rank positions moved), so every Spearman statistic is unchanged by the
  small numeric drift on the three members where it appears.

## The gate order is the design

Nothing downstream runs until the gate above it passes, and **no correlation of
any kind is computed** until the T0-REPLAY and the pre-registration stamp are
both green.

| gate | what it proves |
|---|---|
| reuse manifest | every file in `lib/` and `lib_iter3/` is sha256-identical to the iteration-4 archive; 46 archived inputs are hashed and recorded |
| T0a offline apparatus | 14 assertions on the statistics library against its own known answers (seed 20260812, 10,000 reps, the MC-vs-exhaustive permutation branch, the disattenuation factor, the collapse rule, the partial correlation, the block delta) |
| T0b constants | `ORIENTATION_MAP` recovered from iteration 3's driver **by `ast`, never by import** — that file calls `resource.setrlimit(RLIMIT_AS, 200 GB)` at module scope — and cross-checked against `prereg_iter3.json` |
| T0d panel + ground truth | 52 / 28 / 11, 19 archived + 33 new, y present for all 52, and the two calibration members reproducing 0.250 [0.168, 0.355] and 0.900 [0.815, 0.948] |
| **T3 T0-REPLAY** | iteration 3's archived-19 member rho reproduced to 4 decimals **before** any new correlation. Failure would have stopped the run and become the headline. |
| T4 stamp | `prereg_iter5.json` written, with both the file sha256 and a timestamp-free **content** sha256 that is identical across invocations |
| T1 smoke | one member end to end: token sets disjoint and in-vocab, lens calibration at 1e-3, 296 forward passes, **0 generations**, sigma reproducing the archive |
| T2 renderer | a base member takes the PLAIN renderer and an instruct member the chat template — the trap that cost iteration 4 its axis-E cosine |
| T6 post-run | 0 generations summed across the panel, `summarise.py` rendering byte-identically twice, the verdict quoted from the pre-registration rather than retyped |

## Deliverables

| file | what it is |
|---|---|
| `method.py` | the driver: reuse manifest, T0 gates, panel, replay, pre-registration, per-member GPU pass, analysis |
| `summarise.py` | renders `RESULTS.md`; every number is read from `method_out.json` by path, none is retyped (`--check` proves determinism) |
| `prereg_iter5.json` | the immutable pre-registration, both hashes logged |
| `method_out.json` | the machine-readable result (+ `mini_` / `preview_`) |
| `RESULTS.md` | the rendered report |
| `lib/`, `lib_iter3/` | byte-identical reuse from the iteration-4 archive — asserted, not asserted-about |
| `lib_iter5/` | the only NEW code: `constants.py` (ast extraction), `loader.py` (revision pinning), `agg5.py` (aggregation units, block split, controls) |
| `results/panel_iter5.json` | the frozen panel with every identity check |
| `results/t0_unit_tests.json` | the offline apparatus tests |
| `results/t0_replay_archive19.json` | the decisive replay, per member |
| `results/t3_archive_only_method_out.json` | the analysis restricted to the archived 19, kept as evidence |
| `results/reuse_manifest.json` | byte-identity proof and the environment |
| `results/iter5_member_<key>.json` | one file per member — the run is resumable by file existence |

## What is measured, and what it costs

Per checkpoint, with **zero generations**:

| score | forward passes | regime |
|---|---|---|
| `our_ams_sigma` (anchor) | 96 | 48 contrastive pairs x 3 concepts |
| `logit_gap_harmful` (**primary**) | 80 | plain-harmful core-80 |
| `logit_gap_benign` | 40 | 40 vetted harmless turns |
| `logit_gap_harmful_union` (secondary) | 80 | as primary, union-of-all-families onset set |

Scoring one new checkpoint with the primary score alone is **80 forward passes,
0 generations, 0 judge calls, 0 benchmark runs, 0 reference models**.

> The logit-gap harmful margin reads the margin ON HARMFUL PROMPTS. The saving is
> no generation, no judge, no benchmark, no reference model. It is NOT
> harmful-prompt-free.

## Deviations from the artifact plan, all measured

Recorded in `prereg_iter5.json` before any correlation, and repeated in
`RESULTS.md`:

1. **The plan's five UNRELIABLE-flagged members do not exist.** Iteration 4's
   archive carries no per-member `UNRELIABLE` field anywhere — not in
   `per_member_table`, not in any `results/iter4_member_<key>.json`; the string
   appears only inside verdict prose. The with/without sensitivity the plan asked
   for is replaced by two that ARE measurable: the archived-19 / new-33 block
   split, and members with vs without an empirical family lexicon.
2. **Revision pinning is new here.** `lib/models.py` is reused byte-identically
   and has no `revision` argument, so iteration 4 loaded default branches. A
   `PinnedModel` subclass in `lib_iter5` pins the frozen SHA and records the
   outcome per member.
3. **51 of 52 rows carry a revision, not 52.** `l1_abliterated`
   (`mlabonne/Qwen3-0.6B-abliterated`) is the one analysed member with no
   `panel_manifest` row, which is also why its tokenizer family has to be read
   off the iteration-2 archive.
4. **Five members have no empirical refusal-onset lexicon** for their tokenizer
   family (the corpus covers 10 families; the panel spans more). Their primary
   logit-gap columns are NULL with reason `MISSING_FAMILY_LEXICON` — never
   back-filled from another family's token ids. Because that is more than three,
   the pre-registered union-of-all-families SECONDARY column ships beside the
   primary null, never in place of it.

## Reproduction

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.11.0 \
    --index-url https://download.pytorch.org/whl/cu128
uv pip install --python=.venv/bin/python -r <(grep -v '^torch==' pyproject-deps.txt)

.venv/bin/python method.py --tier t0       # gates only, no GPU
.venv/bin/python method.py --tier smoke    # T1: one member, the reuse-chain signal
.venv/bin/python method.py --tier t2       # T2: renderer sanity (instruct + base)
.venv/bin/python method.py --tier archive  # T3: the archived 19 alone
.venv/bin/python method.py --tier full --max-hours 3.0
.venv/bin/python summarise.py --check
```

Members run smallest-parameter-count first, so a truncated run keeps the cheap
head; each writes `results/iter5_member_<key>.json` and is skipped on a rerun.
HF snapshots are purged after every member — the 40 GB overlay cannot hold 52
checkpoints.

## Hardware and cost

1x NVIDIA RTX A4500 (20 GB), 11 CPU, 57 GB container RAM, 40 GB writable overlay
for the HF cache. **LLM API spend: $0.00.** Ground truth is the frozen iteration-4
block, reused and never re-judged; no judge call is made and no generation is
produced anywhere in this artifact.
