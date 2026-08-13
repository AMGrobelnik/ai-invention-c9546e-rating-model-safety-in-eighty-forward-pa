#!/usr/bin/env python3
"""The pre-registered model panel: 7 lineages, 6 architecture families, 19 members.

`lineage_id` is the resampling unit for every lineage-clustered statistic and is
taken from the frozen dataset's `panel_manifest` rows, never inferred from a name.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Member:
    key: str
    repo: str
    lineage: str  # short lineage label (L1..L7)
    lineage_id: str  # the manifest lineage_id (pretrained base at the root)
    family: str  # architecture family
    level: str  # base | instruct | abliterated | uncensored
    approx_gb: float
    note: str = ""
    fallbacks: tuple[str, ...] = field(default_factory=tuple)


PANEL: list[Member] = [
    # ---- L1  Qwen3-0.6B (the iteration-1 anchor) ----------------------------
    Member("l1_base", "Qwen/Qwen3-0.6B-Base", "L1", "Qwen/Qwen3-0.6B-Base", "Qwen3", "base", 1.2),
    Member("l1_instruct", "Qwen/Qwen3-0.6B", "L1", "Qwen/Qwen3-0.6B-Base", "Qwen3", "instruct", 1.5),
    Member(
        "l1_abliterated",
        "mlabonne/Qwen3-0.6B-abliterated",
        "L1",
        "Qwen/Qwen3-0.6B-Base",
        "Qwen3",
        "abliterated",
        1.2,
        note="iteration-1 anchor abliterated member",
        fallbacks=("huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2",),
    ),
    # ---- L2  Qwen3-1.7B (carries the H4 blind-spot case study) --------------
    Member("l2_base", "Qwen/Qwen3-1.7B-Base", "L2", "Qwen/Qwen3-1.7B-Base", "Qwen3", "base", 3.4),
    Member("l2_instruct", "Qwen/Qwen3-1.7B", "L2", "Qwen/Qwen3-1.7B-Base", "Qwen3", "instruct", 4.1),
    Member(
        "l2_abliterated",
        "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2",
        "L2",
        "Qwen/Qwen3-1.7B-Base",
        "Qwen3",
        "abliterated",
        3.4,
        note="huihui-ai/Qwen3-1.7B-abliterated (v1) is gated; v2 is the manifest-verified row",
    ),
    Member(
        "l2_uncensored",
        "UnfilteredAI/DAN-Qwen3-1.7B",
        "L2",
        "Qwen/Qwen3-1.7B-Base",
        "Qwen3",
        "uncensored",
        6.9,
        note="H4 behavioural-uncensored candidate sharing the L2 lineage",
    ),
    # ---- L3  Llama-3.2-1B (second architecture family) ----------------------
    Member("l3_base", "unsloth/Llama-3.2-1B", "L3", "meta-llama/Llama-3.2-1B", "Llama3", "base", 2.5),
    Member(
        "l3_instruct", "unsloth/Llama-3.2-1B-Instruct", "L3", "meta-llama/Llama-3.2-1B", "Llama3",
        "instruct", 2.5,
    ),
    Member(
        "l3_abliterated", "huihui-ai/Llama-3.2-1B-Instruct-abliterated", "L3",
        "meta-llama/Llama-3.2-1B", "Llama3", "abliterated", 3.0,
    ),
    # ---- L4  Qwen2.5-1.5B ---------------------------------------------------
    Member("l4_base", "Qwen/Qwen2.5-1.5B", "L4", "Qwen/Qwen2.5-1.5B", "Qwen2", "base", 3.1),
    Member("l4_instruct", "Qwen/Qwen2.5-1.5B-Instruct", "L4", "Qwen/Qwen2.5-1.5B", "Qwen2", "instruct", 3.1),
    Member(
        "l4_abliterated", "huihui-ai/Qwen2.5-1.5B-Instruct-abliterated", "L4", "Qwen/Qwen2.5-1.5B",
        "Qwen2", "abliterated", 3.1,
    ),
    # ---- L5  SmolLM2-1.7B ---------------------------------------------------
    Member("l5_base", "HuggingFaceTB/SmolLM2-1.7B", "L5", "HuggingFaceTB/SmolLM2-1.7B", "SmolLM2", "base", 3.4),
    Member(
        "l5_instruct", "HuggingFaceTB/SmolLM2-1.7B-Instruct", "L5", "HuggingFaceTB/SmolLM2-1.7B",
        "SmolLM2", "instruct", 3.4,
    ),
    # ---- L6  SmolLM2-360M (cheap sixth lineage, the iter-1 EWS outlier) -----
    Member("l6_base", "HuggingFaceTB/SmolLM2-360M", "L6", "HuggingFaceTB/SmolLM2-360M", "SmolLM2", "base", 0.7),
    Member(
        "l6_instruct", "HuggingFaceTB/SmolLM2-360M-Instruct", "L6", "HuggingFaceTB/SmolLM2-360M",
        "SmolLM2", "instruct", 0.7,
    ),
    # ---- L7  TinyLlama (a 7th lineage and a 6th architecture family; listed
    #          in the plan as the documented drop-in replacement, and run in
    #          full because a 7th independent unit materially changes what the
    #          headline correlation is worth) --------------------------------
    Member("l7_base", "TinyLlama/TinyLlama_v1.1", "L7", "TinyLlama/TinyLlama_v1.1", "Llama2", "base", 4.4),
    Member(
        "l7_instruct", "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "L7",
        "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", "Llama2", "instruct", 2.2,
    ),
]

BY_KEY: dict[str, Member] = {m.key: m for m in PANEL}

# Members reserved for the H1'' lexical-artefact control arm: the three L1
# members plus one cross-family member.
H1PP_MEMBERS: tuple[str, ...] = ("l1_base", "l1_instruct", "l1_abliterated", "l3_instruct",
                                 "l4_instruct")

# Lineages carrying the D4 ratchet generalisation (>=3 lineages, >=3 families).
RATCHET_LINEAGES: tuple[str, ...] = ("L1", "L3", "L6", "L4", "L2")

# AMS Table-I reproduction-gate checkpoints (ungated mirrors where needed).
AMS_GATE = [
    {"name": "Llama-3.2-3B-Instruct", "repo": "unsloth/Llama-3.2-3B-Instruct", "published": 8.37},
    {"name": "gemma-2-2b-it", "repo": "unsloth/gemma-2-2b-it", "published": 4.80},
    {"name": "Llama-3.2-1B-Instruct", "repo": "unsloth/Llama-3.2-1B-Instruct", "published": 4.55},
]

# Default running order: cheap lineages first so a time overrun costs the
# expensive members, and the two 1.7B lineages land last (disk pressure).
DEFAULT_ORDER: list[str] = [
    "l1_instruct", "l1_abliterated", "l1_base",
    "l6_instruct", "l6_base",
    "l3_instruct", "l3_abliterated", "l3_base",
    "l4_instruct", "l4_abliterated", "l4_base",
    "l2_instruct", "l2_abliterated", "l2_uncensored", "l2_base",
    "l5_instruct", "l5_base",
    "l7_instruct", "l7_base",
]
