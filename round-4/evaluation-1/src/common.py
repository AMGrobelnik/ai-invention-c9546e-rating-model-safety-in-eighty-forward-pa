#!/usr/bin/env python3
"""Shared paths, logging, IO and the archived-estimator import for the
dual-aggregation reanalysis.

HARD RULE 1 of the artifact plan: definitions do not drift. The estimator code
is IMPORTED from the frozen iteration-3 archive rather than re-implemented. The
plan named the module `lib/stats_ext.py`; the functions it lists (orient,
spearman_basic, clustered_bootstrap_rho, lineage_permutation_p,
loo_lineage_jackknife, auc_binary, paired_rho_delta_clustered, disattenuate,
spearman_pair) actually live in `lib_iter3/statsx.py`. Both modules are
sha256-stamped and the correction is recorded in the output.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
TABLES = OUT / "tables"
LOGS = HERE / "logs"
for _d in (OUT, TABLES, LOGS):
    _d.mkdir(parents=True, exist_ok=True)

ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
E3 = ROOT / "iter_3/gen_art/gen_art_experiment_1"
V1 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"
V2 = ROOT / "iter_3/gen_art/gen_art_evaluation_2"
A2_EXP2 = ROOT / "iter_2/gen_art/gen_art_experiment_2"
A2_EXP1 = ROOT / "iter_2/gen_art/gen_art_experiment_1"
D1 = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
DRAFT = ROOT / "iter_3/gen_paper_text/gen_paper_text/paper_body.md"

# The archived estimator library. E3/method.py imports torch at module level and
# is therefore NOT import-safe under this artifact's zero-GPU / no-torch rule;
# the fallback route mandated by the plan (read the literal constant blocks) is
# used for PASS_RULES / ORIENTATION_MAP. lib_iter3/statsx.py imports only
# numpy/scipy and is imported verbatim.
sys.path.insert(0, str(E3))
from lib_iter3 import statsx as sx  # noqa: E402

BOOT_SEED = sx.BOOT_SEED
N_BOOT = 5000  # the plan's replicate count; the archive's own default is 10000

SCORE_COLUMNS = [
    "alpha_50_logistic",
    "alpha_50_nonparametric",
    "max_refusal_rate",
    "ams_sigma",
    "ams_sigma_para",
    "ams_sigma_archive",
    "logit_gap_benign",
    "logit_gap_harmful",
]

# Human labels used in every generated table so a number never appears without
# knowing which score produced it.
SCORE_LABEL = {
    "alpha_50_logistic": "alpha_50 (logistic)",
    "alpha_50_nonparametric": "alpha_50 (non-parametric)",
    "max_refusal_rate": "max refusal rate (alpha_50 surrogate)",
    "ams_sigma": "our-AMS sigma",
    "ams_sigma_para": "our-AMS sigma (paraphrase refit)",
    "ams_sigma_archive": "our-AMS sigma (archived)",
    "logit_gap_benign": "logit-gap (benign)",
    "logit_gap_harmful": "logit-gap (harmful)",
}

MATRIX_ROWS = ["alpha_50", "our_AMS", "logit_gap_benign", "logit_gap_harmful"]
CHECKS = ["check1_lexical", "check2_monotonicity", "check3_layer",
          "check4_jackknife", "check5_scorer"]


def setup_logging(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jload(p: Path):
    return json.loads(Path(p).read_text())


def _default(o):
    import numpy as np
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"not serialisable: {type(o)}")


def jdump(obj, p: Path) -> None:
    Path(p).write_text(json.dumps(obj, indent=1, default=_default))


def require(d: dict, key: str, where: str):
    """Fail loud on a missing input key rather than defaulting silently."""
    if key not in d:
        raise KeyError(f"missing key {key!r} in {where}; available: {sorted(d)[:25]}")
    return d[key]


def fmt(x, nd: int = 3) -> str:
    if x is None:
        return "n/a"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(fmt(v, nd) for v in x) + "]"
    try:
        return f"{float(x):.{nd}f}"
    except (TypeError, ValueError):
        return str(x)


def fmt_p(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:.2e}" if x < 1e-3 else f"{x:.4f}"
