from __future__ import annotations

import re

import numpy as np
import pandas as pd


def normalize_line_item_name(value: object) -> str:
    """
    Normalize financial-statement line-item names for robust matching.
    """
    text = str(value).strip().lower()

    return re.sub(
        r"[^a-z0-9]+",
        "",
        text,
    )


def find_statement_value(
    statement: pd.DataFrame,
    possible_names: list[str],
) -> pd.Series:
    """
    Find the first matching financial-statement line item.

    Matching is case-insensitive and ignores spaces,
    punctuation, underscores, and other formatting differences.
    """

    if statement.empty:
        raise ValueError(
            "Financial statement is empty."
        )

    normalized_index = {
        normalize_line_item_name(index): index
        for index in statement.index
    }

    for name in possible_names:
        normalized_name = normalize_line_item_name(
            name
        )

        if normalized_name in normalized_index:
            original_index = normalized_index[
                normalized_name
            ]

            return pd.to_numeric(
                statement.loc[original_index],
                errors="coerce",
            )

    raise KeyError(
        "Could not find any of: "
        f"{possible_names}"
    )


def clean_statement(
    statement: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and standardize a financial statement.
    """

    if statement.empty:
        raise ValueError(
            "Financial statement is empty."
        )

    cleaned = statement.copy()

    cleaned = cleaned.apply(
        pd.to_numeric,
        errors="coerce",
    )

    cleaned = cleaned.dropna(
        axis=0,
        how="all",
    )

    cleaned = cleaned.dropna(
        axis=1,
        how="all",
    )

    return cleaned


def calculate_ebitda(
    ebit: pd.Series,
    depreciation_amortization: pd.Series,
) -> pd.Series:
    """
    Estimate EBITDA as EBIT + absolute D&A.
    """

    return (
        ebit
        + depreciation_amortization.abs()
    )


def calculate_nopat(
    ebit: pd.Series,
    tax_rate: float = 0.25,
) -> pd.Series:
    """
    Calculate NOPAT using a normalized tax rate.
    """

    if not 0 <= tax_rate <= 1:
        raise ValueError(
            "Tax rate must be between 0 and 1."
        )

    return ebit * (1 - tax_rate)


def calculate_invested_capital(
    total_debt: pd.Series,
    shareholders_equity: pd.Series,
    cash: pd.Series,
) -> pd.Series:
    """
    Estimate invested capital.

    Invested Capital =
    Debt + Equity - Cash
    """

    return (
        total_debt
        + shareholders_equity
        - cash
    )


def calculate_fcf(
    operating_cash_flow: pd.Series,
    capital_expenditure: pd.Series,
) -> pd.Series:
    """
    Calculate free cash flow.

    Yahoo Finance may report capital expenditure
    as a negative cash-flow item. The model therefore
    standardizes CapEx using its absolute value:

        FCF = Operating Cash Flow - |CapEx|
    """

    return (
        operating_cash_flow
        - capital_expenditure.abs()
    )


def calculate_financial_health_score(
    roic: float,
    revenue_growth: float,
    fcf_margin: float,
    net_debt_to_ebitda: float,
    interest_coverage: float,
) -> float:
    """
    Produce a normalized fundamental quality score.

    The score is intended for research prioritization,
    not as a standalone investment decision rule.
    """

    components = []

    components.append(
        np.clip(
            roic / 0.20,
            0,
            1,
        )
    )

    components.append(
        np.clip(
            revenue_growth / 0.15,
            0,
            1,
        )
    )

    components.append(
        np.clip(
            fcf_margin / 0.15,
            0,
            1,
        )
    )

    leverage_score = 1 - np.clip(
        net_debt_to_ebitda / 4,
        0,
        1,
    )

    coverage_score = np.clip(
        interest_coverage / 10,
        0,
        1,
    )

    components.append(
        leverage_score
    )

    components.append(
        coverage_score
    )

    return float(
        np.mean(components)
    )
