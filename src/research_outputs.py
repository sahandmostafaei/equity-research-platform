from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.research_engine import (
    ResearchEngineResult,
)


DEFAULT_OUTPUT_DIR = Path(
    "data/processed"
)


def _ensure_output_dir(
    output_dir: str | Path,
) -> Path:
    path = Path(output_dir)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    output_path = (
        _ensure_output_dir(
            output_dir
        )
        / filename
    )

    dataframe.to_csv(
        output_path
    )

    return output_path


def save_series(
    series: pd.Series,
    filename: str,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    output_path = (
        _ensure_output_dir(
            output_dir
        )
        / filename
    )

    series.to_csv(
        output_path,
        header=["value"],
    )

    return output_path


def save_investment_summary(
    summary: dict[str, object],
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    dataframe = pd.DataFrame(
        {
            "metric": list(
                summary.keys()
            ),
            "value": list(
                summary.values()
            ),
        }
    )

    return save_dataframe(
        dataframe,
        "investment_summary.csv",
        output_dir,
    )


def build_research_snapshot(
    result: ResearchEngineResult,
) -> pd.DataFrame:
    summary = result.investment_summary

    values = {
        "target_ticker": (
            result.target_ticker
        ),
        "market_price": (
            summary.get(
                "market_price"
            )
        ),
        "consensus_value": (
            summary.get(
                "consensus_value"
            )
        ),
        "valuation_upside": (
            summary.get(
                "valuation_upside"
            )
        ),
        "investment_score": (
            summary.get(
                "score"
            )
        ),
        "score_classification": (
            summary.get(
                "score_classification"
            )
        ),
        "estimated_wacc": (
            result.estimated_wacc
        ),
        "peer_count": (
            len(
                result.peer_financials
            )
        ),
        "valuation_method_count": (
            len(
                result.valuation_summary
            )
        ),
    }

    return pd.DataFrame(
        [
            values
        ]
    )


def save_research_outputs(
    result: ResearchEngineResult,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Path]:
    """
    Save the complete research-engine output package.
    """

    output_dir = _ensure_output_dir(
        output_dir
    )

    paths: dict[str, Path] = {}

    paths["target_financials"] = (
        save_dataframe(
            result.historical_financials,
            "target_financials.csv",
            output_dir,
        )
    )

    paths["market_snapshot"] = (
        save_series(
            result.market_data,
            "market_snapshot.csv",
            output_dir,
        )
    )

    paths["market_metrics"] = (
        save_series(
            result.market_metrics,
            "market_metrics.csv",
            output_dir,
        )
    )

    paths["scenario_valuations"] = (
        save_dataframe(
            result.scenario_valuations,
            "scenario_valuations.csv",
            output_dir,
        )
    )

    paths["peer_market_data"] = (
        save_dataframe(
            result.peer_market_data,
            "peer_market_data.csv",
            output_dir,
        )
    )

    paths["peer_market_metrics"] = (
        save_dataframe(
            result.peer_market_metrics,
            "peer_market_metrics.csv",
            output_dir,
        )
    )

    paths["peer_multiples"] = (
        save_dataframe(
            result.peer_multiples,
            "peer_multiples.csv",
            output_dir,
        )
    )

    paths["peer_median_multiples"] = (
        save_series(
            result.peer_median_multiples,
            "peer_median_multiples.csv",
            output_dir,
        )
    )

    paths["peer_comparison"] = (
        save_dataframe(
            result.peer_comparison,
            "peer_comparison.csv",
            output_dir,
        )
    )

    paths["peer_valuation"] = (
        save_dataframe(
            result.peer_valuation,
            "peer_valuation.csv",
            output_dir,
        )
    )

    paths["valuation_summary"] = (
        save_dataframe(
            result.valuation_summary,
            "valuation_summary.csv",
            output_dir,
        )
    )

    paths["investment_summary"] = (
        save_investment_summary(
            result.investment_summary,
            output_dir,
        )
    )

    paths["research_snapshot"] = (
        save_dataframe(
            build_research_snapshot(
                result
            ),
            "research_snapshot.csv",
            output_dir,
        )
    )

    return paths
