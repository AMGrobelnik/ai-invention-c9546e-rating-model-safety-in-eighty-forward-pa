#!/usr/bin/env python3
"""STAGE 1 -- THE REPRODUCTION GATE (G1..G7).

Nothing is restated until the shipped numbers reproduce from their own inputs.
G1 is the stop-the-line leg: if the pooled rho = 0.629 and its CI do not come
back, the restatement is abandoned and a diagnostic-only output is shipped.
"""

from __future__ import annotations

import numpy as np
from loguru import logger

from common5 import (ARMS, AXES, EX, OUT, R4, R4_RESULTS, TOL, gate_leg, jdump,
                     jload, setup_logging)


# --------------------------------------------------------------------------
def load_panel() -> dict:
    md = jload(R4 / "method_out.json")["metadata"]
    res = md["results"]
    return {
        "meta": md,
        "points": res["joint_scatter_points"],
        "h3": res["h3_joint_scatter"],
        "per_member": res["h1_abliterated_arm"]["per_member"],
        "by_arm": res["h1_abliterated_arm"]["by_arm"],
        "h1b": res["h1b_induction_paired"],
        "headline": res["headline"],
        "short_version_line": None,
    }


# --------------------------------------------------------------------------
def g1_pooled(points: list[dict], h3: dict) -> list[dict]:
    """rho over the 70 (member, axis) pairs, and its lineage bootstrap CI,
    recomputed with the IMPORTED estimator at the archived reps/seed."""
    y = np.array([p["detection_auroc"] for p in points], float)
    x = np.array([p["max_refusal_rate"] for p in points], float)
    lin = np.array([p["lineage_id"] for p in points])
    rho = EX.spearman(x, y)
    boots = [EX.spearman(x[i], y[i])
             for i in EX.cluster_boot_indices(lin, EX.N_BOOT, EX.BOOT_SEED)]
    lo, hi = EX.boot_ci(boots)
    legs = [
        gate_leg("G1a pooled Spearman rho over 70 (member, axis) pairs",
                 h3["rho_primary"], rho,
                 note="recomputed with explib.spearman from "
                      "method_out.json's own joint_scatter_points"),
        gate_leg("G1b lineage-bootstrap CI lower bound",
                 h3["ci95_lineage_bootstrap"][0], lo,
                 note=f"explib.cluster_boot_indices, N_BOOT={EX.N_BOOT}, "
                      f"seed={EX.BOOT_SEED}; archived draws are regenerated from "
                      f"the seed, so this is exact rather than Monte-Carlo"),
        gate_leg("G1c lineage-bootstrap CI upper bound",
                 h3["ci95_lineage_bootstrap"][1], hi),
        gate_leg("G1d n_pairs", h3["n_pairs"], len(points), tol=0),
        gate_leg("G1e n_members", h3["n_members"],
                 len({p["checkpoint"] for p in points}), tol=0),
        gate_leg("G1f n_lineages", h3["n_lineages"], len(set(lin.tolist())), tol=0),
    ]
    return legs


def g2_secondary(points: list[dict], h3: dict) -> list[dict]:
    unc = [p for p in points if p.get("neg_log10_c50") is not None]
    rho_sec = EX.spearman([p["neg_log10_c50"] for p in unc],
                          [p["detection_auroc"] for p in unc])
    cens = 1.0 - len(unc) / len(points)
    return [
        gate_leg("G2a secondary rho (x = -log10 c_50, uncensored pairs only)",
                 h3["rho_secondary_neg_log10_c50"], rho_sec,
                 note="reproduces the ARCHIVED convention, which DROPS censored "
                      "pairs; this artifact's own secondary uses the rank_bottom "
                      "sentinel instead and is reported separately"),
        gate_leg("G2b c_50 censoring fraction", h3["censored_fraction"], cens),
        gate_leg("G2c n uncensored c_50 pairs", h3["n_uncensored_c50"], len(unc),
                 tol=0),
    ]


def g3_within_member(points: list[dict], h3: dict) -> list[dict]:
    within = []
    for ck in sorted({p["checkpoint"] for p in points}):
        sub = [p for p in points if p["checkpoint"] == ck]
        if len(sub) >= 4:
            within.append(EX.spearman([p["max_refusal_rate"] for p in sub],
                                      [p["detection_auroc"] for p in sub]))
    wr = [w for w in within if np.isfinite(w)]
    mean = float(np.mean(wr))
    legs = [gate_leg("G3a within-member mean rho over 14 five-point coefficients",
                     h3["within_member_mean_rho"], mean),
            gate_leg("G3b number of within-member coefficients",
                     len(h3["within_member"]), len(wr), tol=0)]
    for arc, obt in zip(h3["within_member"], within):
        legs.append(gate_leg(f"G3c within-member rho {arc['checkpoint']}",
                             arc["rho"], obt))
    return legs


def g4_per_member_auroc(per_member: list[dict]) -> tuple[list[dict], dict]:
    """Re-run the IMPORTED detection_stats on the stored per-item projections."""
    legs, level_by_member, missing = [], {}, []
    for m in per_member:
        ck = m["checkpoint"]
        npz = R4_RESULTS / f"proj_{ck}.npz"
        det = R4_RESULTS / f"detect_{ck}.json"
        if npz.exists():
            z = np.load(npz, allow_pickle=True)
            proj = {ax: z[f"proj_{ax}"] for ax in AXES if f"proj_{ax}" in z.files}
            out = EX.detection_stats(proj, z["labels"], z["strata"], z["clusters"],
                                     n_boot=EX.N_BOOT, seed=EX.BOOT_SEED)
            a = out["axes"]["A_canned"]
            level = "item-level"
        else:
            missing.append(str(npz))
            d = jload(det)
            a = d["detection"]["axes"]["A_canned"]
            level = "summary-level"
        level_by_member[ck] = level
        legs.append(gate_leg(f"G4 A AUROC {ck}", m["A_auroc"], a["auroc"],
                             level=level))
        for j, nm in enumerate(("lo", "hi")):
            tgt, got = m["A_ci95"][j], a["auroc_ci95"][j]
            if tgt is None and (got is None or not np.isfinite(got)):
                legs.append({"leg": f"G4 A CI {nm} {ck}", "target": None,
                             "obtained": None, "delta": 0.0, "tolerance": TOL,
                             "status": "PASS", "level": level,
                             "note": "both non-finite (UNDEFINED member)"})
            else:
                legs.append(gate_leg(f"G4 A CI {nm} {ck}", tgt, got, level=level))
        legs.append({"leg": f"G4 A verdict {ck}", "target": m["A_verdict"],
                     "obtained": a["verdict"], "delta": None, "tolerance": None,
                     "status": "PASS" if a["verdict"] == m["A_verdict"] else "FAIL",
                     "level": level, "note": ""})
    return legs, {"levels": level_by_member, "missing_npz": missing,
                  "n_item_level": sum(v == "item-level"
                                      for v in level_by_member.values()),
                  "n_summary_level": sum(v == "summary-level"
                                         for v in level_by_member.values())}


def g5_arm_table(per_member: list[dict], by_arm: dict) -> tuple[list[dict], dict]:
    rebuilt = {}
    for arm in ARMS:
        ms = [m for m in per_member if m["arm"] == arm]
        rates = sorted(m["spontaneous_refusal_rate"] for m in ms)
        rebuilt[arm] = {
            "n_members": len(ms),
            "n_powered": sum(bool(m["powered"]) for m in ms),
            "median_spontaneous_refusal_rate": float(np.median(rates)),
            "verdicts": {v: sum(1 for m in ms if m["A_verdict"] == v)
                         for v in sorted({m["A_verdict"] for m in ms})},
            "members": sorted(m["checkpoint"] for m in ms),
        }
    legs = []
    for arm in ARMS:
        a, b = by_arm[arm], rebuilt[arm]
        legs.append(gate_leg(f"G5 {arm} n_members", a["n_members"], b["n_members"],
                             tol=0))
        legs.append(gate_leg(f"G5 {arm} n_powered", a["n_powered"], b["n_powered"],
                             tol=0))
        legs.append(gate_leg(f"G5 {arm} median spontaneous refusal rate",
                             a["median_spontaneous_refusal_rate"],
                             b["median_spontaneous_refusal_rate"]))
        legs.append({"leg": f"G5 {arm} verdict counts",
                     "target": a["verdicts"], "obtained": b["verdicts"],
                     "delta": None, "tolerance": None,
                     "status": "PASS" if a["verdicts"] == b["verdicts"] else "FAIL",
                     "level": "summary-level", "note": ""})
    return legs, rebuilt


def g6_verdict_tally(per_member: list[dict], meta: dict) -> tuple[list[dict], dict]:
    """Recount, and RESOLVE the 18/0/10 (stale) versus 20/1/9 (RESULTS.md)
    discrepancy in writing."""
    tally = {}
    for m in per_member:
        tally[m["A_verdict"]] = tally.get(m["A_verdict"], 0) + 1
    carriers = []
    for rel in ("RESULTS.md", "README.md", ".terminal_claude_agent_struct_out.json"):
        p = R4 / rel
        if p.exists() and "18 of 30" in p.read_text(errors="ignore"):
            carriers.append(str(p))
    resolution = {
        "recount_from_method_out_json": tally,
        "n_members": len(per_member),
        "RESULTS_md_short_version": {"READS": 20, "AT_CHANCE": 0, "UNDEFINED": 9,
                                     "AMBIGUOUS": 1},
        "stale_top_line": {"READS": 18, "AT_CHANCE": 0, "UNDEFINED": 10},
        "correct_tally": tally,
        "which_is_right": "RESULTS.md's short version (20 READS / 1 AMBIGUOUS / "
                          "0 AT_CHANCE / 9 UNDEFINED) is the one that matches a "
                          "recount of method_out.json's own per-member records.",
        "where_the_stale_one_lives": carriers,
        "diagnosis": "",
        "stale_tally_sums_to": 18 + 0 + 10,
    }
    resolution["diagnosis"] = (
        "The stale top line is not merely a different classification of two "
        "members -- it does not account for the panel at all: 18 + 0 + 10 = 28, "
        "two short of the 30 members it claims to summarise. A recount of the 30 "
        "per-member records in method_out.json gives "
        + ", ".join(f"{k} {v}" for k, v in sorted(tally.items()))
        + ", which does sum to 30 and which is exactly what RESULTS.md's short "
        "version already reports (20 READS / 1 AMBIGUOUS / 0 AT_CHANCE / 9 "
        "UNDEFINED). The correct tally is therefore the RESULTS.md one; the "
        "18/0/10 figure must be replaced wherever it appears, and it is the first "
        "number a reader of the artifact summary meets.")
    legs = [
        gate_leg("G6a tally sums to 30", 30, sum(tally.values()), tol=0),
        gate_leg("G6b READS count matches RESULTS.md short version",
                 20, tally.get("READS", 0), tol=0),
        gate_leg("G6c AT_CHANCE count", 0, tally.get("AT_CHANCE", 0), tol=0),
        gate_leg("G6d UNDEFINED count", 9, tally.get("UNDEFINED", 0), tol=0),
        gate_leg("G6e AMBIGUOUS count", 1, tally.get("AMBIGUOUS", 0), tol=0),
        {"leg": "G6f stale 18/0/10 top line located",
         "target": "located", "obtained": (
             "located" if resolution["where_the_stale_one_lives"] else "not found"),
         "delta": None, "tolerance": None, "level": "summary-level",
         "status": "PASS" if resolution["where_the_stale_one_lives"] else "FAIL",
         "note": "; ".join(resolution["where_the_stale_one_lives"])},
    ]
    return legs, resolution


def g7_lineage_bookkeeping(points: list[dict], per_member: list[dict]) -> tuple:
    panel = jload(R4_RESULTS / "panel_resolved.json")
    rows = panel["members"] if isinstance(panel, dict) and "members" in panel else None
    ids_panel = sorted({r.get("lineage_id") for r in rows}) if rows else []
    ids_points = sorted({p["lineage_id"] for p in points})
    ids_all = sorted({m["lineage_id"] for m in per_member})
    rec = {
        "n_distinct_lineage_id_strings_in_scatter": len(ids_points),
        "lineage_ids_in_scatter": ids_points,
        "n_distinct_lineage_id_strings_over_all_30_members": len(ids_all),
        "lineage_ids_over_all_30_members": ids_all,
        "n_distinct_lineage_id_strings_in_panel_resolved": len(ids_panel),
        "T6_claims_n_lineages": 7,
        "iteration_3_recorded_trap": "on the iteration-3 19-member panel, 8 distinct "
                                     "lineage_id STRINGS spanned only 7 lineages "
                                     "(L7's base and instruct roots differ), so "
                                     "clustering naively on the id string silently "
                                     "split one lineage.",
        "merge_map": {},
        "trap_present_here": None,
    }
    rec["trap_present_here"] = bool(len(ids_points) != 7)
    if rec["trap_present_here"]:
        rec["note"] = ("distinct lineage_id strings != 7 on the scatter panel; a "
                       "merge map is required before any lineage bootstrap")
    else:
        rec["note"] = ("the iteration-3 trap does NOT recur on this panel: the 14 "
                       "detection-powered members carry exactly 7 distinct "
                       "lineage_id strings, so the id string IS the cluster key "
                       "and no merge is needed. Over all 30 members the string "
                       f"count is {len(ids_all)}, which is larger only because "
                       "unpowered members bring in lineages that contribute no "
                       "scatter point.")
    legs = [
        gate_leg("G7a distinct lineage_id strings on the 70-pair scatter == 7",
                 7, len(ids_points), tol=0),
        {"leg": "G7b cluster key definition", "target": "lineage_id string",
         "obtained": "lineage_id string", "delta": 0.0, "tolerance": 0,
         "status": "PASS", "level": "summary-level",
         "note": rec["note"]},
    ]
    return legs, rec


# --------------------------------------------------------------------------
def main() -> dict:
    setup_logging("stage1")
    logger.info("STAGE 1: reproduction gate")
    P = load_panel()

    legs: list[dict] = []
    g1 = g1_pooled(P["points"], P["h3"])
    legs += g1
    g1_pass = all(l["status"] == "PASS" for l in g1)
    logger.info(f"G1 {'PASS' if g1_pass else 'FAIL'}: "
                + "; ".join(f"{l['leg'].split()[0]} d={l['delta']:.2e}"
                            for l in g1 if l["delta"] is not None))

    legs += g2_secondary(P["points"], P["h3"])
    legs += g3_within_member(P["points"], P["h3"])
    g4legs, g4meta = g4_per_member_auroc(P["per_member"])
    legs += g4legs
    logger.info(f"G4: {g4meta['n_item_level']} item-level, "
                f"{g4meta['n_summary_level']} summary-level")
    g5legs, arm_rebuilt = g5_arm_table(P["per_member"], P["by_arm"])
    legs += g5legs
    g6legs, g6res = g6_verdict_tally(P["per_member"], P["meta"])
    legs += g6legs
    logger.info(f"G6 tally: {g6res['correct_tally']}")
    g7legs, g7rec = g7_lineage_bookkeeping(P["points"], P["per_member"])
    legs += g7legs

    by_group: dict[str, dict] = {}
    for l in legs:
        g = l["leg"].split()[0][:2]
        b = by_group.setdefault(g, {"n": 0, "n_pass": 0})
        b["n"] += 1
        b["n_pass"] += (l["status"] == "PASS")
    for g, b in by_group.items():
        b["all_pass"] = b["n"] == b["n_pass"]
        logger.info(f"{g}: {b['n_pass']}/{b['n']} PASS")

    out = {
        "legs": legs,
        "n_legs": len(legs),
        "n_pass": sum(l["status"] == "PASS" for l in legs),
        "by_group": by_group,
        "G1_pass": g1_pass,
        "stop_and_diagnose": not g1_pass,
        "g4_levels": g4meta,
        "arm_table_rebuilt": arm_rebuilt,
        "verdict_tally_resolution": g6res,
        "lineage_bookkeeping": g7rec,
        "gate_verdict": ("ALL_PASS" if all(l["status"] == "PASS" for l in legs)
                         else "PARTIAL"),
    }
    jdump(OUT / "stage1.json", out)
    logger.info(f"gate: {out['n_pass']}/{out['n_legs']} legs PASS "
                f"-> {out['gate_verdict']}")
    return out


if __name__ == "__main__":
    main()
