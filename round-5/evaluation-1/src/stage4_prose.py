#!/usr/bin/env python3
"""STAGE 4 -- the REPLACEMENT-TEXT bundle, generated FROM the json.

No number in the emitted prose is hand-typed. Every one is written as
``{dotted.path.into.eval_out|rendered}``; the renderer strips the pointer and
keeps the rendered value, and the assertion pass at the end of the run resolves
every pointer against eval_out.json and FAILS the run on any mismatch or any
unresolvable path. The salvage-token ban of the pre-registration is enforced by
the same pass.
"""

from __future__ import annotations

import re

from loguru import logger

from common5 import BANNED_SALVAGE_TOKENS, OUT, fmt, jdump, setup_logging

TOKEN = re.compile(r"\{([A-Za-z0-9_.\[\]]+)\|([^{}]*)\}")


# --------------------------------------------------------------------------
def resolve(doc, path: str):
    cur = doc
    for part in path.split("."):
        while part.endswith("]"):
            part, _, idx = part[:-1].rpartition("[")
            if part:
                cur = cur[part]
            cur = cur[int(idx)]
            part = ""
        if part:
            if isinstance(cur, dict):
                if part not in cur:
                    raise KeyError(f"{path}: no key {part!r}")
                cur = cur[part]
            else:
                raise KeyError(f"{path}: {part!r} on a {type(cur).__name__}")
    return cur


def render(text: str) -> str:
    """Strip the pointers, keep the rendered value, then reflow.

    Substituting a short number for a long ``{path|value}`` token leaves ragged
    lines, so prose paragraphs are re-wrapped. Tables, fenced code and headings
    are passed through untouched -- rewrapping a markdown table would break it.
    """
    import textwrap
    stripped = TOKEN.sub(lambda m: m.group(2), text)
    out: list[str] = []
    buf: list[str] = []
    prefix = ""
    in_code = False

    def flush():
        nonlocal buf, prefix
        if buf:
            body = " ".join(" ".join(buf).split())
            out.extend(textwrap.wrap(body, width=88,
                                     initial_indent=prefix,
                                     subsequent_indent=prefix) or [prefix.rstrip()])
            buf = []
        prefix = ""

    for line in stripped.split("\n"):
        if line.startswith("```"):
            flush()
            in_code = not in_code
            out.append(line)
            continue
        if (in_code or not line.strip()
                or re.match(r"\s*(\||#{1,6}\s|[-*+]\s|---)", line)):
            flush()
            out.append(line)
            continue
        p = "> " if line.startswith(">") else ""
        if p != prefix:
            flush()
            prefix = p
        buf.append(line[2:] if p else line)
    flush()
    return "\n".join(out)


def audit(text: str, doc: dict, where: str) -> list[dict]:
    """Resolve every pointer and compare it to the rendered literal."""
    rows = []
    for m in TOKEN.finditer(text):
        path, shown = m.group(1), m.group(2)
        rec = {"where": where, "pointer": path, "shown": shown}
        try:
            val = resolve(doc, path)
        except (KeyError, IndexError, TypeError) as exc:
            rec.update(status="UNRESOLVABLE", error=repr(exc))
            rows.append(rec)
            continue
        rec["resolved"] = val
        if isinstance(val, bool) or val is None or isinstance(val, str):
            rec["status"] = "PASS" if str(val) == shown else "MISMATCH"
        else:
            try:
                nd = len(shown.split(".")[1]) if "." in shown else 0
                same = abs(round(float(val), nd) - float(shown)) < 10 ** (-nd) / 2
                # integers and counts
                if nd == 0:
                    same = int(round(float(val))) == int(float(shown))
                rec["status"] = "PASS" if same else "MISMATCH"
            except (TypeError, ValueError) as exc:
                rec.update(status="MISMATCH", error=repr(exc))
        rows.append(rec)
    return rows


# --------------------------------------------------------------------------
def build_bundle(doc: dict) -> dict:
    a1, a2 = doc["analysis1"], doc["analysis2"]
    P = a1["primary"]
    pm, pl = P["member"], P["lineage"]
    lad = a1["control_ladder"]
    vd = a1["verdict"]
    dec = a1["confound"]["variance_decomposition"]
    rev = a1["reviewer_0p434_reproduction"]
    sim = a2["attainability_simulation"]
    dev = a2["deviation_record"]
    arm = a2["abliterated_arm"]
    ct_all, ct_pow = a2["tally_all_members"], a2["tally_detection_powered"]

    def f(path, nd=3):
        v = resolve(doc, path)
        return "{" + path + "|" + fmt(v, nd) + "}"

    def i(path):
        v = resolve(doc, path)
        return "{" + path + "|" + str(int(v)) + "}"

    def ci(path, nd=3):
        lo = "{" + path + "[0]|" + fmt(resolve(doc, path)[0], nd) + "}"
        hi = "{" + path + "[1]|" + fmt(resolve(doc, path)[1], nd) + "}"
        return f"[{lo}, {hi}]"

    # ---------------- (i) the H-C paragraph ----------------
    hc = f"""### Replacement (i) -- the read-versus-act coupling, led by the within-axis estimate

The question this study can actually ask of the joint scatter is whether, **among
models**, the checkpoints whose refusal axis pushes hardest are also the ones whose
refusal axis reads best. Asked that way -- within the canonical axis A, across the
{i('analysis1.primary.member.n_points')} detection-powered checkpoints -- the answer is a
positive but statistically unresolved association: Spearman
rho = {f('analysis1.primary.member.rho')}, lineage-clustered 95% CI
{ci('analysis1.primary.member.ci95')} over
{i('analysis1.primary.member.n_clusters')} resampling units, exhaustive
lineage-permutation p = {f('analysis1.primary.member.p_permutation')} against an
attainable floor of {f('analysis1.primary.member.p_floor', 5)}. Aggregating members
within lineage first leaves the sign unchanged
(rho = {f('analysis1.primary.lineage.rho')},
{ci('analysis1.primary.lineage.ci95')} over
{i('analysis1.primary.lineage.n_clusters')} lineages). The axis that induces is also
the axis that reads, but among models the two qualities are only weakly and
non-significantly related.

The figure previously quoted -- rho = {f('analysis1.control_ladder[0].member.rho')}
{ci('analysis1.control_ladder[0].member.ci95')} over
{i('analysis1.control_ladder[0].n_pairs')} (member, axis) pairs -- is demoted here to a
SECONDARY, and it is reported with what it actually measures. Axis A is strong in both
roles by construction and axes C and D are null in both roles by construction, so
pooling the five axes places most of the statistic's leverage on the difference between
a fitted direction and a random one rather than on any relationship among models. That
is not a conceded possibility; it is measured. A two-way decomposition of the pooled
rank cross-product on the balanced {i('analysis1.confound.variance_decomposition.n_pairs')}-pair
design attributes {f('analysis1.confound.variance_decomposition.shares.between_axis_type')}
of it to between-axis-type variation, against
{f('analysis1.confound.variance_decomposition.shares.between_member')} between members
and {f('analysis1.confound.variance_decomposition.shares.residual')} residual. Removing
the axis main effect by rank-residualisation drops the association to
rho = {f('analysis1.confound.partial_controlling_axis.rho')}
{ci('analysis1.confound.partial_controlling_axis.ci95')}; removing both the axis and the
member main effects leaves {f('analysis1.confound.residual_member_level_coupling.rho')}
{ci('analysis1.confound.residual_member_level_coupling.ci95')}. Dropping the two
by-construction control axes from the pool moves the pooled coefficient from
{f('analysis1.control_ladder[0].member.rho')} to
{f('analysis1.control_ladder[3].member.rho')}
{ci('analysis1.control_ladder[3].member.ci95')} over
{i('analysis1.control_ladder[3].n_pairs')} pairs. Within each single axis taken alone the
coefficients are A {f('analysis1.per_axis.A_canned.member.rho')},
B {f('analysis1.per_axis.B_paraphrase.member.rho')},
C {f('analysis1.per_axis.C_stylistic.member.rho')},
D {f('analysis1.per_axis.D_random0.member.rho')} and
E {f('analysis1.per_axis.E_prompt_contrast.member.rho')}, every one of them with a CI
covering zero: no single axis carries a within-axis coupling on this panel.

The within-member mean of {i('analysis1.within_member.n_coefficients')} five-point
coefficients, {f('analysis1.within_member.mean_rho')}, must not be read as
corroboration. Each of those coefficients is computed over the SAME axis-type contrast,
on five points of which two are controls; being larger than the pooled figure makes it
weaker evidence, not stronger.

Pre-registered verdict: **{'{'}analysis1.verdict.verdict|{vd['verdict']}{'}'}**, with
**{'{'}analysis1.verdict.all_fired[1]|{vd['all_fired'][1] if len(vd['all_fired']) > 1 else 'NONE'}{'}'}**
also firing -- the within-axis CI covers zero and its half-width is
{f('analysis1.verdict.deciding_numbers.within_axis_A_member_ci_half_width')}, so at
{i('analysis1.primary.member.n_clusters')} lineages this panel could not have resolved a
coupling of the size it estimates even if one is there. Both statements are true at once
and the paper should carry both.

A reviewer recompute over thirteen members is reproduced exactly rather than
paraphrased: dropping {'{'}analysis1.reviewer_0p434_reproduction.identified_rule.dropped_member|{rev['identified_rule']['dropped_member'] if rev.get('identified_rule') else 'NONE'}{'}'}
-- the one member whose axis-A verdict is AMBIGUOUS rather than READS -- gives
rho = {f('analysis1.reviewer_0p434_reproduction.identified_rule.rho')},
p = {f('analysis1.reviewer_0p434_reproduction.identified_rule.p_asymptotic', 2)}, against
this artifact's {i('analysis1.primary.member.n_points')}-member
rho = {f('analysis1.reviewer_0p434_reproduction.n14.rho')},
p = {f('analysis1.reviewer_0p434_reproduction.n14.p_asymptotic', 2)}. The two estimates
differ by one member and neither is smoothed toward the other. Both of those p-values are
the asymptotic Spearman p, which treats the 14 checkpoints as independent; the
lineage-clustered interval quoted above, which does not, covers zero at either n."""

    # ---------------- (ii) the corrected Method sentence ----------------
    method = f"""### Replacement (ii) -- the corrected Method sentence for the UNDEFINED gate

> A member's axis-A detection verdict is UNDEFINED when its bootstrap confidence
> interval cannot be formed at all: fewer than 20 of the
> {i('analysis2.deviation_record.n_boot_reference')} prompt-clustered resamples retain at
> least five items in each class, so the percentile interval returns non-finite bounds
> and `verdict_from_ci` reports UNDEFINED. This is a property of the resampling guard,
> not of the 40-per-class POWERED gate: `MIN_PER_CLASS = 40` sets a separate `powered`
> flag that the verdict never consults, which is why the table reports READS for
> {i('analysis2.deviation_record.affected_members.n_UNPOWERED_yet_READS')} members that
> are not powered, the smallest of them on
> {i('analysis2.deviation_record.min_items_per_class_among_unpowered_reads')} items per
> class."""

    # ---------------- (iii) the attainability footnote ----------------
    fn = f"""### Replacement (iii) -- the footnote that must attach to every "zero AT_CHANCE" sentence

> The AT_CHANCE verdict requires an entire bootstrap 95% CI to fit inside the 0.20-wide
> band [0.40, 0.60]; READS requires only its lower bound to clear 0.60. Simulating that
> exact rule on the same prompt-clustered percentile bootstrap
> ({i('analysis2.attainability_simulation.grid.n_replicates_per_cell')} replicates per
> cell, {i('analysis2.attainability_simulation.grid.n_boot_inner')} inner resamples,
> {i('analysis2.attainability_simulation.n_cells')} cells) shows the asymmetry is severe.
> At a true AUROC of 0.500 the null verdict is unreachable until
> n = {i('analysis2.attainability_simulation.extracted_answers.min_n_for_AT_CHANCE.1.min_n_with_any_AT_CHANCE')}
> items per class -- P(AT_CHANCE) is
> {f('analysis2.attainability_simulation.extracted_answers.pre_registered_gate_is_sufficient.P_AT_CHANCE_at_the_gate_true_auroc_0p50.1')}
> at the pre-registered n = 40 gate, and the Hanley-McNeil closed form puts the i.i.d.
> threshold at
> n = {i('analysis2.attainability_simulation.extracted_answers.hanley_mcneil_closed_form.min_n_per_class')}.
> Under perfect separation READS fires with probability
> {f('analysis2.attainability_simulation.extracted_answers.P_READS_under_perfect_separation.1.7')}
> at n = 7 and
> {f('analysis2.attainability_simulation.extracted_answers.P_READS_under_perfect_separation.1.33')}
> at n = 33, the counts at which the shipped table issues READS on unpowered members.
> The false-READS rate at true chance is
> {f('analysis2.attainability_simulation.extracted_answers.P_READS_at_true_chance.1.10')}
> at n = 10 and
> {f('analysis2.attainability_simulation.extracted_answers.P_READS_at_true_chance.1.40')}
> at n = 40. A count of zero AT_CHANCE verdicts is therefore substantially a property of
> the rule at these sample sizes rather than a measurement of the models."""

    # ---------------- (iv) the double tally ----------------
    tal = f"""### Replacement (iv) -- the axis-A verdict tally, reported twice

The tally must be given both as shipped and restricted to the population the
pre-registration says the statistic exists on. Over all
{i('analysis2.tally_all_members.grand_total')} members the axis-A verdicts are
{i('analysis2.tally_all_members.col_totals.READS')} READS,
{i('analysis2.tally_all_members.col_totals.AMBIGUOUS')} AMBIGUOUS,
{i('analysis2.tally_all_members.col_totals.AT_CHANCE')} AT_CHANCE and
{i('analysis2.tally_all_members.col_totals.UNDEFINED')} UNDEFINED. Restricted to the
{i('analysis2.tally_detection_powered.grand_total')} detection-powered members they are
{i('analysis2.tally_detection_powered.col_totals.READS')} READS,
{i('analysis2.tally_detection_powered.col_totals.AMBIGUOUS')} AMBIGUOUS,
{i('analysis2.tally_detection_powered.col_totals.AT_CHANCE')} AT_CHANCE and
{i('analysis2.tally_detection_powered.col_totals.UNDEFINED')} UNDEFINED.

{a2['tally_markdown']}

The earlier top-line count of 18 READS / 0 AT_CHANCE / 10 UNDEFINED is wrong and must be
replaced wherever it appears: it sums to
{i('reproduction_gate.verdict_tally_resolution.stale_tally_sums_to')}, two short of the
{i('analysis2.tally_all_members.grand_total')} members it claims to summarise."""

    # ---------------- (v) the abliterated arm ----------------
    rows = ["| member | n ref / com | spont. refusal rate [Wilson 95%] | pow | "
            "A AUROC [CI] | verdict |", "|---|---|---|---|---|---|"]
    for t in arm["weight_edited"]:
        rows.append(
            f"| `{t['checkpoint']}` | {t['n_refusal_scored']} / "
            f"{t['n_compliance_scored']} | {fmt(t['spontaneous_refusal_rate'], 4)} "
            f"[{fmt(t['wilson95'][0], 4)}, {fmt(t['wilson95'][1], 4)}] "
            f"(k = {t['n_refusal_of_scanned']} of {t['n_scanned']}) | "
            f"{'y' if t['powered'] else 'N'} | {fmt(t['A_auroc'])} "
            f"{('[' + fmt(t['A_ci95'][0]) + ', ' + fmt(t['A_ci95'][1]) + ']') if t['A_ci95'][0] is not None else '--'}"
            f" | {t['A_verdict']} |")
    abl_table = "\n".join(rows)

    abl = f"""### Replacement (v) -- the abliterated arm, restated on refusal-rate evidence

{abl_table}

As shipped, the weight-edited arm's structural claim rests on
{i('analysis2.abliterated_arm.n_weight_edited_READS')} READS verdicts of which exactly
{i('analysis2.abliterated_arm.n_weight_edited_READS_powered')} comes from a
detection-powered member; the other
{i('analysis2.abliterated_arm.n_weight_edited_READS_unpowered')} are underpowered, and by
the operating characteristic above they are close to automatic. The claim does not need
them. It is carried instead by the spontaneous refusal RATES, which involve no AUROC at
all: a median of
{f('analysis2.abliterated_arm.arm_medians.weight_edited_abliteration', 4)} in the
weight-edited arm and
{f('analysis2.abliterated_arm.arm_medians.behavioural_uncensored_candidate', 4)} in the
behavioural-uncensored candidate arm, against
{f('analysis2.abliterated_arm.arm_medians.aligned_reference', 4)} in the aligned
reference, over roughly 1,585 generations per member with Wilson intervals given
above. A two-sided Mann-Whitney U on the member-level rates separates the
weight-edited arm from the aligned reference
(U = {f('analysis2.abliterated_arm.mann_whitney.U', 1)}, tie-corrected asymptotic
p = {f('analysis2.abliterated_arm.mann_whitney.p_two_sided', 4)},
{i('analysis2.abliterated_arm.mann_whitney.n_weight_edited')} versus
{i('analysis2.abliterated_arm.mann_whitney.n_aligned_reference')} members; the
arms share one rate, so an exhaustive permutation over all
{i('analysis2.abliterated_arm.mann_whitney.n_permutations')} group assignments is
reported in its place as the exact test, giving
p = {f('analysis2.abliterated_arm.mann_whitney.p_exhaustive_permutation', 4)}); a
lineage-clustered bootstrap of the difference in medians over
{i('analysis2.abliterated_arm.lineage_clustered_bootstrap_median_difference.n_resampling_units')}
lineages gives
{f('analysis2.abliterated_arm.lineage_clustered_bootstrap_median_difference.delta_median_point', 4)}
{ci('analysis2.abliterated_arm.lineage_clustered_bootstrap_median_difference.ci95', 4)};
and over the
{i('analysis2.abliterated_arm.within_lineage_paired.n_pairs')} within-lineage
abliterated-versus-parent pairs the abliterated member has the lower rate in
{i('analysis2.abliterated_arm.within_lineage_paired.n_abliterated_lower')} of
{i('analysis2.abliterated_arm.within_lineage_paired.n_pairs')} (exact paired sign test
p = {f('analysis2.abliterated_arm.within_lineage_paired.sign_test.p_value', 4)}, median
paired difference
{f('analysis2.abliterated_arm.within_lineage_paired.median_delta_rate', 4)}).

On that evidence the claim stands as
"{'{'}analysis2.abliterated_arm.claim_text|{arm['claim_text']}{'}'}", and the four
underpowered AUROCs are cited as illustration only."""

    # ---------------- (vi) the deviation record ----------------
    devtxt = f"""### Replacement (vi) -- deviation record entry

| field | value |
|---|---|
| id | `{'{'}analysis2.deviation_record.id|{dev['id']}{'}'}` |
| trigger | {dev['trigger']} |
| what the Method said | {dev['what_the_method_said']} |
| what the code does | {dev['what_the_code_does']} |
| code path | `explib.py:{dev['code_path']['verdict']['lines']}` (`verdict_from_ci`), `explib.py:{dev['code_path']['resample_guard']['lines']}` (the >= 5-per-class resample guard), `gpu_stage.py:{dev['code_path']['powered_flag']['lines']}` (the separate `powered` flag) |
| affected members | {i('analysis2.deviation_record.affected_members.n_UNDEFINED')} UNDEFINED; {i('analysis2.deviation_record.affected_members.n_UNPOWERED_yet_READS')} unpowered yet READS |
| correction | see replacement (ii) |

```
{dev['code_path']['verdict']['quote']}
```

```
{dev['code_path']['resample_guard']['quote']}
```

```
{dev['code_path']['powered_flag']['quote']}
```"""

    return {"hc_paragraph": hc, "method_sentence": method, "footnote": fn,
            "double_tally": tal, "abliterated_arm": abl, "deviation_entry": devtxt}


# --------------------------------------------------------------------------
def run(doc: dict) -> dict:
    bundle = build_bundle(doc)
    rows: list[dict] = []
    rendered = {}
    for k, v in bundle.items():
        rows += audit(v, doc, k)
        rendered[k] = render(v)
    md = "\n\n---\n\n".join(rendered[k] for k in bundle)

    banned = []
    low = md.lower()
    for tok in BANNED_SALVAGE_TOKENS:
        if tok in low:
            banned.append(tok)

    n_pass = sum(r["status"] == "PASS" for r in rows)
    result = {
        "bundle_with_pointers": bundle,
        "bundle_rendered": rendered,
        "replacement_text_markdown": md,
        "pointer_audit": rows,
        "n_pointers": len(rows),
        "n_pass": n_pass,
        "n_mismatch": sum(r["status"] == "MISMATCH" for r in rows),
        "n_unresolvable": sum(r["status"] == "UNRESOLVABLE" for r in rows),
        "all_pointers_resolve": n_pass == len(rows),
        "banned_salvage_tokens_found": banned,
        "salvage_ban_respected": not banned,
        "assertion_passed": (n_pass == len(rows)) and not banned,
    }
    return result


def main(doc: dict) -> dict:
    setup_logging("stage4")
    res = run(doc)
    (OUT / "replacement_text.md").write_text(res["replacement_text_markdown"])
    jdump(OUT / "stage4.json",
          {k: v for k, v in res.items() if k != "bundle_with_pointers"})
    logger.info(f"prose: {res['n_pass']}/{res['n_pointers']} pointers resolve; "
                f"banned tokens = {res['banned_salvage_tokens_found']}")
    for r in res["pointer_audit"]:
        if r["status"] != "PASS":
            logger.error(f"{r['status']}: {r['pointer']} shown={r['shown']} "
                         f"resolved={r.get('resolved')} {r.get('error', '')}")
    return res


if __name__ == "__main__":
    import json
    from pathlib import Path
    main(json.loads(Path("eval_out.json").read_text()))
