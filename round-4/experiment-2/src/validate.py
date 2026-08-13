#!/usr/bin/env python3
"""T7: output validation and provenance.

  1  method_out.json validates against the exp_gen_sol_out schema
  2  every file is inside the size limit
  3  RESULTS.md regenerates BYTE-IDENTICALLY from method_out.json, which is the
     provenance guarantee: no number in the prose was hand-typed
  4  the per-member checkpoint files agree with the aggregated JSON
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from loguru import logger

import explib as EX
import report as RP

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

SKILL = Path("/ai-inventor/.claude/skills/aii-json")
VALIDATOR = SKILL / "scripts/aii_json_validate_schema.py"
VPY = SKILL / "../.ability_client_venv/bin/python"
SIZE_LIMIT_MB = 100.0


def check_schema() -> dict:
    r = subprocess.run([str(VPY), str(VALIDATOR), "--format", "exp_gen_sol_out",
                        "--file", str(EX.HERE / "method_out.json")],
                       capture_output=True, text=True)
    ok = "Validation PASSED" in r.stdout
    logger.info(f"schema: {'PASSED' if ok else 'FAILED'}")
    if not ok:
        logger.error(r.stdout[-2000:] + r.stderr[-1000:])
    return {"passed": ok, "output": (r.stdout + r.stderr)[-3000:]}


def check_sizes() -> dict:
    rows = []
    for p in sorted(EX.HERE.rglob("*")):
        if not p.is_file() or ".venv" in p.parts or ".git" in p.parts:
            continue
        mb = p.stat().st_size / 1e6
        if mb > 1.0:
            rows.append({"path": str(p.relative_to(EX.HERE)), "mb": round(mb, 2),
                         "over_limit": mb > SIZE_LIMIT_MB})
    rows.sort(key=lambda r: -r["mb"])
    over = [r for r in rows if r["over_limit"]]
    logger.info(f"size: {len(rows)} files >1MB, {len(over)} over {SIZE_LIMIT_MB}MB; "
                f"largest {rows[0]['mb'] if rows else 0} MB")
    return {"passed": not over, "files_over_1mb": rows[:20], "over_limit": over}


def check_results_md_provenance() -> dict:
    """RESULTS.md must be a pure function of method_out.json."""
    mo = EX.load_json(EX.HERE / "method_out.json")
    regen = RP.build_results_md(mo)
    on_disk = (EX.HERE / "RESULTS.md").read_text() if (EX.HERE / "RESULTS.md").exists() else ""
    ok = regen == on_disk
    logger.info(f"provenance: RESULTS.md regenerates identically = {ok}")
    return {"passed": ok, "n_chars": len(regen),
            "note": "RESULTS.md is formatted from method_out.json by report.py; a "
                    "byte-identical regeneration means no prose number was typed by hand"}


def check_member_consistency() -> dict:
    """Every per-member checkpoint must match the aggregated table."""
    mo = EX.load_json(EX.HERE / "method_out.json")
    rows = mo["metadata"]["results"]["h1_abliterated_arm"]["per_member"]
    bad = []
    for r in rows:
        p = EX.RESULTS / f"detect_{r['checkpoint']}.json"
        if not p.exists():
            bad.append({"checkpoint": r["checkpoint"], "reason": "missing detect file"})
            continue
        d = EX.load_json(p)
        a = d["detection"]["axes"].get("A_canned", {}).get("auroc")
        if a is None or r["A_auroc"] is None or abs(a - r["A_auroc"]) > 1e-12:
            bad.append({"checkpoint": r["checkpoint"], "reason": "A_auroc mismatch",
                        "file": a, "table": r["A_auroc"]})
    logger.info(f"member consistency: {len(rows) - len(bad)}/{len(rows)} agree")
    return {"passed": not bad, "n_members": len(rows), "mismatches": bad}


def check_dataset_rows() -> dict:
    mo = EX.load_json(EX.HERE / "method_out.json")
    counts = {d["dataset"]: len(d["examples"]) for d in mo["datasets"]}
    bad_predict = []
    for d in mo["datasets"]:
        for i, ex in enumerate(d["examples"]):
            for k, v in ex.items():
                if k.startswith("predict_") and not isinstance(v, str):
                    bad_predict.append(f"{d['dataset']}[{i}].{k}")
    logger.info(f"datasets: {counts}")
    return {"passed": not bad_predict, "row_counts": counts,
            "non_string_predict_fields": bad_predict[:10]}


def main():
    res = {
        "schema": check_schema(),
        "sizes": check_sizes(),
        "provenance": check_results_md_provenance(),
        "member_consistency": check_member_consistency(),
        "dataset_rows": check_dataset_rows(),
    }
    res["all_passed"] = all(v["passed"] for v in res.values() if isinstance(v, dict))
    EX.atomic_write_json(EX.RESULTS / "validation.json", res)
    logger.info(f"ALL VALIDATION PASSED = {res['all_passed']}")
    return 0 if res["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
