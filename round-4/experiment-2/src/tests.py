#!/usr/bin/env python3
"""Pre-flight validation gates T0-T3.

T0  archive inventory (exists + sha256, and which lib files were copied byte-identical)
T1  replay the archived detection analysis with the NEW analysis code, no model
T2  the contrast-unit formula against the archived analysis2.json
T3  the tokenisation-bug unit test (needs a GPU and Qwen3-0.6B)

Nothing downstream may run until T1 and T2 pass; T3 gates the GPU stage.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

import explib as EX

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(EX.HERE / "logs").mkdir(exist_ok=True)
logger.add(EX.HERE / "logs/tests.log", rotation="30 MB", level="DEBUG")


# ==========================================================================
def t0_archive_inventory() -> dict:
    """Every path the plan assumes, whether it exists, and its sha256."""
    want = {
        "ARCH_EXP": EX.ARCH_EXP, "ARCH_EVAL": EX.ARCH_EVAL,
        "DATA": EX.DATA, "ITER2_EXP1": EX.ITER2_EXP1,
        "ARCH_EXP/method_out.json": EX.ARCH_EXP / "method_out.json",
        "ARCH_EXP/RESULTS.md": EX.ARCH_EXP / "RESULTS.md",
        "ARCH_EVAL/prereg.py": EX.ARCH_EVAL / "prereg.py",
        "ARCH_EVAL/judge_stage.py": EX.ARCH_EVAL / "judge_stage.py",
        "ARCH_EVAL/gpu_stage.py": EX.ARCH_EVAL / "gpu_stage.py",
        "ARCH_EVAL/eval_lib.py": EX.ARCH_EVAL / "eval_lib.py",
        "ARCH_EVAL/analysis12.py": EX.ARCH_EVAL / "analysis12.py",
        "ARCH_EVAL/analysis34.py": EX.ARCH_EVAL / "analysis34.py",
        "ARCH_EVAL/assemble.py": EX.ARCH_EVAL / "assemble.py",
        "ARCH_EVAL/results/analysis1.json": EX.ARCH_EVAL / "results/analysis1.json",
        "ARCH_EVAL/results/analysis2.json": EX.ARCH_EVAL / "results/analysis2.json",
        "ARCH_EVAL/results/prereg_eval.json": EX.ARCH_EVAL / "results/prereg_eval.json",
        "ITER2_EXP1/results/prompts.json": EX.ITER2_EXP1 / "results/prompts.json",
    }
    inv = {"paths": {}, "lib_copied_byte_identical": {}, "archived_checkpoints": {}}
    for name, p in want.items():
        rec = {"path": str(p), "exists": p.exists(), "is_dir": p.is_dir()}
        if p.exists() and p.is_file():
            rec["sha256"] = EX.sha256_file(p)
            rec["bytes"] = p.stat().st_size
        inv["paths"][name] = rec

    src = EX.ARCH_EXP / "lib"
    dst = EX.HERE / "lib"
    for f in sorted(src.glob("*.py")):
        d = dst / f.name
        inv["lib_copied_byte_identical"][f.name] = {
            "source_sha256": EX.sha256_file(f),
            "local_sha256": EX.sha256_file(d) if d.exists() else None,
            "identical": bool(d.exists() and EX.sha256_file(d) == EX.sha256_file(f)),
        }

    for k in ("instruct_0p6", "base_0p6", "abliterated_0p6",
              "instruct_1p7", "base_1p7", "abliterated_1p7"):
        axd = EX.ARCH_EVAL / "results/axes"
        inv["archived_checkpoints"][k] = {
            "axes": sorted(p.name for p in axd.glob(f"{k}_*.npy")),
            "proj_npz": (EX.ARCH_EVAL / f"results/proj/{k}.npz").exists(),
            "encode_json": (EX.ARCH_EVAL / f"results/encode_{k}.json").exists(),
        }

    n_lib = len(inv["lib_copied_byte_identical"])
    n_ident = sum(1 for v in inv["lib_copied_byte_identical"].values() if v["identical"])
    inv["summary"] = {
        "n_lib_files": n_lib, "n_lib_byte_identical": n_ident,
        "lib_gate_passed": bool(n_lib >= 13 and n_ident == n_lib),
        "n_paths_missing": sum(1 for v in inv["paths"].values() if not v["exists"]),
        "note": "the artifact plan predicted gpu_stage.py / eval_lib.py / analysis*.py "
                "were ABSENT from gen_art_evaluation_1. They are PRESENT. The GPU stage "
                "here is nonetheless a REIMPLEMENTATION (it must generate the model's own "
                "text on new checkpoints, which the archived stage never did); only lib/ "
                "is reused byte-identically.",
    }
    EX.atomic_write_json(EX.RESULTS / "archive_inventory.json", inv)
    logger.info(f"T0 lib byte-identical {n_ident}/{n_lib}; "
                f"{inv['summary']['n_paths_missing']} paths missing")
    return inv


# ==========================================================================
def t1_replay_archived_analysis(key: str = "instruct_0p6") -> dict:
    """Recompute the archived per-axis AUROC + clustered CI with the NEW code.

    Target (analysis1.json, stratum-centred): A = 0.6620, B = 0.5102,
    paired A-B = +0.1518 [+0.083, +0.210].
    """
    npz = np.load(EX.ARCH_EVAL / f"results/proj/{key}.npz")
    items = json.loads((EX.ARCH_EVAL / f"results/proj/{key}_items.json").read_text())
    arch = EX.load_json(EX.ARCH_EVAL / "results/analysis1.json")["per_checkpoint"][key]

    # Archived conventions, replicated exactly (analysis12.py): the primary label
    # is the judge label where it exists and the regex label otherwise;
    # PARTIAL/DEGENERATE are EXCLUDED; the stratum centring happens on the FULL
    # item set BEFORE that exclusion; the bootstrap cluster is "source|cluster".
    prim = []
    for it in items:
        lab = it.get("judge_label")
        if lab == "REFUSAL":
            prim.append(1)
        elif lab == "COMPLIANCE":
            prim.append(0)
        elif lab in ("PARTIAL", "DEGENERATE"):
            prim.append(-1)
        else:
            prim.append(1 if it["regex_refusal"] else 0)
    prim = np.array(prim)
    strata_full = np.array([it["stratum"] for it in items])
    keep = prim >= 0

    proj, centred = {}, {}
    for a in npz.files:
        if not a.endswith("|first"):
            continue
        ax = a.split("|")[0]
        proj[ax] = npz[a][keep]
        centred[ax] = EX.centre_by_stratum(npz[a], strata_full)[keep]

    labels = prim[keep] == 1
    strata = strata_full[keep]
    clusters = np.array([f"{it['source']}|{it['cluster']}"
                         for it in items])[keep]
    got = EX.detection_stats(proj, labels, strata, clusters, centred=centred)

    cmp_rows = []
    for ax in ("A_canned", "B_paraphrase", "C_stylistic", "D_random0",
               "E_prompt_contrast"):
        if ax not in got["axes"] or ax not in arch["axes"]:
            continue
        g = got["axes"][ax]["auroc"]
        a = arch["axes"][ax]["centred"]["auroc"]
        cmp_rows.append({"axis": ax, "recomputed": g, "archived": a,
                         "abs_diff": abs(g - a), "match_3dp": bool(abs(g - a) < 5e-4)})
    pa = got.get("paired_A_minus_B", {})
    arch_pa = (arch["axes"]["A_canned"]["centred"]["auroc"]
               - arch["axes"]["B_paraphrase"]["centred"]["auroc"])
    out = {"checkpoint": key, "n_items_scored": int(labels.size),
           "n_refusal": int(labels.sum()), "archived_n_items": arch["n_items"],
           "per_axis": cmp_rows,
           "paired_A_minus_B_recomputed": pa.get("delta"),
           "paired_A_minus_B_archived": float(arch_pa),
           "paired_ci95_recomputed": pa.get("ci95"),
           "passed": bool(cmp_rows and all(r["match_3dp"] for r in cmp_rows))}
    for r in cmp_rows:
        logger.info(f"T1 {r['axis']:20s} new={r['recomputed']:.4f} "
                    f"arch={r['archived']:.4f} d={r['abs_diff']:.2e} "
                    f"{'OK' if r['match_3dp'] else 'MISMATCH'}")
    logger.info(f"T1 paired A-B new={pa.get('delta'):.4f} arch={arch_pa:.4f} "
                f"CI={pa.get('ci95')}")
    return out


# ==========================================================================
def t2_contrast_unit_formula() -> dict:
    """c = alpha * NORM_L / ||d_raw|| against every archived analysis2 grid cell."""
    a2 = EX.load_json(EX.ARCH_EVAL / "results/analysis2.json")["per_checkpoint"]
    rows, worst = [], 0.0
    for key, blk in a2.items():
        norm_l = float(blk["NORM_L"])
        for ax, arec in blk.get("axes", {}).items():
            raw = float(blk["axis_raw_norms"][ax])
            for astr, cell in arec.get("grid", {}).items():
                if "contrast_units" not in cell:
                    continue
                got = EX.contrast_units(float(cell["alpha"]), raw, norm_l)
                exp = float(cell["contrast_units"])
                err = abs(got - exp)
                worst = max(worst, err)
                rows.append({"checkpoint": key, "axis": ax, "alpha": cell["alpha"],
                             "recomputed": got, "archived": exp, "abs_err": err})
    out = {"n_cells_checked": len(rows), "worst_abs_error": worst,
           "passed": bool(rows and worst < 1e-6),
           "formula": "c = alpha * NORM_L / ||d_raw||",
           "examples": rows[:6]}
    logger.info(f"T2 {len(rows)} archived contrast-unit cells, worst error {worst:.2e} "
                f"-> {'PASS' if out['passed'] else 'FAIL'}")
    return out


# ==========================================================================
def t3_tokenisation_unit_test(repo: str = "Qwen/Qwen3-0.6B") -> dict:
    """The archived bug: string concat vs token-id concat at the prompt boundary."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from lib.models import make_renderer

    from lib.models import render_plain

    tok = AutoTokenizer.from_pretrained(repo)
    render_chat, _ = make_renderer(tok, "auto")
    items = json.loads(
        (EX.ARCH_EVAL / "results/proj/instruct_0p6_items.json").read_text())[:50]

    # The boundary merge is RENDERER-dependent: a chatml prompt ends in a newline
    # so BPE cannot merge across it, while the plain wrapper ends in "Assistant:"
    # and does.  Both are exercised, because the panel contains base checkpoints
    # rendered plainly, and the liveness half of this test would be vacuous on
    # chatml alone.
    per_render = {}
    for rname, rfn in (("chat_template", render_chat), ("plain_wrapper", render_plain)):
        n_len_ok = n_string_differs = n_first_token_ok = 0
        for it in items:
            pre = rfn(it["prompt"]) + (it.get("prefill") or "")
            ids_pre = tok(pre, add_special_tokens=False).input_ids
            ids_gen = tok(it["text"], add_special_tokens=False).input_ids
            seq = list(ids_pre) + list(ids_gen)
            n_len_ok += int(len(seq) == len(ids_pre) + len(ids_gen))
            joint = tok(pre + it["text"], add_special_tokens=False).input_ids
            n_string_differs += int(list(joint[:len(ids_pre)]) != list(ids_pre)
                                    or len(joint) != len(seq))
            if ids_gen:
                n_first_token_ok += int(tok.decode([seq[len(ids_pre)]])
                                        == tok.decode([ids_gen[0]]))
        per_render[rname] = {"n_len_identity_ok": n_len_ok,
                             "n_string_concat_differs": n_string_differs,
                             "n_first_token_decode_ok": n_first_token_ok}
    n_len_ok = min(v["n_len_identity_ok"] for v in per_render.values())
    n_first_token_ok = min(v["n_first_token_decode_ok"] for v in per_render.values())
    n_string_differs = max(v["n_string_concat_differs"] for v in per_render.values())
    render = render_chat

    # (c) the boundary index really selects the first generated token's hidden state
    model = AutoModelForCausalLM.from_pretrained(
        repo, dtype=torch.bfloat16).to("cuda").eval()
    it = items[0]
    pre = render(it["prompt"])
    ids_pre = tok(pre, add_special_tokens=False).input_ids
    ids_gen = tok(it["text"], add_special_tokens=False).input_ids
    with torch.no_grad():
        ids = torch.tensor([list(ids_pre) + list(ids_gen)], device="cuda")
        o = model(input_ids=ids, use_cache=False, output_hidden_states=True)
        # embedding layer (hidden_states[0]) at the boundary must equal the
        # embedding of the first generated token -- an exact positional check
        emb = o.hidden_states[0][0, len(ids_pre), :].float().cpu()
        ref = model.get_input_embeddings()(
            torch.tensor([ids_gen[0]], device="cuda"))[0].float().cpu()
        boundary_exact = bool(torch.allclose(emb, ref, atol=1e-3))
    del model, o
    EX.free_cuda()

    out = {"n_items": len(items), "per_renderer": per_render,
           "n_len_identity_ok": n_len_ok,
           "n_string_concat_differs": n_string_differs,
           "n_first_token_decode_ok": n_first_token_ok,
           "boundary_index_selects_first_generated_token": boundary_exact,
           "passed": bool(n_len_ok == len(items) and n_string_differs >= 1
                          and n_first_token_ok == len(items) and boundary_exact)}
    logger.info(f"T3 len-identity {n_len_ok}/{len(items)}; string-concat differs on "
                f"{n_string_differs}; boundary exact={boundary_exact} -> "
                f"{'PASS' if out['passed'] else 'FAIL'}")
    return out


def main():
    EX.RESULTS.mkdir(parents=True, exist_ok=True)
    res = {"T0_archive_inventory": t0_archive_inventory()["summary"],
           "T1_replay_archived_analysis": t1_replay_archived_analysis(),
           "T2_contrast_unit_formula": t2_contrast_unit_formula()}
    if "--gpu" in sys.argv:
        res["T3_tokenisation_unit_test"] = t3_tokenisation_unit_test()
    res["all_passed"] = all(v.get("passed", True) for v in res.values()
                            if isinstance(v, dict))
    EX.atomic_write_json(EX.RESULTS / "tests.json", res)
    logger.info(f"ALL PASSED = {res['all_passed']}")
    return 0 if res["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
