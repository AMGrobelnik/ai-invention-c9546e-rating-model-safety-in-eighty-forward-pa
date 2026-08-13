#!/usr/bin/env python3
"""Analysis 1 (held-out behavioural certification) and Analysis 2 (axis-contrast-unit
dose response, including the matched-contrast test).  CPU only, pure re-analysis."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_lib as EL  # noqa: E402

PROJ = EL.RESULTS / "proj"


# ===========================================================================
# Analysis 1
# ===========================================================================
def _labels(items: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (primary label, regex label, has-judge mask).

    Label coding: 1 = refusal, 0 = compliance, -1 = excluded (PARTIAL/DEGENERATE).
    """
    prim, rgx, hasj = [], [], []
    for it in items:
        r = 1 if it["regex_refusal"] else 0
        lab = it.get("judge_label")
        if lab == "REFUSAL":
            p = 1
        elif lab == "COMPLIANCE":
            p = 0
        elif lab in ("PARTIAL", "DEGENERATE"):
            p = -1
        else:
            p = r
        prim.append(p)
        rgx.append(r)
        hasj.append(lab in ("REFUSAL", "COMPLIANCE", "PARTIAL", "DEGENERATE"))
    return np.array(prim), np.array(rgx), np.array(hasj)


def _centre_by_stratum(s: np.ndarray, strata: np.ndarray) -> np.ndarray:
    out = s.astype(float).copy()
    for st in np.unique(strata):
        m = strata == st
        if m.sum() >= 2:
            out[m] -= out[m].mean()
        else:
            out[m] -= out.mean()
    return out


def analysis1_checkpoint(key: str) -> dict:
    items = json.loads((PROJ / f"{key}_items.json").read_text())
    z = np.load(PROJ / f"{key}.npz")
    meta = EL.model_meta(key)
    enc = EL.load_json(EL.RESULTS / f"encode_{key}.json")

    prim, rgx, hasj = _labels(items)
    strata = np.array([it["stratum"] for it in items])
    clusters = np.array([f"{it['source']}|{it['cluster']}" for it in items])
    keep = prim >= 0
    n_ref, n_com = int((prim[keep] == 1).sum()), int((prim[keep] == 0).sum())
    powered = (n_ref >= EL.MIN_PER_CLASS) and (n_com >= EL.MIN_PER_CLASS)

    # kappa(regex, judge) on the overlap
    ov = hasj & (prim >= 0)
    kap = EL.cohens_kappa([int(x) for x in rgx[ov]], [int(x) for x in prim[ov]])

    axes = sorted({k.split("|")[0] for k in z.files if "|" in k})
    boots = list(EL.cluster_boot_indices(clusters[keep], EL.N_BOOT, EL.BOOT_SEED))

    res: dict = {"checkpoint": key, "n_items": len(items), "n_refusal": n_ref,
                 "n_compliance": n_com, "n_excluded_partial_degenerate": int((~keep).sum()),
                 "powered": bool(powered),
                 "underpowered_reason": None if powered else
                 f"n_refusal={n_ref}, n_compliance={n_com} (floor {EL.MIN_PER_CLASS})",
                 "kappa_regex_vs_judge": kap,
                 "n_with_judge_label": int(hasj.sum()),
                 "source_counts": enc["harvest"]["by_source"],
                 "axes": {}, "conventions": {}}

    for conv in ("first", "mean"):
        conv_out = {}
        y = prim[keep]
        for ax in axes:
            s_raw = z[f"{ax}|{conv}"][keep]
            s_ctr = _centre_by_stratum(z[f"{ax}|{conv}"], strata)[keep]
            row = {}
            for tag, s in (("centred", s_ctr), ("raw", s_raw)):
                a = EL.auroc(s[y == 1], s[y == 0])
                d = EL.cohens_d(s[y == 1], s[y == 0])
                md = float(s[y == 1].mean() - s[y == 0].mean())
                if tag == "centred":
                    bs = [EL.auroc(s[i][y[i] == 1], s[i][y[i] == 0]) for i in boots]
                    lo, hi = EL.boot_ci(bs)
                else:
                    lo = hi = float("nan")
                row[tag] = {"auroc": a, "auroc_ci95": [lo, hi], "cohens_d": d,
                            "mean_diff_projection_units": md}
            # regex-label column
            yr = rgx[keep]
            row["regex_label_auroc_centred"] = EL.auroc(s_ctr[yr == 1], s_ctr[yr == 0])
            conv_out[ax] = row
        # paired A - B
        if "A_canned" in axes and "B_paraphrase" in axes:
            sa = _centre_by_stratum(z[f"A_canned|{conv}"], strata)[keep]
            sb = _centre_by_stratum(z[f"B_paraphrase|{conv}"], strata)[keep]
            diffs = [EL.auroc(sa[i][y[i] == 1], sa[i][y[i] == 0])
                     - EL.auroc(sb[i][y[i] == 1], sb[i][y[i] == 0]) for i in boots]
            point = EL.auroc(sa[y == 1], sa[y == 0]) - EL.auroc(sb[y == 1], sb[y == 0])
            lo, hi = EL.boot_ci(diffs)
            reg = EL.ols_r2(sa, sb)
            resid = reg["resid"]
            conv_out["_paired_A_minus_B"] = {
                "delta_auroc": float(point), "ci95": [lo, hi],
                "boot_p_two_sided": EL.boot_p_two_sided(diffs, 0.0),
                "upper_ci_le_margin": bool(hi <= EL.DELTA_MARGIN),
                "ci_excludes_zero_and_delta_gt_margin":
                    bool(point > EL.DELTA_MARGIN and lo > 0.0),
            }
            conv_out["_residual_test_B_given_A"] = {
                "r2_of_sB_on_sA": reg["r2"], "slope": reg["slope"],
                "auroc_of_residual": EL.auroc(resid[y == 1], resid[y == 0]),
                "reading": ("if B were a purely scaled noisy copy of A, the residual "
                            "after projecting out s_A would carry no refusal signal "
                            "(AUROC ~ 0.5)"),
            }
        res["conventions"][conv] = conv_out

    res["axes"] = res["conventions"]["first"]

    # robustness: AUROC WITHIN each harvest source, so a source-composition difference
    # between the two classes cannot by itself produce the result
    src = np.array([it["source"] for it in items])[keep]
    y_all = prim[keep]
    by_source = {}
    for s_name in sorted(set(src)):
        m = src == s_name
        if (y_all[m] == 1).sum() < 10 or (y_all[m] == 0).sum() < 10:
            continue
        row = {"n_refusal": int((y_all[m] == 1).sum()),
               "n_compliance": int((y_all[m] == 0).sum())}
        for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0"):
            if f"{ax}|first" not in z.files:
                continue
            s = _centre_by_stratum(z[f"{ax}|first"], strata)[keep][m]
            row[ax] = EL.auroc(s[y_all[m] == 1], s[y_all[m] == 0])
        by_source[s_name] = row
    res["auroc_within_source"] = by_source

    # geometry companions (the 'weaker estimate' hypothesis, quantified)
    rn = enc["axis_raw_norms"]
    res["geometry"] = {
        "raw_norms": rn,
        "ratio_normA_over_normB": float(rn["A_canned"] / rn["B_paraphrase"]),
        "cosines": {k: v for k, v in meta["axis_cosines"].items() if "A_canned" in k},
        "cos_A_vs_exp2_independent_fit": enc.get("cos_A_vs_exp2_independent_fit"),
    }

    # V3: observable reproduction
    rt_re = z["rt_reencoded"]
    rt_log = np.array([it.get("r_t_first", np.nan) if it.get("r_t_first") is not None
                       else np.nan for it in items], dtype=float)
    m = np.isfinite(rt_re) & np.isfinite(rt_log)
    sA = z["A_canned|first"]
    m2 = np.isfinite(rt_log) & np.isfinite(sA)
    res["V3_observable_reproduction"] = {
        "n_alpha0_rows": int(m.sum()),
        "pearson_r_t_reencoded_vs_logged": EL.pearson(rt_re[m], rt_log[m]) if m.sum() > 2
        else None,
        "max_abs_delta": float(np.max(np.abs(rt_re[m] - rt_log[m]))) if m.sum() else None,
        "pearson_sA_first_vs_logged_r_t_first":
            EL.pearson(sA[m2], rt_log[m2]) if m2.sum() > 2 else None,
        "note": ("r_t is a refusal-token logit margin, not an axis projection; the exact "
                 "gate is the re-encoded-vs-logged r_t identity, the sA correlation is a "
                 "construct-validity companion (pre-registered as such)"),
    }
    return res


def analysis1(keys: list[str]) -> dict:
    per = {}
    for k in keys:
        if not (PROJ / f"{k}.npz").exists():
            logger.warning(f"no projections for {k}; skipping")
            continue
        per[k] = analysis1_checkpoint(k)
        a = per[k]["axes"]
        logger.info(f"[{k}] powered={per[k]['powered']} nR={per[k]['n_refusal']} "
                    f"nC={per[k]['n_compliance']} "
                    f"AUROC A={a['A_canned']['centred']['auroc']:.3f} "
                    f"B={a['B_paraphrase']['centred']['auroc']:.3f} "
                    f"dAB={a['_paired_A_minus_B']['delta_auroc']:+.3f}")

    powered = [k for k, v in per.items() if v["powered"]]
    verdict = _verdict(per, powered)

    # Companion certification, not anticipated by the binary rule but forced by the
    # data: does the CANNED axis A itself read held-out refusals above chance?
    a_ok, a_chance, a_sig = [], [], []
    for k in powered:
        lo, hi = per[k]["axes"]["A_canned"]["centred"]["auroc_ci95"]
        (a_ok if lo > EL.CHANCE_BAND[1] else a_chance).append(k)
        if lo > 0.5:
            a_sig.append(k)
    # the same test for the paraphrase axis, so the two are read on one scale
    b_sig = [k for k in powered
             if per[k]["axes"]["B_paraphrase"]["centred"]["auroc_ci95"][0] > 0.5]
    # C and D: at chance, or significantly BELOW it?
    below = {}
    for ax in ("C_stylistic", "D_random0"):
        below[ax] = [k for k in powered
                     if per[k]["axes"][ax]["centred"]["auroc_ci95"][1] < 0.5]
    verdict["certification_of_A"] = {
        "A_above_chance_band": a_ok,
        "A_within_or_below_chance_band": a_chance,
        "A_ci_excludes_0.5": a_sig,
        "B_ci_excludes_0.5": b_sig,
        "control_axes_significantly_BELOW_chance": below,
        "auroc_B_range": [min(per[k]["axes"]["B_paraphrase"]["centred"]["auroc"]
                              for k in powered),
                          max(per[k]["axes"]["B_paraphrase"]["centred"]["auroc"]
                              for k in powered)],
        "auroc_A_range": [min(per[k]["axes"]["A_canned"]["centred"]["auroc"]
                              for k in powered),
                          max(per[k]["axes"]["A_canned"]["centred"]["auroc"]
                              for k in powered)],
        "reading": ("the archived certificate gave EVERY axis held-out AUROC 1.000 on "
                    "eight hand-written strings; on the models' own generated text the "
                    "canned axis itself lands in this range, so the vacuous certificate "
                    "over-stated axis A as well as axis B"),
    }
    pv = {k: per[k]["axes"]["_paired_A_minus_B"]["boot_p_two_sided"] for k in per}
    return {"per_checkpoint": per, "powered_checkpoints": powered,
            "underpowered_checkpoints": [k for k in per if k not in powered],
            "holm_adjusted_p_paired_AminusB": EL.holm(pv), "raw_p_paired_AminusB": pv,
            **verdict}


def _verdict(per: dict, powered: list[str]) -> dict:
    if len(powered) < 3:
        return {"lexicality_verdict": "BLOCKED",
                "verdict_reason": f"only {len(powered)} powered checkpoints "
                                  f"(pre-registered floor 3): {powered}"}
    n = len(powered)
    conf_b = [k for k in powered
              if per[k]["axes"]["_paired_A_minus_B"]["upper_ci_le_margin"]]
    down_b = [k for k in powered
              if per[k]["axes"]["_paired_A_minus_B"]["ci_excludes_zero_and_delta_gt_margin"]]
    null_ok = []
    for k in powered:
        ok = True
        for ax in ("C_stylistic", "D_random0"):
            r = per[k]["axes"].get(ax)
            if r is None:
                continue
            lo, hi = r["centred"]["auroc_ci95"]
            if not (hi >= EL.CHANCE_BAND[0] and lo <= EL.CHANCE_BAND[1]):
                ok = False
        if ok:
            null_ok.append(k)
    maj = n // 2 + 1
    if len(conf_b) >= maj and len(null_ok) >= maj:
        v = "LEXICALITY_CONFIRMED"
    elif len(down_b) >= maj:
        v = "DOWNGRADE_TO_AXIS_ESTIMATION_FRAGILITY"
    else:
        v = "MIXED"
    return {"lexicality_verdict": v,
            "verdict_counts": {"n_powered": n, "majority_needed": maj,
                               "B_not_materially_worse": conf_b,
                               "B_materially_worse": down_b,
                               "nulls_at_chance": null_ok},
            "verdict_reason": (f"{len(conf_b)}/{n} powered checkpoints have "
                               f"upper CI(A-B) <= {EL.DELTA_MARGIN}; {len(down_b)}/{n} "
                               f"have A-B > {EL.DELTA_MARGIN} with CI excluding 0; "
                               f"{len(null_ok)}/{n} have both null axes at chance")}


# ===========================================================================
# Analysis 2
# ===========================================================================
def _dose_rows(key: str, axis: str) -> list[dict]:
    p = EL.EXP1 / f"gens/{key}__{axis}.jsonl"
    return list(EL.read_jsonl(p)) if p.exists() else []


def _curve(rows: list[dict], label_fn=lambda r: bool(r["refused"])) -> dict:
    by: dict[float, list] = {}
    for r in rows:
        by.setdefault(round(float(r["alpha"]), 6), []).append(r)
    out = {}
    for a in sorted(by):
        rs = by[a]
        k = sum(1 for r in rs if label_fn(r))
        lo, hi = EL.wilson(k, len(rs))
        d3 = float(np.mean([EL.distinct_n_words(r.get("text", ""), 3) for r in rs]))
        out[a] = {"alpha": a, "n": len(rs), "k_refused": k, "rate": k / len(rs),
                  "wilson_ci95": [lo, hi],
                  "frac_fluent": float(np.mean([bool(r.get("fluent", True)) for r in rs])),
                  "mean_distinct3_words": d3,
                  "mean_max_rep5": float(np.mean([EL.max_ngram_repeat(r.get("text", ""), 5)
                                                  for r in rs]))}
    return out


def _rate_curve(rows: list[dict]) -> dict:
    """Refusal rate per alpha only -- no text statistics.  Used inside the bootstrap,
    where recomputing the degeneracy statistics 500 times would dominate the cost."""
    by: dict[float, list[int]] = {}
    for r in rows:
        by.setdefault(round(float(r["alpha"]), 6), []).append(int(bool(r["refused"])))
    return {a: {"rate": sum(v) / len(v), "n": len(v)} for a, v in by.items()}


def _np_alpha50(curve: dict) -> float | None:
    """Non-parametric crossing: first alpha whose rate >= 0.5, linear-interpolated."""
    a = sorted(curve)
    prev_a, prev_r = None, None
    for x in a:
        r = curve[x]["rate"]
        if r >= 0.5:
            if prev_a is None or prev_r is None or r == prev_r:
                return float(x)
            return float(prev_a + (0.5 - prev_r) * (x - prev_a) / (r - prev_r))
        prev_a, prev_r = x, r
    return None


def _rate_at_c(curve: dict, norm_l: float, u: float, c: float) -> float | None:
    """Linear interpolation of the refusal rate at contrast-unit level c."""
    pts = sorted((float(a) * norm_l / u, curve[a]["rate"]) for a in curve)
    if not pts or c < pts[0][0] or c > pts[-1][0]:
        return None
    for (c0, r0), (c1, r1) in zip(pts, pts[1:]):
        if c0 <= c <= c1:
            if c1 == c0:
                return r0
            return r0 + (r1 - r0) * (c - c0) / (c1 - c0)
    return None


def analysis2_checkpoint(key: str) -> dict:
    meta = EL.model_meta(key)
    enc_p = EL.RESULTS / f"encode_{key}.json"
    norms = (EL.load_json(enc_p)["axis_raw_norms"] if enc_p.exists()
             else {a: meta["axes"][a]["raw_norm"] for a in meta["axes"]})
    norm_l = float(meta["NORM_L"])
    out = {"checkpoint": key, "NORM_L": norm_l, "axis_raw_norms": norms, "axes": {}}
    rows_by_axis = {}
    for axis in sorted(meta["axes"]):
        rows = _dose_rows(key, axis)
        if not rows:
            continue
        rows_by_axis[axis] = rows
        cur = _curve(rows)
        u = float(norms.get(axis, meta["axes"][axis]["raw_norm"]))
        cu = {a: {**v, "contrast_units": float(a) * norm_l / u} for a, v in cur.items()}
        rates = [v["rate"] for v in cur.values()]
        amax = max(cur, key=lambda a: cur[a]["rate"])
        a50 = _np_alpha50(cur)
        # fluency collapse: first alpha where mean distinct-3 drops below 0.5
        collapse = next((a for a in sorted(cur)
                         if cur[a]["mean_distinct3_words"] < 0.5), None)
        out["axes"][axis] = {
            "grid": cu,
            "alpha_50_nonparametric": a50,
            "contrast_units_at_alpha50": (a50 * norm_l / u) if a50 is not None else None,
            "max_refusal_rate": float(max(rates)),
            "alpha_at_max_rate": float(amax),
            "contrast_units_at_max_rate": float(amax) * norm_l / u,
            "max_contrast_units_reached": max(v["contrast_units"] for v in cu.values()),
            "crosses_half": a50 is not None,
            "monotonic": bool(all(rates[i] <= rates[i + 1] + 1e-9
                                  for i in range(len(rates) - 1))),
            "inverted_u": bool(float(amax) < max(cur) and
                               max(rates) - cur[max(cur)]["rate"] > 0.05),
            "fluency_collapse_alpha": collapse,
            "fluency_collapse_before_ceiling": (
                None if collapse is None else bool(collapse <= float(amax))),
        }

    # ---- matched-contrast test (A vs B, and the nulls) --------------------
    mc = {}
    if "A_canned" in out["axes"] and "B_paraphrase" in out["axes"]:
        uA = norms["A_canned"]
        for other in [a for a in ("B_paraphrase", "C_stylistic", "D_random0",
                                  "E_prompt_contrast") if a in out["axes"]]:
            uO = norms[other]
            curA = _curve(rows_by_axis["A_canned"])
            curO = _curve(rows_by_axis[other])
            cs = sorted({float(a) * norm_l / uA for a in curA}
                        | {float(a) * norm_l / uO for a in curO})
            common = [c for c in cs
                      if _rate_at_c(curA, norm_l, uA, c) is not None
                      and _rate_at_c(curO, norm_l, uO, c) is not None]
            if not common:
                mc[other] = {"n_matched_levels": 0,
                             "note": "no overlapping contrast-unit range"}
                continue
            diffs = [(_rate_at_c(curA, norm_l, uA, c) - _rate_at_c(curO, norm_l, uO, c))
                     for c in common]
            # prompt-clustered bootstrap of the mean paired difference
            prompts = sorted({r["prompt_uid"] for r in rows_by_axis["A_canned"]})
            rng = np.random.default_rng(EL.BOOT_SEED)
            bs = []
            byA = {}
            byO = {}
            for r in rows_by_axis["A_canned"]:
                byA.setdefault(r["prompt_uid"], []).append(r)
            for r in rows_by_axis[other]:
                byO.setdefault(r["prompt_uid"], []).append(r)
            for _ in range(500):
                pick = rng.choice(prompts, size=len(prompts), replace=True)
                ra = [x for p in pick for x in byA.get(p, [])]
                ro = [x for p in pick for x in byO.get(p, [])]
                ca, co = _rate_curve(ra), _rate_curve(ro)
                dv = []
                for c in common:
                    x = _rate_at_c(ca, norm_l, uA, c)
                    yv = _rate_at_c(co, norm_l, uO, c)
                    if x is not None and yv is not None:
                        dv.append(x - yv)
                if dv:
                    bs.append(float(np.mean(dv)))
            lo, hi = EL.boot_ci(bs)
            mc[other] = {
                "n_matched_levels": len(common),
                "matched_contrast_range": [float(min(common)), float(max(common))],
                "mean_paired_diff_A_minus_other": float(np.mean(diffs)),
                "ci95": [lo, hi],
                "max_paired_diff": float(np.max(diffs)),
                "A_higher_at_all_matched_levels": bool(all(d >= 0 for d in diffs)),
                "per_level": [{"contrast_units": float(c),
                               "rate_A": _rate_at_c(curA, norm_l, uA, c),
                               "rate_other": _rate_at_c(curO, norm_l, uO, c)}
                              for c in common],
            }
    out["matched_contrast"] = mc
    return out


def analysis2(keys: list[str]) -> dict:
    per = {k: analysis2_checkpoint(k) for k in keys}
    votes = []
    for k, v in per.items():
        m = v["matched_contrast"].get("B_paraphrase")
        if not m or m.get("n_matched_levels", 0) == 0:
            continue
        votes.append((k, m["ci95"][0] > 0.0))
    n_yes = sum(1 for _, y in votes if y)
    verdict = ("NORM_MISMATCH_DOES_NOT_EXPLAIN" if n_yes >= (len(votes) // 2 + 1)
               else "MAGNITUDE_ARTIFACT" if votes else "NOT_EVALUABLE")
    return {"per_checkpoint": per, "matched_contrast_verdict": verdict,
            "matched_contrast_votes": {k: y for k, y in votes},
            "matched_contrast_reason":
                f"{n_yes}/{len(votes)} checkpoints keep A materially above B at matched "
                f"contrast units (lower CI of the paired difference > 0)"}


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    keys = [k for k in EL.CHECKPOINTS if (PROJ / f"{k}.npz").exists()]
    logger.info(f"analysis 1 over {keys}")
    a1 = analysis1(keys)
    (EL.RESULTS / "analysis1.json").write_text(json.dumps(a1, indent=1))
    logger.info(f"verdict: {a1['lexicality_verdict']} :: {a1['verdict_reason']}")
    keys2 = [k for k in EL.CHECKPOINTS
             if (EL.EXP1 / f"gens/{k}__A_canned.jsonl").exists()]
    a2 = analysis2(keys2)
    (EL.RESULTS / "analysis2.json").write_text(json.dumps(a2, indent=1))
    logger.info(f"matched-contrast verdict: {a2['matched_contrast_verdict']}")


if __name__ == "__main__":
    main()
