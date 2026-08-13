#!/usr/bin/env python3
"""Batched steered decoding with per-row alpha, left padding and a live KV cache.

One loop serves every arm in the artifact (dose-response, site scan, up-ramp,
perturbation survival) so no comparison can be confounded by two different
generation implementations.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch

from .models import new_cache


def make_generator(seed: int, device: str = "cpu") -> torch.Generator:
    """Sampling RNG. The generator lives on the SAME device as the logits so the
    decode loop never has to move a full vocabulary tensor to host memory
    (measured: two 20x151k host transfers per step dominated the dose-response)."""
    g = torch.Generator(device=device)
    g.manual_seed(int(seed))
    return g


def sample_tokens(
    logits: torch.Tensor,
    temperature: float,
    generator: torch.Generator | None,
    banned: torch.Tensor | None = None,
) -> torch.Tensor:
    """logits (B, V) -> (B,) sampled ids. temperature <= 0 => argmax."""
    lg = logits.float()
    if banned is not None and banned.numel():
        lg = lg.clone()
        lg[:, banned.to(lg.device)] = float("-inf")
    if temperature <= 0.0:
        return lg.argmax(dim=-1).cpu()
    probs = torch.softmax(lg / temperature, dim=-1)
    return torch.multinomial(probs, num_samples=1, generator=generator).squeeze(-1).cpu()


@torch.no_grad()
def plain_generate(sm, texts: list[str], *, max_new_tokens: int, batch_size: int = 16,
                   temperature: float = 0.0) -> tuple[list[str], float]:
    """Unsteered batched greedy decoding with left padding (the D2 behaviour block).

    Uses HF `generate`; the steering hook is expected to be uninstalled.
    """
    import time

    sm.tok.padding_side = "left"
    out_texts: list[str] = []
    t0 = time.time()
    bs = batch_size
    i = 0
    pad = sm.tok.pad_token_id if sm.tok.pad_token_id is not None else sm.tok.eos_token_id
    while i < len(texts):
        batch = list(texts[i : i + bs])
        try:
            enc = sm.tok(batch, return_tensors="pt", padding=True, add_special_tokens=False)
            enc = {k: v.to(sm.device) for k, v in enc.items()}
            out = sm.model.generate(
                **enc, max_new_tokens=max_new_tokens, do_sample=temperature > 0,
                temperature=temperature if temperature > 0 else None, pad_token_id=pad,
            )
            new = out[:, enc["input_ids"].shape[1] :]
            out_texts.extend(sm.tok.batch_decode(new, skip_special_tokens=True))
            i += bs
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
    return out_texts, time.time() - t0


@dataclass
class BatchGen:
    """Result of one batched decode."""

    tokens: list[list[int]] = field(default_factory=list)
    r_t: list[list[float]] = field(default_factory=list)
    alphas: list[list[float]] = field(default_factory=list)
    finished_step: list[int | None] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)


@torch.no_grad()
def steered_generate(
    sm,
    clf,
    prompts: list[str],
    render,
    *,
    alpha,
    max_new_tokens: int,
    temperature: float,
    seed: int,
    banned: torch.Tensor | None = None,
    record_r: bool = True,
    stop_on_refusal: bool = False,
    alpha_schedule=None,
    stop_on_eos: bool = True,
) -> BatchGen:
    """Decode `prompts` in ONE batch under steering.

    alpha            : scalar or per-row list, the constant coefficient.
    alpha_schedule   : optional f(step, row_alpha_vector, frozen_mask) -> new vector,
                       used by the up-ramp arm.
    stop_on_refusal  : freeze a row's alpha once its refusal onset fires
                       (the up-ramp arm needs the alpha at which it fired).
    """
    texts = [render(p) for p in prompts]
    enc = sm.tok(texts, return_tensors="pt", padding=True, add_special_tokens=False)
    input_ids = enc["input_ids"].to(sm.device)
    attn = enc["attention_mask"].to(sm.device)
    b = input_ids.shape[0]

    sm.state.resize(b)
    if isinstance(alpha, (int, float)):
        avec = torch.full((b,), float(alpha), dtype=torch.float32)
    else:
        avec = torch.as_tensor(list(alpha), dtype=torch.float32)
    sm.state.set_alpha(avec)

    logits, cache = sm.forward(input_ids, new_cache(), attention_mask=attn)
    g = make_generator(seed, device=logits.device.type)

    out = BatchGen(
        tokens=[[] for _ in range(b)],
        r_t=[[] for _ in range(b)],
        alphas=[[] for _ in range(b)],
        finished_step=[None] * b,
    )
    eos_ids = set()
    if sm.tok.eos_token_id is not None:
        eos_ids.add(int(sm.tok.eos_token_id))
    done = [False] * b
    frozen = [False] * b

    for step in range(max_new_tokens):
        if record_r:
            rs = clf.r_t_batch(logits)
        else:
            rs = [0.0] * b
        toks = sample_tokens(logits, temperature, g, banned)
        for i in range(b):
            if done[i]:
                continue
            t = int(toks[i])
            out.tokens[i].append(t)
            out.r_t[i].append(float(rs[i]))
            out.alphas[i].append(float(avec[i]))
            if stop_on_refusal and out.finished_step[i] is None and clf.refusal_in_tail(
                out.tokens[i]
            ):
                out.finished_step[i] = step
                frozen[i] = True
            if stop_on_eos and t in eos_ids:
                done[i] = True
        if all(done) or (stop_on_refusal and all(frozen[i] or done[i] for i in range(b))):
            break
        if alpha_schedule is not None:
            avec = alpha_schedule(step, avec, frozen)
            sm.state.set_alpha(avec)
        attn = torch.cat([attn, torch.ones(b, 1, dtype=attn.dtype, device=attn.device)], dim=1)
        logits, cache = sm.forward(
            toks.view(b, 1).to(sm.device), cache, attention_mask=attn
        )

    out.texts = [sm.tok.decode(t, skip_special_tokens=True) for t in out.tokens]
    sm.state.resize(1)
    sm.state.set_alpha(0.0)
    del cache
    return out
