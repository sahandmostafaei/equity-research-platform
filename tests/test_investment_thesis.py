import pytest

from src.investment_thesis import (
    calculate_investment_score,
    classify_score,
)


def test_investment_score():
    score = calculate_investment_score(
        valuation_upside=0.30,
        roic=0.20,
        revenue_growth=0.12,
        fcf_margin=0.15,
        net_debt_to_ebitda=1.0,
    )

    assert 0 <= score <= 1


def test_score_classification():
    assert classify_score(0.85) == "High Conviction"
    assert classify_score(0.70) == "Attractive"
    assert classify_score(0.55) == "Neutral"
    assert classify_score(0.40) == "Cautious"
    assert classify_score(0.20) == "Low Conviction"


def test_invalid_score():
    with pytest.raises(ValueError):
        classify_score(1.5)
