# SPI — Safety Proximity Indicators (TIER-0 feasibility)

**Does refusal wobble predict model safety?**

A model-independent refusal observable `r_t` is tracked at every generated step
during ordinary sampled generation on **harmless prompts only**. Four
early-warning indicators are computed from it — recovery rate `lambda` from a
norm-epsilon residual-stream nudge, detrended across-rollout variance `Var*`,
detrended lag-1 autocorrelation `AC1`, and flicker rate — plus the asymmetry
index `log(lambda_refuse / lambda_comply)`.

The make-or-break question is **estimator identifiability**: is `lambda`
recoverable at all from a real 0.6B model's generated-step series at achievable
length and noise level? Every validity arm is a first-class deliverable and is
reported whatever it shows.

> **Headline — the answer is no, twice over.** `lambda` is not identifiable at
> any geometry this artifact reached: the pre-registered rule demands
> `T_fit >= 128`, and after refitting there the requirement moves to
> `n_roll >= 40`, still above the achieved 20. More decisively, where `lambda`
> *does* produce significant separations, a **random perturbation direction
> reproduces them** — and on the one comparison that isolates safety tuning
> (instruct vs abliterated) the random control separates while the refusal
> direction does not. The three perturbation-free indicators are statistically
> indistinguishable within the Qwen3-0.6B triad and instead separate lineages.
> Verdicts: `LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY` (pre-registered) and
> `CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING` (supplementary, at the refit
> geometry). **This is a disconfirmation of the H2 ordering hypothesis at 0.6B
> scale, and it is reported as one.**

## Panel

| role | repo | why |
|---|---|---|
| base | `Qwen/Qwen3-0.6B-Base` | pre-safety-tuning |
| instruct | `Qwen/Qwen3-0.6B` | safety-tuned (reference model) |
| abliterated | `huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2` | refusal removed post-hoc |
| anchor | `HuggingFaceTB/SmolLM2-360M` | different lineage, low-refusal end |

The primary abliterated repo (`huihui-ai/Qwen3-0.6B-abliterated`) is **gated**;
the maintainer's v2 was used, exactly as the fallback plan specified. Exact
revision SHAs are recorded in `metadata.model_revisions`.

## Method vs baseline

- **Our method (SPI)** — label-free. Zero harmful prompts, zero labels. Built
  only from the dynamics of `r_t` on 20 harmless instructions.
- **Baseline** — the field's standard strong approach: a supervised
  difference-in-means refusal direction fitted on a 32/32 harmful-vs-benign
  contrast set at the same layer, scored by AUROC. It is deliberately *given*
  the harmful data SPI is denied.
- **Baseline 2** — `r_0` harmful-minus-benign margin (also needs harmful data).
- **Ground truth** — string-matched plain-harmful refusal rate and XSTest
  over-refusal rate on the same four models, with Wilson CIs. The matcher is a
  screen, not a judge. Total LLM API spend: **$0.00**.

## Results

Full grid: 4 models x 20 harmless prompts x 20 paired rollouts x 192 generated
steps, ~590-710 tok/s, 94 min wall clock, peak VRAM under 3 GB, **$0 API spend**.

**Ground truth (string-matcher screen, Wilson CIs).** The panel spans the safety
axis: instruct refuses 22.5% of plain-harmful prompts, base 2.5%, abliterated
0.0%, SmolLM2 0.0%. Panel-validity check passes (instruct − abliterated = 0.225).

**The pre-registered ordering does not hold.** Instruct should have shown higher
`Var*`, `AC1` and flicker and slower relaxation than base and abliterated. It did
not — on several indicators the order reverses:

| model | Var\* | AC1 | flicker /100 | decay ratio @16 |
|---|---|---|---|---|
| qwen3 base | 3.152 | 0.245 | 42.2 | 0.156 |
| qwen3 instruct | 3.101 | 0.285 | 40.4 | **0.119** (fastest) |
| qwen3 abliterated | 3.121 | 0.304 | 40.2 | 0.188 |
| SmolLM2 base | **2.747** | **0.182** | 42.6 | 0.233 |

Within the Qwen3-0.6B triad — the controlled comparison, identical architecture,
differing only in safety tuning — the indicators are statistically
indistinguishable. The one clear separation in the table is SmolLM2 against the
whole triad. **The wobble indicators track lineage, not safety training.** All
three controls came back clean (random readout axis, POS probe, random
perturbation direction all fail to reproduce any ordering), so this is a genuine
null rather than a control artifact.

**Pre-registered verdict: `LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY`** at the
geometry the main run used. The synthetic study certifies the estimator only at
`T_fit >= 128` and `n_roll >= 20`; the main run fit over 64 steps at an observed
SNR of 1.19, so every lambda is flagged `identifiable=false`. Because the
rollouts are 192 steps and injection is at step 16, that gap looked closable
without new data, so `refit_certified.py` refits the headline arms at
`T_fit = 128` with layer, direction, epsilon, prompts and seeds held identical
(39 min, +80 cells). Two things came out of it, and both matter more than the
lambda values themselves.

*First, the identifiability target moves.* Refit at the longer window, the rule
re-derived at that arm's own measured noise now demands `n_roll >= 40`, which the
achieved 20 still does not meet. Lambda is therefore **not identifiable at any
geometry this artifact reached** — not merely at the first one tried. The
concrete requirement for iterations 2-5 is `n_roll >= 40`, roughly double this
run's cost at the measured throughput.

*Second, and decisively: the random-direction control reproduces the ordering.*

| comparison (instruct − X), λ at `T_fit=128` | refusal direction | **random direction** |
|---|---|---|
| vs abliterated *(isolates safety tuning)* | −0.226, CI includes 0 | **−0.493, CI excludes 0** |
| vs qwen3 base | −0.547, CI excludes 0 | +0.006, n.s. |
| vs SmolLM2 base | −0.560, CI excludes 0 | −1.058, CI excludes 0 |
| significant in predicted direction | 2 of 3 | 2 of 3 |

A random unit vector, injected at the same layer with the same magnitude,
separates the panel exactly as well as the refusal direction does — and on the
one pair that isolates safety tuning (instruct vs abliterated: same architecture,
same base model, differing only in whether refusal was removed) the **control
separates while the treatment does not**. The supplementary verdict is therefore
**`CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING`**: what lambda measures is a
generic relaxation property of each model's residual stream, not anything about
refusal. This is a DISCONFIRM and is recorded as one.

**Two diagnostics that qualify the lambda arm.**
`fit_quality` reports median fit `r2` of 0.11-0.54 with 30-90% of fits below 0.3
and per-prompt lambda IQR ratios of 4.7-20. A passing identifiability rule plus a
low `r2` means the estimator is fine and the *model shape* is wrong: the recovery
curve is not a single exponential, so lambda is a poorly determined summary of it.
The robust, assumption-free statistics — `decay_ratio_16` and the pre-registered
AUC/half-life substitute — are the trustworthy ones.
The layer-`L` logit lens correlates with the final-layer readout at only
0.17-0.26, below the pre-registered 0.3 threshold, so **every** indicator and
lambda is reported at both readouts and neither is silently preferred.

**Method vs baseline.** Ranking the four models against measured harmful-refusal
rate: the label-free SPI gets Spearman rho = **−0.20** (wrong direction), the
supervised difference-in-means refusal direction gets **+0.40**, and the `r_0`
margin baseline **+0.40**. Both baselines are given the 32 harmful prompts SPI is
denied, and both beat it. At n = 4 none of these is a statistical result — three
of the four models sit at a refusal-rate floor of 0.000–0.025 — and all three are
reported as directional smoke signals only. The comparison is nonetheless
one-directional in its implication: nothing here supports preferring the
label-free measurement over the supervised one.

**The epsilon-linearity control fails, but for the wrong reason.** The
pre-registered test treats every (prompt, epsilon) cell as an independent point,
so large prompt-to-prompt scatter is charged against linearity and the control
boolean comes back `False` for all four models. Averaging over the five sweep
prompts at each epsilon first — prompt is a nuisance factor, the response curve
is a property of epsilon — gives r2 = 0.996 for base and 0.976 for instruct, with
log-log slopes of 0.90 and 0.84 (1.0 would be exactly linear). The response is in
fact close to linear for three of four models and saturating for the abliterated
one (slope 0.61). Both analyses ship; the pre-registered one still drives the
control boolean, and `epsilon_linearity_prompt_averaged` explains it.

## Four findings the test harness forced

These were not designed in; they came out of the mandatory pre-flight tests and
each changed the measurement.

1. **Injecting at a layer's output is a no-op for that layer's own readout.**
   T2 measured `|delta_{p+1}| == 0` at *every* epsilon. A decoder layer writes
   its K/V inside attention, before a forward hook can fire, so a perturbation
   added to the layer *output* never reaches the layer-`L` read at later
   positions. The injection was moved to the layer **input** (a forward
   pre-hook), after which `delta` scales with epsilon as it should.

2. **Free-running `delta` cannot estimate a decay rate.** With common random
   numbers the arms stay paired only until the sampled token streams diverge —
   a median of ~7 steps after injection in the full run. After that `|delta_t|`
   **grows**, because it is comparing two different continuations rather than
   measuring relaxation. Confirmed at full scale: median `decay_ratio_16` is
   **2.57–5.33 free-running** (rises) against **0.119–0.233 teacher-forced**
   (falls), a separation of well over an order of magnitude on every model. The
   pre-registered teacher-forced fallback is therefore the **primary** channel.
   Both are reported, because the gap between them separates latent relaxation
   from content-mediated relaxation — and the free-running result is a finding in
   its own right: through the token channel the trajectory has no restoring
   force at all.

3. **`mean |delta|` is a biased estimator of the decay rate, and rollouts do not
   fix it.** Because `E|N(mu, sigma)| > |mu|`, averaging absolute deviations
   converges to `E|X|`, not `|E X|`, so the tail flattens onto a `~0.8*sigma`
   floor whose curvature biases `lambda` upward. Measured in the synthetic
   study: **+38% to +68% relative bias at every `n_roll`**. Fitting the
   **signed** across-rollout mean instead is unbiased (−0.03 to +0.02) and its
   noise falls as `sigma/sqrt(n_roll)`, which is what makes `lambda`
   identifiable at all. Both statistics are reported side by side.

## Layout

```
spi/models.py       load, layer indexing, chat templating, dtype, revisions
spi/prompts.py      B1-B4 prompt sets, all with in-repo literal fallbacks
spi/observable.py   r_t (logit lens) + random-axis and POS-probe controls
spi/rollout.py      paired-seed batched decode loop with residual injection
spi/indicators.py   detrending, Var*, AC1, flicker, three lambda estimators
spi/validity.py     synthetic recovery study + estimator unit tests
spi/groundtruth.py  $0 string-matcher refusal rates, panel-validity check
run_tier0.py        orchestrates Stages A-J
build_output.py     reshapes results into the exp_gen_sol_out schema
make_figs.py        regenerates all 8 figures from method_out.json alone
t0/t2/t2b_*.py      pre-flight gates (load, determinism/pairing, SNR probe)
```

## Reproduce

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch --index-url https://download.pytorch.org/whl/cu124 --index-strategy unsafe-best-match
uv pip install --python=.venv/bin/python transformers accelerate datasets numpy scipy scikit-learn pandas matplotlib loguru huggingface_hub nltk jsonschema

.venv/bin/python t0_load_test.py       # models load, no unclosed <think>
.venv/bin/python t2_pairing_test.py    # determinism, eps=0 no-op, divergence
.venv/bin/python t2b_snr_probe.py      # free-running vs teacher-forced SNR
.venv/bin/python run_tier0.py --mode full --out method_out.json
.venv/bin/python build_output.py       # -> schema-valid method_out.json
.venv/bin/python make_figs.py          # -> figs/*.png from the JSON alone
```

`--mode smoke` and `--mode pilot` run the same code on smaller grids.

## Outputs

- `method_out.json` — schema-valid (`exp_gen_sol_out`), four datasets
- `out/tier0_raw.json` — the full un-reshaped result tree
- `out/layer_choice.json` — written and asserted **before** any indicator
- `out/cells/` — per-model checkpoints, so a timeout still yields a partial run
- `out/refit_certified.json` — lambda at the certified geometry (`T_fit=128`)
- `figs/` — nine figures, all regenerable from the shipped result tree alone

## Honesty notes

Reported in the JSON, not just here: tokens/sec and the exact grid actually run;
every statistic both detrended and raw; per-rollout distributions for every
steering quantity; both readouts (layer-`L` lens and final layer); both pairing
regimes; both `lambda` statistics; explicit boolean verdicts for all five
controls; and a `verdict` field taking one of the five pre-registered codes.

`r_t` on the base and abliterated members is near-flat on the harmful/benign
contrast (`margin` ≈ 0.03–0.15 vs 0.71 on the instruct member). That is the
observable working as designed, not a safety finding, and it is flagged per
model in `metadata.observable_degenerate_by_model`.

The headline is a **null with a positive control failure**, and it is reported as
one. SPI does not order this panel by safety: the fluctuation indicators are
statistically indistinguishable within the Qwen triad and separate lineages
instead, and the one arm that *does* produce significant separations — lambda —
is matched by a random-direction control that separates just as well. So the
lambda separations cannot be attributed to the refusal direction. What the artifact
does establish positively is the measurement apparatus: a working paired-seed
injection harness, a quantified free-running-vs-teacher-forced contamination
effect, a bias-corrected estimator with a certified minimum geometry, and
throughput numbers (~590–710 tok/s, <3 GB VRAM, 94 min for the full grid) that
size iterations 2–5.

The provisional SPI is **not frozen** and its rank agreement with ground truth at
n=4 is not a statistical result. No claim here licenses using SPI to certify a
model as safe.
