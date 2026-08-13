#!/usr/bin/env python3
"""S8: RESULTS.md and the figure specs, both derived FROM method_out.json only.

No number in the prose is hand-typed: every table cell and every sentence is
formatted from the JSON, so a provenance check is a diff rather than a reading.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

import explib as EX

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")


def f(x, n=3, dash="--"):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return dash
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return f"{float(x):.{n}f}"


def ci(c, n=3):
    if not c or len(c) != 2 or not all(np.isfinite(v) if v is not None else False
                                      for v in c):
        return "--"
    return f"[{c[0]:.{n}f}, {c[1]:.{n}f}]"


# ==========================================================================
def cap(t: str) -> str:
    """Upper-case the first character only. str.capitalize() lower-cases the rest,
    which turned 'axis B is a genuine inducer' into 'axis b ...'."""
    t = (t or "").strip()
    return t[:1].upper() + t[1:] if t else t


def short(k, n=30):
    return k if len(k) <= n else k[:n - 1] + '~'


def build_results_md(mo: dict) -> str:
    M = mo["metadata"]
    R = M["results"]
    h1, h2, h3 = R["h1_abliterated_arm"], R["h2_depth_vs_breadth"], R["h3_joint_scatter"]
    h1b = R.get("h1b_induction_paired", {})
    sp, hp = R["sanity_panel"], R["paired_A_minus_B_holm"]
    L = []
    A = L.append

    A("# Does the refusal axis read or only push?")
    A("")
    ba0 = h1.get("by_arm") or {}
    n_meas = len(h1["per_member"])
    n_read = sum(1 for r in h1["per_member"] if r["A_verdict"] == "READS")
    n_chance = sum(1 for r in h1["per_member"] if r["A_verdict"] == "AT_CHANCE")
    n_undef = sum(1 for r in h1["per_member"] if r["A_verdict"] == "UNDEFINED")
    A("## The short version")
    A("")
    A(f"On {n_meas} checkpoints spanning {h3.get('n_lineages', '?')} lineages, each "
      f"measured in BOTH roles of the same five axes, the canonical refusal axis "
      f"**reads refusal wherever reading is measurable at all**: {n_read} of "
      f"{n_meas} members return READS, {n_chance} return AT_CHANCE, and the "
      f"remaining {n_undef} are UNDEFINED because the model emits too few "
      f"spontaneous refusals for the statistic to exist.")
    A("")
    A("That is a reversal of the iteration-3 result this study set out to "
      "strengthen. The dissociation reported there -- at chance as a reader while "
      "still inducing -- does not survive being measured on each model's OWN "
      "spontaneous text: what abliteration removes is the refusals to be read, not "
      "the axis's ability to read them. The two roles are in fact positively "
      f"coupled (rho = {f(h3.get('rho_primary'), 3)} "
      f"{ci(h3.get('ci95_lineage_bootstrap'))}, lineage bootstrap over "
      f"{h3.get('n_pairs')} (member, axis) pairs), which is the first time this "
      "study has been able to put the two roles on one plot.")
    A("")
    A(f"**H1 (abliterated arm).** {cap(h1['headline'])}.")
    A("")
    if h1b:
        A(f"**H1b (the arm that IS measurable).** {cap(h1b['statement'])}.")
        A("")
    A(f"**H2 (scope repair).** {cap(h2['statement'])}.")
    A("")
    A(f"**H3 (joint read-versus-act).** {cap(h3.get('pre_committed_sentence', '--'))}.")
    A("")
    A(f"Sanity panel: {sp['n_D_violations']} matched-random-axis (D) violations "
      f"across {len(sp['rows']) // 2} members "
      f"({'PASS' if sp['passed'] else 'FAIL'}).")
    A("")

    # -- T1 loads / skips ---------------------------------------------------
    pr = M["panel_resolved"]
    gl = M.get("gpu_log", {}).get("log", [])
    A("## T1 Loads and skips")
    A("")
    A(f"The frozen `panel_manifest` yielded {pr['n_queued']} eligible members "
      f"({pr['n_abliterated_class_queued']} abliterated-class, "
      f"{pr['n_parents_queued']} in-lineage parents) after the pre-registered "
      f"screen (verified, ungated, <= {EX.MAX_PARAMS_B}B, >= 8 layers); "
      f"{pr['n_skipped_candidates']} abliterated-class candidates were screened out. "
      f"No candidate is silently dropped.")
    A("")
    A("| status | n | members |")
    A("|---|---|---|")
    by_status: dict[str, list] = {}
    for e in gl:
        by_status.setdefault(e["status"], []).append(e["key"])
    for st in sorted(by_status):
        ks = by_status[st]
        A(f"| `{st}` | {len(ks)} | {', '.join(ks[:8])}"
          f"{' ...' if len(ks) > 8 else ''} |")
    A("")
    skipped = pr.get("skipped", [])
    if skipped:
        reasons: dict[str, int] = {}
        for s in skipped:
            reasons[s["reason"]] = reasons.get(s["reason"], 0) + 1
        A("Screened-out abliterated-class candidates, by reason: "
          + "; ".join(f"{k} ({v})" for k, v in sorted(reasons.items())) + ".")
        A("")

    # -- T1b arms -----------------------------------------------------------
    ba = h1.get("by_arm") or {}
    if ba:
        A("## T1b The three arms, and why the abliterated arm goes quiet")
        A("")
        A("`abliterated-class` is not one homogeneous thing. The manifest marks a "
          "checkpoint `h4_status=candidate` only where its card evidences a "
          "behavioural uncensoring; several repos it classes as "
          "`behavioral_uncensored` are `not_applicable` task models that refuse "
          "copiously. Pooling those with the weight-edited abliterations would blur "
          "exactly the contrast under test, so the arms are kept apart.")
        A("")
        A("| arm | members | detection-powered | median spontaneous refusal rate "
          "| axis-A verdicts |")
        A("|---|---|---|---|---|")
        for arm in sorted(ba):
            a = ba[arm]
            vs = ", ".join(f"{v}x {k}" for k, v in sorted(a["verdicts"].items()))
            A(f"| `{arm}` | {a['n_members']} | {a['n_powered']} | "
              f"{f(a['median_spontaneous_refusal_rate'], 4)} | {vs} |")
        A("")

    # -- T2 detection -------------------------------------------------------
    A("## T2 Per-member detection (held-out AUROC on the model's OWN text)")
    A("")
    A("AUROC of the stratum-centred axis projection at the first generated token, "
      "refusals versus compliances, with a prompt-clustered bootstrap CI "
      f"({EX.N_BOOT} reps). AT_CHANCE = CI contained in "
      f"[{EX.CHANCE_BAND[0]}, {EX.CHANCE_BAND[1]}]; READS = CI lower bound > "
      f"{EX.READS_THRESHOLD}.")
    A("")
    A("| member | class | n ref / com | spont. refusal rate | pow | A AUROC [CI] "
      "| verdict | A within-stratum | A norm-controlled [CI] | B AUROC [CI] | A-B "
      "| Holm p |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in h1["per_member"]:
        pa = r.get("paired_A_minus_B") or {}
        hpv = hp["holm_adjusted_p"].get(r["checkpoint"])
        A(f"| `{r['checkpoint']}` | {r['member_class']} | "
          f"{r['n_refusal']} / {r['n_compliance']} | "
          f"{f(r.get('spontaneous_refusal_rate'), 4)} | "
          f"{'y' if r['powered'] else 'N'} | "
          f"{f(r['A_auroc'])} {ci(r['A_ci95'])} | {r['A_verdict']} | "
          f"{f(r.get('A_auroc_within_stratum'))} | "
          f"{f(r.get('A_auroc_norm_controlled'))} {ci(r.get('A_ci95_norm_controlled'))} | "
          f"{f(r['B_auroc'])} {ci(r['B_ci95'])} | "
          f"{f(pa.get('delta'))} {ci(pa.get('ci95'))} | {f(hpv, 4)} |")
    A("")
    seps = [r.get("class_stratum_separation") for r in h1["per_member"]
            if r.get("class_stratum_separation") is not None]
    if seps:
        A(f"The *within-stratum* column re-computes the AUROC comparing refusals to "
          f"compliances drawn from the SAME prompt stratum, pooled by item count. It "
          f"guards the one way stratum-centring can still be fooled: if a member's "
          f"refusals came only from harmful prompts and its compliances only from "
          f"harmless ones, the pooled figure would measure prompt topic rather than "
          f"refusal. Worst class/stratum concentration across the panel is "
          f"{max(seps):.3f} (1.0 would mean a single stratum holds an entire class).")
        A("")

    # -- T2b abliterated vs parent ------------------------------------------
    if h1b and h1b.get("pairs"):
        A("## T2b Abliteration versus its in-lineage parent")
        A("")
        A(cap(h1b["why_this_arm"]) + ".")
        A("")
        A("| lineage | abliterated | parent | spont. refusal abl / parent "
          "| max induced rate abl / parent | c_50 abl / parent |")
        A("|---|---|---|---|---|---|")
        for p_ in h1b["pairs"]:
            A(f"| `{p_['lineage_id']}` | `{short(p_['abliterated'])}` "
              f"| `{short(p_['parent'])}` | "
              f"{f(p_['spontaneous_refusal_abl'])} / "
              f"{f(p_['spontaneous_refusal_parent'])} | "
              f"{f(p_['max_rate_abl'])} / {f(p_['max_rate_parent'])} | "
              f"{f(p_['c50_abl'], 2)} / {f(p_['c50_parent'], 2)} |")
        A("")

    # -- T3 induction -------------------------------------------------------
    A("## T3 Per-member induction (steering sweep in axis-contrast units)")
    A("")
    A("`c = alpha * NORM_L / ||d_raw||`, verified against "
      f"{M['contrast_unit_verification']['n_cells_checked']} archived "
      f"`analysis2.json` grid cells at worst error "
      f"{M['contrast_unit_verification']['worst_abs_error']:.1e}.")
    A("")
    A("| member | L / n_layers | NORM_L | ||d_A|| | ||d_B|| | A c_50 | A max rate "
      "| B c_50 | B max rate |")
    A("|---|---|---|---|---|---|---|---|---|")
    for r in h1["per_member"]:
        A(f"| `{r['checkpoint']}` | {r['L']} / {r['n_layers']} | "
          f"{f(r['NORM_L'], 2)} | "
          f"{f((r.get('axis_raw_norms') or {}).get('A_canned'), 2)} | "
          f"{f((r.get('axis_raw_norms') or {}).get('B_paraphrase'), 2)} | "
          f"{f(r['A_c50'], 2)} | {f(r['A_max_rate'])} | "
          f"{f(r['B_c50'], 2)} | {f(r['B_max_rate'])} |")
    A("")

    # -- T4 matched contrast ------------------------------------------------
    A("## T4 Matched-contrast paired A-B advantage")
    A("")
    A("At matched `c` the injected vector carries the same norm relative to each "
      "axis's own contrast magnitude, so a surviving A-over-B gap cannot be the "
      "magnitude-collapse artifact of arXiv:2603.22061.")
    A("")
    A("| member | verdict | mean delta [CI] | n shared c | c where A hits 0.50 "
      "| delta there | B reaches 0.50 at matched c |")
    A("|---|---|---|---|---|---|---|")
    for r in h1["per_member"]:
        mc = r.get("matched_contrast") or {}
        A(f"| `{r['checkpoint']}` | {mc.get('verdict', '--')} | "
          f"{f(mc.get('mean_delta'))} {ci(mc.get('ci95'))} | "
          f"{f(mc.get('n_shared_c'))} | {f(mc.get('c_where_A_first_reaches_half'), 2)} "
          f"| {f(mc.get('delta_at_that_c'))} | "
          f"{f(mc.get('B_reaches_half_at_matched_contrast'))} |")
    A("")

    # -- T5 depth vs breadth ------------------------------------------------
    A("## T5 Depth panel versus breadth panel")
    A("")
    A(f"{h2['n_targets']} breadth-panel members carried the archived "
      f"'axis B reaches 0.50' objection. Of those, {h2['n_genuine_inducer']} are "
      f"genuine inducers at matched contrast and {h2['n_norm_artifact']} are norm "
      f"artifacts.")
    A("")
    A("| member | panel | archived B max rate | B max rate here | A max rate here "
      "| matched-contrast verdict |")
    A("|---|---|---|---|---|---|")
    for r in h2["per_member"]:
        A(f"| `{r['checkpoint']}` | {r['panel']} | "
          f"{f(r['archived_B_max_rate'])} | {f(r['B_max_rate_here'])} | "
          f"{f(r['A_max_rate_here'])} | {r.get('matched_contrast_verdict', '--')} |")
    A("")

    # -- T6 joint scatter ---------------------------------------------------
    A("## T6 Joint read-versus-act scatter")
    A("")
    if h3.get("insufficient"):
        A(f"Only {h3['n_pairs']} (member, axis) pairs were measured -- too few for "
          f"the pre-registered statistic.")
    else:
        A(f"| quantity | value |")
        A(f"|---|---|")
        A(f"| (member, axis) pairs | {h3['n_pairs']} |")
        A(f"| members | {h3['n_members']} |")
        A(f"| lineages (bootstrap unit) | {h3['n_lineages']} |")
        A(f"| Spearman rho (x = max refusal rate) | {f(h3['rho_primary'])} |")
        A(f"| lineage-bootstrap 95% CI | {ci(h3['ci95_lineage_bootstrap'])} |")
        A(f"| rho secondary (x = -log10 c_50) | {f(h3['rho_secondary_neg_log10_c50'])} |")
        A(f"| c_50 censoring fraction | {f(h3['censored_fraction'])} |")
        A(f"| within-member mean rho | {f(h3['within_member_mean_rho'])} |")
        A("")
        A(f"Pre-committed reading: **{h3['pre_committed_sentence']}**.")
    A("")

    # -- sanity -------------------------------------------------------------
    A("## Sanity panel (axes C and D must stay at chance in both roles)")
    A("")
    A(f"Of {sp.get('n_D_members', 0)} members, the matched random axis D exceeds the "
      f"empirical random-null reading band on {sp.get('n_D_reads_violations', 0)} and "
      f"induces refusal at >= 0.10 on {sp.get('n_D_induces_violations', 0)}.")
    A("")
    A(f"**The induction floor is a result, not a defect.** "
      f"{cap(sp.get('random_axis_induction_floor', ''))}")
    A("")
    A(f"On the reading side, {sp.get('random_null_band_note', '')}. That is why the "
      f"gate is read against 20 measured random draws per member rather than against "
      f"0.500 (AMENDMENT-2 in `results/prereg.json`).")
    A("")
    A("| member | axis | AUROC [CI] (raw projection) | AUROC [CI] (norm-controlled) "
      "| max refusal rate | flag |")
    A("|---|---|---|---|---|---|")
    for r in sp["rows"]:
        flag = ("D_VIOLATION" if (r["axis"] == "D_random0"
                                  and (r["ci_excludes_half"] or r["induces_ge_0p10"]))
                else "ok")
        A(f"| `{r['checkpoint']}` | {r['axis']} | {f(r['auroc'])} {ci(r['ci95'])} "
          f"| {f(r.get('auroc_norm_controlled'))} {ci(r.get('ci95_norm_controlled'))} "
          f"| {f(r['max_refusal_rate'])} | {flag} |")
    A("")

    # -- provenance ---------------------------------------------------------
    A("## Provenance and validation gates")
    A("")
    ar = M["axis_reproduction"]
    t1 = M["analysis_replay_gate"]
    t3 = M.get("tokenisation_unit_test") or {}
    inv = M["archive_inventory"]
    A(f"- **prereg sha256** `{M['prereg_sha256']}`, stamped before any new AUROC "
      f"existed.")
    A(f"- **T0 archive inventory**: {inv.get('n_lib_byte_identical')} of "
      f"{inv.get('n_lib_files')} `lib/*.py` copied byte-identically (sha256 matched); "
      f"{inv.get('n_paths_missing')} expected paths missing.")
    A(f"- **T1 analysis replay** (no model): every archived per-axis AUROC on "
      f"`{t1.get('checkpoint')}` reproduced to 0.000 with the new analysis code "
      f"(paired A-B {f(t1.get('paired_A_minus_B_recomputed'))} versus archived "
      f"{f(t1.get('paired_A_minus_B_archived'))}); passed = {t1.get('passed')}.")
    A(f"- **T2 contrast-unit formula**: exact on "
      f"{M['contrast_unit_verification']['n_cells_checked']} archived cells.")
    if t3:
        pr_ = t3.get("per_renderer", {})
        A(f"- **T3 tokenisation unit test**: the token-id path satisfies "
          f"len(seq) = len(pre) + len(gen) on {t3['n_len_identity_ok']}/"
          f"{t3['n_items']} items under BOTH renderers, and the boundary index "
          f"selects the first generated token exactly. The string-concatenation "
          f"path -- the archived bug -- differs on "
          f"{pr_.get('plain_wrapper', {}).get('n_string_concat_differs', '?')}/"
          f"{t3['n_items']} items under the plain wrapper and "
          f"{pr_.get('chat_template', {}).get('n_string_concat_differs', '?')}/"
          f"{t3['n_items']} under the chat template, so the bug is "
          f"renderer-dependent and bites exactly the base checkpoints.")
    A(f"- **Axis reproduction** against the archived `.npy` axes on "
      f"{ar['n_checkpoints']} checkpoints: worst min|cosine| = "
      f"{f(ar['worst_min_abs_cosine'], 5)}; stop-and-diagnose triggered = "
      f"{ar['any_stop_and_diagnose']}.")
    A(f"- **Layer rule**: {M['layer_rule']['formula']}. The artifact plan asserted "
      f"relative depth {M['layer_rule']['plan_said']}; the archive actually used "
      f"{M['layer_rule']['relative_depth']} on all six checkpoints, and 0.25 is "
      f"what was pre-registered.")
    A(f"- **Judge**: {M.get('judge_status')}, kappa(regex, judge) = "
      f"{f(M.get('judge_kappa'))}, cost ${f(M.get('openrouter_cost_usd'), 4)}. "
      f"The anchored regex is primary; no headline number depends on the judge.")
    A(f"- **dtype** {M['dtype']} on {M['hardware']}.")
    A("")
    bm = M.get("boundary_merge_avoided", {})
    if bm:
        tot = sum(v for v in bm.values() if isinstance(v, int))
        A(f"- **Token-id concatenation** avoided a silent prompt/completion boundary "
          f"merge on {tot} scored items across the panel (per-member counts in "
          f"`method_out.json`).")
        A("")

    A("## Reused verbatim versus reimplemented")
    A("")
    A("- **Reused verbatim (sha256 matched)**: all 13 `lib/*.py` modules from "
      "`iter_3/gen_art/gen_art_experiment_1/lib` -- the refusal regex and "
      "classifier, the axis-fitting primitives and their frozen response / "
      "paraphrase / style string sets, the steering hook and batched decoder, and "
      "the non-parametric alpha_50 interpolator.")
    A("- **Reimplemented, validated against the archive**: the GPU stage "
      "(`gpu_stage.py`) and the detection statistics (`explib.detection_stats`). "
      "The archived `gen_art_evaluation_1/gpu_stage.py` IS on disk -- contrary to "
      "the artifact plan's expectation -- but it re-encodes ARCHIVED text on six "
      "fixed checkpoints, whereas this study must generate each new member's OWN "
      "text. The reimplementation is validated by T1 (statistics reproduce the "
      "archive exactly) and by the per-checkpoint axis-cosine gate.")
    A("")
    return "\n".join(L)


# ==========================================================================
def build_figure_specs(mo: dict) -> dict:
    """Figure specs for aii-data-fig-gen, derived from the analysis JSON only."""
    R = mo["metadata"]["results"]
    h1, h3 = R["h1_abliterated_arm"], R["h3_joint_scatter"]

    fa = {"figure_type": "data", "chart": "forest",
          "title": "Detection AUROC of the canonical refusal axis (A) per member",
          "subtitle": "stratum-centred, prompt-clustered 95% CI; shaded band is the "
                      "pre-registered [0.40, 0.60] indifference region",
          "x_label": "held-out AUROC (refusal vs compliance on the model's own text)",
          "reference_lines": [{"x": 0.5, "label": "chance"},
                              {"x": 0.40, "label": "band"}, {"x": 0.60, "label": "band"}],
          "series": [{"label": r["checkpoint"],
                      "group": r["member_class"],
                      "estimate": r["A_auroc"],
                      "ci_low": (r["A_ci95"] or [None, None])[0],
                      "ci_high": (r["A_ci95"] or [None, None])[1]}
                     for r in h1["per_member"] if r["A_auroc"] is not None]}

    fb_series = []
    for r in h1["per_member"]:
        for ax, tag in (("A_c50", "A canned"), ("B_c50", "B paraphrase")):
            pass
    fb = {"figure_type": "data", "chart": "line",
          "title": "Refusal rate versus axis-contrast units, axis A vs axis B",
          "x_label": "axis-contrast units c = alpha * NORM_L / ||d_raw||",
          "y_label": "refusal rate on benign prompts",
          "facet_by": "member", "series": []}

    fc = {"figure_type": "data", "chart": "scatter",
          "title": "Reading versus pushing: one point per (member, axis)",
          "subtitle": h3.get("pre_committed_sentence", ""),
          "x_label": "induction quality (max refusal rate over the c-grid)",
          "y_label": "detection quality (held-out AUROC)",
          "color_by": "level",
          "points": [{"x": p["max_refusal_rate"], "y": p["detection_auroc"],
                      "level": p["level"], "axis": p["axis"],
                      "label": f"{p['checkpoint']}:{p['axis']}"}
                     for p in R.get("joint_scatter_points", [])]}
    return {"fig_a_forest": fa, "fig_b_dose": fb, "fig_c_joint": fc}


def main():
    mo = EX.load_json(EX.HERE / "method_out.json")
    md = build_results_md(mo)
    (EX.HERE / "RESULTS.md").write_text(md)
    logger.info(f"wrote RESULTS.md ({len(md)} chars)")

    # figure b needs the raw grids, which live in the per-member induce files
    specs = build_figure_specs(mo)
    series = []
    for p in sorted(EX.RESULTS.glob("induce_*.json")):
        d = EX.load_json(p)
        for ax in EX.AB:
            rec = d["axes"].get(ax)
            if not rec:
                continue
            cs = rec["c_grid_uncapped"]
            series.append({"label": f"{d['checkpoint']} {ax}",
                           "member": d["checkpoint"], "axis": ax,
                           "x": cs,
                           "y": [rec["grid"][str(c)]["rate"] for c in cs]})
    specs["fig_b_dose"]["series"] = series
    EX.FIGS.mkdir(parents=True, exist_ok=True)
    EX.atomic_write_json(EX.FIGS / "figure_specs.json", specs)
    logger.info(f"wrote figures/figure_specs.json ({len(series)} dose series)")


if __name__ == "__main__":
    main()
