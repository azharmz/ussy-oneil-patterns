from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType


@dataclass(frozen=True, slots=True)
class CupBodyGeometry:
    left_rim: LandmarkCandidate
    trough: LandmarkCandidate
    right_rim: LandmarkCandidate
    confirmed_date: date
    duration_sessions: int
    decline_sessions: int
    recovery_sessions: int
    depth_pct: float
    right_rim_to_left_rim_ratio: float
    left_right_time_ratio: float
    sessions_within_5pct_of_trough: int
    sessions_within_10pct_of_trough: int
    lower_third_fraction: float
    max_bottom_run_10pct: int
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.left_rim.type != LandmarkType.SWING_HIGH:
            raise ValueError("left_rim must be SWING_HIGH")
        if self.trough.type != LandmarkType.SWING_LOW:
            raise ValueError("trough must be SWING_LOW")
        if self.right_rim.type != LandmarkType.SWING_HIGH:
            raise ValueError("right_rim must be SWING_HIGH")
        if min(self.duration_sessions, self.decline_sessions, self.recovery_sessions) < 1:
            raise ValueError("session counts must be positive")
        if not 0 <= self.depth_pct < 1:
            raise ValueError("depth_pct must be in [0, 1)")
        if self.right_rim_to_left_rim_ratio <= 0 or self.left_right_time_ratio <= 0:
            raise ValueError("ratios must be positive")
        if not 0 <= self.lower_third_fraction <= 1:
            raise ValueError("lower_third_fraction must be in [0, 1]")


def _max_true_run(mask: list[bool]) -> int:
    best = current = 0
    for value in mask:
        if value:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def build_cup_body_geometry(
    frame: pd.DataFrame,
    left_rim: LandmarkCandidate,
    trough: LandmarkCandidate,
    right_rim: LandmarkCandidate,
) -> CupBodyGeometry:
    """Measure shared Cup-body geometry without assigning a pattern verdict."""
    if left_rim.type != LandmarkType.SWING_HIGH or trough.type != LandmarkType.SWING_LOW or right_rim.type != LandmarkType.SWING_HIGH:
        raise ValueError("cup body requires SWING_HIGH -> SWING_LOW -> SWING_HIGH")

    required = {"date", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")

    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    date_to_index = {d: i for i, d in enumerate(dates)}
    for mark in (left_rim, trough, right_rim):
        if mark.price_date not in date_to_index:
            raise ValueError(f"landmark date missing from frame: {mark.price_date}")

    li, ti, ri = (date_to_index[left_rim.price_date], date_to_index[trough.price_date], date_to_index[right_rim.price_date])
    if not li < ti < ri:
        raise ValueError("cup landmarks must be strictly chronological")

    if trough.price >= left_rim.price:
        raise ValueError("cup trough must be below left rim")

    region = frame.iloc[li : ri + 1].copy()
    closes = pd.to_numeric(region["close"], errors="raise").astype(float)
    if (closes <= 0).any():
        raise ValueError("prices must be positive")

    depth = (left_rim.price - trough.price) / left_rim.price
    depth_distance = left_rim.price - trough.price
    lower_third_ceiling = trough.price + depth_distance / 3.0

    within_5 = (closes <= trough.price * 1.05).tolist()
    within_10 = (closes <= trough.price * 1.10).tolist()
    lower_third = closes <= lower_third_ceiling

    decline_sessions = ti - li + 1
    recovery_sessions = ri - ti + 1

    return CupBodyGeometry(
        left_rim=left_rim,
        trough=trough,
        right_rim=right_rim,
        confirmed_date=max(left_rim.confirmed_date, trough.confirmed_date, right_rim.confirmed_date),
        duration_sessions=ri - li + 1,
        decline_sessions=decline_sessions,
        recovery_sessions=recovery_sessions,
        depth_pct=depth,
        right_rim_to_left_rim_ratio=right_rim.price / left_rim.price,
        left_right_time_ratio=decline_sessions / recovery_sessions,
        sessions_within_5pct_of_trough=sum(within_5),
        sessions_within_10pct_of_trough=sum(within_10),
        lower_third_fraction=float(lower_third.mean()),
        max_bottom_run_10pct=_max_true_run(within_10),
        evidence={
            "version": "cup-body-geometry-v0",
            "roundedness_threshold_frozen": False,
        },
    )
