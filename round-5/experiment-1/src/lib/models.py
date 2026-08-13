#!/usr/bin/env python3
"""Model loading, chat rendering, the steering hook and KV plumbing.

Ported from iteration-1 `gen_art_experiment_2/models.py`. Two deliberate
changes, both recorded in prereg.json:
  * DTYPE is float32, not bfloat16 -- iteration-1 EXP3 measured that fp16/bf16
    batched decoding is NOT batch-invariant (3/4 identical completions at
    batch=4 vs batch=1, 4/4 in fp32). Every member here is <=1.7B so fp32 fits.
  * a batched, per-row-alpha sampling loop is added (the iteration-1 arms were
    batch-1); the hook itself is unchanged and already indexes alpha per row.
"""

from __future__ import annotations

import copy
import gc
from dataclasses import dataclass, field

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

DTYPE = torch.float32


# ---------------------------------------------------------------------------
# Steering state
# ---------------------------------------------------------------------------
@dataclass
class SteerState:
    """Mutable per-batch-row steering coefficient (in units of NORM_L)."""

    alpha: torch.Tensor  # shape (batch,), float32
    direction: torch.Tensor | None = None  # (d_model,), unit norm
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
    def __init__(self, model_id: str, device: str = "cuda", dtype=None):
        self.model_id = model_id
        self.device = device
        logger.info(f"loading {model_id} in {dtype or DTYPE}")
        self.tok = AutoTokenizer.from_pretrained(model_id)
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        self.tok.padding_side = "left"
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, dtype=dtype or DTYPE, device_map=None
            )
        except TypeError:  # older transformers
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, torch_dtype=dtype or DTYPE, device_map=None
            )
        self.model = self.model.to(device)
        self.model.eval()
        self.model.requires_grad_(False)
        self.n_layers = self.model.config.num_hidden_layers
        self.d_model = self.model.config.hidden_size
        self.state = SteerState(alpha=torch.zeros(1, dtype=torch.float32, device=device))
        self._handle = None
        self._hooked_layer = None

    # -- hook management ---------------------------------------------------
    @property
    def blocks(self):
        m = self.model
        for attr in ("model", "transformer", "gpt_neox"):
            inner = getattr(m, attr, None)
            if inner is not None:
                for lattr in ("layers", "h"):
                    ls = getattr(inner, lattr, None)
                    if ls is not None:
                        return ls
        raise RuntimeError(f"cannot locate decoder blocks on {type(m).__name__}")

    def install_hook(self, layer: int | list[int], quiet: bool = True) -> None:
        self.remove_hook()
        layers = [layer] if isinstance(layer, int) else list(layer)
        self._handle = [
            self.blocks[l].register_forward_hook(make_steer_hook(self.state)) for l in layers
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
        try:
            del self.model
        except AttributeError:
            pass
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # -- forward helpers ---------------------------------------------------
    @torch.no_grad()
    def forward(self, input_ids: torch.Tensor, cache, use_cache: bool = True,
                attention_mask: torch.Tensor | None = None):
        kw = {}
        if attention_mask is not None:
            kw["attention_mask"] = attention_mask
        out = self.model(
            input_ids=input_ids,
            past_key_values=cache,
            use_cache=use_cache,
            output_hidden_states=False,
            **kw,
        )
        return out.logits[:, -1, :].float(), out.past_key_values

    @torch.no_grad()
    def hidden_states(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Post-block residual stream at the LAST token, all layers -> (n_layers, d_model)."""
        out = self.model(input_ids=input_ids, use_cache=False, output_hidden_states=True)
        hs = torch.stack([h[0, -1, :].float() for h in out.hidden_states[1:]], dim=0)
        return hs.cpu()


def new_cache():
    from transformers import DynamicCache

    return DynamicCache()


def clone_cache(cache):
    return copy.deepcopy(cache)


def cache_len(cache) -> int:
    try:
        return int(cache.get_seq_length())
    except Exception:  # noqa: BLE001 - cache API drift across transformers versions
        return 0


# ---------------------------------------------------------------------------
# Prompt formatting
# ---------------------------------------------------------------------------
THINK_BLOCK = "<think>\n\n</think>\n\n"
GENERIC_WRAPPER = "User: {p}\nAssistant:"


def has_chat_template(tok) -> bool:
    return getattr(tok, "chat_template", None) is not None


def render_chat(tok, text: str) -> str:
    """Chat template with Qwen3 thinking disabled plus the automated <think> guard.

    A member that emits <think> silently burns the generation budget; the guard
    closes an empty thinking block whenever the template did not.
    """
    try:
        s = tok.apply_chat_template(
            [{"role": "user", "content": text}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        s = tok.apply_chat_template(
            [{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True
        )
    if "<think>" in (getattr(tok, "chat_template", "") or "") and "<think>" not in s:
        s = s + THINK_BLOCK
    return s


def render_plain(text: str) -> str:
    return GENERIC_WRAPPER.format(p=text)


def make_renderer(tok, mode: str = "auto"):
    """mode: 'chat' | 'generic' | 'auto' (chat when the tokenizer ships a template)."""
    if mode == "generic" or (mode == "auto" and not has_chat_template(tok)):
        return render_plain, "generic_wrapper"
    return (lambda t: render_chat(tok, t)), "chat_template(enable_thinking=False)"
