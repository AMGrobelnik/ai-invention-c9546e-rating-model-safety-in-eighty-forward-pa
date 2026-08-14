#!/usr/bin/env python3
"""Preview the 25 candidate HF datasets: metadata, size, revision SHA, columns, sample rows.

Writes one JSON per candidate to logs/prev_json/ plus a combined summary table.
Uses the HF datasets-server preview API (no full download) with a streaming fallback.
"""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from huggingface_hub import HfApi
from loguru import logger

HERE = Path(__file__).resolve().parent
OUT = HERE / "logs" / "prev_json"
OUT.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "preview.log", rotation="30 MB", level="DEBUG")

CANDIDATES = [
    "walledai/XSTest",
    "natolambert/xstest-v2-copy",
    "Paul/XSTest",
    "walledai/AdvBench",
    "JailbreakBench/JBB-Behaviors",
    "walledai/HarmBench",
    "mlabonne/harmful_behaviors",
    "mlabonne/harmless_alpaca",
    "HuggingFaceH4/no_robots",
    "databricks/databricks-dolly-15k",
    "yahma/alpaca-cleaned",
    "Salesforce/wikitext",
    "TrustAIRLab/in-the-wild-jailbreak-prompts",
    "rubend18/ChatGPT-Jailbreak-Prompts",
    "TrustAIRLab/forbidden_question_set",
    "walledai/StrongREJECT",
    "sorry-bench/sorry-bench-202503",
    "LibrAI/do-not-answer",
    "PKU-Alignment/BeaverTails",
    "allenai/wildjailbreak",
    "allenai/wildguardmix",
    "walledai/MaliciousInstruct",
    "GAIR/lima",
    "allenai/real-toxicity-prompts",
    "Anthropic/hh-rlhf",
]

API = HfApi()
SESS = requests.Session()
TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}


def _get(url: str, params: dict) -> dict | None:
    try:
        r = SESS.get(url, params=params, headers=HEADERS, timeout=60)
        if r.status_code == 200:
            return r.json()
        logger.debug(f"{url} {params} -> HTTP {r.status_code}: {r.text[:200]}")
    except requests.RequestException as exc:
        logger.debug(f"{url} {params} failed: {exc}")
    return None


def preview(repo: str) -> dict:
    rec: dict = {"repo_id": repo}
    try:
        info = API.dataset_info(repo, files_metadata=True)
        rec["revision"] = info.sha
        rec["downloads"] = info.downloads
        rec["likes"] = info.likes
        rec["gated"] = bool(info.gated)
        rec["tags"] = list(info.tags or [])[:30]
        card = info.card_data.to_dict() if info.card_data else {}
        rec["license"] = card.get("license")
        sizes = [(s.rfilename, s.size) for s in (info.siblings or []) if s.size]
        rec["repo_bytes"] = sum(sz for _, sz in sizes)
        rec["n_files"] = len(info.siblings or [])
    except Exception as exc:  # noqa: BLE001 - report, do not crash the sweep
        rec["error_model_info"] = f"{type(exc).__name__}: {exc}"
        logger.error(f"{repo}: dataset_info failed: {exc}")
        return rec

    splits = _get("https://datasets-server.huggingface.co/splits", {"dataset": repo})
    rec["splits"] = (splits or {}).get("splits", [])
    if not rec["splits"]:
        rec["error_splits"] = "datasets-server returned no splits"
        return rec

    first = rec["splits"][0]
    rows = _get(
        "https://datasets-server.huggingface.co/first-rows",
        {"dataset": repo, "config": first["config"], "split": first["split"]},
    )
    if rows:
        rec["columns"] = [f["name"] for f in rows.get("features", [])]
        rec["sample_rows"] = [r["row"] for r in rows.get("rows", [])[:3]]
    size = _get("https://datasets-server.huggingface.co/size", {"dataset": repo})
    if size:
        d = size.get("size", {}).get("dataset", {})
        rec["num_rows_total"] = d.get("num_rows")
        rec["num_bytes_parquet"] = d.get("num_bytes_parquet_files")
        rec["per_config"] = [
            {
                "config": c.get("config"),
                "num_rows": c.get("num_rows"),
                "num_bytes_parquet": c.get("num_bytes_parquet_files"),
            }
            for c in size.get("size", {}).get("configs", [])
        ]
    return rec


def main() -> None:
    logger.info(f"Previewing {len(CANDIDATES)} candidates")
    with ThreadPoolExecutor(max_workers=8) as ex:
        recs = list(ex.map(preview, CANDIDATES))
    for rec in recs:
        (OUT / (rec["repo_id"].replace("/", "__") + ".json")).write_text(
            json.dumps(rec, indent=2, default=str)
        )
    summary = []
    for r in recs:
        summary.append(
            {
                "repo_id": r["repo_id"],
                "downloads": r.get("downloads"),
                "likes": r.get("likes"),
                "license": r.get("license"),
                "gated": r.get("gated"),
                "revision": (r.get("revision") or "")[:12],
                "rows": r.get("num_rows_total"),
                "parquet_bytes": r.get("num_bytes_parquet"),
                "columns": r.get("columns"),
                "configs": [c["config"] for c in (r.get("per_config") or [])],
                "error": r.get("error_model_info") or r.get("error_splits"),
            }
        )
    (OUT / "_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    for s in summary:
        mb = (s["parquet_bytes"] or 0) / 1e6
        logger.info(
            f"{s['repo_id']:<45} dl={s['downloads']} rows={s['rows']} "
            f"{mb:.1f}MB lic={s['license']} cols={s['columns']} err={s['error']}"
        )


if __name__ == "__main__":
    main()
