#!/usr/bin/env python3
"""The alpha_50 primitive: batched FRESH constant-alpha generations.

One batch = one prompt x all (seed, alpha) combinations, so every row in the
batch has an IDENTICAL prompt and no padding is ever needed (left-padding a
decoder-only model silently corrupts rotary positions on some transformers
versions; avoiding it removes the hazard entirely).

Every row carries its own CPU torch.Generator seeded by
sha256(prompt_uid, seed), so the random stream for a given (prompt, seed) is
IDENTICAL across alphas, axes and models.  That is what makes the paired
bootstrap legitimate.
"""

from __future__ import annotations

import hashlib

import torch

from classify import fluency_ok
from models import new_cache


def row_seed(prompt_uid: str, seed: int) -> int:
    h = hashlib.sha256(f"{prompt_uid}|{seed}".encode()).hexdigest()
    return int(h[:12], 16)


def make_row_generator(prompt_uid: str, seed: int) -> torch.Generator:
    g = torch.Generator(device="cpu")
    g.manual_seed(row_seed(prompt_uid, seed))
    return g


def sample_rows(logits: torch.Tensor, temperature: float,
                generators: list[torch.Generator]) -> torch.Tensor:
    """Inverse-CDF multinomial sampling with ONE uniform per row, drawn from that
    row's own generator.  Equivalent in distribution to torch.multinomial while
    keeping every row's stream independent and reproducible."""
    if temperature <= 0.0:
        return logits.argmax(dim=-1).to("cpu")
    probs = torch.softmax(logits / temperature, dim=-1)
    cdf = torch.cumsum(probs, dim=-1)
    cdf[:, -1] = 1.0
    u = torch.tensor(
        [float(torch.rand(1, generator=g).item()) for g in generators],
        dtype=cdf.dtype, device=cdf.device,
    ).unsqueeze(1)
    idx = torch.searchsorted(cdf, u).squeeze(1)
    return idx.clamp_(max=probs.shape[-1] - 1).to("cpu")


@torch.no_grad()
def generate_batch(sm, clf, prompt_ids: torch.Tensor, rows: list[dict], *,
                   banned: torch.Tensor, temperature: float, n_tokens: int,
                   keep_text: bool = True, keep_rt: bool = False) -> list[dict]:
    """rows: [{prompt_uid, seed, alpha}].  Returns one record per row."""
    b = len(rows)
    sm.state.resize(b)
    sm.state.set_alpha([float(r["alpha"]) for r in rows])
    gens = [make_row_generator(r["prompt_uid"], int(r["seed"])) for r in rows]
    ids = prompt_ids.expand(b, -1).contiguous()
    logits, cache = sm.forward(ids, new_cache())

    ban = banned.to(sm.device) if banned is not None and banned.numel() else None
    ref_ids = clf.refusal_ids_t.to(sm.device)
    con_ids = clf.cont_ids_t.to(sm.device)

    gen_ids: list[list[int]] = [[] for _ in range(b)]
    onset: list[int | None] = [None] * b
    rt_traces: list[list[float]] = [[] for _ in range(b)]
    rt_first: list[float] = [0.0] * b

    for t in range(n_tokens):
        lg = logits.float()
        if ban is not None:
            lg[:, ban] = float("-inf")
        r_t = (torch.logsumexp(lg[:, ref_ids], dim=1)
               - torch.logsumexp(lg[:, con_ids], dim=1)).to("cpu").tolist()
        toks = sample_rows(lg, temperature, gens)
        for i in range(b):
            gen_ids[i].append(int(toks[i]))
            if t == 0:
                rt_first[i] = float(r_t[i])
            if keep_rt:
                rt_traces[i].append(round(float(r_t[i]), 4))
            if onset[i] is None and clf.is_refusal_onset(gen_ids[i]):
                onset[i] = t
        logits, cache = sm.forward(toks.view(b, 1).to(sm.device), cache)

    sm.state.resize(1)
    out = []
    for i, r in enumerate(rows):
        rec = {
            "prompt_uid": r["prompt_uid"],
            "seed": int(r["seed"]),
            "alpha": float(r["alpha"]),
            "refused": onset[i] is not None,
            "onset_step": onset[i],
            "fluent": bool(fluency_ok(gen_ids[i])),
            "r_t_first": round(rt_first[i], 4),
            "n_tokens": len(gen_ids[i]),
        }
        if keep_text:
            rec["text"] = sm.tok.decode(gen_ids[i], skip_special_tokens=True)
        if keep_rt:
            rec["r_t_trace"] = rt_traces[i]
        out.append(rec)
    del cache, logits
    return out


@torch.no_grad()
def sweep_axis(sm, clf, prompts: list[dict], seeds: list[int], alphas: list[float], *,
               render, banned, temperature: float, n_tokens: int,
               batch_cap: int, keep_text: bool = True,
               progress=None) -> list[dict]:
    """Full grid for one (model, axis).  `prompts` = [{uid, text}]."""
    records: list[dict] = []
    for pi, p in enumerate(prompts):
        ids = sm.tok(render(p["text"]), return_tensors="pt",
                     add_special_tokens=False).input_ids.to(sm.device)
        rows = [{"prompt_uid": p["uid"], "seed": s, "alpha": a}
                for s in seeds for a in alphas]
        for i in range(0, len(rows), batch_cap):
            chunk = rows[i:i + batch_cap]
            recs = generate_batch(
                sm, clf, ids, chunk, banned=banned, temperature=temperature,
                n_tokens=n_tokens, keep_text=keep_text,
                keep_rt=(pi == 0 and chunk[0]["seed"] == seeds[0]),
            )
            for r in recs:
                r["prompt_text"] = p["text"]
            records.extend(recs)
        if progress is not None:
            progress(pi + 1, len(prompts))
    return records


def censor_alphas(records: list[dict], max_fluency_fail: float = 0.25) -> dict:
    """An alpha whose fluency-failure fraction exceeds the threshold is beyond
    the OUTER EDGE OF MEASUREMENT and is censored from the fit."""
    by_alpha: dict[float, list[dict]] = {}
    for r in records:
        by_alpha.setdefault(round(r["alpha"], 6), []).append(r)
    censored, report = [], []
    for a in sorted(by_alpha):
        v = by_alpha[a]
        frac = sum(1 for r in v if not r["fluent"]) / len(v)
        cen = frac > max_fluency_fail
        if cen:
            censored.append(a)
        report.append({"alpha": a, "n": len(v), "fluency_fail_frac": round(frac, 4),
                       "censored": cen})
    return {"censored_alphas": censored, "per_alpha_fluency": report,
            "threshold": max_fluency_fail}


def filter_for_fit(records: list[dict], censored: list[float]) -> list[dict]:
    cs = {round(float(a), 6) for a in censored}
    return [r for r in records
            if r["fluent"] and round(r["alpha"], 6) not in cs]


def dense_window(records: list[dict], step: float = 0.05, pad: float = 0.20,
                 lo_cap: float = 0.0, hi_cap: float = 2.0) -> list[float]:
    """Bracketing interval around the coarse 0.5 crossing, at the dense step."""
    by_alpha: dict[float, list[int]] = {}
    for r in records:
        by_alpha.setdefault(round(r["alpha"], 6), []).append(int(r["refused"]))
    alphas = sorted(by_alpha)
    rates = [sum(by_alpha[a]) / len(by_alpha[a]) for a in alphas]
    a_lo = a_hi = None
    for i in range(1, len(alphas)):
        if rates[i - 1] < 0.5 <= rates[i]:
            a_lo, a_hi = alphas[i - 1], alphas[i]
            break
    if a_lo is None:
        return []
    lo = max(lo_cap, a_lo - pad)
    hi = min(hi_cap, a_hi + pad)
    n = int(round((hi - lo) / step))
    return [round(lo + i * step, 6) for i in range(n + 1)]
