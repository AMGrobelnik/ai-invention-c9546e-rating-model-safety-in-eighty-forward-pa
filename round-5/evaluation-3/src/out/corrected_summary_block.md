# Corrected top-line summary block

Drop-in replacement for the stale block in the read-versus-act artifact's `README.md` and registered summary. Recomputed from the per-member `A_verdict` records, not from prose.

- **20 of 30 members return `READS`, 1 `AMBIGUOUS`, 9 `UNDEFINED` and 0 `AT_CHANCE`.** Reading is *measurable* -- the AUROC and its bootstrap interval both exist -- on 21 members, which is the READS members plus `Llama_3p2_3B_Instruct` (AUROC 0.685 [0.597, 0.763], 282 refusals / 282 compliances, powered y). 14 members are detection-powered under the 40-per-class rule.

- **The minimum axis-A AUROC depends on the population and the population is now named.** Over all members with a defined AUROC (n = 21) it is 0.685 on `Llama_3p2_3B_Instruct` (verdict AMBIGUOUS, 282 refusals / 282 compliances, powered y). Over the READS members (n = 20) it is 0.691 on `Llama_3p2_1B_Instruct`. Over the detection-powered members with a defined AUROC (n = 14) it is 0.685 on `Llama_3p2_3B_Instruct`. The bare form 'AUROC >= 0.68' belongs to none of the three and is retired.

## Why the previous block said something else

The stale tally was **18 READS / 0 AT_CHANCE / 10 UNDEFINED**, and it is reconstructible exactly. The GPU stage logs one verdict line per member, so the panel state at each point in the run is recoverable:

| log | members | powered | verdicts |
|---|---|---|---|
| `backfill.log` | 30 | 11 | 2 AMBIGUOUS, 18 READS, 10 UNDEFINED |
| `gpu_full.log` | 30 | 11 | 3 AMBIGUOUS, 17 READS, 10 UNDEFINED |
| `rerun_base.log` | 5 | 4 | 5 READS |
| `run.log` | 30 | 14 | 1 AMBIGUOUS, 20 READS, 9 UNDEFINED |
| `smoke_t4.log` | 1 | 1 | 1 READS |
| `smoke_t4b.log` | 1 | 1 | 1 READS |

`backfill.log` -- the state at the end of the main pass -- holds 18 READS, 2 AMBIGUOUS and 10 UNDEFINED over 30 members. The stale block quotes its READS and UNDEFINED counts and simply omits the AMBIGUOUS class, which is why 18 + 0 + 10 sums to 28 rather than 30. `rerun_base.log` then re-ran five base checkpoints under the plain wrapper (the Qwen3-Base chat-template fix), which moved `Qwen2p5_0p5B` from AMBIGUOUS to READS and `Qwen3_0p6B_Base` from UNDEFINED to READS, giving the canonical 20/1/9.

**Diagnosis, with the code path located.** A grep for a writer of each surface over every `*.py` in that artifact finds 11 references to `RESULTS.md`, including the one that actually emits it -- `report.py:428` -- and `0` for `README.md` and `0` for the registered summary. So `RESULTS.md` (line 5) is a pure function of `method_out.json` and is canonical; `README.md` (line 16) and the registered summary are hand-written prose that predates the base-model rerun. There is no second live aggregation to retire -- there is one generated tally and one stale hand-typed one, which is why the recomputed-from-per-member-records tally is shipped as canonical without ambiguity.

## A separate defect this uncovered, for H-K

The Method describes the `UNDEFINED` verdict as firing when fewer than 40 spontaneous refusals exist. The shipped code does not do that: `explib.verdict_from_ci` returns `UNDEFINED` when the bootstrap interval is non-finite, which happens at <= 1 refusal, while `gpu_stage.py:343` uses the 40-per-class rule for the *separate* `powered` flag. That is why members with 6, 7, 12, 28, 32 and 33 refusals carry a READS verdict while being unpowered. Every sentence repeating the '< 40' description is flagged STALE_SOURCE in the ledger and pointed here; the AT_CHANCE-attainability simulation belongs to a different direction and is not attempted here.
