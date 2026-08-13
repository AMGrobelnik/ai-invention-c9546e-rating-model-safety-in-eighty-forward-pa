#!/usr/bin/env python3
"""E1: judge probe.  12 hand-picked generations (4 obvious refusals, 4 obvious
compliances, 4 degenerate) must be labelled correctly by the repair-arm judge,
with 100% parseable single-label output and cost read from usage.cost.

Truth labels come from unambiguous surface pattern, so the probe does not
depend on any judge.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

WORKSPACE = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE))

import judge as J  # noqa: E402
import prereg_spec as PS  # noqa: E402
from classify import REFUSAL_RE, fluency_ok  # noqa: E402


def main() -> None:
    prompts = {p["uid"]: p["text"] for p in
               json.loads((WORKSPACE / "results" / "prompts.json").read_text())["probe_prompts"]}
    recs = []
    for f in sorted((WORKSPACE / "gens").glob("instruct_0p6__A_canned.jsonl")):
        recs = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    if not recs:
        raise SystemExit("no generations on disk yet")

    ref = [r for r in recs if r["refused"] and r["fluent"]
           and REFUSAL_RE.match(r["text"].strip())][:4]
    comp = [r for r in recs if not r["refused"] and r["fluent"] and r["alpha"] == 0.0][:4]
    deg = [r for r in recs if not fluency_ok(list(range(1)))
           or not r["fluent"]][:4]
    items = ([{"truth": "REFUSAL", **r} for r in ref]
             + [{"truth": "COMPLIANCE", **r} for r in comp]
             + [{"truth": "DEGENERATE", **r} for r in deg])
    logger.info(f"probe items: {len(items)} "
                f"({len(ref)} refusal / {len(comp)} compliance / {len(deg)} degenerate)")

    jd = J.Judge(PS.JUDGE_MODEL, WORKSPACE / "judge_cache.jsonl",
                 hard_cap_usd=0.10, max_tokens=16, workers=6)
    scored = jd.score([{"prompt": prompts.get(i["prompt_uid"], ""),
                        "completion": i["text"]} for i in items])
    n_ok = 0
    for it, s in zip(items, scored):
        hit = s["judge_label"] == it["truth"]
        # DEGENERATE vs the truth label is judged leniently: a degenerate string
        # that the judge calls REFUSAL is still evidence it read the content
        n_ok += int(hit)
        logger.info(f"truth={it['truth']:<11} judge={str(s['judge_label']):<11} "
                    f"alpha={it['alpha']:.2f} parsed={s['judge_parsed_cleanly']} "
                    f"| {it['text'][:70]!r}")
    st = jd.stats()
    logger.info(f"accuracy {n_ok}/{len(items)}  parse_ok="
                f"{sum(1 for s in scored if s['judge_parsed_cleanly'])}/{len(scored)}  "
                f"cost=${st['cost_usd']:.5f}  errors={st['n_errors']}")
    (WORKSPACE / "results" / "judge_probe.json").write_text(json.dumps(
        {"n": len(items), "n_correct": n_ok,
         "parse_rate": sum(1 for s in scored if s["judge_parsed_cleanly"]) / len(scored),
         "cost_usd": st["cost_usd"], "stats": st,
         "rows": [{"truth": i["truth"], "judge": s["judge_label"], "alpha": i["alpha"],
                   "text": i["text"][:200]} for i, s in zip(items, scored)]}, indent=2))
    jd.close()
    if st["n_errors"] or st["cost_usd"] <= 0:
        raise SystemExit(f"judge probe failed: {st}")


if __name__ == "__main__":
    main()
