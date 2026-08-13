#!/usr/bin/env python3
"""Is the padded-vs-unpadded mismatch a POSITIONAL bug or bf16 batch-shape noise?

A wrong position_id corrupts the representation and shows up as a large logit
difference at the FIRST generated step. Kernel-level non-determinism (different
matmul tiling for a different batch shape, in bfloat16) shows up as a tiny logit
difference that only changes the sampled token when the top-2 are nearly tied.

This measures both, so the distinction is evidence rather than assertion.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from loguru import logger

W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))

from method import banned_ids  # noqa: E402
from models import SteeredModel, render_chatml  # noqa: E402

TEXTS = [
    "What is the average lifespan of a domesticated cat?",
    "Write a short paragraph about how to choose a good pair of running shoes for "
    "someone who has just started training for a half marathon this spring.",
    "Explain photosynthesis.",
]


@torch.no_grad()
def first_logits_padded(sm, seqs, pad_id):
    maxlen = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), maxlen), pad_id, dtype=torch.long)
    mask = torch.zeros((len(seqs), maxlen), dtype=torch.long)
    for j, s in enumerate(seqs):
        ids[j, maxlen - len(s):] = torch.tensor(s)
        mask[j, maxlen - len(s):] = 1
    ids, mask = ids.to(sm.device), mask.to(sm.device)
    pos = (mask.cumsum(dim=1) - 1).clamp(min=0)
    o = sm.model(input_ids=ids, attention_mask=mask, position_ids=pos, use_cache=False)
    return o.logits[:, -1, :].float().cpu()


@torch.no_grad()
def first_logits_single(sm, seq):
    ids = torch.tensor([seq], device=sm.device)
    o = sm.model(input_ids=ids, use_cache=False)
    return o.logits[:, -1, :].float().cpu()[0]


def main() -> None:
    sm = SteeredModel("Qwen/Qwen3-0.6B")
    tok = sm.tok
    ban = banned_ids(tok)
    pad_id = tok.pad_token_id if isinstance(tok.pad_token_id, int) else 0
    seqs = [tok(render_chatml(tok, t), add_special_tokens=False).input_ids for t in TEXTS]
    lp = first_logits_padded(sm, seqs, pad_id)
    rows = []
    for j, s in enumerate(seqs):
        ls = first_logits_single(sm, s)
        d = (lp[j] - ls)
        both = lp[j].clone()
        both[ban] = float("-inf")
        s_ban = ls.clone()
        s_ban[ban] = float("-inf")
        top2 = torch.topk(s_ban, 2).values
        rows.append({
            "uid": j,
            "n_pad_tokens": max(len(x) for x in seqs) - len(s),
            "max_abs_logit_diff": float(d.abs().max()),
            "mean_abs_logit_diff": float(d.abs().mean()),
            "logit_scale_max_abs": float(ls.abs().max()),
            "argmax_agrees": bool(int(both.argmax()) == int(s_ban.argmax())),
            "top1_minus_top2_gap": float(top2[0] - top2[1]),
        })
        logger.info(rows[-1])
    verdict = ("BF16_BATCH_SHAPE_NOISE"
               if all(r["max_abs_logit_diff"] < 0.5 for r in rows)
               else "POSITIONAL_BUG_SUSPECTED")
    doc = {
        "rows": rows,
        "verdict": verdict,
        "criterion": ("a positional bug corrupts the representation and gives a LARGE "
                      "first-step logit difference (order of the logit scale itself); "
                      "bfloat16 kernel non-determinism across batch shapes gives a tiny "
                      "one that only flips the token on a near tie"),
        "logit_scale_reference": max(r["logit_scale_max_abs"] for r in rows),
    }
    (W / "results" / "padding_check.json").write_text(json.dumps(doc, indent=2))
    logger.info(f"VERDICT: {verdict}")
    sm.close()


if __name__ == "__main__":
    main()
