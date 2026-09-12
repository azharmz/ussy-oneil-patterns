from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Callable

import pandas as pd


class OhlcvSource(str, Enum):
    R2 = "R2"
    YAHOO_YFINANCE = "YAHOO_YFINANCE"
    TIINGO = "TIINGO"


class SourceUnavailable(Exception):
    """Raised only when a provider cannot supply the requested symbol/window."""


Provider = Callable[[str, date, date], pd.DataFrame]


@dataclass(frozen=True, slots=True)
class RoutedOhlcv:
    source: OhlcvSource
    symbol: str
    start: date
    end: date
    frame: pd.DataFrame
    fallback_reason: str | None


def route_ohlcv(
    *,
    symbol: str,
    start: date,
    end: date,
    r2_provider: Provider,
    yahoo_provider: Provider,
    tiingo_provider: Provider,
) -> RoutedOhlcv:
    """Resolve OHLCV using the frozen P8 priority R2 -> Yahoo -> Tiingo.

    Providers must raise SourceUnavailable only for genuine coverage/availability
    gaps. Data-integrity, schema, authentication, or QC errors intentionally
    propagate and must not trigger silent provider substitution.
    """
    if start > end:
        raise ValueError("start cannot be after end")

    unavailable: list[str] = []
    for source, provider in (
        (OhlcvSource.R2, r2_provider),
        (OhlcvSource.YAHOO_YFINANCE, yahoo_provider),
        (OhlcvSource.TIINGO, tiingo_provider),
    ):
        try:
            frame = provider(symbol, start, end)
        except SourceUnavailable as exc:
            unavailable.append(f"{source.value}:{exc}")
            continue
        if frame.empty:
            raise ValueError(f"{source.value} provider returned empty frame without SourceUnavailable")
        return RoutedOhlcv(
            source=source,
            symbol=symbol,
            start=start,
            end=end,
            frame=frame,
            fallback_reason=("; ".join(unavailable) if unavailable else None),
        )

    raise SourceUnavailable("; ".join(unavailable) or "no provider supplied OHLCV")
