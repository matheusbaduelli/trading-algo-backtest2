from app.core.backtest_engine import run_sma_backtest
import pandas as pd
import numpy as np
def test_sma_backtest_basic():
    dates = pd.date_range('2020-01-01', periods=100)
    prices = pd.Series(100 + np.cumsum(np.random.randn(100)), index=dates)
    df = pd.DataFrame({'Close': prices})
    df['Open'] = df['Close']
    df['High'] = df['Close']
    df['Low'] = df['Close']
    df['Adj Close'] = df['Close']
    df['Volume'] = 1000
    res = run_sma_backtest(df, short_window=5, long_window=20, initial_capital=1000)
    assert 'final_capital' in res
    assert 'total_return' in res
