#!/usr/bin/env python3
"""Shared paths, IO, provenance and the FROZEN estimator imports.

Hard rule of this artifact: the estimators are IMPORTED, never retyped.

* ``frozen_src/explib.py`` is a byte-copy of the iteration-4 experiment's
  ``explib.py`` (verdict_from_ci, centre_by_stratum, detection_stats,
  cluster_boot_indices, auroc, wilson, spearman, boot_ci, and the pre-registered
  constants READS_THRESHOLD / MIN_PER_CLASS / CHANCE_BAND / N_BOOT / BOOT_SEED).
  It is import-safe: it imports only numpy/math/json at module scope.
* ``frozen_src/lib_iter3/statsx.py`` is a byte-copy of the iteration-3
  experiment's estimator library (clustered_bootstrap_rho,
  lineage_permutation_p, loo_lineage_jackknife, spearman_basic).

Neither R4/method.py nor E3/method.py is importable (both execute / import torch
at module scope), which is why only the two libraries above are brought in.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from loguru import logger

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LOGS = HERE / "logs"
FIGS = HERE / "figures"
FROZEN = HERE / "frozen_src"
for _d in (OUT, LOGS, FIGS):
    _d.mkdir(parents=True, exist_ok=True)

ROOT = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop")
R4 = ROOT / "iter_4/gen_art/gen_art_experiment_2"            # art_1xT3w1joqeJ8
R4_RESULTS = R4 / "results"
E3 = ROOT / "iter_3/gen_art/gen_art_experiment_1"            # art_3Cndd5cKsYV0
V4 = ROOT / "iter_4/gen_art/gen_art_evaluation_1"            # art__tq3ZgPRYB0B
V3 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"
D1 = ROOT / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"   # art_CKWQh2cOQLLQ

sys.path.insert(0, str(FROZEN))
import explib as EX                       # noqa: E402
from lib_iter3 import statsx as SX        # noqa: E402

EX.RESULTS = R4_RESULTS                   # explib.HERE now points at frozen_src

# ---- pre-registered analysis constants for THIS artifact -------------------
N_BOOT_NEW = 10_000        # new estimates
BOOT_SEED_NEW = 20260813
N_PERM_EXHAUSTIVE = 5040   # 7!
PERM_FLOOR = 1.0 / 5040.0  # 1.98e-4 -- identity permutation always counts
AXES = ["A_canned", "B_paraphrase", "C_stylistic", "D_random0", "E_prompt_contrast"]
AXIS_SHORT = {"A_canned": "A", "B_paraphrase": "B", "C_stylistic": "C",
              "D_random0": "D", "E_prompt_contrast": "E"}
ARMS = ["aligned_reference", "weight_edited_abliteration",
        "behavioural_uncensored_candidate", "behavioural_uncensored_unverified"]
TOL = 1e-6
BANNED_SALVAGE_TOKENS = ["trending", "marginally significant", "suggestive",
                         "borderline significant", "approaching significance",
                         "nearly significant"]


# --------------------------------------------------------------------------
def setup_logging(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def jload(p: Path):
    return json.loads(Path(p).read_text())


def _jdefault(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        v = float(o)
        return None if not math.isfinite(v) else v
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"not JSON serialisable: {type(o)}")


def clean_nan(o):
    """Replace non-finite floats with None so the JSON is strict-valid."""
    if isinstance(o, dict):
        return {k: clean_nan(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean_nan(v) for v in o]
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, (np.floating,)):
        v = float(o)
        return None if not math.isfinite(v) else v
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return clean_nan(o.tolist())
    return o


def jdump(p: Path, obj, indent: int = 2) -> None:
    Path(p).write_text(json.dumps(clean_nan(obj), indent=indent,
                                  default=_jdefault, allow_nan=False))


def fmt(v, nd: int = 3) -> str:
    if v is None:
        return "--"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if not math.isfinite(f):
        return "--"
    return f"{f:.{nd}f}"


def fmt_ci(ci, nd: int = 3) -> str:
    if ci is None:
        return "--"
    lo, hi = ci
    if lo is None or hi is None:
        return "--"
    if not (math.isfinite(float(lo)) and math.isfinite(float(hi))):
        return "--"
    return f"[{float(lo):.{nd}f}, {float(hi):.{nd}f}]"


def fmt_p(p) -> str:
    if p is None or (isinstance(p, float) and not math.isfinite(p)):
        return "--"
    return f"{float(p):.2e}" if float(p) < 1e-3 else f"{float(p):.4f}"


# --------------------------------------------------------------------------
# Correlation machinery -- point estimate + lineage-clustered CI + exhaustive
# lineage permutation, at BOTH aggregation units.
# --------------------------------------------------------------------------
def _rho(x, y) -> float:
    return SX.spearman_basic(x, y)["rho"]


def rank_bottom(values, censored_flag) -> np.ndarray:
    """Censored values get a single tied SENTINEL rank -- never dropped, never
    imputed to a finite number (the frozen iteration-4 convention).

    Orientation note, recorded because it differs from the iteration-4 wording.
    The iteration-4 evaluation phrased the sentinel as ``max + 1`` because its
    censored quantity was one where censoring meant the LARGEST value.  Here the
    variable is x = -log10(c_50): a censored c_50 means the axis NEVER drove the
    refusal rate to one half, i.e. the WORST possible induction quality, so the
    sentinel must sit strictly BELOW every uncensored value.  Rank 0 is used; all
    censored members are tied at it, which is what "censored, order unknown among
    themselves" means.
    """
    v = np.asarray(values, float).copy()
    cen = np.asarray(censored_flag, bool)
    from scipy.stats import rankdata
    out = np.empty(v.size, float)
    if (~cen).sum() > 0:
        out[~cen] = rankdata(v[~cen])
    out[cen] = 0.0     # tied sentinel strictly BELOW every uncensored value
    return out


def corr_block(x, y, clusters, *, label: str, n_boot: int = N_BOOT_NEW,
               seed: int = BOOT_SEED_NEW, exhaustive_perm: bool = True) -> dict:
    """One correlation reported the way this project reports correlations."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    clusters = list(clusters)
    ok = np.isfinite(x) & np.isfinite(y)
    xs, ys = x[ok], y[ok]
    cs = [c for c, k in zip(clusters, ok) if k]
    n = int(xs.size)
    out = {"label": label, "n_points": n, "n_clusters": len(set(cs)),
           "rho": None, "ci95": None, "n_boot": n_boot, "seed": seed,
           "p_permutation": None, "p_floor": PERM_FLOOR, "at_perm_floor": False,
           "exhaustive": False, "loo_lineage": None, "half_width": None,
           "ci_excludes_zero": None}
    if n < 3:
        out["note"] = "fewer than 3 usable points"
        return out
    cb = SX.clustered_bootstrap_rho(xs, ys, cs, n_boot=n_boot, seed=seed)
    out["rho"] = cb["rho"]
    out["ci95"] = cb["ci95_lineage_clustered"]
    out["n_boot_valid"] = cb["n_boot_valid"]
    if out["ci95"] is not None:
        lo, hi = out["ci95"]
        out["half_width"] = float((hi - lo) / 2.0)
        out["ci_excludes_zero"] = bool(lo > 0 or hi < 0)
    if exhaustive_perm and len(set(cs)) >= 3:
        pm = SX.lineage_permutation_p(xs, ys, cs)
        out["p_permutation"] = pm["p_permutation"]
        out["p_min_achievable"] = pm.get("p_min_achievable")
        out["exhaustive"] = bool(pm.get("exhaustive"))
        out["n_permutations"] = pm.get("n_permutations")
        if out["p_permutation"] is not None and pm.get("p_min_achievable") is not None:
            out["at_perm_floor"] = bool(
                abs(out["p_permutation"] - pm["p_min_achievable"]) < 1e-12)
    if len(set(cs)) >= 3:
        jk = SX.loo_lineage_jackknife(xs, ys, cs)
        out["loo_lineage"] = jk
    return out


def aggregate_to_lineage(rows: list[dict], xkey: str, ykey: str,
                         linkey: str = "lineage_id") -> tuple[list, list, list]:
    """Frozen dual-aggregation convention: member values are averaged WITHIN a
    lineage before the lineage-unit statistic is taken, so every lineage
    contributes exactly one (x, y) pair regardless of how many members it holds.
    """
    by: dict[str, list[tuple[float, float]]] = {}
    for r in rows:
        xv, yv = r.get(xkey), r.get(ykey)
        if xv is None or yv is None:
            continue
        if not (math.isfinite(float(xv)) and math.isfinite(float(yv))):
            continue
        by.setdefault(r[linkey], []).append((float(xv), float(yv)))
    lins = sorted(by)
    xs = [float(np.mean([p[0] for p in by[L]])) for L in lins]
    ys = [float(np.mean([p[1] for p in by[L]])) for L in lins]
    return xs, ys, lins


def dual_unit(rows: list[dict], xkey: str, ykey: str, label: str) -> dict:
    """Member-unit and lineage-unit estimates side by side, as H-U requires."""
    mx = [r.get(xkey) for r in rows]
    my = [r.get(ykey) for r in rows]
    ml = [r["lineage_id"] for r in rows]
    member = corr_block(mx, my, ml, label=f"{label} [member unit]")
    lx, ly, ll = aggregate_to_lineage(rows, xkey, ykey)
    lineage = corr_block(lx, ly, ll, label=f"{label} [lineage unit]")
    same_sign = None
    if member["rho"] is not None and lineage["rho"] is not None:
        same_sign = bool(np.sign(member["rho"]) == np.sign(lineage["rho"]))
    return {"member": member, "lineage": lineage, "same_sign": same_sign}


# --------------------------------------------------------------------------
def _nonfinite(v) -> bool:
    if v is None:
        return True
    try:
        return not math.isfinite(float(v))
    except (TypeError, ValueError):
        return False


def gate_leg(name: str, target, obtained, tol: float = TOL, *,
             note: str = "", level: str = "item-level") -> dict:
    d = None
    if _nonfinite(target) and _nonfinite(obtained):
        # both sides are the SAME absence (an UNDEFINED member has no AUROC and
        # no CI); agreement on absence is agreement, not a failed leg.
        return {"leg": name, "target": None, "obtained": None, "delta": 0.0,
                "tolerance": tol, "status": "PASS", "level": level,
                "note": (note + " | both sides non-finite (UNDEFINED member): "
                                "agreement on absence").strip(" |")}
    if target is not None and obtained is not None:
        try:
            d = abs(float(target) - float(obtained))
        except (TypeError, ValueError):
            d = None
    passed = (d is not None and d <= tol)
    return {"leg": name, "target": target, "obtained": obtained,
            "delta": d, "tolerance": tol, "status": "PASS" if passed else "FAIL",
            "level": level, "note": note}
