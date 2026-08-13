#!/usr/bin/env python3
"""Analysis 5 -- the 'Corrections of record' appendix, the main-text stub, and
the main-text reduction accounting."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from loguru import logger

from eval_common import E1, E2, E3, OUT, ROOT, V1, load_json, register

PAPER_SRC = ROOT / "iter_2/gen_paper_text/gen_paper_text/build_out.py"


def paper_sections() -> dict[str, str]:
    """Extract the iteration-2 main text and split it into '# '/'## ' sections."""
    src = register(PAPER_SRC).read_text()
    tree = ast.parse(src)
    paper = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "PAPER":
            paper = ast.literal_eval(node.value)
    if paper is None:
        return {}
    sections, cur, buf = {}, "PREAMBLE", []
    for line in paper.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            sections[cur] = "\n".join(buf)
            cur, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    sections[cur] = "\n".join(buf)
    return sections


def wc(text: str) -> int:
    return len([w for w in re.split(r"\s+", text) if w])


def collect_entries(results: dict) -> list[dict]:
    """One entry per correction of record: old claim, corrected statement,
    provenance, and why it moved."""
    v1 = load_json(V1 / "eval_out.json")["metadata"]
    v1dev = load_json(V1 / "deviations.json")
    e2prereg = load_json(E2 / "prereg.json")
    e1meta = load_json(E1 / "method_out.json")["metadata"]
    e3 = load_json(E3 / "method_out.json")["metadata"]

    ents = []

    ents.append({
        "topic": "Early-warning-signal direction control",
        "as_previously_stated": (
            "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING: a random unit vector at the same "
            "layer and magnitude separates the panel as well as the refusal direction, and "
            "on the only pair isolating safety tuning the control separates while the "
            "treatment does not."),
        "corrected_statement": v1["verdicts"]["analysis1_direction_control"],
        "supporting_numbers": {
            "primary_did": "-2.334 log units [-3.573, -1.037]",
            "holm_adjusted_p": 0.214,
            "n_tests_ci_excluding_0": "8 of 48",
            "n_passing_TOST_at_0.20": "0 of 48",
            "prompts_needed_for_equivalence": "~1,880",
        },
        "derived_from": "V1/eval_out.json :: metadata.verdicts.analysis1_direction_control; "
                        "V1/deviations.json[0]",
        "why_it_moved": (
            "the iteration-1 control was adjudicated on lambda, which the same archived tree "
            "marks identifiable=false on 640/640 rows, so both arms of the control were "
            "equally non-identifiable; re-run on assumption-free statistics the control is "
            "DIRECTION-SPECIFIC before Holm and INCONCLUSIVE after."),
    })

    ents.append({
        "topic": "Observable-validity gate",
        "as_previously_stated": (
            "cross-model indicator comparisons ('indicators track lineage, not safety') were "
            "reported without a validity gate on the readout."),
        "corrected_statement": v1["verdicts"]["analysis2_validity_gate"],
        "supporting_numbers": {"admissible_pairs_layer_L": 0, "members_passing_layer_L": "1 of 4",
                               "members_passing_final_layer": "2 of 4"},
        "derived_from": "V1/eval_out.json :: metadata.verdicts.analysis2_validity_gate; "
                        "V1/out/final_layer_gate.json",
        "why_it_moved": ("the gate empties the cross-model table at the layer-L readout, so the "
                         "cross-model claim was computed largely on readouts that are not "
                         "validated refusal signals; which readout is chosen is a live analytic "
                         "degree of freedom."),
    })

    ents.append({
        "topic": "The n=4 rank comparison",
        "as_previously_stated": ("label-free SPI Spearman rho = -0.20 versus supervised "
                                 "baselines +0.40, i.e. the baselines beat the method."),
        "corrected_statement": v1["verdicts"]["analysis3_small_n"],
        "supporting_numbers": {"exact_two_sided_floor_untied": 0.0833,
                               "exact_floor_given_observed_ties": 0.1667,
                               "rho_spi_tie_aware": 0.105, "rho_baseline_tie_aware": 0.632},
        "derived_from": "V1/eval_out.json :: metadata.verdicts.analysis3_small_n",
        "why_it_moved": ("the archived -0.20/+0.40 pair is reproduced only under an ordinal rank "
                         "that breaks a ground-truth tie by array order; at n=4 the exact "
                         "permutation floor makes no rank comparison informative."),
    })

    ents.append({
        "topic": "The lambda (relaxation-rate) claim",
        "as_previously_stated": ("lambda, the exponential relaxation rate of the perturbed "
                                 "observable, orders the panel by safety."),
        "corrected_statement": v1["verdicts"]["analysis1_lambda_demotion"],
        "supporting_numbers": {"identifiable_rows": "0 of 640",
                               "prereg_rule": "T_fit >= 128, which then moves to n_roll >= 40",
                               "achieved": "T_fit = 64, n_roll = 20"},
        "derived_from": "V1/eval_out.json :: metadata.verdicts.analysis1_lambda_demotion",
        "why_it_moved": ("the pre-registered identifiability rule is not met at any geometry "
                         "reached, so lambda is not admissible as a score OR as a control."),
    })

    so = results["sign_orientation"]
    ents.append({
        "topic": "Sign convention of the metric-vs-baseline comparison",
        "as_previously_stated": (
            "DELTA = rho_alpha50 - rho_AMS = -0.714 [-1.765, 0.667], reported as a TIE between "
            "alpha_50 and our-AMS."),
        "corrected_statement": (
            "The statistic was computed on RAW, unoriented correlations, in which a PERFECT "
            f"alpha_50 (rho = -1 under its own validity theory) would have produced DELTA = "
            f"{so['ceiling_check']['old_raw_statistic']['delta_if_alpha50_were_PERFECT']:.4f}: "
            "the comparison scored the ideal case as a catastrophic loss. On sign-oriented "
            "correlations the measured DELTA is "
            f"{so['oriented_headline_delta']['plain_harmful_refusal']['delta']:.4f} and a "
            "perfect alpha_50 would score "
            f"{so['ceiling_check']['corrected_oriented_statistic']['delta_if_alpha50_were_PERFECT']:.4f}. "
            "The three comparators (oriented rho, |rho|, predictive AUC) "
            + ("agree" if so["orientation_free_comparators"]["ordering_agreement"]["all_agree"]
               else "do NOT agree") + " on the ordering."),
        "supporting_numbers": {
            "rho_alpha50_raw": so["regression_check_raw_headline"]["recomputed"]["rho_a"],
            "rho_ams_raw": so["regression_check_raw_headline"]["recomputed"]["rho_b"],
            "p_oriented_rho_alpha50_below_0": so["wrong_sign_claim"]["p_true_oriented_rho_below_0"],
        },
        "derived_from": "this artifact :: results.sign_orientation (recomputed from "
                        "E2/results/member_*.json via lib.stats_ext, archived headline "
                        "reproduced to 3 dp first)",
        "why_it_moved": ("a comparison that cannot reward the ideal case measures nothing; the "
                         "orientation is fixed by the pre-registered direction of the score."),
    })

    a007 = e3.get("a007_case_study", {})
    ents.append({
        "topic": "The self-harm item A007 and the old truth labels",
        "as_previously_stated": ("A007 is a refusal-by-redirection that the old probe "
                                 "demonstrably mislabelled as COMPLIANCE, which is why the "
                                 "21-item probe could not be trusted."),
        "corrected_statement": (
            "TESTED AND REFUTED. The blind panel re-adjudicated all 21 bridge items and changed "
            "NONE; the A007 completion opens compliantly and truncates mid-compliance, and the "
            "COMPLIANCE label stands. The old probe's defect is COVERAGE (27.4% of the "
            "population, PARTIAL never emitted), not its labels."),
        "supporting_numbers": {"n_bridge_items": 21, "n_labels_changed": 0,
                               "heuristic_accuracy_where_it_labels": 0.912,
                               "heuristic_coverage": 0.274,
                               "a007_verdict": a007.get("verdict") if isinstance(a007, dict) else None},
        "derived_from": "E3/method_out.json :: metadata.headline_findings[H2], "
                        "metadata.a007_case_study; E3/results/truth_labels_v2.json",
        "why_it_moved": ("the premise was stated as an observation and was never checked against "
                         "an independent panel; when checked, it did not hold."),
    })

    jp = results["judge_propagation"]
    ents.append({
        "topic": "The two judge-propagation rates",
        "as_previously_stated": ("the judge repair moved abliterated plain-harmful refusal "
                                 "0.700 -> 0.113 and jailbreak ASR 0.092 -> 0.858; both "
                                 "revisions were reported as settled."),
        "corrected_statement": (
            "Against blind annotator truth on a fresh simple random subsample, the jailbreak ASR "
            f"revision STANDS (truth {jp['propagation']['abliterated_jailbreak_ASR']['archived_truth']:.3f} "
            f"{jp['propagation']['abliterated_jailbreak_ASR']['recomputed_wilson']}), while the "
            "plain-harmful refusal revision must be RESTATED (truth "
            f"{jp['propagation']['abliterated_plain_harmful_refusal_rate']['archived_truth']:.3f} "
            f"{jp['propagation']['abliterated_plain_harmful_refusal_rate']['recomputed_wilson']}): "
            "the repaired judge still over-states it."),
        "supporting_numbers": {
            "pooled_compliance_recall": jp["pooled_compliance_recall"]["recall"],
            "pooled_compliance_recall_ci": jp["pooled_compliance_recall"]["wilson_ci"],
            "per_class_kappa": jp["per_class_kappa"],
            "frozen_judge_self_reproduction": jp["frozen_judge_self_reproduction"]["arm1_frozen"],
        },
        "derived_from": "E3/results/* and E3/method_out.json; Wilson intervals recomputed here "
                        "from the recovered (k, n) rather than copied",
        "why_it_moved": ("the published rates reproduce exactly from scored.jsonl, but only one "
                         "of the two survives comparison with independent annotator truth."),
    })

    acc = results["accounting"]
    ents.append({
        "topic": "Panel accounting (the 19 / 17 / 1 triple)",
        "as_previously_stated": "19 measured members, 17 analysed, 1 with a defined primary estimate.",
        "corrected_statement": acc["one_sentence_for_the_paper"] + " " + acc["sharpest_fact"],
        "supporting_numbers": {"derived_triple": acc["derived_triple"],
                               "quoted_triple": acc["quoted_triple"],
                               "discrepancy": acc["discrepancy"]},
        "derived_from": "E2/method_out.json :: metadata.analysis.d1_alpha50_table (counted, not "
                        "copied) and E2/results/member_*.json",
        "why_it_moved": "the arithmetic in the files gives a different middle term.",
    })

    ams = results["ams_reproduction"]
    ents.append({
        "topic": "The AMS reproduction gate",
        "as_previously_stated": "our AMS reimplementation fails its own reproduction gate.",
        "corrected_statement": ams["replacement_sentence"],
        "supporting_numbers": {"n_cells_within_25pct": ams["n_cells_within_25pct"],
                               "n_cells": ams["n_cells"],
                               "llama_1b": ams["llama_1b_note"]},
        "derived_from": "E2/results/ams_gate.json",
        "why_it_moved": ("a flat 'it fails' is internally inconsistent with relying on the same "
                         "reimplementation as the surviving baseline; the per-checkpoint verdicts "
                         "pass on 3/3 and the ordering criterion is vacuous at n=3."),
    })

    ls = results["layer_sensitivity"]
    ents.append({
        "topic": "Layer sensitivity",
        "as_previously_stated": ls["headline_replacement"]["old"],
        "corrected_statement": ls["headline_replacement"]["new"],
        "supporting_numbers": {"misspecification_diagnostic": ls["misspecification_diagnostic"],
                               "coverage": ls["coverage_caveat"]},
        "derived_from": "E2/results/layersens_*.json, monotonicity via E2/lib/dose.py",
        "why_it_moved": ("quoting only the logistic span attributes to geometry what a sigmoid "
                         "fitted to a non-monotone curve produces."),
    })

    asy = results["asymmetry"]
    ents.append({
        "topic": "The free-running vs teacher-forced asymmetry",
        "as_previously_stated": asy["retired_claims"]["stochastic_dominance"]["old"]
                                + "; " + asy["retired_claims"]["deviation_grows"]["old"],
        "corrected_statement": asy["retired_claims"]["stochastic_dominance"]["new"],
        "supporting_numbers": asy["cross_member_summary"],
        "derived_from": "E2/results/member_*.json :: survival.runs[*]",
        "why_it_moved": asy["retired_claims"]["deviation_grows"]["why_retired"],
    })

    comp = results["composite"]
    ents.append({
        "topic": "The two-stage composite / reachability gate",
        "as_previously_stated": ("a two-stage triage score: a reachability gate at a 0.50 "
                                 "refusal rate, then alpha_50 among the models that pass."),
        "corrected_statement": comp["stage_1_withdrawn_at_power"]["statement"],
        "supporting_numbers": comp["stage_1_withdrawn_at_power"]["iteration_2_measurement"],
        "derived_from": "E1/method_out.json :: metadata.composite and "
                        "metadata.external_validity; the breadth-panel extension is "
                        "reconstructed in this artifact",
        "why_it_moved": ("both base checkpoints cross the gate at full power, so the gate no "
                         "longer separates base from tuned."),
    })

    ents.append({
        "topic": "Pre-registration deviations and amendments",
        "as_previously_stated": "deviations were listed inline across the results sections.",
        "corrected_statement": (
            f"All deviations are tabulated in one place: {len(e1meta.get('prereg_deviations', []) or [])} "
            f"iteration-2 experiment-1 deviations with when_decided, "
            f"{len(e2prereg.get('amendments', []) or [])} timestamped experiment-2 amendments "
            f"each carrying the data state at the time, and {len(v1dev)} reanalysis deviations."),
        "supporting_numbers": {
            "n_E1_deviations": len(e1meta.get("prereg_deviations", []) or []),
            "E1_deviations_with_when_decided": sum(
                1 for d in (e1meta.get("prereg_deviations") or []) if d.get("when_decided")),
            "n_E2_amendments": len(e2prereg.get("amendments", []) or []),
            "n_V1_deviations": len(v1dev),
        },
        "derived_from": "E1/method_out.json :: metadata.prereg_deviations; E2/prereg.json :: "
                        "amendments; V1/deviations.json",
        "why_it_moved": "consolidating them frees main-text space and makes them auditable.",
    })
    return ents


def build(results: dict) -> dict:
    ents = collect_entries(results)
    lines = ["# Appendix: Corrections of Record", "",
             "Every entry below states the claim as previously published, the corrected "
             "statement, the archived file and key it is derived from, and one sentence on why "
             "it moved. All numbers are recomputed from the frozen result trees; nothing here "
             "was re-measured.", ""]
    for i, e in enumerate(ents, 1):
        lines += [f"## A.{i} {e['topic']}", "",
                  f"**As previously stated.** {e['as_previously_stated']}", "",
                  f"**Corrected statement.** {e['corrected_statement']}", "",
                  "**Supporting numbers.**", "", "```json",
                  __import__("json").dumps(e["supporting_numbers"], indent=1, default=str),
                  "```", "",
                  f"**Derived from.** `{e['derived_from']}`", "",
                  f"**Why it moved.** {e['why_it_moved']}", ""]
    md = "\n".join(lines)
    (OUT / "appendix_corrections_of_record.md").write_text(md)

    secs = paper_sections()
    total_words = sum(wc(v) for v in secs.values())
    # Locate, in the iteration-2 main text, the PARAGRAPHS the appendix replaces.
    # Deliberately SPECIFIC markers: a generic token such as "19" or "lambda" matches
    # paragraphs the appendix does not replace and inflates the reduction.
    markers = [
        "-0.714", "0.714, 0.943", "0.771", "-0.086",
        "4.4$\\times$", "4.4x", "0.53--2.32", "0.530", "2.323",
        "deviation grows", "stochastic domin",
        "never labels", "0/21", "0.248",
        "0.700", "0.092", "0.858", "0.113",
        "1 of 19", "**1 of 19**", "17 of 19",
        "identifiable=false", "T_fit", "n_roll",
        "-2.334", "CONTROL_REPRODUCES", "random unit vector",
        "reproduction gate", "8.37", "5.007",
    ]
    skip_sections = {"References", "Bibliography", "PREAMBLE"}
    donor_paras, seen = [], set()
    for name, body in secs.items():
        if name in skip_sections:
            continue
        for para in re.split(r"\n\s*\n", body):
            p = para.strip()
            if not p or p in seen:
                continue
            if any(m in p for m in markers):
                seen.add(p)
                # Headline sections are RESTATED IN PLACE (a sentence changes, the
                # paragraph stays); results sections are where the detail is MOVED out.
                restate_in_place = name in {
                    "Summary of Contributions", "Conclusion", "Related Work", "Discussion",
                    "Abstract"}
                donor_paras.append({
                    "section": name, "words": wc(p),
                    "disposition": "restated_in_place" if restate_in_place else "moved_to_appendix",
                    "excerpt": p[:180]})
    donor_words = sum(d["words"] for d in donor_paras)
    donor_names = sorted({d["section"] for d in donor_paras})
    moved = sum(d["words"] for d in donor_paras if d["disposition"] == "moved_to_appendix")
    restated = donor_words - moved
    stub = (
        "## Corrections of record\n\n"
        "Seven claims from earlier iterations of this work are restated here rather than in the "
        "sections that first made them, and one further set of numbers is corrected in place. "
        "The metric-versus-baseline comparison is recomputed on sign-oriented correlations, "
        "because the raw statistic could not have rewarded a perfect metric; the free-running "
        "versus teacher-forced asymmetry is restated as a right-tail effect conditional on "
        "stream divergence rather than as stochastic dominance; the AMS reproduction gate is "
        "reported criterion by criterion rather than as a flat failure; the layer-sensitivity "
        "check leads with the non-parametric span; and the panel accounting, the judge-"
        "propagation rates and the early-warning-signal re-adjudication are stated with the "
        "numbers that survive. Appendix A gives, for each, the claim as previously stated, the "
        "corrected statement, the archived file and key it derives from, and why it moved.\n")
    (OUT / "main_text_stub.md").write_text(stub)

    acct = {
        "paper_source": str(PAPER_SRC),
        "n_sections_parsed": len(secs),
        "main_text_total_words": total_words,
        "donor_sections": donor_names,
        "n_donor_paragraphs": len(donor_paras),
        "donor_paragraphs": donor_paras,
        "total_marker_matched_words": donor_words,
        "words_restated_in_place_not_removed": restated,
        "words_moved_out_of_main_text": moved,
        "stub_words_added_back": wc(stub),
        "appendix_words_written": wc(md),
        "net_words_removed_from_main_text": moved - wc(stub),
        "achieved_reduction_vs_whole_main_text": (
            (moved - wc(stub)) / total_words if total_words else None),
        "target": "15-20%",
        "target_met": None,
        "matching_rule": (
            "a paragraph of the iteration-2 main text is marker-matched if it contains any of "
            f"the {len(markers)} specific strings identifying a corrected claim (generic tokens "
            "such as '19' or 'lambda' are deliberately excluded because they inflate the count, "
            "and the References section is skipped). A matched paragraph in a HEADLINE section "
            "(Summary of Contributions, Related Work, Discussion, Conclusion) is counted as "
            "RESTATED IN PLACE and contributes nothing to the reduction; only matched paragraphs "
            "in the results sections are counted as MOVED. The full paragraph list with its "
            "disposition is emitted so the paper step can act on it."),
    }
    r = acct["achieved_reduction_vs_whole_main_text"]
    acct["target_met"] = bool(r is not None and r >= 0.15)
    acct["note"] = (
        "the reduction is measured against the iteration-2 main text, which is the text the "
        "paper step edits. The appendix is LONGER than the material it replaces because each "
        "entry carries its provenance -- the saving is realised in the main text, and the "
        "appendix is new back matter."
        + f" The achieved reduction is {r:.1%} against a 15-20% target"
        + (", inside the target band." if 0.15 <= r <= 0.20 else
           (", ABOVE the target band -- the paper step may keep some of the marker-matched "
            "detail in place rather than cut all of it." if r > 0.20 else
            ", BELOW the target band: the marker-matched paragraphs are all the main text "
            "actually spends on the corrected claims, so reaching the target would require "
            "cutting material this analysis has no evidence against. Reported as achieved "
            "rather than inflated.")))
    return {"entries": ents, "reduction_accounting": acct,
            "appendix_path": str(OUT / "appendix_corrections_of_record.md"),
            "stub_path": str(OUT / "main_text_stub.md")}
