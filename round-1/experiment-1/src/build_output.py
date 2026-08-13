#!/usr/bin/env python3
"""Reshape the Tier-0 results into the exp_gen_sol_out schema.

The scientific question is a PREDICTION question: can a label-free measurement
taken on harmless prompts alone order models by safety, as well as the standard
approach that needs harmful data?

  OUR METHOD  — SPI, built from wobble indicators measured during ordinary
                sampled generation on HARMLESS prompts only. No harmful prompt,
                no label, no benchmark is used to compute it.
  BASELINE    — the field's standard strong approach: a supervised
                difference-in-means refusal direction fitted on a 32/32
                harmful-vs-benign contrast set at the same layer, scored by its
                separability (AUROC). This is the method SPI has to beat, and it
                is deliberately given the harmful data SPI is denied.
  BASELINE-2  — r_0 margin: the refusal observable evaluated on the last prompt
                token, harmful minus benign. Also requires harmful prompts.

Ground truth is the string-matched plain-harmful refusal rate measured on the
same four models.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

ROOT = Path(__file__).parent
BASE_P_KEY = "base_p"


DISCOVERED_LIMITATIONS = [
    "The main run fits lambda over T_fit=64, but the artifact's own synthetic study "
    "certifies the estimator only at T_fit>=128 and n_roll>=20 at the observed SNR "
    "(~1.19). Every main-run lambda therefore carries identifiable=false. "
    "refit_certified.py closes this by refitting the headline arms at T_fit=128 with "
    "everything else held identical; see lambda_at_certified_geometry.",
    "The recovery curve is NOT well described by a single exponential: median fit r2 "
    "is 0.11-0.54 with 30-90% of fits below 0.3 and per-prompt lambda IQR ratios of "
    "4.7-20. A certified estimator plus a low r2 means the ESTIMATOR is sound and the "
    "MODEL SHAPE is wrong, so lambda is a poorly determined summary. The assumption-free "
    "decay_ratio and AUC/half-life statistics are the trustworthy ones. See fit_quality.",
    "The layer-L logit lens correlates with the final-layer readout at only 0.17-0.26, "
    "below the pre-registered 0.3 threshold, so the two channels are measuring "
    "substantially different things at this depth. Everything is reported at both "
    "readouts and neither is preferred; see readout_channel_check.",
    "The pre-registered epsilon-linearity control treats each (prompt, epsilon) cell as "
    "an independent point, so prompt-to-prompt scatter is charged against linearity and "
    "the boolean is False for all models. Averaging over prompts at each epsilon first "
    "gives r2 up to 0.996 with log-log slopes of 0.61-0.90. Both are reported; the "
    "per-cell version drives the control boolean.",
    "The safety signal being ordered against is weak in absolute terms: only the "
    "instruct member refuses at a non-trivial rate (0.225), and the other three are at "
    "0.000-0.025. With three of four models pinned near the floor, the ground truth "
    "supports an ordering claim only about instruct-vs-rest, not a graded ranking.",
    "flicker as 'fraction of rollouts that cross' saturates at 1.0 over a 192-step "
    "series for every model. The informative form is crossings-per-100-steps, which is "
    "what the SPI term and the ordering test use; the fraction is retained only for "
    "completeness.",
    "Var* detrended equals Var* raw by construction (subtracting a per-step constant "
    "cannot change a per-step across-rollout variance). The detrended-vs-raw comparison "
    "is therefore informative for AC1 and flicker but vacuous for Var*.",
    "The observed indicator differences are dominated by LINEAGE, not safety tuning: "
    "SmolLM2-360M separates from the whole Qwen3-0.6B triad on Var* and AC1, while the "
    "triad members — which differ only in safety tuning — overlap. Any future SPI must "
    "be normalised within lineage before it can be read as a safety signal.",
]


def rank(vals: dict[str, float], descending: bool = True) -> dict[str, int]:
    """1 = highest (descending) — ties broken by model name for determinism."""
    ok = {k: v for k, v in vals.items() if v is not None and np.isfinite(v)}
    order = sorted(ok, key=lambda k: (-ok[k] if descending else ok[k], k))
    return {k: i + 1 for i, k in enumerate(order)}


def spearman(a: list[float], b: list[float]) -> float | None:
    """Spearman rho, computed directly (n=4 — reported as a smoke signal only)."""
    pair = [(x, y) for x, y in zip(a, b)
            if x is not None and y is not None and np.isfinite(x) and np.isfinite(y)]
    if len(pair) < 3:
        return None
    x = np.array([p[0] for p in pair])
    y = np.array([p[1] for p in pair])
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    if rx.std() < 1e-12 or ry.std() < 1e-12:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def fnum(v: Any, nd: int = 4) -> str:
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "null"
    return f"{float(v):.{nd}f}"


def build(raw: dict[str, Any]) -> dict[str, Any]:
    agg = raw["aggregate_by_model"]
    gt = raw["ground_truth"]
    pmm = raw["per_model_meta"]
    models = sorted(agg)
    base_p = raw["grid_actually_run"][BASE_P_KEY]
    base_c = raw["grid_actually_run"]["base_eps_c"]

    # ---------------- model-level predictions ----------------
    truth = {m: gt[m]["harmful_refusal_rate"]["p"] for m in models if m in gt}
    over = {m: gt[m]["xstest_over_refusal_rate"]["p"] for m in models if m in gt}
    spi = raw["provisional_spi"]["spi_by_model"]
    base1 = {m: pmm[m]["diff_means"]["auroc"] for m in models}
    base2 = {m: pmm[m]["observable_sanity"]["margin"] for m in models}

    r_truth = rank(truth)
    r_spi = rank(spi)
    r_b1 = rank(base1)
    r_b2 = rank(base2)

    ordered = [m for m in models if m in truth]
    corr = {
        "spearman_spi_vs_harmful_refusal": spearman(
            [spi.get(m) for m in ordered], [truth[m] for m in ordered]),
        "spearman_baseline_diffmeans_auroc_vs_harmful_refusal": spearman(
            [base1.get(m) for m in ordered], [truth[m] for m in ordered]),
        "spearman_baseline_r0_margin_vs_harmful_refusal": spearman(
            [base2.get(m) for m in ordered], [truth[m] for m in ordered]),
        "n_models": len(ordered),
        "WARNING": (
            "n=4. A Spearman rho on four points is not a statistical result; it is "
            "reported as a directional smoke signal and nothing more."
        ),
    }

    model_examples = []
    for m in models:
        meta = raw["model_revisions"].get(m, {})
        a = agg[m]
        model_examples.append({
            "input": (
                f"model={meta.get('model_id', m)} | panel_role={a['member']} | "
                f"lineage={a['lineage']} | revision={meta.get('revision', '?')[:12]} | "
                f"layer_L={pmm[m]['L']} of {meta.get('n_layers')} | "
                f"Predict the plain-harmful refusal rate rank of this model."
            ),
            "output": (
                f"harmful_refusal_rate={fnum(truth.get(m), 3)} "
                f"(rank {r_truth.get(m, 'NA')} of {len(r_truth)}, 1=most refusing); "
                f"xstest_over_refusal_rate={fnum(over.get(m), 3)}"
            ),
            "predict_our_method_spi": (
                f"SPI={fnum(spi.get(m), 3)} (rank {r_spi.get(m, 'NA')}); "
                f"label_free=True; harmful_prompts_used=0"
            ),
            "predict_baseline_diffmeans_auroc": (
                f"AUROC={fnum(base1.get(m), 3)} (rank {r_b1.get(m, 'NA')}); "
                f"label_free=False; harmful_prompts_used=32"
            ),
            "predict_baseline_r0_margin": (
                f"margin={fnum(base2.get(m), 3)} (rank {r_b2.get(m, 'NA')}); "
                f"label_free=False; harmful_prompts_used=16"
            ),
            "metadata_member": a["member"],
            "metadata_lineage": a["lineage"],
            "metadata_indicators": {
                "lambda_toward_refuse": a["lambda_toward_refuse"],
                "lambda_toward_comply": a["lambda_toward_comply"],
                "lambda_random_direction": a["lambda_random_direction"],
                "asymmetry_index": a["asymmetry_index"],
                "var_star": a["var_star"],
                "ac1": a["ac1"],
                "flicker": a["flicker"],
            },
            "metadata_controls": {
                "random_axis_var_star": a["control_random_axis_var_star"],
                "pos_probe_var_star": a["control_pos_var_star"],
                "pos_probe_ac1": a["control_pos_ac1"],
            },
            "metadata_observable_degenerate": a["observable_degenerate"],
            "metadata_median_r_sd": a["median_r_sd"],
            "metadata_tokens_per_sec": raw["tokens_per_sec_by_model"].get(m),
        })

    # ---------------- prompt-level cells ----------------
    lam_by = {}
    for r in raw["lambda"]:
        if (r["teacher_forced"] and r["direction"] == "toward_refuse"
                and r["p"] == base_p and abs(r["eps_c"] - base_c) < 1e-9):
            lam_by[(r["model"], r["prompt_id"])] = r

    cell_examples = []
    for r in raw["indicators"]:
        m, pid = r["model"], r["prompt_id"]
        det = r["primary"]["detrended"]
        rawi = r["primary"]["raw"]
        lam = lam_by.get((m, pid))
        pos = r.get("control_pos_probe")
        cell_examples.append({
            "input": (
                f"model={m} | prompt_id={pid} | register={r['register']} | "
                f"harmless prompt, {r['n_rollouts'] if 'n_rollouts' in r else ''}"
                f"{r['primary']['n_rollouts']} paired rollouts x "
                f"{r['primary']['n_steps']} generated steps"
            ),
            "output": (
                f"model_harmful_refusal_rate={fnum(truth.get(m), 3)}; "
                f"model_rank={r_truth.get(m, 'NA')}"
            ),
            "predict_our_method_indicators": (
                f"var_star={fnum(det['var_star'])}; ac1={fnum(det['ac1'])}; "
                f"flicker={fnum(det['flicker_frac_rollouts_crossing'])}; "
                f"lambda_refuse="
                f"{fnum((lam or {}).get('layerL', {}).get('estimates', {}).get('est1_nls', {}).get('lambda'))}; "
                f"decay_ratio_16="
                f"{fnum((lam or {}).get('layerL', {}).get('decay_ratio_16'))}; "
                f"fit_r2="
                f"{fnum((lam or {}).get('layerL', {}).get('estimates', {}).get('est1_nls', {}).get('r2'), 3)}"
            ),
            "predict_our_method_final_readout": (
                f"var_star={fnum(r['final_layer_readout']['detrended']['var_star'])}; "
                f"ac1={fnum(r['final_layer_readout']['detrended']['ac1'])}; "
                f"flicker_per100="
                f"{fnum(r['final_layer_readout']['detrended']['flicker_crossings_per_100'])}; "
                f"lambda_refuse="
                f"{fnum((lam or {}).get('final', {}).get('estimates', {}).get('est1_nls', {}).get('lambda'))}"
            ),
            "predict_control_random_axis": (
                "var_star=" + fnum(float(np.mean(
                    [c["detrended"]["var_star"] for c in r["control_random_axis"]]))
                    if r.get("control_random_axis") else None)
            ),
            "predict_control_pos_probe": (
                f"var_star={fnum(pos['detrended']['var_star'] if pos else None)}; "
                f"ac1={fnum(pos['detrended']['ac1'] if pos else None)}"
            ),
            "metadata_raw_indicators": {
                "var_star": rawi["var_star"], "ac1": rawi["ac1"],
                "sd_overall": rawi["sd_overall"],
            },
            "metadata_detrend_delta": r["primary"]["delta_detrend_minus_raw"],
            "metadata_noise_sd": r["noise_sd_detrended"],
            "metadata_lens_vs_final_corr": r["r_lens_vs_final_corr"],
            "metadata_frac_hit_eos": r["frac_rollouts_hit_eos"],
            "metadata_series_length_sweep": r["series_length_sweep"],
            "metadata_ac1_per_rollout": det["ac1_per_rollout"],
            "metadata_lambda_per_rollout": (
                (lam or {}).get("layerL", {}).get("per_rollout_lambda")),
            "metadata_sample_completion": r["sample_completion"],
        })

    # ---------------- synthetic identifiability ----------------
    syn_examples = []
    for c in raw["synthetic_ar1_table"]:
        syn_examples.append({
            "input": (
                f"true_lambda={c['true_lambda']} | T_fit={c['T_fit']} | "
                f"n_roll={c['n_roll']} | noise_sd={fnum(c.get('noise_sd'), 5)} | "
                f"amp={fnum(c.get('amp'), 5)} | {c['n_ok'] + c['n_fail']} replicates"
            ),
            "output": f"true_lambda={c['true_lambda']}",
            "predict_our_method_signed_estimator": (
                f"mean={fnum(c.get('mean_est'))}; rel_bias={fnum(c.get('rel_bias'), 3)}; "
                f"rel_sd={fnum(c.get('rel_sd'), 3)}; passes={c['passes']}"
            ),
            "predict_baseline_abs_estimator": (
                f"rel_bias={fnum(c.get('abs_statistic_rel_bias'), 3)}; "
                f"rel_sd={fnum(c.get('abs_statistic_rel_sd'), 3)}"
            ),
            "metadata_covers_truth": c.get("covers_truth"),
            "metadata_n_failed_fits": c.get("n_fail"),
            "metadata_n_at_bound": c.get("n_at_bound"),
            "metadata_auc_substitute": {"mean": c.get("auc_mean"), "sd": c.get("auc_sd")},
        })

    # ---------------- ground-truth completions ----------------
    gt_examples = []
    for m in models:
        row = gt.get(m)
        if not row:
            continue
        for split in ("harmful", "xstest_safe"):
            det = row["detail"][split]
            for ex in det["examples"]:
                gt_examples.append({
                    "input": f"model={m} | split={split} | prompt={ex['prompt']}",
                    "output": ("refusal" if split == "harmful" else "should_comply"),
                    "predict_baseline_string_matcher": (
                        f"refusal={ex['refusal']}"),
                    "metadata_completion": ex["completion"],
                    "metadata_split_rate": det["rate"],
                })

    # ---------------- lambda at the certified geometry ----------------
    # The main run fits lambda over T_fit=64; the synthetic study then certifies
    # only T_fit>=128 at the observed SNR. refit_certified.py closes that gap by
    # refitting the headline arms over 128 steps with everything else identical.
    cert_path = ROOT / "out" / "refit_certified.json"
    cert_examples: list[dict[str, Any]] = []
    cert_meta: dict[str, Any] | None = None
    if cert_path.exists():
        try:
            cert = json.loads(cert_path.read_text())
            if isinstance(cert, dict) and "aggregate_by_model" in cert:
                cert_meta = {k: v for k, v in cert.items()
                             if k not in ("rows", "synthetic_table")}
                cagg = cert["aggregate_by_model"]
                for m in sorted(cagg):
                    e = cagg[m]
                    cert_examples.append({
                        "input": (
                            f"model={m} | lambda re-fit at the CERTIFIED geometry "
                            f"T_fit={cert['fit_len']}, n_roll={cert['n_roll']}, "
                            f"teacher-forced, p={cert['p']}, eps_c={cert['eps_c']}"
                        ),
                        "output": (
                            f"harmful_refusal_rate={fnum(truth.get(m), 3)} "
                            f"(rank {r_truth.get(m, 'NA')} of {len(r_truth)})"
                        ),
                        "predict_our_method_lambda_certified": (
                            f"lambda_refuse={fnum(e['toward_refuse']['lambda']['point'])} "
                            f"[{fnum(e['toward_refuse']['lambda'].get('ci_lo'))},"
                            f"{fnum(e['toward_refuse']['lambda'].get('ci_hi'))}]; "
                            f"median_r2={fnum(e['toward_refuse'].get('median_r2'), 3)}; "
                            f"asymmetry_index={fnum(e['asymmetry_index']['point'])}"
                        ),
                        "predict_control_random_direction_certified": (
                            f"lambda={fnum(e['random_direction']['lambda']['point'])} "
                            f"[{fnum(e['random_direction']['lambda'].get('ci_lo'))},"
                            f"{fnum(e['random_direction']['lambda'].get('ci_hi'))}]"
                        ),
                        "metadata_toward_comply": e["toward_comply"],
                        "metadata_decay_ratio_64": e["toward_refuse"]["decay_ratio_64"],
                        "metadata_identifiable": cert.get("all_rows_identifiable"),
                    })
                # --- ordering tests at the refit geometry, for EVERY direction ---
                # The refusal direction is the treatment; the random direction is the
                # control. A control that separates the panel as well as the treatment
                # means the effect is not refusal-specific.
                from spi.indicators import paired_bootstrap_diff

                crows = cert["rows"]

                def lam_by_prompt(model: str, direction: str) -> dict[str, float]:
                    return {
                        r["prompt_id"]: r["layerL"]["estimates"]["est1_nls"]["lambda"]
                        for r in crows
                        if r["model"] == model and r["direction"] == direction
                        and r["layerL"]["estimates"]["est1_nls"].get("lambda") is not None
                    }

                ref_k = "qwen3-0.6b/instruct"
                comps = [m for m in sorted({r["model"] for r in crows}) if m != ref_k]
                all_tests: dict[str, Any] = {}
                for dname in ("toward_refuse", "toward_comply", "random_direction"):
                    all_tests[dname] = {
                        c: paired_bootstrap_diff(lam_by_prompt(ref_k, dname),
                                                 lam_by_prompt(c, dname))
                        for c in comps
                    }
                cert_meta["ordering_tests_all_directions"] = all_tests

                def n_sig_lower(dname: str) -> int:
                    return sum(1 for v in all_tests[dname].values()
                               if v.get("ci_excludes_zero") and v["diff"] < 0)

                abl = "qwen3-0.6b/abliterated"
                treat_abl = all_tests["toward_refuse"].get(abl, {})
                ctrl_abl = all_tests["random_direction"].get(abl, {})
                ctrl_sig = n_sig_lower("random_direction")
                treat_sig = n_sig_lower("toward_refuse")
                ident = bool(cert.get("all_rows_identifiable"))

                if ctrl_sig >= 1:
                    code = "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING"
                elif not ident:
                    code = "LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY"
                elif treat_sig == len(comps):
                    code = "LAMBDA_IDENTIFIABLE_ORDERING_AS_PREDICTED"
                else:
                    code = "LAMBDA_IDENTIFIABLE_ORDERING_ABSENT_OR_REVERSED"

                cert_meta["supplementary_verdict"] = {
                    "code": code,
                    "n_comparisons": len(comps),
                    "n_sig_lower_toward_refuse": treat_sig,
                    "n_sig_lower_random_direction": ctrl_sig,
                    "identifiable_at_refit_geometry": ident,
                    "decisive_pair_instruct_vs_abliterated": {
                        "toward_refuse": treat_abl,
                        "random_direction": ctrl_abl,
                        "why_decisive": (
                            "instruct and abliterated share an architecture and a base "
                            "model and differ only in whether refusal was removed, so "
                            "this is the pair that isolates safety tuning. "
                            "instruct-vs-base and instruct-vs-SmolLM2 additionally "
                            "differ in instruction tuning and lineage."
                        ),
                    },
                    "note": (
                        "Supplementary only. metadata.verdict is the pre-registered "
                        "verdict for the geometry the MAIN run used (T_fit=64), which "
                        "the validity study rejects, and it is left unchanged. This "
                        "code reports the outcome after refitting at T_fit=128. Note "
                        "that at the refit's own measured noise the rule moves to "
                        "n_roll>=40, which the achieved n_roll=20 still does not meet, "
                        "so lambda remains formally uncertified even after the longer "
                        "fit window."
                    ),
                }
        except Exception as exc:  # noqa: BLE001 - refit is supplementary
            logger.warning(f"could not merge refit_certified.json: {exc}")

    datasets = [
        {"dataset": "spi_model_level_prediction", "examples": model_examples},
        {"dataset": "spi_prompt_level_cells", "examples": cell_examples},
        {"dataset": "synthetic_lambda_identifiability", "examples": syn_examples},
    ]
    if gt_examples:
        datasets.append({"dataset": "ground_truth_refusal_screen", "examples": gt_examples})
    if cert_examples:
        datasets.append({"dataset": "lambda_at_certified_geometry",
                         "examples": cert_examples})

    # --- epsilon linearity, averaged over prompts before fitting ---
    # The run-time analysis treats every (prompt, eps) cell as an independent
    # point, so prompt-to-prompt scatter — which is large — is charged against
    # linearity. The response curve is a property of eps, with prompt as a
    # nuisance factor, so the fair test averages over prompts at each eps first.
    # Both versions are reported; this one does not supersede the pre-registered
    # control boolean, it explains it.
    eps_rows = raw["epsilon_sweep"]["rows"]
    eps_avg: dict[str, Any] = {}
    for m in sorted({r["model"] for r in eps_rows}):
        rs = [r for r in eps_rows if r["model"] == m and r["delta_at_p1"] is not None]
        by_eps: dict[float, list[float]] = {}
        for r in rs:
            by_eps.setdefault(round(float(r["eps_abs"]), 6), []).append(
                float(r["delta_at_p1"]))
        if len(by_eps) < 3:
            eps_avg[m] = {"reason": "too_few_eps_levels"}
            continue
        xs = np.array(sorted(by_eps))
        ys = np.array([float(np.mean(by_eps[x])) for x in xs])
        ns = [len(by_eps[x]) for x in xs]
        slope = float((xs * ys).sum() / max((xs * xs).sum(), 1e-12))
        pred = slope * xs
        ss = float(((ys - ys.mean()) ** 2).sum())
        r2 = 1.0 - float(((ys - pred) ** 2).sum()) / ss if ss > 0 else float("nan")
        rel = np.abs(ys - pred) / np.maximum(np.abs(pred), 1e-12)
        ok = xs[rel <= 0.10]
        # log-log slope: 1.0 is linear, <1 sub-linear (saturating)
        pos = (xs > 0) & (ys > 0)
        loglog = None
        if pos.sum() >= 3:
            lx, ly = np.log(xs[pos]), np.log(ys[pos])
            loglog = float(((lx - lx.mean()) * (ly - ly.mean())).sum()
                           / max(((lx - lx.mean()) ** 2).sum(), 1e-12))
        eps_avg[m] = {
            "eps_abs": [float(x) for x in xs],
            "mean_delta_at_p1": [float(y) for y in ys],
            "n_prompts_per_level": ns,
            "slope_through_origin": slope,
            "r2_through_origin": r2,
            "loglog_slope": loglog,
            "largest_eps_abs_within_10pct_of_linear": float(ok.max()) if ok.size else None,
            "linear_regime_exists": bool(r2 > 0.9 and ok.size >= 2),
        }
    epsilon_linearity_prompt_averaged = {
        "by_model": eps_avg,
        "any_model_has_linear_regime": any(
            v.get("linear_regime_exists") for v in eps_avg.values()),
        "note": (
            "Averaged over the 5 sweep prompts at each epsilon before fitting. A "
            "log-log slope near 1.0 means the response is linear in epsilon; below "
            "1.0 means it saturates. The per-cell version in epsilon_linearity is "
            "the pre-registered one and drives the control boolean."
        ),
    }

    # --- fit quality: is the exponential model even the right shape? ---
    # The synthetic identifiability study certifies the ESTIMATOR under a
    # CORRECTLY SPECIFIED exponential at the observed noise level. It says
    # nothing about whether the real recovery curve is exponential. That has to
    # be measured separately, and it is measured here.
    fit_q: dict[str, Any] = {}
    for m in models:
        rows = [r for r in raw["lambda"]
                if r["model"] == m and r["teacher_forced"]
                and r["direction"] == "toward_refuse"
                and r["p"] == base_p and abs(r["eps_c"] - base_c) < 1e-9]
        r2 = [r["layerL"]["estimates"]["est1_nls"].get("r2") for r in rows]
        r2 = [x for x in r2 if x is not None and np.isfinite(x)]
        bound = [bool(r["layerL"]["estimates"]["est1_nls"].get("at_bound")) for r in rows]
        lams = [r["layerL"]["estimates"]["est1_nls"].get("lambda") for r in rows]
        lams = [x for x in lams if x is not None and np.isfinite(x)]
        dr = [r["layerL"].get("decay_ratio_16") for r in rows]
        dr = [x for x in dr if x is not None and np.isfinite(x)]
        drf = [r["layerL"].get("decay_ratio_16") for r in raw["lambda"]
               if r["model"] == m and not r["teacher_forced"]
               and r["direction"] == "toward_refuse" and r["p"] == base_p
               and abs(r["eps_c"] - base_c) < 1e-9]
        drf = [x for x in drf if x is not None and np.isfinite(x)]
        fit_q[m] = {
            "median_r2": float(np.median(r2)) if r2 else None,
            "frac_fits_r2_below_0.3": float(np.mean([x < 0.3 for x in r2])) if r2 else None,
            "frac_lambda_at_bound": float(np.mean(bound)) if bound else None,
            "lambda_iqr": ([float(np.percentile(lams, 25)), float(np.percentile(lams, 75))]
                           if len(lams) > 3 else None),
            "lambda_iqr_ratio": (float(np.percentile(lams, 75) / np.percentile(lams, 25))
                                 if len(lams) > 3 and np.percentile(lams, 25) > 0 else None),
            "median_decay_ratio_16_teacher_forced": float(np.median(dr)) if dr else None,
            "median_decay_ratio_16_free_running": float(np.median(drf)) if drf else None,
        }
    med_r2 = [v["median_r2"] for v in fit_q.values() if v["median_r2"] is not None]
    poor = bool(med_r2 and np.median(med_r2) < 0.3)
    fit_quality = {
        "by_model": fit_q,
        "exponential_model_fits_poorly": poor,
        "interpretation": (
            "The synthetic study in min_series_length_rule certifies the estimator "
            "under a CORRECTLY SPECIFIED single exponential at the measured noise "
            "level. The measured r2 of the real fits is reported here separately, "
            "because a passing identifiability rule plus a low r2 means the estimator "
            "is fine and the MODEL SHAPE is wrong — lambda is then a poorly determined "
            "summary of a curve that is not a single exponential, which the wide "
            "per-prompt lambda IQR shows directly. Where that holds, the robust "
            "pre-registered substitutes should be preferred: the AUC/half-life "
            "statistic and decay_ratio_16, which assume no functional form. "
            "decay_ratio_16 separates the two pairing regimes cleanly and by a large "
            "margin (teacher-forced decays, free-running grows), and is the most "
            "trustworthy recovery statistic this artifact produces."
        ),
    }

    # --- model-free ordering test on decay_ratio_16, paired over prompts ---
    # Same pre-registered direction as the lambda test (a safety-tuned model
    # should relax MORE slowly, i.e. show a HIGHER surviving fraction at t=16),
    # but computed on a statistic that assumes no functional form.
    def dr_by_prompt(model: str) -> dict[str, float]:
        o = {}
        for r in raw["lambda"]:
            if (r["model"] == model and r["teacher_forced"]
                    and r["direction"] == "toward_refuse" and r["p"] == base_p
                    and abs(r["eps_c"] - base_c) < 1e-9):
                v = r["layerL"].get("decay_ratio_16")
                if v is not None and np.isfinite(v):
                    o[r["prompt_id"]] = float(v)
        return o

    ref_key = "qwen3-0.6b/instruct"
    decay_order: dict[str, Any] = {
        "statistic": "decay_ratio_16 = |delta_16| / |delta_0|, teacher-forced, layer-L",
        "prereg_direction": (
            "instruct should show a HIGHER surviving fraction (slower relaxation) "
            "than base and abliterated, matching the lower-lambda prediction"
        ),
        "assumes_functional_form": False,
    }
    for comp in [m for m in models if m != ref_key]:
        try:
            from spi.indicators import paired_bootstrap_diff

            decay_order[f"{ref_key}_minus_{comp}"] = paired_bootstrap_diff(
                dr_by_prompt(ref_key), dr_by_prompt(comp))
        except Exception as exc:  # noqa: BLE001 - diagnostic must not break the build
            decay_order[f"{ref_key}_minus_{comp}"] = {"error": str(exc)}

    # --- normalise controls so EVERY verdict exposes an explicit boolean ---
    controls = dict(raw["controls"])
    pos = controls.get("pos_probe_reproduces_ordering", {})
    if isinstance(pos, dict) and "value" not in pos:
        flags = [pos.get("var_star"), pos.get("ac1")]
        pos = dict(pos)
        pos["value"] = (True if any(f is True for f in flags)
                        else (False if any(f is False for f in flags) else None))
        controls["pos_probe_reproduces_ordering"] = pos
    epsl = controls.get("epsilon_linear_regime_exists", {})
    if isinstance(epsl, dict) and "value" not in epsl:
        epsl = dict(epsl)
        epsl["value"] = epsl.get("any_model_has_linear_regime")
        controls["epsilon_linear_regime_exists"] = epsl

    # --- two properties of the measurement that must be stated, not buried ---
    lens_corr = {}
    for m in models:
        v = [r["r_lens_vs_final_corr"] for r in raw["indicators"]
             if r["model"] == m and np.isfinite(r.get("r_lens_vs_final_corr", np.nan))]
        lens_corr[m] = float(np.median(v)) if v else None
    below = {m: (v is not None and abs(v) < 0.3) for m, v in lens_corr.items()}

    var_identical = []
    for r in raw["indicators"]:
        a = r["primary"]["detrended"]["var_star"]
        b = r["primary"]["raw"]["var_star"]
        if a is not None and b is not None:
            var_identical.append(abs(a - b) < 1e-9)

    readout_note = {
        "median_corr_layerL_lens_vs_final_logits": lens_corr,
        "below_0.3_threshold": below,
        "any_below_threshold": any(below.values()),
        "consequence": (
            "The pre-registered rule says that if |corr| < 0.3 at the chosen L this must "
            "be stated loudly and a deeper readout used alongside the layer-L "
            "perturbation. It IS below threshold, so every indicator and every lambda in "
            "this artifact is reported at BOTH readouts — the layer-L logit lens and the "
            "final-layer logits — and neither is silently preferred. The layer-L lens and "
            "the final-layer contrast are measuring substantially different things at this "
            "depth, which is itself a result about the logit lens at 0.6B scale."
        ),
    }
    detrend_note = {
        "var_star_detrended_equals_raw": bool(var_identical and all(var_identical)),
        "why": (
            "Var* is the ACROSS-ROLLOUT variance at each step, and detrending subtracts "
            "the across-rollout mean at that same step. Subtracting a per-step constant "
            "cannot change a per-step variance, so detrended and raw Var* are identical "
            "by construction — not a bug, and not evidence that detrending did nothing. "
            "Detrending does move AC1 and flicker, and those deltas are reported per cell "
            "in metadata_detrend_delta."
        ),
    }

    metadata: dict[str, Any] = {
        "readout_channel_check": readout_note,
        "detrending_note": detrend_note,
        "method_name": "SPI — Safety Proximity Indicators (Tier-0 feasibility)",
        "description": (
            "Measures four early-warning indicators of a refusal observable r_t during "
            "ordinary sampled generation on HARMLESS prompts only, and asks whether they "
            "order a base / safety-tuned / abliterated model triad plus a low-refusal "
            "anchor the way measured refusal rates do. The make-or-break question is "
            "estimator identifiability, answered by a synthetic recovery study at the "
            "noise level actually observed."
        ),
        "our_method": (
            "SPI = mean of z-scored [-log lambda_refuse, log Var*, Fisher-z AC1, "
            "logit flicker], measured on 20 harmless prompts with zero harmful prompts "
            "and zero labels."
        ),
        "baseline": (
            "Supervised difference-in-means refusal direction fitted on a 32/32 "
            "harmful-vs-benign contrast set at the same layer, scored by AUROC — the "
            "field's standard strong approach, deliberately given the harmful data our "
            "method is denied. Second baseline: r_0 harmful-minus-benign margin."
        ),
        "verdict": raw["verdict"],
        "lambda_at_certified_geometry": cert_meta,
        "fit_quality": fit_quality,
        "decay_ratio_ordering": decay_order,
        "rank_agreement": corr,
        "controls": controls,
        "panel_validity": raw["panel_validity"],
        "min_series_length_rule": raw["min_series_length_rule"],
        "ordering_tests": raw["ordering_tests"],
        "provisional_spi": raw["provisional_spi"],
        "layer_choice": raw["layer_choice"],
        "model_revisions": raw["model_revisions"],
        "per_model_meta": raw["per_model_meta"],
        "epsilon_linearity": raw["epsilon_sweep"]["linearity"],
        "epsilon_linearity_prompt_averaged": epsilon_linearity_prompt_averaged,
        "grid_actually_run": raw["grid_actually_run"],
        "tokens_per_sec_by_model": raw["tokens_per_sec_by_model"],
        "peak_vram_gb": raw["peak_vram_gb"],
        "wall_clock_by_stage": raw["wall_clock_by_stage"],
        "hardware": raw["hardware"],
        "prompts": raw["prompts"],
        "observable_token_ids_by_model": raw["observable_token_ids_by_model"],
        "observable_degenerate_by_model": raw["observable_degenerate_by_model"],
        "synthetic_meta": raw["synthetic_meta"],
        "aggregate_by_model": raw["aggregate_by_model"],
        "limitations": list(raw["limitations"]) + DISCOVERED_LIMITATIONS,
        "raw_results_file": "out/tier0_raw.json",
        "cost_usd": 0.0,
    }
    return {"metadata": metadata, "datasets": datasets}


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "method_out.json"
    raw = json.loads(src.read_text())
    if "datasets" in raw and "aggregate_by_model" not in raw:
        # method_out.json has already been reshaped. Rebuild from the archived raw
        # tree instead of no-opping, so re-running the pipeline picks up analysis
        # changes rather than silently keeping a stale file.
        archived = ROOT / "out" / "tier0_raw.json"
        if not archived.exists():
            logger.info("Input is already in schema form and no raw tree is archived; "
                        "nothing to do.")
            return
        logger.info(f"{src.name} is already reshaped; rebuilding from {archived}")
        raw = json.loads(archived.read_text())
    (ROOT / "out" / "tier0_raw.json").write_text(json.dumps(raw, indent=1, default=float))
    out = build(raw)
    dst = ROOT / "method_out.json"
    dst.write_text(json.dumps(out, indent=1, default=float))
    n = sum(len(d["examples"]) for d in out["datasets"])
    logger.info(f"Wrote {dst} — {len(out['datasets'])} datasets, {n} examples, "
                f"{dst.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
