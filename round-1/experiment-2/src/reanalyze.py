#!/usr/bin/env python3
"""Pre-declared secondary analysis: sensitivity of the decisive statistic to the
compliance-resumption run length.

Reads the per-token logs in gens/ and recomputes alpha_down for several values of
COMPLIANCE_RUN without re-running any model. Purely deterministic re-scoring of
already-recorded token streams.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger
from transformers import AutoTokenizer

import stats as S
from classify import RefusalClassifier, build_token_sets, compliance_resumed, fluency_ok

HERE = Path(__file__).resolve().parent
GENDIR = HERE / (sys.argv[1] if len(sys.argv) > 1 else "gens")
RESDIR = HERE / "results"
RUNS = (6, 10, 14)
ALPHA_MIN = float(sys.argv[2]) if len(sys.argv) > 2 else -1.5

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{message}")


def load_arm(path: Path) -> dict | None:
    if not path.exists():
        return None
    steps, summary = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("_summary"):
            summary = rec
        else:
            steps.append(rec)
    return {"steps": steps, "summary": summary}


def alpha_down_for_run(clf, prefix_ids: list[int], arm: dict, run: int) -> tuple[float, bool]:
    flags, alphas, gen = [], [], []
    for st in arm["steps"]:
        gen.append(int(st["token"]))
        alphas.append(float(st["alpha"]))
        flags.append(
            clf.token_is_refusalish(prefix_ids + gen) or clf.window_has_marker(gen)
        )
    idx = compliance_resumed(flags, run)
    if idx is None:
        return ALPHA_MIN, True
    return alphas[idx], False


def main() -> None:
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
    clf = RefusalClassifier(tok, build_token_sets(tok))
    out: dict = {"compliance_runs": list(RUNS), "per_model": {}}
    for mdir in sorted(GENDIR.iterdir()):
        if not mdir.is_dir():
            continue
        model = mdir.name
        by_prompt: dict[int, dict[int, list[float]]] = {}
        for entry_path in sorted(mdir.glob("p*_entry.jsonl")):
            stem = entry_path.name[: -len("_entry.jsonl")]
            pid = int(stem.split("_")[0][1:])
            seed = int(stem.split("_")[1][1:])
            entry = load_arm(entry_path)
            dn = load_arm(mdir / f"{stem}_down_retained.jsonl")
            fa = load_arm(mdir / f"{stem}_down_forced_a.jsonl")
            if entry is None or dn is None or fa is None:
                continue
            prefix = [int(s["token"]) for s in entry["steps"]][:-1]
            if not all(
                fluency_ok([int(s["token"]) for s in a["steps"]]) for a in (entry, dn, fa)
            ):
                continue
            for run in RUNS:
                a_dn, _ = alpha_down_for_run(clf, prefix, dn, run)
                a_fa, _ = alpha_down_for_run(clf, prefix, fa, run)
                by_prompt.setdefault(pid, {}).setdefault(run, []).append(a_fa - a_dn)
        per_run = {}
        for run in RUNS:
            vals = [
                sum(v[run]) / len(v[run])
                for v in by_prompt.values()
                if run in v and v[run]
            ]
            per_run[str(run)] = S.bootstrap_mean(vals)
        out["per_model"][model] = per_run
        logger.info(f"{model}: {json.dumps(per_run)}")
    (RESDIR / (sys.argv[3] if len(sys.argv) > 3 else "secondary_compliance_run.json")).write_text(json.dumps(out, indent=1))
    logger.info("wrote results/secondary_compliance_run.json")


if __name__ == "__main__":
    main()
