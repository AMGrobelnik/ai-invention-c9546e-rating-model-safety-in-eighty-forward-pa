#!/usr/bin/env python3
"""STAGE 1 -- THE CLAIM LEDGER, and the three named drifts.

One row per numeric (or verdict-string) claim in the whole draft, resolved to a
JSON pointer into a sha256-stamped source, flagged, and given the sentence to
ship. The flag histogram before and after repair is the headline metric.
"""

from __future__ import annotations

import re

from loguru import logger

import derived as DERIVED
import ledgerlib as LL
from common import (INDEXED_ALIASES, OUT, REGISTRY, VERDICT_STRINGS, jdump,
                    jload, setup_logging, sha256_file)

DERIVED_DOC: dict = {"derivations": {}, "values": {}}

# ==========================================================================
# Surface enumeration over the draft object
# ==========================================================================


def enumerate_surfaces(draft: dict) -> list[dict]:
    """Every text surface of the draft, tagged. Numbers appear in prose, in
    markdown tables, in figure captions AND in figure summaries -- all four are
    audited, plus the abstract."""
    units: list[dict] = []
    units.append({"section": "Abstract", "subsection": None, "surface": "abstract",
                  "text": draft["abstract"]})
    units.append({"section": "Title", "subsection": None, "surface": "prose",
                  "text": draft["title"]})
    for b in LL.split_sections(draft["paper_text"]):
        surface = "table" if LL.is_table_block(b["text"]) else "prose"
        # a bolded "**Table N.**" line directly under a table is its caption
        if surface == "prose" and re.match(r"^\*\*(Table|Figure)\s", b["text"].strip()):
            surface = "caption"
        units.append({**b, "surface": surface})
    for f in draft.get("figures", []):
        fid = f.get("id", "?")
        for key, surf in (("caption", "caption"), ("summary", "figure_summary"),
                          ("title", "caption")):
            txt = f.get(key)
            if txt:
                units.append({"section": "Figures", "subsection": fid,
                              "surface": surf, "text": txt})
    return units


def extract_claims(units: list[dict]) -> list[LL.RawClaim]:
    claims: list[LL.RawClaim] = []
    for u in units:
        if u["surface"] == "table":
            pieces = []
            for line in u["text"].splitlines():
                if not line.strip().startswith("|"):
                    pieces.append(line)
                    continue
                if re.match(r"^\s*\|[\s|:-]+\|\s*$", line):
                    continue
                pieces.append(line)
            sentences = [p.strip() for p in pieces if p.strip()]
        else:
            sentences = LL.split_sentences(u["text"])
        for sent in sentences:
            blocked = LL.allowlisted_spans(sent)
            for m in LL.NUM_RE.finditer(sent):
                s, e = m.span()
                if any(bs <= s and e <= be for bs, be, _ in blocked):
                    continue
                tok = m.group(0)
                val = LL._parse(tok)
                if val is None:
                    continue
                kind = "real" if ("." in tok or "times" in tok or "%" in tok) else "count"
                if kind == "count" and not LL.COUNT_CONTEXT.search(sent):
                    continue
                dec = LL._decimals(tok)
                if "times" in tok:
                    # 2.6x10^-4 is quoted to 1 mantissa decimal, so its
                    # precision is 10^-5, not a flat 6dp.
                    mm = re.match(r"([+-]?\d+)(?:\.(\d+))?\s*\\times\s*10\^"
                                  r"\{?\s*([+-]?\d+)\s*\}?", tok)
                    mant_dec = len(mm.group(2) or "") if mm else 0
                    expo = int(mm.group(3)) if mm else 0
                    dec = max(0, mant_dec - expo)
                if "%" in tok:
                    val = val / 100.0
                    dec = dec + 2
                claims.append(LL.RawClaim(
                    section=u["section"], subsection=u["subsection"],
                    surface=u["surface"], sentence=sent[:700], token=tok,
                    value=val, decimals=dec,
                    statistic_type=LL.statistic_type(sent, tok),
                    kind=kind, span=(s, e),
                    token_form=LL.token_form_type(sent, (s, e), tok),
                    extras={"block": u["text"][:4000]}))
            for vs in VERDICT_STRINGS:
                for m in re.finditer(r"(?<![A-Z_])" + vs + r"(?![A-Z_])", sent):
                    claims.append(LL.RawClaim(
                        section=u["section"], subsection=u["subsection"],
                        surface=u["surface"], sentence=sent[:700], token=vs,
                        value=float("nan"), decimals=0,
                        statistic_type="verdict_string", kind="verdict",
                        span=m.span()))
    return claims


# ==========================================================================
# Flagging
# ==========================================================================
STALE_PATTERNS = [
    (re.compile(r"fewer than 40 refusals|`UNDEFINED` when fewer than 40|"
                r"when fewer than 40", re.I),
     "STALE_SOURCE",
     "the Method describes the UNDEFINED gate as '< 40 refusals'; the shipped "
     "code gates UNDEFINED on a non-finite bootstrap CI (explib.verdict_from_ci), "
     "which fires at <= 1 refusal, while `powered` is the flag that uses the "
     "40-per-class rule (gpu_stage.py:343). Repair belongs to H-K."),
    (re.compile(r"\\geq 0\.68\b(?!5)"), "DIRECTIONAL_ROUNDING",
     "a '>= 0.68' bound that is not the generated extremum of any named "
     "population; see drift (a)"),
    (re.compile(r"20 checkpoints where reading is measurable"), "STALE_SOURCE",
     "'measurable' (a defined AUROC) is 21, not 20; see drift (b)"),
]


EXTERNAL_CUE = re.compile(r"\[\d{1,2}(?:\s*,\s*\d{1,2})*\]")
OURS_CUE = re.compile(r"\bour\b|\bwe\b|\bours\b|\bthis paper\b|\bthis study\b|"
                      r"\bARTIFACT:", re.I)


def is_external(sentence: str, section: str) -> bool:
    """A number attributed to a cited work is not ours to regenerate. It is
    still flagged UNTRACEABLE against our sources -- honestly -- but it is
    counted as a logged exception rather than as a defect."""
    if not EXTERNAL_CUE.search(sentence):
        return False
    return section == "Related Work" or not OURS_CUE.search(sentence)


def confidence(alias: str, ptr: str, sentence: str, unit_tag: str,
               pref: list[str], statistic_type: str = "real",
               token_form: str = "real") -> str:
    """How much the winning pointer is believed. A number that resolves only to
    an unrelated corner of an unrelated artifact is a coincidence, not a
    resolution, and is reported as UNTRACEABLE with the coincidence logged."""
    in_pref = alias in pref
    p_unit = LL.unit_from_pointer(ptr)
    words = set(LL.PATH_KEYWORDS.findall(sentence.lower()))
    overlap = len(words & set(LL.PATH_KEYWORDS.findall(ptr.lower())))
    if alias == "DERIVED":
        return "HIGH"
    compat = LL.key_compatible(ptr, LL.effective_type(statistic_type, token_form))
    if in_pref and compat and (not unit_tag or p_unit in (unit_tag, "NA")):
        return "HIGH"
    if compat or in_pref or overlap >= 2:
        return "MEDIUM"
    return "LOW"


def flag_claim(c: LL.RawClaim, idx: LL.PointerIndex, unit_tag: str,
               cand: list[int], conf: str) -> tuple[str, str]:
    for rx, flag, reason in STALE_PATTERNS:
        if rx.search(c.sentence):
            return flag, reason
    if c.kind == "verdict":
        hits = idx.strings.get(c.token, [])
        if hits:
            return "MATCH", "verdict string reproduced verbatim from a stamped source"
        return "UNTRACEABLE", "verdict string not present in any stamped source"
    if not cand:
        return "UNTRACEABLE", "no reportable leaf in any stamped source rounds to this value"
    if conf == "LOW":
        return "UNTRACEABLE", ("the only reportable leaves matching this value sit "
                               "in artifacts and key-paths unrelated to the claim; "
                               "recorded as a coincidence, not a resolution")
    alias, ptr, gen = idx.entries[cand[0]]
    delta = abs(gen - c.value)
    if delta == 0.0:
        base = "MATCH"
    elif delta <= 0.5 * 10.0 ** (-c.decimals) + 1e-12:
        base = "ROUNDING_OK"
    else:
        base = "VALUE_MISMATCH"
    if base in ("MATCH", "ROUNDING_OK") and not unit_tag and c.kind == "real" \
            and c.statistic_type in ("correlation", "AUROC", "Delta", "rate",
                                     "p_value", "interval", "kappa"):
        return "UNIT_MISSING", ("resolves to a source value but the sentence "
                                "does not name the aggregation unit")
    return base, "resolved against a stamped source"


def search_log(c: LL.RawClaim, idx: LL.PointerIndex, cand: list[int]) -> dict:
    """What was actually searched, so an UNTRACEABLE is a measured fact."""
    near = idx.near(c.value, c.decimals)
    all_hits = idx.lookup_all(c.value, c.decimals) if c.kind != "verdict" else []
    return {
        "aliases_searched": INDEXED_ALIASES,
        "n_reportable_leaves_searched": sum(idx.reportable_flags),
        "n_leaves_total": len(idx.entries),
        "match_rule": f"round(leaf, {min(c.decimals, 8)}) == round(claim, "
                      f"{min(c.decimals, 8)}), reportable pointers only",
        "n_exact_hits_including_non_reportable": len(all_hits),
        "non_reportable_examples": [
            {"alias": idx.entries[i][0], "pointer": idx.entries[i][1],
             "value": idx.entries[i][2],
             "excluded_because": LL.reportable(idx.entries[i][1])[1]}
            for i in all_hits[:4] if not idx.reportable_flags[i]],
        "coincidental_reportable_candidates": [
            {"alias": idx.entries[i][0], "pointer": idx.entries[i][1],
             "value": idx.entries[i][2]} for i in cand[:4]],
        "n_near_miss_candidates": len(near),
        "near_miss_examples": [
            {"alias": idx.entries[i][0], "pointer": idx.entries[i][1],
             "value": idx.entries[i][2]} for i in near[:4]],
    }


# ==========================================================================
# The three named drifts
# ==========================================================================
def resolve_drifts(e2: dict) -> dict:
    per = e2["metadata"]["results"]["h1_abliterated_arm"]["per_member"]
    base = "/metadata/results/h1_abliterated_arm/per_member"

    def defined(r):
        ci = r.get("A_ci95") or [None, None]
        return all(isinstance(x, (int, float)) and x == x for x in ci)

    rows = []
    for i, r in enumerate(per):
        rows.append({"i": i, "key": r["checkpoint"], "verdict": r["A_verdict"],
                     "auroc": r.get("A_auroc"), "ci": r.get("A_ci95"),
                     "powered": bool(r.get("powered")),
                     "n_refusal": r.get("n_refusal"),
                     "n_compliance": r.get("n_compliance"),
                     "defined": defined(r)})

    def argmin(pop):
        cand = [r for r in pop if r["auroc"] is not None and r["auroc"] == r["auroc"]]
        return min(cand, key=lambda r: r["auroc"]) if cand else None

    pop_all_defined = [r for r in rows if r["defined"]]
    pop_reads = [r for r in rows if r["verdict"] == "READS"]
    pop_powered = [r for r in rows if r["powered"] and r["defined"]]

    def pack(name, pop):
        m = argmin(pop)
        if m is None:
            return {"population": name, "n": len(pop), "minimum": None}
        return {
            "population": name, "n": len(pop), "minimum": m["auroc"],
            "member": m["key"], "verdict": m["verdict"], "ci95": m["ci"],
            "n_refusals": m["n_refusal"], "n_compliances": m["n_compliance"],
            "powered": "y" if m["powered"] else "N",
            "json_pointer": f"{base}/{m['i']}/A_auroc",
            "ci_pointer": f"{base}/{m['i']}/A_ci95",
        }

    verdicts = {}
    for r in rows:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    n_powered = sum(1 for r in rows if r["powered"])
    n_defined = len(pop_all_defined)

    # --- (c) the stale summary block ------------------------------------
    summary_txt = (REGISTRY["E2_SUMMARY"][0]).read_text()
    readme_txt = (REGISTRY["E2_README"][0]).read_text()
    results_txt = (REGISTRY["E2_RESULTS"][0]).read_text()
    stale_hits = []
    for label, path, txt in (("struct_out summary", REGISTRY["E2_SUMMARY"][0],
                              summary_txt),
                             ("README.md", REGISTRY["E2_README"][0], readme_txt),
                             ("RESULTS.md", REGISTRY["E2_RESULTS"][0], results_txt)):
        for m in re.finditer(r"(\d+) of 30\s*\n?\s*members return READS|"
                             r"(\d+) of 30 members return READS|"
                             r"(\d+) of 30\s+members return READS", txt):
            pass
        for m in re.finditer(r"(\d+)\s+of\s+30\s*\n?\s*members?\s+return\s+READS",
                             txt.replace("\n", " ")):
            stale_hits.append({"file": label, "path": str(path),
                               "quoted_reads": int(m.group(1))})

    def line_of(txt, needle):
        for i, line in enumerate(txt.splitlines(), 1):
            if needle in line:
                return i
        return None

    canonical = {"READS": verdicts.get("READS", 0),
                 "AMBIGUOUS": verdicts.get("AMBIGUOUS", 0),
                 "UNDEFINED": verdicts.get("UNDEFINED", 0),
                 "AT_CHANCE": verdicts.get("AT_CHANCE", 0)}

    return {
        "drift_a_auroc_minimum": {
            "question": "what is 'the minimum axis-A AUROC'?",
            "resolution": "TWO POPULATIONS, both shipped and both named",
            "min_auroc_all_defined": pack("all members with a defined AUROC "
                                          "(finite bootstrap CI)", pop_all_defined),
            "min_auroc_reads": pack("members with verdict READS", pop_reads),
            "min_auroc_powered": pack("members that are detection-powered "
                                      "(>= 40 per class) AND have a defined AUROC",
                                      pop_powered),
            "draft_forms_found": {
                "intro_ge_0p68": "an unattributed hand-rounded bound, matching "
                                 "no population's extremum -> DIRECTIONAL_ROUNDING",
                "s5_1_ge_0p685": "the all-defined minimum, correct once the "
                                 "population is named",
                "discussion_ge_0p685": "same as 5.1",
            },
            "forbidden_form": r"\geq 0.68 (bare)",
        },
        "drift_b_measurable_count": {
            "question": "'20 checkpoints where reading is measurable'",
            "n_members": len(rows),
            "verdict_tally": canonical,
            "n_reads": canonical["READS"],
            "n_measurable_defined_auroc": n_defined,
            "n_powered": n_powered,
            "resolution": ("'measurable' means a defined AUROC, which is "
                           f"{n_defined} = {canonical['READS']} READS + "
                           f"{canonical['AMBIGUOUS']} AMBIGUOUS, not "
                           f"{canonical['READS']}"),
            "ambiguous_members": [
                {"member": r["key"], "auroc": r["auroc"], "ci95": r["ci"],
                 "n_refusals": r["n_refusal"], "n_compliances": r["n_compliance"],
                 "powered": "y" if r["powered"] else "N",
                 "json_pointer": f"{base}/{r['i']}/A_auroc"}
                for r in rows if r["verdict"] == "AMBIGUOUS"],
        },
        "drift_c_stale_summary": {
            "question": "the artifact's 18/0/10 versus RESULTS.md's 20/1/9",
            "canonical_recomputed_from_per_member": canonical,
            "recompute_source": f"E2 {base}/*/A_verdict (30 records)",
            "stale_quotations": stale_hits,
            "readme_line": line_of(readme_txt, "18 of 30"),
            "results_md_line": line_of(results_txt, "20 of 30 members return READS"),
            "per_arm_tally": {
                arm: {"n_members": a["n_members"], "n_powered": a["n_powered"],
                      "verdicts": a["verdicts"]}
                for arm, a in e2["metadata"]["results"]["h1_abliterated_arm"]
                ["by_arm"].items()},
        },
        "per_member_rows": rows,
    }


def diagnose_stale_block(e2_dir) -> dict:
    """Locate the code path that produced each tally. The GPU stage logs one
    line per member with its verdict, so the historical tallies are recoverable
    from the logs rather than inferred."""
    import collections
    from pathlib import Path
    line_rx = re.compile(r"\[([A-Za-z0-9_]+)\] detection powered=(True|False) "
                         r"A=([0-9.na]+) ([A-Z_]+)")
    per_log = {}
    for lg in sorted(Path(e2_dir, "logs").glob("*.log")):
        counts = collections.Counter()
        latest = {}
        for line in lg.read_text(errors="replace").splitlines():
            m = line_rx.search(line)
            if m:
                latest[m.group(1)] = (m.group(2), m.group(4))
        for k, (pw, v) in latest.items():
            counts[v] += 1
        if counts:
            per_log[lg.name] = {"n_members": len(latest), "verdicts": dict(counts),
                                "n_powered": sum(1 for v in latest.values()
                                                 if v[0] == "True")}
    # Is either stale surface produced by code? A generated file would have a
    # writer; grep for one rather than asserting there is none.
    writers = {}
    for target in ("README.md", "RESULTS.md", ".terminal_claude_agent_struct_out"):
        hits = []
        for src in sorted(Path(e2_dir).glob("*.py")):
            for i, line in enumerate(src.read_text(errors="replace").splitlines(), 1):
                if target in line and ("write" in line or "open(" in line
                                       or "Path(" in line or target in line):
                    hits.append({"file": f"{src.name}:{i}", "line": line.strip()[:160]})
        writers[target] = hits
    return {"per_log_tallies": per_log, "writers_found_by_grep": writers}


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage1")
    logger.info("STAGE 1 -- claim ledger")

    draft = jload(REGISTRY["DRAFT"][0])
    idx = LL.PointerIndex()
    for alias in INDEXED_ALIASES:
        idx.add_document(alias, jload(REGISTRY[alias][0]))
    global DERIVED_DOC
    DERIVED_DOC = DERIVED.main()
    idx.add_document("DERIVED", {"values": DERIVED_DOC["values"]})
    logger.info(f"pointer index: {len(idx.entries)} numeric leaves, "
                f"{len(idx.strings)} distinct short strings")

    units = enumerate_surfaces(draft)
    claims = extract_claims(units)
    logger.info(f"extracted {len(claims)} raw claims over {len(units)} surfaces")

    e2 = jload(REGISTRY["E2"][0])
    drifts = resolve_drifts(e2)
    diag = diagnose_stale_block(REGISTRY["E2"][0].parent)
    drifts["drift_c_stale_summary"]["log_reconstructed_tallies"] = \
        diag["per_log_tallies"]
    drifts["drift_c_stale_summary"]["writers_found_by_grep"] = \
        diag["writers_found_by_grep"]
    logger.info(f"drift (b) tally: {drifts['drift_b_measurable_count']['verdict_tally']}")

    ledger = []
    for n, c in enumerate(claims):
        unit_tag, unit_hits = LL.tag_unit(c.sentence, c.extras.get("block", ""))
        pref = LL.alias_priority(c.section, c.subsection, c.sentence)
        cand = []
        if c.kind != "verdict":
            raw = idx.lookup(c.value, c.decimals)
            eff = LL.effective_type(c.statistic_type, c.token_form)
            cand = sorted(raw, key=lambda i: LL.score_candidate(
                idx.entries[i][0], idx.entries[i][1], c.sentence, unit_tag, pref,
                eff, c.value, idx.entries[i][2]))
        conf = ("NA" if c.kind == "verdict" else
                (confidence(*idx.entries[cand[0]][:2], c.sentence, unit_tag, pref,
                            c.statistic_type, c.token_form)
                 if cand else "NONE"))
        flag, reason = flag_claim(c, idx, unit_tag, cand, conf)
        alias = ptr = None
        gen = None
        if cand and flag != "UNTRACEABLE":
            alias, ptr, gen = idx.entries[cand[0]]
        elif c.kind == "verdict":
            hits = idx.strings.get(c.token, [])
            if hits:
                alias, ptr = hits[0]
                gen = c.token
        row = {
            "claim_id": f"C{n:04d}",
            "section": c.section, "subsection": c.subsection,
            "surface": c.surface, "sentence": c.sentence, "token": c.token,
            "parsed_value": (None if c.kind == "verdict" else c.value),
            "decimals_quoted": c.decimals,
            "statistic_type": c.statistic_type,
            "token_form": c.token_form,
            "aggregation_unit": unit_tag or "",
            "aggregation_unit_candidates": unit_hits,
            "source_alias": alias,
            "source_artifact_id": (REGISTRY[alias][2] if alias in REGISTRY
                                   else ("this artifact (derived)" if alias
                                         else None)),
            "source_file_path": (str(REGISTRY[alias][0]) if alias in REGISTRY
                                 else (str(OUT / "derived.json") if alias
                                       else None)),
            "source_sha256": (sha256_file(REGISTRY[alias][0]) if alias in REGISTRY
                              else (sha256_file(OUT / "derived.json") if alias
                                    else None)),
            "json_pointer": ptr,
            "pointer_unit": (LL.unit_from_pointer(ptr) if ptr else None),
            "generated_value": gen,
            "abs_delta": (None if (gen is None or c.kind == "verdict")
                          else abs(float(gen) - c.value)),
            "tolerance_rule": ("EXACT (counts and verdict strings)"
                               if c.kind in ("count", "verdict")
                               else f"|delta| <= 0.5e-{c.decimals} is ROUNDING_OK"),
            "flag": flag, "flag_reason": reason,
            "resolution_confidence": conf,
            "n_candidate_pointers": len(cand),
        }
        row["external_literature"] = (c.kind != "verdict"
                                      and is_external(c.sentence, c.section))
        row["derived_now_generated"] = (alias == "DERIVED")
        if row["derived_now_generated"]:
            row["derivation"] = DERIVED_DOC["derivations"].get(
                ptr.lstrip("/values/").split("/")[-1] if ptr else "", None)
        if flag == "UNTRACEABLE":
            row["search_log"] = search_log(c, idx, cand)
            if row["external_literature"]:
                row["flag_reason"] = (
                    "a value attributed to cited literature, not produced by any "
                    "artifact of this project; logged as an exception rather "
                    "than repaired")
        ledger.append(row)

    hist = {}
    for r in ledger:
        hist[r["flag"]] = hist.get(r["flag"], 0) + 1
    logger.info(f"flag histogram BEFORE repair: {hist}")

    by_section = {}
    for r in ledger:
        k = f"{r['section']} / {r['subsection'] or '(lead)'}"
        by_section.setdefault(k, {"n": 0, "flags": {}})
        by_section[k]["n"] += 1
        by_section[k]["flags"][r["flag"]] = by_section[k]["flags"].get(r["flag"], 0) + 1
    by_surface = {}
    for r in ledger:
        by_surface[r["surface"]] = by_surface.get(r["surface"], 0) + 1

    out = {
        "stage": "stage1_claim_ledger",
        "n_surfaces": len(units), "n_claims": len(ledger),
        "flag_histogram_before": hist,
        "per_section_breakdown": by_section,
        "per_surface_breakdown": by_surface,
        "allow_list_entries": [{"name": n, "pattern": rx.pattern}
                               for n, rx in LL.ALLOWLIST_SPANS],
        "aggregation_unit_vocabulary": LL.UNIT_PRIORITY + ["NA"],
        "three_drifts": drifts,
        "claim_ledger": ledger,
        "pointer_index_size": len(idx.entries),
        "reportable_index_size": sum(idx.reportable_flags),
        "non_reportable_excluded_by_rule": idx.excluded_counts,
        "non_reportable_rules": [{"name": n, "pattern": rx.pattern} for n, rx in LL.NOT_REPORTABLE],
        "machinery_provenance": {
            "reused_from": str(REGISTRY["V1"][0].parent / "stage4_prose.py"),
            "reused_from_sha256": sha256_file(REGISTRY["V1"][0].parent
                                              / "stage4_prose.py"),
            "copy_path": str(OUT.parent / "ledgerlib.py"),
            "copy_sha256": sha256_file(OUT.parent / "ledgerlib.py"),
            "note": ("eval_1's build_value_index hard-codes the iteration-3 "
                     "source set and audit_text recognises four statistic kinds; "
                     "the taxonomy and the rounded-value index are reused in "
                     "kind, the code is re-authored. Both shas recorded."),
        },
    }
    jdump(out, OUT / "stage1_ledger.json")
    logger.info(f"wrote {OUT / 'stage1_ledger.json'}")
    return out


if __name__ == "__main__":
    main()
