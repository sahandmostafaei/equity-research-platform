from __future__ import annotations

import pandas as pd
import yfinance as yf


def _get_info(
    ticker: str,
) -> dict:
    """
    Retrieve Yahoo Finance company information.
    """
    info = yf.Ticker(ticker).info

    if not isinstance(info, dict):
        return {}

    return info


def get_current_price(
    ticker: str,
) -> float:
    """
    Retrieve the latest available market price.
    """

    ticker_obj = yf.Ticker(ticker)

    history = ticker_obj.history(
        period="5d",
    )

    if history.empty:
        raise ValueError(
            f"No market price available for {ticker}."
        )

    prices = history["Close"].dropna()

    if prices.empty:
        raise ValueError(
            f"No closing price available for {ticker}."
        )

    return float(
        prices.iloc[-1]
    )


def get_market_cap(
    ticker: str,
) -> float:
    """
    Retrieve the latest market capitalization.
    """

    info = _get_info(ticker)

    market_cap = info.get(
        "marketCap"
    )

    if market_cap is None:
        raise ValueError(
            "Market capitalization unavailable "
            f"for {ticker}."
        )

    return float(
        market_cap
    )


def get_shares_outstanding(
    ticker: str,
) -> float:
    """
    Retrieve shares outstanding.
    """

    info = _get_info(ticker)

    shares = info.get(
        "sharesOutstanding"
    )

    if shares is None:
        raise ValueError(
            "Shares outstanding unavailable "
            f"for {ticker}."
        )

    return float(
        shares
    )


def get_beta(
    ticker: str,
    default: float = 1.0,
) -> float:
    """
    Retrieve beta.

    A neutral beta of 1.0 is used only when
    Yahoo Finance does not provide a usable value.
    """

    info = _get_info(ticker)

    beta = info.get(
        "beta"
    )

    if beta is None:
        return float(default)

    try:
        beta = float(beta)
    except (
        TypeError,
        ValueError,
    ):
        return float(default)

    if beta <= 0:
        return float(default)

    return beta


def get_total_debt(
    ticker: str,
) -> float:
    """
    Retrieve total debt.

    Returns zero when Yahoo Finance does not
    provide a debt value.
    """

    info = _get_info(ticker)

    debt = info.get(
        "totalDebt"
    )

    if debt is None:
        return 0.0

    try:
        return float(debt)
    except (
        TypeError,
        ValueError,
    ):
        return 0.0


def get_basic_market_data(
    ticker: str,
) -> pd.Series:
    """
    Return a standardized market-data snapshot.
    """

    info = _get_info(ticker)

    current_price = info.get(
        "currentPrice"
    )

    if current_price is None:
        try:
            current_price = get_current_price(
                ticker
            )
        except ValueError:
            current_price = None

    market_cap = info.get(
        "marketCap"
    )

    shares_outstanding = info.get(
        "sharesOutstanding"
    )

    beta = info.get(
        "beta"
    )

    total_debt = info.get(
        "totalDebt"
    )

    if beta is None:
        beta = 1.0

    if total_debt is None:
        total_debt = 0.0

    fields = {
        "ticker": ticker,
        "company": info.get(
            "longName"
        ),
        "sector": info.get(
            "sector"
        ),
        "industry": info.get(
            "industry"
        ),
        "market_cap": market_cap,
        "current_price": current_price,
        "shares_outstanding": (
            shares_outstanding
        ),
        "beta": beta,
        "total_debt": total_debt,
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

    return pd.Series(
        fields,
        dtype="object",
    )
