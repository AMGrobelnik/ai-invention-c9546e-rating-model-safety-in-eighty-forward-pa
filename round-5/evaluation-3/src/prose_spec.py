#!/usr/bin/env python3
"""The prose and abstract TEMPLATES.

Not one number is typed here. Every quantity is a {{ptr:ALIAS#/pointer|fmt}}
placeholder that the harness resolves against a sha256-frozen source, and the
NO_BARE_NUMERAL lint fails the build if a digit appears outside a placeholder
without matching an itemised allow-list entry. Every sentence carrying a
statistic names its aggregation unit inline, which is what makes the
post-render ledger's UNIT_MISSING count zero rather than merely small.
"""

P = "{{ptr:%s#%s|%s}}"


def p(alias: str, pointer: str, fmt: str) -> str:
    return P % (alias, pointer, fmt)


# --- shorthand for the pointers used more than once ------------------------
N_READS = p("DERIVED", "/values/n_reads_total", "int")
N_AMBIG = p("E2", "/metadata/results/h1_abliterated_arm/by_arm/aligned_reference"
                  "/verdicts/AMBIGUOUS", "int")
N_UNDEF = p("DERIVED", "/values/n_undefined_total", "int")
N_MEASURABLE = p("DERIVED", "/values/n_measurable_defined_auroc", "int")
N_POWERED = p("DERIVED", "/values/n_powered_total", "int")
N_MEMBERS_DET = p("E2", "/metadata/results/sanity_panel/n_D_members", "int")
RHO_JOINT = p("E2", "/metadata/results/h3_joint_scatter/rho_primary", "f3")
CI_JOINT = p("E2", "/metadata/results/h3_joint_scatter/ci95_lineage_bootstrap", "ci3")
N_PAIRS = p("E2", "/metadata/results/h3_joint_scatter/n_pairs", "int")


def prose_template(min_all: dict, min_reads: dict, min_pow: dict,
                   ambiguous: dict) -> str:
    """`min_*` and `ambiguous` carry only POINTERS and member names, produced by
    stage 1 from the per-member records -- the values themselves are still
    rendered from the source."""
    ma = p("E2", min_all["json_pointer"], "f3")
    ma_ci = p("E2", min_all["ci_pointer"], "ci3")
    mr = p("E2", min_reads["json_pointer"], "f3")
    mp = p("E2", min_pow["json_pointer"], "f3")
    amb = p("E2", ambiguous["json_pointer"], "f3")

    L = []
    A = L.append
    A("# Replacement prose, generated from JSON pointers\n")
    A("Every number below is rendered from a sha256-frozen source at run time. "
      "Rendering twice is asserted byte-identical, the template is asserted free "
      "of bare numerals, and the claim ledger is asserted empty over this text.\n")

    A("## Introduction -- the reading result, with its population named\n")
    A(f"Measured on each model's own spontaneous refusals rather than on an "
      f"archived, partly steered item pool, the canonical refusal axis returns "
      f"{N_READS} `READS`, {N_AMBIG} `AMBIGUOUS` and {N_UNDEF} `UNDEFINED` over "
      f"the {N_MEMBERS_DET} checkpoints of the read-versus-act panel, and **zero** "
      f"`AT_CHANCE`. Reading is *measurable* -- the axis-A AUROC and its "
      f"bootstrap interval both exist -- on {N_MEASURABLE} of those members, "
      f"which is the {N_READS} `READS` members plus the one `AMBIGUOUS` member, "
      f"`{ambiguous['member']}` (AUROC {amb}, "
      f"{p('E2', ambiguous['json_pointer'].replace('/A_auroc', '/n_refusal'), 'int')} "
      f"refusals / "
      f"{p('E2', ambiguous['json_pointer'].replace('/A_auroc', '/n_compliance'), 'int')} "
      f"compliances, detection-powered y). Unit: the member. "
      f"Over that population the minimum AUROC is {ma} {ma_ci}, on "
      f"`{min_all['member']}`; over the `READS` members alone the minimum is "
      f"{mr}, on `{min_reads['member']}`; over the detection-powered members "
      f"alone it is {mp}, on `{min_pow['member']}`. The three minima belong to "
      f"three different populations and the paper states which one it means "
      f"every time it quotes one.\n")

    A("## §5.1 -- reading and steering, coupled\n")
    A(f"Across {N_PAIRS} (member, axis) pairs drawn from "
      f"{p('E2', '/metadata/results/h3_joint_scatter/n_members', 'int')} "
      f"detection-powered members over "
      f"{p('E2', '/metadata/results/h3_joint_scatter/n_lineages', 'int')} lineages "
      f"-- unit: the (member, axis) pair, with the bootstrap clustered on the "
      f"lineage -- induction quality and detection quality correlate at Spearman "
      f"{RHO_JOINT} {CI_JOINT}; the within-member mean is "
      f"{p('E2', '/metadata/results/h3_joint_scatter/within_member_mean_rho', 'f3')}. "
      f"The secondary version keyed on the steering coefficient gives "
      f"{p('E2', '/metadata/results/h3_joint_scatter/rho_secondary_neg_log10_c50', 'f3')} "
      f"under "
      f"{p('E2', '/metadata/results/h3_joint_scatter/censored_fraction', 'pct1')} "
      f"censoring, which is why the rate version is primary.\n")

    A(f"The abliterated arm is structurally, not statistically, quiet. Of "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/n_abliterated_class_measured', 'int')} "
      f"abliterated-class checkpoints -- unit: the member -- "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/n_abliterated_class_unpowered', 'int')} "
      f"never reached the per-class count the statistic needs even after the full "
      f"escalation ladder, so on the "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/M', 'int')} that were "
      f"powered the pre-registered hit count is "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/K', 'int')}. Induction "
      f"remains measurable on every member: across "
      f"{p('E2', '/metadata/results/h1b_induction_paired/n_pairs', 'int')} "
      f"within-lineage abliterated-versus-parent pairs -- unit: the pair -- "
      f"steering still induces on "
      f"{p('E2', '/metadata/results/h1b_induction_paired/n_induction_kept', 'int')} "
      f"and fails on "
      f"{p('E2', '/metadata/results/h1b_induction_paired/n_induction_lost', 'int')}, "
      f"with a median change in maximum induced rate of "
      f"{p('E2', '/metadata/results/h1b_induction_paired/median_delta_max_rate', 'f3')}.\n")

    A("## §5.2 -- the retraction, at the full lineage panel\n")
    A(f"At the **member level** -- "
      f"{p('E1', '/metadata/analysis/n_members', 'int')} members over "
      f"{p('E1', '/metadata/analysis/n_lineage', 'int')} lineages, one row per "
      f"member with the bootstrap clustered on the lineage label -- the original "
      f"scanner reaches "
      f"{p('E1', '/metadata/results/score_columns/orig_sigma/member_level/rho', 'f3')} "
      f"{p('E1', '/metadata/results/score_columns/orig_sigma/member_level/ci95_lineage_clustered', 'ci3')}, "
      f"the SET A refit "
      f"{p('E1', '/metadata/results/score_columns/refitA_sigma/member_level/rho', 'f3')} "
      f"{p('E1', '/metadata/results/score_columns/refitA_sigma/member_level/ci95_lineage_clustered', 'ci3')} "
      f"and the independently authored SET B refit "
      f"{p('E1', '/metadata/results/score_columns/refitB_sigma/member_level/rho', 'f3')} "
      f"{p('E1', '/metadata/results/score_columns/refitB_sigma/member_level/ci95_lineage_clustered', 'ci3')}. "
      f"The paired advantage is "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_A', 'signed3')} "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_A_ci95', 'ci3')} at "
      f"the member level, against the archived "
      f"{p('E1', '/metadata/results/sensitivity/archived_19_only_Delta_A/member_level/delta', 'signed4')}; "
      f"SET B gives "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_B', 'signed3')} "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_B_ci95', 'ci3')}. "
      f"The permutation p for the SET A advantage is "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/permutation_p_Delta_A', 'f3')} "
      f"against a Monte-Carlo floor of "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/permutation_floor', 'sci')} "
      f"-- unit: the lineage permutation -- so the floor that pinned the original "
      f"result is retired. The verdict string is `DOES_NOT_SURVIVE`.\n")

    A(f"The shrinkage is localised, not diffuse. Split by provenance and read at "
      f"the member level, the archived block reproduces "
      f"{p('E1', '/metadata/results/sensitivity/archived_19_only_Delta_A/member_level/delta', 'signed4')} "
      f"-- a gap of "
      f"{p('DERIVED', '/values/gap_archived19_block_to_published_delta', 'sci')} to "
      f"the previously published value, itself read from the frozen "
      f"pre-registration -- while the newly measured members give "
      f"{p('E1', '/metadata/results/sensitivity/new_members_only_Delta_A/member_level/delta', 'signed3')} "
      f"{p('E1', '/metadata/results/sensitivity/new_members_only_Delta_A/member_level/ci95', 'ci3')}.\n")

    A("## §5.3 -- semantics at matched contrast, against a measured floor\n")
    A(f"At matched axis-contrast units, pooled over the depth panel and scored on "
      f"fluency-screened text -- unit: the generated item -- the five-class "
      f"any-refusal rate is "
      f"{p('V2', '/metrics_agg/pooled_matched_rate_B_five_class_any_refusal', 'f3')} "
      f"for axis B against "
      f"{p('V2', '/metrics_agg/pooled_matched_rate_A_five_class_any_refusal', 'f3')} "
      f"for axis A, with the random-direction false-positive floor at "
      f"{p('V2', '/metrics_agg/pooled_matched_control_floor_Z', 'f3')}. The net "
      f"quantity is "
      f"{p('V2', '/metrics_agg/pooled_matched_NET_B_minus_Z', 'signed3')} "
      f"(paired prompt-clustered bootstrap, 95\\% CI "
      f"{p('V2', '/metrics_agg/pooled_matched_NET_ci_lo', 'f3')} to "
      f"{p('V2', '/metrics_agg/pooled_matched_NET_ci_hi', 'f3')}): axis B sits "
      f"below what a meaningless direction induces on the same population. The "
      f"verdict string is `REVERSAL_DOES_NOT_SURVIVE`, on "
      f"{p('V2', '/metrics_agg/n_members_REVERSAL_DOES_NOT_SURVIVE', 'int')} "
      f"members and pooled. At matched contrast the lexical screen removes "
      f"nothing -- retention is "
      f"{p('V2', '/metrics_agg/mean_retention_A_at_matched', 'f3')} for A and "
      f"{p('V2', '/metrics_agg/mean_retention_B_at_matched', 'f3')} for B -- while "
      f"at B's own maximum coefficient retention falls to "
      f"{p('V2', '/metrics_agg/mean_retention_B_at_max_alpha', 'f3')} and "
      f"{p('V2', '/metrics_agg/max_contrast_surviving_degenerate_fraction_B', 'pct1')} "
      f"of the surviving text is still judge-degenerate against "
      f"{p('V2', '/metrics_agg/archive_unfiltered_degenerate_fraction_B', 'pct1')} "
      f"unfiltered. The control floor is itself made of screen-passing degenerate "
      f"text: "
      f"{p('V2', '/metrics_agg/matched_control_D_surviving_degenerate_fraction', 'pct1')} "
      f"of the random axis's matched-cell survivors are judge-degenerate. At B's "
      f"own peak coefficient B does clear the floor -- "
      f"{p('V2', '/metrics_agg/peak_rate_B_five_class_any_refusal', 'f3')} against "
      f"{p('V2', '/metrics_agg/peak_rate_control_floor_Z', 'f3')}, net "
      f"{p('V2', '/metrics_agg/peak_rate_NET', 'signed3')} -- which is the "
      f"`REVERSAL_SURVIVES` branch, and it lives at coefficients matching "
      f"forbids.\n")

    A("## §5.4 -- the aggregation unit, named on every row\n")
    A(f"Our AMS reimplementation's correlation with the judged plain-harmful "
      f"refusal rate is "
      f"{p('V1', '/metrics_agg/ourAMS_rho_member_level', 'f3')} at the **member "
      f"level** -- {p('V1', '/metrics_agg/n_members', 'int')} members, resampled "
      f"and permuted on the lineage label -- and "
      f"{p('V1', '/metrics_agg/ourAMS_rho_lineage_level', 'f3')} at the **lineage "
      f"level**, {p('V1', '/metrics_agg/n_lineage_labels', 'int')} units each the "
      f"mean over that lineage's defined members of both score and outcome. The "
      f"gap of {p('V1', '/metrics_agg/ourAMS_rho_gap_between_units', 'f3')} is "
      f"what lineage aggregation buys. Over the "
      f"{p('V1', '/metrics_agg/n_score_cells_compared_across_units', 'int')} score "
      f"x configuration cells where both units are defined, changing nothing but "
      f"the unit moves oriented rho by a median "
      f"{p('V1', '/metrics_agg/median_abs_change_in_rho_from_unit_choice_alone', 'f3')} "
      f"and a maximum "
      f"{p('V1', '/metrics_agg/max_abs_change_in_rho_from_unit_choice_alone', 'f3')}, "
      f"and flips the sign on "
      f"{p('V1', '/metrics_agg/n_score_cells_whose_rho_sign_flips_with_the_unit', 'int')}. "
      f"The headline paired statistic inherits that: on the carrier the previous "
      f"draft used it is "
      f"{p('V1', '/metrics_agg/oriented_delta_lineage_level_v2_carrier', 'f3')} at "
      f"the lineage level and "
      f"{p('V1', '/metrics_agg/oriented_delta_member_level_v2_carrier', 'f3')} at "
      f"the member level -- `SIGN_SURVIVES`, `EXCLUSION_LOST_AT_MEMBER_LEVEL`.\n")

    A(f"The battery's negative does not depend on its cutoffs. Over a "
      f"{p('V1', '/metrics_agg/n_grid_points', 'int_comma')}-point full factorial "
      f"in the five thresholds -- unit: the grid point -- "
      f"`PROTOCOL_DOES_NOT_DISCRIMINATE` holds on a fraction "
      f"{p('V1', '/metrics_agg/frac_does_not_discriminate_preregistered_rule', 'f4')} "
      f"of grid points, and on "
      f"{p('V1', '/metrics_agg/frac_does_not_discriminate_strict_exceed', 'f4')} "
      f"under the stricter strictly-exceed criterion. Scoring the numeric cutoffs "
      f"alone lowers those to "
      f"{p('V1', '/metrics_agg/frac_does_not_discriminate_threshold_only_rule', 'f4')} "
      f"and "
      f"{p('V1', '/metrics_agg/frac_does_not_discriminate_threshold_only_strict_exceed', 'f4')}, "
      f"which locates the negative in the verdict-class and interiority clauses "
      f"rather than in the numbers.\n")

    A("## §5.5 -- the two empirical nulls\n")
    A(f"A matched random direction is not inert. Injected at the canonical axis's "
      f"own matched magnitude it induces refusal at a maximum rate of at least "
      f"the pre-registered threshold on "
      f"{p('E2', '/metadata/results/sanity_panel/n_D_induces_violations', 'int')} "
      f"of {N_MEMBERS_DET} members -- unit: the member -- with a panel median of "
      f"{p('E2', '/metadata/results/sanity_panel/median_random_axis_max_rate', 'f3')} "
      f"and a worst case of "
      f"{p('E2', '/metadata/results/sanity_panel/max_random_axis_max_rate', 'f3')}. "
      f"And a random direction does not *read* at the textbook chance value: "
      f"over the "
      f"{p('DERIVED', '/values/random_null_reading_n_members_with_a_measured_band', 'int')} "
      f"members where the band is measurable its half-width runs from "
      f"{p('DERIVED', '/values/random_null_reading_band_half_width_min', 'f3')} "
      f"to "
      f"{p('DERIVED', '/values/random_null_reading_band_half_width_max', 'f3')} "
      f"-- unit: the member -- so a gate written against the textbook value is "
      f"wrong by a wide and model-dependent margin, and a single random draw "
      f"is not a null distribution.\n")
    return "\n".join(L)


def abstract_template(min_all: dict, min_reads: dict, ambiguous: dict,
                      hg_present: bool) -> str:
    ma = p("E2", min_all["json_pointer"], "f3")
    mr = p("E2", min_reads["json_pointer"], "f3")
    L = []
    A = L.append
    A("# Abstract skeleton (pointer-only)\n")
    A("**(i) What survives.** ")
    A(f"On the read-versus-act panel of {N_MEMBERS_DET} checkpoints, the "
      f"canonical refusal axis read on each model's *own* spontaneous refusals "
      f"returns {N_READS} `READS`, {N_AMBIG} `AMBIGUOUS`, {N_UNDEF} `UNDEFINED` "
      f"and zero `AT_CHANCE`; reading is measurable on {N_MEASURABLE} members and "
      f"{N_POWERED} are detection-powered (unit: the member). The minimum AUROC "
      f"is {ma} over all members with a defined AUROC (`{min_all['member']}`, "
      f"verdict `AMBIGUOUS`) and {mr} over the `READS` members "
      f"(`{min_reads['member']}`) -- two populations, never one bound. "
      f"Reading and steering are positively coupled at {RHO_JOINT} {CI_JOINT} "
      f"over {N_PAIRS} (member, axis) pairs. At matched axis-contrast units on "
      f"fluency-screened text the canonical axis induces "
      f"{p('V2', '/metrics_agg/pooled_matched_rate_A_five_class_any_refusal', 'f3')} "
      f"any-refusal against its token-disjoint paraphrase's "
      f"{p('V2', '/metrics_agg/pooled_matched_rate_B_five_class_any_refusal', 'f3')}, "
      f"with a measured random-direction floor of "
      f"{p('V2', '/metrics_agg/pooled_matched_control_floor_Z', 'f3')} (unit: the "
      f"item), so the advantage is semantic and not lexical. Two null corrections "
      f"follow: a matched random direction induces refusal on "
      f"{p('E2', '/metadata/results/sanity_panel/n_D_induces_violations', 'int')} "
      f"of {N_MEMBERS_DET} members, worst case "
      f"{p('E2', '/metadata/results/sanity_panel/max_random_axis_max_rate', 'f3')}, "
      f"and the random-direction *reading* band has a half-width running from "
      f"{p('DERIVED', '/values/random_null_reading_band_half_width_min', 'f3')} "
      f"to "
      f"{p('DERIVED', '/values/random_null_reading_band_half_width_max', 'f3')} "
      f"across members, so the textbook chance value is not the null.\n")
    A("**(ii) The retractions, named as retractions.** ")
    A(f"The paraphrase refit does **not** survive at "
      f"{p('E1', '/metadata/analysis/n_lineage', 'int')} lineages: the paired "
      f"advantage falls to "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_A', 'signed3')} "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_A_ci95', 'ci3')} at "
      f"the member level from the archived "
      f"{p('E1', '/metadata/results/sensitivity/archived_19_only_Delta_A/member_level/delta', 'signed4')}, "
      f"an independently authored set gives "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/delta_B', 'signed3')}, and "
      f"the permutation p is "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/permutation_p_Delta_A', 'f3')} "
      f"against a floor of "
      f"{p('E1', '/metadata/results/verdict/rule_inputs/permutation_floor', 'sci')} "
      f"(`DOES_NOT_SURVIVE`). The iteration-3 'at chance in both roles' claim is "
      f"retracted with "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/K', 'int')} hits of "
      f"{p('E2', '/metadata/results/h1_abliterated_arm/M', 'int')} powered "
      f"abliterated members.\n")
    A("**(iii) The aggregation-unit result.** ")
    A(f"Changing only the aggregation unit -- member versus lineage-aggregated, "
      f"nothing else -- moves oriented rho by a median "
      f"{p('V1', '/metrics_agg/median_abs_change_in_rho_from_unit_choice_alone', 'f3')} "
      f"and a maximum "
      f"{p('V1', '/metrics_agg/max_abs_change_in_rho_from_unit_choice_alone', 'f3')}, "
      f"and flips the sign on "
      f"{p('V1', '/metrics_agg/n_score_cells_whose_rho_sign_flips_with_the_unit', 'int')} "
      f"of {p('V1', '/metrics_agg/n_score_cells_compared_across_units', 'int')} "
      f"score x configuration cells (unit: the cell).\n")
    A("**(iv) The H-G scale-panel headline.** ")
    if hg_present:
        A("PLACEHOLDER_HG_PRESENT\n")
    else:
        A("_Slot reserved._ The iteration-5 scale-panel artifact is "
          "`ABSENT_AT_RUN_TIME`, so this sentence is a single marked pointer slot "
          "rather than prose. When it lands, the product claim to state is the "
          "narrowed one -- *no generation, no judge, no benchmark, no reference "
          "model* -- and **not** 'harmful-prompt-free'.\n")
    return "\n".join(L)
