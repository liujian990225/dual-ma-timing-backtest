from __future__ import annotations

from pathlib import Path
import pandas as pd


def generate_markdown_report(
    summary: pd.DataFrame,
    optimization_result: pd.DataFrame,
    best_params: dict,
    output_path: str | Path,
) -> None:
    """Generate a simple Markdown report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    top_results = optimization_result.head(10)

    content = f"""# Backtest Report

## 1. Strategy Summary

This report presents a dual moving-average timing strategy backtest.

The strategy holds the asset when the short-term moving average is above the long-term moving average, and stays in cash otherwise.

To prevent look-ahead bias, trading position is shifted by one trading day.

## 2. Performance Summary

{summary.to_markdown()}

## 3. Best Parameters from Optimization

```text
short_window: {best_params.get("short_window")}
long_window: {best_params.get("long_window")}
sharpe_ratio: {best_params.get("sharpe_ratio")}
annual_return: {best_params.get("annual_return")}
max_drawdown: {best_params.get("max_drawdown")}
```

## 4. Top 10 Parameter Results

{top_results.to_markdown(index=False)}

## 5. Notes

- The strategy is trend-following and may perform better in directional markets.
- It may suffer from whipsaw trades in sideways markets.
- Sample-out validation is needed to reduce overfitting risk.
- Transaction costs have been included through commission and slippage assumptions.
"""

    output_path.write_text(content, encoding="utf-8")
