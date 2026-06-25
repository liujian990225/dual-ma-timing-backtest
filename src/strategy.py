from __future__ import annotations

import pandas as pd


def generate_ma_signal(
    df: pd.DataFrame,
    short_window: int,
    long_window: int,
) -> pd.DataFrame:
    """Generate dual moving-average timing signals.

    signal: target position generated after market close
    position: actual position used on the next trading day

    The one-day shift prevents look-ahead bias.
    """
    if short_window <= 0 or long_window <= 0:
        raise ValueError("Moving-average windows must be positive integers.")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window.")
    if "close" not in df.columns:
        raise ValueError("Input DataFrame must contain a 'close' column.")

    result = df.copy()
    result["ma_short"] = result["close"].rolling(short_window).mean()
    result["ma_long"] = result["close"].rolling(long_window).mean()

    result["signal"] = 0
    result.loc[result["ma_short"] > result["ma_long"], "signal"] = 1

    # Avoid look-ahead bias: trade on the next day after signal generation.
    result["position"] = result["signal"].shift(1).fillna(0)

    return result
