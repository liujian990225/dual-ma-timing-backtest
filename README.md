# Dual MA Timing Backtest

基于双均线交叉的指数择时策略回测与参数优化项目。项目使用 Python 实现行情数据获取、数据清洗、策略信号生成、交易成本模拟、绩效评估、参数优化、样本内/样本外验证和结果可视化，适合作为量化研究、数据分析或金融科技方向的简历项目。

## 1. Project Overview

双均线择时策略是一类经典趋势跟踪策略。当短期均线高于长期均线时，认为市场处于上升趋势并持仓；当短期均线低于长期均线时，认为市场趋势转弱并空仓。

本项目重点不是追求历史收益最大化，而是构建一个结构清晰、可复现、可解释的量化回测流程。

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
│   ├── __init__.py
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

排序指标默认使用夏普比率，也可以根据收益回撤比或年化收益率筛选。

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

## 11. Key Findings Template

你可以在真实运行后补充如下结论：

```text
双均线策略在趋势性较强的市场环境中表现较好，能够在下跌趋势中降低风险暴露；
但在震荡市场中容易出现频繁交易和假突破信号。
样本外表现通常弱于样本内结果，说明均线参数存在一定过拟合风险。
```

## 12. Limitations

- 双均线策略存在信号滞后
- 震荡行情中容易反复交易
- 参数选择对结果影响较大
- 简化交易成本假设可能低估真实摩擦
- 未考虑流动性冲击和涨跌停约束

## 13. Future Improvements

- 加入波动率过滤器
- 加入成交量过滤器
- 增加多资产组合回测
- 增加滚动窗口 Walk-forward 优化
- 使用 Plotly 或 Streamlit 构建交互式展示
- 与 Backtrader 或 VectorBT 框架结果对照验证

## 14. Resume Description

```text
基于 Python 构建指数双均线择时策略回测系统，完成行情数据清洗、交易信号生成、交易成本模拟、净值计算、绩效评估和参数优化；通过信号滞后处理避免未来函数，并采用样本内参数寻优与样本外验证评估策略稳定性；输出净值曲线、回撤曲线、买卖点图和参数热力图，并将项目模块化封装至 GitHub。
```
