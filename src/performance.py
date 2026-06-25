from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_performance(
    returns: pd.Series,
    nav: pd.Series,
    periods_per_year: int = 252,
) -> dict:
    """Calculate core performance metrics."""
    returns = returns.dropna()
    nav = nav.dropna()

    if len(nav) == 0:
        raise ValueError("NAV series is empty.")

    total_return = nav.iloc[-1] - 1
    annual_return = nav.iloc[-1] ** (periods_per_year / len(nav)) - 1
    annual_volatility = returns.std() * np.sqrt(periods_per_year)

    sharpe_ratio = (
        annual_return / annual_volatility
        if annual_volatility != 0 and not np.isnan(annual_volatility)
        else np.nan
    )

    cummax = nav.cummax()
    drawdown = nav / cummax - 1
    max_drawdown = drawdown.min()

    calmar_ratio = (
        annual_return / abs(max_drawdown)
        if max_drawdown != 0 and not np.isnan(max_drawdown)
        else np.nan
    )

    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "calmar_ratio": calmar_ratio,
    }


def build_performance_summary(
    df: pd.DataFrame,
    periods_per_year: int = 252,
) -> pd.DataFrame:
    strategy = calculate_performance(
        df["strategy_return"],
        df["strategy_nav"],
        periods_per_year,
    )
    benchmark = calculate_performance(
        df["market_return"],
        df["benchmark_nav"],
        periods_per_year,
    )

    summary = pd.DataFrame({
        "strategy": strategy,
        "benchmark": benchmark,
    })

    summary.loc["trade_count", "strategy"] = df["trade"].sum()
    summary.loc["trade_count", "benchmark"] = np.nan
    summary.loc["holding_ratio", "strategy"] = df["position"].mean()
    summary.loc["holding_ratio", "benchmark"] = 1.0
    summary.loc["excess_total_return", "strategy"] = (
        strategy["total_return"] - benchmark["total_return"]
    )
    summary.loc["excess_total_return", "benchmark"] = np.nan

    return summary
