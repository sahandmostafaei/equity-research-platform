import pandas as pd

from src.financial_analysis import (
    calculate_fcf_margin,
    calculate_net_debt,
    calculate_roa,
    calculate_roe,
)


def test_net_debt():
    debt = pd.Series([100.0])
    cash = pd.Series([30.0])

    result = calculate_net_debt(debt, cash)

    assert result.iloc[0] == 70.0


def test_roa():
    net_income = pd.Series([20.0])
    assets = pd.Series([200.0])

    result = calculate_roa(net_income, assets)

    assert result.iloc[0] == 0.10


def test_roe():
    net_income = pd.Series([20.0])
    equity = pd.Series([100.0])

    result = calculate_roe(net_income, equity)

    assert result.iloc[0] == 0.20


def test_fcf_margin():
    fcf = pd.Series([25.0])
    revenue = pd.Series([100.0])

    result = calculate_fcf_margin(fcf, revenue)

    assert result.iloc[0] == 0.25
