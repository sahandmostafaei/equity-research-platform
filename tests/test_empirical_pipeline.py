import pandas as pd

from src.empirical_pipeline import (
    build_research_engine,
    save_company_financials,
    save_company_market_data,
)


def test_build_research_engine():

    engine = build_research_engine(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
        ],
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
    ]

    assert engine.start_date == "2018-01-01"

    assert engine.end_date is None


def test_build_research_engine_with_dates():

    engine = build_research_engine(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
        ],
        start_date="2020-01-01",
        end_date="2025-01-01",
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
    ]

    assert engine.start_date == "2020-01-01"

    assert engine.end_date == "2025-01-01"


def test_save_company_financials(tmp_path):

    dataframe = pd.DataFrame(
        {
            "revenue": [
                100.0,
                120.0,
            ],
            "ebitda": [
                20.0,
                25.0,
            ],
        }
    )

    path = save_company_financials(
        ticker="MSFT",
        dataframe=dataframe,
        output_dir=tmp_path,
    )

    assert path.exists()

    assert path.name == (
        "MSFT_financials.csv"
    )


def test_save_company_market_data(tmp_path):

    market_data = pd.Series(
        {
            "market_cap": 1000.0,
            "share_price": 100.0,
        }
    )

    path = save_company_market_data(
        ticker="MSFT",
        market_data=market_data,
        output_dir=tmp_path,
    )

    assert path.exists()

    assert path.name == (
        "MSFT_market_data.csv"
    )

    saved = pd.read_csv(
        path,
        index_col=0,
    )

    assert "value" in saved.columns
