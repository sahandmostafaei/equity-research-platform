from __future__ import annotations

import pandas as pd


def standardize_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize DataFrame column names.
    """

    result = dataframe.copy()

    result.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        for column in result.columns
    ]

    return result


def clean_numeric_series(
    series: pd.Series,
) -> pd.Series:
    """
    Convert a financial series to numeric values.
    """

    return pd.to_numeric(
        series,
        errors="coerce",
    )


def align_financial_series(
    *series: pd.Series,
) -> list[pd.Series]:
    """
    Align multiple financial series on a common index.
    """

    dataframe = pd.concat(
        series,
        axis=1,
        join="inner",
    )

    return [
        dataframe.iloc[:, i]
        for i in range(dataframe.shape[1])
    ]


def calculate_average_growth(
    series: pd.Series,
) -> float:
    """
    Calculate the geometric average growth rate.
    """

    cleaned = series.dropna()

    if len(cleaned) < 2:
        raise ValueError(
            "At least two observations are required."
        )

    beginning = cleaned.iloc[0]
    ending = cleaned.iloc[-1]
    periods = len(cleaned) - 1

    if beginning <= 0 or ending <= 0:
        raise ValueError(
            "Beginning and ending values must be positive."
        )

    return float(
        (ending / beginning) ** (1 / periods) - 1
    )


def create_financial_summary(
    revenue: pd.Series,
    ebitda: pd.Series,
    free_cash_flow: pd.Series,
) -> pd.DataFrame:
    """
    Create a compact financial-performance summary.
    """

    summary = pd.DataFrame(
        {
            "revenue": revenue,
            "ebitda": ebitda,
            "free_cash_flow": free_cash_flow,
        }
    )

    summary["ebitda_margin"] = (
        summary["ebitda"]
        / summary["revenue"]
    )

    summary["fcf_margin"] = (
        summary["free_cash_flow"]
        / summary["revenue"]
    )

    return summary
