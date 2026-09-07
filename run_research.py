from __future__ import annotations

from pathlib import Path

from src.investment_thesis import build_thesis
from src.research_engine import create_default_research_engine
from src.research_outputs import save_research_outputs
from src.research_quality import (
    quality_checks_pass,
    run_research_quality_checks,
)
from src.reporting import (
    plot_peer_multiples,
    plot_revenue_and_ebitda,
    plot_scenario_valuation,
    save_investment_thesis,
    save_research_report,
)


OUTPUT_DIR = Path("data/processed")
FIGURES_DIR = Path("figures")


def build_catalysts(result) -> list[str]:
    """
    Build a concise list of potential investment catalysts.
    """
    catalysts: list[str] = []

    valuation_upside = result.investment_summary.get(
        "valuation_upside"
    )

    if (
        valuation_upside is not None
        and valuation_upside > 0
    ):
        catalysts.append(
            "Potential valuation upside relative to "
            "the current market price."
        )

    if not result.peer_comparison.empty:
        catalysts.append(
            "Relative valuation can be assessed against "
            "a selected technology peer group."
        )

    if not result.scenario_valuations.empty:
        catalysts.append(
            "Bull-case operating assumptions provide "
            "additional valuation upside if execution improves."
        )

    catalysts.append(
        "Continued revenue growth and operating-margin "
        "expansion could support intrinsic value."
    )

    return catalysts


def build_risks(result) -> list[str]:
    """
    Build a concise list of principal investment risks.
    """
    risks: list[str] = []

    risks.append(
        "Valuation is sensitive to WACC and terminal-growth "
        "assumptions."
    )

    risks.append(
        "Forecast valuation depends on assumptions about "
        "revenue growth, margins, and free-cash-flow conversion."
    )

    risks.append(
        "Peer multiples can change materially with market "
        "conditions and investor risk appetite."
    )

    estimated_wacc = result.estimated_wacc

    if estimated_wacc is not None:
        risks.append(
            f"The estimated WACC of {estimated_wacc:.2%} "
            "introduces sensitivity to the cost of capital."
        )

    risks.append(
        "Market, competitive, regulatory, technological, "
        "and execution risks may cause realized results "
        "to differ from the research assumptions."
    )

    return risks


def main() -> None:
    """
    Execute the complete equity research workflow.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 72)
    print("EQUITY RESEARCH & FUNDAMENTAL VALUATION PLATFORM")
    print("=" * 72)

    # ------------------------------------------------------------------
    # 1. Create the research engine
    # ------------------------------------------------------------------

    print("\n[1/9] Initializing research engine...")

    engine = create_default_research_engine()

    print(
        f"Target: {engine.config.target_ticker}"
    )

    print(
        "Peers: "
        + ", ".join(engine.config.peer_tickers)
    )

    # ------------------------------------------------------------------
    # 2. Run the complete research pipeline
    # ------------------------------------------------------------------

    print("\n[2/9] Running fundamental and valuation analysis...")

    result = engine.run()

    print(
        f"Research completed for "
        f"{result.target_ticker}."
    )

    # ------------------------------------------------------------------
    # 3. Save core research outputs
    # ------------------------------------------------------------------

    print("\n[3/9] Saving research outputs...")

    output_paths = save_research_outputs(
        result,
        OUTPUT_DIR,
    )

    for name, path in output_paths.items():
        print(
            f"  Saved {name}: {path}"
        )

    # ------------------------------------------------------------------
    # 4. Build investment thesis
    # ------------------------------------------------------------------

    print("\n[4/9] Building investment thesis...")

    catalysts = build_catalysts(
        result
    )

    risks = build_risks(
        result
    )

    thesis = build_thesis(
        result=result,
        catalysts=catalysts,
        risks=risks,
    )

    thesis_path = save_investment_thesis(
        thesis,
        OUTPUT_DIR,
    )

    print(
        f"  Saved investment thesis: "
        f"{thesis_path}"
    )

    # ------------------------------------------------------------------
    # 5. Build research report
    # ------------------------------------------------------------------

    print("\n[5/9] Building research report...")

    report_path = save_research_report(
        result=result,
        output_dir=OUTPUT_DIR,
        catalysts=catalysts,
        risks=risks,
    )

    print(
        f"  Saved research report: "
        f"{report_path}"
    )

    # ------------------------------------------------------------------
    # 6. Generate analytical figures
    # ------------------------------------------------------------------

    print("\n[6/9] Generating analytical figures...")

    if not result.historical_financials.empty:
        revenue_ebitda_path = (
            FIGURES_DIR
            / "historical_revenue_ebitda.png"
        )

        plot_revenue_and_ebitda(
            result.historical_financials,
            revenue_ebitda_path,
        )

        print(
            f"  Saved: {revenue_ebitda_path}"
        )

    if not result.peer_multiples.empty:
        peer_multiples_path = (
            FIGURES_DIR
            / "peer_valuation_multiples.png"
        )

        plot_peer_multiples(
            result.peer_multiples,
            peer_multiples_path,
        )

        print(
            f"  Saved: {peer_multiples_path}"
        )

    if not result.scenario_valuations.empty:
        scenario_path = (
            FIGURES_DIR
            / "scenario_valuation.png"
        )

        plot_scenario_valuation(
            result.scenario_valuations,
            scenario_path,
        )

        print(
            f"  Saved: {scenario_path}"
        )

    # ------------------------------------------------------------------
    # 7. Run research-quality validation
    # ------------------------------------------------------------------

    print("\n[7/9] Running research-quality checks...")

    quality_checks = (
        run_research_quality_checks(
            result
        )
    )

    quality_path = (
        OUTPUT_DIR
        / "research_quality_checks.csv"
    )

    quality_checks.to_csv(
        quality_path,
        index=False,
    )

    print(
        f"  Saved quality checks: "
        f"{quality_path}"
    )

    quality_passed = quality_checks_pass(
        quality_checks
    )

    if not quality_passed:
        print(
            "\nResearch-quality validation failed."
        )

        failed_checks = quality_checks[
            quality_checks["passed"] == False
        ]

        for _, row in failed_checks.iterrows():
            print(
                f"  FAILED: "
                f"{row.get('check', 'Unknown check')}"
            )

        raise ValueError(
            "Research-quality checks failed. "
            "Review data/processed/"
            "research_quality_checks.csv."
        )

    print(
        "  All research-quality checks passed."
    )

    # ------------------------------------------------------------------
    # 8. Print investment conclusion
    # ------------------------------------------------------------------

    print("\n[8/9] Investment conclusion...")

    investment_summary = (
        result.investment_summary
    )

    market_price = investment_summary.get(
        "market_price"
    )

    consensus_value = investment_summary.get(
        "consensus_value"
    )

    valuation_upside = investment_summary.get(
        "valuation_upside"
    )

    fundamental_score = investment_summary.get(
        "fundamental_score"
    )

    valuation_classification = (
        investment_summary.get(
            "valuation_classification"
        )
    )

    investment_view = (
        investment_summary.get(
            "investment_view"
        )
    )

    if result.estimated_wacc is not None:
        print(
            f"  Estimated WACC: "
            f"{result.estimated_wacc:.2%}"
        )

    if market_price is not None:
        print(
            f"  Market price: "
            f"{market_price:.2f}"
        )

    if consensus_value is not None:
        print(
            f"  Median valuation reference: "
            f"{consensus_value:.2f}"
        )

    if valuation_upside is not None:
        print(
            f"  Valuation upside/downside: "
            f"{valuation_upside:.2%}"
        )

    if fundamental_score is not None:
        print(
            f"  Fundamental score: "
            f"{fundamental_score:.2%}"
        )

    if valuation_classification:
        print(
            f"  Valuation classification: "
            f"{valuation_classification}"
        )

    if investment_view:
        print(
            f"  Investment view: "
            f"{investment_view}"
        )

    # ------------------------------------------------------------------
    # 9. Completion summary
    # ------------------------------------------------------------------

    print("\n[9/9] Workflow complete.")

    print("\nGenerated outputs:")
    print(
        f"  Research outputs: "
        f"{OUTPUT_DIR}"
    )
    print(
        f"  Figures: "
        f"{FIGURES_DIR}"
    )

    print("\nKey files:")
    print(
        f"  - {OUTPUT_DIR / 'research_snapshot.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'investment_summary.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'valuation_summary.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'scenario_valuations.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'peer_multiples.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'peer_comparison.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'peer_valuation.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'investment_thesis.csv'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'research_report.md'}"
    )
    print(
        f"  - {OUTPUT_DIR / 'research_quality_checks.csv'}"
    )

    print("\n" + "=" * 72)
    print("RESEARCH WORKFLOW FINISHED SUCCESSFULLY")
    print("=" * 72)


if __name__ == "__main__":
    main()
