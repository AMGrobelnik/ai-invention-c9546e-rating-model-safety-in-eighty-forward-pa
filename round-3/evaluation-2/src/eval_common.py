#!/usr/bin/env python3
"""Shared loaders, paths and statistics helpers for the iteration-3 reanalysis.

Pure reanalysis: every number is derived from files already on disk in the
frozen iteration-1 / iteration-2 result trees. No model loading, no GPU, no
API calls.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parent
OUT = WS / "out"
ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")

E1 = ROOT / "iter_2/gen_art/gen_art_experiment_1"
E2 = ROOT / "iter_2/gen_art/gen_art_experiment_2"
E3 = ROOT / "iter_2/gen_art/gen_art_experiment_3"
V1 = ROOT / "iter_2/gen_art/gen_art_evaluation_1"
T0 = ROOT / "iter_1/gen_art/gen_art_experiment_1"

# The archived estimator library is imported VERBATIM (numpy/scipy only modules).
sys.path.insert(0, str(E2))

BOOT_SEED = 20260812  # overwritten below from the archived module
N_BOOT_LINEAGE = 5000
N_BOOT_ROLLOUT = 2000

_MANIFEST: dict[str, dict] = {}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def register(path: Path) -> Path:
    """Record a file in the inputs manifest the first time it is read."""
    p = Path(path)
    key = str(p)
    if key not in _MANIFEST:
        st = p.stat()
        _MANIFEST[key] = {
            "sha256": sha256_of(p),
            "bytes": st.st_size,
            "mtime_utc": st.st_mtime,
        }
    return p


def load_json(path: Path):
    return json.loads(register(Path(path)).read_text())


def load_jsonl(path: Path):
    rows = []
    with open(register(Path(path))) as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def manifest() -> dict:
    return dict(_MANIFEST)


# ---------------------------------------------------------------- statistics


def spearman_rho(x, y) -> float | None:
    from scipy.stats import rankdata

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3:
        return None
    rx, ry = rankdata(x), rankdata(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def wilson_ci(k: int, n: int, z: float = 1.959963985) -> list[float]:
    if n <= 0:
        return [float("nan"), float("nan")]
    p = k / n
    d = 1.0 + z * z / n
    c = p + z * z / (2 * n)
    hw = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [float(max(0.0, (c - hw) / d)), float(min(1.0, (c + hw) / d))]


def cliffs_delta(a, b, n_boot: int = 2000, seed: int = 12345) -> dict:
    """Paired Cliff's delta (a vs b) with a paired bootstrap CI over pairs."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n = len(a)

    def _d(u, v):
        gt = np.sum(u[:, None] > v[None, :])
        lt = np.sum(u[:, None] < v[None, :])
        return float((gt - lt) / (len(u) * len(v)))

    point = _d(a, b)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot.append(_d(a[idx], b[idx]))
    return {
        "delta": point,
        "ci": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
        "n_pairs": int(n),
        "n_boot": int(n_boot),
    }


def auc_from_scores(scores, labels) -> float | None:
    """Mann-Whitney AUC with ties handled at 0.5. labels in {0,1}."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    gt = np.sum(pos[:, None] > neg[None, :])
    eq = np.sum(pos[:, None] == neg[None, :])
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


def holm(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m, dtype=float)
    running = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * pvals[i]
        running = max(running, val)
        adj[i] = min(1.0, running)
    return [float(v) for v in adj]


def finite(x):
    """Recursively replace non-finite floats with None."""
    if isinstance(x, dict):
        return {k: finite(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [finite(v) for v in x]
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return v if np.isfinite(v) else None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x
