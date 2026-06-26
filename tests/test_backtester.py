import pandas as pd

from src.backtester import run_backtest


def test_run_backtest_outputs_nav():
    df = pd.DataFrame({
        "close": [100, 101, 102, 101, 103],
        "position": [0, 1, 1, 0, 1],
    })

    result = run_backtest(df, fee=0.001)

    assert "strategy_nav" in result.columns
    assert "benchmark_nav" in result.columns
    assert "trade" in result.columns
