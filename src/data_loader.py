from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_price_data(
    source: str,
    symbol: str,
    csv_path: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Load OHLCV price data from AkShare or a local CSV file."""
    if source == "akshare":
        return _load_from_akshare(symbol, start_date, end_date)

    if source == "csv":
        return _load_from_csv(csv_path)

    raise ValueError(f"Unsupported data source: {source}")


def _load_from_csv(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return pd.read_csv(path)


def _load_from_akshare(
    symbol: str,
    start_date: str | None,
    end_date: str | None,
) -> pd.DataFrame:
    try:
        import akshare as ak
    except ImportError as exc:
        raise ImportError(
            "AkShare is not installed. Run `pip install akshare` or set source='csv'."
        ) from exc

    df = ak.stock_zh_index_daily(symbol=symbol)

    rename_map = {
        "date": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    df = df.rename(columns=rename_map)

    if start_date is not None:
        df = df[pd.to_datetime(df["date"]) >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[pd.to_datetime(df["date"]) <= pd.to_datetime(end_date)]

    return df
