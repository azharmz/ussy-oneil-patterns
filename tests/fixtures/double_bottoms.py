from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry, build_double_bottom_geometry


@dataclass(frozen=True)
class DoubleBottomFixture:
    name: str
    label: str
    geometry: DoubleBottomGeometry


def _mark(kind, price, day):
    d = date(2026, 1, 2) + timedelta(days=day)
    return LandmarkCandidate(kind, price, d, d, "fixture")


def _geometry(prices, days=(0, 12, 24, 36, 42)):
    marks = [
        _mark(LandmarkType.SWING_HIGH, prices[0], days[0]),
        _mark(LandmarkType.SWING_LOW, prices[1], days[1]),
        _mark(LandmarkType.SWING_HIGH, prices[2], days[2]),
        _mark(LandmarkType.SWING_LOW, prices[3], days[3]),
        _mark(LandmarkType.SWING_HIGH, prices[4], days[4]),
    ]
    start = marks[0].price_date
    end = marks[-1].price_date
    all_days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    session_index = {d: i for i, d in enumerate(all_days)}
    return build_double_bottom_geometry(session_index, *marks)


def double_bottom_fixtures():
    return [
        DoubleBottomFixture("canonical_w", "POSITIVE", _geometry((100, 78, 92, 76, 96))),
        DoubleBottomFixture("too_deep", "NEGATIVE", _geometry((100, 58, 88, 56, 94))),
        DoubleBottomFixture("no_second_undercut", "NEGATIVE", _geometry((100, 78, 92, 80, 96))),
        DoubleBottomFixture("weak_middle_rebound", "AMBIGUOUS", _geometry((100, 78, 82, 76, 94))),
        DoubleBottomFixture("shallow_undercut", "AMBIGUOUS", _geometry((100, 78, 92, 77.8, 96))),
    ]
