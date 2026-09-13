from datetime import date, timedelta

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.ascending_base_detector import AscendingBaseState
from oneil_patterns.morphology.ascending_base_right_edge import (
    ASCENDING_BASE_RIGHT_EDGE_CONTRACT_VERSION,
    assess_ascending_base_right_edge,
    build_ascending_base_right_edge_geometry,
)


def _mark(kind, price, day, confirm_day):
    start = date(2026, 1, 2)
    return LandmarkCandidate(
        kind,
        price,
        start + timedelta(days=day),
        start + timedelta(days=confirm_day),
        "fixture",
    )


def _frame(extra_days=0):
    start = date(2026, 1, 2)
    rows = []
    for i in range(80 + extra_days):
        low = 120.0
        if i == 50:
            low = 108.0
        if i > 50:
            low = 115.0
        rows.append({
            "date": start + timedelta(days=i),
            "open": 120.0,
            "high": 122.0,
            "low": low,
            "close": 120.0,
            "volume": 1000,
        })
    return pd.DataFrame(rows)


def _marks():
    return (
        _mark(LandmarkType.SWING_HIGH, 100.0, 0, 5),
        _mark(LandmarkType.SWING_LOW, 90.0, 10, 15),
        _mark(LandmarkType.SWING_HIGH, 110.0, 20, 25),
        _mark(LandmarkType.SWING_LOW, 99.0, 30, 35),
        _mark(LandmarkType.SWING_HIGH, 120.0, 40, 45),
    )


def _index(frame):
    return {d: i for i, d in enumerate(pd.to_datetime(frame["date"]).dt.date)}


def test_right_edge_candidate_is_recognized_after_third_pullback_begins():
    frame = _frame()
    asof = date(2026, 1, 2) + timedelta(days=55)
    geometry = build_ascending_base_right_edge_geometry(
        frame,
        _index(frame),
        *_marks(),
        asof_date=asof,
    )
    result = assess_ascending_base_right_edge(geometry)
    assert geometry.evidence["version"] == ASCENDING_BASE_RIGHT_EDGE_CONTRACT_VERSION
    assert geometry.peak_3.price == 120.0
    assert geometry.observed_trough_3_price == 108.0
    assert geometry.observed_trough_3_date == date(2026, 1, 2) + timedelta(days=50)
    assert result.state == AscendingBaseState.RECOGNIZED


def test_fixed_asof_geometry_is_invariant_to_future_extension():
    base = _frame()
    extended = _frame(extra_days=20)
    asof = date(2026, 1, 2) + timedelta(days=55)
    baseline = build_ascending_base_right_edge_geometry(base, _index(base), *_marks(), asof_date=asof)
    later = build_ascending_base_right_edge_geometry(extended, _index(extended), *_marks(), asof_date=asof)
    assert later.observed_trough_3_date == baseline.observed_trough_3_date
    assert later.observed_trough_3_price == baseline.observed_trough_3_price
    assert later.pullback_depths == baseline.pullback_depths
    assert later.duration_sessions == baseline.duration_sessions


def test_confirmation_date_is_latest_required_confirmed_landmark():
    frame = _frame()
    asof = date(2026, 1, 2) + timedelta(days=55)
    geometry = build_ascending_base_right_edge_geometry(frame, _index(frame), *_marks(), asof_date=asof)
    assert geometry.confirmed_date == max(mark.confirmed_date for mark in _marks())


def test_unconfirmed_third_peak_is_rejected_by_constructor():
    frame = _frame()
    marks = list(_marks())
    marks[-1] = _mark(LandmarkType.SWING_HIGH, 120.0, 40, 60)
    asof = date(2026, 1, 2) + timedelta(days=55)
    try:
        build_ascending_base_right_edge_geometry(frame, _index(frame), *marks, asof_date=asof)
    except ValueError as exc:
        assert "not confirmed" in str(exc)
    else:
        raise AssertionError("expected unconfirmed third peak to fail")
