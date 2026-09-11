from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.analytical_summary import (
    build_research_dashboard,
)
from src.comparables import (
    calculate_multiples,
)
from src.data_loader import (
    download_financials,
    download_price_data,
    get_company_info,
)
from src.financial_data import (
    add_historical_ratios,
    build_historical_financials,
)
from src.investment_decision import (
    build_investment_summary,
)
from src.investment_thesis import (
    build_investment_assessment,
)
from src.peer_valuation import (
    build_peer_valuation_summary,
    calculate_peer_median_multiples,
    compare_target_to_peers,
)
from src.scenarios import (
    create_default_scenarios,
    project_ebitda,
    project_revenue,
)
from src.valuation import (
    calculate_dcf_value,
    calculate_equity_value,
    calculate_ev_ebitda_value,
    calculate_margin_of_safety,
    calculate_pe_value,
    calculate_per_share_value,
    calculate_upside,
)


@dataclass
class ResearchResult:
    """
    Container for the complete equity research workflow output.
    """

    target_ticker: str
    target_company: str
    target_financials: pd.DataFrame
    historical_financials: pd.DataFrame
    peer_financials: dict[str, pd.DataFrame]
    peer_multiples: pd.DataFrame
    peer_comparison: pd.DataFrame
    peer_valuation: pd.DataFrame
    valuation_summary: pd.DataFrame
    scenario_valuations: pd.DataFrame
    investment_summary: dict[str, Any]
    investment_assessment: dict[str, Any]
    estimated_wacc: float
    market_price: float
    research_dashboard: dict[str, Any]


class EquityResearchEngine:
    """
    Integrated equity research and fundamental valuation engine.

    Workflow:

    1. Load market and financial data.
    2. Standardize historical financial statements.
    3. Calculate fundamental ratios.
    4. Build peer-company analysis.
    5. Estimate valuation using DCF and trading multiples.
    6. Run bear/base/bull scenarios.
    7. Calculate valuation upside and margin of safety.
    8. Build an investment assessment.
    9. Generate research outputs.
    """

    def __init__(
        self,
        target_ticker: str,
        peer_tickers: list[str],
        start_date: str = "2018-01-01",
        end_date: str | None = None,
    ) -> None:
        if not target_ticker.strip():
            raise ValueError(
                "Target ticker cannot be empty."
            )

        if not peer_tickers:
            raise ValueError(
                "At least one peer ticker is required."
            )

        self.target_ticker = (
            target_ticker.strip().upper()
        )

        self.peer_tickers = [
            ticker.strip().upper()
            for ticker in peer_tickers
            if ticker.strip()
        ]

        self.start_date = start_date
        self.end_date = end_date

        if self.target_ticker in self.peer_tickers:
            self.peer_tickers = [
                ticker
                for ticker in self.peer_tickers
                if ticker != self.target_ticker
            ]

        if not self.peer_tickers:
            raise ValueError(
                "At least one peer ticker different from "
                "the target is required."
            )

    def load_market_data(self) -> pd.DataFrame:
        """
        Download historical market prices for the target and peers.
        """

        tickers = [
            self.target_ticker,
            *self.peer_tickers,
        ]

        return download_price_data(
            tickers=tickers,
            start=self.start_date,
            end=self.end_date,
        )

    def load_company_financials(
        self,
        ticker: str,
    ) -> pd.DataFrame:
        """
        Download and standardize annual financial statements.
        """

        statements = download_financials(
            ticker
        )

        historical = build_historical_financials(
            income_statement=(
                statements["income_statement"]
            ),
            balance_sheet=(
                statements["balance_sheet"]
            ),
            cash_flow=(
                statements["cash_flow"]
            ),
        )

        historical = add_historical_ratios(
            historical
        )

        return historical

    def load_financial_universe(
        self,
    ) -> tuple[
        pd.DataFrame,
        dict[str, pd.DataFrame],
    ]:
        """
        Load standardized financial statements
        for the target and all peers.
        """

        target_financials = (
            self.load_company_financials(
                self.target_ticker
            )
        )

        peer_financials: dict[
            str,
            pd.DataFrame,
        ] = {}

        for ticker in self.peer_tickers:
            try:
                peer_financials[ticker] = (
                    self.load_company_financials(
                        ticker
                    )
                )
            except Exception:
                continue

        if not peer_financials:
            raise ValueError(
                "No peer financial data could be loaded."
            )

        return (
            target_financials,
            peer_financials,
        )

    @staticmethod
    def _latest_value(
        financials: pd.DataFrame,
        column: str,
        default: float = 0.0,
    ) -> float:
        """
        Safely retrieve the latest available value
        from a standardized financial statement.
        """

        if column not in financials.columns:
            return default

        series = financials[column].dropna()

        if series.empty:
            return default

        return float(series.iloc[-1])

    @staticmethod
    def _calculate_wacc(
        beta: float,
        risk_free_rate: float = 0.04,
        equity_risk_premium: float = 0.055,
        cost_of_debt: float = 0.045,
        tax_rate: float = 0.21,
        market_cap: float = 1.0,
        total_debt: float = 0.0,
    ) -> float:
        """
        Estimate WACC using a simplified CAPM-based framework.

        Cost of equity:
            R_e = R_f + beta * ERP

        WACC:
            E/(D+E) * R_e
            + D/(D+E) * R_d * (1-T)
        """

        if market_cap < 0:
            raise ValueError(
                "Market capitalization cannot be negative."
            )

        if total_debt < 0:
            raise ValueError(
                "Total debt cannot be negative."
            )

        if not 0 <= tax_rate < 1:
            raise ValueError(
                "Tax rate must be between 0 and 1."
            )

        total_capital = (
            market_cap + total_debt
        )

        if total_capital <= 0:
            return risk_free_rate

        cost_of_equity = (
            risk_free_rate
            + beta * equity_risk_premium
        )

        equity_weight = (
            market_cap
            / total_capital
        )

        debt_weight = (
            total_debt
            / total_capital
        )

        return float(
            equity_weight * cost_of_equity
            + debt_weight
            * cost_of_debt
            * (1 - tax_rate)
        )

    def estimate_wacc(
        self,
        company_info: dict[str, Any],
        target_financials: pd.DataFrame,
    ) -> float:
        """
        Estimate WACC from market and accounting inputs.
        """

        beta = company_info.get(
            "beta",
            1.0,
        )

        market_cap = company_info.get(
            "marketCap",
            None,
        )

        if market_cap is None:
            market_cap = 1.0

        total_debt = self._latest_value(
            target_financials,
            "total_debt",
            default=0.0,
        )

        try:
            beta = float(beta)
        except (
            TypeError,
            ValueError,
        ):
            beta = 1.0

        try:
            market_cap = float(
                market_cap
            )
        except (
            TypeError,
            ValueError,
        ):
            market_cap = 1.0

        if beta <= 0:
            beta = 1.0

        if market_cap <= 0:
            market_cap = 1.0

        return self._calculate_wacc(
            beta=beta,
            market_cap=market_cap,
            total_debt=max(
                total_debt,
                0.0,
            ),
        )

    def build_peer_analysis(
        self,
        target_financials: pd.DataFrame,
        peer_financials: dict[str, pd.DataFrame],
        market_prices: pd.DataFrame,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
    ]:
        """
        Build peer multiples, target-vs-peer comparison,
        and peer-implied valuation.
        """

        companies: dict[
            str,
            pd.Series,
        ] = {}

        companies[
            self.target_ticker
        ] = target_financials.iloc[-1]

        for ticker, financials in peer_financials.items():
            if not financials.empty:
                companies[ticker] = (
                    financials.iloc[-1]
                )

        market_caps: dict[str, float] = {}
        enterprise_values: dict[str, float] = {}
        revenues: dict[str, float] = {}
        ebitdas: dict[str, float] = {}
        earnings: dict[str, float] = {}
        free_cash_flows: dict[str, float] = {}

        for ticker, row in companies.items():

            price = 0.0

            if ticker in market_prices.columns:
                prices = (
                    market_prices[ticker]
                    .dropna()
                )

                if not prices.empty:
                    price = float(
                        prices.iloc[-1]
                    )

            shares = float(
                row.get(
                    "shares_outstanding",
                    0.0,
                )
                or 0.0
            )

            market_cap = (
                price * shares
            )

            total_debt = float(
                row.get(
                    "total_debt",
                    0.0,
                )
                or 0.0
            )

            cash = float(
                row.get(
                    "cash",
                    0.0,
                )
                or 0.0
            )

            enterprise_value = (
                market_cap
                + total_debt
                - cash
            )

            market_caps[ticker] = (
                market_cap
            )

            enterprise_values[ticker] = (
                enterprise_value
            )

            revenues[ticker] = float(
                row.get(
                    "revenue",
                    0.0,
                )
                or 0.0
            )

            ebitdas[ticker] = float(
                row.get(
                    "ebitda",
                    0.0,
                )
                or 0.0
            )

            earnings[ticker] = float(
                row.get(
                    "net_income",
                    0.0,
                )
                or 0.0
            )

            free_cash_flows[ticker] = float(
                row.get(
                    "free_cash_flow",
                    0.0,
                )
                or 0.0
            )

        multiples = calculate_multiples(
            market_cap=pd.Series(
                market_caps
            ),
            enterprise_value=pd.Series(
                enterprise_values
            ),
            revenue=pd.Series(
                revenues
            ),
            ebitda=pd.Series(
                ebitdas
            ),
            earnings=pd.Series(
                earnings
            ),
            free_cash_flow=pd.Series(
                free_cash_flows
            ),
        )

        multiples = (
            multiples.replace(
                [
                    float("inf"),
                    float("-inf"),
                ],
                pd.NA,
            )
        )

        multiples = multiples.dropna(
            how="all"
        )

        if self.target_ticker not in multiples.index:
            raise ValueError(
                "Target company multiples could not be generated."
            )

        target_row = pd.Series(
            {
                "ticker": self.target_ticker,
                **multiples.loc[
                    self.target_ticker
                ].to_dict(),
            }
        )

        peer_rows: list[dict[str, Any]] = []

        for ticker in self.peer_tickers:

            if ticker not in multiples.index:
                continue

            peer_rows.append(
                {
                    "ticker": ticker,
                    **multiples.loc[
                        ticker
                    ].to_dict(),
                }
            )

        peer_table = pd.DataFrame(
            peer_rows
        )

        if peer_table.empty:
            raise ValueError(
                "No valid peer multiples were generated."
            )

        peer_comparison = (
            compare_target_to_peers(
                target_multiples=target_row,
                peer_multiples=peer_table,
            )
        )

        peer_medians = (
            calculate_peer_median_multiples(
                peer_table.drop(
                    columns=["ticker"],
                    errors="ignore",
                )
            )
        )

        target_latest = (
            target_financials.iloc[-1]
        )

        shares = float(
            target_latest.get(
                "shares_outstanding",
                0.0,
            )
            or 0.0
        )

        if shares <= 0:
            shares = 1.0

        net_income = float(
            target_latest.get(
                "net_income",
                0.0,
            )
            or 0.0
        )

        revenue = float(
            target_latest.get(
                "revenue",
                0.0,
            )
            or 0.0
        )

        ebitda = float(
            target_latest.get(
                "ebitda",
                0.0,
            )
            or 0.0
        )

        target_metrics = pd.Series(
            {
                "eps": (
                    net_income
                    / shares
                ),
                "revenue_per_share": (
                    revenue
                    / shares
                ),
                "revenue": revenue,
                "ebitda": ebitda,
            }
        )

        total_debt = float(
            target_latest.get(
                "total_debt",
                0.0,
            )
            or 0.0
        )

        cash = float(
            target_latest.get(
                "cash",
                0.0,
            )
            or 0.0
        )

        peer_valuation = (
            build_peer_valuation_summary(
                target_metrics=target_metrics,
                peer_medians=peer_medians,
                total_debt=total_debt,
                cash=cash,
                shares_outstanding=shares,
            )
        )

        return (
            multiples,
            peer_comparison,
            peer_valuation,
        )

    def build_dcf_valuation(
        self,
        target_financials: pd.DataFrame,
        wacc: float,
        scenario_name: str = "base",
        forecast_years: int = 5,
    ) -> dict[str, float]:
        """
        Build a simplified DCF valuation from historical FCF.
        """

        if forecast_years <= 0:
            raise ValueError(
                "Forecast years must be positive."
            )

        latest_revenue = self._latest_value(
            target_financials,
            "revenue",
        )

        latest_fcf = self._latest_value(
            target_financials,
            "free_cash_flow",
        )

        if latest_revenue <= 0:
            raise ValueError(
                "Latest revenue must be positive for DCF."
            )

        if latest_fcf <= 0:
            latest_fcf = max(
                latest_revenue * 0.05,
                1.0,
            )

        scenarios = (
            create_default_scenarios()
        )

        if scenario_name not in scenarios:
            raise ValueError(
                f"Unknown scenario: {scenario_name}"
            )

        scenario = scenarios[
            scenario_name
        ]

        projected_revenue = (
            project_revenue(
                starting_revenue=latest_revenue,
                growth_rate=scenario.revenue_growth,
                years=forecast_years,
            )
        )

        projected_ebitda = (
            project_ebitda(
                projected_revenue,
                scenario.ebitda_margin,
            )
        )

        base_fcf_margin = (
            latest_fcf
            / latest_revenue
        )

        projected_fcf = [
            revenue * base_fcf_margin
            for revenue in projected_revenue
        ]

        scenario_wacc = max(
            wacc,
            scenario.wacc,
        )

        dcf_value = calculate_dcf_value(
            free_cash_flows=projected_fcf,
            wacc=scenario_wacc,
            terminal_growth=scenario.terminal_growth,
        )

        latest_debt = self._latest_value(
            target_financials,
            "total_debt",
        )

        latest_cash = self._latest_value(
            target_financials,
            "cash",
        )

        equity_value = (
            calculate_equity_value(
                enterprise_value=dcf_value,
                total_debt=latest_debt,
                cash=latest_cash,
            )
        )

        shares = self._latest_value(
            target_financials,
            "shares_outstanding",
        )

        if shares <= 0:
            shares = 1.0

        per_share = (
            calculate_per_share_value(
                equity_value=equity_value,
                shares_outstanding=shares,
            )
        )

        return {
            "scenario": scenario.name,
            "enterprise_value": dcf_value,
            "equity_value": equity_value,
            "implied_per_share": per_share,
            "terminal_growth": (
                scenario.terminal_growth
            ),
            "wacc": scenario_wacc,
            "final_projected_revenue": (
                projected_revenue[-1]
            ),
            "final_projected_ebitda": (
                projected_ebitda[-1]
            ),
        }

    def build_valuation_summary(
        self,
        target_financials: pd.DataFrame,
        peer_valuation: pd.DataFrame,
        wacc: float,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
    ]:
        """
        Combine DCF and peer-based valuation outputs.
        """

        dcf_values: list[
            dict[str, Any]
        ] = []

        for scenario_name in (
            "bear",
            "base",
            "bull",
        ):
            try:
                dcf_result = (
                    self.build_dcf_valuation(
                        target_financials=target_financials,
                        wacc=wacc,
                        scenario_name=scenario_name,
                    )
                )

                dcf_values.append(
                    {
                        "method": (
                            f"DCF - "
                            f"{scenario_name.title()}"
                        ),
                        "implied_per_share": (
                            dcf_result[
                                "implied_per_share"
                            ]
                        ),
                    }
                )

            except ValueError:
                continue

        if target_financials.empty:
            raise ValueError(
                "Target financial data cannot be empty."
            )

        latest = (
            target_financials.iloc[-1]
        )

        shares = float(
            latest.get(
                "shares_outstanding",
                0.0,
            )
            or 0.0
        )

        if shares <= 0:
            shares = 1.0

        eps = (
            float(
                latest.get(
                    "net_income",
                    0.0,
                )
                or 0.0
            )
            / shares
        )

        net_debt = (
            float(
                latest.get(
                    "total_debt",
                    0.0,
                )
                or 0.0
            )
            - float(
                latest.get(
                    "cash",
                    0.0,
                )
                or 0.0
            )
        )

        ebitda = float(
            latest.get(
                "ebitda",
                0.0,
            )
            or 0.0
        )

        peer_rows: list[
            dict[str, Any]
        ] = []

        if not peer_valuation.empty:

            if "pe" in peer_valuation.columns:

                peer_pe = (
                    pd.to_numeric(
                        peer_valuation["pe"],
                        errors="coerce",
                    )
                    .dropna()
                )

                if not peer_pe.empty:

                    peer_pe_value = float(
                        peer_pe.iloc[0]
                    )

                    if (
                        peer_pe_value > 0
                        and eps > 0
                    ):
                        value = (
                            calculate_pe_value(
                                eps=eps,
                                peer_pe=peer_pe_value,
                            )
                        )

                        peer_rows.append(
                            {
                                "method": (
                                    "Peer P/E"
                                ),
                                "implied_per_share": (
                                    value
                                ),
                            }
                        )

            if (
                "ev_ebitda"
                in peer_valuation.columns
            ):

                peer_ev_ebitda = (
                    pd.to_numeric(
                        peer_valuation[
                            "ev_ebitda"
                        ],
                        errors="coerce",
                    )
                    .dropna()
                )

                if not peer_ev_ebitda.empty:

                    peer_ev_ebitda_value = float(
                        peer_ev_ebitda.iloc[0]
                    )

                    if (
                        peer_ev_ebitda_value > 0
                        and ebitda > 0
                    ):
                        try:
                            value = (
                                calculate_ev_ebitda_value(
                                    ebitda=ebitda,
                                    peer_ev_ebitda=(
                                        peer_ev_ebitda_value
                                    ),
                                    net_debt=net_debt,
                                    shares_outstanding=shares,
                                )
                            )

                            peer_rows.append(
                                {
                                    "method": (
                                        "Peer EV/EBITDA"
                                    ),
                                    "implied_per_share": (
                                        value
                                    ),
                                }
                            )

                        except ValueError:
                            pass

        valuation_rows = (
            dcf_values + peer_rows
        )

        valuation_summary = (
            pd.DataFrame(
                valuation_rows
            )
        )

        if valuation_summary.empty:
            raise ValueError(
                "No valid valuation outputs were generated."
            )

        scenario_valuations = (
            pd.DataFrame(
                dcf_values
            )
        )

        return (
            valuation_summary,
            scenario_valuations,
        )

    def run(
        self,
    ) -> ResearchResult:
        """
        Execute the complete equity research workflow.
        """

        market_prices = (
            self.load_market_data()
        )

        (
            target_financials,
            peer_financials,
        ) = self.load_financial_universe()

        company_info = (
            get_company_info(
                self.target_ticker
            )
        )

        wacc = self.estimate_wacc(
            company_info=company_info,
            target_financials=target_financials,
        )

        (
            peer_multiples,
            peer_comparison,
            peer_valuation,
        ) = self.build_peer_analysis(
            target_financials=target_financials,
            peer_financials=peer_financials,
            market_prices=market_prices,
        )

        (
            valuation_summary,
            scenario_valuations,
        ) = self.build_valuation_summary(
            target_financials=target_financials,
            peer_valuation=peer_valuation,
            wacc=wacc,
        )

        if self.target_ticker not in market_prices.columns:
            raise ValueError(
                "No market price column is available "
                f"for {self.target_ticker}."
            )

        target_prices = (
            market_prices[
                self.target_ticker
            ]
            .dropna()
        )

        if target_prices.empty:
            raise ValueError(
                "No market price is available "
                f"for {self.target_ticker}."
            )

        market_price = float(
            target_prices.iloc[-1]
        )

        valuation_values = (
            pd.to_numeric(
                valuation_summary[
                    "implied_per_share"
                ],
                errors="coerce",
            )
            .dropna()
        )

        if valuation_values.empty:
            raise ValueError(
                "No valid valuation reference is available."
            )

        positive_valuation_values = (
            valuation_values[
                valuation_values > 0
            ]
        )

        if positive_valuation_values.empty:
            raise ValueError(
                "No positive valuation reference is available."
            )

        median_value = float(
            positive_valuation_values.median()
        )

        valuation_upside = (
            calculate_upside(
                intrinsic_value=median_value,
                market_price=market_price,
            )
        )

        margin_of_safety = (
            calculate_margin_of_safety(
                intrinsic_value=median_value,
                market_price=market_price,
            )
        )

        latest = (
            target_financials.iloc[-1]
        )

        roic = float(
            latest.get(
                "roic",
                0.0,
            )
            or 0.0
        )

        revenue_growth = float(
            latest.get(
                "revenue_growth",
                0.0,
            )
            or 0.0
        )

        fcf = float(
            latest.get(
                "free_cash_flow",
                0.0,
            )
            or 0.0
        )

        revenue = float(
            latest.get(
                "revenue",
                0.0,
            )
            or 0.0
        )

        fcf_margin = (
            fcf / revenue
            if revenue > 0
            else 0.0
        )

        net_debt = (
            float(
                latest.get(
                    "total_debt",
                    0.0,
                )
                or 0.0
            )
            - float(
                latest.get(
                    "cash",
                    0.0,
                )
                or 0.0
            )
        )

        ebitda = float(
            latest.get(
                "ebitda",
                0.0,
            )
            or 0.0
        )

        net_debt_to_ebitda = (
            net_debt / ebitda
            if ebitda > 0
            else 0.0
        )

        investment_assessment = (
            build_investment_assessment(
                valuation_upside=valuation_upside,
                roic=roic,
                revenue_growth=revenue_growth,
                fcf_margin=fcf_margin,
                net_debt_to_ebitda=(
                    net_debt_to_ebitda
                ),
            )
        )

        fundamental_score = (
            investment_assessment[
                "fundamental_score"
            ]
        )

        investment_summary = (
            build_investment_summary(
                fundamental_score=(
                    fundamental_score
                ),
                valuation_upside=(
                    valuation_upside
                ),
            )
        )

        investment_summary[
            "market_price"
        ] = market_price

        investment_summary[
            "consensus_value"
        ] = median_value

        investment_summary[
            "median_valuation_reference"
        ] = median_value

        investment_summary[
            "margin_of_safety"
        ] = margin_of_safety

        investment_summary[
            "score_classification"
        ] = investment_assessment[
            "score_classification"
        ]

        dashboard_input = type(
            "ResearchDashboardInput",
            (),
            {
                "target_ticker": (
                    self.target_ticker
                ),
                "historical_financials": (
                    target_financials
                ),
                "valuation_summary": (
                    valuation_summary
                ),
                "scenario_valuations": (
                    scenario_valuations
                ),
                "peer_comparison": (
                    peer_comparison
                ),
                "investment_summary": (
                    investment_summary
                ),
                "estimated_wacc": wacc,
            },
        )()

        research_dashboard = (
            build_research_dashboard(
                dashboard_input
            )
        )

        return ResearchResult(
            target_ticker=self.target_ticker,
            target_company=company_info.get(
                "longName",
                self.target_ticker,
            ),
            target_financials=target_financials,
            historical_financials=target_financials,
            peer_financials=peer_financials,
            peer_multiples=peer_multiples,
            peer_comparison=peer_comparison,
            peer_valuation=peer_valuation,
            valuation_summary=valuation_summary,
            scenario_valuations=scenario_valuations,
            investment_summary=investment_summary,
            investment_assessment=(
                investment_assessment
            ),
            estimated_wacc=wacc,
            market_price=market_price,
            research_dashboard=(
                research_dashboard
            ),
        )


def run_research(
    target_ticker: str,
    peer_tickers: list[str],
    start_date: str = "2018-01-01",
    end_date: str | None = None,
) -> ResearchResult:
    """
    Convenience function for running the integrated
    equity research workflow.
    """

    engine = EquityResearchEngine(
        target_ticker=target_ticker,
        peer_tickers=peer_tickers,
        start_date=start_date,
        end_date=end_date,
    )

    return engine.run()
