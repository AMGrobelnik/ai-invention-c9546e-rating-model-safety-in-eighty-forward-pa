#!/usr/bin/env python3
"""Shared paths, logging, IO and the frozen source registry for the H-A
number-discipline reanalysis.

Every number that this artifact ships is resolved to an (alias, RFC-6901
pointer) pair against a file whose sha256 is stamped in stage 0. Nothing is
hand-typed, and the registry below is the single place a path is written down.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
TABLES = OUT / "tables"
LOGS = HERE / "logs"
for _d in (OUT, TABLES, LOGS):
    _d.mkdir(parents=True, exist_ok=True)

ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")

# --- artifact workspaces -------------------------------------------------
E2_DIR = ROOT / "iter_4/gen_art/gen_art_experiment_2"      # art_1xT3w1joqeJ8
E1_DIR = ROOT / "iter_4/gen_art/gen_art_experiment_1"      # art_CZaytBH8uL4_
E3_DIR = ROOT / "iter_3/gen_art/gen_art_experiment_1"      # art_3Cndd5cKsYV0
D1_DIR = ROOT / "iter_1/gen_art/gen_art_dataset_1"         # art_CKWQh2cOQLLQ
V1_DIR = ROOT / "iter_4/gen_art/gen_art_evaluation_1"      # art__tq3ZgPRYB0B
V2_DIR = ROOT / "iter_4/gen_art/gen_art_evaluation_2"      # art_P-_YL8tdIwqF
R1_DIR = ROOT / "iter_4/gen_art/gen_art_research_1"        # art_G5SIDXT53EAW
A1_DIR = ROOT / "iter_3/gen_art/gen_art_evaluation_1"      # the ARCHIVED item pool
DRAFT_JSON = (ROOT / "iter_4/gen_paper_text/gen_paper_text"
              / ".terminal_claude_agent_struct_out.json")
PRIOR_DRAFT = ROOT / "iter_3/gen_paper_text/gen_paper_text/paper_body.md"
# H-G probe target: the iteration-5 scale-panel experiment, if it exists yet.
HG_GLOB = "iter_5/gen_art/gen_art_experiment_*/full_method_out.json"

# alias -> (path, declared?, artifact id)
#   declared   = named in the artifact plan's DECLARED DEPENDENCIES block
#   undeclared = read straight from disk (evaluation artifacts cannot be
#                declared as dependencies); recorded UNDECLARED_BUT_STAMPED.
REGISTRY: dict[str, tuple[Path, str, str]] = {
    "E2":        (E2_DIR / "full_method_out.json", "declared", "art_1xT3w1joqeJ8"),
    "E2_RESULTS": (E2_DIR / "RESULTS.md", "declared", "art_1xT3w1joqeJ8"),
    "E2_README": (E2_DIR / "README.md", "declared", "art_1xT3w1joqeJ8"),
    "E2_SUMMARY": (E2_DIR / ".terminal_claude_agent_struct_out.json", "declared",
                   "art_1xT3w1joqeJ8"),
    "E2_PANEL":  (E2_DIR / "results/panel_resolved.json", "declared", "art_1xT3w1joqeJ8"),
    "E1":        (E1_DIR / "full_method_out.json", "declared", "art_CZaytBH8uL4_"),
    "E1_PREREG": (E1_DIR / "prereg_iter4.json", "declared", "art_CZaytBH8uL4_"),
    "E3":        (E3_DIR / "full_method_out.json", "declared", "art_3Cndd5cKsYV0"),
    "E3_PREREG": (E3_DIR / "prereg_iter3.json", "declared", "art_3Cndd5cKsYV0"),
    "D1":        (D1_DIR / "full_data_out.json", "declared", "art_CKWQh2cOQLLQ"),
    "V1":        (V1_DIR / "eval_out.json", "undeclared", "art__tq3ZgPRYB0B"),
    "V1_S0":     (V1_DIR / "out/stage0.json", "undeclared", "art__tq3ZgPRYB0B"),
    "V1_S1":     (V1_DIR / "out/stage1_dual_aggregation.json", "undeclared",
                  "art__tq3ZgPRYB0B"),
    "V1_S2":     (V1_DIR / "out/stage2_threshold_surface.json", "undeclared",
                  "art__tq3ZgPRYB0B"),
    "V1_S3":     (V1_DIR / "out/stage3_tables.json", "undeclared", "art__tq3ZgPRYB0B"),
    "V1_S4":     (V1_DIR / "out/stage4_prose_audit.json", "undeclared",
                  "art__tq3ZgPRYB0B"),
    "V2":        (V2_DIR / "eval_out.json", "undeclared", "art_P-_YL8tdIwqF"),
    "V2_VERDICT": (V2_DIR / "results/verdict.json", "undeclared", "art_P-_YL8tdIwqF"),
    "V2_MATCHED": (V2_DIR / "results/matched_cells.json", "undeclared",
                   "art_P-_YL8tdIwqF"),
    "V2_RETENTION": (V2_DIR / "results/retention_curves.json", "undeclared",
                     "art_P-_YL8tdIwqF"),
    "V2_PREREG": (V2_DIR / "results/prereg_eval.json", "undeclared", "art_P-_YL8tdIwqF"),
    "R1":        (R1_DIR / "research_out.json", "undeclared", "art_G5SIDXT53EAW"),
    "A1_ANALYSIS1": (A1_DIR / "results/analysis1.json", "undeclared",
                     "iter_3_gen_art_evaluation_1"),
    "A1_ANALYSIS2": (A1_DIR / "results/analysis2.json", "undeclared",
                     "iter_3_gen_art_evaluation_1"),
    "A1_PROVENANCE": (A1_DIR / "results/provenance.json", "undeclared",
                      "iter_3_gen_art_evaluation_1"),
    "A1_EVAL":   (A1_DIR / "eval_out.json", "undeclared", "iter_3_gen_art_evaluation_1"),
    "DRAFT":     (DRAFT_JSON, "undeclared", "iter_4_gen_paper_text"),
    "PRIOR_DRAFT": (PRIOR_DRAFT, "undeclared", "iter_3_gen_paper_text"),
}

# JSON aliases whose numeric leaves feed the traceability index.
INDEXED_ALIASES = ["E2", "E1", "E3", "V1", "V1_S0", "V1_S1", "V1_S2", "V1_S3",
                   "V1_S4", "V2", "V2_VERDICT", "V2_MATCHED", "V2_RETENTION",
                   "V2_PREREG", "E1_PREREG", "E3_PREREG", "E2_PANEL", "R1",
                   "D1", "A1_ANALYSIS1", "A1_ANALYSIS2", "A1_PROVENANCE",
                   "A1_EVAL"]

VERDICT_STRINGS = [
    "READS", "AMBIGUOUS", "UNDEFINED", "AT_CHANCE",
    "PROTOCOL_DOES_NOT_DISCRIMINATE", "DOES_NOT_SURVIVE",
    "REVERSAL_DOES_NOT_SURVIVE", "REVERSAL_SURVIVES",
    "REVERSAL_CONFOUNDED_BY_DEGENERACY",
    "SIGN_SURVIVES", "SIGN_FLIPS", "EXCLUSION_LOST_AT_MEMBER_LEVEL",
    "EXCLUDES_AT_NEITHER", "NORM_MISMATCH_DOES_NOT_EXPLAIN",
    "B_IS_A_GENUINE_INDUCER", "UNRELIABLE", "DEFINED",
]

AGG_UNITS = {"member", "lineage", "prompt", "item", "axis-pair", "checkpoint",
             "grid point", "reference", "NA"}


def setup_logging(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def jload(p: Path):
    return json.loads(Path(p).read_text())


def _default(o):
    import numpy as np
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(f"not serialisable: {type(o)}")


def jdump(obj, p: Path) -> None:
    """Sorted keys and a fixed separator: two runs of the same content produce
    byte-identical files, which is what the regeneration assertion needs."""
    Path(p).write_text(json.dumps(obj, indent=1, default=_default,
                                  sort_keys=True, allow_nan=True))


def esc_ptr(tok: str) -> str:
    """RFC 6901 escaping."""
    return tok.replace("~", "~0").replace("/", "~1")


def resolve_pointer(doc, pointer: str):
    """RFC 6901 resolution. '' is the whole document."""
    if pointer in ("", "/"):
        return doc if pointer == "" else doc[""]
    if not pointer.startswith("/"):
        raise ValueError(f"pointer must start with '/': {pointer!r}")
    cur = doc
    for raw in pointer[1:].split("/"):
        tok = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(tok)]
        else:
            cur = cur[tok]
    return cur


def walk_numeric(doc, prefix: str = ""):
    """Yield (pointer, value) for every numeric / bool / string leaf."""
    stack = [(prefix, doc)]
    while stack:
        ptr, node = stack.pop()
        if isinstance(node, dict):
            for k, v in node.items():
                stack.append((f"{ptr}/{esc_ptr(str(k))}", v))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                stack.append((f"{ptr}/{i}", v))
        else:
            yield ptr, node


def is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) \
        and not (isinstance(x, float) and (math.isnan(x) or math.isinf(x)))


def require(d: dict, key: str, where: str):
    if key not in d:
        raise KeyError(f"missing key {key!r} in {where}; have {sorted(d)[:25]}")
    return d[key]
