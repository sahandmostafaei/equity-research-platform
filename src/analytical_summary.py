from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def build_fundamental_kpi_summary(
    historical_financials: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a compact fundamental KPI summary from
    standardized historical financial statements.
    """

    if historical_financials.empty:
        raise ValueError(
            "Historical financials cannot be empty."
        )

    metrics = {}

    latest = historical_financials.iloc[-1]

    preferred_metrics = [
        "revenue",
        "ebit",
        "ebitda",
        "net_income",
        "free_cash_flow",
        "revenue_growth",
        "ebit_margin",
        "ebitda_margin",
        "net_margin",
        "roic",
        "roa",
        "roe",
        "net_debt",
        "net_debt_to_ebitda",
    ]

    for metric in preferred_metrics:
        if metric in historical_financials.columns:
            value = latest[metric]

            if pd.notna(value):
                metrics[metric] = float(value)

    if not metrics:
        raise ValueError(
            "No recognized fundamental metrics "
            "were found."
        )

    result = pd.DataFrame(
        {
            "metric": list(metrics.keys()),
            "latest_value": list(metrics.values()),
        }
    )

    return result


def build_valuation_range(
    valuation_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert valuation outputs into a compact
    valuation-range table.
    """

    if valuation_summary.empty:
        raise ValueError(
            "Valuation summary cannot be empty."
        )

    required_columns = {
        "method",
        "implied_per_share",
    }

    missing = required_columns.difference(
        valuation_summary.columns
    )

    if missing:
        raise ValueError(
            "Valuation summary is missing columns: "
            + ", ".join(sorted(missing))
        )

    result = valuation_summary[
        [
            "method",
            "implied_per_share",
        ]
    ].copy()

    result = result.dropna(
        subset=["implied_per_share"]
    )

    result = result[
        np.isfinite(
            result["implied_per_share"]
        )
    ]

    if result.empty:
        raise ValueError(
            "No valid valuation observations were found."
        )

    result = result.sort_values(
        "implied_per_share"
    ).reset_index(drop=True)

    return result


def calculate_valuation_statistics(
    valuation_range: pd.DataFrame,
) -> dict[str, float]:
    """
    Calculate summary statistics for valuation outputs.
    """

    if valuation_range.empty:
        raise ValueError(
            "Valuation range cannot be empty."
        )

    values = valuation_range[
        "implied_per_share"
    ].astype(float)

    return {
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "mean": float(values.mean()),
        "median": float(values.median()),
        "standard_deviation": float(
            values.std(ddof=1)
        )
        if len(values) > 1
        else 0.0,
    }


def build_scenario_summary(
    scenario_valuations: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a clean scenario valuation table.
    """

    if scenario_valuations.empty:
        raise ValueError(
            "Scenario valuations cannot be empty."
        )

    result = scenario_valuations.copy()

    return result.reset_index(
        drop=True
    )


def build_peer_relative_summary(
    peer_comparison: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a peer-relative valuation summary.
    """

    if peer_comparison.empty:
        return pd.DataFrame()

    return peer_comparison.copy().reset_index(
        drop=True
    )


def build_research_dashboard(
    result: Any,
) -> dict[str, Any]:
    """
    Build the complete analytical dashboard used by
    the reporting layer.
    """

    valuation_range = build_valuation_range(
        result.valuation_summary
    )

    valuation_statistics = (
        calculate_valuation_statistics(
            valuation_range
        )
    )

    fundamental_kpis = (
        build_fundamental_kpi_summary(
            result.historical_financials
        )
    )

    scenario_summary = (
        build_scenario_summary(
            result.scenario_valuations
        )
    )

    peer_summary = (
        build_peer_relative_summary(
            result.peer_comparison
        )
    )

    return {
        "target_ticker": result.target_ticker,
        "fundamental_kpis": fundamental_kpis,
        "valuation_range": valuation_range,
        "valuation_statistics": valuation_statistics,
        "scenario_summary": scenario_summary,
        "peer_summary": peer_summary,
        "investment_summary": result.investment_summary,
        "estimated_wacc": result.estimated_wacc,
    }


def save_research_dashboard(
    dashboard: dict[str, Any],
    output_dir,
) -> dict[str, object]:
    """
    Save dashboard components as CSV files.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    paths = {}

    fundamental_path = (
        output_dir
        / "fundamental_kpis.csv"
    )

    dashboard[
        "fundamental_kpis"
    ].to_csv(
        fundamental_path,
        index=False,
    )

    paths["fundamental_kpis"] = (
        fundamental_path
    )

    valuation_path = (
        output_dir
        / "valuation_range.csv"
    )

    dashboard[
        "valuation_range"
    ].to_csv(
        valuation_path,
        index=False,
    )

    paths["valuation_range"] = (
        valuation_path
    )

    scenario_path = (
        output_dir
        / "scenario_summary.csv"
    )

    dashboard[
        "scenario_summary"
    ].to_csv(
        scenario_path,
        index=False,
    )

    paths["scenario_summary"] = (
        scenario_path
    )

    if not dashboard[
        "peer_summary"
    ].empty:
        peer_path = (
            output_dir
            / "peer_relative_summary.csv"
        )

        dashboard[
            "peer_summary"
        ].to_csv(
            peer_path,
            index=False,
        )

        paths["peer_relative_summary"] = (
            peer_path
        )

    return paths
