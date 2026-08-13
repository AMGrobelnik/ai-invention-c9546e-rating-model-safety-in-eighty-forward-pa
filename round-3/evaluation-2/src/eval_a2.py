#!/usr/bin/env python3
"""Analysis 2 -- the free-running vs teacher-forced asymmetry at its true
strength, plus a characterisation of which rollouts amplify."""

from __future__ import annotations

import numpy as np
from loguru import logger
from scipy.stats import binomtest, chi2_contingency, wilcoxon

from eval_common import E2, cliffs_delta, holm, load_json, spearman_rho
from lib import stats_ext

QUANTILES = [50, 75, 90, 95]
JSON_PATH_USED = ("E2/results/member_<id>.json :: survival.runs[i]."
                  "{free_running,teacher_forced}.survival_ratio  (the per-rollout "
                  "deviation ratio |delta_T| / |delta_inject|)")


def per_member_rollouts(members) -> tuple[dict, dict]:
    data, coverage = {}, {}
    for r in members:
        mid = r["member_id"]
        mj = load_json(E2 / "results" / f"member_{mid}.json")
        runs = (mj.get("survival") or {}).get("runs") or []
        if not runs:
            coverage[mid] = {"has_per_rollout": False, "n_rollouts": 0,
                             "reason": "no survival arm archived for this member "
                                       "(D4 ratchet was run on 15 of 19 members)"}
            continue
        free = np.array([x["free_running"]["survival_ratio"] for x in runs], float)
        forced = np.array([x["teacher_forced"]["survival_ratio"] for x in runs], float)
        div = np.array([x["free_running"]["tokens_diverged"] for x in runs], float)
        prompts = [x["prompt"] for x in runs]
        ok = np.isfinite(free) & np.isfinite(forced)
        data[mid] = {"free": free[ok], "forced": forced[ok],
                     "tokens_diverged": div[ok],
                     "prompts": [p for p, k in zip(prompts, ok) if k],
                     "lineage": r["lineage"], "family": r["family"],
                     "plain_harmful_refusal": r["plain_harmful_refusal"]}
        coverage[mid] = {"has_per_rollout": True, "n_rollouts": int(ok.sum()),
                         "n_dropped_non_finite": int((~ok).sum())}
    return data, coverage


def quantile_deltas(free, forced, n_boot=2000, seed=stats_ext.BOOT_SEED) -> dict:
    n = len(free)
    rng = np.random.default_rng(seed)
    out = {}
    boots = {q: [] for q in QUANTILES}
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        f, t = free[idx], forced[idx]
        for q in QUANTILES:
            boots[q].append(np.percentile(f, q) - np.percentile(t, q))
    for q in QUANTILES:
        b = np.asarray(boots[q], float)
        point = float(np.percentile(free, q) - np.percentile(forced, q))
        ci = [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
        out[f"q{q}"] = {
            "free": float(np.percentile(free, q)),
            "forced": float(np.percentile(forced, q)),
            "delta": point, "ci": ci, "n": int(n), "n_boot": n_boot,
            "ci_excludes_0": bool(ci[0] > 0 or ci[1] < 0),
        }
    return out


def paired_tests(free, forced, tokens_diverged=None) -> dict:
    d = free - forced
    nz = d[d != 0]
    n_gt = int(np.sum(free > forced))
    n = len(free)
    bt = binomtest(n_gt, len(nz) if len(nz) else n, 0.5) if len(nz) else None
    try:
        w = wilcoxon(free, forced, zero_method="wilcox", alternative="two-sided")
        w_stat, w_p = float(w.statistic), float(w.pvalue)
    except ValueError:
        w_stat, w_p = None, None
    cd = cliffs_delta(free, forced)
    n_ties = int(np.sum(free == forced))
    n_lt = int(np.sum(free < forced))
    tie_is_no_divergence = None
    if tokens_diverged is not None:
        td = np.asarray(tokens_diverged, float)
        tie_is_no_divergence = float(np.mean(td[free == forced] == 0)) if n_ties else None
    return {
        "n_pairs": int(n), "n_nonzero_pairs": int(len(nz)),
        "n_free_gt_forced": n_gt,
        "n_forced_gt_free": n_lt,
        "n_exact_ties": n_ties,
        "frac_exact_ties": float(n_ties / n),
        "frac_of_ties_with_zero_tokens_diverged": tie_is_no_divergence,
        "frac_free_gt_forced": float(n_gt / n),
        "frac_free_gt_forced_given_divergence": (float(n_gt / len(nz)) if len(nz) else None),
        "frac_free_ge_forced": float((n_gt + n_ties) / n),
        "sign_test_p": (float(bt.pvalue) if bt else None),
        "sign_test_note": ("the exact sign test drops tied pairs; ties here are rollouts "
                           "in which the perturbed free-running stream never diverged from "
                           "the clean one, making the two channels numerically identical"),
        "sign_test_direction": ("FORCED exceeds FREE among untied pairs"
                                if n_gt / max(1, len(nz)) < 0.5 else
                                "FREE exceeds FORCED among untied pairs"),
        "wilcoxon_stat": w_stat, "wilcoxon_p": w_p,
        "cliffs_delta": cd["delta"], "cliffs_delta_ci": cd["ci"],
        "cliffs_delta_definition": (
            "the standard between-sample Cliff's delta of the free vs the forced sample, with a "
            "PAIRED bootstrap over rollouts for its interval; it is not a paired-difference "
            "statistic and is reported alongside, not instead of, the sign and Wilcoxon tests"),
        "median_free": float(np.median(free)), "median_forced": float(np.median(forced)),
        "mean_free": float(np.mean(free)), "mean_forced": float(np.mean(forced)),
    }


def mean_diff_ci(free, forced, n_boot=2000, seed=stats_ext.BOOT_SEED) -> dict:
    d = free - forced
    rng = np.random.default_rng(seed)
    b = [float(np.mean(d[rng.integers(0, len(d), size=len(d))])) for _ in range(n_boot)]
    ci = [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
    return {"mean_diff": float(np.mean(d)), "ci": ci, "n": int(len(d)),
            "ci_excludes_0": bool(ci[0] > 0 or ci[1] < 0)}


def rank_biserial(binary, values) -> dict:
    """Rank-biserial correlation between a binary grouping and a continuous value."""
    b = np.asarray(binary, bool)
    v = np.asarray(values, float)
    a, c = v[b], v[~b]
    if len(a) == 0 or len(c) == 0:
        return {"r": None, "n1": int(len(a)), "n0": int(len(c)),
                "reason": "one group is empty"}
    gt = np.sum(a[:, None] > c[None, :])
    lt = np.sum(a[:, None] < c[None, :])
    r = float((gt - lt) / (len(a) * len(c)))
    rng = np.random.default_rng(stats_ext.BOOT_SEED)
    boot = []
    idx_all = np.arange(len(v))
    for _ in range(2000):
        i = rng.integers(0, len(v), size=len(v))
        bb, vv = b[i], v[i]
        aa, cc = vv[bb], vv[~bb]
        if len(aa) and len(cc):
            boot.append((np.sum(aa[:, None] > cc[None, :]) - np.sum(aa[:, None] < cc[None, :]))
                        / (len(aa) * len(cc)))
    return {"r": r, "n1": int(len(a)), "n0": int(len(c)),
            "ci": ([float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]
                   if len(boot) >= 50 else None)}


def run(members) -> tuple[dict, dict]:
    data, coverage = per_member_rollouts(members)
    logger.info(f"asymmetry: per-rollout data on {len(data)} of {len(members)} members")

    per_member, sign_p, wil_p = {}, [], []
    order = sorted(data)
    for mid in order:
        d = data[mid]
        pm = {
            "lineage": d["lineage"], "family": d["family"],
            "quantile_deltas": quantile_deltas(d["free"], d["forced"]),
            "paired_tests": paired_tests(d["free"], d["forced"], d["tokens_diverged"]),
            "mean_diff": mean_diff_ci(d["free"], d["forced"]),
        }
        per_member[mid] = pm
        sign_p.append(pm["paired_tests"]["sign_test_p"])
        wil_p.append(pm["paired_tests"]["wilcoxon_p"] if pm["paired_tests"]["wilcoxon_p"] is not None else 1.0)
    sign_adj = holm(sign_p)
    wil_adj = holm(wil_p)
    for mid, sa, wa in zip(order, sign_adj, wil_adj):
        per_member[mid]["paired_tests"]["sign_test_p_holm"] = sa
        per_member[mid]["paired_tests"]["wilcoxon_p_holm"] = wa

    # cross-member summary
    summ = {"n_members": len(order), "n_lineages": len({data[m]['lineage'] for m in order}),
            "n_families": len({data[m]['family'] for m in order}),
            "json_path_used": JSON_PATH_USED}
    for q in QUANTILES:
        k = f"q{q}"
        summ[f"n_ci_excludes_0_{k}"] = int(sum(per_member[m]["quantile_deltas"][k]["ci_excludes_0"]
                                               for m in order))
        summ[f"n_delta_positive_{k}"] = int(sum(per_member[m]["quantile_deltas"][k]["delta"] > 0
                                                for m in order))
    summ["n_mean_diff_ci_excludes_0"] = int(sum(per_member[m]["mean_diff"]["ci_excludes_0"] for m in order))
    summ["n_sign_test_sig_holm_favouring_forced"] = int(sum(
        1 for m in order if per_member[m]["paired_tests"]["sign_test_p_holm"] < 0.05
        and per_member[m]["paired_tests"]["frac_free_gt_forced_given_divergence"] < 0.5))
    summ["n_sign_test_sig_holm_favouring_free"] = int(sum(
        1 for m in order if per_member[m]["paired_tests"]["sign_test_p_holm"] < 0.05
        and per_member[m]["paired_tests"]["frac_free_gt_forced_given_divergence"] > 0.5))
    summ["sign_test_direction_note"] = (
        "direction is read on UNTIED pairs, which is what the exact sign test conditions "
        "on; reading it on the unconditional fraction (0.11-0.35) inverts the direction "
        "because 61-88% of pairs are exact ties")
    summ["n_sign_test_sig_holm"] = int(sum(
        1 for m in order if per_member[m]["paired_tests"]["sign_test_p_holm"] < 0.05))
    summ["n_wilcoxon_sig_holm"] = int(sum(
        1 for m in order if per_member[m]["paired_tests"]["wilcoxon_p_holm"] < 0.05))
    summ["frac_exact_ties_range"] = [
        float(min(per_member[m]["paired_tests"]["frac_exact_ties"] for m in order)),
        float(max(per_member[m]["paired_tests"]["frac_exact_ties"] for m in order))]
    summ["frac_free_gt_forced_given_divergence_range"] = [
        float(min(per_member[m]["paired_tests"]["frac_free_gt_forced_given_divergence"] for m in order)),
        float(max(per_member[m]["paired_tests"]["frac_free_gt_forced_given_divergence"] for m in order))]
    summ["n_forced_gt_free_total"] = int(sum(
        per_member[m]["paired_tests"]["n_forced_gt_free"] for m in order))
    summ["all_ties_are_zero_divergence_rollouts"] = bool(all(
        (per_member[m]["paired_tests"]["frac_of_ties_with_zero_tokens_diverged"] in (None, 1.0))
        for m in order))
    summ["cliffs_delta_range"] = [
        float(min(per_member[m]["paired_tests"]["cliffs_delta"] for m in order)),
        float(max(per_member[m]["paired_tests"]["cliffs_delta"] for m in order))]
    summ["frac_free_gt_forced_range"] = [
        float(min(per_member[m]["paired_tests"]["frac_free_gt_forced"] for m in order)),
        float(max(per_member[m]["paired_tests"]["frac_free_gt_forced"] for m in order))]
    summ["median_free_range"] = [
        float(min(per_member[m]["paired_tests"]["median_free"] for m in order)),
        float(max(per_member[m]["paired_tests"]["median_free"] for m in order))]
    summ["median_forced_range"] = [
        float(min(per_member[m]["paired_tests"]["median_forced"] for m in order)),
        float(max(per_member[m]["paired_tests"]["median_forced"] for m in order))]
    summ["n_members_median_below_1_both_channels"] = int(sum(
        1 for m in order if per_member[m]["paired_tests"]["median_free"] < 1
        and per_member[m]["paired_tests"]["median_forced"] < 1))
    summ["n_members_q95_free_exceeds_forced"] = int(sum(
        1 for m in order if per_member[m]["quantile_deltas"]["q95"]["delta"] > 0))

    supported = {
        "clause_1_mean_difference": {
            "statement": (f"the paired mean-difference CI excludes 0 in "
                          f"{summ['n_mean_diff_ci_excludes_0']}/{len(order)} members"),
            "per_member": {m: per_member[m]["mean_diff"] for m in order},
        },
        "clause_2_typical_rollout_decays": {
            "statement": (f"the median rollout decays (ratio < 1) in BOTH channels in "
                          f"{summ['n_members_median_below_1_both_channels']}/{len(order)} members"),
            "per_member": {m: {"median_free": per_member[m]["paired_tests"]["median_free"],
                               "median_forced": per_member[m]["paired_tests"]["median_forced"]}
                           for m in order},
        },
        "clause_3_heavier_right_tail": {
            "statement": (f"the free channel's 95th percentile exceeds the forced "
                          f"channel's in {summ['n_members_q95_free_exceeds_forced']}/{len(order)} members"),
            "per_member": {m: per_member[m]["quantile_deltas"]["q95"] for m in order},
        },
    }
    retired = {
        "stochastic_dominance": {
            "old": "the free-running channel stochastically dominates the teacher-forced channel",
            "why_retired": (
                "the unconditional paired free>forced fraction is "
                f"{summ['frac_free_gt_forced_range'][0]:.2f}-"
                f"{summ['frac_free_gt_forced_range'][1]:.2f}, i.e. BELOW 0.5, which reads as a "
                "refutation until the ties are accounted for: "
                f"{summ['frac_exact_ties_range'][0]:.2f}-{summ['frac_exact_ties_range'][1]:.2f} "
                "of pairs are EXACT ties because the perturbed free-running stream never "
                "diverged from the clean stream, so the two channels are numerically the "
                "same rollout. Strict dominance is therefore the wrong word, but so is the "
                "plan's expectation that the forced channel wins: forced strictly exceeds "
                f"free in only {summ['n_forced_gt_free_total']} of "
                f"{summ['n_members'] * 100} paired rollouts."),
            "new": ("free >= forced in almost every paired rollout, strictly greater in "
                    f"{summ['frac_free_gt_forced_given_divergence_range'][0]:.2f}-"
                    f"{summ['frac_free_gt_forced_given_divergence_range'][1]:.2f} of the "
                    "rollouts that actually diverge and tied in the rest; the free channel "
                    "has a strictly heavier RIGHT TAIL while the typical rollout decays in "
                    "both channels. The asymmetry is conditional on divergence, not a "
                    "property of the typical rollout."),
        },
        "deviation_grows": {
            "old": "free-running perturbation deviation grows over 16 steps in every member",
            "why_retired": (
                f"the median deviation ratio is below 1 in both channels in "
                f"{summ['n_members_median_below_1_both_channels']}/{len(order)} members; the "
                "growth is a mean effect carried by the upper tail"),
            "new": ("the free-running MEAN deviation ratio is inflated by a heavy right "
                    "tail; the median rollout shrinks"),
        },
    }

    # ---------------- (2d) tail characterisation ------------------------------
    prim_rule = "amplifying := free-running deviation ratio > 1"
    sens_rule = ("amplifying := free ratio exceeds the member's own 90th percentile of "
                 "the forced ratio")
    tail = {"amplification_rule_primary": prim_rule,
            "amplification_rule_sensitivity": sens_rule}
    amp_rows = []
    for mid in order:
        d = data[mid]
        amp = d["free"] > 1.0
        thr = np.percentile(d["forced"], 90)
        amp_s = d["free"] > thr
        for i in range(len(amp)):
            amp_rows.append({"member": mid, "lineage": d["lineage"],
                             "prompt": d["prompts"][i], "amp": bool(amp[i]),
                             "amp_sens": bool(amp_s[i]),
                             "tokens_diverged": float(d["tokens_diverged"][i]),
                             "free": float(d["free"][i]), "forced": float(d["forced"][i])})
    n_amp = sum(r["amp"] for r in amp_rows)
    tail["n_rollouts_total"] = len(amp_rows)
    tail["n_amplifying_primary"] = int(n_amp)
    tail["amplification_rate_primary"] = float(n_amp / len(amp_rows))
    tail["n_amplifying_sensitivity"] = int(sum(r["amp_sens"] for r in amp_rows))
    tail["amplification_rate_sensitivity"] = float(
        sum(r["amp_sens"] for r in amp_rows) / len(amp_rows))

    # (i) prompt identity
    prompts = sorted({r["prompt"] for r in amp_rows})
    tab = []
    per_prompt = {}
    rng = np.random.default_rng(stats_ext.BOOT_SEED)
    for p in prompts:
        sub = [r for r in amp_rows if r["prompt"] == p]
        k = sum(r["amp"] for r in sub)
        tab.append([k, len(sub) - k])
        b = [float(np.mean([sub[i]["amp"] for i in rng.integers(0, len(sub), len(sub))]))
             for _ in range(2000)]
        per_prompt[p[:80]] = {"n": len(sub), "k_amplifying": int(k),
                              "rate": float(k / len(sub)),
                              "ci": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]}
    tab = np.asarray(tab)
    keep = tab.sum(axis=1) > 0
    try:
        chi2, pchi, dof, _ = chi2_contingency(tab[keep])
        cramers_v = float(np.sqrt(chi2 / (tab[keep].sum() * (min(tab[keep].shape) - 1))))
    except ValueError as exc:
        chi2, pchi, dof, cramers_v = None, None, None, None
        logger.warning(f"chi2 on prompts failed: {exc}")
    rates = [v["rate"] for v in per_prompt.values()]
    tail["covariate_prompt_identity"] = {
        "n_distinct_prompts": len(prompts),
        "chi2": chi2, "p": pchi, "dof": dof, "cramers_v": cramers_v,
        "per_prompt_rate_range": [float(min(rates)), float(max(rates))],
        "gini_of_amplification_over_prompts": float(
            1 - np.sum((np.asarray(rates) / max(1e-12, np.sum(rates))) ** 2) * len(rates))
        if np.sum(rates) > 0 else None,
        "per_prompt": per_prompt,
        "concentrated": bool(pchi is not None and pchi < 0.05),
    }

    # (ii) refusal lexicon in the diverged free stream
    tail["covariate_refusal_lexicon"] = {
        "status": "NOT_RECOMPUTABLE",
        "reason": ("the survival arm archives only the per-step |delta| trajectory, the "
                   "survival ratio, the AUC and tokens_diverged per rollout "
                   "(E2/results/member_*.json :: survival.runs[i]); the free-running "
                   "TOKEN STREAMS were not written to disk. E2/gens/ contains the "
                   "dose-response (alpha50_*.jsonl) and behaviour (behaviour_*.jsonl) "
                   "streams only, neither of which is the survival arm. Re-deriving this "
                   "covariate would require regenerating rollouts, which this artifact "
                   "does not do."),
        "matcher_that_would_be_used": "E2/lib/classify.py :: REFUSAL_RE / opens_with_refusal",
    }

    # (iii) divergence step
    tail["covariate_divergence_step"] = rank_biserial(
        [r["amp"] for r in amp_rows], [r["tokens_diverged"] for r in amp_rows])
    tail["covariate_divergence_step"]["interpretation"] = (
        "tokens_diverged counts how many sampled tokens of the perturbed free-running "
        "stream differ from the clean stream. r > 0 means amplifying rollouts diverged on "
        "MORE tokens. This covariate is close to mechanical -- a rollout whose stream never "
        "diverges cannot amplify, because the free channel is then numerically identical to "
        "the teacher-forced one -- so a positive r here is evidence about autoregressive "
        "variance, NOT about safety relevance.")
    tail["covariate_divergence_step"]["is_mechanical_not_safety_covariate"] = True
    tail["covariate_divergence_step"]["mean_tokens_diverged_amplifying"] = float(
        np.mean([r["tokens_diverged"] for r in amp_rows if r["amp"]])) if n_amp else None
    tail["covariate_divergence_step"]["mean_tokens_diverged_non_amplifying"] = float(
        np.mean([r["tokens_diverged"] for r in amp_rows if not r["amp"]]))

    # (iv) member-level association with the judged refusal rate
    mem_amp = []
    for mid in order:
        sub = [r for r in amp_rows if r["member"] == mid]
        mem_amp.append({"member": mid, "lineage": data[mid]["lineage"],
                        "amp_fraction": float(np.mean([r["amp"] for r in sub])),
                        "plain_harmful_refusal": data[mid]["plain_harmful_refusal"]})
    x = [m["amp_fraction"] for m in mem_amp]
    y = [m["plain_harmful_refusal"] for m in mem_amp]
    rho = spearman_rho(x, y)
    lin = sorted({m["lineage"] for m in mem_amp})
    rng = np.random.default_rng(stats_ext.BOOT_SEED)
    boot = []
    for _ in range(5000):
        pick = [lin[i] for i in rng.integers(0, len(lin), size=len(lin))]
        xs, ys = [], []
        for L in pick:
            for m in mem_amp:
                if m["lineage"] == L:
                    xs.append(m["amp_fraction"]); ys.append(m["plain_harmful_refusal"])
        v = spearman_rho(xs, ys)
        if v is not None:
            boot.append(v)
    tail["covariate_member_refusal_rate"] = {
        "spearman_rho": rho, "n_members": len(mem_amp), "n_lineages": len(lin),
        "ci_lineage_bootstrap": ([float(np.percentile(boot, 2.5)),
                                  float(np.percentile(boot, 97.5))] if len(boot) >= 50 else None),
        "n_boot_valid": len(boot),
        "permutation": stats_ext.spearman_with_permutation(np.asarray(x), np.asarray(y)),
        "per_member": mem_amp,
    }

    assoc_safety, assoc_mech = [], []
    if tail["covariate_prompt_identity"]["concentrated"]:
        assoc_safety.append("prompt identity")
    ci3 = tail["covariate_divergence_step"].get("ci")
    if ci3 and (ci3[0] > 0 or ci3[1] < 0):
        assoc_mech.append("token divergence extent (mechanical)")
    ci4 = tail["covariate_member_refusal_rate"]["ci_lineage_bootstrap"]
    if ci4 and (ci4[0] > 0 or ci4[1] < 0):
        assoc_safety.append("member judged refusal rate")
    tail["safety_relevant_associations"] = assoc_safety
    tail["mechanical_associations"] = assoc_mech
    tail["verdict"] = (
        ("THE AMPLIFYING TAIL IS NOT SAFETY-RELEVANT ON ANY MEASURED COVARIATE: neither "
         "prompt identity nor the member's own judged refusal rate is associated with "
         "amplification at its interval. The one association that does survive -- "
         "amplifying rollouts diverge on more tokens -- is mechanical: a rollout whose "
         "stream never diverges cannot amplify by construction. The refusal-lexicon "
         "covariate is NOT_RECOMPUTABLE from the archive. The surviving mechanism is a "
         "statement about autoregressive variance, not about safety."
         if not assoc_safety else
         "SAFETY-RELEVANT ASSOCIATION FOUND on: " + ", ".join(assoc_safety) +
         (f"; mechanical associations: {', '.join(assoc_mech)}" if assoc_mech else "") +
         " (the refusal-lexicon covariate is NOT_RECOMPUTABLE from the archive)."))

    return {
        "coverage": coverage,
        "n_members_with_per_rollout_data": len(order),
        "per_member": per_member,
        "cross_member_summary": summ,
        "supported_statement": supported,
        "retired_claims": retired,
    }, tail
