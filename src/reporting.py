from __future__ import annotations

from pathlib import Path
from typing import Iterable

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

    dataframe.to_csv(
        path,
        index=False,
    )


def save_text(
    text: str,
    path: str | Path,
) -> None:
    """
    Save text content to a UTF-8 file.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        text,
        encoding="utf-8",
    )


def save_investment_thesis(
    thesis: dict,
    path: str | Path,
) -> None:
    """
    Save a structured investment thesis as CSV.
    """

    dataframe = pd.DataFrame(
        [
            thesis
        ]
    )

    save_dataframe(
        dataframe,
        path,
    )


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
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_valuation_sensitivity(
    sensitivity: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Plot a DCF valuation sensitivity table.
    """

    if sensitivity.empty:
        raise ValueError(
            "Sensitivity table cannot be empty."
        )

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
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_peer_multiples(
    multiples: pd.DataFrame,
    output_path: str | Path,
    columns: Iterable[str] | None = None,
) -> None:
    """
    Plot selected peer valuation multiples.
    """

    if multiples.empty:
        raise ValueError(
            "Peer multiples cannot be empty."
        )

    if columns is None:
        columns = [
            column
            for column in [
                "pe",
                "ev_ebitda",
                "ev_sales",
                "price_sales",
            ]
            if column in multiples.columns
        ]

    columns = list(columns)

    if not columns:
        raise ValueError(
            "No valid multiple columns were supplied."
        )

    figure, axis = plt.subplots(
        figsize=(11, 6)
    )

    multiples[columns].plot(
        kind="bar",
        ax=axis,
    )

    axis.set_title(
        "Peer Valuation Multiples"
    )

    axis.set_xlabel(
        "Company"
    )

    axis.set_ylabel(
        "Multiple"
    )

    axis.grid(
        axis="y",
        alpha=0.3,
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_scenario_valuation(
    scenario_valuations: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Plot valuation estimates across scenarios.
    """

    if scenario_valuations.empty:
        raise ValueError(
            "Scenario valuation data cannot be empty."
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    dataframe = scenario_valuations.copy()

    if "scenario" in dataframe.columns:
        dataframe = dataframe.set_index(
            "scenario"
        )

    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        raise ValueError(
            "No numeric valuation columns were found."
        )

    dataframe[numeric_columns].plot(
        kind="bar",
        ax=axis,
    )

    axis.set_title(
        "Scenario Valuation Analysis"
    )

    axis.set_xlabel(
        "Scenario"
    )

    axis.set_ylabel(
        "Estimated Value"
    )

    axis.grid(
        axis="y",
        alpha=0.3,
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def build_research_report(
    target_ticker: str,
    investment_summary: dict,
    valuation_summary: pd.DataFrame,
    peer_comparison: pd.DataFrame | None = None,
) -> str:
    """
    Build a concise Markdown research report from
    structured analytical outputs.

    Numerical results are taken directly from the supplied
    data rather than fabricated by the reporting layer.
    """

    lines = [
        f"# Equity Research Report — {target_ticker}",
        "",
        "## Investment Summary",
        "",
    ]

    market_price = investment_summary.get(
        "market_price"
    )

    consensus_value = investment_summary.get(
        "consensus_value"
    )

    valuation_upside = investment_summary.get(
        "valuation_upside"
    )

    fundamental_score = investment_summary.get(
        "fundamental_score"
    )

    valuation_classification = (
        investment_summary.get(
            "valuation_classification"
        )
    )

    investment_view = investment_summary.get(
        "investment_view"
    )

    if market_price is not None:
        lines.append(
            f"- Market price: {market_price:.2f}"
        )

    if consensus_value is not None:
        lines.append(
            f"- Consensus valuation: "
            f"{consensus_value:.2f}"
        )

    if valuation_upside is not None:
        lines.append(
            f"- Valuation upside/downside: "
            f"{valuation_upside:.1%}"
        )

    if fundamental_score is not None:
        lines.append(
            f"- Fundamental score: "
            f"{fundamental_score:.2f}"
        )

    if valuation_classification:
        lines.append(
            f"- Valuation classification: "
            f"{valuation_classification}"
        )

    if investment_view:
        lines.append(
            f"- Investment view: "
            f"{investment_view}"
        )

    lines.extend(
        [
            "",
            "## Valuation Methods",
            "",
        ]
    )

    if valuation_summary.empty:
        lines.append(
            "No valuation-method output was available."
        )
    else:
        lines.append(
            valuation_summary.to_markdown(
                index=False
            )
        )

    if (
        peer_comparison is not None
        and not peer_comparison.empty
    ):
        lines.extend(
            [
                "",
                "## Peer Comparison",
                "",
                peer_comparison.to_markdown(
                    index=False
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Methodological Note",
            "",
            (
                "This report is generated from the "
                "research pipeline outputs. Valuation "
                "results depend on the underlying financial "
                "data, assumptions, discount rates, terminal "
                "growth, and peer-selection methodology."
            ),
        ]
    )

    return "\n".join(
        lines
    )


def save_research_report(
    target_ticker: str,
    investment_summary: dict,
    valuation_summary: pd.DataFrame,
    output_path: str | Path,
    peer_comparison: pd.DataFrame | None = None,
) -> None:
    """
    Build and save the Markdown research report.
    """

    report = build_research_report(
        target_ticker=target_ticker,
        investment_summary=investment_summary,
        valuation_summary=valuation_summary,
        peer_comparison=peer_comparison,
    )

    save_text(
        report,
        output_path,
    )
