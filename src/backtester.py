from __future__ import annotations

import pandas as pd


def run_backtest(df: pd.DataFrame, fee: float = 0.001) -> pd.DataFrame:
    """Run vectorized backtest for a long-only timing strategy."""
    required = ["close", "position"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for backtest: {missing}")

    result = df.copy()
    result["market_return"] = result["close"].pct_change().fillna(0)
    result["trade"] = result["position"].diff().abs().fillna(result["position"].abs())

    result["strategy_return"] = (
        result["position"] * result["market_return"]
        - result["trade"] * fee
    )

    result["benchmark_nav"] = (1 + result["market_return"]).cumprod()
    result["strategy_nav"] = (1 + result["strategy_return"]).cumprod()

    result["strategy_cummax"] = result["strategy_nav"].cummax()
    result["strategy_drawdown"] = result["strategy_nav"] / result["strategy_cummax"] - 1

    result["benchmark_cummax"] = result["benchmark_nav"].cummax()
    result["benchmark_drawdown"] = result["benchmark_nav"] / result["benchmark_cummax"] - 1

    return result.dropna()
