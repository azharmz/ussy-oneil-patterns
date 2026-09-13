from datetime import date

import pandas as pd
import pytest

from oneil_patterns.validation.development_sources import _r2_client
from oneil_patterns.validation.source_router import OhlcvSource, SourceUnavailable, route_ohlcv


def _frame():
    return pd.DataFrame(
        {
            "date": [date(2024, 1, 2)],
            "open": [10.0],
            "high": [11.0],
            "low": [9.0],
            "close": [10.5],
            "adj_close": [10.5],
            "volume": [1000],
        }
    )


def test_missing_r2_configuration_is_source_unavailable(monkeypatch):
    for name in ("R2_ENDPOINT", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET_NAME"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(SourceUnavailable, match="R2 provider not configured"):
        _r2_client()


def test_router_falls_through_only_explicit_unavailable():
    def unavailable(symbol, start, end):
        raise SourceUnavailable("coverage absent")

    routed = route_ohlcv(
        symbol="TEST",
        start=date(2024, 1, 1),
        end=date(2024, 1, 3),
        r2_provider=unavailable,
        yahoo_provider=lambda symbol, start, end: _frame(),
        tiingo_provider=unavailable,
    )
    assert routed.source == OhlcvSource.YAHOO_YFINANCE
    assert "R2:coverage absent" in routed.fallback_reason


def test_router_does_not_mask_operational_failure():
    def broken(symbol, start, end):
        raise RuntimeError("auth/config failure")

    with pytest.raises(RuntimeError, match="auth/config failure"):
        route_ohlcv(
            symbol="TEST",
            start=date(2024, 1, 1),
            end=date(2024, 1, 3),
            r2_provider=broken,
            yahoo_provider=lambda symbol, start, end: _frame(),
            tiingo_provider=lambda symbol, start, end: _frame(),
        )
