from __future__ import annotations

from typing import Iterable

import pandas as pd
import yfinance as yf


def download_price_data(
    tickers: Iterable[str],
    start: str,
    end: str | None = None,
) -> pd.DataFrame:
    """
    Download adjusted closing prices for a list of securities.

    Parameters
    ----------
    tickers:
        Iterable of ticker symbols.
    start:
        Start date in YYYY-MM-DD format.
    end:
        Optional end date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Adjusted closing prices indexed by date.
    """
    tickers = list(tickers)

    if not tickers:
        raise ValueError("At least one ticker must be supplied.")

    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError("No market data was returned.")

    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            prices = data["Close"]
        else:
            prices = data.xs("Close", axis=1, level=0)
    else:
        prices = data[["Close"]].rename(columns={"Close": tickers[0]})

    prices = prices.dropna(how="all").sort_index()

    return prices


def download_financials(ticker: str) -> dict[str, pd.DataFrame]:
    """
    Download core financial statements for a company.

    Returns
    -------
    dict
        Income statement, balance sheet, and cash flow statement.
    """
    ticker_obj = yf.Ticker(ticker)

    return {
        "income_statement": ticker_obj.income_stmt,
        "balance_sheet": ticker_obj.balance_sheet,
        "cash_flow": ticker_obj.cashflow,
    }


def get_company_info(ticker: str) -> dict:
    """
    Retrieve basic company information.
    """
    ticker_obj = yf.Ticker(ticker)

    try:
        return ticker_obj.info
    except Exception:
        return {}
