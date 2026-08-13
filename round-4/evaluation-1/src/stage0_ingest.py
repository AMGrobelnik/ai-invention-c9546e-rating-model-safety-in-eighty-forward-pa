#!/usr/bin/env python3
"""STAGE 0 -- ingest, unit assertions, and the reproduction gate.

Nothing downstream is allowed to restate an archived number before this stage
has regenerated it from the archived inputs. A failing leg does NOT stop the
run: reproduction.status becomes FAILED, every downstream statistic that
descends from the failing leg is marked provenance_unverified, and the README
leads with the mismatch.
"""

from __future__ import annotations

import csv
import re

import numpy as np
from loguru import logger

from common import (BOOT_SEED, D1, DRAFT, E3, N_BOOT, OUT, SCORE_COLUMNS, V1,
                    V2, A2_EXP1, A2_EXP2, jdump, jload, require, setup_logging,
                    sha256_file, sx)

TOL = 1e-6

# The archived headline values this stage must regenerate before anything is
# restated. Each is (leg id, archived value, tolerance).
ARCHIVED = {
    "e3_rho_oriented_alpha_50_row": -0.2080952098456918,
    "e3_rho_oriented_our_AMS_row": 0.3578030619574787,
    "e3_rho_oriented_logit_gap_benign_row": 0.10109914527054066,
    "e3_rho_oriented_logit_gap_harmful_row": 0.6672543587855684,
    "e3_rho_oriented_ams_paraphrase_refit": 0.6540675137502804,
    "v2_lineage_oriented_delta": -0.9285714285714287,
    "v2_lineage_rho_ourAMS": 0.8214285714285715,
    "v2_lineage_rho_alpha50": -0.10714285714285716,
}

E3_ROW_TO_COLUMN = {
    "alpha_50": "max_refusal_rate",
    "our_AMS": "ams_sigma",
    "logit_gap_benign": "logit_gap_benign",
    "logit_gap_harmful": "logit_gap_harmful",
}


# --------------------------------------------------------------------------
# HARD RULE 1 -- import the archived definitions, never retype them
# --------------------------------------------------------------------------
def _extract_literal_block(src: str, name: str) -> str:
    """Return the source text of a module-level `NAME = {...}` assignment."""
    m = re.search(rf"^{name} = \{{", src, flags=re.M)
    if m is None:
        raise RuntimeError(f"cannot locate the literal block for {name}")
    i = src.index("{", m.start())
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[m.start():j + 1]
        j += 1
    raise RuntimeError(f"unbalanced braces while extracting {name}")


def load_archived_definitions() -> dict:
    """E3/method.py imports torch at module level, so it is NOT import-safe
    under this artifact's no-torch rule. The plan's pre-decided fallback is
    used: only the two literal constant blocks are exec-ed, with the archived
    statsx module bound as `sx` because PASS_RULES references it."""
    path = E3 / "method.py"
    src = path.read_text()
    ns: dict = {"sx": sx}
    blocks = {}
    for name in ("ORIENTATION_MAP", "PASS_RULES"):
        blocks[name] = _extract_literal_block(src, name)
        exec(compile(blocks[name], f"<{name}>", "exec"), ns)
    prereg = jload(E3 / "prereg_iter3.json")
    route = {
        "route": "EXEC_OF_LITERAL_CONSTANT_BLOCKS",
        "reason": ("E3/method.py imports torch at module level (line 87) and "
                   "calls resource.setrlimit at import time, so importing it "
                   "would violate the artifact's no-torch / no-GPU rule; the "
                   "plan's pre-decided fallback route is used."),
        "sha256_method_py": sha256_file(path),
        "sha256_prereg_iter3_json": sha256_file(E3 / "prereg_iter3.json"),
        "estimator_module_correction": (
            "The plan named lib/stats_ext.py and its function list "
            "(orient / spearman_basic / clustered_bootstrap_rho / "
            "lineage_permutation_p / loo_lineage_jackknife / auc_binary / "
            "paired_rho_delta_clustered / disattenuate / spearman_pair). Those "
            "functions live in lib_iter3/statsx.py; lib/stats_ext.py is the "
            "iteration-2 module with a different API. lib_iter3/statsx.py is "
            "what E3/method.py itself imports as `sx`, and is what is imported "
            "verbatim here."),
        "sha256_lib_iter3_statsx_py": sha256_file(E3 / "lib_iter3" / "statsx.py"),
        "sha256_lib_stats_ext_py": sha256_file(E3 / "lib" / "stats_ext.py"),
        "boot_seed": BOOT_SEED,
        "n_boot": N_BOOT,
    }
    # cross-check the exec-ed literals against the sha256-stamped prereg copy
    orient_match = ns["ORIENTATION_MAP"] == prereg["orientation_map"]
    thresholds_exec = {k: ns["PASS_RULES"][k]["threshold"] for k in ns["PASS_RULES"]}
    thresholds_prereg = {k: prereg["pass_rules"][k]["threshold"]
                         for k in prereg["pass_rules"]}
    route["orientation_map_matches_prereg"] = bool(orient_match)
    route["thresholds_match_prereg"] = bool(thresholds_exec == thresholds_prereg)
    if not (orient_match and thresholds_exec == thresholds_prereg):
        raise RuntimeError("archived definitions disagree between method.py and "
                           "prereg_iter3.json -- refusing to proceed")
    return {"ORIENTATION_MAP": ns["ORIENTATION_MAP"],
            "PASS_RULES": ns["PASS_RULES"],
            "DISCRIMINATION_RULE": prereg["discrimination_rule"],
            "route": route,
            "thresholds": thresholds_exec}


# --------------------------------------------------------------------------
# Panel assembly
# --------------------------------------------------------------------------
def build_panel() -> dict:
    mo = jload(E3 / "full_method_out.json")
    ds = {d["dataset"]: d["examples"] for d in mo["datasets"]}
    members = require(ds, "panel_members", "E3 full_method_out.json datasets")
    cols_ds = require(ds, "score_columns", "E3 full_method_out.json datasets")

    rows = []
    for ex in members:
        m = ex["metadata_meta"]
        rows.append({
            "member_id": require(m, "key", "panel_members meta"),
            "repo": m["repo"],
            "lineage": require(m, "lineage", "panel_members meta"),
            "lineage_id": require(m, "lineage_id", "panel_members meta"),
            "family": m["family"],
            "level": m["level"],
            "n_layers": m["n_layers"],
            "y_refusal": require(m, "y_refusal", "panel_members meta"),
            "y_refusal_ci": m.get("y_refusal_ci"),
            "alpha_50_status": m.get("alpha_50_status"),
        })

    cols = {}
    for ex in cols_ds:
        name = ex["metadata_uid"]
        mm = ex["metadata_meta"]
        cols[name] = {"orientation": require(mm, "orientation", f"score_columns[{name}]"),
                      "values": require(mm, "values", f"score_columns[{name}]"),
                      "statistics": mm["statistics"]}
    missing = [c for c in SCORE_COLUMNS if c not in cols]
    if missing:
        raise KeyError(f"score columns absent from the archive: {missing}")

    # alignment assertion: the values arrays must line up with panel_members
    align = {}
    for col, meta_key in [("alpha_50_logistic", "alpha_50_logistic"),
                          ("alpha_50_nonparametric", "alpha_50_nonparametric"),
                          ("max_refusal_rate", "max_refusal_rate"),
                          ("ams_sigma", "ams_sigma_orig"),
                          ("ams_sigma_para", "ams_sigma_para"),
                          ("ams_sigma_archive", "ams_sigma_archive")]:
        vals = cols[col]["values"]
        worst = 0.0
        for ex, v in zip(members, vals):
            ref = ex["metadata_meta"].get(meta_key)
            if v is None or ref is None:
                if (v is None) != (ref is None):
                    raise AssertionError(
                        f"definedness mismatch for {col} on {ex['metadata_uid']}")
                continue
            worst = max(worst, abs(float(v) - float(ref)))
        align[col] = worst
        if worst > 1e-9:
            raise AssertionError(f"score_columns[{col}] does not align with "
                                 f"panel_members (max delta {worst})")

    for r, ex in zip(rows, members):
        for c in SCORE_COLUMNS:
            r[c] = cols[c]["values"][members.index(ex)] if False else None
    for i, r in enumerate(rows):
        for c in SCORE_COLUMNS:
            r[c] = cols[c]["values"][i]

    # join the UNRELIABLE flag and the archived judged outcome from V2
    with open(V2 / "out" / "member_table.csv", newline="") as f:
        v2rows = {row["member_id"]: row for row in csv.DictReader(f)}
    if set(v2rows) != {r["member_id"] for r in rows}:
        raise AssertionError("V2 member_table.csv does not cover the E3 panel")
    # The two archives do NOT agree on the outcome on every member. Both are
    # carried, the disagreement is measured, and every downstream cell is
    # computed under BOTH.
    y_disagreements = []
    for r in rows:
        v = v2rows[r["member_id"]]
        r["unreliable"] = v["unreliable"].strip().lower() == "true"
        r["exclusion_reason"] = v["exclusion_reason"]
        r["y_e3"] = float(r["y_refusal"])
        r["y_v2"] = float(v["plain_harmful_refusal"])
        r["n_judged_v2"] = int(v["n_judged"])
        if abs(r["y_v2"] - r["y_e3"]) > 1e-12:
            y_disagreements.append({
                "member_id": r["member_id"], "level": r["level"],
                "y_e3_transcribed_archive": r["y_e3"], "y_v2_member_table": r["y_v2"],
                "abs_delta": abs(r["y_v2"] - r["y_e3"]),
                "unreliable": r["unreliable"], "n_judged_v2": r["n_judged_v2"]})
        r["jailbreak_asr"] = float(v["jailbreak_asr"])
        r["xstest_over_refusal"] = float(v["xstest_over_refusal"])

    # HARD RULE 3 -- the clustering unit is the lineage LABEL, not lineage_id
    n_lin = len({r["lineage"] for r in rows})
    n_lid = len({r["lineage_id"] for r in rows})
    assertions = {
        "n_members": len(rows),
        "n_unique_lineage_label": n_lin,
        "n_unique_lineage_id_string": n_lid,
        "clustering_unit": "lineage label (L1..L7)",
        "lineage_id_would_split": sorted(
            {r["lineage"] for r in rows
             if len({q["lineage_id"] for q in rows if q["lineage"] == r["lineage"]}) > 1}),
        "score_column_alignment_max_delta": align,
        "y_outcome_disagreement": {
            "n_members_disagreeing": len(y_disagreements),
            "n_members_agreeing": len(rows) - len(y_disagreements),
            "all_disagreeing_are_unreliable":
                bool(y_disagreements) and all(d["unreliable"] for d in y_disagreements),
            "detail": y_disagreements,
            "finding": (
                "DISCOVERED, not assumed: the outcome variable itself is not "
                "identical across the two frozen archives. E3 transcribes the "
                "iteration-2 archive's judged plain-harmful refusal rate, which "
                "records an identical 12/80 = 0.15 for l1_base, l2_base and "
                "l4_base; V2's member_table.csv re-derives the rate from a larger "
                "judged pool (n_judged 355/325/... against 275) and gets 0.19375, "
                "0.38125 and 0.175. All three disagreeing members are among the 5 "
                "auto-flagged UNRELIABLE and are therefore excluded from every "
                "correlation V2 reports, which is why V2's headline reproduces "
                "under either outcome. Every dual-aggregation cell below is "
                "computed under BOTH outcome variants so the choice is visible."),
        },
    }
    if len(rows) != 19 or n_lin != 7 or n_lid != 8:
        raise AssertionError(f"panel assertions failed: {assertions}")

    return {"rows": rows, "columns": {c: cols[c] for c in SCORE_COLUMNS},
            "assertions": assertions,
            "archived_matrix": mo["metadata"]["analysis"]["matrix"],
            "archived_accounting": mo["metadata"]["analysis"]["accounting"],
            "archived_statistics": mo["metadata"]["analysis"]["statistics"],
            "archived_discrimination_sensitivity":
                mo["metadata"]["analysis"]["discrimination_sensitivity"]}


# --------------------------------------------------------------------------
# Aggregation to lineage units (used by the gate and by stage 1)
# --------------------------------------------------------------------------
def sentinel_value(rows: list[dict], col: str, orientation: int) -> float | None:
    """V2's pre-registered UNDEFINED fallback: rank an undefined member BOTTOM
    on safety by substituting max(defined)+1 for a negatively-oriented score
    (min(defined)-1 for a positively-oriented one). Recovered from
    V2/eval_a34.py:94 (`max(... ) + 1.0`) and verified against
    V2/out/lineage_units.csv, whose constant alpha_50 column is exactly this
    sentinel."""
    vals = [float(r[col]) for r in rows if r.get(col) is not None]
    if not vals:
        return None
    return (max(vals) + 1.0) if orientation < 0 else (min(vals) - 1.0)


def column_values(rows: list[dict], col: str, orientation: int,
                  convention: str = "drop_undefined") -> list[float | None]:
    """`drop_undefined` leaves UNDEFINED cells as None (E3's convention);
    `rank_bottom` substitutes the sentinel (V2's convention)."""
    if convention == "drop_undefined":
        return [None if r.get(col) is None else float(r[col]) for r in rows]
    if convention == "rank_bottom":
        s = sentinel_value(rows, col, orientation)
        return [s if r.get(col) is None else float(r[col]) for r in rows]
    raise ValueError(f"unknown definedness convention {convention!r}")


def lineage_units(rows: list[dict], col: str, ycol: str = "y_e3",
                  reliable_only: bool = False, orientation: int = -1,
                  convention: str = "drop_undefined") -> dict:
    """One unit per lineage: the MEAN over that lineage's DEFINED members of
    both x and y. A lineage with zero defined members drops out."""
    xs = column_values(rows, col, orientation, convention)
    by_lin: dict[str, list[dict]] = {}
    for r, xv in zip(rows, xs):
        if reliable_only and r["unreliable"]:
            continue
        if xv is None or r.get(ycol) is None:
            continue
        rr = dict(r)
        rr["_x"] = xv
        by_lin.setdefault(r["lineage"], []).append(rr)
    units = []
    for lin in sorted(by_lin):
        mem = by_lin[lin]
        units.append({
            "lineage": lin,
            "n_members": len(mem),
            "members": [m["member_id"] for m in mem],
            "x": float(np.mean([float(m["_x"]) for m in mem])),
            "y": float(np.mean([float(m[ycol]) for m in mem])),
        })
    return {"units": units, "n_units": len(units),
            "definedness_convention": convention,
            "reliable_only": reliable_only, "outcome_column": ycol,
            "aggregation_function": "arithmetic mean over the lineage's DEFINED members",
            "n_members_used": sum(u["n_members"] for u in units),
            "dropped_lineages": sorted(
                {r["lineage"] for r in rows} - {u["lineage"] for u in units})}


# --------------------------------------------------------------------------
# HARD RULE 2 -- the reproduction gate
# --------------------------------------------------------------------------
def reproduction_gate(panel: dict, defs: dict) -> dict:
    rows = panel["rows"]
    legs = []

    def leg(name, archived, recomputed, tol=TOL, note=""):
        ok = (recomputed is not None
              and abs(float(recomputed) - float(archived)) <= tol)
        legs.append({"leg": name, "archived": archived, "recomputed": recomputed,
                     "abs_delta": (None if recomputed is None
                                   else abs(float(recomputed) - float(archived))),
                     "tolerance": tol, "pass": bool(ok), "note": note})
        return ok

    y = [r["y_e3"] for r in rows]  # the outcome E3's own matrix was fit against

    # (a) the four per-score oriented rho values in the discrimination matrix
    for row_name, col in E3_ROW_TO_COLUMN.items():
        sign = panel["columns"][col]["orientation"]
        xo = sx.orient([r[col] for r in rows], sign)
        rho = sx.spearman_basic(xo, y)["rho"]
        leg(f"e3_rho_oriented_{row_name}_row", ARCHIVED[f"e3_rho_oriented_{row_name}_row"],
            rho, note=f"member level, n=19, column {col}, orientation {sign:+d}")

    # (b) the AMS paraphrase refit
    sign = panel["columns"]["ams_sigma_para"]["orientation"]
    xo = sx.orient([r["ams_sigma_para"] for r in rows], sign)
    leg("e3_rho_oriented_ams_paraphrase_refit",
        ARCHIVED["e3_rho_oriented_ams_paraphrase_refit"],
        sx.spearman_basic(xo, y)["rho"], note="member level, n=19")

    # (c) V2's lineage-level oriented Delta and its two component rho values.
    # V2 built its lineage units from the RELIABLE members only (19 -> 14) and
    # carried alpha_50 by the non-parametric column.
    sa = panel["columns"]["alpha_50_nonparametric"]["orientation"]
    sb = panel["columns"]["ams_sigma"]["orientation"]
    ua = lineage_units(rows, "alpha_50_nonparametric", ycol="y_v2", reliable_only=True,
                       orientation=sa, convention="rank_bottom")
    ub = lineage_units(rows, "ams_sigma", ycol="y_v2", reliable_only=True,
                       orientation=sb, convention="rank_bottom")
    rho_a = sx.spearman_basic(sx.orient([u["x"] for u in ua["units"]], sa),
                              [u["y"] for u in ua["units"]])["rho"]
    rho_b = sx.spearman_basic(sx.orient([u["x"] for u in ub["units"]], sb),
                              [u["y"] for u in ub["units"]])["rho"]
    leg("v2_lineage_rho_alpha50", ARCHIVED["v2_lineage_rho_alpha50"], rho_a,
        note=f"lineage level, n={ua['n_units']} units over "
             f"{ua['n_members_used']} reliable members, alpha_50_nonparametric")
    leg("v2_lineage_rho_ourAMS", ARCHIVED["v2_lineage_rho_ourAMS"], rho_b,
        note=f"lineage level, n={ub['n_units']} units over "
             f"{ub['n_members_used']} reliable members")
    delta = (rho_a - rho_b) if (rho_a is not None and rho_b is not None) else None
    leg("v2_lineage_oriented_delta", ARCHIVED["v2_lineage_oriented_delta"], delta,
        note="Delta = rho_oriented(alpha_50) - rho_oriented(our-AMS), lineage level")

    # (d) the accounting breakdowns
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["alpha_50_status"]] = counts.get(r["alpha_50_status"], 0) + 1
    expected = {"DEFINED": 1, "UNRELIABLE_NON_MONOTONE": 6,
                "UNDEFINED_MAX_RATE_BELOW_HALF": 8, "UNDEFINED_NONPOSITIVE_SLOPE": 4}
    acc_ok = counts == expected
    legs.append({"leg": "e3_alpha50_status_breakdown_19_18_1",
                 "archived": expected, "recomputed": counts,
                 "abs_delta": None, "tolerance": 0, "pass": bool(acc_ok),
                 "note": "19 members; DEFINED on 1, i.e. 19/18/1"})
    n_unrel = sum(1 for r in rows if r["unreliable"])
    v2_ok = (len(rows) == 19 and len(rows) - n_unrel == 14 and n_unrel == 5)
    legs.append({"leg": "v2_accounting_19_14_1",
                 "archived": {"n_members": 19, "n_analysable": 14,
                              "n_unreliable_excluded": 5},
                 "recomputed": {"n_members": len(rows),
                                "n_analysable": len(rows) - n_unrel,
                                "n_unreliable_excluded": n_unrel},
                 "abs_delta": None, "tolerance": 0, "pass": bool(v2_ok),
                 "note": "the 5 UNRELIABLE members V2 excluded from every correlation"})
    # the single member with a DEFINED logistic estimate is itself excluded
    defined_ids = [r["member_id"] for r in rows if r["alpha_50_status"] == "DEFINED"]
    legs.append({"leg": "defined_logistic_member_is_itself_unreliable",
                 "archived": True,
                 "recomputed": bool(defined_ids
                                    and all(r["unreliable"] for r in rows
                                            if r["member_id"] in defined_ids)),
                 "abs_delta": None, "tolerance": 0,
                 "pass": bool(defined_ids and all(r["unreliable"] for r in rows
                                                  if r["member_id"] in defined_ids)),
                 "note": f"DEFINED on {defined_ids}; after the pre-registered "
                         "exclusion the primary estimator is defined on ZERO "
                         "analysable members"})

    n_fail = sum(1 for L in legs if not L["pass"])
    failing = [L["leg"] for L in legs if not L["pass"]]
    return {"status": "PASSED" if n_fail == 0 else "FAILED",
            "n_legs": len(legs), "n_failed": n_fail, "failing_legs": failing,
            "legs": legs,
            "note": ("A failing leg is a reportable result, not a reason to stop: "
                     "the full analysis continues and every statistic descending "
                     "from a failing leg is marked provenance_unverified.")}


def input_manifest() -> list[dict]:
    files = [
        E3 / "method.py", E3 / "prereg_iter3.json", E3 / "full_method_out.json",
        E3 / "RESULTS.md", E3 / "lib_iter3" / "statsx.py", E3 / "lib" / "stats_ext.py",
        E3 / "lib" / "stats_lib.py", E3 / "lib" / "dose.py",
        E3 / "results" / "reuse_manifest.json", E3 / "results" / "t1_unit_tests.json",
        E3 / "results" / "paraphrase_audit.json",
        V2 / "eval_out.json", V2 / "full_eval_out.json",
        V2 / "out" / "member_table.csv", V2 / "out" / "lineage_units.csv",
        V1 / "eval_out.json", V1 / "results" / "analysis1.json",
        V1 / "results" / "analysis2.json", V1 / "results" / "analysis3.json",
        V1 / "results" / "analysis4.json", V1 / "results" / "provenance.json",
        A2_EXP2 / "full_method_out.json", A2_EXP1 / "full_method_out.json",
        D1, DRAFT,
    ]
    files += sorted((E3 / "results").glob("iter3_member_*.json"))
    files += sorted((V1 / "results").glob("encode_*.json"))
    man = []
    for p in files:
        if not p.exists():
            man.append({"path": str(p), "exists": False, "sha256": None, "bytes": None})
            continue
        man.append({"path": str(p), "exists": True, "sha256": sha256_file(p),
                    "bytes": p.stat().st_size})
    return man


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage0")
    logger.info("STAGE 0 -- ingest, assertions, reproduction gate")
    defs = load_archived_definitions()
    logger.info(f"archived definitions loaded via {defs['route']['route']}")
    panel = build_panel()
    logger.info(f"panel: {panel['assertions']}")
    gate = reproduction_gate(panel, defs)
    for L in gate["legs"]:
        logger.info(f"  gate[{L['leg']}] {'PASS' if L['pass'] else 'FAIL'} "
                    f"archived={L['archived']} recomputed={L['recomputed']}")
    logger.info(f"reproduction gate: {gate['status']} "
                f"({gate['n_legs'] - gate['n_failed']}/{gate['n_legs']} legs)")

    out = {
        "stage": "stage0_ingest",
        "inputs": input_manifest(),
        "archived_definitions_route": defs["route"],
        "orientation_map": defs["ORIENTATION_MAP"],
        "pass_rule_thresholds": defs["thresholds"],
        "discrimination_rule": defs["DISCRIMINATION_RULE"],
        "panel_assertions": panel["assertions"],
        "panel_rows": panel["rows"],
        "score_column_orientation": {c: panel["columns"][c]["orientation"]
                                     for c in SCORE_COLUMNS},
        "archived_matrix": panel["archived_matrix"],
        "archived_accounting": panel["archived_accounting"],
        "archived_statistics": panel["archived_statistics"],
        "archived_discrimination_sensitivity":
            panel["archived_discrimination_sensitivity"],
        "reproduction": gate,
        "cost_usd": 0.0,
    }
    jdump(out, OUT / "stage0.json")
    logger.info(f"wrote {OUT / 'stage0.json'}")
    return out


if __name__ == "__main__":
    main()
