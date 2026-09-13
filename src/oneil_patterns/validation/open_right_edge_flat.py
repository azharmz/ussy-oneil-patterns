from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.flat_base import (
    MAX_DEPTH_PCT,
    MIN_DURATION_SESSIONS,
    TIGHT_MAX_CLOSE_DISPERSION,
    TIGHT_MAX_NORMALIZED_RANGE,
    WIDE_LOOSE_MIN_CLOSE_DISPERSION,
    WIDE_LOOSE_MIN_NORMALIZED_RANGE,
    FlatBaseFault,
    FlatBaseState,
)

OPEN_RIGHT_EDGE_FLAT_VERSION = "p8-open-right-edge-flat-v0.2"


@dataclass(frozen=True, slots=True)
class OpenRightEdgeFlatObservation:
    start: LandmarkCandidate
    asof_date: date
    duration_sessions: int
    observed_low_date: date
    observed_low: float
    observed_high: float
    depth_from_start_pct: float
    normalized_high_low_range: float
    close_dispersion_pct: float
    upper_band_fraction_5pct: float
    state: FlatBaseState
    faults: tuple[FlatBaseFault, ...]


def observe_open_right_edge_flat(
    frame: pd.DataFrame,
    start: LandmarkCandidate,
    *,
    asof_date: date,
) -> OpenRightEdgeFlatObservation:
    """Assess a Flat Base observation from a confirmed start high through T.

    `asof_date` is an observation horizon, never a fabricated structural turn.
    The Flat Base hard gates and research bands are reused unchanged. Under the
    P8 v0.2 state policy, a research-only WIDE_LOOSE fault is ambiguous rather
    than a hard rejection when duration/depth hard gates pass.
    """
    if start.type != LandmarkType.SWING_HIGH:
        raise ValueError("open-right-edge Flat observation requires a SWING_HIGH start")
    if start.confirmed_date > asof_date:
        raise ValueError("start high is not known by asof_date")

    required = {"date", "high", "low", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("open-right-edge Flat observation received future bars")
    region = ordered.loc[(dates >= start.price_date) & (dates <= asof_date)].copy()
    if region.empty:
        raise ValueError("open-right-edge Flat region is empty")
    if region[["high", "low", "close"]].isna().any().any():
        raise ValueError("open-right-edge Flat region contains missing prices")

    region_dates = pd.to_datetime(region["date"], errors="raise").dt.date.tolist()
    observed_high = float(region["high"].max())
    low_pos = int(region["low"].astype(float).values.argmin())
    observed_low = float(region.iloc[low_pos]["low"])
    observed_low_date = region_dates[low_pos]
    mean_close = float(region["close"].mean())
    if start.price <= 0 or observed_high <= 0 or mean_close <= 0:
        raise ValueError("prices must be positive")

    duration = len(region)
    depth = max(0.0, (float(start.price) - observed_low) / float(start.price))
    normalized_range = (observed_high - observed_low) / observed_high
    close_dispersion = float(region["close"].std(ddof=0)) / mean_close
    upper_band_fraction = float((region["close"] >= observed_high * 0.95).mean())

    faults: list[FlatBaseFault] = []
    hard_failure = False
    if duration < MIN_DURATION_SESSIONS:
        faults.append(FlatBaseFault.TOO_SHORT)
        hard_failure = True
    if depth > MAX_DEPTH_PCT:
        faults.append(FlatBaseFault.TOO_DEEP)
        hard_failure = True

    wide_loose = (
        normalized_range >= WIDE_LOOSE_MIN_NORMALIZED_RANGE
        or close_dispersion >= WIDE_LOOSE_MIN_CLOSE_DISPERSION
    )
    if wide_loose:
        faults.append(FlatBaseFault.WIDE_LOOSE)

    tight = (
        normalized_range <= TIGHT_MAX_NORMALIZED_RANGE
        and close_dispersion <= TIGHT_MAX_CLOSE_DISPERSION
    )

    if hard_failure:
        state = FlatBaseState.REJECTED
    elif wide_loose:
        state = FlatBaseState.AMBIGUOUS
    elif tight:
        state = FlatBaseState.RECOGNIZED
    else:
        state = FlatBaseState.AMBIGUOUS

    return OpenRightEdgeFlatObservation(
        start=start,
        asof_date=asof_date,
        duration_sessions=duration,
        observed_low_date=observed_low_date,
        observed_low=observed_low,
        observed_high=observed_high,
        depth_from_start_pct=depth,
        normalized_high_low_range=normalized_range,
        close_dispersion_pct=close_dispersion,
        upper_band_fraction_5pct=upper_band_fraction,
        state=state,
        faults=tuple(faults),
    )


def enumerate_open_right_edge_flats(
    frame: pd.DataFrame,
    landmarks: list[LandmarkCandidate],
    *,
    asof_date: date,
) -> list[OpenRightEdgeFlatObservation]:
    """Enumerate label-agnostic right-edge Flat observations from all known highs."""
    starts = [
        item
        for item in landmarks
        if item.type == LandmarkType.SWING_HIGH
        and item.confirmed_date <= asof_date
        and item.price_date <= asof_date
    ]
    starts.sort(key=lambda item: (item.price_date, item.confirmed_date, item.price))
    return [observe_open_right_edge_flat(frame, item, asof_date=asof_date) for item in starts]
