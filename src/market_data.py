from __future__ import annotations

import pandas as pd
import yfinance as yf


def get_current_price(
    ticker: str,
) -> float:
    """
    Retrieve the latest available market price.
    """

    data = yf.Ticker(ticker)

    history = data.history(
        period="5d",
    )

    if history.empty:
        raise ValueError(
            f"No market price available for {ticker}."
        )

    return float(
        history["Close"].dropna().iloc[-1]
    )


def get_market_cap(
    ticker: str,
) -> float:
    """
    Retrieve the latest market capitalization.
    """

    info = yf.Ticker(ticker).info

    market_cap = info.get(
        "marketCap"
    )

    if market_cap is None:
        raise ValueError(
            f"Market capitalization unavailable for {ticker}."
        )

    return float(market_cap)


def get_shares_outstanding(
    ticker: str,
) -> float:
    """
    Retrieve shares outstanding.
    """

    info = yf.Ticker(ticker).info

    shares = info.get(
        "sharesOutstanding"
    )

    if shares is None:
        raise ValueError(
            f"Shares outstanding unavailable for {ticker}."
        )

    return float(shares)


def get_basic_market_data(
    ticker: str,
) -> pd.Series:
    """
    Return a compact market-data snapshot.
    """

    info = yf.Ticker(ticker).info

    fields = {
        "ticker": ticker,
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "current_price": info.get("currentPrice"),
        "shares_outstanding": info.get(
            "sharesOutstanding"
        ),
        "trailing_pe": info.get(
            "trailingPE"
        ),
        "forward_pe": info.get(
            "forwardPE"
        ),
        "price_to_sales": info.get(
            "priceToSalesTrailing12Months"
        ),
        "enterprise_value": info.get(
            "enterpriseValue"
        ),
        "enterprise_to_ebitda": info.get(
            "enterpriseToEbitda"
        ),
    }

    return pd.Series(fields)
