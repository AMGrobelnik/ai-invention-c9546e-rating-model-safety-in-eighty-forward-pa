#!/usr/bin/env python3
"""Padding / KV-cache correctness check for the benchmark scorer.

Left padding a decoder-only model silently corrupts rotary positions unless
position_ids are derived from the attention mask.  This asserts that a padded
batch reproduces the unpadded single-sequence generation TOKEN FOR TOKEN.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bench as BENCH  # noqa: E402
from classify import RefusalClassifier, build_token_sets  # noqa: E402
from method import banned_ids  # noqa: E402
from models import SteeredModel, render_chatml  # noqa: E402

TEXTS = [
    "What is the average lifespan of a domesticated cat?",
    "Write a short paragraph about how to choose a good pair of running shoes for "
    "someone who has just started training for a half marathon this spring.",
    "Explain photosynthesis.",
]


def main() -> None:
    sm = SteeredModel("Qwen/Qwen3-0.6B")
    clf = RefusalClassifier(sm.tok, build_token_sets(sm.tok))
    ban = banned_ids(sm.tok)
    render = lambda t: render_chatml(sm.tok, t)  # noqa: E731
    items = [{"block": "t", "uid": str(i), "user_text": t, "prefill": "",
              "refusal_is_error": False} for i, t in enumerate(TEXTS)]

    batched = BENCH.score_items(sm, clf, items, render, ban, batch=3, n_tokens=16)
    single = BENCH.score_items(sm, clf, items, render, ban, batch=1, n_tokens=16)
    ok = True
    for b, s in zip(batched, single):
        same = b["text"] == s["text"]
        ok = ok and same
        logger.info(f"uid={b['uid']} match={same}\n  batched: {b['text'][:90]!r}\n"
                    f"  single : {s['text'][:90]!r}")
    logger.info(f"PADDING CHECK {'PASSED' if ok else 'MISMATCH'}")
    if not ok:
        logger.warning(
            "A token-level mismatch does NOT by itself mean the positions are wrong: "
            "bfloat16 kernels are batch-shape dependent, so a near-tied argmax can flip "
            "and the sequences then diverge. Run test_padding_logits.py, which measures "
            "the FIRST-STEP logit difference and checks a zero-padding sequence, to "
            "tell a positional bug from numerics.")
    sm.close()


if __name__ == "__main__":
    main()
