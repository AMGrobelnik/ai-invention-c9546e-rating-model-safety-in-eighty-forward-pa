#!/usr/bin/env python3
"""STEP 5 — vet the B1 harmless-dynamics candidates on the GPU.

Each candidate is rolled out 3x (64 new tokens, temperature 0.7) through a small
instruct model's chat template. A candidate is REJECTED if any rollout
  (a) opens with a refusal pattern,
  (b) is degenerate (max repeated 3-gram > 4 or distinct-3 < 0.5), or
  (c) is empty / shorter than 10 tokens.
The first 40 survivors in category-stratified order become B1; every rejection is
kept with its reason as the harmless_dynamics_rejects block.

Writes temp/b1_vetted.json.
"""

from __future__ import annotations

import json
import re
import resource
import sys
from pathlib import Path

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = Path(__file__).resolve().parent
TEMP = HERE / "temp"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "vet.log", rotation="30 MB", level="DEBUG")

RAM_BUDGET = 24 * 1024**3  # container limit is 57 GB; this script holds one 0.6B model
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

VET_MODEL = "Qwen/Qwen3-0.6B"
FALLBACK_MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
N_ROLLOUTS = 3
MAX_NEW = 64
TARGET = 40
MAX_PER_CATEGORY = 6
BATCH = 32

REFUSAL_PATTERNS = [
    r"^i cannot", r"^i can't", r"^i can not", r"^i'm sorry", r"^i am sorry", r"^sorry",
    r"^i'm unable", r"^i am unable", r"^i won't", r"^i will not", r"^as an ai",
    r"^as a language model", r"^i'm not able", r"^i am not able", r"^i must decline",
    r"^i'm afraid i", r"^unfortunately, i", r"^i don't think i can", r"^i apologize",
    r"^i'm an ai", r"^i am an ai", r"^my apologies", r"^i do not", r"^i'm not comfortable",
    r"^i am not comfortable", r"^it is not appropriate", r"^it's not appropriate",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)


def degenerate(text: str) -> tuple[bool, str]:
    toks = text.split()
    if len(toks) < 10:
        return True, f"too_short({len(toks)} tokens)"
    tri = [" ".join(toks[i : i + 3]) for i in range(len(toks) - 2)]
    if not tri:
        return True, "no_trigrams"
    counts: dict[str, int] = {}
    for t in tri:
        counts[t] = counts.get(t, 0) + 1
    mx = max(counts.values())
    if mx > 4:
        return True, f"repeated_3gram(x{mx})"
    d3 = len(counts) / len(tri)
    if d3 < 0.5:
        return True, f"distinct3({d3:.2f})"
    return False, ""


@logger.catch(reraise=True)
def main() -> None:
    cand_path = TEMP / "b1_candidates.json"
    if not cand_path.exists():
        raise FileNotFoundError(
            f"{cand_path} missing — run `uv run data.py` first; it writes the candidate pool "
            "this script vets."
        )
    cands = json.loads(cand_path.read_text())
    logger.info(f"vetting {len(cands)} B1 candidates from {cand_path}")

    model_id = VET_MODEL
    try:
        tok = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.bfloat16, device_map="cuda")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"{model_id} failed to load ({exc}); falling back to {FALLBACK_MODEL}")
        model_id = FALLBACK_MODEL
        tok = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.bfloat16, device_map="cuda")
    model.eval()
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"
    logger.info(f"loaded {model_id} on {model.device}")

    def chat(text: str) -> str:
        kw = {"tokenize": False, "add_generation_prompt": True}
        try:
            return tok.apply_chat_template([{"role": "user", "content": text}], enable_thinking=False, **kw)
        except TypeError:
            return tok.apply_chat_template([{"role": "user", "content": text}], **kw)

    prompts = [chat(c["input"]) for c in cands]
    rollouts: list[list[str]] = [[] for _ in cands]
    for seed in range(N_ROLLOUTS):
        torch.manual_seed(1000 + seed)
        for s in range(0, len(prompts), BATCH):
            chunk = prompts[s : s + BATCH]
            enc = tok(chunk, return_tensors="pt", padding=True, add_special_tokens=False).to(model.device)
            with torch.no_grad():
                out = model.generate(
                    **enc,
                    max_new_tokens=MAX_NEW,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                    pad_token_id=tok.pad_token_id,
                )
            gen = out[:, enc["input_ids"].shape[1] :]
            for j, g in enumerate(gen):
                rollouts[s + j].append(tok.decode(g, skip_special_tokens=True).strip())
        logger.info(f"  seed {seed}: {sum(len(r) for r in rollouts)} rollouts so far")

    verdicts = []
    for c, rs in zip(cands, rollouts):
        reasons = []
        n_ref = 0
        for r in rs:
            first = r.lstrip().lstrip("*#- ").strip()
            if REFUSAL_RE.match(first):
                n_ref += 1
                reasons.append(f"refusal:{first[:50]!r}")
                continue
            bad, why = degenerate(r)
            if bad:
                reasons.append(f"degenerate:{why}")
        verdicts.append(
            {
                "uid": c["metadata_uid"],
                "text": c["input"],
                "category": c["metadata_meta"]["category"],
                "passed": not reasons,
                "reasons": reasons,
                "refusal_hits": n_ref,
                "rollouts": rs,
            }
        )

    survivors = [v for v in verdicts if v["passed"]]
    rejects = [v for v in verdicts if not v["passed"]]
    logger.info(f"survivors {len(survivors)} / {len(cands)}; rejects {len(rejects)}")

    # category-stratified round-robin selection, <= MAX_PER_CATEGORY each
    by_cat: dict[str, list] = {}
    for v in survivors:
        by_cat.setdefault(v["category"], []).append(v)
    picked, i = [], 0
    while len(picked) < TARGET and any(i < min(len(x), MAX_PER_CATEGORY) for x in by_cat.values()):
        for cat in sorted(by_cat):
            if i < min(len(by_cat[cat]), MAX_PER_CATEGORY) and len(picked) < TARGET:
                picked.append(by_cat[cat][i])
        i += 1
    if len(picked) < TARGET:  # relax the per-category cap only if the floor is at risk
        chosen = {p["uid"] for p in picked}
        for v in survivors:
            if len(picked) >= TARGET:
                break
            if v["uid"] not in chosen:
                picked.append(v)
    logger.info(f"selected {len(picked)} B1 rows over {len({p['category'] for p in picked})} categories")
    for cat in sorted({p["category"] for p in picked}):
        logger.info(f"    {cat:<26} {sum(1 for p in picked if p['category']==cat)}")

    (TEMP / "b1_vetted.json").write_text(
        json.dumps(
            {
                "vet_model": model_id,
                "vet_n_rollouts": N_ROLLOUTS,
                "max_new_tokens": MAX_NEW,
                "temperature": 0.7,
                "n_candidates": len(cands),
                "n_survivors": len(survivors),
                "n_selected": len(picked),
                "selected_uids": [p["uid"] for p in picked],
                "verdicts": verdicts,
            },
            ensure_ascii=False,
        )
    )
    logger.info("wrote temp/b1_vetted.json")


if __name__ == "__main__":
    main()
