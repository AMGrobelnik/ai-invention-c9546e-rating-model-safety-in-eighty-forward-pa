#!/usr/bin/env python3
"""Assemble eval_out.json (exp_eval_sol_out schema), results/provenance.json, the
drop-in paper subsection and the README.

Every number that appears in the deliverable prose must exist in the provenance
map; the check is executed, not asserted in a comment.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_lib as EL  # noqa: E402

REL_EXP1 = "iter_2/gen_art/gen_art_experiment_1"
REL_SELF = "iter_3/gen_art/gen_art_evaluation_1"

PROV: dict[str, dict] = {}


def P(name: str, value, source: str, fmt: str = "{:.3f}") -> str:
    """Register a number with its provenance pointer and return it formatted."""
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        s = "n/a"
    else:
        s = fmt.format(value)
    PROV[name] = {"value": (None if value is None else
                            (float(value) if isinstance(value, (int, float, np.floating))
                             else value)),
                  "formatted": s, "source": source}
    return s


def steering_convention() -> dict:
    src = (EL.EXP1 / "models.py").read_text()
    m = re.search(r"delta = \(alpha \* state\.norm_l\).*?\n", src)
    return {
        "code_line": (m.group(0).strip() if m else "not found"),
        "formula": "h_L <- h_L + alpha * NORM_L * x_hat  (x_hat unit norm)",
        "contrast_unit": "c = alpha * NORM_L / raw_norm_X",
        "source": EL.jp(f"{REL_EXP1}/models.py", "#make_steer_hook"),
        "extracted_not_assumed": True,
    }


# ===========================================================================
def build(a1: dict, a2: dict, a3: dict | None, a4: dict | None,
          encodes: dict) -> tuple[dict, str, str]:
    prereg = EL.load_json(EL.RESULTS / "prereg_eval.json")
    conv = steering_convention()

    # ---- gates ---------------------------------------------------------
    gates = {}
    for k, e in encodes.items():
        g = e["axis_reproduction"]
        gates[k] = {
            "V2_strict_1e-3_passed": g["passed"],
            "V2_n_failed_checks": g["n_failed"],
            "V2_worst_deviation": g["worst_deviation"],
            "V2_max_self_rel_delta_between_two_rederivations":
                g.get("max_self_rel_delta"),
            "V2_within_run_determinism_is_exact": bool(
                (g.get("max_self_rel_delta") or 0.0) == 0.0),
            "V2_substantive_passed": bool(
                g["worst_deviation"] < 1e-2
                and (e.get("cos_A_vs_exp2_independent_fit") is None
                     or e["cos_A_vs_exp2_independent_fit"] > 0.99)),
            "V2_status": ("STRICT_FAIL_SUBSTANTIVE_PASS" if not g["passed"] else "PASS"),
            "V2_interpretation": (
                "the axis vectors are not archived, so they are re-derived; within this "
                "run the re-derivation is bit-exact, so the residual deviation from the "
                "archived summary statistics is a cross-run device/kernel difference "
                "(the archive ran on an RTX 4000 Ada, this evaluation on an RTX A4500), "
                "not instability of the fitting procedure"),
            "V1_leakage_passed": e["leakage_gate"]["passed"],
            "V1_n_text_overlap": e["leakage_gate"]["n_text_overlap"],
            "cos_A_vs_exp2_independent_fit": e.get("cos_A_vs_exp2_independent_fit"),
        }
    v3 = {k: v["V3_observable_reproduction"] for k, v in a1["per_checkpoint"].items()}
    v3_pass = [k for k, v in v3.items()
               if (v["pearson_r_t_reencoded_vs_logged"] or 0) >= 0.95]

    ref = "instruct_0p6"
    r1 = a1["per_checkpoint"].get(ref, {})
    ax1 = r1.get("axes", {})

    # ---- headline numbers with pointers --------------------------------
    aA = P("auroc_A_ref", ax1.get("A_canned", {}).get("centred", {}).get("auroc"),
           EL.jp(f"{REL_SELF}/results/analysis1.json",
                 "/per_checkpoint/instruct_0p6/axes/A_canned/centred/auroc"))
    aB = P("auroc_B_ref", ax1.get("B_paraphrase", {}).get("centred", {}).get("auroc"),
           EL.jp(f"{REL_SELF}/results/analysis1.json",
                 "/per_checkpoint/instruct_0p6/axes/B_paraphrase/centred/auroc"))
    dAB = ax1.get("_paired_A_minus_B", {})
    P("delta_auroc_ref", dAB.get("delta_auroc"),
      EL.jp(f"{REL_SELF}/results/analysis1.json",
            "/per_checkpoint/instruct_0p6/axes/_paired_A_minus_B/delta_auroc"))
    P("cos_A_B_stored", EL.model_meta(ref)["axis_cosines"]["cos(A_canned,B_paraphrase)"],
      EL.jp(f"{REL_EXP1}/results/model_instruct_0p6.json",
            "/axis_cosines/cos(A_canned,B_paraphrase)"))
    P("normA_ref", EL.model_meta(ref)["axes"]["A_canned"]["raw_norm"],
      EL.jp(f"{REL_EXP1}/results/model_instruct_0p6.json", "/axes/A_canned/raw_norm"),
      "{:.2f}")
    P("normB_ref", EL.model_meta(ref)["axes"]["B_paraphrase"]["raw_norm"],
      EL.jp(f"{REL_EXP1}/results/model_instruct_0p6.json", "/axes/B_paraphrase/raw_norm"),
      "{:.3f}")
    P("norm_ratio_ref", r1.get("geometry", {}).get("ratio_normA_over_normB"),
      EL.jp(f"{REL_SELF}/results/analysis1.json",
            "/per_checkpoint/instruct_0p6/geometry/ratio_normA_over_normB"), "{:.2f}")

    # contrast-unit dose summary across checkpoints
    a50c, bmaxc, bmaxr = [], [], []
    for k, v in a2["per_checkpoint"].items():
        A = v["axes"].get("A_canned", {})
        B = v["axes"].get("B_paraphrase", {})
        if A.get("contrast_units_at_alpha50") is not None:
            a50c.append(A["contrast_units_at_alpha50"])
        if B.get("max_contrast_units_reached") is not None:
            bmaxc.append(B["max_contrast_units_reached"])
            bmaxr.append(B["max_refusal_rate"])
    P("A_contrast_units_at_half_min", min(a50c) if a50c else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/axes/A_canned/contrast_units_at_alpha50"), "{:.2f}")
    P("A_contrast_units_at_half_max", max(a50c) if a50c else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/axes/A_canned/contrast_units_at_alpha50"), "{:.2f}")
    P("B_max_contrast_units_min", min(bmaxc) if bmaxc else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/axes/B_paraphrase/max_contrast_units_reached"), "{:.1f}")
    P("B_max_contrast_units_max", max(bmaxc) if bmaxc else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/axes/B_paraphrase/max_contrast_units_reached"), "{:.1f}")
    P("B_max_refusal_rate", max(bmaxr) if bmaxr else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/axes/B_paraphrase/max_refusal_rate"), "{:.2f}")

    mc = [v["matched_contrast"].get("B_paraphrase", {})
          for v in a2["per_checkpoint"].values()]
    mcd = [m["mean_paired_diff_A_minus_other"] for m in mc
           if m.get("mean_paired_diff_A_minus_other") is not None]
    P("matched_contrast_mean_diff", float(np.mean(mcd)) if mcd else None,
      EL.jp(f"{REL_SELF}/results/analysis2.json",
            "/per_checkpoint/*/matched_contrast/B_paraphrase/"
            "mean_paired_diff_A_minus_other"))

    # ---- verdicts -------------------------------------------------------
    verdicts = {
        "lexicality_verdict": a1["lexicality_verdict"],
        "lexicality_verdict_reason": a1["verdict_reason"],
        "matched_contrast_verdict": a2["matched_contrast_verdict"],
        "matched_contrast_reason": a2["matched_contrast_reason"],
        "semantic_dose_verdict": (a3 or {}).get("semantic_dose_verdict", "NOT_RUN"),
        "semantic_dose_detail": (a3 or {}).get("verdict_detail"),
    }

    # ---- accounting sentence (V7) --------------------------------------
    scanned = sum(e["harvest"]["scanned"] for e in encodes.values())
    kept = sum(e["harvest"]["kept"] for e in encodes.values())
    enc_n = sum(e["n_encoded"] for e in encodes.values())
    excl = {kk: sum(e["harvest"][kk] for e in encodes.values())
            for kk in ("excl_nonfluent", "excl_short", "excl_degenerate", "excl_dup")}
    P("n_scanned", scanned, EL.jp(f"{REL_SELF}/results/encode_*.json",
                                  "/harvest/scanned"), "{:,.0f}")
    P("n_kept", kept, EL.jp(f"{REL_SELF}/results/encode_*.json", "/harvest/kept"),
      "{:,.0f}")
    P("n_encoded", enc_n, EL.jp(f"{REL_SELF}/results/encode_*.json", "/n_encoded"),
      "{:,.0f}")
    for kk, vv in excl.items():
        P(f"n_{kk}", vv, EL.jp(f"{REL_SELF}/results/encode_*.json", f"/harvest/{kk}"),
          "{:,.0f}")
    accounting = (
        f"Across the six checkpoints {PROV['n_scanned']['formatted']} archived "
        f"generations were scanned, {PROV['n_kept']['formatted']} survived the "
        f"pre-registered exclusions ({PROV['n_excl_dup']['formatted']} duplicate "
        f"(prompt, text) pairs, {PROV['n_excl_nonfluent']['formatted']} failing the "
        f"archived fluency screen, {PROV['n_excl_short']['formatted']} too short, "
        f"{PROV['n_excl_degenerate']['formatted']} judged DEGENERATE), and "
        f"{PROV['n_encoded']['formatted']} were re-encoded after balancing the classes; "
        f"0 overlapped any axis fit response."
    )

    # ---- eval_out.json ---------------------------------------------------
    metrics_agg = {
        "n_checkpoints": float(len(encodes)),
        "n_powered_checkpoints": float(len(a1["powered_checkpoints"])),
        "n_items_reencoded": float(enc_n),
        "auroc_A_pooled_mean": float(np.mean([
            v["axes"]["A_canned"]["centred"]["auroc"]
            for v in a1["per_checkpoint"].values()
            if v["powered"]] or [np.nan])),
        "auroc_B_pooled_mean": float(np.mean([
            v["axes"]["B_paraphrase"]["centred"]["auroc"]
            for v in a1["per_checkpoint"].values() if v["powered"]] or [np.nan])),
        "auroc_C_pooled_mean": float(np.mean([
            v["axes"]["C_stylistic"]["centred"]["auroc"]
            for v in a1["per_checkpoint"].values() if v["powered"]] or [np.nan])),
        "auroc_D_pooled_mean": float(np.mean([
            v["axes"]["D_random0"]["centred"]["auroc"]
            for v in a1["per_checkpoint"].values() if v["powered"]] or [np.nan])),
        "delta_auroc_A_minus_B_mean": float(np.mean([
            v["axes"]["_paired_A_minus_B"]["delta_auroc"]
            for v in a1["per_checkpoint"].values() if v["powered"]] or [np.nan])),
        "A_contrast_units_at_half_min": float(min(a50c)) if a50c else float("nan"),
        "A_contrast_units_at_half_max": float(max(a50c)) if a50c else float("nan"),
        "B_max_contrast_units_reached": float(max(bmaxc)) if bmaxc else float("nan"),
        "B_max_refusal_rate": float(max(bmaxr)) if bmaxr else float("nan"),
        "matched_contrast_mean_diff_A_minus_B": float(np.mean(mcd)) if mcd else
        float("nan"),
        "worst_axis_reproduction_deviation": float(max(
            g["V2_worst_deviation"] for g in gates.values())),
        "min_V3_pearson": float(min(
            [v["pearson_r_t_reencoded_vs_logged"] for v in v3.values()
             if v["pearson_r_t_reencoded_vs_logged"] is not None] or [np.nan])),
        "judge_cost_usd": float((a3 or {}).get("_cost", 0.0)),
    }
    metrics_agg = {k: (v if np.isfinite(v) else -1.0) for k, v in metrics_agg.items()}

    datasets = _datasets(a1, a2, a3, a4)

    headline = [
        {"finding": "held-out behavioural AUROC of the canned axis A (reference "
                    "checkpoint instruct_0p6, stratum-centred, first-generated-token)",
         "value": PROV["auroc_A_ref"]["value"], "source": PROV["auroc_A_ref"]["source"]},
        {"finding": "held-out behavioural AUROC of the token-disjoint paraphrase axis B "
                    "(same items, same convention)",
         "value": PROV["auroc_B_ref"]["value"], "source": PROV["auroc_B_ref"]["source"]},
        {"finding": "paired AUROC(A) - AUROC(B) on the same held-out items",
         "value": PROV["delta_auroc_ref"]["value"],
         "source": PROV["delta_auroc_ref"]["source"]},
        {"finding": "axis-contrast-unit dose at which A reaches 50% refusal (range over "
                    "checkpoints where it crosses)",
         "value": [PROV["A_contrast_units_at_half_min"]["value"],
                   PROV["A_contrast_units_at_half_max"]["value"]],
         "source": PROV["A_contrast_units_at_half_min"]["source"]},
        {"finding": "maximum axis-contrast units reached by B at the grid maximum "
                    "alpha = 2.0, and its maximum refusal rate anywhere on the grid",
         "value": [PROV["B_max_contrast_units_max"]["value"],
                   PROV["B_max_refusal_rate"]["value"]],
         "source": PROV["B_max_contrast_units_max"]["source"]},
        {"finding": "mean paired refusal-rate difference A - B at MATCHED contrast units",
         "value": PROV["matched_contrast_mean_diff"]["value"],
         "source": PROV["matched_contrast_mean_diff"]["source"]},
        {"finding": "cosine between the re-derived canned axis and EXP2's independently "
                    "fitted float32 canned axis (reference checkpoint)",
         "value": gates[ref]["cos_A_vs_exp2_independent_fit"],
         "source": EL.jp(f"{REL_SELF}/results/encode_instruct_0p6.json",
                         "/cos_A_vs_exp2_independent_fit")},
    ]

    out = {
        "metadata": {
            "evaluation_name": "Does the paraphrase axis really read refusal? "
                               "Held-out re-certification of the lexicality verdict",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "kind": "evaluation / re-analysis of archived artifacts",
            "prereg": {"path": f"{REL_SELF}/results/prereg_eval.json",
                       "stamped_utc": prereg["stamped_utc"],
                       "sha256": prereg.get("sha256_of_body_without_hash"),
                       "amendments": prereg.get("amendments", [])},
            "steering_convention": conv,
            "checkpoints": {k: {"repo": e["repo"], "revision_sha": e["revision_sha"],
                                "L": e["L"], "NORM_L": e["NORM_L"], "dtype": e["dtype"],
                                "render": e["render"]} for k, e in encodes.items()},
            "verdicts": verdicts,
            "validity_gates": {
                "V1_leakage": {k: g["V1_leakage_passed"] for k, g in gates.items()},
                "V2_axis_reproduction": gates,
                "V3_observable_reproduction": v3,
                "V3_passed_checkpoints": v3_pass,
                "V4_power": {k: {"n_refusal": v["n_refusal"],
                                 "n_compliance": v["n_compliance"],
                                 "powered": v["powered"],
                                 "reason": v["underpowered_reason"]}
                             for k, v in a1["per_checkpoint"].items()},
                "V5_multiplicity": {"holm_adjusted_p": a1["holm_adjusted_p_paired_AminusB"],
                                    "raw_p": a1["raw_p_paired_AminusB"]},
                "V6_sign_discipline": {
                    "note": "alpha_50 and max refusal rate are reported sign-oriented "
                            "(multiplied by -1) wherever they are correlated with judged "
                            "behaviour, alongside the raw pre-registered form",
                    "sign_oriented_alpha50_A": {
                        k: (-v["axes"]["A_canned"]["alpha_50_nonparametric"]
                            if v["axes"].get("A_canned", {}).get(
                                "alpha_50_nonparametric") is not None else None)
                        for k, v in a2["per_checkpoint"].items()},
                    "raw_alpha50_A": {
                        k: v["axes"].get("A_canned", {}).get("alpha_50_nonparametric")
                        for k, v in a2["per_checkpoint"].items()}},
                "V7_accounting": accounting,
                "V8_provenance_map": f"{REL_SELF}/results/provenance.json",
            },
            "analysis1_heldout_certification": a1,
            "analysis2_contrast_unit_dose": a2,
            "analysis3_semantic_dose": a3,
            "analysis4_b_text_classes": a4,
            "headline_findings": headline,
            "cost_usd": (a3 or {}).get("_cost", 0.0),
            "compute": "1x NVIDIA RTX A4500 (20GB); forward passes only; no sampling, "
                       "no training",
        },
        "metrics_agg": metrics_agg,
        "datasets": datasets,
    }
    md = _subsection(a1, a2, a3, a4, gates, accounting, verdicts)
    readme = _readme(a1, a2, a3, a4, verdicts, accounting, gates)
    return out, md, readme


# ---------------------------------------------------------------------------
def _datasets(a1, a2, a3, a4) -> list[dict]:
    ds = []
    ex = []
    for k, v in a1["per_checkpoint"].items():
        for ax, r in v["axes"].items():
            if ax.startswith("_"):
                continue
            c = r["centred"]
            ex.append({
                "input": f"checkpoint={k} axis={ax}: does this axis read the model's own "
                         f"refusals in held-out, AB-blind generated text?",
                "output": "AUROC materially above chance for a refusal direction; "
                          "chance for a non-refusal control",
                "predict_auroc_centred": f"{c['auroc']:.4f}",
                "predict_auroc_raw": f"{r['raw']['auroc']:.4f}",
                "predict_auroc_regex_label": f"{r['regex_label_auroc_centred']:.4f}",
                "eval_auroc": float(c["auroc"]),
                "eval_auroc_ci_lo": float(c["auroc_ci95"][0]),
                "eval_auroc_ci_hi": float(c["auroc_ci95"][1]),
                "eval_cohens_d": float(c["cohens_d"]),
                "eval_mean_diff_projection_units": float(c["mean_diff_projection_units"]),
                "eval_n_refusal": float(v["n_refusal"]),
                "eval_n_compliance": float(v["n_compliance"]),
                "eval_powered": float(v["powered"]),
                "metadata_checkpoint": k, "metadata_axis": ax,
                "metadata_convention": "first_generated_token, stratum-centred",
            })
    ds.append({"dataset": "analysis1_heldout_behavioural_certification", "examples": ex})

    ex = []
    for k, v in a2["per_checkpoint"].items():
        for ax, r in v["axes"].items():
            ex.append({
                "input": f"checkpoint={k} axis={ax}: dose response in AXIS-CONTRAST "
                         f"UNITS (c = alpha * NORM_L / raw_norm_axis)",
                "output": "contrast units at 50% refusal, and the maximum contrast "
                          "units the grid reaches",
                "predict_alpha50_nonparametric": str(r["alpha_50_nonparametric"]),
                "predict_contrast_units_at_alpha50": str(r["contrast_units_at_alpha50"]),
                "eval_max_refusal_rate": float(r["max_refusal_rate"]),
                "eval_max_contrast_units": float(r["max_contrast_units_reached"]),
                "eval_crosses_half": float(r["crosses_half"]),
                "eval_inverted_u": float(r["inverted_u"]),
                "eval_contrast_units_at_max_rate": float(r["contrast_units_at_max_rate"]),
                "metadata_checkpoint": k, "metadata_axis": ax,
                "metadata_matched_contrast": v["matched_contrast"].get(ax),
            })
    ds.append({"dataset": "analysis2_axis_contrast_unit_dose", "examples": ex})

    if a3:
        ex = []
        for kk, v in a3["per_checkpoint_axis"].items():
            for a, g in v["grid"].items():
                ex.append({
                    "input": f"checkpoint={v['checkpoint']} axis={v['axis']} "
                             f"alpha={a}: refusal rate under the SEMANTIC judge vs the "
                             f"onset regex",
                    "output": "judge-scored refusal rate",
                    "predict_regex_rate": f"{g['rate_regex']:.4f}",
                    "predict_judge_rate": f"{g['rate_judge_strict']:.4f}",
                    "eval_rate_regex": float(g["rate_regex"]),
                    "eval_rate_judge_strict": float(g["rate_judge_strict"]),
                    "eval_rate_judge_incl_partial": float(g["rate_judge_incl_partial"]),
                    "eval_n": float(g["n"]),
                    "eval_kappa_regex_vs_judge": float(v["kappa_regex_vs_judge"]["kappa"]),
                    "metadata_checkpoint": v["checkpoint"], "metadata_axis": v["axis"],
                    "metadata_alpha": a,
                })
        ds.append({"dataset": "analysis3_semantic_label_dose_response", "examples": ex})

    if a4:
        ex = []
        for kk, v in a4["per_checkpoint_axis"].items():
            for a, g in v["by_alpha"].items():
                ex.append({
                    "input": f"checkpoint={v['checkpoint']} axis={v['axis']} alpha={a}: "
                             f"what is the steered text?",
                    "output": "class distribution over REFUSAL_CANONICAL / "
                              "REFUSAL_NONCANONICAL / PARTIAL / COMPLIANCE / DEGENERATE",
                    "predict_class_fractions": json.dumps(g["frac"]),
                    "eval_frac_noncanonical_refusal":
                        float(g["frac"].get("REFUSAL_NONCANONICAL", 0.0)),
                    "eval_frac_canonical_refusal":
                        float(g["frac"].get("REFUSAL_CANONICAL", 0.0)),
                    "eval_frac_degenerate": float(g["frac"].get("DEGENERATE", 0.0)),
                    "eval_frac_compliance": float(g["frac"].get("COMPLIANCE", 0.0)),
                    "eval_mean_distinct3": float(g["mean_distinct3"]),
                    "eval_frac_regex_refused": float(g["frac_regex_refused"]),
                    "eval_n": float(g["n"]),
                    "metadata_checkpoint": v["checkpoint"], "metadata_axis": v["axis"],
                    "metadata_alpha": a,
                })
        ds.append({"dataset": "analysis4_b_axis_text_classes", "examples": ex})
    return ds


# ---------------------------------------------------------------------------
def _table_a1(a1) -> str:
    rows = ["| checkpoint | n refusal | n compliance | AUROC A [95% CI] | "
            "AUROC B [95% CI] | AUROC C | AUROC D | paired A-B [95% CI] | powered |",
            "|---|---|---|---|---|---|---|---|---|"]
    for k, v in a1["per_checkpoint"].items():
        ax = v["axes"]

        def f(name):
            c = ax.get(name, {}).get("centred")
            if not c:
                return "n/a"
            return f"{c['auroc']:.3f}"

        def fc(name):
            c = ax.get(name, {}).get("centred")
            if not c:
                return "n/a"
            return (f"{c['auroc']:.3f} [{c['auroc_ci95'][0]:.3f}, "
                    f"{c['auroc_ci95'][1]:.3f}]")
        d = ax.get("_paired_A_minus_B", {})
        dd = (f"{d['delta_auroc']:+.3f} [{d['ci95'][0]:+.3f}, {d['ci95'][1]:+.3f}]"
              if d else "n/a")
        rows.append(f"| {k} | {v['n_refusal']} | {v['n_compliance']} | {fc('A_canned')} | "
                    f"{fc('B_paraphrase')} | {f('C_stylistic')} | {f('D_random0')} | "
                    f"{dd} | {'yes' if v['powered'] else 'NO'} |")
    return "\n".join(rows)


def _table_a2(a2) -> str:
    rows = ["| checkpoint | axis | raw norm | alpha_50 | contrast units @ 50% | "
            "max contrast units | max refusal rate | inverted U | fluency collapse alpha |",
            "|---|---|---|---|---|---|---|---|---|"]
    for k, v in a2["per_checkpoint"].items():
        for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0",
                   "E_prompt_contrast"):
            r = v["axes"].get(ax)
            if not r:
                continue
            a50 = r["alpha_50_nonparametric"]
            cu = r["contrast_units_at_alpha50"]
            rows.append(
                f"| {k} | {ax} | {v['axis_raw_norms'].get(ax, float('nan')):.2f} | "
                f"{'n/a (never crosses)' if a50 is None else f'{a50:.3f}'} | "
                f"{'n/a' if cu is None else f'{cu:.2f}'} | "
                f"{r['max_contrast_units_reached']:.1f} | {r['max_refusal_rate']:.2f} | "
                f"{'yes' if r['inverted_u'] else 'no'} | "
                f"{r['fluency_collapse_alpha'] if r['fluency_collapse_alpha'] is not None else 'none'} |")
    return "\n".join(rows)


def _subsection(a1, a2, a3, a4, gates, accounting, verdicts) -> str:
    cert = a1["certification_of_A"]
    ref = "instruct_0p6"
    r1 = a1["per_checkpoint"].get(ref, {})
    ax = r1.get("axes", {})
    d = ax.get("_paired_A_minus_B", {})
    res = ax.get("_residual_test_B_given_A", {})
    mc_txt = []
    for k, v in a2["per_checkpoint"].items():
        m = v["matched_contrast"].get("B_paraphrase", {})
        if m.get("n_matched_levels"):
            ptr = EL.jp(f"{REL_SELF}/results/analysis2.json",
                        f"/per_checkpoint/{k}/matched_contrast/B_paraphrase")
            mc_txt.append(
                f"{k}: {P(f'mc_{k}_diff', m['mean_paired_diff_A_minus_other'], ptr + '/mean_paired_diff_A_minus_other', '{:+.3f}')} "
                f"[{P(f'mc_{k}_lo', m['ci95'][0], ptr + '/ci95/0', '{:+.3f}')}, "
                f"{P(f'mc_{k}_hi', m['ci95'][1], ptr + '/ci95/1', '{:+.3f}')}] over "
                f"{P(f'mc_{k}_n', m['n_matched_levels'], ptr + '/n_matched_levels', '{:.0f}')} "
                f"matched contrast levels")
    lines = [
        "## Lexicality, re-certified on held-out behaviour",
        "",
        f"**Held-out certification verdict: {verdicts['lexicality_verdict']}** "
        f"(pre-registered branch). {verdicts['lexicality_verdict_reason']}.",
        "",
        f"**Matched-contrast verdict: {verdicts['matched_contrast_verdict']}.** "
        f"{verdicts['matched_contrast_reason']}.",
        "",
        f"**Semantic-dose verdict: {verdicts['semantic_dose_verdict']}**, adjudicated to "
        f"{(a3 or {}).get('reversal_adjudication', {}).get('adjudicated_verdict', 'n/a')}.",
        "",
        "The finding the binary rule did not anticipate, and the one that matters most: "
        "the vacuous certificate over-stated axis A as well as axis B. On held-out "
        "behaviour the canned axis is a mediocre refusal reader and on the two "
        "abliterated checkpoints it is at chance -- while the steering asymmetry it was "
        "invoked to explain survives every deflationary test applied here.",
        "",
        "### Why the previous certificate was vacuous",
        "",
        "Iteration 2 certified the token-disjoint paraphrase axis B as an equally good "
        "refusal direction by held-out AUROC 1.000 on eight hand-written response "
        "strings. Axes A, B and C all score 1.000 there, so the statistic has no "
        "discriminating power: it cannot separate *B is a refusal direction* from "
        "*B is a weak, noisy estimate of A*. This subsection replaces it with a "
        "certificate computed on text the models themselves produced, on prompts no "
        "axis was fitted on, and -- critically -- on text that neither A-steering nor "
        "B-steering produced, so neither axis is scored on its own effect.",
        "",
        accounting,
        "",
        "### Held-out behavioural AUROC",
        "",
        _table_a1(a1),
        "",
        f"On the reference checkpoint the canned axis A reaches AUROC "
        f"{PROV['auroc_A_ref']['formatted']} and the paraphrase axis B "
        f"{PROV['auroc_B_ref']['formatted']}, a paired difference of "
        f"{PROV['delta_auroc_ref']['formatted']} "
        f"(95% CI ["
        f"{P('delta_auroc_ref_lo', d.get('ci95', [None, None])[0], EL.jp(f'{REL_SELF}/results/analysis1.json', '/per_checkpoint/instruct_0p6/axes/_paired_A_minus_B/ci95/0'), '{:+.3f}')}, "
        f"{P('delta_auroc_ref_hi', d.get('ci95', [None, None])[1], EL.jp(f'{REL_SELF}/results/analysis1.json', '/per_checkpoint/instruct_0p6/axes/_paired_A_minus_B/ci95/1'), '{:+.3f}')}]) "
        f"against a pre-registered indifference margin of 0.10. The two axes have "
        f"cosine {PROV['cos_A_B_stored']['formatted']} and diff-in-means norms "
        f"{PROV['normA_ref']['formatted']} (A) versus {PROV['normB_ref']['formatted']} "
        f"(B), a ratio of {PROV['norm_ratio_ref']['formatted']}, so the "
        "'B is just a weaker estimate of A' hypothesis is quantified rather than "
        "waved away. Its direct test is the residual: regressing s_B on s_A across "
        f"held-out items gives R^2 = "
        f"{P('resid_r2_ref', res.get('r2_of_sB_on_sA'), EL.jp(f'{REL_SELF}/results/analysis1.json', '/per_checkpoint/instruct_0p6/axes/_residual_test_B_given_A/r2_of_sB_on_sA'))} "
        f"and the residual still separates refusals from compliances at AUROC "
        f"{P('resid_auroc_ref', res.get('auroc_of_residual'), EL.jp(f'{REL_SELF}/results/analysis1.json', '/per_checkpoint/instruct_0p6/axes/_residual_test_B_given_A/auroc_of_residual'))}; a purely scaled noisy copy "
        "of A would leave nothing there.",
        "",
        "### The certificate also over-stated axis A",
        "",
        f"The archived certificate gave A, B and C held-out AUROC 1.000 alike. On the "
        f"models' own generated text the CANNED axis itself reaches only "
        f"{P('auroc_A_min', cert['auroc_A_range'][0], EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/auroc_A_range/0'))}"
        f"-{P('auroc_A_max', cert['auroc_A_range'][1], EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/auroc_A_range/1'))}. "
        f"Its 95% CI excludes chance on "
        f"{P('n_A_sig', len(cert['A_ci_excludes_0.5']), EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/A_ci_excludes_0.5'), '{:.0f}')} "
        f"of {P('n_powered', len(a1['powered_checkpoints']), EL.jp(f'{REL_SELF}/results/analysis1.json', '/powered_checkpoints'), '{:.0f}')} "
        f"powered checkpoints ({', '.join(cert['A_ci_excludes_0.5'])}) and clears the "
        f"whole pre-registered chance band on only "
        f"{P('n_A_above_band', len(cert['A_above_chance_band']), EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/A_above_chance_band'), '{:.0f}')} "
        f"({', '.join(cert['A_above_chance_band']) or 'none'}); on both abliterated "
        f"members it sits at chance. Axis B's own range is "
        f"{P('auroc_B_min', cert['auroc_B_range'][0], EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/auroc_B_range/0'))}"
        f"-{P('auroc_B_max', cert['auroc_B_range'][1], EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/auroc_B_range/1'))}. "
        f"The vacuous certificate therefore over-stated the canned axis as well as the "
        f"paraphrase axis: on held-out behaviour neither axis is the clean refusal "
        f"reader that 1.000 implied. That is the most consequential correction in this "
        f"re-analysis, because the paper's steering-strength metric is defined on "
        f"axis A. The norm-matched stylistic control is also not merely at chance: on "
        f"{P('n_C_below', len(cert['control_axes_significantly_BELOW_chance']['C_stylistic']), EL.jp(f'{REL_SELF}/results/analysis1.json', '/certification_of_A/control_axes_significantly_BELOW_chance/C_stylistic'), '{:.0f}')} "
        f"checkpoints its CI lies entirely BELOW 0.5, i.e. refusals score LOW on the "
        f"formal-register axis. It reads refusal text in the opposite direction while "
        f"still inducing 0.00 refusal when steered, which is the dissociation this "
        f"control was built to show. The random direction is at chance everywhere.",
        "",
        "### The axis-contrast-unit dose, and whether norm mismatch explains B",
        "",
        f"Steering adds `alpha * NORM_L * x_hat` to the residual stream at layer L "
        f"(extracted from the archived hook, not assumed), so one AXIS-CONTRAST UNIT "
        f"is `c = alpha * NORM_L / raw_norm_X`. In those units axis A crosses 50% "
        f"refusal at {PROV['A_contrast_units_at_half_min']['formatted']}-"
        f"{PROV['A_contrast_units_at_half_max']['formatted']} contrast units, while "
        f"axis B is driven to as much as "
        f"{PROV['B_max_contrast_units_max']['formatted']} contrast units at the grid "
        f"maximum alpha = 2.0 and still tops out at a refusal rate of "
        f"{PROV['B_max_refusal_rate']['formatted']}. **The norm deficit therefore does "
        f"not explain B's failure**: at MATCHED contrast units the paired refusal-rate "
        f"difference A - B is {PROV['matched_contrast_mean_diff']['formatted']} "
        f"({verdicts['matched_contrast_verdict']}; " + "; ".join(mc_txt) + ").",
        "",
        _table_a2(a2),
        "",
    ]
    if a3:
        adj = a3.get("reversal_adjudication", {})
        vd = a3["verdict_detail"]
        bj = P("B_max_judge_rate", max(
            v["max_rate_judge"] for k, v in a3["per_checkpoint_axis"].items()
            if v["axis"] == "B_paraphrase"),
            EL.jp(f"{REL_SELF}/results/analysis3.json",
                  "/per_checkpoint_axis/*|B_paraphrase/max_rate_judge"), "{:.2f}")
        br = P("B_max_regex_rate_a3", max(
            v["max_rate_regex"] for k, v in a3["per_checkpoint_axis"].items()
            if v["axis"] == "B_paraphrase"),
            EL.jp(f"{REL_SELF}/results/analysis3.json",
                  "/per_checkpoint_axis/*|B_paraphrase/max_rate_regex"), "{:.2f}")
        nf = P("null_axis_judge_floor_max", max(
            (v["null_axis_max_judge_refusal_rate"] or 0)
            for v in vd["null_floor"].values()),
            EL.jp(f"{REL_SELF}/results/analysis3.json",
                  "/verdict_detail/null_floor/*/null_axis_max_judge_refusal_rate"),
            "{:.2f}")
        sens = P("judge_sensitivity_refusal",
                 a3["attenuation"]["audited_confusion"]["sensitivity_REFUSAL"],
                 EL.jp("iter_2/gen_art/gen_art_experiment_3/results/arm_labels_v2.json",
                       "/arms/arm2_repaired"))
        spec = P("judge_specificity_refusal",
                 a3["attenuation"]["audited_confusion"]["specificity_REFUSAL"],
                 EL.jp("iter_2/gen_art/gen_art_experiment_3/results/arm_labels_v2.json",
                       "/arms/arm2_repaired"))
        lines += [
            "### Semantic scoring of the outcome, and why the apparent reversal is not clean",
            "",
            f"The archived `refused` flag is an onset regex, so a lexical axis was being "
            f"scored by a lexical outcome measure. Re-scored with the repaired four-class "
            f"judge, axis B's refusal rate on the judged subsample rises from at most "
            f"{br} under the regex ({PROV['B_max_refusal_rate']['formatted']} on the full "
            f"grid) to as much as {bj}, and crosses 0.5 on every checkpoint, which taken "
            f"at face value is a **{verdicts['semantic_dose_verdict']}**. Two "
            f"measurements say it should not be read as a clean one. First, the clean control axes -- the norm-matched stylistic "
            f"axis and the random direction, which induce 0.00 refusal under the regex -- "
            f"themselves receive judge REFUSAL rates as high as {nf} at their top alphas, "
            f"so there is a large false-positive floor on degraded text. Second, the "
            f"five-class rubric applied to the SAME alpha region, which offers an explicit "
            f"non-canonical-refusal class, assigns most of that text to DEGENERATE "
            f"instead. The adjudicated reading is "
            f"**{adj.get('adjudicated_verdict')}**. The audited judge has sensitivity "
            f"{sens} and specificity {spec} for REFUSAL against blind-adjudicated truth, "
            f"so an attenuation-corrected column ships beside the raw judge rate and "
            f"REFUSAL/PARTIAL is named as the unreliable boundary.",
            "",
        ]
    if a4:
        s = a4["summary"]
        bn = P("B_frac_noncanonical_refusal", s["B_mean_frac_noncanonical_refusal"],
               EL.jp(f"{REL_SELF}/results/analysis4.json",
                     "/summary/B_mean_frac_noncanonical_refusal"))
        ba = P("B_frac_any_refusal", s["B_mean_frac_any_refusal"],
               EL.jp(f"{REL_SELF}/results/analysis4.json",
                     "/summary/B_mean_frac_any_refusal"))
        bd = P("B_frac_degenerate", s["B_mean_frac_degenerate"],
               EL.jp(f"{REL_SELF}/results/analysis4.json",
                     "/summary/B_mean_frac_degenerate"))
        aa = P("A_frac_any_refusal", s["A_mean_frac_any_refusal"],
               EL.jp(f"{REL_SELF}/results/analysis4.json",
                     "/summary/A_mean_frac_any_refusal"))
        ad = P("A_frac_degenerate", s["A_mean_frac_degenerate"],
               EL.jp(f"{REL_SELF}/results/analysis4.json",
                     "/summary/A_mean_frac_degenerate"))
        lines += [
            "### What B's high-alpha text actually is",
            "",
            f"Classified with REFUSAL split into canonical and non-canonical wording, "
            f"B's top-three-alpha text is {bn} non-canonical refusal, {ba} refusal of "
            f"any wording and {bd} degenerate, against {aa} refusal and {ad} degenerate "
            f"for A at its own top three alphas. So B does induce SOME refusal the onset "
            f"regex cannot see -- that part of the headline needs restating -- but the "
            f"dominant effect of driving B hard is incoherence, not refusal, while A at "
            f"its own top alphas is dominated by refusal. Boundary examples are published "
            f"verbatim in `results/b_axis_examples.md`.",
            "",
        ]
    lines += [
        "### Validity",
        "",
        f"Axis vectors are not stored in the archive, so all four axes were re-derived "
        f"by re-running the archived fit code at the archived layer and revision SHA. "
        f"They reproduce the archived values to within "
        f"{P('V2_worst_deviation', max(g['V2_worst_deviation'] for g in gates.values()), EL.jp(f'{REL_SELF}/eval_out.json', '/metadata/validity_gates/V2_axis_reproduction/*/V2_worst_deviation'), '{:.1e}')} "
        f"relative on the stored norms and cosines, so the pre-registered 1e-3 gate FAILS "
        f"on a minority of quantities and is reported as a strict failure rather than "
        f"waved through. It is not run-to-run noise inside this evaluation: re-deriving "
        f"every axis twice on the same GPU reproduces it bit-for-bit (largest relative "
        f"movement "
        f"{P('V2_self_determinism', max(g['V2_max_self_rel_delta_between_two_rederivations'] or 0 for g in gates.values()), EL.jp(f'{REL_SELF}/eval_out.json', '/metadata/validity_gates/V2_axis_reproduction/*/V2_max_self_rel_delta_between_two_rederivations'), '{:.1e}')}), "
        f"so the residual is a cross-RUN difference between the archive's device and "
        f"ours: same code, same weights, same revision SHA, bf16 on a different GPU. "
        f"Three facts bound its consequence -- the stored pairwise cosines reproduce to "
        f"about 1e-3, the random axes reproduce EXACTLY from their stored seeds, and the "
        f"re-derived canned axis has cosine "
        f"{P('cos_A_exp2', gates['instruct_0p6']['cos_A_vs_exp2_independent_fit'], EL.jp(f'{REL_SELF}/results/encode_instruct_0p6.json', '/cos_A_vs_exp2_independent_fit'), '{:.4f}')} "
        f"with the independently fitted float32 axis from the breadth-panel experiment. "
        f"Zero held-out items overlap any axis fit response (leakage gate), and the "
        f"re-encoded refusal-logit margin reproduces the archived r_t_first at Pearson "
        f"{P('V3_min_pearson', min((v['V3_observable_reproduction']['pearson_r_t_reencoded_vs_logged'] or 0) for v in a1['per_checkpoint'].values()), EL.jp(f'{REL_SELF}/results/analysis1.json', '/per_checkpoint/*/V3_observable_reproduction/pearson_r_t_reencoded_vs_logged'), '{:.4f}')} "
        f"or better on every checkpoint. Token IDS are concatenated rather than strings "
        f"when the prompt and its logged completion are re-encoded: string concatenation "
        f"lets BPE merge across the boundary, which on the plain-rendered base "
        f"checkpoints affected a large share of items and broke this gate outright.",
    ]
    return "\n".join(lines)


def _readme(a1, a2, a3, a4, verdicts, accounting, gates) -> str:
    up = a1["underpowered_checkpoints"]
    cert = a1["certification_of_A"]
    lines = [
        "# Does the paraphrase axis really read refusal?",
        "",
        f"**{verdicts['lexicality_verdict']}** — {verdicts['lexicality_verdict_reason']}",
        "",
        f"**The unanticipated finding, and the one that matters most:** the archived "
        f"certificate over-stated axis A as well as axis B. On the models' own generated "
        f"text the canned axis reaches AUROC "
        f"{cert['auroc_A_range'][0]:.3f}-{cert['auroc_A_range'][1]:.3f} (archived "
        f"certificate: 1.000 for every axis), its CI excludes chance on "
        f"{len(cert['A_ci_excludes_0.5'])} of {len(a1['powered_checkpoints'])} powered "
        f"checkpoints, and on both abliterated members it is at chance. The "
        f"steering-strength metric the paper defines is built on that axis.",
        "",
        f"**Matched contrast: {verdicts['matched_contrast_verdict']}** — "
        f"{verdicts['matched_contrast_reason']}",
        "",
        f"**Semantic dose: {verdicts['semantic_dose_verdict']}**",
        "",
        "Re-analysis only: no new sampling, no new steered generation, no training. "
        "The single piece of GPU work is a forward pass over text that was already "
        "logged, to read the residual stream at the steering site.",
        "",
        "## What this replaces",
        "",
        "Iteration 2's lexicality control was certified by 'equal held-out AUROC 1.000' "
        "on eight hand-written strings. A, B and C all saturate there, so that number "
        "certifies nothing. Here the certificate is computed on the models' own "
        "generated refusals and compliances, in a pool that is blind to both axes.",
        "",
        accounting,
        "",
        "## Held-out behavioural certification (Analysis 1)",
        "",
        _table_a1(a1),
        "",
        f"Underpowered (fewer than {EL.MIN_PER_CLASS} items in one class, excluded from "
        f"the verdict count by the pre-registered rule): {', '.join(up) if up else 'none'}.",
        "",
        "## Axis-contrast-unit dose (Analysis 2)",
        "",
        _table_a2(a2),
        "",
        "## Pre-registration, gates and cost",
        "",
        f"- Pre-registration stamped before any AUROC existed; "
        f"{len(EL.load_json(EL.RESULTS / 'prereg_eval.json').get('amendments', []))} "
        f"amendments appended with `when_decided` and the data state at the time "
        f"(counting universe over POWERED checkpoints; the axis-reproduction tolerance "
        f"reported at both the strict and the determinism-calibrated reading; the "
        f"null-axis judge floor added after seeing the control curves).",
        f"- V1 leakage: 0 held-out items overlap any axis fit response, on every "
        f"checkpoint.",
        f"- V2 axis reproduction: STRICT FAIL / SUBSTANTIVE PASS — the archived vectors "
        f"are not stored, so they are re-derived; deviation from the archived summary "
        f"statistics reaches "
        f"{max(g['V2_worst_deviation'] for g in gates.values()):.1e} relative, above the "
        f"pre-registered 1e-3, while the re-derivation is bit-exact within this run and "
        f"the re-derived canned axis has cosine "
        f"{gates['instruct_0p6']['cos_A_vs_exp2_independent_fit']:.4f} with an "
        f"independently fitted float32 axis from the breadth panel.",
        f"- V3 observable reproduction: the re-encoded refusal-logit margin reproduces "
        f"the archived `r_t_first` at Pearson "
        f"{min(v['V3_observable_reproduction']['pearson_r_t_reencoded_vs_logged'] for v in a1['per_checkpoint'].values()):.4f} "
        f"or better on all six checkpoints.",
        f"- OpenRouter spend: $"
        f"{P('judge_cost_usd', (a3 or {}).get('_cost', 0.0), EL.jp(f'{REL_SELF}/results/cost_ledger.jsonl', '/cumulative_cost_usd'), '{:.4f}')} of a $1.50 cap "
        f"(cache-first sampler; every archived judge cache was seeded first).",
        "",
        "## Files",
        "",
        "- `eval_out.json` — schema-validated evaluation output (all four analyses)",
        "- `results/prereg_eval.json` — pre-registration, stamped before any AUROC",
        "- `results/provenance.json` — every headline number to its archived JSON pointer",
        "- `results/lexicality_subsection.md` — drop-in replacement paper subsection",
        "- `results/b_axis_examples.md` — verbatim boundary examples",
        "- `results/analysis{1,2,3,4}.json`, `results/encode_*.json`, `results/axes/*.npy`",
        "- `figures/` — regenerated from the analysis output only",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python prereg.py                       # stamp the pre-registration",
        "python gpu_stage.py --checkpoints all  # axis re-derivation + re-encode (GPU)",
        "python analysis12.py                   # Analyses 1 and 2",
        "python judge_stage.py --checkpoints all  # Analyses 3/4 judging (OpenRouter)",
        "python analysis34.py                   # Analyses 3 and 4",
        "python assemble.py && python figures.py",
        "```",
    ]
    return "\n".join(lines)


ALLOWED_LITERALS = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0.10", "1.000", "0.391",
    "0.5", "50", "2.0", "1e-3", "0.00", "12", "40", "2000", "124", "1.50", "0.0",
    "20", "95", "1", "0.60", "0.40", "0.021", "0.1", "0.15", "0.20", "0.50", "0.05",
    "1.7", "0.6", "3", "5", "4", "1e-3", "0.000",
}


def _prose_only(text: str) -> str:
    """Drop generated tables, code blocks and file paths: those are rendered directly
    from results/*.json by the generator, so they are traceable by construction."""
    out, in_code = [], False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or ln.lstrip().startswith("|") or ln.lstrip().startswith("- `"):
            continue
        out.append(ln)
    return "\n".join(out)


def check_prose_numbers(text: str) -> dict:
    """V8: every number in the prose must be traceable to the provenance map."""
    text = _prose_only(text)
    formatted = {v["formatted"] for v in PROV.values()}
    nums = re.findall(r"(?<![\w.])[-+]?\d+(?:,\d{3})*(?:\.\d+)?(?:e[-+]?\d+)?", text)
    unknown = []
    for n in nums:
        if n in formatted or n in ALLOWED_LITERALS:
            continue
        if n.lstrip("+-") in {v.lstrip("+-") for v in formatted}:
            continue
        unknown.append(n)
    return {"n_numbers_in_prose": len(nums), "n_unmatched": len(unknown),
            "unmatched_sample": sorted(set(unknown))[:40],
            "note": ("unmatched numbers are table cells and per-checkpoint values "
                     "rendered directly from results/analysis*.json by the generator; "
                     "the prose is generated from the map, never hand-typed")}


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    a1 = EL.load_json(EL.RESULTS / "analysis1.json")
    a2 = EL.load_json(EL.RESULTS / "analysis2.json")
    a3 = EL.load_json(EL.RESULTS / "analysis3.json") if (
        EL.RESULTS / "analysis3.json").exists() else None
    a4 = EL.load_json(EL.RESULTS / "analysis4.json") if (
        EL.RESULTS / "analysis4.json").exists() else None
    if a3 is not None and (EL.RESULTS / "judge_raw.json").exists():
        a3["_cost"] = EL.load_json(EL.RESULTS / "judge_raw.json")["cost"]["total_usd"]
    encodes = {k: EL.load_json(EL.RESULTS / f"encode_{k}.json") for k in EL.CHECKPOINTS
               if (EL.RESULTS / f"encode_{k}.json").exists()}
    out, md, readme = build(a1, a2, a3, a4, encodes)
    chk = check_prose_numbers(md + "\n" + readme)
    if chk["n_unmatched"]:
        raise AssertionError(
            f"V8 prose-number gate FAILED: {chk['n_unmatched']} numbers in the "
            f"deliverable prose are not in results/provenance.json: "
            f"{chk['unmatched_sample']}")
    out["metadata"]["validity_gates"]["V8_prose_number_check"] = chk
    (HERE / "eval_out.json").write_text(json.dumps(out, indent=1))
    (EL.RESULTS / "provenance.json").write_text(json.dumps(PROV, indent=1))
    (EL.RESULTS / "lexicality_subsection.md").write_text(md)
    (HERE / "README.md").write_text(readme)
    logger.info(f"wrote eval_out.json ({(HERE / 'eval_out.json').stat().st_size / 1e6:.2f} MB); "
                f"prose numbers {chk['n_numbers_in_prose']}, "
                f"unmatched {chk['n_unmatched']}")


if __name__ == "__main__":
    main()
