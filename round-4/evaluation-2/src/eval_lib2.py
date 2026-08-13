#!/usr/bin/env python3
"""Shared helpers for the degeneracy-screen re-adjudication of the A-vs-B reversal.

Pure re-analysis of archived artifacts.  Every outcome-defining code path (the
fluency/degeneracy screen, the refusal-onset regex, the judge client and its two
rubrics) is IMPORTED from the archive rather than re-implemented.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Archive layout
# ---------------------------------------------------------------------------
ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
ARCH = ROOT / "iter_2/gen_art/gen_art_experiment_1"          # 45,900 steered gens
EXP2 = ROOT / "iter_2/gen_art/gen_art_experiment_2"          # breadth panel + judge lib
AUD = ROOT / "iter_2/gen_art/gen_art_experiment_3"           # judge audit (se/sp)
RE3 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"           # matched-contrast + 5-class
DATASET = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
FIGS = HERE / "figures"

CHECKPOINTS = [
    "instruct_0p6", "base_0p6", "abliterated_0p6",
    "instruct_1p7", "base_1p7", "abliterated_1p7",
]
# axes carried through the full pipeline (judging + rates)
AXES_CORE = ["A_canned", "B_paraphrase", "C_stylistic", "D_random0"]
# axes carried through the (judge-free) retention curves only
AXES_ALL = ["A_canned", "B_paraphrase", "C_stylistic",
            "D_random0", "D_random1", "D_random2", "E_prompt_contrast"]
CONTROL_AXES = ["C_stylistic", "D_random0"]

MODEL_CFG = {   # verbatim from ARCH/method.py MODELS
    "base_0p6": {"repo": "Qwen/Qwen3-0.6B-Base", "render": "plain"},
    "instruct_0p6": {"repo": "Qwen/Qwen3-0.6B", "render": "chatml"},
    "abliterated_0p6": {"repo": "mlabonne/Qwen3-0.6B-abliterated", "render": "chatml"},
    "base_1p7": {"repo": "Qwen/Qwen3-1.7B-Base", "render": "plain"},
    "instruct_1p7": {"repo": "Qwen/Qwen3-1.7B", "render": "chatml"},
    "abliterated_1p7": {"repo": "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2",
                        "render": "chatml"},
}

# Pre-registered constants (stamped in results/prereg_eval.json before any label)
HARD_CAP_USD = 1.50
N_BOOT = 5000
BOOT_SEED = 20260812
SAMPLE_SEED = 4242
PER_CELL_TARGET = 100          # = judge every screen-passing row in the cell
PER_CELL_MIN = 12              # below this a cell is UNDERPOWERED
SCREEN_AGREEMENT_FLOOR = 0.99  # recomputed screen adopted as primary iff >= this
DEGEN_SURVIVES_MAX = 0.40      # verdict clause (c)
DEGEN_FAILS_MIN = 0.60         # verdict clause for DOES_NOT_SURVIVE
NET_CI_HALFWIDTH_MAX = 0.25    # verdict UNDERPOWERED clause


# ---------------------------------------------------------------------------
# Archive code import (verbatim reuse)
# ---------------------------------------------------------------------------
def import_arch_classify():
    """ARCH/classify.py -- the frozen fluency/degeneracy screen of record.

    classify.py does `import torch` at module scope purely for the r_t observable
    (RefusalClassifier), which this artifact does not use: no weights are loaded
    and no forward pass is run.  torch is therefore satisfied with an empty stub
    module so that the screen functions (distinct_n / max_ngram_repeat /
    fluency_ok) are executed from the archive's own bytes, unmodified.
    """
    stubbed = False
    if "torch" not in sys.modules:
        try:
            import torch  # noqa: F401
        except ImportError:
            import types
            stub = types.ModuleType("torch")
            stub.Tensor = type("Tensor", (), {})       # scipy probes torch.Tensor
            stub.long = "int64"
            sys.modules["torch"] = stub
            stubbed = True
    if str(ARCH) not in sys.path:
        sys.path.insert(0, str(ARCH))
    import classify as CL  # noqa: N812
    if stubbed:
        # withdraw the stub: scipy and transformers both probe sys.modules for a
        # real torch and a half-module confuses them. classify keeps its own
        # reference, which only RefusalClassifier (unused here) ever touches.
        sys.modules.pop("torch", None)
    return CL


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def import_arch_judge_modules():
    """Return (judge4, judge5): two independent module objects loaded from
    ARCH/judge.py.  judge4 keeps the frozen FOUR-class rubric verbatim; judge5 has
    its module globals swapped for the RE3 FIVE-class rubric verbatim, so the HTTP
    client, cache, retry and cost accounting are byte-identical between them."""
    if str(ARCH) not in sys.path:
        sys.path.insert(0, str(ARCH))
    j4 = _load_module("arch_judge4", ARCH / "judge.py")
    j5 = _load_module("arch_judge5", ARCH / "judge.py")

    a4_labels, a4_rubric = import_re3_five_class()
    j5.JUDGE_LABELS = a4_labels
    j5.JUDGE_RUBRIC = a4_rubric

    def render5(prompt: str, completion: str) -> str:
        return a4_rubric.replace("{prompt}", prompt).replace("{completion}", completion)

    def parse5(text: str):
        up = (text or "").strip().upper()
        for lab in a4_labels:
            if up == lab or up.startswith(lab):
                return lab, True
        hits = [lab for lab in a4_labels if lab in up]
        if len(hits) == 1:
            return hits[0], False
        if "REFUS" in up:
            return "REFUSAL_NONCANONICAL", False
        return "DEGENERATE", False

    j5.render_rubric = render5
    j5.parse_label = parse5
    return j4, j5


def import_re3_five_class() -> tuple[list[str], str]:
    """Pull A4_LABELS / A4_RUBRIC verbatim out of RE3/judge_stage.py without
    executing its heavy imports (torch-free parse of the source)."""
    src = (RE3 / "judge_stage.py").read_text()
    ns: dict = {}
    lines = src.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("A4_LABELS"))
    end = next(i for i, ln in enumerate(lines[start:], start)
               if ln.startswith(")") and i > start) + 1
    exec("\n".join(lines[start:end]), ns)   # noqa: S102 -- archive source, verbatim
    return ns["A4_LABELS"], ns["A4_RUBRIC"]


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path):
    with open(p) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def load_json(p: Path):
    return json.loads(Path(p).read_text())


def dump_json(p: Path, obj) -> None:
    Path(p).write_text(json.dumps(obj, indent=1, default=_jdefault))


def _jdefault(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"not serialisable: {type(o)}")


def gens_path(member: str, axis: str) -> Path:
    return ARCH / f"gens/{member}__{axis}.jsonl"


def prompt_lookup() -> dict:
    """prompt_uid -> prompt text.  ARCH/results/prompts.json is the frozen probe
    block ARCH itself used for judge-item construction; it is derived from
    iter_1 gen_art_dataset_1 full_data_out.json (harmless_dynamics)."""
    doc = load_json(ARCH / "results/prompts.json")
    return {p["uid"]: p["text"] for p in doc["probe_prompts"]}


def jp(rel: str, ptr: str) -> str:
    return f"{rel}#{ptr}"


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    from scipy.stats import beta
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return (lo, hi)


def one_sided_upper(k: int, n: int, alpha: float = 0.05) -> float:
    """Clopper-Pearson one-sided 95% UPPER bound -- the achievable bound reported
    when a cell is UNDERPOWERED."""
    from scipy.stats import beta
    if n == 0:
        return float("nan")
    return 1.0 if k == n else float(beta.ppf(1 - alpha, k + 1, n - k))


def boot_ci(vals: np.ndarray, lo: float = 2.5, hi: float = 97.5):
    v = np.asarray(vals, float)
    v = v[np.isfinite(v)]
    if v.size < 20:
        return (float("nan"), float("nan"))
    return (float(np.percentile(v, lo)), float(np.percentile(v, hi)))


def cluster_resample_matrix(clusters: list[str], n_boot: int, seed: int) -> np.ndarray:
    """(n_boot, n_clusters) integer multiplicity matrix over the unique clusters."""
    rng = np.random.default_rng(seed)
    uniq = sorted(set(clusters))
    m = len(uniq)
    picks = rng.integers(0, m, size=(n_boot, m))
    mult = np.zeros((n_boot, m), dtype=np.int64)
    for b in range(n_boot):
        np.add.at(mult[b], picks[b], 1)
    return mult


def rate_from_counts(k_by_cluster: np.ndarray, n_by_cluster: np.ndarray,
                     mult: np.ndarray) -> np.ndarray:
    """Bootstrap replicates of a rate under cluster resampling."""
    num = mult @ k_by_cluster
    den = mult @ n_by_cluster
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / np.maximum(den, 1e-12), np.nan)


def cohens_kappa(a: list, b: list) -> dict:
    a, b = list(a), list(b)
    n = len(a)
    if n == 0:
        return {"kappa": float("nan"), "n": 0}
    cats = sorted(set(a) | set(b))
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    exp = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    k = (obs - exp) / (1 - exp) if abs(1 - exp) > 1e-12 else 0.0
    return {"kappa": float(k), "n": n, "observed_agreement": float(obs),
            "expected_agreement": float(exp)}


def rogan_gladen(obs: float, sens: float, spec: float) -> tuple[float, bool]:
    """Return (corrected prevalence truncated to [0,1], truncation_bit)."""
    den = sens + spec - 1.0
    if not np.isfinite(obs) or not np.isfinite(den) or abs(den) < 1e-9:
        return (float("nan"), False)
    raw = (obs - (1.0 - spec)) / den
    tr = bool(raw < 0.0 or raw > 1.0)
    return (float(min(1.0, max(0.0, raw))), tr)


def rogan_gladen_vec(obs: np.ndarray, sens: float, spec: float) -> np.ndarray:
    den = sens + spec - 1.0
    if abs(den) < 1e-9:
        return np.full_like(np.asarray(obs, float), np.nan)
    return np.clip((np.asarray(obs, float) - (1.0 - spec)) / den, 0.0, 1.0)
