def generate_markdown_report(summary, optimization_result, best_params, output_path):
    """Create a lightweight markdown report."""
    top_results = optimization_result.head(10)
    text = "# Backtest Report\n\n"
    text += "## Performance Summary\n\n"
    text += summary.to_markdown()
    text += "\n\n## Best Parameters\n\n"
    text += f"short_window: {best_params.get('short_window')}\n"
    text += f"long_window: {best_params.get('long_window')}\n"
    text += f"sharpe_ratio: {best_params.get('sharpe_ratio')}\n"
    text += "\n## Top Parameter Results\n\n"
    text += top_results.to_markdown(index=False)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
