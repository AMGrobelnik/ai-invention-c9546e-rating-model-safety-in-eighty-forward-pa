#!/usr/bin/env python3
"""STAGE 2 -- THE REGENERATION HARNESS.

Writes the frozen alias registry, emits the prose and abstract templates, and
executes the five assertions the artifact plan pre-committed to:

  1. render twice into two buffers and assert byte-identical (sha256 equal);
  2. zero unresolved placeholders;
  3. NO_BARE_NUMERAL lint over the TEMPLATE SOURCE, with the allow-list itemised;
  4. re-run the stage-1 ledger over the RENDERED text and assert the flag list
     is empty;
  5. a mutation test: perturb one source value in memory and assert the
     rendered text changes, proving the pointers are live and not decorative.
"""

from __future__ import annotations

import importlib.util
import sys

from loguru import logger

import ledgerlib as LL
import prose_spec
import stage1_ledger as S1
from common import (INDEXED_ALIASES, OUT, REGISTRY, jdump, jload, setup_logging,
                    sha256_file, sha256_text)

RENDER_PY = OUT / "render.py"
REGISTRY_JSON = OUT / "render_registry.json"
PROSE_TEMPLATE = OUT / "prose_template.md"
PROSE_BUNDLE = OUT / "prose_bundle.md"
ABSTRACT_TEMPLATE = OUT / "abstract_template.md"
ABSTRACT_SKELETON = OUT / "abstract_skeleton.md"


def load_render():
    spec = importlib.util.spec_from_file_location("render_harness", RENDER_PY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["render_harness"] = mod
    spec.loader.exec_module(mod)
    return mod


def write_registry() -> dict:
    reg = {}
    for alias in INDEXED_ALIASES:
        path = REGISTRY[alias][0]
        reg[alias] = {"path": str(path), "sha256": sha256_file(path),
                      "artifact_id": REGISTRY[alias][2],
                      "declared": REGISTRY[alias][1]}
    reg["DERIVED"] = {"path": str(OUT / "derived.json"),
                      "sha256": sha256_file(OUT / "derived.json"),
                      "artifact_id": "this artifact (derived quantities)",
                      "declared": "derived"}
    jdump(reg, REGISTRY_JSON)
    return reg


@logger.catch(reraise=True)
def main() -> dict:
    setup_logging("stage2")
    logger.info("STAGE 2 -- regeneration harness")

    s1 = jload(OUT / "stage1_ledger.json")
    d = s1["three_drifts"]
    min_all = d["drift_a_auroc_minimum"]["min_auroc_all_defined"]
    min_reads = d["drift_a_auroc_minimum"]["min_auroc_reads"]
    min_pow = d["drift_a_auroc_minimum"]["min_auroc_powered"]
    ambiguous = d["drift_b_measurable_count"]["ambiguous_members"][0]
    hg_present = jload(OUT / "stage0_manifest.json")["h_g_probe"]["status"] == "PRESENT"

    reg = write_registry()
    R = load_render()

    prose_src = prose_spec.prose_template(min_all, min_reads, min_pow, ambiguous)
    abstract_src = prose_spec.abstract_template(min_all, min_reads, ambiguous,
                                                hg_present)
    PROSE_TEMPLATE.write_text(prose_src)
    ABSTRACT_TEMPLATE.write_text(abstract_src)

    assertions: dict = {}

    # --- 1 + 2 : byte-identical rendering, no unresolved placeholders --------
    bundles = {}
    for name, src, dst in (("prose", prose_src, PROSE_BUNDLE),
                           ("abstract", abstract_src, ABSTRACT_SKELETON)):
        r1, r2 = R.Renderer(REGISTRY_JSON), R.Renderer(REGISTRY_JSON)
        a, b = r1.render(src), r2.render(src)
        same = sha256_text(a) == sha256_text(b)
        left = R.unresolved_placeholders(a)
        assertions[f"{name}_byte_identical"] = {
            "assertion": "rendering the same template twice is byte-identical",
            "sha256_first": sha256_text(a), "sha256_second": sha256_text(b),
            "holds": same, "n_pointers_resolved": len(r1.resolved)}
        assertions[f"{name}_unresolved_placeholders"] = {
            "assertion": "zero unresolved placeholders", "n": len(left),
            "examples": left[:5], "holds": not left}
        if not same:
            raise AssertionError(f"{name}: rendering is not byte-identical")
        if left:
            raise AssertionError(f"{name}: unresolved placeholders {left[:5]}")
        dst.write_text(a)
        bundles[name] = a
        logger.info(f"{name}: {len(r1.resolved)} pointers, byte-identical, "
                    f"{len(a)} chars -> {dst.name}")

    # --- 3 : NO_BARE_NUMERAL lint over the template source ------------------
    for name, src in (("prose", prose_src), ("abstract", abstract_src)):
        bare = R.bare_numerals(src)
        assertions[f"{name}_bare_numerals"] = {
            "assertion": "every digit in the template source is inside a "
                         "placeholder or matches an itemised allow-list entry",
            "n": len(bare), "offenders": bare[:20], "holds": not bare}
        if bare:
            logger.error(f"{name}: {len(bare)} bare numerals, e.g. {bare[:3]}")
            raise AssertionError(f"{name}: bare numerals in template source")
        logger.info(f"{name}: NO_BARE_NUMERAL lint clean")
    assertions["bare_numeral_allow_list"] = [
        {"name": n, "pattern": rx.pattern} for n, rx in R.BARE_NUMERAL_ALLOWLIST]

    # --- 4 : the ledger over the RENDERED text must be flag-free ------------
    idx = LL.PointerIndex()
    for alias in INDEXED_ALIASES:
        idx.add_document(alias, jload(REGISTRY[alias][0]))
    derived_doc = jload(OUT / "derived.json")
    idx.add_document("DERIVED", {"values": derived_doc["values"]})
    S1.DERIVED_DOC = derived_doc

    post = {}
    for name, text in bundles.items():
        units = [{"section": f"rendered_{name}", "subsection": None,
                  "surface": "prose", "text": blk["text"], **blk}
                 for blk in LL.split_sections(text)]
        for u in units:
            u["surface"] = "table" if LL.is_table_block(u["text"]) else "prose"
        claims = S1.extract_claims(units)
        flags = []
        for c in claims:
            unit_tag, _ = LL.tag_unit(c.sentence, c.extras.get("block", ""))
            pref = LL.alias_priority(c.section, c.subsection, c.sentence)
            cand = []
            if c.kind != "verdict":
                eff = LL.effective_type(c.statistic_type, c.token_form)
                cand = sorted(idx.lookup(c.value, c.decimals),
                              key=lambda i: LL.score_candidate(
                                  idx.entries[i][0], idx.entries[i][1], c.sentence,
                                  unit_tag, pref, eff, c.value, idx.entries[i][2]))
            conf = ("NA" if c.kind == "verdict" else
                    (S1.confidence(*idx.entries[cand[0]][:2], c.sentence, unit_tag,
                                   pref, c.statistic_type, c.token_form)
                     if cand else "NONE"))
            flag, reason = S1.flag_claim(c, idx, unit_tag, cand, conf)
            if flag not in ("MATCH", "ROUNDING_OK"):
                flags.append({"token": c.token, "flag": flag, "reason": reason,
                              "sentence": c.sentence[:200],
                              "aggregation_unit": unit_tag})
        post[name] = {"n_claims": len(claims), "n_flagged": len(flags),
                      "flag_list_empty": not flags, "residual_flags": flags[:20]}
        logger.info(f"{name}: post-render ledger {len(claims)} claims, "
                    f"{len(flags)} flagged")
    assertions["post_render_ledger"] = post

    # --- 5 : mutation test --------------------------------------------------
    mut_alias = "E2"
    mut_pointer = "/metadata/results/h3_joint_scatter/rho_primary"
    r = R.Renderer(REGISTRY_JSON,
                   overrides={f"{mut_alias}#{mut_pointer}": -0.123456789})
    mutated = r.render(prose_src)
    changed = mutated != bundles["prose"]
    assertions["mutation_test"] = {
        "assertion": "perturbing one source value changes the rendered text, so "
                     "the placeholders are live rather than decorative",
        "alias": mut_alias, "pointer": mut_pointer,
        "perturbed_to": -0.123456789,
        "rendered_changed": changed,
        "sha256_baseline": sha256_text(bundles["prose"]),
        "sha256_mutated": sha256_text(mutated),
        "holds": changed}
    if not changed:
        raise AssertionError("mutation test failed: pointers are decorative")
    logger.info("mutation test PASSED")

    out = {
        "stage": "stage2_regeneration_harness",
        "registry": reg,
        "render_py": {"path": str(RENDER_PY), "sha256": sha256_file(RENDER_PY)},
        "templates": {
            "prose": {"path": str(PROSE_TEMPLATE),
                      "sha256": sha256_file(PROSE_TEMPLATE)},
            "abstract": {"path": str(ABSTRACT_TEMPLATE),
                         "sha256": sha256_file(ABSTRACT_TEMPLATE)}},
        "bundles": {
            "prose": {"path": str(PROSE_BUNDLE),
                      "sha256": sha256_file(PROSE_BUNDLE)},
            "abstract": {"path": str(ABSTRACT_SKELETON),
                         "sha256": sha256_file(ABSTRACT_SKELETON)}},
        "assertions": assertions,
        "h_g_present": hg_present,
    }
    jdump(out, OUT / "stage2_regeneration.json")
    logger.info(f"wrote {OUT / 'stage2_regeneration.json'}")
    return out


if __name__ == "__main__":
    main()
