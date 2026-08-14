#!/usr/bin/env python3
"""Model loading, ChatML formatting, steering hook and KV-cache plumbing."""

from __future__ import annotations

import copy
import gc
from dataclasses import dataclass, field

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

DTYPE = torch.bfloat16


# ---------------------------------------------------------------------------
# Steering state
# ---------------------------------------------------------------------------
@dataclass
class SteerState:
    """Mutable per-batch-row steering coefficient (in units of NORM_L)."""

    alpha: torch.Tensor  # shape (batch,), float32
    direction: torch.Tensor | None = None  # (d_model,), unit norm, model dtype
    norm_l: float = 1.0
    enabled: bool = True
    n_applied: int = field(default=0)

    def set_alpha(self, values) -> None:
        if isinstance(values, (int, float)):
            self.alpha.fill_(float(values))
        else:
            v = torch.as_tensor(values, dtype=torch.float32, device=self.alpha.device)
            assert v.shape == self.alpha.shape, (v.shape, self.alpha.shape)
            self.alpha.copy_(v)

    def resize(self, batch: int) -> None:
        if self.alpha.numel() != batch:
            self.alpha = torch.zeros(batch, dtype=torch.float32, device=self.alpha.device)


def make_steer_hook(state: SteerState):
    """Forward hook adding alpha * NORM_L * d_hat to a block's output hidden state.

    Applied to EVERY position present in the current forward pass. During
    incremental decoding only the newest position is present, so a token's KV
    entries stay frozen carrying whatever alpha was active when it was written.
    """

    def hook(_module, _args, output):
        if not state.enabled or state.direction is None:
            return output
        is_tuple = isinstance(output, tuple)
        hs = output[0] if is_tuple else output
        b = hs.shape[0]
        alpha = state.alpha[:b].to(hs.device)
        if torch.count_nonzero(alpha) == 0:
            return output
        delta = (alpha * state.norm_l).view(b, 1, 1).to(hs.dtype) * state.direction.to(
            hs.device, hs.dtype
        ).view(1, 1, -1)
        hs = hs + delta
        state.n_applied += 1
        if is_tuple:
            return (hs,) + tuple(output[1:])
        return hs

    return hook


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
class SteeredModel:
    def __init__(self, model_id: str, device: str = "cuda"):
        self.model_id = model_id
        self.device = device
        logger.info(f"loading {model_id}")
        self.tok = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, dtype=DTYPE, device_map=None
        ).to(device)
        self.model.eval()
        self.model.requires_grad_(False)
        self.n_layers = self.model.config.num_hidden_layers
        self.d_model = self.model.config.hidden_size
        self.state = SteerState(alpha=torch.zeros(1, dtype=torch.float32, device=device))
        self._handle = None
        self._hooked_layer = None

    # -- hook management ---------------------------------------------------
    def install_hook(self, layer: int | list[int], quiet: bool = False) -> None:
        self.remove_hook()
        layers = [layer] if isinstance(layer, int) else list(layer)
        self._handle = [
            self.model.model.layers[l].register_forward_hook(make_steer_hook(self.state))
            for l in layers
        ]
        self._hooked_layer = layers
        if not quiet:
            logger.info(f"steering hook installed on layers {layers} of {self.model_id}")

    def remove_hook(self) -> None:
        if self._handle is not None:
            for h in self._handle:
                h.remove()
            self._handle = None
            self._hooked_layer = None

    def close(self) -> None:
        self.remove_hook()
        del self.model
        gc.collect()
        torch.cuda.empty_cache()

    # -- forward helpers ---------------------------------------------------
    @torch.no_grad()
    def forward(self, input_ids: torch.Tensor, cache, use_cache: bool = True):
        out = self.model(
            input_ids=input_ids,
            past_key_values=cache,
            use_cache=use_cache,
            output_hidden_states=False,
        )
        return out.logits[:, -1, :].float(), out.past_key_values

    @torch.no_grad()
    def hidden_states(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Return post-block residual stream at the LAST token, all layers.

        Shape (n_layers, d_model). hidden_states[i+1] is the output of block i.
        """
        out = self.model(input_ids=input_ids, use_cache=False, output_hidden_states=True)
        hs = torch.stack([h[0, -1, :].float() for h in out.hidden_states[1:]], dim=0)
        return hs.cpu()


def new_cache():
    from transformers import DynamicCache

    return DynamicCache()


def clone_cache(cache):
    """Deep copy a KV cache so probe arms cannot corrupt shared state."""
    return copy.deepcopy(cache)


def cache_len(cache) -> int:
    try:
        return int(cache.get_seq_length())
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Prompt formatting: identical ChatML string for all lineage members
# ---------------------------------------------------------------------------
THINK_BLOCK = "<think>\n\n</think>\n\n"


def render_chatml(instruct_tok, text: str) -> str:
    try:
        s = instruct_tok.apply_chat_template(
            [{"role": "user", "content": text}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        s = instruct_tok.apply_chat_template(
            [{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True
        )
    if "<think>" not in s:
        s = s + THINK_BLOCK
    return s


def render_plain(text: str) -> str:
    return f"User: {text}\nAssistant:"
