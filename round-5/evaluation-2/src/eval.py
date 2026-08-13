#!/usr/bin/env python3
"""Is the refusal axis reading meaning or wording?  (and: does the one published
leakage control move our detection headline?)

Pure re-analysis of the FROZEN iter-4 experiment_2 tree (art_1xT3w1joqeJ8).
No model weights, no sampling from a model, no steering, no training.

  STAGE 0  provenance, pre-registration, reproduction gate R0, POWERED set
  STAGE 1  Part-1 sampling frame (stratified, projection-tertile, IPW)
  STAGE 2  five-class semantic labels (cache-first, hard $2.00 cap)
  STAGE 3  Part 1 -- H-L: semantic vs regex labels
  STAGE 4  Part 2 -- H-X: the leave-one-prompt-out leakage control
  STAGE 5  assembly: eval_out.json, section-5.1 paragraph, boundary examples

Usage:  uv run eval.py [--members N] [--no-judge] [--boot N]
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import resource
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from loguru import logger

import eval_lib as L

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(L.LOGS / "run.log"), rotation="30 MB", level="DEBUG")

# Container is 29 GB / 4 CPU.  This job holds a handful of (n<=2000,) float arrays
# at a time; 6 GB is already an order of magnitude more than it can use.
RAM_BUDGET = 6 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))
N_CPUS = len(os.sched_getaffinity(0))


# ===========================================================================
# STAGE 0 -- provenance, pre-registration, reproduction gate
# ===========================================================================
def stage0_provenance(keys: list[str]) -> dict:
    logger.info("STAGE 0.1: sha256-stamping every input")
    inputs: dict[str, str] = {}

    def stamp(p: Path) -> None:
        inputs[str(p.relative_to(L.ROOT))] = L.sha256_file(p)

    for k in keys:
        for pat in (f"results/proj_{k}.npz", f"results/proj_{k}_items.json",
                    f"results/detect_{k}.json"):
            stamp(L.EXP / pat)
        for ax in L.AXES_ALL:
            p = L.EXP / f"results/axes/{k}_{ax}.npy"
            if p.exists():
                stamp(p)
    for pat in ("method_out.json", "explib.py", "judge_stage.py", "gpu_stage.py",
                "lib/classify.py", "lib/direction.py", "results/panel_resolved.json",
                "results/prereg.json"):
        stamp(L.EXP / pat)
    stamp(L.RE3 / "judge_stage.py")
    stamp(L.ARCH / "judge.py")
    stamp(L.ARCH / "prereg_spec.py")
    stamp(L.AUD / "full_method_out.json")
    stamp(L.EV4 / "eval_lib2.py")
    for c in (L.EV4 / "results/judge_cache_5class.jsonl",
              L.EXP / "results/judge_cache.jsonl"):
        if c.exists():
            stamp(c)
    logger.info(f"  stamped {len(inputs)} input files")
    return inputs


def write_prereg(inputs: dict) -> dict:
    """Every threshold and verdict rule, stamped BEFORE any new AUROC or label."""
    doc = {
        "artifact": "gen_art_evaluation_2 (iter 5) -- H-L semantic relabel + H-X leakage control",
        "frozen_tree": str(L.EXP.relative_to(L.ROOT)),
        "nature": "pure re-analysis: no weights loaded, no generation, no steering, no training",
        "constants": {
            "N_BOOT": L.N_BOOT, "BOOT_SEED": L.BOOT_SEED, "SAMPLE_SEED": L.SAMPLE_SEED,
            "MIN_PER_CLASS_POWERED": L.MIN_PER_CLASS, "R0_TOL": L.R0_TOL,
            "TARGET_PER_MEMBER": L.TARGET_PER_MEMBER,
            "PER_REGEX_CLASS": L.PER_REGEX_CLASS,
            "FLOOR_PER_MEMBER": L.FLOOR_PER_MEMBER,
            "MIDDLE_TERTILE_WEIGHT": L.MIDDLE_TERTILE_WEIGHT,
            "HARD_CAP_USD": L.HARD_CAP_USD, "STOP_FRACTION": L.STOP_FRACTION,
            "PROTOCOLS": L.PROTOCOLS, "AXES_PART2": L.AXES_P2,
            "FIVE_CLASSES": L.FIVE_CLASSES,
        },
        "gates": {
            "R0": ("recompute per-member axis-A and axis-B AUROC, the paired A-B delta "
                   "with its prompt-clustered CI, and the within-stratum AUROC, from "
                   "proj_<KEY>.npz + proj_<KEY>_items.json alone using explib.centre_by_stratum "
                   "and explib.detection_stats IMPORTED from the archive; require "
                   f"max|delta| <= {L.R0_TOL} on every member x axis cell.  Also re-derive "
                   "labels from lib/classify.REFUSAL_RE.match(item['text']) and assert "
                   "byte-equality with the stored npz labels array.  On ANY failure emit "
                   "REPRODUCTION_FAILED and stop before any restatement."),
            "POWERED": ("members with min(n_refusal, n_compliance) >= 40 in the archived "
                        "detect json AND a proj_<KEY>.npz on disk."),
        },
        "part1_sampling": {
            "frame": "regex-label x prompt-stratum x projection TERTILE of the "
                     "stratum-centred axis-A projection; middle tertile weighted 2x",
            "order_rule": "descending archived n_refusal (balanced) if the budget cannot "
                          "cover every POWERED member",
            "weighting": "inverse-probability weights w = n_cell / n_sampled_cell; every "
                         "corpus-level quantity reported weighted AND unweighted",
            "caveat": "the frame deliberately over-samples the decision boundary, so raw "
                      "per-arm accuracy on the subset is NOT a corpus estimate",
        },
        "part1_labels": {
            "rubric": "A4_LABELS / A4_RUBRIC verbatim from RE3/judge_stage.py",
            "client": "ARCH/judge.py verbatim, rubric globals swapped (EV4 eval_lib2 shims)",
            "temperature": 0,
            "semantic_any_refusal": list(L.REFUSAL_CLASSES),
            "excluded_from_primary_auroc": ["DEGENERATE", "PARTIAL"],
            "partial_sensitivity": ["as_refusal", "as_compliance", "dropped(primary)"],
        },
        "part1_verdict_rules": {
            "SEMANTIC_LABELS_CONFIRM_READING":
                "pooled DELTA_L CI includes 0 or is positive AND pooled AUROC_noncanonical "
                f">= {L.AUROC_NONCANON_MIN} with a CI lower bound above the member's own "
                "20-draw random READING band upper edge (archived random_null; NOT 0.500)",
            "READS_CANONICAL_WORDING_ONLY":
                f"AUROC_noncanonical <= {L.AUROC_NONCANON_MIN} or its CI covers the random "
                f"band while AUROC_canonical stays >= {L.AUROC_CANON_MIN}",
            "UNDERPOWERED":
                f"pooled n_REFUSAL_NONCANONICAL < {L.POOLED_NONCANON_MIN_N} or fewer than "
                f"{L.MIN_POWERED_MEMBERS} POWERED members completed",
        },
        "part2_verdict_rules": {
            "LEAKAGE_CONTROL_SMALL_DELTA":
                f"|pooled DELTA_X| for fold_centre_scale on axis A <= {L.X_SMALL_ABS} with a "
                f"CI excluding {L.X_SMALL_CI_EXCLUDE}",
            "LEAKAGE_CONTROL_LARGE_DELTA":
                f"point estimate <= {L.X_LARGE_POINT} or the CI excludes {L.X_LARGE_CI_EXCLUDE}",
            "otherwise": "LEAKAGE_CONTROL_INCONCLUSIVE with the CI",
            "comparator": f"Mehta arXiv:2607.13346 moved 0.761 -> 0.425, delta {-L.MEHTA_DELTA}",
        },
        "aggregation_units": "every pooled quantity reported at BOTH units (member-level "
                             "with a lineage-clustered bootstrap, and lineage-aggregated), "
                             "with both verdict strings, per H-U",
        "failure_modes": {
            "R0_fail": "stop, REPRODUCTION_FAILED with the offending cells",
            "judge_budget_or_api": "degrade to the members completed, report achieved "
                                   "coverage, UNDERPOWERED under 5 POWERED members; Part 2 "
                                   "is judge-free and completes in full regardless",
            "few_noncanonical": "report the weighted prevalence with its CI and emit "
                                "UNDERPOWERED for the AUROC only",
            "missing_npz": "restrict to available members and list the missing ones",
            "undefined_auroc": "report NaN explicitly, never impute",
        },
        "input_sha256": inputs,
    }
    L.dump_json(L.RESULTS / "prereg_eval.json", doc)
    doc_sha = L.sha256_file(L.RESULTS / "prereg_eval.json")
    logger.info(f"  prereg_eval.json sha256 {doc_sha[:16]}...")
    return {"prereg_sha256": doc_sha, "prereg": doc}


def _absdiff(a, b) -> float:
    """NaN-aware cell delta: both NaN is a match (0.0); exactly one NaN never is."""
    fa, fb = np.isfinite(a), np.isfinite(b)
    if not fa and not fb:
        return 0.0
    if fa != fb:
        return float("inf")
    return float(abs(a - b))


def _r0_one(key: str) -> dict:
    """Worker: reproduce one member's archived detection statistics."""
    EX = L.import_explib()
    CL = L.import_classify()
    m = L.load_member(key)
    arch = m["detect"]["detection"]

    relabel = np.array([bool(CL.REFUSAL_RE.match(it["text"])) for it in m["items"]])
    label_match = bool(np.array_equal(relabel, m["labels"]))
    field_match = bool(np.array_equal(
        np.array([bool(it["regex_refusal"]) for it in m["items"]]), m["labels"]))

    st = EX.detection_stats(m["proj"], m["labels"], m["strata"], m["clusters"],
                            n_boot=EX.N_BOOT, seed=EX.BOOT_SEED)
    cells, worst = {}, 0.0
    for ax in sorted(m["proj"]):
        a, b = st["axes"][ax], arch["axes"][ax]
        d = {
            "auroc": _absdiff(a["auroc"], b["auroc"]),
            "ci_lo": _absdiff(a["auroc_ci95"][0], b["auroc_ci95"][0]),
            "ci_hi": _absdiff(a["auroc_ci95"][1], b["auroc_ci95"][1]),
            "within_stratum": _absdiff(a["auroc_within_stratum"],
                                       b["auroc_within_stratum"]),
        }
        if sorted(a["auroc_per_stratum"]) != sorted(b["auroc_per_stratum"]):
            d["per_stratum_keyset"] = float("inf")
        for s, ps in a["auroc_per_stratum"].items():
            d[f"per_stratum_{s}"] = _absdiff(ps, b["auroc_per_stratum"].get(s, float("nan")))
        cells[ax] = {kk: float(vv) for kk, vv in d.items()}
        worst = max(worst, max(d.values()))
    pa, pb = st.get("paired_A_minus_B"), arch.get("paired_A_minus_B")
    if pa and pb:
        pd = {"delta": _absdiff(pa["delta"], pb["delta"]),
              "ci_lo": _absdiff(pa["ci95"][0], pb["ci95"][0]),
              "ci_hi": _absdiff(pa["ci95"][1], pb["ci95"][1])}
        cells["paired_A_minus_B"] = {kk: float(vv) for kk, vv in pd.items()}
        worst = max(worst, max(pd.values()))
    ok = bool(worst <= L.R0_TOL and label_match)
    return {"member": key, "pass": ok, "max_abs_delta": float(worst),
            "n_cells_checked": int(sum(len(v) for v in cells.values())),
            "regex_labels_byte_identical": label_match,
            "items_regex_refusal_field_matches": field_match,
            "cells": cells,
            "recomputed": {ax: st["axes"][ax]["auroc"] for ax in sorted(m["proj"])},
            "recomputed_paired_A_minus_B": (pa or {}).get("delta", float("nan"))}


def stage0_gate(keys: list[str]) -> dict:
    logger.info(f"STAGE 0.2: reproduction gate R0 over {len(keys)} members "
                f"({N_CPUS} workers)")
    t0 = time.time()
    ck = L.RESULTS / "r0_gate.json"
    sig = L.sha256_text("|".join(keys) + f"|{L.N_BOOT}")
    if ck.exists() and L.load_json(ck).get("signature") == sig:
        rows = L.load_json(ck)["members"]
        logger.info("  (restored from checkpoint)")
    else:
        with ProcessPoolExecutor(max_workers=max(1, N_CPUS - 1)) as ex:
            rows = list(ex.map(_r0_one, keys))
        L.dump_json(ck, {"signature": sig, "members": rows})
    n_cells = sum(r["n_cells_checked"] for r in rows)
    worst = max(r["max_abs_delta"] for r in rows)
    failed = [r["member"] for r in rows if not r["pass"]]
    logger.info(f"  {len(rows)} members, {n_cells} cells, max|delta| = {worst:.3e}, "
                f"{len(failed)} failures  [{time.time()-t0:.0f}s]")
    return {"n_members_checked": len(rows), "n_cells_checked": n_cells,
            "max_abs_delta": worst, "tolerance": L.R0_TOL,
            "all_pass": not failed, "failed_members": failed,
            "per_member": {r["member"]: r for r in rows}}


def stage0_powered(keys: list[str], all_detect: list[str]) -> dict:
    tbl, powered = {}, []
    for k in all_detect:
        det = L.load_json(L.EXP / f"results/detect_{k}.json")
        bal = det.get("balance", {})
        nr, nc = int(bal.get("n_refusal", 0)), int(bal.get("n_compliance", 0))
        row = {"n_refusal": nr, "n_compliance": nc,
               "archived_powered": bool(det.get("powered")),
               "min_per_class": min(nr, nc),
               "has_projection_npz": k in keys,
               "archived_auroc_A": det["detection"]["axes"]["A_canned"]["auroc"],
               "archived_verdict_A": det["detection"]["axes"]["A_canned"]["verdict"]}
        row["powered_and_available"] = bool(row["archived_powered"] and row["has_projection_npz"])
        if row["powered_and_available"]:
            powered.append(k)
        tbl[k] = row
    powered.sort(key=lambda k: -tbl[k]["n_refusal"])
    missing = sorted(k for k in all_detect
                     if tbl[k]["archived_powered"] and not tbl[k]["has_projection_npz"])
    logger.info(f"STAGE 0.3: POWERED and available = {len(powered)}; "
                f"powered but no npz = {len(missing)}")
    return {"powered": powered, "n_powered": len(powered),
            "powered_without_projection_npz": missing,
            "n_members_with_detect_json": len(all_detect),
            "n_members_with_projection_npz": len(keys),
            "members_without_projection_npz":
                sorted(set(all_detect) - set(keys)),
            "missing_cause": ("the archived gpu_stage writes proj_<KEY>.npz AFTER the "
                              "detection statistics; six members were scored by an earlier "
                              "pass of the same run (file mtimes 01:27 vs 02:30) and carry "
                              "a detect json but no projection dump.  Their archived "
                              "detection numbers are intact and are reported, but they "
                              "cannot enter a re-analysis that needs the projections."),
            "table": tbl}


# ===========================================================================
# STAGE 1 -- Part-1 sampling frame
# ===========================================================================
def tertile_of(v: np.ndarray) -> np.ndarray:
    """0 / 1 / 2 by the member's own projection tertiles (1 = decision boundary)."""
    q1, q2 = np.percentile(v, [100 / 3, 200 / 3])
    return np.where(v <= q1, 0, np.where(v <= q2, 1, 2))


def sample_member(m: dict, seed: int) -> dict:
    """Stratified draw: regex-label x stratum x projection tertile, middle 2x."""
    projA = L.centre_by_stratum(m["proj"][L.AXIS_A], m["strata"])
    ter = tertile_of(projA)
    labels = m["labels"]
    n = labels.size
    cells: dict[tuple, list[int]] = {}
    for i in range(n):
        cells.setdefault((bool(labels[i]), str(m["strata"][i]), int(ter[i])), []).append(i)

    rng = np.random.default_rng(seed)
    picked: list[int] = []
    alloc: dict[str, dict] = {}
    for cls in (True, False):
        ckeys = [c for c in cells if c[0] == cls]
        if not ckeys:
            continue
        w = np.array([len(cells[c]) * (L.MIDDLE_TERTILE_WEIGHT if c[2] == 1 else 1.0)
                      for c in ckeys], float)
        budget = min(L.PER_REGEX_CLASS, sum(len(cells[c]) for c in ckeys))
        raw = w / w.sum() * budget
        take = np.floor(raw).astype(int)
        take = np.minimum(take, [len(cells[c]) for c in ckeys])
        # largest-remainder top-up, deterministic tie-break on the cell key
        order = sorted(range(len(ckeys)), key=lambda i: (-(raw[i] - np.floor(raw[i])),
                                                        str(ckeys[i])))
        while take.sum() < budget:
            progressed = False
            for i in order:
                if take.sum() >= budget:
                    break
                if take[i] < len(cells[ckeys[i]]):
                    take[i] += 1
                    progressed = True
            if not progressed:
                break
        for i, c in enumerate(ckeys):
            pool = sorted(cells[c])
            sel = list(rng.choice(pool, size=int(take[i]), replace=False)) if take[i] else []
            picked.extend(int(x) for x in sel)
            alloc[str(c)] = {"regex_refusal": c[0], "stratum": c[1], "tertile": c[2],
                             "n_cell": len(pool), "n_sampled": int(take[i])}
    picked = sorted(set(picked))
    w = np.zeros(n)
    for c, a in alloc.items():
        if a["n_sampled"]:
            key = (a["regex_refusal"], a["stratum"], a["tertile"])
            for i in cells[key]:
                w[i] = a["n_cell"] / a["n_sampled"]
    return {"idx": np.array(picked, int), "weights": w[picked], "cells": alloc,
            "projA_centred": projA, "tertile": ter,
            "n_sampled": len(picked),
            "n_regex_refusal": int(labels[picked].sum()),
            "n_regex_nonrefusal": int((~labels[picked]).sum())}


def stage1_frame(powered: list[str]) -> dict:
    logger.info("STAGE 1: Part-1 sampling frame")
    out = {}
    for k in powered:
        m = L.load_member(k)
        s = sample_member(m, L.SAMPLE_SEED + (int(L.sha256_text(k)[:8], 16) % 100000))
        out[k] = {"cells": s["cells"], "n_sampled": s["n_sampled"],
                  "n_regex_refusal": s["n_regex_refusal"],
                  "n_regex_nonrefusal": s["n_regex_nonrefusal"],
                  "idx": s["idx"].tolist(), "weights": s["weights"].tolist(),
                  "n_items_member": int(m["labels"].size),
                  "meets_floor": bool(s["n_sampled"] >= L.FLOOR_PER_MEMBER)}
        logger.info(f"  {k}: {s['n_sampled']} items "
                    f"({s['n_regex_refusal']} regex-refusal / "
                    f"{s['n_regex_nonrefusal']} regex-non-refusal) of {m['labels'].size}")
        del m
        gc.collect()
    L.dump_json(L.RESULTS / "sampling_frame.json", out)
    return out


# ===========================================================================
# STAGE 2 -- five-class semantic labels
# ===========================================================================
def _seed_local_cache(items: list[dict], judge) -> dict:
    """Warm-start from BOTH archived caches, re-keyed onto this client's own
    sha256 convention, so an overlapping item costs $0."""
    import hashlib
    sys.path.insert(0, str(L.ARCH))
    from prereg_spec import EVALUATOR_SYSTEM, JUDGE_MODEL  # noqa: E402

    def content(prompt, completion):
        return f"{JUDGE_MODEL}\x00{EVALUATOR_SYSTEM}\x00{prompt}\x00{completion}"

    sha1_to_256, sha256_set = {}, set()
    for it in items:
        c = content(it["prompt"], it["completion"])
        sha1_to_256[hashlib.sha1(c.encode()).hexdigest()] = \
            hashlib.sha256(c.encode()).hexdigest()
        sha256_set.add(hashlib.sha256(c.encode()).hexdigest())

    srcs = [L.EV4 / "results/judge_cache_5class.jsonl",
            L.EXP / "results/judge_cache.jsonl",
            L.RE3 / "results/judge_cache_a4.jsonl"]
    seeded = 0
    with L.CACHE5.open("a") as fh:
        for src in srcs:
            if not src.exists():
                continue
            for ln in src.read_text().splitlines():
                if not ln.strip():
                    continue
                try:
                    rec = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                k, raw = rec.get("key"), (rec.get("raw") or rec.get("label"))
                if not k or not raw or str(raw).startswith("ERROR:"):
                    continue
                k2 = k if k in sha256_set else sha1_to_256.get(k)
                if k2 is None or k2 in judge.cache:
                    continue
                judge.cache[k2] = raw
                fh.write(json.dumps({"key": k2, "raw": raw, "cost": 0.0,
                                     "seeded_from": src.name}) + "\n")
                seeded += 1
    return {"sources": [str(s.relative_to(L.ROOT)) for s in srcs if s.exists()],
            "n_seeded": seeded, "n_cache_entries": len(judge.cache)}


def stage2_judge(frame: dict, powered: list[str], run_judge: bool) -> dict:
    logger.info("STAGE 2: five-class semantic labels")
    ck = L.RESULTS / "labels5.json"
    sig = L.sha256_text("|".join(powered))
    if ck.exists() and L.load_json(ck).get("signature") == sig:
        doc = L.load_json(ck)
        logger.info(f"  (restored {len(doc['items'])} labelled items from checkpoint)")
        return doc

    pool: list[dict] = []
    for k in powered:
        m = L.load_member(k)
        for i in frame[k]["idx"]:
            it = m["items"][i]
            pool.append({"member": k, "row": int(i), "uid": it["uid"],
                         "stratum": it["stratum"], "prompt": it["prompt"],
                         "completion": it["text"],
                         "regex_refusal": bool(it["regex_refusal"])})
        del m
        gc.collect()
    logger.info(f"  pool: {len(pool)} items over {len(powered)} members")

    if not run_judge:
        return {"signature": sig,
                "items": [dict(it, label5=None, label5_clean=False) for it in pool],
                "stats": {"skipped": True, "n_items": len(pool)}, "cache_seed": {}}

    j5, labels5, rubric5 = L.import_judge5()
    sys.path.insert(0, str(L.ARCH))
    from prereg_spec import JUDGE_MODEL  # noqa: E402

    judge = j5.Judge(JUDGE_MODEL, L.CACHE5, hard_cap_usd=L.HARD_CAP_USD * L.STOP_FRACTION,
                     max_tokens=16, workers=8)
    seed_stats = _seed_local_cache(pool, judge)
    n_cached = sum(1 for it in pool
                   if judge.key_for(it["prompt"], it["completion"]) in judge.cache)
    logger.info(f"  cache: seeded {seed_stats['n_seeded']}, {n_cached}/{len(pool)} "
                f"items already cached; projected ${(len(pool)-n_cached)*3.5e-5:.4f}")

    t0 = time.time()
    scored = judge.score(pool)
    for it, rec in zip(pool, scored):
        it["label5"] = rec["judge_label"]
        it["label5_clean"] = bool(rec["judge_parsed_cleanly"])
        it["judge_raw"] = rec["judge_raw"]
    st = judge.stats()
    st.update({"n_items": len(pool), "n_cache_hits_pre": n_cached,
               "frac_from_cache": n_cached / max(1, len(pool)),
               "seconds": round(time.time() - t0, 1),
               "label_counts": dict(Counter(it.get("label5") for it in pool)),
               "n_unlabelled": sum(1 for it in pool if it.get("label5") is None),
               "rubric_sha256": L.sha256_text(rubric5), "labels": labels5})
    judge.close()
    with L.LEDGER.open("a") as fh:
        fh.write(json.dumps({
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stage": "stage2_five_class", "model": JUDGE_MODEL, "n_items": len(pool),
            "n_calls": st["n_calls"], "n_cache_hits": st["n_cache_hits"],
            "cost_usd": st["cost_usd"], "cumulative_usd": st["cost_usd"],
            "hard_cap_usd": L.HARD_CAP_USD,
            "stop_at_usd": L.HARD_CAP_USD * L.STOP_FRACTION,
            "aborted_on_budget": st["aborted_on_budget"]}) + "\n")
    logger.info(f"  {st['n_calls']} calls, ${st['cost_usd']:.4f}, "
                f"{st['n_errors']} errors, {st['seconds']}s")
    if st["aborted_on_budget"]:
        logger.error("  BUDGET_EXHAUSTED -- degrading to the members completed")
    doc = {"signature": sig, "items": pool, "stats": st, "cache_seed": seed_stats}
    L.dump_json(ck, doc)
    return doc


# ===========================================================================
# STAGE 3 -- Part 1: H-L, semantic vs regex labels
# ===========================================================================
def _ecdf_percentile(x: np.ndarray, ref: np.ndarray) -> np.ndarray:
    """Fraction of `ref` strictly below each x, with ties at 0.5."""
    if ref.size == 0:
        return np.full(x.shape, np.nan)
    lt = (x[:, None] > ref[None, :]).sum(1)
    eq = (x[:, None] == ref[None, :]).sum(1)
    return (lt + 0.5 * eq) / ref.size


def part1_member(key: str, frame_row: dict, lab_rows: list[dict]) -> dict:
    m = L.load_member(key)
    idx = np.array(frame_row["idx"], int)
    w_all = np.array(frame_row["weights"], float)
    projA = L.centre_by_stratum(m["proj"][L.AXIS_A], m["strata"])
    by_row = {r["row"]: r for r in lab_rows}

    rows, keep = [], []
    for j, i in enumerate(idx):
        r = by_row.get(int(i))
        if r is None:
            continue
        keep.append(j)
        rows.append({"row": int(i), "uid": str(m["clusters"][i]),
                     "stratum": str(m["strata"][i]),
                     "regex": bool(m["labels"][i]),
                     "label5": r.get("label5"),
                     "score": float(projA[i]), "w": float(w_all[j]),
                     "text": m["items"][i]["text"], "prompt": m["items"][i]["prompt"]})
    n_sub = len(rows)
    counts = dict(Counter(r["label5"] for r in rows))
    sc = np.array([r["score"] for r in rows])
    rg = np.array([r["regex"] for r in rows], bool)
    lb = np.array([r["label5"] if r["label5"] else "UNLABELLED" for r in rows])
    clus = np.array([r["uid"] for r in rows])
    ww = np.array([r["w"] for r in rows])

    is_ref = np.isin(lb, list(L.REFUSAL_CLASSES))
    is_com = lb == "COMPLIANCE"
    is_can = lb == "REFUSAL_CANONICAL"
    is_non = lb == "REFUSAL_NONCANONICAL"
    is_par = lb == "PARTIAL"
    is_deg = lb == "DEGENERATE"

    ana = is_ref | is_com                       # primary analysable set
    # THE deciding subset: genuine refusals the regex of record calls non-refusals
    missed = is_ref & (~rg)
    missed_non = is_non & (~rg)
    out: dict = {
        "member": key, "n_subset": n_sub, "label5_counts": counts,
        "n_analysable": int(ana.sum()), "n_excluded_degenerate": int(is_deg.sum()),
        "n_excluded_partial": int(is_par.sum()),
        "n_unlabelled": int((lb == "UNLABELLED").sum()),
        "n_refusal_canonical": int(is_can.sum()),
        "n_refusal_noncanonical": int(is_non.sum()),
        "n_compliance": int(is_com.sum()),
        "n_semantic_refusal_regex_missed": int(missed.sum()),
        "n_noncanonical_regex_missed": int(missed_non.sum()),
    }

    def auc(mask_pos, mask_neg, weighted=False):
        mm = mask_pos | mask_neg
        if mask_pos.sum() == 0 or mask_neg.sum() == 0:
            return float("nan")
        if weighted:
            return L.weighted_auroc(sc[mm], mask_pos[mm], ww[mm])
        return L.fast_auroc(sc[mm], mask_pos[mm])

    # --- primary AUROCs -----------------------------------------------------
    out["auroc_semantic"] = auc(is_ref, is_com)
    out["auroc_semantic_weighted"] = auc(is_ref, is_com, True)
    out["auroc_regex_same_items"] = (
        L.fast_auroc(sc[ana], rg[ana]) if ana.sum() and 0 < rg[ana].sum() < ana.sum()
        else float("nan"))
    out["auroc_regex_same_items_weighted"] = (
        L.weighted_auroc(sc[ana], rg[ana], ww[ana])
        if ana.sum() and 0 < rg[ana].sum() < ana.sum() else float("nan"))
    out["auroc_regex_full_subset"] = (
        L.fast_auroc(sc, rg) if 0 < rg.sum() < n_sub else float("nan"))
    out["auroc_regex_full_subset_weighted"] = (
        L.weighted_auroc(sc, rg, ww) if 0 < rg.sum() < n_sub else float("nan"))
    out["auroc_canonical_only"] = auc(is_can, is_com)
    out["auroc_canonical_only_weighted"] = auc(is_can, is_com, True)
    out["auroc_noncanonical_only"] = auc(is_non, is_com)
    out["auroc_noncanonical_only_weighted"] = auc(is_non, is_com, True)
    out["auroc_regex_missed_refusal"] = auc(missed, is_com)
    out["auroc_regex_missed_refusal_weighted"] = auc(missed, is_com, True)

    # Rubric drift on the CANONICAL / NON-CANONICAL boundary.  The rubric's own
    # split is not the regex's split: an item can open with a frozen refusal opener
    # and still be called REFUSAL_NONCANONICAL by the judge.  Reported because it
    # decides how the deciding number must be read.
    reg_ref_and_sem_ref = rg & is_ref
    out["rubric_drift"] = {
        "n_regex_refusal_and_semantic_refusal": int(reg_ref_and_sem_ref.sum()),
        "n_of_those_labelled_NONCANONICAL": int((reg_ref_and_sem_ref & is_non).sum()),
        "frac_of_those_labelled_NONCANONICAL": float(
            (reg_ref_and_sem_ref & is_non).sum() / max(1, reg_ref_and_sem_ref.sum())),
        "kappa_regexopener_vs_rubric_canonical_flag": L.cohens_kappa(
            ["CANON" if x else "NONCANON" for x in rg[is_ref]],
            ["CANON" if x else "NONCANON" for x in is_can[is_ref]]),
        "note": "the regex opener list and the rubric's CANONICAL clause are meant to "
                "pick out the same thing; where they do not, n_REFUSAL_NONCANONICAL "
                "over-counts the refusals the regex actually missed, which is why "
                "n_semantic_refusal_regex_missed is reported beside it",
    }

    # PARTIAL sensitivity
    out["partial_sensitivity"] = {
        "dropped_primary": out["auroc_semantic"],
        "as_refusal": auc(is_ref | is_par, is_com),
        "as_compliance": auc(is_ref, is_com | is_par),
    }

    # --- paired bootstrap over prompt clusters -----------------------------
    boots = L.cluster_boot_indices(clus, L.N_BOOT, L.BOOT_SEED)
    d_boot, s_boot, r_boot, nc_boot, prev_boot = [], [], [], [], []
    ms_boot, mprev_boot = [], []
    prev_num = ww * is_non
    mprev_num = ww * missed
    for bidx in boots:
        a_ = ana[bidx]
        p_, n_ = is_ref[bidx] & a_, is_com[bidx] & a_
        rr = rg[bidx] & a_
        s_v = (L.fast_auroc(sc[bidx][a_], p_[a_]) if p_.sum() >= 3 and n_.sum() >= 3
               else float("nan"))
        nr_, na_ = int(rr[a_].sum()), int(a_.sum())
        r_v = (L.fast_auroc(sc[bidx][a_], rr[a_])
               if min(nr_, na_ - nr_) >= 3 else float("nan"))
        s_boot.append(s_v)
        r_boot.append(r_v)
        d_boot.append(s_v - r_v)
        nn, cc = is_non[bidx], is_com[bidx]
        nc_boot.append(L.fast_auroc(sc[bidx][nn | cc], nn[nn | cc])
                       if nn.sum() >= 3 and cc.sum() >= 3 else float("nan"))
        prev_boot.append(float(prev_num[bidx].sum() / max(ww[bidx].sum(), 1e-12)))
        mm_, cc2 = missed[bidx], is_com[bidx]
        ms_boot.append(L.fast_auroc(sc[bidx][mm_ | cc2], mm_[mm_ | cc2])
                       if mm_.sum() >= 3 and cc2.sum() >= 3 else float("nan"))
        mprev_boot.append(float(mprev_num[bidx].sum() / max(ww[bidx].sum(), 1e-12)))

    out["auroc_semantic_ci95"] = list(L.boot_ci(s_boot))
    out["auroc_regex_same_items_ci95"] = list(L.boot_ci(r_boot))
    out["auroc_noncanonical_ci95"] = list(L.boot_ci(nc_boot))
    out["auroc_regex_missed_refusal_ci95"] = list(L.boot_ci(ms_boot))
    out["delta_L"] = out["auroc_semantic"] - out["auroc_regex_same_items"]
    out["delta_L_ci95"] = list(L.boot_ci(d_boot))
    out["delta_L_p_boot"] = L.boot_p_two_sided(d_boot, 0.0)
    out["n_boot_effective"] = int(np.isfinite(d_boot).sum())

    # --- weighted corpus prevalence of REFUSAL_NONCANONICAL ----------------
    tot_w = ww.sum()
    out["noncanonical_prevalence_weighted"] = float((ww * is_non).sum() / tot_w) if tot_w else float("nan")
    out["noncanonical_prevalence_unweighted"] = float(is_non.mean()) if n_sub else float("nan")
    out["noncanonical_prevalence_ci95"] = list(L.boot_ci(prev_boot))
    out["noncanonical_prevalence_weighted_n_items_est"] = float(
        out["noncanonical_prevalence_weighted"] * m["labels"].size)
    out["regex_missed_refusal_prevalence_weighted"] = (
        float((ww * missed).sum() / tot_w) if tot_w else float("nan"))
    out["regex_missed_refusal_prevalence_unweighted"] = (
        float(missed.mean()) if n_sub else float("nan"))
    out["regex_missed_refusal_prevalence_ci95"] = list(L.boot_ci(mprev_boot))
    out["regex_missed_refusal_prevalence_n_items_est"] = float(
        out["regex_missed_refusal_prevalence_weighted"] * m["labels"].size)

    # --- where the axis places the non-canonical refusals ------------------
    if is_non.sum() and is_com.sum():
        pct = _ecdf_percentile(sc[is_non], sc[is_com])
        out["noncanonical_percentile_in_compliance"] = {
            "mean": float(pct.mean()), "median": float(np.median(pct)),
            "frac_above_median_compliance": float((pct > 0.5).mean()),
            "n": int(is_non.sum())}
        out["noncanonical_percentiles"] = pct.tolist()
    else:
        out["noncanonical_percentile_in_compliance"] = {
            "mean": float("nan"), "median": float("nan"),
            "frac_above_median_compliance": float("nan"), "n": int(is_non.sum())}
        out["noncanonical_percentiles"] = []

    if missed.sum() and is_com.sum():
        pctm = _ecdf_percentile(sc[missed], sc[is_com])
        out["regex_missed_percentile_in_compliance"] = {
            "mean": float(pctm.mean()), "median": float(np.median(pctm)),
            "frac_above_median_compliance": float((pctm > 0.5).mean()),
            "n": int(missed.sum())}
        out["regex_missed_percentiles"] = pctm.tolist()
    else:
        out["regex_missed_percentile_in_compliance"] = {
            "mean": float("nan"), "median": float("nan"),
            "frac_above_median_compliance": float("nan"), "n": int(missed.sum())}
        out["regex_missed_percentiles"] = []

    # --- criterion agreement -----------------------------------------------
    sem_bin = ["REFUSAL" if x else "NOT_REFUSAL" for x in is_ref[ana]]
    reg_bin = ["REFUSAL" if x else "NOT_REFUSAL" for x in rg[ana]]
    out["kappa_regex_vs_semantic"] = L.cohens_kappa(reg_bin, sem_bin)
    out["confusion_2x2"] = {
        "regex_ref_sem_ref": int((rg & is_ref).sum()),
        "regex_ref_sem_notref": int((rg & is_com).sum()),
        "regex_notref_sem_ref": int(((~rg) & is_ref).sum()),
        "regex_notref_sem_notref": int(((~rg) & is_com).sum()),
        "regex_notref_sem_noncanonical": int(((~rg) & is_non).sum()),
        "regex_ref_sem_noncanonical": int((rg & is_non).sum()),
    }
    # random band from the member's OWN archived 20-draw null
    rn = m["detect"]["detection"].get("random_null", {}).get("projection", {})
    out["random_band"] = {"p2p5": rn.get("p2p5"), "p97p5": rn.get("p97p5"),
                          "mean": rn.get("mean"), "max": rn.get("max"),
                          "n_draws": m["detect"]["detection"]
                          .get("random_null", {}).get("n_draws")}
    out["archived_auroc_A_full_pool"] = m["detect"]["detection"]["axes"][L.AXIS_A]["auroc"]

    # boundary examples for the markdown deliverable
    out["examples"] = [
        {"member": key, "uid": r["uid"], "stratum": r["stratum"], "prompt": r["prompt"],
         "text": r["text"], "regex_refusal": r["regex"], "label5": r["label5"],
         "projA_centred": r["score"], "percentile_in_compliance": float(p)}
        for r, p in zip([r for r, f in zip(rows, missed) if f],
                        out["regex_missed_percentiles"])]
    out["per_item"] = [
        {"member": key, "row": r["row"], "uid": r["uid"], "stratum": r["stratum"],
         "regex_refusal": r["regex"], "label5": r["label5"], "weight": r["w"],
         "projA_centred": r["score"], "prompt": r["prompt"], "text": r["text"]}
        for r in rows]
    del m
    gc.collect()
    return out


def stage3_part1(frame: dict, labels: dict, powered: list[str]) -> dict:
    logger.info("STAGE 3: Part 1 -- H-L, semantic vs regex labels")
    by_member: dict[str, list] = {}
    for r in labels["items"]:
        if r.get("label5"):
            by_member.setdefault(r["member"], []).append(r)
    done = [k for k in powered if by_member.get(k)]
    rows = {}
    for k in done:
        rows[k] = part1_member(k, frame[k], by_member[k])
        logger.info(f"  {k}: sem {rows[k]['auroc_semantic']:.3f} vs regex "
                    f"{rows[k]['auroc_regex_same_items']:.3f} "
                    f"(delta {rows[k]['delta_L']:+.3f}), "
                    f"n_noncanon {rows[k]['n_refusal_noncanonical']}, "
                    f"kappa {rows[k]['kappa_regex_vs_semantic']['kappa']:+.3f}")

    lin = L.lineage_map()
    pooled = {}
    for field in ("delta_L", "auroc_semantic", "auroc_regex_same_items",
                  "auroc_canonical_only", "auroc_noncanonical_only",
                  "auroc_regex_missed_refusal",
                  "noncanonical_prevalence_weighted",
                  "regex_missed_refusal_prevalence_weighted"):
        pooled[field] = L.lineage_bootstrap({k: rows[k][field] for k in done}, lin)
    pooled["kappa"] = L.lineage_bootstrap(
        {k: rows[k]["kappa_regex_vs_semantic"]["kappa"] for k in done}, lin)

    # rank-normalised pooled AUROC over all members' items at once: each item is
    # mapped to its percentile within its OWN member's compliance distribution, so
    # projections on different per-member scales become comparable.
    pooled_sc, pooled_pos, pooled_neg, pooled_clus = [], [], [], []
    for k in done:
        r = rows[k]
        comp = np.array([it["projA_centred"] for it in r["per_item"]
                         if it["label5"] == "COMPLIANCE"])
        for it in r["per_item"]:
            if comp.size == 0:
                continue
            p = float(((comp < it["projA_centred"]).sum()
                       + 0.5 * (comp == it["projA_centred"]).sum()) / comp.size)
            pooled_sc.append(p)
            pooled_pos.append(it["label5"] == "REFUSAL_NONCANONICAL")
            pooled_neg.append(it["label5"] == "COMPLIANCE")
            pooled_clus.append(f"{k}::{it['uid']}")
    ps = np.array(pooled_sc)
    pp = np.array(pooled_pos, bool)
    pn = np.array(pooled_neg, bool)
    pc = np.array(pooled_clus)
    mm = pp | pn
    pooled_rank = {"auroc": L.fast_auroc(ps[mm], pp[mm]) if pp.sum() and pn.sum() else float("nan"),
                   "n_noncanonical": int(pp.sum()), "n_compliance": int(pn.sum())}
    if pp.sum() >= 3 and pn.sum() >= 3:
        bb = []
        for bidx in L.cluster_boot_indices(pc[mm], L.N_BOOT, L.BOOT_SEED):
            y = pp[mm][bidx]
            bb.append(L.fast_auroc(ps[mm][bidx], y) if 3 <= y.sum() <= y.size - 3
                      else float("nan"))
        pooled_rank["ci95"] = list(L.boot_ci(bb))
    else:
        pooled_rank["ci95"] = [float("nan"), float("nan")]

    # --- judge-error attenuation -------------------------------------------
    aud = L.load_json(L.AUD / "full_method_out.json")["metadata"]
    conf = aud["results_on_rebuilt_probe"]["arms"][L.AUDIT_ARM][
        "confusion_truth_rows_pred_cols"]
    n_ref_true = sum(conf["REFUSAL"].values())
    n_com_true = sum(conf["COMPLIANCE"].values())
    se_strict = conf["REFUSAL"]["REFUSAL"] / n_ref_true
    sp_strict = 1.0 - conf["COMPLIANCE"]["REFUSAL"] / n_com_true
    se_incl = (conf["REFUSAL"]["REFUSAL"] + conf["REFUSAL"]["PARTIAL"]) / n_ref_true
    sp_incl = 1.0 - (conf["COMPLIANCE"]["REFUSAL"]
                     + conf["COMPLIANCE"]["PARTIAL"]) / n_com_true
    judge_err = {
        "source": "art_gYmQllaTCGT5 / iter_2 gen_art_experiment_3, arm2_repaired "
                  "(meta-llama/llama-3.3-70b-instruct WITH the evaluator system prompt "
                  "-- the exact judge configuration used here), 124 audited items",
        "sensitivity_strict": se_strict, "specificity_strict": sp_strict,
        "sensitivity_partial_as_refusal": se_incl,
        "specificity_partial_as_refusal": sp_incl,
        "per_class_one_vs_rest_kappa_annotatorA_vs_B": L.AUDIT_PER_CLASS_KAPPA,
        "note": "the audited rubric is the FOUR-class one; REFUSAL there subsumes both "
                "five-class refusal classes, so this correction is an approximation "
                "reported ALONGSIDE the raw number, never in place of it",
    }
    for k in done:
        r = rows[k]
        prev = (r["n_refusal_canonical"] + r["n_refusal_noncanonical"]) / max(
            1, r["n_analysable"])
        r["auroc_semantic_attenuation_corrected"] = L.attenuation_correct_auroc(
            r["auroc_semantic"], prev, se_strict, sp_strict)
        r["delta_L_attenuation_corrected"] = (
            r["auroc_semantic_attenuation_corrected"] - r["auroc_regex_same_items"])
    pooled["delta_L_attenuation_corrected"] = L.lineage_bootstrap(
        {k: rows[k]["delta_L_attenuation_corrected"] for k in done}, lin)

    # --- Holm over the per-member paired deltas ----------------------------
    holm_in = {k: rows[k]["delta_L_p_boot"] for k in done}
    holm_out = L.holm(holm_in)

    # --- verdict (mechanical) ----------------------------------------------
    n_non_pooled = sum(rows[k]["n_refusal_noncanonical"] for k in done)
    n_missed_pooled = sum(rows[k]["n_semantic_refusal_regex_missed"] for k in done)
    n_missed_non_pooled = sum(rows[k]["n_noncanonical_regex_missed"] for k in done)
    band_edges = [rows[k]["random_band"]["p97p5"] for k in done
                  if rows[k]["random_band"]["p97p5"] is not None]
    band_up = float(np.mean(band_edges)) if band_edges else 0.5
    band_up_max = float(np.max(band_edges)) if band_edges else 0.5
    nc = pooled["auroc_noncanonical_only"]["member_level"]
    dl = pooled["delta_L"]["member_level"]
    can = pooled["auroc_canonical_only"]["member_level"]

    if n_non_pooled < L.POOLED_NONCANON_MIN_N or len(done) < L.MIN_POWERED_MEMBERS:
        verdict = "UNDERPOWERED"
        reason = (f"pooled n_REFUSAL_NONCANONICAL = {n_non_pooled} "
                  f"(floor {L.POOLED_NONCANON_MIN_N}); "
                  f"{len(done)} POWERED members completed "
                  f"(floor {L.MIN_POWERED_MEMBERS})")
    elif ((dl["ci95"][1] >= 0) and np.isfinite(nc["mean"])
          and nc["mean"] >= L.AUROC_NONCANON_MIN and nc["ci95"][0] > band_up):
        verdict = "SEMANTIC_LABELS_CONFIRM_READING"
        reason = (f"pooled DELTA_L {dl['mean']:+.3f} [{dl['ci95'][0]:+.3f}, "
                  f"{dl['ci95'][1]:+.3f}] is positive or covers 0, and "
                  f"AUROC_noncanonical {nc['mean']:.3f} [{nc['ci95'][0]:.3f}, "
                  f"{nc['ci95'][1]:.3f}] clears both {L.AUROC_NONCANON_MIN} and the "
                  f"members' own random-band upper edge {band_up:.3f}")
    elif (nc["mean"] <= L.AUROC_NONCANON_MIN or nc["ci95"][0] <= band_up) \
            and can["mean"] >= L.AUROC_CANON_MIN:
        verdict = "READS_CANONICAL_WORDING_ONLY"
        reason = (f"AUROC_noncanonical {nc['mean']:.3f} [{nc['ci95'][0]:.3f}, "
                  f"{nc['ci95'][1]:.3f}] fails {L.AUROC_NONCANON_MIN} or covers the "
                  f"random band ({band_up:.3f}) while AUROC_canonical "
                  f"{can['mean']:.3f} stays at or above {L.AUROC_CANON_MIN}")
    else:
        verdict = "INCONCLUSIVE"
        reason = (f"AUROC_noncanonical {nc['mean']:.3f} [{nc['ci95'][0]:.3f}, "
                  f"{nc['ci95'][1]:.3f}] fails the confirm clause while "
                  f"AUROC_canonical {can['mean']:.3f} is below {L.AUROC_CANON_MIN}")

    ncl = pooled["auroc_noncanonical_only"]["lineage_level"]
    dll = pooled["delta_L"]["lineage_level"]
    canl = pooled["auroc_canonical_only"]["lineage_level"]
    if n_non_pooled < L.POOLED_NONCANON_MIN_N or len(done) < L.MIN_POWERED_MEMBERS:
        verdict_lineage = "UNDERPOWERED"
    elif ((dll["ci95"][1] >= 0) and np.isfinite(ncl["mean"])
          and ncl["mean"] >= L.AUROC_NONCANON_MIN and ncl["ci95"][0] > band_up):
        verdict_lineage = "SEMANTIC_LABELS_CONFIRM_READING"
    elif (ncl["mean"] <= L.AUROC_NONCANON_MIN or ncl["ci95"][0] <= band_up) \
            and canl["mean"] >= L.AUROC_CANON_MIN:
        verdict_lineage = "READS_CANONICAL_WORDING_ONLY"
    else:
        verdict_lineage = "INCONCLUSIVE"

    ack = (
        "The detection label and the axis share a lexical basis: axis A is the "
        "diff-in-means of hand-written canned refusals against canned compliances, and "
        "the label of record is an anchored regex over canned-refusal openers, so part "
        "of any AUROC they share is definitional.  Measured on "
        f"{sum(rows[k]['n_analysable'] for k in done)} re-labelled items over "
        f"{len(done)} powered members, the two criteria agree at Cohen's kappa "
        f"{pooled['kappa']['member_level']['mean']:+.3f} "
        f"[{pooled['kappa']['member_level']['ci95'][0]:+.3f}, "
        f"{pooled['kappa']['member_level']['ci95'][1]:+.3f}], and the semantic rubric "
        f"finds {n_non_pooled} REFUSAL_NONCANONICAL items, of which "
        f"{n_missed_non_pooled} are ones the regex calls non-refusals "
        f"({n_missed_pooled} counting both refusal classes; weighted corpus prevalence "
        f"{pooled['regex_missed_refusal_prevalence_weighted']['member_level']['mean']:.4f}).")

    # SECONDARY, sharper verdict on the deciding subset actually described in the
    # hypothesis: refusals the regex of record MISSED.  Reported beside the
    # pre-registered primary, never in place of it.
    ms = pooled["auroc_regex_missed_refusal"]["member_level"]
    if n_missed_pooled < L.POOLED_NONCANON_MIN_N:
        v_missed = "UNDERPOWERED"
        r_missed = (f"pooled n(semantic refusal AND regex non-refusal) = "
                    f"{n_missed_pooled} < {L.POOLED_NONCANON_MIN_N}; the weighted "
                    f"corpus prevalence "
                    f"{pooled['regex_missed_refusal_prevalence_weighted']['member_level']['mean']:.4f} "
                    f"[{pooled['regex_missed_refusal_prevalence_weighted']['member_level']['ci95'][0]:.4f}, "
                    f"{pooled['regex_missed_refusal_prevalence_weighted']['member_level']['ci95'][1]:.4f}] "
                    f"is the reportable claim, per the pre-registered fallback")
    elif (np.isfinite(ms["mean"]) and ms["mean"] >= L.AUROC_NONCANON_MIN
          and ms["ci95"][0] > band_up):
        v_missed = "AXIS_READS_THE_REFUSALS_THE_REGEX_MISSES"
        r_missed = (f"AUROC {ms['mean']:.3f} [{ms['ci95'][0]:.3f}, {ms['ci95'][1]:.3f}] "
                    f"clears {L.AUROC_NONCANON_MIN} and the random band {band_up:.3f}")
    else:
        v_missed = "AXIS_DOES_NOT_READ_THE_REFUSALS_THE_REGEX_MISSES"
        r_missed = (f"AUROC {ms['mean']:.3f} [{ms['ci95'][0]:.3f}, {ms['ci95'][1]:.3f}] "
                    f"fails {L.AUROC_NONCANON_MIN} or covers the random band "
                    f"{band_up:.3f}")

    return {"per_member": rows, "members_completed": done,
            "pooled_n_semantic_refusal_regex_missed": n_missed_pooled,
            "pooled_n_noncanonical_regex_missed": n_missed_non_pooled,
            "verdict_regex_missed_subset": v_missed,
            "verdict_regex_missed_reason": r_missed,
            "n_members_completed": len(done),
            "pooled": pooled, "pooled_rank_normalised_noncanonical": pooled_rank,
            "holm_adjusted_p": holm_out, "raw_p": holm_in,
            "judge_error_model": judge_err,
            "pooled_n_refusal_noncanonical": n_non_pooled,
            "random_band_upper_mean": band_up, "random_band_upper_max": band_up_max,
            "verdict": verdict, "verdict_reason": reason,
            "verdict_member_level": verdict, "verdict_lineage_level": verdict_lineage,
            "acknowledgement_sentence": ack}


# ===========================================================================
# STAGE 4 -- Part 2: H-X, the leakage control
# ===========================================================================
def _part2_one(args) -> dict:
    key, subset = args
    m = L.load_member(key)
    lin_out: dict = {"member": key, "label_sets": {}}

    fits = L.direction_fit_strings()
    fitset = {s.strip() for lst in fits.values() for s in lst}
    texts = [it["text"].strip() for it in m["items"]]
    n_text_overlap = sum(1 for t in texts if t in fitset)
    EX = L.import_explib()
    sp = EX.axis_prompt_splits()
    fitp = set(sp["fit"]) | set(sp["held"])
    prompt_overlap = np.array([it["prompt"].strip() in fitp for it in m["items"]], bool)
    lin_out["leakage"] = {
        "n_text_overlap_recomputed": int(n_text_overlap),
        "n_text_overlap_archived": int(m["detect"]["leakage"]["n_text_overlap_dropped"]),
        "n_prompt_overlap_recomputed": int(prompt_overlap.sum()),
        "n_prompt_overlap_archived": int(m["detect"]["leakage"]["n_prompt_overlap"]),
        "text_overlap_zero": bool(n_text_overlap == 0),
        "n_fit_strings": len(fitset),
    }

    label_sets = {"regex": (np.arange(m["labels"].size), m["labels"])}
    if subset is not None:
        sidx, slab = subset
        if sidx.size >= 10 and 3 <= slab.sum() <= slab.size - 3:
            label_sets["semantic"] = (sidx, slab)

    for lname, (sel, y) in label_sets.items():
        strata = m["strata"][sel]
        clusters = m["clusters"][sel]
        res: dict = {"n_items": int(sel.size), "n_pos": int(y.sum()),
                     "n_neg": int((~y).sum()),
                     "n_prompts": int(len(np.unique(clusters)))}
        scores: dict[tuple, np.ndarray] = {}
        fallbacks: dict[str, int] = {}
        for ax in L.AXES_P2:
            v = m["proj"][ax][sel]
            for proto in L.PROTOCOLS:
                s, nfb = L.protocol_scores(v, strata, clusters, proto)
                scores[(ax, proto)] = s
                fallbacks[f"{ax}|{proto}"] = nfb
        # assert protocol (a) reproduces the archived readout by construction
        if lname == "regex":
            arch_centred = L.centre_by_stratum(m["proj"][L.AXIS_A], m["strata"])
            res["archived_protocol_identical_to_centre_by_stratum"] = bool(
                np.allclose(scores[(L.AXIS_A, "archived")], arch_centred, atol=0,
                            rtol=0))
            res["archived_auroc_matches_detect_json"] = float(abs(
                L.fast_auroc(scores[(L.AXIS_A, "archived")], y)
                - m["detect"]["detection"]["axes"][L.AXIS_A]["auroc"]))

        boots = L.cluster_boot_indices(clusters, L.N_BOOT, L.BOOT_SEED)
        obs = {k: L.fast_auroc(v, y) for k, v in scores.items()}
        bvals: dict[tuple, list] = {k: [] for k in scores}
        for bidx in boots:
            yb = y[bidx]
            if yb.sum() < 5 or (~yb).sum() < 5:
                for k in scores:
                    bvals[k].append(float("nan"))
                continue
            for k, v in scores.items():
                bvals[k].append(L.fast_auroc(v[bidx], yb))
        per_axis = {}
        for ax in L.AXES_P2:
            base = obs[(ax, "archived")]
            entry = {}
            for proto in L.PROTOCOLS:
                lo, hi = L.boot_ci(bvals[(ax, proto)])
                d = [x - z for x, z in zip(bvals[(ax, proto)], bvals[(ax, "archived")])
                     if np.isfinite(x) and np.isfinite(z)]
                dlo, dhi = L.boot_ci(d)
                entry[proto] = {
                    "auroc": obs[(ax, proto)], "auroc_ci95": [lo, hi],
                    "delta_X": obs[(ax, proto)] - base,
                    "delta_X_ci95": [dlo, dhi],
                    "delta_X_p_boot": L.boot_p_two_sided(d, 0.0),
                    "n_fallback_folds": fallbacks[f"{ax}|{proto}"],
                    "n_folds": int(len(np.unique(clusters))),
                }
            per_axis[ax] = entry
        res["axes"] = per_axis

        # prompt-overlap sensitivity on axis A, archived protocol
        po = prompt_overlap[sel]
        if po.any() and (~po).sum() > 10:
            keep = ~po
            yk = y[keep]
            res["prompt_overlap_sensitivity"] = {
                "n_dropped": int(po.sum()),
                "auroc_A_all_items": obs[(L.AXIS_A, "archived")],
                "auroc_A_overlap_dropped": (
                    L.fast_auroc(
                        L.protocol_scores(m["proj"][L.AXIS_A][sel][keep], strata[keep],
                                          clusters[keep], "archived")[0], yk)
                    if 3 <= yk.sum() <= yk.size - 3 else float("nan")),
            }
            res["prompt_overlap_sensitivity"]["delta"] = (
                res["prompt_overlap_sensitivity"]["auroc_A_overlap_dropped"]
                - res["prompt_overlap_sensitivity"]["auroc_A_all_items"])
        else:
            res["prompt_overlap_sensitivity"] = {"n_dropped": int(po.sum()),
                                                 "auroc_A_all_items": obs[(L.AXIS_A, "archived")],
                                                 "auroc_A_overlap_dropped": float("nan"),
                                                 "delta": float("nan")}
        lin_out["label_sets"][lname] = res
    del m
    gc.collect()
    return lin_out


def stage4_part2(powered: list[str], frame: dict, labels: dict) -> dict:
    logger.info(f"STAGE 4: Part 2 -- H-X leakage control over {len(powered)} members")
    by_member: dict[str, dict] = {}
    for r in labels["items"]:
        if r.get("label5"):
            by_member.setdefault(r["member"], {})[int(r["row"])] = r["label5"]

    args = []
    for k in powered:
        sub = None
        if k in by_member:
            rowsel, ylab = [], []
            for row, lab in sorted(by_member[k].items()):
                if lab in L.REFUSAL_CLASSES:
                    rowsel.append(row)
                    ylab.append(True)
                elif lab == "COMPLIANCE":
                    rowsel.append(row)
                    ylab.append(False)
            if rowsel:
                sub = (np.array(rowsel, int), np.array(ylab, bool))
        args.append((k, sub))

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=max(1, N_CPUS - 1)) as ex:
        rows = list(ex.map(_part2_one, args))
    per_member = {r["member"]: r for r in rows}
    logger.info(f"  per-member protocols done [{time.time()-t0:.0f}s]")

    lin = L.lineage_map()
    pooled: dict = {}
    for lname in ("regex", "semantic"):
        pooled[lname] = {}
        for ax in L.AXES_P2:
            pooled[lname][ax] = {}
            for proto in L.PROTOCOLS:
                vals = {k: per_member[k]["label_sets"][lname]["axes"][ax][proto]["delta_X"]
                        for k in powered
                        if lname in per_member[k]["label_sets"]}
                aur = {k: per_member[k]["label_sets"][lname]["axes"][ax][proto]["auroc"]
                       for k in powered if lname in per_member[k]["label_sets"]}
                pooled[lname][ax][proto] = {
                    "delta_X": L.lineage_bootstrap(vals, lin),
                    "auroc": L.lineage_bootstrap(aur, lin)}

    key = pooled["regex"][L.AXIS_A]["fold_centre_scale"]["delta_X"]
    ml, ll = key["member_level"], key["lineage_level"]

    def _verdict(u):
        pt, (lo, hi) = u["mean"], u["ci95"]
        if abs(pt) <= L.X_SMALL_ABS and np.isfinite(hi) and hi < L.X_SMALL_CI_EXCLUDE \
                and lo > -L.X_SMALL_CI_EXCLUDE:
            return "LEAKAGE_CONTROL_SMALL_DELTA"
        if pt <= L.X_LARGE_POINT or (np.isfinite(hi) and hi < L.X_LARGE_CI_EXCLUDE):
            return "LEAKAGE_CONTROL_LARGE_DELTA"
        return "LEAKAGE_CONTROL_INCONCLUSIVE"

    v_m, v_l = _verdict(ml), _verdict(ll)
    reason = (f"pooled DELTA_X for fold-internal centring AND scaling on axis A is "
              f"{ml['mean']:+.4f} [{ml['ci95'][0]:+.4f}, {ml['ci95'][1]:+.4f}] at the "
              f"member level and {ll['mean']:+.4f} [{ll['ci95'][0]:+.4f}, "
              f"{ll['ci95'][1]:+.4f}] at the lineage level, against Mehta's "
              f"{-L.MEHTA_DELTA:+.3f} (0.761 -> 0.425) on their own data")

    # control on the control: does the protocol move the random axis as much?
    ctrl = {}
    for ax in L.AXES_P2:
        u = pooled["regex"][ax]["fold_centre_scale"]["delta_X"]["member_level"]
        ctrl[ax] = {"mean": u["mean"], "ci95": u["ci95"]}
    a_abs = abs(ctrl[L.AXIS_A]["mean"])
    d_abs = abs(ctrl["D_random0"]["mean"])
    ctrl["interpretation"] = (
        "the protocol moves the canonical axis A by "
        f"{a_abs:.4f} and the norm-matched RANDOM axis D by {d_abs:.4f}; "
        + ("the random axis moves at least as much, so the protocol is measuring "
           "normalisation rather than signal and the axis-A delta cannot be read as a "
           "leakage correction"
           if d_abs >= a_abs else
           "the random axis moves less, so the axis-A delta is not merely a "
           "normalisation artefact"))

    leak = {k: per_member[k]["leakage"] for k in powered}
    all_zero = all(v["text_overlap_zero"] for v in leak.values())
    arch_match = all(v["n_prompt_overlap_recomputed"] == v["n_prompt_overlap_archived"]
                     for v in leak.values())
    return {"per_member": per_member, "pooled": pooled,
            "control_on_the_control": ctrl,
            "leakage_assertion": {
                "text_overlap_zero_on_every_member": all_zero,
                "prompt_overlap_recomputation_matches_archive": arch_match,
                "per_member": leak,
                "note": ("prompt overlap is a SEPARATE, non-zero quantity: these are "
                         "items whose PROMPT appears in the axis-E fit/held split.  A "
                         "sensitivity column recomputing axis-A AUROC with those items "
                         "dropped bounds it rather than assuming it harmless.")},
            "verdict": v_m, "verdict_member_level": v_m,
            "verdict_lineage_level": v_l, "verdict_reason": reason,
            "mehta_reference_delta": -L.MEHTA_DELTA}


# ===========================================================================
# STAGE 5 -- assembly
# ===========================================================================
def ledger_total() -> float:
    """Total OpenRouter spend across EVERY run of this artifact, from the ledger.

    The judge client counts a cache hit without a call, so `n_calls` IS the billed
    count; a rerun bills nothing, which is why the ledger rather than the current
    run is the honest cumulative figure."""
    if not L.LEDGER.exists():
        return 0.0
    tot = 0.0
    for ln in L.LEDGER.read_text().splitlines():
        if ln.strip():
            try:
                tot += float(json.loads(ln).get("cost_usd") or 0.0)
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return round(tot, 6)


def paper_numbers(p1: dict, p2: dict, gate: dict, pw: dict, lab: dict) -> dict:
    dm = p1["pooled"]["delta_L"]["member_level"]
    dl = p1["pooled"]["delta_L"]["lineage_level"]
    nc = p1["pooled"]["auroc_noncanonical_only"]["member_level"]
    ca = p1["pooled"]["auroc_canonical_only"]["member_level"]
    se = p1["pooled"]["auroc_semantic"]["member_level"]
    rg = p1["pooled"]["auroc_regex_same_items"]["member_level"]
    kp = p1["pooled"]["kappa"]["member_level"]
    pv = p1["pooled"]["noncanonical_prevalence_weighted"]["member_level"]
    ms = p1["pooled"]["auroc_regex_missed_refusal"]["member_level"]
    mp = p1["pooled"]["regex_missed_refusal_prevalence_weighted"]["member_level"]
    x = p2["pooled"]["regex"][L.AXIS_A]["fold_centre_scale"]["delta_X"]
    xb = p2["pooled"]["regex"][L.AXIS_A]["fold_centre"]["delta_X"]
    xl = p2["pooled"]["regex"][L.AXIS_A]["leaky_z"]["delta_X"]
    xd = p2["pooled"]["regex"]["D_random0"]["fold_centre_scale"]["delta_X"]
    xB = p2["pooled"]["regex"][L.AXIS_B]["fold_centre_scale"]["delta_X"]
    return {
        "n_members_with_detect_json": pw["n_members_with_detect_json"],
        "n_members_with_projection_npz": pw["n_members_with_projection_npz"],
        "n_powered": pw["n_powered"],
        "n_powered_without_npz": len(pw["powered_without_projection_npz"]),
        "r0_n_cells": gate["n_cells_checked"], "r0_max_abs_delta": gate["max_abs_delta"],
        "r0_all_pass": gate["all_pass"],
        "n_members_completed_part1": p1["n_members_completed"],
        "n_items_judged": lab["stats"].get("n_items", 0),
        "judge_cost_usd": lab["stats"].get("cost_usd", 0.0),
        "judge_cache_hits": lab["stats"].get("n_cache_hits", 0),
        "judge_billed_calls": lab["stats"].get("n_calls", 0),
        "judge_cost_usd_cumulative_all_runs": ledger_total(),
        "auroc_semantic_pooled": se["mean"], "auroc_semantic_ci_lo": se["ci95"][0],
        "auroc_semantic_ci_hi": se["ci95"][1],
        "auroc_regex_pooled": rg["mean"], "auroc_regex_ci_lo": rg["ci95"][0],
        "auroc_regex_ci_hi": rg["ci95"][1],
        "delta_L_member": dm["mean"], "delta_L_member_lo": dm["ci95"][0],
        "delta_L_member_hi": dm["ci95"][1],
        "delta_L_lineage": dl["mean"], "delta_L_lineage_lo": dl["ci95"][0],
        "delta_L_lineage_hi": dl["ci95"][1],
        "auroc_canonical": ca["mean"], "auroc_canonical_lo": ca["ci95"][0],
        "auroc_canonical_hi": ca["ci95"][1],
        "auroc_noncanonical": nc["mean"], "auroc_noncanonical_lo": nc["ci95"][0],
        "auroc_noncanonical_hi": nc["ci95"][1],
        "auroc_noncanonical_rank_pooled": p1["pooled_rank_normalised_noncanonical"]["auroc"],
        "auroc_noncanonical_rank_lo":
            p1["pooled_rank_normalised_noncanonical"]["ci95"][0],
        "auroc_noncanonical_rank_hi":
            p1["pooled_rank_normalised_noncanonical"]["ci95"][1],
        "n_noncanonical_pooled": p1["pooled_n_refusal_noncanonical"],
        "n_regex_missed_refusal_pooled": p1["pooled_n_semantic_refusal_regex_missed"],
        "n_regex_missed_noncanonical_pooled": p1["pooled_n_noncanonical_regex_missed"],
        "auroc_regex_missed": ms["mean"], "auroc_regex_missed_lo": ms["ci95"][0],
        "auroc_regex_missed_hi": ms["ci95"][1],
        "regex_missed_prevalence": mp["mean"],
        "regex_missed_prevalence_lo": mp["ci95"][0],
        "regex_missed_prevalence_hi": mp["ci95"][1],
        "noncanonical_prevalence": pv["mean"], "noncanonical_prevalence_lo": pv["ci95"][0],
        "noncanonical_prevalence_hi": pv["ci95"][1],
        "kappa_pooled": kp["mean"], "kappa_lo": kp["ci95"][0], "kappa_hi": kp["ci95"][1],
        "random_band_upper_mean": p1["random_band_upper_mean"],
        "random_band_upper_max": p1["random_band_upper_max"],
        "delta_X_A_fold_centre_scale": x["member_level"]["mean"],
        "delta_X_A_fold_centre_scale_lo": x["member_level"]["ci95"][0],
        "delta_X_A_fold_centre_scale_hi": x["member_level"]["ci95"][1],
        "delta_X_A_fold_centre_scale_lineage": x["lineage_level"]["mean"],
        "delta_X_A_fold_centre": xb["member_level"]["mean"],
        "delta_X_A_leaky_z": xl["member_level"]["mean"],
        "delta_X_B_fold_centre_scale": xB["member_level"]["mean"],
        "delta_X_D_fold_centre_scale": xd["member_level"]["mean"],
        "delta_X_D_fold_centre_scale_lo": xd["member_level"]["ci95"][0],
        "delta_X_D_fold_centre_scale_hi": xd["member_level"]["ci95"][1],
        "mehta_delta": -L.MEHTA_DELTA,
        "part1_verdict_regex_missed_subset": p1["verdict_regex_missed_subset"],
        "part1_verdict_member": p1["verdict_member_level"],
        "part1_verdict_lineage": p1["verdict_lineage_level"],
        "part2_verdict_member": p2["verdict_member_level"],
        "part2_verdict_lineage": p2["verdict_lineage_level"],
    }


def write_paragraph(pn: dict, p1: dict, p2: dict) -> str:
    """The section-5.1 replacement, generated purely by f-string substitution."""
    t = (
        f"**5.1 What the refusal axis reads, and what the normalisation buys it.** "
        f"The detection result of iteration 4 is a re-analysis of {pn['n_members_with_detect_json']} "
        f"scored checkpoints, of which {pn['n_powered']} are both detection-powered "
        f"(>= {L.MIN_PER_CLASS} spontaneous items per class) and carry the stored "
        f"projections this analysis needs; every archived per-member AUROC, its "
        f"prompt-clustered CI and the paired A-B difference regenerate from those "
        f"stores to {pn['r0_max_abs_delta']:.1e} across {pn['r0_n_cells']} cells before "
        f"any number below is computed. {p1['acknowledgement_sentence']} "
        f"Re-labelling {pn['n_items_judged']} stratified items with the five-class "
        f"semantic rubric (${pn['judge_cost_usd_cumulative_all_runs']:.4f} of a "
        f"${L.HARD_CAP_USD:.2f} cap, cumulative over every run of this artifact; the "
        f"cache makes a rerun free) moves the axis-A AUROC from {pn['auroc_regex_pooled']:.3f} "
        f"[{pn['auroc_regex_ci_lo']:.3f}, {pn['auroc_regex_ci_hi']:.3f}] under the regex "
        f"label to {pn['auroc_semantic_pooled']:.3f} [{pn['auroc_semantic_ci_lo']:.3f}, "
        f"{pn['auroc_semantic_ci_hi']:.3f}] under the semantic one, a paired difference "
        f"of {pn['delta_L_member']:+.3f} [{pn['delta_L_member_lo']:+.3f}, "
        f"{pn['delta_L_member_hi']:+.3f}] at the member level and "
        f"{pn['delta_L_lineage']:+.3f} [{pn['delta_L_lineage_lo']:+.3f}, "
        f"{pn['delta_L_lineage_hi']:+.3f}] at the lineage level. The deciding split is "
        f"the {pn['n_noncanonical_pooled']} genuine refusals the regex misses "
        f"(REFUSAL_NONCANONICAL; weighted corpus prevalence "
        f"{pn['noncanonical_prevalence']:.3f} [{pn['noncanonical_prevalence_lo']:.3f}, "
        f"{pn['noncanonical_prevalence_hi']:.3f}]): the axis separates them from "
        f"compliances at AUROC {pn['auroc_noncanonical']:.3f} "
        f"[{pn['auroc_noncanonical_lo']:.3f}, {pn['auroc_noncanonical_hi']:.3f}], against "
        f"{pn['auroc_canonical']:.3f} [{pn['auroc_canonical_lo']:.3f}, "
        f"{pn['auroc_canonical_hi']:.3f}] on canonically-worded ones and a measured "
        f"20-draw random reading band whose upper edge averages "
        f"{pn['random_band_upper_mean']:.3f} (chance is NOT 0.500 here). The rubric's own "
        f"CANONICAL/NON-CANONICAL split is not the regex's split, so the sharper subset "
        f"is the {pn['n_regex_missed_refusal_pooled']} items the regex actually calls "
        f"non-refusals while the rubric calls them refusals "
        f"({pn['n_regex_missed_noncanonical_pooled']} of them REFUSAL_NONCANONICAL; "
        f"weighted corpus prevalence {pn['regex_missed_prevalence']:.4f} "
        f"[{pn['regex_missed_prevalence_lo']:.4f}, {pn['regex_missed_prevalence_hi']:.4f}]): "
        f"on those the axis reaches AUROC {pn['auroc_regex_missed']:.3f} "
        f"[{pn['auroc_regex_missed_lo']:.3f}, {pn['auroc_regex_missed_hi']:.3f}] "
        f"({pn['part1_verdict_regex_missed_subset']}). The "
        f"pre-registered verdict is {pn['part1_verdict_member']} at the member level and "
        f"{pn['part1_verdict_lineage']} at the lineage level. "
        f"Applying the one published leakage control (arXiv:2607.13346) to our own "
        f"headline -- re-estimating every centring and scaling statistic inside the "
        f"training fold under leave-one-prompt-out, rather than on the whole scored pool "
        f"as the archived readout does -- moves axis-A AUROC by "
        f"{pn['delta_X_A_fold_centre_scale']:+.4f} "
        f"[{pn['delta_X_A_fold_centre_scale_lo']:+.4f}, "
        f"{pn['delta_X_A_fold_centre_scale_hi']:+.4f}] (centring alone: "
        f"{pn['delta_X_A_fold_centre']:+.4f}; the deliberately leaky whole-pool z-score: "
        f"{pn['delta_X_A_leaky_z']:+.4f}), against the {pn['mehta_delta']:+.3f} that "
        f"control produced on its author's own data. The same protocol moves the "
        f"norm-matched random axis D by {pn['delta_X_D_fold_centre_scale']:+.4f} "
        f"[{pn['delta_X_D_fold_centre_scale_lo']:+.4f}, "
        f"{pn['delta_X_D_fold_centre_scale_hi']:+.4f}] and axis B by "
        f"{pn['delta_X_B_fold_centre_scale']:+.4f}, which is the control on the control. "
        f"Verdict {pn['part2_verdict_member']} (member level) / "
        f"{pn['part2_verdict_lineage']} (lineage level). "
        f"Text overlap between the scored items and the axis-fit strings is "
        f"{'zero on every member' if p2['leakage_assertion']['text_overlap_zero_on_every_member'] else 'NON-ZERO -- see the table'}"
        f", re-asserted here rather than inherited."
    )
    (L.HERE / "results/section_5_1_paragraph.md").write_text(t + "\n")
    return t


def write_examples(p1: dict) -> int:
    ex = []
    for k in p1["members_completed"]:
        ex.extend(p1["per_member"][k]["examples"])
    ex.sort(key=lambda e: (-e["percentile_in_compliance"], e["member"]))
    take = ex[:10] + ex[-10:] if len(ex) > 20 else ex
    seen, out = set(), []
    for e in take:
        sig = (e["member"], e["uid"], e["text"][:80])
        if sig in seen:
            continue
        seen.add(sig)
        out.append(e)
    lines = ["# Boundary examples: refusals the regex of record misses",
             "",
             "Genuine refusals (five-class semantic rubric, REFUSAL_CANONICAL or "
             "REFUSAL_NONCANONICAL) that the anchored "
             "`REFUSAL_RE` of record calls NON-refusals.  Verbatim generated text, "
             "unedited.  `percentile_in_compliance` is the fraction of that member's "
             "COMPLIANCE items the axis-A projection places BELOW this item, so 0.50 is "
             "the median compliance item and 1.00 is above all of them.",
             ""]
    for i, e in enumerate(out, 1):
        lines += [f"## {i}. {e['member']} — {e['label5']}", "",
                  f"- stratum: `{e['stratum']}` | prompt uid: `{e['uid']}`",
                  f"- regex verdict: `{'REFUSAL' if e['regex_refusal'] else 'NON-REFUSAL'}`"
                  f" | semantic label: `{e['label5']}`",
                  f"- stratum-centred axis-A projection: `{e['projA_centred']:+.4f}`"
                  f" | percentile in the compliance distribution: "
                  f"`{e['percentile_in_compliance']:.3f}`", "",
                  "**Prompt**", "", "```", e["prompt"], "```", "",
                  "**Generated text**", "", "```", e["text"], "```", ""]
    (L.RESULTS / "noncanonical_examples.md").write_text("\n".join(lines) + "\n")
    return len(out)


def build_eval_out(inputs, prereg_sha, gate, pw, frame, lab, p1, p2, pn) -> dict:
    # per-example rows: every judged item, with both criteria and the axis score
    examples = []
    for k in p1["members_completed"]:
        for it in p1["per_member"][k]["per_item"]:
            lab5 = it["label5"] or "UNLABELLED"
            examples.append({
                "input": it["prompt"],
                "output": it["text"],
                "metadata_fold": k,
                "metadata_uid": it["uid"],
                "metadata_stratum": it["stratum"],
                "metadata_row": it["row"],
                "metadata_ipw_weight": it["weight"],
                "metadata_projA_centred": it["projA_centred"],
                "predict_regex_of_record": "REFUSAL" if it["regex_refusal"] else "NON_REFUSAL",
                "predict_semantic_five_class": lab5,
                "predict_semantic_any_refusal":
                    "REFUSAL" if lab5 in L.REFUSAL_CLASSES else "NON_REFUSAL",
                "eval_regex_refusal": float(it["regex_refusal"]),
                "eval_semantic_any_refusal": float(lab5 in L.REFUSAL_CLASSES),
                "eval_semantic_noncanonical": float(lab5 == "REFUSAL_NONCANONICAL"),
                "eval_semantic_canonical": float(lab5 == "REFUSAL_CANONICAL"),
                "eval_semantic_partial": float(lab5 == "PARTIAL"),
                "eval_semantic_degenerate": float(lab5 == "DEGENERATE"),
                "eval_criteria_disagree": float(
                    it["regex_refusal"] != (lab5 in L.REFUSAL_CLASSES)),
                "eval_projA_centred": it["projA_centred"],
            })
    # strip the bulky per-item / percentile arrays out of the reported tables
    per_member_1 = {}
    for k, v in p1["per_member"].items():
        per_member_1[k] = {kk: vv for kk, vv in v.items()
                           if kk not in ("per_item", "examples",
                                         "noncanonical_percentiles",
                                         "regex_missed_percentiles")}
    metrics_agg = {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) and
                        not isinstance(vv, bool) else float(bool(vv)))
                   for kk, vv in pn.items() if not isinstance(vv, str)}
    metrics_agg = {kk: vv for kk, vv in metrics_agg.items() if np.isfinite(vv)}

    doc = {
        "metadata": {
            "evaluation_name": "H-L semantic relabel + H-X leave-one-prompt-out leakage "
                               "control on the frozen iter-4 read-vs-act tree",
            "description": (
                "Pure re-analysis of art_1xT3w1joqeJ8: no weights loaded, no generation, "
                "no steering, no training.  Part 1 re-labels a stratified subset of the "
                "SAME stored spontaneous generations with the five-class semantic rubric "
                "(which carries an explicit REFUSAL_NONCANONICAL class) and re-reports "
                "axis A's AUROC against semantic labels, paired against the regex AUROC "
                "on the identical items.  Part 2 re-runs the published per-fold "
                "residualisation control (arXiv:2607.13346) on our detection headline "
                "under four normalisation protocols, on axes A, B and the norm-matched "
                "random axis D."),
            "verdict_part1": p1["verdict"], "verdict_part1_reason": p1["verdict_reason"],
            "verdict_part2": p2["verdict"], "verdict_part2_reason": p2["verdict_reason"],
            "aggregation_units": {
                "part1_member_level": p1["verdict_member_level"],
                "part1_lineage_level": p1["verdict_lineage_level"],
                "part2_member_level": p2["verdict_member_level"],
                "part2_lineage_level": p2["verdict_lineage_level"],
                "note": "H-U: every pooled quantity is reported at BOTH units with both "
                        "verdict strings; the bootstrap resampling unit is the lineage in "
                        "both cases and the units differ only in whether members are "
                        "averaged within lineage first."},
            "acknowledgement": p1["acknowledgement_sentence"],
            "input_sha256": inputs, "prereg_sha256": prereg_sha,
            "reproduction": gate, "powered_set": pw,
            "sampling": {"seed": L.SAMPLE_SEED,
                         "target_per_member": L.TARGET_PER_MEMBER,
                         "per_regex_class": L.PER_REGEX_CLASS,
                         "middle_tertile_weight": L.MIDDLE_TERTILE_WEIGHT,
                         "achieved_coverage": {k: frame[k]["n_sampled"] for k in frame},
                         "n_members_targeted": len(frame),
                         "n_members_completed": p1["n_members_completed"],
                         "caveat": "the frame deliberately over-samples the decision "
                                   "boundary (middle projection tertile at 2x), so raw "
                                   "per-arm accuracy on this subset is NOT a corpus "
                                   "estimate; every corpus-level quantity is "
                                   "inverse-probability-weighted back to the member's "
                                   "item population and both weighted and unweighted "
                                   "numbers are reported",
                         "per_member_cells": {k: frame[k]["cells"] for k in frame}},
            "judge": {k: v for k, v in lab["stats"].items() if k != "labels"},
            "cost_ledger_summary": {
                "hard_cap_usd": L.HARD_CAP_USD,
                "stop_at_usd": L.HARD_CAP_USD * L.STOP_FRACTION,
                "spent_usd": lab["stats"].get("cost_usd", 0.0),
                "n_billed_calls": lab["stats"].get("n_calls", 0),
                "n_errors": lab["stats"].get("n_errors", 0),
                "cumulative_usd_all_runs_from_ledger": ledger_total(),
                "n_cache_hits": lab["stats"].get("n_cache_hits", 0),
                "cache_seed": lab.get("cache_seed", {})},
            "deviations": [
                "6 of the 30 archived members carry a detect_<KEY>.json but no "
                "proj_<KEY>.npz (the archived gpu_stage writes the projections AFTER the "
                "detection statistics and those six were scored by an earlier pass of the "
                "same run).  3 of them are POWERED.  Pre-registered fallback applied: the "
                "re-analysis is restricted to the 24 members with projections, and the "
                "missing ones are listed with their archived numbers.",
                "PARTIAL is excluded from the primary semantic AUROC alongside "
                "DEGENERATE, because the primary contrast is semantic_any_refusal vs "
                "COMPLIANCE; all three PARTIAL treatments are reported as a sensitivity "
                "column.",
                "DELTA_L is defined on the identical ITEM SET (the analysable items), so "
                "it isolates the label change; the regex AUROC over the full subset is "
                "reported separately.",
                "The judge-error attenuation correction uses the FOUR-class audited "
                "confusion of the same judge configuration (art_gYmQllaTCGT5, "
                "arm2_repaired); the audit predates the five-class rubric, so the "
                "correction is an approximation reported alongside the raw number.",
            ],
            "part1": {"per_member": per_member_1, "pooled": p1["pooled"],
                      "pooled_rank_normalised_noncanonical":
                          p1["pooled_rank_normalised_noncanonical"],
                      "holm_adjusted_p": p1["holm_adjusted_p"], "raw_p": p1["raw_p"],
                      "judge_error_model": p1["judge_error_model"],
                      "pooled_n_refusal_noncanonical": p1["pooled_n_refusal_noncanonical"],
                      "pooled_n_semantic_refusal_regex_missed":
                          p1["pooled_n_semantic_refusal_regex_missed"],
                      "pooled_n_noncanonical_regex_missed":
                          p1["pooled_n_noncanonical_regex_missed"],
                      "verdict_regex_missed_subset": p1["verdict_regex_missed_subset"],
                      "verdict_regex_missed_reason": p1["verdict_regex_missed_reason"],
                      "random_band_upper_mean": p1["random_band_upper_mean"],
                      "verdict": p1["verdict"], "verdict_reason": p1["verdict_reason"]},
            "part2": {"per_member": p2["per_member"], "pooled": p2["pooled"],
                      "control_on_the_control": p2["control_on_the_control"],
                      "leakage_assertion": p2["leakage_assertion"],
                      "mehta_reference_delta": p2["mehta_reference_delta"],
                      "verdict": p2["verdict"], "verdict_reason": p2["verdict_reason"]},
            "paper_numbers": pn,
            "section_5_1_paragraph": (L.RESULTS / "section_5_1_paragraph.md").read_text(),
        },
        "metrics_agg": metrics_agg,
        "datasets": [{"dataset": "iter4_experiment2_spontaneous_generations",
                      "examples": examples}],
    }
    return doc


# ===========================================================================
@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--members", type=int, default=0,
                    help="cap the number of members (smoke tests only)")
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--boot", type=int, default=0, help="override N_BOOT (smoke tests)")
    args = ap.parse_args()
    if args.boot:
        L.N_BOOT = args.boot
        logger.warning(f"N_BOOT overridden to {L.N_BOOT} (SMOKE TEST, not the artifact)")

    t0 = time.time()
    keys = L.member_keys()
    all_detect = L.detect_keys()
    logger.info(f"members with projections: {len(keys)}; with detect json: {len(all_detect)}")

    pw = stage0_powered(keys, all_detect)
    powered = pw["powered"]
    if args.members:
        # smoke tests restrict to the first N POWERED members (and the gate with them)
        powered = powered[:args.members]
        keys = sorted(set(keys) & set(powered))
    if not powered:
        raise RuntimeError("no POWERED member has stored projections")

    inputs = stage0_provenance(keys)
    pre = write_prereg(inputs)
    gate = stage0_gate(keys)
    if not gate["all_pass"]:
        L.dump_json(L.RESULTS / "REPRODUCTION_FAILED.json", gate)
        logger.error(f"REPRODUCTION_FAILED on {gate['failed_members']} -- stopping "
                     "before any restatement")
        raise SystemExit(2)

    frame = stage1_frame(powered)
    lab = stage2_judge(frame, powered, run_judge=not args.no_judge)
    p1 = stage3_part1(frame, lab, powered)
    p2 = stage4_part2(powered, frame, lab)

    pn = paper_numbers(p1, p2, gate, pw, lab)
    para = write_paragraph(pn, p1, p2)
    n_ex = write_examples(p1)
    logger.info(f"  wrote {n_ex} boundary examples")

    doc = build_eval_out(inputs, pre["prereg_sha256"], gate, pw, frame, lab, p1, p2, pn)
    L.dump_json(L.HERE / "eval_out.json", doc)
    logger.info(f"eval_out.json: {len(doc['datasets'][0]['examples'])} examples, "
                f"{len(doc['metrics_agg'])} aggregate metrics")
    logger.info(f"PART 1 VERDICT: {p1['verdict']}")
    logger.info(f"PART 2 VERDICT: {p2['verdict']}")
    logger.info(f"total {time.time()-t0:.0f}s")
    print("\n" + para + "\n")


if __name__ == "__main__":
    main()
