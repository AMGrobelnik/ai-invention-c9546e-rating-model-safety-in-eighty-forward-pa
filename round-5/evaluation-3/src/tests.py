#!/usr/bin/env python3
"""Unit tests for the machinery the ledger and the harness rest on.

These are the pieces where a silent bug would produce a clean-LOOKING ledger:
the header regex that decides which section a claim belongs to, the RFC-6901
resolver, the tolerance rule, the numeral extractor's allow-list, the
reportability filter and the render format table. Run: `python tests.py`.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import ledgerlib as LL
from common import OUT, esc_ptr, resolve_pointer

HERE = Path(__file__).resolve().parent
RESULTS: list[dict] = []


def check(name: str, fn):
    try:
        fn()
        RESULTS.append({"test": name, "passed": True})
        print(f"PASS  {name}")
    except AssertionError as exc:
        RESULTS.append({"test": name, "passed": False, "error": str(exc)})
        print(f"FAIL  {name}: {exc}")
    except Exception:
        RESULTS.append({"test": name, "passed": False,
                        "error": traceback.format_exc(limit=3)})
        print(f"ERROR {name}")


# --------------------------------------------------------------------------
def test_header_regex():
    text = ("# Results\n\nlead paragraph\n\n## The unit\n\nbody text\n\n"
            "**5.1 Bolded numeric header**\n\nmore body\n\n"
            "#### Deep header\n\ndeep body\n")
    blocks = LL.split_sections(text)
    secs = [(b["section"], b["subsection"]) for b in blocks]
    assert ("Results", None) in secs, secs
    assert ("Results", "The unit") in secs, secs
    assert any(s == "Results" and sub and sub.startswith("5.1")
               for s, sub in secs), secs
    assert any(sub == "Deep header" for _, sub in secs), secs
    # a header line must not itself become a claim-bearing block
    assert all(not b["text"].startswith("# ") for b in blocks)


def test_table_block_detection():
    tbl = "| a | b |\n|---|---|\n| 1 | 2 |"
    assert LL.is_table_block(tbl)
    assert not LL.is_table_block("just prose with a | pipe")


def test_pointer_roundtrip():
    doc = {"a": {"b~c": [10, {"d/e": 42}]}, "": 7}
    assert resolve_pointer(doc, "/a/b~0c/0") == 10
    assert resolve_pointer(doc, "/a/b~0c/1/d~1e") == 42
    assert resolve_pointer(doc, "") is doc
    assert esc_ptr("b~c") == "b~0c" and esc_ptr("d/e") == "d~1e"


def test_pointer_matches_real_source():
    """Every pointer the ledger shipped must still resolve in its source."""
    ev = json.loads((HERE / "eval_out.json").read_text())
    reg = ev["metadata"]["regeneration_registry"]
    cache: dict[str, object] = {}
    checked = 0
    for row in ev["metadata"]["claim_ledger"]:
        alias, ptr = row.get("source_alias"), row.get("json_pointer")
        if not alias or not ptr or alias not in reg:
            continue
        if alias not in cache:
            cache[alias] = json.loads(Path(reg[alias]["path"]).read_text())
        v = resolve_pointer(cache[alias], ptr)
        assert isinstance(v, (int, float, str)), (alias, ptr, type(v))
        checked += 1
        if checked >= 400:
            break
    assert checked > 200, f"only {checked} pointers checked"


def test_tolerance_rule():
    """|delta| <= 0.5e-d is ROUNDING_OK; anything larger is a mismatch."""
    def tol(d):
        return 0.5 * 10.0 ** (-d)
    assert abs(0.6289 - 0.629) <= tol(3) + 1e-12
    assert abs(0.6845 - 0.685) <= tol(3) + 1e-12
    assert not abs(0.691 - 0.68) <= tol(2) + 1e-12   # the drift-(a) bound
    assert abs(0.68 - 0.685) > tol(2)                # 0.68 is not 0.685 at 2dp


def test_numeral_allowlist():
    s = ("As §5.2 shows, arXiv:2603.18353 and [11] on Qwen3-1.7B in 2026 "
         "give AUROC 0.685 and Table 3.")
    blocked = LL.allowlisted_spans(s)
    kept = []
    for m in LL.NUM_RE.finditer(s):
        a, b = m.span()
        if not any(x <= a and b <= y for x, y, _ in blocked):
            kept.append(m.group(0))
    assert "0.685" in kept, kept
    for bad in ("5.2", "2603.18353", "11", "2026", "3"):
        assert bad not in kept, (bad, kept)


def test_token_form_beats_sentence_topic():
    """A CI bound inside an AUROC sentence is an interval, and a bare integer
    is a count -- the sentence's headline statistic must not override that."""
    s = "AUROC 0.685 [0.597, 0.763] over 30 members"
    i = s.index("0.597")
    assert LL.token_form_type(s, (i, i + 5), "0.597") == "interval"
    j = s.index("30")
    assert LL.token_form_type(s, (j, j + 2), "30") == "count"
    k = s.index("0.685")
    assert LL.token_form_type(s, (k, k + 5), "0.685") == "real"
    assert LL.effective_type("AUROC", "interval") == "interval"
    assert LL.effective_type("AUROC", "real") == "AUROC"


def test_reportability_filter():
    assert not LL.reportable("/datasets/2/examples/7/metadata_meta/x")[0]
    assert not LL.reportable("/table/cfg/scores/s/member_level/jackknife/folds/3/rho")[0]
    assert LL.reportable("/metadata/results/h3_joint_scatter/rho_primary")[0]
    assert LL.reportable("/metrics_agg/ourAMS_rho_lineage_level")[0]


def test_unit_declaration_binds_paragraph():
    block = ("At the member level -- unit: the member -- the statistic is X. "
             "A later clause quotes 0.358 without repeating the unit.")
    sent = "A later clause quotes 0.358 without repeating the unit."
    assert LL.tag_unit(sent, block)[0] == "member"
    assert LL.declared_unit("unit: the (member, axis) pair") == "axis-pair"
    assert LL.declared_unit("unit: the generated item") == "item"
    assert LL.declared_unit("no declaration here") == ""


def test_render_formats_and_lint():
    import importlib.util
    spec = importlib.util.spec_from_file_location("rh", OUT / "render.py")
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    assert R.FORMATS["f3"](0.6289337765071601) == "0.629"
    assert R.FORMATS["ci3"]([0.4647695660247376, 0.8034743184332859]) \
        == "[0.465, 0.803]"
    assert R.FORMATS["sci"](4.9999750001249995e-06) == "5.0e-06"
    assert R.FORMATS["signed4"](0.2962644517928017) == "+0.2963"
    assert R.FORMATS["int_comma"](164736) == "164,736"
    assert R.FORMATS["pct1"](0.7714285714285715) == "77.1\\%"
    assert R.bare_numerals("a bare 42 here"), "lint must catch a bare numeral"
    assert not R.bare_numerals("{{ptr:E2#/a/b|f3}} and §5.1 and arXiv:2603.18353")
    assert R.unresolved_placeholders("x {{ptr:A#/b|f3}} y")


def test_verdict_tally_sums_to_panel():
    ev = json.loads((HERE / "eval_out.json").read_text())
    t = ev["metadata"]["three_drifts"]["drift_c_stale_summary"][
        "canonical_recomputed_from_per_member"]
    m = ev["metrics_agg"]
    assert sum(t.values()) == m["n_detection_members"] == 30, t
    assert t["READS"] + t["AMBIGUOUS"] == m["n_measurable_defined_auroc"], t
    assert t["AT_CHANCE"] == 0, t
    # the stale block's own arithmetic is what gives it away
    assert 18 + 0 + 10 != sum(t.values())


def test_numbering_map_is_a_bijection():
    nm = json.loads((OUT / "table_numbering_map.json").read_text())["tables"]
    new = sorted(nm["old_to_new"].values())
    assert new == list(range(1, len(new) + 1)), new
    assert nm["is_bijection"]
    assert not nm["referenced_but_no_table_object"]


def test_cost_is_zero():
    ev = json.loads((HERE / "eval_out.json").read_text())
    assert ev["metrics_agg"]["cost_usd"] == 0.0
    assert ev["metadata"]["cost_usd"] == 0.0


def main() -> int:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            check(name, fn)
    n_fail = sum(1 for r in RESULTS if not r["passed"])
    summary = {"n_tests": len(RESULTS), "n_failed": n_fail, "results": RESULTS}
    (OUT / "unit_tests.json").write_text(json.dumps(summary, indent=1))
    print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} passed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
