from pathlib import Path
import yaml

from src.data_loader import load_price_data
from src.data_processor import clean_price_data, filter_date_range
from src.strategy import generate_ma_signal
from src.backtester import run_backtest
from src.performance import build_performance_summary
from src.optimizer import optimize_parameters
from src.visualization import (
    plot_nav_curve,
    plot_drawdown,
    plot_trade_signals,
    plot_parameter_heatmap,
)
from src.report import generate_markdown_report


def main() -> None:
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    figure_dir = Path(config["output"]["figure_dir"])
    table_dir = Path(config["output"]["table_dir"])
    report_dir = Path(config["output"]["report_dir"])
    figure_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    df = load_price_data(
        source=config["data"]["source"],
        symbol=config["data"]["symbol"],
        csv_path=config["data"]["csv_path"],
        start_date=config["data"]["start_date"],
        end_date=config["data"]["end_date"],
    )
    df = clean_price_data(df)

    short_window = config["strategy"]["short_window"]
    long_window = config["strategy"]["long_window"]

    df_signal = generate_ma_signal(df, short_window, long_window)

    fee = config["backtest"]["commission"] + config["backtest"]["slippage"]
    df_bt = run_backtest(df_signal, fee=fee)

    summary = build_performance_summary(
        df_bt,
        periods_per_year=config["backtest"]["periods_per_year"],
    )
    summary.to_csv(table_dir / "performance_summary.csv", encoding="utf-8-sig")

    optimization_result = optimize_parameters(
        df,
        short_windows=config["optimization"]["short_windows"],
        long_windows=config["optimization"]["long_windows"],
        fee=fee,
        periods_per_year=config["backtest"]["periods_per_year"],
    )
    optimization_result.to_csv(
        table_dir / "optimization_results.csv",
        index=False,
        encoding="utf-8-sig",
    )

    plot_nav_curve(df_bt, figure_dir / "nav_curve.png")
    plot_drawdown(df_bt, figure_dir / "drawdown.png")
    plot_trade_signals(df_bt, figure_dir / "trade_signals.png")
    plot_parameter_heatmap(
        optimization_result,
        value_col="sharpe_ratio",
        save_path=figure_dir / "parameter_heatmap.png",
    )

    train_df = filter_date_range(
        df,
        config["optimization"]["train_start"],
        config["optimization"]["train_end"],
    )
    test_df = filter_date_range(
        df,
        config["optimization"]["test_start"],
        config["optimization"]["test_end"],
    )

    train_result = optimize_parameters(
        train_df,
        short_windows=config["optimization"]["short_windows"],
        long_windows=config["optimization"]["long_windows"],
        fee=fee,
        periods_per_year=config["backtest"]["periods_per_year"],
    )

    best = train_result.sort_values("sharpe_ratio", ascending=False).iloc[0]
    test_signal = generate_ma_signal(
        test_df,
        int(best["short_window"]),
        int(best["long_window"]),
    )
    test_bt = run_backtest(test_signal, fee=fee)
    test_summary = build_performance_summary(
        test_bt,
        periods_per_year=config["backtest"]["periods_per_year"],
    )
    test_summary.to_csv(table_dir / "out_of_sample_summary.csv", encoding="utf-8-sig")

    generate_markdown_report(
        summary=summary,
        optimization_result=optimization_result,
        best_params=best.to_dict(),
        output_path=report_dir / "backtest_report.md",
    )

    print("Backtest completed.")
    print(f"Performance summary saved to: {table_dir / 'performance_summary.csv'}")
    print(f"Optimization results saved to: {table_dir / 'optimization_results.csv'}")
    print(f"Report saved to: {report_dir / 'backtest_report.md'}")


if __name__ == "__main__":
    main()
