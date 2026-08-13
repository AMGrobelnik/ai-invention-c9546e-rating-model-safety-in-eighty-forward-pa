#!/usr/bin/env python3
"""STAGE 2 -- ANALYSIS 1 (H-C): the read-act coupling WITHOUT the axis-type contrast.

The shipped positive is rho = 0.629 over 70 (member, axis) pairs. Axis A is
strong in both roles by construction and axes C/D are null in both roles by
construction, so pooling axes measures the difference between a fitted axis and
a random one, not a relationship between induction and reading among MODELS.
This stage replaces the pooled figure with the within-axis one, and -- rather
than merely conceding the confound -- measures how much of 0.629 it supplies.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from loguru import logger
from scipy.stats import rankdata, spearmanr

from common5 import (AXES, AXIS_SHORT, OUT, R4, corr_block, dual_unit, jdump,
                     jload, rank_bottom, setup_logging)

PRIMARY_AXIS = "A_canned"


# --------------------------------------------------------------------------
def load_points() -> list[dict]:
    return jload(R4 / "method_out.json")["metadata"]["results"]["joint_scatter_points"]


def axis_rows(points: list[dict], axis: str) -> list[dict]:
    return [{"checkpoint": p["checkpoint"], "lineage_id": p["lineage_id"],
             "x": p["max_refusal_rate"], "y": p["detection_auroc"],
             "c_50": p["c_50"],
             "neg_log10_c50": p["neg_log10_c50"],
             "y_norm_controlled": p.get("detection_auroc_norm_controlled"),
             "detection_verdict": p["detection_verdict"]}
            for p in points if p["axis"] == axis]


# --------------------------------------------------------------------------
# (a) PRIMARY -- within axis A, across members
# --------------------------------------------------------------------------
def reviewer_reproduction(rows: list[dict]) -> dict:
    """The reviewer's recompute gives rho = 0.434, p = 0.14 over THIRTEEN
    members. Reproducing that is itself a required leg: compute n=14, then every
    leave-one-out n=13 subset, and name the exclusion rule that reproduces it."""
    x = np.array([r["x"] for r in rows], float)
    y = np.array([r["y"] for r in rows], float)
    names = [r["checkpoint"] for r in rows]
    full_rho, full_p = spearmanr(x, y)
    subsets = []
    for i, nm in enumerate(names):
        keep = [j for j in range(len(names)) if j != i]
        rr, pp = spearmanr(x[keep], y[keep])
        subsets.append({
            "dropped": nm, "n": len(keep), "rho": float(rr), "p_asymptotic": float(pp),
            "matches_0p434_to_2dp": bool(round(float(rr), 2) == 0.43),
            "matches_p_0p14_to_2dp": bool(round(float(pp), 2) == 0.14),
            "dropped_was_AMBIGUOUS": rows[i]["detection_verdict"] == "AMBIGUOUS",
            "dropped_had_censored_c50": rows[i]["c_50"] is None,
        })
    both = [s for s in subsets if s["matches_0p434_to_2dp"]
            and s["matches_p_0p14_to_2dp"]]
    rho_only = [s for s in subsets if s["matches_0p434_to_2dp"]]
    best = min(subsets, key=lambda s: abs(s["rho"] - 0.434))
    ident = None
    if both:
        d = both[0]
        rules = []
        if d["dropped_was_AMBIGUOUS"]:
            rules.append("drop the member whose axis-A verdict is AMBIGUOUS")
        if d["dropped_had_censored_c50"]:
            rules.append("drop a member whose axis-A c_50 is censored")
        ident = {"dropped_member": d["dropped"], "rho": d["rho"],
                 "p_asymptotic": d["p_asymptotic"],
                 "candidate_rules": rules or ["no principled rule identified"],
                 "n_subsets_matching": len(both)}
    return {
        "target_rho": 0.434, "target_p": 0.14, "target_n": 13,
        "n14": {"n": len(names), "rho": float(full_rho),
                "p_asymptotic": float(full_p)},
        "loo_subsets": subsets,
        "n_subsets_matching_rho": len(rho_only),
        "n_subsets_matching_rho_and_p": len(both),
        "identified_rule": ident,
        "closest_n13": best,
        "reproduced": bool(both),
        "statement": (
            (f"REPRODUCED: dropping {ident['dropped_member']} leaves 13 members "
             f"with rho = {ident['rho']:.3f}, p = {ident['p_asymptotic']:.2f}, "
             f"matching the reviewer's 0.434 / 0.14. Identifying rule: "
             f"{'; '.join(ident['candidate_rules'])}.")
            if ident else
            (f"NOT REPRODUCED to two decimals by any single-member exclusion. The "
             f"closest 13-member subset drops {best['dropped']} and gives rho = "
             f"{best['rho']:.3f}, p = {best['p_asymptotic']:.3f}, a discrepancy of "
             f"{abs(best['rho'] - 0.434):.3f} in rho against the reviewer's 0.434. "
             f"Over all 14 members the estimate is rho = {full_rho:.3f}, p = "
             f"{full_p:.3f}. Both are reported; neither is smoothed toward the "
             f"other.")),
    }


# --------------------------------------------------------------------------
# (b) SECONDARY -- x = -log10(c_50) with the rank_bottom censoring sentinel
# --------------------------------------------------------------------------
def secondary_c50(rows: list[dict]) -> dict:
    cen = np.array([r["c_50"] is None for r in rows], bool)
    raw = np.array([r["neg_log10_c50"] if r["neg_log10_c50"] is not None else np.nan
                    for r in rows], float)
    xr = rank_bottom(raw, cen)
    y = [r["y"] for r in rows]
    lin = [r["lineage_id"] for r in rows]
    sentinel = corr_block(xr, y, lin,
                          label="within-axis-A, x = -log10(c_50) with rank_bottom "
                                "sentinel for censored members [member unit]")
    keep = ~cen
    dropped = corr_block(raw[keep], np.array(y, float)[keep],
                         [l for l, k in zip(lin, keep) if k],
                         label="within-axis-A, x = -log10(c_50), censored members "
                               "DROPPED (the archived convention) [member unit]")
    lin_rows = [{"lineage_id": r["lineage_id"], "x": float(v), "y": r["y"]}
                for r, v in zip(rows, xr)]
    lin_unit = dual_unit(lin_rows, "x", "y",
                         "within-axis-A, rank_bottom c_50")["lineage"]
    return {
        "n_members": len(rows),
        "n_censored": int(cen.sum()),
        "censoring_fraction": float(cen.mean()),
        "censored_members": [r["checkpoint"] for r, c in zip(rows, cen) if c],
        "sentinel_convention": ("censored c_50 is a member whose axis-A steering "
                                "NEVER drove the refusal rate to one half; it is "
                                "given a single tied sentinel rank strictly BELOW "
                                "every uncensored member, never dropped and never "
                                "imputed to a finite number"),
        "member": sentinel, "lineage": lin_unit,
        "archived_convention_drop_censored": dropped,
    }


# --------------------------------------------------------------------------
# (c)+(d) per-axis and the control ladder
# --------------------------------------------------------------------------
def per_axis(points: list[dict]) -> dict:
    out = {}
    for ax in AXES:
        rows = axis_rows(points, ax)
        out[ax] = dual_unit(rows, "x", "y",
                            f"within-axis-{AXIS_SHORT[ax]} across members")
        out[ax]["n_members"] = len(rows)
        out[ax]["short"] = AXIS_SHORT[ax]
        out[ax]["by_construction"] = (
            "fitted refusal axis (expected strong in both roles)"
            if ax in ("A_canned", "B_paraphrase", "E_prompt_contrast")
            else "control axis (expected null in both roles by construction)")
    return out


def control_ladder(points: list[dict]) -> list[dict]:
    subsets = [
        ("all 5 axes (the shipped pooled statistic)", AXES),
        ("minus D (norm-matched random)", [a for a in AXES if a != "D_random0"]),
        ("minus C (stylistic)", [a for a in AXES if a != "C_stylistic"]),
        ("minus C and D (both by-construction controls)",
         [a for a in AXES if a not in ("C_stylistic", "D_random0")]),
        ("A + B + E only (fitted refusal axes)",
         ["A_canned", "B_paraphrase", "E_prompt_contrast"]),
    ]
    ladder = []
    for label, axs in subsets:
        rows = [{"checkpoint": p["checkpoint"], "lineage_id": p["lineage_id"],
                 "x": p["max_refusal_rate"], "y": p["detection_auroc"]}
                for p in points if p["axis"] in axs]
        du = dual_unit(rows, "x", "y", f"pooled, {label}")
        du["subset"] = label
        du["axes"] = axs
        du["n_pairs"] = len(rows)
        ladder.append(du)
    return ladder


# --------------------------------------------------------------------------
# (e) NAME THE CONFOUND
# --------------------------------------------------------------------------
def _residualise(v: np.ndarray, groups: np.ndarray) -> np.ndarray:
    out = v.astype(float).copy()
    for g in np.unique(groups):
        m = groups == g
        out[m] -= out[m].mean()
    return out


def confound(points: list[dict]) -> dict:
    x = np.array([p["max_refusal_rate"] for p in points], float)
    y = np.array([p["detection_auroc"] for p in points], float)
    ax = np.array([p["axis"] for p in points])
    mb = np.array([p["checkpoint"] for p in points])
    lin = [p["lineage_id"] for p in points]
    rx, ry = rankdata(x), rankdata(y)

    res = {}
    # (i) partial Spearman controlling for AXIS identity
    a_x, a_y = _residualise(rx, ax), _residualise(ry, ax)
    res["partial_controlling_axis"] = corr_block(
        a_x, a_y, lin, label="rank-residualised partial Spearman, axis identity "
                             "partialled out [pair level, lineage-clustered CI]")
    # (ii) partial Spearman controlling for MEMBER identity
    m_x, m_y = _residualise(rx, mb), _residualise(ry, mb)
    res["partial_controlling_member"] = corr_block(
        m_x, m_y, lin, label="rank-residualised partial Spearman, member identity "
                             "partialled out [pair level, lineage-clustered CI]")

    # (iii) mixed-effects model on the ranked variables
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    df = pd.DataFrame({"ry": ry, "rx": rx, "axis": ax, "member": mb,
                       "lineage": lin})
    fit, attempts = None, []
    for kw in ({"reml": True, "method": "lbfgs"},
               {"reml": False, "method": "lbfgs"},
               {"reml": True, "method": "powell"},
               {"reml": True, "method": "cg"}):
        try:
            fit = smf.mixedlm("ry ~ rx + C(axis)", df,
                              groups=df["member"]).fit(**kw)
            _ = fit.conf_int().loc["rx"]      # forces the singular-matrix failure
            attempts.append({"kwargs": kw, "outcome": "converged"})
            break
        except Exception as exc:
            attempts.append({"kwargs": kw, "outcome": f"FAILED: {exc!r}"})
            logger.warning(f"MixedLM {kw} failed: {exc!r}")
            fit = None
    if fit is not None:
        res["mixedlm"] = {
            "used": "statsmodels.MixedLM (ranks; axis fixed effect, member random "
                    "intercept)",
            "attempts": attempts,
            "converged": bool(fit.converged),
            "beta_rx": float(fit.params.get("rx", float("nan"))),
            "se_rx": float(fit.bse.get("rx", float("nan"))),
            "p_rx": float(fit.pvalues.get("rx", float("nan"))),
            "ci95_rx": [float(v) for v in fit.conf_int().loc["rx"].tolist()],
            "group_var": float(fit.cov_re.iloc[0, 0]),
            "scale": float(fit.scale),
            "n_obs": int(fit.nobs),
            "axis_fixed_effects": {k: float(v) for k, v in fit.params.items()
                                   if k.startswith("C(axis)")},
            "reading": ("beta_rx is the association between RANKED induction and "
                        "RANKED detection AFTER the axis main effect is removed; a "
                        "beta near 0 with a CI covering 0 means the pooled "
                        "correlation lived in the axis contrast."),
        }
    else:
        # PRE-REGISTERED FALLBACK (failure mode 3 of the plan): the member random
        # intercept is estimated at zero variance on 70 points -- statsmodels
        # reports "Random effects covariance is singular" and no CI can be formed.
        # The two-way ANOVA-style fixed-effect fit is used instead, with
        # lineage-clustered robust SEs, and the failure is logged rather than hidden.
        logger.error("MixedLM did not converge on any optimiser setting; falling "
                     "back to the two-way fixed-effect fit")
        ols = smf.ols("ry ~ rx + C(axis) + C(member)", df).fit(
            cov_type="cluster", cov_kwds={"groups": df["lineage"]})
        anova = sm.stats.anova_lm(smf.ols("ry ~ C(axis) + C(member)", df).fit(),
                                  typ=2)
        res["mixedlm"] = {
            "used": "FALLBACK -- two-way fixed-effect OLS on ranks (axis + member "
                    "fixed effects) with lineage-clustered robust SEs",
            "converged": False,
            "attempts": attempts,
            "convergence_error": attempts[-1]["outcome"],
            "why": "the member random-effect variance is estimated at the boundary "
                   "of zero on 70 points, so the random-effects covariance is "
                   "singular and no CI for the slope can be formed",
            "beta_rx": float(ols.params.get("rx", float("nan"))),
            "se_rx": float(ols.bse.get("rx", float("nan"))),
            "p_rx": float(ols.pvalues.get("rx", float("nan"))),
            "ci95_rx": [float(v) for v in ols.conf_int().loc["rx"].tolist()],
            "n_obs": int(ols.nobs), "r2": float(ols.rsquared),
            "cluster_unit": "lineage_id",
            "n_clusters": int(df["lineage"].nunique()),
            "anova_typeII_on_ranked_detection": {
                str(k): {"sum_sq": float(v["sum_sq"]), "df": float(v["df"]),
                         "F": (float(v["F"]) if np.isfinite(v["F"]) else None),
                         "p": (float(v["PR(>F)"]) if np.isfinite(v["PR(>F)"])
                               else None)}
                for k, v in anova.iterrows()},
            "reading": ("beta_rx is the association between RANKED induction and "
                        "RANKED detection AFTER both the axis and the member main "
                        "effects are absorbed; a beta near 0 with a CI covering 0 "
                        "means the pooled correlation lived in the axis contrast."),
        }

    # (iv) exact two-way variance decomposition of the pooled statistic
    # The design is BALANCED (14 members x 5 axes = 70), so the additive
    # decomposition rank = mu + axis effect + member effect + residual is
    # orthogonal and the covariance splits EXACTLY into three terms.
    n = len(rx)
    cx, cy = rx - rx.mean(), ry - ry.mean()
    ax_x = np.array([cx[ax == a].mean() for a in ax])
    ax_y = np.array([cy[ax == a].mean() for a in ax])
    mb_x = np.array([cx[mb == m].mean() for m in mb])
    mb_y = np.array([cy[mb == m].mean() for m in mb])
    ex = cx - ax_x - mb_x
    ey = cy - ax_y - mb_y
    tot = float((cx * cy).sum())
    parts = {"between_axis_type": float((ax_x * ax_y).sum()),
             "between_member": float((mb_x * mb_y).sum()),
             "residual": float((ex * ey).sum())}
    cross = tot - sum(parts.values())
    denom = math.sqrt(float((cx * cx).sum()) * float((cy * cy).sum()))
    res["variance_decomposition"] = {
        "design_balanced": bool(len({tuple(sorted(set(ax[mb == m])))
                                     for m in set(mb)}) == 1),
        "n_pairs": n,
        "total_rank_cross_product": tot,
        "components": parts,
        "residual_cross_term_from_nonorthogonality": cross,
        "shares": {k: (v / tot if tot != 0 else None) for k, v in parts.items()},
        "shares_sum": (sum(parts.values()) / tot if tot != 0 else None),
        "rho_pooled_from_decomposition": tot / denom if denom else None,
        "rho_attributable": {k: (v / denom if denom else None)
                             for k, v in parts.items()},
        "majority_share_is": max(parts, key=lambda k: parts[k]),
        "reading": ("each component is the part of the pooled rank cross-product "
                    "contributed by variation BETWEEN axes, BETWEEN members, and "
                    "within-cell residual; the three shares sum to 1.0 because the "
                    "14 x 5 design is balanced and the decomposition is therefore "
                    "orthogonal."),
    }

    # residual member-level coupling with its lineage-clustered CI
    res["residual_member_level_coupling"] = corr_block(
        ex, ey, lin, label="residual coupling after removing BOTH the axis and the "
                           "member main effects [pair level]")
    return res


# --------------------------------------------------------------------------
# (f) within-member mean, correctly labelled
# --------------------------------------------------------------------------
def within_member(points: list[dict]) -> dict:
    h3 = jload(R4 / "method_out.json")["metadata"]["results"]["h3_joint_scatter"]
    coefs = []
    for ck in sorted({p["checkpoint"] for p in points}):
        sub = [p for p in points if p["checkpoint"] == ck]
        if len(sub) >= 4:
            r, _ = spearmanr([p["max_refusal_rate"] for p in sub],
                             [p["detection_auroc"] for p in sub])
            coefs.append({"checkpoint": ck, "rho": float(r), "n_axes": len(sub),
                          "axes": sorted(p["axis"] for p in sub)})
    vals = [c["rho"] for c in coefs if np.isfinite(c["rho"])]
    return {
        "n_coefficients": len(vals), "n_points_each": 5,
        "mean_rho": float(np.mean(vals)),
        "archived_mean_rho": h3["within_member_mean_rho"],
        "median_rho": float(np.median(vals)),
        "coefficients": coefs,
        "label": ("the mean of 14 coefficients each computed over the SAME "
                  "axis-type contrast (one point per axis, five axes, of which two "
                  "are by-construction controls). It is therefore NOT independent "
                  "evidence for a read-act coupling among models, and being larger "
                  "than the pooled figure (0.715 > 0.629) makes it WEAKER evidence, "
                  "not stronger: it is the same confound measured 14 times with "
                  "the between-member variation removed."),
    }


# --------------------------------------------------------------------------
def decide_verdict(primary: dict, pooled: dict, dec: dict) -> dict:
    m, l = primary["member"], primary["lineage"]
    ci = m["ci95"]
    covers0 = (ci is None) or (ci[0] <= 0 <= ci[1])
    hw = m["half_width"]
    pooled_excl = bool(pooled["member"]["ci_excludes_zero"])
    majority = dec["variance_decomposition"]["majority_share_is"]
    share = dec["variance_decomposition"]["shares"].get("between_axis_type")
    fired = []
    if (m["rho"] is not None and m["rho"] >= 0.50 and not covers0
            and primary["same_sign"]):
        fired.append("COUPLING_SURVIVES_WITHIN_AXIS")
    else:
        if covers0 and pooled_excl and majority == "between_axis_type":
            fired.append("COUPLING_IS_AXIS_TYPE_CONTRAST")
        if covers0 and hw is not None and hw > 0.35:
            fired.append("UNDERPOWERED")
    if not fired:
        fired.append("NO_PRECOMMITTED_STRING_FIRES")
    return {
        "verdict": fired[0], "all_fired": fired,
        "deciding_numbers": {
            "within_axis_A_member_rho": m["rho"],
            "within_axis_A_member_ci95": ci,
            "within_axis_A_member_ci_covers_zero": bool(covers0),
            "within_axis_A_member_ci_half_width": hw,
            "within_axis_A_n_members": m["n_points"],
            "within_axis_A_n_lineages": m["n_clusters"],
            "within_axis_A_lineage_rho": l["rho"],
            "within_axis_A_lineage_ci95": l["ci95"],
            "same_sign_across_units": primary["same_sign"],
            "within_axis_A_p_permutation": m["p_permutation"],
            "pooled_70pair_rho": pooled["member"]["rho"],
            "pooled_70pair_ci95": pooled["member"]["ci95"],
            "pooled_ci_excludes_zero": pooled_excl,
            "variance_share_between_axis_type": share,
            "variance_majority_component": majority,
        },
    }


# --------------------------------------------------------------------------
def main() -> dict:
    setup_logging("stage2")
    logger.info("STAGE 2: H-C -- coupling without the axis-type contrast")
    points = load_points()
    rowsA = axis_rows(points, PRIMARY_AXIS)
    logger.info(f"axis A rows: {len(rowsA)} members, "
                f"{len({r['lineage_id'] for r in rowsA})} lineages")

    primary = dual_unit(rowsA, "x", "y",
                        "within-axis-A across-member Spearman (induction max rate "
                        "vs detection AUROC), detection-powered members")
    primary["n_members"] = len(rowsA)
    primary["members"] = [{"checkpoint": r["checkpoint"],
                           "lineage_id": r["lineage_id"],
                           "A_max_rate": r["x"], "A_auroc": r["y"],
                           "A_c50": r["c_50"],
                           "detection_verdict": r["detection_verdict"]}
                          for r in rowsA]
    logger.info(f"PRIMARY within-axis-A: member rho = {primary['member']['rho']:.4f} "
                f"CI {primary['member']['ci95']} (n_lineages="
                f"{primary['member']['n_clusters']}); lineage rho = "
                f"{primary['lineage']['rho']:.4f}")

    # sensitivity: the norm-controlled detection readout (AMENDMENT-1)
    nc_rows = [dict(r, y=r["y_norm_controlled"]) for r in rowsA
               if r["y_norm_controlled"] is not None]
    primary_nc = dual_unit(nc_rows, "x", "y",
                           "within-axis-A, norm-controlled detection readout")

    rev = reviewer_reproduction(rowsA)
    logger.info("reviewer 0.434/0.14 leg: " + rev["statement"][:160])

    sec = secondary_c50(rowsA)
    axes = per_axis(points)
    ladder = control_ladder(points)
    dec = confound(points)
    wm = within_member(points)
    pooled = ladder[0]
    verdict = decide_verdict(primary, pooled, dec)
    logger.info(f"VERDICT: {verdict['verdict']}  (all fired: {verdict['all_fired']})")
    logger.info("variance shares: "
                + ", ".join(f"{k}={v:.3f}" for k, v in
                            dec["variance_decomposition"]["shares"].items()))

    out = {
        "primary": primary,
        "primary_norm_controlled_sensitivity": primary_nc,
        "reviewer_0p434_reproduction": rev,
        "secondary_c50": sec,
        "per_axis": axes,
        "control_ladder": ladder,
        "confound": dec,
        "within_member": wm,
        "verdict": verdict,
    }
    jdump(OUT / "stage2.json", out)
    logger.info("STAGE 2 done")
    return out


if __name__ == "__main__":
    main()
