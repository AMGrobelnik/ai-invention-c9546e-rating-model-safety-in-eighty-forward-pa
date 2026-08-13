#!/usr/bin/env python3
"""Same numbers, both counting units.

A pure-reanalysis EVALUATION over the FROZEN iteration-2/3 archives: zero GPU,
zero generation, zero LLM/API spend, no model downloads, no network.

  stage 0  ingest, unit assertions, reproduction gate      -> out/stage0.json
  stage 1  dual aggregation (the H-U repair)               -> out/stage1_dual_aggregation.json
  stage 2  threshold sensitivity surface (H-T)             -> out/stage2_threshold_surface.json
  stage 3  the three missing tables (H-A)                  -> out/tables/*.{md,csv}
  stage 4  prose audit + repaired replacement text         -> out/stage4_prose_audit.json
  assemble fold into eval_out.json + README.md

Each stage writes its own json and is independently re-runnable, so a late
failure never loses earlier work.

    uv run eval.py              # everything
    uv run eval.py --stage 2    # one stage
"""

from __future__ import annotations

import argparse
import sys
import time

from loguru import logger

from common import setup_logging

STAGES = {
    0: ("stage0_ingest", "ingest, assertions, reproduction gate"),
    1: ("stage1_dual", "dual aggregation"),
    2: ("stage2_sweep", "threshold sensitivity surface"),
    3: ("stage3_tables", "the three tables"),
    4: ("stage4_prose", "prose audit"),
    5: ("assemble", "assemble eval_out.json + README.md"),
}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", type=int, default=None, choices=sorted(STAGES),
                    help="run a single stage (default: all, in order)")
    args = ap.parse_args()
    setup_logging("eval")

    todo = [args.stage] if args.stage is not None else sorted(STAGES)
    t0 = time.time()
    for st in todo:
        mod_name, what = STAGES[st]
        logger.info(f"=== stage {st}: {what} ({mod_name}.py) ===")
        t = time.time()
        mod = __import__(mod_name)
        mod.main()
        logger.info(f"=== stage {st} done in {time.time() - t:.1f}s ===")
    logger.info(f"ALL DONE in {time.time() - t0:.1f}s; cost_usd = 0.0")


if __name__ == "__main__":
    sys.exit(main())
