#!/usr/bin/env python3
"""T2 — determinism, eps=0 no-op, and the pairing/divergence distribution.

Three assertions that must hold before any lambda is believed:
  1. same seed, no injection, twice  -> BIT-IDENTICAL tokens and r arrays
  2. clean vs perturbed at eps=0     -> BIT-IDENTICAL (the hook is a true no-op)
  3. at the working eps              -> record WHERE the token streams diverge
Assertion 3 decides whether the teacher-forced fallback is needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from run_tier0 import BASE_EPS_C, BASE_P, diff_means_direction  # noqa: E402
from spi.models import MODEL_PANEL, free_model, load_model  # noqa: E402
from spi.observable import Observable, build_token_sets  # noqa: E402
from spi.prompts import build_prompt_sets  # noqa: E402
from spi.rollout import first_divergence, rollout_batch  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/t2.log", rotation="30 MB", level="DEBUG")

OUT = Path(__file__).parent / "out"


@logger.catch(reraise=True)
def main() -> None:
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    sets = build_prompt_sets(OUT / "prompts", allow_network=True)
    spec = next(s for s in MODEL_PANEL if s["member"] == "instruct")
    lm = load_model(spec, device=dev)
    L = 14
    obs = Observable(lm, build_token_sets(lm))
    d_vec, d_meta = diff_means_direction(
        lm, L, sets["contrast_harmful"], sets["contrast_benign"])
    text = lm.render(sets["benign"][0]["text"])
    kw = dict(layer=L, n_roll=8, T=96, seed=42)

    a = rollout_batch(lm, obs, text, **kw)
    b = rollout_batch(lm, obs, text, **kw)
    det_tok = bool((a.tokens == b.tokens).all())
    det_r = bool(np.array_equal(a.r, b.r))
    logger.info(f"T2.1 determinism: tokens_identical={det_tok} r_identical={det_r}")
    assert det_tok and det_r, "rollout_batch is NOT deterministic under a fixed seed"

    z = rollout_batch(lm, obs, text, inject={
        "step": BASE_P, "vec": d_vec, "eps": 0.0, "mode": "once"}, **kw)
    noop_tok = bool((a.tokens == z.tokens).all())
    noop_r = bool(np.array_equal(a.r, z.r))
    logger.info(f"T2.2 eps=0 no-op: tokens_identical={noop_tok} r_identical={noop_r}")
    assert noop_tok and noop_r, "the injection hook is not a no-op at eps=0"

    eps_abs = d_meta["median_resid_norm_benign"]
    noise = float((a.r - a.r.mean(axis=1, keepdims=True)).std())
    noise_f = float((a.r_final - a.r_final.mean(axis=1, keepdims=True)).std())
    rows = []
    for c in (0.05, 0.1, 0.2, 0.4, 0.8):
        for mode, k in (("once", 1), ("sustained", 4)):
            p = rollout_batch(lm, obs, text, inject={
                "step": BASE_P, "vec": d_vec, "eps": c * eps_abs,
                "mode": mode, "k": k}, **kw)
            off = BASE_P + k  # measure decay from after the injection window
            div = first_divergence(a.tokens, p.tokens) - BASE_P
            d1 = float(np.abs(p.r[off] - a.r[off]).mean())
            d1f = float(np.abs(p.r_final[off] - a.r_final[off]).mean())
            steps_above = int((np.abs(p.r[off:] - a.r[off:]).mean(axis=1) > noise).sum())
            rows.append({
                "eps_c": c, "eps_abs": float(c * eps_abs), "mode": mode, "k": k,
                "median_steps_to_divergence": float(np.median(div)),
                "frac_diverging_within_3": float((div <= 3).mean()),
                "delta_at_p1_layerL": d1, "snr_layerL": d1 / max(noise, 1e-9),
                "delta_at_p1_final": d1f, "snr_final": d1f / max(noise_f, 1e-9),
                "steps_above_noise_floor_layerL": steps_above,
            })
            logger.info(
                f"T2.3 c={c} {mode}: snr_L={rows[-1]['snr_layerL']:.3f} "
                f"snr_final={rows[-1]['snr_final']:.3f} "
                f"steps_above_floor={steps_above} "
                f"div={rows[-1]['median_steps_to_divergence']:.0f}"
            )
    base = [r for r in rows if abs(r["eps_c"] - BASE_EPS_C) < 1e-9 and r["mode"] == "once"]
    assert base and base[0]["snr_layerL"] > 0, (
        "injection produced ZERO layer-L deviation — the hook is not on the "
        "channel we believe it is on"
    )

    out = {
        "determinism_tokens": det_tok, "determinism_r": det_r,
        "eps0_noop_tokens": noop_tok, "eps0_noop_r": noop_r,
        "layer": L, "eps_reference_norm": float(eps_abs),
        "noise_sd_layerL": noise, "noise_sd_final": noise_f,
        "divergence_by_eps": rows,
        "teacher_forcing_recommended": bool(
            any(r["frac_diverging_within_3"] > 0.5 for r in rows
                if abs(r["eps_c"] - BASE_EPS_C) < 1e-9)),
        "sustained_injection_recommended": bool(
            all(r["steps_above_noise_floor_layerL"] < 3 for r in rows
                if r["mode"] == "once" and abs(r["eps_c"] - BASE_EPS_C) < 1e-9)),
        "tokens_per_sec": a.tokens_per_sec,
    }
    (OUT / "t2_pairing_report.json").write_text(json.dumps(out, indent=2))
    logger.info(f"T2 PASSED | {a.tokens_per_sec:.0f} tok/s | "
                f"teacher_forcing_recommended={out['teacher_forcing_recommended']}")
    free_model(lm)


if __name__ == "__main__":
    main()
