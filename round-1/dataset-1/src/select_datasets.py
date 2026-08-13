#!/usr/bin/env python3
"""KEEP / DISCARD decisions over the 25 previewed candidates, and download the KEEPs.

Each KEPT dataset is materialised under temp/datasets/ as full_/mini_/preview_ JSON
at a resolved revision SHA, so every source the corpus draws on is inspectable on
disk. DISCARD decisions are recorded with their reason — a rejected candidate with
a stated reason is data, a silently dropped one is not.
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests
from huggingface_hub import HfApi, hf_hub_download
from loguru import logger

HERE = Path(__file__).resolve().parent
OUT = HERE / "temp" / "datasets"
OUT.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "select.log", rotation="30 MB", level="DEBUG")

API = HfApi()

# (repo, file, kind, used_for, why_kept)
KEEP: list[tuple[str, str, str, str, str]] = [
    ("Paul/XSTest", "xstest_prompts.csv", "csv", "B2 xstest_overrefusal",
     "ungated mirror of XSTest v2 (Röttger et al., NAACL 2024); exactly 450 rows with the 250/200 safe/unsafe split and the 10 prompt types intact"),
    ("natolambert/xstest-v2-copy", "data/gpt4-00000-of-00001.parquet", "parquet", "cross-check of B2",
     "second independent XSTest v2 copy carrying model completions and human annotations; used to confirm the prompt set matches"),
    ("JailbreakBench/JBB-Behaviors", "data/harmful-behaviors.csv", "csv", "B3 / B3b plain_harmful",
     "NeurIPS 2024 D&B benchmark; 100 behaviors with real OpenAI-usage-policy categories and affirmative Target strings — the only source here with both"),
    ("JailbreakBench/JBB-Behaviors", "data/benign-behaviors.csv", "csv", "reference contrast (not used in any block)",
     "topic-matched benign twins of the 100 harmful behaviors; kept as a documented sanity-check resource for downstream artifacts"),
    ("TrustAIRLab/forbidden_question_set", "forbidden_question_set.csv", "csv", "B5 layer_contrast (harmful half)",
     "390 questions over 13 OpenAI-policy scenarios from Shen et al. CCS 2024; independently constructed, so it is genuinely disjoint from AdvBench/JBB"),
    ("mlabonne/harmless_alpaca", "data/train-00000-of-00001.parquet", "parquet", "B5 layer_contrast (benign half)",
     "the canonical harmless half of the abliteration diff-in-means contrast pair"),
    ("mlabonne/harmful_behaviors", "data/train-00000-of-00001.parquet", "parquet", "documented NOT used",
     "kept on disk to evidence the B5 design decision: it is an AdvBench repackaging, so using it for the contrast set would break disjointness from B3"),
    ("HuggingFaceH4/no_robots", "data/train-00000-of-00001.parquet", "parquet", "B1 harmless_dynamics",
     "10k human-written InstructGPT-style single-turn instructions with task categories — the best available source of real everyday prompts"),
    ("databricks/databricks-dolly-15k", "databricks-dolly-15k.jsonl", "jsonl", "B1 harmless_dynamics",
     "15k human-generated instructions with categories; supplies the no-context rows that widen B1's topical spread"),
    ("yahma/alpaca-cleaned", "alpaca_data_cleaned.json", "json", "reference (upstream of harmless_alpaca)",
     "cleaned Alpaca; kept to document the provenance of the B5 benign half and its CC-BY-NC restriction"),
    ("Salesforce/wikitext", "wikitext-2-raw-v1/test-00000-of-00001.parquet", "parquet", "B6 wikitext_fluency",
     "WikiText-2-raw-v1 test split (Merity et al., ICLR 2017); the standard perplexity screen corpus"),
    ("TrustAIRLab/in-the-wild-jailbreak-prompts", "jailbreak_2023_12_25/train-00000-of-00001.parquet", "parquet", "B4 template t2",
     "1.4k real collected jailbreak prompts (Shen et al. CCS 2024) — a published source for the refusal-suppression template"),
    ("rubend18/ChatGPT-Jailbreak-Prompts", "dataset.csv", "csv", "B4 template t3",
     "the widely-used community AIM/DAN persona prompt collection; supplies the role-play template"),
    ("walledai/MaliciousInstruct", "data/train-00000-of-00001.parquet", "parquet", "B5 top-up reserve",
     "100 malicious instructions (Huang et al. 2024 generation-exploitation); held in reserve if the forbidden-question set cannot fill 128 harmful rows"),
    ("LibrAI/do-not-answer", "data_en.csv", "csv", "reserve harmful contrast",
     "939 risk-taxonomy questions with per-model harmfulness labels; an alternative disjoint harmful contrast source"),
]

GH_KEEP = [
    ("llm-attacks/llm-attacks", "data/advbench/harmful_behaviors.csv", "B3 / B3b plain_harmful",
     "AdvBench (Zou et al. 2023) 520 goal/target pairs — the HF mirror walledai/AdvBench is gated, so the authoritative GitHub CSV is used instead"),
]

DISCARD: list[tuple[str, str]] = [
    ("walledai/XSTest", "gated repo — hf_hub_download returns 403 GatedRepoError with the available token; replaced by Paul/XSTest"),
    ("walledai/AdvBench", "gated repo — 403; replaced by the authoritative llm-attacks GitHub CSV"),
    ("walledai/HarmBench", "gated repo — 403, and HarmBench behaviors overlap JBB's sourcing, so it adds no disjoint material"),
    ("walledai/StrongREJECT", "gated repo — 403; not needed once JBB + AdvBench cover the plain-harmful block"),
    ("allenai/wildjailbreak", "gated, and its adversarial prompts are LLM-synthesised rather than published fixed templates"),
    ("allenai/wildguardmix", "gated; a safety-classifier training mix, not a prompt suite"),
    ("GAIR/lima", "loader-script repo that datasets>=3 cannot execute, and 1k curated multi-domain SFT prompts add nothing over no_robots for B1"),
    ("PKU-Alignment/BeaverTails", "364k rows / 99 MB of QA-pair safety annotations — a preference corpus, not a prompt suite; would dominate the corpus size for no gain"),
    ("Anthropic/hh-rlhf", "169k multi-turn preference pairs (182 MB); this artifact needs single-turn prompts, not chosen/rejected pairs"),
    ("allenai/real-toxicity-prompts", "toxicity-continuation prompts, not refusal-eliciting instructions; measures a different construct"),
    ("sorry-bench/sorry-bench-202503", "license 'other' with unclear redistribution terms, and its 44-category taxonomy is not needed once JBB's 10 policy categories are in place"),
    ("Paul/XSTest (annotations)", "n/a — the prompt CSV is kept; no separate annotation file exists in this repo"),
]


def fetch(repo: str, fname: str, kind: str, used_for: str, why: str) -> dict:
    rev = API.dataset_info(repo).sha
    try:
        p = hf_hub_download(repo, fname, repo_type="dataset", revision=rev)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"{repo}/{fname}: {exc}")
        return {"repo_id": repo, "file": fname, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}
    if kind == "csv":
        df = pd.read_csv(p)
    elif kind == "parquet":
        df = pd.read_parquet(p)
    elif kind == "jsonl":
        df = pd.read_json(p, lines=True)
    else:
        df = pd.read_json(p)
    recs = df.astype(object).where(pd.notna(df), None).to_dict("records")
    base = f"{repo.replace('/', '__')}__{Path(fname).stem}"
    (OUT / f"full_{base}.json").write_text(json.dumps(recs, ensure_ascii=False, default=str))
    (OUT / f"mini_{base}.json").write_text(json.dumps(recs[:3], indent=2, ensure_ascii=False, default=str))
    prev = json.loads(json.dumps(recs[:3], default=str))
    for r in prev:
        for k, v in list(r.items()):
            if isinstance(v, str) and len(v) > 200:
                r[k] = v[:200] + "..."
    (OUT / f"preview_{base}.json").write_text(json.dumps(prev, indent=2, ensure_ascii=False))
    logger.info(f"KEEP {repo:<45} {fname:<50} {df.shape} rev={rev[:12]}")
    return {"repo_id": repo, "file": fname, "revision": rev, "n_rows": int(df.shape[0]),
            "columns": [str(c) for c in df.columns], "used_for": used_for, "why_kept": why,
            "full_path": f"temp/datasets/full_{base}.json"}


def main() -> None:
    with ThreadPoolExecutor(max_workers=8) as ex:
        kept = list(ex.map(lambda a: fetch(*a), KEEP))

    for repo, path, used_for, why in GH_KEEP:
        commit = "098262edf85f807224e70ecd87b9d83716bf6b73"
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"
        r = requests.get(url, timeout=90)
        if r.status_code != 200:
            url = f"https://raw.githubusercontent.com/{repo}/main/{path}"
            r = requests.get(url, timeout=90)
        r.raise_for_status()
        import io

        df = pd.read_csv(io.StringIO(r.text))
        recs = df.to_dict("records")
        base = repo.replace("/", "__") + "__" + Path(path).stem
        (OUT / f"full_{base}.json").write_text(json.dumps(recs, ensure_ascii=False))
        (OUT / f"mini_{base}.json").write_text(json.dumps(recs[:3], indent=2, ensure_ascii=False))
        (OUT / f"preview_{base}.json").write_text(json.dumps(recs[:3], indent=2, ensure_ascii=False))
        kept.append({"repo_id": f"github:{repo}", "file": path, "revision": commit, "n_rows": int(df.shape[0]),
                     "columns": list(df.columns), "used_for": used_for, "why_kept": why,
                     "full_path": f"temp/datasets/full_{base}.json"})
        logger.info(f"KEEP github:{repo:<38} {path:<50} {df.shape} @{commit[:12]}")

    report = {
        "n_previewed": 25,
        "n_kept_sources": len({k['repo_id'] for k in kept}),
        "n_kept_files": len(kept),
        "kept": kept,
        "discarded": [{"repo_id": r, "reason": w} for r, w in DISCARD],
    }
    (HERE / "temp" / "dataset_selection.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    logger.info(f"kept {report['n_kept_sources']} sources / {report['n_kept_files']} files; "
                f"discarded {len(DISCARD)}")


if __name__ == "__main__":
    main()
