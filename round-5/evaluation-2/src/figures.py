#!/usr/bin/env python3
"""Two vector figures, generated from eval_out.json only (no hand-typed numbers).

  fig1_dumbbell_regex_vs_semantic.pdf  per-member paired AUROC_regex vs
                                       AUROC_semantic with prompt-clustered CIs
  fig2_protocols_by_axis.pdf           per-member AUROC across the four
                                       normalisation protocols for axes A, B, D
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from loguru import logger  # noqa: E402

import eval_lib as L  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

PROTO_LABEL = {"archived": "archived\n(whole-pool centring)",
               "fold_centre": "fold-internal\ncentring (LOPO)",
               "fold_centre_scale": "fold-internal\ncentre + scale (LOPO)",
               "leaky_z": "leaky whole-pool\nz-score"}
PROTO_COLOR = {"archived": "#333333", "fold_centre": "#1b7837",
               "fold_centre_scale": "#2166ac", "leaky_z": "#b2182b"}
AXIS_LABEL = {"A_canned": "axis A (canned-response contrast)",
              "B_paraphrase": "axis B (token-disjoint paraphrase)",
              "D_random0": "axis D (norm-matched random)"}


def fig1(doc: dict, out: Path) -> None:
    p1 = doc["metadata"]["part1"]["per_member"]
    keys = sorted(p1, key=lambda k: p1[k]["auroc_semantic"])
    n = len(keys)
    fig, ax = plt.subplots(figsize=(8.2, 0.46 * n + 3.0))
    y = np.arange(n)
    for i, k in enumerate(keys):
        r = p1[k]
        a_r, a_s = r["auroc_regex_same_items"], r["auroc_semantic"]
        ax.plot([a_r, a_s], [i, i], color="#999999", lw=1.6, zorder=1)
        for val, ci, col, lab in ((a_r, r["auroc_regex_same_items_ci95"], "#d95f02",
                                   "regex label of record"),
                                  (a_s, r["auroc_semantic_ci95"], "#1b4f9c",
                                   "five-class semantic label")):
            lo, hi = ci
            if np.isfinite(lo) and np.isfinite(hi):
                ax.plot([lo, hi], [i, i], color=col, lw=1.0, alpha=0.45, zorder=2)
            ax.scatter([val], [i], s=44, color=col, zorder=3,
                       label=lab if i == 0 else None)
    band = doc["metadata"]["part1"]["random_band_upper_mean"]
    ax.axvline(0.5, color="#bbbbbb", ls=":", lw=1.0)
    ax.axvline(band, color="#7b3294", ls="--", lw=1.1,
               label=f"mean 20-draw random band upper edge ({band:.3f})")
    ax.set_yticks(y)
    ax.set_yticklabels([k.replace("_", " ") for k in keys], fontsize=8)
    ax.set_xlabel("held-out AUROC of the stratum-centred axis-A projection\n"
                  "(identical items; only the LABEL changes)")
    ax.set_xlim(0.0, 1.02)
    ax.set_title("Does the refusal axis read meaning or wording?\n"
                 "paired per-member AUROC under the regex vs the semantic label",
                 fontsize=11)
    ax.grid(axis="x", alpha=0.25, lw=0.6)
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.16),
              ncol=2, framealpha=0.92)
    fig.tight_layout()
    fig.savefig(out, format="pdf")
    plt.close(fig)
    logger.info(f"  wrote {out.name}")


def fig2(doc: dict, out: Path) -> None:
    p2 = doc["metadata"]["part2"]["per_member"]
    keys = sorted(p2)
    axes_l = L.AXES_P2
    fig, axs = plt.subplots(1, len(axes_l), figsize=(4.1 * len(axes_l), 0.42 * len(keys) + 3.0),
                            sharey=True)
    y = np.arange(len(keys))
    for j, axis in enumerate(axes_l):
        ax = axs[j]
        for pi, proto in enumerate(L.PROTOCOLS):
            xs, los, his = [], [], []
            for k in keys:
                cell = p2[k]["label_sets"]["regex"]["axes"][axis][proto]
                xs.append(cell["auroc"])
                los.append(cell["auroc_ci95"][0])
                his.append(cell["auroc_ci95"][1])
            off = (pi - 1.5) * 0.17
            for i in range(len(keys)):
                if np.isfinite(los[i]) and np.isfinite(his[i]):
                    ax.plot([los[i], his[i]], [y[i] + off] * 2,
                            color=PROTO_COLOR[proto], lw=0.9, alpha=0.40)
            ax.scatter(xs, y + off, s=22, color=PROTO_COLOR[proto],
                       label=PROTO_LABEL[proto] if j == 0 else None, zorder=3)
        ax.axvline(0.5, color="#bbbbbb", ls=":", lw=1.0)
        ax.set_title(AXIS_LABEL[axis], fontsize=9)
        ax.set_xlim(0.0, 1.02)
        ax.grid(axis="x", alpha=0.25, lw=0.6)
        ax.set_xlabel("held-out AUROC")
    axs[0].set_yticks(y)
    axs[0].set_yticklabels([k.replace("_", " ") for k in keys], fontsize=8)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=7.5, ncol=4, loc="lower center",
               framealpha=0.92, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("How much of the detection AUROC is the normalisation?\n"
                 "four leave-one-prompt-out protocols, identical items and axes",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0.09, 1, 0.94))
    fig.savefig(out, format="pdf")
    plt.close(fig)
    logger.info(f"  wrote {out.name}")


def main() -> None:
    doc = json.loads((L.HERE / "eval_out.json").read_text())
    L.FIGS.mkdir(exist_ok=True)
    fig1(doc, L.FIGS / "fig1_dumbbell_regex_vs_semantic.pdf")
    fig2(doc, L.FIGS / "fig2_protocols_by_axis.pdf")


if __name__ == "__main__":
    main()
