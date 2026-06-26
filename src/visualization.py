from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def _ensure_parent(save_path: str | Path) -> None:
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)


def plot_nav_curve(df: pd.DataFrame, save_path: str | Path) -> None:
    _ensure_parent(save_path)
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["strategy_nav"], label="Strategy NAV")
    plt.plot(df.index, df["benchmark_nav"], label="Benchmark NAV")
    plt.title("Strategy NAV vs Benchmark NAV")
    plt.xlabel("Date")
    plt.ylabel("NAV")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_drawdown(df: pd.DataFrame, save_path: str | Path) -> None:
    _ensure_parent(save_path)
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["strategy_drawdown"], label="Strategy Drawdown")
    plt.plot(df.index, df["benchmark_drawdown"], label="Benchmark Drawdown")
    plt.title("Drawdown Comparison")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_trade_signals(df: pd.DataFrame, save_path: str | Path) -> None:
    _ensure_parent(save_path)
    buy_signal = df[(df["position"] == 1) & (df["position"].shift(1) == 0)]
    sell_signal = df[(df["position"] == 0) & (df["position"].shift(1) == 1)]

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["close"], label="Close")
    if "ma_short" in df.columns:
        plt.plot(df.index, df["ma_short"], label="MA Short")
    if "ma_long" in df.columns:
        plt.plot(df.index, df["ma_long"], label="MA Long")

    plt.scatter(buy_signal.index, buy_signal["close"], marker="^", label="Buy")
    plt.scatter(sell_signal.index, sell_signal["close"], marker="v", label="Sell")

    plt.title("Price, Moving Averages and Trade Signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_parameter_heatmap(
    optimization_result: pd.DataFrame,
    value_col: str,
    save_path: str | Path,
) -> None:
    _ensure_parent(save_path)

    pivot = optimization_result.pivot(
        index="short_window",
        columns="long_window",
        values=value_col,
    )

    plt.figure(figsize=(10, 6))
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label=value_col)
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xlabel("Long Window")
    plt.ylabel("Short Window")
    plt.title(f"Parameter Heatmap: {value_col}")

    for i, short in enumerate(pivot.index):
        for j, long in enumerate(pivot.columns):
            value = pivot.loc[short, long]
            if pd.notna(value):
                plt.text(j, i, f"{value:.2f}", ha="center", va="center")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
