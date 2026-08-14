#!/usr/bin/env python3
"""Probe the UP-ramp success rate as a function of the alpha step size."""

from __future__ import annotations

import sys

import numpy as np
import torch
from loguru import logger

from classify import RefusalClassifier, build_token_sets
from direction import fit_direction_profile, median_norms_all_layers
from method import CFG, banned_ids, greedy_first_tokens
from models import SteeredModel, render_chatml
from prompts import BENIGN_RAMP_PROMPTS, get_contrast_splits
from ramp import run_down_forced_a, run_down_retained, run_up_ramp

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{message}")

POS, LAYER = 2, 22


def main() -> None:
    sm = SteeredModel("Qwen/Qwen3-0.6B")
    splits = get_contrast_splits()
    render = lambda t: render_chatml(sm.tok, t)  # noqa: E731
    prof = fit_direction_profile(sm, splits, render)
    norms = median_norms_all_layers(sm, BENIGN_RAMP_PROMPTS[:10], render)
    sm.state.direction = torch.tensor(
        prof["directions"][POS, LAYER], dtype=torch.bfloat16, device=sm.device
    )
    sm.state.norm_l = norms[LAYER]
    WINDOW = list(range(LAYER - 2, LAYER + 3))
    sm.install_hook(WINDOW)
    ban = banned_ids(sm.tok)
    ts = build_token_sets(sm.tok, greedy_first_tokens(sm, BENIGN_RAMP_PROMPTS[:5], render))
    clf = RefusalClassifier(sm.tok, ts)

    for delta, amax in ((0.05, 2.0), (0.1, 2.5), (0.2, 3.0), (0.4, 4.0)):
        cfg = {**CFG, "delta": delta, "alpha_max": amax}
        ups, fails = [], 0
        for p in BENIGN_RAMP_PROMPTS[:5]:
            ids = sm.tok(render(p), return_tensors="pt", add_special_tokens=False).input_ids.to(
                sm.device
            )
            for seed in (1, 2):
                up = run_up_ramp(sm, clf, ids, temperature=0.7, seed=seed, banned=ban, cfg=cfg)
                if up.failed:
                    fails += 1
                else:
                    ups.append(up.alpha_threshold)
                    if len(ups) <= 3:
                        logger.info(f"  d={delta} a_up={up.alpha_threshold:.2f} {up.text!r}")
        logger.info(
            f"delta={delta} amax={amax}: up_fail={fails}/10 "
            f"mean_alpha_up={np.mean(ups) if ups else None}"
        )
    sm.close()


if __name__ == "__main__":
    main()
