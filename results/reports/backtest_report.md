# Backtest Report

## 1. Strategy Summary

This report presents a dual moving-average timing strategy backtest.

The strategy holds the asset when the short-term moving average is above the long-term moving average, and stays in cash otherwise.

To prevent look-ahead bias, trading position is shifted by one trading day.

## 2. Performance Summary

|                     |    strategy |    benchmark |
|:--------------------|------------:|-------------:|
| total_return        |  0.0569856  |   0.113057   |
| annual_return       |  0.00390439 |   0.00755962 |
| annual_volatility   |  0.149423   |   0.220327   |
| sharpe_ratio        |  0.0261298  |   0.034311   |
| max_drawdown        | -0.42698    |  -0.466961   |
| calmar_ratio        |  0.00914422 |   0.016189   |
| trade_count         | 74          | nan          |
| holding_ratio       |  0.490234   |   1          |
| excess_total_return | -0.0560713  | nan          |

## 3. Best Parameters from Optimization

```text
short_window: 5.0
long_window: 180.0
sharpe_ratio: 0.38405365274325876
annual_return: 0.060526063115004636
max_drawdown: -0.3370183870669614
```

## 4. Top 10 Parameter Results

|   short_window |   long_window |   trade_count |   holding_ratio |   total_return |   annual_return |   annual_volatility |   sharpe_ratio |   max_drawdown |   calmar_ratio |
|---------------:|--------------:|--------------:|----------------:|---------------:|----------------:|--------------------:|---------------:|---------------:|---------------:|
|              5 |            60 |           105 |        0.498047 |       0.792946 |       0.041907  |            0.150018 |       0.279346 |      -0.330241 |      0.126898  |
|              5 |           180 |            49 |        0.474885 |       0.653628 |       0.037268  |            0.15325  |       0.243185 |      -0.345119 |      0.107986  |
|             30 |           180 |            19 |        0.478349 |       0.628684 |       0.0361217 |            0.15077  |       0.239581 |      -0.331918 |      0.108827  |
|             10 |            30 |           135 |        0.502767 |       0.618244 |       0.034133  |            0.149424 |       0.22843  |      -0.360771 |      0.0946112 |
|              5 |            30 |           169 |        0.496956 |       0.59588  |       0.03313   |            0.149215 |       0.222029 |      -0.311788 |      0.106258  |
|             10 |           180 |            33 |        0.475751 |       0.529692 |       0.0314059 |            0.152087 |       0.2065   |      -0.347869 |      0.0902811 |
|             10 |            60 |            76 |        0.489676 |       0.439526 |       0.0259467 |            0.149762 |       0.173253 |      -0.358382 |      0.0723996 |
|              5 |           120 |            69 |        0.482406 |       0.410867 |       0.0249194 |            0.147717 |       0.168697 |      -0.336692 |      0.0740125 |
|             20 |           180 |            21 |        0.478637 |       0.40076  |       0.0248203 |            0.151201 |       0.164154 |      -0.377371 |      0.0657716 |
|             30 |           250 |            25 |        0.454331 |       0.38433  |       0.0244408 |            0.154508 |       0.158185 |      -0.434846 |      0.0562055 |

## 5. Notes

- The strategy is trend-following and may perform better in directional markets.
- It may suffer from whipsaw trades in sideways markets.
- Sample-out validation is needed to reduce overfitting risk.
- Transaction costs have been included through commission and slippage assumptions.
