#!/usr/bin/env python3
"""Claim extraction, pointer resolution and flagging.

This is the machinery of iteration-4 eval_1's stage-4 prose audit, widened from
"correlations, AUROCs and Deltas in Results + Contributions" to EVERY numeric
claim on EVERY surface of the draft (prose, markdown tables, figure captions,
figure summaries, abstract) plus the verdict strings. The two functional pieces
copied in spirit -- a value index keyed on the rounded number, and a status
taxonomy -- are re-implemented here rather than imported, because eval_1's
`build_value_index` hard-codes the iteration-3 source set and its
`audit_text` only recognises four statistic kinds. Both source shas are
recorded by stage 1 so the copy is traceable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from common import is_num

# --------------------------------------------------------------------------
# Section / surface splitting
# --------------------------------------------------------------------------
HEADER_RE = re.compile(r"^(#{1,4})\s+(.*\S)\s*$|^\*\*(\d+(?:\.\d+)*)\s+(.*\S)\*\*\s*$")


def split_sections(text: str) -> list[dict]:
    """Split a markdown body into blocks tagged with (section, subsection).

    The regex is exercised by `test_header_regex` in tests.py.
    """
    blocks, sec, sub = [], "(front matter)", None
    for raw_block in text.split("\n\n"):
        block = raw_block.strip("\n")
        if not block.strip():
            continue
        first = block.split("\n", 1)[0]
        m = HEADER_RE.match(first)
        if m:
            if m.group(1):
                level, title = len(m.group(1)), m.group(2)
            else:
                level, title = 2, f"{m.group(3)} {m.group(4)}"
            if level == 1:
                sec, sub = title, None
            else:
                sub = title
            rest = block.split("\n", 1)[1] if "\n" in block else ""
            if not rest.strip():
                continue
            block = rest
        blocks.append({"section": sec, "subsection": sub, "text": block})
    return blocks


def is_table_block(block: str) -> bool:
    lines = [l for l in block.splitlines() if l.strip()]
    return len(lines) >= 2 and lines[0].lstrip().startswith("|")


SENT_SPLIT = re.compile(r"(?<=[.;:])\s+(?=[A-Z`$*\\(\[])")


def split_sentences(par: str) -> list[str]:
    return [p.strip() for p in SENT_SPLIT.split(par.replace("\n", " ")) if p.strip()]


# --------------------------------------------------------------------------
# Numeral extraction with an explicit allow-list of non-claim digits
# --------------------------------------------------------------------------
NUM_RE = re.compile(
    r"(?P<sci>[+-]?\d+(?:\.\d+)?\s*\\times\s*10\^\{?\s*[+-]?\d+\s*\}?)"
    r"|(?P<pct>\d+(?:\.\d+)?\\?%)"
    r"|(?P<dec>[+-]?\d{1,3}(?:,\d{3})*\.\d+|[+-]?\d*\.\d+)"
    r"|(?P<int>[+-]?\d{1,3}(?:,\d{3})+|[+-]?\d+)"
)

# Contexts in which a digit is NOT a claim. Each entry is (name, regex over the
# whole sentence producing spans to suppress). Every entry is itemised in the
# output so the allow-list is auditable rather than implicit.
ALLOWLIST_SPANS = [
    ("section_reference", re.compile(r"§\s*\d+(?:\.\d+)*|Section~?\s*\d+(?:\.\d+)*")),
    ("arxiv_id", re.compile(r"arXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?")),
    ("bib_marker", re.compile(r"\[\d{1,2}(?:\s*,\s*\d{1,2})*\]")),
    ("table_or_figure_number", re.compile(r"(?:Table|Figure|Fig\.?)\s*~?\s*\d+")),
    ("figure_or_artifact_tag", re.compile(r"\[(?:FIGURE|ARTIFACT):[^\]]+\]")),
    ("model_or_repo_name", re.compile(
        r"[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)*[-_.]\d+(?:[.p]\d+)*[A-Za-z-]*"
        r"|\b[A-Za-z]+\d+(?:\.\d+)?[Bb]\b")),
    ("year", re.compile(r"\b(?:19|20)\d{2}\b(?!\s*(?:checkpoints|members|lineages))")),
    ("journal_locator", re.compile(r"\b\d+\s*[:(]\s*\d+")),
    ("layer_index", re.compile(r"\bL\s*=\s*\d+|\blayer[- ]\$?L\$?\b")),
    ("latex_footnote_marker", re.compile(r"\^\{?\d\}?(?![0-9])(?!\s*\})")),
]

# Words that make a bare integer a countable claim rather than incidental prose.
COUNT_CONTEXT = re.compile(
    r"\b(checkpoints?|members?|lineages?|families|pairs?|items?|prompts?|"
    r"generations?|axes|axis|draws?|replicates?|folds?|rows?|cells?|"
    r"READS|AMBIGUOUS|UNDEFINED|AT_CHANCE|claims?|entries|references?|"
    r"grid points?|permutations?|forward passes|calls?|passages?|models?|"
    r"of\s+\d+|traceable|untraceable|mismatch)", re.I)


@dataclass
class RawClaim:
    section: str
    subsection: str | None
    surface: str
    sentence: str
    token: str
    value: float
    decimals: int
    statistic_type: str
    kind: str  # "real" | "count" | "verdict"
    token_form: str = "real"
    span: tuple[int, int] = (0, 0)
    extras: dict = field(default_factory=dict)


def allowlisted_spans(sent: str) -> list[tuple[int, int, str]]:
    spans = []
    for name, rx in ALLOWLIST_SPANS:
        for m in rx.finditer(sent):
            spans.append((m.start(), m.end(), name))
    return spans


def _decimals(tok: str) -> int:
    t = tok.replace(",", "")
    if "." in t and "times" not in t:
        return len(t.split(".")[1].rstrip("\\%").rstrip("%"))
    return 0


def _parse(tok: str) -> float | None:
    t = tok.replace(",", "").replace("\\%", "").replace("%", "").strip()
    m = re.match(r"([+-]?\d+(?:\.\d+)?)\s*\\times\s*10\^\{?\s*([+-]?\d+)\s*\}?", t)
    if m:
        return float(m.group(1)) * (10.0 ** int(m.group(2)))
    try:
        return float(t)
    except ValueError:
        return None


STAT_HINTS = [
    (re.compile(r"AUROC|AUC", re.I), "AUROC"),
    (re.compile(r"\\rho|Spearman|correlat|rank corr", re.I), "correlation"),
    (re.compile(r"\\Delta|Delta_[AB]|advantage", re.I), "Delta"),
    (re.compile(r"\\kappa|kappa", re.I), "kappa"),
    (re.compile(r"\bp\s*=|permutation|floor", re.I), "p_value"),
    (re.compile(r"\bCI\b|confidence interval|\[\s*[+-]?\d", re.I), "interval"),
    (re.compile(r"rate|fraction|retention|proportion", re.I), "rate"),
    (re.compile(r"cosine|\\cos", re.I), "cosine"),
    (re.compile(r"contrast units?|coefficient|\bc\b\s*=", re.I), "contrast_units"),
    (re.compile(r"\$\d|USD|\bspend\b|\bcost", re.I), "cost_usd"),
    (re.compile(r"minutes|seconds|hours|runtime|wall", re.I), "runtime"),
    (re.compile(r"norm", re.I), "norm"),
]


BRACKET_RE = re.compile(r"\[\s*[+-]?\d[^\]]*\]")


def token_form_type(sent: str, span: tuple[int, int], tok: str) -> str:
    """The claim's TYPE as fixed by the token itself, independent of what the
    rest of the sentence is about. A CI bound inside [a, b] is an interval and a
    bare integer is a count, even in a sentence whose headline is an AUROC."""
    for m in BRACKET_RE.finditer(sent):
        if m.start() <= span[0] and span[1] <= m.end():
            return "interval"
    if "." not in tok and "times" not in tok and "%" not in tok:
        return "count"
    return "real"


def statistic_type(sent: str, tok: str) -> str:
    if tok.strip().startswith("$") or "%" in tok:
        pass
    for rx, name in STAT_HINTS:
        if rx.search(sent):
            return name
    return "count" if "." not in tok else "real"


# --------------------------------------------------------------------------
# Aggregation-unit tagging. A blank tag is a UNIT_MISSING flag, never a guess.
# --------------------------------------------------------------------------
UNIT_PATTERNS = {
    "member": [r"\bmember[- ]level\b", r"\bper member\b", r"\bmembers?\b",
               r"\bcheckpoint[- ]level\b", r"\b\d+ of \d+ (?:members|checkpoints)\b",
               r"\bof 30 (?:members|checkpoints)\b", r"\bof 52\b", r"\bof 19\b"],
    "lineage": [r"\blineage[- ]level\b", r"\blineage[- ]aggregated\b",
                r"\b\d+ lineages?\b", r"\blineage[- ]clustered\b",
                r"\blineage bootstrap\b", r"\bn_\{?\\text\{lineage\}?\}?\b",
                r"\bper lineage\b", r"\blineage unit\b"],
    "item": [r"\bheld-out items?\b", r"\bper item\b", r"\bitem level\b",
             r"\b7,241\b", r"\bitems? are scored\b", r"\bscored items\b",
             r"\bn = 600\b", r"\bitems\b"],
    "prompt": [r"\bper prompt\b", r"\bprompt[- ]clustered\b", r"\bprompt level\b",
               r"\bprompts?\b"],
    "axis-pair": [r"\(member, axis\) pairs?\b", r"\baxis pairs?\b",
                  r"\bmember, axis\b"],
    "checkpoint": [r"\bdepth[- ]panel checkpoints?\b", r"\bper checkpoint\b",
                   r"\bsix checkpoints\b", r"\b6 of 6\b", r"\bcheckpoints?\b"],
    "grid point": [r"\bgrid points?\b", r"\bfull factorial\b", r"\bfactorial in\b"],
    "reference": [r"\breferences?\b", r"\bbibliograph", r"\bentries\b",
                  r"\bcited\b"],
}
_UNIT_RX = {u: [re.compile(p, re.I) for p in ps] for u, ps in UNIT_PATTERNS.items()}
# order matters: the most specific unit wins when several match.
UNIT_PRIORITY = ["axis-pair", "grid point", "lineage", "member", "item",
                 "prompt", "checkpoint", "reference"]


# An explicit "unit: the item" declaration binds the WHOLE paragraph, which is
# how a long multi-clause sentence keeps its unit after sentence splitting.
UNIT_DECL = re.compile(r"unit:\s*the\s+([a-z ,()-]+)", re.I)
UNIT_DECL_MAP = {
    "member": "member", "lineage": "lineage", "item": "item",
    "generated item": "item", "prompt": "prompt", "checkpoint": "checkpoint",
    "grid point": "grid point", "cell": "member", "pair": "axis-pair",
    "(member, axis)": "axis-pair", "reference": "reference",
    "lineage permutation": "lineage",
}


def declared_unit(text: str) -> str:
    for m in UNIT_DECL.finditer(text):
        key = m.group(1).strip().lower()
        if key in UNIT_DECL_MAP:
            return UNIT_DECL_MAP[key]
        # longest key first: "(member, axis) pair" must not resolve to "member"
        for k, v in sorted(UNIT_DECL_MAP.items(), key=lambda kv: -len(kv[0])):
            if k in key:
                return v
    return ""


def tag_unit(sent: str, block: str = "") -> tuple[str, list[str]]:
    decl = declared_unit(sent) or declared_unit(block)
    hits = [u for u in UNIT_PRIORITY if any(rx.search(sent) for rx in _UNIT_RX[u])]
    if decl:
        return decl, ([decl] + [h for h in hits if h != decl])
    return (hits[0] if hits else ""), hits


# --------------------------------------------------------------------------
# Pointer index
# --------------------------------------------------------------------------
UNIT_FROM_POINTER = [
    (re.compile(r"member_level|/per_member|member-level"), "member"),
    (re.compile(r"lineage_level|lineage_aggregated|per_lineage|rho_lineage"), "lineage"),
    (re.compile(r"joint_scatter|_pairs?\b"), "axis-pair"),
    (re.compile(r"grid|surfaces?/|by_required"), "grid point"),
    (re.compile(r"per_checkpoint|per_member_matched|/members?/"), "checkpoint"),
    (re.compile(r"prompt"), "prompt"),
    (re.compile(r"item|pooled_matched|rates_filtered"), "item"),
    (re.compile(r"metadata_audit"), "reference"),
]


def unit_from_pointer(ptr: str) -> str:
    for rx, u in UNIT_FROM_POINTER:
        if rx.search(ptr):
            return u
    return "NA"


# --------------------------------------------------------------------------
# Reportability filter.
#
# With ~123k numeric leaves across the stamped sources, a 2-decimal number
# collides with SOMETHING almost surely, so an unfiltered index resolves a claim
# to a per-example record or a jackknife fold and calls it traceable. That is a
# false MATCH, which is worse than an honest UNTRACEABLE. Tier 1 therefore holds
# only leaves whose pointer denotes a REPORTABLE summary statistic; Tier 2 holds
# everything and is used solely to populate the search log of an UNTRACEABLE
# row, never to resolve a claim.
# --------------------------------------------------------------------------
NOT_REPORTABLE = [
    ("per_example_record", re.compile(r"^/datasets/\d+/examples/")),
    ("jackknife_fold", re.compile(r"/jackknife/folds/|/loo_[a-z]+/folds/|/folds/\d")),
    ("permutation_draw", re.compile(r"/null_distribution/|/perm_draws?/|/replicates?/\d")),
    ("screened_out_candidate", re.compile(r"/skipped/|/panel_selection/reject")),
    ("judge_or_generation_cache", re.compile(r"/judge_cache|/generations?/\d|/rollouts?/\d")),
    ("bibliography_record", re.compile(r"^/sources/|/bibtex")),
    ("raw_grid_cell", re.compile(r"/grid/\d+/|/cells?/\d+/(?!.*summary)")),
    ("axis_raw_vector", re.compile(r"/aurocs_projection/\d|/shared_c/\d|/alphas?/\d")),
    ("timestamp_or_path", re.compile(r"created_utc|_seconds?$|sha256|/path$|elapsed")),
]


def reportable(ptr: str) -> tuple[bool, str]:
    for name, rx in NOT_REPORTABLE:
        if rx.search(ptr):
            return False, name
    return True, ""


class PointerIndex:
    """value -> candidate (alias, pointer). Lookup is by rounding to the number
    of decimals the paper actually quoted, so a claim written to 3dp is
    compared against the source at 3dp -- never the other way round."""

    def __init__(self) -> None:
        self.entries: list[tuple[str, str, float]] = []   # alias, pointer, value
        self.reportable_flags: list[bool] = []
        self.by_round: dict[int, dict[float, list[int]]] = {d: {} for d in range(0, 9)}
        self.by_round_all: dict[int, dict[float, list[int]]] = {d: {} for d in range(0, 9)}
        self.strings: dict[str, list[tuple[str, str]]] = {}
        self.excluded_counts: dict[str, int] = {}

    def add_document(self, alias: str, doc) -> None:
        from common import walk_numeric
        for ptr, val in walk_numeric(doc):
            if is_num(val):
                ok, why = reportable(ptr)
                if not ok:
                    self.excluded_counts[why] = self.excluded_counts.get(why, 0) + 1
                i = len(self.entries)
                self.entries.append((alias, ptr, float(val)))
                self.reportable_flags.append(ok)
                for d in range(0, 9):
                    key = round(float(val), d)
                    self.by_round_all[d].setdefault(key, []).append(i)
                    if ok:
                        self.by_round[d].setdefault(key, []).append(i)
            elif isinstance(val, str) and 0 < len(val) <= 80:
                self.strings.setdefault(val.strip(), []).append((alias, ptr))

    def lookup(self, value: float, decimals: int) -> list[int]:
        return self.by_round[min(decimals, 8)].get(round(value, min(decimals, 8)), [])

    def lookup_all(self, value: float, decimals: int) -> list[int]:
        return self.by_round_all[min(decimals, 8)].get(round(value, min(decimals, 8)), [])

    def near(self, value: float, decimals: int) -> list[int]:
        """Candidates one unit-in-the-last-place away: the VALUE_MISMATCH set."""
        step = 10.0 ** (-min(decimals, 8))
        out = []
        for k in (value - step, value + step, value - 2 * step, value + 2 * step):
            out.extend(self.by_round[min(decimals, 8)].get(round(k, min(decimals, 8)), []))
        return out


# alias preference by draft section: the artifact that owns the section is
# searched first, so a coincidental numeric collision elsewhere cannot win.
SECTION_ALIAS_PRIORITY = [
    (re.compile(r"archived pool|archived item pool|re-encoded|iteration-3 "
                r"certificate|earlier certificate|previous certificate|"
                r"7,241", re.I), ["A1_ANALYSIS1", "A1_ANALYSIS2", "A1_PROVENANCE",
                                  "A1_EVAL"]),
    (re.compile(r"prompt sets|panel manifest|verified checkpoints|"
                r"harmless|XSTest|AdvBench|WikiText|jailbreak items|"
                r"stratified core|frozen manifest", re.I), ["D1"]),
    (re.compile(r"5\.1|Reading and steering|both roles|spontaneous|READS|"
                r"AT_CHANCE|UNDEFINED|abliterat|induction|induce|random direction|"
                r"empirical null|axis-contrast|contrast units|escalation ladder|"
                r"read.act|joint scatter|detection", re.I), ["E2"]),
    (re.compile(r"5\.2|28 lineages|scale panel|paraphrase refit|SET B|Delta_A|"
                r"\\Delta_A|R1 |R2 |R3 |R4 |52 members|archived 19|new members|"
                r"Table I|reimplementation", re.I), ["E1", "E1_PREREG"]),
    (re.compile(r"5\.3|semantic|matched contrast|degenerat|fluency|five-class|"
                r"four-class|Rogan|floor|retention|judge", re.I),
     ["V2", "V2_VERDICT", "V2_MATCHED", "V2_RETENTION"]),
    (re.compile(r"5\.4|aggregation unit|threshold|discrimination matrix|"
                r"falsification|battery|member level|lineage level|logit-gap|"
                r"grid point|factorial|prose audit|traceable|lineage-aggregated|"
                r"lineage aggregat|aggregation|our-AMS|our AMS|alpha_\{?50|"
                r"\\alpha_\{50\}|permutation", re.I),
     ["V1_S1", "V1_S2", "V1", "V1_S0", "V1_S4", "E3"]),
]


def alias_priority(section: str, subsection: str | None, sentence: str) -> list[str]:
    """All four artifact families can be named in one sentence (a Contributions
    bullet routinely is), so the rules are SCORED by how many of their cues the
    sentence carries and the best-scoring family leads. Taking the first rule
    that matches would hand every sentence containing the word 'induce' to the
    read-versus-act artifact."""
    ctx = f"{section} {subsection or ''} {sentence}"
    scored = []
    for i, (rx, aliases) in enumerate(SECTION_ALIAS_PRIORITY):
        n = len(rx.findall(ctx))
        if n:
            scored.append((-n, i, aliases))
    scored.sort()
    out: list[str] = []
    for _, _, aliases in scored:
        out.extend(a for a in aliases if a not in out)
    return out


PATH_KEYWORDS = re.compile(r"[a-z][a-z0-9_]{3,}")

# A pointer is semantically compatible with a claim when the key it ends in
# names the same kind of statistic the sentence is quoting. This is what stops
# a rate resolving to a checkpoint count in an unrelated artifact.
STAT_KEY_COMPAT = {
    "correlation": re.compile(r"rho|spearman|corr"),
    "AUROC": re.compile(r"auroc|\bauc\b|auc_"),
    "Delta": re.compile(r"delta|advantage|diff|gap"),
    "interval": re.compile(r"ci95|ci_|_ci|_lo|_hi|lower|upper|bound|range|band"),
    "p_value": re.compile(r"(^|_)p($|_)|p_boot|p_perm|p_min|pvalue|floor|adjusted"),
    "rate": re.compile(r"rate|fraction|frac|retention|prevalence|proportion|share"),
    "kappa": re.compile(r"kappa"),
    "count": re.compile(r"(^|[_/])n([_/]|$)|count|members|lineages|pairs|items|"
                        r"total|passes|generations|reps|folds|checked|scored|"
                        r"cells|calls|strings|draws|queued|scanned|kept|"
                        r"checkpoints|prompts|rows|replicates|_k$|_m$"),
    "cost_usd": re.compile(r"cost|usd|spend|price"),
    "runtime": re.compile(r"second|minute|hour|wall|elapsed|runtime"),
    "cosine": re.compile(r"cos"),
    "contrast_units": re.compile(r"c50|contrast|alpha|coefficient|units"),
    "norm": re.compile(r"norm"),
    "real": re.compile(r"rho|auroc|auc|delta|rate|fraction|kappa|cos|mean|median|"
                       r"value|score|sigma|estimate|point|norm|c50|contrast|"
                       r"threshold|floor|min|max|gap|advantage|retention|"
                       r"depth|layer|relative|alpha|error|jaccard|param|"
                       r"seconds|minutes|usd|cost|spend|width|band|magnitude"),
    "verdict_string": re.compile(r"verdict|status|tier|class"),
}


def effective_type(statistic_type: str, token_form: str) -> str:
    """The type used to judge whether a pointer is a plausible source: the
    token's own form wins when it fixes the type (a bare integer is a count, a
    bracketed number is an interval), otherwise the sentence's headline
    statistic decides."""
    return token_form if token_form in ("count", "interval") else statistic_type


def key_compatible(ptr: str, statistic_type: str) -> bool:
    tail = "/".join(ptr.lower().split("/")[-3:])
    rx = STAT_KEY_COMPAT.get(statistic_type)
    return bool(rx and rx.search(tail))


def score_candidate(alias: str, ptr: str, sentence: str, unit_tag: str,
                    pref: list[str], statistic_type: str = "real",
                    value: float | None = None, generated: float | None = None
                    ) -> tuple:
    p_unit = unit_from_pointer(ptr)
    sent_words = set(w.lower() for w in PATH_KEYWORDS.findall(sentence.lower()))
    path_words = set(PATH_KEYWORDS.findall(ptr.lower()))
    overlap = len(sent_words & path_words)
    exact = 0 if (value is not None and generated is not None
                  and float(generated) == float(value)) else 1
    return (
        pref.index(alias) if alias in pref else len(pref) + 1,
        exact,
        0 if key_compatible(ptr, statistic_type) else 1,
        0 if unit_from_pointer(ptr) != "NA" else 1,
        0 if (unit_tag and p_unit == unit_tag) else 1,
        -overlap,
        ptr.count("/"),
        len(ptr),
        alias, ptr,
    )
