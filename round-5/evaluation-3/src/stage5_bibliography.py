#!/usr/bin/env python3
"""STAGE 5 -- BIBLIOGRAPHY MECHANICS.

Parses the draft's reference list, detects every truncated author list, and
completes it from the corrected BibTeX block already shipped by the
citation-audit research artifact. Then RE-ASSERTS that each correction that
audit found is actually applied in the current draft, one ledger row per entry
with flag APPLIED / NOT_APPLIED / SUPERSEDED and both strings quoted.

No author list is ever fabricated: an entry the audit does not cover and whose
authors are not otherwise reachable stays NOT_APPLIED with a reason.
"""

from __future__ import annotations

import re

from loguru import logger

from common import OUT, REGISTRY, jdump, jload, setup_logging

ENTRY_RE = re.compile(r"^\[(\d+)\]\s+(.*)$", re.S)
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?")
INITIAL_RE = re.compile(r"\b[A-Z]\.(?:-[A-Z]\.)*\s+[A-Z][\w'’-]+")


def parse_references(paper_text: str) -> list[dict]:
    m = re.search(r"^# References\s*$", paper_text, re.M)
    if not m:
        raise ValueError("no '# References' heading in the draft")
    body = paper_text[m.end():]
    out = []
    for block in body.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        em = ENTRY_RE.match(b)
        if not em:
            continue
        num, txt = int(em.group(1)), " ".join(em.group(2).split())
        am = ARXIV_RE.search(txt)
        # The author list ends at the first sentence-ending period -- one NOT
        # preceded by a single capital letter, which is what an initial looks
        # like. Splitting on every ". " instead truncates "T. M. Bury" to "T".
        parts = re.split(r"(?<![A-Z])\.\s+(?=[A-Z*])", txt, maxsplit=1)
        author_field = parts[0].strip() if parts else txt
        out.append({
            "number": num, "raw": txt,
            "arxiv_id": am.group(1) if am else None,
            "arxiv_version": am.group(2) if am and am.group(2) else None,
            "author_field": author_field,
            "n_named_authors": len(INITIAL_RE.findall(author_field)),
            "authors_head": author_field,
        })
    return out


TRUNCATION_RULES = [
    ("et_al", lambda e: bool(re.search(r"\bet al\.?", e["author_field"]))),
    ("single_surname_no_initial",
     lambda e: e["n_named_authors"] == 0),
    ("trailing_comma", lambda e: e["author_field"].rstrip().endswith(",")),
]


def authors_from_bibtex(bibtex: str) -> list[str]:
    m = re.search(r"author\s*=\s*\{(.*?)\}\s*,\s*\n", bibtex, re.S)
    if not m:
        return []
    return [a.strip() for a in re.split(r"\s+and\s+", m.group(1)) if a.strip()]


def abbreviate(name: str) -> str:
    parts = name.replace("{", "").replace("}", "").split()
    if len(parts) == 1:
        return parts[0]
    initials = " ".join(f"{p[0]}." for p in parts[:-1] if p and p[0].isalpha())
    return f"{initials} {parts[-1]}"


def format_author_list(names: list[str]) -> str:
    short = [abbreviate(n) for n in names]
    if len(short) == 1:
        return short[0]
    return ", ".join(short[:-1]) + ", and " + short[-1]


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage5")
    logger.info("STAGE 5 -- bibliography mechanics")
    draft = jload(REGISTRY["DRAFT"][0])
    r1 = jload(REGISTRY["R1"][0])
    audit = {a["id"]: a for a in r1["metadata_audit"]}

    refs = parse_references(draft["paper_text"])
    logger.info(f"parsed {len(refs)} reference entries")

    fixes, truncated = [], 0
    for e in refs:
        flags = [name for name, fn in TRUNCATION_RULES if fn(e)]
        a = audit.get(e["arxiv_id"]) if e["arxiv_id"] else None
        names = authors_from_bibtex(a["bibtex"]) if a and a.get("bibtex") else []
        completed = format_author_list(names) if names else None
        row = {
            "number": e["number"], "arxiv_id": e["arxiv_id"],
            "current_author_field": e["author_field"],
            "truncation_flags": flags,
            "n_named_authors_in_draft": e["n_named_authors"],
            "audit_entry_found": a is not None,
            "audit_status": (a or {}).get("status"),
            "audit_note": (a or {}).get("note"),
            "authoritative_authors": names or None,
            "completed_author_field": completed,
            "bibtex": (a or {}).get("bibtex"),
        }
        if flags:
            truncated += 1
            if completed:
                row["action"] = "COMPLETED_FROM_AUDITED_BIBTEX"
            else:
                row["action"] = "NOT_APPLIED"
                row["reason"] = ("the citation audit does not cover this entry "
                                 "and no authoritative author list is reachable "
                                 "offline; an author list is never fabricated")
        else:
            row["action"] = "NO_TRUNCATION_DETECTED"
        fixes.append(row)

    # --- re-assert every correction the audit found -------------------------
    corrections = []
    text = draft["paper_text"]
    for a in r1["metadata_audit"]:
        if a.get("status") != "MISMATCH":
            continue
        ref = next((e for e in refs if e["arxiv_id"] == a["id"]), None)
        names = authors_from_bibtex(a.get("bibtex", ""))
        want_surname = names[0].split()[-1] if names else None
        want_initial = names[0][0] if names else None
        cur = ref["author_field"] if ref else ""
        raw = ref["raw"] if ref else ""

        def norm(t):
            return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()

        title_ok = (not a.get("actual_title")
                    or norm(a["actual_title"])[:60] in norm(raw))
        applied = None
        if ref is None:
            applied, why = "NOT_APPLIED", "entry not present in the draft's list"
        elif want_surname is None:
            applied, why = "NOT_APPLIED", "audit entry carries no BibTeX authors"
        else:
            # the surname must be present AND the leading initial must be the
            # right one; "M. S. B. Nadaf" satisfies both for "Mohammed ... Nadaf"
            surname_ok = re.search(rf"\b{re.escape(want_surname)}\b", cur) is not None
            initial_ok = re.match(rf"\s*{want_initial}\.", cur) is not None \
                or re.match(rf"\s*{re.escape(names[0].split()[0])}\b", cur) is not None
            has_right = surname_ok and initial_ok
            wrong_et_al = ("et al" in cur.lower() and len(names) == 1)
            if has_right and not wrong_et_al and title_ok:
                applied, why = "APPLIED", ("the corrected author field and title "
                                           "are both in the draft")
            elif has_right and not wrong_et_al and not title_ok:
                applied, why = ("NOT_APPLIED",
                                "author corrected but the title still differs "
                                "from the arXiv record")
            elif has_right and wrong_et_al:
                applied, why = ("NOT_APPLIED",
                                "initial corrected but 'et al.' remains on a "
                                "single-author paper")
            else:
                applied, why = "NOT_APPLIED", "the draft still carries the old form"
        corrections.append({
            "arxiv_id": a["id"], "reference_number": ref["number"] if ref else None,
            "audit_note": a.get("note"),
            "cited_string_in_audit": a.get("cited_title"),
            "actual_string": a.get("actual_title"),
            "draft_author_field": cur,
            "draft_entry": raw,
            "title_matches_arxiv_record": title_ok,
            "corrected_author_field": format_author_list(names) if names else None,
            "flag": applied, "reason": why,
        })

    hist = {}
    for c in corrections:
        hist[c["flag"]] = hist.get(c["flag"], 0) + 1
    logger.info(f"{len(corrections)} audited corrections -> {hist}")

    # --- the completed reference list, ready to paste ----------------------
    lines = ["# Completed reference list (author fields regenerated from the "
             "audited BibTeX; every other field left as the draft has it)\n"]
    for e, fx in zip(refs, fixes):
        if fx.get("completed_author_field"):
            tail = e["raw"][len(e["author_field"]):].lstrip(". ").strip()
            lines.append(f"[{e['number']}] {fx['completed_author_field']}. {tail}\n")
        else:
            lines.append(f"[{e['number']}] {e['raw']}\n")
    (OUT / "references_completed.md").write_text("\n".join(lines))

    out = {
        "stage": "stage5_bibliography",
        "n_references": len(refs),
        "n_entries_with_truncation_flag": truncated,
        "n_audited_corrections": len(corrections),
        "correction_flag_histogram": hist,
        "audit_source": {"artifact": "art_G5SIDXT53EAW",
                         "n_audited": r1.get("audited_count"),
                         "n_mismatch": r1.get("mismatch_count")},
        "reference_11": next((f for f in fixes if f["number"] == 11), None),
        "bibliography_fixes": fixes,
        "corrections_reassertion": corrections,
        "completed_list_path": str(OUT / "references_completed.md"),
        "policy": "an author list is never fabricated; an unresolvable entry "
                  "stays NOT_APPLIED with a reason",
        "web_lookups_performed": 0,
    }
    jdump(out, OUT / "stage5_bibliography.json")
    logger.info(f"wrote {OUT / 'stage5_bibliography.json'}")
    return out


if __name__ == "__main__":
    main()
