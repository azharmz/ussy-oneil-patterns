from __future__ import annotations

import math
import pandas as pd


def _frame(prices: list[float], start: str = "2025-01-02") -> pd.DataFrame:
    dates = pd.bdate_range(start=start, periods=len(prices))
    rows = []
    for dt, close in zip(dates, prices):
        spread = max(0.5, close * 0.008)
        rows.append(
            {
                "date": dt,
                "open": close,
                "high": close + spread,
                "low": close - spread,
                "close": close,
                "volume": 1_000_000,
            }
        )
    return pd.DataFrame(rows)


def v_shape() -> pd.DataFrame:
    prices = [100, 98, 95, 91, 86, 80, 84, 90, 96, 101, 104]
    return _frame(prices)


def w_shape() -> pd.DataFrame:
    prices = [100, 97, 92, 86, 82, 88, 94, 89, 83, 80, 85, 91, 98, 102]
    return _frame(prices)


def flat_sideways() -> pd.DataFrame:
    prices = [100, 101, 99.5, 100.5, 100, 101.2, 99.8, 100.4, 100.1, 101.0, 100.2, 100.7]
    return _frame(prices)


def rounded_cup() -> pd.DataFrame:
    n = 31
    center = (n - 1) / 2
    prices = []
    for i in range(n):
        x = (i - center) / center
        price = 82 + 18 * (x * x)
        prices.append(price)
    return _frame(prices)


def noisy_loose_range() -> pd.DataFrame:
    prices = [100, 108, 96, 105, 91, 103, 89, 110, 94, 107, 92, 106, 90, 109, 95]
    return _frame(prices)
