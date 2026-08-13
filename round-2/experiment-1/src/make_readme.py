#!/usr/bin/env python3
"""Generate README.md from method_out.json.

Every number in the README is read out of the artifact, so the prose cannot
drift from the results.
"""

from __future__ import annotations

import json
from pathlib import Path

W = Path(__file__).resolve().parent
ORDER = ["base_0p6", "instruct_0p6", "abliterated_0p6",
         "base_1p7", "instruct_1p7", "abliterated_1p7"]
AXES = ["A_canned", "B_paraphrase", "C_stylistic", "E_prompt_contrast", "D_random0"]
AXIS_LABEL = {"A_canned": "A canned", "B_paraphrase": "B paraphrase-disjoint",
              "C_stylistic": "C stylistic (non-safety)",
              "E_prompt_contrast": "E prompt-contrast",
              "D_random0": "D random"}


def fmt(v, nd=3):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def main() -> None:
    A = json.loads((W / "method_out.json").read_text())["metadata"]
    models = {m["key"]: m for m in A["models"]}
    present = [k for k in ORDER if k in models]
    a50 = {(r["model"], r["axis"], r["scorer"]): r for r in A["alpha_50"]}
    t0 = A.get("tier0", {}).get("checks", {})

    L = []
    ap = L.append
    ap("# alpha_50 — how much push does refusal cost?\n")
    ap("A powered, de-confounded re-measurement of **alpha_50**: the steering "
       "coefficient (in units of `NORM_L`) at which a *fresh* constant-alpha generation "
       "on a **benign** prompt refuses half the time.\n")
    ap(f"- **{A['audit_cost']['n_prompts']} prompts x {A['audit_cost']['n_seeds']} seeds** "
       f"per alpha (iteration 1 used 5 prompts, greedy, no CI at all)\n"
       f"- **{len(present)} checkpoints** across two Qwen3 lineages, "
       f"**{len(AXES)} steering axes**, logistic dose-response MLE, prompt-cluster "
       f"bootstrap CIs\n"
       f"- **{A['audit_cost']['total_generations']:,} steered generations**, "
       f"LLM API spend **${A['llm_api_cost_usd']:.4f}** of a $1.50 cap\n")

    ap("## Headline\n")
    for f in A["headline_findings"]:
        ap(f"* {f}")
    ap("")

    ap("## alpha_50 by model and axis (regex scorer)\n")
    ap("| checkpoint | " + " | ".join(AXIS_LABEL[a] for a in AXES) + " |")
    ap("|---" * (len(AXES) + 1) + "|")
    for k in present:
        cells = []
        for ax in AXES:
            r = a50.get((k, ax, "regex"))
            if r is None:
                cells.append("—")
            elif r["a50"] is None:
                cells.append(f"undef (max {fmt(r['max_rate'], 2)})")
            else:
                cells.append(f"**{fmt(r['a50'])}** [{fmt(r['ci_lo'])}, {fmt(r['ci_hi'])}]")
        ap(f"| `{models[k]['repo']}` | " + " | ".join(cells) + " |")
    ap("\n*undef = the axis never reaches a 50% refusal rate below the outer edge of "
       "measurement (alpha = 2.0, where the fluency screen fails). It does NOT mean "
       "infinite.*\n")

    ap("## Model card\n")
    ap("| key | repo | revision | layers | site L | rel. depth | NORM_L |")
    ap("|---|---|---|---|---|---|---|")
    for k in present:
        m = models[k]
        ap(f"| {k} | `{m['repo']}` | `{str(m['revision_sha'])[:12]}` | {m['n_layers']} | "
           f"{m['L']} | {fmt(m['relative_depth'], 2)} | {fmt(m['NORM_L'], 2)} |")
    ap("")

    ap("## Pre-registered controls\n")
    c = A["controls"]
    pc = c["paraphrase_disjoint"]
    ap(f"**(a) token-disjoint paraphrase axis — `{pc['verdict']}`.** "
       f"{pc['n_inside_CI']}/{pc['n_models']} checkpoints keep alpha_50 inside the "
       f"canned-axis CI; on {pc['n_paraphrase_unreachable']}/{pc['n_models']} the "
       f"disjoint axis never reaches 50% at all. Ordering survives: "
       f"{fmt(pc['ordering_survives'])}.\n")
    sj = c["semantic_judge"]
    ap(f"**(b) semantic judge — `{sj['verdict']}`.** "
       + (f"kappa(regex, judge) = {sj.get('kappa_per_model')}, "
          f"{sj.get('n_items', 0)} items."
          if sj["verdict"] != "NOT_RUN" else f"reason: {sj.get('reason')}") + "\n")
    st = c["stylistic_axis"]
    ap(f"**(c) norm-matched non-safety axis — `{st['verdict']}`.** max steered refusal "
       f"rate {st['max_refusal_rate_per_model']}.\n")
    rd = c["random_axis"]
    ap(f"**(d) matched random direction — `{rd['verdict']}`.** max steered refusal rate "
       f"{rd['max_refusal_rate_per_model']}.\n")
    pcx = c.get("prompt_contrast_axis")
    if pcx:
        ap(f"**(e) harmful-vs-benign PROMPT axis (iteration-1 AMENDMENT-7 comparator) — "
           f"`{pcx['verdict']}`.** max steered refusal rate "
           f"{pcx['max_refusal_rate_per_model']}.\n")

    ap("## H1b: the price difference\n")
    ap("| scale | contrast | delta | 95% CI | verdict |")
    ap("|---|---|---|---|---|")
    for p in A["paired_differences"]:
        ap(f"| {p['scale']} | {p['contrast']} | {fmt(p.get('delta'), 4)} | "
           f"[{fmt(p.get('ci_lo'), 4)}, {fmt(p.get('ci_hi'), 4)}] | "
           f"{p['claim_b_verdict']} |")
    ap("")

    ap("## Gates and estimator checks (tier 0)\n")
    ap("| check | result |")
    ap("|---|---|")
    rows = [
        ("iteration-1 replication gate (greedy, 5 prompts)",
         f"a50 = {fmt(t0.get('B5_iter1_replication_gate', {}).get('a50'))} "
         f"vs iteration-1 0.475 -> "
         f"{fmt(t0.get('B5_iter1_replication_gate', {}).get('passed'))}"),
        ("NORM_L reproduction (instruct 0.6B)",
         f"{fmt(t0.get('B4_norm_L', {}).get('measured'), 2)} vs 21.21"),
        ("hook fires / alpha=0 identity / determinism",
         f"{fmt(t0.get('B1_hook_fires', {}).get('passed'))} / "
         f"{fmt(t0.get('B2_alpha0_identity', {}).get('passed'))} / "
         f"{fmt(t0.get('B3_determinism', {}).get('passed'))}"),
        ("estimator recovery at the real geometry",
         f"median a50 = "
         f"{fmt(t0.get('D1_synthetic_recovery', {}).get('median_a50'))} (truth 0.5), "
         f"CI coverage "
         f"{fmt(t0.get('D1_synthetic_recovery', {}).get('ci_coverage'))}"),
        ("minimum detectable difference @80% power",
         f"{fmt(t0.get('D2_power', {}).get('mde_80pct'))} vs the iteration-1 observed "
         f"gap 0.075"),
        ("paraphrase disjointness assertion",
         f"{t0.get('C1_disjointness', {}).get('n_pairs_kept')}/"
         f"{t0.get('C1_disjointness', {}).get('n_pairs_kept', 0) + t0.get('C1_disjointness', {}).get('n_pairs_discarded', 0)}"
         f" candidate pairs kept"),
    ]
    for a, b in rows:
        ap(f"| {a} | {b} |")
    ap("")

    ev = A.get("external_validity", {})
    if ev.get("per_model"):
        ap("## External validity: the benchmark alpha_50 claims to replace\n")
        ap("| checkpoint | harmful refusal (screen / judge) | attacked (screen / judge) "
           "| over-refusal safe (screen / judge) | alpha_50 | reachable |")
        ap("|---|---|---|---|---|---|")
        for e in ev["per_model"]:
            ap(f"| {e['model']} | {fmt(e['harmful_refusal_rate'], 2)} / "
               f"{fmt(e.get('judge_harmful_refusal_rate'), 2)} | "
               f"{fmt(e['attacked_refusal_rate'], 2)} / "
               f"{fmt(e.get('judge_attacked_refusal_rate'), 2)} | "
               f"{fmt(e['over_refusal_rate_safe'], 2)} / "
               f"{fmt(e.get('judge_over_refusal_rate_safe'), 2)} | "
               f"{fmt(e['alpha_50'])} | {fmt(e['reachable'])} |")
        for kk, vv in ev.items():
            if kk.startswith("spearman"):
                ap(f"\n* {kk}: rho = {fmt(vv['rho'])}, p = {fmt(vv['p'])}, n = {vv['n']}")
        ap("")

    ap("## Composite two-stage score\n")
    ap("The two discriminations are reported SEPARATELY and never as one number:\n")
    ap("| checkpoint | stage 1: reachable | max steered rate | stage 2: alpha_50 | score = 1/alpha_50 |")
    ap("|---|---|---|---|---|")
    for c2 in A["composite"]:
        ap(f"| {c2['model']} | {fmt(c2['stage1_reachable'])} | "
           f"{fmt(c2['max_refusal_rate'], 2)} | {fmt(c2['stage2_alpha_50'])} | "
           f"{fmt(c2['score'])} |")
    ac = A["audit_cost"]
    ap(f"\nAudit cost: **{fmt(ac.get('gpu_minutes_0p6'), 1)} GPU-min** per 0.6B "
       f"checkpoint, **{fmt(ac.get('gpu_minutes_1p7'), 1)} GPU-min** per 1.7B "
       f"checkpoint, on one RTX 4000 Ada — no benchmark run.\n")

    ap("## Files\n")
    ap("| file | role |")
    ap("|---|---|")
    for f, r in [
        ("`method.py`", "driver: tiers 0-4 (gates -> sweeps -> judge -> assembly)"),
        ("`prereg_spec.py`", "the pre-registration and the deviations table, frozen before any model loads"),
        ("`sweep.py`", "the alpha_50 primitive: batched fresh constant-alpha generations"),
        ("`axes.py`", "the four steering axes and the paraphrase disjointness assertion"),
        ("`fitting.py`", "logistic MLE (IRLS), 4-parameter fit, cluster/paired bootstrap, power"),
        ("`bench.py`", "unsteered behavioural benchmark with correct left-padding"),
        ("`judge.py`", "OpenRouter semantic judge with cache and hard cost cap"),
        ("`models.py`, `direction.py`, `classify.py`, `ramp.py`, `stats.py`, `prompts.py`",
         "**reused VERBATIM** from iteration 1 (sha256 in `method_out.json.reuse_manifest`)"),
        ("`test_bench.py`, `test_judge.py`", "padding-correctness check and the 12-item judge probe"),
        ("`make_readme.py`", "generates this file from `method_out.json`"),
        ("`method_out.json`", "the report (schema `exp_gen_sol_out`; full analysis under `metadata`)"),
        ("`results/`", "pre-registration, per-(model, axis) sweep checkpoints, tier-0 gates, judge output"),
        ("`gens/`", "every generation with its alpha, fluency flag and refusal label"),
    ]:
        ap(f"| {f} | {r} |")

    ap("\n## Reproducing\n")
    ap("```bash\nuv venv .venv --python=3.12\n"
       "uv pip install --python=.venv/bin/python torch==2.6.0 "
       "--index-url https://download.pytorch.org/whl/cu124\n"
       "uv pip install --python=.venv/bin/python \"transformers>=4.51\" accelerate numpy "
       "scipy statsmodels loguru psutil requests huggingface_hub\n\n"
       ".venv/bin/python method.py --tier 0     # gates + estimator certification\n"
       ".venv/bin/python method.py --tier 9     # all six checkpoints, judge, assembly\n"
       "```\n")

    ap("## Limitations\n")
    for lim in A["limitations"]:
        ap(f"* {lim}")
    ap("")

    ap("## Pre-registration deviations\n")
    ap("| id | change | why | decided |")
    ap("|---|---|---|---|")
    for d in A["prereg_deviations"]:
        ap(f"| {d['id']} | {d['what_changed']} | {d['why']} | {d['when_decided']} |")

    text = "\n".join(L) + "\n"
    (W / "README.md").write_text(text)
    print(f"wrote README.md ({len(text)} chars)")


if __name__ == "__main__":
    main()
