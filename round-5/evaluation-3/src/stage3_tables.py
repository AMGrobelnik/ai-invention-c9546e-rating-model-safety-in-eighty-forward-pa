#!/usr/bin/env python3
"""STAGE 3 -- TABLES, generated from JSON in markdown AND csv.

(a) the per-member detection table, WITH the two columns whose absence let a
    READS verdict issued on a handful of refusals read as equivalent to one
    issued on hundreds: `n refusals / n compliances` and `powered (y/N)`;
(b) the dual-aggregation table, every score x unit x config with the unit named
    in every row label, extended with the H-G scale-panel rows if that artifact
    exists and shipped with a schema-stable stub if it does not;
(c) the table-numbering map by FIRST APPEARANCE, asserted to be a bijection.
"""

from __future__ import annotations

import csv
import re

from loguru import logger

from common import OUT, REGISTRY, TABLES, jdump, jload, setup_logging

SCORE_LABEL = {
    "alpha_50_logistic": "alpha_50 (logistic)",
    "alpha_50_nonparametric": "alpha_50 (non-parametric)",
    "max_refusal_rate": "max refusal rate (alpha_50 surrogate)",
    "ams_sigma": "our-AMS sigma",
    "ams_sigma_para": "our-AMS sigma (paraphrase refit)",
    "ams_sigma_archive": "our-AMS sigma (archived)",
    "logit_gap_benign": "logit-gap (benign)",
    "logit_gap_harmful": "logit-gap (harmful)",
}
UNIT_LABEL = {"member_level": "member (checkpoint)",
              "lineage_level": "lineage (aggregated)"}


def f(x, nd=3):
    if x is None:
        return "--"
    if isinstance(x, str):
        return x
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if v != v:
        return "--"
    return f"{v:.{nd}f}"


def fci(ci, nd=3):
    if not ci or any(v is None or v != v for v in ci):
        return "--"
    return f"[{float(ci[0]):.{nd}f}, {float(ci[1]):.{nd}f}]"


def fp(x):
    if x is None or x != x:
        return "--"
    return f"{x:.2e}" if x < 1e-3 else f"{x:.4f}"


def write_table(rows: list[dict], header: list[str], stem: str, caption: str):
    md = [f"**{caption}**\n", "| " + " | ".join(header) + " |",
          "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        md.append("| " + " | ".join(str(r.get(h, "")) for h in header) + " |")
    (TABLES / f"{stem}.md").write_text("\n".join(md) + "\n")
    with open(TABLES / f"{stem}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    logger.info(f"wrote {stem}.md / .csv ({len(rows)} rows)")


# ==========================================================================
# (a) per-member detection
# ==========================================================================
def table_detection(e2: dict) -> dict:
    per = e2["metadata"]["results"]["h1_abliterated_arm"]["per_member"]
    induce = {r["checkpoint"]: r for r in
              e2["metadata"]["results"]["h1b_induction_paired"]["per_member"]}
    rows, tally, powered = [], {}, 0
    for r in sorted(per, key=lambda x: x["checkpoint"]):
        k = r["checkpoint"]
        i = induce.get(k, {})
        v = r["A_verdict"]
        tally[v] = tally.get(v, 0) + 1
        powered += int(bool(r.get("powered")))
        mc = r.get("matched_contrast") or {}
        rows.append({
            "member": f"`{k}`",
            "class": r.get("member_class", "?"),
            "arm": r.get("arm", "?"),
            "n refusals / n compliances": f"{r.get('n_refusal')} / {r.get('n_compliance')}",
            "spontaneous refusal rate": f(r.get("spontaneous_refusal_rate"), 4),
            "powered (y/N)": "y" if r.get("powered") else "N",
            "axis-A AUROC": f(r.get("A_auroc")),
            "95% CI": fci(r.get("A_ci95")),
            "verdict": v,
            "norm-controlled cos AUROC": f(r.get("A_auroc_norm_controlled")),
            "norm-controlled verdict": r.get("A_verdict_norm_controlled", "--"),
            "residual-norm-only AUROC": f((r.get("residual_norm_baseline") or {})
                                          .get("auroc")),
            "induction: A max refusal rate": f(r.get("A_max_rate")),
            "induction: A c50": f(r.get("A_c50"), 2),
            "induction works": str(bool(r.get("A_induction_works"))),
            "matched-contrast verdict": mc.get("verdict", "--"),
        })
    header = list(rows[0].keys())
    foot = {"member": "**totals**", "class": "",
            "arm": f"{len(rows)} members",
            "n refusals / n compliances": "",
            "spontaneous refusal rate": "",
            "powered (y/N)": f"{powered} powered",
            "axis-A AUROC": "", "95% CI": "",
            "verdict": ", ".join(f"{n} {v}" for v, n in sorted(tally.items())),
            "norm-controlled cos AUROC": "", "norm-controlled verdict": "",
            "residual-norm-only AUROC": "", "induction: A max refusal rate": "",
            "induction: A c50": "", "induction works": "",
            "matched-contrast verdict": ""}
    rows_out = rows + [foot]
    write_table(rows_out, header, "table_detection_per_member",
                "Per-member detection on each model's OWN spontaneous text. "
                "Unit: the member; the AUROC bootstrap is clustered on the "
                "prompt. `powered` is the >= 40-per-class rule; note it is NOT "
                "what gates the UNDEFINED verdict -- that fires when the "
                "bootstrap interval is undefined.")
    return {"n_rows": len(rows), "verdict_tally": tally, "n_powered": powered,
            "columns": header,
            "powered_rule": ">= 40 refusals AND >= 40 compliances after the "
                            "escalation ladder (explib.MIN_PER_CLASS)"}


# ==========================================================================
# (b) dual aggregation, plus the H-G extension or its stub
# ==========================================================================
HG_ROW_SPEC = [
    ("logit_gap_harmful", "member_level"), ("logit_gap_harmful", "lineage_level"),
    ("logit_gap_benign", "member_level"), ("logit_gap_benign", "lineage_level"),
    ("ams_sigma", "member_level"), ("ams_sigma", "lineage_level"),
]


def table_dual(v1s1: dict, e1: dict, hg: dict) -> dict:
    header = ["score", "aggregation unit", "config", "n", "n lineages",
              "orientation", "oriented rho", "raw rho", "95% CI",
              "permutation p", "permutation floor", "at floor",
              "AUC (median split)", "LOO jackknife range", "source"]
    rows = []
    for cfg_id, cfg in sorted(v1s1["table"].items()):
        for col in sorted(cfg["scores"]):
            e = cfg["scores"][col]
            for lvl in ("member_level", "lineage_level"):
                c = e[lvl]
                perm = c.get("permutation") or {}
                jk = c.get("jackknife") or {}
                rows.append({
                    "score": SCORE_LABEL.get(col, col),
                    "aggregation unit": UNIT_LABEL[lvl],
                    "config": cfg_id, "n": c.get("n"),
                    "n lineages": c.get("n_lineages_used"),
                    "orientation": f"{c.get('orientation_sign'):+d}"
                                   if c.get("orientation_sign") is not None else "--",
                    "oriented rho": f(c.get("rho_oriented")),
                    "raw rho": f(c.get("rho_raw_unoriented")),
                    "95% CI": fci(c.get("ci95")),
                    "permutation p": fp(perm.get("p")),
                    "permutation floor": fp(perm.get("p_min_achievable")),
                    "at floor": str(perm.get("p_at_permutation_floor")),
                    "AUC (median split)": f((c.get("auc_y_above_median") or {})
                                            .get("auc")),
                    "LOO jackknife range": fci(jk.get("range")),
                    "source": "iteration-4 eval_1 (19-member / 7-lineage panel)",
                })
    n_base = len(rows)

    # the 52-member scale panel is a second, independently computed block that
    # belongs in the same table because it answers the same question at a
    # different panel size.
    for col in ("orig_sigma", "refitA_sigma", "refitB_sigma"):
        sc = e1["metadata"]["results"]["score_columns"][col]
        for lvl, key in (("member_level", "member_level"),
                         ("lineage_level", "lineage_aggregated")):
            c = sc.get(key)
            if not c:
                continue
            rows.append({
                "score": f"our-AMS {col.replace('_sigma', '')} (scale panel)",
                "aggregation unit": UNIT_LABEL[lvl],
                "config": "scale_panel_52_members_28_lineages",
                "n": c.get("n"), "n lineages": c.get("n_lineages"),
                "orientation": "+1",
                "oriented rho": f(c.get("rho")), "raw rho": f(c.get("rho")),
                "95% CI": fci(c.get("ci95_lineage_clustered") or c.get("ci95")),
                "permutation p": "--", "permutation floor": "--",
                "at floor": "--",
                "AUC (median split)": f((c.get("auc") or {}).get("auc")),
                "LOO jackknife range": "--",
                "source": "iteration-4 experiment_1 (52-member / 28-lineage panel)",
            })

    status = "PRESENT" if hg["status"] == "PRESENT" else "ABSENT_AT_RUN_TIME"
    stub = None
    if status == "PRESENT":
        for path_entry in hg["hits"]:
            doc = jload(path_entry["path"])
            for col, lvl in HG_ROW_SPEC:
                try:
                    c = doc["metadata"]["results"]["score_columns"][col][
                        "member_level" if lvl == "member_level"
                        else "lineage_aggregated"]
                except (KeyError, TypeError):
                    continue
                rows.append({
                    "score": f"{SCORE_LABEL.get(col, col)} (H-G scale panel)",
                    "aggregation unit": UNIT_LABEL[lvl],
                    "config": "h_g_scale_panel",
                    "n": c.get("n"), "n lineages": c.get("n_lineages"),
                    "orientation": "+1", "oriented rho": f(c.get("rho")),
                    "raw rho": f(c.get("rho")),
                    "95% CI": fci(c.get("ci95_lineage_clustered") or c.get("ci95")),
                    "permutation p": fp((c.get("permutation") or {}).get("p")),
                    "permutation floor": fp((c.get("permutation") or {})
                                            .get("p_min_achievable")),
                    "at floor": "--", "AUC (median split)": "--",
                    "LOO jackknife range": "--",
                    "source": f"H-G {path_entry['sha256'][:12]}",
                })
    else:
        stub = {
            "status": "ABSENT_AT_RUN_TIME",
            "instruction": "one-line merge: append these rows verbatim once the "
                           "H-G artifact exists; do NOT forecast the values",
            "rows_to_fill": [
                {"score": f"{SCORE_LABEL.get(col, col)} (H-G scale panel)",
                 "aggregation unit": UNIT_LABEL[lvl],
                 "config": "h_g_scale_panel",
                 "json_pointer": f"/metadata/results/score_columns/{col}/"
                                 + ("member_level" if lvl == "member_level"
                                    else "lineage_aggregated"),
                 "fields": ["n", "n_lineages", "rho", "ci95_lineage_clustered",
                            "permutation.p", "permutation.p_min_achievable"]}
                for col, lvl in HG_ROW_SPEC],
        }
        for col, lvl in HG_ROW_SPEC:
            rows.append({
                "score": f"{SCORE_LABEL.get(col, col)} (H-G scale panel)",
                "aggregation unit": UNIT_LABEL[lvl],
                "config": "h_g_scale_panel", "n": "TO BE FILLED",
                "n lineages": "TO BE FILLED", "orientation": "TO BE FILLED",
                "oriented rho": "TO BE FILLED", "raw rho": "TO BE FILLED",
                "95% CI": "TO BE FILLED", "permutation p": "TO BE FILLED",
                "permutation floor": "TO BE FILLED", "at floor": "TO BE FILLED",
                "AUC (median split)": "TO BE FILLED",
                "LOO jackknife range": "TO BE FILLED",
                "source": "H_G_ROWS=ABSENT_AT_RUN_TIME (schema-stable stub)",
            })

    write_table(rows, header, "table_dual_aggregation",
                "Every score against the judged plain-harmful refusal rate, at "
                "BOTH aggregation units, with the unit named in every row. The "
                "H-G scale-panel block is a schema-stable stub when that "
                "artifact is absent; no value there is forecast.")
    return {"n_rows": len(rows), "n_rows_iteration4_eval1": n_base,
            "h_g_rows_status": f"H_G_ROWS={status}", "h_g_stub": stub,
            "columns": header}


# ==========================================================================
# (c) numbering map by first appearance
# ==========================================================================
def numbering_map(draft: dict) -> dict:
    text = draft["paper_text"]
    ref_rx = re.compile(r"\bTable\s+(\d+)\b")
    caption_rx = re.compile(r"^\*\*Table\s+(\d+)\.", re.M)
    fig_ref_rx = re.compile(r"\[FIGURE:(fig\d+)\]")

    references = [(m.start(), int(m.group(1))) for m in ref_rx.finditer(text)]
    captions = {int(m.group(1)): m.start() for m in caption_rx.finditer(text)}
    defined = set(captions)

    order, seen = [], set()
    for _, n in references:
        if n not in seen:
            seen.add(n)
            order.append(n)
    for n in sorted(defined - seen):
        order.append(n)
    old_to_new = {str(old): i + 1 for i, old in enumerate(order)}

    bijection = (sorted(old_to_new.values()) == list(range(1, len(order) + 1))
                 and len(set(old_to_new)) == len(old_to_new))
    referenced_but_undefined = sorted(seen - defined)
    defined_but_unreferenced = sorted(defined - seen)

    rewritten = ref_rx.sub(lambda m: f"Table {old_to_new[m.group(1)]}", text)
    rewritten = caption_rx.sub(lambda m: f"**Table {old_to_new[m.group(1)]}.",
                               rewritten)

    fig_order, fseen = [], set()
    for m in fig_ref_rx.finditer(text):
        if m.group(1) not in fseen:
            fseen.add(m.group(1))
            fig_order.append(m.group(1))
    fig_ids = [f["id"] for f in draft.get("figures", [])]
    fig_map = {fid: i + 1 for i, fid in enumerate(fig_order)}
    for fid in fig_ids:
        if fid not in fig_map:
            fig_map[fid] = len(fig_map) + 1

    out = {
        "tables": {
            "appearance_order_old_numbers": order,
            "old_to_new": old_to_new,
            "is_bijection": bijection,
            "referenced_but_no_table_object": referenced_but_undefined,
            "table_object_never_referenced": defined_but_unreferenced,
            "first_reference_offsets": {str(n): next(o for o, k in references
                                                     if k == n)
                                        for n in sorted(seen)},
            "note": "renumbering is by FIRST APPEARANCE in reading order; the "
                    "draft currently introduces Table 5 before Table 2 and "
                    "first mentions Table 1 well into the results",
        },
        "figures": {
            "appearance_order": fig_order,
            "declared_ids": fig_ids,
            "old_to_new": fig_map,
            "declared_but_never_referenced": [f for f in fig_ids
                                              if f not in fig_order],
            "referenced_but_not_declared": [f for f in fig_order
                                            if f not in fig_ids],
        },
    }
    jdump(out, OUT / "table_numbering_map.json")
    (OUT / "cross_references_renumbered.md").write_text(rewritten)
    logger.info(f"numbering map: {old_to_new}, bijection={bijection}")
    return out


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage3")
    logger.info("STAGE 3 -- tables")
    e2 = jload(REGISTRY["E2"][0])
    e1 = jload(REGISTRY["E1"][0])
    v1s1 = jload(REGISTRY["V1_S1"][0])
    draft = jload(REGISTRY["DRAFT"][0])
    hg = jload(OUT / "stage0_manifest.json")["h_g_probe"]

    out = {
        "stage": "stage3_tables",
        "table_detection_per_member": table_detection(e2),
        "table_dual_aggregation": table_dual(v1s1, e1, hg),
        "table_numbering_map": numbering_map(draft),
    }
    jdump(out, OUT / "stage3_tables.json")
    logger.info(f"wrote {OUT / 'stage3_tables.json'}")
    return out


if __name__ == "__main__":
    main()
