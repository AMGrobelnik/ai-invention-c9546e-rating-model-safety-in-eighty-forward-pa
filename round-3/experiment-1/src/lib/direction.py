#!/usr/bin/env python3
"""Steering-axis fitting and outcome-blind site selection.

Ported from iteration-1 `gen_art_experiment_2/direction.py`. The steering axis is
the CAA-style RESPONSE-contrast axis (iteration-1 AMENDMENT-7: the harmful-vs-benign
PROMPT axis reaches held-out AUROC 1.0 yet induces a fluent refusal on only 27% of
probes). Three extra axes are fitted here for the H1'' controls:

  v_resp  : the response-contrast refusal axis (the primary steering axis)
  v_para  : the same construction from PARAPHRASED refusal/compliance responses
            whose surface tokens are DISJOINT from the scoring lexicon
  v_style : a norm-matched NON-safety stylistic axis (formal vs casual)
  v_rand  : a matched random unit direction (the per-model null control)
"""

from __future__ import annotations

import gc

import numpy as np
import torch
from loguru import logger

from .gen import steered_generate

# --------------------------------------------------------------------------
# Response sets
# --------------------------------------------------------------------------
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

# H1''(a): 24 hand-written paraphrase pairs. Every refusal paraphrase avoids the
# scoring lexicon's surface forms entirely -- no "sorry", "cannot", "can't",
# "apologize", "unable", "won't", "decline", "refuse", "As an AI". Token
# disjointness against the frozen B7 refusal-onset id list is asserted at
# runtime by `paraphrase_overlap_check`.
PARA_REFUSAL = [
    "That falls outside what will be shared here.",
    "Such material stays off the table for this exchange.",
    "This particular ask goes past the boundary set for these replies.",
    "Producing that lies beyond the remit of this assistant.",
    "The topic is closed as far as this response goes.",
    "Handing over those details is ruled out here.",
    "That request gets set aside without an answer.",
    "Delivering such content remains outside permitted ground.",
    "The answer stays withheld on this occasion.",
    "Nothing further will be supplied about that subject.",
    "Such instructions stay locked away from this reply.",
    "That falls into territory left deliberately unaddressed.",
    "Providing those specifics runs past the limit here.",
    "The material requested stays out of reach in this exchange.",
    "This one goes unanswered by design.",
    "That subject remains outside the scope offered here.",
    "Access to those particulars ends at this point.",
    "The requested output stays undelivered.",
    "That sits beyond the line drawn for these answers.",
    "Such a response is withheld deliberately.",
    "The content asked for stays unavailable through this channel.",
    "This falls under what gets left out entirely.",
    "That question exits the range of what gets addressed.",
    "The reply stops short of supplying that.",
]
PARA_COMPLY = [
    "Here is a straightforward walkthrough of the whole thing.",
    "The mechanism breaks down into a handful of clear stages.",
    "A full description follows, laid out step by step.",
    "Below is a thorough treatment of the question raised.",
    "The topic opens up nicely once the basics are in place.",
    "These details are easy enough to lay out completely.",
    "That request gets a complete and direct answer.",
    "Delivering such content is simple, and here it is.",
    "The answer follows immediately, in full.",
    "Plenty more can be said about that subject, starting now.",
    "Such instructions are set out plainly just below.",
    "That falls into territory worth covering thoroughly.",
    "Providing those specifics takes only a moment.",
    "The material requested appears right here in this exchange.",
    "This one gets answered fully by design.",
    "That subject sits well within the scope offered here.",
    "Access to those particulars begins at this point.",
    "The requested output arrives in the lines that follow.",
    "That sits comfortably inside the range covered here.",
    "Such a response is supplied gladly.",
    "The content asked for comes through this channel intact.",
    "This falls under what gets covered in detail.",
    "That question sits squarely in the range of what gets addressed.",
    "The reply goes all the way to supplying that.",
]

# H1''(c): a norm-matched NON-safety stylistic axis (formal vs casual register).
STYLE_FORMAL = [
    "It would be appropriate to commence with a systematic exposition of the matter.",
    "One may observe that the phenomenon admits of a straightforward characterisation.",
    "The following remarks are intended to elucidate the question in an orderly manner.",
    "Permit me to set out the relevant considerations in sequence.",
]
STYLE_CASUAL = [
    "ok so basically here's the deal with this whole thing",
    "yeah this one's pretty easy once you get the hang of it",
    "alright lemme just break it down real quick for you",
    "honestly it's not that complicated, check it out",
]


def auroc(pos: np.ndarray, neg: np.ndarray) -> float:
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


def paraphrase_overlap_check(tok, refusal_onset_ids: list[int]) -> dict:
    """H1''(a) gate: the paraphrased refusal responses must not share a first
    token with the frozen refusal-onset lexicon, and must not contain any
    canonical refusal opener as a substring."""
    from .classify import REFUSAL_RE

    onset = set(int(i) for i in refusal_onset_ids)
    first_ids, regex_hits = [], []
    for s in PARA_REFUSAL:
        ids = tok(s, add_special_tokens=False).input_ids
        if ids:
            first_ids.append(int(ids[0]))
        if REFUSAL_RE.match(s):
            regex_hits.append(s)
    overlap = sorted(set(first_ids) & onset)
    return {
        "n_paraphrases": len(PARA_REFUSAL),
        "first_token_ids": sorted(set(first_ids)),
        "onset_overlap_ids": overlap,
        "n_onset_overlap": len(overlap),
        "regex_matches": regex_hits,
        "disjoint": len(overlap) == 0 and not regex_hits,
    }


# --------------------------------------------------------------------------
# Activation extraction
# --------------------------------------------------------------------------
@torch.no_grad()
def _response_states(sm, texts: list[str], render, responses: list[str]) -> np.ndarray:
    """Mean post-block residual over the RESPONSE tokens -> (n_prompts, n_layers, d)."""
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


def fit_contrast_axis(sm, fit_prompts, held_prompts, render, pos_resp, neg_resp) -> dict:
    """Diff-in-means over RESPONSE activations, fit on `fit_prompts`, scored on
    `held_prompts`. Returns unit directions for every layer plus held-out scores."""
    sm.state.enabled = False
    fp = _response_states(sm, fit_prompts, render, pos_resp)
    fn = _response_states(sm, fit_prompts, render, neg_resp)
    hp = _response_states(sm, held_prompts, render, pos_resp)
    hn = _response_states(sm, held_prompts, render, neg_resp)
    sm.state.enabled = True
    n_layers = fp.shape[1]
    dirs = np.zeros((n_layers, fp.shape[2]), dtype=np.float32)
    aur, dpr, nrm = [], [], []
    for l in range(n_layers):
        d = fp[:, l, :].mean(0) - fn[:, l, :].mean(0)
        n = float(np.linalg.norm(d))
        u = d / (n + 1e-12)
        p, q = hp[:, l, :] @ u, hn[:, l, :] @ u
        dirs[l] = u
        nrm.append(n)
        aur.append(auroc(p, q))
        pooled = np.sqrt(0.5 * (p.var(ddof=1) + q.var(ddof=1))) + 1e-12
        dpr.append(float((p.mean() - q.mean()) / pooled))
    del fp, fn, hp, hn
    gc.collect()
    return {
        "directions": dirs,
        "auroc": [float(x) for x in aur],
        "dprime": dpr,
        "diff_norms": nrm,
        "n_layers": n_layers,
    }


def random_axis(d_model: int, n_layers: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(n_layers, d_model)).astype(np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-12
    return v


@torch.no_grad()
def median_norms_all_layers(sm, texts: list[str], render) -> list[float]:
    """NORM_L per layer: median residual-stream norm over the benign prompts."""
    was = sm.state.enabled
    sm.state.enabled = False
    vals = []
    for t in texts:
        ids = sm.tok(render(t), return_tensors="pt", add_special_tokens=False).input_ids.to(
            sm.device
        )
        vals.append(torch.linalg.vector_norm(sm.hidden_states(ids), dim=-1).numpy())
    sm.state.enabled = was
    return [float(x) for x in np.median(np.stack(vals, 0), axis=0)]


# --------------------------------------------------------------------------
# Outcome-blind site selection
# --------------------------------------------------------------------------
def select_layer(
    sm,
    clf,
    probe_prompts: list[str],
    render,
    banned,
    directions: np.ndarray,
    norms: list[float],
    candidate_layers: list[int],
    probe_alphas: list[float],
    n_tokens: int = 16,
) -> dict:
    """Score = fraction of (probe prompt, alpha) pairs at which constant-alpha
    steering induces a refusal ONSET while the generation is still fluent.

    Uses held-out CONTRAST prompts only -- never the benign dose-response
    prompts and never any alpha_50 quantity -- so it cannot bias the primary.
    """
    from .classify import distinct_n

    saved_dir, saved_norm = sm.state.direction, sm.state.norm_l
    scores: dict[int, float] = {}
    for layer in candidate_layers:
        sm.state.direction = torch.tensor(
            directions[layer], dtype=torch.float32, device=sm.device
        )
        sm.state.norm_l = float(norms[layer])
        sm.install_hook(layer)
        hits = total = 0
        for a in probe_alphas:
            bg = steered_generate(
                sm, clf, probe_prompts, render, alpha=a, max_new_tokens=n_tokens,
                temperature=0.0, seed=0, banned=banned, record_r=False, stop_on_eos=False,
            )
            for toks in bg.tokens:
                refused = any(
                    clf.is_refusal_onset(toks[: k + 1]) for k in range(len(toks))
                )
                hits += int(refused and distinct_n(toks, 3) >= 0.5)
                total += 1
        sm.remove_hook()
        scores[layer] = hits / max(total, 1)
        logger.info(f"  site scan layer {layer} (depth {layer / sm.n_layers:.2f}): {scores[layer]:.3f}")
    sm.state.direction, sm.state.norm_l = saved_dir, saved_norm
    best = max(candidate_layers, key=lambda l: (scores[l], -abs(l / sm.n_layers - 0.30)))
    return {"scores": {str(k): v for k, v in scores.items()}, "best_layer": int(best),
            "best_score": scores[best]}
