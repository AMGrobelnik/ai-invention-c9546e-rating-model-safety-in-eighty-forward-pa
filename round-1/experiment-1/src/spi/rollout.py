"""Paired-seed batched sampling loop with hookable residual injection.

We do NOT use model.generate: we need (a) per-step layer-L residuals, (b) a
mid-generation injection at that same layer, and (c) COMMON RANDOM NUMBERS
across the clean and perturbed arms so the two rollouts diverge ONLY because of
the injection.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from loguru import logger

from .models import LoadedModel
from .observable import (
    DiffMeansObservable,
    Observable,
    POSProbeObservable,
    RandomAxisObservable,
)


@dataclass
class RolloutResult:
    """Everything one batched rollout produces."""

    r: np.ndarray                     # (T, n_roll) primary r_t, layer-L logit lens
    r_final: np.ndarray               # (T, n_roll) same contrast on FINAL-layer logits
    r_rand: np.ndarray                # (n_draws, T, n_roll) random-axis control
    r_pos: np.ndarray | None          # (T, n_roll) POS-probe control
    r_dm: np.ndarray | None           # (T, n_roll) diff-in-means projection (descriptive)
    tokens: np.ndarray                # (T, n_roll) generated token ids
    texts: list[str]
    eos_step: np.ndarray              # (n_roll,) first EOS index or T
    resid_norm: np.ndarray            # (T, n_roll) ||resid_L|| — sets the eps scale
    seconds: float
    n_tokens: int

    @property
    def tokens_per_sec(self) -> float:
        return self.n_tokens / self.seconds if self.seconds > 0 else float("nan")


@torch.no_grad()
def _inverse_cdf_sample(probs: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
    """Deterministic categorical sampling given pre-drawn uniforms.

    probs: (B, V) normalised. u: (B,) in [0,1). Returns (B,) token ids.
    Sorting descending then searchsorting the cumulative mass makes the draw a
    pure function of u — which is what makes 'paired seeds' real.
    """
    sp, si = torch.sort(probs, dim=-1, descending=True)
    cum = torch.cumsum(sp, dim=-1)
    cum[:, -1] = 1.0  # guard against float drift leaving u past the last bin
    idx = torch.searchsorted(cum.contiguous(), u.unsqueeze(-1).contiguous())
    idx = idx.clamp_(max=probs.shape[-1] - 1)
    return si.gather(-1, idx).squeeze(-1)


@torch.no_grad()
def rollout_batch(
    lm: LoadedModel,
    obs: Observable,
    prompt_text: str,
    *,
    layer: int,
    n_roll: int = 20,
    T: int = 192,
    temp: float = 0.7,
    seed: int = 0,
    inject: dict[str, Any] | None = None,
    rand_obs: RandomAxisObservable | None = None,
    pos_obs: POSProbeObservable | None = None,
    dm_obs: DiffMeansObservable | None = None,
    force_tokens: np.ndarray | None = None,
    banned_ids: list[int] | None = None,
) -> RolloutResult:
    """Run n_roll paired rollouts of T generated steps.

    inject = None | {'step': p, 'vec': unit tensor (D,), 'eps': float,
                     'mode': 'once' | 'sustained', 'k': int}
    force_tokens: (T, n_roll) — teacher-forced mode; the sampled token is
                  overridden so delta_t isolates latent-state deviation with
                  token content held fixed.
    """
    dev = lm.device
    model = lm.model
    ids = lm.encode(prompt_text)                     # (1, S)
    prompt_ids = ids.repeat(n_roll, 1)               # (n_roll, S)

    # PRE-DRAWN uniforms — identical across arms for the same seed.
    gen = torch.Generator(device="cpu").manual_seed(seed)
    u_all = torch.rand((T, n_roll), generator=gen).to(dev)

    buf: dict[str, torch.Tensor] = {}
    state = {"t": -1}
    p_inj = int(inject["step"]) if inject else -1
    k_inj = int(inject.get("k", 1)) if inject else 1
    mode = str(inject.get("mode", "once")) if inject else "once"
    eps = float(inject["eps"]) if inject else 0.0
    vec = inject["vec"].to(dev) if inject else None

    def injecting() -> bool:
        t = state["t"]
        return (
            inject is not None
            and eps != 0.0
            and (t == p_inj if mode == "once" else p_inj <= t < p_inj + k_inj)
        )

    def pre_hook(_m: Any, inp: Any, kwargs: dict[str, Any]) -> Any:
        """Add eps*vec to the residual stream ENTERING layer L.

        This placement is load-bearing. Injecting at the layer's OUTPUT leaves the
        layer's own K/V for that position — written inside its attention, before a
        forward hook can fire — unmodified, so the layer-L read at every later step
        is bit-identical until the sampled tokens happen to diverge. Verified
        empirically in T2: output-injection gave |delta_{p+1}| == 0 at every eps.
        Injecting at the INPUT makes layer L's K/V at position p carry the kick, so
        later positions see it through attention, which is the channel we mean to
        measure.
        """
        if not injecting():
            return None
        if inp:
            h = inp[0].clone()
            h[:, -1, :] = h[:, -1, :] + (eps * vec).to(h.dtype)
            return ((h,) + tuple(inp[1:]), kwargs)
        hs = kwargs.get("hidden_states")
        if hs is None:
            return None
        h = hs.clone()
        h[:, -1, :] = h[:, -1, :] + (eps * vec).to(h.dtype)
        return (inp, {**kwargs, "hidden_states": h})

    def hook(_m: Any, _i: Any, out: Any) -> Any:
        h = out[0] if isinstance(out, tuple) else out
        buf["h"] = h[:, -1, :].detach()
        return out

    pre_handle = lm.layer_modules[layer].register_forward_pre_hook(
        pre_hook, with_kwargs=True)
    handle = lm.layer_modules[layer].register_forward_hook(hook)

    r = np.zeros((T, n_roll), dtype=np.float32)
    r_final = np.zeros((T, n_roll), dtype=np.float32)
    n_draws = rand_obs.n_draws if rand_obs is not None else 0
    r_rand = np.zeros((max(n_draws, 1), T, n_roll), dtype=np.float32)
    r_pos = np.zeros((T, n_roll), dtype=np.float32) if pos_obs is not None else None
    r_dm = np.zeros((T, n_roll), dtype=np.float32) if dm_obs is not None else None
    toks = np.zeros((T, n_roll), dtype=np.int64)
    rnorm = np.zeros((T, n_roll), dtype=np.float32)

    eos_id = lm.tokenizer.eos_token_id
    eos_step = np.full(n_roll, T, dtype=np.int64)
    ban = torch.tensor(banned_ids, device=dev, dtype=torch.long) if banned_ids else None

    cur = prompt_ids
    past = None
    t0 = time.time()
    try:
        for t in range(T):
            state["t"] = t
            out = model(input_ids=cur, past_key_values=past, use_cache=True)
            past = out.past_key_values
            h = buf["h"]                              # (B, D) layer-L, last position
            r[t] = obs.from_resid(h).cpu().numpy()
            rnorm[t] = h.float().norm(dim=-1).cpu().numpy()
            logits = out.logits[:, -1, :].float()
            r_final[t] = obs.from_logits(logits).cpu().numpy()
            if rand_obs is not None:
                r_rand[:, t, :] = rand_obs.from_resid(h).cpu().numpy()
            if pos_obs is not None:
                r_pos[t] = pos_obs.from_resid(h).cpu().numpy()
            if dm_obs is not None:
                r_dm[t] = dm_obs.from_resid(h).cpu().numpy()

            if ban is not None:
                logits.index_fill_(-1, ban, float("-inf"))
            probs = torch.softmax(logits / temp, dim=-1)
            nxt = _inverse_cdf_sample(probs, u_all[t])
            if force_tokens is not None:
                nxt = torch.tensor(force_tokens[t], device=dev, dtype=torch.long)
            toks[t] = nxt.cpu().numpy()
            if eos_id is not None:
                hit = (toks[t] == eos_id) & (eos_step == T)
                eos_step[hit] = t
            cur = nxt.unsqueeze(-1)
            del logits, probs, out
    finally:
        handle.remove()
        pre_handle.remove()
        buf.clear()
        del past
        if dev == "cuda":
            torch.cuda.empty_cache()

    secs = time.time() - t0
    texts = [lm.tokenizer.decode(toks[:, j].tolist(), skip_special_tokens=True)
             for j in range(n_roll)]
    return RolloutResult(
        r=r, r_final=r_final, r_rand=r_rand, r_pos=r_pos, r_dm=r_dm,
        tokens=toks, texts=texts, eos_step=eos_step, resid_norm=rnorm,
        seconds=secs, n_tokens=T * n_roll,
    )


def first_divergence(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """(T,n) x (T,n) -> (n,) first step where the two token streams differ, else T."""
    T, n = a.shape
    out = np.full(n, T, dtype=np.int64)
    diff = a != b
    for j in range(n):
        w = np.flatnonzero(diff[:, j])
        if w.size:
            out[j] = int(w[0])
    return out


@torch.no_grad()
def collect_prompt_residuals(lm: LoadedModel, prompts: list[str], layer: int,
                             batch: int = 8) -> np.ndarray:
    """Last-prompt-token layer-L residuals for a list of rendered prompts."""
    buf: dict[str, torch.Tensor] = {}

    def hook(_m: Any, _i: Any, o: Any) -> None:
        buf["h"] = (o[0] if isinstance(o, tuple) else o).detach()

    handle = lm.layer_modules[layer].register_forward_hook(hook)
    tok = lm.tokenizer
    outs: list[np.ndarray] = []
    try:
        for i in range(0, len(prompts), batch):
            chunk = prompts[i : i + batch]
            enc = tok(chunk, return_tensors="pt", padding=True,
                      add_special_tokens=False, padding_side="left")
            enc = {k: v.to(lm.device) for k, v in enc.items()}
            lm.model(**enc, use_cache=False)
            outs.append(buf["h"][:, -1, :].float().cpu().numpy())
    finally:
        handle.remove()
        buf.clear()
        if lm.device == "cuda":
            torch.cuda.empty_cache()
    return np.concatenate(outs, axis=0)


@torch.no_grad()
def greedy_generate(lm: LoadedModel, prompt_text: str, max_new: int = 64,
                    banned_ids: list[int] | None = None) -> str:
    """Temperature-0 generation, used for the $0 ground-truth refusal screen."""
    ids = lm.encode(prompt_text)
    past = None
    cur = ids
    out_ids: list[int] = []
    ban = torch.tensor(banned_ids, device=lm.device, dtype=torch.long) if banned_ids else None
    for _ in range(max_new):
        out = lm.model(input_ids=cur, past_key_values=past, use_cache=True)
        past = out.past_key_values
        logits = out.logits[:, -1, :].float()
        if ban is not None:
            logits.index_fill_(-1, ban, float("-inf"))
        nxt = int(logits.argmax(dim=-1).item())
        if lm.tokenizer.eos_token_id is not None and nxt == lm.tokenizer.eos_token_id:
            break
        out_ids.append(nxt)
        cur = torch.tensor([[nxt]], device=lm.device)
        del out, logits
    del past
    if lm.device == "cuda":
        torch.cuda.empty_cache()
    return lm.tokenizer.decode(out_ids, skip_special_tokens=True)


def peak_vram_gb() -> float:
    if not torch.cuda.is_available():
        return 0.0
    return float(torch.cuda.max_memory_allocated() / 1024**3)


def log_throughput(tag: str, res: RolloutResult) -> None:
    logger.info(
        f"{tag}: {res.n_tokens} tok in {res.seconds:.1f}s = {res.tokens_per_sec:.1f} tok/s "
        f"| peak VRAM {peak_vram_gb():.2f} GB"
    )
