import pandas as pd
import pytest

from src.research_engine import (
    build_investment_assessment,
)


def test_build_investment_assessment():
    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF",
                "EV/EBITDA",
                "P/E",
            ],
            "implied_per_share": [
                120.0,
                110.0,
                115.0,
            ],
        }
    )

    result = build_investment_assessment(
        valuation_summary=valuation_summary,
        roic=0.15,
        revenue_growth=0.10,
        fcf_margin=0.15,
        net_debt_to_ebitda=1.0,
    )

    assert isinstance(result, dict)

    assert "fundamental_score" in result
    assert "valuation_upside" in result
    assert "valuation_classification" in result

    assert 0.0 <= result["fundamental_score"] <= 1.0


def test_build_investment_assessment_rejects_empty_valuation():
    valuation_summary = pd.DataFrame()

    with pytest.raises(ValueError):
        build_investment_assessment(
            valuation_summary=valuation_summary,
            roic=0.15,
            revenue_growth=0.10,
            fcf_margin=0.15,
            net_debt_to_ebitda=1.0,
        )


def test_build_investment_assessment_with_positive_valuation():
    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF",
                "EV/EBITDA",
            ],
            "implied_per_share": [
                150.0,
                140.0,
            ],
        }
    )

    result = build_investment_assessment(
        valuation_summary=valuation_summary,
        roic=0.20,
        revenue_growth=0.12,
        fcf_margin=0.18,
        net_debt_to_ebitda=0.5,
    )

    assert result["fundamental_score"] > 0
    assert result["valuation_upside"] is not None


def test_build_investment_assessment_handles_multiple_methods():
    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF",
                "P/E",
                "EV/EBITDA",
                "Price/Sales",
            ],
            "implied_per_share": [
                100.0,
                110.0,
                105.0,
                95.0,
            ],
        }
    )

    result = build_investment_assessment(
        valuation_summary=valuation_summary,
        roic=0.12,
        revenue_growth=0.08,
        fcf_margin=0.12,
        net_debt_to_ebitda=1.5,
    )

    assert isinstance(result, dict)
    assert isinstance(
        result["fundamental_score"],
        float,
    )
    assert 0.0 <= result["fundamental_score"] <= 1.0
