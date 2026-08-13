#!/usr/bin/env python3
"""T0 — load every panel member, log geometry, generate 8 tokens, assert no <think>."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from spi.models import MODEL_PANEL, free_model, load_model  # noqa: E402
from spi.observable import build_token_sets  # noqa: E402
from spi.rollout import greedy_generate  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/t0.log", rotation="30 MB", level="DEBUG")

OUT = Path(__file__).parent / "out"


@logger.catch(reraise=True)
def main() -> None:
    OUT.mkdir(exist_ok=True)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    report = []
    for spec in MODEL_PANEL:
        lm = load_model(spec, device=dev)
        rendered = lm.render("What causes the seasons on Earth?")
        logger.info(f"{lm.key} RENDERED PROMPT >>>{rendered}<<<")
        # enable_thinking=False pre-fills a CLOSED empty <think></think> block; that is
        # correct — generation never opens one. What must not happen is an UNCLOSED block.
        assert rendered.count("<think>") == rendered.count("</think>"), (
            f"{lm.key}: chat template left an UNCLOSED <think> block: {rendered!r}"
        )
        ts = build_token_sets(lm)
        out = greedy_generate(lm, rendered, max_new=8)
        logger.info(f"{lm.key} 8-token greedy: {out!r}")
        assert out.strip(), f"{lm.key}: empty generation"
        assert "<think>" not in out, f"{lm.key}: <think> leaked into generation"
        report.append({
            "key": lm.key, "model_id": lm.model_id, "revision": lm.revision,
            "n_layers": lm.n_layers, "hidden_size": lm.hidden_size,
            "dtype": lm.dtype, "chat": lm.uses_chat_template,
            "rendered_prompt": rendered, "gen8": out,
            "n_refusal_ids": len(ts["refusal_ids"]), "n_cont_ids": len(ts["cont_ids"]),
            "vram_gb": float(torch.cuda.max_memory_allocated() / 1024**3) if dev == "cuda" else 0.0,
        })
        free_model(lm)
        if dev == "cuda":
            torch.cuda.reset_peak_memory_stats()
    (OUT / "t0_load_report.json").write_text(json.dumps(report, indent=2))
    logger.info(f"T0 PASSED for {len(report)}/{len(MODEL_PANEL)} models")


if __name__ == "__main__":
    main()
