from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_dataframe(
    dataframe: pd.DataFrame,
    path: str | Path,
) -> None:
    """
    Save a DataFrame as CSV.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(path)


def plot_revenue_and_ebitda(
    revenue: pd.Series,
    ebitda: pd.Series,
    output_path: str | Path,
) -> None:
    """
    Plot historical revenue and EBITDA.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    axis.plot(
        revenue.index,
        revenue.values,
        marker="o",
        label="Revenue",
    )

    axis.plot(
        ebitda.index,
        ebitda.values,
        marker="o",
        label="EBITDA",
    )

    axis.set_title(
        "Revenue and EBITDA"
    )

    axis.set_xlabel(
        "Period"
    )

    axis.set_ylabel(
        "Value"
    )

    axis.legend()

    axis.grid(
        alpha=0.3
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=200,
    )

    plt.close(figure)


def plot_valuation_sensitivity(
    sensitivity: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Plot a DCF valuation sensitivity table.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    image = axis.imshow(
        sensitivity.values,
        aspect="auto",
    )

    axis.set_xticks(
        range(len(sensitivity.columns))
    )

    axis.set_xticklabels(
        [
            f"{value:.1%}"
            for value in sensitivity.columns
        ]
    )

    axis.set_yticks(
        range(len(sensitivity.index))
    )

    axis.set_yticklabels(
        [
            f"{value:.1%}"
            for value in sensitivity.index
        ]
    )

    axis.set_xlabel(
        "Terminal Growth"
    )

    axis.set_ylabel(
        "WACC"
    )

    axis.set_title(
        "DCF Valuation Sensitivity"
    )

    figure.colorbar(
        image,
        ax=axis,
        label="Enterprise Value",
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=200,
    )

    plt.close(figure)
