from pathlib import Path

import pandas as pd

from src.empirical_pipeline import (
    build_research_engine,
    save_company_financials,
    save_company_market_data,
)


def test_save_company_financials(tmp_path):
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0, 110.0],
            "ebitda": [20.0, 25.0],
        }
    )

    path = save_company_financials(
        ticker="MSFT",
        dataframe=dataframe,
        output_dir=tmp_path,
    )

    assert path.exists()
    assert path.name == "MSFT_financials.csv"


def test_save_company_market_data(tmp_path):
    market_data = pd.Series(
        {
            "market_cap": 1000.0,
            "current_price": 100.0,
        }
    )

    path = save_company_market_data(
        ticker="MSFT",
        market_data=market_data,
        output_dir=tmp_path,
    )

    assert path.exists()
    assert path.name == "MSFT_market_data.csv"


def test_build_research_engine():
    engine = build_research_engine(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
        ],
    )

    assert (
        engine.config.target_ticker
        == "MSFT"
    )

    assert (
        engine.config.peer_tickers
        == [
            "GOOGL",
            "META",
        ]
    )
