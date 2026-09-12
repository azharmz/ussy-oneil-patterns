from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Callable

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.segmentation.model import BaseSegmentCandidate, SegmentStage


class FlatBaseFixtureLabel(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True, slots=True)
class FlatBaseFixture:
    name: str
    label: FlatBaseFixtureLabel
    rationale: str
    frame_factory: Callable[[], pd.DataFrame]
    segment_factory: Callable[[], BaseSegmentCandidate]


def _segment(*, duration: int, depth: float) -> BaseSegmentCandidate:
    start_date = date(2026, 1, 2)
    end_date = start_date + timedelta(days=duration - 1)
    start = LandmarkCandidate(
        LandmarkType.SWING_HIGH, 100.0, start_date, start_date, "fixture"
    )
    trough = LandmarkCandidate(
        LandmarkType.SWING_LOW,
        100.0 * (1 - depth),
        end_date,
        end_date,
        "fixture",
    )
    return BaseSegmentCandidate(
        start=start,
        trough=trough,
        recovery=None,
        stage=SegmentStage.DECLINE_CONFIRMED,
        start_date=start_date,
        end_date=end_date,
        confirmed_date=end_date,
        duration_sessions=duration,
        decline_sessions=duration,
        recovery_sessions=None,
        depth_pct=depth,
        recovery_pct=None,
        recovery_to_start_ratio=None,
        recovered_depth_fraction=None,
    )


def _frame(duration: int, closes: list[float]) -> pd.DataFrame:
    if len(closes) != duration:
        raise ValueError("closes length must equal duration")
    dates = pd.date_range("2026-01-02", periods=duration, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "high": [x + 0.5 for x in closes],
            "low": [x - 0.5 for x in closes],
            "close": closes,
        }
    )


def textbook_tight_frame() -> pd.DataFrame:
    duration = 30
    closes = [98.5 + ((i % 5) - 2) * 0.22 for i in range(duration)]
    return _frame(duration, closes)


def short_tight_frame() -> pd.DataFrame:
    duration = 20
    closes = [98.5 + ((i % 4) - 1.5) * 0.20 for i in range(duration)]
    return _frame(duration, closes)


def too_deep_frame() -> pd.DataFrame:
    duration = 30
    closes = [99.0 - min(i, 12) * 0.8 for i in range(duration)]
    return _frame(duration, closes)


def wide_loose_frame() -> pd.DataFrame:
    duration = 30
    closes = [100.0 if i % 2 == 0 else 91.5 for i in range(duration)]
    return _frame(duration, closes)


def borderline_tightness_frame() -> pd.DataFrame:
    duration = 30
    closes = [98.0 + ((i % 6) - 2.5) * 0.75 for i in range(duration)]
    return _frame(duration, closes)


FIXTURES = (
    FlatBaseFixture(
        name="textbook_tight",
        label=FlatBaseFixtureLabel.POSITIVE,
        rationale="Meets frozen duration/depth gates and is deliberately sideways/tight.",
        frame_factory=textbook_tight_frame,
        segment_factory=lambda: _segment(duration=30, depth=0.10),
    ),
    FlatBaseFixture(
        name="too_short",
        label=FlatBaseFixtureLabel.NEGATIVE,
        rationale="Tight geometry but duration is below the frozen 25-session minimum.",
        frame_factory=short_tight_frame,
        segment_factory=lambda: _segment(duration=20, depth=0.08),
    ),
    FlatBaseFixture(
        name="too_deep",
        label=FlatBaseFixtureLabel.NEGATIVE,
        rationale="Duration is sufficient but depth exceeds the frozen 15% maximum.",
        frame_factory=too_deep_frame,
        segment_factory=lambda: _segment(duration=30, depth=0.18),
    ),
    FlatBaseFixture(
        name="wide_loose",
        label=FlatBaseFixtureLabel.NEGATIVE,
        rationale="Passes hard gates but intentionally violates sideways/tight character.",
        frame_factory=wide_loose_frame,
        segment_factory=lambda: _segment(duration=30, depth=0.10),
    ),
    FlatBaseFixture(
        name="borderline_tightness",
        label=FlatBaseFixtureLabel.AMBIGUOUS,
        rationale="Passes hard gates but tightness is intentionally intermediate.",
        frame_factory=borderline_tightness_frame,
        segment_factory=lambda: _segment(duration=30, depth=0.10),
    ),
)
