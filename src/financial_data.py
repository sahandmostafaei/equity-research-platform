from __future__ import annotations

import pandas as pd

from src.financial_statements import (
    calculate_ebitda,
    calculate_fcf,
    calculate_invested_capital,
    calculate_nopat,
    find_statement_value,
)


LINE_ITEM_ALIASES = {
    "revenue": [
        "Total Revenue",
        "Operating Revenue",
        "Revenue",
    ],
    "ebit": [
        "EBIT",
        "Operating Income",
    ],
    "net_income": [
        "Net Income",
        "Net Income Common Stockholders",
        "Net Income Including Noncontrolling Interests",
    ],
    "depreciation_amortization": [
        "Reconciled Depreciation",
        "Depreciation And Amortization",
        "Depreciation",
        "Depreciation Amortization Depletion",
    ],
    "operating_cash_flow": [
        "Operating Cash Flow",
        "Total Cash From Operating Activities",
        "Cash Flow From Continuing Operating Activities",
    ],
    "capital_expenditure": [
        "Capital Expenditure",
        "Capital Expenditure Reported",
        "Purchase Of PPE",
    ],
    "total_debt": [
        "Total Debt",
        "Total Debt And Capital Lease Obligation",
    ],
    "cash": [
        "Cash Cash Equivalents And Short Term Investments",
        "Cash And Cash Equivalents",
        "Cash Financial",
    ],
    "total_assets": [
        "Total Assets",
    ],
    "shareholders_equity": [
        "Stockholders Equity",
        "Common Stock Equity",
        "Total Equity Gross Minority Interest",
    ],
    "interest_expense": [
        "Interest Expense Non Operating",
        "Interest Expense",
    ],
}


def extract_line_item(
    statement: pd.DataFrame,
    metric: str,
) -> pd.Series:
    """
    Extract a standardized financial metric from a Yahoo Finance statement.
    """
    if metric not in LINE_ITEM_ALIASES:
        raise KeyError(f"Unknown financial metric: {metric}")

    return find_statement_value(
        statement,
        LINE_ITEM_ALIASES[metric],
    )


def build_historical_financials(
    income_statement: pd.DataFrame,
    balance_sheet: pd.DataFrame,
    cash_flow: pd.DataFrame,
    tax_rate: float = 0.25,
) -> pd.DataFrame:
    """
    Build a standardized annual historical financial dataset.
    """
    revenue = extract_line_item(
        income_statement,
        "revenue",
    )
    ebit = extract_line_item(
        income_statement,
        "ebit",
    )
    net_income = extract_line_item(
        income_statement,
        "net_income",
    )
    depreciation = extract_line_item(
        income_statement,
        "depreciation_amortization",
    )

    operating_cash_flow = extract_line_item(
        cash_flow,
        "operating_cash_flow",
    )
    capital_expenditure = extract_line_item(
        cash_flow,
        "capital_expenditure",
    )

    total_debt = extract_line_item(
        balance_sheet,
        "total_debt",
    )
    cash = extract_line_item(
        balance_sheet,
        "cash",
    )
    total_assets = extract_line_item(
        balance_sheet,
        "total_assets",
    )
    shareholders_equity = extract_line_item(
        balance_sheet,
        "shareholders_equity",
    )

    ebitda = calculate_ebitda(
        ebit,
        depreciation,
    )

    free_cash_flow = calculate_fcf(
        operating_cash_flow,
        capital_expenditure,
    )

    nopat = calculate_nopat(
        ebit,
        tax_rate=tax_rate,
    )

    invested_capital = calculate_invested_capital(
        total_debt,
        shareholders_equity,
        cash,
    )

    historical = pd.concat(
        [
            revenue.rename("revenue"),
            ebitda.rename("ebitda"),
            ebit.rename("ebit"),
            net_income.rename("net_income"),
            operating_cash_flow.rename("operating_cash_flow"),
            capital_expenditure.rename("capital_expenditure"),
            free_cash_flow.rename("free_cash_flow"),
            total_debt.rename("total_debt"),
            cash.rename("cash"),
            total_assets.rename("total_assets"),
            shareholders_equity.rename("shareholders_equity"),
            nopat.rename("nopat"),
            invested_capital.rename("invested_capital"),
        ],
        axis=1,
    )

    historical = historical.sort_index()

    return historical


def add_historical_ratios(
    historical: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add standard fundamental analysis ratios.
    """
    result = historical.copy()

    result["revenue_growth"] = result["revenue"].pct_change()
    result["ebitda_margin"] = (
        result["ebitda"] / result["revenue"]
    )
    result["ebit_margin"] = (
        result["ebit"] / result["revenue"]
    )
    result["net_margin"] = (
        result["net_income"] / result["revenue"]
    )
    result["fcf_margin"] = (
        result["free_cash_flow"] / result["revenue"]
    )
    result["roic"] = (
        result["nopat"] / result["invested_capital"]
    )
    result["roa"] = (
        result["net_income"] / result["total_assets"]
    )
    result["roe"] = (
        result["net_income"] / result["shareholders_equity"]
    )
    result["net_debt"] = (
        result["total_debt"] - result["cash"]
    )
    result["net_debt_to_ebitda"] = (
        result["net_debt"] / result["ebitda"]
    )

    return result
