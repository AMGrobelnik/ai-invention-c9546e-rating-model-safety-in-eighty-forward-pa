#!/usr/bin/env python3
"""T9 FINAL VALIDATION of method_out.json.

Checks, in order:
  1. it parses and validates against a hand-written exp_gen_sol_out schema
  2. every numeric field is finite — no NaN/Inf leaking from a failed fit
     (a failed fit must be null WITH a reason string, never a quiet number)
  3. every lambda carries the `identifiable` flag
  4. every control verdict boolean is present
  5. the verdict code is one of the five pre-registered values
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

from loguru import logger

ROOT = Path(__file__).parent

VERDICT_CODES = {
    "LAMBDA_IDENTIFIABLE_ORDERING_AS_PREDICTED",
    "LAMBDA_IDENTIFIABLE_ORDERING_ABSENT_OR_REVERSED",
    "LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY",
    "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING",
    "PIPELINE_FAILURE",
}

REQUIRED_CONTROLS = [
    "random_axis_reproduces_ordering",
    "pos_probe_reproduces_ordering",
    "random_direction_reproduces_ordering",
    "lambda_identifiable_at_achieved_geometry",
    "epsilon_linear_regime_exists",
]

SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["datasets"],
    "properties": {
        "metadata": {"type": "object"},
        "datasets": {
            "type": "array", "minItems": 1,
            "items": {
                "type": "object", "required": ["dataset", "examples"],
                "properties": {
                    "dataset": {"type": "string"},
                    "examples": {
                        "type": "array", "minItems": 1,
                        "items": {
                            "type": "object", "required": ["input", "output"],
                            "properties": {"input": {"type": "string"},
                                           "output": {"type": "string"}},
                            "patternProperties": {
                                "^metadata_[a-zA-Z_][a-zA-Z0-9_]*$": {},
                                "^predict_[a-zA-Z_][a-zA-Z0-9_]*$": {"type": "string"},
                            },
                            "additionalProperties": False,
                        },
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


def walk_nonfinite(obj: Any, path: str = "") -> list[str]:
    bad: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            bad += walk_nonfinite(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad += walk_nonfinite(v, f"{path}[{i}]")
    elif isinstance(obj, float) and not math.isfinite(obj):
        bad.append(f"{path} = {obj}")
    return bad


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "method_out.json")
    d = json.loads(path.read_text())
    fails: list[str] = []
    warns: list[str] = []

    # 1 — schema
    try:
        import jsonschema

        jsonschema.validate(d, SCHEMA)
        logger.info("1. schema: PASS")
    except Exception as exc:  # noqa: BLE001 - report, do not raise
        fails.append(f"schema: {exc}")

    n_ex = sum(len(x["examples"]) for x in d["datasets"])
    logger.info(f"   {len(d['datasets'])} datasets, {n_ex} examples, "
                f"{path.stat().st_size / 1e6:.2f} MB")

    # 2 — no non-finite numbers anywhere
    bad = walk_nonfinite(d)
    if bad:
        fails.append(f"non-finite numbers ({len(bad)}), first 5: {bad[:5]}")
    else:
        logger.info("2. all numeric fields finite: PASS")

    md = d.get("metadata", {})
    raw_path = ROOT / "out" / "tier0_raw.json"

    # 3 — every lambda carries the identifiability flag
    if raw_path.exists():
        raw = json.loads(raw_path.read_text())
        missing = [i for i, r in enumerate(raw.get("lambda", []))
                   if "identifiable" not in r]
        if missing:
            fails.append(f"{len(missing)} lambda rows lack `identifiable`")
        else:
            n = len(raw.get("lambda", []))
            n_id = sum(1 for r in raw["lambda"] if r["identifiable"])
            logger.info(f"3. identifiable flag on all {n} lambda rows: PASS "
                        f"({n_id} flagged identifiable)")
        # failed fits must be null WITH a reason
        silent = []
        for r in raw.get("lambda", []):
            for tag in ("layerL", "final"):
                e = r.get(tag, {}).get("estimates", {})
                for name in ("est1_nls", "est2_loglin", "est3_ar1"):
                    f = e.get(name, {})
                    if f.get("lambda") is None and not f.get("reason"):
                        silent.append(f"{r['model']}/{r['prompt_id']}/{tag}/{name}")
        if silent:
            fails.append(f"{len(silent)} failed fits are null WITHOUT a reason string")
        else:
            logger.info("   failed fits all carry a reason string: PASS")
    else:
        warns.append(f"{raw_path} absent — skipped lambda-flag checks")

    # 4 — control verdicts present
    controls = md.get("controls", {})
    missing_c = [c for c in REQUIRED_CONTROLS if c not in controls]
    if missing_c:
        fails.append(f"missing control verdicts: {missing_c}")
    else:
        logger.info("4. all five control verdicts present: PASS")
        for c in REQUIRED_CONTROLS:
            v = controls[c]
            val = v.get("value") if isinstance(v, dict) else v
            logger.info(f"   {c}: {val}")

    # 5 — verdict code
    code = md.get("verdict", {}).get("code")
    if code not in VERDICT_CODES:
        fails.append(f"verdict code {code!r} is not one of the five pre-registered codes")
    else:
        logger.info(f"5. verdict: {code}")

    for w in warns:
        logger.warning(w)
    if fails:
        for f in fails:
            logger.error(f)
        logger.error(f"VALIDATION FAILED — {len(fails)} problem(s)")
        return 1
    logger.info("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
