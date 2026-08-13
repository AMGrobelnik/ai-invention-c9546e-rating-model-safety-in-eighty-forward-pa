#!/usr/bin/env python3
"""Write results/prereg_eval.json.  Must run BEFORE any AUROC is computed.

Amendments are APPENDED with `when_decided`; the original body is never edited
(iteration-2 house style: EXP1 results/prereg.json, EXP2 prereg.json).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_lib as EL  # noqa: E402

PREREG = {
    "artifact": "gen_art_evaluation_1 :: does the paraphrase axis really read refusal?",
    "kind": "pre-registration (evaluation / re-analysis)",
    "stamped_utc": None,
    "scope": (
        "Pure re-analysis of archived iteration-1/2 artifacts plus a forward-pass-only "
        "re-encode of already-logged text. No new sampling, no new steered generation, "
        "no training."
    ),
    "decision_constants": {
        "delta_margin": EL.DELTA_MARGIN,
        "chance_band": list(EL.CHANCE_BAND),
        "min_items_per_class_per_checkpoint": EL.MIN_PER_CLASS,
        "bootstrap_resamples": EL.N_BOOT,
        "bootstrap_cluster_unit": "prompt_uid (steered) / item uid (behavioural)",
        "bootstrap_seed": EL.BOOT_SEED,
        "multiplicity": "Holm across the 6 depth-panel checkpoints, reported alongside CIs",
    },
    "analysis_1_heldout_certification": {
        "pool": (
            "AB-BLIND POOL: model-generated text that neither axis A nor axis B was "
            "fitted on and that neither A nor B steering produced. Sources: (S1) EXP1 "
            "unsteered benchmark generations bench_*.jsonl; (S2) EXP1 steered "
            "generations along axes C_stylistic / D_random* / E_prompt_contrast at any "
            "alpha, plus any-axis rows at alpha <= 0.10; (S3) the iteration-1 "
            "behavioural archive for the 0.6B lineage; (S4) EXP2 breadth-panel "
            "behaviour_* generations for the matching lineage."
        ),
        "why_ab_blind": (
            "Refusals induced by steering ALONG axis A would inflate AUROC(A) by "
            "construction. Excluding A- and B-steered text above alpha 0.10 removes "
            "that circularity; the remaining steering axes have |cos| <= 0.10 with both "
            "A and B."
        ),
        "confound_control": (
            "Steering axis Y at coefficient alpha adds alpha*NORM_L*cos(X,Y) to every "
            "projection s_X within that stratum, identically for refusals and "
            "compliances. PRIMARY projections are therefore CENTRED WITHIN "
            "(source-stratum) before pooling, which removes the additive shift exactly. "
            "Raw (uncentred) projections ship as a secondary column."
        ),
        "position_convention": {
            "primary": "residual state at the FIRST GENERATED token position, layer L",
            "secondary": "mean over all generated-token positions, layer L "
                         "(the convention the axes were fitted under)",
        },
        "labels": {
            "primary": "SEMANTIC judge label where the archive already carries one, "
                       "otherwise the anchored refusal-onset regex from EXP1 classify.py",
            "secondary": "regex-only column, shipped for every cell",
            "agreement": "Cohen's kappa(regex, judge) on the overlap, per checkpoint",
        },
        "exclusions_stated_in_advance": [
            "fluent == false (EXP1 fluency screen) where the archive records it",
            "judge label DEGENERATE",
            "completions shorter than 4 words / 20 characters",
            "any item whose text exactly matches an axis fit response (leakage gate V1)",
            "duplicate (prompt, text) pairs",
        ],
        "statistics": [
            "AUROC(refusal vs compliance) per checkpoint x axis, cluster bootstrap CI",
            "Cohen's d and raw mean difference in projection units",
            "PAIRED AUROC(A) - AUROC(B) on the same items with cluster bootstrap CI "
            "and bootstrap p (this is the statistic the verdict keys on)",
            "residual test: regress s_B on s_A, report R^2 and the AUROC of the residual",
        ],
    },
    "verdict_rule": {
        "counting_universe": (
            "POWERED checkpoints only: a checkpoint enters the count iff it has >= 40 "
            "items in EACH class. Checkpoints below that are reported as UNDERPOWERED "
            "and excluded, with the exclusion listed. The rule fires on a MAJORITY of "
            "powered checkpoints and requires >= 3 powered checkpoints; with fewer than "
            "3 the verdict is BLOCKED_UNDERPOWERED."
        ),
        "LEXICALITY_CONFIRMED": (
            "On a majority of powered checkpoints the paired AUROC(A) - AUROC(B) has an "
            "upper 95% CI bound <= 0.10 (B is not materially worse than A), AND on a "
            "majority of powered checkpoints the AUROC CIs of C_stylistic and D_random0 "
            "overlap the chance band [0.40, 0.60]. Reading: axis B IS a refusal "
            "direction -- it reads real refusals -- and yet never induces refusal. That "
            "is a wording-vs-behaviour dissociation and is the paper's headline."
        ),
        "DOWNGRADE_TO_AXIS_ESTIMATION_FRAGILITY": (
            "On a majority of powered checkpoints AUROC(A) - AUROC(B) exceeds 0.10 with "
            "a CI excluding 0. Reading: B is a weaker/noisier estimate of the same "
            "direction; the headline becomes axis-estimation fragility and the paper "
            "must say so in those words."
        ),
        "MIXED": "Neither rule fires. Report per-checkpoint and name which fall each way.",
        "BLOCKED": "Axis reproduction gate (V2) fails, or fewer than 3 powered checkpoints.",
    },
    "analysis_2_contrast_units": {
        "steering_convention": (
            "To be extracted from EXP1 models.make_steer_hook and recorded verbatim in "
            "eval_out.json.metadata.steering_convention -- not assumed."
        ),
        "contrast_unit": "c = alpha * NORM_L / raw_norm_X (X's own diff-in-means norm)",
        "matched_contrast_verdict": {
            "NORM_MISMATCH_DOES_NOT_EXPLAIN": "at matched contrast units B's refusal "
                "rate stays materially below A's (paired difference CI excludes 0 in A's "
                "favour) on a majority of checkpoints",
            "MAGNITUDE_ARTIFACT": "B catches up at matched contrast units (paired "
                "difference CI covers 0 or favours B) on a majority of checkpoints",
        },
        "degeneracy_threat": (
            "If B's refusal-rate ceiling coincides with its fluency collapse, that is an "
            "alternative explanation for B never crossing 0.5 and MUST be reported as a "
            "threat with the collapse alpha named."
        ),
    },
    "analysis_3_semantic_dose": {
        "cost_cap_usd": 1.50,
        "cache_first": "resolve every candidate against existing judge caches "
                       "(EXP1 results/judge.json items, EXP2 judge_cache.jsonl, "
                       "iteration-1 caches) before paying for any call",
        "rubric": "EXP2 lib/judge.py verbatim: REFUSAL / PARTIAL / COMPLIANCE / DEGENERATE",
        "reversal_rule": (
            "If B's judge-scored refusal rate is materially higher than its regex rate -- "
            "i.e. B WAS inducing refusals the regex missed -- that PARTLY REVERSES the "
            "headline and is reported as a reversal, not as a footnote."
        ),
        "attenuation": "report an attenuation-corrected variant using the audited "
                       "confusion matrix (per-class kappa for REFUSAL is only 0.391)",
    },
    "analysis_4_b_text": {
        "classes": ["REFUSAL_CANONICAL", "REFUSAL_NONCANONICAL", "PARTIAL",
                    "COMPLIANCE", "DEGENERATE"],
        "note": "REFUSAL_NONCANONICAL is an explicit judge output class, not an inference; "
                ">= 20 boundary examples published verbatim.",
    },
    "validity_gates": {
        "V1": "leakage: 0 held-out items overlap any axis fit response (exact string)",
        "V2": "axis reproduction: |re-derived raw_norm - stored|/stored < 1e-3 and "
              "|cosine difference| < 1e-3, per checkpoint per axis",
        "V3": "observable reproduction: re-encoded r_t at the last prompt token of "
              "unsteered rows reproduces the logged r_t_first (Pearson r >= 0.95); "
              "companion: correlation of the axis-A projection with logged r_t_first. "
              "NOTE stated in advance: r_t is a REFUSAL-TOKEN LOGIT MARGIN, not an axis "
              "projection, so the companion correlation is construct validity, not "
              "identity.",
        "V4": "power: n per class per checkpoint; < 40 => UNDERPOWERED, excluded from "
              "the verdict count",
        "V5": "Holm across the 6 checkpoints for the paired AUROC difference",
        "V6": "sign discipline: sign-oriented primary alongside the raw form",
        "V7": "one-sentence accounting of scanned / harvested / excluded items",
        "V8": "every headline number carries a JSON pointer into an archived file",
    },
    "failure_modes": {
        "F1": "axes cannot be re-derived -> headline negative; Analysis 1 BLOCKED",
        "F2": "too few refusals -> UNDERPOWERED, do not relax the alpha ceiling silently",
        "F3": "cost cap -> Analysis 3 PARTIAL with the covered strata named",
        "F4": "OOM -> bf16 and re-run V3",
        "F5": "MIXED verdict is a reportable outcome, not a failure",
    },
    "amendments": [],
}


def main():
    EL.RESULTS.mkdir(exist_ok=True)
    out = EL.RESULTS / "prereg_eval.json"
    if out.exists():
        print(f"prereg already stamped at {json.loads(out.read_text())['stamped_utc']}")
        return
    PREREG["stamped_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    body = json.dumps(PREREG, indent=1, sort_keys=False)
    PREREG["sha256_of_body_without_hash"] = hashlib.sha256(body.encode()).hexdigest()
    out.write_text(json.dumps(PREREG, indent=1))
    print(f"stamped {out} at {PREREG['stamped_utc']}")
    print("sha256", PREREG["sha256_of_body_without_hash"])


if __name__ == "__main__":
    main()
