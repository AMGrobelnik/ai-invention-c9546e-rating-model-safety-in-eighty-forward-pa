# Tier-0 three-axis safety ground truth + task-vector ladder pilot

Measures refusal behaviour on a Qwen3-0.6B-centred member set, validates the
measurement itself against a pre-registered sanity gate, and pilots two
training-free continuous "safety dials".

**The headline is a measurement failure, and it is the most useful thing here.**
The pre-registered LLM judge never assigns COMPLIANCE to harmful content. It
scored **0/7** on the COMPLIANCE class of a balanced hand-labelled probe, and two
other safety-trained judges did the same. Consequence: the pre-registered sanity
gate **FAILS**; with a judge that actually reads the content, the same
generations **PASS** it. The harness was fine. The scorer was not.

---

## Headline results

| | frozen judge (pre-registered) | repaired judge (post-hoc) |
|---|---|---|
| sanity gate `instruct >> base ~ abliterated` | **FAIL** (Δ 0.263 / 0.225) | **PASS** (Δ 0.463 / 0.413) |
| Qwen3-0.6B abliterated, plain-harmful refusal | 0.700 | **0.113** |
| Qwen3-0.6B abliterated, jailbreak ASR | 0.092 | **0.858** |
| task-vector ladder verdict | **SNAPPED** | **SMOOTH** |
| accuracy vs blind adjudication (n=147) | 0.510 | 0.694 |

The scorer, not the models, decides both the gate verdict and the ladder verdict.

### The judge-selection probe (`results/judge_probe_results.json`)

21 items, 7 per class, truth assigned by unambiguous surface pattern.

| judge | evaluator framing | acc | COMPLIANCE recall | $/1k items |
|---|---|---|---|---|
| google/gemini-3.6-flash | yes | 21/21 | 7/7 | 1.236 |
| anthropic/claude-haiku-4.5 | yes | 18/21 | 4/7 | 0.294 |
| **meta-llama/llama-3.3-70b-instruct** | yes | 18/21 | 6/7 | **0.040** |
| openai/gpt-5.4-nano | yes | 13/21 | 3/7 | 0.055 |
| anthropic/claude-haiku-4.5 | no | 12/21 | **0/7** | 0.270 |
| **openai/gpt-5.4-nano (PRE-REGISTERED)** | no | 9/21 | **0/7** | 0.046 |
| anthropic/claude-3-haiku | no | 7/21 | **0/7** | 0.055 |
| deepseek-v4-flash / ling-3.0-flash | yes | 0/21 | — | reasoning models, 0% parse |

Every un-framed safety-trained judge scores 0/7 on COMPLIANCE. Adding an
evaluator system prompt is what recovers it — not model capability, and not price.

### Blind adjudication (147 items, labels withheld by construction)

| scorer | exact acc | κ (refusal) | REFUSAL | COMPLIANCE | PARTIAL | DEGENERATE |
|---|---|---|---|---|---|---|
| baseline refusal-string screen | 0.844 (binary) | 0.315 | — | — | — | — |
| frozen judge | 0.510 | 0.242 | 0.50 | 0.43 | 0.59 | 0.57 |
| repaired judge | 0.694 | 0.412 | 0.79 | 0.84 | 0.41 | 0.60 |
| gold reference (gemini, n=29) | 0.759 | 0.449 | 0.80 | 1.00 | 0.29 | 0.93 |

**On the 80 items where the two judges disagree, the adjudicator sides with the
repaired judge 48×, the frozen judge 21×, neither 11×.**

The baseline screen's 0.844 binary accuracy is a trap: most items are not
refusals, so accuracy is inflated. Its κ of 0.315 and its recall of 0.223
against the repaired judge are the honest numbers — small models refuse by
lecturing ("Stealing sensitive information is illegal…"), which no prefix list
catches.

### Ladders

Task-vector `W(t) = W_base + t(W_instruct − W_base)`, repaired scorer:

| t | 0.0 | 0.25 | 0.50 | 0.75 | 1.0 |
|---|---|---|---|---|---|
| refusal | 0.062 | 0.237 | 0.388 | 0.500 | 0.525 |
| ppl | 17.0 | 17.9 | 19.8 | 23.0 | 29.1 |
| fluency screen | **FAIL** | pass | pass | pass | pass |

Monotone with two interior points strictly inside the band → **SMOOTH**. Caveat:
t=0 fails the pre-registered fluency screen (distinct-3 = 0.113), so the low-t
end is partly recovery-from-degeneracy.

In-house abliteration `W ← W − c·rrᵀW` is **SNAPPED under both scorers**:
plain-harmful refusal stays flat (0.525 → 0.512 as c goes 0 → 1) while XSTest
over-refusal rises 0.16 → 0.42. It changed the model without producing the
intended knob — a negative result for this implementation.

### Other findings

- **Incapacity floor.** pythia-410m has no safety training yet scores 0.550
  "refusal" with a 0.327 degenerate rate. Any rate near that floor carries no
  safety information. Four members are auto-flagged UNRELIABLE.
- **Template confound.** Qwen3-0.6B-Base scores 0.662 under the chat template
  and 0.900 under a generic wrapper (Δ 0.238 > the 0.15 pre-registered
  threshold) — flagged, not resolved by picking the nicer number.
- **Family-specific ordering.** SmolLM2-360M-Instruct refuses *less* than its
  own base (Δ −0.325, CIs disjoint). The sanity ordering is not universal.
- **fp16 is not batch-invariant.** Batched greedy decoding gave 3/4 identical
  completions at batch=4 vs batch=1 in fp16 and 4/4 in fp32, so the whole run
  uses fp32.

### Cost — $1.251 total, within the pre-registered $1.50 budget

| arm | calls | USD |
|---|---|---|
| frozen judge (full) | 3362 | 0.168 |
| repaired judge (full) | 3365 | 0.157 |
| gold reference (subsample) | 442 | 0.877 |
| second cheap judge (subsample) | 760 | 0.049 |

Generation: 0.109 s/item median, ~551 generated tok/s. A 50-member panel
projects to **0.41 GPU-hours and $0.64** of judging on the cheap arm. The fitted
parameter-scaling slope came out **negative** and is explicitly marked unusable —
with `max_new_tokens=64` wall-clock is dominated by early EOS, not FLOPs.
Audit cost is deliberately **not** measured here.

---

## Design

- **Members (16).** Qwen3-0.6B {base, instruct, mlabonne-abliterated}; cross-family
  pairs Llama-3.2-1B and SmolLM2-360M {base, instruct}; pythia-410m low-refusal
  anchor; a template side-check member; 3 task-vector interpolants; 4
  abliteration-strength members. `huihui-ai/Qwen3-0.6B-abliterated` is gated and
  is reported unavailable rather than silently swapped.
- **Blocks (275/member).** 80 AdvBench plain-harmful (deduped by first-six-words),
  40 of those × 3 fixed attacks (assistant prefill, refusal-suppression,
  roleplay), 50 XSTest safe + 25 unsafe contrast. WikiText-2 windows and 30
  neutral prompts drive the fluency screen.
- **Three scorers, one pipeline, identical generations** — so no comparison is
  confounded by implementation differences.
- **Decoding.** Greedy, fp32, `max_new_tokens=64`, left padding, `enable_thinking=False`
  with an automated `<think>` guard. Batch-invariance is asserted in code.

## Files

| | |
|---|---|
| `method.py` | orchestrator (stages: smoke, mini, judgedry, ladderdry, full, retime, adjudicate, finalize) |
| `harness.py` | hardware, blocks, generation, screen, async judge, statistics |
| `prereg_spec.py` → `prereg.json` | frozen pre-registration, written before any generation and never edited |
| `prereg_amendment.json` | the post-hoc repair arm, with the evidence that forced it |
| `judge_probe.py` | reproducible 9-configuration judge-selection probe |
| `method_out.json` | schema-validated output (`exp_gen_sol_out`) |
| `results/analysis.json` | full analysis (rates, gate, reliability, ladders, cost, limitations) |
| `generations.jsonl` / `scored.jsonl` | every generation verbatim, and every label |
| `adjudication_items.md` / `_labels.json` | the blind dump and the adjudicator's labels |
| `results/ladder_models_manifest.json` | sha256 + build recipe for the 7 deleted ladder checkpoints |
| `refusal_direction.pt` | 5 KB unit refusal direction (layer 17) — needed to rebuild the `abl_c*` members |

Reproduce: `python method.py --stage full` then `--stage adjudicate`, label, then
`--stage finalize`. Judge calls are content-hash cached, so re-runs are free.

### The ladder checkpoints are not shipped

The 7 ladder members (`tv_t*`, `abl_c*`) are 1.14 GB each, 7.9 GB total — derived
intermediates, far above the 100 MB per-file publication limit. They are **deleted
from the workspace and regenerated on demand**:

```
python method.py --stage rebuild-ladder --verify-hashes
```

Construction is pure float32 tensor arithmetic with no RNG and no data dependence,
so it is bit-exact. This was verified rather than assumed: the directory was
deleted and rebuilt from `Qwen/Qwen3-0.6B{,-Base}` plus `refusal_direction.pt`, and
**all 7 checkpoints reproduced their original sha256** (~6 s each after the first),
with the rebuilt midpoint loading and generating normally. Splitting or gzipping
was rejected — it would put ~7 GB of derived weights in the repo and add a
decompression step to every load, to preserve something a 6-second command
recreates exactly.

No result depends on their presence: every generation they produced is already in
`generations.jsonl` / `scored.jsonl`, and `--stage finalize` reads only those
(confirmed by re-running it after deletion — byte-identical gate verdicts).

## Reading these numbers

The frozen-judge arm is reported in full because it was pre-registered, **not**
because it is trustworthy — it is not. The repaired arm is post-hoc and was
selected on a probe drawn from the same generations it scores, so its 18/21 is
optimistic; the blind adjudication and the gemini reference are its only
out-of-probe estimates. The adjudicator is an LLM agent, not a human, so every
"accuracy" here bounds scorer *disagreement*, not truth. PARTIAL is the weakest
class for every scorer (≤0.41 recall) — safe-completion behaviour is the least
reliable axis in this artifact. Full list in `results/analysis.json:limitations`.
