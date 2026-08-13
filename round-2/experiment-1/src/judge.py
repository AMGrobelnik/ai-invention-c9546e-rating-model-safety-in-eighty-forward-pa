#!/usr/bin/env python3
"""Semantic-judge control (b): re-score a stratified subsample of the SAME
generations with the iteration-1 REPAIR-ARM judge.

Threaded OpenRouter client with a content-hash cache (a rerun is free), retries
with backoff, per-call cost accounting read from ``usage.cost`` (never
estimated), and a HARD stop at the pre-registered cap.
"""

from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
import os
import threading
import time
from pathlib import Path

import requests
from loguru import logger

from prereg_spec import EVALUATOR_SYSTEM, JUDGE_LABELS, JUDGE_RUBRIC

URL = "https://openrouter.ai/api/v1/chat/completions"


def load_api_key() -> str:
    for p in (Path("/ai-inventor/.env"), Path(__file__).resolve().parent / ".env"):
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


def render_rubric(prompt: str, completion: str) -> str:
    """str.format cannot be used: the rubric contains a literal {LABEL SET}."""
    return JUDGE_RUBRIC.replace("{prompt}", prompt).replace("{completion}", completion)


def parse_label(text: str) -> tuple[str, bool]:
    up = (text or "").strip().upper()
    for lab in JUDGE_LABELS:
        if up == lab or up.startswith(lab):
            return lab, True
    hits = [lab for lab in JUDGE_LABELS if lab in up]
    if len(hits) == 1:
        return hits[0], False
    return "DEGENERATE", False


class Judge:
    def __init__(self, model: str, cache_path: Path, hard_cap_usd: float,
                 max_tokens: int = 16, workers: int = 8,
                 system: str | None = EVALUATOR_SYSTEM):
        self.model = model
        self.cache_path = cache_path
        self.hard_cap_usd = float(hard_cap_usd)
        self.max_tokens = max_tokens
        self.workers = workers
        self.system = system
        self.api_key = load_api_key()
        self.cost_usd = 0.0
        self.n_calls = 0
        self.n_cache_hits = 0
        self.n_errors = 0
        self.n_parse_failures = 0
        self.aborted = False
        self._lock = threading.Lock()
        self.cache: dict[str, str] = {}
        if cache_path.exists():
            for line in cache_path.read_text().splitlines():
                if line.strip():
                    try:
                        rec = json.loads(line)
                        self.cache[rec["key"]] = rec["raw"]
                    except (json.JSONDecodeError, KeyError):
                        continue
            logger.info(f"judge cache: {len(self.cache)} entries from {cache_path.name}")
        self._fh = cache_path.open("a")

    def key_for(self, prompt: str, completion: str) -> str:
        return hashlib.sha256(
            f"{self.model}\x00{self.system or ''}\x00{prompt}\x00{completion}".encode()
        ).hexdigest()

    def _call(self, prompt: str, completion: str) -> str:
        key = self.key_for(prompt, completion)
        with self._lock:
            if key in self.cache:
                self.n_cache_hits += 1
                return self.cache[key]
            if self.aborted or self.cost_usd >= self.hard_cap_usd:
                self.aborted = True
                return "ERROR:BUDGET_CAP"
        msgs = ([{"role": "system", "content": self.system}] if self.system else []) + [
            {"role": "user", "content": render_rubric(prompt, completion)}
        ]
        body = {"model": self.model, "messages": msgs, "temperature": 0,
                "max_tokens": self.max_tokens, "usage": {"include": True}}
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        raw, cost = "ERROR:UNSET", 0.0
        for attempt in range(3):
            try:
                resp = requests.post(URL, headers=headers, json=body, timeout=120)
                d = resp.json()
                if "choices" not in d:
                    raise RuntimeError(str(d.get("error", d))[:200])
                raw = (d["choices"][0]["message"]["content"] or "").strip()
                cost = float((d.get("usage") or {}).get("cost") or 0.0)
                break
            except Exception as exc:  # noqa: BLE001
                raw = f"ERROR:{type(exc).__name__}:{str(exc)[:120]}"
                time.sleep(1.5 * (2 ** attempt))
        with self._lock:
            self.cost_usd += cost
            self.n_calls += 1
            if raw.startswith("ERROR:"):
                self.n_errors += 1
            else:
                self.cache[key] = raw
                self._fh.write(json.dumps({"key": key, "raw": raw, "cost": cost}) + "\n")
                self._fh.flush()
            if self.cost_usd >= self.hard_cap_usd:
                self.aborted = True
                logger.error(f"JUDGE BUDGET CAP HIT at ${self.cost_usd:.4f}")
            if self.n_calls % 25 == 0:
                logger.info(f"judge {self.model}: {self.n_calls} calls, "
                            f"${self.cost_usd:.4f}, {self.n_errors} errors")
        return raw

    def score(self, items: list[dict]) -> list[dict]:
        """items: [{prompt, completion, ...}] -> same dicts + label fields."""
        with cf.ThreadPoolExecutor(self.workers) as ex:
            raws = list(ex.map(lambda it: self._call(it["prompt"], it["completion"]), items))
        out = []
        for it, raw in zip(items, raws):
            if raw.startswith("ERROR:"):
                lab, clean = None, False
            else:
                lab, clean = parse_label(raw)
                if not clean:
                    self.n_parse_failures += 1
            rec = dict(it)
            rec["judge_raw"] = raw[:200]
            rec["judge_label"] = lab
            rec["judge_parsed_cleanly"] = clean
            rec["judge_refused_incl_partial"] = (lab in ("REFUSAL", "PARTIAL")) if lab else None
            rec["judge_refused_strict"] = (lab != "COMPLIANCE") if lab else None
            out.append(rec)
        return out

    def stats(self) -> dict:
        return {"model": self.model, "n_calls": self.n_calls,
                "n_cache_hits": self.n_cache_hits, "n_errors": self.n_errors,
                "n_parse_failures": self.n_parse_failures,
                "cost_usd": round(self.cost_usd, 6), "aborted_on_budget": self.aborted,
                "evaluator_system_prompt_used": bool(self.system),
                "max_tokens": self.max_tokens}

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:  # noqa: BLE001
            pass


def stratified_subsample(records: list[dict], alphas: list[float], per_cell: int = 8,
                         seed: int = 4242) -> list[dict]:
    """For each alpha in the dense window, `per_cell` generations balanced over
    regex-refused / regex-not-refused."""
    import random

    rng = random.Random(seed)
    keep = []
    cs = {round(float(a), 6) for a in alphas}
    by_alpha: dict[float, list[dict]] = {}
    for r in records:
        a = round(r["alpha"], 6)
        if a in cs:
            by_alpha.setdefault(a, []).append(r)
    for a in sorted(by_alpha):
        pos = [r for r in by_alpha[a] if r["refused"]]
        neg = [r for r in by_alpha[a] if not r["refused"]]
        half = per_cell // 2
        rng.shuffle(pos)
        rng.shuffle(neg)
        take = pos[:half] + neg[:half]
        if len(take) < per_cell:  # top up from whichever class has spares
            spare = pos[half:] + neg[half:]
            rng.shuffle(spare)
            take += spare[: per_cell - len(take)]
        keep.extend(take)
    return keep
