from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.data_loader import download_price_data


@dataclass
class ResearchUniverse:
    """
    Defines a research universe of securities.
    """

    tickers: list[str]
    start_date: str
    end_date: str | None = None


def build_price_universe(
    universe: ResearchUniverse,
) -> pd.DataFrame:
    """
    Download market data for a research universe.
    """
    return download_price_data(
        tickers=universe.tickers,
        start=universe.start_date,
        end=universe.end_date,
    )


def calculate_returns(
    prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    """
    return prices.pct_change().dropna(how="all")


def calculate_cumulative_returns(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate cumulative returns.
    """
    return (1 + returns).cumprod() - 1
