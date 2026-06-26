import pandas as pd

from src.strategy import generate_ma_signal


def test_generate_ma_signal_has_position_shift():
    df = pd.DataFrame({
        "close": [1, 2, 3, 4, 5, 4, 3, 2, 1, 2],
    })
    result = generate_ma_signal(df, short_window=2, long_window=3)

    assert "signal" in result.columns
    assert "position" in result.columns
    assert result["position"].iloc[0] == 0
    assert result["position"].iloc[4] == result["signal"].iloc[3]
