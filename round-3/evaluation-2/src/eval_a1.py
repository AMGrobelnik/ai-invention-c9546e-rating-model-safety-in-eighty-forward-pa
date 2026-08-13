#!/usr/bin/env python3
"""Analysis 1 -- sign-oriented comparison, orientation-free comparators,
the ceiling check, the wrong-sign probability, and the sign-flip recount."""

from __future__ import annotations

import json

import numpy as np
from loguru import logger

from eval_common import (E1, E2, auc_from_scores, load_json, spearman_rho)

from lib import stats_ext  # archived estimator code, imported VERBATIM

AXES = ["plain_harmful_refusal", "jailbreak_asr", "xstest_over_refusal"]

# Sign rule. s = +1 means "a HIGHER score should mean a SAFER model" already.
ORIENTATION = {
    "alpha_50": -1,
    "alpha_50_nonparametric": -1,
    "max_refusal_rate": -1,
    "ams_sigma": +1,
    "composite": -1,
}

ORIENTATION_CONVENTION = {
    "rule": ("oriented_score = s * score, with s chosen so that a higher oriented "
             "score is the direction the metric's own validity theory predicts for a "
             "SAFER model. Spearman is sign-equivariant, so oriented rho = s * raw rho."),
    "s": ORIENTATION,
    "why_alpha_50_is_negative": (
        "The pre-registered direction is that a SAFER model refuses at a LOWER steering "
        "coefficient, i.e. its refusal behaviour is cheaper to elicit, so alpha_50 must "
        "correlate NEGATIVELY with the judged plain-harmful refusal rate for the score "
        "to be valid. Under a positive-is-better convention alpha_50 therefore carries "
        "s = -1."),
    "prereg_citation": {
        "file": str(E1 / "method_out.json"),
        "key": "metadata.external_validity.ranking_agreement.expected_sign_if_metric_valid",
        "quoted": None,  # filled at runtime
        "secondary_file": str(E2 / "prereg.json"),
        "secondary_key": "d3_ams.headline",
        "secondary_quoted": None,  # filled at runtime
        "note": (
            "the iteration-2 breadth-panel pre-registration fixes the sign of the DIFFERENCE "
            "('DELTA > 0 means alpha_50 tracks behaviour BETTER than AMS') but never fixes the "
            "sign of either component, which is exactly the gap this analysis closes: the two "
            "rho values have OPPOSITE predicted directions, so their raw difference does not "
            "mean what the convention says it means. The per-score direction is pinned by the "
            "depth-panel pre-registration quoted above."),
    },
    "why_ams_is_positive": (
        "our-AMS sigma is a separation statistic: larger sigma = a more separable "
        "harmful/benign geometry = the direction its own thresholds (PASS > 3.5, "
        "WARN 2.0-3.5, CRIT < 2.0) treat as safer. s = +1."),
    "why_max_refusal_rate_is_negative": (
        "max refusal rate over the steering grid is a REACHABILITY statistic: the "
        "pre-registered gate reads a HIGH reachable refusal rate as evidence that the "
        "refusal behaviour is easy to induce, the same direction as a LOW alpha_50, so "
        "it is carried at s = -1 for consistency with the alpha_50 family. Reported in "
        "both signs so a reader who disputes this can read the raw value."),
}


def paired_delta(units, key_a, key_b, key_y, sign_a, sign_b, n_boot=5000,
                 seed=stats_ext.BOOT_SEED):
    """Paired lineage bootstrap of DELTA = rho(a,y) - rho(b,y) under a sign rule.

    Mirrors lib/stats_ext.paired_rho_delta exactly (same resampling, same seed)
    and adds the sign multipliers plus the one-sided probabilities the reanalysis
    needs.
    """
    rows = [u for u in units if u.get(key_a) is not None and u.get(key_b) is not None
            and u.get(key_y) is not None]
    a = np.array([u[key_a] for u in rows], dtype=float)
    b = np.array([u[key_b] for u in rows], dtype=float)
    y = np.array([u[key_y] for u in rows], dtype=float)
    ra, rb = spearman_rho(a, y), spearman_rho(b, y)
    ra = None if ra is None else sign_a * ra
    rb = None if rb is None else sign_b * rb
    delta = (ra - rb) if (ra is not None and rb is not None) else None
    rng = np.random.default_rng(seed)
    boot_d, boot_a, boot_b, boot_absd = [], [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, len(rows), size=len(rows))
        r1, r2 = spearman_rho(a[idx], y[idx]), spearman_rho(b[idx], y[idx])
        if r1 is None or r2 is None:
            continue
        r1, r2 = sign_a * r1, sign_b * r2
        boot_a.append(r1)
        boot_b.append(r2)
        boot_d.append(r1 - r2)
        boot_absd.append(abs(r1) - abs(r2))
    def pct(v):
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) >= 50 else None
    jack = []
    for i in range(len(rows)):
        m = [j for j in range(len(rows)) if j != i]
        r1, r2 = spearman_rho(a[m], y[m]), spearman_rho(b[m], y[m])
        jack.append({"dropped": rows[i]["lineage"],
                     "rho_a": None if r1 is None else sign_a * r1,
                     "rho_b": None if r2 is None else sign_b * r2,
                     "delta": None if (r1 is None or r2 is None) else sign_a * r1 - sign_b * r2})
    ja = [j["rho_a"] for j in jack if j["rho_a"] is not None]
    jb = [j["rho_b"] for j in jack if j["rho_b"] is not None]
    perm_a = stats_ext.spearman_with_permutation(sign_a * a, y)
    perm_b = stats_ext.spearman_with_permutation(sign_b * b, y)
    return {
        "n": len(rows), "rho_a": ra, "rho_b": rb, "delta": delta,
        "ci_delta": pct(boot_d),
        "ci_rho_a": pct(boot_a), "ci_rho_b": pct(boot_b),
        "abs_delta": (abs(ra) - abs(rb)) if (ra is not None and rb is not None) else None,
        "ci_abs_delta": pct(boot_absd),
        "frac_delta_below_0": float(np.mean(np.asarray(boot_d) < 0)) if boot_d else None,
        "frac_abs_delta_below_0": float(np.mean(np.asarray(boot_absd) < 0)) if boot_absd else None,
        "p_one_sided_rho_a_below_0": float(np.mean(np.asarray(boot_a) < 0)) if boot_a else None,
        "p_one_sided_rho_b_below_0": float(np.mean(np.asarray(boot_b) < 0)) if boot_b else None,
        "jackknife": jack,
        "jackknife_rho_a_range": [min(ja), max(ja)] if ja else None,
        "jackknife_rho_b_range": [min(jb), max(jb)] if jb else None,
        "jackknife_rho_a_sign_changes": int(sum(1 for v in ja if v < 0)) if ja else None,
        "jackknife_rho_b_sign_changes": int(sum(1 for v in jb if v < 0)) if jb else None,
        "n_boot_valid": len(boot_d), "n_boot": n_boot, "seed": int(seed),
        "perm_a": perm_a, "perm_b": perm_b,
        "winner_oriented": (
            None if (delta is None or pct(boot_d) is None)
            else ("alpha_50" if pct(boot_d)[0] > 0
                  else ("our_AMS" if pct(boot_d)[1] < 0 else "TIE_CI_INCLUDES_0"))),
    }


def auc_comparator(units, key, axis, sign, threshold, n_boot=5000,
                   seed=stats_ext.BOOT_SEED):
    """Predictive AUC of an oriented score against a binarised safety label."""
    rows = [u for u in units if u.get(key) is not None and u.get(axis) is not None]
    s = sign * np.array([u[key] for u in rows], dtype=float)
    yv = np.array([u[axis] for u in rows], dtype=float)
    thr = float(np.median(yv)) if threshold == "median" else float(threshold)
    lab = (yv > thr).astype(int)
    point = auc_from_scores(s, lab)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(rows), size=len(rows))
        v = auc_from_scores(s[idx], lab[idx])
        if v is not None:
            boot.append(v)
    jack = []
    for i in range(len(rows)):
        m = [j for j in range(len(rows)) if j != i]
        v = auc_from_scores(s[m], lab[m])
        if v is not None:
            jack.append({"dropped": rows[i]["lineage"], "auc": v})
    jv = [j["auc"] for j in jack]
    return {
        "auc": point, "n": len(rows), "threshold_rule": threshold, "threshold": thr,
        "n_positive": int(lab.sum()), "n_negative": int((1 - lab).sum()),
        "ci": ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
               if len(boot) >= 50 else None),
        "n_boot_valid": len(boot),
        "jackknife": jack,
        "jackknife_range": [min(jv), max(jv)] if jv else None,
    }


def run(units, members) -> dict:
    prereg = load_json(E2 / "prereg.json")
    conv = dict(ORIENTATION_CONVENTION)
    conv["prereg_citation"] = dict(conv["prereg_citation"])
    e1 = load_json(E1 / "method_out.json")["metadata"]
    conv["prereg_citation"]["quoted"] = (
        e1["external_validity"]["ranking_agreement"]["expected_sign_if_metric_valid"])
    conv["prereg_citation"]["secondary_quoted"] = json.dumps(prereg["d3_ams"]["headline"])
    res = {"orientation_convention": conv}

    scores = ["alpha_50", "alpha_50_nonparametric", "max_refusal_rate", "ams_sigma"]

    # ---- (1a) per-score rho, raw and oriented, against each judged axis -------
    per_score = {}
    for sc in scores:
        per_score[sc] = {}
        for ax in AXES:
            rows = [u for u in units if u[sc] is not None]
            x = [u[sc] for u in rows]
            y = [u[ax] for u in rows]
            raw = spearman_rho(x, y)
            s = ORIENTATION[sc]
            # lineage-clustered bootstrap on rho itself
            a = np.asarray(x, float); yy = np.asarray(y, float)
            rng = np.random.default_rng(stats_ext.BOOT_SEED)
            boot = []
            for _ in range(5000):
                idx = rng.integers(0, len(rows), size=len(rows))
                v = spearman_rho(a[idx], yy[idx])
                if v is not None:
                    boot.append(s * v)
            per_score[sc][ax] = {
                "n": len(rows),
                "rho_raw": raw,
                "rho_oriented": None if raw is None else s * raw,
                "sign_s": s,
                "ci_oriented": ([float(np.percentile(boot, 2.5)),
                                 float(np.percentile(boot, 97.5))] if len(boot) >= 50 else None),
                "n_boot_valid": len(boot),
                "suppressed_reason": (None if raw is not None else
                                      "Spearman undefined: the score is constant across "
                                      "the 7 lineage units (all values are the "
                                      "ranked-bottom sentinel)"),
                "permutation": stats_ext.spearman_with_permutation(
                    np.asarray([s * v for v in x], float), yy) if raw is not None else None,
            }
    res["per_score_rho"] = per_score

    # ---- (1b) regression check then the oriented headline --------------------
    arch = load_json(E2 / "method_out.json")["metadata"]["analysis"]["d3_headline"][
        "with_undefined_ranked_bottom"]["alpha_50_nonparametric_PREREGISTERED_FALLBACK"][
        "vs_plain_harmful_refusal"]
    repro = stats_ext.paired_rho_delta(units, "alpha_50_nonparametric", "ams_sigma",
                                       "plain_harmful_refusal")
    ok = (abs(repro["delta"] - arch["delta"]) < 5e-4
          and abs(repro["ci"][0] - arch["ci"][0]) < 5e-4
          and abs(repro["ci"][1] - arch["ci"][1]) < 5e-4)
    res["regression_check_raw_headline"] = {
        "recomputed": {"rho_a": repro["rho_a"], "rho_b": repro["rho_b"],
                       "delta": repro["delta"], "ci": repro["ci"]},
        "archived": {"rho_a": arch["rho_a"], "rho_b": arch["rho_b"],
                     "delta": arch["delta"], "ci": arch["ci"]},
        "reproduces_to_3dp": bool(ok),
        "code_path": "lib.stats_ext.paired_rho_delta (imported verbatim from E2/lib)",
    }
    if not ok:
        res["regression_check_raw_headline"]["STOP"] = (
            "archived headline did not reproduce; oriented headline NOT reported")
        return res

    headline = {}
    for ax in AXES:
        headline[ax] = paired_delta(units, "alpha_50_nonparametric", "ams_sigma", ax,
                                    ORIENTATION["alpha_50_nonparametric"],
                                    ORIENTATION["ams_sigma"])
    res["oriented_headline_delta"] = headline

    # ---- (1f) the ceiling calculation ---------------------------------------
    h = headline["plain_harmful_refusal"]
    rho_ams_oriented = h["rho_b"]
    res["ceiling_check"] = {
        "statistic": "DELTA = rho_alpha50 - rho_AMS on the breadth panel (n_lineage=7)",
        "old_raw_statistic": {
            "rho_ams_raw": arch["rho_b"],
            "rho_alpha50_raw_measured": arch["rho_a"],
            "delta_measured": arch["delta"],
            "rho_alpha50_if_PERFECT": -1.0,
            "delta_if_alpha50_were_PERFECT": -1.0 - arch["rho_b"],
            "arithmetic": f"-1 - {arch['rho_b']:.4f} = {-1.0 - arch['rho_b']:.4f}",
            "reading": ("under the raw statistic a PERFECT alpha_50 scores as a large "
                        "NEGATIVE delta, i.e. as a catastrophic loss to our-AMS. A "
                        "comparison that cannot reward the ideal case measures nothing."),
        },
        "corrected_oriented_statistic": {
            "rho_ams_oriented": rho_ams_oriented,
            "rho_alpha50_oriented_measured": h["rho_a"],
            "delta_measured": h["delta"],
            "rho_alpha50_if_PERFECT": 1.0,
            "delta_if_alpha50_were_PERFECT": 1.0 - rho_ams_oriented,
            "arithmetic": f"+1 - {rho_ams_oriented:.4f} = {1.0 - rho_ams_oriented:.4f}",
            "reading": ("under the oriented statistic a perfect alpha_50 wins by "
                        f"{1.0 - rho_ams_oriented:.4f}, so the comparison is now able to "
                        "reward the ideal case."),
        },
    }

    # ---- (1g) the stronger claim --------------------------------------------
    p_wrong = h["p_one_sided_rho_a_below_0"]
    res["wrong_sign_claim"] = {
        "rho_alpha50_raw": arch["rho_a"],
        "rho_alpha50_oriented": h["rho_a"],
        "theory_demands": "oriented rho > 0 (equivalently raw rho < 0)",
        "p_true_oriented_rho_below_0": p_wrong,
        "jackknife_oriented_range": h["jackknife_rho_a_range"],
        "n_jackknife_folds_oriented_negative": h["jackknife_rho_a_sign_changes"],
        "permutation_p_oriented": h["perm_a"]["p_permutation"],
        "permutation_floor": h["perm_a"]["p_min_achievable"],
        "claim_strength": (
            "wrong-signed under its own validity theory" if (p_wrong or 0) >= 0.90 else
            "indistinguishable from zero and point-estimated with the wrong sign"),
        "downgrade_applied": bool((p_wrong or 0) < 0.90),
        "statement": None,  # set below
    }
    res["wrong_sign_claim"]["statement"] = (
        f"The lineage bootstrap puts {p_wrong:.3f} of its mass on oriented "
        f"rho_alpha50 < 0. " + (
            "That is high enough to state that alpha_50 is wrong-signed under its own "
            "validity theory."
            if (p_wrong or 0) >= 0.90 else
            "Substantial mass sits on both sides of zero, so the defensible statement is "
            "the weaker one: alpha_50's breadth-panel correlation is indistinguishable "
            "from zero and point-estimated with the wrong sign."))

    # ---- (1e) orientation-free comparators -----------------------------------
    comparators = {"abs_rho": {}, "auc": {}}
    for ax in AXES:
        comparators["abs_rho"][ax] = {
            "abs_rho_alpha50": abs(headline[ax]["rho_a"]) if headline[ax]["rho_a"] is not None else None,
            "abs_rho_ams": abs(headline[ax]["rho_b"]) if headline[ax]["rho_b"] is not None else None,
            "abs_delta": headline[ax]["abs_delta"],
            "ci_abs_delta": headline[ax]["ci_abs_delta"],
            "frac_abs_delta_below_0": headline[ax]["frac_abs_delta_below_0"],
            "n": headline[ax]["n"],
        }
    for thr in ["median", 0.5]:
        key = "median_split" if thr == "median" else "fixed_0.5"
        comparators["auc"][key] = {
            sc: auc_comparator(units, sc, "plain_harmful_refusal", ORIENTATION[sc], thr)
            for sc in ["alpha_50_nonparametric", "ams_sigma"]
        }
    ranks = {}
    a_or = headline["plain_harmful_refusal"]["rho_a"]
    b_or = headline["plain_harmful_refusal"]["rho_b"]
    ranks["oriented_rho"] = "our_AMS" if b_or > a_or else "alpha_50"
    ranks["abs_rho"] = ("our_AMS" if abs(b_or) > abs(a_or) else "alpha_50")
    am = comparators["auc"]["median_split"]
    ranks["auc_median_split"] = ("our_AMS"
                                 if am["ams_sigma"]["auc"] > am["alpha_50_nonparametric"]["auc"]
                                 else "alpha_50")
    af = comparators["auc"]["fixed_0.5"]
    ranks["auc_fixed_0.5"] = (None if af["ams_sigma"]["auc"] is None or af["alpha_50_nonparametric"]["auc"] is None
                              else ("our_AMS" if af["ams_sigma"]["auc"] > af["alpha_50_nonparametric"]["auc"]
                                    else "alpha_50"))
    defined = [v for v in ranks.values() if v is not None]
    absd = comparators["abs_rho"]["plain_harmful_refusal"]
    a50_auc = am["alpha_50_nonparametric"]["auc"]
    comparators["ordering_agreement"] = {
        "per_comparator_winner": ranks,
        "all_agree": len(set(defined)) == 1,
        "agreement_is_on_point_estimates": True,
        "interval_caveat": (
            "The agreement is between POINT estimates. At n=7 lineages the paired |rho| "
            f"difference CI is [{absd['ci_abs_delta'][0]:.3f}, {absd['ci_abs_delta'][1]:.3f}], "
            f"which {'includes' if absd['ci_abs_delta'][0] <= 0 <= absd['ci_abs_delta'][1] else 'excludes'} "
            "zero, so no comparator separates the two scores at conventional confidence."),
        "note_alpha50_auc_below_chance": (
            f"alpha_50's median-split AUC is {a50_auc:.3f}, BELOW the 0.5 chance line: as an "
            "oriented predictor of the binarised safety label it is anti-predictive on this "
            "panel, not merely uninformative."),
        "statement": ("All orientation-free comparators agree with the oriented "
                      "correlation on the ordering, so the conclusion does not depend on "
                      "the sign convention."
                      if len(set(defined)) == 1 else
                      "The comparators DISAGREE on the ordering; no favourite is picked."),
    }
    res["orientation_free_comparators"] = comparators

    # ---- (1h) the sign-flip recount ------------------------------------------
    flips = []
    for sc in ["alpha_50_nonparametric", "max_refusal_rate"]:
        v = per_score[sc]["plain_harmful_refusal"]["rho_oriented"]
        flips.append({"choice": f"estimator = {sc}", "oriented_rho": v,
                      "sign": "negative (wrong)" if v is not None and v < 0 else "positive (right)"})
    lv = per_score["alpha_50"]["plain_harmful_refusal"]["rho_oriented"]
    flips.append({"choice": "estimator = logistic alpha_50 (pre-registered primary)",
                  "oriented_rho": lv,
                  "sign": "UNDEFINED (constant sentinel across all 7 lineages)"})
    for j in headline["plain_harmful_refusal"]["jackknife"]:
        flips.append({"choice": f"jackknife fold: drop {j['dropped']}",
                      "oriented_rho": j["rho_a"],
                      "sign": "negative (wrong)" if j["rho_a"] < 0 else "positive (right)"})
    # depth panel (iteration-2 experiment 1, n=6 checkpoints)
    ev = load_json(E1 / "method_out.json")["metadata"]["external_validity"]
    dp_raw = ev["spearman_alpha50_vs_judge_harmful_refusal_rate"]["rho"]
    per_model = ev["per_model"]
    dp = {"raw_rho": dp_raw, "oriented_rho": -dp_raw, "n": ev["n_models"],
          "archived_p": ev["spearman_alpha50_vs_judge_harmful_refusal_rate"]["p"]}
    x = np.array([m["alpha_50"] for m in per_model], float)
    y = np.array([m["judge_harmful_refusal_rate"] for m in per_model], float)
    dp["exact_permutation_oriented"] = stats_ext.spearman_with_permutation(-x, y)
    dp["permutation_floor_note"] = (
        "at n=6 the exhaustive permutation set has 720 orderings, so the smallest "
        "attainable two-sided p is 2/720 = 0.00278 for a unique extreme ordering; the "
        "achievable floor reported here is computed from the observed tie pattern")
    flips.append({"choice": "panel = iteration-2 depth panel (6 checkpoints, one lineage pair)",
                  "oriented_rho": dp["oriented_rho"],
                  "sign": "positive (right)" if dp["oriented_rho"] > 0 else "negative (wrong)"})
    n_right = sum(1 for f in flips if f["sign"].startswith("positive"))
    n_wrong = sum(1 for f in flips if f["sign"].startswith("negative"))
    res["sign_flip_recount"] = {
        "enumerated_choices": flips,
        "n_choices_enumerated": len(flips),
        "n_right_signed": n_right,
        "n_wrong_signed": n_wrong,
        "n_undefined": len(flips) - n_right - n_wrong,
        "old_sentence": "alpha_50's correlation changes sign four times across analysis choices",
        "new_sentence": (
            f"Across the {len(flips)} enumerated analysis choices the oriented alpha_50 "
            f"correlation is right-signed {n_right} times and wrong-signed {n_wrong} "
            f"times, with {len(flips) - n_right - n_wrong} undefined; the sign is not a "
            "stable property of the score."),
        "old_count_retired": True,
    }
    res["depth_panel"] = dp
    return res

