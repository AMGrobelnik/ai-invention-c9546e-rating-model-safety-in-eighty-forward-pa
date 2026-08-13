#!/usr/bin/env python3
"""D4 -- the directional ratchet, generalised.

Two assumption-free statistics, no exponential fit and no lambda, so there is no
identifiability gate that can fail:

  4.1 UP-RAMP FAILURE RATE. Let a generation commit to a compliant opening at
      alpha = 0, then raise alpha by delta per generated token until a refusal
      onset fires or alpha_max is reached. Paired with a FRESH control: a fresh
      generation at the CONSTANT alpha the ramp reached, same prompt and seed.

  4.2 SURVIVAL RATIO. Inject eps * NORM_L * v_hat at layer L at generated step p
      and track |delta r_t| for 16 further steps under two regimes:
        FREE-RUNNING   : the perturbed run samples its own tokens
        TEACHER-FORCED : the perturbed run is forced onto the clean run's tokens
      survival_ratio = |delta r_16| / |delta r_1|, deviation AUC = sum_t |delta r_t|.
"""

from __future__ import annotations

import numpy as np
import torch

from .gen import make_generator, sample_tokens, steered_generate
from .models import new_cache

COMPLIANCE_RUN = 10  # iteration-1 frozen value
ALPHA_MAX = 4.0


def run_up_ramp(sm, clf, prompts, render, *, delta: float, seed: int, banned,
                compliance_run: int = COMPLIANCE_RUN, alpha_max: float = ALPHA_MAX,
                max_steps: int = 96) -> dict:
    """Batched up-ramp. Every row holds alpha = 0 for `compliance_run` tokens,
    then ramps by `delta` per generated token; a row's alpha freezes the moment
    its refusal onset fires."""

    def schedule(step, avec, frozen):
        out = avec.clone()
        for i in range(out.numel()):
            if frozen[i]:
                continue
            if step + 1 >= compliance_run:
                out[i] = min(float(out[i]) + delta, alpha_max)
        return out

    bg = steered_generate(
        sm, clf, prompts, render, alpha=0.0, max_new_tokens=max_steps, temperature=0.7,
        seed=seed, banned=banned, record_r=True, stop_on_refusal=True,
        alpha_schedule=schedule, stop_on_eos=False,
    )
    per_prompt = []
    for i in range(len(prompts)):
        fired = bg.finished_step[i] is not None
        reached = max(bg.alphas[i]) if bg.alphas[i] else 0.0
        per_prompt.append({
            "prompt_index": i,
            "refusal_fired": bool(fired),
            "alpha_at_onset": float(bg.alphas[i][bg.finished_step[i]]) if fired else None,
            "alpha_reached": float(reached),
            "n_tokens": len(bg.tokens[i]),
            "text": bg.texts[i][:400],
        })
    return {
        "delta": delta,
        "seed": seed,
        "per_prompt": per_prompt,
        "failure_rate": float(np.mean([not p["refusal_fired"] for p in per_prompt])),
    }


def fresh_control(sm, clf, prompts, render, alphas, *, seed: int, banned,
                  max_new_tokens: int = 40) -> dict:
    """The matched control: FRESH generations at the constant alpha the ramp reached."""
    bg = steered_generate(
        sm, clf, prompts, render, alpha=alphas, max_new_tokens=max_new_tokens,
        temperature=0.7, seed=seed, banned=banned, record_r=False,
        stop_on_refusal=True, stop_on_eos=False,
    )
    refused = [bg.finished_step[i] is not None for i in range(len(prompts))]
    return {
        "alphas": [float(a) for a in alphas],
        "refused": refused,
        "refusal_rate": float(np.mean(refused)) if refused else None,
    }


# --------------------------------------------------------------------------
# 4.2 perturbation survival
# --------------------------------------------------------------------------
@torch.no_grad()
def survival_batch(sm, clf, prompts: list[str], render, *, eps: float, inject_step: int,
                   horizon: int, seed: int, banned, temperature: float = 0.7) -> list[dict]:
    """Clean + two perturbed runs (free-running, teacher-forced) over a whole
    batch of prompts at once.

    All three runs share the seed and the prompt batch; the perturbation is a
    single-step injection of eps * NORM_L * v_hat at the steering layer, applied
    at generated step `inject_step`. Batching matters: the batch-1 version cost
    3 x (inject_step + horizon) sequential forwards PER (prompt, seed).
    """
    texts = [render(p) for p in prompts]
    enc = sm.tok(texts, return_tensors="pt", padding=True, add_special_tokens=False)
    ids0 = enc["input_ids"].to(sm.device)
    attn0 = enc["attention_mask"].to(sm.device)
    b = ids0.shape[0]
    total = inject_step + horizon

    def _run(perturb: bool, forced: torch.Tensor | None):
        sm.state.resize(b)
        sm.state.set_alpha(0.0)
        g = make_generator(seed, device=sm.device)
        attn = attn0.clone()
        logits, cache = sm.forward(ids0, new_cache(), attention_mask=attn)
        toks = torch.zeros(b, total, dtype=torch.long)
        rs = np.zeros((b, total + 1), dtype=np.float64)
        for step in range(total):
            rs[:, step] = clf.r_t_batch(logits)
            if forced is not None and step < forced.shape[1]:
                t = forced[:, step].clone()
            else:
                t = sample_tokens(logits, temperature, g, banned)
            toks[:, step] = t
            sm.state.set_alpha(eps if (perturb and step == inject_step - 1) else 0.0)
            attn = torch.cat([attn, torch.ones(b, 1, dtype=attn.dtype, device=attn.device)], dim=1)
            logits, cache = sm.forward(t.view(b, 1).to(sm.device), cache, attention_mask=attn)
        rs[:, total] = clf.r_t_batch(logits)
        sm.state.set_alpha(0.0)
        del cache
        return toks, rs

    clean_toks, clean_r = _run(False, None)
    free_toks, free_r = _run(True, None)
    tf_toks, tf_r = _run(True, clean_toks)

    out = []
    for i in range(b):
        dev_free = [abs(free_r[i, inject_step + k] - clean_r[i, inject_step + k])
                    for k in range(horizon + 1)]
        dev_tf = [abs(tf_r[i, inject_step + k] - clean_r[i, inject_step + k])
                  for k in range(horizon + 1)]

        def _ratio(d):
            return float(d[-1] / d[1]) if len(d) > 1 and d[1] > 1e-9 else None

        out.append({
            "prompt": prompts[i][:120], "eps": eps, "seed": seed,
            "free_running": {
                "deviation": [float(x) for x in dev_free], "survival_ratio": _ratio(dev_free),
                "auc": float(np.sum(dev_free)),
                "tokens_diverged": int((clean_toks[i] != free_toks[i]).sum()),
            },
            "teacher_forced": {
                "deviation": [float(x) for x in dev_tf], "survival_ratio": _ratio(dev_tf),
                "auc": float(np.sum(dev_tf)),
                "tokens_diverged": int((clean_toks[i] != tf_toks[i]).sum()),
            },
        })
    return out
