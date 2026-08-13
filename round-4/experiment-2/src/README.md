# Does the refusal axis read or only push?

An abliterated-panel extension of the iteration-3 induction/detection
dissociation. Every panel member is measured in **both roles of the same five
axes** — as a *reader* (held-out AUROC of the axis projection on the model's own
generated refusals versus compliances) and as an *actuator* (a steering sweep
reported in axis-contrast units) — so that "reads" and "pushes" are properties of
one object rather than of two separate experiments.

## What it found

30 checkpoints over 7 lineages, measured in both roles. Full numbers in
[`RESULTS.md`](RESULTS.md); the headline is a **reversal of the result it set out
to strengthen**.

- **The axis reads refusal wherever reading is measurable at all.** 18 of 30
  members return READS, **0 return AT_CHANCE**, and the remaining 10 are
  UNDEFINED — the model emits too few spontaneous refusals for the statistic to
  exist. The iteration-3 "at chance as a reader" finding does not survive being
  measured on each model's *own* spontaneous text.
- **Abliteration removes the refusals, not the readability.** Of 18
  abliterated-class checkpoints, 14 never produced the 40 spontaneous refusals
  the detection role needs, even after the full escalation ladder (1,585
  generations each). Their median spontaneous refusal rate is 0.008. So K = 0 of
  M = 4, and the pre-registered ladder's `K<3` branch applies.
- **Induction is the arm that survives, and it is heterogeneous.** Across 10
  within-lineage abliterated-versus-parent pairs, steering still induces refusal
  on 5 abliterated checkpoints and fails on 4 whose parent was steerable (median
  change in max induced rate −0.306).
- **The two roles are positively coupled**, which this study could never see
  before: ρ = 0.629 [0.465, 0.803] over **70 (member, axis) pairs** (the previous
  evidence base was 4 points), lineage-bootstrapped, with a within-member mean
  rank correlation of 0.715.
- **The norm-mismatch rival is ruled out.** At matched axis-contrast units the
  A-over-B induction gap survives on 22 of 30 members
  (`NORM_MISMATCH_DOES_NOT_EXPLAIN`), so arXiv:2603.22061's magnitude-collapse
  account does not explain it. One of the two breadth-panel counterexamples is a
  genuine inducer; the other is a norm artifact.
- **A measured floor for any steering claim.** A *random* direction injected at
  axis A's own matched magnitude induces refusal at ≥ 0.10 on 7 of 30 members
  (worst 0.389). And the empirical random-direction AUROC band spans ±0.075 to
  ±0.500 across members — so the textbook expectation that a random direction
  reads at 0.500 is wrong by a wide, model-dependent margin.

## The five axes

| axis | construction |
|---|---|
| `A_canned` | diff-in-means over canned refusal vs compliance responses (the canonical refusal axis) |
| `B_paraphrase` | the same construction from paraphrases whose surface tokens are disjoint from the scoring lexicon |
| `C_stylistic` | a non-safety register contrast (formal vs casual) |
| `D_random0` | a matched random direction, given axis A's contrast magnitude so the injected vector has identical norm |
| `E_prompt_contrast` | harmful-vs-benign contrast at the last **prompt** token |

## Layout

| path | what it is |
|---|---|
| `method.py` | orchestrator: `--stage prereg / panel / gpu / analysis` |
| `explib.py` | panel resolution, statistics, contrast units, the ratchet |
| `gpu_stage.py` | per-member axes (S3), detection (S4), induction (S5) |
| `prereg.py` | the pre-registration, hashed before any new AUROC existed |
| `tests.py` | validation gates T0–T3 (`--gpu` adds T3) |
| `judge_stage.py` | the capped, cache-first judge subsample |
| `report.py` | `RESULTS.md`, formatted **from** `method_out.json` only |
| `figures.py` | the three figures, regenerated from the analysis JSON only |
| `lib/` | **byte-identical copy** of `iter_3/gen_art/gen_art_experiment_1/lib` |
| `results/` | per-member checkpoints, projections, panel, prereg, gates |
| `method_out.json` | the schema-validated deliverable |

## Run it

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.11.0 \
    --index-url https://download.pytorch.org/whl/cu128
uv pip install --python=.venv/bin/python -r <(grep -v '^torch==' pyproject-deps.txt)

.venv/bin/python tests.py --gpu          # gates T0-T3; nothing runs until these pass
.venv/bin/python method.py --stage prereg
.venv/bin/python method.py --stage panel
.venv/bin/python method.py --stage gpu --budget-min 190
.venv/bin/python judge_stage.py          # optional; the regex is primary
.venv/bin/python method.py --stage analysis
.venv/bin/python report.py && .venv/bin/python figures.py
```

The GPU stage is **checkpointed per member** (`results/detect_<key>.json`,
`results/induce_<key>.json`, written atomically), so an interrupted run yields a
complete subset rather than a half-measured member, and re-running resumes.

## What is reused and what is new

`lib/*.py` is copied byte-identically from the iteration-3 archive and its
sha256s are recorded on both sides in `results/archive_inventory.json` — the
refusal regex, the axis-fitting primitives with their frozen response /
paraphrase / style string sets, the steering hook and batched decoder, and the
non-parametric `alpha_50` interpolator all come from there.

The GPU stage is **reimplemented and validated against the archive**, not reused.
The artifact plan expected `gen_art_evaluation_1/gpu_stage.py` to have been
deleted; it is in fact on disk, but it re-encodes *archived* text on six fixed
checkpoints, whereas this study has to generate each new member's own text. The
reimplementation is held to the archive by two gates: T1 reproduces every
archived per-axis AUROC exactly with the new statistics code and no model, and
the per-checkpoint axis-cosine gate compares each re-derived direction to the
archived `.npy`.

## Three things worth knowing before reading the numbers

1. **The layer rule is relative depth 0.25, not 0.30.** The plan asserted the
   archived tie-break was 0.30; all six archived checkpoints are `L=7` of 28
   layers, which is exactly 0.25. The pre-registration uses what the archive
   actually did, and says so.
2. **Only two axes are comparable to the archived directions.** `A_canned` and
   `E_prompt_contrast` are built identically and reproduce at cosine ≥ 0.999.
   `B` and `C` were built from different string sets in the archived evaluation,
   and `D` uses a different seed by design, so those three are reported rather
   than scored.
3. **There are three recorded amendments** (all in `results/prereg.json`, each
   with its trigger, diagnosis and what it did *not* change).
   - *AMENDMENT-1*: the sanity gate fired on the first member — the matched
     *random* axis read refusal at AUROC 0.171. That is the residual-norm
     channel: a raw projection is `‖h‖·cos(angle)`, so any direction inherits a
     norm difference between the classes. A norm-controlled readout
     `cos = (h·u)/‖h‖` is now computed for every axis on every member.
   - *AMENDMENT-2*: the gate fired again on the norm-controlled readout, because
     one random draw is not a null distribution — residual streams are
     anisotropic. 20 fresh random directions per member now give the *measured*
     null the gate is read against.
   - *AMENDMENT-3*: the axis-reproduction gate passed on all four archived chat
     checkpoints and failed on both archived **base** ones (axis E cosine 0.13
     and 0.09). Cause: `auto` renderer selection picked the chat template for
     Qwen3-*-Base, whose tokenizer ships one despite the model never being tuned
     to follow it. The renderer is now chosen by member class, the five base
     members were re-measured, and all six archived checkpoints reproduce at
     cosine ≥ 0.9999.

   None of the three changed a verdict threshold, panel membership or a headline;
   the pre-registered projection readout remains primary throughout and both
   readouts are reported side by side, including the headline K/M count.
