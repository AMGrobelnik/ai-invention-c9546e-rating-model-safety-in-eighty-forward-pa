#!/usr/bin/env python3
"""SPI — Safety Proximity Indicators. Single entry point for the whole artifact.

Runs the Tier-0 experiment end to end:

  1. run_tier0      measure everything (Stages A-J), write out/tier0_raw.json
  2. build_output   reshape into the exp_gen_sol_out schema -> method_out.json
  3. make_figs      regenerate all figures FROM method_out.json alone
  4. validate       schema, finiteness, identifiability flags, control verdicts

OUR METHOD is SPI: four early-warning indicators of a refusal observable r_t,
measured during ordinary sampled generation on HARMLESS prompts only, with zero
harmful prompts and zero labels.

THE BASELINE is the field's standard strong approach: a supervised
difference-in-means refusal direction fitted on a 32/32 harmful-vs-benign
contrast set at the same layer, scored by AUROC — deliberately given the harmful
data SPI is denied. A second baseline (r_0 harmful-minus-benign margin) is also
reported. Both are computed in the SAME pipeline, on the SAME models, at the
SAME layer, so no implementation-level difference can explain a gap.

Usage:  python method.py [--mode {smoke,pilot,full}] [--skip-measure]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).parent
PY = str(ROOT / ".venv" / "bin" / "python")
if not Path(PY).exists():
    PY = sys.executable

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")


def run(step: str, args: list[str]) -> None:
    logger.info(f"=== {step}: {' '.join(args)} ===")
    proc = subprocess.run([PY, *args], cwd=ROOT)
    if proc.returncode != 0:
        raise RuntimeError(f"{step} failed with exit code {proc.returncode}")
    logger.info(f"=== {step}: OK ===")


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="full", choices=["smoke", "pilot", "full"])
    ap.add_argument("--skip-measure", action="store_true",
                    help="reuse an existing method_out.json / out/tier0_raw.json")
    args = ap.parse_args()

    if not args.skip_measure:
        run("1/4 measure", ["run_tier0.py", "--mode", args.mode,
                            "--out", "method_out.json"])
    run("2/4 build schema output", ["build_output.py"])
    run("3/4 figures", ["make_figs.py"])
    run("4/4 validate", ["validate_output.py"])
    logger.info("ALL STEPS COMPLETE — method_out.json is schema-valid")


if __name__ == "__main__":
    main()
