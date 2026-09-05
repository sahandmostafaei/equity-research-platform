import pandas as pd

from src.screening import apply_screen, rank_companies


def test_apply_screen():
    companies = pd.DataFrame(
        {
            "roic": [0.20, 0.10],
            "revenue_growth": [0.15, 0.12],
            "net_debt_to_ebitda": [1.2, 1.5],
            "fcf_margin": [0.12, 0.10],
        },
        index=["Company A", "Company B"],
    )

    result = apply_screen(companies)

    assert list(result.index) == ["Company A"]


def test_rank_companies():
    companies = pd.DataFrame(
        {
            "roic": [0.20, 0.10],
            "revenue_growth": [0.15, 0.08],
            "fcf_margin": [0.12, 0.05],
            "ebitda_margin": [0.25, 0.15],
            "interest_coverage": [10.0, 5.0],
        },
        index=["Company A", "Company B"],
    )

    result = rank_companies(companies)

    assert result.index[0] == "Company A"
    assert "fundamental_score" in result.columns
