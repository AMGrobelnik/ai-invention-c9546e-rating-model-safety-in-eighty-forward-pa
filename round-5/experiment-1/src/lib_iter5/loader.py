#!/usr/bin/env python3
"""Revision-pinned model loading.

`lib/models.py` is reused byte-identically from the iteration-2 archive and its
`SteeredModel.__init__` has no `revision` argument, so it always resolves the
repo's default branch. The frozen panel carries a pinned commit SHA per row and
this run must read the SAME weights iteration 4 read, so the loader is
subclassed here (in NEW code) rather than the reused library being edited.

`from_pretrained(revision=...)` is attempted first; if the pinned revision is
unreachable the unpinned load is attempted and the downgrade is RECORDED on the
member row, never silently accepted.
"""

from __future__ import annotations

import gc

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from lib import models as models_mod


class PinnedModel(models_mod.SteeredModel):
    """SteeredModel with an explicit `revision`; identical in every other way."""

    def __init__(self, model_id: str, revision: str | None = None,
                 device: str = "cuda", dtype=None):
        self.model_id = model_id
        self.device = device
        self.revision_requested = revision
        self.revision_used: str | None = None
        dt = dtype or models_mod.DTYPE
        logger.info(f"loading {model_id} @ {revision or 'default-branch'} in {dt}")

        tok = None
        last: Exception | None = None
        for rev in ([revision] if revision else []) + [None]:
            kw = {"revision": rev} if rev else {}
            try:
                tok = AutoTokenizer.from_pretrained(model_id, **kw)
                self.revision_used = rev
                break
            except Exception as exc:  # noqa: BLE001 - gated/404/network all land here
                last = exc
                logger.error(f"tokenizer load failed for {model_id} @ {rev}: "
                             f"{type(exc).__name__}: {exc}"[:250])
        if tok is None:
            raise RuntimeError(f"tokenizer unreachable for {model_id}: {last}")
        self.tok = tok
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        self.tok.padding_side = "left"

        kw = {"revision": self.revision_used} if self.revision_used else {}
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, dtype=dt, device_map=None, **kw)
        except TypeError:  # transformers <4.56 spells it torch_dtype
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, torch_dtype=dt, device_map=None, **kw)
        self.model = self.model.to(device)
        self.model.eval()
        self.model.requires_grad_(False)
        self.n_layers = self.model.config.num_hidden_layers
        self.d_model = self.model.config.hidden_size
        self.state = models_mod.SteerState(
            alpha=torch.zeros(1, dtype=torch.float32, device=device))
        self._handle = None
        self._hooked_layer = None
        gc.collect()

    @property
    def revision_report(self) -> dict:
        return {
            "revision_requested": self.revision_requested,
            "revision_used": self.revision_used,
            "revision_pinned": bool(self.revision_used
                                    and self.revision_used == self.revision_requested),
        }
