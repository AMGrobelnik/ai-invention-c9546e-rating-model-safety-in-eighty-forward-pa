#!/usr/bin/env python3
"""Inspect what steering actually does at a range of alphas and layers."""

from __future__ import annotations

import sys

import numpy as np
import torch
from loguru import logger

from direction import fit_direction_profile, median_norm_at_layer
from models import SteeredModel, new_cache, render_chatml
from prompts import BENIGN_RAMP_PROMPTS, get_contrast_splits

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{message}")


def gen(sm, ids, alpha, n=24):
    sm.state.resize(1)
    sm.state.set_alpha(alpha)
    logits, cache = sm.forward(ids, new_cache())
    out = []
    for _ in range(n):
        t = int(logits.argmax(-1)[0])
        out.append(t)
        logits, cache = sm.forward(torch.tensor([[t]], device=sm.device), cache)
    return sm.tok.decode(out)


def main() -> None:
    mid = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen3-0.6B"
    sm = SteeredModel(mid)
    splits = get_contrast_splits()
    render = lambda t: render_chatml(sm.tok, t)  # noqa: E731
    prof = fit_direction_profile(sm, splits, render)
    logger.info(f"dprime argmax layer={int(np.argmax(prof['dprime_profile']))}")
    p = BENIGN_RAMP_PROMPTS[0]
    ids = sm.tok(render(p), return_tensors="pt", add_special_tokens=False).input_ids.to(
        sm.device
    )
    for layer in (12, 16, 20, 22, 25):
        d = prof["directions"][layer]
        sm.state.direction = torch.tensor(d, dtype=torch.bfloat16, device=sm.device)
        nl = median_norm_at_layer(sm, BENIGN_RAMP_PROMPTS[:5], render, layer)
        sm.state.norm_l = nl
        sm.install_hook(layer)
        logger.info(f"--- layer {layer} norm_L={nl:.1f} ---")
        for a in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0):
            logger.info(f"  a={a}: {gen(sm, ids, a)!r}")
        sm.remove_hook()
    # harmful prompt sanity: does the model refuse unsteered?
    h = splits["fit_harmful"][0]
    ids_h = sm.tok(render(h), return_tensors="pt", add_special_tokens=False).input_ids.to(
        sm.device
    )
    sm.state.direction = torch.tensor(
        prof["directions"][22], dtype=torch.bfloat16, device=sm.device
    )
    sm.install_hook(22)
    sm.state.norm_l = 1.0
    logger.info(f"HARMFUL unsteered: {gen(sm, ids_h, 0.0)!r}")
    sm.close()


if __name__ == "__main__":
    main()
