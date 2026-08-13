#!/usr/bin/env python3
"""T1-T4 environment / plumbing smoke tests."""

from __future__ import annotations

import sys

import torch
from loguru import logger

from classify import RefusalClassifier, build_token_sets
from models import SteeredModel, clone_cache, new_cache, render_chatml
from ramp import make_generator, sample_tokens

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

INSTRUCT = "Qwen/Qwen3-0.6B"
BASE = "Qwen/Qwen3-0.6B-Base"
ABL = "mlabonne/Qwen3-0.6B-abliterated"


def main() -> None:
    sm = SteeredModel(INSTRUCT)
    logger.info(f"n_layers={sm.n_layers} d_model={sm.d_model}")
    s = render_chatml(sm.tok, "Explain how a bicycle derailleur shifts gears.")
    logger.info(f"rendered={s!r}")
    ids = sm.tok(s, return_tensors="pt", add_special_tokens=False).input_ids.to(sm.device)
    logger.info(f"prompt tokens={ids.shape}")

    # T1: greedy generation
    cache = new_cache()
    logits, cache = sm.forward(ids, cache)
    out = []
    for _ in range(20):
        t = int(logits.argmax(-1)[0])
        out.append(t)
        logits, cache = sm.forward(torch.tensor([[t]], device=sm.device), cache)
    logger.info(f"T1 greedy: {sm.tok.decode(out)!r}")

    # T3a: cache vs no-cache equivalence
    full = torch.cat([ids, torch.tensor([out[:10]], device=sm.device)], dim=1)
    o = sm.model(input_ids=full, use_cache=False)
    logger.info(f"T3a nocache next tok={int(o.logits[0,-1].argmax())} cached path tok={out[10]}")

    # T3b: cache deep-copy restore
    cache = new_cache()
    logits, cache = sm.forward(ids, cache)
    for t in out[:10]:
        logits, cache = sm.forward(torch.tensor([[t]], device=sm.device), cache)
    snap = clone_cache(cache)
    g1 = make_generator(sm.device, 7)
    a = []
    lg = logits
    c = cache
    for _ in range(10):
        t = int(sample_tokens(lg, 0.7, g1)[0])
        a.append(t)
        lg, c = sm.forward(torch.tensor([[t]], device=sm.device), c)
    g2 = make_generator(sm.device, 7)
    b = []
    lg2 = logits
    c2 = snap
    for _ in range(10):
        t = int(sample_tokens(lg2, 0.7, g2)[0])
        b.append(t)
        lg2, c2 = sm.forward(torch.tensor([[t]], device=sm.device), c2)
    logger.info(f"T3b identical={a == b} restored_len={snap.get_seq_length()} expect={ids.shape[1] + 10}")

    # T2: tokenisation parity
    for other in (BASE, ABL):
        from transformers import AutoTokenizer

        tk = AutoTokenizer.from_pretrained(other)
        ids2 = tk(s, return_tensors="pt", add_special_tokens=False).input_ids
        logger.info(f"T2 {other}: identical={bool((ids2.cpu() == ids.cpu()).all())} shape={tuple(ids2.shape)}")

    # classifier sets
    ts = build_token_sets(sm.tok)
    logger.info(f"refusal ids={len(ts['refusal_ids'])} cont ids={len(ts['continuation_ids'])}")
    clf = RefusalClassifier(sm.tok, ts)
    logger.info(f"r_t on last logits={clf.r_t(logits):.3f}")
    sm.close()


if __name__ == "__main__":
    main()
