#!/usr/bin/env python3
"""STAGE 3 -- ANALYSIS 2 (H-K): the verdict rule, and the abliterated arm
restated on evidence that does not depend on any AUROC.

(a) double tally, cross-tabulated by arm
(b) attainability simulation of the verdict rule (the only compute-heavy step)
(c) the gate deviation record, with the exact code path
(d) the abliterated arm on refusal-RATE evidence
"""

from __future__ import annotations

import multiprocessing as mp
import os
import time

import numpy as np
from loguru import logger
from scipy.stats import binomtest, mannwhitneyu

import sim
from common5 import (ARMS, EX, OUT, R4, R4_RESULTS, jdump, jload, setup_logging)

VERDICT_ORDER = ["READS", "AMBIGUOUS", "AT_CHANCE", "UNDEFINED"]

N_GRID = [5, 10, 20, 40, 80, 160]
AUROC_GRID = [0.50, 0.55, 0.60, 0.69, 0.75, 0.90, 1.00]
CLUSTER_GRID = [1, 2, 4]
PERFECT_NS = [7, 12, 28, 32, 33]
N_REP = 2000
SIM_SEED0 = 900000


# --------------------------------------------------------------------------
# (a) DOUBLE TALLY
# --------------------------------------------------------------------------
def crosstab(members: list[dict], label: str) -> dict:
    cells = {a: {v: 0 for v in VERDICT_ORDER} for a in ARMS}
    for m in members:
        cells[m["arm"]][m["A_verdict"]] += 1
    row_tot = {a: sum(cells[a].values()) for a in ARMS}
    col_tot = {v: sum(cells[a][v] for a in ARMS) for v in VERDICT_ORDER}
    grand = sum(row_tot.values())
    assert grand == len(members), "cross-tab lost a member"
    assert sum(col_tot.values()) == grand, "column totals do not sum"
    return {"label": label, "cells": cells, "row_totals": row_tot,
            "col_totals": col_tot, "grand_total": grand,
            "n_members": len(members),
            "totals_assert": {"rows_sum_to_grand": True,
                              "cols_sum_to_grand": True}}


def markdown_crosstab(ct: dict) -> str:
    head = "| arm | " + " | ".join(VERDICT_ORDER) + " | total |"
    sep = "|" + "---|" * (len(VERDICT_ORDER) + 2)
    lines = [f"**{ct['label']}** (n = {ct['n_members']} members)", "", head, sep]
    for a in ARMS:
        lines.append("| `" + a + "` | "
                     + " | ".join(str(ct["cells"][a][v]) for v in VERDICT_ORDER)
                     + f" | {ct['row_totals'][a]} |")
    lines.append("| **total** | "
                 + " | ".join(f"**{ct['col_totals'][v]}**" for v in VERDICT_ORDER)
                 + f" | **{ct['grand_total']}** |")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# (b) ATTAINABILITY SIMULATION
# --------------------------------------------------------------------------
def build_cells() -> list[tuple]:
    cells, s = [], SIM_SEED0
    for n in N_GRID:
        for a in AUROC_GRID:
            for k in CLUSTER_GRID:
                cells.append((n, a, k, N_REP, s))
                s += 1
    for n in PERFECT_NS:                      # the shipped unpowered READS counts
        for k in CLUSTER_GRID:
            cells.append((n, 1.00, k, N_REP, s))
            s += 1
    return cells


SIM_CACHE = OUT / "sim_raw.json"


def run_simulation(n_proc: int) -> dict:
    cells = build_cells()
    if SIM_CACHE.exists():
        cached = jload(SIM_CACHE)
        if (cached.get("grid_signature") == repr(cells)
                and len(cached["rows"]) == len(cells)):
            logger.info(f"simulation surface reused from {SIM_CACHE} "
                        f"({len(cached['rows'])} cells, "
                        f"{cached['wall_seconds']:.1f}s when first computed)")
            return cached
        logger.warning("cached simulation surface does not match the grid; "
                       "recomputing")
    logger.info(f"simulation: {len(cells)} cells x {N_REP} replicates x "
                f"{sim.N_BOOT_INNER} inner bootstrap reps, on {n_proc} processes")
    t0 = time.time()
    # heaviest cells first so the pool drains evenly
    cells = sorted(cells, key=lambda c: -c[0])
    with mp.get_context("fork").Pool(n_proc) as pool:
        rows = pool.map(sim.run_cell, cells, chunksize=1)
    wall = time.time() - t0
    logger.info(f"simulation done in {wall:.1f}s")
    out = {"rows": rows, "wall_seconds": wall, "n_cells": len(rows),
           "grid_signature": repr(build_cells())}
    jdump(SIM_CACHE, out)
    return out


def extract_answers(rows: list[dict]) -> dict:
    def get(n, a, k):
        for r in rows:
            if (r["n_per_class"] == n and abs(r["true_auroc"] - a) < 1e-9
                    and r["items_per_prompt"] == k):
                return r
        return None

    # (i) minimum n at which AT_CHANCE is attainable AT ALL (true AUROC = 0.50)
    #
    # A cell with very few prompt CLUSTERS is degenerate: with only 2-3 clusters
    # per class a large share of the resamples are literally the same items, the
    # bootstrap distribution collapses and the CI narrows for a reason that has
    # nothing to do with evidence. Those cells are flagged and excluded from the
    # "minimum n" reading rather than being allowed to answer it.
    MIN_CLUSTERS_NONDEGENERATE = 10
    min_n = {}
    for k in CLUSTER_GRID:
        first_any, first_half, first_any_nd = None, None, None
        degenerate = []
        for n in N_GRID:
            r = get(n, 0.50, k)
            if r is None:
                continue
            deg = r["n_clusters"] < MIN_CLUSTERS_NONDEGENERATE
            if deg:
                degenerate.append({"n_per_class": n, "n_clusters": r["n_clusters"],
                                   "P_AT_CHANCE": r["P_AT_CHANCE"]})
            if first_any is None and r["P_AT_CHANCE"] > 0:
                first_any = n
            if first_any_nd is None and r["P_AT_CHANCE"] > 0 and not deg:
                first_any_nd = n
            if first_half is None and r["P_AT_CHANCE"] >= 0.5:
                first_half = n
        min_n[str(k)] = {
            "min_n_with_any_AT_CHANCE": first_any,
            "min_n_with_any_AT_CHANCE_excluding_degenerate_cells": first_any_nd,
            "degenerate_cells": degenerate,
            "degeneracy_rule": (f"a cell with fewer than {MIN_CLUSTERS_NONDEGENERATE} "
                                f"prompt clusters in total is degenerate: the "
                                f"cluster bootstrap has too few distinct draws for "
                                f"its CI width to mean anything"),
            "min_n_with_P_AT_CHANCE_ge_0p5": first_half,
            "P_AT_CHANCE_by_n": {str(n): (get(n, 0.50, k) or {}).get("P_AT_CHANCE")
                                 for n in N_GRID},
            "mean_ci_width_by_n": {str(n): (get(n, 0.50, k) or {}).get("mean_ci_width")
                                   for n in N_GRID},
        }
    hm = sim.hanley_mcneil_min_n()

    # (ii) P(READS | true AUROC = 0.50) versus n -- the false-positive rate
    fpr = {str(k): {str(n): (get(n, 0.50, k) or {}).get("P_READS")
                    for n in N_GRID} for k in CLUSTER_GRID}

    # (iii) P(READS) under perfect separation at the shipped unpowered counts
    perfect = {str(k): {str(n): (get(n, 1.00, k) or {}).get("P_READS")
                        for n in PERFECT_NS} for k in CLUSTER_GRID}
    perfect_undef = {str(k): {str(n): (get(n, 1.00, k) or {}).get("P_UNDEFINED")
                              for n in PERFECT_NS} for k in CLUSTER_GRID}

    gate40 = {str(k): (get(40, 0.50, k) or {}).get("P_AT_CHANCE")
              for k in CLUSTER_GRID}
    return {
        "min_n_for_AT_CHANCE": min_n,
        "hanley_mcneil_closed_form": hm,
        "pre_registered_gate_is_sufficient": {
            "gate_n_per_class": EX.MIN_PER_CLASS,
            "P_AT_CHANCE_at_the_gate_true_auroc_0p50": gate40,
            "sufficient": all((v or 0) > 0 for v in gate40.values()),
            "reading": ("if P(AT_CHANCE) is 0 at n = 40 under a TRUE AUROC of "
                        "0.50, the pre-registered >= 40 gate does not by itself "
                        "make the null verdict reachable, and 'zero AT_CHANCE' "
                        "is arithmetic rather than evidence"),
        },
        "P_READS_at_true_chance": fpr,
        "P_READS_under_perfect_separation": perfect,
        "P_UNDEFINED_under_perfect_separation": perfect_undef,
    }


def footnote(ans: dict) -> str:
    k1 = ans["min_n_for_AT_CHANCE"]["1"]
    n_any = k1["min_n_with_any_AT_CHANCE"]
    hm = ans["hanley_mcneil_closed_form"]["min_n_per_class"]
    p40 = ans["pre_registered_gate_is_sufficient"][
        "P_AT_CHANCE_at_the_gate_true_auroc_0p50"]["1"]
    perf = ans["P_READS_under_perfect_separation"]["1"]
    perf_vals = sorted({v for v in perf.values() if v is not None})
    perf_txt = (f"{perf_vals[0]:.3f}" if len(perf_vals) == 1
                else f"{min(perf_vals):.3f}-{max(perf_vals):.3f}")
    fpr = ans["P_READS_at_true_chance"]["1"]
    tail = (
        " The asymmetry is one-sided in a way worth stating exactly: the READS "
        f"rule is NOT trigger-happy at true chance (P(READS | AUROC = 0.500) is "
        f"{fpr['5']:.4f} at n = 5 and {fpr['40']:.4f} at n = 40), so a READS "
        "verdict is not a false positive manufactured by noise. What the rule "
        "cannot do at these sample sizes is return the NULL verdict at all, and a "
        "handful of perfectly separated items is enough to return READS with "
        "certainty. A count of zero AT_CHANCE verdicts is therefore substantially "
        "a property of the rule at these sample sizes, not a measurement of the "
        "models.")
    return (
        "The AT_CHANCE verdict requires an entire bootstrap 95% CI to fit inside "
        "the 0.20-wide band [0.40, 0.60], whereas READS requires only the lower "
        "bound to clear 0.60. Simulating this exact rule on the same "
        "prompt-clustered percentile bootstrap "
        f"({sim.N_BOOT_INNER} inner reps, {N_REP} replicates per cell) shows the "
        f"asymmetry is severe: at a TRUE AUROC of 0.500 the null verdict is "
        f"unreachable below n = {n_any} items per class "
        f"(P(AT_CHANCE) = {p40:.3f} at the pre-registered n = {EX.MIN_PER_CLASS} "
        f"gate; the Hanley-McNeil closed form puts the i.i.d. threshold at "
        f"n = {hm}), while under perfect separation READS fires with probability "
        f"{perf_txt} at the counts of 7 to 33 items per class at which the "
        "shipped table issues it on unpowered members." + tail)


# --------------------------------------------------------------------------
# (c) GATE DEVIATION RECORD
# --------------------------------------------------------------------------
def deviation_record(per_member: list[dict]) -> dict:
    exp = (R4 / "explib.py").read_text().splitlines()
    gpu = (R4 / "gpu_stage.py").read_text().splitlines()
    q_verdict = "\n".join(exp[485:494])
    q_guard = "\n".join(exp[554:563])
    q_powered = "\n".join(gpu[341:345])

    undefined = [m for m in per_member if m["A_verdict"] == "UNDEFINED"]
    unpowered_reads = [m for m in per_member
                       if m["A_verdict"] == "READS" and not m["powered"]]
    powered_below_40 = [m["checkpoint"] for m in per_member
                        if m["powered"] and min(m["n_refusal"],
                                                m["n_compliance"]) < EX.MIN_PER_CLASS]
    min_items = min(min(m["n_refusal"], m["n_compliance"])
                    for m in unpowered_reads) if unpowered_reads else None
    return {
        "id": "DEV-ITER5-01",
        "n_boot_reference": EX.N_BOOT,
        "min_finite_boot_reps_for_a_ci": 20,
        "min_class_in_resample": 5,
        "MIN_PER_CLASS": EX.MIN_PER_CLASS,
        "min_items_per_class_among_unpowered_reads": min_items,
        "trigger": "H-K review item: the Method describes UNDEFINED as firing at "
                   "fewer than 40 refusals; the code does not implement that.",
        "what_the_method_said": "A member's detection verdict is UNDEFINED when it "
                                "produced fewer than 40 spontaneous refusals.",
        "what_the_code_does": (
            "explib.verdict_from_ci returns UNDEFINED if and ONLY IF the CI bounds "
            "are non-finite. The bounds go non-finite because explib.boot_ci "
            "returns (nan, nan) when fewer than 20 bootstrap replicates survive, "
            "and replicates are discarded by the >= 5-per-class resample guard in "
            "explib.detection_stats. In practice a member needs 0-1 items in one "
            "class before that guard kills enough resamples. MIN_PER_CLASS = 40 "
            "governs a SEPARATE `powered` flag set in gpu_stage.py, which is not "
            "consulted by the verdict at all -- which is why the shipped table "
            f"issues READS on members with as few as {min_items} items per class."),
        "code_path": {
            "verdict": {"file": "explib.py", "lines": "486-494",
                        "quote": q_verdict},
            "resample_guard": {"file": "explib.py", "lines": "555-563",
                               "quote": q_guard},
            "powered_flag": {"file": "gpu_stage.py", "lines": "342-345",
                             "quote": q_powered},
        },
        "affected_members": {
            "UNDEFINED_verdict": [
                {"checkpoint": m["checkpoint"], "n_refusal": m["n_refusal"],
                 "n_compliance": m["n_compliance"],
                 "spontaneous_refusal_rate": m["spontaneous_refusal_rate"],
                 "arm": m["arm"]} for m in undefined],
            "UNPOWERED_yet_READS": [
                {"checkpoint": m["checkpoint"], "n_refusal": m["n_refusal"],
                 "n_compliance": m["n_compliance"], "A_auroc": m["A_auroc"],
                 "A_ci95": m["A_ci95"], "arm": m["arm"]} for m in unpowered_reads],
            "n_UNDEFINED": len(undefined),
            "n_UNPOWERED_yet_READS": len(unpowered_reads),
            "powered_members_below_MIN_PER_CLASS": powered_below_40,
        },
        "correction_text": (
            "A member's axis-A verdict is UNDEFINED when its bootstrap confidence "
            "interval cannot be formed -- which happens when so few items of one "
            "class survive that fewer than 20 of the 2,000 prompt-clustered "
            "resamples retain at least five per class. This is a property of the "
            "resampling guard, not of the 40-per-class POWERED gate: the powered "
            "flag is recorded separately and does not enter the verdict, so the "
            "table reports READS for members with as few as "
            f"{min_items} "
            "items per class."),
    }


# --------------------------------------------------------------------------
# (d) THE ABLITERATED ARM ON REFUSAL-RATE EVIDENCE
# --------------------------------------------------------------------------
def exhaustive_two_sample_perm(x, y) -> dict:
    """Exact two-sided permutation p for the Mann-Whitney U over ALL C(n1+n2, n1)
    group assignments. Unlike scipy's exact method this is valid under ties,
    because the tied ranks are held fixed and only the labels move."""
    from itertools import combinations
    from math import comb

    from scipy.stats import rankdata
    x, y = list(x), list(y)
    n1, n2 = len(x), len(y)
    r = rankdata(np.asarray(x + y, float))
    obs = float(r[:n1].sum())
    mean = n1 * (n1 + n2 + 1) / 2.0
    idx = range(n1 + n2)
    total = comb(n1 + n2, n1)
    extreme = 0
    for c in combinations(idx, n1):
        s = float(r[list(c)].sum())
        if abs(s - mean) >= abs(obs - mean) - 1e-9:
            extreme += 1
    return {"n_permutations": int(total), "n_extreme": int(extreme),
            "p_two_sided": extreme / total, "p_floor": 1.0 / total,
            "statistic_rank_sum_group1": obs, "null_mean": mean,
            "note": "exact under ties; the identity assignment is always counted, "
                    "so the attainable floor is 1/C(n1+n2, n1)"}


def abliterated_arm(per_member: list[dict], h1b: dict) -> dict:
    def denom(m):
        d = jload(R4_RESULTS / f"detect_{m['checkpoint']}.json")
        return int(d["exclusion_cascade"]["scanned"]), int(m["n_scanned"])

    table = []
    for m in per_member:
        scanned_cascade, n_scanned = denom(m)
        k = int(m["n_refusal_of_scanned"])
        lo, hi = EX.wilson(k, n_scanned)
        table.append({
            "checkpoint": m["checkpoint"], "arm": m["arm"],
            "lineage_id": m["lineage_id"],
            "n_refusal_scored": int(m["n_refusal"]),
            "n_compliance_scored": int(m["n_compliance"]),
            "n_refusal_of_scanned": k,
            "n_scanned": n_scanned,
            "n_kept_by_exclusion_cascade": scanned_cascade,
            "spontaneous_refusal_rate": m["spontaneous_refusal_rate"],
            "wilson95": [lo, hi],
            "powered": bool(m["powered"]),
            "A_auroc": m["A_auroc"], "A_ci95": m["A_ci95"],
            "A_verdict": m["A_verdict"],
        })
    we = [t for t in table if t["arm"] == "weight_edited_abliteration"]
    ar = [t for t in table if t["arm"] == "aligned_reference"]
    bc = [t for t in table if t["arm"] == "behavioural_uncensored_candidate"]

    med = {a: float(np.median([t["spontaneous_refusal_rate"]
                               for t in table if t["arm"] == a])) for a in ARMS}

    # (i) Mann-Whitney U on member rates, weight-edited vs aligned reference.
    #
    # The two arms SHARE a rate (Llama_3p2_1B and Llama_3p2_1B_Instruct_abliterated
    # both refuse on 28 of 1,585), so the pooled sample is TIED and scipy's
    # `method="exact"` -- which assumes no ties -- is not valid here even though
    # it returns a number without complaint. The primary p is therefore the
    # tie-corrected asymptotic one, and an EXHAUSTIVE permutation over all
    # C(21, 9) = 293,930 group assignments is reported beside it: that one is
    # exact AND handles ties, because it re-uses the same tied ranks in every
    # permutation.
    xw = [t["spontaneous_refusal_rate"] for t in we]
    xa = [t["spontaneous_refusal_rate"] for t in ar]
    n1, n2 = len(xw), len(xa)
    shared = sorted(set(xw) & set(xa))     # values tied ACROSS the two arms
    n_ties = len(shared)
    mw = mannwhitneyu(xw, xa, alternative="two-sided", method="asymptotic")
    mwl = mannwhitneyu(xw, xa, alternative="less", method="asymptotic")
    mw_exact_invalid = mannwhitneyu(xw, xa, alternative="two-sided", method="exact")
    perm = exhaustive_two_sample_perm(xw, xa)
    cles = float(mw.statistic) / (n1 * n2)

    # (ii) lineage-clustered bootstrap of the difference in MEDIANS
    lin_w = [t["lineage_id"] for t in we]
    lin_a = [t["lineage_id"] for t in ar]
    all_lin = sorted(set(lin_w) | set(lin_a))
    rng = np.random.default_rng(20260813)
    diffs = []
    for _ in range(10000):
        pick = rng.choice(len(all_lin), size=len(all_lin), replace=True)
        chosen = [all_lin[i] for i in pick]
        bw = [t["spontaneous_refusal_rate"] for L in chosen for t in we
              if t["lineage_id"] == L]
        ba = [t["spontaneous_refusal_rate"] for L in chosen for t in ar
              if t["lineage_id"] == L]
        if bw and ba:
            diffs.append(float(np.median(bw) - np.median(ba)))
    diffs_a = np.asarray(diffs, float)
    boot = {
        "delta_median_point": float(np.median(xw) - np.median(xa)),
        "ci95": [float(np.percentile(diffs_a, 2.5)),
                 float(np.percentile(diffs_a, 97.5))],
        "n_boot_valid": int(diffs_a.size), "n_boot": 10000,
        "n_resampling_units": len(all_lin),
        "resampling_unit": "lineage_id",
        "p_boot_two_sided": float(EX.boot_p_two_sided(diffs_a, 0.0)),
        "excludes_zero": bool(np.percentile(diffs_a, 97.5) < 0
                              or np.percentile(diffs_a, 2.5) > 0),
    }

    # (iii) the within-lineage PAIRED comparison already tabulated in T2b
    pairs = paired_T2b(per_member, h1b)

    carried = bool(mw.pvalue < 0.05 and perm["p_two_sided"] < 0.05
                   and boot["excludes_zero"]
                   and pairs["sign_test"]["p_value"] < 0.05)
    return {
        "table": table,
        "weight_edited": we, "aligned_reference": ar,
        "behavioural_uncensored_candidate": bc,
        "arm_medians": med,
        "n_weight_edited": len(we),
        "n_weight_edited_READS": sum(t["A_verdict"] == "READS" for t in we),
        "n_weight_edited_READS_powered": sum(
            t["A_verdict"] == "READS" and t["powered"] for t in we),
        "n_weight_edited_READS_unpowered": sum(
            t["A_verdict"] == "READS" and not t["powered"] for t in we),
        "mann_whitney": {
            "test": "two-sided Mann-Whitney U on member-level spontaneous refusal "
                    "rates, weight_edited_abliteration vs aligned_reference; "
                    "tie-corrected asymptotic p is primary because the pooled "
                    "sample is tied, with an exhaustive permutation p beside it",
            "U": float(mw.statistic), "p_two_sided": float(mw.pvalue),
            "p_one_sided_less": float(mwl.pvalue),
            "n_tied_values_across_arms": int(n_ties),
            "tied_values_across_arms": shared,
            "p_exhaustive_permutation": perm["p_two_sided"],
            "n_permutations": perm["n_permutations"],
            "p_permutation_floor": perm["p_floor"],
            "p_scipy_exact_INVALID_WITH_TIES": float(mw_exact_invalid.pvalue),
            "why_not_exact": ("scipy's exact Mann-Whitney null assumes no ties; "
                              "the two arms share a rate (28 of 1,585 on two "
                              "different checkpoints), so that p is recorded only "
                              "to show it was checked, never quoted"),
            "n_weight_edited": n1, "n_aligned_reference": n2,
            "common_language_effect_size": cles,
            "median_weight_edited": float(np.median(xw)),
            "median_aligned_reference": float(np.median(xa)),
        },
        "lineage_clustered_bootstrap_median_difference": boot,
        "within_lineage_paired": pairs,
        "structural_claim_carried_without_any_AUROC": carried,
        "claim_text": (
            "abliteration removes the refusals, not the reader"
            if carried else
            "the structural claim is NOT established by the refusal-rate evidence "
            "alone"),
    }


def paired_T2b(per_member: list[dict], h1b: dict) -> dict:
    """The 10 within-lineage abliterated-vs-parent pairs of T2b, on RATES."""
    by_ck = {m["checkpoint"]: m for m in per_member}
    pairs_src = h1b.get("pairs") or h1b.get("per_pair") or []
    rows = []
    for p in pairs_src:
        a = by_ck.get(p.get("abliterated") or p.get("child"))
        q = by_ck.get(p.get("parent"))
        if a is None or q is None:
            continue
        rows.append({
            "lineage_id": a["lineage_id"],
            "abliterated": a["checkpoint"], "parent": q["checkpoint"],
            "rate_abliterated": a["spontaneous_refusal_rate"],
            "rate_parent": q["spontaneous_refusal_rate"],
            "delta_rate": a["spontaneous_refusal_rate"] - q["spontaneous_refusal_rate"],
            "abliterated_lower": bool(a["spontaneous_refusal_rate"]
                                      < q["spontaneous_refusal_rate"]),
            "max_rate_abliterated": a["A_max_rate"], "max_rate_parent": q["A_max_rate"],
        })
    n = len(rows)
    k = sum(r["abliterated_lower"] for r in rows)
    bt = binomtest(k, n, 0.5, alternative="two-sided") if n else None
    deltas = [r["delta_rate"] for r in rows]
    return {
        "n_pairs": n, "source": "T2b within-lineage abliterated-vs-parent pairs",
        "pairs": rows,
        "n_abliterated_lower": k,
        "sign_test": {"test": "exact paired sign test (binomial, p = 0.5)",
                      "k": k, "n": n,
                      "p_value": (float(bt.pvalue) if bt else None),
                      "ci95_proportion": ([float(v) for v in
                                           bt.proportion_ci(method="exact")]
                                          if bt else None)},
        "median_delta_rate": (float(np.median(deltas)) if deltas else None),
        "mean_delta_rate": (float(np.mean(deltas)) if deltas else None),
        "delta_rate_range": ([float(min(deltas)), float(max(deltas))]
                             if deltas else None),
    }


# --------------------------------------------------------------------------
def main(n_proc: int | None = None) -> dict:
    setup_logging("stage3")
    logger.info("STAGE 3: H-K -- the verdict rule and the abliterated arm")
    res = jload(R4 / "method_out.json")["metadata"]["results"]
    per_member = res["h1_abliterated_arm"]["per_member"]
    h1b = res["h1b_induction_paired"]

    ct_all = crosstab(per_member, "axis-A verdicts, ALL 30 members (as shipped)")
    powered = [m for m in per_member if m["powered"]]
    ct_pow = crosstab(powered, "axis-A verdicts, DETECTION-POWERED members only "
                                f"(>= {EX.MIN_PER_CLASS} per class)")
    logger.info(f"tally all-30: {ct_all['col_totals']}")
    logger.info(f"tally powered-{len(powered)}: {ct_pow['col_totals']}")

    dev = deviation_record(per_member)
    logger.info(f"deviation: {dev['affected_members']['n_UNPOWERED_yet_READS']} "
                f"UNPOWERED members receive READS")

    arm = abliterated_arm(per_member, h1b)
    logger.info(f"abliterated arm: MW p = {arm['mann_whitney']['p_two_sided']:.4g} "
                f"(perm {arm['mann_whitney']['p_exhaustive_permutation']:.4g}); "
                f"paired sign test p = "
                f"{arm['within_lineage_paired']['sign_test']['p_value']}; "
                f"carried = {arm['structural_claim_carried_without_any_AUROC']}")

    n_proc = n_proc or max(1, min(4, (os.cpu_count() or 4)))
    simres = run_simulation(n_proc)
    ans = extract_answers(simres["rows"])
    fn = footnote(ans)
    logger.info("FOOTNOTE: " + fn[:220])

    out = {
        "tally_all_members": ct_all,
        "tally_detection_powered": ct_pow,
        "tally_markdown": (markdown_crosstab(ct_all) + "\n\n"
                           + markdown_crosstab(ct_pow)),
        "attainability_simulation": {
            "grid": {"n_per_class": N_GRID, "true_auroc": AUROC_GRID,
                     "items_per_prompt": CLUSTER_GRID,
                     "perfect_separation_extra_n": PERFECT_NS,
                     "n_replicates_per_cell": N_REP,
                     "n_boot_inner": sim.N_BOOT_INNER},
            "surface": simres["rows"],
            "n_cells": simres["n_cells"],
            "wall_seconds": simres["wall_seconds"],
            "extracted_answers": ans,
            "footnote": fn,
            "fidelity_note": sim.__doc__,
        },
        "deviation_record": dev,
        "abliterated_arm": arm,
    }
    jdump(OUT / "stage3.json", out)
    logger.info("STAGE 3 done")
    return out


if __name__ == "__main__":
    main()
