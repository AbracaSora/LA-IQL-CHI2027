"""Analyze the shortened six-item human-evaluation questionnaire.

The script keeps participant-level dependence explicit and generates the
two-system figure used in the paper. It does not write participant-level data.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


DIMENSIONS = (
    ("diversity", "Interactional variety"),
    ("naturalness", "Resemblance to authentic\nteacher–student interaction"),
    ("helpfulness", "Support for understanding\nand discussion"),
)
SYSTEMS = ("LA-IQL Direct", "Direct-role LLM")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path)
    return parser.parse_args()


def load_long(responses: Path, mapping: Path) -> pd.DataFrame:
    frame = pd.read_csv(responses, encoding="utf-8-sig")
    source_map = pd.read_csv(mapping)
    source_map = source_map[
        source_map["matrix_index_excluding_demographics"] <= 18
    ].copy()

    # Tencent's export places the 54 matrix responses after six metadata fields.
    rating_columns = list(frame.columns[6:60])
    if len(rating_columns) != 54:
        raise ValueError(f"Expected 54 rating columns, found {len(rating_columns)}")

    records: list[dict[str, object]] = []
    dimension_keys = [key for key, _ in DIMENSIONS]
    for _, response in frame.iterrows():
        participant = str(response.iloc[0])
        for index, column in enumerate(rating_columns):
            match = re.search(r"(\d)\s*分", str(response[column]))
            records.append(
                {
                    "participant": participant,
                    "matrix": index // 3 + 1,
                    "dimension": dimension_keys[index % 3],
                    "score": int(match.group(1)) if match else np.nan,
                }
            )

    long = pd.DataFrame(records).merge(
        source_map[
            [
                "matrix_index_excluding_demographics",
                "item_id",
                "display_label",
                "source",
            ]
        ],
        left_on="matrix",
        right_on="matrix_index_excluding_demographics",
        validate="many_to_one",
    )
    complete_counts = long.groupby("participant")["score"].count()
    complete_participants = complete_counts[complete_counts == 54].index
    return long[
        long["participant"].isin(complete_participants)
        & long["source"].isin(SYSTEMS)
    ].copy()


def participant_summary(long: pd.DataFrame) -> pd.DataFrame:
    participant_means = (
        long.groupby(["participant", "source", "dimension"], as_index=False)[
            "score"
        ].mean()
    )
    summary = (
        participant_means.groupby(["source", "dimension"])["score"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    critical = stats.t.ppf(0.975, summary["count"] - 1)
    summary["ci95"] = critical * summary["std"] / np.sqrt(summary["count"])
    return summary


def draw(summary: pd.DataFrame, output: Path) -> None:
    colors = {"LA-IQL Direct": "#1f77b4", "Direct-role LLM": "#e07a1f"}
    offsets = {"LA-IQL Direct": -0.11, "Direct-role LLM": 0.11}
    labels = {key: label for key, label in DIMENSIONS}
    y_base = np.arange(len(DIMENSIONS))

    fig, ax = plt.subplots(figsize=(7.2, 3.25))
    for system in SYSTEMS:
        rows = summary[summary["source"] == system].set_index("dimension")
        ordered = rows.loc[[key for key, _ in DIMENSIONS]]
        y = y_base + offsets[system]
        ax.errorbar(
            ordered["mean"],
            y,
            xerr=ordered["ci95"],
            fmt="o",
            markersize=6.5,
            capsize=3,
            linewidth=1.7,
            color=colors[system],
            label=system,
        )

    ax.set_xlim(1, 5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xlabel("Mean rating (1 = very poor, 5 = very good)")
    ax.set_yticks(y_base, [labels[key] for key, _ in DIMENSIONS])
    ax.invert_yaxis()
    ax.grid(axis="x", color="#d9d9d9", linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    long = load_long(args.responses, args.mapping)
    summary = participant_summary(long)
    draw(summary, args.output)
    if args.summary_output is not None:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(args.summary_output, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
