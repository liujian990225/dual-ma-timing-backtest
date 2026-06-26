# Dual MA Timing Backtest

基于双均线交叉的指数择时策略回测与参数优化项目。项目使用 Python 实现行情数据获取、数据清洗、策略信号生成、交易成本模拟、绩效评估、参数优化、样本内/样本外验证和结果可视化，适合作为量化研究、数据分析或金融科技方向的简历项目。

## 1. Project Overview

双均线择时策略是一类经典趋势跟踪策略。当短期均线高于长期均线时，认为市场处于上升趋势并持仓；当短期均线低于长期均线时，认为市场趋势转弱并空仓。

本项目重点不是追求历史收益最大化，而是构建一个结构清晰、可复现、可解释的量化回测流程。项目不仅实现了基础双均线策略，还加入了交易成本、参数优化、样本内/样本外验证和结果可视化，用于展示完整的量化策略研究流程。

## 2. Strategy Logic

策略规则：

- 计算短期移动平均线 `MA_short`
- 计算长期移动平均线 `MA_long`
- 当 `MA_short > MA_long` 时，目标仓位为 1
- 当 `MA_short <= MA_long` 时，目标仓位为 0
- 为避免未来函数，信号在 T 日收盘后生成，T+1 日才生效

核心处理：

```python
df["position"] = df["signal"].shift(1)
```

该处理保证策略不会使用当天收盘后才产生的信号去赚取当天收益，从而避免 look-ahead bias。

## 3. Features

- 支持 AkShare 获取 A 股指数数据
- 支持本地 CSV 数据读取
- 支持双均线择时信号生成
- 支持手续费和滑点模拟
- 支持策略净值与买入持有基准对比
- 支持年化收益率、最大回撤、夏普比率等指标计算
- 支持参数遍历优化
- 支持样本内/样本外验证
- 支持净值曲线、回撤曲线、买卖点图、参数热力图输出
- 支持配置文件统一管理参数

## 4. Project Structure

```text
dual-ma-timing-backtest/
├── README.md
├── requirements.txt
├── config.yaml
├── main.py
├── src/
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── strategy.py
│   ├── backtester.py
│   ├── performance.py
│   ├── optimizer.py
│   ├── visualization.py
│   └── report.py
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── figures/
│   ├── tables/
│   └── reports/
└── tests/
```

## 5. Quick Start

### 5.1 Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-extra.txt
```

### 5.2 Run backtest

```bash
python main.py
```

运行后会自动生成：

```text
results/figures/nav_curve.png
results/figures/drawdown.png
results/figures/trade_signals.png
results/figures/parameter_heatmap.png
results/tables/performance_summary.csv
results/tables/optimization_results.csv
results/tables/out_of_sample_summary.csv
results/reports/backtest_report.md
```

## 6. Configuration

主要参数在 `config.yaml` 中配置。

```yaml
data:
  source: "akshare"
  symbol: "sh000300"
  start_date: "2010-01-01"
  end_date: "2024-12-31"

strategy:
  short_window: 20
  long_window: 60

backtest:
  initial_cash: 1000000
  commission: 0.0003
  slippage: 0.0002
```

## 7. Backtest Assumptions

- 回测频率：日频
- 策略类型：多头择时，满仓或空仓
- 买入规则：短期均线高于长期均线后，下一交易日持仓
- 卖出规则：短期均线低于或等于长期均线后，下一交易日空仓
- 交易成本：手续费 + 滑点
- 基准策略：买入并持有
- 不考虑融资融券、涨跌停限制和冲击成本
- 不使用未来数据

## 8. Performance Metrics

项目输出以下指标：

- 累计收益率
- 年化收益率
- 年化波动率
- 夏普比率
- 最大回撤
- 收益回撤比
- 交易次数
- 持仓天数比例
- 基准收益率
- 超额收益率

## 9. Parameter Optimization

项目支持遍历短期均线和长期均线参数组合，并输出不同参数组合的表现。

默认参数空间：

```yaml
optimization:
  short_windows: [5, 10, 20, 30, 60]
  long_windows: [30, 60, 120, 180, 250]
```

筛选规则：

```text
short_window < long_window
```

排序指标默认使用夏普比率。参数优化结果并不代表未来一定有效，因此项目进一步加入样本内/样本外验证，用于观察参数稳定性和过拟合风险。

## 10. In-sample and Out-of-sample Test

为降低参数过拟合风险，项目支持样本内参数寻优和样本外验证。

默认划分：

```text
训练区间：2010-01-01 至 2018-12-31
测试区间：2019-01-01 至 2024-12-31
```

研究流程：

1. 在训练区间遍历参数
2. 选择综合表现较好的参数
3. 将该参数应用于测试区间
4. 比较样本内和样本外表现

## 11. Backtest Results

### 11.1 Overall Performance

默认双均线参数为 `short_window = 20`、`long_window = 60`。整体回测结果如下：

| Metric | Strategy | Benchmark |
|---|---:|---:|
| Total Return | 5.70% | 11.31% |
| Annual Return | 0.39% | 0.76% |
| Annual Volatility | 14.94% | 22.03% |
| Sharpe Ratio | 0.026 | 0.034 |
| Max Drawdown | -42.70% | -46.70% |
| Trade Count | 74 | - |
| Holding Ratio | 49.02% | 100.00% |
| Excess Total Return | -5.61% | - |

从整体结果看，默认双均线策略的累计收益和年化收益均低于买入持有基准，但策略的年化波动率和最大回撤也低于基准。这说明双均线择时在该区间内没有明显提升收益，但在降低市场暴露和控制回撤方面有一定作用。

### 11.2 Out-of-sample Performance

样本外测试结果如下：

| Metric | Strategy | Benchmark |
|---|---:|---:|
| Total Return | -9.01% | 32.51% |
| Annual Return | -1.85% | 5.71% |
| Annual Volatility | 13.57% | 19.28% |
| Sharpe Ratio | -0.136 | 0.296 |
| Max Drawdown | -34.51% | -45.60% |
| Trade Count | 27 | - |
| Holding Ratio | 44.32% | 100.00% |
| Excess Total Return | -41.52% | - |

样本外结果显示，策略收益明显弱于买入持有基准，说明样本内表现较好的均线参数在未来区间并没有稳定延续。与此同时，策略最大回撤低于基准，说明其仍然具备一定风险控制能力。整体来看，双均线策略在趋势不连续或市场快速反转阶段容易出现信号滞后和收益损失。

### 11.3 Parameter Optimization Results

参数优化结果中，样本内表现最好的组合为：

```text
short_window = 5
long_window = 60
```

该组合的表现如下：

| Metric | Value |
|---|---:|
| Total Return | 79.29% |
| Annual Return | 4.19% |
| Annual Volatility | 15.00% |
| Sharpe Ratio | 0.279 |
| Max Drawdown | -33.02% |
| Trade Count | 105 |
| Holding Ratio | 49.80% |

从参数优化结果看，较短的短期均线能够更快捕捉趋势变化，因此在样本内取得了更高收益。但该组合交易次数较多，也意味着策略对市场噪声更敏感。结合样本外结果可以看出，参数优化存在一定过拟合风险，不能仅根据历史最优参数判断策略未来表现。

## 12. Key Findings

1. 默认双均线策略没有显著跑赢买入持有基准，但最大回撤和波动率相对更低。
2. 参数优化可以显著改善样本内表现，其中 `5/60` 组合在历史区间内表现较好。
3. 样本外测试中策略收益明显下降，说明双均线参数存在敏感性和过拟合风险。
4. 双均线策略更适合作为趋势过滤和风险控制工具，而不是单独作为稳定收益增强策略。
5. 策略在趋势行情中更容易发挥作用，在震荡行情中容易产生频繁交易和假信号。

## 13. Limitations

- 双均线策略存在信号滞后
- 震荡行情中容易反复交易
- 参数选择对结果影响较大
- 简化交易成本假设可能低估真实摩擦
- 未考虑流动性冲击和涨跌停约束
- 当前项目只测试单一指数，尚未验证多资产适用性

## 14. Future Improvements

- 加入波动率过滤器
- 加入成交量过滤器
- 增加趋势强度过滤条件，例如 `close > MA250`
- 增加多资产组合回测
- 增加滚动窗口 Walk-forward 优化
- 使用 Plotly 或 Streamlit 构建交互式展示
- 与 Backtrader 或 VectorBT 框架结果对照验证

## 15. Resume Description

```text
基于 Python 构建指数双均线择时策略回测系统，完成行情数据获取、数据清洗、交易信号生成、交易成本模拟、净值计算、绩效评估、参数优化和样本外验证；通过信号滞后处理避免未来函数，并输出净值曲线、回撤曲线、买卖点图和参数热力图。研究发现双均线策略可在一定程度上降低最大回撤，但收益表现依赖市场趋势环境，存在参数敏感和样本外衰减问题。
```
