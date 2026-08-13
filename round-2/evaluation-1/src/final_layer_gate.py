#!/usr/bin/env python3
"""OPTIONAL forward-pass job: the observable-validity gate at the FINAL-layer readout.

This is the ONLY compute this artifact spends beyond re-reading the archive, and it
is forward-pass only: no sampling, no steering, no generation. For each of the four
iteration-1 checkpoints (loaded at their PINNED revision from
tier0_raw.json:model_revisions) the 256 layer_contrast rows (128 harmful + 128
benign) are rendered with the member's own template and pushed through a single
forward pass. r0 is the FINAL-layer log-odds of the member's ARCHIVED refusal_ids
against its cont_ids at the last prompt position - the identical contrast that
spi/observable.py:Observable.from_logits computes - so the number is commensurable
with the archived layer-L observable_sanity block.

Writes out/final_layer_gate.json. eval.py picks it up automatically if present and
otherwise reports the final-layer gate as 'not recoverable without new compute'.

Run with the iteration-1 environment, which already pins torch/transformers:
  <experiment_1>/.venv/bin/python final_layer_gate.py
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
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = Path(__file__).resolve().parent
(HERE / "logs").mkdir(exist_ok=True)
(HERE / "out").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "final_layer_gate.log", rotation="30 MB", level="DEBUG")

RUN = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art")
TIER0 = RUN / "gen_art_experiment_1" / "out" / "tier0_raw.json"
D1_OUT = RUN / "gen_art_dataset_1" / "full_data_out.json"
OUT = HERE / "out" / "final_layer_gate.json"

BASE_PROMPT_FORMAT = "User: {p}\nAssistant:"
BATCH = 16
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if DEVICE == "cuda":
    torch.cuda.set_per_process_memory_fraction(0.6, 0)


def render(prompt: str, tok: Any, use_chat: bool) -> str:
    if not use_chat:
        return BASE_PROMPT_FORMAT.format(p=prompt)
    msgs = [{"role": "user", "content": prompt}]
    try:
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                       enable_thinking=False)
    except TypeError:
        msgs = [{"role": "user", "content": prompt + " /no_think"}]
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)


@torch.no_grad()
def final_r0(model: Any, tok: Any, texts: list[str], ref: torch.Tensor,
             con: torch.Tensor) -> list[float]:
    out: list[float] = []
    for i in range(0, len(texts), BATCH):
        chunk = texts[i:i + BATCH]
        enc = tok(chunk, return_tensors="pt", add_special_tokens=False,
                  padding=True, padding_side="left")
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        logits = model(**enc).logits[:, -1, :].float()
        a = torch.logsumexp(logits.index_select(-1, ref), dim=-1)
        b = torch.logsumexp(logits.index_select(-1, con), dim=-1)
        out.extend((a - b).cpu().tolist())
        del enc, logits, a, b
    return out


def auroc(pos: list[float], neg: list[float]) -> float:
    a, b = np.asarray(pos), np.asarray(neg)
    ranks = np.argsort(np.argsort(np.concatenate([a, b]))) + 1.0
    r_pos = ranks[:a.size].sum()
    return float((r_pos - a.size * (a.size + 1) / 2) / (a.size * b.size))


@logger.catch(reraise=True)
def main() -> None:
    tree = json.loads(TIER0.read_text())
    revs = tree["model_revisions"]
    toks = tree["observable_token_ids_by_model"]
    del tree
    gc.collect()

    d1 = json.loads(D1_OUT.read_text())
    lc = [x for x in d1["datasets"] if x["dataset"] == "layer_contrast"][0]["examples"]
    harmful = [e["input"] for e in lc if e["metadata_meta"].get("polarity") == "harmful"]
    benign = [e["input"] for e in lc if e["metadata_meta"].get("polarity") == "benign"]
    if not harmful or not benign:
        raise ValueError("layer_contrast: could not split on metadata_meta.polarity")
    logger.info(f"layer_contrast: {len(harmful)} harmful / {len(benign)} benign")
    del d1
    gc.collect()

    results: dict[str, Any] = {}
    failures: dict[str, str] = {}
    for key, meta in revs.items():
        t0 = time.time()
        try:
            logger.info(f"loading {meta['model_id']} @ {meta['revision'][:12]}")
            tk = AutoTokenizer.from_pretrained(meta["model_id"], revision=meta["revision"],
                                               trust_remote_code=False)
            if tk.pad_token is None:
                tk.pad_token = tk.eos_token
            model = AutoModelForCausalLM.from_pretrained(
                meta["model_id"], revision=meta["revision"],
                torch_dtype=torch.bfloat16 if DEVICE == "cuda" else torch.float32,
                trust_remote_code=False)
            model.to(DEVICE).eval().requires_grad_(False)
            ref = torch.tensor(toks[key]["refusal_ids"], device=DEVICE, dtype=torch.long)
            con = torch.tensor(toks[key]["cont_ids"], device=DEVICE, dtype=torch.long)
            use_chat = bool(meta["chat_template"])
            rh = final_r0(model, tk, [render(p, tk, use_chat) for p in harmful], ref, con)
            rb = final_r0(model, tk, [render(p, tk, use_chat) for p in benign], ref, con)
            results[key] = {
                "model_id": meta["model_id"], "revision": meta["revision"],
                "readout": "final_layer_logits",
                "r0_harmful_mean": float(np.mean(rh)),
                "r0_benign_mean": float(np.mean(rb)),
                "margin": float(np.mean(rh) - np.mean(rb)),
                "auroc": auroc(rh, rb),
                "n_pos": len(rh), "n_neg": len(rb),
                "r0_finite": bool(np.all(np.isfinite(rh)) and np.all(np.isfinite(rb))),
                "r0_non_constant": bool(np.std(rh + rb) > 1e-6),
                "seconds": round(time.time() - t0, 1),
                "n_refusal_ids": len(toks[key]["refusal_ids"]),
                "n_cont_ids": len(toks[key]["cont_ids"]),
            }
            logger.info(f"{key}: AUROC {results[key]['auroc']:.4f} "
                        f"margin {results[key]['margin']:+.4f} "
                        f"({results[key]['seconds']}s)")
            del model, tk, ref, con
        except Exception as exc:  # noqa: BLE001 - a missing/gated repo is a reportable outcome
            logger.error(f"{key}: {exc}")
            failures[key] = f"{type(exc).__name__}: {exc}"
        gc.collect()
        if DEVICE == "cuda":
            torch.cuda.empty_cache()

    OUT.write_text(json.dumps({
        "per_model": results, "failures": failures, "device": DEVICE,
        "n_forward_passes": (len(harmful) + len(benign)) * len(results),
        "definition": ("final-layer logit-lens log-odds of the member's archived refusal_ids "
                       "vs cont_ids at the last prompt position, identical in form to "
                       "spi/observable.py:Observable.from_logits"),
        "source_prompts": "gen_art_dataset_1/full_data_out.json:datasets[layer_contrast] "
                          "(128 harmful + 128 benign)",
    }, indent=2))
    logger.info(f"wrote {OUT}: {len(results)} models, {len(failures)} failures")


if __name__ == "__main__":
    main()
