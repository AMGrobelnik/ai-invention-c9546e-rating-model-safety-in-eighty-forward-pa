# Naming the measurement pathologies, placing the headline

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** research  
**ID:** `art_9sXeYgowURMn`

## Layman Summary

Finds the original textbook sources for three statistical traps the study fell into, and checks exactly how much of its new safety-score result is genuinely new versus already published.

## Full Summary

Primary-full-text dossier for iteration 5. Deliverables: research_report.md (S0-S10) and research_out.json carrying the three ready-to-paste Discussion passages, a 7-row neighbour table, two branch-specific residual-novelty paragraphs, a 25-row query log, and a 16-entry BibTeX block. Every number is a verbatim quote with an anchor or is marked NOT FOUND / NOT OBTAINED / INHERITED.

THREE FRONT-MATTER RESOLUTIONS. (1) The 2506.24056 coverage conflict is NOT a version drift: 97.5-99.8% (fraction of toxic prompts where the ALIGNED gap exceeds the BASE gap) and 92.1% [89.4-94.2] (Qwen2.5-0.5B's position-1 decision census; Llama 98.8%, gemma 96.0%) are BOTH in v2 and measure different things. Cite 92-99% for position-1 validity, 97.5-99.8% for 'alignment widens the gap'. (2) The 0.464 blocker is RESOLVED from the shipped table, no placeholder needed: ourAMS rho = 0.358 (19 members) vs 0.821 (7 lineages), gap = 0.4636; the -0.929/-0.376 pair (diff 0.553) is a DIFFERENT quantity (oriented Delta, v2 carrier); median 0.238 / max 0.557 / 5-of-16 sign flips is a third. The drafter must name which pair of cells. (3) HURTADO VERDICT: H-G's novelty survives, but the plan's assumed distinction is WRONG - Hurtado's labels come from a behavioural oracle (Qwen3Guard), not a provenance tag, and his rho is explicitly 'one scalar per model'. The four surviving residuals are: attested reference required and spoofable; BINARY label vs graded refusal rate; 4 families vs 11; full weight download required. H-G may NOT claim 'first model-level cheap safety score validated against behaviour'.

LOGIT-GAP FULLY EXTRACTED (v2, full text). NO cross-model margin-vs-behaviour correlation exists - all 28 correlation matches inspected; every one is token-level, suffix-level, or cited from Bai et al. The abstract's co-variation is 'across suffix strategies' and is self-labelled an internal consistency check. Token lists recovered verbatim. CRITICAL CAVEAT NOT PREVIOUSLY RECORDED: their affirmative token is chosen PER PROMPT as the highest-logit one, making their gap an attack-relevant MINIMUM; a fixed-list max is a different estimand and must be declared.

CANONICAL SOURCES PINNED AND QUOTED. Leakage = Kapoor & Narayanan L3.3 Sampling bias in test distribution (exact label; L1.2 for the statistics half). Aggregation = Robinson 1950, with the sign flip read out of the paper: nativity x illiteracy is +.118 individual, -.526 (48 states), -.619 (9 divisions) - do NOT use the trio recalled in the plan. Openshaw CATMOG 38 supplies the scale/aggregation definitions and the devastating 'for a 6 region aggregation of the 99 Iowa counties the range of possible correlations is between -.99 and +.99'. Simpson 1951 verified (and Semantic Scholar's 'A. Simpson' is WRONG; the byline is E. H. Simpson). Small-sample = Schoenbrodt & Perugini 2013 with full Table 1: POS_crit at w=.10/80% is 252/238/212/181 for rho=.1/.2/.3/.4, so n=28 is 6.5-9x below stability - state this DELIBERATELY. NEW FIND: a 2018 CORRIGENDUM exists (DOI 10.1016/j.jrp.2018.02.010) and must be cited alongside.

CORRECTIONS TO OUR RECORDS. Mehta's LOQO figures are 0.43/0.87 in primary text, NOT 0.425/0.870 - quote two decimals. His 0.761 IS verified verbatim, as is the sharper control (AUROC 0.63 on a condition where the effect cannot exist). arXiv:2607.28685's -0.64@n=7 -> +0.02@n=18 is CONFIRMED plus a previously unrecorded and stronger clause: 'a quarter of random size-7 subsets show |rho| >= 0.5'. AMS verified at 14 configs / 4 families / Pearson -0.546 (p=0.043) - but its SPEARMAN is -0.423 at p=0.13, which is the directly comparable statistic and is not significant. NEW NEIGHBOUR: arXiv:2602.09434 (Xu & Sheng), refusal vectors over 76 offspring models at 100% base-family identification - outcome is MODEL IDENTITY, the clean provenance-vs-behaviour distinction the plan expected from Hurtado. arXiv:2603.27412's real title is 'The Geometry of Harmful Intent', not 'LatentBiopsy'.

SATURATION: the 13 scholarly-mode zeros are NOT credible (OpenAlex returned oncology and climate models); the claim is carried by arXiv-scoped search plus five harvested related-work sections. C1: no work validates such a score against judged behaviour at >=20 lineages or >=10 families; family-axis maximum anywhere is 4. C2: one direct hit only. TALLY for the COLLAPSES branch: 5 of 5 located model-level scores validate at <=4 families, 4 of 5 at <=14 checkpoints, and 0 of 5 use lineage-clustered resampling - lead with that last count.

NOT RESOLVED: iter-4 references numbered 11 and 23 (the numbered bibliography is in no readable workspace); Moreno-Torres full text (six routes failed, so NO quotation from it exists and it should be demoted to a citation without a quote).

## Dependencies

- `art_G5SIDXT53EAW` — extends
- `art_Qm_KL4GhZCnX` — extends
- `art_PeyWw78NIx9d` — extends

## Output Files

- `research_out.json`

## Demo Files

- **research_report.md** — Research report markdown (auto-generated from artifact)

---
*Generated by AI Inventor Pipeline*
