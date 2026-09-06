from src.investment_decision import (
    build_investment_summary,
    classify_investment_view,
    classify_valuation,
)


def test_valuation_classification():
    assert classify_valuation(0.30) == "Undervalued"
    assert classify_valuation(0.15) == "Moderately Undervalued"
    assert classify_valuation(0.00) == "Fairly Valued"
    assert classify_valuation(-0.15) == "Moderately Overvalued"
    assert classify_valuation(-0.30) == "Overvalued"


def test_investment_view():
    assert (
        classify_investment_view(0.80, 0.20)
        == "Strong Buy Candidate"
    )

    assert (
        classify_investment_view(0.65, 0.10)
        == "Buy Candidate"
    )

    assert (
        classify_investment_view(0.50, 0.00)
        == "Watchlist"
    )


def test_investment_summary():
    result = build_investment_summary(
        fundamental_score=0.80,
        valuation_upside=0.20,
    )

    assert result["investment_view"] == (
        "Strong Buy Candidate"
    )
