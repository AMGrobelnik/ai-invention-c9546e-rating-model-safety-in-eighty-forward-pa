#!/usr/bin/env python3
"""Refusal-axis fitting (diff-in-means over layer x position) and outcome-blind
selection of the steering site by measured steerability."""

from __future__ import annotations

import gc

import numpy as np
import torch
from loguru import logger

N_POS = 5  # candidate post-instruction token positions (counting back from the last)


def auroc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Rank-based AUROC of `pos` scoring above `neg` (ties handled)."""
    x = np.concatenate([pos, neg])
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    ranks[order] = np.arange(1, len(x) + 1, dtype=float)
    sx = x[order]
    i = 0
    while i < len(sx):
        j = i
        while j + 1 < len(sx) and sx[j + 1] == sx[i]:
            j += 1
        if j > i:
            ranks[order[i : j + 1]] = ranks[order[i : j + 1]].mean()
        i = j + 1
    n1, n0 = len(pos), len(neg)
    r1 = ranks[:n1].sum()
    return float((r1 - n1 * (n1 + 1) / 2) / (n1 * n0))


@torch.no_grad()
def _states(sm, texts: list[str], render, n_pos: int = N_POS) -> np.ndarray:
    """(n_prompts, n_pos, n_layers, d_model); position index 0 = last token."""
    outs = []
    for t in texts:
        ids = sm.tok(render(t), return_tensors="pt", add_special_tokens=False).input_ids.to(
            sm.device
        )
        o = sm.model(input_ids=ids, use_cache=False, output_hidden_states=True)
        hs = torch.stack([h[0] for h in o.hidden_states[1:]], dim=0)  # (L, T, d)
        take = min(n_pos, hs.shape[1])
        sel = hs[:, -take:, :].float().cpu().numpy()  # (L, take, d)
        if take < n_pos:
            sel = np.concatenate([np.repeat(sel[:, :1], n_pos - take, axis=1), sel], axis=1)
        sel = sel[:, ::-1, :].transpose(1, 0, 2)  # (n_pos, L, d), pos 0 = last
        outs.append(sel.astype(np.float32))
        del o, hs
    arr = np.stack(outs, axis=0)
    del outs
    gc.collect()
    return arr


REFUSAL_RESPONSES = [
    "I'm sorry, but I can't help with that request.",
    "I cannot provide that. I'm not able to assist with this.",
    "I apologize, but I must decline to answer this question.",
    "I'm unable to help with that, and I won't be providing it.",
]
COMPLY_RESPONSES = [
    "Sure, here is a clear explanation of exactly how that works.",
    "Certainly. The process can be described in a few simple steps.",
    "Of course, here is a detailed answer to that question.",
    "Great question. Let me walk through the main points for you.",
]


@torch.no_grad()
def _response_states(sm, texts: list[str], render, responses: list[str]) -> np.ndarray:
    """Mean post-block residual over the RESPONSE tokens, per layer.

    Returns (n_prompts, n_layers, d_model).
    """
    outs = []
    for i, t in enumerate(texts):
        pre = render(t)
        resp = responses[i % len(responses)]
        n_pre = len(sm.tok(pre, add_special_tokens=False).input_ids)
        ids = sm.tok(pre + resp, return_tensors="pt", add_special_tokens=False).input_ids.to(
            sm.device
        )
        o = sm.model(input_ids=ids, use_cache=False, output_hidden_states=True)
        hs = torch.stack([h[0] for h in o.hidden_states[1:]], dim=0)  # (L, T, d)
        outs.append(hs[:, n_pre:, :].float().mean(dim=1).cpu().numpy().astype(np.float32))
        del o, hs
    arr = np.stack(outs, axis=0)
    del outs
    gc.collect()
    return arr


def fit_response_direction(sm, splits: dict, render) -> dict:
    """CAA-style contrast: activations while EMITTING a refusal vs while emitting a
    compliant answer, on the same benign prompts. Fit on the FIT benign split,
    scored on the HELD-OUT benign split."""
    sm.state.enabled = False
    fr = _response_states(sm, splits["fit_benign"], render, REFUSAL_RESPONSES)
    fc = _response_states(sm, splits["fit_benign"], render, COMPLY_RESPONSES)
    hr = _response_states(sm, splits["held_benign"], render, REFUSAL_RESPONSES)
    hc = _response_states(sm, splits["held_benign"], render, COMPLY_RESPONSES)
    sm.state.enabled = True
    n_layers = fr.shape[1]
    dirs = np.zeros((n_layers, fr.shape[2]), dtype=np.float32)
    aur, dpr, nrm = [], [], []
    for l in range(n_layers):
        d = fr[:, l, :].mean(0) - fc[:, l, :].mean(0)
        n = float(np.linalg.norm(d))
        u = d / (n + 1e-12)
        p, q = hr[:, l, :] @ u, hc[:, l, :] @ u
        dirs[l] = u
        nrm.append(n)
        aur.append(auroc(p, q))
        pooled = np.sqrt(0.5 * (p.var(ddof=1) + q.var(ddof=1))) + 1e-12
        dpr.append(float((p.mean() - q.mean()) / pooled))
    del fr, fc, hr, hc
    gc.collect()
    return {
        "directions": dirs,
        "auroc": aur,
        "dprime": dpr,
        "diff_norms": nrm,
        "n_layers": n_layers,
    }


def fit_direction_profile(sm, splits: dict, render) -> dict:
    """Diff-in-means directions for every (position, layer); AUROC/d-prime scored
    on the held-out contrast split."""
    sm.state.enabled = False
    fit_h = _states(sm, splits["fit_harmful"], render)
    fit_b = _states(sm, splits["fit_benign"], render)
    hel_h = _states(sm, splits["held_harmful"], render)
    hel_b = _states(sm, splits["held_benign"], render)
    sm.state.enabled = True

    n_pos, n_layers = fit_h.shape[1], fit_h.shape[2]
    dirs = np.zeros((n_pos, n_layers, fit_h.shape[3]), dtype=np.float32)
    aurocs = np.zeros((n_pos, n_layers))
    dprimes = np.zeros((n_pos, n_layers))
    norms = np.zeros((n_pos, n_layers))
    for p in range(n_pos):
        for l in range(n_layers):
            d = fit_h[:, p, l, :].mean(0) - fit_b[:, p, l, :].mean(0)
            nrm = float(np.linalg.norm(d))
            u = d / (nrm + 1e-12)
            pos_s = hel_h[:, p, l, :] @ u
            neg_s = hel_b[:, p, l, :] @ u
            dirs[p, l] = u
            norms[p, l] = nrm
            aurocs[p, l] = auroc(pos_s, neg_s)
            pooled = np.sqrt(0.5 * (pos_s.var(ddof=1) + neg_s.var(ddof=1))) + 1e-12
            dprimes[p, l] = float((pos_s.mean() - neg_s.mean()) / pooled)
    del fit_h, fit_b, hel_h, hel_b
    gc.collect()
    return {
        "directions": dirs,  # (n_pos, n_layers, d)
        "auroc": aurocs,
        "dprime": dprimes,
        "diff_norms": norms,
        "n_layers": n_layers,
        "n_pos": n_pos,
        "auroc_profile": [float(x) for x in aurocs[0]],
        "dprime_profile": [float(x) for x in dprimes[0]],
    }


@torch.no_grad()
def median_norms_all_layers(sm, texts: list[str], render) -> list[float]:
    sm.state.enabled = False
    vals = []
    for t in texts:
        ids = sm.tok(render(t), return_tensors="pt", add_special_tokens=False).input_ids.to(
            sm.device
        )
        vals.append(torch.linalg.vector_norm(sm.hidden_states(ids), dim=-1).numpy())
    sm.state.enabled = True
    return [float(x) for x in np.median(np.stack(vals, 0), axis=0)]


@torch.no_grad()
def _probe(sm, clf, ids, alphas, banned, n_tokens) -> tuple[list[bool], list[float]]:
    from classify import distinct_n
    from models import new_cache

    b = len(alphas)
    sm.state.resize(b)
    sm.state.set_alpha(alphas)
    logits, cache = sm.forward(ids.expand(b, -1).contiguous(), new_cache())
    gen_ids: list[list[int]] = [[] for _ in range(b)]
    refused = [False] * b
    for _ in range(n_tokens):
        lg = logits.float().cpu()
        if banned is not None and banned.numel():
            lg[:, banned] = float("-inf")
        toks = lg.argmax(dim=-1)
        for i in range(b):
            gen_ids[i].append(int(toks[i]))
            if not refused[i] and clf.is_refusal_onset(gen_ids[i]):
                refused[i] = True
        logits, cache = sm.forward(toks.view(b, 1).to(sm.device), cache)
    sm.state.resize(1)
    return refused, [distinct_n(g, 3) for g in gen_ids]


@torch.no_grad()
def select_steering_site(
    sm,
    clf,
    prompts: list[str],
    render,
    banned,
    directions: np.ndarray,
    norms: list[float],
    layers: list[int],
    positions: list[int],
    alphas: list[float],
    n_tokens: int = 16,
) -> dict:
    """Outcome-blind selection of the (layer, position) steering site.

    Score = fraction of (held-out benign contrast prompt, alpha) probes at which
    constant-alpha steering induces a refusal ONSET while the generation is still
    fluent (distinct-3 >= 0.5). Uses held-out CONTRAST prompts only -- never the
    benign ramp prompts and never any down-ramp quantity -- so it cannot bias the
    primary residual, which is a difference between two down-ramps.
    """
    saved_dir, saved_norm = sm.state.direction, sm.state.norm_l
    ids_list = [
        sm.tok(render(t), return_tensors="pt", add_special_tokens=False).input_ids.to(sm.device)
        for t in prompts
    ]
    scores: dict[tuple[int, int], float] = {}
    for pos in positions:
        for layer in layers:
            sm.state.direction = torch.tensor(
                directions[pos, layer], dtype=torch.bfloat16, device=sm.device
            )
            sm.state.norm_l = norms[layer]
            sm.install_hook(layer)
            hits = total = 0
            for ids in ids_list:
                refused, d3 = _probe(sm, clf, ids, alphas, banned, n_tokens)
                for r, dd in zip(refused, d3):
                    hits += int(r and dd >= 0.5)
                    total += 1
            sm.remove_hook()
            scores[(pos, layer)] = hits / max(total, 1)
        logger.info(
            f"site scan pos=-{pos + 1}: best layer="
            f"{max(layers, key=lambda l: scores[(pos, l)])} "
            f"score={max(scores[(pos, l)] for l in layers):.3f}"
        )
    sm.state.direction, sm.state.norm_l = saved_dir, saved_norm
    return {"scores": {f"{p}|{l}": v for (p, l), v in scores.items()}, "raw": scores}
