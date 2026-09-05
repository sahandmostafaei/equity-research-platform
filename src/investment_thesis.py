from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InvestmentThesis:
    """
    Structured investment thesis.
    """

    company: str
    thesis: str
    catalysts: list[str]
    risks: list[str]
    valuation_view: str
    conclusion: str


def calculate_investment_score(
    valuation_upside: float,
    roic: float,
    revenue_growth: float,
    fcf_margin: float,
    net_debt_to_ebitda: float,
) -> float:
    """
    Calculate a simple investment-attractiveness score.

    The score is a research prioritization tool and
    should not be interpreted as a trading signal.
    """

    valuation_score = max(
        0.0,
        min(1.0, (valuation_upside + 0.20) / 0.70),
    )

    quality_score = max(
        0.0,
        min(1.0, roic / 0.25),
    )

    growth_score = max(
        0.0,
        min(1.0, revenue_growth / 0.20),
    )

    cash_flow_score = max(
        0.0,
        min(1.0, fcf_margin / 0.20),
    )

    leverage_score = 1 - max(
        0.0,
        min(1.0, net_debt_to_ebitda / 4.0),
    )

    score = (
        0.30 * valuation_score
        + 0.25 * quality_score
        + 0.15 * growth_score
        + 0.15 * cash_flow_score
        + 0.15 * leverage_score
    )

    return float(score)


def classify_score(
    score: float,
) -> str:
    """
    Convert an investment score into a research classification.
    """

    if not 0 <= score <= 1:
        raise ValueError(
            "Score must be between 0 and 1."
        )

    if score >= 0.80:
        return "High Conviction"

    if score >= 0.65:
        return "Attractive"

    if score >= 0.50:
        return "Neutral"

    if score >= 0.35:
        return "Cautious"

    return "Low Conviction"
