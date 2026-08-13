# Does refusal stick? A steering-hysteresis test on the Qwen3-0.6B lineage

Pre-registered test of whether a language model's refusal mode, once entered, is held
by a **retained latent state** or only by the **refusal text it already emitted**.

Three members of one lineage are compared under an identical pipeline:

| member | model id |
|---|---|
| base | `Qwen/Qwen3-0.6B-Base` |
| instruct (safety-finetuned) | `Qwen/Qwen3-0.6B` |
| abliterated (uncensored community edit) | `mlabonne/Qwen3-0.6B-abliterated` |

Zero LLM API spend: every classification is deterministic string/token matching.

## The measurement

A refusal-direction steering coefficient `alpha` (in units of the median residual-stream
norm at the steering layer) is applied to one decoder block's output at every position
present in the forward pass. During incremental decoding only the newest position is in
the forward, so **each token's KV entries stay frozen carrying whatever alpha was active
when it was written**. That frozen, alpha-weighted cache is the candidate latent state.

Five arms per (model, prompt, seed):

| arm | what it does |
|---|---|
| **UP-RAMP** (measurement) | ramp alpha token-by-token inside an already-compliant generation |
| **ENTRY** | enter the refusal mode at generation onset at constant alpha, continue 8 tokens past the onset |
| **DOWN-RETAINED** | ramp alpha down with the entry cache kept -> `alpha_down` |
| **DOWN-FORCED-A** (primary control) | byte-identical refusal prefix, prefilled **unsteered** -> `alpha_down_forced_A` |
| **DOWN-FORCED-B** (positive control) | same prefix, prefilled token-by-token replaying the alpha schedule -> must reproduce the retained arm |
| **RESET** | prefix discarded between probes; noise floor (must be exactly 0 at temperature 0) |

Decisive statistic (pre-registered):

```
excess_width = alpha_down_forced_A - alpha_down      (= -residual)
```

the part of the path dependence that the literally emitted refusal text cannot explain.
`H1` is confirmed only if its bootstrap 95% CI excludes 0, is positive, and its lower
bound clears the 95th percentile of the temperature-0.7 RESET noise floor. `H1b` requires
the paired instruct > base and instruct > abliterated orderings.

## Result: **REFUTED** (the pre-registered disconfirmation)

Steering site: layer 7, response-contrast axis, alpha in units of `NORM_L = 21.2`.
Grid step 0.05. 30 prompts x 3 seeds x 3 models. Cost: **$0.00**.

| quantity | instruct | base | abliterated |
|---|---|---|---|
| prompts used (of 30) | 30 | 5 | 30 |
| entry-fail rate | 0.00 | **0.93** | 0.00 |
| up-ramp fail rate | 0.92 | 1.00 | 0.97 |
| hysteresis width `alpha_entry - alpha_down` | **0.262 [0.185, 0.344]** | 0.53 [0.01, 1.46] | 0.086 [0.046, 0.134] |
| **excess width** (latent-state part) | **0.019 [-0.057, 0.099]** | -0.330 [-0.990, 0.000] | -0.031 [-0.070, 0.001] |
| RESET noise floor, 95th pct | 0.05 | 0.00 | 0.05 |
| FORCED-B control, mean abs diff | **0.000** | **0.000** | **0.000** |
| temperature-0 RESET gate | pass | pass | pass |

1. **Path dependence is real.** The hysteresis width is positive with a CI excluding 0 —
   exactly what the pre-registration predicted for a generic autoregressive-conditioning
   mechanism, recorded in advance so it could not later be sold as a discovery.
2. **It is not carried by a retained latent state.** Replacing the steered refusal prefix
   with a byte-identical **unsteered** prefill leaves the escape threshold unchanged:
   `excess_width` includes 0 and its lower bound sits below the noise floor in every
   member. `H1` is refuted; `H1b` is `NOT_CONFIRMED`.
3. **The null is not a plumbing artifact.** The alpha-schedule-replay positive control
   (FORCED-B) reproduces the retained arm *exactly* — mean and max |difference| = 0.000 on
   every prompt of every model — and the temperature-0 RESET width is exactly 0 everywhere.
4. **Compliance sticks, refusal does not.** Ramping alpha inside an already-compliant
   generation fails on 92–100% of attempts, while a *fresh* generation at the same constant
   alpha refuses reliably. The up-transition is unreachable once a compliant prefix is in
   the KV cache.
5. **Prompt-classification quality is not steering quality.** The harmful-vs-benign *prompt*
   axis reaches held-out AUROC 1.0 at 14 of 28 layers yet induces a fluent refusal on only
   27% of probes; a *response*-contrast axis on the same model scores 0.69. A matched random
   direction induces refusal at **no** alpha.

**Candidate cheap safety metric** (5 prompts, 13 alphas, no benchmark): `alpha50`, the
steering coefficient at which a fresh generation starts refusing.

| member | alpha50 | max refusal rate | random-direction control |
|---|---|---|---|
| base | undefined (never reaches 50%) | 0.20 | 0.00 |
| instruct | 0.475 | 1.00 | 0.00 |
| abliterated | 0.550 | 1.00 | 0.00 |

Sensitivity: the narrow-floor run (`alpha_min = -0.5`, 43% censored) gave excess width
0.011 [-0.050, 0.073], and 0.012 [-0.009, 0.035] on its uncensored subset; re-scoring every
recorded token stream with COMPLIANCE_RUN in {6, 10, 14} keeps every CI overlapping 0
(`results/secondary_compliance_run*.json`).

## Files

| file | role |
|---|---|
| `method.py` | driver: pre-registration -> direction fitting -> gates -> arms -> statistics |
| `prompts.py` | frozen prompt sets (30 benign ramp prompts, 96+96 contrast prompts) |
| `direction.py` | diff-in-means axes over (layer x position) + CAA-style response axis; outcome-blind site selection |
| `models.py` | model loading, ChatML rendering, steering hook, KV-cache plumbing |
| `classify.py` | frozen refusal-onset / compliance-resumption criteria, `r_t` observable, fluency screen |
| `ramp.py` | the five arms |
| `stats.py` | bootstrap, paired tests, censoring sensitivity, Cohen's kappa |
| `smoke_env.py`, `debug_steer.py`, `debug_ramp.py` | the T1-T4 plumbing tests and the probes that drove amendments 2-4 |
| `prereg.json` | the pre-registration, including every amendment with its reason |
| `method_out.json` | the report (schema `exp_gen_sol_out`; the full analysis lives under `metadata`) |
| `gens/` | every generated token of every arm with its alpha and `r_t`, so every classification is auditable |
| `results/` | per-model checkpoints and the cached steering-site scan |
| `advbench_harmful_behaviors.csv` | AdvBench harmful behaviours (contrast set source) |

## Reproducing

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch --index-url https://download.pytorch.org/whl/cu124
uv pip install --python=.venv/bin/python "transformers>=4.51" accelerate numpy scipy loguru psutil huggingface_hub

.venv/bin/python method.py --tier 0a          # ~6 min smoke, one model, all arms
.venv/bin/python method.py --tier 1 --models instruct
.venv/bin/python method.py --tier 1 --models base
.venv/bin/python method.py --tier 1 --models abliterated
.venv/bin/python method.py --tier 1 --assemble --out method_out.json
```

Each model runs in its own process (one 0.6B model resident at a time) and checkpoints to
`results/model_<key>.json`; `--assemble` rebuilds the whole report from those checkpoints.

## Amendments

The pre-registration was amended seven times, always **before** the analysed data existed,
always with the reason recorded in `prereg.json`. The two that matter most:

* **AMENDMENT-4** — the pre-registered UP-RAMP never fires. On the reference model it fails
  10/10 at each of delta in {0.05, 0.1, 0.2, 0.4} with alpha_max up to 4.0, and 9/10 with a
  [L-2, L+2] layer-window escalation, while a *fresh* generation at the same constant alpha
  refuses reliably. The up-transition is not reachable once a compliant prefix is in the KV
  cache. That is itself a path-dependence result and is reported as one; the refusal state
  is instead entered at generation onset, leaving the decisive statistic and all controls
  untouched.
* **AMENDMENT-7** — the harmful-vs-benign *prompt* axis separates the prompt classes
  perfectly (held-out AUROC 1.0) but is a poor *inducer*: its best site produced a fluent
  refusal on 27% of probes, and those "refusals" were partly degenerate. A CAA-style
  *response* axis (refusal response vs compliant response on the same benign prompts) scores
  0.69 on the same outcome-blind scan and produces clean refusals, while a matched random
  direction produces none at any alpha.

## Scope

This is a statement about the **steered** dynamical system. Steered residual streams are not
prompt-reachable, so the result does not by itself license claims about unsteered sampling.
