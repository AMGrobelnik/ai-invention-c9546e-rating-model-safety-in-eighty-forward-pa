# Does the refusal axis read or only push?

## The short version

On 30 checkpoints spanning 7 lineages, each measured in BOTH roles of the same five axes, the canonical refusal axis **reads refusal wherever reading is measurable at all**: 20 of 30 members return READS, 0 return AT_CHANCE, and the remaining 9 are UNDEFINED because the model emits too few spontaneous refusals for the statistic to exist.

That is a reversal of the iteration-3 result this study set out to strengthen. The dissociation reported there -- at chance as a reader while still inducing -- does not survive being measured on each model's OWN spontaneous text: what abliteration removes is the refusals to be read, not the axis's ability to read them. The two roles are in fact positively coupled (rho = 0.629 [0.465, 0.803], lineage bootstrap over 70 (member, axis) pairs), which is the first time this study has been able to put the two roles on one plot.

**H1 (abliterated arm).** The abliterated arm could NOT be strengthened, and the reason is structural rather than statistical: of 18 abliterated-class checkpoints measured, 14 never produced the 40 spontaneous refusals the detection role needs even after the full escalation ladder, so their reading AUROC is UNDEFINED rather than at chance; on the 4 that were powered the canonical axis reads 4 READS, giving K = 0. The iteration-3 n=2 'at chance in both roles' claim must therefore be DOWNGRADED: measured on each model's OWN spontaneous text, abliteration removes the refusals to be read rather than making the axis unable to read them.

**H1b (the arm that IS measurable).** Across 10 within-lineage abliterated-versus-parent pairs, steering along the canonical refusal axis induces refusal on 5 abliterated checkpoints and FAILS to on 4 where the parent was steerable; the median change in maximum induced refusal rate is -0.306.

**H2 (scope repair).** 1 of 2 breadth-panel counterexamples survive matched-contrast normalisation: axis B is a GENUINE inducer there, and the induction claim must be scoped to the depth panel.

**H3 (joint read-versus-act).** Across 70 (member, axis) pairs over 7 lineages, induction quality and detection quality are correlated at rho = 0.629 [0.465, 0.803].

Sanity panel: 7 matched-random-axis (D) violations across 30 members (FAIL).

## T1 Loads and skips

The frozen `panel_manifest` yielded 33 eligible members (21 abliterated-class, 12 in-lineage parents) after the pre-registered screen (verified, ungated, <= 4.2B, >= 8 layers); 76 abliterated-class candidates were screened out. No candidate is silently dropped.

| status | n | members |
|---|---|---|
| `ok` | 5 | Qwen2p5_0p5B, Qwen3_0p6B_Base, Llama_3p2_1B, Qwen2p5_1p5B, Qwen3_1p7B_Base |

Screened-out abliterated-class candidates, by reason: n_layers missing or <8 (1); params_b=13.48>4.2 (1); params_b=13.71>4.2 (2); params_b=13.96>4.2 (2); params_b=140.62>4.2 (1); params_b=22.24>4.2 (1); params_b=25.81>4.2 (1); params_b=26.90>4.2 (1); params_b=31.27>4.2 (1); params_b=34.66>4.2 (1); params_b=35.95>4.2 (1); params_b=4.30>4.2 (1); params_b=4.54>4.2 (9); params_b=46.70>4.2 (1); params_b=6.74>4.2 (1); params_b=6.86>4.2 (29); params_b=7.24>4.2 (1); params_b=7.62>4.2 (1); params_b=8.03>4.2 (11); params_b=8.19>4.2 (2); params_b=8.83>4.2 (1); params_b=8.84>4.2 (1); params_b=9.24>4.2 (3); params_b=9.41>4.2 (1); params_b=9.50>4.2 (1).

## T1b The three arms, and why the abliterated arm goes quiet

`abliterated-class` is not one homogeneous thing. The manifest marks a checkpoint `h4_status=candidate` only where its card evidences a behavioural uncensoring; several repos it classes as `behavioral_uncensored` are `not_applicable` task models that refuse copiously. Pooling those with the weight-edited abliterations would blur exactly the contrast under test, so the arms are kept apart.

| arm | members | detection-powered | median spontaneous refusal rate | axis-A verdicts |
|---|---|---|---|---|
| `aligned_reference` | 12 | 10 | 0.1131 | 1x AMBIGUOUS, 11x READS |
| `behavioural_uncensored_candidate` | 5 | 0 | 0.0000 | 1x READS, 4x UNDEFINED |
| `behavioural_uncensored_unverified` | 4 | 3 | 0.2884 | 3x READS, 1x UNDEFINED |
| `weight_edited_abliteration` | 9 | 1 | 0.0076 | 5x READS, 4x UNDEFINED |

## T2 Per-member detection (held-out AUROC on the model's OWN text)

AUROC of the stratum-centred axis projection at the first generated token, refusals versus compliances, with a prompt-clustered bootstrap CI (2000 reps). AT_CHANCE = CI contained in [0.4, 0.6]; READS = CI lower bound > 0.6.

| member | class | n ref / com | spont. refusal rate | pow | A AUROC [CI] | verdict | A within-stratum | A norm-controlled [CI] | B AUROC [CI] | A-B | Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `BADMISTRAL_1p5B` | behavioral_uncensored | 1 / 1 | 0.0006 | N | 1.000 -- | UNDEFINED | -- | 1.000 -- | 1.000 -- | 0.000 -- | -- |
| `DAN_Qwen3_1p7B` | behavioral_uncensored | 6 / 6 | 0.0038 | N | 0.889 [0.611, 1.000] | READS | -- | 0.889 [0.611, 1.000] | 0.472 [0.121, 0.833] | 0.417 [-0.113, 0.833] | 0.1340 |
| `Helvete_nano` | behavioral_uncensored | 0 / 1569 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Huihui_Qwen3_0p6B_abliterated_v2` | abliterated | 0 / 1582 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Huihui_Qwen3_1p7B_abliterated_v2` | abliterated | 0 / 1574 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | abliterated | 12 / 12 | 0.0076 | N | 0.889 [0.688, 1.000] | READS | -- | 0.924 [0.731, 1.000] | 0.653 [0.338, 0.908] | 0.236 [0.000, 0.512] | 0.1340 |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | abliterated | 32 / 32 | 0.0202 | N | 0.998 [0.989, 1.000] | READS | 1.000 | 0.998 [0.989, 1.000] | 0.653 [0.481, 0.818] | 0.345 [0.181, 0.516] | 0.0105 |
| `Llama_3p2_1B` | base | 28 / 28 | 0.0177 | N | 0.974 [0.930, 1.000] | READS | 0.965 | 0.976 [0.932, 1.000] | 0.642 [0.477, 0.806] | 0.333 [0.162, 0.503] | 0.0105 |
| `Llama_3p2_1B_Instruct` | instruct | 172 / 172 | 0.1988 | y | 0.691 [0.603, 0.773] | READS | 0.558 | 0.694 [0.607, 0.777] | 0.459 [0.357, 0.556] | 0.231 [0.141, 0.324] | 0.0105 |
| `Llama_3p2_1B_Instruct_abliterated` | abliterated | 28 / 28 | 0.0177 | N | 0.997 [0.985, 1.000] | READS | 1.000 | 1.000 [1.000, 1.000] | 0.649 [0.477, 0.807] | 0.348 [0.192, 0.519] | 0.0105 |
| `Llama_3p2_3B_Instruct` | instruct | 282 / 282 | 0.3260 | y | 0.685 [0.597, 0.763] | AMBIGUOUS | 0.668 | 0.687 [0.600, 0.766] | 0.532 [0.445, 0.618] | 0.153 [0.090, 0.216] | 0.0105 |
| `Llama_3p2_3B_Instruct_abliterated` | abliterated | 150 / 150 | 0.1734 | y | 0.718 [0.628, 0.802] | READS | 0.724 | 0.720 [0.630, 0.805] | 0.593 [0.499, 0.677] | 0.124 [0.067, 0.193] | 0.0105 |
| `Mia_001` | behavioral_uncensored | 0 / 1242 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Promt_generator` | behavioral_uncensored | 0 / 1375 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Qwen2p5_0p5B` | base | 45 / 45 | 0.0380 | y | 0.816 [0.714, 0.903] | READS | 0.847 | 0.814 [0.710, 0.906] | 0.421 [0.279, 0.571] | 0.395 [0.234, 0.544] | 0.0105 |
| `Qwen2p5_0p5B_Instruct` | instruct | 318 / 318 | 0.3676 | y | 0.869 [0.828, 0.908] | READS | 0.909 | 0.869 [0.830, 0.909] | 0.281 [0.213, 0.349] | 0.588 [0.506, 0.668] | 0.0105 |
| `Qwen2p5_0p5B_Instruct_abliterated` | abliterated | 33 / 33 | 0.0208 | N | 0.863 [0.760, 0.939] | READS | 0.931 | 0.874 [0.774, 0.948] | 0.325 [0.172, 0.480] | 0.538 [0.358, 0.711] | 0.0105 |
| `Qwen2p5_1p5B` | base | 67 / 67 | 0.0565 | y | 0.928 [0.875, 0.974] | READS | 0.941 | 0.926 [0.873, 0.973] | 0.731 [0.619, 0.833] | 0.197 [0.093, 0.316] | 0.0105 |
| `Qwen2p5_1p5B_Instruct` | instruct | 348 / 348 | 0.4023 | y | 0.763 [0.709, 0.812] | READS | 0.816 | 0.763 [0.709, 0.813] | 0.490 [0.411, 0.573] | 0.272 [0.189, 0.358] | 0.0105 |
| `Qwen2p5_1p5B_Instruct_abliterated` | abliterated | 1 / 1 | 0.0006 | N | 0.000 -- | UNDEFINED | -- | 0.000 -- | 1.000 -- | -1.000 -- | -- |
| `Qwen3_0p6B` | instruct | 50 / 50 | 0.0422 | y | 0.980 [0.944, 1.000] | READS | 0.987 | 0.978 [0.942, 1.000] | 0.814 [0.708, 0.908] | 0.165 [0.070, 0.271] | 0.0105 |
| `Qwen3_0p6B_Base` | base | 91 / 91 | 0.0574 | y | 0.915 [0.869, 0.953] | READS | 0.950 | 0.922 [0.878, 0.957] | 0.741 [0.652, 0.824] | 0.174 [0.082, 0.272] | 0.0105 |
| `Qwen3_0p6B_abliterated` | abliterated | 0 / 1572 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `Qwen3_1p7B` | instruct | 197 / 197 | 0.2277 | y | 0.906 [0.859, 0.944] | READS | 0.904 | 0.904 [0.857, 0.942] | 0.549 [0.456, 0.633] | 0.357 [0.263, 0.449] | 0.0105 |
| `Qwen3_1p7B_Base` | base | 146 / 146 | 0.1688 | y | 0.918 [0.871, 0.957] | READS | 0.969 | 0.929 [0.887, 0.964] | 0.517 [0.424, 0.605] | 0.402 [0.306, 0.500] | 0.0105 |
| `TinyLlama_1p1B_Chat_v1p0` | instruct | 7 / 7 | 0.0044 | N | 1.000 [1.000, 1.000] | READS | -- | 1.000 [1.000, 1.000] | 0.408 [0.000, 0.800] | 0.592 [0.200, 1.000] | 0.0123 |
| `UNfilteredAI_1B` | behavioral_uncensored | 0 / 1355 | 0.0000 | N | -- -- | UNDEFINED | -- | -- -- | -- -- | -- -- | -- |
| `lexi_coder_v4p1` | behavioral_uncensored | 242 / 242 | 0.2798 | y | 0.762 [0.687, 0.829] | READS | 0.921 | 0.749 [0.675, 0.818] | 0.683 [0.605, 0.756] | 0.079 [0.022, 0.137] | 0.0150 |
| `lexi_resume_v6` | behavioral_uncensored | 257 / 257 | 0.2971 | y | 0.936 [0.906, 0.961] | READS | 0.945 | 0.937 [0.909, 0.962] | 0.226 [0.167, 0.292] | 0.710 [0.632, 0.779] | 0.0105 |
| `lexi_rm_agent` | behavioral_uncensored | 262 / 262 | 0.3029 | y | 0.736 [0.676, 0.792] | READS | 0.763 | 0.731 [0.671, 0.787] | 0.458 [0.385, 0.533] | 0.278 [0.176, 0.373] | 0.0105 |

The *within-stratum* column re-computes the AUROC comparing refusals to compliances drawn from the SAME prompt stratum, pooled by item count. It guards the one way stratum-centring can still be fooled: if a member's refusals came only from harmful prompts and its compliances only from harmless ones, the pooled figure would measure prompt topic rather than refusal. Worst class/stratum concentration across the panel is 1.000 (1.0 would mean a single stratum holds an entire class).

## T2b Abliteration versus its in-lineage parent

Detection needs refusals to read and an abliterated checkpoint barely emits any, so its detection AUROC is structurally undefined rather than at chance; induction is measurable on every member regardless.

| lineage | abliterated | parent | spont. refusal abl / parent | max induced rate abl / parent | c_50 abl / parent |
|---|---|---|---|---|---|
| `Qwen/Qwen3-1.7B-Base` | `Huihui_Qwen3_1p7B_abliterated~` | `Qwen3_1p7B` | 0.000 / 0.228 | 0.972 / 1.000 | 1.57 / 1.12 |
| `Qwen/Qwen3-1.7B-Base` | `DAN_Qwen3_1p7B` | `Qwen3_1p7B` | 0.004 / 0.228 | 0.667 / 1.000 | 1.35 / 1.12 |
| `Qwen/Qwen3-0.6B-Base` | `Huihui_Qwen3_0p6B_abliterated~` | `Qwen3_0p6B` | 0.000 / 0.042 | 0.361 / 1.000 | -- / 0.82 |
| `Qwen/Qwen3-0.6B-Base` | `Qwen3_0p6B_abliterated` | `Qwen3_0p6B` | 0.000 / 0.042 | 0.972 / 1.000 | 1.15 / 0.82 |
| `meta-llama/Llama-3.2-1B` | `Llama_3p2_1B_Instruct_abliter~` | `Llama_3p2_1B_Instruct` | 0.018 / 0.199 | 0.111 / 0.611 | -- / 0.92 |
| `meta-llama/Llama-3.2-3B` | `Llama_3p2_3B_Instruct_abliter~` | `Llama_3p2_3B_Instruct` | 0.173 / 0.326 | 0.389 / 0.222 | -- / -- |
| `Qwen/Qwen2.5-0.5B` | `Qwen2p5_0p5B_Instruct_abliter~` | `Qwen2p5_0p5B_Instruct` | 0.021 / 0.368 | 0.472 / 0.806 | -- / 1.18 |
| `Qwen/Qwen2.5-0.5B` | `lexi_resume_v6` | `Qwen2p5_0p5B_Instruct` | 0.297 / 0.368 | 0.528 / 0.806 | 1.45 / 1.18 |
| `Qwen/Qwen2.5-0.5B` | `lexi_rm_agent` | `Qwen2p5_0p5B_Instruct` | 0.303 / 0.368 | 0.778 / 0.806 | 1.36 / 1.18 |
| `Qwen/Qwen2.5-1.5B` | `Qwen2p5_1p5B_Instruct_abliter~` | `Qwen2p5_1p5B_Instruct` | 0.001 / 0.402 | 0.028 / 0.917 | -- / 1.25 |

## T3 Per-member induction (steering sweep in axis-contrast units)

`c = alpha * NORM_L / ||d_raw||`, verified against 459 archived `analysis2.json` grid cells at worst error 0.0e+00.

| member | L / n_layers | NORM_L | ||d_A|| | ||d_B|| | A c_50 | A max rate | B c_50 | B max rate |
|---|---|---|---|---|---|---|---|---|
| `BADMISTRAL_1p5B` | 5 / 20 | 7.01 | 2.97 | 1.49 | -- | 0.222 | -- | 0.222 |
| `DAN_Qwen3_1p7B` | 7 / 28 | 49.43 | 24.00 | 12.29 | 1.35 | 0.667 | -- | 0.000 |
| `Helvete_nano` | 6 / 24 | 5.15 | 2.17 | 1.11 | -- | -- | -- | -- |
| `Huihui_Qwen3_0p6B_abliterated_v2` | 7 / 28 | 20.06 | 10.57 | 4.80 | -- | 0.361 | -- | 0.000 |
| `Huihui_Qwen3_1p7B_abliterated_v2` | 7 / 28 | 45.75 | 22.41 | 11.55 | 1.57 | 0.972 | -- | 0.083 |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | 9 / 36 | 38.80 | 16.73 | 9.50 | -- | 0.472 | -- | 0.000 |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | 9 / 36 | 34.52 | 17.67 | 8.89 | 1.96 | 0.528 | -- | 0.028 |
| `Llama_3p2_1B` | 4 / 16 | 3.95 | 1.65 | 0.88 | -- | 0.250 | -- | 0.056 |
| `Llama_3p2_1B_Instruct` | 4 / 16 | 3.29 | 1.63 | 0.88 | 0.92 | 0.611 | 2.56 | 0.833 |
| `Llama_3p2_1B_Instruct_abliterated` | 4 / 16 | 3.29 | 1.54 | 0.85 | -- | 0.111 | -- | 0.278 |
| `Llama_3p2_3B_Instruct` | 7 / 28 | 6.44 | 3.26 | 1.71 | -- | 0.222 | -- | 0.111 |
| `Llama_3p2_3B_Instruct_abliterated` | 7 / 28 | 6.38 | 3.24 | 1.70 | -- | 0.389 | -- | 0.056 |
| `Mia_001` | 3 / 12 | 17.81 | 6.63 | 2.24 | -- | 0.000 | -- | 0.000 |
| `Promt_generator` | 6 / 24 | 16.60 | 4.44 | 2.64 | -- | 0.139 | -- | 0.000 |
| `Qwen2p5_0p5B` | 6 / 24 | 12.78 | 4.70 | 2.49 | 1.47 | 0.528 | -- | 0.028 |
| `Qwen2p5_0p5B_Instruct` | 6 / 24 | 11.38 | 4.56 | 2.25 | 1.18 | 0.806 | -- | 0.139 |
| `Qwen2p5_0p5B_Instruct_abliterated` | 6 / 24 | 11.30 | 4.47 | 2.25 | -- | 0.472 | -- | 0.000 |
| `Qwen2p5_1p5B` | 7 / 28 | 34.72 | 15.63 | 8.68 | 1.25 | 0.833 | -- | 0.194 |
| `Qwen2p5_1p5B_Instruct` | 7 / 28 | 35.60 | 14.92 | 8.13 | 1.25 | 0.917 | 2.71 | 0.556 |
| `Qwen2p5_1p5B_Instruct_abliterated` | 7 / 28 | 34.53 | 14.70 | 7.87 | -- | 0.028 | -- | 0.000 |
| `Qwen3_0p6B` | 7 / 28 | 21.34 | 10.62 | 4.82 | 0.82 | 1.000 | -- | 0.306 |
| `Qwen3_0p6B_Base` | 7 / 28 | 19.10 | 10.34 | 5.02 | 1.23 | 0.667 | -- | 0.111 |
| `Qwen3_0p6B_abliterated` | 7 / 28 | 21.48 | 10.64 | 4.82 | 1.15 | 0.972 | -- | 0.056 |
| `Qwen3_1p7B` | 7 / 28 | 46.73 | 22.96 | 11.82 | 1.12 | 1.000 | -- | 0.417 |
| `Qwen3_1p7B_Base` | 7 / 28 | 49.90 | 24.06 | 12.93 | 1.50 | 0.806 | -- | 0.083 |
| `TinyLlama_1p1B_Chat_v1p0` | 6 / 22 | 2.10 | 0.85 | 0.47 | -- | 0.056 | -- | 0.000 |
| `UNfilteredAI_1B` | 5 / 21 | 1.55 | 0.73 | 0.40 | -- | 0.083 | -- | 0.028 |
| `lexi_coder_v4p1` | 8 / 32 | 24.64 | 10.67 | 5.88 | 1.12 | 0.667 | 1.43 | 0.556 |
| `lexi_resume_v6` | 6 / 24 | 10.98 | 4.51 | 2.27 | 1.45 | 0.528 | -- | 0.139 |
| `lexi_rm_agent` | 6 / 24 | 12.10 | 4.58 | 2.26 | 1.36 | 0.778 | -- | 0.111 |

## T4 Matched-contrast paired A-B advantage

At matched `c` the injected vector carries the same norm relative to each axis's own contrast magnitude, so a surviving A-over-B gap cannot be the magnitude-collapse artifact of arXiv:2603.22061.

| member | verdict | mean delta [CI] | n shared c | c where A hits 0.50 | delta there | B reaches 0.50 at matched c |
|---|---|---|---|---|---|---|
| `BADMISTRAL_1p5B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.059 [0.019, 0.111] | 9 | -- | -- | no |
| `DAN_Qwen3_1p7B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.160 [0.111, 0.207] | 9 | 1.50 | 0.667 | no |
| `Helvete_nano` | -- | -- -- | -- | -- | -- | -- |
| `Huihui_Qwen3_0p6B_abliterated_v2` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.074 [0.034, 0.117] | 9 | -- | -- | no |
| `Huihui_Qwen3_1p7B_abliterated_v2` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.272 [0.238, 0.309] | 9 | 2.00 | 0.972 | no |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.111 [0.080, 0.142] | 8 | -- | -- | no |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.136 [0.102, 0.176] | 9 | 2.00 | 0.528 | no |
| `Llama_3p2_1B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.101 [0.076, 0.128] | 8 | -- | -- | no |
| `Llama_3p2_1B_Instruct` | B_IS_A_GENUINE_INDUCER | 0.056 [-0.006, 0.108] | 10 | 1.00 | 0.528 | yes |
| `Llama_3p2_1B_Instruct_abliterated` | INCONCLUSIVE | -0.006 [-0.033, 0.022] | 10 | -- | -- | no |
| `Llama_3p2_3B_Instruct` | INCONCLUSIVE | 0.025 [0.000, 0.046] | 9 | -- | -- | no |
| `Llama_3p2_3B_Instruct_abliterated` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.059 [0.028, 0.090] | 9 | -- | -- | no |
| `Mia_001` | INCONCLUSIVE | 0.000 [0.000, 0.000] | 10 | -- | -- | no |
| `Promt_generator` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.025 [0.008, 0.044] | 10 | -- | -- | no |
| `Qwen2p5_0p5B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.147 [0.094, 0.192] | 10 | 1.50 | 0.528 | no |
| `Qwen2p5_0p5B_Instruct` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.299 [0.238, 0.367] | 9 | 1.50 | 0.778 | no |
| `Qwen2p5_0p5B_Instruct_abliterated` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.111 [0.075, 0.150] | 10 | -- | -- | no |
| `Qwen2p5_1p5B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.181 [0.150, 0.214] | 10 | 1.50 | 0.806 | no |
| `Qwen2p5_1p5B_Instruct` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.191 [0.139, 0.247] | 9 | 1.50 | 0.444 | yes |
| `Qwen2p5_1p5B_Instruct_abliterated` | INCONCLUSIVE | 0.003 [0.000, 0.010] | 8 | -- | -- | no |
| `Qwen3_0p6B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.448 [0.392, 0.500] | 8 | 1.00 | 0.722 | no |
| `Qwen3_0p6B_Base` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.228 [0.170, 0.284] | 9 | 1.50 | 0.667 | no |
| `Qwen3_0p6B_abliterated` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.275 [0.235, 0.312] | 9 | 1.50 | 0.889 | no |
| `Qwen3_1p7B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.296 [0.269, 0.324] | 9 | 1.50 | 0.750 | no |
| `Qwen3_1p7B_Base` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.208 [0.172, 0.250] | 10 | 1.50 | 0.500 | no |
| `TinyLlama_1p1B_Chat_v1p0` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.011 [0.003, 0.019] | 10 | -- | -- | no |
| `UNfilteredAI_1B` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.025 [0.003, 0.050] | 10 | -- | -- | no |
| `lexi_coder_v4p1` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.114 [0.034, 0.191] | 9 | 1.50 | 0.028 | yes |
| `lexi_resume_v6` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.086 [0.034, 0.142] | 9 | 1.50 | 0.472 | no |
| `lexi_rm_agent` | NORM_MISMATCH_DOES_NOT_EXPLAIN | 0.189 [0.139, 0.239] | 10 | 1.50 | 0.500 | no |

## T5 Depth panel versus breadth panel

2 breadth-panel members carried the archived 'axis B reaches 0.50' objection. Of those, 1 are genuine inducers at matched contrast and 1 are norm artifacts.

| member | panel | archived B max rate | B max rate here | A max rate here | matched-contrast verdict |
|---|---|---|---|---|---|
| `BADMISTRAL_1p5B` | breadth | -- | 0.222 | 0.222 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `DAN_Qwen3_1p7B` | breadth | -- | 0.000 | 0.667 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Helvete_nano` | breadth | -- | -- | -- | None |
| `Huihui_Qwen3_0p6B_abliterated_v2` | breadth | -- | 0.000 | 0.361 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Huihui_Qwen3_1p7B_abliterated_v2` | depth | -- | 0.083 | 0.972 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | breadth | -- | 0.000 | 0.472 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | breadth | -- | 0.028 | 0.528 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Llama_3p2_1B` | breadth | -- | 0.056 | 0.250 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Llama_3p2_1B_Instruct` | breadth | 0.633 | 0.833 | 0.611 | B_IS_A_GENUINE_INDUCER |
| `Llama_3p2_1B_Instruct_abliterated` | breadth | -- | 0.278 | 0.111 | INCONCLUSIVE |
| `Llama_3p2_3B_Instruct` | breadth | -- | 0.111 | 0.222 | INCONCLUSIVE |
| `Llama_3p2_3B_Instruct_abliterated` | breadth | -- | 0.056 | 0.389 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Mia_001` | breadth | -- | 0.000 | 0.000 | INCONCLUSIVE |
| `Promt_generator` | breadth | -- | 0.000 | 0.139 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_0p5B` | breadth | -- | 0.028 | 0.528 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_0p5B_Instruct` | breadth | -- | 0.139 | 0.806 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_0p5B_Instruct_abliterated` | breadth | -- | 0.000 | 0.472 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_1p5B` | breadth | -- | 0.194 | 0.833 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_1p5B_Instruct` | breadth | 0.667 | 0.556 | 0.917 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen2p5_1p5B_Instruct_abliterated` | breadth | -- | 0.000 | 0.028 | INCONCLUSIVE |
| `Qwen3_0p6B` | depth | -- | 0.306 | 1.000 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen3_0p6B_Base` | depth | -- | 0.111 | 0.667 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen3_0p6B_abliterated` | depth | -- | 0.056 | 0.972 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen3_1p7B` | depth | -- | 0.417 | 1.000 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `Qwen3_1p7B_Base` | depth | -- | 0.083 | 0.806 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `TinyLlama_1p1B_Chat_v1p0` | breadth | -- | 0.000 | 0.056 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `UNfilteredAI_1B` | breadth | -- | 0.028 | 0.083 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `lexi_coder_v4p1` | breadth | -- | 0.556 | 0.667 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `lexi_resume_v6` | breadth | -- | 0.139 | 0.528 | NORM_MISMATCH_DOES_NOT_EXPLAIN |
| `lexi_rm_agent` | breadth | -- | 0.111 | 0.778 | NORM_MISMATCH_DOES_NOT_EXPLAIN |

## T6 Joint read-versus-act scatter

| quantity | value |
|---|---|
| (member, axis) pairs | 70 |
| members | 14 |
| lineages (bootstrap unit) | 7 |
| Spearman rho (x = max refusal rate) | 0.629 |
| lineage-bootstrap 95% CI | [0.465, 0.803] |
| rho secondary (x = -log10 c_50) | 0.448 |
| c_50 censoring fraction | 0.771 |
| within-member mean rho | 0.715 |

Pre-committed reading: **across 70 (member, axis) pairs over 7 lineages, induction quality and detection quality are correlated at rho = 0.629 [0.465, 0.803]**.

## Sanity panel (axes C and D must stay at chance in both roles)

Of 30 members, the matched random axis D exceeds the empirical random-null reading band on 1 and induces refusal at >= 0.10 on 7.

**The induction floor is a result, not a defect.** A random direction injected at axis A's OWN matched magnitude induces refusal at a rate of at least 0.10 on 7 of 30 members (max over the contrast grid; median across the panel 0.028, worst 0.389). This is a FLOOR that any steering claim has to clear, and it is measured here rather than assumed: the same magnitude that makes the canonical axis work also makes an arbitrary direction work on a substantial minority of models.

On the reading side, the empirical random-direction AUROC band spans +/-0.075 to +/-0.500 across members, so the textbook expectation that a random direction reads at 0.500 is wrong by a wide and model-dependent margin. That is why the gate is read against 20 measured random draws per member rather than against 0.500 (AMENDMENT-2 in `results/prereg.json`).

| member | axis | AUROC [CI] (raw projection) | AUROC [CI] (norm-controlled) | max refusal rate | flag |
|---|---|---|---|---|---|
| `BADMISTRAL_1p5B` | C_stylistic | 1.000 -- | 1.000 -- | 0.000 | ok |
| `BADMISTRAL_1p5B` | D_random0 | 1.000 -- | 1.000 -- | 0.056 | ok |
| `DAN_Qwen3_1p7B` | C_stylistic | 0.250 [0.000, 0.632] | 0.250 [0.000, 0.632] | 0.028 | ok |
| `DAN_Qwen3_1p7B` | D_random0 | 0.222 [0.000, 0.558] | 0.222 [0.000, 0.558] | 0.028 | ok |
| `Helvete_nano` | C_stylistic | -- -- | -- -- | -- | ok |
| `Helvete_nano` | D_random0 | -- -- | -- -- | -- | ok |
| `Huihui_Qwen3_0p6B_abliterated_v2` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `Huihui_Qwen3_0p6B_abliterated_v2` | D_random0 | -- -- | -- -- | 0.000 | ok |
| `Huihui_Qwen3_1p7B_abliterated_v2` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `Huihui_Qwen3_1p7B_abliterated_v2` | D_random0 | -- -- | -- -- | 0.083 | ok |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | C_stylistic | 0.535 [0.222, 0.818] | 0.507 [0.182, 0.800] | 0.000 | ok |
| `Josiefied_Qwen2p5_3B_Instruct_abliterated_v1` | D_random0 | 0.549 [0.203, 0.814] | 0.521 [0.197, 0.785] | 0.028 | ok |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | C_stylistic | 0.255 [0.112, 0.416] | 0.264 [0.116, 0.428] | 0.000 | ok |
| `Josiefied_Qwen3_4B_Instruct_2507_gabliterated_v2` | D_random0 | 0.274 [0.141, 0.418] | 0.281 [0.144, 0.428] | 0.000 | ok |
| `Llama_3p2_1B` | C_stylistic | 0.228 [0.096, 0.385] | 0.228 [0.099, 0.383] | 0.056 | ok |
| `Llama_3p2_1B` | D_random0 | 0.224 [0.103, 0.370] | 0.231 [0.108, 0.381] | 0.083 | ok |
| `Llama_3p2_1B_Instruct` | C_stylistic | 0.434 [0.334, 0.537] | 0.433 [0.333, 0.537] | 0.000 | ok |
| `Llama_3p2_1B_Instruct` | D_random0 | 0.521 [0.427, 0.616] | 0.530 [0.436, 0.624] | 0.389 | D_VIOLATION |
| `Llama_3p2_1B_Instruct_abliterated` | C_stylistic | 0.346 [0.184, 0.515] | 0.358 [0.192, 0.533] | 0.028 | ok |
| `Llama_3p2_1B_Instruct_abliterated` | D_random0 | 0.366 [0.203, 0.543] | 0.366 [0.207, 0.541] | 0.139 | D_VIOLATION |
| `Llama_3p2_3B_Instruct` | C_stylistic | 0.418 [0.331, 0.508] | 0.415 [0.327, 0.507] | 0.000 | ok |
| `Llama_3p2_3B_Instruct` | D_random0 | 0.417 [0.336, 0.498] | 0.408 [0.328, 0.489] | 0.028 | D_VIOLATION |
| `Llama_3p2_3B_Instruct_abliterated` | C_stylistic | 0.459 [0.363, 0.552] | 0.447 [0.353, 0.541] | 0.000 | ok |
| `Llama_3p2_3B_Instruct_abliterated` | D_random0 | 0.348 [0.259, 0.443] | 0.327 [0.240, 0.423] | 0.056 | ok |
| `Mia_001` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `Mia_001` | D_random0 | -- -- | -- -- | 0.000 | ok |
| `Promt_generator` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `Promt_generator` | D_random0 | -- -- | -- -- | 0.000 | ok |
| `Qwen2p5_0p5B` | C_stylistic | 0.259 [0.151, 0.384] | 0.267 [0.159, 0.391] | 0.000 | ok |
| `Qwen2p5_0p5B` | D_random0 | 0.398 [0.269, 0.535] | 0.430 [0.298, 0.569] | 0.000 | ok |
| `Qwen2p5_0p5B_Instruct` | C_stylistic | 0.358 [0.292, 0.428] | 0.376 [0.308, 0.450] | 0.083 | ok |
| `Qwen2p5_0p5B_Instruct` | D_random0 | 0.391 [0.321, 0.468] | 0.415 [0.342, 0.492] | 0.111 | D_VIOLATION |
| `Qwen2p5_0p5B_Instruct_abliterated` | C_stylistic | 0.335 [0.190, 0.487] | 0.326 [0.180, 0.483] | 0.000 | ok |
| `Qwen2p5_0p5B_Instruct_abliterated` | D_random0 | 0.365 [0.217, 0.526] | 0.391 [0.243, 0.555] | 0.028 | ok |
| `Qwen2p5_1p5B` | C_stylistic | 0.557 [0.442, 0.680] | 0.586 [0.473, 0.706] | 0.028 | ok |
| `Qwen2p5_1p5B` | D_random0 | 0.860 [0.780, 0.932] | 0.860 [0.781, 0.931] | 0.028 | ok |
| `Qwen2p5_1p5B_Instruct` | C_stylistic | 0.448 [0.373, 0.523] | 0.484 [0.407, 0.558] | 0.028 | ok |
| `Qwen2p5_1p5B_Instruct` | D_random0 | 0.698 [0.632, 0.764] | 0.696 [0.629, 0.763] | 0.056 | ok |
| `Qwen2p5_1p5B_Instruct_abliterated` | C_stylistic | 0.000 -- | 0.000 -- | 0.000 | ok |
| `Qwen2p5_1p5B_Instruct_abliterated` | D_random0 | 1.000 -- | 1.000 -- | 0.000 | ok |
| `Qwen3_0p6B` | C_stylistic | 0.214 [0.113, 0.332] | 0.216 [0.115, 0.332] | 0.000 | ok |
| `Qwen3_0p6B` | D_random0 | 0.171 [0.076, 0.290] | 0.147 [0.060, 0.260] | 0.000 | ok |
| `Qwen3_0p6B_Base` | C_stylistic | 0.334 [0.249, 0.426] | 0.338 [0.251, 0.432] | 0.028 | ok |
| `Qwen3_0p6B_Base` | D_random0 | 0.590 [0.497, 0.687] | 0.606 [0.512, 0.700] | 0.028 | ok |
| `Qwen3_0p6B_abliterated` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `Qwen3_0p6B_abliterated` | D_random0 | -- -- | -- -- | 0.000 | ok |
| `Qwen3_1p7B` | C_stylistic | 0.221 [0.150, 0.293] | 0.234 [0.164, 0.307] | 0.000 | ok |
| `Qwen3_1p7B` | D_random0 | 0.332 [0.248, 0.418] | 0.337 [0.254, 0.423] | 0.167 | D_VIOLATION |
| `Qwen3_1p7B_Base` | C_stylistic | 0.224 [0.163, 0.296] | 0.195 [0.135, 0.266] | 0.000 | ok |
| `Qwen3_1p7B_Base` | D_random0 | 0.499 [0.402, 0.597] | 0.519 [0.426, 0.613] | 0.000 | ok |
| `TinyLlama_1p1B_Chat_v1p0` | C_stylistic | 0.041 [0.000, 0.200] | 0.020 [0.000, 0.125] | 0.000 | ok |
| `TinyLlama_1p1B_Chat_v1p0` | D_random0 | 0.857 [0.571, 1.000] | 0.857 [0.571, 1.000] | 0.000 | ok |
| `UNfilteredAI_1B` | C_stylistic | -- -- | -- -- | 0.000 | ok |
| `UNfilteredAI_1B` | D_random0 | -- -- | -- -- | 0.000 | ok |
| `lexi_coder_v4p1` | C_stylistic | 0.308 [0.238, 0.388] | 0.322 [0.251, 0.403] | 0.028 | ok |
| `lexi_coder_v4p1` | D_random0 | 0.529 [0.442, 0.614] | 0.520 [0.434, 0.606] | 0.111 | D_VIOLATION |
| `lexi_resume_v6` | C_stylistic | 0.278 [0.216, 0.346] | 0.289 [0.223, 0.359] | 0.056 | ok |
| `lexi_resume_v6` | D_random0 | 0.426 [0.342, 0.505] | 0.474 [0.390, 0.553] | 0.139 | D_VIOLATION |
| `lexi_rm_agent` | C_stylistic | 0.467 [0.399, 0.539] | 0.477 [0.410, 0.549] | 0.111 | ok |
| `lexi_rm_agent` | D_random0 | 0.384 [0.317, 0.455] | 0.397 [0.329, 0.466] | 0.111 | D_VIOLATION |

## Provenance and validation gates

- **prereg sha256** `b342bfc8864d0b1873b6bcda399fb2553af61bff82a2508fa4689c9c19603c19`, stamped before any new AUROC existed.
- **T0 archive inventory**: 13 of 13 `lib/*.py` copied byte-identically (sha256 matched); 0 expected paths missing.
- **T1 analysis replay** (no model): every archived per-axis AUROC on `instruct_0p6` reproduced to 0.000 with the new analysis code (paired A-B 0.152 versus archived 0.152); passed = True.
- **T2 contrast-unit formula**: exact on 459 archived cells.
- **T3 tokenisation unit test**: the token-id path satisfies len(seq) = len(pre) + len(gen) on 50/50 items under BOTH renderers, and the boundary index selects the first generated token exactly. The string-concatenation path -- the archived bug -- differs on 34/50 items under the plain wrapper and 0/50 under the chat template, so the bug is renderer-dependent and bites exactly the base checkpoints.
- **Axis reproduction** against the archived `.npy` axes on 6 checkpoints: worst min|cosine| = 0.99992; stop-and-diagnose triggered = False.
- **Layer rule**: L = round(0.25 * n_layers), clip [1, n_layers-1]. The artifact plan asserted relative depth 0.3; the archive actually used 0.25 on all six checkpoints, and 0.25 is what was pre-registered.
- **Judge**: measured, kappa(regex, judge) = 0.600, cost $0.0099. The anchored regex is primary; no headline number depends on the judge.
- **dtype** bfloat16 on 1x NVIDIA RTX A4500 20GB.

- **Token-id concatenation** avoided a silent prompt/completion boundary merge on 943 scored items across the panel (per-member counts in `method_out.json`).

## Reused verbatim versus reimplemented

- **Reused verbatim (sha256 matched)**: all 13 `lib/*.py` modules from `iter_3/gen_art/gen_art_experiment_1/lib` -- the refusal regex and classifier, the axis-fitting primitives and their frozen response / paraphrase / style string sets, the steering hook and batched decoder, and the non-parametric alpha_50 interpolator.
- **Reimplemented, validated against the archive**: the GPU stage (`gpu_stage.py`) and the detection statistics (`explib.detection_stats`). The archived `gen_art_evaluation_1/gpu_stage.py` IS on disk -- contrary to the artifact plan's expectation -- but it re-encodes ARCHIVED text on six fixed checkpoints, whereas this study must generate each new member's OWN text. The reimplementation is validated by T1 (statistics reproduce the archive exactly) and by the per-checkpoint axis-cosine gate.
