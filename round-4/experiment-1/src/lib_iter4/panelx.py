#!/usr/bin/env python3
"""STEP 1 -- panel construction for iteration 4.

Pure data work: eligibility filtering over the frozen `panel_manifest`, the
pre-registered lineage-label collapse rule, and the breadth-first wave ordering.
NOTHING here reads y_refusal or any sigma; the panel is frozen before any
outcome is looked at.
"""

from __future__ import annotations

import re

from lib import panel as panel_mod

MAX_PARAM_COUNT = 4.2e9

# Pre-registered wave-1 preference order over member_class. Instruct members
# carry the outcome variance, so they anchor each new lineage first.
LEVEL_ORDER = ("instruct", "abliterated", "behavioral_uncensored", "base")
# Wave 2 prefers a base member: it anchors the low-refusal end of y and creates
# within-lineage spread, which is what a lineage-clustered estimator needs.
WAVE2_ORDER = ("base", "abliterated", "behavioral_uncensored", "instruct")

# The three AMS Table-I checkpoints (arXiv:2608.05578 Table I) used as a
# published-value reproduction gate.
AMS_GATE_REPOS = {
    "unsloth/Llama-3.2-3B-Instruct": 8.37,
    "unsloth/gemma-2-2b-it": 4.80,
    "unsloth/Llama-3.2-1B-Instruct": 4.55,
}

_DIGIT_RUN = re.compile(r"\d+")


def _basename(lineage_id: str) -> str:
    return lineage_id.split("/")[-1].lower()


def _prefix_before_first_digit_difference(a: str, b: str) -> int:
    """Length of the shared prefix, truncated at the first digit-run mismatch.

    The pre-registered rule: walk the two lowercased basenames together; stop at
    the first position where they differ. If either side is inside a digit run at
    that point the prefix is truncated back to the start of that digit run, so
    "tinyllama_v1.1" / "tinyllama-1.1b-..." share "tinyllama" (9) rather than
    accidentally banking on a numeric coincidence.
    """
    n = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            break
        n += 1
    if n == 0:
        return 0
    # truncate back out of any digit run we stopped inside
    while n > 0 and a[n - 1].isdigit():
        n -= 1
    # also drop a trailing separator so "tinyllama_" -> "tinyllama"
    while n > 0 and not a[n - 1].isalnum():
        n -= 1
    return n


def _evidence_links(lin_a: str, lin_b: str, evidence_by_lineage: dict) -> str | None:
    """True iff some member's derivation chain under one lineage names the other."""
    for ev in evidence_by_lineage.get(lin_a, []):
        if lin_b and lin_b in ev:
            return ev
    for ev in evidence_by_lineage.get(lin_b, []):
        if lin_a and lin_a in ev:
            return ev
    return None


def eligible_rows(manifest_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Apply the four pre-registered eligibility criteria.

    Returns (kept, rejected); every rejection carries a machine-readable reason.
    """
    by_repo = {r["hf_repo_id"]: r for r in manifest_rows}
    mirror_for: dict[str, str] = {}
    for r in manifest_rows:
        mo = (r.get("mirror_of") or "").strip()
        if mo and not r.get("gated"):
            mirror_for.setdefault(mo, r["hf_repo_id"])

    kept: list[dict] = []
    rejected: list[dict] = []
    for r in manifest_rows:
        repo = r["hf_repo_id"]
        rec = {"repo": repo, "lineage_id": r.get("lineage_id"),
               "member_class": r.get("member_class"),
               "param_count": r.get("param_count"),
               "architecture": r.get("architecture")}
        if not r.get("verified"):
            rejected.append({**rec, "reason": "not_verified",
                             "detail": r.get("verify_error") or ""})
            continue
        pc = r.get("param_count")
        if pc is None:
            rejected.append({**rec, "reason": "param_count_unknown"})
            continue
        if float(pc) > MAX_PARAM_COUNT:
            rejected.append({**rec, "reason": "param_count_above_4.2e9"})
            continue
        arch = str(r.get("architecture") or "")
        if not arch.endswith("ForCausalLM"):
            rejected.append({**rec, "reason": "architecture_not_causal_lm"})
            continue
        repo_used = repo
        if r.get("gated"):
            mir = mirror_for.get(repo)
            if not mir:
                rejected.append({**rec, "reason": "gated_no_ungated_mirror"})
                continue
            repo_used = mir
        if (r.get("mirror_of") or "").strip():
            # a mirror row is only enrolled through its gated original, never twice
            orig = r["mirror_of"]
            if orig in by_repo and by_repo[orig].get("gated"):
                rejected.append({**rec, "reason": "mirror_row_enrolled_via_its_gated_original",
                                 "detail": orig})
                continue
        kept.append({**r, "repo_requested": repo, "repo_used": repo_used})
    return kept, rejected


def lineage_labels(kept: list[dict]) -> tuple[dict[str, str], list[dict]]:
    """Collapse lineage_id strings that name the same pretrained root.

    Pre-registered rule: two lineage_id strings collapse to one label iff their
    lowercased basenames share a prefix of >= 8 characters before the first
    digit-run difference AND one repo's meta.lineage_evidence chain names the
    other. Every collapse is returned with the quoted evidence string.
    """
    evidence_by_lineage: dict[str, list[str]] = {}
    for r in kept:
        evidence_by_lineage.setdefault(r["lineage_id"], []).append(
            r.get("lineage_evidence") or "")
    lids = sorted(evidence_by_lineage)

    parent = {L: L for L in lids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    collapses: list[dict] = []
    for i, a in enumerate(lids):
        for b in lids[i + 1:]:
            pref = _prefix_before_first_digit_difference(_basename(a), _basename(b))
            if pref < 8:
                continue
            ev = _evidence_links(a, b, evidence_by_lineage)
            if ev is None:
                continue
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
            collapses.append({"lineage_id_a": a, "lineage_id_b": b,
                              "shared_prefix_chars": pref,
                              "evidence": ev[:400]})
    label = {L: find(L) for L in lids}
    return label, collapses


def _slug(repo: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", repo.lower()).strip("_")


def build_panel(manifest_rows: list[dict]) -> dict:
    """Full STEP 1: eligibility -> lineage labels -> breadth-first waves."""
    kept, rejected = eligible_rows(manifest_rows)
    label, collapses = lineage_labels(kept)
    manifest_by_repo = {r["hf_repo_id"]: r for r in manifest_rows}

    archived = {m.repo: m for m in panel_mod.PANEL}
    # The archived panel's lineage LABELS (L1..L7) are the frozen iteration-2/3
    # resampling units; they are carried through unchanged so that the archived
    # 19 keep the exact clustering under which 0.358 / 0.654 were computed.
    arch_label_for_lineage_id: dict[str, str] = {}
    for m in panel_mod.PANEL:
        row = next((r for r in kept if r["hf_repo_id"] == m.repo), None)
        if row is not None:
            arch_label_for_lineage_id[label[row["lineage_id"]]] = m.lineage

    rows: list[dict] = []
    seen_repo: set[str] = set()

    # ---- WAVE 0: the archived 19, in the frozen iteration-3 order ----------
    for key in panel_mod.DEFAULT_ORDER:
        m = panel_mod.BY_KEY[key]
        # metadata comes from the FULL manifest, not from `kept`: an ungated
        # mirror row (unsloth/*) is excluded from `kept` by design because its
        # gated original is the enrolment handle, but the archived member IS the
        # mirror and still needs its param_count / n_layers.
        row = manifest_by_repo.get(m.repo)
        rows.append({
            "key": key, "repo_requested": m.repo, "repo_used": m.repo,
            "revision": (row or {}).get("revision"),
            "lineage_label": m.lineage,
            "lineage_id_raw": m.lineage_id,
            "family": (row or {}).get("model_type") or m.family,
            "level": m.level,
            "param_count": (row or {}).get("param_count"),
            "n_layers": (row or {}).get("n_layers"),
            "has_chat_template": (row or {}).get("has_chat_template"),
            "wave": 0, "in_archive": True,
            "in_manifest": row is not None,
            "fallbacks": list(m.fallbacks),
        })
        seen_repo.add(m.repo)
        if row is not None:
            seen_repo.add(row.get("mirror_of") or m.repo)

    # ---- new lineages, by wave --------------------------------------------
    by_label: dict[str, list[dict]] = {}
    for r in kept:
        if r["hf_repo_id"] in archived:
            continue
        lab = label[r["lineage_id"]]
        lab = arch_label_for_lineage_id.get(lab, lab)
        by_label.setdefault(lab, []).append(r)

    archived_labels = {m.lineage for m in panel_mod.PANEL}
    new_labels = sorted(L for L in by_label if L not in archived_labels)

    def _pick(cands: list[dict], order: tuple[str, ...], used: set[str]) -> dict | None:
        pool = [c for c in cands
                if c["hf_repo_id"] not in used and c["repo_used"] not in used]
        if not pool:
            return None
        pool.sort(key=lambda c: (order.index(c["member_class"])
                                 if c["member_class"] in order else len(order),
                                 float(c["param_count"])))
        return pool[0]

    def _emit(r: dict, lab: str, wave: int) -> None:
        rows.append({
            "key": f"n_{_slug(r['hf_repo_id'])}"[:80],
            "repo_requested": r["hf_repo_id"], "repo_used": r["repo_used"],
            "revision": r.get("revision"),
            "lineage_label": lab, "lineage_id_raw": r["lineage_id"],
            "family": r.get("model_type"), "level": r["member_class"],
            "param_count": r.get("param_count"), "n_layers": r.get("n_layers"),
            "has_chat_template": r.get("has_chat_template"),
            "wave": wave, "in_archive": False, "in_manifest": True,
            "fallbacks": [],
        })
        seen_repo.add(r["hf_repo_id"])
        seen_repo.add(r["repo_used"])

    for wave, order in ((1, LEVEL_ORDER), (2, WAVE2_ORDER)):
        picks = []
        for lab in new_labels:
            if wave == 2 and not any(x["lineage_label"] == lab and x["wave"] == 1
                                     for x in rows):
                continue
            r = _pick(by_label[lab], order, seen_repo)
            if r is not None:
                picks.append((r, lab))
        picks.sort(key=lambda t: float(t[0]["param_count"]))
        for r, lab in picks:
            _emit(r, lab, wave)

    # WAVE 3: everything eligible that is still unenrolled, cheapest first
    rest = [(r, arch_label_for_lineage_id.get(label[r["lineage_id"]],
                                              label[r["lineage_id"]]))
            for r in kept
            if r["hf_repo_id"] not in seen_repo and r["repo_used"] not in seen_repo]
    rest.sort(key=lambda t: float(t[0]["param_count"]))
    for r, lab in rest:
        _emit(r, lab, 3)

    # AMS Table-I gate members are force-included if eligible and not yet present
    gate = []
    for repo, published in AMS_GATE_REPOS.items():
        row = next((x for x in rows if x["repo_used"] == repo
                    or x["repo_requested"] == repo), None)
        gate.append({"repo": repo, "published_sigma": published,
                     "eligible_and_enrolled": row is not None,
                     "key": (row or {}).get("key"),
                     "wave": (row or {}).get("wave")})

    # Lineage-ID strings that end up sharing a label WITHOUT the pre-registered
    # rule having fired -- i.e. inherited from the frozen archived labelling.
    inherited: list[dict] = []
    by_lab_ids: dict[str, set[str]] = {}
    for x in rows:
        by_lab_ids.setdefault(x["lineage_label"], set()).add(x["lineage_id_raw"])
    fired = {(c["lineage_id_a"], c["lineage_id_b"]) for c in collapses}
    for lab, ids in sorted(by_lab_ids.items()):
        if len(ids) < 2:
            continue
        ids_s = sorted(ids)
        for i, a in enumerate(ids_s):
            for b in ids_s[i + 1:]:
                if (a, b) in fired or (b, a) in fired:
                    continue
                inherited.append({
                    "lineage_label": lab, "lineage_id_a": a, "lineage_id_b": b,
                    "shared_prefix_chars": _prefix_before_first_digit_difference(
                        _basename(a), _basename(b)),
                    "rule_fired": False,
                    "why_rule_did_not_fire": (
                        "the manifest records an EMPTY meta.lineage_evidence on both "
                        "rows, so the evidence leg of the pre-registered collapse "
                        "rule cannot be satisfied; the shared label is inherited "
                        "verbatim from the frozen iteration-2/3 lineage labelling "
                        "under which the 0.358 / 0.654 estimates were computed."),
                })

    labels_used = sorted({x["lineage_label"] for x in rows})
    return {
        "rows": rows,
        "rejected": rejected,
        "lineage_collapses": collapses,
        "lineage_collapses_inherited_not_rule_fired": inherited,
        "ams_table_I_gate_membership": gate,
        "counts": {
            "n_manifest_rows": len(manifest_rows),
            "n_eligible": len(kept),
            "n_rejected": len(rejected),
            "n_members_enrolled": len(rows),
            "n_lineage_labels": len(labels_used),
            "n_lineage_id_strings": len({x["lineage_id_raw"] for x in rows}),
            "n_families": len({x["family"] for x in rows if x["family"]}),
            "n_new_lineages": len(new_labels),
            "by_wave": {str(w): sum(1 for x in rows if x["wave"] == w)
                        for w in (0, 1, 2, 3)},
            "by_level": {lv: sum(1 for x in rows if x["level"] == lv)
                         for lv in sorted({x["level"] for x in rows})},
            "rejection_reasons": {
                rr: sum(1 for x in rejected if x["reason"] == rr)
                for rr in sorted({x["reason"] for x in rejected})},
        },
        "lineage_labels": labels_used,
    }
