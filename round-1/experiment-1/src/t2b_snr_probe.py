#!/usr/bin/env python3
"""T2b — the decisive SNR probe.

T2 showed the tension the whole artifact turns on: at an epsilon small enough to
stay in the linear regime the layer-L deviation is ~1% of the natural wobble,
and at an epsilon large enough to be measurable the sampled token streams
diverge within a few steps, so r^pert - r^clean stops isolating the injection.

This script measures, per epsilon:
  - FREE-RUNNING delta (tokens allowed to diverge)
  - TEACHER-FORCED delta (perturbed arm forced onto the clean arm's tokens, so
    pairing can never break and delta isolates latent relaxation)
at BOTH readouts (layer-L logit lens and final-layer), for one-shot and
sustained injection. The output decides the headline geometry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from run_tier0 import BASE_P, diff_means_direction  # noqa: E402
from spi.models import MODEL_PANEL, free_model, load_model  # noqa: E402
from spi.observable import Observable, build_token_sets  # noqa: E402
from spi.prompts import build_prompt_sets  # noqa: E402
from spi.rollout import rollout_batch  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/t2b.log", rotation="30 MB", level="DEBUG")

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
    eps_abs = d_meta["median_resid_norm_benign"]
    logger.info(f"median ||resid_L|| on benign = {eps_abs:.2f}")

    rows = []
    for pid in range(3):
        text = lm.render(sets["benign"][pid]["text"])
        kw = dict(layer=L, n_roll=16, T=128, seed=500 + pid)
        clean = rollout_batch(lm, obs, text, **kw)
        nse = float((clean.r - clean.r.mean(axis=1, keepdims=True)).std())
        nsf = float((clean.r_final - clean.r_final.mean(axis=1, keepdims=True)).std())
        for c in (0.05, 0.1, 0.2, 0.4, 0.8, 1.6):
            for mode, k in (("once", 1), ("sustained", 4)):
                for tf in (False, True):
                    p = rollout_batch(
                        lm, obs, text,
                        inject={"step": BASE_P, "vec": d_vec, "eps": c * eps_abs,
                                "mode": mode, "k": k},
                        force_tokens=clean.tokens if tf else None, **kw)
                    off = BASE_P + k
                    dL = np.abs(p.r[off:] - clean.r[off:]).mean(axis=1)
                    dF = np.abs(p.r_final[off:] - clean.r_final[off:]).mean(axis=1)
                    rows.append({
                        "prompt": sets["benign"][pid]["id"], "eps_c": c, "mode": mode,
                        "teacher_forced": tf,
                        "snr_L_at_start": float(dL[0] / max(nse, 1e-9)),
                        "snr_F_at_start": float(dF[0] / max(nsf, 1e-9)),
                        "snr_L_at_16": float(dL[16] / max(nse, 1e-9)) if dL.size > 16 else None,
                        "steps_above_floor_L": int((dL > nse).sum()),
                        "steps_above_floor_F": int((dF > nsf).sum()),
                        "decay_ratio_L": float(dL[16] / max(dL[0], 1e-12)) if dL.size > 16 else None,
                        "noise_L": nse, "noise_F": nsf,
                    })
                    del p
        del clean
    (OUT / "t2b_snr_probe.json").write_text(json.dumps(rows, indent=2))

    logger.info("=== median over 3 prompts ===")
    logger.info(f"{'c':>5} {'mode':>10} {'tf':>5} {'snrL0':>8} {'snrF0':>8} "
                f"{'snrL16':>8} {'aboveL':>7} {'decayL':>8}")
    for c in (0.05, 0.1, 0.2, 0.4, 0.8, 1.6):
        for mode in ("once", "sustained"):
            for tf in (False, True):
                sel = [r for r in rows if r["eps_c"] == c and r["mode"] == mode
                       and r["teacher_forced"] == tf]
                if not sel:
                    continue
                def med(k: str) -> float:
                    v = [r[k] for r in sel if r[k] is not None]
                    return float(np.median(v)) if v else float("nan")
                logger.info(
                    f"{c:>5} {mode:>10} {str(tf):>5} {med('snr_L_at_start'):>8.3f} "
                    f"{med('snr_F_at_start'):>8.3f} {med('snr_L_at_16'):>8.3f} "
                    f"{med('steps_above_floor_L'):>7.0f} {med('decay_ratio_L'):>8.3f}"
                )
    free_model(lm)


if __name__ == "__main__":
    main()
