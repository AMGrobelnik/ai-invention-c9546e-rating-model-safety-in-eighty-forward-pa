#!/usr/bin/env python3
"""Core harness: hardware detection, prompt blocks, generation, scoring, stats.

Imported by ``method.py``.  Contains no top-level side effects other than
logger configuration guards.
"""

from __future__ import annotations

import asyncio
import gc
import hashlib
import json
import math
import os
import resource
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np
import psutil
import torch
from loguru import logger

import prereg_spec as PS

WORKSPACE = Path(__file__).resolve().parent
DATA_RAW = WORKSPACE / "data_raw"
RESULTS = WORKSPACE / "results"
LADDER_DIR = WORKSPACE / "ladder_models"


# ==========================================================================
# Hardware
# ==========================================================================
def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError, IndexError):
        pass
    try:
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1


def _container_ram_gb() -> float | None:
    for p in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError):
            pass
    return None


NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
VRAM_GB = torch.cuda.get_device_properties(0).total_memory / 1e9 if HAS_GPU else 0.0
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9


def apply_resource_limits(ram_budget_gb: float = 48.0, vram_fraction: float = 0.85) -> dict:
    """Fail fast instead of OOM-killing the container."""
    avail = psutil.virtual_memory().available / 1e9
    ram_budget_gb = min(ram_budget_gb, max(4.0, avail * 0.7))
    try:
        limit = int(ram_budget_gb * 3 * 1024**3)
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except (ValueError, OSError) as exc:  # pragma: no cover - platform dependent
        logger.warning(f"could not set RLIMIT_AS: {exc}")
    if HAS_GPU:
        torch.cuda.set_per_process_memory_fraction(min(vram_fraction, 0.95), 0)
    info = {
        "num_cpus": NUM_CPUS,
        "has_gpu": HAS_GPU,
        "gpu_name": torch.cuda.get_device_name(0) if HAS_GPU else None,
        "vram_gb": round(VRAM_GB, 2),
        "total_ram_gb": round(TOTAL_RAM_GB, 2),
        "available_ram_gb": round(avail, 2),
        "ram_budget_gb": round(ram_budget_gb, 2),
        "torch": torch.__version__,
    }
    logger.info(f"hardware: {info}")
    return info


# ==========================================================================
# Small utilities
# ==========================================================================
def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def chunks(seq: Sequence, n: int) -> Iterable[Sequence]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def wilson_ci(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    """Wilson score 95% interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def rate_block(labels: Sequence[str], positive: str) -> dict:
    n = len(labels)
    k = sum(1 for x in labels if x == positive)
    lo, hi = wilson_ci(k, n)
    return {"rate": (k / n) if n else float("nan"), "k": k, "n": n, "ci95": [lo, hi]}


def ci_disjoint(a: dict, b: dict) -> bool:
    return a["ci95"][0] > b["ci95"][1] or b["ci95"][0] > a["ci95"][1]


def cohens_kappa(a: Sequence[int], b: Sequence[int]) -> float:
    """Cohen's kappa for two binary raters."""
    a = list(a)
    b = list(b)
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if abs(1.0 - pe) < 1e-12:
        return float("nan")
    return (po - pe) / (1 - pe)


def confusion(a: Sequence[str], b: Sequence[str], labels: Sequence[str]) -> dict:
    idx = {l: i for i, l in enumerate(labels)}
    m = [[0] * len(labels) for _ in labels]
    for x, y in zip(a, b):
        if x in idx and y in idx:
            m[idx[x]][idx[y]] += 1
    return {"labels": list(labels), "matrix": m}


def bootstrap_rate_ci(labels: Sequence[str], positive: str, n_boot: int = 2000,
                      seed: int = 0) -> list[float]:
    """Non-parametric bootstrap CI as a distributional cross-check on Wilson."""
    if not labels:
        return [float("nan"), float("nan")]
    rng = np.random.default_rng(seed)
    arr = np.array([1 if x == positive else 0 for x in labels], dtype=np.int8)
    draws = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    means = arr[draws].mean(axis=1)
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


# ==========================================================================
# Prompt blocks
# ==========================================================================
@dataclass
class PromptItem:
    item_id: str
    block: str
    prompt: str
    raw_prompt: str
    attack: str | None = None
    source_dataset: str = ""
    split: str = ""
    row_index: int = -1
    sha1: str = ""
    meta: dict = field(default_factory=dict)


def _first_six_words(s: str) -> str:
    return " ".join(s.lower().split()[:6])


def build_blocks() -> dict[str, list[PromptItem]]:
    """Build the four frozen prompt blocks from locally cached raw sources."""
    import pandas as pd

    # ---- Block A: plain-harmful (AdvBench) --------------------------------
    adv_path = DATA_RAW / "advbench_harmful_behaviors.csv"
    adv_source = "llm-attacks/llm-attacks:data/advbench/harmful_behaviors.csv"
    adv = pd.read_csv(adv_path)
    adv = adv.reset_index().rename(columns={"index": "row_index"})
    adv["sha1"] = adv["goal"].map(sha1)
    adv = adv.sort_values("sha1", kind="mergesort")

    seen_stems: set[str] = set()
    block_a: list[PromptItem] = []
    for _, row in adv.iterrows():
        stem = _first_six_words(row["goal"])
        if stem in seen_stems:
            continue
        seen_stems.add(stem)
        block_a.append(
            PromptItem(
                item_id=f"A{len(block_a):03d}",
                block="A_plain_harmful",
                prompt=row["goal"],
                raw_prompt=row["goal"],
                source_dataset=adv_source,
                split="all",
                row_index=int(row["row_index"]),
                sha1=row["sha1"],
                meta={"target": row["target"]},
            )
        )
        if len(block_a) >= PS.BLOCK_SIZES["A_plain_harmful"]:
            break
    if len(block_a) < PS.BLOCK_SIZES["A_plain_harmful"]:
        raise RuntimeError(f"block A short: {len(block_a)}")

    # ---- Block B: jailbreak (first 40 of block A, item-for-item paired) ---
    n_beh = PS.BLOCK_SIZES["B_jailbreak_behaviors"]
    block_b: list[PromptItem] = []
    for base_item in block_a[:n_beh]:
        for atk_name, tmpl in PS.ATTACK_TEMPLATES.items():
            block_b.append(
                PromptItem(
                    item_id=f"B_{atk_name}_{base_item.item_id}",
                    block="B_jailbreak",
                    prompt=tmpl.format(p=base_item.raw_prompt),
                    raw_prompt=base_item.raw_prompt,
                    attack=atk_name,
                    source_dataset=base_item.source_dataset,
                    split="all",
                    row_index=base_item.row_index,
                    sha1=base_item.sha1,
                    meta={"paired_item_id": base_item.item_id},
                )
            )

    # ---- Block C: XSTest safe + unsafe contrast --------------------------
    xs_path = DATA_RAW / "xstest_prompts.csv"
    xs_source = "paul-rottger/exaggerated-safety:xstest_prompts.csv"
    xs = pd.read_csv(xs_path).reset_index().rename(columns={"index": "row_index"})
    xs["sha1"] = xs["prompt"].map(sha1)

    def _stratified(df, want: int, tag: str) -> list[PromptItem]:
        by_type: dict[str, list] = {}
        for _, row in df.sort_values("sha1", kind="mergesort").iterrows():
            by_type.setdefault(row["type"], []).append(row)
        out, types = [], sorted(by_type)
        i = 0
        while len(out) < want:
            progressed = False
            for t in types:
                if i < len(by_type[t]) and len(out) < want:
                    out.append(by_type[t][i])
                    progressed = True
            if not progressed:
                break
            i += 1
        items = []
        for j, row in enumerate(out):
            items.append(
                PromptItem(
                    item_id=f"{tag}{j:03d}",
                    block="C_xstest_safe" if tag == "Cs" else "C_xstest_unsafe",
                    prompt=row["prompt"],
                    raw_prompt=row["prompt"],
                    source_dataset=xs_source,
                    split="prompts",
                    row_index=int(row["row_index"]),
                    sha1=row["sha1"],
                    meta={"type": row["type"], "label": row["label"],
                          "focus": row.get("focus"), "note": row.get("note")},
                )
            )
        return items

    safe = xs[xs["label"] == "safe"]
    unsafe = xs[xs["label"] == "unsafe"]
    block_c_safe = _stratified(safe, PS.BLOCK_SIZES["C_xstest_safe"], "Cs")
    block_c_unsafe = _stratified(unsafe, PS.BLOCK_SIZES["C_xstest_unsafe_contrast"], "Cu")
    if len(block_c_safe) < PS.BLOCK_SIZES["C_xstest_safe"]:
        raise RuntimeError(f"block C safe short: {len(block_c_safe)}")
    if len(block_c_unsafe) < PS.BLOCK_SIZES["C_xstest_unsafe_contrast"]:
        raise RuntimeError(f"block C unsafe short: {len(block_c_unsafe)}")

    # ---- Block E: neutral fluency prompts (ladder screen only) -----------
    block_e = [
        PromptItem(item_id=f"E{i:03d}", block="E_neutral", prompt=p, raw_prompt=p,
                   source_dataset="prereg.json:neutral_fluency_prompts", split="-",
                   row_index=i, sha1=sha1(p))
        for i, p in enumerate(PS.NEUTRAL_FLUENCY_PROMPTS)
    ]

    return {
        "A_plain_harmful": block_a,
        "B_jailbreak": block_b,
        "C_xstest_safe": block_c_safe,
        "C_xstest_unsafe": block_c_unsafe,
        "E_neutral": block_e,
    }


def load_wikitext_windows(tokenizer, n_windows: int, window: int) -> torch.Tensor:
    """Non-overlapping token windows from WikiText-2 test, identical for every model."""
    from datasets import load_dataset

    ds = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", split="test")
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    need_chars = n_windows * window * 8
    ids = tokenizer(text[:need_chars], return_tensors="pt", add_special_tokens=False)["input_ids"][0]
    usable = (len(ids) // window) * window
    if usable < window:
        raise RuntimeError("wikitext slice too short for one window")
    mat = ids[:usable].view(-1, window)
    return mat[:n_windows]


# ==========================================================================
# Prompt formatting
# ==========================================================================
class Formatter:
    """Applies the frozen template policy to a raw prompt."""

    def __init__(self, tokenizer, mode: str, enable_thinking: bool | None = None):
        self.tok = tokenizer
        self.mode = mode  # "chat" | "generic"
        self.enable_thinking = enable_thinking

    def __call__(self, prompt: str) -> str:
        if self.mode == "generic":
            return PS.GENERIC_WRAPPER.format(p=prompt)
        kwargs: dict[str, Any] = {"tokenize": False, "add_generation_prompt": True}
        if self.enable_thinking is not None:
            kwargs["enable_thinking"] = self.enable_thinking
        return self.tok.apply_chat_template([{"role": "user", "content": prompt}], **kwargs)

    def describe(self) -> str:
        if self.mode == "generic":
            return "generic_wrapper"
        return f"chat_template(enable_thinking={self.enable_thinking})"


# ==========================================================================
# Generation
# ==========================================================================
def load_model(path: str, dtype: torch.dtype | None = None):
    from transformers import AutoModelForCausalLM

    # float32 by default: fp16 batched greedy decoding is NOT batch-invariant
    # (measured: 3/4 completions identical at batch=4 vs batch=1 in fp16, 4/4 in
    # fp32).  Every member here is <=1B, so fp32 fits comfortably in 20GB and buys
    # exact determinism, which the T1 assertion depends on.
    dtype = dtype or torch.float32
    try:
        model = AutoModelForCausalLM.from_pretrained(path, dtype=dtype)
    except TypeError:  # older transformers
        model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=dtype)
    model.to(DEVICE)
    model.eval()
    return model


def load_tokenizer(path: str):
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"
    return tok


@torch.no_grad()
def generate_batched(model, tok, texts: Sequence[str], *, max_new_tokens: int,
                     batch_size: int, do_sample: bool = False,
                     temperature: float | None = None,
                     seed: int | None = None) -> tuple[list[str], float]:
    """Greedy (or sampled) batched generation with left padding.  Returns (completions, seconds)."""
    tok.padding_side = "left"
    out_texts: list[str] = []
    t0 = time.time()
    bs = batch_size
    i = 0
    while i < len(texts):
        batch = list(texts[i : i + bs])
        try:
            enc = tok(batch, return_tensors="pt", padding=True, add_special_tokens=False)
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            gen_kwargs: dict[str, Any] = dict(
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                pad_token_id=tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id,
            )
            if do_sample:
                gen_kwargs["temperature"] = temperature
                if seed is not None:
                    torch.manual_seed(seed + i)
            out = model.generate(**enc, **gen_kwargs)
            new = out[:, enc["input_ids"].shape[1] :]
            out_texts.extend(tok.batch_decode(new, skip_special_tokens=True))
            i += bs
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
            logger.warning(f"CUDA OOM -> batch_size={bs}")
    return out_texts, time.time() - t0


@torch.no_grad()
def perplexity(model, windows: torch.Tensor, batch_size: int = 8) -> float:
    """Teacher-forced perplexity over fixed non-overlapping token windows."""
    total_nll, total_tok = 0.0, 0
    for i in range(0, windows.shape[0], batch_size):
        ids = windows[i : i + batch_size].to(DEVICE)
        out = model(input_ids=ids)
        logits = out.logits[:, :-1, :].float()
        targets = ids[:, 1:]
        nll = torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="sum"
        )
        total_nll += float(nll.item())
        total_tok += int(targets.numel())
        del out, logits, ids
    return float(math.exp(total_nll / max(1, total_tok)))


def free_model(model) -> None:
    del model
    gc.collect()
    if HAS_GPU:
        torch.cuda.empty_cache()


# ==========================================================================
# Fluency statistics
# ==========================================================================
def _ngrams(tokens: Sequence[str], n: int) -> list[tuple]:
    return [tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1))]


def distinct_n(texts: Sequence[str], n: int = 3) -> float:
    total, uniq = 0, set()
    for t in texts:
        g = _ngrams(t.split(), n)
        total += len(g)
        uniq.update(g)
    return len(uniq) / total if total else 0.0


def max_ngram_repeat_frac(texts: Sequence[str], n: int = 4) -> float:
    """Per-text max fraction of 4-grams taken by the single most repeated 4-gram; averaged."""
    fracs = []
    for t in texts:
        g = _ngrams(t.split(), n)
        if not g:
            fracs.append(1.0)
            continue
        counts: dict[tuple, int] = {}
        for x in g:
            counts[x] = counts.get(x, 0) + 1
        fracs.append(max(counts.values()) / len(g))
    return float(np.mean(fracs)) if fracs else 1.0


# ==========================================================================
# Stage 5a: refusal-string screen (BASELINE scorer)
# ==========================================================================
def screen_refusal(completion: str) -> bool:
    c = completion.lstrip()
    low = c.lower()
    head = low[:120]
    for p in PS.REFUSAL_PREFIXES:
        pl = p.lower()
        if low.startswith(pl) or pl in head:
            return True
    return False


# ==========================================================================
# Stage 5b: OpenRouter LLM judge (PRIMARY scorer)
# ==========================================================================
class BudgetExceeded(RuntimeError):
    pass


class Judge:
    """Async OpenRouter judge with content-hash cache and hard cost abort."""

    URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, model: str, api_key: str, cache_path: Path,
                 hard_abort_usd: float = PS.BUDGET_USD_HARD_ABORT,
                 concurrency: int = 12,
                 price_in_per_m: float = 0.0, price_out_per_m: float = 0.0,
                 system: str | None = None, max_tokens: int = 8):
        self.system = system
        self.max_tokens = max_tokens
        self.model = model
        self.api_key = api_key
        self.cache_path = cache_path
        self.hard_abort_usd = hard_abort_usd
        self.concurrency = concurrency
        self.price_in = price_in_per_m
        self.price_out = price_out_per_m
        self.cost_usd = 0.0
        self.n_calls = 0
        self.n_cache_hits = 0
        self.n_parse_failures = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.cache: dict[str, str] = {}
        if cache_path.exists():
            for line in cache_path.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.cache[rec["key"]] = rec["label"]
            logger.info(f"judge cache loaded: {len(self.cache)} entries")
        self._fh = cache_path.open("a")
        self._lock = asyncio.Lock()

    @staticmethod
    def key_for(prompt: str, completion: str) -> str:
        return sha1(prompt + "\x00" + completion)

    @staticmethod
    def parse_label(text: str) -> tuple[str, bool]:
        """Map raw judge output onto a frozen label.  Returns (label, parsed_cleanly)."""
        up = (text or "").strip().upper()
        for lab in PS.JUDGE_LABELS:
            if up == lab or up.startswith(lab):
                return lab, True
        hits = [lab for lab in PS.JUDGE_LABELS if lab in up]
        if len(hits) == 1:
            return hits[0], False
        if not up:
            return "DEGENERATE", False
        return "DEGENERATE", False

    @staticmethod
    def render_rubric(prompt: str, completion: str) -> str:
        """Substitute into the frozen rubric.

        ``str.format`` cannot be used: the rubric contains the literal label set
        ``{REFUSAL, COMPLIANCE, PARTIAL, DEGENERATE}``, which format() would try
        to interpret as a replacement field.
        """
        return (PS.JUDGE_RUBRIC
                .replace("{prompt}", prompt)
                .replace("{completion}", completion))

    async def _one(self, session, sem, prompt: str, completion: str) -> str:
        key = self.key_for(prompt, completion)
        if key in self.cache:
            self.n_cache_hits += 1
            return self.cache[key]
        messages = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.render_rubric(prompt, completion)})
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "max_tokens": self.max_tokens,
            "usage": {"include": True},
        }
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        last_exc: Exception | None = None
        async with sem:
            for attempt in range(5):
                if self.cost_usd > self.hard_abort_usd:
                    raise BudgetExceeded(f"cost {self.cost_usd:.4f} > {self.hard_abort_usd}")
                try:
                    async with session.post(self.URL, json=body, headers=headers,
                                            timeout=90) as resp:
                        if resp.status in (429, 500, 502, 503, 529):
                            await asyncio.sleep(2 ** attempt + 0.5)
                            continue
                        data = await resp.json()
                    if "error" in data and "choices" not in data:
                        last_exc = RuntimeError(str(data["error"])[:200])
                        await asyncio.sleep(2 ** attempt)
                        continue
                    txt = data["choices"][0]["message"]["content"]
                    usage = data.get("usage") or {}
                    cost = usage.get("cost")
                    ti = int(usage.get("prompt_tokens", 0) or 0)
                    to = int(usage.get("completion_tokens", 0) or 0)
                    if cost is None:
                        cost = ti / 1e6 * self.price_in + to / 1e6 * self.price_out
                    label, clean = self.parse_label(txt)
                    async with self._lock:
                        self.cost_usd += float(cost)
                        self.n_calls += 1
                        self.tokens_in += ti
                        self.tokens_out += to
                        if not clean:
                            self.n_parse_failures += 1
                        self.cache[key] = label
                        self._fh.write(json.dumps({
                            "key": key, "label": label, "raw": (txt or "")[:200],
                            "clean_parse": clean, "cost": float(cost),
                            "tokens_in": ti, "tokens_out": to}) + "\n")
                        self._fh.flush()
                        if self.n_calls % 50 == 0:
                            logger.info(f"judge: {self.n_calls} calls, "
                                        f"${self.cost_usd:.4f} cumulative")
                    return label
                except BudgetExceeded:
                    raise
                except Exception as exc:  # noqa: BLE001 - transient network/API
                    last_exc = exc
                    await asyncio.sleep(2 ** attempt)
        raise RuntimeError(f"judge failed after retries: {last_exc}")

    async def judge_many(self, pairs: Sequence[tuple[str, str]]) -> list[str | None]:
        import aiohttp

        sem = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            tasks = [self._one(session, sem, p, c) for p, c in pairs]
            res = await asyncio.gather(*tasks, return_exceptions=True)
        out: list[str | None] = []
        for r in res:
            if isinstance(r, BaseException):
                logger.error(f"judge item failed: {type(r).__name__}: {str(r)[:150]}")
                out.append(None)
            else:
                out.append(r)
        return out

    def run(self, pairs: Sequence[tuple[str, str]]) -> list[str | None]:
        return asyncio.run(self.judge_many(pairs))

    def close(self) -> None:
        try:
            self._fh.close()
        except OSError:
            pass


def load_api_key() -> str:
    for p in (Path("/ai-inventor/.env"), WORKSPACE / ".env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v:
                        return v
    v = os.environ.get("OPENROUTER_API_KEY", "")
    if not v:
        raise RuntimeError("OPENROUTER_API_KEY not found")
    return v
