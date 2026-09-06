from pathlib import Path

import pandas as pd

from src.empirical_pipeline import (
    build_universe_financial_dataset,
    build_universe_market_dataset,
)
from src.config import (
    get_float_config,
    get_config_value,
    load_research_config,
)


CONFIG_PATH = Path(
    "../data/research_config.csv"
)

OUTPUT_DIR = Path(
    "../data/processed"
)


config = load_research_config(
    CONFIG_PATH
)

target = get_config_value(
    config,
    "target_ticker",
)

peers = [
    get_config_value(
        config,
        f"peer_{index}",
    )
    for index in range(1, 5)
]

tax_rate = get_float_config(
    config,
    "tax_rate",
)

universe = [
    target,
    *peers,
]


financial_datasets = (
    build_universe_financial_dataset(
        tickers=universe,
        tax_rate=tax_rate,
        output_dir=OUTPUT_DIR,
    )
)


market_datasets = (
    build_universe_market_dataset(
        tickers=universe,
        output_dir=OUTPUT_DIR,
    )
)


latest_rows = []

for ticker, financials in (
    financial_datasets.items()
):
    latest = financials.iloc[-1].copy()
    latest["ticker"] = ticker
    latest_rows.append(latest)


historical_summary = pd.DataFrame(
    latest_rows
)

historical_summary.to_csv(
    OUTPUT_DIR
    / "universe_historical_summary.csv"
)


market_summary = pd.DataFrame(
    market_datasets
).T

market_summary.to_csv(
    OUTPUT_DIR
    / "universe_market_summary.csv"
)


print("Target:", target)
print("Peers:", peers)
print(
    "Financial datasets:",
    len(financial_datasets),
)
print(
    "Market datasets:",
    len(market_datasets),
)
