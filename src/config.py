from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_CONFIG_PATH = Path(
    "data/research_config.csv"
)


def load_research_config(
    path: str | Path = DEFAULT_CONFIG_PATH,
) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Research configuration not found: {path}"
        )

    config = pd.read_csv(path)

    required_columns = {
        "parameter",
        "value",
        "unit",
        "category",
        "description",
    }

    missing = (
        required_columns
        - set(config.columns)
    )

    if missing:
        raise ValueError(
            f"Missing configuration columns: "
            f"{sorted(missing)}"
        )

    if config["parameter"].duplicated().any():
        raise ValueError(
            "Configuration parameters must be unique."
        )

    return config


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


def get_float_config(
    config: pd.DataFrame,
    parameter: str,
) -> float:
    value = get_config_value(
        config,
        parameter,
    )

    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"Configuration value is not numeric: "
            f"{parameter}"
        ) from exc


def get_int_config(
    config: pd.DataFrame,
    parameter: str,
) -> int:
    value = get_config_value(
        config,
        parameter,
    )

    try:
        return int(float(value))
    except ValueError as exc:
        raise ValueError(
            f"Configuration value is not an integer: "
            f"{parameter}"
        ) from exc
