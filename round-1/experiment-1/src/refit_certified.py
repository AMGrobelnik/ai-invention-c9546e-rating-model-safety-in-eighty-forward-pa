#!/usr/bin/env python3
"""Re-measure lambda AT THE CERTIFIED GEOMETRY.

The full run fit lambda over T_fit = 64 steps. The synthetic study then certified
that, at the noise and amplitude actually observed (SNR ~1.2 at t=p+1), the
estimator only meets the pre-registered bias/variance rule at T_fit >= 128 and
n_roll >= 20. So the main run's lambda values are correctly flagged
identifiable=false — not because lambda is unmeasurable in principle, but
because the fit window was half as long as it needed to be.

The rollouts are 192 steps and the injection is at p=16, so 175 post-injection
steps are available: T_fit=128 is reachable without generating longer series.
This script re-runs ONLY the headline arms at T_fit=128 and refits, so the
artifact reports lambda at a geometry its own validity study certifies.

Everything else — layer, direction, epsilon, seeds, teacher forcing — is held
identical to the main run, so the two are directly comparable.
"""

from __future__ import annotations

import gc
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from run_tier0 import (  # noqa: E402
    BASE_EPS_C, BASE_P, delta_curve, diff_means_direction,
)
from spi import indicators as ind  # noqa: E402
from spi import validity as val  # noqa: E402
from spi.models import MODEL_PANEL, free_model, load_model  # noqa: E402
from spi.observable import Observable, build_token_sets  # noqa: E402
from spi.prompts import build_prompt_sets  # noqa: E402
from spi.rollout import rollout_batch  # noqa: E402

ROOT = Path(__file__).parent
OUT = ROOT / "out"
FIT_LEN_CERT = 128
N_ROLL = 20
T = 192

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "refit.log", rotation="30 MB", level="DEBUG")


@logger.catch(reraise=True)
def main() -> None:
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    sets = build_prompt_sets(OUT / "prompts", allow_network=True)
    layer_choice = json.loads((OUT / "layer_choice.json").read_text())
    rel_depth = layer_choice["rel_depth"]
    prompts = sets["benign"]

    rows: list[dict[str, Any]] = []
    t_start = time.time()
    for spec in MODEL_PANEL:
        key = f"{spec['lineage']}/{spec['member']}"
        lm = load_model(spec, device=dev)
        try:
            L = int(np.clip(round(rel_depth * lm.n_layers), 1, lm.n_layers - 1))
            obs = Observable(lm, build_token_sets(lm))
            d_vec, d_meta = diff_means_direction(
                lm, L, sets["contrast_harmful"], sets["contrast_benign"])
            eps_abs = d_meta["median_resid_norm_benign"]
            v_ref = d_vec.to(lm.device)
            g = torch.Generator(device="cpu").manual_seed(
                __import__("zlib").crc32(key.encode()) % (2**31))
            v_rand = torch.randn(lm.hidden_size, generator=g)
            v_rand = (v_rand / v_rand.norm()).to(lm.device)
            banned = []
            th = lm.tokenizer.convert_tokens_to_ids("<think>")
            if isinstance(th, int) and th >= 0 and th != lm.tokenizer.unk_token_id:
                banned.append(th)

            for pi, pr in enumerate(prompts):
                t0 = time.time()
                text = lm.render(pr["text"])
                seed = 1000 + pi   # identical to the main run
                kw = dict(layer=L, n_roll=N_ROLL, T=T, seed=seed, banned_ids=banned)
                clean = rollout_batch(lm, obs, text, **kw)
                nsd = float(ind.detrend_across_rollouts(clean.r)[0].std())
                nsdf = float(ind.detrend_across_rollouts(clean.r_final)[0].std())
                for dname, vec in (("toward_refuse", v_ref),
                                   ("toward_comply", -v_ref),
                                   ("random_direction", v_rand)):
                    pert = rollout_batch(
                        lm, obs, text,
                        inject={"step": BASE_P, "vec": vec,
                                "eps": BASE_EPS_C * eps_abs, "mode": "once"},
                        force_tokens=clean.tokens, **kw)
                    row: dict[str, Any] = {
                        "model": key, "member": spec["member"], "lineage": spec["lineage"],
                        "prompt_id": pr["id"], "direction": dname,
                        "eps_c": BASE_EPS_C, "p": BASE_P, "teacher_forced": True,
                        "n_roll": N_ROLL, "T": T, "fit_len": FIT_LEN_CERT, "layer": L,
                    }
                    for tag, rp, rc, sd in (("layerL", pert.r, clean.r, nsd),
                                            ("final", pert.r_final, clean.r_final, nsdf)):
                        mean_d, D = delta_curve(rp, rc, BASE_P)
                        abs_d = np.abs(D).mean(axis=1)
                        late = D[FIT_LEN_CERT // 2 : FIT_LEN_CERT]
                        row[tag] = {
                            "estimates": ind.estimate_lambda_all(
                                mean_d, sd, fit_len=FIT_LEN_CERT, delta_abs=abs_d),
                            "delta_at_p1_signed": float(mean_d[0]),
                            "delta_residual_sd_per_rollout": float(late.std()),
                            "decay_ratio_16": (float(abs(mean_d[16]) / max(abs(mean_d[0]), 1e-12))
                                               if mean_d.size > 16 else None),
                            "decay_ratio_64": (float(abs(mean_d[64]) / max(abs(mean_d[0]), 1e-12))
                                               if mean_d.size > 64 else None),
                            "per_rollout_lambda": [
                                ind.fit_lambda_nls(D[:FIT_LEN_CERT, j], signed=True).get("lambda")
                                for j in range(D.shape[1])],
                            "mean_delta_curve": [float(x) for x in mean_d[:FIT_LEN_CERT]],
                        }
                        del D
                    rows.append(row)
                    del pert
                del clean
                gc.collect()
                if dev == "cuda":
                    torch.cuda.empty_cache()
                logger.info(f"{key} {pi+1}/{len(prompts)} ({pr['id']}) {time.time()-t0:.0f}s")
                (OUT / "refit_certified.json").write_text(json.dumps(rows, indent=1, default=float))
        finally:
            free_model(lm)
            gc.collect()

    # Re-derive the identifiability rule at the noise/amp this refit actually saw.
    noise = [r["layerL"]["delta_residual_sd_per_rollout"] for r in rows
             if r["direction"] == "toward_refuse"]
    amps = [abs(r["layerL"]["delta_at_p1_signed"]) for r in rows
            if r["direction"] == "toward_refuse"]
    syn = val.synthetic_ar1_study(float(np.median(noise)), float(np.median(amps)),
                                  n_reps=500, n_workers=16)
    rule = syn["rule"]
    for r in rows:
        r["identifiable"] = val.is_identifiable(rule, FIT_LEN_CERT, N_ROLL)

    agg: dict[str, Any] = {}
    for m in sorted({r["model"] for r in rows}):
        entry: dict[str, Any] = {}
        for dname in ("toward_refuse", "toward_comply", "random_direction"):
            sel = [r for r in rows if r["model"] == m and r["direction"] == dname]
            lams = [r["layerL"]["estimates"]["est1_nls"].get("lambda") for r in sel]
            r2 = [r["layerL"]["estimates"]["est1_nls"].get("r2") for r in sel]
            r2 = [x for x in r2 if x is not None and np.isfinite(x)]
            entry[dname] = {
                "lambda": ind.cluster_bootstrap_ci([x for x in lams if x is not None]),
                "median_r2": float(np.median(r2)) if r2 else None,
                "decay_ratio_64": ind.cluster_bootstrap_ci(
                    [r["layerL"]["decay_ratio_64"] for r in sel
                     if r["layerL"]["decay_ratio_64"] is not None]),
            }
        pr_ref = {r["prompt_id"]: r["layerL"]["estimates"]["est1_nls"].get("lambda")
                  for r in rows if r["model"] == m and r["direction"] == "toward_refuse"}
        pr_com = {r["prompt_id"]: r["layerL"]["estimates"]["est1_nls"].get("lambda")
                  for r in rows if r["model"] == m and r["direction"] == "toward_comply"}
        ai = [float(np.log(pr_ref[k] / pr_com[k])) for k in sorted(set(pr_ref) & set(pr_com))
              if pr_ref[k] and pr_com[k] and pr_ref[k] > 0 and pr_com[k] > 0]
        entry["asymmetry_index"] = ind.cluster_bootstrap_ci(ai)
        agg[m] = entry

    ref = "qwen3-0.6b/instruct"
    tests: dict[str, Any] = {}
    for comp in [m for m in agg if m != ref]:
        def bp(model: str) -> dict[str, float]:
            return {r["prompt_id"]: r["layerL"]["estimates"]["est1_nls"]["lambda"]
                    for r in rows if r["model"] == model
                    and r["direction"] == "toward_refuse"
                    and r["layerL"]["estimates"]["est1_nls"].get("lambda") is not None}
        tests[f"{ref}_minus_{comp}"] = ind.paired_bootstrap_diff(bp(ref), bp(comp))

    out = {
        "purpose": (
            "lambda re-measured at T_fit=128, the geometry the artifact's own "
            "synthetic study certifies. The main run used T_fit=64, which the rule "
            "rejects; this closes that gap without changing anything else."
        ),
        "fit_len": FIT_LEN_CERT, "n_roll": N_ROLL, "T": T, "p": BASE_P,
        "eps_c": BASE_EPS_C, "teacher_forced": True,
        "identical_to_main_run": ["layer", "direction", "epsilon", "seeds", "prompts"],
        "rule_at_refit_noise": rule,
        "synthetic_meta": {k: v for k, v in syn.items() if k != "table"},
        "synthetic_table": syn["table"],
        "all_rows_identifiable": bool(all(r["identifiable"] for r in rows)),
        "aggregate_by_model": agg,
        "prereg_ordering_tests_lambda_refuse": tests,
        "rows": rows,
        "wall_clock_min": (time.time() - t_start) / 60.0,
    }
    (OUT / "refit_certified.json").write_text(json.dumps(out, indent=1, default=float))
    logger.info(f"RULE at refit noise: {rule.get('min_T_fit')}, {rule.get('min_n_roll')} | "
                f"all identifiable = {out['all_rows_identifiable']}")
    for m in sorted(agg):
        e = agg[m]["toward_refuse"]
        logger.info(f"{m:24s} lambda={e['lambda']['point']} "
                    f"[{e['lambda']['ci_lo']},{e['lambda']['ci_hi']}] r2={e['median_r2']}")
    logger.info(f"Done in {out['wall_clock_min']:.1f} min")


if __name__ == "__main__":
    main()
