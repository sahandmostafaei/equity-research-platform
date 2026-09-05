from __future__ import annotations

import numpy as np
import pandas as pd


def find_statement_value(
    statement: pd.DataFrame,
    possible_names: list[str],
) -> pd.Series:
    """
    Find the first matching financial-statement line item.
    """

    if statement.empty:
        raise ValueError("Financial statement is empty.")

    normalized = {
        str(index).lower().replace(" ", "").replace("_", ""): index
        for index in statement.index
    }

    for name in possible_names:
        key = name.lower().replace(" ", "").replace("_", "")

        if key in normalized:
            return pd.to_numeric(
                statement.loc[normalized[key]],
                errors="coerce",
            )

    raise KeyError(
        f"Could not find any of: {possible_names}"
    )


def clean_statement(
    statement: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and standardize a financial statement.
    """

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
    Estimate EBITDA as EBIT + D&A.
    """

    return ebit + depreciation_amortization.abs()


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
    Produce a simple normalized fundamental quality score.

    The score is intended for research prioritization,
    not as a standalone investment decision rule.
    """

    components = []

    components.append(
        np.clip(roic / 0.20, 0, 1)
    )

    components.append(
        np.clip(revenue_growth / 0.15, 0, 1)
    )

    components.append(
        np.clip(fcf_margin / 0.15, 0, 1)
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

    components.append(leverage_score)
    components.append(coverage_score)

    return float(np.mean(components))
