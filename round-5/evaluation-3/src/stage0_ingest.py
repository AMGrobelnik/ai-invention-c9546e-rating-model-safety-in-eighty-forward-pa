#!/usr/bin/env python3
"""STAGE 0 -- INGEST GATE.

sha256 every consumed file, then re-assert a set of archived legs read straight
out of the JSONs to full float repr. A leg passes only when the exact double is
reachable by an RFC-6901 pointer inside a stamped input; the pointer is
recorded, so a later stage can quote the number without retyping it. Any failed
leg HALTS the run with GATE_FAILED -- the paper is never repaired against an
input that cannot be reproduced.
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

from common import (HG_GLOB, INDEXED_ALIASES, OUT, REGISTRY, ROOT, is_num,
                    jdump, jload, setup_logging, sha256_file, walk_numeric)

# name -> (exact double, alias to search, human description)
GATE_LEGS: list[tuple[str, float, str, str]] = [
    ("logit_gap_harmful_rho_oriented", 0.6672543587855684, "E3",
     "iteration-3 discrimination matrix: logit-gap harmful oriented rho"),
    ("our_ams_rho_oriented", 0.3578030619574787, "E3",
     "iteration-3: our-AMS sigma oriented rho at the member level"),
    ("alpha50_rho_oriented", -0.2080952098456918, "E3",
     "iteration-3: alpha_50 oriented rho at the member level"),
    ("ams_paraphrase_refit_rho", 0.6540675137502804, "E3",
     "iteration-3: our-AMS paraphrase-refit oriented rho"),
    ("v1_lineage_rho_our_ams", 0.8214285714285715, "V1_S1",
     "iteration-4 eval_1: our-AMS oriented rho at the lineage-aggregated unit"),
    ("v1_lineage_oriented_delta", -0.9285714285714287, "V1_S1",
     "iteration-4 eval_1: oriented Delta at the lineage-aggregated unit"),
]

# legs asserted to a stated number of decimals rather than to full repr,
# because the artifact rounds them in its own summary.
GATE_LEGS_ROUNDED: list[tuple[str, float, int, str, str]] = [
    ("archived19_delta_A", 0.2963, 4, "E1",
     "scale panel: archived-19 block Delta_A"),
    ("full_panel_delta_A", 0.099, 3, "E1",
     "scale panel: full 52-member Delta_A"),
]


def build_leaf_index(docs: dict[str, object]) -> dict[str, list[tuple[str, object]]]:
    """alias -> [(pointer, leaf_value)] over every leaf in the document."""
    idx = {}
    for alias, doc in docs.items():
        idx[alias] = list(walk_numeric(doc))
    return idx


def find_exact(leaves: list[tuple[str, object]], target: float) -> list[str]:
    return [p for p, v in leaves if is_num(v) and float(v) == target]


def find_rounded(leaves: list[tuple[str, object]], target: float,
                 nd: int) -> list[str]:
    return [p for p, v in leaves if is_num(v) and round(float(v), nd) == round(target, nd)]


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage0")
    logger.info("STAGE 0 -- ingest gate")

    inputs = []
    for alias, (path, decl, art) in REGISTRY.items():
        if not path.exists():
            raise FileNotFoundError(f"registry alias {alias} missing: {path}")
        inputs.append({
            "alias": alias, "path": str(path),
            "path_relative_to_run": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path), "bytes": path.stat().st_size,
            "declared": decl, "artifact_id": art,
            "declaration_note": ("declared dependency" if decl == "declared"
                                 else "UNDECLARED_BUT_STAMPED: evaluation and "
                                      "paper artifacts cannot be declared as "
                                      "dependencies; read directly from disk"),
        })
    logger.info(f"stamped {len(inputs)} input files")

    docs = {a: jload(REGISTRY[a][0]) for a in INDEXED_ALIASES}
    leaves = build_leaf_index(docs)
    n_leaves = sum(len(v) for v in leaves.values())
    logger.info(f"indexed {n_leaves} leaves over {len(leaves)} documents")

    legs = []
    for name, target, alias, desc in GATE_LEGS:
        hits = find_exact(leaves[alias], target)
        legs.append({
            "leg": name, "expected": repr(target), "alias": alias,
            "description": desc, "match_mode": "exact_double",
            "n_pointers": len(hits), "pointers": hits[:6],
            "passed": bool(hits),
            "observed": (float(target) if hits else None),
        })
    for name, target, nd, alias, desc in GATE_LEGS_ROUNDED:
        hits = find_rounded(leaves[alias], target, nd)
        obs = None
        if hits:
            doc_leaves = dict(leaves[alias])
            obs = float(doc_leaves[hits[0]])
        legs.append({
            "leg": name, "expected": target, "alias": alias,
            "description": desc, "match_mode": f"rounded_{nd}dp",
            "n_pointers": len(hits), "pointers": hits[:6],
            "passed": bool(hits), "observed": obs,
        })

    failed = [l for l in legs if not l["passed"]]
    if failed:
        for l in failed:
            logger.error(f"GATE_FAILED leg={l['leg']} expected={l['expected']} "
                         f"not reachable in alias {l['alias']}")
        out = {"stage": "stage0_ingest", "gate": "GATE_FAILED",
               "inputs": inputs, "legs": legs, "failed_legs": failed}
        jdump(out, OUT / "stage0_manifest.json")
        raise SystemExit("GATE_FAILED: " + ", ".join(l["leg"] for l in failed))
    logger.info(f"ingest gate PASSED on {len(legs)} legs")

    # H-G probe: is the iteration-5 scale-panel experiment on disk yet?
    hg_hits = []
    for p in sorted(ROOT.glob(HG_GLOB)):
        try:
            txt = p.read_text()
        except OSError:
            continue
        if "logit_gap_harmful" in txt:
            hg_hits.append({"path": str(p), "sha256": sha256_file(p)})
    hg = {"status": "PRESENT" if hg_hits else "ABSENT_AT_RUN_TIME",
          "glob": HG_GLOB, "hits": hg_hits,
          "note": ("the H-G scale-panel rows are appended when the artifact "
                   "exists; absence is a normal outcome, not a failure")}
    logger.info(f"H-G probe: {hg['status']}")

    out = {
        "stage": "stage0_ingest", "gate": "GATE_PASSED",
        "n_inputs": len(inputs), "inputs": inputs,
        "n_leaves_indexed": n_leaves,
        "leaves_per_alias": {a: len(v) for a, v in leaves.items()},
        "legs": legs, "n_legs": len(legs),
        "h_g_probe": hg,
    }
    jdump(out, OUT / "stage0_manifest.json")
    logger.info(f"wrote {OUT / 'stage0_manifest.json'}")
    return out


if __name__ == "__main__":
    main()
