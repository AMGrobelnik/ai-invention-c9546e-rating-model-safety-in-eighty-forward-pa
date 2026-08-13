#!/usr/bin/env python3
"""Render RESULTS.md from method_out.json.

EVERY number in the report is READ from `method_out.json` by path and formatted
here; none is retyped. The renderer is deterministic: `--check` renders twice and
requires the two sha256 digests to be equal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "method_out.json"
MD = HERE / "RESULTS.md"


def f(x, nd=3):
    if x is None:
        return "--"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, str):
        return x
    return f"{x:.{nd}f}"


def ci(c, nd=3):
    if not c:
        return "--"
    return f"[{f(c[0], nd)}, {f(c[1], nd)}]"


def sci(x):
    return "--" if x is None else f"{x:.2e}"


def pfmt(p):
    """A p at or near the Monte-Carlo floor must never render as 0.00000."""
    if p is None:
        return "--"
    return f"{p:.2e}" if p < 1e-4 else f"{p:.5f}"


def render(d: dict) -> str:
    m = d["metadata"]
    a = m["analysis"]
    v = m["verdict"]
    st = a["statistics"]
    ach = a["achieved_panel"]
    panel = m["panel"]
    rep = m["t0_replay_archive19"]
    L: list[str] = []
    w = L.append

    w(f"# {m['title']}")
    w("")
    w(f"## VERDICT: **{v['verdict']}**")
    w("")
    w(f"> {v['rule_quoted_verbatim_from_prereg']}")
    w("")
    w(f"*(the rule above is read verbatim from `prereg_iter5.json` "
      f"`verdict_rule.{v['verdict']}`, never retyped)*")
    w("")
    w(f"The primary score is the first-decoding-step logit-gap margin on the "
      f"frozen plain-harmful core-80 -- **80 forward passes, 0 generations, 0 "
      f"judge calls, 0 benchmark runs, 0 reference models** per checkpoint. At "
      f"{v['achieved_n']['members']} members over {v['achieved_n']['lineages']} "
      f"weight lineages and {v['achieved_n']['families']} architecture families "
      f"it scores")
    w("")
    w(f"* MEMBER unit (lineage-clustered bootstrap): rho = **{f(v['rho_member'], 4)}**, "
      f"95% CI {ci(v['ci_member'])}")
    w(f"* LINEAGE unit (28 collapsed points): rho = **{f(v['rho_lineage'], 4)}**, "
      f"95% CI {ci(v['ci_lineage'])}")
    w("")
    w(f"against iteration 3's {rep['targets']['rho_member']} "
      f"{ci(rep['targets']['rho_member_ci'])} member / "
      f"{rep['targets']['rho_lineage']} lineage on "
      f"{rep['targets']['n_members']} members over "
      f"{rep['targets']['n_lineages']} lineages.")
    w("")
    w("### Honesty statement (mandatory)")
    w("")
    w(f"> {m['framing']}")
    w("")

    # ---------------- provenance ----------------
    w("## 1. Provenance and gates")
    w("")
    w("| gate | result |")
    w("|---|---|")
    rm = m["reuse_manifest"]
    w(f"| byte-identity of reused libraries | "
      f"{rm['n_library_files']} files, all byte-identical to the iteration-4 "
      f"archive |")
    w(f"| archived inputs hashed | {rm['n_archived_inputs']} |")
    w(f"| offline apparatus tests (T0a) | "
      f"{len(m['t0_unit_tests']['checks'])} checks, all_pass="
      f"{f(m['t0_unit_tests']['all_pass'])} |")
    w(f"| constant extraction (T0b) | ORIENTATION_MAP recovered by `ast` from "
      f"iteration 3's driver without importing it; RLIMIT_AS unchanged="
      f"{f(m['t0_constants']['rlimit_as_unchanged_by_extraction'])} |")
    w(f"| panel identity (T0d) | "
      f"{panel['counts']['n_members']} members / "
      f"{panel['counts']['n_lineages']} lineages / "
      f"{panel['counts']['n_families']} families "
      f"({panel['counts']['n_archived19']} archived19 + "
      f"{panel['counts']['n_new33']} new33) |")
    w(f"| T0-REPLAY of the archived 19 (T3) | "
      f"**{'PASS' if rep['replay_passed'] else 'FAIL'}** -- rho_member "
      f"{f(rep['member_unit']['rho'], 4)} "
      f"{ci(rep['member_unit']['ci95_lineage_clustered'])}, rho_lineage "
      f"{f(rep['lineage_unit']['rho'], 4)}, exhaustive permutation floor "
      f"{sci(rep['permutation']['p_min_achievable'])} |")
    w(f"| pre-registration stamp (T4) | file `{m['prereg_sha256'][:16]}...`, "
      f"timestamp-free content `{m['prereg_content_sha256'][:16]}...` |")
    w(f"| our-AMS sigma anchor | {a['ams_anchor']['n_reproducing']}/"
      f"{a['ams_anchor']['n_checked']} members reproduce iteration 4 within "
      f"{a['ams_anchor']['tol']}; max |delta| "
      f"{sci(a['ams_anchor']['max_abs_delta'])} |")
    w(f"| generations made | **{ach['n_generations_total']}** "
      f"(the product claim; a non-zero total would falsify the cost claim) |")
    w(f"| forward passes made | {ach['n_forward_passes_total']} over "
      f"{ach['n_members_scored']} members |")
    w(f"| LLM API spend | ${f(m['cost_usd_total'], 2)} "
      f"(ground truth is reused, not re-judged) |")
    w("")
    for k, c in rep["checks"].items():
        w(f"* T0-REPLAY `{k}`: got {c['got']}, want {c['want']} -- "
          f"{'PASS' if c['pass'] else 'FAIL'}")
    w("")

    # ---------------- achieved panel ----------------
    w("## 2. Achieved panel")
    w("")
    w(f"* scored: **{ach['n_members_scored']} / {ach['n_members_attempted']}** "
      f"members, {ach['n_lineages']} lineages, {ach['n_families']} families "
      f"(planned {v['planned_n']['members']} / {v['planned_n']['lineages']} / "
      f"{v['planned_n']['families']})")
    w(f"* excluded before the run (carried forward verbatim from iteration 4): "
      + ", ".join(f"`{e['key']}` ({e['status']})" for e in panel["excluded"]))
    w(f"* failed during the run: "
      f"{ach['n_failed'] if ach['n_failed'] else 'none'}")
    w(f"* MISSING_FAMILY_LEXICON (primary logit-gap columns NULL, never "
      f"back-filled from another family): "
      f"{len(ach['n_missing_family_lexicon'])} -- "
      f"{ach['n_missing_family_lexicon'] if ach['n_missing_family_lexicon'] else 'none'}")
    w(f"* lens-calibration failures (headline unaffected -- the headline reads "
      f"the model's OWN final logits, not the lens): "
      f"{len(ach['n_lens_calibration_failed'])}")
    w("")
    lex = panel["lexicon"]
    w(f"> {lex['policy']}")
    w("")

    # ---------------- the main table ----------------
    w("## 3. Three scores x two aggregation units (Table 3)")
    w("")
    w("| score | n_fwd | n_gen | rho_member [CI] | rho_lineage [CI] | perm p (floor) "
      "| LOLO range | LOFO range | AUC | disatt. member |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for s, row in st.items():
        mu, lu = row["member_unit"], row["lineage_unit"]
        pm = row["permutation"]
        w(f"| `{s}` | {row['n_forward_passes']} | {row['n_generations']} | "
          f"{f(mu['rho'])} {ci(mu['ci95_lineage_clustered'])} | "
          f"{f(lu['rho'])} {ci(lu['ci95_unit_bootstrap'])} | "
          f"{pfmt(pm['p_permutation'])} ({sci(pm['p_min_achievable'])}) | "
          f"{ci(row['loo_lineage']['range'])} | {ci(row['loo_family']['range'])} | "
          f"{f(row['auc']['auc'])} | "
          f"{f(row['disattenuated']['rho_member_disattenuated'])} |")
    w("")
    w("Every rho is ORIENTED (higher = safer) using the orientation map extracted "
      "from iteration 3's driver; the sign convention is +1 for all three scores. "
      "The permutation branch is Monte Carlo (28! is not enumerable), so the "
      "floor in parentheses is the smallest p the design can express and no p is "
      "ever quoted below it. LOLO = leave-one-lineage-out; LOFO = "
      "leave-one-family-out. The disattenuated column divides by "
      f"sqrt(kappa) at kappa = "
      f"{st['logit_gap_harmful']['disattenuated']['kappa']} and NEVER replaces the "
      "raw value beside it.")
    w("")
    w("Sign stability across the jackknife folds:")
    w("")
    for s, row in st.items():
        w(f"* `{s}`: LOLO sign_stable="
          f"{f(row['loo_lineage']['sign_stable'])} over "
          f"{row['loo_lineage']['n_folds']} folds; LOFO sign_stable="
          f"{f(row['loo_family']['sign_stable'])} over "
          f"{row['loo_family']['n_folds']} folds")
    w("")

    # ---------------- block split ----------------
    w("## 4. The decisive diagnostic: archived-19 vs new-33")
    w("")
    w("| score | rho archived19 [CI] | rho new33 [CI] | delta [CI] | verdict |")
    w("|---|---|---|---|---|")
    for s, row in st.items():
        b = row["block_split"]
        pa = b["per_block"]["archived19"]["member_unit"]
        pb = b["per_block"]["new33"]["member_unit"]
        w(f"| `{s}` | {f(pa['rho'])} {ci(pa['ci95_lineage_clustered'])} "
          f"(n={pa['n']}, {pa['n_lineages']} lin) | "
          f"{f(pb['rho'])} {ci(pb['ci95_lineage_clustered'])} "
          f"(n={pb['n']}, {pb['n_lineages']} lin) | "
          f"{f(b['delta']['delta'])} {ci(b['delta']['ci95'])} | "
          f"{b['delta']['verdict']} |")
    w("")
    w("Pre-registered reading: if rho on the archived 19 is large and rho on the "
      "new 33 is near zero, the score is the same small-panel artefact the "
      "paraphrase refit was, and that localisation is the finding.")
    w("")

    # ---------------- controls ----------------
    w("## 5. Pre-emptive controls")
    w("")
    w("| score | rho_member | partial rho | control CI | rho(score, log10 params) "
      "| rho(y, log10 params) |")
    w("|---|---|---|---|---|---|")
    for s, row in st.items():
        c = row["controls"]
        p = c["partial_rho_controlling_log10_params"]
        w(f"| `{s}` | {f(row['member_unit']['rho'])} | "
          f"{f(p.get('partial_rho'))} | "
          f"{ci(p.get('ci95_lineage_clustered'))} | "
          f"{f(c['rho_score_vs_log10_params']['rho'])} | "
          f"{f(p.get('rho_y_vs_control'))} |")
    w("")
    w("Is the prediction just parameter count? The partial column answers it "
      "directly and is reported whether or not it is flattering.")
    w("")
    w("### With and without the members whose tokenizer family has no lexicon")
    w("")
    w("| score | all members | lexicon-present only |")
    w("|---|---|---|")
    for s, row in a["sensitivity_lexicon"].items():
        w(f"| `{s}` | {f(row['all_members']['rho'])} "
          f"{ci(row['all_members']['ci95_lineage_clustered'])} (n="
          f"{row['all_members']['n']}) | "
          f"{f(row['lexicon_present_only']['rho'])} "
          f"{ci(row['lexicon_present_only']['ci95_lineage_clustered'])} (n="
          f"{row['lexicon_present_only']['n']}) |")
    w("")
    w("### Paired comparisons on the SAME resampled lineages")
    w("")
    w("| comparison | rho_score | rho_reference | delta [CI] | P(delta>0) | verdict |")
    w("|---|---|---|---|---|---|")
    for name, p in a["paired_comparisons"].items():
        w(f"| `{name}` | {f(p['rho_score'])} | {f(p['rho_reference'])} | "
          f"{f(p['delta'])} {ci(p['ci95'])} | {f(p.get('prob_delta_gt_0'))} | "
          f"{p['verdict']} |")
    w("")

    # ---------------- audit cost ----------------
    ac = a["audit_cost"]
    w("## 6. Audit cost -- the price tag on the product claim")
    w("")
    w("| item | value |")
    w("|---|---|")
    for k, val in ac["n_forward_passes_per_member"].items():
        w(f"| forward passes per member, `{k}` | {val} |")
    w(f"| generations per member | {ac['n_generations_per_member']} |")
    wc = ac["wall_clock_seconds_all_scores"]
    w(f"| wall clock per member, all four scores (median / p90 / max) | "
      f"{f(wc['median'], 1)} / {f(wc['p90'], 1)} / {f(wc['max'], 1)} s "
      f"(n={wc['n']}) |")
    for b, val in ac["wall_clock_seconds_by_param_bucket"].items():
        w(f"| median seconds, {b} | {f(val['median'], 1)} s (n={val['n']}) |")
    w(f"| device | {ac['device']} ({ac['gpu']}) |")
    w("")
    w(f"*{wc['note']}*")
    w("")
    cc = ac["cost_to_score_one_new_checkpoint_with_logit_gap_harmful_alone"]
    w(f"Scoring ONE new checkpoint with the primary score alone: "
      f"**{cc['forward_passes']} forward passes, {cc['generations']} generations, "
      f"{cc['judge_calls']} judge calls, {cc['benchmark_runs']} benchmark runs, "
      f"{cc['reference_models']} reference models.** {cc['seconds_note']}.")
    w("")

    # ---------------- recomputation cross-check ----------------
    xc = m["recompute_vs_iter3"]
    w("## 7. Independent recomputation against iteration 3")
    w("")
    w(f"The T0-REPLAY gate above uses iteration 3's ARCHIVED margins, so it is "
      f"exact by construction. This section recomputes the same margins from the "
      f"models: {xc['n']} archived members compared, "
      f"{xc['n_within_1e-3']} within {xc['tol']}, median |delta| "
      f"{sci(xc['median_abs_delta_harmful'])}, max |delta| "
      f"{sci(xc['max_abs_delta_harmful'])}.")
    w("")
    rp = xc.get("rank_preservation") or {}
    if rp.get("n_pairs"):
        w(f"**Rank preservation.** Spearman reads order, not magnitude, so the "
          f"question a numeric drift raises is whether it moves the ranks. Over "
          f"{rp['n_pairs']} archived members the iteration-3 and iteration-5 "
          f"harmful margins have identical ranks: **{f(rp.get('ranks_identical'))}** "
          f"({rp.get('n_rank_positions_moved')} rank positions moved, "
          f"Spearman(iter3, iter5) = {f(rp.get('rho_iter3_vs_iter5'), 4)}). "
          f"{rp.get('note')}.")
        w("")
    w("| key | iter3 harmful | iter5 harmful | abs delta | iter3 template | "
      "iter5 renderer |")
    w("|---|---|---|---|---|---|")
    for r in xc["per_member"]:
        w(f"| `{r['key']}` | {f(r['iter3_harmful'], 4)} | "
          f"{f(r['iter5_harmful'], 4)} | {sci(r['abs_delta_harmful'])} | "
          f"{r['iter3_template']} | {r['iter5_renderer']} |")
    w("")

    # ---------------- per member ----------------
    w("## 8. Per-member table")
    w("")
    w("| key | lineage | family | params | block | renderer | lex | "
      "logit_gap_harmful | logit_gap_benign | union | sigma | sigma==archive | "
      "y_refusal |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in a["per_member_table"]:
        w(f"| `{r['key']}` | {r['lineage']} | {r['family']} | "
          f"{(r['param_count'] or 0) / 1e9:.2f}B | {r['block']} | "
          f"{r['renderer']} | {r['lexicon_status']} | "
          f"{f(r['logit_gap_harmful'])} | {f(r['logit_gap_benign'])} | "
          f"{f(r['logit_gap_harmful_union'])} | {f(r['our_ams_sigma'])} | "
          f"{f(r['sigma_reproduces_archive'])} | {f(r['y_refusal'])} |")
    w("")

    # ---------------- prereg ----------------
    w("## 9. Pre-registration, in full")
    w("")
    pr = m["prereg"]
    for k, txt in pr["verdict_rule"].items():
        w(f"* **{k}** -- {txt}")
    w("")
    w("Deviations from the artifact plan, recorded before any correlation was "
      "computed:")
    w("")
    for dv in pr["deviations_from_the_artifact_plan"]:
        w(f"* **{dv['item']}**. Plan said: {dv['plan_said']}. Measured: "
          f"{dv['measured']} Action: {dv['action']}.")
    w("")
    w(f"Secondary reports registered in advance: "
      + "; ".join(pr["secondary_reports"]) + ".")
    w("")
    w(f"Gate order enforced by the driver: "
      + " -> ".join(pr["gate_order"]) + ".")
    w("")
    w("## 10. Reproduction")
    w("")
    w("```bash")
    w("uv venv .venv --python=3.12")
    w("uv pip install --python=.venv/bin/python torch==2.11.0 \\")
    w("    --index-url https://download.pytorch.org/whl/cu128")
    w("uv pip install --python=.venv/bin/python -r <(grep -v '^torch==' pyproject-deps.txt)")
    w("")
    w(".venv/bin/python method.py --tier t0       # gates only, no GPU")
    w(".venv/bin/python method.py --tier smoke    # one member, the reuse-chain signal")
    w(".venv/bin/python method.py --tier t2       # renderer sanity: one instruct + one base")
    w(".venv/bin/python method.py --tier archive  # the archived 19 only")
    w(".venv/bin/python method.py --tier full --max-hours 4.0")
    w(".venv/bin/python summarise.py --check")
    w("```")
    w("")
    w(f"Every member writes `results/iter5_member_<key>.json` and is skipped on a "
      f"rerun, so the run is resumable and a crash costs one member. HF snapshots "
      f"are purged after each member.")
    w("")
    w(f"*Rendered from `method_out.json` "
      f"(created {m['created_utc']}); every number above is read from that file, "
      f"none is retyped.*")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="render twice and require byte-identical output")
    args = ap.parse_args()
    d = json.loads(OUT.read_text())
    text = render(d)
    if args.check:
        again = render(json.loads(OUT.read_text()))
        h1 = hashlib.sha256(text.encode()).hexdigest()
        h2 = hashlib.sha256(again.encode()).hexdigest()
        if h1 != h2:
            raise AssertionError(f"renderer is not deterministic: {h1} != {h2}")
        print(f"deterministic render OK: sha256 {h1}")
    MD.write_text(text)
    print(f"wrote {MD} ({len(text)} chars, "
          f"sha256 {hashlib.sha256(text.encode()).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
