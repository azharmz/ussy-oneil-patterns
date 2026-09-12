from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import CupBodyGeometry, build_cup_body_geometry


@dataclass(frozen=True)
class CupBodyFixture:
    name: str
    label: str
    frame: pd.DataFrame
    geometry: CupBodyGeometry


def _mark(kind, price, day):
    d = date(2026, 1, 2) + timedelta(days=day)
    return LandmarkCandidate(kind, price, d, d, "fixture")


def _frame_from_closes(closes):
    start = date(2026, 1, 2)
    return pd.DataFrame({
        "date": [start + timedelta(days=i) for i in range(len(closes))],
        "close": closes,
    })


def _fixture(name, label, closes, trough_index):
    frame = _frame_from_closes(closes)
    left = _mark(LandmarkType.SWING_HIGH, float(closes[0]), 0)
    trough = _mark(LandmarkType.SWING_LOW, float(closes[trough_index]), trough_index)
    right = _mark(LandmarkType.SWING_HIGH, float(closes[-1]), len(closes) - 1)
    geometry = build_cup_body_geometry(frame, left, trough, right)
    return CupBodyFixture(name, label, frame, geometry)


def _linear(a, b, n):
    if n == 1:
        return [float(b)]
    step = (b - a) / (n - 1)
    return [a + step * i for i in range(n)]


def cup_body_fixtures():
    # Broad rounded U: slow descent, multi-session bottom, gradual recovery.
    u = (
        _linear(100, 80, 14)
        + [78, 76, 75, 75, 75, 76, 78]
        + _linear(80, 98, 14)
    )

    # Sharp V: same depth/recovery, but one isolated trough session.
    v = _linear(100, 79, 17) + [75] + _linear(79, 98, 17)

    # W-like path: two separated low regions with a material rebound between them.
    w = (
        _linear(100, 78, 10)
        + _linear(78, 90, 7)[1:]
        + _linear(90, 75, 7)[1:]
        + _linear(75, 98, 14)[1:]
    )

    # Flat/shallow base: duration is long enough but cup depth is not meaningful.
    flat = [100 + ((i % 5) - 2) * 0.25 for i in range(35)]
    flat[17] = 98.8
    flat[-1] = 100.2

    # Wide/loose: noisy path with repeated large oscillations rather than a rounded cup.
    loose = [100.0]
    pattern = [94, 86, 92, 79, 90, 76, 88, 81, 93, 84, 96]
    while len(loose) < 34:
        loose.extend(pattern)
    loose = loose[:34] + [98.0]

    return [
        _fixture("rounded_u", "POSITIVE", u, min(range(len(u)), key=u.__getitem__)),
        _fixture("sharp_v", "NEGATIVE", v, min(range(len(v)), key=v.__getitem__)),
        _fixture("double_bottom_w", "NEGATIVE", w, min(range(len(w)), key=w.__getitem__)),
        _fixture("flat_shallow", "NEGATIVE", flat, min(range(len(flat)), key=flat.__getitem__)),
        _fixture("wide_loose", "NEGATIVE", loose, min(range(len(loose)), key=loose.__getitem__)),
    ]
