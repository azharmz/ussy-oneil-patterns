from datetime import date

import pandas as pd
import pytest

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import HandleState
from oneil_patterns.validation.open_right_edge_handle import (
    enumerate_open_right_edge_handles,
    observe_open_right_edge_handle,
)


def _mark(kind, d, price, confirmed=None):
    return LandmarkCandidate(kind, price, d, confirmed or d, "test")


def _cup():
    left = _mark(LandmarkType.SWING_HIGH, date(2024, 1, 2), 100.0)
    trough = _mark(LandmarkType.SWING_LOW, date(2024, 1, 8), 70.0)
    right = _mark(LandmarkType.SWING_HIGH, date(2024, 1, 12), 96.0, date(2024, 1, 15))
    return CupBodyGeometry(
        left_rim=left,
        trough=trough,
        right_rim=right,
        confirmed_date=date(2024, 1, 15),
        duration_sessions=9,
        decline_sessions=5,
        recovery_sessions=5,
        depth_pct=0.30,
        right_rim_to_left_rim_ratio=0.96,
        left_right_time_ratio=1.0,
        sessions_within_5pct_of_trough=2,
        sessions_within_10pct_of_trough=3,
        lower_third_fraction=0.4,
        max_bottom_run_10pct=2,
    )


def _frame(end="2024-01-24"):
    dates = pd.date_range("2024-01-02", end, freq="B")
    return pd.DataFrame(
        {
            "date": dates,
            "open": [90.0] * len(dates),
            "high": [97.0] * len(dates),
            "low": [80.0] * len(dates),
            "close": [90.0] * len(dates),
        }
    )


def test_open_handle_recognized_without_fabricated_recovery():
    cup = _cup()
    low = _mark(LandmarkType.SWING_LOW, date(2024, 1, 17), 90.0, date(2024, 1, 18))
    result = observe_open_right_edge_handle(
        _frame("2024-01-24"), cup, low, asof_date=date(2024, 1, 24)
    )
    assert result.state == HandleState.RECOGNIZED
    assert result.handle_low == low
    assert result.asof_date == date(2024, 1, 24)
    assert result.duration_sessions >= 5


def test_completed_recovery_high_excludes_open_handle():
    cup = _cup()
    low = _mark(LandmarkType.SWING_LOW, date(2024, 1, 17), 90.0, date(2024, 1, 18))
    recovery = _mark(LandmarkType.SWING_HIGH, date(2024, 1, 22), 95.0, date(2024, 1, 23))
    out = enumerate_open_right_edge_handles(
        _frame("2024-01-24"), cup, [cup.right_rim, low, recovery], asof_date=date(2024, 1, 24)
    )
    assert out == []


def test_future_rows_are_rejected():
    cup = _cup()
    low = _mark(LandmarkType.SWING_LOW, date(2024, 1, 17), 90.0, date(2024, 1, 18))
    with pytest.raises(ValueError, match="future bars"):
        observe_open_right_edge_handle(
            _frame("2024-01-25"), cup, low, asof_date=date(2024, 1, 24)
        )
