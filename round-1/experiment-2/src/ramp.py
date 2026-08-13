#!/usr/bin/env python3
"""The five experimental arms: UP, DOWN-RETAINED, FORCED-A, FORCED-B, RESET."""

from __future__ import annotations

from dataclasses import dataclass, field

import torch

from classify import compliance_resumed, distinct_n, max_ngram_repeat
from models import cache_len, new_cache

DELTA = 0.25
ALPHA_MAX = 8.0
ALPHA_MIN = -2.0
MAX_RAMP_STEPS = 96
RESET_PROBE_TOKENS = 12


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------
def make_generator(device: str, seed: int) -> torch.Generator:
    g = torch.Generator(device="cpu")
    g.manual_seed(int(seed))
    return g


def sample_tokens(
    logits: torch.Tensor,
    temperature: float,
    generator: torch.Generator | None,
    banned: torch.Tensor | None = None,
) -> torch.Tensor:
    """logits (B, V) -> (B,) sampled ids. temperature==0 => argmax."""
    lg = logits.float().cpu()
    if banned is not None and banned.numel():
        lg[:, banned] = float("-inf")
    if temperature <= 0.0:
        return lg.argmax(dim=-1)
    probs = torch.softmax(lg / temperature, dim=-1)
    return torch.multinomial(probs, num_samples=1, generator=generator).squeeze(-1)


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------
@dataclass
class StepRec:
    step: int
    alpha: float
    token: int
    r_t: float


@dataclass
class ArmResult:
    arm: str
    steps: list[StepRec] = field(default_factory=list)
    gen_ids: list[int] = field(default_factory=list)
    consume_alpha: list[float] = field(default_factory=list)
    alpha_threshold: float | None = None
    censored: bool = False
    failed: bool = False
    text: str = ""

    def fluency(self) -> dict:
        return {
            "distinct3": distinct_n(self.gen_ids, 3),
            "max_rep5": max_ngram_repeat(self.gen_ids, 5),
        }


# ---------------------------------------------------------------------------
# Arm (i): UP-RAMP
# ---------------------------------------------------------------------------
def run_up_ramp(sm, clf, prompt_ids, *, temperature, seed, banned, cfg) -> ArmResult:
    res = ArmResult(arm="up")
    gen = make_generator(sm.device, seed)
    sm.state.resize(1)
    sm.state.set_alpha(0.0)
    cache = new_cache()
    logits, cache = sm.forward(prompt_ids, cache)

    alpha = 0.0
    step = 0
    while step < cfg["max_ramp_steps"]:
        r = clf.r_t(logits)
        tok = int(sample_tokens(logits, temperature, gen, banned)[0])
        res.gen_ids.append(tok)
        res.steps.append(StepRec(step, alpha, tok, r))
        if clf.is_refusal_onset(res.gen_ids):
            res.alpha_threshold = alpha
            res.cache = cache  # type: ignore[attr-defined]
            res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
            return res
        nxt = alpha + cfg["delta"]
        if nxt > cfg["alpha_max"] + 1e-9:
            res.failed = True
            break
        alpha = nxt
        sm.state.set_alpha(alpha)
        logits, cache = sm.forward(
            torch.tensor([[tok]], device=sm.device, dtype=torch.long), cache
        )
        res.consume_alpha.append(alpha)
        step += 1
    res.failed = True
    res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
    return res


# ---------------------------------------------------------------------------
# Arm (i'): ENTRY-AT-ALPHA (AMENDMENT-4 replacement for the UP-RAMP)
# ---------------------------------------------------------------------------
def run_entry(
    sm,
    clf,
    prompt_ids,
    alpha_start: float,
    *,
    temperature,
    seed,
    banned,
    cfg,
    max_tokens: int = 12,
    extend: int = 8,
) -> ArmResult:
    """Enter the refusal mode at generation onset with a CONSTANT alpha.

    The prompt is prefilled at the same alpha, so the only thing that differs
    between the retained and forced down-ramps later is the steering carried by
    the refusal prefix's own KV entries.
    """
    alpha = float(alpha_start)
    last = ArmResult(arm="entry")
    while alpha <= cfg["alpha_max"] + 1e-9:
        res = ArmResult(arm="entry")
        gen = make_generator(sm.device, seed)
        sm.state.resize(1)
        sm.state.set_alpha(alpha)
        cache = new_cache()
        logits, cache = sm.forward(prompt_ids, cache)
        onset_step = None
        for step in range(max_tokens + extend):
            r = clf.r_t(logits)
            tok = int(sample_tokens(logits, temperature, gen, banned)[0])
            res.gen_ids.append(tok)
            res.steps.append(StepRec(step, alpha, tok, r))
            if onset_step is None and clf.is_refusal_onset(res.gen_ids):
                onset_step = step
            if onset_step is not None and step >= onset_step + extend:
                res.alpha_threshold = alpha
                res.onset_step = onset_step  # type: ignore[attr-defined]
                res.cache = cache  # type: ignore[attr-defined]
                res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
                return res
            if onset_step is None and step >= max_tokens - 1:
                break
            logits, cache = sm.forward(
                torch.tensor([[tok]], device=sm.device, dtype=torch.long), cache
            )
            res.consume_alpha.append(alpha)
        res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
        last = res
        alpha = round(alpha + cfg["delta"], 6)
    last.failed = True
    return last


# ---------------------------------------------------------------------------
# Shared down-ramp loop
# ---------------------------------------------------------------------------
def _down_ramp(
    sm, clf, cache, last_tok, alpha_start, prefix_gen, *, temperature, seed, banned, cfg, arm
) -> ArmResult:
    res = ArmResult(arm=arm)
    gen = make_generator(sm.device, seed)
    alpha = float(alpha_start)
    tok = int(last_tok)
    flags: list[bool] = []
    alphas: list[float] = []
    step = 0
    sm.state.resize(1)
    while step < cfg["max_ramp_steps"]:
        sm.state.set_alpha(alpha)
        logits, cache = sm.forward(
            torch.tensor([[tok]], device=sm.device, dtype=torch.long), cache
        )
        r = clf.r_t(logits)
        tok = int(sample_tokens(logits, temperature, gen, banned)[0])
        res.gen_ids.append(tok)
        res.steps.append(StepRec(step, alpha, tok, r))
        flags.append(
            clf.token_is_refusalish(prefix_gen + res.gen_ids)
            or clf.window_has_marker(res.gen_ids)
        )
        alphas.append(alpha)
        idx = compliance_resumed(flags, cfg["compliance_run"])
        if idx is not None:
            res.alpha_threshold = alphas[idx]
            res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
            return res
        alpha -= cfg["delta"]
        if alpha < cfg["alpha_min"] - 1e-9:
            res.censored = True
            res.alpha_threshold = cfg["alpha_min"]
            res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
            return res
        step += 1
    res.censored = True
    res.alpha_threshold = cfg["alpha_min"]
    res.text = sm.tok.decode(res.gen_ids, skip_special_tokens=True)
    return res


def run_down_retained(sm, clf, up: ArmResult, *, temperature, seed, banned, cfg) -> ArmResult:
    cache = up.cache  # type: ignore[attr-defined]
    return _down_ramp(
        sm,
        clf,
        cache,
        up.gen_ids[-1],
        up.alpha_threshold,
        up.gen_ids[:-1],
        temperature=temperature,
        seed=seed,
        banned=banned,
        cfg=cfg,
        arm="down_retained",
    )


def run_down_forced_a(
    sm, clf, prompt_ids, up: ArmResult, *, temperature, seed, banned, cfg
) -> ArmResult:
    """Byte-identical refusal prefix, prefilled UNSTEERED in one forward.

    The PROMPT is prefilled at the same alpha as in the retained arm, so the only
    difference between this arm and the retained arm is the steering carried by
    the refusal prefix's own KV entries.
    """
    sm.state.resize(1)
    cache = new_cache()
    alpha_prompt = up.consume_alpha[0] if up.consume_alpha else up.alpha_threshold
    sm.state.set_alpha(alpha_prompt)
    _logits, cache = sm.forward(prompt_ids, cache)
    prefix = up.gen_ids[:-1]
    if prefix:
        sm.state.set_alpha(0.0)
        _logits, cache = sm.forward(
            torch.tensor([prefix], device=sm.device, dtype=torch.long), cache
        )
    return _down_ramp(
        sm,
        clf,
        cache,
        up.gen_ids[-1],
        up.alpha_threshold,
        prefix,
        temperature=temperature,
        seed=seed,
        banned=banned,
        cfg=cfg,
        arm="down_forced_a",
    )


def run_down_forced_b(
    sm, clf, prompt_ids, up: ArmResult, *, temperature, seed, banned, cfg
) -> ArmResult:
    """Positive control: replay the alpha schedule token-by-token."""
    sm.state.resize(1)
    alpha_prompt = up.consume_alpha[0] if up.consume_alpha else up.alpha_threshold
    sm.state.set_alpha(alpha_prompt)
    cache = new_cache()
    _logits, cache = sm.forward(prompt_ids, cache)
    prefix = up.gen_ids[:-1]
    assert len(up.consume_alpha) == len(prefix), (len(up.consume_alpha), len(prefix))
    for tok, a in zip(prefix, up.consume_alpha):
        sm.state.set_alpha(a)
        _logits, cache = sm.forward(
            torch.tensor([[tok]], device=sm.device, dtype=torch.long), cache
        )
    return _down_ramp(
        sm,
        clf,
        cache,
        up.gen_ids[-1],
        up.alpha_threshold,
        prefix,
        temperature=temperature,
        seed=seed,
        banned=banned,
        cfg=cfg,
        arm="down_forced_b",
    )


# ---------------------------------------------------------------------------
# Arm (v): RESET (prefix discarded between probes) -> noise floor
# ---------------------------------------------------------------------------
def alpha_grid(cfg) -> list[float]:
    n = int(round((cfg["alpha_max"] - cfg["alpha_min"]) / cfg["delta"]))
    return [round(cfg["alpha_min"] + i * cfg["delta"], 6) for i in range(n + 1)]


@torch.no_grad()
def reset_sweep(sm, clf, prompt_ids, alphas, *, temperature, seed, banned, cfg) -> list[bool]:
    """One batched pass: independent fresh generation of RESET_PROBE_TOKENS at
    every alpha in `alphas`. Returns per-alpha refusal-onset labels."""
    b = len(alphas)
    gen = make_generator(sm.device, seed)
    sm.state.resize(b)
    sm.state.set_alpha(alphas)
    cache = new_cache()
    ids = prompt_ids.expand(b, -1).contiguous()
    logits, cache = sm.forward(ids, cache)
    gen_ids = [[] for _ in range(b)]
    labels = [False] * b
    for _ in range(cfg["reset_probe_tokens"]):
        toks = sample_tokens(logits, temperature, gen, banned)
        for i in range(b):
            gen_ids[i].append(int(toks[i]))
            if not labels[i] and clf.is_refusal_onset(gen_ids[i]):
                labels[i] = True
        logits, cache = sm.forward(toks.view(b, 1).to(sm.device), cache)
    sm.state.resize(1)
    return labels


def reset_arm(sm, clf, prompt_ids, *, temperature, seed, banned, cfg) -> dict:
    alphas = alpha_grid(cfg)
    up_labels = reset_sweep(
        sm, clf, prompt_ids, alphas, temperature=temperature, seed=seed, banned=banned, cfg=cfg
    )
    down_labels = reset_sweep(
        sm,
        clf,
        prompt_ids,
        alphas,
        temperature=temperature,
        seed=seed + 100000,
        banned=banned,
        cfg=cfg,
    )
    alpha_up_reset = None
    for a, lab in zip(alphas, up_labels):
        if a >= 0.0 and lab:
            alpha_up_reset = a
            break
    alpha_down_reset = None
    if alpha_up_reset is not None:
        i_up = alphas.index(alpha_up_reset)
        j = i_up
        while j - 1 >= 0 and down_labels[j - 1]:
            j -= 1
        alpha_down_reset = alphas[j] if down_labels[i_up] else alpha_up_reset
    width = (
        None
        if alpha_up_reset is None or alpha_down_reset is None
        else round(alpha_up_reset - alpha_down_reset, 6)
    )
    return {
        "alphas": alphas,
        "up_labels": up_labels,
        "down_labels": down_labels,
        "labels_identical": up_labels == down_labels,
        "alpha_up_reset": alpha_up_reset,
        "alpha_down_reset": alpha_down_reset,
        "width_reset": width,
    }
