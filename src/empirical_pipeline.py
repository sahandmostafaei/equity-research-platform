from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_loader import download_financials
from src.financial_data import (
    add_historical_ratios,
    build_historical_financials,
)
from src.market_data import get_basic_market_data
from src.research_engine import (
    ResearchEngine,
    ResearchEngineConfig,
)


DEFAULT_OUTPUT_DIR = Path("data/processed")


def retrieve_company_financials(
    ticker: str,
    tax_rate: float = 0.25,
) -> pd.DataFrame:
    """
    Retrieve and standardize annual financial statements.
    """
    statements = download_financials(ticker)

    historical = build_historical_financials(
        income_statement=statements["income_statement"],
        balance_sheet=statements["balance_sheet"],
        cash_flow=statements["cash_flow"],
        tax_rate=tax_rate,
    )

    return add_historical_ratios(historical)


def retrieve_company_market_data(
    ticker: str,
) -> pd.Series:
    """
    Retrieve current market information.
    """
    return get_basic_market_data(ticker)


def save_company_financials(
    ticker: str,
    dataframe: pd.DataFrame,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """
    Save standardized historical financials.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = output_dir / f"{ticker}_financials.csv"

    dataframe.to_csv(path)

    return path


def save_company_market_data(
    ticker: str,
    market_data: pd.Series,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """
    Save current market data.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = output_dir / f"{ticker}_market_data.csv"

    market_data.to_frame(
        name="value"
    ).to_csv(path)

    return path


def build_universe_financial_dataset(
    tickers: list[str],
    tax_rate: float = 0.25,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, pd.DataFrame]:
    """
    Retrieve financial data for a research universe.
    """
    results: dict[str, pd.DataFrame] = {}

    for ticker in tickers:
        financials = retrieve_company_financials(
            ticker=ticker,
            tax_rate=tax_rate,
        )

        save_company_financials(
            ticker=ticker,
            dataframe=financials,
            output_dir=output_dir,
        )

        results[ticker] = financials

    return results


def build_universe_market_dataset(
    tickers: list[str],
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, pd.Series]:
    """
    Retrieve current market data for a research universe.
    """
    results: dict[str, pd.Series] = {}

    for ticker in tickers:
        market_data = retrieve_company_market_data(
            ticker
        )

        save_company_market_data(
            ticker=ticker,
            market_data=market_data,
            output_dir=output_dir,
        )

        results[ticker] = market_data

    return results


def build_research_engine(
    target_ticker: str,
    peer_tickers: list[str],
    tax_rate: float = 0.25,
    risk_free_rate: float = 0.04,
    equity_risk_premium: float = 0.055,
    pre_tax_cost_of_debt: float = 0.045,
    forecast_years: int = 5,
    fcf_conversion: float = 0.50,
) -> ResearchEngine:
    """
    Construct a configured research engine.
    """
    config = ResearchEngineConfig(
        target_ticker=target_ticker,
        peer_tickers=peer_tickers,
        tax_rate=tax_rate,
        risk_free_rate=risk_free_rate,
        equity_risk_premium=equity_risk_premium,
        pre_tax_cost_of_debt=pre_tax_cost_of_debt,
        forecast_years=forecast_years,
        fcf_conversion=fcf_conversion,
    )

    return ResearchEngine(config)
