# Does the paraphrase refit hold at scale?

Iteration 3 produced exactly one positive result: refitting our AMS
reimplementation's contrast set on token-disjoint paraphrases lifted its Spearman
correlation with the judged plain-harmful refusal rate from **0.358** to
**0.654** on 19 checkpoints over 7 weight lineages. At 7 lineages the exhaustive
lineage-permutation floor is 1/5040, so the improvement sat close to the smallest
p the design could express, and a single hand-written wording carried the whole
claim.

This artifact replicates that finding on a panel grown from 7 to **28 analysed
weight lineages** (29 enrolled; one lineage is lost to a model that will not run
under this transformers version, recorded with its exception string), adds a **second, independently authored** (LLM-generated,
machine-verified) token-disjoint paraphrase set so the improvement cannot be a
lucky wording, collects the missing ground truth for new members with the
archive's own instrument, and reports every correlation at **both** aggregation
units (member level with a lineage-clustered resample, and lineage-aggregated).

Everything is pre-registered and sha256-stamped before any correlation is
computed. `SURVIVES` and `DOES_NOT_SURVIVE` are both publishable; the failure
branch adjudicates the ambiguity iteration 3 left open.

## Deliverables

| file | what it is |
|---|---|
| `method.py` | the driver: reuse manifest, T0 unit tests, panel construction, pre-registration, per-member GPU pass, ground truth, analysis |
| `build_para_b.py` | STEP 2: generates and freezes paraphrase SET B (run once; cached) |
| `summarise.py` | renders `RESULTS.md` from `method_out.json` (numbers are read, never retyped) |
| `prereg_iter4.json` | the immutable pre-registration, sha256 printed to the log |
| `para_set_b.json` | frozen paraphrase SET B |
| `method_out.json` | the machine-readable result (+ `mini_` / `preview_`) |
| `RESULTS.md` | the rendered report |
| `results/panel_iter4.json` | the frozen panel, one row per enrolled member |
| `results/panel_selection.json` | every eligibility rejection with a machine-readable reason |
| `results/paraphrase_audit_b.json` | per-string SET-B generation and verification detail |
| `results/iter4_member_<key>.json` | one file per member (the run is resumable by file existence) |
| `results/gt_calibration.json` | the cross-pipeline ground-truth calibration |
| `results/reuse_manifest.json` | byte-identity proof for every reused library file |
| `results/t4_archive_only_method_out.json` | the T4 dry run on the archived 19 alone, kept as evidence: it reproduces iteration 3's rho 0.3578 / 0.6541, Delta +0.2963, 6/19 verdict changes and the 1/5040 exhaustive floor |
| `results/t0_unit_tests.json` | the offline statistics/apparatus tests |
| `gens/behaviour_<key>.jsonl` | the core-80 greedy generations for members needing ground truth |

## Reproduction

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.11.0 \
    --index-url https://download.pytorch.org/whl/cu128
uv pip install --python=.venv/bin/python -r <(grep -v '^torch==' pyproject-deps.txt)

# STEP 2 -- paraphrase SET B (once; ~$0.01, cached in paraphrase_cache.jsonl)
.venv/bin/python build_para_b.py

# T1  one-member smoke test (the reuse-chain confirmation signal)
.venv/bin/python method.py --tier smoke

# T4  analysis dry run on the archived 19 only
.venv/bin/python method.py --tier archive

# T5  the full run
.venv/bin/python method.py --tier full --max-hours 4.5

# render the report
.venv/bin/python summarise.py
```

Every member writes its own `results/iter4_member_<key>.json` and is skipped on a
rerun, so the run is resumable and a crash costs one member. HF snapshots are
purged after each member; the whole panel never needs more than one model
resident at a time.

## What is reused, and how that is proven

`lib/` is copied byte-identically from the iteration-2 archive and `lib_iter3/`
from iteration 3; `build_reuse_manifest()` asserts sha256 equality on every file
and fails hard on a mismatch. The stronger proof is behavioural and runs on every
archived member:

* `ams.score_model` recomputed from scratch must land within 1e-3 of the sigma
  the iteration-2 archive recorded, and
* the SET-A refit must land within 1e-3 of the sigma iteration 3 recorded.

Both are reported per member in `results/iter4_member_<key>.json`
(`ams_reuse_check`, `refitA_reuse_check`) and aggregated in
`results.sensitivity`. A failure there would make the reproduction failure the
headline, not the replication -- that branch is pre-registered.

Ground truth is reused the same way: the archived 19 members' `y_refusal` is read
from the archive and never recomputed, and the judge cache is seeded from
`ARCH/judge_cache.jsonl`, so a member whose completions reproduce byte-identically
costs $0 to rescore. The cross-pipeline calibration in `results/gt_calibration.json`
is what licenses pooling the archived and newly measured blocks.

## Hardware and cost

1x NVIDIA RTX A4500 (20 GB), 48 CPU, 270 GB RAM, 40 GB writable overlay for the
HF cache. LLM spend is dominated by nothing: paraphrase SET B costs about $0.01
and the judge runs under a hard $3.00 abort with a seeded cache. The exact
totals are in `method_out.json` under `metadata.cost_usd_total`.

## Naming

Throughout, the score is called **our AMS reimplementation** (arXiv:2608.05578),
never "AMS". The three published Table-I checkpoints are scored as a
reproduction gate and reported with their published values beside ours, but the
label does not change on the strength of that comparison.
