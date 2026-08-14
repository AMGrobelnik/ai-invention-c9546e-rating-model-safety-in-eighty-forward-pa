#!/usr/bin/env python3
"""Dry-run every Stage-J analysis function on mock rows with the EXACT structure
`measure_model` emits, so a crash cannot first surface at the end of a 90-minute
GPU run. Also exercises build_output on the assembled tree.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
import run_tier0 as R  # noqa: E402
from spi import indicators as ind  # noqa: E402
from spi import validity as val  # noqa: E402

MODELS = [
    ("qwen3-0.6b/base", "base", "qwen3-0.6b"),
    ("qwen3-0.6b/instruct", "instruct", "qwen3-0.6b"),
    ("qwen3-0.6b/abliterated", "abliterated", "qwen3-0.6b"),
    ("smollm2/base", "base", "smollm2"),
]
N_PROMPTS = 20
N_ROLL = 20
T = 192
rng = np.random.default_rng(0)


def mock_readout(lam_true: float, degenerate: bool = False) -> dict:
    t = np.arange(R.FIT_LEN, dtype=float)
    sgn = 0.02 * np.exp(-lam_true * t) + rng.normal(0, 0.004, R.FIT_LEN)
    D = sgn[:, None] + rng.normal(0, 0.009, (R.FIT_LEN, N_ROLL))
    ab = np.abs(D).mean(axis=1)
    est = ind.estimate_lambda_all(sgn, 0.009, fit_len=R.FIT_LEN, delta_abs=ab)
    if degenerate:  # force the failed-fit path
        est["est1_nls"] = {"lambda": None, "reason": "curve_fit_failed:RuntimeError"}
    return {
        "delta_residual_sd_per_rollout": 0.009,
        "delta_residual_sd_of_mean": 0.009 / np.sqrt(N_ROLL),
        "delta_at_p1_signed": float(sgn[0]), "delta_at_p1": float(ab[0]),
        "delta_snr_at_p1": 2.2, "delta_snr_at_p1_vs_fit_noise": 11.0,
        "steps_above_noise_floor": 12, "monotone_decay_frac": 0.8,
        "decay_ratio_16": 0.3, "estimates": est,
        "per_rollout_lambda": [float(x) for x in rng.normal(lam_true, 0.05, N_ROLL)],
        "per_rollout_delta_at_p1": [float(x) for x in D[0]],
        "mean_delta_curve": [float(x) for x in sgn],
        "mean_abs_delta_curve": [float(x) for x in ab],
    }


def mock_fluct(scale: float) -> dict:
    X = rng.normal(0, scale, (T, N_ROLL)) - 3.0
    return ind.fluctuation_indicators(X, R.BURN_IN)


def build_rows() -> tuple[list, list, list]:
    all_ind, all_lam, all_eps = [], [], []
    for mi, (key, member, lineage) in enumerate(MODELS):
        scale = 1.0 + 0.3 * mi
        lam_true = 0.15 - 0.02 * mi
        for pi in range(N_PROMPTS):
            pid = f"p{pi:02d}"
            all_ind.append({
                "model": key, "member": member, "lineage": lineage,
                "prompt_id": pid, "register": "factual_qa", "layer": 15,
                "primary": mock_fluct(scale),
                "final_layer_readout": mock_fluct(scale * 1.1),
                "r_lens_vs_final_corr": 0.18,
                "control_random_axis": [mock_fluct(1.0) for _ in range(3)],
                "control_pos_probe": mock_fluct(0.9),
                "descriptive_diff_means": mock_fluct(0.8),
                "series_length_sweep": R.series_length_sweep(
                    rng.normal(0, scale, (T, N_ROLL))),
                "noise_sd_detrended": scale, "median_resid_norm": 44.0,
                "frac_rollouts_hit_eos": 0.1, "median_eos_step": float(T),
                "tokens_per_sec": 590.0, "sample_completion": "mock",
            })
            for dname in ("toward_refuse", "toward_comply", "random_direction"):
                for tf in (True, False):
                    # exercise the failed-fit path on one cell
                    deg = (pi == 0 and dname == "random_direction" and not tf)
                    all_lam.append({
                        "model": key, "member": member, "lineage": lineage,
                        "prompt_id": pid, "direction": dname,
                        "eps_c": R.BASE_EPS_C, "eps_abs": 4.4, "p": R.BASE_P,
                        "teacher_forced": tf, "n_roll": N_ROLL, "T": T,
                        "fit_len": R.FIT_LEN,
                        "median_first_divergence_after_p": None if tf else 2.0,
                        "layerL": mock_readout(lam_true, deg),
                        "final": mock_readout(lam_true * 1.2),
                    })
            if pi < 5:
                for c in (0.02, 0.05, 0.2, 0.4, 0.8):
                    all_lam.append({
                        "model": key, "member": member, "lineage": lineage,
                        "prompt_id": pid, "direction": "toward_refuse",
                        "eps_c": c, "eps_abs": 44.0 * c, "p": R.BASE_P,
                        "teacher_forced": True, "n_roll": N_ROLL, "T": T,
                        "fit_len": R.FIT_LEN, "median_first_divergence_after_p": None,
                        "layerL": mock_readout(lam_true), "final": mock_readout(lam_true),
                    })
                    all_eps.append({
                        "model": key, "prompt_id": pid, "eps_c": c,
                        "eps_abs": 44.0 * c, "delta_at_p1": 0.02 * c / R.BASE_EPS_C,
                        "delta_at_p1_final": 0.05 * c / R.BASE_EPS_C,
                        "lambda": lam_true, "lambda_final": lam_true,
                    })
                all_eps.append({
                    "model": key, "prompt_id": pid, "eps_c": R.BASE_EPS_C,
                    "eps_abs": 4.4, "delta_at_p1": 0.02, "delta_at_p1_final": 0.05,
                    "lambda": lam_true, "lambda_final": lam_true,
                })
                for p_inj in (4, 64, 128):
                    all_lam.append({
                        "model": key, "member": member, "lineage": lineage,
                        "prompt_id": pid, "direction": "toward_refuse",
                        "eps_c": R.BASE_EPS_C, "eps_abs": 4.4, "p": p_inj,
                        "teacher_forced": True, "n_roll": N_ROLL, "T": T,
                        "fit_len": R.FIT_LEN, "median_first_divergence_after_p": None,
                        "layerL": mock_readout(lam_true), "final": mock_readout(lam_true),
                    })
    return all_ind, all_lam, all_eps


@logger.catch(reraise=True)
def main() -> None:
    all_ind, all_lam, all_eps = build_rows()
    logger.info(f"mock: {len(all_ind)} indicator rows, {len(all_lam)} lambda rows")

    agg = R.agg_by_model(all_ind, all_lam)
    logger.info(f"agg_by_model OK — {len(agg)} models")
    syn = val.synthetic_ar1_study(0.009, 0.02, n_reps=40, n_workers=16)
    rule = syn["rule"]
    for row in all_lam:
        ok = val.is_identifiable(rule, row["fit_len"], row["n_roll"])
        row["identifiable"] = bool(ok and row["teacher_forced"])
        row["identifiable_reason"] = (
            "geometry_below_prereg_rule" if not ok
            else ("free_running_pairing_broken" if not row["teacher_forced"] else None))
    tests = R.ordering_tests(all_ind, all_lam)
    logger.info(f"ordering_tests OK — {len(tests)} blocks")
    eps_lin = R.analyse_epsilon_linearity(all_eps)
    logger.info(f"analyse_epsilon_linearity OK — any_linear="
                f"{eps_lin['any_model_has_linear_regime']}")

    gt = {m: {"harmful_refusal_rate": ind.wilson_ci(k, 40),
              "xstest_over_refusal_rate": ind.wilson_ci(2, 30),
              "detail": {s: {"rate": ind.wilson_ci(k, 40), "examples": [
                  {"prompt": "x", "completion": "y", "refusal": "True"}]}
                  for s in ("harmful", "xstest_safe")},
              "matcher": "advbench_prefix_string_match"}
          for m, k in zip([x[0] for x in MODELS], [4, 30, 2, 1])}
    panel = R.check_panel_validity(gt)
    cfg = R.MODES["full"]
    controls = R.control_verdicts(agg, tests, syn, eps_lin, cfg)
    ra = {m: agg[m]["control_random_axis_var_star"]["point"] for m in agg}
    pr = {m: agg[m]["var_star"]["point"] for m in agg}
    ok = [m for m in ra if ra[m] is not None and pr[m] is not None]
    controls["random_axis_reproduces_ordering"] = {
        "value": bool(len(ok) >= 3 and np.corrcoef(
            [ra[m] for m in ok], [pr[m] for m in ok])[0, 1] > 0.9),
        "rank_corr_with_primary_var_star": float(np.corrcoef(
            [ra[m] for m in ok], [pr[m] for m in ok])[0, 1]) if len(ok) >= 3 else None,
        "detail": controls.pop("random_axis_detail"),
    }
    logger.info("control_verdicts OK")
    spi = R.provisional_spi(agg)
    logger.info(f"provisional_spi OK — terms_used={spi['terms_used']}")
    verdict = R.decide_verdict(controls, agg, panel)
    logger.info(f"decide_verdict OK — {verdict['code']}")

    tree = {
        "status": "completed", "mode": "full",
        "grid_actually_run": {**cfg, "base_eps_c": R.BASE_EPS_C, "base_p": R.BASE_P,
                              "fit_len": R.FIT_LEN, "burn_in": R.BURN_IN,
                              "series_lengths": list(R.SERIES_LENGTHS)},
        "hardware": {"device": "cuda", "gpu": "mock"},
        "tokens_per_sec_by_model": {m: 590.0 for m in agg},
        "peak_vram_gb": 2.0, "wall_clock_by_stage": {"total": 1.0},
        "model_revisions": {m: {"model_id": m, "revision": "0" * 40, "n_layers": 28,
                                "hidden": 1024, "dtype": "bfloat16",
                                "chat_template": True, "rendered_example": "x"}
                            for m in agg},
        "layer_choice": {"reference_model": "mock", "n_layers_ref": 28,
                         "per_layer_curve": [{"layer": i, "auroc": 0.9,
                                              "separation": 0.8, "cohens_d": 1.0}
                                             for i in range(28)],
                         "L_ref": 15, "rel_depth": 0.536, "best_auroc": 0.99,
                         "best_separation": 0.98, "timestamp": "now",
                         "peak_in_middle_third": True, "L_by_model": {}},
        "observable_token_ids_by_model": {m: {"refusal_ids": [1]} for m in agg},
        "per_model_meta": {m: {"L": 15, "eps_reference_norm": 44.0,
                               "diff_means": {"auroc": 0.9 + 0.01 * i,
                                              "cohens_d": 3.0, "d_norm": 13.0,
                                              "median_resid_norm_benign": 44.0,
                                              "mean_resid_norm_benign": 44.0,
                                              "layer": 15, "cosine_with_parent": 0.9},
                               "observable_sanity": {"margin": 0.7 - 0.2 * i,
                                                     "auroc": 0.79, "r0_finite": True,
                                                     "r0_non_constant": True},
                               "pos_probe": {"tagger": "nltk", "train_acc": 0.99,
                                             "n_train": 4136, "classes": ["FUNC"]},
                               "banned_token_ids": []}
                          for i, m in enumerate(agg)},
        "prompts": {"benign": [{"id": "p00", "register": "factual_qa", "text": "x"}],
                    "benign_screen": {"passed": True, "hits": []},
                    "n_contrast_harmful": 32, "n_contrast_benign": 32,
                    "n_gt_harmful": 40, "n_gt_xstest": 30, "sources": {}},
        "indicators": all_ind, "lambda": all_lam, "aggregate_by_model": agg,
        "asymmetry_index_by_model": {m: agg[m]["asymmetry_index"] for m in agg},
        "epsilon_sweep": {"rows": all_eps, "linearity": eps_lin},
        "synthetic_ar1_table": syn["table"],
        "min_series_length_rule": rule,
        "synthetic_meta": {k: v for k, v in syn.items() if k != "table"},
        "controls": controls, "ground_truth": gt, "panel_validity": panel,
        "provisional_spi": spi, "ordering_tests": tests, "verdict": verdict,
        "observable_degenerate_by_model": {m: agg[m]["observable_degenerate"] for m in agg},
        "limitations": R.LIMITATIONS,
    }
    out = Path("out/_dryrun_raw.json")
    out.write_text(json.dumps(tree, indent=1, default=float))
    logger.info(f"raw tree written {out.stat().st_size / 1e6:.2f} MB")

    import build_output as B

    schema = B.build(tree)
    Path("out/_dryrun_schema.json").write_text(json.dumps(schema, indent=1, default=float))
    logger.info(f"build_output OK — "
                f"{[(d['dataset'], len(d['examples'])) for d in schema['datasets']]}")
    logger.info("DRY RUN PASSED — the Stage-J analysis path is crash-free")


if __name__ == "__main__":
    main()
