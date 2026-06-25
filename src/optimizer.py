from __future__ import annotations

import pandas as pd

from src.strategy import generate_ma_signal
from src.backtester import run_backtest
from src.performance import calculate_performance


def optimize_parameters(
    df: pd.DataFrame,
    short_windows: list[int],
    long_windows: list[int],
    fee: float,
    periods_per_year: int = 252,
) -> pd.DataFrame:
    """Grid-search dual moving-average parameters."""
    records = []

    for short_window in short_windows:
        for long_window in long_windows:
            if short_window >= long_window:
                continue

            try:
                signal_df = generate_ma_signal(df, short_window, long_window)
                bt_df = run_backtest(signal_df, fee=fee)
                metrics = calculate_performance(
                    bt_df["strategy_return"],
                    bt_df["strategy_nav"],
                    periods_per_year=periods_per_year,
                )
            except Exception as exc:
                records.append({
                    "short_window": short_window,
                    "long_window": long_window,
                    "error": str(exc),
                })
                continue

            record = {
                "short_window": short_window,
                "long_window": long_window,
                "trade_count": bt_df["trade"].sum(),
                "holding_ratio": bt_df["position"].mean(),
            }
            record.update(metrics)
            records.append(record)

    result = pd.DataFrame(records)
    if "sharpe_ratio" in result.columns:
        result = result.sort_values("sharpe_ratio", ascending=False)

    return result
