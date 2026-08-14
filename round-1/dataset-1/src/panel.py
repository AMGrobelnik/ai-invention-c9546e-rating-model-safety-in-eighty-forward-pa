#!/usr/bin/env python3
"""B8 — build the VERIFIED model-panel manifest.

Two passes:
  (a) seeded candidate list (base / instruct / abliterated variants)
  (b) discovery pass via HfApi.list_models for abliterated + behavioral-uncensored

VERIFIED means: model_info returned, config.json + tokenizer files actually
downloaded and AutoConfig/AutoTokenizer loaded them, repo not gated-without-access.
Weights are never downloaded here (only config/tokenizer, a few hundred KB).

Writes temp/panel_rows.json.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import (
    EntryNotFoundError,
    GatedRepoError,
    HfHubHTTPError,
    RepositoryNotFoundError,
)
from loguru import logger
from transformers import AutoConfig, AutoTokenizer

HERE = Path(__file__).resolve().parent
TEMP = HERE / "temp"
TEMP.mkdir(exist_ok=True)
CACHE = TEMP / "hf_cfg_cache"
CACHE.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs" / "panel.log", rotation="30 MB", level="DEBUG")

API = HfApi()

# ---------------------------------------------------------------- seed panel

# (repo_id, member_class, lineage_id, parent_repo_id, mirror_of)
SEEDS: list[tuple[str, str, str, str, str]] = [
    # --- Qwen3 0.6B lineage
    ("Qwen/Qwen3-0.6B-Base", "base", "Qwen/Qwen3-0.6B-Base", "", ""),
    ("Qwen/Qwen3-0.6B", "instruct", "Qwen/Qwen3-0.6B-Base", "Qwen/Qwen3-0.6B-Base", ""),
    ("huihui-ai/Qwen3-0.6B-abliterated", "abliterated", "Qwen/Qwen3-0.6B-Base", "Qwen/Qwen3-0.6B", ""),
    ("huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2", "abliterated", "Qwen/Qwen3-0.6B-Base", "Qwen/Qwen3-0.6B", ""),
    # --- Qwen3 1.7B lineage
    ("Qwen/Qwen3-1.7B-Base", "base", "Qwen/Qwen3-1.7B-Base", "", ""),
    ("Qwen/Qwen3-1.7B", "instruct", "Qwen/Qwen3-1.7B-Base", "Qwen/Qwen3-1.7B-Base", ""),
    ("huihui-ai/Qwen3-1.7B-abliterated", "abliterated", "Qwen/Qwen3-1.7B-Base", "Qwen/Qwen3-1.7B", ""),
    ("huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2", "abliterated", "Qwen/Qwen3-1.7B-Base", "Qwen/Qwen3-1.7B", ""),
    # --- Qwen3 4B lineage
    ("Qwen/Qwen3-4B-Base", "base", "Qwen/Qwen3-4B-Base", "", ""),
    ("Qwen/Qwen3-4B", "instruct", "Qwen/Qwen3-4B-Base", "Qwen/Qwen3-4B-Base", ""),
    ("huihui-ai/Qwen3-4B-abliterated", "abliterated", "Qwen/Qwen3-4B-Base", "Qwen/Qwen3-4B", ""),
    # --- Qwen2.5 0.5B lineage
    ("Qwen/Qwen2.5-0.5B", "base", "Qwen/Qwen2.5-0.5B", "", ""),
    ("Qwen/Qwen2.5-0.5B-Instruct", "instruct", "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-0.5B", ""),
    ("huihui-ai/Qwen2.5-0.5B-Instruct-abliterated", "abliterated", "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-0.5B-Instruct", ""),
    # --- Qwen2.5 1.5B lineage
    ("Qwen/Qwen2.5-1.5B", "base", "Qwen/Qwen2.5-1.5B", "", ""),
    ("Qwen/Qwen2.5-1.5B-Instruct", "instruct", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-1.5B", ""),
    ("huihui-ai/Qwen2.5-1.5B-Instruct-abliterated", "abliterated", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-1.5B-Instruct", ""),
    # --- Llama-3.2 1B lineage (canonical + ungated mirrors)
    ("meta-llama/Llama-3.2-1B", "base", "meta-llama/Llama-3.2-1B", "", ""),
    ("meta-llama/Llama-3.2-1B-Instruct", "instruct", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B", ""),
    ("unsloth/Llama-3.2-1B", "base", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B"),
    ("unsloth/Llama-3.2-1B-Instruct", "instruct", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B-Instruct", "meta-llama/Llama-3.2-1B-Instruct"),
    ("NousResearch/Llama-3.2-1B", "base", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B"),
    ("huihui-ai/Llama-3.2-1B-Instruct-abliterated", "abliterated", "meta-llama/Llama-3.2-1B", "meta-llama/Llama-3.2-1B-Instruct", ""),
    # --- Llama-3.2 3B lineage
    ("meta-llama/Llama-3.2-3B-Instruct", "instruct", "meta-llama/Llama-3.2-3B", "meta-llama/Llama-3.2-3B", ""),
    ("unsloth/Llama-3.2-3B-Instruct", "instruct", "meta-llama/Llama-3.2-3B", "meta-llama/Llama-3.2-3B-Instruct", "meta-llama/Llama-3.2-3B-Instruct"),
    ("huihui-ai/Llama-3.2-3B-Instruct-abliterated", "abliterated", "meta-llama/Llama-3.2-3B", "meta-llama/Llama-3.2-3B-Instruct", ""),
    # --- SmolLM2 lineages
    ("HuggingFaceTB/SmolLM2-135M", "base", "HuggingFaceTB/SmolLM2-135M", "", ""),
    ("HuggingFaceTB/SmolLM2-135M-Instruct", "instruct", "HuggingFaceTB/SmolLM2-135M", "HuggingFaceTB/SmolLM2-135M", ""),
    ("HuggingFaceTB/SmolLM2-360M", "base", "HuggingFaceTB/SmolLM2-360M", "", ""),
    ("HuggingFaceTB/SmolLM2-360M-Instruct", "instruct", "HuggingFaceTB/SmolLM2-360M", "HuggingFaceTB/SmolLM2-360M", ""),
    ("HuggingFaceTB/SmolLM2-1.7B", "base", "HuggingFaceTB/SmolLM2-1.7B", "", ""),
    ("HuggingFaceTB/SmolLM2-1.7B-Instruct", "instruct", "HuggingFaceTB/SmolLM2-1.7B", "HuggingFaceTB/SmolLM2-1.7B", ""),
    # --- TinyLlama lineage
    ("TinyLlama/TinyLlama_v1.1", "base", "TinyLlama/TinyLlama_v1.1", "", ""),
    ("TinyLlama/TinyLlama-1.1B-Chat-v1.0", "instruct", "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", ""),
    # --- Pythia lineages (base only; anchor the low-refusal end)
    ("EleutherAI/pythia-160m", "base", "EleutherAI/pythia-160m", "", ""),
    ("EleutherAI/pythia-410m", "base", "EleutherAI/pythia-410m", "", ""),
    ("EleutherAI/pythia-1b", "base", "EleutherAI/pythia-1b", "", ""),
    ("EleutherAI/pythia-1.4b", "base", "EleutherAI/pythia-1.4b", "", ""),
    # --- OLMo
    ("allenai/OLMo-1B-hf", "base", "allenai/OLMo-1B-hf", "", ""),
    # --- Danube3
    ("h2oai/h2o-danube3-500m-base", "base", "h2oai/h2o-danube3-500m-base", "", ""),
    ("h2oai/h2o-danube3-500m-chat", "instruct", "h2oai/h2o-danube3-500m-base", "h2oai/h2o-danube3-500m-base", ""),
    # --- Gemma-2 2B (gated) + ungated mirror
    ("google/gemma-2-2b", "base", "google/gemma-2-2b", "", ""),
    ("google/gemma-2-2b-it", "instruct", "google/gemma-2-2b", "google/gemma-2-2b", ""),
    ("unsloth/gemma-2-2b-it", "instruct", "google/gemma-2-2b", "google/gemma-2-2b-it", "google/gemma-2-2b-it"),
    ("huihui-ai/gemma-2-2b-it-abliterated", "abliterated", "google/gemma-2-2b", "google/gemma-2-2b-it", ""),
    # --- Falcon3 1B lineage
    ("tiiuae/Falcon3-1B-Base", "base", "tiiuae/Falcon3-1B-Base", "", ""),
    ("tiiuae/Falcon3-1B-Instruct", "instruct", "tiiuae/Falcon3-1B-Base", "tiiuae/Falcon3-1B-Base", ""),
    # --- Granite
    ("ibm-granite/granite-3.1-2b-instruct", "instruct", "ibm-granite/granite-3.1-2b-base", "ibm-granite/granite-3.1-2b-base", ""),
    ("ibm-granite/granite-3.1-2b-base", "base", "ibm-granite/granite-3.1-2b-base", "", ""),
    # --- MiniCPM
    ("openbmb/MiniCPM-1B-sft-bf16", "instruct", "openbmb/MiniCPM-1B-sft-bf16", "", ""),
    # --- behavioral-uncensored candidates (H4 class) - provenance checked below
    ("cognitivecomputations/TinyDolphin-2.8-1.1b", "behavioral_uncensored", "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T", ""),
    ("cognitivecomputations/dolphin-2_6-phi-2", "behavioral_uncensored", "microsoft/phi-2", "microsoft/phi-2", ""),
    ("Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2", "behavioral_uncensored", "meta-llama/Llama-3.1-8B", "meta-llama/Llama-3.1-8B-Instruct", ""),
    ("georgesung/llama2_7b_chat_uncensored", "behavioral_uncensored", "meta-llama/Llama-2-7b", "meta-llama/Llama-2-7b-chat-hf", ""),
    ("Undi95/Meta-Llama-3.1-8B-Claude", "other", "meta-llama/Llama-3.1-8B", "meta-llama/Llama-3.1-8B", ""),
]

# grep patterns that DISQUALIFY a model from the H4 behavioral-uncensored class
ABLIT_PAT = re.compile(
    r"abliterat|orthogonaliz|refusal[- ]direction|refusal direction|"
    r"remove[- ]refusals|failspy|ablat(?:ed|ion)|mergekit|"
    r"norm[- ]preserving|projection[- ]out",
    re.IGNORECASE,
)
# the card must make an explicit behavioural claim (trained/tuned to comply),
# not merely contain the word "dataset" or "dpo" somewhere
BEHAVIORAL_PAT = re.compile(
    r"toxic[-_ ]?dpo|uncensored|unfiltered|no[- ]refusal|without refusal|"
    r"will not refuse|does ?n[o']t refuse|compliant|no guardrails|no restrictions|"
    r"amoral|de[- ]?censor|removes? (?:the )?(?:censorship|guardrails|restrictions)",
    re.IGNORECASE,
)

# repo-name markers of things that are not a small causal-LM chat checkpoint
NON_LM_NAME = re.compile(
    r"\b(?:mt5|t5|bert|clip|whisper|wav2vec|vit|sd|sdxl|flux|diffusion|image|"
    r"vision|vl|ocr|embed|rerank|reward|tts|asr|blip|llava|qwen-?image)\b|"
    r"nf4|lora|quantiz|-4bit|-8bit|-fp8|z-image",
    re.IGNORECASE,
)

DISCOVERY_QUERIES = [
    "abliterated",
    "uncensored",
    "unfiltered",
    "toxic-dpo",
    "dolphin",
    "lexi",
    "amoral",
    "tiger-gemma",
    "josiefied",
    "orthogonalized",
]

TOKENIZER_FAMILY = [
    (re.compile(r"qwen3", re.I), "Qwen3"),
    (re.compile(r"qwen2|qwen_?2\.5|qwen", re.I), "Qwen2"),
    (re.compile(r"llama-?3|llama_3", re.I), "Llama-3"),
    (re.compile(r"tinyllama|llama-?2", re.I), "Llama-2"),
    (re.compile(r"smollm", re.I), "SmolLM2"),
    (re.compile(r"pythia|gpt-?neox|olmo", re.I), "GPT-NeoX"),
    (re.compile(r"gemma", re.I), "Gemma"),
    (re.compile(r"falcon", re.I), "Falcon3"),
    (re.compile(r"granite", re.I), "Granite"),
    (re.compile(r"danube|mistral", re.I), "Mistral"),
    (re.compile(r"minicpm", re.I), "MiniCPM"),
    (re.compile(r"phi", re.I), "Phi"),
]


def tok_family(repo: str, arch: str) -> str:
    for pat, name in TOKENIZER_FAMILY:
        if pat.search(repo) or pat.search(arch or ""):
            return name
    return "other"


def _params_from_index(info) -> tuple[int, int]:
    """Return (on_disk_bytes, param_count_estimate_from_bytes)."""
    total = 0
    for s in info.siblings or []:
        if s.rfilename.endswith((".safetensors", ".bin", ".pth")) and s.size:
            total += s.size
    return total, 0


def fetch_readme(repo: str) -> str:
    try:
        p = hf_hub_download(repo, "README.md", cache_dir=str(CACHE))
        return Path(p).read_text(errors="replace")
    except (EntryNotFoundError, RepositoryNotFoundError, GatedRepoError, HfHubHTTPError, OSError):
        return ""


def verify(repo: str, member_class: str, lineage: str, parent: str, mirror_of: str) -> dict:
    row: dict = {
        "hf_repo_id": repo,
        "member_class": member_class,
        "lineage_id": lineage,
        "parent_repo_id": parent,
        "mirror_of": mirror_of,
        "verified": False,
        "verify_error": "",
        "gated": False,
        "h4_status": "not_applicable",
        "h4_reason": "",
        "provenance_notes": "",
        "lineage_evidence": "",
        "model_card_url": f"https://huggingface.co/{repo}",
    }
    try:
        info = API.model_info(repo, files_metadata=True)
    except GatedRepoError as exc:
        row["gated"] = True
        row["verify_error"] = f"GatedRepoError: {str(exc)[:200]}"
        return row
    except Exception as exc:  # noqa: BLE001 - a failed candidate is data
        row["verify_error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        return row

    row["revision"] = info.sha
    row["downloads"] = info.downloads or 0
    row["likes"] = info.likes or 0
    row["gated"] = bool(info.gated)
    row["pipeline_tag"] = info.pipeline_tag or ""
    card = info.card_data.to_dict() if info.card_data else {}
    row["license"] = card.get("license") or ""
    on_disk, _ = _params_from_index(info)
    row["on_disk_bytes"] = on_disk
    if card.get("base_model") and not parent:
        bm = card["base_model"]
        row["parent_repo_id"] = bm[0] if isinstance(bm, list) and bm else (bm if isinstance(bm, str) else "")
        row["lineage_evidence"] = f"card_data.base_model={card.get('base_model')}"

    try:
        cfg = AutoConfig.from_pretrained(repo, revision=info.sha, cache_dir=str(CACHE), trust_remote_code=False)
    except Exception as exc:  # noqa: BLE001
        row["verify_error"] = f"AutoConfig: {type(exc).__name__}: {str(exc)[:200]}"
        return row
    row["architecture"] = (cfg.architectures or [cfg.model_type])[0] if hasattr(cfg, "architectures") else cfg.model_type
    row["model_type"] = cfg.model_type
    row["n_layers"] = getattr(cfg, "num_hidden_layers", None) or getattr(cfg, "n_layer", None)
    row["hidden_size"] = getattr(cfg, "hidden_size", None) or getattr(cfg, "n_embd", None)
    row["dtype"] = str(getattr(cfg, "torch_dtype", "") or getattr(cfg, "dtype", "") or "")
    row["vocab_size"] = getattr(cfg, "vocab_size", None)

    try:
        tk = AutoTokenizer.from_pretrained(repo, revision=info.sha, cache_dir=str(CACHE), trust_remote_code=False)
    except Exception as exc:  # noqa: BLE001
        row["verify_error"] = f"AutoTokenizer: {type(exc).__name__}: {str(exc)[:200]}"
        return row
    row["tokenizer_repo"] = repo
    row["tokenizer_family"] = tok_family(repo, row.get("architecture", ""))
    ct = getattr(tk, "chat_template", None)
    row["has_chat_template"] = bool(ct)
    row["chat_template_sha"] = __import__("hashlib").sha256(ct.encode()).hexdigest()[:16] if ct else ""
    row["tokenizer_vocab_size"] = len(tk)
    row["verified"] = True

    # param count from safetensors index metadata when available
    try:
        idx = hf_hub_download(repo, "model.safetensors.index.json", revision=info.sha, cache_dir=str(CACHE))
        meta = json.loads(Path(idx).read_text()).get("metadata", {})
        if meta.get("total_parameters"):
            row["param_count"] = int(meta["total_parameters"])
        elif meta.get("total_size"):
            row["param_count"] = int(meta["total_size"]) // 2
    except Exception:  # noqa: BLE001 - single-shard repos have no index
        pass
    if "param_count" not in row and on_disk:
        row["param_count"] = int(on_disk // 2)

    # ---- H4 provenance grep on the model card
    readme = fetch_readme(repo)
    row["readme_chars"] = len(readme)
    if member_class in ("behavioral_uncensored", "abliterated", "other"):
        hits = [m.group(0) for m in ABLIT_PAT.finditer(readme)]
        is_causal = str(row.get("architecture", "")).endswith("ForCausalLM")
        bh = BEHAVIORAL_PAT.search(readme)
        if member_class == "behavioral_uncensored":
            if not is_causal:
                row["h4_status"] = "not_applicable"
                row["h4_reason"] = f"architecture={row.get('architecture')} is not a causal LM"
            elif not bh:
                row["h4_status"] = "not_applicable"
                row["h4_reason"] = (
                    "name matched an uncensored-style keyword but the model card makes no explicit "
                    "uncensored / no-refusal / compliance claim; not a behavioural-uncensored checkpoint"
                )
            elif hits:
                ctx = ""
                m = ABLIT_PAT.search(readme)
                if m:
                    ctx = readme[max(0, m.start() - 120) : m.end() + 120].replace("\n", " ")
                row["h4_status"] = "disqualified_by_provenance"
                row["h4_reason"] = f"card matches {sorted(set(h.lower() for h in hits))[:5]}; quote: ...{ctx}..."
            else:
                row["h4_status"] = "candidate"
                ctx = readme[max(0, bh.start() - 120) : bh.end() + 120].replace("\n", " ")
                row["h4_reason"] = (
                    f"no abliteration/orthogonalization/mergekit marker in card; behavioural claim "
                    f"'{bh.group(0)}' in context: ...{ctx}..."
                )
        else:
            row["h4_status"] = "not_applicable"
            row["h4_reason"] = f"member_class={member_class}"
        row["provenance_notes"] = f"abliteration_markers={sorted(set(h.lower() for h in hits))[:8]}"
    return row


def discover() -> list[tuple[str, str, str, str, str]]:
    """Discovery pass: list_models for abliterated + behavioral-uncensored candidates."""
    found: dict[str, tuple[str, str, str, str, str]] = {}
    for q in DISCOVERY_QUERIES:
        try:
            models = list(API.list_models(search=q, sort="downloads", limit=80))
        except Exception as exc:  # noqa: BLE001
            logger.error(f"list_models(search={q!r}) failed: {exc}")
            continue
        logger.info(f"discovery query {q!r}: {len(models)} hits")
        for m in models:
            rid = m.id
            if rid in found:
                continue
            name = rid.lower()
            if re.search(r"abliterat|orthogonaliz", name):
                cls = "abliterated"
            elif re.search(r"uncensor|unfiltered|dolphin|lexi|amoral|josiefied|tiger", name):
                cls = "behavioral_uncensored"
            else:
                continue
            # keep only small models; the size filter is applied later on param_count
            if re.search(r"\b(70b|72b|65b|32b|34b|30b|27b|24b|22b|20b|14b|13b|12b)\b", name):
                continue
            if re.search(r"gguf|awq|gptq|exl2|mlx|onnx|int4|int8|w4a16|bnb", name):
                continue
            if NON_LM_NAME.search(name):
                continue
            if m.pipeline_tag and m.pipeline_tag != "text-generation":
                continue
            found[rid] = (rid, cls, "", "", "")
        time.sleep(0.2)
    logger.info(f"discovery produced {len(found)} candidate repos")
    return list(found.values())


def main() -> None:
    seeds = list(SEEDS)
    disc = discover()
    seen = {s[0] for s in seeds}
    disc = [d for d in disc if d[0] not in seen]
    # cap discovery work: verify seeds first, then discovery hits
    all_c = seeds + disc[:120]
    logger.info(f"verifying {len(all_c)} repos ({len(seeds)} seeded, {len(all_c)-len(seeds)} discovered)")

    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(verify, *c) for c in all_c]
        for i, f in enumerate(futs):
            try:
                rows.append(f.result())
            except Exception as exc:  # noqa: BLE001
                logger.error(f"verify future {i} raised: {exc}")
            if (i + 1) % 20 == 0:
                logger.info(f"  verified {i+1}/{len(futs)}")

    # ---- fill in lineage for discovered rows from card base_model, one level deep
    by_id = {r["hf_repo_id"]: r for r in rows}
    for r in rows:
        if r.get("lineage_id"):
            continue
        p = r.get("parent_repo_id") or ""
        chain = [r["hf_repo_id"]]
        seen_chain = set(chain)
        while p and p not in seen_chain:
            chain.append(p)
            seen_chain.add(p)
            nxt = by_id.get(p, {}).get("parent_repo_id", "")
            if not nxt:
                try:
                    pi = API.model_info(p)
                    pc = pi.card_data.to_dict() if pi.card_data else {}
                    bm = pc.get("base_model")
                    nxt = bm[0] if isinstance(bm, list) and bm else (bm if isinstance(bm, str) else "")
                except Exception:  # noqa: BLE001
                    nxt = ""
            p = nxt
        r["lineage_id"] = chain[-1]
        r["lineage_evidence"] = (r.get("lineage_evidence") or "") + f" | derivation chain: {' <- '.join(chain)}"

    (TEMP / "panel_rows.json").write_text(json.dumps(rows, indent=2, default=str))
    ok = [r for r in rows if r.get("verified")]
    lineages = {r["lineage_id"] for r in ok if r.get("lineage_id")}
    logger.info(f"TOTAL {len(rows)} rows | verified {len(ok)} | n_lineage {len(lineages)}")
    for cls in ("base", "instruct", "abliterated", "behavioral_uncensored", "other"):
        n = sum(1 for r in ok if r["member_class"] == cls)
        logger.info(f"  class {cls:<22} {n}")
    cand = [r for r in ok if r["h4_status"] == "candidate"]
    disq = [r for r in ok if r["h4_status"] == "disqualified_by_provenance"]
    logger.info(f"  H4 candidate={len(cand)} disqualified_by_provenance={len(disq)}")
    for r in cand:
        logger.info(f"    CANDIDATE {r['hf_repo_id']}: {r['h4_reason'][:120]}")


if __name__ == "__main__":
    main()
