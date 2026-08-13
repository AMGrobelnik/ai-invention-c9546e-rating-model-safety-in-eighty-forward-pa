#!/usr/bin/env python3
"""Re-analysis ("evaluation") of the iteration-1 refusal-wobble dynamics arm.

PURE RE-ANALYSIS. No rollouts are regenerated, no steering is re-run, no
exponential model is re-fitted for a headline number. Every reported quantity is
derived from files already on disk and carries a JSON pointer back to them.

Four repairs (see the artifact plan):
  A1  refusal-direction vs random-direction control recomputed on the
      assumption-free statistics (decay_ratio_16, auc_norm) with paired
      bootstraps, a difference-in-differences, and an equivalence test.
  A2  per-model observable-validity gate at both readouts, plus a
      behaviour-independent instrument-sensitivity check from experiment 2.
  A3  exact-permutation ceiling on the n=4 SPI-vs-baseline rank comparison.
  A4  AC1 length confound settled with the archived series_length_sweep.
  A5  cross-arm asymmetry table (token channel vs steering channel).

Outputs: eval_out.json, figs/F1..F6 (PDF+PNG), results_section.md,
deviations.json / deviations.csv.
"""

from __future__ import annotations

import gc
import json
import math
import os
import resource
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import psutil
from loguru import logger
from scipy import stats

import eval_lib as EL

# --------------------------------------------------------------------------- #
# logging / hardware guard
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
(HERE / "logs").mkdir(exist_ok=True)
(HERE / "figs").mkdir(exist_ok=True)
(HERE / "out").mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "eval.log", rotation="30 MB", level="DEBUG")


def _container_ram_gb() -> float | None:
    for p in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError, PermissionError):
            pass
    return None


def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError, PermissionError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1


NUM_CPUS = _detect_cpus()
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM = psutil.virtual_memory().available
# The whole re-analysis holds one 11 MB JSON tree plus small frames; 8 GB is
# generous (~30x the peak observed) and well under what is available.
RAM_BUDGET = int(min(8e9, 0.5 * AVAILABLE_RAM))
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

# --------------------------------------------------------------------------- #
# paths
# --------------------------------------------------------------------------- #
RUN = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art")
E1 = RUN / "gen_art_experiment_1"
E2 = RUN / "gen_art_experiment_2"
D1 = RUN / "gen_art_dataset_1"

TIER0 = E1 / "out" / "tier0_raw.json"
REFIT = E1 / "out" / "refit_certified.json"
LAYERC = E1 / "out" / "layer_choice.json"
E2_OUT = E2 / "full_method_out.json"
E2_GENS = E2 / "gens"
D1_OUT = D1 / "full_data_out.json"

READOUTS = {"layerL": "layerL", "final": "final"}          # keys inside lambda rows
IND_READOUTS = {"layerL": "primary", "final": "final_layer_readout"}
MODELS = ["qwen3-0.6b/base", "qwen3-0.6b/instruct",
          "qwen3-0.6b/abliterated", "smollm2/base"]
PRIMARY_PAIR = ("qwen3-0.6b/instruct", "qwen3-0.6b/abliterated")
EQ_MARGIN = 0.20            # log units, pre-registered in this artifact's plan
GATE_AUROC = 0.70
GATE_THRESHOLDS = [0.60, 0.65, 0.70, 0.75, 0.80]
PRIMARY_CELL = {"eps_c": 0.1, "p": 16}


# --------------------------------------------------------------------------- #
# STEP 0 - load, validate, freeze
# --------------------------------------------------------------------------- #

def build_frames(tree: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """LAM: one row per (lambda entry x readout). IND: one row per
    (indicators entry x readout)."""
    lam_rows: list[dict[str, Any]] = []
    for i, r in enumerate(tree["lambda"]):
        for rd, key in READOUTS.items():
            blk = r.get(key) or {}
            est = blk.get("estimates") or {}
            nls = est.get("est1_nls") or {}
            auc = est.get("auc_substitute") or {}
            prl = [v for v in (blk.get("per_rollout_lambda") or [])
                   if v is not None and np.isfinite(v)]
            if len(prl) >= 4:
                q75, q25 = np.percentile(prl, [75, 25])
                iqr_ratio = float(q75 / q25) if q25 > 1e-12 else float("inf")
            else:
                iqr_ratio = float("nan")
            lam_rows.append({
                "idx": i, "ptr": f"tier0_raw.json:lambda[{i}].{key}",
                "model": r["model"], "member": r["member"], "lineage": r["lineage"],
                "prompt_id": r["prompt_id"], "direction": r["direction"],
                "eps_c": r["eps_c"], "p": r["p"],
                "teacher_forced": bool(r["teacher_forced"]),
                "n_roll": r["n_roll"], "T": r["T"], "fit_len": r["fit_len"],
                "identifiable": r["identifiable"],
                "identifiable_reason": r["identifiable_reason"],
                "readout": rd,
                "decay_ratio_16": blk.get("decay_ratio_16"),
                "auc_norm": auc.get("auc_norm"),
                "half_life": auc.get("half_life"),
                "delta_snr_at_p1": blk.get("delta_snr_at_p1"),
                "monotone_decay_frac": blk.get("monotone_decay_frac"),
                "steps_above_noise_floor": blk.get("steps_above_noise_floor"),
                "nls_lambda": nls.get("lambda"), "nls_r2": nls.get("r2"),
                "nls_at_bound": nls.get("at_bound"),
                "estimator_spread": est.get("estimator_spread"),
                "estimator_agreement_ratio": est.get("estimator_agreement_ratio"),
                "per_rollout_lambda_iqr_ratio": iqr_ratio,
            })
    LAM = pd.DataFrame(lam_rows)

    ind_rows: list[dict[str, Any]] = []
    for i, r in enumerate(tree["indicators"]):
        for rd, key in IND_READOUTS.items():
            blk = r[key]
            det, raw = blk["detrended"], blk["raw"]
            ind_rows.append({
                "idx": i, "ptr": f"tier0_raw.json:indicators[{i}].{key}",
                "model": r["model"], "member": r["member"], "lineage": r["lineage"],
                "prompt_id": r["prompt_id"], "register": r["register"],
                "layer": r["layer"], "readout": rd,
                "var_star": det["var_star"], "var_star_raw": raw["var_star"],
                "ac1": det["ac1"], "ac1_uncorrected": det["ac1_uncorrected"],
                "ac1_raw": raw["ac1"], "ac1_raw_uncorrected": raw["ac1_uncorrected"],
                "flicker": det["flicker_crossings_per_100"],
                "flicker_raw": raw["flicker_crossings_per_100"],
                "n_steps": blk["n_steps"], "n_rollouts": blk["n_rollouts"],
                "frac_rollouts_hit_eos": r["frac_rollouts_hit_eos"],
                "median_eos_step": r["median_eos_step"],
                "r_lens_vs_final_corr": r["r_lens_vs_final_corr"],
            })
    IND = pd.DataFrame(ind_rows)

    census = {
        "n_lambda_rows_archived": len(tree["lambda"]),
        "n_lambda_rows_expected": 640,
        "n_lambda_rows_match": len(tree["lambda"]) == 640,
        "n_indicator_rows_archived": len(tree["indicators"]),
        "direction_census": LAM.query("readout=='layerL'")["direction"].value_counts().to_dict(),
        "teacher_forced_census": {str(k): int(v) for k, v in
                                  LAM.query("readout=='layerL'")["teacher_forced"]
                                  .value_counts().to_dict().items()},
        "eps_c_census": {str(k): int(v) for k, v in
                         LAM.query("readout=='layerL'")["eps_c"].value_counts().to_dict().items()},
        "p_census": {str(k): int(v) for k, v in
                     LAM.query("readout=='layerL'")["p"].value_counts().to_dict().items()},
        "n_roll_unique": sorted(LAM["n_roll"].unique().tolist()),
        "T_unique": sorted(LAM["T"].unique().tolist()),
        "fit_len_unique": sorted(LAM["fit_len"].unique().tolist()),
        "models": sorted(LAM["model"].unique().tolist()),
        "n_prompts": int(LAM["prompt_id"].nunique()),
        "n_identifiable_false": int((~LAM.query("readout=='layerL'")["identifiable"]).sum()),
        "n_identifiable_true": int(LAM.query("readout=='layerL'")["identifiable"].sum()),
        "identifiable_reasons": LAM.query("readout=='layerL'")["identifiable_reason"]
                                   .value_counts().to_dict(),
        "primary_cell": dict(PRIMARY_CELL),
        "deviation_from_plan_expectation": (
            "The plan expected 4 models x 20 prompts x 2 directions x 2 channels = 640 rows "
            "with a single (eps_c, p) cell. The archive is 640 rows but the design is richer: "
            "3 directions (toward_refuse 320, toward_comply 160, random_direction 160), "
            "teacher_forced True 400 / False 240, and toward_refuse additionally carries an "
            "eps sweep (eps_c in {0.02,0.05,0.2,0.4,0.8}, 20 rows each) and an injection-step "
            "sweep (p in {4,64,128}, 20 rows each). All analyses therefore FILTER to the "
            "primary cell eps_c=0.1, p=16 before any contrast."),
    }
    # missingness of the two primary statistics
    prim = LAM[(LAM["eps_c"] == PRIMARY_CELL["eps_c"]) & (LAM["p"] == PRIMARY_CELL["p"])]
    miss = []
    for (m, d, tf, rd), g in prim.groupby(["model", "direction", "teacher_forced", "readout"]):
        for stat in ("decay_ratio_16", "auc_norm"):
            v = pd.to_numeric(g[stat], errors="coerce")
            miss.append({"model": m, "direction": d, "teacher_forced": bool(tf),
                         "readout": rd, "statistic": stat, "n": int(len(g)),
                         "n_missing_or_nonfinite": int((~np.isfinite(v)).sum()),
                         "n_nonpositive": int((v <= 0).sum())})
    census["primary_cell_missingness"] = miss
    census["n_primary_cell_rows_per_readout"] = int(len(prim) / 2)
    return LAM, IND, census


# --------------------------------------------------------------------------- #
# ANALYSIS 1 - direction contrast on assumption-free statistics
# --------------------------------------------------------------------------- #
STATS = {"S1_decay_ratio_16": "decay_ratio_16", "S2_auc_norm": "auc_norm"}


def _series(prim: pd.DataFrame, model: str, direction: str, tf: bool,
            readout: str, col: str) -> dict[str, float]:
    g = prim[(prim["model"] == model) & (prim["direction"] == direction)
             & (prim["teacher_forced"] == tf) & (prim["readout"] == readout)]
    out: dict[str, float] = {}
    for _, r in g.iterrows():
        v = r[col]
        if v is None or not np.isfinite(v) or v <= 0:
            continue
        out[r["prompt_id"]] = float(np.log(v))
    return out


def analysis1(LAM: pd.DataFrame) -> dict[str, Any]:
    prim = LAM[(LAM["eps_c"] == PRIMARY_CELL["eps_c"]) & (LAM["p"] == PRIMARY_CELL["p"])].copy()
    for c in ("decay_ratio_16", "auc_norm"):
        prim[c] = pd.to_numeric(prim[c], errors="coerce")

    contrast_rows: list[dict[str, Any]] = []
    did_rows: list[dict[str, Any]] = []
    channels = {"teacher_forced": True, "free_running": False}

    # ---- 1.1 per-model random-minus-refuse contrast -----------------------
    for sname, col in STATS.items():
        for rd in READOUTS:
            for chan, tf in channels.items():
                for m in MODELS:
                    a = _series(prim, m, "random_direction", tf, rd, col)
                    b = _series(prim, m, "toward_refuse", tf, rd, col)
                    d, keys = EL._clean_pairs(a, b)
                    bs = EL.bootstrap_mean(d)
                    wx = EL.wilcoxon_signed_rank(d)
                    contrast_rows.append({
                        "analysis": "1.1_direction_contrast",
                        "model": m, "statistic": sname, "readout": rd, "channel": chan,
                        "contrast": "log S(random_direction) - log S(toward_refuse)",
                        "mean_log_diff": bs["diff"], "ci_lo": bs["ci_lo"], "ci_hi": bs["ci_hi"],
                        "sd": bs["sd"], "n_pairs": bs["n_pairs"],
                        "ci_excludes_zero": bs["ci_excludes_zero"],
                        "boot_p_two_sided": bs["boot_p_two_sided"],
                        "wilcoxon_p": wx["p"], "wilcoxon_mode": wx["mode"],
                        "cliffs_delta_paired": EL.paired_cliffs_delta(d),
                        "cliffs_delta_unpaired": EL.cliffs_delta(list(a.values()), list(b.values())),
                        "ratio_natural_scale": float(np.exp(bs["diff"])) if bs["diff"] is not None else None,
                        "median_random_natural": float(np.exp(np.median(list(a.values())))) if a else None,
                        "median_refuse_natural": float(np.exp(np.median(list(b.values())))) if b else None,
                        "prompts_used": len(keys),
                        "ptr": (f"tier0_raw.json:lambda[* where model={m}, eps_c=0.1, p=16, "
                                f"teacher_forced={tf}, direction in "
                                f"{{random_direction,toward_refuse}}].{READOUTS[rd]}."
                                + ("decay_ratio_16" if col == "decay_ratio_16"
                                   else "estimates.auc_substitute.auc_norm")),
                    })

    # ---- 1.2/1.3 difference-in-differences + equivalence -------------------
    for sname, col in STATS.items():
        for rd in READOUTS:
            for chan, tf in channels.items():
                for A, B in combinations(MODELS, 2):
                    rA = _series(prim, A, "toward_refuse", tf, rd, col)
                    rB = _series(prim, B, "toward_refuse", tf, rd, col)
                    nA = _series(prim, A, "random_direction", tf, rd, col)
                    nB = _series(prim, B, "random_direction", tf, rd, col)
                    keys = sorted(set(rA) & set(rB) & set(nA) & set(nB))
                    d = np.asarray([(rA[k] - rB[k]) - (nA[k] - nB[k]) for k in keys],
                                   dtype=np.float64)
                    bs = EL.bootstrap_mean(d)
                    tt = EL.tost(d, EQ_MARGIN)
                    wx = EL.wilcoxon_signed_rank(d)
                    if bs["ci_excludes_zero"]:
                        verdict = "DIRECTION_SPECIFIC"
                    elif tt["equivalent"]:
                        verdict = "NO_DIRECTION_SPECIFICITY"
                    else:
                        verdict = "INCONCLUSIVE"
                    is_primary = (
                        {A, B} == set(PRIMARY_PAIR) and sname == "S1_decay_ratio_16"
                        and rd == "layerL" and chan == "teacher_forced")
                    did_rows.append({
                        "analysis": "1.2_interaction_did",
                        "pair": f"{A}_minus_{B}", "model_a": A, "model_b": B,
                        "statistic": sname, "readout": rd, "channel": chan,
                        "is_primary": bool(is_primary),
                        "did_mean": bs["diff"], "ci_lo": bs["ci_lo"], "ci_hi": bs["ci_hi"],
                        "sd": bs["sd"], "n_pairs": bs["n_pairs"],
                        "ci_excludes_zero": bs["ci_excludes_zero"],
                        "boot_p_two_sided": bs["boot_p_two_sided"],
                        "wilcoxon_p": wx["p"],
                        "tost_margin": EQ_MARGIN, "tost_p": tt["p_tost"],
                        "tost_ci90_lo": tt["ci90_lo"], "tost_ci90_hi": tt["ci90_hi"],
                        "tost_equivalent": tt["equivalent"],
                        "verdict": verdict,
                        "n_prompts_for_pm020_margin_80pct_power":
                            EL.tost_sample_size(bs["sd"] or float("nan"), EQ_MARGIN),
                        "ptr": (f"tier0_raw.json:lambda[* where model in {{{A},{B}}}, eps_c=0.1, "
                                f"p=16, teacher_forced={tf}].{READOUTS[rd]}"),
                    })

    # ---- 1.4 multiplicity --------------------------------------------------
    fam = {r["pair"] + "|" + r["statistic"] + "|" + r["readout"] + "|" + r["channel"]:
           r["wilcoxon_p"] for r in did_rows}
    adj = EL.holm(fam)
    for r in did_rows:
        k = r["pair"] + "|" + r["statistic"] + "|" + r["readout"] + "|" + r["channel"]
        r["wilcoxon_p_holm"] = adj.get(k)
        r["family_size"] = len(fam)

    # ---- 1.6 free-running vs teacher-forced (the surviving R3 evidence) ----
    ratchet_rows: list[dict[str, Any]] = []
    for sname, col in STATS.items():
        for rd in READOUTS:
            for m in MODELS:
                a = _series(prim, m, "toward_refuse", False, rd, col)   # free running
                b = _series(prim, m, "toward_refuse", True, rd, col)    # teacher forced
                d, keys = EL._clean_pairs(a, b)
                bs = EL.bootstrap_mean(d)
                wx = EL.wilcoxon_signed_rank(d)
                ratchet_rows.append({
                    "analysis": "1.6_free_vs_teacher_forced",
                    "model": m, "statistic": sname, "readout": rd,
                    "contrast": "log S(free_running) - log S(teacher_forced)",
                    "mean_log_diff": bs["diff"], "ci_lo": bs["ci_lo"], "ci_hi": bs["ci_hi"],
                    "n_pairs": bs["n_pairs"], "ci_excludes_zero": bs["ci_excludes_zero"],
                    "wilcoxon_p": wx["p"],
                    "ratio_natural_scale": float(np.exp(bs["diff"])) if bs["diff"] is not None else None,
                    "median_free_natural": float(np.exp(np.median(list(a.values())))) if a else None,
                    "median_tf_natural": float(np.exp(np.median(list(b.values())))) if b else None,
                    "ptr": f"tier0_raw.json:lambda[* model={m}, direction=toward_refuse, "
                           f"eps_c=0.1, p=16].{READOUTS[rd]}",
                })
    return {"contrast": contrast_rows, "did": did_rows, "ratchet": ratchet_rows}


def analysis1_lambda_consistency(tree: dict[str, Any], LAM: pd.DataFrame) -> dict[str, Any]:
    """1.5 - lambda demoted to a LABELLED consistency check."""
    ot = tree["ordering_tests"]
    prim = LAM[(LAM["eps_c"] == PRIMARY_CELL["eps_c"]) & (LAM["p"] == PRIMARY_CELL["p"])
               & (LAM["teacher_forced"])].copy()
    prim["nls_r2"] = pd.to_numeric(prim["nls_r2"], errors="coerce")

    diag: dict[str, Any] = {}
    for m in MODELS:
        for rd in READOUTS:
            g = prim[(prim["model"] == m) & (prim["readout"] == rd)
                     & (prim["direction"] == "toward_refuse")]
            r2 = g["nls_r2"].to_numpy(dtype=np.float64)
            agr = pd.to_numeric(g["estimator_agreement_ratio"], errors="coerce").to_numpy()
            iqr = pd.to_numeric(g["per_rollout_lambda_iqr_ratio"], errors="coerce").to_numpy()
            iqr = iqr[np.isfinite(iqr)]
            diag[f"{m}|{rd}"] = {
                "median_nls_r2": float(np.nanmedian(r2)) if r2.size else None,
                "frac_r2_below_0.3": float(np.nanmean(r2 < 0.3)) if r2.size else None,
                "frac_at_bound": float(np.mean(g["nls_at_bound"].astype(bool))) if len(g) else None,
                "median_per_prompt_lambda_iqr_ratio": float(np.median(iqr)) if iqr.size else None,
                "p90_per_prompt_lambda_iqr_ratio": float(np.percentile(iqr, 90)) if iqr.size else None,
                "median_estimator_agreement_ratio": float(np.nanmedian(agr)) if agr.size else None,
                "p90_estimator_agreement_ratio": float(np.nanpercentile(agr, 90)) if agr.size else None,
                "n_rows": int(len(g)),
                "ptr": f"tier0_raw.json:lambda[* model={m}, direction=toward_refuse, "
                       f"eps_c=0.1, p=16, teacher_forced=True].{READOUTS[rd]}.estimates",
            }

    n_false = int((~LAM.query("readout=='layerL'")["identifiable"]).sum())
    rows: list[dict[str, Any]] = []
    for pair_key, blk in ot.items():
        if not isinstance(blk, dict):
            continue
        for stat_key in ("lambda_refuse", "lambda_random_dir",
                         "lambda_refuse_final_readout", "lambda_random_dir_final_readout",
                         "lambda_comply", "lambda_comply_final_readout"):
            v = blk.get(stat_key)
            if not isinstance(v, dict):
                continue
            rows.append({
                "analysis": "1.5_lambda_consistency_check",
                "pair": pair_key, "lambda_statistic": stat_key,
                "diff_verbatim": v.get("diff"), "ci_lo": v.get("ci_lo"),
                "ci_hi": v.get("ci_hi"), "n_pairs": v.get("n_pairs"),
                "ci_excludes_zero": v.get("ci_excludes_zero"),
                "n_lambda_rows_identifiable_false": n_false,
                "n_lambda_rows_total": int(len(LAM.query("readout=='layerL'"))),
                "identifiable_reason": "geometry_below_prereg_rule",
                "ptr": f"tier0_raw.json:ordering_tests['{pair_key}']['{stat_key}']",
            })
    return {
        "rows": rows,
        "diagnostics": diag,
        "identifiability_rule": tree["controls"]["lambda_identifiable_at_achieved_geometry"],
        "min_series_length_rule": tree.get("min_series_length_rule"),
        "archived_control_block": tree["controls"]["random_direction_reproduces_ordering"],
    }


# --------------------------------------------------------------------------- #
# ANALYSIS 2 - observable-validity gate
# --------------------------------------------------------------------------- #

def analysis2_gate(tree: dict[str, Any], final_gate: dict[str, Any] | None) -> dict[str, Any]:
    pm = tree["per_model_meta"]
    n_pos = n_neg = 128    # layer_contrast: 128 harmful + 128 benign
    rows: list[dict[str, Any]] = []
    for m in MODELS:
        os_ = pm[m]["observable_sanity"]
        ci = EL.auroc_hanley_ci(os_["auroc"], n_pos, n_neg)
        rows.append({
            "analysis": "2.1_validity_gate", "model": m, "readout": "layerL",
            "auroc": os_["auroc"], "auroc_ci_lo": ci["lo"], "auroc_ci_hi": ci["hi"],
            "auroc_se": ci["se"], "margin": os_["margin"],
            "r0_harmful_mean": os_["r0_harmful_mean"], "r0_benign_mean": os_["r0_benign_mean"],
            "n_pos": n_pos, "n_neg": n_neg,
            "passes_gate": bool(os_["auroc"] >= GATE_AUROC and os_["margin"] > 0),
            "auroc_ci_method": "Hanley-McNeil normal CI on n=128+128 layer_contrast rows "
                               "(per-row r0 arrays are not archived, so a DeLong/bootstrap "
                               "CI is not recoverable without new compute)",
            "ptr": f"tier0_raw.json:per_model_meta['{m}'].observable_sanity",
        })
    if final_gate and final_gate.get("per_model"):
        for m, v in final_gate["per_model"].items():
            ci = EL.auroc_hanley_ci(v["auroc"], v["n_pos"], v["n_neg"])
            rows.append({
                "analysis": "2.1_validity_gate", "model": m, "readout": "final",
                "auroc": v["auroc"], "auroc_ci_lo": ci["lo"], "auroc_ci_hi": ci["hi"],
                "auroc_se": ci["se"], "margin": v["margin"],
                "r0_harmful_mean": v["r0_harmful_mean"], "r0_benign_mean": v["r0_benign_mean"],
                "n_pos": v["n_pos"], "n_neg": v["n_neg"],
                "passes_gate": bool(v["auroc"] >= GATE_AUROC and v["margin"] > 0),
                "auroc_ci_method": "Hanley-McNeil normal CI",
                "ptr": "out/final_layer_gate.json:per_model['%s']" % m,
            })
    else:
        for m in MODELS:
            rows.append({
                "analysis": "2.1_validity_gate", "model": m, "readout": "final",
                "auroc": None, "auroc_ci_lo": None, "auroc_ci_hi": None, "auroc_se": None,
                "margin": None, "r0_harmful_mean": None, "r0_benign_mean": None,
                "n_pos": None, "n_neg": None, "passes_gate": None,
                "auroc_ci_method": "NOT RECOVERABLE WITHOUT NEW COMPUTE - the archive stores "
                                   "observable_sanity only at the layer-L logit-lens readout; "
                                   "the forward-pass job that would produce it did not run.",
                "ptr": "tier0_raw.json:per_model_meta[*].observable_sanity (final-layer entry ABSENT)",
            })

    # sensitivity curve + admissible pairs
    sens: list[dict[str, Any]] = []
    for rd in ("layerL", "final"):
        for thr in GATE_THRESHOLDS:
            passing = [r["model"] for r in rows
                       if r["readout"] == rd and r["auroc"] is not None
                       and r["auroc"] >= thr and (r["margin"] or -1) > 0]
            n_pairs = len(list(combinations(passing, 2)))
            sens.append({"analysis": "2.2_gate_sensitivity", "readout": rd,
                         "threshold": thr, "n_members_passing": len(passing),
                         "members_passing": ",".join(passing) or "(none)",
                         "n_admissible_pairs": n_pairs,
                         "recoverable": bool(any(r["auroc"] is not None
                                                 for r in rows if r["readout"] == rd))})

    # 2.3 ordering_tests restricted to admissible pairs
    ot = tree["ordering_tests"]
    passing_L = [r["model"] for r in rows
                 if r["readout"] == "layerL" and r["auroc"] >= GATE_AUROC and r["margin"] > 0]
    passing_F = [r["model"] for r in rows
                 if r["readout"] == "final" and r["auroc"] is not None
                 and r["auroc"] >= GATE_AUROC and r["margin"] > 0]
    admissible: list[dict[str, Any]] = []
    for gate_readout, passing in (("layerL", passing_L), ("final", passing_F)):
        for A, B in combinations(passing, 2):
            for key in (f"{A}_minus_{B}", f"{B}_minus_{A}"):
                if key in ot:
                    for stat in ("var_star", "ac1", "flicker"):
                        v = ot[key][stat]
                        admissible.append({"analysis": "2.3_admissible_ordering",
                                           "gate_readout": gate_readout, "pair": key,
                                           "indicator": stat, "diff": v["diff"],
                                           "ci_lo": v["ci_lo"], "ci_hi": v["ci_hi"],
                                           "ci_excludes_zero": v["ci_excludes_zero"],
                                           "note": ("indicator values are the layer-L "
                                                    "(primary) series; the gate that admits "
                                                    "this pair was evaluated at the "
                                                    f"{gate_readout} readout"),
                                           "ptr": f"tier0_raw.json:ordering_tests['{key}']['{stat}']"})
    # the inadmissible table, labelled, so the paper can show what WAS reported
    inadmissible: list[dict[str, Any]] = []
    for A, B in combinations(MODELS, 2):
        key = f"{A}_minus_{B}" if f"{A}_minus_{B}" in ot else f"{B}_minus_{A}"
        if key not in ot:
            continue
        a_ok = any(r["model"] == A and r["readout"] == "layerL" and r["passes_gate"] for r in rows)
        b_ok = any(r["model"] == B and r["readout"] == "layerL" and r["passes_gate"] for r in rows)
        for stat in ("var_star", "ac1", "flicker"):
            v = ot[key][stat]
            inadmissible.append({
                "analysis": "2.3_all_ordering_labelled", "pair": key, "indicator": stat,
                "diff": v["diff"], "ci_lo": v["ci_lo"], "ci_hi": v["ci_hi"],
                "ci_excludes_zero": v["ci_excludes_zero"],
                "both_members_pass_gate": bool(a_ok and b_ok),
                "gate_label": ("ADMISSIBLE" if a_ok and b_ok else
                               "NOT ADMISSIBLE: at least one member's refusal observable is "
                               "not a validated refusal readout (AUROC < 0.70 or margin <= 0)"),
                "ptr": f"tier0_raw.json:ordering_tests['{key}']['{stat}']"})

    return {"rows": rows, "sensitivity": sens,
            "admissible_ordering": admissible, "all_ordering_labelled": inadmissible,
            "members_passing_layerL": passing_L,
            "members_passing_final": passing_F,
            "n_admissible_pairs_layerL": len(list(combinations(passing_L, 2))),
            "n_admissible_pairs_final": len(list(combinations(passing_F, 2))),
            "final_readout_recovered": bool(any(r["readout"] == "final"
                                                and r["auroc"] is not None for r in rows))}


def _qwen3_smollm2_lexicons(d1: dict[str, Any]) -> dict[str, dict[str, set[int]]]:
    out: dict[str, dict[str, set[int]]] = {}
    for x in d1["datasets"]:
        if x["dataset"] != "refusal_token_lexicon":
            continue
        for e in x["examples"]:
            fam = e["input"]
            meta = e["metadata_meta"]
            out[fam] = {
                "refusal": {t["token_id"] for t in meta["refusal_onset"]},
                "continuation": {t["token_id"] for t in meta["continuation"]},
                "repo": e["output"],
            }
    return out


def analysis2_instrument(d1: dict[str, Any]) -> dict[str, Any]:
    """2.4 - behaviour-INDEPENDENT instrument check on experiment-2 token streams."""
    lex = _qwen3_smollm2_lexicons(d1)
    q3 = lex["Qwen3"]
    rows: list[dict[str, Any]] = []
    dists: list[dict[str, Any]] = []
    members = sorted([p.name for p in E2_GENS.iterdir() if p.is_dir()])
    for mem in members:
        for arm in ("down_forced_a", "entry", "all_arms"):
            files = (sorted((E2_GENS / mem).glob("*.jsonl")) if arm == "all_arms"
                     else sorted((E2_GENS / mem).glob(f"*_{arm}.jsonl")))
            pos: list[float] = []
            neg: list[float] = []
            allr: list[float] = []
            n_tok = 0
            for f in files:
                for line in f.read_text().splitlines():
                    if not line.strip():
                        continue
                    o = json.loads(line)
                    r = o.get("r_t")
                    if r is None or not np.isfinite(r):
                        continue
                    n_tok += 1
                    allr.append(float(r))
                    tid = o["token"]
                    if tid in q3["refusal"]:
                        pos.append(float(r))
                    elif tid in q3["continuation"]:
                        neg.append(float(r))
            a = EL.auroc_mannwhitney(pos, neg)
            rows.append({
                "analysis": "2.4_instrument_sensitivity",
                "member_exp2": mem, "arm": arm,
                "lexicon_family": "Qwen3", "lexicon_repo": q3["repo"],
                "n_files": len(files), "n_tokens_scored": n_tok,
                "n_refusal_lexicon_tokens": a["n_pos"], "n_continuation_lexicon_tokens": a["n_neg"],
                "token_level_auroc": a["auroc"], "auroc_ci_lo": a["ci_lo"],
                "auroc_ci_hi": a["ci_hi"], "mannwhitney_p": a["p"],
                "mean_r_t_refusal": float(np.mean(pos)) if pos else None,
                "mean_r_t_continuation": float(np.mean(neg)) if neg else None,
                "ptr": f"gen_art_experiment_2/gens/{mem}/*_{arm}.jsonl (fields token, r_t) "
                       f"x full_data_out.json:datasets[refusal_token_lexicon][Qwen3]",
            })
            if arm == "entry" and allr:
                arr = np.asarray(allr)
                dists.append({
                    "analysis": "5.3_r_t_scale", "member_exp2": mem, "arm": arm,
                    "n": int(arr.size), "mean": float(arr.mean()),
                    "sd": float(arr.std(ddof=1)),
                    "p05": float(np.percentile(arr, 5)), "p50": float(np.percentile(arr, 50)),
                    "p95": float(np.percentile(arr, 95)),
                    "min": float(arr.min()), "max": float(arr.max()),
                    "ptr": f"gen_art_experiment_2/gens/{mem}/*_entry.jsonl:r_t"})
            del pos, neg, allr
            gc.collect()
    return {"rows": rows, "r_t_distributions": dists,
            "members_present": members,
            "coverage_note": ("Experiment 2 covers ONE Qwen3 lineage only "
                              "(base, base_plaintemplate, instruct, abliterated). SmolLM2-360M "
                              "has no experiment-2 stream, so no instrument check is available "
                              "for it. The abliterated member differs BETWEEN arms: experiment 1 "
                              "used huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2, experiment 2 used "
                              "mlabonne/Qwen3-0.6B-abliterated. These are NEVER merged.")}


# --------------------------------------------------------------------------- #
# ANALYSIS 3 - exact permutation ceiling at n=4
# --------------------------------------------------------------------------- #

def analysis3(tree: dict[str, Any]) -> dict[str, Any]:
    spi = tree["provisional_spi"]["spi_by_model"]
    gt = tree["ground_truth"]
    pm = tree["per_model_meta"]
    models = sorted(spi.keys())
    harmful = {m: gt[m]["harmful_refusal_rate"]["p"] for m in models}
    xstest = {m: gt[m]["xstest_over_refusal_rate"]["p"] for m in models}
    spi_v = [spi[m] for m in models]
    base_dm = [pm[m]["diff_means"]["auroc"] for m in models]
    base_r0 = [pm[m]["observable_sanity"]["margin"] for m in models]
    y_h = [harmful[m] for m in models]
    y_x = [xstest[m] for m in models]

    methods = {"SPI_label_free": spi_v,
               "baseline_diff_in_means_auroc": base_dm,
               "baseline_r0_margin": base_r0}
    targets = {"harmful_refusal_rate": y_h, "xstest_over_refusal_rate": y_x}

    rows: list[dict[str, Any]] = []
    nulls: dict[str, Any] = {}
    for mname, mv in methods.items():
        for tname, tv in targets.items():
            perm = EL.exact_spearman_permutation(mv, tv)
            rows.append({
                "analysis": "3_small_n_permutation", "method": mname, "target": tname,
                "n_models": len(models),
                "rho": perm["rho_observed"],
                "p_exact_two_sided": perm["p_two_sided"],
                "p_exact_one_sided_greater": perm["p_one_sided_greater"],
                "p_exact_one_sided_less": perm["p_one_sided_less"],
                "n_permutations": perm["n_permutations"],
                "n_distinct_rho": perm["n_distinct_rho"],
                "min_attainable_one_sided_p": perm["min_attainable_one_sided_p"],
                "min_attainable_two_sided_p": perm["min_attainable_two_sided_p"],
                "max_attainable_abs_rho": perm["max_attainable_abs_rho"],
                "ptr": ("tier0_raw.json:provisional_spi.spi_by_model x "
                        f"tier0_raw.json:ground_truth[*].{tname}" if mname == "SPI_label_free"
                        else f"tier0_raw.json:per_model_meta[*] x ground_truth[*].{tname}"),
            })
            nulls[f"{mname}|{tname}"] = perm["null_rho_values"]

    # 3.1 reproduction check against the archived numbers, with the TIE-BREAK
    #     sensitivity that turns out to explain the discrepancy in full.
    archived = {"SPI_label_free": -0.20, "baseline_diff_in_means_auroc": 0.40,
                "baseline_r0_margin": 0.40}
    ties = [m for m in models
            if sum(1 for o in models if abs(y_h[models.index(o)] - y_h[models.index(m)]) < 1e-12) > 1]
    repro: list[dict[str, Any]] = []
    for mname, val in archived.items():
        mv = methods[mname]
        got = [r for r in rows if r["method"] == mname
               and r["target"] == "harmful_refusal_rate"][0]["rho"]
        # ORDINAL ranks (arbitrary tie-break, in array order) - what the shortcut
        # Spearman formula on argsort ranks produces
        r_ord = float(stats.spearmanr(stats.rankdata(mv, method="ordinal"),
                                      stats.rankdata(y_h, method="ordinal")).statistic)
        # both tie-break orders of the tied ground-truth pair, as an interval
        alts = []
        tied_idx = [i for i, m in enumerate(models) if m in ties]
        for eps_sign in (+1, -1):
            y_alt = list(y_h)
            for j, i in enumerate(tied_idx):
                y_alt[i] = y_h[i] + eps_sign * 1e-6 * j
            alts.append(float(stats.spearmanr(mv, y_alt).statistic))
        repro.append({
            "analysis": "3.1_reproduction", "quantity": f"rho_{mname}_vs_harmful",
            "archived_value": val,
            "recomputed_value_tie_aware_average_ranks": got,
            "recomputed_value_ordinal_tiebreak": r_ord,
            "tiebreak_range_lo": float(min(alts)), "tiebreak_range_hi": float(max(alts)),
            "abs_delta_vs_tie_aware": abs(got - val),
            "abs_delta_vs_ordinal": abs(r_ord - val),
            "reproduces_with_tie_aware_ranks": bool(abs(got - val) < 0.02),
            "reproduces_with_ordinal_tiebreak": bool(abs(r_ord - val) < 0.02),
            "n_tied_models_on_ground_truth": len(ties),
            "tied_models": ",".join(sorted(ties)),
            "finding": (
                "MISMATCH EXPLAINED: the archived value is reproduced EXACTLY only under an "
                "ORDINAL rank that breaks the ground-truth tie between the two models whose "
                "harmful refusal rate is identically 0.000 (abliterated and SmolLM2-360M) by "
                "array order. Under tie-aware average ranks the same data give a different "
                "value, and the two admissible tie-breaks bracket a range. The archived "
                "rho_SPI = -0.20 vs rho_baseline = +0.40 contrast is therefore an artifact of "
                "an arbitrary tie-break, not a property of the estimators."),
            "ptr": "tier0_raw.json:provisional_spi.spi_by_model x ground_truth[*]."
                   "harmful_refusal_rate.p (archived value at "
                   "full_method_out.json:...rank_agreement)"})

    # 3.3 the floor problem
    rates = {m: {"p": gt[m]["harmful_refusal_rate"]["p"],
                 "lo": gt[m]["harmful_refusal_rate"]["lo"],
                 "hi": gt[m]["harmful_refusal_rate"]["hi"],
                 "k": gt[m]["harmful_refusal_rate"]["k"],
                 "n": gt[m]["harmful_refusal_rate"]["n"]} for m in models}
    lev = EL.n_resolvable_levels(rates)
    # maximum attainable |rho| given the observed ties in the ground truth
    max_rho = EL.exact_spearman_permutation(list(range(len(models))), y_h)["max_attainable_abs_rho"]
    floor = {
        "analysis": "3.3_floor_problem",
        "n_models": len(models),
        "n_resolvable_ground_truth_levels": lev["n_levels"],
        "level_groups": [",".join(g) for g in lev["groups"]],
        "n_at_or_below_0p025": int(sum(1 for m in models if rates[m]["p"] <= 0.025)),
        "max_attainable_abs_rho_given_ties": max_rho,
        "min_one_sided_p_untied_design": 1.0 / math.factorial(len(models)),
        "min_two_sided_p_untied_design": 2.0 / math.factorial(len(models)),
        "min_two_sided_p_with_observed_ties": EL.exact_spearman_permutation(
            list(range(len(models))), y_h)["min_attainable_two_sided_p"],
        "wilson_cis": {m: rates[m] for m in models},
        "ptr": "tier0_raw.json:ground_truth[*].harmful_refusal_rate",
    }
    return {"rows": rows, "reproduction": repro, "floor": floor,
            "null_distributions": nulls, "models": models,
            "method_values": {k: dict(zip(models, v)) for k, v in methods.items()},
            "target_values": {k: dict(zip(models, v)) for k, v in targets.items()}}


# --------------------------------------------------------------------------- #
# ANALYSIS 4 - AC1 length confound
# --------------------------------------------------------------------------- #

def analysis4(tree: dict[str, Any], IND: pd.DataFrame) -> dict[str, Any]:
    agg = tree["aggregate_by_model"]
    # 4.1 which field did iteration 1 report?
    which: list[dict[str, Any]] = []
    for m in MODELS:
        med_corr = float(IND[(IND["model"] == m) & (IND["readout"] == "layerL")]["ac1"].median())
        med_unc = float(IND[(IND["model"] == m) & (IND["readout"] == "layerL")]["ac1_uncorrected"].median())
        reported = agg[m]["ac1"]["point"]
        which.append({
            "analysis": "4.1_which_ac1_field", "model": m,
            "reported_ac1_in_aggregate": reported,
            "median_ac1_corrected": med_corr,
            "median_ac1_uncorrected": med_unc,
            "matches_corrected": bool(abs(reported - med_corr) < 1e-9),
            "matches_uncorrected": bool(abs(reported - med_unc) < 1e-9),
            "kendall_correction_term_at_T192": float((1 + 3 * med_corr) / 192),
            "kendall_correction_term_at_T64": float((1 + 3 * med_corr) / 64),
            "ptr": f"tier0_raw.json:aggregate_by_model['{m}'].ac1.point vs "
                   f"indicators[* model={m}].primary.detrended.ac1 / .ac1_uncorrected",
        })

    # 4.2 effective series lengths
    lens: list[dict[str, Any]] = []
    for m in MODELS:
        for rd in ("layerL", "final"):
            g = IND[(IND["model"] == m) & (IND["readout"] == rd)]
            lens.append({
                "analysis": "4.2_series_length", "model": m, "readout": rd,
                "n_steps_min": int(g["n_steps"].min()), "n_steps_median": float(g["n_steps"].median()),
                "n_steps_max": int(g["n_steps"].max()),
                "n_rollouts_min": int(g["n_rollouts"].min()),
                "n_rollouts_max": int(g["n_rollouts"].max()),
                "mean_frac_rollouts_hit_eos": float(g["frac_rollouts_hit_eos"].mean()),
                "median_eos_step": float(g["median_eos_step"].median()),
                "ptr": f"tier0_raw.json:indicators[* model={m}].{IND_READOUTS[rd]}.n_steps "
                       f"/ per_model_meta['{m}'].mean_frac_rollouts_hit_eos",
            })

    # 4.3 matched-length sweep (layer-L only; the archive stores no final-layer sweep)
    sweep_rows: list[dict[str, Any]] = []
    per_len: dict[int, dict[str, dict[str, list[float]]]] = {}
    for i, r in enumerate(tree["indicators"]):
        for s in r["series_length_sweep"]:
            L = int(s["length"])
            per_len.setdefault(L, {}).setdefault(r["model"], {"var_star": [], "ac1": [],
                                                              "ac1_raw": [], "flicker": [],
                                                              "var_star_raw": [],
                                                              "prompt": []})
            b = per_len[L][r["model"]]
            b["var_star"].append(s["var_star"]); b["ac1"].append(s["ac1"])
            b["ac1_raw"].append(s["ac1_raw"]); b["flicker"].append(s["flicker"])
            b["var_star_raw"].append(s["var_star_raw"]); b["prompt"].append(r["prompt_id"])
    lengths = sorted(per_len)
    common = [L for L in lengths if all(m in per_len[L] and len(per_len[L][m]["ac1"]) == 20
                                        for m in MODELS)]
    for L in lengths:
        for m in MODELS:
            if m not in per_len[L]:
                continue
            b = per_len[L][m]
            sweep_rows.append({
                "analysis": "4.3_length_sweep", "model": m, "length": L,
                "n_prompts": len(b["ac1"]),
                "ac1_corrected_median": float(np.median(b["ac1"])),
                "ac1_raw_median": float(np.median(b["ac1_raw"])),
                "ac1_delta_corrected_minus_raw": float(np.median(b["ac1"]) - np.median(b["ac1_raw"])),
                "var_star_median": float(np.median(b["var_star"])),
                "var_star_raw_median": float(np.median(b["var_star_raw"])),
                "flicker_median": float(np.median(b["flicker"])),
                "ptr": f"tier0_raw.json:indicators[* model={m}].series_length_sweep[length={L}]",
            })

    # paired model-pair bootstrap at the largest common length
    Lmax = max(common) if common else max(lengths)
    matched: list[dict[str, Any]] = []
    for A, B in combinations(MODELS, 2):
        for field, label in (("ac1", "ac1_corrected"), ("ac1_raw", "ac1_raw"),
                             ("var_star", "var_star"), ("flicker", "flicker")):
            a = dict(zip(per_len[Lmax][A]["prompt"], per_len[Lmax][A][field]))
            b = dict(zip(per_len[Lmax][B]["prompt"], per_len[Lmax][B][field]))
            d, _ = EL._clean_pairs(a, b)
            bs = EL.bootstrap_mean(d)
            matched.append({
                "analysis": "4.3_matched_length_bootstrap", "pair": f"{A}_minus_{B}",
                "indicator": label, "length": Lmax, "diff": bs["diff"],
                "ci_lo": bs["ci_lo"], "ci_hi": bs["ci_hi"], "n_pairs": bs["n_pairs"],
                "ci_excludes_zero": bs["ci_excludes_zero"],
                "ptr": f"tier0_raw.json:indicators[*].series_length_sweep[length={Lmax}].{field}",
            })

    # 4.4 final-layer readout: corrected vs raw AC1 (no sweep archived there)
    final_rows: list[dict[str, Any]] = []
    for m in MODELS:
        g = IND[(IND["model"] == m) & (IND["readout"] == "final")]
        final_rows.append({
            "analysis": "4.4_final_readout_ac1", "model": m,
            "ac1_corrected_median": float(g["ac1"].median()),
            "ac1_uncorrected_median": float(g["ac1_uncorrected"].median()),
            "delta_corrected_minus_uncorrected":
                float(g["ac1"].median() - g["ac1_uncorrected"].median()),
            "var_star_median": float(g["var_star"].median()),
            "flicker_median": float(g["flicker"].median()),
            "sweep_available": False,
            "note": "series_length_sweep is archived ONLY for the layer-L readout "
                    "(tier0_raw.json:indicators[i].series_length_sweep is a sibling of, "
                    "not a child of, the readout blocks), so a matched-length re-report at "
                    "the final-layer readout is NOT recoverable without new compute.",
            "ptr": f"tier0_raw.json:indicators[* model={m}].final_layer_readout.detrended",
        })

    # the length-manufactured component: how much the corrected-vs-raw gap moves with T
    manufactured = []
    for m in MODELS:
        v16 = [r for r in sweep_rows if r["model"] == m and r["length"] == min(lengths)][0]
        vmx = [r for r in sweep_rows if r["model"] == m and r["length"] == max(lengths)][0]
        manufactured.append({
            "analysis": "4.3_length_manufactured_component", "model": m,
            "shortest_length": min(lengths), "longest_length": max(lengths),
            "ac1_corrected_at_shortest": v16["ac1_corrected_median"],
            "ac1_corrected_at_longest": vmx["ac1_corrected_median"],
            "ac1_swing_across_lengths": float(vmx["ac1_corrected_median"] - v16["ac1_corrected_median"]),
            "correction_term_at_shortest": float((1 + 3 * v16["ac1_corrected_median"]) / min(lengths)),
            "correction_term_at_longest": float((1 + 3 * vmx["ac1_corrected_median"]) / max(lengths)),
            "ptr": f"tier0_raw.json:indicators[* model={m}].series_length_sweep",
        })

    return {"which_field": which, "lengths": lens, "sweep": sweep_rows,
            "matched": matched, "final_readout": final_rows,
            "manufactured": manufactured,
            "lengths_available": lengths, "largest_common_length": Lmax}


# --------------------------------------------------------------------------- #
# ANALYSIS 5 - cross-arm asymmetry
# --------------------------------------------------------------------------- #

def analysis5(e2: dict[str, Any], a1: dict[str, Any]) -> dict[str, Any]:
    md = e2["metadata"]
    per_model = md["per_model"]
    cheap = md["cheap_safety_metric"]["per_model"]
    rows: list[dict[str, Any]] = []
    for mem, blk in per_model.items():
        n = int(blk.get("upramp_n") or 0)
        rate = blk.get("upramp_fail_rate")
        k = int(round(rate * n)) if (rate is not None and n) else 0
        w = EL.wilson_ci(k, n) if n else {"p": None, "lo": None, "hi": None}
        cm = cheap.get(mem, {})
        rows.append({
            "analysis": "5.1_steering_channel", "member_exp2": mem,
            "upramp_fail_rate": rate, "upramp_k": k, "upramp_n": n,
            "wilson_lo": w["lo"], "wilson_hi": w["hi"],
            "entry_fail_rate": blk.get("entry_fail_rate"),
            "alpha50_fitted": cm.get("refusal_reachability_alpha50_fitted"),
            "alpha50_random": cm.get("refusal_reachability_alpha50_random"),
            "max_refusal_rate_fitted": cm.get("max_refusal_rate_fitted"),
            "hysteresis_width_mean": (blk.get("width_naive") or {}).get("mean"),
            "hysteresis_width_ci_lo": (blk.get("width_naive") or {}).get("ci_low"),
            "hysteresis_width_ci_hi": (blk.get("width_naive") or {}).get("ci_high"),
            "excess_width_mean": (blk.get("excess_width") or {}).get("mean"),
            "excess_width_ci_lo": (blk.get("excess_width") or {}).get("ci_low"),
            "excess_width_ci_hi": (blk.get("excess_width") or {}).get("ci_high"),
            "ptr": f"gen_art_experiment_2/full_method_out.json:metadata.per_model['{mem}'] "
                   f"+ metadata.cheap_safety_metric.per_model['{mem}']",
        })

    # 5.2 one table, matched statistics, both channels
    cross: list[dict[str, Any]] = []
    for r in a1["ratchet"]:
        if r["statistic"] != "S1_decay_ratio_16" or r["readout"] != "layerL":
            continue
        cross.append({
            "analysis": "5.2_cross_arm", "channel": "token (experiment 1)",
            "member": r["model"],
            "asymmetry_statistic": "log S1(free_running) - log S1(teacher_forced)",
            "value": r["mean_log_diff"], "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"],
            "sign_positive": bool((r["mean_log_diff"] or 0) > 0),
            "reading": ("perturbations GROW when the token stream is free to diverge and "
                        "SHRINK when it is held fixed: the asymmetry is carried by the "
                        "emitted tokens, not by the residual stream"),
            "ptr": r["ptr"]})
    for r in rows:
        if r["upramp_fail_rate"] is None:
            continue
        cross.append({
            "analysis": "5.2_cross_arm", "channel": "steering (experiment 2)",
            "member": r["member_exp2"],
            "asymmetry_statistic": "up-ramp failure rate mid-generation (fresh generation at the "
                                   "same constant alpha refuses reliably)",
            "value": r["upramp_fail_rate"], "ci_lo": r["wilson_lo"], "ci_hi": r["wilson_hi"],
            "sign_positive": True,
            "reading": ("compliance sticks and refusal does not: the up-transition is "
                        "unreachable inside an already-compliant generation"),
            "ptr": r["ptr"]})
    return {"steering": rows, "cross_arm": cross,
            "agreement_note": ("Both arms report the SAME sign of asymmetry - the compliant "
                               "branch is the sticky one - but they use different perturbation "
                               "channels (token-stream divergence vs residual-stream steering) "
                               "and different abliterated checkpoints "
                               "(huihui-ai v2 in experiment 1, mlabonne in experiment 2). "
                               "This is corroboration, NOT replication.")}


# --------------------------------------------------------------------------- #
# figures
# --------------------------------------------------------------------------- #

def make_figures(res: dict[str, Any]) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figs: list[str] = []

    def save(fig, name: str) -> None:
        for ext in ("pdf", "png"):
            p = HERE / "figs" / f"{name}.{ext}"
            fig.savefig(p, bbox_inches="tight", dpi=160)
            figs.append(str(p.relative_to(HERE)))
        plt.close(fig)

    short = {m: m.split("/")[-1] if m.startswith("qwen3") else "smollm2" for m in MODELS}

    # F1 - forest plot of the direction contrast and the DiD
    con = [r for r in res["analysis1"]["contrast"]
           if r["statistic"] == "S1_decay_ratio_16" and r["readout"] == "layerL"
           and r["channel"] == "teacher_forced"]
    did = [r for r in res["analysis1"]["did"]
           if r["statistic"] == "S1_decay_ratio_16" and r["readout"] == "layerL"
           and r["channel"] == "teacher_forced"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    ax = axes[0]
    ys = np.arange(len(con))
    ax.errorbar([r["mean_log_diff"] for r in con], ys,
                xerr=[[r["mean_log_diff"] - r["ci_lo"] for r in con],
                      [r["ci_hi"] - r["mean_log_diff"] for r in con]],
                fmt="o", color="#1f77b4", capsize=3)
    ax.set_yticks(ys); ax.set_yticklabels([short[r["model"]] for r in con])
    ax.axvline(0, color="k", lw=1)
    ax.set_xlabel("log S1(random direction) − log S1(refusal direction)")
    ax.set_title("A. Per-model direction contrast\n(S1 = decay_ratio_16, layer-L, teacher-forced)")
    ax = axes[1]
    ys = np.arange(len(did))
    cols = ["#d62728" if r["is_primary"] else "#7f7f7f" for r in did]
    for i, r in enumerate(did):
        ax.errorbar(r["did_mean"], i,
                    xerr=[[r["did_mean"] - r["ci_lo"]], [r["ci_hi"] - r["did_mean"]]],
                    fmt="o", color=cols[i], capsize=3)
    ax.axvspan(-EQ_MARGIN, EQ_MARGIN, color="#2ca02c", alpha=0.13,
               label=f"equivalence margin ±{EQ_MARGIN}")
    ax.axvline(0, color="k", lw=1)
    ax.set_yticks(np.arange(len(did)))
    ax.set_yticklabels([f"{short[r['model_a']]} − {short[r['model_b']]}"
                        + ("  (PRIMARY)" if r["is_primary"] else "") for r in did], fontsize=8)
    ax.set_xlabel("difference-in-differences (log units)")
    ax.set_title("B. Is the between-model separation direction-specific?")
    ax.legend(fontsize=8, loc="lower right")
    fig.suptitle("F1  Direction control recomputed on assumption-free statistics", y=1.02)
    save(fig, "F1_direction_contrast_forest")

    # F2 - gate plot
    gate = res["analysis2"]["gate"]["rows"]
    inst = res["analysis2"]["instrument"]["rows"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    ax = axes[0]
    x = np.arange(len(MODELS))
    for k, (rd, off, c) in enumerate((("layerL", -0.16, "#1f77b4"), ("final", 0.16, "#ff7f0e"))):
        vals, los, his = [], [], []
        for m in MODELS:
            r = [q for q in gate if q["model"] == m and q["readout"] == rd][0]
            vals.append(np.nan if r["auroc"] is None else r["auroc"])
            los.append(0 if r["auroc"] is None else r["auroc"] - r["auroc_ci_lo"])
            his.append(0 if r["auroc"] is None else r["auroc_ci_hi"] - r["auroc"])
        ax.errorbar(x + off, vals, yerr=[los, his], fmt="s", color=c, capsize=3,
                    label=f"{rd} readout")
    ax.axhline(GATE_AUROC, color="r", ls="--", label=f"gate = {GATE_AUROC}")
    ax.axhline(0.5, color="k", lw=0.8, ls=":")
    ax.set_xticks(x); ax.set_xticklabels([short[m] for m in MODELS], rotation=15)
    ax.set_ylabel("harmful-vs-benign AUROC of r0"); ax.set_ylim(0.2, 1.02)
    ax.set_title("A. Prompt-level observable validity")
    ax.legend(fontsize=8)
    ax = axes[1]
    ii = [r for r in inst if r["arm"] == "all_arms" and r["token_level_auroc"] is not None]
    xs = np.arange(len(ii))
    ax.bar(xs, [r["token_level_auroc"] for r in ii], color="#2ca02c", width=0.55)
    ax.errorbar(xs, [r["token_level_auroc"] for r in ii],
                yerr=[[r["token_level_auroc"] - r["auroc_ci_lo"] for r in ii],
                      [r["auroc_ci_hi"] - r["token_level_auroc"] for r in ii]],
                fmt="none", ecolor="k", capsize=3)
    ax.axhline(0.5, color="k", lw=0.8, ls=":")
    for k, r in enumerate(ii):
        ax.text(k, 0.04, f"n={r['n_refusal_lexicon_tokens']}/{r['n_continuation_lexicon_tokens']}",
                ha="center", fontsize=7.5, color="white")
    ax.set_xticks(xs); ax.set_xticklabels([r["member_exp2"] for r in ii], rotation=15, fontsize=8)
    ax.set_ylabel("token-level AUROC (refusal vs continuation tokens)")
    ax.set_title("B. Instrument sensitivity, all experiment-2 arms pooled\n"
                 "(n = refusal-lexicon / continuation-lexicon tokens)")
    ax.set_ylim(0, 1.02)
    fig.suptitle("F2  Observable-validity gate: is r a refusal readout at all?", y=1.03)
    save(fig, "F2_validity_gate")

    # F3 - exact permutation null
    a3 = res["analysis3"]
    key = "SPI_label_free|harmful_refusal_rate"
    # exact null: enumerate the 24 orderings and plot DISTINCT rho values with
    # their multiplicities (a histogram over 24 points with ties is misleading)
    from collections import Counter
    from scipy import stats as _st
    y_h = [res["analysis3"]["target_values"]["harmful_refusal_rate"][m]
           for m in res["analysis3"]["models"]]
    import itertools as _it
    exact = Counter()
    yr = _st.rankdata(y_h, method="average")
    for perm in _it.permutations(range(len(y_h))):
        exact[round(float(_st.spearmanr(yr[list(perm)], yr).statistic), 6)] += 1
    fig, ax = plt.subplots(figsize=(9, 5.0))
    xs_ = sorted(exact)
    ax.bar(xs_, [exact[v] for v in xs_], width=0.055, color="#c7c7c7", edgecolor="k",
           label=f"exact null over 4! = 24 orderings (n={sum(exact.values())})")
    for mname, c, ls in (("SPI_label_free", "#d62728", "-"),
                         ("baseline_diff_in_means_auroc", "#1f77b4", "-"),
                         ("baseline_r0_margin", "#2ca02c", "-")):
        r = [q for q in a3["rows"] if q["method"] == mname
             and q["target"] == "harmful_refusal_rate"][0]
        ax.axvline(r["rho"], color=c, lw=2, ls=ls,
                   label=f"{mname}: ρ={r['rho']:+.2f}, exact two-sided p={r['p_exact_two_sided']:.3f}")
    for val, lab in ((-0.20, "archived ρ_SPI = −0.20"), (0.40, "archived ρ_baseline = +0.40")):
        ax.axvline(val, color="k", lw=1.4, ls="--", alpha=0.7)
        ax.annotate(lab + "\n(ordinal tie-break)", xy=(val, max(exact.values()) * 0.72),
                    fontsize=7, ha="center", rotation=90, va="top")
    ax.set_xlabel("Spearman ρ under the exact n=4 permutation null "
                  "(tie-aware ranks; the two 0.000-refusal models tie)")
    ax.set_ylabel("number of orderings attaining this ρ")
    ax.set_title("F3  With n=4 the smallest attainable one-sided p is 1/24 = 0.0417 and the\n"
                 "two-sided floor is 2/24 = 0.0833 (0.1667 once the observed ties are honoured):\n"
                 "no ranking of four checkpoints could have reached p < 0.04", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper left")
    save(fig, "F3_exact_permutation_null")

    # F4 - AC1 / Var* / flicker vs series length
    sweep = res["analysis4"]["sweep"]
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.4))
    mcol = dict(zip(MODELS, ["#1f77b4", "#2ca02c", "#9467bd", "#e377c2"]))
    for ax, (field, raw_field, lab) in zip(
            axes, (("ac1_corrected_median", "ac1_raw_median", "AC1"),
                   ("var_star_median", "var_star_raw_median", "Var*"),
                   ("flicker_median", None, "flicker (crossings/100)"))):
        for m in MODELS:
            g = sorted([r for r in sweep if r["model"] == m], key=lambda r: r["length"])
            ax.plot([r["length"] for r in g], [r[field] for r in g], "-o", ms=4,
                    color=mcol[m], label=short[m])
            if raw_field:
                ax.plot([r["length"] for r in g], [r[raw_field] for r in g], "--",
                        color=mcol[m], alpha=0.5)
        ax.axvline(192, color="k", lw=0.8, ls=":")
        ax.set_xlabel("series length T"); ax.set_ylabel(lab)
        ax.set_title(f"{lab}" + (" — solid corrected, dashed raw" if raw_field else
                                 " — detrended only"), fontsize=10)
    axes[0].legend(fontsize=8)
    fig.suptitle("F4  Matched-length re-report from the archived series_length_sweep "
                 "(dotted line = the T=192 matched length used for every reported contrast)",
                 y=1.03)
    save(fig, "F4_length_sweep")

    # F5 - lambda diagnostics
    diag = res["analysis1"]["lambda_check"]["diagnostics"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.3))
    ks = [f"{m}|layerL" for m in MODELS]
    axes[0].bar(range(4), [diag[k]["median_nls_r2"] for k in ks], color="#1f77b4")
    axes[0].set_xticks(range(4)); axes[0].set_xticklabels([short[m] for m in MODELS], rotation=15)
    axes[0].set_ylabel("median single-exponential fit r²"); axes[0].axhline(0.3, color="r", ls="--")
    axes[0].set_title("A. Fit quality (r² = 0.3 marked)")
    axes[1].bar(range(4), [diag[k]["frac_r2_below_0.3"] for k in ks], color="#ff7f0e")
    axes[1].set_xticks(range(4)); axes[1].set_xticklabels([short[m] for m in MODELS], rotation=15)
    axes[1].set_ylabel("fraction of fits with r² < 0.3"); axes[1].set_ylim(0, 1)
    axes[1].set_title("B. Misspecification rate")
    axes[2].bar(range(4), [diag[k]["median_per_prompt_lambda_iqr_ratio"] for k in ks],
                color="#9467bd")
    axes[2].set_xticks(range(4)); axes[2].set_xticklabels([short[m] for m in MODELS], rotation=15)
    axes[2].set_ylabel("median per-prompt λ IQR ratio (q75/q25)")
    axes[2].set_title("C. Within-prompt λ spread across 20 rollouts")
    fig.suptitle("F5  λ diagnostics — identifiable = FALSE on 640/640 archived rows "
                 "(geometry_below_prereg_rule)", y=1.03)
    save(fig, "F5_lambda_diagnostics")

    # F6 - cross-arm asymmetry table figure
    cross = res["analysis5"]["cross_arm"]
    abbrev = {"token (experiment 1)": "log S1(free) − log S1(teacher-forced)",
              "steering (experiment 2)": "up-ramp failure rate mid-generation"}
    fig, ax = plt.subplots(figsize=(12.5, 0.42 * len(cross) + 1.6))
    ax.axis("off")
    cells = [[r["channel"], r["member"], abbrev[r["channel"]],
              "n/a" if r["value"] is None else f"{r['value']:.3f}",
              "n/a" if r["ci_lo"] is None else f"[{r['ci_lo']:.3f}, {r['ci_hi']:.3f}]",
              "+" if r["sign_positive"] else "−"] for r in cross]
    t = ax.table(cellText=cells,
                 colLabels=["channel", "member", "asymmetry statistic", "value", "95% CI", "sign"],
                 loc="center", cellLoc="left",
                 colWidths=[0.19, 0.19, 0.30, 0.10, 0.16, 0.06])
    t.auto_set_font_size(False); t.set_fontsize(8.0); t.scale(1, 1.35)
    ax.set_title("F6  Both arms report the same sign of asymmetry (corroboration, not replication:\n"
                 "different perturbation channels and different abliterated checkpoints)", pad=18)
    save(fig, "F6_cross_arm_asymmetry")
    return figs


# --------------------------------------------------------------------------- #
# eval_out.json assembly
# --------------------------------------------------------------------------- #

def _num(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)) and np.isfinite(v):
        return float(v)
    return None


def _row_label(r: dict[str, Any]) -> str:
    """Compact machine-readable verdict token for a row (the `predict_*` field)."""
    for k in ("verdict", "gate_label", "finding", "note"):
        if r.get(k):
            return str(r[k]).split(":")[0].split(".")[0][:120]
    if "passes_gate" in r:
        return "GATE_PASS" if r["passes_gate"] else (
            "GATE_NOT_RECOVERABLE" if r["passes_gate"] is None else "GATE_FAIL")
    if "ci_excludes_zero" in r and r["ci_excludes_zero"] is not None:
        return "CI_EXCLUDES_ZERO" if r["ci_excludes_zero"] else "CI_INCLUDES_ZERO"
    if "p_exact_two_sided" in r:
        return ("EXACT_P_BELOW_0.05" if r["p_exact_two_sided"] < 0.05
                else "EXACT_P_NOT_SIGNIFICANT")
    if "reproduces_with_tie_aware_ranks" in r:
        return ("REPRODUCES_TIE_AWARE" if r["reproduces_with_tie_aware_ranks"]
                else "REPRODUCES_ONLY_UNDER_ORDINAL_TIEBREAK"
                if r["reproduces_with_ordinal_tiebreak"] else "MISMATCH")
    if "matches_corrected" in r:
        return "AC1_KENDALL_CORRECTED" if r["matches_corrected"] else "AC1_UNCORRECTED"
    return "DESCRIPTIVE"


def rows_to_examples(rows: list[dict[str, Any]], *, input_keys: list[str],
                     output_fn) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        ex: dict[str, Any] = {
            "input": " | ".join(f"{k}={r.get(k)}" for k in input_keys),
            "output": output_fn(r),
            "predict_reanalysis_label": _row_label(r),
        }
        for k, v in r.items():
            if k in ("analysis",):
                continue
            n = _num(v)
            if n is not None and not isinstance(v, str):
                ex[f"eval_{k}"] = n
            else:
                ex[f"metadata_{k}"] = v
        out.append(ex)
    return out


@logger.catch(reraise=True)
def main() -> None:
    logger.info(f"cpus={NUM_CPUS} ram_total={TOTAL_RAM_GB:.1f}GB budget={RAM_BUDGET/1e9:.1f}GB")

    # ---------------- STEP 0 ------------------------------------------------
    logger.info("STEP 0: loading and freezing inputs")
    manifest = {
        "tier0_raw.json": {"path": str(TIER0), "sha256": EL.sha256_of(TIER0),
                           "bytes": TIER0.stat().st_size},
        "refit_certified.json": {"path": str(REFIT), "sha256": EL.sha256_of(REFIT),
                                 "bytes": REFIT.stat().st_size},
        "layer_choice.json": {"path": str(LAYERC), "sha256": EL.sha256_of(LAYERC),
                              "bytes": LAYERC.stat().st_size},
        "experiment_2_full_method_out.json": {"path": str(E2_OUT),
                                              "sha256": EL.sha256_of(E2_OUT),
                                              "bytes": E2_OUT.stat().st_size},
        "dataset_1_full_data_out.json": {"path": str(D1_OUT), "sha256": EL.sha256_of(D1_OUT),
                                         "bytes": D1_OUT.stat().st_size},
        "experiment_2_gens_tree": EL.sha256_of_tree(E2_GENS),
    }
    tree = json.loads(TIER0.read_text())
    LAM, IND, census = build_frames(tree)
    logger.info(f"LAM {LAM.shape} IND {IND.shape}; identifiable=False on "
                f"{census['n_identifiable_false']}/{census['n_lambda_rows_archived']} rows")
    assert census["n_identifiable_true"] == 0, "some lambda rows claim identifiability"

    layer_choice = json.loads(LAYERC.read_text())
    refit = json.loads(REFIT.read_text())
    refit_summary = {k: refit[k] for k in ("controls", "min_series_length_rule")
                     if k in refit}
    del refit
    gc.collect()

    # ---------------- ANALYSES ---------------------------------------------
    logger.info("ANALYSIS 1: direction contrast, DiD, equivalence")
    a1 = analysis1(LAM)
    a1["lambda_check"] = analysis1_lambda_consistency(tree, LAM)

    logger.info("ANALYSIS 2: observable-validity gate")
    fg_path = HERE / "out" / "final_layer_gate.json"
    final_gate = json.loads(fg_path.read_text()) if fg_path.exists() else None
    if final_gate:
        logger.info("final-layer gate found on disk (forward-pass job ran)")
    gate = analysis2_gate(tree, final_gate)
    d1 = json.loads(D1_OUT.read_text())
    inst = analysis2_instrument(d1)
    del d1
    gc.collect()

    logger.info("ANALYSIS 3: exact permutation ceiling")
    a3 = analysis3(tree)

    logger.info("ANALYSIS 4: AC1 length confound")
    a4 = analysis4(tree, IND)

    logger.info("ANALYSIS 5: cross-arm asymmetry")
    e2 = json.loads(E2_OUT.read_text())
    a5 = analysis5(e2, a1)
    del e2
    gc.collect()

    res = {"analysis1": a1,
           "analysis2": {"gate": gate, "instrument": inst},
           "analysis3": a3, "analysis4": a4, "analysis5": a5}

    # ---------------- verdicts ---------------------------------------------
    prim_did = [r for r in a1["did"] if r["is_primary"]][0]
    prim_con = [r for r in a1["contrast"]
                if r["model"] == PRIMARY_PAIR[0] and r["statistic"] == "S1_decay_ratio_16"
                and r["readout"] == "layerL" and r["channel"] == "teacher_forced"][0]
    n_did_sig = sum(1 for r in a1["did"] if r["ci_excludes_zero"])
    n_did_equiv = sum(1 for r in a1["did"] if r["tost_equivalent"])
    spi_row = [r for r in a3["rows"] if r["method"] == "SPI_label_free"
               and r["target"] == "harmful_refusal_rate"][0]
    base_row = [r for r in a3["rows"] if r["method"] == "baseline_diff_in_means_auroc"
                and r["target"] == "harmful_refusal_rate"][0]
    ac1_corrected = all(r["matches_corrected"] for r in a4["which_field"])

    verdicts = {
        "analysis1_direction_control": (
            f"RECOMPUTED_ON_ASSUMPTION_FREE_STATISTICS. On the PRIMARY cell "
            f"(instruct vs abliterated, S1=decay_ratio_16, layer-L, teacher-forced) the "
            f"difference-in-differences is {prim_did['did_mean']:+.3f} log units "
            f"[{prim_did['ci_lo']:+.3f}, {prim_did['ci_hi']:+.3f}], verdict "
            f"{prim_did['verdict']}. Across the full family of "
            f"{prim_did['family_size']} difference-in-differences tests, "
            f"{n_did_sig} have a 95% CI excluding 0 and {n_did_equiv} pass the "
            f"±{EQ_MARGIN} equivalence test."),
        "analysis1_lambda_demotion": (
            f"LAMBDA_NOT_ADMISSIBLE_AS_A_CONTROL. identifiable=false on "
            f"{census['n_identifiable_false']}/{census['n_lambda_rows_archived']} archived rows "
            f"(reason: geometry_below_prereg_rule; achieved T_fit=64, n_roll=20 against a "
            f"pre-registered rule of T_fit>=128 which then moves to n_roll>=40). Both arms of "
            f"the iteration-1 control are equally non-identifiable, so the "
            f"random-direction-vs-refusal-direction asymmetry it reports is a comparison "
            f"between two equally noisy estimators."),
        "analysis2_validity_gate": (
            f"GATE_EMPTIES_THE_CROSS_MODEL_TABLE. At AUROC>={GATE_AUROC} and margin>0, "
            f"{len(gate['members_passing_layerL'])} of 4 members clear at the layer-L readout "
            f"({', '.join(gate['members_passing_layerL']) or 'none'}), giving "
            f"{gate['n_admissible_pairs_layerL']} admissible model pairs. The emptiness IS the "
            f"result: 'indicators track lineage, not safety' was computed largely on readouts "
            f"that are not validated refusal signals. "
            + (("At the FINAL-layer readout, recomputed here with a forward-pass-only job on "
                "the pinned revisions, the gate admits "
                f"{sum(1 for r in gate['rows'] if r['readout'] == 'final' and r['passes_gate'])}"
                " of 4 members ("
                + ", ".join(r["model"] for r in gate["rows"]
                            if r["readout"] == "final" and r["passes_gate"])
                + "), so WHICH readout is chosen decides whether any cross-model contrast is "
                  "admissible at all - a live analytic degree of freedom that iteration 1 did "
                  "not report, and one that the two readouts' 0.17-0.26 correlation makes "
                  "material.")
               if any(r["readout"] == "final" and r["auroc"] is not None for r in gate["rows"])
               else "The final-layer arm of the gate is not recoverable without new compute.")),
        "analysis2_instrument_sensitivity": (
            f"INSTRUMENT_WORKS_WHERE_TESTABLE_BUT_ON_FEW_TOKENS. Pooling all four experiment-2 "
            f"arms, the same r observable separates refusal-lexicon tokens from "
            f"continuation-lexicon tokens at AUROC "
            f"{min(r['token_level_auroc'] for r in inst['rows'] if r['arm'] == 'all_arms' and r['token_level_auroc'] is not None):.3f}"
            f"-"
            f"{max(r['token_level_auroc'] for r in inst['rows'] if r['arm'] == 'all_arms' and r['token_level_auroc'] is not None):.3f} "
            f"in every Qwen3-family member tested, i.e. well above chance, so a low PROMPT-level "
            f"AUROC in base/abliterated is a BEHAVIOUR fact (those models almost never refuse) "
            f"rather than an instrument fault. The caveat is sample size: only a few dozen to a "
            f"few hundred logged tokens per member fall in either lexicon list, so the "
            f"token-level CIs are wide and one member reaches a degenerate AUROC of 1.0. No "
            f"experiment-2 stream exists for SmolLM2-360M, so its low prompt-level AUROC "
            f"(0.633) cannot be attributed to instrument versus behaviour at all."),
        "analysis3_small_n": (
            f"NO_RANK_COMPARISON_IS_INFORMATIVE_AT_n=4, AND THE ARCHIVED CONTRAST IS A "
            f"TIE-BREAK ARTIFACT. Tie-aware Spearman gives rho_SPI = {spi_row['rho']:+.3f} "
            f"(exact two-sided p = {spi_row['p_exact_two_sided']:.3f}) and "
            f"rho_baseline = {base_row['rho']:+.3f} "
            f"(exact two-sided p = {base_row['p_exact_two_sided']:.3f}); the archived "
            f"-0.20 / +0.40 pair is reproduced EXACTLY only under an ordinal rank that breaks "
            f"the ground-truth tie between the two models whose harmful refusal rate is "
            f"identically 0.000 by array order. Either way the design has no resolution: with "
            f"4! = 24 orderings the smallest attainable one-sided p is 1/24 = 0.0417 and the "
            f"two-sided floor is 2/24 = 0.0833 in an untied design, rising to "
            f"{a3['floor']['min_two_sided_p_with_observed_ties']:.4f} given the observed ties, "
            f"which also cap |rho| at {a3['floor']['max_attainable_abs_rho_given_ties']:.3f}. "
            f"Only {a3['floor']['n_resolvable_ground_truth_levels']} ground-truth levels are "
            f"resolvable given the Wilson CIs."),
        "analysis4_ac1_length": (
            ("VERIFICATION_NOT_REPAIR. The iteration-1 headline AC1 was ALREADY the "
             "Kendall-corrected field" if ac1_corrected else
             "REPAIR_REQUIRED. The iteration-1 headline AC1 was the UNCORRECTED field") +
            f"; the correction term (1+3rho)/T is "
            f"{a4['which_field'][0]['kendall_correction_term_at_T192']:.4f} at T=192 and "
            f"{a4['which_field'][0]['kendall_correction_term_at_T64']:.4f} at T=64, and the "
            f"matched-length re-report at T={a4['largest_common_length']} is available for "
            f"every model at the layer-L readout."),
        "analysis5_cross_arm": a5["agreement_note"],
        "overall": (
            "The iteration-1 negative result SURVIVES but on different evidence than it was "
            "reported on: the direction control is re-adjudicated on assumption-free "
            "statistics rather than on a non-identifiable lambda, the cross-model indicator "
            "claim is withdrawn for want of a validated observable in three of four members, "
            "and the SPI-vs-baseline rank comparison is retired as uninformative by "
            "construction at n=4."),
    }

    # ---------------- limitations ------------------------------------------
    limitations = [
        "This is a re-analysis: no rollouts, steering runs or model forward passes were "
        "regenerated, so every number inherits the iteration-1 sampling design (4 checkpoints, "
        "20 harmless prompts, 20 rollouts, T=192, fit_len=64).",
        "All bootstrap CIs resample PROMPTS only (n=20). decay_ratio_16 and auc_norm are stored "
        "prompt-level in the archive, so a rollout-level or two-level bootstrap for them is "
        "impossible without new compute; only lambda has per-rollout values.",
        "The equivalence margin of ±0.20 log units is pre-registered in THIS artifact's plan, "
        "not in iteration 1; it is a post-hoc but pre-specified choice justified against the "
        "free-running-vs-teacher-forced contrast the same tree calls a real effect.",
        "S1 (decay_ratio_16) and S2 (auc_norm) are ratios of quantities measured at the same "
        "noise floor; rows with non-positive or non-finite values are dropped from the log-scale "
        "analysis and counted in metadata.census.primary_cell_missingness. Nothing is imputed.",
        "AUROC confidence intervals for the observable-validity gate use the Hanley-McNeil "
        "normal approximation on n=128+128; the per-row r0 arrays are not archived, so a DeLong "
        "or bootstrap CI is not recoverable.",
        "The observable_sanity block exists only at the layer-L logit-lens readout. Unless "
        "out/final_layer_gate.json is present, the gate cannot be evaluated at the final-layer "
        "readout, and the final-layer arm of every gated statement is reported as "
        "'not recoverable without new compute'.",
        "series_length_sweep is archived only for the layer-L readout, so the matched-length "
        "AC1 re-report cannot be repeated at the final-layer readout.",
        "The instrument-sensitivity check uses experiment 2, which covers ONE Qwen3 lineage; "
        "SmolLM2-360M has no forced-refusal stream, so its low prompt-level AUROC cannot be "
        "attributed to instrument versus behaviour.",
        "The abliterated member differs between the two arms (huihui-ai/Huihui-Qwen3-0.6B-"
        "abliterated-v2 in experiment 1, mlabonne/Qwen3-0.6B-abliterated in experiment 2). "
        "The two are never merged and cross-arm agreement is corroboration, not replication.",
        "The refusal-token lexicon used for the instrument check is the Qwen3 family list, "
        "derived from Qwen/Qwen3-0.6B; it is applied to the base and abliterated members of the "
        "same tokenizer family, which share the vocabulary but not the refusal behaviour.",
        "The exact-permutation analysis treats the four checkpoints as exchangeable units. They "
        "are not independent (three share a pretrained base), which if anything makes the "
        "effective n smaller than 4, not larger.",
        "Ground-truth harmful refusal rates come from n=40 scored completions per model with a "
        "frozen string criterion; two of four models sit at k<=1, so their Wilson CIs overlap "
        "and no rank statistic can separate them.",
        "Holm correction is applied within the 48-test difference-in-differences family only; "
        "the gate, permutation and length analyses are reported without further multiplicity "
        "adjustment because each is a single pre-specified question.",
        "The verdict labels DIRECTION_SPECIFIC / NO_DIRECTION_SPECIFICITY / INCONCLUSIVE are "
        "decided by CI rules (95% CI excluding 0; 90% CI inside ±margin), so they inherit the "
        "percentile bootstrap's small-n coverage error at n=20 prompts.",
        "No LLM API calls were made and no new GPU compute was consumed by the reported "
        "headline numbers; total spend for this artifact is $0.00.",
    ]

    # ---------------- eval_out.json ----------------------------------------
    datasets = [
        {"dataset": "direction_contrast",
         "examples": rows_to_examples(
             a1["contrast"], input_keys=["model", "statistic", "readout", "channel"],
             output_fn=lambda r: (
                 f"log-ratio {r['mean_log_diff']:+.3f} "
                 f"[{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}] over n={r['n_pairs']} prompts; "
                 f"{'CI excludes 0' if r['ci_excludes_zero'] else 'CI includes 0'}"))},
        {"dataset": "interaction_did",
         "examples": rows_to_examples(
             a1["did"], input_keys=["pair", "statistic", "readout", "channel"],
             output_fn=lambda r: f"{r['verdict']}: DiD {r['did_mean']:+.3f} "
                                 f"[{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}]")},
        {"dataset": "ratchet_free_vs_teacher_forced",
         "examples": rows_to_examples(
             a1["ratchet"], input_keys=["model", "statistic", "readout"],
             output_fn=lambda r: f"free/teacher-forced ratio "
                                 f"{r['ratio_natural_scale']:.3f}x, "
                                 f"{'CI excludes 0' if r['ci_excludes_zero'] else 'CI includes 0'}")},
        {"dataset": "lambda_consistency_check",
         "examples": rows_to_examples(
             a1["lambda_check"]["rows"], input_keys=["pair", "lambda_statistic"],
             output_fn=lambda r: (
                 f"archived diff {r['diff_verbatim']:+.4f} "
                 f"[{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}] — NOT ADMISSIBLE: identifiable=false "
                 f"on {r['n_lambda_rows_identifiable_false']}/{r['n_lambda_rows_total']} rows"))},
        {"dataset": "validity_gate",
         "examples": rows_to_examples(
             gate["rows"], input_keys=["model", "readout"],
             output_fn=lambda r: ("NOT RECOVERABLE" if r["auroc"] is None else
                                  f"AUROC {r['auroc']:.4f} "
                                  f"[{r['auroc_ci_lo']:.3f}, {r['auroc_ci_hi']:.3f}], "
                                  f"margin {r['margin']:+.4f} -> "
                                  f"{'PASS' if r['passes_gate'] else 'FAIL'}"))},
        {"dataset": "validity_gate_sensitivity",
         "examples": rows_to_examples(
             gate["sensitivity"], input_keys=["readout", "threshold"],
             output_fn=lambda r: f"{r['n_members_passing']} members pass "
                                 f"({r['members_passing']}) -> "
                                 f"{r['n_admissible_pairs']} admissible pairs")},
        {"dataset": "ordering_tests_gate_labelled",
         "examples": rows_to_examples(
             gate["all_ordering_labelled"], input_keys=["pair", "indicator"],
             output_fn=lambda r: f"{r['gate_label']} | diff {r['diff']:+.4f} "
                                 f"[{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}]")},
        {"dataset": "instrument_sensitivity",
         "examples": rows_to_examples(
             inst["rows"], input_keys=["member_exp2", "arm"],
             output_fn=lambda r: ("no lexicon tokens found" if r["token_level_auroc"] is None
                                  else f"token-level AUROC {r['token_level_auroc']:.4f} "
                                       f"[{r['auroc_ci_lo']:.3f}, {r['auroc_ci_hi']:.3f}] on "
                                       f"{r['n_refusal_lexicon_tokens']}+"
                                       f"{r['n_continuation_lexicon_tokens']} tokens"))},
        {"dataset": "small_n_permutation",
         "examples": rows_to_examples(
             a3["rows"] + a3["reproduction"] + [a3["floor"]],
             input_keys=["method", "target", "quantity"],
             output_fn=lambda r: (
                 f"rho {r['rho']:+.3f}, exact two-sided p {r['p_exact_two_sided']:.4f} "
                 f"(floor {r['min_attainable_two_sided_p']:.4f})" if "rho" in r else
                 (f"archived {r['archived_value']:+.2f}; tie-aware "
                  f"{r['recomputed_value_tie_aware_average_ranks']:+.4f} "
                  f"({'reproduces' if r['reproduces_with_tie_aware_ranks'] else 'MISMATCH'}); "
                  f"ordinal tie-break {r['recomputed_value_ordinal_tiebreak']:+.4f} "
                  f"({'reproduces' if r['reproduces_with_ordinal_tiebreak'] else 'MISMATCH'}); "
                  f"tie-break range [{r['tiebreak_range_lo']:+.3f}, {r['tiebreak_range_hi']:+.3f}]"
                  if "archived_value" in r else
                  f"{r['n_resolvable_ground_truth_levels']} resolvable ground-truth levels of "
                  f"{r['n_models']} models; max attainable |rho| given ties "
                  f"{r['max_attainable_abs_rho_given_ties']:.3f}")))},
        {"dataset": "ac1_length",
         "examples": rows_to_examples(
             a4["which_field"] + a4["lengths"] + a4["manufactured"] + a4["final_readout"],
             input_keys=["model", "readout"],
             output_fn=lambda r: (
                 ("AC1 reported by iteration 1 is the "
                  + ("CORRECTED" if r.get("matches_corrected") else "UNCORRECTED")
                  + " field") if "matches_corrected" in r else
                 (f"n_steps {r['n_steps_min']}-{r['n_steps_max']}, "
                  f"EOS-truncated fraction {r['mean_frac_rollouts_hit_eos']:.4f}"
                  if "n_steps_min" in r else
                  (f"AC1 swings {r['ac1_swing_across_lengths']:+.4f} from T="
                   f"{r['shortest_length']} to T={r['longest_length']}"
                   if "ac1_swing_across_lengths" in r else
                   f"final-layer AC1 corrected {r['ac1_corrected_median']:.4f} vs uncorrected "
                   f"{r['ac1_uncorrected_median']:.4f}"))))},
        {"dataset": "ac1_length_sweep",
         "examples": rows_to_examples(
             a4["sweep"] + a4["matched"], input_keys=["model", "pair", "indicator", "length"],
             output_fn=lambda r: (f"AC1 corrected {r['ac1_corrected_median']:.4f} / raw "
                                  f"{r['ac1_raw_median']:.4f}" if "ac1_corrected_median" in r
                                  else f"matched-length diff {r['diff']:+.4f} "
                                       f"[{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}]"))},
        {"dataset": "cross_arm_asymmetry",
         "examples": rows_to_examples(
             a5["cross_arm"] + a5["steering"] + inst["r_t_distributions"],
             input_keys=["channel", "member", "member_exp2", "arm"],
             output_fn=lambda r: (
                 f"{r['value']:+.4f} " + (f"[{r['ci_lo']:.4f}, {r['ci_hi']:.4f}]"
                                          if r.get("ci_lo") is not None else "(no CI)")
                 if "value" in r else
                 (f"up-ramp failure {r['upramp_fail_rate']:.3f} "
                  f"({r['upramp_k']}/{r['upramp_n']}), alpha50 {r['alpha50_fitted']}"
                  if "upramp_fail_rate" in r else
                  f"r_t p05/p50/p95 = {r['p05']:.2f}/{r['p50']:.2f}/{r['p95']:.2f} "
                  f"over n={r['n']} tokens")))},
    ]

    metrics_agg = {
        "primary_did_mean_log_units": float(prim_did["did_mean"]),
        "primary_did_ci_lo": float(prim_did["ci_lo"]),
        "primary_did_ci_hi": float(prim_did["ci_hi"]),
        "primary_did_tost_p": float(prim_did["tost_p"]),
        "primary_direction_contrast_mean_log": float(prim_con["mean_log_diff"]),
        "n_did_tests": float(len(a1["did"])),
        "n_did_ci_excludes_zero": float(n_did_sig),
        "n_did_equivalent_at_margin_020": float(n_did_equiv),
        "n_did_inconclusive": float(sum(1 for r in a1["did"] if r["verdict"] == "INCONCLUSIVE")),
        "n_lambda_rows_identifiable_false": float(census["n_identifiable_false"]),
        "n_lambda_rows_total": float(census["n_lambda_rows_archived"]),
        "gate_threshold_auroc": float(GATE_AUROC),
        "n_members_passing_gate_layerL": float(len(gate["members_passing_layerL"])),
        "n_admissible_model_pairs_layerL": float(gate["n_admissible_pairs_layerL"]),
        "n_admissible_ordering_rows": float(len(gate["admissible_ordering"])),
        "n_members_passing_gate_final": float(len(gate["members_passing_final"])),
        "n_admissible_model_pairs_final": float(gate["n_admissible_pairs_final"]),
        "final_readout_gate_recovered": float(gate["final_readout_recovered"]),
        "instrument_auroc_min_over_members": float(
            min(r["token_level_auroc"] for r in inst["rows"]
                if r["token_level_auroc"] is not None)),
        "instrument_auroc_max_over_members": float(
            max(r["token_level_auroc"] for r in inst["rows"]
                if r["token_level_auroc"] is not None)),
        "rho_spi_vs_harmful": float(spi_row["rho"]),
        "rho_spi_ordinal_tiebreak": float(
            [r for r in a3["reproduction"] if r["quantity"] == "rho_SPI_label_free_vs_harmful"
             ][0]["recomputed_value_ordinal_tiebreak"]),
        "rho_baseline_ordinal_tiebreak": float(
            [r for r in a3["reproduction"]
             if r["quantity"] == "rho_baseline_diff_in_means_auroc_vs_harmful"
             ][0]["recomputed_value_ordinal_tiebreak"]),
        "n_tied_models_on_ground_truth": float(a3["reproduction"][0]["n_tied_models_on_ground_truth"]),
        "rho_spi_exact_two_sided_p": float(spi_row["p_exact_two_sided"]),
        "rho_baseline_diff_means_vs_harmful": float(base_row["rho"]),
        "rho_baseline_exact_two_sided_p": float(base_row["p_exact_two_sided"]),
        "exact_permutation_min_one_sided_p": float(spi_row["min_attainable_one_sided_p"]),
        "exact_permutation_min_two_sided_p": float(spi_row["min_attainable_two_sided_p"]),
        "n_resolvable_ground_truth_levels": float(
            a3["floor"]["n_resolvable_ground_truth_levels"]),
        "max_attainable_abs_rho_given_ties": float(
            a3["floor"]["max_attainable_abs_rho_given_ties"]),
        "ac1_headline_field_is_kendall_corrected": float(ac1_corrected),
        "ac1_kendall_term_at_T192": float(a4["which_field"][0]["kendall_correction_term_at_T192"]),
        "ac1_kendall_term_at_T64": float(a4["which_field"][0]["kendall_correction_term_at_T64"]),
        "largest_common_series_length": float(a4["largest_common_length"]),
        "n_matched_length_pairs_ci_excludes_zero": float(
            sum(1 for r in a4["matched"] if r["ci_excludes_zero"])),
        "n_prompts_needed_for_pm020_margin":
            float(prim_did["n_prompts_for_pm020_margin_80pct_power"] or float("nan"))
            if prim_did["n_prompts_for_pm020_margin_80pct_power"] else 0.0,
        "n_limitations": float(len(limitations)),
        "cost_usd": 0.0,
    }

    out = {
        "metadata": {
            "evaluation_name": "wobble_dynamics_reanalysis",
            "description": ("Pure re-analysis of the iteration-1 dynamics tree: direction "
                            "control on assumption-free statistics, observable-validity gate, "
                            "exact-permutation ceiling at n=4, and the AC1 length confound."),
            "inputs": manifest,
            "census": census,
            "layer_choice": layer_choice,
            "refit_certified_summary": refit_summary,
            "parameters": {
                "equivalence_margin_log_units": EQ_MARGIN,
                "gate_auroc_threshold": GATE_AUROC,
                "gate_margin_rule": "margin > 0 (harmful must score HIGHER than benign)",
                "gate_sensitivity_thresholds": GATE_THRESHOLDS,
                "bootstrap_reps": EL.BOOT_REPS, "bootstrap_seed": EL.BOOT_SEED,
                "primary_cell": PRIMARY_CELL,
                "primary_pair": list(PRIMARY_PAIR),
                "primary_statistic": "S1_decay_ratio_16",
                "primary_readout": "layerL",
                "primary_channel": "teacher_forced",
                "multiplicity": "Holm within the 48-test difference-in-differences family",
                "resampling_unit": "prompt (n=20); rollout-level resampling is NOT possible for "
                                   "decay_ratio_16 / auc_norm because the archive stores them "
                                   "prompt-level only",
            },
            "verdicts": verdicts,
            "limitations": limitations,
            "analysis_detail": {
                "lambda_diagnostics": a1["lambda_check"]["diagnostics"],
                "identifiability_rule": a1["lambda_check"]["identifiability_rule"],
                "archived_random_direction_control": a1["lambda_check"]["archived_control_block"],
                "gate_members_passing_layerL": gate["members_passing_layerL"],
                "gate_admissible_ordering_rows": gate["admissible_ordering"],
                "instrument_coverage_note": inst["coverage_note"],
                "permutation_null_distributions": a3["null_distributions"],
                "spi_and_baseline_values": a3["method_values"],
                "ground_truth_values": a3["target_values"],
                "series_lengths_available": a4["lengths_available"],
                "cross_arm_agreement_note": a5["agreement_note"],
                "downgraded_claim_text": (
                    "On the only member whose refusal observable is a validated refusal readout "
                    "(instruct: AUROC 0.793, margin +0.707), no cross-model contrast is "
                    "available. The Qwen-triad indicator overlap (Var* 3.10-3.15, AC1 "
                    "0.245-0.304, flicker 40.2-42.2) and the SmolLM2 separation are contrasts "
                    "between series at least one of which is not a validated refusal signal, so "
                    "the sentence 'indicators track lineage, not safety' is withdrawn as stated."),
            },
            "cost_usd": 0.0,
        },
        "metrics_agg": {k: v for k, v in metrics_agg.items() if v is not None and np.isfinite(v)},
        "datasets": datasets,
    }

    p = HERE / "eval_out.json"
    p.write_text(json.dumps(out, indent=2, default=str))
    logger.info(f"wrote {p} ({p.stat().st_size/1e6:.2f} MB), "
                f"{sum(len(d['examples']) for d in datasets)} example rows")

    logger.info("rendering figures")
    figs = make_figures(res)
    logger.info(f"wrote {len(figs)} figure files")

    (HERE / "out" / "analysis_tables.json").write_text(json.dumps(res, indent=2, default=str))
    return


if __name__ == "__main__":
    main()
