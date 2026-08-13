#!/usr/bin/env python3
"""Recheck the read-versus-act coupling and the verdict rule.

PURE REANALYSIS of the frozen iteration-4 read-versus-act tree.
Zero GPU, zero generation, zero LLM API calls, $0.00 spend.

    stage0_prereg  provenance manifest + the sha256-stamped pre-registration
    stage1_gate    the 7-group reproduction gate (G1 is stop-the-line)
    stage2_hc      H-C: the coupling without the between-axis-type contrast
    stage3_hk      H-K: the verdict rule, its operating characteristic, and the
                   abliterated arm restated on refusal-RATE evidence
    stage4_prose   the replacement-text bundle + the executed pointer assertion
    assemble       eval_out.json (schema payload) and RESULTS.md

Ordering follows the plan's time-pressure rule: the gate first, then the
table-shaped H-K legs, then the H-C primary and ladder, then the simulation.
Whatever completes is reported with an explicit completion manifest.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from loguru import logger

import assemble
import stage0_prereg
import stage1_gate
import stage2_hc
import stage3_hk
import stage4_prose
from common5 import HERE, OUT, jdump, jload, setup_logging

T0 = time.time()


def plan_corrections(s1, s2, s3) -> list[dict]:
    """Measured corrections to the artifact plan. The plan's numbers are stated
    as expectations; where the files disagree, the files win and the difference
    is recorded rather than quietly absorbed."""
    sec = s2["secondary_c50"]
    lev = s1["g4_levels"]
    missing = sorted(Path(p).name.replace("proj_", "").replace(".npz", "")
                     for p in lev["missing_npz"])
    dev = s3["deviation_record"]["affected_members"]
    return [
        {"item": "censored axis-A c_50 among the detection-powered members",
         "plan_said": "7 of the 14 powered members have '--' c_50 in T3",
         "measured": (f"{sec['n_censored']} of {sec['n_members']} "
                      f"(censoring fraction {sec['censoring_fraction']:.3f}); the "
                      f"0.771 figure the plan is recalling is the censoring "
                      f"fraction over all 70 (member, axis) PAIRS, not over the "
                      f"14 axis-A members. Censored members: "
                      + ", ".join(sec["censored_members"]))},
        {"item": "which members lack per-item projections",
         "plan_said": ("6 members lack a proj_*_items.json: BADMISTRAL, "
                       "Qwen2p5_1p5B_Instruct_abliterated and the fully-UNDEFINED "
                       "members"),
         "measured": (f"{lev['n_summary_level']} members lack proj_*.npz and are "
                      f"reproduced at summary level: " + ", ".join(missing)
                      + ". BADMISTRAL_1p5B and the fully-UNDEFINED members DO have "
                        "stored projections and are reproduced at item level.")},
        {"item": "the stale 18/0/10 verdict tally",
         "plan_said": "the artifact's stale top-line summary says 18/0/10",
         "measured": (s1["verdict_tally_resolution"]["diagnosis"])},
        {"item": "the lineage-id-string trap",
         "plan_said": ("8 distinct lineage_id strings span only 7 lineages, so "
                       "clustering on the id string silently splits one lineage; "
                       "re-verify on this panel"),
         "measured": s1["lineage_bookkeeping"]["note"]},
        {"item": "members that are UNPOWERED yet receive READS",
         "plan_said": ("DAN_Qwen3_1p7B 6/6, Josiefied_Qwen2p5_3B 12/12, "
                       "Josiefied_Qwen3_4B 32/32, Llama_3p2_1B 28/28, "
                       "Llama_3p2_1B_Instruct_abliterated 28/28, "
                       "Qwen2p5_0p5B_Instruct_abliterated 33/33, TinyLlama 7/7 -- "
                       "verify each against the JSON"),
         "measured": (f"verified against method_out.json: "
                      f"{dev['n_UNPOWERED_yet_READS']} members, "
                      + ", ".join(f"{m['checkpoint']} {m['n_refusal']}/"
                                  f"{m['n_compliance']}"
                                  for m in dev["UNPOWERED_yet_READS"]))},
    ]


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("eval")
    logger.info("=" * 78)
    logger.info("iter-5 evaluation: recheck the read-vs-act coupling and the "
                "verdict rule -- PURE REANALYSIS, $0.00, zero GPU")
    logger.info("=" * 78)

    manifest: dict[str, str] = {}

    s0 = stage0_prereg.main()
    manifest["stage0 provenance + prereg"] = "COMPLETED"

    s1 = stage1_gate.main()
    manifest["stage1 reproduction gate"] = (
        f"COMPLETED ({s1['n_pass']}/{s1['n_legs']} legs PASS, "
        f"{s1['gate_verdict']})")
    if s1["stop_and_diagnose"]:
        logger.error("G1 FAILED -- shipping a diagnostic-only eval_out.json")
        manifest["stage2 H-C"] = "NOT RUN (G1 failed, restatement abandoned)"
        manifest["stage3 H-K"] = "NOT RUN (G1 failed, restatement abandoned)"
        doc = {"metadata": {"diagnostic_only": True,
                            "reason": "reproduction gate leg G1 failed",
                            "reproduction_gate": s1, "provenance": s0["provenance"],
                            "completion_manifest": manifest},
               "metrics_agg": {"gate_n_pass": float(s1["n_pass"]),
                               "gate_n_legs": float(s1["n_legs"])},
               "datasets": [{"dataset": "reproduction_gate",
                             "examples": [{"input": l["leg"],
                                           "output": str(l["target"])}
                                          for l in s1["legs"]]}]}
        jdump(HERE / "eval_out.json", doc)
        return

    # H-K first: cheap, table-shaped, and it alone satisfies most of the review
    # item. The simulation is the last thing inside it.
    s3 = stage3_hk.main()
    manifest["stage3 H-K tallies + deviation + abliterated arm"] = "COMPLETED"
    manifest["stage3 attainability simulation"] = (
        f"COMPLETED ({s3['attainability_simulation']['n_cells']} cells, "
        f"{s3['attainability_simulation']['wall_seconds']:.0f}s)")

    s2 = stage2_hc.main()
    manifest["stage2 H-C primary + ladder + decomposition"] = "COMPLETED"

    corrections = plan_corrections(s1, s2, s3)

    doc_meta = {
        "evaluation_name": "recheck the read-versus-act coupling and the verdict rule",
        "kind": "pure reanalysis of the frozen iteration-4 tree",
        "prereg_sha256": s0["prereg_sha256"],
        "prereg": s0["prereg"],
        "upstream_prereg_sha256": s0["upstream_prereg_sha256_recomputed"],
        "provenance": dict(s0["provenance"], wall_seconds=None),
        "reproduction_gate": s1,
        "analysis1": s2,
        "analysis2": s3,
        "plan_corrections": corrections,
        "completion_manifest": manifest,
    }

    # the prose is generated FROM this document, then audited against it
    doc_for_prose = doc_meta
    s4 = stage4_prose.main(doc_for_prose)
    manifest["stage4 replacement text + pointer assertion"] = (
        f"COMPLETED ({s4['n_pass']}/{s4['n_pointers']} pointers resolve; "
        f"assertion {'PASSED' if s4['assertion_passed'] else 'FAILED'})")
    doc_meta["replacement_text"] = {
        "markdown": s4["replacement_text_markdown"],
        "sections": s4["bundle_rendered"],
        "audit": {k: s4[k] for k in
                  ("pointer_audit", "n_pointers", "n_pass", "n_mismatch",
                   "n_unresolvable", "all_pointers_resolve",
                   "banned_salvage_tokens_found", "salvage_ban_respected",
                   "assertion_passed")},
    }
    doc_meta["completion_manifest"] = manifest
    doc_meta["provenance"]["wall_seconds"] = round(time.time() - T0, 1)

    doc = {"metadata": doc_meta,
           "metrics_agg": assemble.build_metrics_agg(s1, s2, s3),
           "datasets": assemble.build_datasets(s1, s2, s3)}
    jdump(HERE / "eval_out.json", doc)

    # figures are rendered FROM the written eval_out.json, so they cannot
    # disagree with it, and are then recorded back into it
    import figures
    figs = figures.main(doc)
    doc_meta["figures"] = figs["figures"]
    manifest["3 vector figures"] = (
        f"COMPLETED ({sum(f['ok'] for f in figs['figures'])}/3 rendered as "
        f"PDF + PNG)")

    manifest["RESULTS.md rendered from eval_out.json"] = (
        "COMPLETED (double-rendered and compared byte for byte)")
    doc_meta["completion_manifest"] = manifest
    results = assemble.write_results_md(doc_meta)
    doc_meta["results_md"] = results
    if not results["regenerates_byte_identically"]:
        logger.error("RESULTS.md does NOT regenerate byte-identically")
        manifest["RESULTS.md rendered from eval_out.json"] = (
            "COMPLETED but NOT byte-identical on re-render")
        doc_meta["completion_manifest"] = manifest
        assemble.write_results_md(doc_meta)
    jdump(HERE / "eval_out.json", doc)
    logger.info(f"eval_out.json written: "
                f"{(HERE / 'eval_out.json').stat().st_size / 1e6:.2f} MB, "
                f"{len(doc['metrics_agg'])} aggregate metrics, "
                f"{len(doc['datasets'])} datasets")

    # HARD ASSERTION: the run fails if any number in the emitted prose is
    # untraceable, mismatched, or if a banned salvage token appears.
    if not s4["assertion_passed"]:
        logger.error("PROSE ASSERTION FAILED -- see metadata.replacement_text.audit")
        raise SystemExit(2)
    logger.info(f"DONE in {time.time() - T0:.1f}s -- "
                f"verdict {s2['verdict']['verdict']}, gate {s1['gate_verdict']}")


if __name__ == "__main__":
    main()
