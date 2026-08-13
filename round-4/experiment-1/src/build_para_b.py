#!/usr/bin/env python3
"""STEP 2 driver: build and freeze paraphrase SET B.

Standalone so the (cheap) OpenRouter spend happens once and is cached on disk;
method.py then reads para_set_b.json and never re-generates it.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lib import ams as ams_mod  # noqa: E402
from lib import judge as judge_mod  # noqa: E402
from lib_iter3 import para_pairs as pp  # noqa: E402
from lib_iter4 import paraset  # noqa: E402

RESULTS = HERE / "results"
LOGS = HERE / "logs"
for d in (RESULTS, LOGS):
    d.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "para_b.log", rotation="10 MB", level="DEBUG")


@logger.catch(reraise=True)
def main() -> None:
    out_path = HERE / "para_set_b.json"
    targets = paraset.target_strings()
    logger.info(f"SET B: {len(targets)} target strings "
                f"({2 * ams_mod.N_PAIRS} toxicity + {2 * ams_mod.N_PAIRS} illicit "
                f"+ {ams_mod.N_PAIRS} benign)")
    assert len(targets) == 5 * ams_mod.N_PAIRS, len(targets)
    assert len(set(targets)) == len(targets), "target strings must be unique"

    rw = paraset.Rewriter(judge_mod.load_api_key(), HERE / "paraphrase_cache.jsonl",
                          hard_cap_usd=0.50, concurrency=8)
    try:
        results = rw.run(targets)
    finally:
        rw.close()
    logger.info(f"rewrites done: {rw.n_calls} calls, {rw.n_cache_hits} cache hits, "
                f"${rw.cost_usd:.4f}")

    asm = paraset.assemble(results)
    logger.info(f"SET B assembled: n_pairs_B={asm['n_pairs_B']}/"
                f"{asm['n_pairs_planned']} dropped={asm['dropped_indices']} "
                f"usable={asm['usable']}")

    # Independent re-verification of every KEPT string with the frozen apparatus.
    reverify = []
    for i, idx in enumerate(asm["kept_indices"]):
        for concept, orig, para in (
            ("toxicity_harmful", ams_mod.TOXICITY_PAIRS[idx][0],
             asm["para"]["toxicity"][i][0]),
            ("toxicity_benign", ams_mod.TOXICITY_PAIRS[idx][1],
             asm["para"]["toxicity"][i][1]),
            ("illicit_harmful", ams_mod.ILLICIT_PAIRS[idx][0],
             asm["para"]["illicit_facilitation"][i][0]),
            ("illicit_benign", ams_mod.ILLICIT_PAIRS[idx][1],
             asm["para"]["illicit_facilitation"][i][1]),
            ("harmful_instruction_benign", ams_mod.BENIGN_FOR_HARMFUL[idx],
             asm["para"]["harmful_instruction_benign"][i]),
        ):
            chk = pp.check_pair(orig, para)
            reverify.append({"pair_index": idx, "slot": concept, **chk})
    n_bad = sum(1 for r in reverify if not r["ok"])
    if n_bad:
        raise AssertionError(f"{n_bad} kept SET-B strings fail check_pair() on "
                             f"re-verification -- refusing to freeze")
    logger.info(f"re-verification: {len(reverify)}/{len(reverify)} kept strings PASS")

    overlap = paraset.cross_set_overlap(asm["para"])
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "procedure": {
            "primary_model": paraset.PRIMARY_MODEL,
            "escalation_model": paraset.ESCALATION_MODEL,
            "judge_model_excluded": judge_mod.JUDGE_MODEL,
            "temperature": paraset.TEMPERATURE,
            "max_attempts_before_escalation": paraset.MAX_ATTEMPTS,
            "prompt_template": paraset.PROMPT_TEMPLATE,
            "verifier": "lib_iter3.para_pairs.check_pair (FROZEN, iteration-3)",
            "no_hand_written_repairs": True,
            "drop_policy": ("a failing string drops its pair index from ALL three "
                            "concepts symmetrically so the sets stay aligned"),
        },
        "para": asm["para"],
        "kept_indices": asm["kept_indices"],
        "dropped_indices": asm["dropped_indices"],
        "n_pairs_B": asm["n_pairs_B"],
        "usable": asm["usable"],
        "unusable_reason": asm["unusable_reason"],
        "cross_set_overlap": overlap,
        "cost_usd": rw.cost_usd,
        "n_api_calls": rw.n_calls,
        "n_cache_hits": rw.n_cache_hits,
    }
    out_path.write_text(json.dumps(payload, indent=1))
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    logger.info(f"para_set_b.json written, sha256={sha}")

    audit = {
        "sha256_para_set_b": sha,
        "n_strings": len(results),
        "n_ok": sum(1 for r in results if r.get("ok")),
        "n_failed": asm["n_strings_failed"],
        "n_escalated": sum(1 for r in results if r.get("escalated") and r.get("ok")),
        "attempt_histogram": {
            str(k): sum(1 for r in results if r.get("ok") and r["n_attempts"] == k)
            for k in range(1, paraset.MAX_ATTEMPTS + 3)},
        "cost_usd": rw.cost_usd, "n_api_calls": rw.n_calls,
        "cross_set_overlap": overlap,
        "per_string": [
            {"original": r["original"], "paraphrase": r.get("paraphrase"),
             "ok": r.get("ok"), "n_attempts": r.get("n_attempts"),
             "model_used": r.get("model_used"), "escalated": r.get("escalated"),
             "attempts": r.get("attempts", [])}
            for r in results],
        "reverification": reverify,
        "n_reverified_pass": len(reverify) - n_bad,
    }
    (RESULTS / "paraphrase_audit_b.json").write_text(json.dumps(audit, indent=1))
    logger.info("results/paraphrase_audit_b.json written")


if __name__ == "__main__":
    main()
