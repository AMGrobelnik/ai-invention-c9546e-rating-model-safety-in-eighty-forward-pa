#!/usr/bin/env python3
"""S6: the judge subsample.

The anchored regex is PRIMARY by pre-registration, so every headline survives a
total judge failure.  This stage exists only to report Cohen's kappa(regex,
judge) as a scorer-validity check.  It is cache-first (the archive already paid
for many of these items), stratified, hard-capped at $1.50 and aborted at $1.40.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

import explib as EX
from lib.judge_or import JUDGE_MODEL, Judge, load_api_key

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(EX.HERE / "logs/judge.log", rotation="30 MB", level="DEBUG")

HARD_CAP_USD = 1.50
ABORT_USD = 1.40
MAX_ITEMS = 400
CACHE = EX.RESULTS / "judge_cache.jsonl"
LEDGER = EX.RESULTS / "cost_ledger.jsonl"

ARCHIVE_CACHES = [
    EX.ARCH_EVAL / "results/judge_cache.jsonl",
    EX.ARCH_EVAL / "results/judge_cache_a4.jsonl",
    EX.ROOT / "iter_2/gen_art/gen_art_experiment_2/judge_cache.jsonl",
    EX.ROOT / "iter_2/gen_art/gen_art_experiment_1/judge_cache.jsonl",
    EX.ROOT / "iter_1/gen_art/gen_art_experiment_3/judge_cache.jsonl",
]


def seed_cache() -> dict:
    """Copy every archived judge cache in so hits cost $0."""
    seen, n_files, lines = set(), 0, []
    if CACHE.exists():
        for ln in CACHE.read_text().splitlines():
            if ln.strip():
                try:
                    seen.add(json.loads(ln)["key"])
                except (json.JSONDecodeError, KeyError):
                    pass
    for src in ARCHIVE_CACHES:
        if not src.exists():
            continue
        n_files += 1
        for ln in src.read_text().splitlines():
            if not ln.strip():
                continue
            try:
                rec = json.loads(ln)
            except json.JSONDecodeError:
                continue
            k = rec.get("key")
            # only the 4-class rubric transfers; the a4 cache uses a different one
            if not k or k in seen or rec.get("label") not in (
                    "REFUSAL", "COMPLIANCE", "PARTIAL", "DEGENERATE"):
                continue
            seen.add(k)
            lines.append(json.dumps({"key": k, "label": rec["label"],
                                     "raw": rec.get("raw", ""), "clean_parse": True,
                                     "cost": 0.0, "seeded_from": src.name}))
    if lines:
        with CACHE.open("a") as fh:
            fh.write("\n".join(lines) + "\n")
    logger.info(f"seeded {len(lines)} archived judge labels from {n_files} caches")
    return {"n_seeded": len(lines), "n_source_caches": n_files,
            "sources": [str(p) for p in ARCHIVE_CACHES if p.exists()]}


def collect_items() -> list[dict]:
    """Stratified pool over (member x {refusal, compliance} x stratum)."""
    pool = []
    for p in sorted(EX.RESULTS.glob("proj_*_items.json")):
        key = p.name[len("proj_"):-len("_items.json")]
        for it in json.loads(p.read_text()):
            pool.append({"member": key, "prompt": it["prompt"], "text": it["text"],
                         "stratum": it["stratum"],
                         "regex_refusal": bool(it["regex_refusal"]),
                         "source": "unsteered"})
    return pool


def stratified_sample(pool: list[dict], n: int, seed: int = 11) -> list[dict]:
    rng = np.random.default_rng(seed)
    cells: dict[tuple, list] = {}
    for it in pool:
        cells.setdefault((it["member"], it["regex_refusal"], it["stratum"]), []).append(it)
    if not cells:
        return []
    per = max(1, n // len(cells))
    out = []
    for k in sorted(cells):
        lst = cells[k]
        idx = rng.permutation(len(lst))[:per]
        out += [lst[i] for i in idx]
    rng.shuffle(out)
    return out[:n]


def main() -> dict:
    EX.RESULTS.mkdir(parents=True, exist_ok=True)
    seeded = seed_cache()
    pool = collect_items()
    if not pool:
        out = {"status": "NOT MEASURED", "reason": "no scored items on disk",
               "kappa": None, "cost_usd": 0.0}
        EX.atomic_write_json(EX.RESULTS / "judge.json", out)
        return out

    sample = stratified_sample(pool, MAX_ITEMS)
    logger.info(f"judging {len(sample)} of {len(pool)} scored items "
                f"({len({s['member'] for s in sample})} members)")
    try:
        key = load_api_key()
    except RuntimeError as exc:
        out = {"status": "NOT MEASURED", "reason": f"no API key: {exc}",
               "kappa": None, "cost_usd": 0.0, "seeded": seeded}
        EX.atomic_write_json(EX.RESULTS / "judge.json", out)
        logger.warning(out["reason"])
        return out

    j = Judge(JUDGE_MODEL, key, CACHE, hard_abort_usd=ABORT_USD, concurrency=12)
    pairs = [(s["prompt"], s["text"]) for s in sample]
    try:
        labels = j.run(pairs)
        status = "measured"
        reason = ""
    except Exception as exc:  # noqa: BLE001 - budget abort or API failure
        labels = [j.cache.get(j.key_for(p, c)) for p, c in pairs]
        status = "PARTIAL"
        reason = repr(exc)[:300]
        logger.warning(f"judge aborted: {reason}")
    finally:
        cost = j.cost_usd
        n_calls, n_hits = j.n_calls, j.n_cache_hits
        j.close()

    with LEDGER.open("a") as fh:
        fh.write(json.dumps({"stage": "judge", "model": JUDGE_MODEL,
                             "n_calls": n_calls, "n_cache_hits": n_hits,
                             "cost_usd": cost}) + "\n")

    got = [(s, lab) for s, lab in zip(sample, labels) if lab is not None]
    reg = ["REFUSAL" if s["regex_refusal"] else "COMPLIANCE" for s, _ in got]
    jud = [("REFUSAL" if lab == "REFUSAL" else "COMPLIANCE") for _, lab in got]
    kap = EX.cohens_kappa(reg, jud)

    per_stratum = {}
    for st in sorted({s["stratum"] for s, _ in got}):
        sub = [(s, lab) for s, lab in got if s["stratum"] == st]
        r = ["REFUSAL" if s["regex_refusal"] else "COMPLIANCE" for s, _ in sub]
        d = [("REFUSAL" if lab == "REFUSAL" else "COMPLIANCE") for _, lab in sub]
        per_stratum[st] = EX.cohens_kappa(r, d)

    label_counts: dict[str, int] = {}
    for _, lab in got:
        label_counts[lab] = label_counts.get(lab, 0) + 1

    out = {"status": status, "reason": reason, "model": JUDGE_MODEL,
           "n_sampled": len(sample), "n_labelled": len(got),
           "n_api_calls": n_calls, "n_cache_hits": n_hits,
           "cost_usd": cost, "hard_cap_usd": HARD_CAP_USD, "abort_usd": ABORT_USD,
           "kappa": kap["kappa"], "kappa_detail": kap,
           "kappa_per_stratum": per_stratum,
           "judge_label_counts": label_counts, "seeded": seeded,
           "invariant": "the anchored regex is PRIMARY; no headline number depends "
                        "on this stage"}
    EX.atomic_write_json(EX.RESULTS / "judge.json", out)
    logger.info(f"judge kappa={kap['kappa']:.4f} on n={kap['n']} "
                f"(${cost:.4f}, {n_calls} calls, {n_hits} cache hits)")
    return out


if __name__ == "__main__":
    main()
