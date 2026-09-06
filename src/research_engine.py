from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.config import (
    get_float_config,
    get_int_config,
    load_research_config,
)
from src.data_loader import download_financials
from src.financial_data import (
    add_historical_ratios,
    build_historical_financials,
)
from src.investment_decision import build_investment_summary
from src.investment_thesis import (
    calculate_investment_score,
    classify_score,
)
from src.market_data import get_basic_market_data
from src.research_metrics import build_market_metrics
from src.scenario_valuation import run_all_scenarios
from src.scenarios import Scenario


@dataclass
class ResearchEngineConfig:
    target_ticker: str
    peer_tickers: list[str]
    tax_rate: float = 0.25
    risk_free_rate: float = 0.04
    equity_risk_premium: float = 0.055
    pre_tax_cost_of_debt: float = 0.045
    forecast_years: int = 5
    fcf_conversion: float = 0.50


@dataclass
class ResearchEngineResult:
    target_ticker: str
    historical_financials: pd.DataFrame
    market_data: pd.Series
    market_metrics: pd.Series
    scenario_valuations: pd.DataFrame
    investment_summary: dict[str, object]


class ResearchEngine:
    """
    High-level equity research workflow.

    Architecture:

        Configuration
            ↓
        Financial Data
            ↓
        Fundamental Analysis
            ↓
        Market Analysis
            ↓
        Forecasting
            ↓
        Scenario Valuation
            ↓
        Investment Assessment
    """

    def __init__(
        self,
        config: ResearchEngineConfig,
    ) -> None:
        self.config = config

    def load_target_financials(
        self,
    ) -> pd.DataFrame:
        statements = download_financials(
            self.config.target_ticker
        )

        historical = build_historical_financials(
            income_statement=statements["income_statement"],
            balance_sheet=statements["balance_sheet"],
            cash_flow=statements["cash_flow"],
            tax_rate=self.config.tax_rate,
        )

        return add_historical_ratios(historical)

    def load_market_data(self) -> pd.Series:
        return get_basic_market_data(
            self.config.target_ticker
        )

    def calculate_market_metrics(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.Series:
        required = [
            "revenue",
            "ebitda",
            "net_income",
            "free_cash_flow",
            "total_debt",
            "cash",
        ]

        available = historical_financials.dropna(
            subset=required
        )

        if available.empty:
            raise ValueError(
                "No complete historical financial observation "
                "is available for market-metric calculation."
            )

        latest = available.iloc[-1]

        market_cap = float(
            market_data["market_cap"]
        )

        shares_outstanding = float(
            market_data["shares_outstanding"]
        )

        return build_market_metrics(
            market_cap=market_cap,
            total_debt=float(latest["total_debt"]),
            cash=float(latest["cash"]),
            revenue=float(latest["revenue"]),
            ebitda=float(latest["ebitda"]),
            net_income=float(latest["net_income"]),
            free_cash_flow=float(
                latest["free_cash_flow"]
            ),
            shares_outstanding=shares_outstanding,
        )

    def estimate_cost_of_capital(
        self,
        market_data: pd.Series,
    ) -> float:
        market_cap = float(
            market_data["market_cap"]
        )

        beta = float(
            market_data.get("beta", 1.0)
            or 1.0
        )

        cost_of_equity = (
            self.config.risk_free_rate
            + beta
            * self.config.equity_risk_premium
        )

        debt = float(
            market_data.get("totalDebt", 0.0)
            or 0.0
        )

        after_tax_cost_of_debt = (
            self.config.pre_tax_cost_of_debt
            * (1 - self.config.tax_rate)
        )

        total_capital = market_cap + debt

        if total_capital <= 0:
            raise ValueError(
                "Total capital must be positive."
            )

        equity_weight = (
            market_cap / total_capital
        )

        debt_weight = (
            debt / total_capital
        )

        return (
            equity_weight * cost_of_equity
            + debt_weight * after_tax_cost_of_debt
        )

    def build_scenarios(
        self,
    ) -> dict[str, Scenario]:
        return {
            "bear": Scenario(
                name="Bear",
                revenue_growth=0.03,
                ebitda_margin=0.18,
                wacc=0.11,
                terminal_growth=0.02,
            ),
            "base": Scenario(
                name="Base",
                revenue_growth=0.07,
                ebitda_margin=0.22,
                wacc=0.09,
                terminal_growth=0.025,
            ),
            "bull": Scenario(
                name="Bull",
                revenue_growth=0.12,
                ebitda_margin=0.26,
                wacc=0.08,
                terminal_growth=0.03,
            ),
        }

    def run_scenarios(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.DataFrame:
        historical_revenue = (
            historical_financials["revenue"]
            .dropna()
        )

        if historical_revenue.empty:
            raise ValueError(
                "Historical revenue cannot be empty."
            )

        latest = historical_financials.dropna(
            subset=[
                "total_debt",
                "cash",
            ]
        ).iloc[-1]

        return run_all_scenarios(
            historical_revenue=historical_revenue,
            scenarios=self.build_scenarios(),
            total_debt=float(
                latest["total_debt"]
            ),
            cash=float(
                latest["cash"]
            ),
            shares_outstanding=float(
                market_data["shares_outstanding"]
            ),
            fcf_conversion=self.config.fcf_conversion,
            years=self.config.forecast_years,
        )

    def build_investment_assessment(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
        scenario_valuations: pd.DataFrame,
    ) -> dict[str, object]:
        required = [
            "roic",
            "revenue_growth",
            "fcf_margin",
            "net_debt_to_ebitda",
        ]

        available = historical_financials.dropna(
            subset=required
        )

        if available.empty:
            raise ValueError(
                "No complete fundamental observation "
                "is available for investment scoring."
            )

        latest = available.iloc[-1]

        market_price = float(
            market_data["current_price"]
        )

        valuation_values = (
            scenario_valuations[
                "per_share_value"
            ]
        )

        consensus_value = float(
            valuation_values.median()
        )

        valuation_upside = (
            consensus_value / market_price
        ) - 1

        investment_score = (
            calculate_investment_score(
                valuation_upside=valuation_upside,
                roic=float(latest["roic"]),
                revenue_growth=float(
                    latest["revenue_growth"]
                ),
                fcf_margin=float(
                    latest["fcf_margin"]
                ),
                net_debt_to_ebitda=float(
                    latest["net_debt_to_ebitda"]
                ),
            )
        )

        summary = build_investment_summary(
            fundamental_score=investment_score,
            valuation_upside=valuation_upside,
        )

        summary["consensus_value"] = (
            consensus_value
        )

        summary["market_price"] = market_price

        summary["score_classification"] = (
            classify_score(investment_score)
        )

        return summary

    def run(self) -> ResearchEngineResult:
        historical_financials = (
            self.load_target_financials()
        )

        market_data = self.load_market_data()

        market_metrics = (
            self.calculate_market_metrics(
                historical_financials=historical_financials,
                market_data=market_data,
            )
        )

        scenario_valuations = (
            self.run_scenarios(
                historical_financials=historical_financials,
                market_data=market_data,
            )
        )

        investment_summary = (
            self.build_investment_assessment(
                historical_financials=historical_financials,
                market_data=market_data,
                scenario_valuations=scenario_valuations,
            )
        )

        return ResearchEngineResult(
            target_ticker=self.config.target_ticker,
            historical_financials=historical_financials,
            market_data=market_data,
            market_metrics=market_metrics,
            scenario_valuations=scenario_valuations,
            investment_summary=investment_summary,
        )


def create_default_research_engine() -> ResearchEngine:
    """
    Create the default MSFT research engine.

    Configuration is loaded from data/research_config.csv
    when available. Hard-coded defaults provide a safe fallback.
    """
    try:
        config_table = load_research_config()

        target_ticker = get_config_value(
            config_table,
            "target_ticker",
        )

        peer_tickers = [
            get_config_value(
                config_table,
                f"peer_{index}",
            )
            for index in range(1, 5)
        ]

        tax_rate = get_float_config(
            config_table,
            "tax_rate",
        )

        risk_free_rate = get_float_config(
            config_table,
            "risk_free_rate",
        )

        equity_risk_premium = get_float_config(
            config_table,
            "equity_risk_premium",
        )

        pre_tax_cost_of_debt = get_float_config(
            config_table,
            "pre_tax_cost_of_debt",
        )

        forecast_years = get_int_config(
            config_table,
            "forecast_years",
        )

        fcf_conversion = get_float_config(
            config_table,
            "fcf_conversion",
        )

    except (
        FileNotFoundError,
        KeyError,
        ValueError,
    ):
        target_ticker = "MSFT"
        peer_tickers = [
            "GOOGL",
            "META",
            "AAPL",
            "AMZN",
        ]
        tax_rate = 0.25
        risk_free_rate = 0.04
        equity_risk_premium = 0.055
        pre_tax_cost_of_debt = 0.045
        forecast_years = 5
        fcf_conversion = 0.50

    return ResearchEngine(
        ResearchEngineConfig(
            target_ticker=target_ticker,
            peer_tickers=peer_tickers,
            tax_rate=tax_rate,
            risk_free_rate=risk_free_rate,
            equity_risk_premium=equity_risk_premium,
            pre_tax_cost_of_debt=pre_tax_cost_of_debt,
            forecast_years=forecast_years,
            fcf_conversion=fcf_conversion,
        )
    )


def get_config_value(
    config: pd.DataFrame,
    parameter: str,
) -> str:
    matches = config.loc[
        config["parameter"] == parameter,
        "value",
    ]

    if matches.empty:
        raise KeyError(
            f"Configuration parameter not found: {parameter}"
        )

    return str(matches.iloc[0])
