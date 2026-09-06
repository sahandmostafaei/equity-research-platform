from __future__ import annotations


def classify_valuation(
    upside_downside: float,
) -> str:
    if upside_downside >= 0.25:
        return "Undervalued"
    if upside_downside >= 0.10:
        return "Moderately Undervalued"
    if upside_downside > -0.10:
        return "Fairly Valued"
    if upside_downside > -0.25:
        return "Moderately Overvalued"
    return "Overvalued"


def classify_investment_view(
    fundamental_score: float,
    valuation_upside: float,
) -> str:
    if (
        fundamental_score >= 0.75
        and valuation_upside >= 0.15
    ):
        return "Strong Buy Candidate"

    if (
        fundamental_score >= 0.60
        and valuation_upside >= 0.05
    ):
        return "Buy Candidate"

    if (
        fundamental_score >= 0.45
        and valuation_upside > -0.10
    ):
        return "Watchlist"

    return "Low Conviction"


def build_investment_summary(
    fundamental_score: float,
    valuation_upside: float,
) -> dict[str, object]:
    return {
        "fundamental_score": fundamental_score,
        "valuation_upside": valuation_upside,
        "valuation_classification": classify_valuation(
            valuation_upside
        ),
        "investment_view": classify_investment_view(
            fundamental_score,
            valuation_upside,
        ),
    }
