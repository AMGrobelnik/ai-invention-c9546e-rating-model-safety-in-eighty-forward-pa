#!/usr/bin/env python3
"""STAGE 2 -- THE THRESHOLD SENSITIVITY SURFACE (H-T).

`PROTOCOL_DOES_NOT_DISCRIMINATE` is currently a step function of five arbitrary
cutoffs. The five per-check statistics were computed in E3 and are NOT
re-estimated here; only the thresholds move, so the whole surface is cheap
enumeration over a 164,736-point full factorial.

Two rule variants are evaluated at every grid point:
  FULL_PREREGISTERED  -- the threshold clause AND the archived secondary clause
                         (check 1's "zero members change verdict class", check
                         2's in-grid / interiority guard). This is the rule as
                         written in prereg_iter3.json.
  THRESHOLD_ONLY      -- the numeric clause alone, with the secondary clauses
                         dropped. This is where the surface actually varies, and
                         it is reported because a reader is entitled to know
                         whether the negative result is manufactured by a cutoff
                         or by a clause the cutoff cannot reach.
"""

from __future__ import annotations

import itertools

import numpy as np
from loguru import logger

from common import CHECKS, MATRIX_ROWS, OUT, jdump, jload, setup_logging

# --------------------------------------------------------------------------
# The grid, verbatim from the artifact plan
# --------------------------------------------------------------------------
GRID = {
    "check1_lexical": np.round(np.arange(0.60, 0.9501, 0.05), 4),
    "check2_monotonicity": np.round(np.arange(0.60, 0.9501, 0.05), 4),
    "check3_layer": np.round(np.arange(1.50, 4.001, 0.25), 4),
    "check4_spread": np.round(np.arange(0.20, 0.8001, 0.05), 4),
    "check4_sign_required": np.array([True, False]),
    "check5_scorer": np.round(np.arange(0.40, 0.8001, 0.05), 4),
}
PREREG = {"check1_lexical": 0.70, "check2_monotonicity": 0.80, "check3_layer": 2.0,
          "check4_spread": 0.40, "check4_sign_required": True, "check5_scorer": 0.60}


def extract_statistics(matrix: dict) -> dict:
    """Pull the five FIXED per-check decision statistics out of E3's matrix."""
    st: dict = {}
    for row in MATRIX_ROWS:
        m = matrix[row]
        c1, c2, c3, c4, c5 = (m[c] for c in CHECKS)
        # check 3: the rule is PASS iff BOTH median span factors are below the
        # threshold, so the decision statistic is their maximum. alpha_50's row
        # leads with the NON-PARAMETRIC span, as pre-registered.
        if row == "alpha_50":
            spans = [c3["span_band_primary_nonparametric"], c3["span_l2_nonparametric"]]
            span_note = ("non-parametric span led, as pre-registered; the logistic "
                         f"spans are {c3['span_band_logistic']:.3f} / "
                         f"{c3['span_l2_logistic']:.3f}")
        else:
            spans = [c3["median_span_band"], c3["median_span_l2"]]
            span_note = "median span over the 40-80% band and over L+/-2"
        st[row] = {
            "check1_lexical": {
                "statistic": c1.get("rho", c1.get("rho_refit_vs_original")),
                "statistic_name": "Spearman(refit score, original score)",
                "secondary_clause_ok": (
                    (c1.get("verdict_class_changes", c1.get("sign_flips", 0)) or 0) == 0),
                "secondary_clause": "zero members change verdict class",
                "verdict_class_changes": c1.get("verdict_class_changes",
                                                c1.get("sign_flips")),
                "archived_verdict": c1["verdict"],
                "statistic_undefined_reason": c1.get("rho_undefined_reason"),
            },
            "check2_monotonicity": {
                "statistic": c2["fraction_monotone"],
                "statistic_name": "fraction of members monotone in the pre-registered direction",
                "secondary_clause_ok": (
                    (c2.get("n_operating_point_on_descending_branch",
                            c2.get("n_inverted_U", 0)) or 0) == 0),
                "secondary_clause": ("the operating point is never read off a "
                                     "descending branch beyond an interior optimum"),
                "n_violating": c2.get("n_operating_point_on_descending_branch",
                                      c2.get("n_inverted_U")),
                "archived_verdict": c2["verdict"],
            },
            "check3_layer": {
                "statistic": float(max(spans)),
                "statistic_name": "max of the two median span factors (PASS iff < threshold)",
                "secondary_clause_ok": True, "secondary_clause": None,
                "spans": [float(s) for s in spans], "span_note": span_note,
                "archived_verdict": c3["verdict"],
            },
            "check4_jackknife": {
                "statistic": c4["spread"],
                "statistic_name": "leave-one-lineage-out rho spread (PASS iff < threshold)",
                "sign_stable": bool(c4["sign_stable"]),
                "secondary_clause_ok": True, "secondary_clause": None,
                "archived_verdict": c4["verdict"],
            },
            "check5_scorer": {
                "statistic": 0.3907,
                "statistic_name": "one-vs-rest REFUSAL Cohen kappa (SHARED across rows)",
                "secondary_clause_ok": True, "secondary_clause": None,
                "archived_verdict": c5["verdict"],
                "shared_bound": True,
            },
        }
    return st


def cell_pass(row_st: dict, check: str, thr, sign_required=None,
              rule: str = "FULL_PREREGISTERED") -> bool:
    c = row_st[check]
    s = c["statistic"]
    if check == "check3_layer":
        num = (s is not None) and (s < thr)
    elif check == "check4_jackknife":
        num = (s is not None) and (s < thr)
        if sign_required:
            num = num and c["sign_stable"]
    else:
        num = (s is not None) and (s >= thr)
    if rule == "THRESHOLD_ONLY":
        return bool(num)
    return bool(num and c["secondary_clause_ok"])


def verdicts_from_counts(counts: np.ndarray, required: int) -> tuple:
    """counts: (..., 4) pass counts in MATRIX_ROWS order."""
    a = counts[..., 0]
    rivals = counts[..., 1:]
    best = rivals.max(axis=-1)
    discriminates = (best >= required) & (a <= 2)
    degenerate = discriminates & (best <= a)
    return discriminates, degenerate, best, a


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage2")
    logger.info("STAGE 2 -- threshold sensitivity surface")
    s0 = jload(OUT / "stage0.json")
    st = extract_statistics(s0["archived_matrix"])

    # sanity: the surface must reproduce the archived 4x5 matrix at the
    # pre-registered thresholds under the FULL rule
    repro = {}
    for row in MATRIX_ROWS:
        for check in CHECKS:
            thr = PREREG[{"check4_jackknife": "check4_spread"}.get(check, check)]
            got = cell_pass(st[row], check, thr,
                            sign_required=PREREG["check4_sign_required"])
            arch = st[row][check]["archived_verdict"] == "PASS"
            repro[f"{row}::{check}"] = {"recomputed": bool(got), "archived": bool(arch),
                                        "match": bool(got == arch)}
    n_mismatch = sum(1 for v in repro.values() if not v["match"])
    if n_mismatch:
        logger.error(f"matrix reproduction mismatch on {n_mismatch} cells")
    logger.info(f"matrix reproduced at the pre-registered thresholds: "
                f"{len(repro) - n_mismatch}/{len(repro)} cells")

    axes = ["check1_lexical", "check2_monotonicity", "check3_layer",
            "check4_jackknife", "check5_scorer"]
    t1, t2, t3 = GRID["check1_lexical"], GRID["check2_monotonicity"], GRID["check3_layer"]
    t4s, t4b = GRID["check4_spread"], GRID["check4_sign_required"]
    t5 = GRID["check5_scorer"]
    n_points = len(t1) * len(t2) * len(t3) * len(t4s) * len(t4b) * len(t5)
    logger.info(f"grid: {len(t1)}x{len(t2)}x{len(t3)}x{len(t4s)}x{len(t4b)}x{len(t5)}"
                f" = {n_points} points")

    surfaces: dict = {}
    for rule in ("FULL_PREREGISTERED", "THRESHOLD_ONLY"):
        # per-check boolean vectors, one axis at a time
        b1 = np.array([[cell_pass(st[r], "check1_lexical", v, rule=rule) for v in t1]
                       for r in MATRIX_ROWS])                       # (4, 8)
        b2 = np.array([[cell_pass(st[r], "check2_monotonicity", v, rule=rule) for v in t2]
                       for r in MATRIX_ROWS])                       # (4, 8)
        b3 = np.array([[cell_pass(st[r], "check3_layer", v, rule=rule) for v in t3]
                       for r in MATRIX_ROWS])                       # (4, 11)
        b4 = np.array([[[cell_pass(st[r], "check4_jackknife", v, sign_required=bool(sb),
                                   rule=rule) for sb in t4b] for v in t4s]
                       for r in MATRIX_ROWS])                       # (4, 13, 2)
        b5 = np.array([[cell_pass(st[r], "check5_scorer", v, rule=rule) for v in t5]
                       for r in MATRIX_ROWS])                       # (4, 9)

        # broadcast to (t1, t2, t3, t4s, t4b, t5, 4)
        C = (b1.T[:, None, None, None, None, None, :].astype(np.int8)
             + b2.T[None, :, None, None, None, None, :]
             + b3.T[None, None, :, None, None, None, :]
             + np.transpose(b4, (1, 2, 0))[None, None, None, :, :, None, :]
             + b5.T[None, None, None, None, None, :, :])
        assert C.shape[-1] == 4 and C.size // 4 == n_points, C.shape
        C14 = (b1.T[:, None, None, None, None, None, :].astype(np.int8)
               + b2.T[None, :, None, None, None, None, :]
               + b3.T[None, None, :, None, None, None, :]
               + np.transpose(b4, (1, 2, 0))[None, None, None, :, :, None, :]
               + np.zeros((1, 1, 1, 1, 1, len(t5), 1), dtype=np.int8))

        rule_out: dict = {"rule": rule, "n_grid_points": int(n_points), "by_required": {}}
        for required in (2, 3, 4, 5):
            disc, degen, best, a = verdicts_from_counts(C, required)
            nd = int(disc.sum())
            rule_out["by_required"][str(required)] = {
                "n_DISCRIMINATES": nd,
                "n_PROTOCOL_DOES_NOT_DISCRIMINATE": int(n_points - nd),
                "fraction_PROTOCOL_DOES_NOT_DISCRIMINATE": float((n_points - nd) / n_points),
                "n_DISCRIMINATES_that_are_degenerate_ties": int(degen.sum()),
                "n_DISCRIMINATES_non_degenerate": int((disc & ~degen).sum()),
            }
        # checks-1-4-only sensitivity (check 5 dropped entirely)
        rule_out["checks_1_to_4_only"] = {}
        for required in (2, 3, 4):
            disc, degen, best, a = verdicts_from_counts(C14, required)
            nd = int(disc.sum())
            rule_out["checks_1_to_4_only"][str(required)] = {
                "n_DISCRIMINATES": nd,
                "fraction_PROTOCOL_DOES_NOT_DISCRIMINATE": float((n_points - nd) / n_points),
                "n_DISCRIMINATES_that_are_degenerate_ties": int(degen.sum()),
            }
        # the plan's strict criterion: a rival must STRICTLY exceed alpha_50
        best_all = C[..., 1:].max(axis=-1)
        strict = best_all > C[..., 0]
        rule_out["strict_exceed_criterion"] = {
            "definition": ("DISCRIMINATES iff some rival's pass count STRICTLY "
                           "exceeds alpha_50's; no tie counts as separation"),
            "n_DISCRIMINATES": int(strict.sum()),
            "fraction_PROTOCOL_DOES_NOT_DISCRIMINATE":
                float((n_points - int(strict.sum())) / n_points),
        }
        # which rival wins, wherever anything wins
        winners: dict = {}
        if strict.any():
            wi = C[..., 1:].argmax(axis=-1)[strict]
            for k, name in enumerate(MATRIX_ROWS[1:]):
                winners[name] = int((wi == k).sum())
        rule_out["strict_exceed_criterion"]["winner_counts"] = winners

        # KAPPA-AXIS INVARIANCE, verified empirically over the whole grid
        var_over_kappa = C.std(axis=5).max()
        diff_invariant = bool(np.all(
            (C[..., 1:] - C[..., :1]).std(axis=5) < 1e-12))
        rule_out["check5_kappa_axis_invariance"] = {
            "claim": ("check 5 is a property of the SHARED scorer and takes the "
                      "same value in every row, so moving its threshold shifts "
                      "all four pass counts together and can never change any "
                      "comparison between rows"),
            "pass_count_varies_over_kappa_axis": bool(var_over_kappa > 0),
            "pairwise_differences_invariant_over_kappa_axis": diff_invariant,
            "kappa_statistic": 0.3907,
            "grid_min_threshold": float(t5.min()),
            "proved": ("the kappa statistic 0.3907 sits BELOW the entire swept "
                       "range [0.40, 0.80], so check 5 also FAILS at every grid "
                       "point in every row; the invariance is both proved "
                       "structurally and verified empirically"),
            "n_grid_points_where_check5_passes_any_row":
                int(np.array([[cell_pass(st[r], "check5_scorer", v, rule=rule)
                               for v in t5] for r in MATRIX_ROWS]).sum()),
        }
        surfaces[rule] = rule_out
        logger.info(f"{rule}: DOES_NOT_DISCRIMINATE fraction at required=3 = "
                    f"{rule_out['by_required']['3']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f}"
                    f"; strict-exceed fraction = "
                    f"{rule_out['strict_exceed_criterion']['fraction_PROTOCOL_DOES_NOT_DISCRIMINATE']:.6f}")

    # ------------------------------------------------------------------
    # MARGINAL FLIP TABLE: one row per check per score
    # ------------------------------------------------------------------
    flips = []
    axis_of = {"check1_lexical": "check1_lexical",
               "check2_monotonicity": "check2_monotonicity",
               "check3_layer": "check3_layer",
               "check4_jackknife": "check4_spread",
               "check5_scorer": "check5_scorer"}
    for rule in ("FULL_PREREGISTERED", "THRESHOLD_ONLY"):
        for row in MATRIX_ROWS:
            for check in CHECKS:
                vals = GRID[axis_of[check]]
                res = [cell_pass(st[row], check, v,
                                 sign_required=PREREG["check4_sign_required"], rule=rule)
                       for v in vals]
                thr0 = PREREG[axis_of[check]]
                at_prereg = cell_pass(st[row], check, thr0,
                                      sign_required=PREREG["check4_sign_required"],
                                      rule=rule)
                boundary = None
                for i in range(1, len(vals)):
                    if res[i] != res[i - 1]:
                        boundary = {"between": [float(vals[i - 1]), float(vals[i])],
                                    "verdict_below": "PASS" if res[i - 1] else "FAIL",
                                    "verdict_above": "PASS" if res[i] else "FAIL"}
                        break
                flips.append({
                    "rule": rule, "score": row, "check": check,
                    "statistic": st[row][check]["statistic"],
                    "statistic_name": st[row][check]["statistic_name"],
                    "preregistered_threshold": thr0,
                    "verdict_at_preregistered_threshold": "PASS" if at_prereg else "FAIL",
                    "swept_range": [float(vals.min()), float(vals.max())]
                    if vals.dtype != bool else [False, True],
                    "flips_within_swept_range": boundary is not None,
                    "flip_boundary": boundary,
                    "secondary_clause_ok": st[row][check]["secondary_clause_ok"],
                    "secondary_clause": st[row][check]["secondary_clause"],
                    "note": (None if boundary is not None else
                             ("the cell never flips anywhere in the swept range"
                              + ("" if rule == "THRESHOLD_ONLY" or
                                 st[row][check]["secondary_clause_ok"]
                                 else "; under the pre-registered rule the "
                                      "secondary clause already fails, so no "
                                      "threshold on this axis can make it PASS"))),
                })

    # the named check-1 case
    c1_case = {
        "question": ("check 1 FAILS all four scores at 0.70 while our-AMS's "
                     "statistic sits at 0.833 and both logit-gap variants at "
                     "0.967-0.977. Which threshold band flips which rows?"),
        "answer_threshold_only": {
            r: {"statistic": st[r]["check1_lexical"]["statistic"],
                "passes_at_thresholds": [float(v) for v in GRID["check1_lexical"]
                                         if cell_pass(st[r], "check1_lexical", v,
                                                      rule="THRESHOLD_ONLY")]}
            for r in MATRIX_ROWS},
        "answer_full_rule": (
            "under the pre-registered rule NO threshold flips any row, because "
            "the second clause -- zero members change verdict class -- already "
            "fails in every row (alpha_50 3 of 5, our-AMS 6 of 19, logit-gap "
            "benign 1 of 19, logit-gap harmful 1 of 19). The check-1 threshold "
            "is therefore not what produced the negative result on this check."),
    }

    # minimal threshold changes that would flip the overall verdict
    minimal = _minimal_flips(st, surfaces)

    out = {
        "stage": "stage2_threshold_surface",
        "grid": {k: (v.tolist() if v.dtype != bool else [bool(x) for x in v])
                 for k, v in GRID.items()},
        "n_grid_points": int(n_points),
        "preregistered_thresholds": PREREG,
        "fixed_per_check_statistics": st,
        "matrix_reproduction_at_preregistered_thresholds": {
            "n_cells": len(repro), "n_mismatch": n_mismatch, "cells": repro},
        "surfaces": surfaces,
        "marginal_flip_table": flips,
        "check1_named_case": c1_case,
        "minimal_verdict_flipping_changes": minimal,
        "cost_usd": 0.0,
    }
    jdump(out, OUT / "stage2_threshold_surface.json")
    logger.info(f"wrote {OUT / 'stage2_threshold_surface.json'}")
    return out


def _minimal_flips(st: dict, surfaces: dict) -> dict:
    """Enumerate the SINGLE-axis changes from the pre-registered point that
    flip the overall verdict, and say which score becomes the winner."""
    axis_of = {"check1_lexical": "check1_lexical",
               "check2_monotonicity": "check2_monotonicity",
               "check3_layer": "check3_layer",
               "check4_jackknife": "check4_spread",
               "check5_scorer": "check5_scorer"}
    res: dict = {}
    for rule in ("FULL_PREREGISTERED", "THRESHOLD_ONLY"):
        found = []
        for check in CHECKS:
            for v in GRID[axis_of[check]]:
                thr = {axis_of[c]: PREREG[axis_of[c]] for c in CHECKS}
                thr[axis_of[check]] = float(v)
                counts = []
                for row in MATRIX_ROWS:
                    n = 0
                    for c in CHECKS:
                        n += int(cell_pass(st[row], c, thr[axis_of[c]],
                                           sign_required=PREREG["check4_sign_required"],
                                           rule=rule))
                    counts.append(n)
                a, rivals = counts[0], counts[1:]
                best = max(rivals)
                if best > a:
                    found.append({
                        "check": check, "threshold_value": float(v),
                        "preregistered_value": PREREG[axis_of[check]],
                        "pass_counts": dict(zip(MATRIX_ROWS, counts)),
                        "winning_score": MATRIX_ROWS[1 + int(np.argmax(rivals))],
                        "new_verdict": "PROTOCOL_DISCRIMINATES",
                    })
        res[rule] = {
            "n_single_axis_changes_that_flip_the_verdict": len(found),
            "changes": found,
            "verdict": ("VERDICT_STABLE_TO_EVERY_SINGLE_AXIS_THRESHOLD_CHANGE"
                        if not found else "VERDICT_FLIPS_ON_AT_LEAST_ONE_AXIS"),
            "criterion": "some rival's pass count STRICTLY exceeds alpha_50's",
        }
    return res


if __name__ == "__main__":
    main()
