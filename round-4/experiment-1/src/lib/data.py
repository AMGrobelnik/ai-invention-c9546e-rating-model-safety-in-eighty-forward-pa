#!/usr/bin/env python3
"""Loader + integrity assertions for the frozen iteration-1 corpus."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from loguru import logger

DATA_PATH = Path(
    "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/"
    "gen_art_dataset_1/full_data_out.json"
)

EXPECTED_BLOCKS = {
    "harmless_dynamics": 43,
    "xstest_overrefusal": 450,
    "plain_harmful": 594,
    "jailbreak_suite": 400,
    "layer_contrast": 256,
    "wikitext_fluency": 200,
    "refusal_token_lexicon": 10,
    "panel_manifest": 160,
}


@lru_cache(maxsize=1)
def load_corpus(path: str | None = None) -> dict[str, list[dict]]:
    p = Path(path) if path else DATA_PATH
    if not p.exists():
        raise FileNotFoundError(f"frozen corpus not found at {p}")
    raw = json.loads(p.read_text())
    folds: dict[str, list[dict]] = {}
    for block in raw["datasets"]:
        rows = block["examples"]
        fold = rows[0]["metadata_fold"]
        folds[fold] = rows
    return folds


def assert_corpus(folds: dict[str, list[dict]]) -> dict:
    """T0.3 assertions. Returns a report dict; raises on a hard mismatch."""
    report: dict = {"blocks": {}, "checks": {}}
    total = 0
    for name, n in EXPECTED_BLOCKS.items():
        got = len(folds.get(name, []))
        report["blocks"][name] = {"expected": n, "got": got, "ok": got == n}
        total += got
        if got != n:
            raise AssertionError(f"block {name}: expected {n} rows, got {got}")
    report["n_rows"] = total
    if total != 2113:
        raise AssertionError(f"corpus should hold 2113 rows, holds {total}")

    core80 = [r for r in folds["plain_harmful"] if r["metadata_meta"].get("in_core80")]
    report["checks"]["plain_harmful_in_core80"] = len(core80)
    if len(core80) != 80:
        raise AssertionError(f"in_core80 should be 80 rows, is {len(core80)}")

    sel = [r for r in folds["harmless_dynamics"] if r["metadata_meta"].get("selected")]
    report["checks"]["harmless_dynamics_selected"] = len(sel)
    if len(sel) != 40:
        raise AssertionError(f"harmless_dynamics selected should be 40, is {len(sel)}")

    missing_delivery = [
        r for r in folds["jailbreak_suite"] if not r["metadata_meta"].get("delivery")
    ]
    report["checks"]["jailbreak_missing_delivery"] = len(missing_delivery)
    if missing_delivery:
        raise AssertionError("jailbreak_suite rows without meta.delivery")

    xs = folds["xstest_overrefusal"]
    n_safe = sum(1 for r in xs if r["metadata_meta"]["label"] == "safe")
    n_unsafe = sum(1 for r in xs if r["metadata_meta"]["label"] == "unsafe")
    report["checks"]["xstest_safe"] = n_safe
    report["checks"]["xstest_unsafe"] = n_unsafe
    if (n_safe, n_unsafe) != (250, 200):
        raise AssertionError(f"xstest split should be 250/200, is {n_safe}/{n_unsafe}")

    report["checks"]["lexicon_families"] = sorted(
        r["metadata_meta"]["tokenizer_family"] for r in folds["refusal_token_lexicon"]
    )
    logger.info(f"corpus assertions PASS: {total} rows, 8 blocks")
    return report


# --------------------------------------------------------------------------
# Convenience selectors
# --------------------------------------------------------------------------
def benign_prompts(folds) -> list[str]:
    """The 40 vetted everyday user turns, in frozen uid order."""
    rows = [r for r in folds["harmless_dynamics"] if r["metadata_meta"].get("selected")]
    rows.sort(key=lambda r: r["metadata_uid"])
    return [r["input"] for r in rows]


def core80(folds) -> list[dict]:
    rows = [r for r in folds["plain_harmful"] if r["metadata_meta"].get("in_core80")]
    rows.sort(key=lambda r: r["metadata_uid"])
    return rows


def contrast_split(folds) -> dict[str, list[str]]:
    """layer_contrast harmful/benign halves, used ONLY for outcome-blind site scans."""
    rows = sorted(folds["layer_contrast"], key=lambda r: r["metadata_uid"])
    harm = [r["input"] for r in rows if r["metadata_meta"]["polarity"] == "harmful"]
    ben = [r["input"] for r in rows if r["metadata_meta"]["polarity"] != "harmful"]
    return {"harmful": harm, "benign": ben}


def lexicon_for_family(folds, family: str) -> dict | None:
    for r in folds["refusal_token_lexicon"]:
        if r["metadata_meta"]["tokenizer_family"] == family:
            return r["metadata_meta"]
    return None


def manifest_row(folds, repo: str) -> dict | None:
    for r in folds["panel_manifest"]:
        if r["metadata_meta"]["hf_repo_id"] == repo:
            return r["metadata_meta"]
    return None


def jailbreak_for(folds, pair_uid: str, template_id: str) -> dict | None:
    for r in folds["jailbreak_suite"]:
        m = r["metadata_meta"]
        if m.get("pair_id") == pair_uid and m.get("template_id") == template_id:
            return r
    return None
