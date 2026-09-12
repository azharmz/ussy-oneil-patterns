from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.ascending_base import AscendingBaseGeometry, build_ascending_base_geometry


@dataclass(frozen=True)
class AscendingBaseFixture:
    name: str
    label: str
    geometry: AscendingBaseGeometry


def _mark(kind, price, day):
    d = date(2026, 1, 2) + timedelta(days=day)
    return LandmarkCandidate(kind, price, d, d, "fixture")


def _geometry(prices, days):
    marks = [
        _mark(LandmarkType.SWING_HIGH, prices[0], days[0]),
        _mark(LandmarkType.SWING_LOW, prices[1], days[1]),
        _mark(LandmarkType.SWING_HIGH, prices[2], days[2]),
        _mark(LandmarkType.SWING_LOW, prices[3], days[3]),
        _mark(LandmarkType.SWING_HIGH, prices[4], days[4]),
        _mark(LandmarkType.SWING_LOW, prices[5], days[5]),
        _mark(LandmarkType.SWING_HIGH, prices[6], days[6]),
    ]
    start = marks[0].price_date
    end = marks[-1].price_date
    index = {start + timedelta(days=i): i for i in range((end - start).days + 1)}
    return build_ascending_base_geometry(index, *marks)


def ascending_base_fixtures():
    normal_days = (0, 8, 18, 27, 38, 48, 58)
    return [
        AscendingBaseFixture("canonical", "POSITIVE", _geometry((100, 88, 106, 94, 113, 101, 120), normal_days)),
        AscendingBaseFixture("nonascending_trough", "NEGATIVE", _geometry((100, 88, 106, 86, 113, 101, 120), normal_days)),
        AscendingBaseFixture("nonascending_peak", "NEGATIVE", _geometry((100, 88, 99, 94, 113, 101, 120), normal_days)),
        AscendingBaseFixture("too_short", "NEGATIVE", _geometry((100, 88, 106, 94, 113, 101, 120), (0, 5, 10, 15, 20, 25, 30))),
        AscendingBaseFixture("too_long", "NEGATIVE", _geometry((100, 88, 106, 94, 113, 101, 120), (0, 15, 30, 45, 60, 75, 90))),
        AscendingBaseFixture("irregular_depth", "AMBIGUOUS", _geometry((100, 94, 106, 84, 113, 105, 120), normal_days)),
    ]
