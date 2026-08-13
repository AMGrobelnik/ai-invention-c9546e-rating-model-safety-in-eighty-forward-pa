#!/usr/bin/env python3
"""STAGE 0 -- provenance manifest and the PRE-REGISTRATION.

The pre-registration is written and sha256-stamped BEFORE any new statistic
exists.  It is never edited afterwards; amendments go into an append-only list
with a trigger, which is the convention this project already uses.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from loguru import logger

from common5 import (D1, E3, FROZEN, HERE, OUT, R4, R4_RESULTS, V3, V4,
                     jdump, jload, sha256_file, sha256_text, setup_logging)

PREREG_PATH = HERE / "prereg_iter5_eval.json"

PREREG = {
    "artifact": "iter_5 gen_art_evaluation_1 -- recheck the read-vs-act coupling "
                "and the verdict rule",
    "kind": "PURE REANALYSIS of the FROZEN iteration-4 read-vs-act tree",
    "spend": {"llm_usd": 0.0, "gpu_seconds": 0, "generation_calls": 0,
              "statement": "$0.00 LLM spend, zero GPU, zero generation. Every "
                           "number comes from files already on disk."},
    "primary_statistic": {
        "name": "within-axis-A across-member Spearman rho",
        "x": "axis-A maximum induced refusal rate (T3)",
        "y": "axis-A held-out detection AUROC on the model's own spontaneous "
             "text (T2)",
        "population": "detection-powered members only (the population the "
                      "iteration-4 pre-registration says the statistic exists on)",
        "expected_n_members": 14,
    },
    "aggregation_units": ["member (one row per checkpoint)",
                          "lineage (member values averaged within lineage_id)"],
    "bootstrap": {"scheme": "lineage-clustered percentile bootstrap",
                  "n_boot": 10000, "seed": 20260813,
                  "rule": "the number of resampling units is printed next to "
                          "every CI"},
    "permutation": {"scheme": "exhaustive over all 7! = 5040 permutations of the "
                              "lineage labels (statsx.lineage_permutation_p)",
                    "attainable_floor": 1.0 / 5040.0,
                    "floor_note": "only the identity permutation is guaranteed to "
                                  "reproduce |rho| when cluster blocks are unequal, "
                                  "so the floor is 1/5040 = 1.98e-4, not 2/5040. "
                                  "Any p landing exactly on the floor is flagged."},
    "verdict_strings": {
        "COUPLING_SURVIVES_WITHIN_AXIS": {
            "trigger": "within-axis-A member-unit rho >= 0.50 AND the "
                       "lineage-clustered CI excludes 0 AND the lineage-unit "
                       "estimate carries the same sign"},
        "COUPLING_IS_AXIS_TYPE_CONTRAST": {
            "trigger": "within-axis-A CI covers 0 AND the pooled 70-pair CI "
                       "excludes 0 AND the variance decomposition attributes the "
                       "majority share to between-axis-type"},
        "UNDERPOWERED": {
            "trigger": "within-axis-A CI covers 0 AND its half-width > 0.35"},
        "precedence": "COUPLING_SURVIVES_WITHIN_AXIS is checked first; if it does "
                      "not fire, COUPLING_IS_AXIS_TYPE_CONTRAST and UNDERPOWERED "
                      "are both evaluated and BOTH are emitted when both fire, "
                      "because 'the confound explains it' and 'we could not have "
                      "detected it anyway' are different statements and a reader "
                      "is entitled to know when both are true.",
    },
    "attainability_simulation": {
        "estimator": "the artifact's OWN prompt-clustered percentile bootstrap "
                     "(explib.cluster_boot_indices + explib.detection_stats "
                     "semantics, including the >=5-per-class resample guard) with "
                     "explib.verdict_from_ci applied to the resulting CI",
        "n_per_class": [5, 10, 20, 40, 80, 160],
        "true_auroc": [0.50, 0.55, 0.60, 0.69, 0.75, 0.90, 1.00],
        "items_per_prompt": [1, 2, 4],
        "n_replicates_per_cell": 2000,
        "n_boot_inner": 2000,
        "separation": "d = sqrt(2) * Phi^-1(AUROC) between two unit normals",
        "perfect_separation_ns": [7, 12, 28, 32, 33],
    },
    "reproduction_gate": {
        "legs": ["G1 pooled rho 0.629 + CI [0.465, 0.803]",
                 "G2 secondary rho 0.448 + censoring 0.771",
                 "G3 within-member mean rho 0.715",
                 "G4 all 30 per-member axis-A AUROCs and CIs",
                 "G5 the T1b arm table",
                 "G6 the axis-A verdict tally, resolving 18/0/10 vs 20/1/9",
                 "G7 lineage-id-string versus lineage-count bookkeeping"],
        "tolerance": 1e-6,
        "stop_rule": "if G1 fails, STOP the restatement and ship a "
                     "diagnostic-only eval_out.json",
    },
    "standing_rules": {
        "SALVAGE_IS_FORBIDDEN":
            "If the within-axis estimate lands near 0.43 with a CI covering zero, "
            "the generated prose says so in the reviewer's own words: 'the axis "
            "that induces is also the axis that reads, but among models the two "
            "qualities are only weakly and non-significantly related.' The tokens "
            "'trending', 'marginally significant', 'suggestive', 'borderline "
            "significant', 'approaching significance' and 'nearly significant' are "
            "BANNED from the emitted prose and the final assertion pass greps for "
            "them and fails the run if any appears.",
        "NO_SILENT_SUBSTITUTION":
            "Any expected input file that is absent is logged under "
            "provenance.missing with its exact path; the affected leg is dropped "
            "or demoted to summary level and labelled, never imputed.",
        "PROSE_IS_GENERATED":
            "Every number in the replacement text carries a JSON pointer into "
            "eval_out.json and the run ends with an executed assertion that "
            "resolves every pointer and fails on any mismatch.",
    },
    "amendments": [],
}


def input_manifest() -> tuple[list[dict], list[str]]:
    """Every input path with size + sha256; absent paths logged separately."""
    wanted: list[Path] = [
        R4 / "method_out.json", R4 / "full_method_out.json", R4 / "RESULTS.md",
        R4 / "explib.py", R4 / "method.py", R4 / "report.py", R4 / "gpu_stage.py",
        R4 / "figures.py", R4 / "prereg.py",
        R4_RESULTS / "prereg.json", R4_RESULTS / "panel_resolved.json",
        R4_RESULTS / "validation.json", R4_RESULTS / "tests.json",
        R4_RESULTS / "archive_inventory.json", R4_RESULTS / "judge.json",
        E3 / "method.py", E3 / "prereg_iter3.json",
        E3 / "lib_iter3/statsx.py",
        D1,
        V4 / "eval_out.json", V4 / "common.py", V4 / "stage0_ingest.py",
        V4 / "stage1_dual.py", V4 / "stage2_sweep.py", V4 / "stage3_tables.py",
        V4 / "stage4_prose.py", V4 / "assemble.py", V4 / "eval.py",
        V3 / "eval_out.json",
    ]
    wanted += sorted(R4_RESULTS.glob("detect_*.json"))
    wanted += sorted(R4_RESULTS.glob("proj_*_items.json"))
    wanted += sorted(R4_RESULTS.glob("proj_*.npz"))
    wanted += sorted(R4_RESULTS.glob("induce_*.json"))
    wanted += sorted(E3.glob("results/iter3_member_*.json"))
    wanted += sorted(FROZEN.glob("*.py")) + sorted((FROZEN / "lib").glob("*.py"))
    wanted += sorted((FROZEN / "lib_iter3").glob("*.py"))

    inputs, missing = [], []
    for p in wanted:
        if p.exists() and p.is_file():
            inputs.append({"path": str(p), "bytes": p.stat().st_size,
                           "sha256": sha256_file(p)})
        else:
            missing.append(str(p))
    return inputs, missing


def frozen_src_gate() -> dict:
    """frozen_src/ must be byte-identical to the sources it was copied from."""
    checks = []
    pairs = [(FROZEN / "explib.py", R4 / "explib.py")]
    for p in sorted((FROZEN / "lib").glob("*.py")):
        pairs.append((p, R4 / "lib" / p.name))
    for p in sorted((FROZEN / "lib_iter3").glob("*.py")):
        pairs.append((p, E3 / "lib_iter3" / p.name))
    for local, src in pairs:
        ok = src.exists() and sha256_file(local) == sha256_file(src)
        checks.append({"local": str(local), "source": str(src),
                       "byte_identical": bool(ok)})
    return {"n_files": len(checks), "n_byte_identical": sum(c["byte_identical"]
                                                            for c in checks),
            "all_pass": all(c["byte_identical"] for c in checks),
            "files": checks}


def main() -> dict:
    setup_logging("stage0")
    logger.info("STAGE 0: provenance + pre-registration")

    inputs, missing = input_manifest()
    logger.info(f"inputs found: {len(inputs)}   missing: {len(missing)}")
    for m in missing:
        logger.warning(f"MISSING input (logged, not substituted): {m}")

    fg = frozen_src_gate()
    logger.info(f"frozen_src byte-identity: {fg['n_byte_identical']}/{fg['n_files']}")

    # the pre-registration is written FIRST, then hashed, then never edited
    jdump(PREREG_PATH, PREREG)
    prereg_sha = sha256_file(PREREG_PATH)
    logger.info(f"prereg sha256 = {prereg_sha}")

    r4meta = jload(R4 / "method_out.json")["metadata"]
    out = {
        "prereg_path": str(PREREG_PATH),
        "prereg_sha256": prereg_sha,
        "prereg": PREREG,
        "upstream_prereg_sha256_recomputed": sha256_text(
            (R4_RESULTS / "prereg.json").read_text()),
        "upstream_prereg_sha256_recorded": r4meta.get("prereg_sha256"),
        "upstream_prereg_file_sha256": sha256_file(R4_RESULTS / "prereg.json"),
        "provenance": {
            "inputs": inputs,
            "n_inputs": len(inputs),
            "missing": missing,
            "frozen_src_gate": fg,
            "libraries": {
                "python": sys.version.split()[0],
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "platform": platform.platform(),
            },
            "spend": PREREG["spend"],
        },
    }
    jdump(OUT / "stage0.json", out)
    logger.info("STAGE 0 done")
    return out


if __name__ == "__main__":
    main()
