from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.capital_cost import calculate_cost_of_equity, calculate_wacc
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
from src.peer_valuation import calculate_peer_median_multiples
from src.research_metrics import build_market_metrics
from src.scenarios import create_default_scenarios
from src.scenario_valuation import run_all_scenarios
from src.valuation_summary import calculate_consensus_value


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
    High-level orchestration layer for equity research.

    The engine connects:
        Financial Data
        -> Fundamental Analysis
        -> Market Analysis
        -> Forecasting
        -> Valuation
        -> Scenario Analysis
        -> Investment Assessment
    """

    def __init__(
        self,
        config: ResearchEngineConfig,
    ) -> None:
        self.config = config

    def load_target_financials(
        self,
    ) -> pd.DataFrame:
        """
        Retrieve and standardize target-company financial statements.
        """
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
        """
        Retrieve current market information for the target.
        """
        return get_basic_market_data(
            self.config.target_ticker
        )

    def calculate_market_metrics(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.Series:
        """
        Calculate valuation and market metrics from
        the latest available financial information.
        """
        latest = historical_financials.dropna(
            subset=["revenue", "ebitda", "net_income"]
        ).iloc[-1]

        market_cap = float(
            market_data["market_cap"]
        )

        total_debt = float(
            latest["total_debt"]
        )

        cash = float(
            latest["cash"]
        )

        revenue = float(
            latest["revenue"]
        )

        ebitda = float(
            latest["ebitda"]
        )

        net_income = float(
            latest["net_income"]
        )

        free_cash_flow = float(
            latest["free_cash_flow"]
        )

        shares_outstanding = float(
            market_data["shares_outstanding"]
        )

        return build_market_metrics(
            market_cap=market_cap,
            total_debt=total_debt,
            cash=cash,
            revenue=revenue,
            ebitda=ebitda,
            net_income=net_income,
            free_cash_flow=free_cash_flow,
            shares_outstanding=shares_outstanding,
        )

    def estimate_cost_of_capital(
        self,
        market_data: pd.Series,
    ) -> float:
        """
        Estimate WACC using CAPM and market capital structure.
        """
        market_cap = float(
            market_data["market_cap"]
        )

        beta = float(
            market_data.get("beta", 1.0)
        )

        cost_of_equity = calculate_cost_of_equity(
            risk_free_rate=self.config.risk_free_rate,
            beta=beta,
            equity_risk_premium=self.config.equity_risk_premium,
        )

        debt = float(
            market_data.get("totalDebt", 0.0)
            or 0.0
        )

        after_tax_cost_of_debt = (
            self.config.pre_tax_cost_of_debt
            * (1 - self.config.tax_rate)
        )

        return calculate_wacc(
            market_value_equity=market_cap,
            market_value_debt=debt,
            cost_of_equity=cost_of_equity,
            after_tax_cost_of_debt=after_tax_cost_of_debt,
        )

    def run_scenarios(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.DataFrame:
        """
        Run Bear/Base/Bull valuation scenarios.
        """
        scenarios = create_default_scenarios()

        historical_revenue = (
            historical_financials["revenue"]
            .dropna()
        )

        latest = historical_financials.dropna(
            subset=["total_debt", "cash"]
        ).iloc[-1]

        total_debt = float(
            latest["total_debt"]
        )

        cash = float(
            latest["cash"]
        )

        shares_outstanding = float(
            market_data["shares_outstanding"]
        )

        return run_all_scenarios(
            historical_revenue=historical_revenue,
            scenarios=scenarios,
            total_debt=total_debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
            fcf_conversion=self.config.fcf_conversion,
            years=self.config.forecast_years,
        )

    def build_investment_assessment(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
        scenario_valuations: pd.DataFrame,
    ) -> dict[str, object]:
        """
        Build a research-level investment assessment.
        """
        latest = historical_financials.dropna(
            subset=[
                "roic",
                "revenue_growth",
                "fcf_margin",
                "net_debt_to_ebitda",
            ]
        ).iloc[-1]

        market_price = float(
            market_data["current_price"]
        )

        valuation_values = (
            scenario_valuations["per_share_value"]
        )

        consensus_value = calculate_consensus_value(
            valuation_values
        )

        valuation_upside = (
            consensus_value / market_price
        ) - 1

        investment_score = calculate_investment_score(
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

        classification = classify_score(
            investment_score
        )

        summary = build_investment_summary(
            fundamental_score=investment_score,
            valuation_upside=valuation_upside,
        )

        summary["consensus_value"] = consensus_value
        summary["market_price"] = market_price
        summary["score_classification"] = classification

        return summary

    def run(self) -> ResearchEngineResult:
        """
        Execute the complete equity research workflow.
        """
        historical_financials = (
            self.load_target_financials()
        )

        market_data = self.load_market_data()

        market_metrics = self.calculate_market_metrics(
            historical_financials=historical_financials,
            market_data=market_data,
        )

        scenario_valuations = self.run_scenarios(
            historical_financials=historical_financials,
            market_data=market_data,
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
    Create the default research engine for the initial universe.
    """
    config = ResearchEngineConfig(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
            "AAPL",
            "AMZN",
        ],
    )

    return ResearchEngine(config)
