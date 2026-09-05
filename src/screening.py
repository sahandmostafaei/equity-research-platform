from __future__ import annotations

import pandas as pd


def apply_screen(
    companies: pd.DataFrame,
    minimum_roic: float = 0.15,
    minimum_revenue_growth: float = 0.10,
    maximum_net_debt_to_ebitda: float = 2.0,
    minimum_fcf_margin: float = 0.08,
) -> pd.DataFrame:
    """
    Apply fundamental investment-screening criteria.
    """
    required_columns = {
        "roic",
        "revenue_growth",
        "net_debt_to_ebitda",
        "fcf_margin",
    }

    missing = required_columns - set(companies.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    mask = (
        (companies["roic"] >= minimum_roic)
        & (
            companies["revenue_growth"]
            >= minimum_revenue_growth
        )
        & (
            companies["net_debt_to_ebitda"]
            <= maximum_net_debt_to_ebitda
        )
        & (companies["fcf_margin"] >= minimum_fcf_margin)
    )

    return companies.loc[mask].copy()


def rank_companies(
    companies: pd.DataFrame,
    metrics: dict[str, float] | None = None,
) -> pd.DataFrame:
    """
    Rank companies using normalized fundamental metrics.
    """
    if metrics is None:
        metrics = {
            "roic": 0.30,
            "revenue_growth": 0.20,
            "fcf_margin": 0.20,
            "ebitda_margin": 0.15,
            "interest_coverage": 0.15,
        }

    result = companies.copy()

    score = pd.Series(
        0.0,
        index=result.index,
    )

    for column, weight in metrics.items():
        if column not in result.columns:
            raise ValueError(
                f"Missing ranking column: {column}"
            )

        normalized = (
            result[column] - result[column].min()
        )

        denominator = (
            result[column].max()
            - result[column].min()
        )

        if denominator == 0:
            normalized = normalized * 0
        else:
            normalized = normalized / denominator

        score += normalized * weight

    result["fundamental_score"] = score

    return result.sort_values(
        "fundamental_score",
        ascending=False,
    )
