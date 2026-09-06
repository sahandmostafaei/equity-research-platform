import pandas as pd

from src.research_engine import (
    ResearchEngine,
    ResearchEngineConfig,
)


def test_research_engine_config_defaults():
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
        ],
    )

    assert config.target_ticker == "MSFT"
    assert config.forecast_years == 5
    assert config.fcf_conversion == 0.50


def test_research_engine_initializes():
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=["GOOGL"],
    )

    engine = ResearchEngine(config)

    assert (
        engine.config.target_ticker
        == "MSFT"
    )


def test_research_engine_market_metrics():
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=["GOOGL"],
    )

    engine = ResearchEngine(config)

    historical = pd.DataFrame(
        {
            "revenue": [
                100.0,
                110.0,
            ],
            "ebitda": [
                25.0,
                30.0,
            ],
            "net_income": [
                15.0,
                18.0,
            ],
            "free_cash_flow": [
                12.0,
                15.0,
            ],
            "total_debt": [
                20.0,
                22.0,
            ],
            "cash": [
                10.0,
                12.0,
            ],
        }
    )

    market_data = pd.Series(
        {
            "market_cap": 500.0,
            "shares_outstanding": 100.0,
        }
    )

    result = (
        engine.calculate_market_metrics(
            historical_financials=historical,
            market_data=market_data,
        )
    )

    assert result["market_cap"] == 500.0
    assert result["enterprise_value"] == 510.0
    assert result["eps"] == 0.18
    assert result["ev_ebitda"] == 17.0
    assert result["fcf_yield"] == 0.03


def test_research_engine_scenario_structure():
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=["GOOGL"],
    )

    engine = ResearchEngine(config)

    historical = pd.DataFrame(
        {
            "revenue": [
                100.0,
                110.0,
            ],
            "total_debt": [
                20.0,
                22.0,
            ],
            "cash": [
                10.0,
                12.0,
            ],
        }
    )

    market_data = pd.Series(
        {
            "shares_outstanding": 100.0,
        }
    )

    result = engine.run_scenarios(
        historical_financials=historical,
        market_data=market_data,
    )

    assert len(result) == 3

    assert set(
        result["scenario"]
    ) == {
        "Bear",
        "Base",
        "Bull",
    }


def test_research_engine_investment_assessment():
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=["GOOGL"],
    )

    engine = ResearchEngine(config)

    historical = pd.DataFrame(
        {
            "roic": [0.18],
            "revenue_growth": [0.12],
            "fcf_margin": [0.15],
            "net_debt_to_ebitda": [1.0],
        }
    )

    market_data = pd.Series(
        {
            "current_price": 100.0,
        }
    )

    scenarios = pd.DataFrame(
        {
            "per_share_value": [
                110.0,
                120.0,
                130.0,
            ]
        }
    )

    result = (
        engine.build_investment_assessment(
            historical_financials=historical,
            market_data=market_data,
            scenario_valuations=scenarios,
        )
    )

    assert result["market_price"] == 100.0
    assert result["consensus_value"] == 120.0
    assert result["valuation_upside"] == 0.20

    assert (
        0
        <= result["fundamental_score"]
        <= 1
    )

    assert "investment_view" in result
