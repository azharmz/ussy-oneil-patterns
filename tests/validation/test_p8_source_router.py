from datetime import date

import pandas as pd
import pytest

from oneil_patterns.validation.source_router import (
    OhlcvSource,
    SourceUnavailable,
    route_ohlcv,
)


def _frame():
    return pd.DataFrame({
        "date": [date(2023, 1, 3)],
        "open": [10.0],
        "high": [11.0],
        "low": [9.5],
        "close": [10.5],
        "adj_close": [10.4],
        "volume": [1000],
    })


def test_r2_wins_when_available():
    calls = []

    def r2(symbol, start, end):
        calls.append("r2")
        return _frame()

    def should_not_run(*args):
        raise AssertionError("lower-priority provider was called")

    result = route_ohlcv(
        symbol="SNPS", start=date(2023, 4, 1), end=date(2023, 5, 18),
        r2_provider=r2, yahoo_provider=should_not_run, tiingo_provider=should_not_run,
    )
    assert result.source == OhlcvSource.R2
    assert result.fallback_reason is None
    assert calls == ["r2"]


def test_yahoo_is_second_when_r2_window_unavailable():
    calls = []

    def r2(*args):
        calls.append("r2")
        raise SourceUnavailable("historical window absent")

    def yahoo(*args):
        calls.append("yahoo")
        return _frame()

    def tiingo(*args):
        raise AssertionError("Tiingo must not run when Yahoo succeeds")

    result = route_ohlcv(
        symbol="SNPS", start=date(2023, 4, 1), end=date(2023, 5, 18),
        r2_provider=r2, yahoo_provider=yahoo, tiingo_provider=tiingo,
    )
    assert result.source == OhlcvSource.YAHOO_YFINANCE
    assert calls == ["r2", "yahoo"]
    assert "R2:historical window absent" in result.fallback_reason


def test_tiingo_is_third_when_r2_and_yahoo_unavailable():
    def r2(*args):
        raise SourceUnavailable("window absent")

    def yahoo(*args):
        raise SourceUnavailable("symbol unavailable")

    result = route_ohlcv(
        symbol="IPHI", start=date(2019, 1, 1), end=date(2019, 12, 31),
        r2_provider=r2, yahoo_provider=yahoo, tiingo_provider=lambda *args: _frame(),
    )
    assert result.source == OhlcvSource.TIINGO
    assert "R2:window absent" in result.fallback_reason
    assert "YAHOO_YFINANCE:symbol unavailable" in result.fallback_reason


def test_qc_error_does_not_silently_fallback():
    def broken_r2(*args):
        raise ValueError("checksum mismatch")

    with pytest.raises(ValueError, match="checksum mismatch"):
        route_ohlcv(
            symbol="SNPS", start=date(2023, 4, 1), end=date(2023, 5, 18),
            r2_provider=broken_r2,
            yahoo_provider=lambda *args: _frame(),
            tiingo_provider=lambda *args: _frame(),
        )


def test_all_unavailable_is_explicit():
    def unavailable(*args):
        raise SourceUnavailable("not covered")

    with pytest.raises(SourceUnavailable):
        route_ohlcv(
            symbol="OLD", start=date(2000, 1, 1), end=date(2000, 2, 1),
            r2_provider=unavailable, yahoo_provider=unavailable, tiingo_provider=unavailable,
        )
