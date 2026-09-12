from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

import pandas as pd


class AnchorRule(str, Enum):
    FIRST_SESSION = "FIRST_SESSION"
    LAST_SESSION = "LAST_SESSION"
    HIGHEST_HIGH = "HIGHEST_HIGH"
    LOWEST_LOW = "LOWEST_LOW"


@dataclass(frozen=True, slots=True)
class ResolvedAnchor:
    rule: AnchorRule
    source_range_start: date
    source_range_end: date
    session_date: date
    price: float | None = None


def _window(frame: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    if start > end:
        raise ValueError("anchor start cannot be after end")
    required = {"date", "high", "low"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"OHLCV missing anchor columns: {sorted(missing)}")

    out = frame.copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise").dt.date
    out["high"] = pd.to_numeric(out["high"], errors="raise")
    out["low"] = pd.to_numeric(out["low"], errors="raise")
    out = out.loc[(out["date"] >= start) & (out["date"] <= end)].copy()
    if out.empty:
        raise ValueError("source anchor range contains no trading sessions")
    if out["date"].duplicated().any():
        raise ValueError("source anchor range contains duplicate trading dates")
    return out.sort_values("date").reset_index(drop=True)


def resolve_anchor(
    frame: pd.DataFrame,
    *,
    source_range_start: date,
    source_range_end: date,
    rule: AnchorRule,
) -> ResolvedAnchor:
    """Resolve a source-stated coarse date range to one trading session.

    The caller must choose the rule from source semantics before detector output is
    inspected. This helper is an adjudication/calendar tool, not a pattern detector.
    """

    work = _window(frame, source_range_start, source_range_end)
    if rule is AnchorRule.FIRST_SESSION:
        row = work.iloc[0]
        price = None
    elif rule is AnchorRule.LAST_SESSION:
        row = work.iloc[-1]
        price = None
    elif rule is AnchorRule.HIGHEST_HIGH:
        row = work.loc[work["high"].idxmax()]
        price = float(row["high"])
    elif rule is AnchorRule.LOWEST_LOW:
        row = work.loc[work["low"].idxmin()]
        price = float(row["low"])
    else:  # pragma: no cover - Enum exhaustiveness guard
        raise ValueError(f"unsupported anchor rule: {rule}")

    return ResolvedAnchor(
        rule=rule,
        source_range_start=source_range_start,
        source_range_end=source_range_end,
        session_date=row["date"],
        price=price,
    )


def resolve_first_pivot_cross(
    frame: pd.DataFrame,
    *,
    source_range_start: date,
    source_range_end: date,
    pivot: float,
) -> ResolvedAnchor:
    """Resolve a source-cited breakout period to the first intraday pivot cross.

    This is permitted only when the authoritative source supplies the pivot/buy
    point and a breakout week/date range. It must not be used to discover a pivot.
    """

    if pivot <= 0:
        raise ValueError("pivot must be positive")
    work = _window(frame, source_range_start, source_range_end)
    crossed = work.loc[work["high"] > float(pivot)]
    if crossed.empty:
        raise ValueError("no pivot cross inside source-cited breakout range")
    row = crossed.iloc[0]
    return ResolvedAnchor(
        rule=AnchorRule.FIRST_SESSION,
        source_range_start=source_range_start,
        source_range_end=source_range_end,
        session_date=row["date"],
        price=float(pivot),
    )
