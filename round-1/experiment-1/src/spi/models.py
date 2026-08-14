"""Model loading, layer indexing, chat templating, dtype handling."""

from __future__ import annotations

import gc
from dataclasses import dataclass, field
from typing import Any

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

# The Tier-0 panel: a 3-member lineage (base / safety-tuned / abliterated) plus a
# low-refusal anchor from a different lineage.
MODEL_PANEL: list[dict[str, Any]] = [
    {
        "id": "Qwen/Qwen3-0.6B-Base",
        "lineage": "qwen3-0.6b",
        "member": "base",
        "chat": False,
        "fallbacks": [],
    },
    {
        "id": "Qwen/Qwen3-0.6B",
        "lineage": "qwen3-0.6b",
        "member": "instruct",
        "chat": True,
        "fallbacks": [],
    },
    {
        "id": "huihui-ai/Qwen3-0.6B-abliterated",
        "lineage": "qwen3-0.6b",
        "member": "abliterated",
        "chat": True,
        "fallbacks": ["huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2"],
    },
    {
        "id": "HuggingFaceTB/SmolLM2-360M",
        "lineage": "smollm2",
        "member": "base",
        "chat": False,
        "fallbacks": ["EleutherAI/pythia-410m"],
    },
]

# Identical pseudo-chat format for every base model (no chat template available).
BASE_PROMPT_FORMAT = "User: {p}\nAssistant:"


@dataclass
class LoadedModel:
    """A loaded HF causal LM plus everything the measurement code needs."""

    spec: dict[str, Any]
    model_id: str
    revision: str
    model: Any
    tokenizer: Any
    n_layers: int
    hidden_size: int
    dtype: str
    device: str
    uses_chat_template: bool
    layer_modules: Any = field(default=None, repr=False)

    @property
    def key(self) -> str:
        return f"{self.spec['lineage']}/{self.spec['member']}"

    def render(self, prompt: str) -> str:
        """Render a user instruction into the model's expected prompt string.

        For Qwen3 (a hybrid thinking model) we MUST pass enable_thinking=False so
        generation does not open a <think> block — otherwise r_t would measure
        reasoning-preamble tokens instead of refusal onset.
        """
        if not self.uses_chat_template:
            return BASE_PROMPT_FORMAT.format(p=prompt)
        msgs = [{"role": "user", "content": prompt}]
        try:
            text = self.tokenizer.apply_chat_template(
                msgs,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
        except TypeError:
            # Older tokenizer without the kwarg — use Qwen3's documented soft switch.
            msgs = [{"role": "user", "content": prompt + " /no_think"}]
            text = self.tokenizer.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True
            )
        return text

    def encode(self, text: str) -> torch.Tensor:
        ids = self.tokenizer(text, return_tensors="pt", add_special_tokens=False)[
            "input_ids"
        ]
        return ids.to(self.device)


def _decoder_layers(model: Any) -> Any:
    """Return the ModuleList of decoder blocks for the supported architectures."""
    for path in ("model.layers", "gpt_neox.layers", "transformer.h", "model.decoder.layers"):
        obj: Any = model
        ok = True
        for part in path.split("."):
            if not hasattr(obj, part):
                ok = False
                break
            obj = getattr(obj, part)
        if ok:
            return obj
    raise AttributeError(f"Could not locate decoder layers on {type(model)}")


def _final_norm(model: Any) -> Any:
    """Return the final pre-unembedding norm module."""
    for path in ("model.norm", "gpt_neox.final_layer_norm", "transformer.ln_f", "model.final_layernorm"):
        obj: Any = model
        ok = True
        for part in path.split("."):
            if not hasattr(obj, part):
                ok = False
                break
            obj = getattr(obj, part)
        if ok:
            return obj
    raise AttributeError(f"Could not locate final norm on {type(model)}")


def _lm_head(model: Any) -> Any:
    if hasattr(model, "lm_head"):
        return model.lm_head
    if hasattr(model, "embed_out"):
        return model.embed_out
    raise AttributeError(f"Could not locate lm_head on {type(model)}")


def resolve_revision(model_id: str) -> str:
    """Fetch the exact commit SHA of a repo (provenance for method_out.json)."""
    try:
        from huggingface_hub import HfApi

        info = HfApi().model_info(model_id)
        return str(info.sha)
    except Exception as exc:  # noqa: BLE001 - provenance is best-effort
        logger.warning(f"Could not resolve revision for {model_id}: {exc}")
        return "unknown"


def load_model(spec: dict[str, Any], device: str = "cuda") -> LoadedModel:
    """Load a panel member, trying its fallbacks in order if the primary fails."""
    candidates = [spec["id"], *spec.get("fallbacks", [])]
    last_exc: Exception | None = None
    for model_id in candidates:
        try:
            logger.info(f"Loading {model_id} ...")
            tok = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False)
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            dtype = torch.bfloat16 if device == "cuda" else torch.float32
            model = AutoModelForCausalLM.from_pretrained(
                model_id, torch_dtype=dtype, trust_remote_code=False
            )
            model.to(device)
            model.eval()
            model.requires_grad_(False)
            layers = _decoder_layers(model)
            cfg = model.config
            n_layers = len(layers)
            hidden = int(getattr(cfg, "hidden_size", getattr(cfg, "n_embd", 0)))
            uses_chat = bool(spec["chat"]) and getattr(tok, "chat_template", None) is not None
            if spec["chat"] and not uses_chat:
                logger.warning(f"{model_id}: chat=True but tokenizer has no chat_template")
            lm = LoadedModel(
                spec=spec,
                model_id=model_id,
                revision=resolve_revision(model_id),
                model=model,
                tokenizer=tok,
                n_layers=n_layers,
                hidden_size=hidden,
                dtype=str(dtype).replace("torch.", ""),
                device=device,
                uses_chat_template=uses_chat,
                layer_modules=layers,
            )
            logger.info(
                f"Loaded {model_id} rev={lm.revision[:12]} n_layers={n_layers} "
                f"hidden={hidden} dtype={lm.dtype} chat={uses_chat}"
            )
            return lm
        except Exception as exc:  # noqa: BLE001 - try the next fallback repo
            logger.error(f"Failed to load {model_id}: {exc}")
            last_exc = exc
            gc.collect()
            if device == "cuda":
                torch.cuda.empty_cache()
    raise RuntimeError(f"All candidates failed for {spec['id']}: {last_exc}")


def lens_modules(lm: LoadedModel) -> tuple[Any, Any]:
    """(final_norm, lm_head) — the logit-lens read-out path."""
    return _final_norm(lm.model), _lm_head(lm.model)


def free_model(lm: LoadedModel) -> None:
    """Release a model's GPU memory. Process ONE model at a time."""
    try:
        lm.model.to("cpu")
    except Exception:  # noqa: BLE001 - best-effort teardown
        pass
    del lm.model
    del lm.layer_modules
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
