#!/usr/bin/env python3
"""STAGE 1 -- DUAL AGGREGATION (the H-U repair).

The draft reports the SAME our-AMS correlation as 0.358 in one section (19
members, lineage-clustered) and 0.821 in another (7 lineage-aggregated units).
This stage computes every score at BOTH units, under the analysis-choice grid
that separates the three things conflated in that gap -- the aggregation unit,
the UNRELIABLE exclusion, and the UNDEFINED convention -- and states n and the
permutation floor in every cell.

The permutation unit is the LINEAGE in BOTH aggregations. That is the point
that makes the two rows comparable: members within a lineage are not
independent, so a member-level permutation over 19! would be an invalid null.
"""

from __future__ import annotations

import numpy as np
from loguru import logger

from common import (N_BOOT, OUT, SCORE_COLUMNS, jdump, jload, setup_logging, sx)
from stage0_ingest import column_values, lineage_units

ALPHA50_ROW_COLUMN = "max_refusal_rate"          # E3's alpha_50 row carrier
ALPHA50_V2_COLUMN = "alpha_50_nonparametric"     # V2's alpha_50 row carrier
AMS_COLUMN = "ams_sigma"

# The analysis-choice grid. `primary` cells get the full statistic set; the
# others are reported as a rho-only sensitivity surface.
CONFIGS = [
    {"id": "all19_drop_undefined_yE3", "reliable_only": False,
     "convention": "drop_undefined", "ycol": "y_e3", "primary": True,
     "label": "all 19 members / UNDEFINED dropped / outcome as transcribed by E3",
     "reproduces": "E3's discrimination-matrix row (member level)"},
    {"id": "reliable14_rank_bottom_yV2", "reliable_only": True,
     "convention": "rank_bottom", "ycol": "y_v2", "primary": True,
     "label": "14 reliable members / UNDEFINED ranked bottom / outcome from V2's member table",
     "reproduces": "V2's oriented-Delta evaluation (lineage level)"},
    {"id": "all19_rank_bottom_yE3", "reliable_only": False,
     "convention": "rank_bottom", "ycol": "y_e3", "primary": False,
     "label": "all 19 members / UNDEFINED ranked bottom / E3 outcome", "reproduces": None},
    {"id": "reliable14_drop_undefined_yE3", "reliable_only": True,
     "convention": "drop_undefined", "ycol": "y_e3", "primary": False,
     "label": "14 reliable members / UNDEFINED dropped / E3 outcome", "reproduces": None},
    {"id": "all19_drop_undefined_yV2", "reliable_only": False,
     "convention": "drop_undefined", "ycol": "y_v2", "primary": False,
     "label": "all 19 members / UNDEFINED dropped / V2 outcome", "reproduces": None},
    {"id": "reliable14_rank_bottom_yE3", "reliable_only": True,
     "convention": "rank_bottom", "ycol": "y_e3", "primary": False,
     "label": "14 reliable members / UNDEFINED ranked bottom / E3 outcome", "reproduces": None},
]


# --------------------------------------------------------------------------
# cell construction
# --------------------------------------------------------------------------
def member_level_vectors(rows, col, orientation, cfg):
    sel = [r for r in rows if not (cfg["reliable_only"] and r["unreliable"])]
    xs = column_values(sel, col, orientation, cfg["convention"])
    ys = [r[cfg["ycol"]] for r in sel]
    lin = [r["lineage"] for r in sel]
    ids = [r["member_id"] for r in sel]
    keep = [i for i in range(len(sel)) if xs[i] is not None and ys[i] is not None]
    return ([xs[i] for i in keep], [ys[i] for i in keep],
            [lin[i] for i in keep], [ids[i] for i in keep])


def lineage_level_vectors(rows, col, orientation, cfg):
    lu = lineage_units(rows, col, ycol=cfg["ycol"],
                       reliable_only=cfg["reliable_only"],
                       orientation=orientation, convention=cfg["convention"])
    us = lu["units"]
    return ([u["x"] for u in us], [u["y"] for u in us],
            [u["lineage"] for u in us], [u["lineage"] for u in us], lu)


def n_ties(v) -> int:
    """number of values that share their value with at least one other."""
    from collections import Counter
    c = Counter(round(float(x), 12) for x in v)
    return int(sum(k for k in c.values() if k > 1))


def cell(x, y, lineages, orientation, unit_name, full: bool = True) -> dict:
    xo = sx.orient(x, orientation)
    n = len(x)
    n_lin = len(set(lineages))
    basic = sx.spearman_basic(xo, y)
    raw = sx.spearman_basic(list(map(float, x)), y)
    out = {
        "unit": unit_name, "n": n, "n_lineages_used": n_lin,
        "orientation_sign": int(orientation),
        "rho_oriented": basic["rho"], "rho_raw_unoriented": raw["rho"],
        "p_asymptotic_oriented": basic["p_asymptotic"],
        "n_tied_x": n_ties(x), "n_tied_y": n_ties(y),
        "tie_note": ("scipy average-rank Spearman, as the archived code uses; "
                     "max_refusal_rate carries ties at 0.0"),
    }
    if not full or basic["rho"] is None:
        out["ci95"] = None
        out["ci_suppressed_reason"] = ("rho undefined" if basic["rho"] is None
                                       else "rho-only sensitivity cell")
        return out

    # (ii) CI. Member level: lineage-CLUSTERED bootstrap. Lineage level: an
    # ordinary unit bootstrap, obtained from the SAME archived estimator by
    # making each unit its own cluster.
    if n_lin <= 3:
        out["ci95"] = None
        out["ci_suppressed_reason"] = (
            f"n_lineages = {n_lin} <= 3; a bootstrap over {n_lin} numbers is not "
            "an interval (the rule iteration 2 used when it suppressed a pooled "
            "CI over 2 numbers)")
        out["n_boot_valid"] = 0
    else:
        bs = sx.clustered_bootstrap_rho(xo, y, lineages, n_boot=N_BOOT)
        out["ci95"] = bs["ci95_lineage_clustered"]
        out["n_boot_valid"] = bs["n_boot_valid"]
        out["ci_suppressed_reason"] = None
    out["bootstrap_resampling_unit"] = ("lineage label (clustered)" if unit_name == "member"
                                        else "lineage unit (ordinary)")

    # (iii) exhaustive lineage permutation
    perm = sx.lineage_permutation_p(xo, y, lineages)
    p = perm.get("p_permutation")
    floor = perm.get("p_min_achievable")
    out["permutation"] = {
        "p": p, "p_min_achievable": floor,
        "p_min_two_sided_symmetric_reference": perm.get(
            "p_min_two_sided_symmetric_reference"),
        "exhaustive": perm.get("exhaustive"),
        "n_permutations": perm.get("n_permutations"),
        "n_extreme": perm.get("n_extreme"),
        "permutation_unit": "lineage (identical at both aggregations, by design)",
        "p_at_permutation_floor": bool(p is not None and floor is not None
                                       and abs(p - floor) < 1e-12),
    }
    if n_lin < 5:
        out["permutation"]["verdict"] = "PERMUTATION_UNINFORMATIVE_AT_THIS_N"
        out["permutation"]["verdict_reason"] = (
            f"the exhaustive floor is 1/{n_lin}! = {floor}; at n_lineages <= 3 "
            "that floor exceeds 0.05, so no p can reach significance")
    else:
        out["permutation"]["verdict"] = "INFORMATIVE"

    # (v) orientation-free comparator
    out["auc_y_above_median"] = sx.auc_binary(xo, y)
    # (vi) leave-one-lineage-out jackknife
    jk = sx.loo_lineage_jackknife(xo, y, lineages)
    out["jackknife"] = {"range": jk["range"], "spread": jk["spread"],
                        "sign_stable": jk["sign_stable"], "n_folds": jk["n_folds"],
                        "folds": jk["folds"]}
    out["disattenuated"] = {
        "reliability_0.75": sx.disattenuate(basic["rho"], sx.JUDGE_SELF_AGREEMENT_FROZEN),
        "reliability_0.9597": sx.disattenuate(basic["rho"],
                                              sx.JUDGE_SELF_AGREEMENT_REPAIRED),
    }
    parts = [f"rho_oriented={basic['rho']:.3f}"]
    parts.append(f"95% CI {[round(v, 3) for v in out['ci95']]}" if out["ci95"]
                 else f"CI suppressed ({out['ci_suppressed_reason']})")
    if p is not None and floor is not None:
        parts.append(f"exhaustive lineage permutation p={p:.3e} (floor {floor:.3e})")
    parts.append(f"n={n} {unit_name}s over {n_lin} lineages")
    out["printed"] = ", ".join(parts)
    return out


# --------------------------------------------------------------------------
# paired Delta and orientation-free companions
# --------------------------------------------------------------------------
def paired_delta(x_a, x_b, y, lineages, sign_a, sign_b, unit_name) -> dict:
    """Delta = rho_oriented(score A) - rho_oriented(score B) on the SAME
    resampled lineages, using the archived paired estimator verbatim."""
    a = sx.orient(x_a, sign_a)
    b = sx.orient(x_b, sign_b)
    res = sx.paired_rho_delta_clustered(a, b, y, lineages, n_boot=N_BOOT)
    n_lin = len(set(lineages))
    if n_lin <= 3:
        res["ci95"] = None
        res["ci_suppressed_reason"] = f"n_lineages = {n_lin} <= 3"
    res["unit"] = unit_name
    res["n_lineages_used"] = n_lin

    # exhaustive permutation on Delta itself: permute the lineage blocks of y
    # once and recompute BOTH correlations, so the null is the same for both.
    import itertools
    import math
    from scipy.stats import rankdata
    idx = [i for i in range(len(y)) if a[i] is not None and b[i] is not None
           and y[i] is not None]
    ra = rankdata([a[i] for i in idx])
    rb = rankdata([b[i] for i in idx])
    ry = rankdata([y[i] for i in idx])
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    blocks = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    d0 = res.get("delta")
    if d0 is not None and math.factorial(len(uniq)) <= 40320:
        cnt = 0
        nfac = math.factorial(len(uniq))
        for perm in itertools.permutations(range(len(uniq))):
            yy = np.empty_like(ry)
            for si, L in enumerate(uniq):
                tgt = blocks[uniq[perm[si]]]
                for j, mem in enumerate(blocks[L]):
                    yy[mem] = ry[tgt[j % len(tgt)]]
            r1, r2 = sx._rho(ra, yy), sx._rho(rb, yy)
            if r1 is not None and r2 is not None and abs(r1 - r2) >= abs(d0) - 1e-12:
                cnt += 1
        res["permutation"] = {"p": cnt / nfac, "p_min_achievable": 1.0 / nfac,
                              "n_permutations": nfac, "n_extreme": cnt,
                              "exhaustive": True,
                              "permutation_unit": "lineage"}
    else:
        res["permutation"] = None

    # ceiling check: what an IDEAL score would have scored
    rho_b = res.get("rho_reference")
    res["ceiling"] = {
        "oriented_ceiling_delta": (None if rho_b is None else 1.0 - rho_b),
        "definition": ("Delta for a perfect metric: an oriented rho of +1.0 "
                       "against the same reference"),
        "old_unoriented_statistic_note": (
            "the pre-registered unoriented statistic gave a perfect alpha_50 "
            "Delta = -1.821 on V2's lineage units, i.e. it could not have "
            "rewarded the ideal case at all"),
    }
    # |rho| comparator with a clustered paired bootstrap on the same draws
    res["abs_rho_difference"] = _abs_rho_delta(a, b, y, lineages)
    return res


def _abs_rho_delta(a, b, y, lineages, n_boot: int = N_BOOT) -> dict:
    idx = [i for i in range(len(y)) if a[i] is not None and b[i] is not None
           and y[i] is not None]
    A = np.array([float(a[i]) for i in idx])
    B = np.array([float(b[i]) for i in idx])
    Y = np.array([float(y[i]) for i in idx])
    lin = [lineages[i] for i in idx]
    uniq = sorted(set(lin))
    by = {L: [j for j, v in enumerate(lin) if v == L] for L in uniq}
    ra, rb = sx._rho(A, Y), sx._rho(B, Y)
    if ra is None or rb is None:
        return {"point": None, "ci95": None}
    rng = np.random.default_rng(sx.BOOT_SEED)
    boot = []
    for _ in range(n_boot):
        sel: list[int] = []
        for k in rng.integers(0, len(uniq), size=len(uniq)):
            sel.extend(by[uniq[k]])
        if len(sel) < 3:
            continue
        r1, r2 = sx._rho(A[sel], Y[sel]), sx._rho(B[sel], Y[sel])
        if r1 is not None and r2 is not None:
            boot.append(abs(r1) - abs(r2))
    ci = ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
          if len(boot) >= 50 and len(uniq) > 3 else None)
    return {"point": abs(ra) - abs(rb), "ci95": ci, "n_boot_valid": len(boot),
            "note": "orientation-free comparator: |rho(A)| - |rho(B)|"}


# --------------------------------------------------------------------------
# why they differ
# --------------------------------------------------------------------------
def icc_one_way(values, lineages) -> dict:
    """One-way random-effects variance decomposition on the members that carry
    a defined value. ICC = between / (between + within)."""
    pairs = [(float(v), L) for v, L in zip(values, lineages) if v is not None]
    if len(pairs) < 3:
        return {"icc": None, "n": len(pairs)}
    groups: dict[str, list[float]] = {}
    for v, L in pairs:
        groups.setdefault(L, []).append(v)
    k = len(groups)
    n_tot = len(pairs)
    grand = float(np.mean([v for v, _ in pairs]))
    ss_b = sum(len(g) * (np.mean(g) - grand) ** 2 for g in groups.values())
    ss_w = sum(sum((v - np.mean(g)) ** 2 for v in g) for g in groups.values())
    df_b, df_w = k - 1, n_tot - k
    if df_b <= 0 or df_w <= 0:
        return {"icc": None, "n": n_tot, "n_lineages": k,
                "note": "no within-lineage replication"}
    ms_b, ms_w = ss_b / df_b, ss_w / df_w
    n0 = (n_tot - sum(len(g) ** 2 for g in groups.values()) / n_tot) / (k - 1)
    var_b = max((ms_b - ms_w) / n0, 0.0)
    icc = var_b / (var_b + ms_w) if (var_b + ms_w) > 0 else None
    return {"icc": icc, "var_between_lineage": var_b, "var_within_lineage": float(ms_w),
            "ms_between": float(ms_b), "ms_within": float(ms_w),
            "n": n_tot, "n_lineages": k,
            "members_per_lineage": {L: len(g) for L, g in sorted(groups.items())},
            "mean_n0": float(n0)}


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage1")
    logger.info("STAGE 1 -- dual aggregation")
    s0 = jload(OUT / "stage0.json")
    rows = s0["panel_rows"]
    orient_by_col = s0["score_column_orientation"]
    unverified = s0["reproduction"]["status"] != "PASSED"

    table: dict = {}
    for cfg in CONFIGS:
        cfg_out: dict = {"config": cfg, "scores": {}}
        for col in SCORE_COLUMNS:
            sign = orient_by_col[col]
            xm, ym, lm, idm = member_level_vectors(rows, col, sign, cfg)
            xl, yl, ll, idl, lu = lineage_level_vectors(rows, col, sign, cfg)
            full = bool(cfg["primary"])
            entry = {
                "score": col, "orientation_sign": sign,
                "member_level": cell(xm, ym, lm, sign, "member", full=full),
                "lineage_level": cell(xl, yl, ll, sign, "lineage", full=full),
                "lineage_unit_detail": {
                    "n_units": lu["n_units"],
                    "members_per_unit": {u["lineage"]: u["n_members"]
                                         for u in lu["units"]},
                    "dropped_lineages": lu["dropped_lineages"],
                    "aggregation_function": lu["aggregation_function"],
                },
            }
            if full:
                # WHY THEY DIFFER: the mechanical decomposition
                icc_x = icc_one_way([r_ for r_ in _col_for(rows, col, sign, cfg)],
                                    [r["lineage"] for r in _sel(rows, cfg)])
                icc_y = icc_one_way([r[cfg["ycol"]] for r in _sel(rows, cfg)],
                                    [r["lineage"] for r in _sel(rows, cfg)])
                # reconciliation: member-level rho on lineage-mean-substituted values
                mean_x = {u["lineage"]: u["x"] for u in lu["units"]}
                mean_y = {u["lineage"]: u["y"] for u in lu["units"]}
                sub_x = [mean_x[L] for L in lm if L in mean_x]
                sub_y = [mean_y[L] for L in lm if L in mean_x]
                rec = sx.spearman_basic(sx.orient(sub_x, sign), sub_y)
                entry["why_they_differ"] = {
                    "n_member_level": entry["member_level"]["n"],
                    "n_lineage_level": entry["lineage_level"]["n"],
                    "n_reduction": entry["member_level"]["n"] - entry["lineage_level"]["n"],
                    "icc_score": icc_x, "icc_outcome": icc_y,
                    "reconciliation": {
                        "rho_member_level_on_lineage_mean_substituted_values": rec["rho"],
                        "rho_lineage_level": entry["lineage_level"]["rho_oriented"],
                        "agrees": (rec["rho"] is not None
                                   and entry["lineage_level"]["rho_oriented"] is not None
                                   and abs(rec["rho"]
                                           - entry["lineage_level"]["rho_oriented"]) < 1e-9),
                        "note": ("substituting every member's x and y by its lineage "
                                 "mean and recomputing at member level must reproduce "
                                 "the lineage-level rho up to the tie structure "
                                 "introduced by unequal lineage sizes"),
                    },
                    "rho_gap_lineage_minus_member": (
                        None if (entry["lineage_level"]["rho_oriented"] is None
                                 or entry["member_level"]["rho_oriented"] is None)
                        else entry["lineage_level"]["rho_oriented"]
                        - entry["member_level"]["rho_oriented"]),
                }
            cfg_out["scores"][col] = entry
        table[cfg["id"]] = cfg_out
        logger.info(f"config {cfg['id']} done")

    # ------------------------------------------------------------------
    # the oriented Delta at both levels, for both alpha_50 carriers
    # ------------------------------------------------------------------
    deltas: dict = {}
    for cfg in [c for c in CONFIGS if c["primary"]]:
        for a50 in (ALPHA50_ROW_COLUMN, ALPHA50_V2_COLUMN):
            sa, sb = orient_by_col[a50], orient_by_col[AMS_COLUMN]
            key = f"{cfg['id']}::{a50}_minus_{AMS_COLUMN}"
            sel = _sel(rows, cfg)
            xa = column_values(sel, a50, sa, cfg["convention"])
            xb = column_values(sel, AMS_COLUMN, sb, cfg["convention"])
            yy = [r[cfg["ycol"]] for r in sel]
            ll = [r["lineage"] for r in sel]
            mem = paired_delta(xa, xb, yy, ll, sa, sb, "member")

            ua = lineage_units(rows, a50, ycol=cfg["ycol"],
                               reliable_only=cfg["reliable_only"], orientation=sa,
                               convention=cfg["convention"])
            ub = lineage_units(rows, AMS_COLUMN, ycol=cfg["ycol"],
                               reliable_only=cfg["reliable_only"], orientation=sb,
                               convention=cfg["convention"])
            common = [u["lineage"] for u in ua["units"]
                      if u["lineage"] in {v["lineage"] for v in ub["units"]}]
            mxa = {u["lineage"]: u["x"] for u in ua["units"]}
            mxb = {u["lineage"]: u["x"] for u in ub["units"]}
            myy = {u["lineage"]: u["y"] for u in ub["units"]}
            lin_d = paired_delta([mxa[L] for L in common], [mxb[L] for L in common],
                                 [myy[L] for L in common], common, sa, sb, "lineage")

            sign_survives = "SIGN_SURVIVES"
            if mem.get("delta") is None or lin_d.get("delta") is None:
                sign_survives = "UNDETERMINED_DELTA_UNDEFINED"
            elif np.sign(mem["delta"]) != np.sign(lin_d["delta"]):
                sign_survives = "SIGN_FLIPS"

            def _excl(d):
                c = d.get("ci95")
                return bool(c and (c[0] > 0 or c[1] < 0))
            em, el = _excl(mem), _excl(lin_d)
            ci_verdict = ("EXCLUSION_SURVIVES" if (em and el)
                          else "EXCLUSION_LOST_AT_MEMBER_LEVEL" if (el and not em)
                          else "EXCLUSION_LOST_AT_LINEAGE_LEVEL" if (em and not el)
                          else "EXCLUDES_AT_NEITHER")
            deltas[key] = {
                "config": cfg["id"], "alpha_50_carrier": a50, "reference": AMS_COLUMN,
                "member_level": mem, "lineage_level": lin_d,
                "sign_survives_unit_choice": sign_survives,
                "ci_exclusion_survives_unit_choice": ci_verdict,
                "auc_pair": {
                    "member_level": {
                        a50: table[cfg["id"]]["scores"][a50]["member_level"]
                        .get("auc_y_above_median", {}).get("auc"),
                        AMS_COLUMN: table[cfg["id"]]["scores"][AMS_COLUMN]["member_level"]
                        .get("auc_y_above_median", {}).get("auc")},
                    "lineage_level": {
                        a50: table[cfg["id"]]["scores"][a50]["lineage_level"]
                        .get("auc_y_above_median", {}).get("auc"),
                        AMS_COLUMN: table[cfg["id"]]["scores"][AMS_COLUMN]["lineage_level"]
                        .get("auc_y_above_median", {}).get("auc")},
                },
            }
            logger.info(f"delta {key}: member {mem.get('delta')} "
                        f"lineage {lin_d.get('delta')} -> {sign_survives} / {ci_verdict}")

    # ------------------------------------------------------------------
    # the headline our-AMS discrepancy the draft ships
    # ------------------------------------------------------------------
    p_mem = table["all19_drop_undefined_yE3"]["scores"][AMS_COLUMN]["member_level"]
    p_lin = table["reliable14_rank_bottom_yV2"]["scores"][AMS_COLUMN]["lineage_level"]
    headline = {
        "draft_section_5_2_value": 0.3578030619574787,
        "draft_section_5_3_value": 0.8214285714285715,
        "same_statistic": ("oriented Spearman of our-AMS sigma against the judged "
                           "plain-harmful refusal rate"),
        "recomputed_member_level": p_mem["rho_oriented"],
        "recomputed_lineage_level": p_lin["rho_oriented"],
        "gap_in_rho": p_lin["rho_oriented"] - p_mem["rho_oriented"],
        "n_member_level": p_mem["n"], "n_lineage_level": p_lin["n"],
        "verdict": "SAME_STATISTIC_TWO_UNITS_BOTH_CORRECT_NEITHER_LABELLED",
        "why": ("the two values are estimands of different quantities: lineage "
                "aggregation averages within-lineage members, removes the "
                "within-lineage variance entirely and reduces n from 19 to 7. "
                "They are not a contradiction, but a paper arguing that analysis "
                "choices swing conclusions must name the unit at every "
                "correlation, and the current draft names it at neither."),
        "gap_is_larger_than_the_effect_argued_about": True,
    }

    # how much does the UNIT choice alone move things, across all 8 score columns?
    swing = []
    for cfg in [c for c in CONFIGS if c["primary"]]:
        for col in SCORE_COLUMNS:
            e = table[cfg["id"]]["scores"][col]
            rm = e["member_level"]["rho_oriented"]
            rl = e["lineage_level"]["rho_oriented"]
            if rm is None or rl is None:
                continue
            swing.append({"config": cfg["id"], "score": col,
                          "rho_member": rm, "rho_lineage": rl,
                          "abs_change": abs(rl - rm),
                          "sign_flips": bool(np.sign(rm) != np.sign(rl)
                                             and abs(rm) > 1e-12 and abs(rl) > 1e-12)})
    swing.sort(key=lambda r: -r["abs_change"])
    headline["unit_swing_summary"] = {
        "n_score_x_config_cells": len(swing),
        "n_cells_whose_sign_flips_with_the_unit": sum(1 for r in swing if r["sign_flips"]),
        "max_abs_change_in_rho": swing[0]["abs_change"] if swing else None,
        "max_abs_change_cell": swing[0] if swing else None,
        "median_abs_change_in_rho": float(np.median([r["abs_change"] for r in swing]))
        if swing else None,
        "all_cells": swing,
        "reading": ("changing nothing but the aggregation unit -- same members, "
                    "same outcome, same estimator -- moves the oriented "
                    "correlation by this much. That is the paper's own thesis "
                    "measured on the paper's own numbers."),
    }

    out = {"stage": "stage1_dual_aggregation",
           "provenance_unverified": bool(unverified),
           "boot_seed": sx.BOOT_SEED, "n_boot": N_BOOT,
           "configs": CONFIGS, "table": table, "deltas": deltas,
           "headline_discrepancy": headline,
           "methodological_note": _method_note(table, headline)}
    jdump(out, OUT / "stage1_dual_aggregation.json")
    logger.info(f"wrote {OUT / 'stage1_dual_aggregation.json'}")
    return out


def _sel(rows, cfg):
    return [r for r in rows if not (cfg["reliable_only"] and r["unreliable"])]


def _col_for(rows, col, sign, cfg):
    return column_values(_sel(rows, cfg), col, sign, cfg["convention"])


def _method_note(table, headline) -> str:
    ams = table["all19_drop_undefined_yE3"]["scores"]["ams_sigma"]
    icc = ams["why_they_differ"]["icc_score"]
    iccy = ams["why_they_differ"]["icc_outcome"]
    return (
        f"Lineage aggregation replaces each lineage's members by their mean, which "
        f"removes the within-lineage variance and reduces n from "
        f"{headline['n_member_level']} members to {headline['n_lineage_level']} "
        f"lineage units. For our-AMS sigma the intraclass correlation is "
        f"{icc['icc']:.3f} (between-lineage variance {icc['var_between_lineage']:.4f} "
        f"against within-lineage {icc['var_within_lineage']:.4f}); for the judged "
        f"outcome it is {iccy['icc']:.3f}. The member-level and lineage-level "
        f"correlations are therefore estimands of different quantities rather than "
        f"a contradiction: the first asks whether a checkpoint's score tracks that "
        f"checkpoint's behaviour, the second whether a lineage's average score "
        f"tracks that lineage's average behaviour. The unequal lineage sizes "
        f"({icc['members_per_lineage']}) are also why only the identity permutation "
        f"is guaranteed to reproduce |rho|, so the exhaustive floor is 1/5040 and "
        f"not 2/5040. A paper whose thesis is that analysis choices swing "
        f"conclusions must name the unit at every correlation it reports.")


if __name__ == "__main__":
    main()
