import pandas as pd

from src.performance import calculate_performance


def test_calculate_performance_returns_metrics():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01])
    nav = (1 + returns).cumprod()

    metrics = calculate_performance(returns, nav)

    assert "total_return" in metrics
    assert "annual_return" in metrics
    assert "max_drawdown" in metrics
