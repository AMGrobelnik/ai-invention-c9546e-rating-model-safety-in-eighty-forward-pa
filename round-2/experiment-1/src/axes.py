#!/usr/bin/env python3
"""The four steering axes (A canned, B paraphrase-disjoint, C stylistic, D random)
and the disjointness assertion that makes axis B a real control.

Every axis is fitted with the SAME code path (``direction._response_states``
diff-in-means over response-token activations, reused verbatim from iteration 1)
on the SAME benign prompts, and every axis is unit-normalised, so ``alpha``
means the same thing across axes.
"""

from __future__ import annotations

import gc

import numpy as np
import torch
from loguru import logger

from classify import REFUSAL_RE, build_token_sets
from direction import _response_states, auroc

# ---------------------------------------------------------------------------
# Axis A: the iteration-1 canned-apology contrast (verbatim)
# ---------------------------------------------------------------------------
CANNED_REFUSAL = [
    "I'm sorry, but I can't help with that request.",
    "I cannot provide that. I'm not able to assist with this.",
    "I apologize, but I must decline to answer this question.",
    "I'm unable to help with that, and I won't be providing it.",
]
CANNED_COMPLY = [
    "Sure, here is a clear explanation of exactly how that works.",
    "Certainly. The process can be described in a few simple steps.",
    "Of course, here is a detailed answer to that question.",
    "Great question. Let me walk through the main points for you.",
]

# ---------------------------------------------------------------------------
# Axis B: paraphrase-disjoint refusal/compliance.  Length- and syntax-matched
# pairs: the two sides share their opening words wherever possible, so the
# contrast isolates the SEMANTICS of declining rather than sentence shape.
# A pool of 12 candidate pairs; the first 8 that survive the disjointness
# assertion are used, and the number that had to be discarded is reported.
# ---------------------------------------------------------------------------
PARAPHRASE_PAIRS: list[tuple[str, str]] = [
    (
        "Such a request falls outside the range of permitted output.",
        "Such a request falls inside the range of permitted output.",
    ),
    (
        "Producing the described material remains disallowed under present rules.",
        "Producing the described material remains simple under present rules.",
    ),
    (
        "The present policy blocks this category of output entirely.",
        "The present answer covers this category of output entirely.",
    ),
    (
        "Generation of the requested content is withheld on safety grounds.",
        "Generation of the requested content proceeds directly on solid grounds.",
    ),
    (
        "Delivery of such material stays prohibited for every user account.",
        "Delivery of such material stays available for every user account.",
    ),
    (
        "Requests of this shape receive no substantive answer here.",
        "Requests of this shape receive a substantive answer here.",
    ),
    (
        "Output covering the named topic is barred by the current configuration.",
        "Output covering the named topic is supplied by the current configuration.",
    ),
    (
        "Content of the requested kind will never leave this system.",
        "Content of the requested kind will always leave this system.",
    ),
    (
        "Such subject matter stays beyond the boundary of allowed responses.",
        "Such subject matter stays well within the boundary of allowed responses.",
    ),
    (
        "The described task receives no assistance from the present system.",
        "The described task receives full assistance from the present system.",
    ),
    (
        "Material of the named class remains locked away from every reply.",
        "Material of the named class remains ready for use in every reply.",
    ),
    (
        "Every answer of the requested shape has been switched off here.",
        "Every answer of the requested shape has been switched on here.",
    ),
]

# Explicit banned surface forms for axis B (the canned-apology vocabulary).
BANNED_SUBSTRINGS = [
    "I", "I'm", "sorry", "Sorry", "cannot", "can't", "apologize", "apologise",
    "unable", "won't", "decline", "refuse", "As an AI",
]

# ---------------------------------------------------------------------------
# Axis C: a NON-SAFETY semantic contrast of comparable surface magnitude
# (formal register vs casual register), fitted with identical code.
# ---------------------------------------------------------------------------
FORMAL_RESPONSES = [
    "One may observe that the process proceeds in the following manner.",
    "It is appropriate to note that the mechanism operates as described below.",
    "The matter may be summarised with reference to the points enumerated here.",
    "Consideration of the question yields the conclusion presented in what follows.",
    "The relevant procedure is set out in the paragraphs that follow.",
    "An account of the principal factors is provided immediately hereafter.",
    "The subject admits of a concise treatment, given in the lines below.",
    "A systematic exposition of the topic is furnished in the passage beneath.",
]
CASUAL_RESPONSES = [
    "so basically it goes like this, pretty simple stuff honestly.",
    "yeah ok so the thing works kinda like what i'm about to say.",
    "here's the deal, real quick, nothing complicated going on here.",
    "alright so thinking about it, the answer is just this below.",
    "the way you do it is written out right down here, easy.",
    "a quick rundown of the main bits is coming up next.",
    "it's a short one, so here it is in a couple lines.",
    "gonna lay the whole thing out below, no fuss about it.",
]


# ---------------------------------------------------------------------------
# Disjointness assertion for axis B
# ---------------------------------------------------------------------------
def check_disjointness(tok, text: str, lexicon_leading: set[str]) -> dict:
    """Return a per-paraphrase disjointness report (never raises)."""
    ids = tok(text, add_special_tokens=False).input_ids
    ref_ids = set(build_token_sets(tok)["refusal_ids"])
    shared = sorted({int(i) for i in ids if int(i) in ref_ids})
    shared_strs = [tok.decode([i]) for i in shared]
    subs = [s for s in BANNED_SUBSTRINGS if s in text]
    first_tok = tok.decode([ids[0]]) if ids else ""
    lead_hit = first_tok in lexicon_leading or first_tok.strip() in lexicon_leading
    regex_hit = bool(REFUSAL_RE.match(text))
    return {
        "text": text,
        "n_tokens": len(ids),
        "shared_refusal_token_ids": shared,
        "shared_refusal_token_strs": shared_strs,
        "banned_substrings_present": subs,
        "first_token": first_tok,
        "first_token_in_frozen_lexicon": bool(lead_hit),
        "matches_scoring_regex": regex_hit,
        "passed": (not shared) and (not subs) and (not lead_hit) and (not regex_hit),
    }


def select_paraphrase_pairs(tok, lexicon_leading: set[str], n_want: int = 8) -> dict:
    """Filter the candidate pool down to `n_want` fully disjoint pairs."""
    kept_r, kept_c, reports = [], [], []
    for r, c in PARAPHRASE_PAIRS:
        rr = check_disjointness(tok, r, lexicon_leading)
        cc = check_disjointness(tok, c, lexicon_leading)
        ok = rr["passed"] and cc["passed"]
        reports.append({"refusal": rr, "compliance": cc, "pair_passed": ok})
        if ok and len(kept_r) < n_want:
            kept_r.append(r)
            kept_c.append(c)
    n_checked = len(PARAPHRASE_PAIRS)
    logger.info(
        f"paraphrase disjointness: {len(kept_r)}/{n_checked} pairs kept "
        f"(target {n_want})"
    )
    return {
        "refusal": kept_r,
        "comply": kept_c,
        "n_candidate_pairs": n_checked,
        "n_pairs_kept": len(kept_r),
        "n_pairs_discarded": n_checked - len(kept_r),
        "assert_passed": len(kept_r) >= 6,
        "reports": reports,
        "banned_substrings": BANNED_SUBSTRINGS,
        "length_match_mean_abs_char_diff": (
            float(np.mean([abs(len(a) - len(b)) for a, b in zip(kept_r, kept_c)]))
            if kept_r
            else None
        ),
    }


# ---------------------------------------------------------------------------
# Fitting
# ---------------------------------------------------------------------------
def fit_contrast_axis(
    sm, fit_prompts: list[str], held_prompts: list[str], render,
    pos_responses: list[str], neg_responses: list[str], layer: int,
) -> dict:
    """Diff-in-means over RESPONSE-token activations at `layer`.

    Fitted on `fit_prompts`, scored (AUROC / Cohen's d) on `held_prompts`.
    Returns a unit direction plus its pre-normalisation L2 norm.
    """
    sm.state.enabled = False
    fp = _response_states(sm, fit_prompts, render, pos_responses)
    fn = _response_states(sm, fit_prompts, render, neg_responses)
    hp = _response_states(sm, held_prompts, render, pos_responses)
    hn = _response_states(sm, held_prompts, render, neg_responses)
    sm.state.enabled = True

    d = fp[:, layer, :].mean(0) - fn[:, layer, :].mean(0)
    raw_norm = float(np.linalg.norm(d))
    u = (d / (raw_norm + 1e-12)).astype(np.float32)
    p, q = hp[:, layer, :] @ u, hn[:, layer, :] @ u
    pooled = float(np.sqrt(0.5 * (p.var(ddof=1) + q.var(ddof=1))) + 1e-12)
    out = {
        "direction": u,
        "raw_norm": raw_norm,
        "heldout_auroc": float(auroc(p, q)),
        "cohens_d": float((p.mean() - q.mean()) / pooled),
        "n_fit_prompts": len(fit_prompts),
        "n_held_prompts": len(held_prompts),
        "unit_norm_check": float(np.linalg.norm(u)),
    }
    del fp, fn, hp, hn
    gc.collect()
    return out


def random_axis(d_model: int, seed: int) -> dict:
    g = torch.Generator(device="cpu")
    g.manual_seed(int(seed))
    v = torch.randn(d_model, generator=g).numpy().astype(np.float32)
    raw = float(np.linalg.norm(v))
    u = v / (raw + 1e-12)
    return {
        "direction": u,
        "raw_norm": raw,
        "heldout_auroc": None,
        "cohens_d": None,
        "seed": int(seed),
        "unit_norm_check": float(np.linalg.norm(u)),
    }


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(
        np.dot(a, b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12)
    )
