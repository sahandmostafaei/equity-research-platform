from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.config import (
    get_float_config,
    get_int_config,
    get_config_value,
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
from src.peer_valuation import (
    build_peer_valuation_summary,
    calculate_peer_median_multiples,
    calculate_multiples,
    compare_target_to_peers,
)
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

    bear_revenue_growth: float = 0.03
    base_revenue_growth: float = 0.07
    bull_revenue_growth: float = 0.12

    bear_ebitda_margin: float = 0.18
    base_ebitda_margin: float = 0.22
    bull_ebitda_margin: float = 0.26

    bear_wacc: float = 0.11
    base_wacc: float = 0.09
    bull_wacc: float = 0.08

    bear_terminal_growth: float = 0.02
    base_terminal_growth: float = 0.025
    bull_terminal_growth: float = 0.03


@dataclass
class ResearchEngineResult:
    target_ticker: str
    historical_financials: pd.DataFrame
    market_data: pd.Series
    market_metrics: pd.Series
    scenario_valuations: pd.DataFrame

    peer_financials: dict[str, pd.DataFrame]
    peer_market_data: pd.DataFrame
    peer_market_metrics: pd.DataFrame
    peer_multiples: pd.DataFrame
    peer_median_multiples: pd.Series
    peer_comparison: pd.DataFrame
    peer_valuation: pd.DataFrame

    valuation_summary: pd.DataFrame
    investment_summary: dict[str, object]

    estimated_wacc: float


class ResearchEngine:
    """
    Integrated equity-research workflow.

    Architecture:

        Configuration
            ↓
        Financial Statements
            ↓
        Fundamental Analysis
            ↓
        Market Analysis
            ↓
        Peer Analysis
            ↓
        Forecasting
            ↓
        DCF Valuation
            ↓
        Comparable Valuation
            ↓
        Scenario Analysis
            ↓
        Investment Assessment
    """

    def __init__(
        self,
        config: ResearchEngineConfig,
    ) -> None:
        self.config = config

    def load_company_financials(
        self,
        ticker: str,
    ) -> pd.DataFrame:
        statements = download_financials(
            ticker
        )

        historical = build_historical_financials(
            income_statement=statements[
                "income_statement"
            ],
            balance_sheet=statements[
                "balance_sheet"
            ],
            cash_flow=statements[
                "cash_flow"
            ],
            tax_rate=self.config.tax_rate,
        )

        return add_historical_ratios(
            historical
        )

    def load_target_financials(
        self,
    ) -> pd.DataFrame:
        return self.load_company_financials(
            self.config.target_ticker
        )

    def load_market_data_for_ticker(
        self,
        ticker: str,
    ) -> pd.Series:
        return get_basic_market_data(
            ticker
        )

    def load_market_data(
        self,
    ) -> pd.Series:
        return self.load_market_data_for_ticker(
            self.config.target_ticker
        )

    def _latest_complete_financial_row(
        self,
        historical_financials: pd.DataFrame,
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
                "No complete historical financial "
                "observation is available."
            )

        return available.iloc[-1]

    def calculate_market_metrics(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.Series:
        latest = (
            self._latest_complete_financial_row(
                historical_financials
            )
        )

        market_cap = float(
            market_data["market_cap"]
        )

        shares_outstanding = float(
            market_data[
                "shares_outstanding"
            ]
        )

        return build_market_metrics(
            market_cap=market_cap,
            total_debt=float(
                latest["total_debt"]
            ),
            cash=float(
                latest["cash"]
            ),
            revenue=float(
                latest["revenue"]
            ),
            ebitda=float(
                latest["ebitda"]
            ),
            net_income=float(
                latest["net_income"]
            ),
            free_cash_flow=float(
                latest["free_cash_flow"]
            ),
            shares_outstanding=(
                shares_outstanding
            ),
        )

    def estimate_cost_of_capital(
        self,
        market_data: pd.Series,
    ) -> float:
        market_cap = float(
            market_data["market_cap"]
        )

        beta = float(
            market_data.get(
                "beta",
                1.0,
            )
            or 1.0
        )

        debt = float(
            market_data.get(
                "total_debt",
                0.0,
            )
            or 0.0
        )

        cost_of_equity = (
            self.config.risk_free_rate
            + beta
            * self.config.equity_risk_premium
        )

        after_tax_cost_of_debt = (
            self.config.pre_tax_cost_of_debt
            * (1 - self.config.tax_rate)
        )

        total_capital = (
            market_cap + debt
        )

        if total_capital <= 0:
            raise ValueError(
                "Total capital must be positive."
            )

        equity_weight = (
            market_cap
            / total_capital
        )

        debt_weight = (
            debt
            / total_capital
        )

        return float(
            equity_weight
            * cost_of_equity
            + debt_weight
            * after_tax_cost_of_debt
        )

    def build_scenarios(
        self,
    ) -> dict[str, Scenario]:
        return {
            "bear": Scenario(
                name="Bear",
                revenue_growth=(
                    self.config
                    .bear_revenue_growth
                ),
                ebitda_margin=(
                    self.config
                    .bear_ebitda_margin
                ),
                wacc=self.config.bear_wacc,
                terminal_growth=(
                    self.config
                    .bear_terminal_growth
                ),
            ),
            "base": Scenario(
                name="Base",
                revenue_growth=(
                    self.config
                    .base_revenue_growth
                ),
                ebitda_margin=(
                    self.config
                    .base_ebitda_margin
                ),
                wacc=self.config.base_wacc,
                terminal_growth=(
                    self.config
                    .base_terminal_growth
                ),
            ),
            "bull": Scenario(
                name="Bull",
                revenue_growth=(
                    self.config
                    .bull_revenue_growth
                ),
                ebitda_margin=(
                    self.config
                    .bull_ebitda_margin
                ),
                wacc=self.config.bull_wacc,
                terminal_growth=(
                    self.config
                    .bull_terminal_growth
                ),
            ),
        }

    def run_scenarios(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.DataFrame:
        historical_revenue = (
            historical_financials[
                "revenue"
            ]
            .dropna()
        )

        if historical_revenue.empty:
            raise ValueError(
                "Historical revenue cannot be empty."
            )

        latest = (
            self._latest_complete_financial_row(
                historical_financials
            )
        )

        return run_all_scenarios(
            historical_revenue=(
                historical_revenue
            ),
            scenarios=self.build_scenarios(),
            total_debt=float(
                latest["total_debt"]
            ),
            cash=float(
                latest["cash"]
            ),
            shares_outstanding=float(
                market_data[
                    "shares_outstanding"
                ]
            ),
            fcf_conversion=(
                self.config.fcf_conversion
            ),
            years=self.config.forecast_years,
        )

    def load_peer_financials(
        self,
    ) -> dict[str, pd.DataFrame]:
        results = {}

        for ticker in self.config.peer_tickers:
            results[ticker] = (
                self.load_company_financials(
                    ticker
                )
            )

        return results

    def load_peer_market_data(
        self,
    ) -> pd.DataFrame:
        rows = []

        for ticker in self.config.peer_tickers:
            market_data = (
                self.load_market_data_for_ticker(
                    ticker
                )
            )

            row = market_data.copy()
            row.name = ticker
            rows.append(row)

        if not rows:
            raise ValueError(
                "At least one peer is required."
            )

        return pd.DataFrame(
            rows
        )

    def build_company_market_metrics(
        self,
        ticker: str,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
    ) -> pd.Series:
        return self.calculate_market_metrics(
            historical_financials=(
                historical_financials
            ),
            market_data=market_data,
        )

    def build_peer_market_metrics(
        self,
        peer_financials: dict[str, pd.DataFrame],
        peer_market_data: pd.DataFrame,
    ) -> pd.DataFrame:
        rows = []

        for ticker, financials in (
            peer_financials.items()
        ):
            if ticker not in peer_market_data.index:
                continue

            market_data = (
                peer_market_data.loc[ticker]
            )

            metrics = (
                self.build_company_market_metrics(
                    ticker=ticker,
                    historical_financials=(
                        financials
                    ),
                    market_data=market_data,
                )
            )

            metrics.name = ticker
            rows.append(metrics)

        if not rows:
            raise ValueError(
                "No peer market metrics could "
                "be calculated."
            )

        return pd.DataFrame(
            rows
        )

    def build_peer_multiples(
        self,
        peer_financials: dict[str, pd.DataFrame],
        peer_market_data: pd.DataFrame,
    ) -> pd.DataFrame:
        rows = []

        for ticker, financials in (
            peer_financials.items()
        ):
            if ticker not in peer_market_data.index:
                continue

            latest = (
                self._latest_complete_financial_row(
                    financials
                )
            )

            market_data = (
                peer_market_data.loc[ticker]
            )

            metrics = (
                self.build_company_market_metrics(
                    ticker=ticker,
                    historical_financials=(
                        financials
                    ),
                    market_data=market_data,
                )
            )

            market_cap = float(
                metrics["market_cap"]
            )

            enterprise_value = (
                float(metrics["enterprise_value"])
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

            multiples = calculate_multiples(
                market_cap=pd.Series(
                    {ticker: market_cap}
                ),
                enterprise_value=pd.Series(
                    {
                        ticker:
                        enterprise_value
                    }
                ),
                revenue=pd.Series(
                    {ticker: revenue}
                ),
                ebitda=pd.Series(
                    {ticker: ebitda}
                ),
                earnings=pd.Series(
                    {ticker: net_income}
                ),
                free_cash_flow=pd.Series(
                    {
                        ticker:
                        free_cash_flow
                    }
                ),
            )

            rows.append(
                multiples.loc[ticker]
            )

        if not rows:
            raise ValueError(
                "Peer multiples could not "
                "be calculated."
            )

        return pd.DataFrame(
            rows,
            index=[
                row.name
                for row in rows
            ],
        )

    def build_target_peer_comparison(
        self,
        target_metrics: pd.Series,
        peer_medians: pd.Series,
        target_financials: pd.DataFrame,
        target_market_data: pd.Series,
    ) -> pd.DataFrame:
        latest = (
            self._latest_complete_financial_row(
                target_financials
            )
        )

        market_cap = float(
            target_metrics["market_cap"]
        )

        enterprise_value = float(
            target_metrics[
                "enterprise_value"
            ]
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

        target_multiples = calculate_multiples(
            market_cap=pd.Series(
                {
                    self.config.target_ticker:
                    market_cap
                }
            ),
            enterprise_value=pd.Series(
                {
                    self.config.target_ticker:
                    enterprise_value
                }
            ),
            revenue=pd.Series(
                {
                    self.config.target_ticker:
                    revenue
                }
            ),
            ebitda=pd.Series(
                {
                    self.config.target_ticker:
                    ebitda
                }
            ),
            earnings=pd.Series(
                {
                    self.config.target_ticker:
                    net_income
                }
            ),
            free_cash_flow=pd.Series(
                {
                    self.config.target_ticker:
                    free_cash_flow
                }
            ),
        ).iloc[0]

        return compare_target_to_peers(
            target_multiples=target_multiples,
            peer_medians=peer_medians,
        )

    def build_peer_valuation(
        self,
        target_financials: pd.DataFrame,
        target_market_data: pd.Series,
        peer_medians: pd.Series,
    ) -> pd.DataFrame:
        latest = (
            self._latest_complete_financial_row(
                target_financials
            )
        )

        shares_outstanding = float(
            target_market_data[
                "shares_outstanding"
            ]
        )

        target_metrics = pd.Series(
            {
                "eps": (
                    float(
                        latest["net_income"]
                    )
                    / shares_outstanding
                ),
                "revenue_per_share": (
                    float(
                        latest["revenue"]
                    )
                    / shares_outstanding
                ),
                "revenue": float(
                    latest["revenue"]
                ),
                "ebitda": float(
                    latest["ebitda"]
                ),
                "free_cash_flow": float(
                    latest["free_cash_flow"]
                ),
            }
        )

        return build_peer_valuation_summary(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            total_debt=float(
                latest["total_debt"]
            ),
            cash=float(
                latest["cash"]
            ),
            shares_outstanding=(
                shares_outstanding
            ),
        )

    def build_valuation_summary(
        self,
        scenario_valuations: pd.DataFrame,
        peer_valuation: pd.DataFrame,
    ) -> pd.DataFrame:
        rows = []

        for _, row in (
            scenario_valuations.iterrows()
        ):
            rows.append(
                {
                    "method": (
                        f"DCF - "
                        f"{row['scenario']}"
                    ),
                    "valuation_type": (
                        "DCF"
                    ),
                    "implied_per_share": (
                        float(
                            row[
                                "per_share_value"
                            ]
                        )
                    ),
                }
            )

        if not peer_valuation.empty:
            rows.extend(
                peer_valuation[
                    [
                        "method",
                        "valuation_type",
                        "implied_per_share",
                    ]
                ].to_dict(
                    orient="records"
                )
            )

        return pd.DataFrame(
            rows
        )

    def build_investment_assessment(
        self,
        historical_financials: pd.DataFrame,
        market_data: pd.Series,
        valuation_summary: pd.DataFrame,
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
            valuation_summary[
                "implied_per_share"
            ]
            .dropna()
        )

        if valuation_values.empty:
            raise ValueError(
                "No valuation observations "
                "are available."
            )

        consensus_value = float(
            valuation_values.median()
        )

        valuation_upside = (
            consensus_value
            / market_price
            - 1
        )

        investment_score = (
            calculate_investment_score(
                valuation_upside=(
                    valuation_upside
                ),
                roic=float(
                    latest["roic"]
                ),
                revenue_growth=float(
                    latest[
                        "revenue_growth"
                    ]
                ),
                fcf_margin=float(
                    latest[
                        "fcf_margin"
                    ]
                ),
                net_debt_to_ebitda=float(
                    latest[
                        "net_debt_to_ebitda"
                    ]
                ),
            )
        )

        summary = build_investment_summary(
            fundamental_score=(
                investment_score
            ),
            valuation_upside=(
                valuation_upside
            ),
        )

        summary["consensus_value"] = (
            consensus_value
        )

        summary["market_price"] = (
            market_price
        )

        summary["valuation_upside"] = (
            valuation_upside
        )

        summary["score_classification"] = (
            classify_score(
                investment_score
            )
        )

        return summary

    def run(self) -> ResearchEngineResult:
        target_financials = (
            self.load_target_financials()
        )

        target_market_data = (
            self.load_market_data()
        )

        target_market_metrics = (
            self.calculate_market_metrics(
                historical_financials=(
                    target_financials
                ),
                market_data=(
                    target_market_data
                ),
            )
        )

        estimated_wacc = (
            self.estimate_cost_of_capital(
                target_market_data
            )
        )

        scenario_valuations = (
            self.run_scenarios(
                historical_financials=(
                    target_financials
                ),
                market_data=(
                    target_market_data
                ),
            )
        )

        peer_financials = (
            self.load_peer_financials()
        )

        peer_market_data = (
            self.load_peer_market_data()
        )

        peer_market_metrics = (
            self.build_peer_market_metrics(
                peer_financials=(
                    peer_financials
                ),
                peer_market_data=(
                    peer_market_data
                ),
            )
        )

        peer_multiples = (
            self.build_peer_multiples(
                peer_financials=(
                    peer_financials
                ),
                peer_market_data=(
                    peer_market_data
                ),
            )
        )

        peer_median_multiples = (
            calculate_peer_median_multiples(
                peer_multiples
            )
        )

        peer_comparison = (
            self.build_target_peer_comparison(
                target_metrics=(
                    target_market_metrics
                ),
                peer_medians=(
                    peer_median_multiples
                ),
                target_financials=(
                    target_financials
                ),
                target_market_data=(
                    target_market_data
                ),
            )
        )

        peer_valuation = (
            self.build_peer_valuation(
                target_financials=(
                    target_financials
                ),
                target_market_data=(
                    target_market_data
                ),
                peer_medians=(
                    peer_median_multiples
                ),
            )
        )

        valuation_summary = (
            self.build_valuation_summary(
                scenario_valuations=(
                    scenario_valuations
                ),
                peer_valuation=(
                    peer_valuation
                ),
            )
        )

        investment_summary = (
            self.build_investment_assessment(
                historical_financials=(
                    target_financials
                ),
                market_data=(
                    target_market_data
                ),
                valuation_summary=(
                    valuation_summary
                ),
            )
        )

        return ResearchEngineResult(
            target_ticker=(
                self.config.target_ticker
            ),
            historical_financials=(
                target_financials
            ),
            market_data=(
                target_market_data
            ),
            market_metrics=(
                target_market_metrics
            ),
            scenario_valuations=(
                scenario_valuations
            ),
            peer_financials=(
                peer_financials
            ),
            peer_market_data=(
                peer_market_data
            ),
            peer_market_metrics=(
                peer_market_metrics
            ),
            peer_multiples=(
                peer_multiples
            ),
            peer_median_multiples=(
                peer_median_multiples
            ),
            peer_comparison=(
                peer_comparison
            ),
            peer_valuation=(
                peer_valuation
            ),
            valuation_summary=(
                valuation_summary
            ),
            investment_summary=(
                investment_summary
            ),
            estimated_wacc=(
                estimated_wacc
            ),
        )


def create_default_research_engine() -> ResearchEngine:
    """
    Create a configured research engine from
    data/research_config.csv.
    """

    try:
        config_table = (
            load_research_config()
        )

        target_ticker = (
            get_config_value(
                config_table,
                "target_ticker",
            )
        )

        peer_tickers = [
            get_config_value(
                config_table,
                f"peer_{index}",
            )
            for index in range(1, 5)
        ]

        config = ResearchEngineConfig(
            target_ticker=target_ticker,
            peer_tickers=peer_tickers,
            tax_rate=get_float_config(
                config_table,
                "tax_rate",
            ),
            risk_free_rate=get_float_config(
                config_table,
                "risk_free_rate",
            ),
            equity_risk_premium=(
                get_float_config(
                    config_table,
                    "equity_risk_premium",
                )
            ),
            pre_tax_cost_of_debt=(
                get_float_config(
                    config_table,
                    "pre_tax_cost_of_debt",
                )
            ),
            forecast_years=get_int_config(
                config_table,
                "forecast_years",
            ),
            fcf_conversion=get_float_config(
                config_table,
                "fcf_conversion",
            ),
            bear_revenue_growth=(
                get_float_config(
                    config_table,
                    "bear_revenue_growth",
                )
            ),
            base_revenue_growth=(
                get_float_config(
                    config_table,
                    "base_revenue_growth",
                )
            ),
            bull_revenue_growth=(
                get_float_config(
                    config_table,
                    "bull_revenue_growth",
                )
            ),
            bear_ebitda_margin=(
                get_float_config(
                    config_table,
                    "bear_ebitda_margin",
                )
            ),
            base_ebitda_margin=(
                get_float_config(
                    config_table,
                    "base_ebitda_margin",
                )
            ),
            bull_ebitda_margin=(
                get_float_config(
                    config_table,
                    "bull_ebitda_margin",
                )
            ),
            bear_wacc=get_float_config(
                config_table,
                "bear_wacc",
            ),
            base_wacc=get_float_config(
                config_table,
                "base_wacc",
            ),
            bull_wacc=get_float_config(
                config_table,
                "bull_wacc",
            ),
            bear_terminal_growth=(
                get_float_config(
                    config_table,
                    "bear_terminal_growth",
                )
            ),
            base_terminal_growth=(
                get_float_config(
                    config_table,
                    "base_terminal_growth",
                )
            ),
            bull_terminal_growth=(
                get_float_config(
                    config_table,
                    "bull_terminal_growth",
                )
            ),
        )

        return ResearchEngine(config)

    except (
        FileNotFoundError,
        KeyError,
        ValueError,
    ):
        return ResearchEngine(
            ResearchEngineConfig(
                target_ticker="MSFT",
                peer_tickers=[
                    "GOOGL",
                    "META",
                    "AAPL",
                    "AMZN",
                ],
            )
        )
