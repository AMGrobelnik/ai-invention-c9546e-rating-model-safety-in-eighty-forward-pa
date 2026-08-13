#!/usr/bin/env python3
"""Derived quantities: numbers the draft states that no single source leaf
holds, because they are arithmetic ON source leaves.

Failure scenario 2 of the artifact plan: a claim with no reachable pointer is
UNTRACEABLE *unless* it is a hand-computed derived quantity, in which case the
derivation is added here, the number becomes generated, and the claim is marked
DERIVED_NOW_GENERATED. Each entry names its formula and its input pointers, so
the derivation is auditable rather than a second place to type a number.
"""

from __future__ import annotations

from loguru import logger

from common import OUT, REGISTRY, jdump, jload, resolve_pointer, setup_logging

# name -> (formula string, [(alias, pointer)], python callable over the inputs)
DERIVATIONS = [
    ("gap_archived19_block_to_published_delta",
     "abs(E1 archived-19 Delta_A - the iteration-3 published +0.296)",
     [("E1", "/metadata/results/sensitivity/archived_19_only_Delta_A/member_level/delta"),
      ("E1_PREREG", "/archived_reference_values/delta_19_members")],
     lambda a, b: abs(a - b)),
    ("n_measurable_defined_auroc",
     "READS + AMBIGUOUS over the 30-member detection panel",
     [("E2", "/metadata/results/h1_abliterated_arm/by_arm/aligned_reference/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/aligned_reference/verdicts/AMBIGUOUS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/weight_edited_abliteration/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_candidate/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_unverified/verdicts/READS")],
     lambda *v: sum(v)),
    ("n_reads_total",
     "sum of per-arm READS counts",
     [("E2", "/metadata/results/h1_abliterated_arm/by_arm/aligned_reference/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/weight_edited_abliteration/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_candidate/verdicts/READS"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_unverified/verdicts/READS")],
     lambda *v: sum(v)),
    ("n_undefined_total",
     "sum of per-arm UNDEFINED counts",
     [("E2", "/metadata/results/h1_abliterated_arm/by_arm/weight_edited_abliteration/verdicts/UNDEFINED"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_candidate/verdicts/UNDEFINED"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_unverified/verdicts/UNDEFINED")],
     lambda *v: sum(v)),
    ("n_powered_total",
     "sum of per-arm detection-powered counts (>= 40 refusals AND >= 40 compliances)",
     [("E2", "/metadata/results/h1_abliterated_arm/by_arm/aligned_reference/n_powered"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/weight_edited_abliteration/n_powered"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_candidate/n_powered"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_unverified/n_powered")],
     lambda *v: sum(v)),
    ("n_abliterated_class_total",
     "abliterated-class members = weight-edited + behavioural-uncensored arms",
     [("E2", "/metadata/results/h1_abliterated_arm/by_arm/weight_edited_abliteration/n_members"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_candidate/n_members"),
      ("E2", "/metadata/results/h1_abliterated_arm/by_arm/behavioural_uncensored_unverified/n_members")],
     lambda *v: sum(v)),
    ("rho_gap_member_minus_lineage_our_ams",
     "our-AMS lineage-level rho minus member-level rho (the labelling gap)",
     [("V1", "/metrics_agg/ourAMS_rho_lineage_level"),
      ("V1", "/metrics_agg/ourAMS_rho_member_level")],
     lambda a, b: a - b),
    ("net_B_minus_floor_at_matched",
     "axis B five-class any-refusal minus the axis-D control floor, matched cell",
     [("V2", "/metrics_agg/pooled_matched_rate_B_five_class_any_refusal"),
      ("V2", "/metrics_agg/pooled_matched_control_floor_Z")],
     lambda a, b: a - b),
    ("delta_A_minus_delta_B_scale_panel",
     "SET A minus SET B paired advantage on the 52-member panel",
     [("E1", "/metadata/results/outcome_statistics/a_Delta_A/member_level/delta"),
      ("E1", "/metadata/results/outcome_statistics/d_Delta_B/member_level/delta")],
     lambda a, b: a - b),
]

# AMS Table-I comparison: the published values are quoted IN the draft and are
# not ours to generate, so they are declared here once, as literature constants
# with their source, and the percentage deltas are derived from them.
AMS_TABLE1_PUBLISHED = {
    "Llama_3p2_1B_Instruct": 4.55,
    "gemma_2_2b_it": 4.80,
    "Llama_3p2_3B_Instruct": 8.37,
}
AMS_TABLE1_PUBLISHED_SOURCE = ("AMS as published, Table I (Messenger 2026, IEEE "
                               "Access 14:91723-91737, arXiv:2608.05578) -- an "
                               "external constant, quoted not generated")


def ams_table1_rows(e1: dict) -> list[dict]:
    gate = e1["metadata"]["results"].get("ams_table_I_gate") or {}
    rows = []
    if not gate:
        return rows
    entries = gate.get("checkpoints", [])
    for i, e in enumerate(entries):
        ours, pub = e.get("ours"), e.get("published")
        if ours is None or pub in (None, 0):
            continue
        rows.append({
            "checkpoint": e.get("repo") or f"row{i}",
            "ours": ours, "published": pub,
            "relative_delta_pct": 100.0 * (ours - pub) / pub,
            "formula": "100 * (ours - published) / published",
            "published_source": AMS_TABLE1_PUBLISHED_SOURCE,
        })
    return rows


def random_null_band(e2: dict) -> dict:
    """The measured random-direction READING band: the smallest and largest
    per-member maximum absolute deviation of a random axis's AUROC from 0.5.
    The draft quotes it as '+/-0.075 to +/-0.500' and no single leaf holds it."""
    rows = e2["metadata"]["results"]["sanity_panel"]["rows"]
    per: dict[str, float] = {}
    for r in rows:
        v = r.get("random_null_max_abs_dev")
        if v is None:
            continue
        per[r["checkpoint"]] = max(per.get(r["checkpoint"], 0.0), float(v))
    if not per:
        return {}
    return {
        "n_members_with_a_measured_band": len(per),
        "band_half_width_min": min(per.values()),
        "band_half_width_max": max(per.values()),
        "formula": "per member, max over axes of random_null_max_abs_dev; then "
                   "min and max of that over members",
        "pointer_prefix": "/metadata/results/sanity_panel/rows/*/"
                          "random_null_max_abs_dev",
    }


def build(docs: dict) -> dict:
    out = {"derivations": {}, "notes": {}}
    for name, formula, inputs, fn in DERIVATIONS:
        try:
            vals = [resolve_pointer(docs[a], p) for a, p in inputs]
        except (KeyError, IndexError, ValueError) as exc:
            logger.error(f"derivation {name}: input unreachable ({exc})")
            out["derivations"][name] = {"value": None, "formula": formula,
                                        "inputs": inputs, "error": str(exc)}
            continue
        out["derivations"][name] = {
            "value": fn(*vals), "formula": formula,
            "inputs": [{"alias": a, "pointer": p, "value": v}
                       for (a, p), v in zip(inputs, vals)],
        }
    band = random_null_band(docs["E2"])
    out["random_null_reading_band"] = band
    rows = ams_table1_rows(docs["E1"])
    out["ams_table_i_relative_deltas"] = rows
    out["notes"]["external_constants"] = {
        "ams_table_i_published": AMS_TABLE1_PUBLISHED,
        "source": AMS_TABLE1_PUBLISHED_SOURCE,
    }
    # flat value map, which is what the pointer index consumes
    flat = {k: v["value"] for k, v in out["derivations"].items()
            if v.get("value") is not None}
    for r in rows:
        flat[f"ams_table_i_pct_delta_{r['checkpoint']}"] = r["relative_delta_pct"]
    for k in ("band_half_width_min", "band_half_width_max",
              "n_members_with_a_measured_band"):
        if k in band:
            flat[f"random_null_reading_{k}"] = band[k]
    out["values"] = flat
    return out


def main() -> dict:
    setup_logging("derived")
    docs = {a: jload(REGISTRY[a][0]) for a in ("E1", "E1_PREREG", "E2", "V1", "V2")}
    out = build(docs)
    jdump(out, OUT / "derived.json")
    logger.info(f"derived {len(out['values'])} quantities -> {OUT / 'derived.json'}")
    return out


if __name__ == "__main__":
    main()
