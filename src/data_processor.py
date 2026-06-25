from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw OHLCV data and set date as index."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.drop_duplicates(subset="date", keep="last")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["close"])
    df = df.set_index("date")

    return df


def filter_date_range(
    df: pd.DataFrame,
    start_date: str | None,
    end_date: str | None,
) -> pd.DataFrame:
    result = df.copy()
    if start_date is not None:
        result = result[result.index >= pd.to_datetime(start_date)]
    if end_date is not None:
        result = result[result.index <= pd.to_datetime(end_date)]
    return result
