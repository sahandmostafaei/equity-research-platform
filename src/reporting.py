from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
    output_dir: Path,
) -> Path:
    """
    Save a DataFrame as a CSV file.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        output_dir
        / filename
    )

    dataframe.to_csv(
        path,
        index=False,
    )

    return path


def save_text(
    text: str,
    filename: str,
    output_dir: Path,
) -> Path:
    """
    Save text content to a file.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        output_dir
        / filename
    )

    path.write_text(
        text,
        encoding="utf-8",
    )

    return path


def plot_revenue_and_ebitda(
    revenue: pd.Series,
    ebitda: pd.Series,
    output_path: Path,
) -> Path:
    """
    Plot historical revenue and EBITDA.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = pd.DataFrame(
        {
            "Revenue": revenue,
            "EBITDA": ebitda,
        }
    ).dropna(
        how="all"
    )

    if data.empty:
        raise ValueError(
            "Revenue and EBITDA data "
            "cannot both be empty."
        )

    ax = data.plot(
        kind="line",
        marker="o",
        figsize=(10, 6),
    )

    ax.set_title(
        "Historical Revenue and EBITDA"
    )

    ax.set_xlabel(
        "Period"
    )

    ax.set_ylabel(
        "Value"
    )

    ax.grid(
        alpha=0.3
    )

    figure = ax.get_figure()

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return output_path


def plot_valuation_sensitivity(
    sensitivity: pd.DataFrame,
    output_path: Path,
) -> Path:
    """
    Plot DCF valuation sensitivity.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if sensitivity.empty:
        raise ValueError(
            "Sensitivity data cannot be empty."
        )

    ax = sensitivity.plot(
        figsize=(10, 6),
        marker="o",
    )

    ax.set_title(
        "DCF Valuation Sensitivity"
    )

    ax.set_xlabel(
        "WACC"
    )

    ax.set_ylabel(
        "Valuation"
    )

    ax.grid(
        alpha=0.3
    )

    figure = ax.get_figure()

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return output_path


def save_investment_thesis(
    thesis: dict,
    output_path: Path,
) -> Path:
    """
    Save the structured investment thesis
    as a one-row CSV file.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = pd.DataFrame(
        [thesis]
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    return output_path


def plot_peer_multiples(
    multiples: pd.DataFrame,
    output_path: Path,
) -> Path:
    """
    Plot selected peer valuation multiples.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if multiples.empty:
        raise ValueError(
            "Peer multiples cannot be empty."
        )

    preferred_columns = [
        "pe",
        "ev_ebitda",
        "ev_sales",
        "price_sales",
    ]

    columns = [
        column
        for column in preferred_columns
        if column in multiples.columns
    ]

    if not columns:
        raise ValueError(
            "No supported peer-multiple "
            "columns were found."
        )

    data = multiples[
        columns
    ].copy()

    ax = data.plot(
        kind="bar",
        figsize=(11, 6),
    )

    ax.set_title(
        "Peer Valuation Multiples"
    )

    ax.set_xlabel(
        "Company"
    )

    ax.set_ylabel(
        "Multiple"
    )

    ax.grid(
        axis="y",
        alpha=0.3,
    )

    figure = ax.get_figure()

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return output_path


def plot_scenario_valuation(
    scenario_valuations: pd.DataFrame,
    output_path: Path,
) -> Path:
    """
    Plot scenario-based valuation outputs.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if scenario_valuations.empty:
        raise ValueError(
            "Scenario valuations "
            "cannot be empty."
        )

    data = scenario_valuations.copy()

    numeric_columns = [
        column
        for column in data.columns
        if pd.api.types.is_numeric_dtype(
            data[column]
        )
    ]

    if not numeric_columns:
        raise ValueError(
            "No numeric scenario valuation "
            "columns were found."
        )

    if "scenario" in data.columns:
        labels = data[
            "scenario"
        ].astype(str)

        values = data[
            numeric_columns
        ].iloc[:, 0]

    else:
        labels = (
            data.index.astype(str)
        )

        values = data[
            numeric_columns
        ].iloc[:, 0]

    figure, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.bar(
        labels,
        values,
    )

    ax.set_title(
        "Scenario Valuation"
    )

    ax.set_xlabel(
        "Scenario"
    )

    ax.set_ylabel(
        "Valuation"
    )

    ax.grid(
        axis="y",
        alpha=0.3,
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return output_path


def build_research_report(
    target_ticker: str,
    investment_summary: dict,
    valuation_summary: pd.DataFrame,
    peer_comparison: pd.DataFrame | None = None,
) -> str:
    """
    Build a concise Markdown equity research report.
    """

    market_price = investment_summary.get(
        "market_price"
    )

    median_valuation = (
        investment_summary.get(
            "consensus_value"
        )
    )

    valuation_upside = (
        investment_summary.get(
            "valuation_upside"
        )
    )

    fundamental_score = (
        investment_summary.get(
            "fundamental_score"
        )
    )

    valuation_classification = (
        investment_summary.get(
            "valuation_classification"
        )
    )

    investment_view = (
        investment_summary.get(
            "investment_view"
        )
    )

    lines: list[str] = []

    lines.append(
        f"# Equity Research Report — "
        f"{target_ticker}"
    )

    lines.append("")

    lines.append(
        "## Investment Overview"
    )

    lines.append("")

    lines.append(
        f"- **Ticker:** {target_ticker}"
    )

    if market_price is not None:
        lines.append(
            f"- **Market Price:** "
            f"{float(market_price):.2f}"
        )

    if median_valuation is not None:
        lines.append(
            f"- **Median Valuation Reference:** "
            f"{float(median_valuation):.2f}"
        )

    if valuation_upside is not None:
        lines.append(
            f"- **Valuation Upside:** "
            f"{float(valuation_upside):.2%}"
        )

    if fundamental_score is not None:
        lines.append(
            f"- **Fundamental Score:** "
            f"{float(fundamental_score):.2f}"
        )

    if valuation_classification:
        lines.append(
            f"- **Valuation Classification:** "
            f"{valuation_classification}"
        )

    if investment_view:
        lines.append(
            f"- **Investment View:** "
            f"{investment_view}"
        )

    lines.append("")

    lines.append(
        "## Valuation Summary"
    )

    lines.append("")

    if valuation_summary.empty:
        lines.append(
            "No valuation observations were available."
        )

    else:
        lines.append(
            valuation_summary.to_markdown(
                index=False
            )
        )

    lines.append("")

    lines.append(
        "## Peer Comparison"
    )

    lines.append("")

    if (
        peer_comparison is None
        or peer_comparison.empty
    ):
        lines.append(
            "No peer comparison data were available."
        )

    else:
        lines.append(
            peer_comparison.to_markdown(
                index=False
            )
        )

    lines.append("")

    lines.append(
        "## Methodology"
    )

    lines.append("")

    lines.append(
        "The research workflow combines "
        "historical financial-statement analysis, "
        "fundamental metrics, scenario-based "
        "discounted cash-flow valuation, and "
        "relative valuation using selected peers."
    )

    lines.append("")

    lines.append(
        "The valuation outputs are analytical "
        "estimates rather than investment advice. "
        "Results are sensitive to financial "
        "statement quality, market data, forecast "
        "assumptions, WACC, terminal growth, and "
        "peer selection."
    )

    lines.append("")

    lines.append(
        "## Limitations"
    )

    lines.append("")

    lines.append(
        "- Market and company data are retrieved dynamically."
    )

    lines.append(
        "- Scenario assumptions are analytical assumptions, not forecasts guaranteed by management."
    )

    lines.append(
        "- Peer multiples depend on the comparability of the selected companies."
    )

    lines.append(
        "- DCF values are sensitive to discount rates and terminal assumptions."
    )

    lines.append(
        "- Independent verification is required before using the analysis for an investment decision."
    )

    lines.append("")

    return "\n".join(
        lines
    )


def save_research_report(
    target_ticker: str,
    investment_summary: dict,
    valuation_summary: pd.DataFrame,
    output_path: Path,
    peer_comparison: pd.DataFrame | None = None,
) -> Path:
    """
    Build and save the Markdown research report.
    """

    report = build_research_report(
        target_ticker=target_ticker,
        investment_summary=investment_summary,
        valuation_summary=valuation_summary,
        peer_comparison=peer_comparison,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        report,
        encoding="utf-8",
    )

    return output_path
