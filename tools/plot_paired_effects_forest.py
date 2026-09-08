"""Regenerate the appendix forest plot from the paired effects in the paper."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figure"

COLORS = {"G1": "#389bb5", "G2": "#e89400", "LR": "#7a7a7a"}

TD = [
    ("RQ1  Distinct-2", "G1", 0.0252, -0.0282, 0.0688, False),
    ("RQ1  Cycle-2", "G1", 0.0900, 0.0438, 0.1400, True),
    ("RQ1  Motif rate", "G1", 0.1422, 0.0889, 0.2013, True),
    ("RQ1  Normalized entropy", "G1", 0.0258, -0.0156, 0.0659, False),
    ("RQ2  Paired bigram JSD", "G2", 0.0007, -0.0043, 0.0063, False),
    ("RQ2  Transition JSD", "G2", 0.0009, -0.0055, 0.0091, False),
    ("RQ2  Bigram support", "G2", 0.0073, -0.00001, 0.0140, False),
    ("LR  Local trigram redundancy", "LR", 0.00001, -0.0041, 0.0042, False),
]

DIRECT = [
    ("RQ1  Distinct-2", "G1", -0.0108, -0.0377, 0.0165, False),
    ("RQ1  Cycle-2", "G1", -0.1220, -0.1447, -0.0986, True),
    ("RQ1  Motif rate", "G1", -0.2543, -0.2963, -0.2100, True),
    ("RQ2  Paired bigram JSD", "G2", 0.0232, 0.0152, 0.0305, True),
    ("RQ2  Bigram support", "G2", 0.0384, 0.0283, 0.0492, True),
    ("RQ2  Trigram support", "G2", 0.3898, 0.3551, 0.4238, True),
]


def panel(ax, rows, title, left_label, right_label, xlim):
    y = list(range(len(rows)))[::-1]
    for yi, (label, goal, mean, low, high, significant) in zip(y, rows):
        color = COLORS[goal]
        ax.errorbar(
            mean,
            yi,
            xerr=[[mean - low], [high - mean]],
            fmt="o",
            ms=7,
            mfc=color if significant else "white",
            mec=color,
            mew=1.8,
            ecolor=color,
            elinewidth=1.8,
            capsize=3,
        )
    ax.axvline(0, color="#555555", linestyle="--", linewidth=1.2)
    ax.set_yticks(y, [r[0] for r in rows])
    ax.set_xlim(*xlim)
    ax.set_title(title, fontsize=15, fontweight="bold", pad=25)
    ax.text(0.01, 1.01, left_label, transform=ax.transAxes, color="#555555", fontsize=11)
    ax.text(0.99, 1.01, right_label, transform=ax.transAxes, ha="right", color="#555555", fontsize=11)
    ax.set_xlabel("Desirability-aligned paired effect (95% CI)")
    ax.grid(axis="x", color="#e5e5e5", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)


fig, axes = plt.subplots(1, 2, figsize=(13.2, 8.5))
fig.subplots_adjust(left=0.20, right=0.98, bottom=0.18, top=0.88, wspace=0.72)
panel(axes[0], TD, "TD vs w/o TD", "← w/o TD", "TD →", (-0.24, 0.24))
panel(axes[1], DIRECT, "Direct vs Candidate", "← Candidate", "Direct →", (-0.50, 0.50))

legend = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor=c, markeredgecolor=c, label=label)
    for label, c in [("RQ1 interaction-pattern diversity", COLORS["G1"]),
                     ("RQ2 human-pattern alignment", COLORS["G2"]),
                     ("LR language realization", COLORS["LR"])]
]
fig.legend(handles=legend, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.015))
fig.text(
    0.5,
    0.085,
    "Filled markers: reported p or BH q < .05; hollow markers: not significant or not tested.",
    ha="center",
    color="#555555",
    fontsize=10,
)

for suffix in ("pdf", "png"):
    fig.savefig(OUT / f"paired_effects_forest.{suffix}", dpi=220, bbox_inches="tight")
plt.close(fig)
