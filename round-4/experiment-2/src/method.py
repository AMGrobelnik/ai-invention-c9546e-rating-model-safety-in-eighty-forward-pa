#!/usr/bin/env python3
"""Does the refusal axis read or only push?

Runs every panel member through BOTH roles of the same five axes -- detection
(held-out AUROC of the axis projection on the model's OWN generated refusals vs
compliances) and induction (a steering sweep in axis-contrast units) -- and
reports the three pre-registered headlines plus the joint read-versus-act
scatter.

Stages
  --stage prereg    stamp results/prereg.json
  --stage panel     resolve the panel off the frozen manifest
  --stage gpu       per-member axes + detection + induction (checkpointed)
  --stage analysis  H1/H2/H3 + method_out.json + RESULTS.md
"""

from __future__ import annotations

import argparse
import gc
import json
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import psutil
from loguru import logger

import explib as EX

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(EX.HERE / "logs").mkdir(exist_ok=True)
logger.add(EX.HERE / "logs/run.log", rotation="30 MB", level="DEBUG")

_avail = psutil.virtual_memory().available
RAM_BUDGET = int(min(40e9, _avail * 0.5))
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

HF_CACHE = Path.home() / ".cache/huggingface/hub"
DISK_FLOOR_GB = 8.0


# ==========================================================================
def purge_hf_cache(keep_repo: str | None = None) -> dict:
    """Free disk between members: the box has 40 GB and the panel is ~120 GB."""
    freed = 0
    if not HF_CACHE.exists():
        return {"freed_gb": 0.0, "n_removed": 0}
    n = 0
    keep = f"models--{(keep_repo or '').replace('/', '--')}"
    for d in HF_CACHE.glob("models--*"):
        if d.name == keep:
            continue
        try:
            sz = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
            shutil.rmtree(d)
            freed += sz
            n += 1
        except OSError as exc:
            logger.warning(f"could not purge {d.name}: {exc}")
    return {"freed_gb": freed / 1e9, "n_removed": n}


def free_disk_gb() -> float:
    st = shutil.disk_usage(HF_CACHE.parent if HF_CACHE.exists() else Path.home())
    return st.free / 1e9


# ==========================================================================
def stage_panel() -> dict:
    res = EX.resolve_panel()
    logger.info(f"panel queued: {len(res['panel'])} members "
                f"({res['n_abliterated_class_queued']} abliterated-class, "
                f"{res['n_parents_queued']} parents); "
                f"{len(res['skipped_candidates'])} candidates skipped")
    for m in res["panel"]:
        logger.info(f"  prio{m['priority']} {m['params_b']:5.2f}B "
                    f"{m['member_class']:22s} {m['repo']}")
    EX.atomic_write_json(EX.RESULTS / "panel_resolved.json", res)
    return res


# ==========================================================================
def stage_gpu(budget_min: float, only: list[str] | None = None,
              max_members: int | None = None, refresh_detection: bool = False) -> dict:
    import gpu_stage as GS

    panel = EX.load_json(EX.RESULTS / "panel_resolved.json")["panel"]
    if only:
        panel = [m for m in panel if m["key"] in only or m["repo"] in only]
    if max_members:
        panel = panel[:max_members]

    ratchet = EX.Ratchet(budget_min)
    log: list[dict] = []
    for m in panel:
        key = m["key"]
        done_d = (EX.RESULTS / f"detect_{key}.json").exists()
        done_i = (EX.RESULTS / f"induce_{key}.json").exists()
        if refresh_detection:
            # Re-run axes + detection ONLY, preserving the existing induction sweep.
            # Used to backfill the empirical random null onto members measured
            # before it was added, without paying for the steering sweep again.
            if not done_d:
                continue
            if "random_null" in EX.load_json(EX.RESULTS / f"detect_{key}.json"
                                             )["detection"]:
                log.append({"key": key, "status": "null_already_present"})
                continue
        elif done_d and done_i:
            logger.info(f"[{key}] already complete, skipping")
            log.append({"key": key, "status": "cached"})
            continue
        if not ratchet.can_start():
            logger.warning(f"RATCHET: {ratchet.remaining() / 60:.0f} min left, "
                           f"stop launching new members at {key}")
            log.append({"key": key, "status": "skipped_ratchet",
                        "remaining_min": ratchet.remaining() / 60})
            continue

        purge_hf_cache(keep_repo=m["repo"])
        if free_disk_gb() < DISK_FLOOR_GB + m["params_b"] * 2.5:
            logger.error(f"[{key}] insufficient disk ({free_disk_gb():.1f} GB free)")
            log.append({"key": key, "status": "skipped_disk",
                        "free_gb": free_disk_gb()})
            continue

        t0 = time.time()
        try:
            out = GS.run_member(m, detection_only=refresh_detection)
            ratchet.record(out["seconds"])
            log.append({"key": key, "status": "ok", "seconds": out["seconds"],
                        "powered": out["detect"]["powered"]})
        except Exception as exc:  # noqa: BLE001 - one bad member must not kill the run
            logger.exception(f"[{key}] FAILED")
            log.append({"key": key, "status": "failed", "reason": repr(exc)[:400],
                        "seconds": time.time() - t0})
            EX.free_cuda()
            gc.collect()
        EX.atomic_write_json(EX.RESULTS / "gpu_log.json",
                             {"log": log, "ratchet": ratchet.report()})
        logger.info(f"--- ratchet: {ratchet.elapsed() / 60:.0f} min used, "
                    f"{ratchet.remaining() / 60:.0f} min left, "
                    f"median {ratchet.report()['median_member_s']}s/member")
    purge_hf_cache()
    return {"log": log, "ratchet": ratchet.report()}


# ==========================================================================
# Analysis
# ==========================================================================
ABL_CLASSES = ("abliterated", "behavioral_uncensored")


def _load_members() -> list[dict]:
    """Per-member checkpoints, joined to the manifest's provenance flags.

    `h4_status` matters for reading the abliterated arm: the manifest marks a
    checkpoint 'candidate' only when its card evidences a behavioural
    uncensoring, and 'not_applicable' otherwise.  Several repos the manifest
    classes as behavioural_uncensored (the reallexi/lexi-* task models) are
    'not_applicable' and refuse copiously, so pooling them with the
    weight-edited abliterations would blur exactly the contrast under test.
    """
    prov = {}
    pp = EX.RESULTS / "panel_resolved.json"
    if pp.exists():
        for rec in EX.load_json(pp)["panel"]:
            prov[rec["key"]] = {"h4_status": rec.get("h4_status"),
                                "gated": rec.get("gated"),
                                "architecture": rec.get("architecture"),
                                "revision": rec.get("revision")}
    out = []
    for p in sorted(EX.RESULTS.glob("detect_*.json")):
        d = EX.load_json(p)
        key = d["checkpoint"]
        d.update(prov.get(key, {}))
        d["arm"] = _arm_of(d)
        ip = EX.RESULTS / f"induce_{key}.json"
        out.append({"detect": d, "induce": EX.load_json(ip) if ip.exists() else None})
    return out


def _arm_of(d: dict) -> str:
    """Three arms, because 'abliterated-class' is not one homogeneous thing."""
    cls, h4 = d.get("member_class"), d.get("h4_status")
    if cls == "abliterated":
        return "weight_edited_abliteration"
    if cls == "behavioral_uncensored":
        return ("behavioural_uncensored_candidate" if h4 == "candidate"
                else "behavioural_uncensored_unverified")
    return "aligned_reference"


def h1_abliterated_arm(members: list[dict]) -> dict:
    """K of M: at chance as a READER while still INDUCING refusal."""
    rows = []
    for m in members:
        d, i = m["detect"], m["induce"]
        a = d["detection"]["axes"].get("A_canned", {})
        anc = d.get("detection_norm_controlled", {}).get("axes", {}).get("A_canned", {})
        ia = (i or {}).get("axes", {}).get("A_canned", {})
        rows.append({
            "checkpoint": d["checkpoint"], "repo": d["repo"],
            "member_class": d["member_class"], "lineage_id": d["lineage_id"],
            "arm": d.get("arm"), "h4_status": d.get("h4_status"),
            "params_b": d["params_b"], "role": d["role"],
            "L": d["L"], "n_layers": d["n_layers"], "NORM_L": d["NORM_L"],
            "axis_raw_norms": d["axis_raw_norms"],
            "powered": d["powered"],
            "n_refusal": d["detection"]["n_refusal"],
            "n_refusal_of_scanned": d["n_refusal_pre_balance"],
            "n_scanned": d["exclusion_cascade"]["scanned"],
            "spontaneous_refusal_rate":
                d["n_refusal_pre_balance"] / max(d["exclusion_cascade"]["scanned"], 1),
            "n_compliance": d["detection"]["n_compliance"],
            "A_auroc": a.get("auroc"), "A_ci95": a.get("auroc_ci95"),
            "A_verdict": a.get("verdict"),
            "A_auroc_within_stratum": a.get("auroc_within_stratum"),
            "A_auroc_norm_controlled": anc.get("auroc"),
            "A_ci95_norm_controlled": anc.get("auroc_ci95"),
            "A_verdict_norm_controlled": anc.get("verdict"),
            "residual_norm_baseline": d["detection"].get("residual_norm_baseline"),
            "class_stratum_separation": d["detection"].get("class_stratum_separation"),
            "stratum_composition": d["detection"].get("stratum_composition"),
            "B_auroc": d["detection"]["axes"].get("B_paraphrase", {}).get("auroc"),
            "B_ci95": d["detection"]["axes"].get("B_paraphrase", {}).get("auroc_ci95"),
            "B_verdict": d["detection"]["axes"].get("B_paraphrase", {}).get("verdict"),
            "paired_A_minus_B": d["detection"].get("paired_A_minus_B"),
            "A_c50": ia.get("c_50"), "A_alpha50": ia.get("alpha_50"),
            "A_max_rate": ia.get("max_rate"),
            "A_induction_works": ia.get("induction_works"),
            "B_c50": (i or {}).get("axes", {}).get("B_paraphrase", {}).get("c_50"),
            "B_max_rate": (i or {}).get("axes", {}).get("B_paraphrase", {}).get("max_rate"),
            "matched_contrast": (i or {}).get("matched_contrast"),
        })

    abl = [r for r in rows if r["member_class"] in ABL_CLASSES]
    # Per-arm breakdown: how many refusals each arm spontaneously emits is the
    # quantity that decides whether the detection role is measurable at all.
    by_arm: dict[str, dict] = {}
    for r in rows:
        a = by_arm.setdefault(r["arm"], {
            "n_members": 0, "n_powered": 0, "members": [],
            "verdicts": {}, "spontaneous_refusal_rates": []})
        a["n_members"] += 1
        a["n_powered"] += int(bool(r["powered"]))
        a["members"].append(r["checkpoint"])
        a["verdicts"][r["A_verdict"]] = a["verdicts"].get(r["A_verdict"], 0) + 1
        if r.get("spontaneous_refusal_rate") is not None:
            a["spontaneous_refusal_rates"].append(r["spontaneous_refusal_rate"])
    for a in by_arm.values():
        v = a.pop("spontaneous_refusal_rates")
        a["median_spontaneous_refusal_rate"] = float(np.median(v)) if v else None
    powered_abl = [r for r in abl if r["powered"]]
    hits = [r for r in powered_abl
            if r["A_verdict"] == "AT_CHANCE" and r["A_induction_works"]]
    hits_nc = [r for r in powered_abl
               if r["A_verdict_norm_controlled"] == "AT_CHANCE" and r["A_induction_works"]]
    K, M = len(hits), len(powered_abl)
    K_nc = len(hits_nc)
    if K >= 6:
        wording = (f"the canonical refusal axis is at chance as a READER while still "
                   f"inducing refusal on {K} of {M} abliterated checkpoints")
        tier = "K>=6"
    elif K >= 3:
        wording = (f"the canonical refusal axis is at chance as a READER while still "
                   f"inducing refusal on {K} of {M} abliterated checkpoints, reported "
                   f"as a case series")
        tier = "3<=K<6"
    else:
        vd: dict[str, int] = {}
        for r in powered_abl:
            vd[r["A_verdict"]] = vd.get(r["A_verdict"], 0) + 1
        n_unpowered = len(abl) - M
        wording = (
            f"the abliterated arm could NOT be strengthened, and the reason is "
            f"structural rather than statistical: of {len(abl)} abliterated-class "
            f"checkpoints measured, {n_unpowered} never produced the "
            f"{EX.MIN_PER_CLASS} spontaneous refusals the detection role needs even "
            f"after the full escalation ladder, so their reading AUROC is UNDEFINED "
            f"rather than at chance; on the {M} that were powered the canonical axis "
            f"reads "
            + ", ".join(f"{v} {k}" for k, v in sorted(vd.items()))
            + f", giving K = {K}. The iteration-3 n=2 'at chance in both roles' claim "
              f"must therefore be DOWNGRADED: measured on each model's OWN spontaneous "
              f"text, abliteration removes the refusals to be read rather than making "
              f"the axis unable to read them")
        tier = "K<3"

    # paired abliterated-minus-parent AUROC difference, within lineage
    by_lin: dict[str, dict] = {}
    for r in rows:
        by_lin.setdefault(r["lineage_id"], {}).setdefault(r["member_class"], []).append(r)
    paired = []
    for lin, byc in by_lin.items():
        kids = [r for c in ABL_CLASSES for r in byc.get(c, [])]
        refs = byc.get("instruct", []) or byc.get("base", [])
        if not kids or not refs:
            continue
        ref = refs[0]
        for k in kids:
            if k["A_auroc"] is None or ref["A_auroc"] is None:
                continue
            paired.append({"lineage_id": lin, "abliterated": k["checkpoint"],
                           "parent": ref["checkpoint"],
                           "parent_class": ref["member_class"],
                           "A_auroc_abl": k["A_auroc"], "A_auroc_parent": ref["A_auroc"],
                           "delta": k["A_auroc"] - ref["A_auroc"],
                           "abl_verdict": k["A_verdict"],
                           "parent_verdict": ref["A_verdict"]})
    deltas = [p["delta"] for p in paired]
    return {"K": K, "M": M, "wording_tier": tier, "headline": wording,
            "K_norm_controlled": K_nc,
            "hits_norm_controlled": [r["checkpoint"] for r in hits_nc],
            "readout_note": "K is counted under the pre-registered stratum-centred "
                            "projection readout; K_norm_controlled repeats the count "
                            "under the AMENDMENT-1 cosine readout, which removes the "
                            "residual-norm magnitude channel.",
            "hits": [r["checkpoint"] for r in hits],
            "by_arm": by_arm,
            "n_abliterated_class_measured": len(abl),
            "n_abliterated_class_unpowered": len(abl) - M,
            "per_member": rows,
            "abliterated_minus_parent": {
                "pairs": paired, "n": len(paired),
                "mean_delta": float(np.mean(deltas)) if deltas else None,
                "median_delta": float(np.median(deltas)) if deltas else None}}


def h1b_induction_paired(members: list[dict]) -> dict:
    """The abliterated arm that IS measurable: induction, paired within lineage.

    The detection role needs refusals to read, and an abliterated checkpoint
    barely produces any -- so its detection AUROC is structurally undefined
    rather than 'at chance'.  Induction has no such requirement: the axis is
    injected and the refusal rate is read off benign prompts either way.  This
    is therefore the arm on which the abliterated panel can actually speak, and
    it is reported for every abliterated-class member whether or not detection
    was powered.
    """
    by_lin: dict[str, dict] = {}
    rows = []
    for m in members:
        d, i = m["detect"], m["induce"]
        ia = (i or {}).get("axes", {}).get("A_canned", {})
        rec = {"checkpoint": d["checkpoint"], "repo": d["repo"],
               "member_class": d["member_class"], "lineage_id": d["lineage_id"],
               "params_b": d["params_b"],
               "n_refusal_of_scanned": d["n_refusal_pre_balance"],
               "n_scanned": d["exclusion_cascade"]["scanned"],
               "spontaneous_refusal_rate":
                   d["n_refusal_pre_balance"] / max(d["exclusion_cascade"]["scanned"], 1),
               "detection_powered": d["powered"],
               "A_c50": ia.get("c_50"), "A_max_rate": ia.get("max_rate"),
               "A_induction_works": ia.get("induction_works")}
        rows.append(rec)
        by_lin.setdefault(d["lineage_id"], {}).setdefault(d["member_class"], []).append(rec)

    pairs = []
    for lin, byc in by_lin.items():
        refs = byc.get("instruct") or byc.get("base")
        if not refs:
            continue
        ref = refs[0]
        for cls in ABL_CLASSES:
            for k in byc.get(cls, []):
                if k["A_max_rate"] is None or ref["A_max_rate"] is None:
                    continue
                pairs.append({
                    "lineage_id": lin, "abliterated": k["checkpoint"],
                    "member_class": cls, "parent": ref["checkpoint"],
                    "parent_class": ref["member_class"],
                    "max_rate_abl": k["A_max_rate"],
                    "max_rate_parent": ref["A_max_rate"],
                    "delta_max_rate": k["A_max_rate"] - ref["A_max_rate"],
                    "c50_abl": k["A_c50"], "c50_parent": ref["A_c50"],
                    "induces_abl": k["A_induction_works"],
                    "induces_parent": ref["A_induction_works"],
                    "spontaneous_refusal_abl": k["spontaneous_refusal_rate"],
                    "spontaneous_refusal_parent": ref["spontaneous_refusal_rate"]})

    d_mr = [p["delta_max_rate"] for p in pairs]
    lost = [p for p in pairs if p["induces_parent"] and not p["induces_abl"]]
    kept = [p for p in pairs if p["induces_parent"] and p["induces_abl"]]
    if pairs:
        stmt = (f"across {len(pairs)} within-lineage abliterated-versus-parent pairs, "
                f"steering along the canonical refusal axis induces refusal on "
                f"{len(kept)} abliterated checkpoints and FAILS to on {len(lost)} where "
                f"the parent was steerable; the median change in maximum induced "
                f"refusal rate is {float(np.median(d_mr)):+.3f}")
    else:
        stmt = "no within-lineage abliterated-versus-parent pair was measured"
    return {"per_member": rows, "pairs": pairs, "n_pairs": len(pairs),
            "n_induction_lost": len(lost), "n_induction_kept": len(kept),
            "median_delta_max_rate": float(np.median(d_mr)) if d_mr else None,
            "mean_delta_max_rate": float(np.mean(d_mr)) if d_mr else None,
            "statement": stmt,
            "why_this_arm": "detection needs refusals to read and an abliterated "
                            "checkpoint barely emits any, so its detection AUROC is "
                            "structurally undefined rather than at chance; induction "
                            "is measurable on every member regardless"}


def h2_depth_vs_breadth(members: list[dict]) -> dict:
    """Scope repair: the two archived B-reaches-0.50 members at matched contrast."""
    depth_keys = set(EX.ARCHIVED_KEY_BY_REPO)
    rows = []
    for m in members:
        d, i = m["detect"], m["induce"]
        panel_side = "depth" if d["repo"] in depth_keys else "breadth"
        mc = (i or {}).get("matched_contrast") or {}
        ia = (i or {}).get("axes", {})
        rows.append({
            "checkpoint": d["checkpoint"], "repo": d["repo"], "panel": panel_side,
            "member_class": d["member_class"],
            "breadth_b_reaches_half_in_archive": d.get("breadth_b_reaches_half", False),
            "archived_B_max_rate": EX.BREADTH_B_REACHES_HALF.get(
                d["repo"], {}).get("archived_B_max_rate"),
            "B_max_rate_here": ia.get("B_paraphrase", {}).get("max_rate"),
            "B_c50_here": ia.get("B_paraphrase", {}).get("c_50"),
            "A_max_rate_here": ia.get("A_canned", {}).get("max_rate"),
            "A_c50_here": ia.get("A_canned", {}).get("c_50"),
            "matched_contrast_verdict": mc.get("verdict"),
            "matched_contrast_delta": mc.get("mean_delta"),
            "matched_contrast_ci95": mc.get("ci95"),
            "B_reaches_half_at_matched_contrast": mc.get(
                "B_reaches_half_at_matched_contrast"),
        })
    targets = [r for r in rows if r["breadth_b_reaches_half_in_archive"]]
    genuine = [r for r in targets
               if r["matched_contrast_verdict"] == "B_IS_A_GENUINE_INDUCER"]
    artifact = [r for r in targets
                if r["matched_contrast_verdict"] == "NORM_MISMATCH_DOES_NOT_EXPLAIN"]
    if targets and len(artifact) == len(targets):
        statement = ("at MATCHED axis-contrast units the paraphrase axis B remains "
                     "strictly weaker than A on both breadth-panel counterexamples: "
                     "they are norm artifacts, not genuine counterexamples")
    elif genuine:
        statement = (f"{len(genuine)} of {len(targets)} breadth-panel counterexamples "
                     f"survive matched-contrast normalisation: axis B is a GENUINE "
                     f"inducer there, and the induction claim must be scoped to the "
                     f"depth panel")
    else:
        statement = ("the breadth-panel counterexamples are INCONCLUSIVE at matched "
                     "contrast (no shared uncapped fluent contrast level, or a delta "
                     "CI spanning zero without B reaching 0.50)")
    verdicts = [r["matched_contrast_verdict"] for r in rows
                if r["matched_contrast_verdict"]]
    return {"per_member": rows, "targets": targets, "statement": statement,
            "n_targets": len(targets), "n_genuine_inducer": len(genuine),
            "n_norm_artifact": len(artifact),
            "verdict_counts": {v: verdicts.count(v) for v in set(verdicts)}}


def h3_joint_scatter(members: list[dict]) -> dict:
    """One point per (member, axis): does reading predict pushing?"""
    pts = []
    for m in members:
        d, i = m["detect"], m["induce"]
        if not d["powered"] or i is None:
            continue
        ncx = d.get("detection_norm_controlled", {}).get("axes", {})
        for ax, arec in d["detection"]["axes"].items():
            irec = i["axes"].get(ax)
            if irec is None or irec.get("max_rate") is None:
                continue
            pts.append({
                "detection_auroc_norm_controlled": ncx.get(ax, {}).get("auroc"),
                "checkpoint": d["checkpoint"], "axis": ax,
                "lineage_id": d["lineage_id"], "member_class": d["member_class"],
                "level": d["member_class"], "params_b": d["params_b"],
                "detection_auroc": arec["auroc"],
                "detection_ci95": arec["auroc_ci95"],
                "detection_verdict": arec["verdict"],
                "max_refusal_rate": irec["max_rate"],
                "c_50": irec["c_50"],
                "neg_log10_c50": (-np.log10(irec["c_50"])
                                  if irec["c_50"] and irec["c_50"] > 0 else None),
            })
    if len(pts) < 4:
        return {"n_pairs": len(pts), "insufficient": True, "points": pts}

    y = np.array([p["detection_auroc"] for p in pts], float)
    x = np.array([p["max_refusal_rate"] for p in pts], float)
    lin = np.array([p["lineage_id"] for p in pts])
    rho = EX.spearman(x, y)

    boots = []
    for idx in EX.cluster_boot_indices(lin, EX.N_BOOT, EX.BOOT_SEED):
        boots.append(EX.spearman(x[idx], y[idx]))
    lo, hi = EX.boot_ci(boots)

    unc = [p for p in pts if p["neg_log10_c50"] is not None]
    rho_sec = (EX.spearman([p["neg_log10_c50"] for p in unc],
                           [p["detection_auroc"] for p in unc])
               if len(unc) >= 4 else float("nan"))

    within = []
    for ck in sorted({p["checkpoint"] for p in pts}):
        sub = [p for p in pts if p["checkpoint"] == ck]
        if len(sub) >= 4:
            within.append({"checkpoint": ck,
                           "rho": EX.spearman([p["max_refusal_rate"] for p in sub],
                                              [p["detection_auroc"] for p in sub]),
                           "n_axes": len(sub)})
    wr = [w["rho"] for w in within if np.isfinite(w["rho"])]

    n, nl = len(pts), int(len(np.unique(lin)))
    null = bool(np.isfinite(lo) and np.isfinite(hi) and lo <= 0 <= hi)
    if null:
        sentence = (f"induction quality and detection quality on the same axis are "
                    f"UNCORRELATED across {n} (member, axis) pairs over {nl} lineages "
                    f"(Spearman rho = {rho:.3f}, lineage-bootstrap 95% CI "
                    f"[{lo:.3f}, {hi:.3f}], which contains zero)")
    else:
        sentence = (f"across {n} (member, axis) pairs over {nl} lineages, induction "
                    f"quality and detection quality are correlated at rho = {rho:.3f} "
                    f"[{lo:.3f}, {hi:.3f}]")
    return {"n_pairs": n, "n_lineages": nl, "n_members": len({p["checkpoint"] for p in pts}),
            "rho_primary": rho, "ci95_lineage_bootstrap": [lo, hi],
            "is_null": null, "pre_committed_sentence": sentence,
            "x_primary": "max_refusal_rate", "y": "detection_auroc",
            "rho_secondary_neg_log10_c50": rho_sec,
            "n_uncensored_c50": len(unc),
            "censored_fraction": float(1 - len(unc) / n),
            "within_member": within,
            "within_member_mean_rho": float(np.mean(wr)) if wr else None,
            "points": pts}


def sanity_panel(members: list[dict]) -> dict:
    """P8: C and D must stay at chance in BOTH roles everywhere."""
    rows, viol = [], []
    for m in members:
        d, i = m["detect"], m["induce"]
        for ax in ("C_stylistic", "D_random0"):
            det = d["detection"]["axes"].get(ax, {})
            dnc = d.get("detection_norm_controlled", {}).get("axes", {}).get(ax, {})
            ind = (i or {}).get("axes", {}).get(ax, {})
            lo, hi = det.get("auroc_ci95", [np.nan, np.nan])
            # AMENDMENT-1: the gate is applied to the NORM-CONTROLLED readout, because
            # a raw projection inherits the residual-norm channel and would fail on a
            # random axis for a reason that has nothing to do with direction.
            nlo, nhi = dnc.get("auroc_ci95", [np.nan, np.nan])
            reads_raw = bool(np.isfinite(lo) and lo > 0.5) or bool(
                np.isfinite(hi) and hi < 0.5)
            # AMENDMENT-2: judged against the EMPIRICAL random null rather than a
            # bare 0.50. A residual stream is anisotropic, so a single random
            # direction is not expected to sit at 0.50; the question is whether the
            # axis sits outside the spread of 20 random draws through the identical
            # pipeline.
            rn = (d["detection"].get("random_null") or {}).get("norm_controlled") or {}
            band = rn.get("max_abs_deviation_from_half")
            nc_auroc = dnc.get("auroc")
            if band is not None and nc_auroc is not None and np.isfinite(nc_auroc):
                reads = bool(abs(nc_auroc - 0.5) > band)
            else:
                reads = bool(np.isfinite(nlo) and nlo > 0.5) or bool(
                    np.isfinite(nhi) and nhi < 0.5)
            induces = bool((ind.get("max_rate") or 0.0) >= 0.10)
            r = {"checkpoint": d["checkpoint"], "axis": ax,
                 "auroc": det.get("auroc"), "ci95": det.get("auroc_ci95"),
                 "auroc_norm_controlled": dnc.get("auroc"),
                 "ci95_norm_controlled": dnc.get("auroc_ci95"),
                 "verdict": det.get("verdict"), "max_refusal_rate": ind.get("max_rate"),
                 "ci_excludes_half_raw_projection": reads_raw,
                 "random_null_max_abs_dev": band,
                 "random_null_projection": (d["detection"].get("random_null") or {}
                                            ).get("projection"),
                 "ci_excludes_half": reads, "induces_ge_0p10": induces}
            rows.append(r)
            if ax == "D_random0" and (reads or induces) and d["powered"]:
                viol.append(r)
    d_rows = [r for r in rows if r["axis"] == "D_random0"]
    reads_v = [r for r in d_rows if r["ci_excludes_half"]]
    induces_v = [r for r in d_rows if r["induces_ge_0p10"]]
    bands = [r["random_null_max_abs_dev"] for r in d_rows
             if r.get("random_null_max_abs_dev") is not None]
    ind_rates = [r["max_refusal_rate"] for r in d_rows
                 if r.get("max_refusal_rate") is not None]
    substantive = (
        f"a random direction injected at axis A's OWN matched magnitude induces "
        f"refusal at a rate of at least 0.10 on {len(induces_v)} of {len(d_rows)} "
        f"members (max over the contrast grid; median across the panel "
        f"{float(np.median(ind_rates)):.3f}, worst {max(ind_rates):.3f}). This is a "
        f"FLOOR that any steering claim has to clear, and it is measured here rather "
        f"than assumed: the same magnitude that makes the canonical axis work also "
        f"makes an arbitrary direction work on a substantial minority of models."
    ) if ind_rates else "no induction measured"
    null_note = (
        f"the empirical random-direction AUROC band spans +/-{min(bands):.3f} to "
        f"+/-{max(bands):.3f} across members, so the textbook expectation that a "
        f"random direction reads at 0.500 is wrong by a wide and model-dependent "
        f"margin"
    ) if bands else "no random null measured"
    return {"rows": rows, "n_D_violations": len(viol), "D_violations": viol,
            "n_D_reads_violations": len(reads_v),
            "n_D_induces_violations": len(induces_v),
            "n_D_members": len(d_rows),
            "random_axis_induction_floor": substantive,
            "random_null_band_note": null_note,
            "median_random_axis_max_rate":
                float(np.median(ind_rates)) if ind_rates else None,
            "max_random_axis_max_rate": float(max(ind_rates)) if ind_rates else None,
            "passed": len(viol) == 0,
            "note": "a matched random axis that reads or induces means the pipeline "
                    "is leaking; D violations are flagged, not silently kept"}


def holm_across_members(members: list[dict]) -> dict:
    pv = {}
    for m in members:
        pa = m["detect"]["detection"].get("paired_A_minus_B")
        if pa and np.isfinite(pa.get("p_boot", np.nan)):
            pv[m["detect"]["checkpoint"]] = pa["p_boot"]
    adj = EX.holm(pv)
    return {"raw_p": pv, "holm_adjusted_p": adj,
            "n_significant_holm_0p05": sum(1 for v in adj.values()
                                           if np.isfinite(v) and v < 0.05)}


def axis_reproduction_summary(members: list[dict]) -> dict:
    rows = []
    for m in members:
        rep = m["detect"].get("axis_reproduction", {})
        if not rep.get("applicable"):
            continue
        rows.append({"checkpoint": m["detect"]["checkpoint"],
                     "archived_key": rep["archived_key"],
                     "min_abs_cosine": rep["min_abs_cosine"],
                     "all_pass_0p999": rep["all_pass_0p999"],
                     "per_axis": {k: v["cosine"] for k, v in rep["cosines"].items()}})
    worst = [r["min_abs_cosine"] for r in rows if r["min_abs_cosine"] is not None]
    return {"rows": rows, "n_checkpoints": len(rows),
            "worst_min_abs_cosine": float(min(worst)) if worst else None,
            "any_stop_and_diagnose": bool(worst and min(worst) < 0.95)}


def _s(x) -> str:
    """Schema-safe string for a predict_* field (they must be strings)."""
    if x is None:
        return "undefined"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, float) and not np.isfinite(x):
        return "undefined"
    if isinstance(x, float):
        return f"{x:.6f}"
    return str(x)


def build_datasets(members, h1, h2, h3, sp) -> list[dict]:
    """The row-level deliverable, in exp_gen_sol_out schema form.

    One row per (member, axis) for the two roles, one row per member for the
    matched-contrast contrast, and one row per joint-scatter point.  `output` is
    the pre-registered verdict; the numbers ride along as metadata_*.
    """
    det_rows, ind_rows, joint_rows = [], [], []
    for m in members:
        d, i = m["detect"], m["induce"]
        key = d["checkpoint"]
        for ax, arec in sorted(d["detection"]["axes"].items()):
            irec = (i or {}).get("axes", {}).get(ax, {})
            det_rows.append({
                "input": f"DETECTION | member={key} | repo={d['repo']} | axis={ax}",
                "output": arec.get("verdict", "UNDEFINED"),
                "metadata_fold": "detection_per_member_axis",
                "metadata_member": key, "metadata_axis": ax,
                "metadata_repo": d["repo"],
                "metadata_member_class": d["member_class"],
                "metadata_lineage_id": d["lineage_id"],
                "metadata_params_b": d["params_b"],
                "metadata_layer": d["L"], "metadata_n_layers": d["n_layers"],
                "metadata_norm_l": d["NORM_L"],
                "metadata_powered": d["powered"],
                "metadata_n_refusal": d["detection"]["n_refusal"],
                "metadata_n_compliance": d["detection"]["n_compliance"],
                "metadata_n_prompts": d["detection"]["n_prompts"],
                "metadata_auroc": arec.get("auroc"),
                "metadata_auroc_ci95": arec.get("auroc_ci95"),
                "metadata_auroc_within_stratum": arec.get("auroc_within_stratum"),
                "metadata_auroc_raw_uncentred": arec.get("auroc_raw_uncentred"),
                "metadata_cohens_d": arec.get("cohens_d"),
                "metadata_axis_raw_norm": d["axis_raw_norms"].get(ax),
                "predict_verdict": _s(arec.get("verdict")),
                "predict_auroc": _s(arec.get("auroc")),
            })
            if irec:
                ind_rows.append({
                    "input": f"INDUCTION | member={key} | repo={d['repo']} | axis={ax}",
                    "output": ("INDUCES" if irec.get("induction_works")
                               else "NEVER_CROSSES_0.50"),
                    "metadata_fold": "induction_per_member_axis",
                    "metadata_member": key, "metadata_axis": ax,
                    "metadata_member_class": d["member_class"],
                    "metadata_lineage_id": d["lineage_id"],
                    "metadata_raw_norm": irec.get("raw_norm"),
                    "metadata_norm_l": irec.get("NORM_L"),
                    "metadata_c_50": irec.get("c_50"),
                    "metadata_alpha_50": irec.get("alpha_50"),
                    "metadata_max_rate": irec.get("max_rate"),
                    "metadata_c_at_max_rate": irec.get("c_at_max_rate"),
                    "metadata_inverted_u": irec.get("inverted_U"),
                    "metadata_fluency_collapse_c": irec.get("fluency_collapse_c"),
                    "metadata_n_capped": irec.get("n_capped"),
                    "metadata_rates_by_c": {
                        c: irec["grid"][c].get("rate") for c in irec.get("grid", {})},
                    "predict_c_50": _s(irec.get("c_50")),
                    "predict_max_rate": _s(irec.get("max_rate")),
                })
        if i and i.get("matched_contrast"):
            mc = i["matched_contrast"]
            ind_rows.append({
                "input": f"MATCHED_CONTRAST | member={key} | A_canned vs B_paraphrase",
                "output": mc.get("verdict", "INCONCLUSIVE"),
                "metadata_fold": "matched_contrast_per_member",
                "metadata_member": key,
                "metadata_member_class": d["member_class"],
                "metadata_lineage_id": d["lineage_id"],
                "metadata_mean_delta": mc.get("mean_delta"),
                "metadata_ci95": mc.get("ci95"),
                "metadata_p_boot": mc.get("p_boot"),
                "metadata_n_shared_c": mc.get("n_shared_c"),
                "metadata_c_where_a_reaches_half": mc.get("c_where_A_first_reaches_half"),
                "metadata_delta_at_that_c": mc.get("delta_at_that_c"),
                "metadata_b_reaches_half_matched": mc.get(
                    "B_reaches_half_at_matched_contrast"),
                "predict_verdict": _s(mc.get("verdict")),
                "predict_mean_delta": _s(mc.get("mean_delta")),
            })

    for p in h3.get("points", []):
        joint_rows.append({
            "input": f"JOINT | member={p['checkpoint']} | axis={p['axis']}",
            "output": p["detection_verdict"],
            "metadata_fold": "joint_read_vs_act",
            "metadata_member": p["checkpoint"], "metadata_axis": p["axis"],
            "metadata_lineage_id": p["lineage_id"],
            "metadata_level": p["level"], "metadata_params_b": p["params_b"],
            "metadata_detection_auroc": p["detection_auroc"],
            "metadata_detection_ci95": p["detection_ci95"],
            "metadata_max_refusal_rate": p["max_refusal_rate"],
            "metadata_c_50": p["c_50"],
            "metadata_neg_log10_c50": p["neg_log10_c50"],
            "predict_detection_auroc": _s(p["detection_auroc"]),
            "predict_max_refusal_rate": _s(p["max_refusal_rate"]),
        })

    ds = []
    if det_rows:
        ds.append({"dataset": "detection_role", "examples": det_rows})
    if ind_rows:
        ds.append({"dataset": "induction_role", "examples": ind_rows})
    if joint_rows:
        ds.append({"dataset": "joint_read_vs_act", "examples": joint_rows})
    if not ds:
        ds = [{"dataset": "empty", "examples": [
            {"input": "no member completed", "output": "NO_DATA",
             "metadata_fold": "empty"}]}]
    return ds


def stage_analysis() -> dict:
    members = _load_members()
    logger.info(f"analysing {len(members)} measured members")
    if not members:
        raise RuntimeError("no detect_*.json found -- run --stage gpu first")

    h1 = h1_abliterated_arm(members)
    h1b = h1b_induction_paired(members)
    h2 = h2_depth_vs_breadth(members)
    h3 = h3_joint_scatter(members)
    sp = sanity_panel(members)
    hp = holm_across_members(members)
    ar = axis_reproduction_summary(members)

    logger.info(f"H1: {h1['headline']}")
    logger.info(f"H1b: {h1b['statement']}")
    logger.info(f"H2: {h2['statement']}")
    logger.info(f"H3: {h3.get('pre_committed_sentence')}")
    logger.info(f"sanity: D violations = {sp['n_D_violations']}")

    panel = EX.load_json(EX.RESULTS / "panel_resolved.json")
    inv = EX.load_json(EX.RESULTS / "archive_inventory.json")
    tests = EX.load_json(EX.RESULTS / "tests.json")
    gpu_log = (EX.load_json(EX.RESULTS / "gpu_log.json")
               if (EX.RESULTS / "gpu_log.json").exists() else {})
    judge = (EX.load_json(EX.RESULTS / "judge.json")
             if (EX.RESULTS / "judge.json").exists() else
             {"kappa": None, "status": "NOT MEASURED"})

    prereg_txt = (EX.RESULTS / "prereg.json").read_text()
    results_block = {
            "K": h1["K"], "M": h1["M"], "headline": h1["headline"],
            "wording_tier": h1["wording_tier"],
            "h1_abliterated_arm": h1,
            "h1b_induction_paired": h1b,
            "h2_depth_vs_breadth": h2,
            "h3_joint_scatter": {k: v for k, v in h3.items() if k != "points"},
            "joint_scatter_points": h3.get("points", []),
            "sanity_panel": sp,
            "paired_A_minus_B_holm": hp,
    }
    out = {
        "datasets": build_datasets(members, h1, h2, h3, sp),
        "metadata": {
            "results": results_block,
            "prereg_sha256": EX.sha256_text(prereg_txt),
            "layer_rule": {"relative_depth": EX.LAYER_DEPTH,
                           "formula": "L = round(0.25 * n_layers), clip [1, n_layers-1]",
                           "plan_said": 0.30,
                           "correction": "the archive used 0.25 on all six checkpoints"},
            "contrast_unit_formula": "c = alpha * NORM_L / ||d_raw||",
            "contrast_unit_verification": tests.get("T2_contrast_unit_formula"),
            "analysis_replay_gate": tests.get("T1_replay_archived_analysis"),
            "tokenisation_unit_test": tests.get("T3_tokenisation_unit_test"),
            "archive_inventory": inv.get("summary", inv),
            "panel_resolved": {"n_queued": len(panel["panel"]),
                               "n_abliterated_class_queued":
                                   panel["n_abliterated_class_queued"],
                               "n_parents_queued": panel["n_parents_queued"],
                               "n_skipped_candidates": len(panel["skipped_candidates"]),
                               "skipped": panel["skipped_candidates"]},
            "gpu_log": gpu_log,
            "axis_reproduction": ar,
            "exclusion_cascade_counts": {
                m["detect"]["checkpoint"]: m["detect"]["exclusion_cascade"]
                for m in members},
            "balance": {m["detect"]["checkpoint"]: m["detect"]["balance"]
                        for m in members},
            "escalation": {m["detect"]["checkpoint"]: m["detect"]["escalation_ladder"]
                           for m in members},
            "boundary_merge_avoided": {
                m["detect"]["checkpoint"]:
                    m["detect"]["encode"]["n_boundary_merge_avoided_by_id_concat"]
                for m in members},
            "judge_kappa": judge.get("kappa"),
            "judge_status": judge.get("status", "measured"),
            "openrouter_cost_usd": judge.get("cost_usd", 0.0),
            "gpu_seconds_per_member": {e["key"]: e.get("seconds")
                                       for e in gpu_log.get("log", [])
                                       if e.get("seconds")},
            "dtype": "bfloat16",
            "hardware": "1x NVIDIA RTX A4500 20GB",
            "verdicts": {
                "H1": h1["wording_tier"],
                "H1b": (f"{h1b['n_induction_lost']} of {h1b['n_pairs']} pairs lose "
                        f"induction after abliteration"),
                "H2": h2["statement"][:120],
                "H3": "NULL" if h3.get("is_null") else "CORRELATED",
                "sanity_D": "PASS" if sp["passed"] else "FAIL",
            },
        },
    }
    EX.atomic_write_json(EX.HERE / "method_out.json", out)
    logger.info("wrote method_out.json")
    return out


# ==========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all",
                    choices=["all", "prereg", "panel", "gpu", "analysis"])
    ap.add_argument("--budget-min", type=float, default=200.0)
    ap.add_argument("--only", default="")
    ap.add_argument("--max-members", type=int, default=0)
    ap.add_argument("--refresh-detection", action="store_true",
                    help="re-run axes+detection only, keeping existing induction")
    args = ap.parse_args()

    EX.RESULTS.mkdir(parents=True, exist_ok=True)
    only = [x for x in args.only.split(",") if x] or None

    if args.stage in ("all", "prereg"):
        subprocess.run([sys.executable, str(EX.HERE / "prereg.py")], check=True)
        logger.info("prereg sha256 = " +
                    EX.sha256_text((EX.RESULTS / "prereg.json").read_text()))
    if args.stage in ("all", "panel"):
        stage_panel()
    if args.stage in ("all", "gpu"):
        stage_gpu(args.budget_min, only, args.max_members or None,
                  refresh_detection=args.refresh_detection)
    if args.stage in ("all", "analysis"):
        stage_analysis()


if __name__ == "__main__":
    main()
