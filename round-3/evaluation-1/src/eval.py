#!/usr/bin/env python3
"""End-to-end entry point for the lexicality re-certification evaluation.

Stages, in order (each checkpoints to results/ so a partial run is reportable):

  prereg   stamp results/prereg_eval.json (must precede any AUROC)
  gpu      re-derive the four axes per checkpoint (V2), harvest the AB-blind
           held-out pool (V1), re-encode it with forward passes only, project
           onto every axis (V3)                                     [GPU]
  a12      Analysis 1 (held-out behavioural certification) and
           Analysis 2 (axis-contrast-unit dose + matched-contrast test)
  judge    Analysis 3/4 labelling via OpenRouter, cache-first, hard $1.50 cap
  a34      aggregate the judged items into Analyses 3 and 4
  assemble eval_out.json + provenance.json + the paper subsection + README
  figures  regenerate every figure from the analysis output only

Usage:
  python eval.py                      # everything, in order
  python eval.py --stages a12,assemble
  python eval.py --checkpoints instruct_0p6   # smoke tier (one checkpoint)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
VENV = HERE / ".venv/bin/python"
GPU_VENV = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_2/"
                "gen_art/gen_art_experiment_1/.venv/bin/python")

STAGES = ["prereg", "gpu", "a12", "judge", "a34", "assemble", "figures"]


def run(cmd: list[str], name: str) -> None:
    logger.info(f"--- {name}: {' '.join(str(c) for c in cmd)}")
    t0 = time.time()
    r = subprocess.run([str(c) for c in cmd], cwd=HERE)
    if r.returncode != 0:
        raise RuntimeError(f"stage {name} failed with exit code {r.returncode}")
    logger.info(f"--- {name} done in {time.time() - t0:.0f}s")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default=",".join(STAGES))
    ap.add_argument("--checkpoints", default="all")
    ap.add_argument("--max-items", type=int, default=2000)
    ap.add_argument("--per-cell", type=int, default=20)
    ap.add_argument("--a4-per-cell", type=int, default=45)
    args = ap.parse_args()

    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(HERE / "logs/eval.log", level="DEBUG")

    want = [s.strip() for s in args.stages.split(",") if s.strip()]
    for s in want:
        if s not in STAGES:
            raise SystemExit(f"unknown stage {s!r}; choose from {STAGES}")

    py, gpy = str(VENV), str(GPU_VENV if GPU_VENV.exists() else VENV)
    if "prereg" in want:
        run([py, "prereg.py"], "prereg")
    if "gpu" in want:
        run([gpy, "-u", "gpu_stage.py", "--checkpoints", args.checkpoints,
             "--max-items", args.max_items], "gpu")
    if "a12" in want:
        run([py, "-u", "analysis12.py"], "a12")
    if "judge" in want:
        run([py, "-u", "judge_stage.py", "--checkpoints", args.checkpoints,
             "--per-cell", args.per_cell, "--a4-per-cell", args.a4_per_cell], "judge")
    if "a34" in want:
        run([py, "-u", "analysis34.py"], "a34")
    if "assemble" in want:
        run([py, "-u", "assemble.py"], "assemble")
    if "figures" in want:
        run([py, "-u", "figures.py"], "figures")
    logger.info("evaluation complete")


if __name__ == "__main__":
    main()
