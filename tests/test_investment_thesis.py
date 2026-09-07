import pytest

from src.investment_thesis import (
    InvestmentThesis,
    build_investment_assessment,
    build_thesis,
    calculate_investment_score,
    classify_score,
    classify_valuation_view,
)


def test_investment_score_is_between_zero_and_one():
    score = calculate_investment_score(
        valuation_upside=0.20,
        roic=0.20,
        revenue_growth=0.10,
        fcf_margin=0.15,
        net_debt_to_ebitda=1.0,
    )

    assert 0.0 <= score <= 1.0


def test_high_quality_company_gets_higher_score():
    strong = calculate_investment_score(
        valuation_upside=0.30,
        roic=0.25,
        revenue_growth=0.20,
        fcf_margin=0.20,
        net_debt_to_ebitda=0.0,
    )

    weak = calculate_investment_score(
        valuation_upside=-0.20,
        roic=0.05,
        revenue_growth=0.02,
        fcf_margin=0.03,
        net_debt_to_ebitda=4.0,
    )

    assert strong > weak


def test_score_classification():
    assert classify_score(0.85) == "High Conviction"
    assert classify_score(0.70) == "Attractive"
    assert classify_score(0.55) == "Neutral"
    assert classify_score(0.40) == "Cautious"
    assert classify_score(0.20) == "Low Conviction"


def test_score_rejects_invalid_values():
    with pytest.raises(ValueError):
        classify_score(-0.01)

    with pytest.raises(ValueError):
        classify_score(1.01)


def test_valuation_classification():
    assert (
        classify_valuation_view(0.30)
        == "Significantly Undervalued"
    )

    assert (
        classify_valuation_view(0.15)
        == "Moderately Undervalued"
    )

    assert (
        classify_valuation_view(0.00)
        == "Fairly Valued"
    )

    assert (
        classify_valuation_view(-0.15)
        == "Moderately Overvalued"
    )

    assert (
        classify_valuation_view(-0.30)
        == "Significantly Overvalued"
    )


def test_build_investment_assessment():
    result = build_investment_assessment(
        valuation_upside=0.20,
        roic=0.20,
        revenue_growth=0.10,
        fcf_margin=0.15,
        net_debt_to_ebitda=1.0,
    )

    assert "fundamental_score" in result
    assert "score_classification" in result
    assert "valuation_upside" in result
    assert "valuation_classification" in result

    assert result["valuation_upside"] == 0.20


def test_investment_thesis_validation():
    thesis = InvestmentThesis(
        company="Microsoft",
        thesis="Strong fundamental profile.",
        catalysts=[
            "Revenue growth",
        ],
        risks=[
            "Valuation sensitivity",
        ],
        valuation_view="Moderately Undervalued",
        conclusion="Further diligence warranted.",
    )

    thesis.validate()

    result = thesis.to_dict()

    assert result["company"] == "Microsoft"
    assert len(result["catalysts"]) == 1
    assert len(result["risks"]) == 1


def test_empty_thesis_rejected():
    thesis = InvestmentThesis(
        company="",
        thesis="",
        catalysts=[],
        risks=[],
        valuation_view="",
        conclusion="",
    )

    with pytest.raises(ValueError):
        thesis.validate()


def test_build_thesis():
    result = build_thesis(
        company="Microsoft",
        valuation_upside=0.20,
        fundamental_score=0.75,
        catalysts=[
            "Cloud growth",
            "Operating leverage",
        ],
        risks=[
            "High valuation",
            "Competition",
        ],
    )

    assert isinstance(
        result,
        InvestmentThesis,
    )

    assert result.company == "Microsoft"
    assert len(result.catalysts) == 2
    assert len(result.risks) == 2
    assert result.valuation_view == (
        "Moderately Undervalued"
    )
