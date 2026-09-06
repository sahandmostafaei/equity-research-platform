from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_research_table(
    dataframe: pd.DataFrame,
    output_path: str | Path,
) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=True,
    )


def build_company_snapshot(
    company: str,
    ticker: str,
    sector: str,
    metrics: pd.Series,
) -> pd.Series:
    snapshot = pd.Series(
        {
            "company": company,
            "ticker": ticker,
            "sector": sector,
        }
    )

    return pd.concat(
        [snapshot, metrics]
    )


def build_peer_comparison_table(
    target_name: str,
    target_metrics: pd.Series,
    peer_metrics: pd.DataFrame,
) -> pd.DataFrame:
    target = pd.DataFrame(
        [target_metrics],
        index=[target_name],
    )

    return pd.concat(
        [target, peer_metrics],
        axis=0,
    )
