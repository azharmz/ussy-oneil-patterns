from datetime import date

import pandas as pd
import pytest

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body_detector import CupBodyFault, CupBodyState
from oneil_patterns.validation.open_right_edge_cnh import (
    enumerate_open_right_edge_cnh,
    observe_open_right_edge_cnh,
)


def _mark(kind, d, price, confirmed=None):
    return LandmarkCandidate(kind, price, d, confirmed or d, "test")


def _frame(periods=45):
    dates = pd.bdate_range("2024-01-02", periods=periods)
    closes = []
    for i in range(periods):
        if i < 18:
            closes.append(99.0 - i * 0.9)
        elif i < 24:
            closes.append(82.0 + abs(i - 21) * 0.3)
        else:
            closes.append(min(98.0, 83.0 + (i - 24) * 0.8))
    highs = [c + 1.0 for c in closes]
    return pd.DataFrame({"date": dates, "high": highs, "close": closes})


def test_open_cnh_uses_confirmed_start_trough_and_observation_horizon():
    frame = _frame(45)
    dates = pd.to_datetime(frame["date"]).dt.date.tolist()
    left = _mark(LandmarkType.SWING_HIGH, dates[0], 100.0, dates[2])
    trough = _mark(LandmarkType.SWING_LOW, dates[21], 80.0, dates[24])
    result = observe_open_right_edge_cnh(frame, left, trough, asof_date=dates[-1])

    assert result.left_rim == left
    assert result.trough == trough
    assert result.asof_date == dates[-1]
    assert result.duration_sessions == 45
    assert abs(result.depth_pct - 0.20) < 1e-12
    assert result.state in {CupBodyState.RECOGNIZED, CupBodyState.AMBIGUOUS}


def test_open_cnh_short_observation_is_rejected_without_fabricating_right_rim():
    frame = _frame(25)
    dates = pd.to_datetime(frame["date"]).dt.date.tolist()
    left = _mark(LandmarkType.SWING_HIGH, dates[0], 100.0, dates[2])
    trough = _mark(LandmarkType.SWING_LOW, dates[18], 82.0, dates[20])
    result = observe_open_right_edge_cnh(frame, left, trough, asof_date=dates[-1])

    assert result.state == CupBodyState.REJECTED
    assert CupBodyFault.TOO_SHORT in result.faults
    assert not hasattr(result, "right_rim")


def test_open_cnh_rejects_future_rows():
    frame = _frame(45)
    dates = pd.to_datetime(frame["date"]).dt.date.tolist()
    left = _mark(LandmarkType.SWING_HIGH, dates[0], 100.0, dates[2])
    trough = _mark(LandmarkType.SWING_LOW, dates[21], 80.0, dates[24])
    with pytest.raises(ValueError, match="future bars"):
        observe_open_right_edge_cnh(frame, left, trough, asof_date=dates[-2])


def test_enumerator_stops_extending_old_trough_after_confirmed_recovery_high():
    frame = _frame(45)
    dates = pd.to_datetime(frame["date"]).dt.date.tolist()
    left = _mark(LandmarkType.SWING_HIGH, dates[0], 100.0, dates[2])
    trough = _mark(LandmarkType.SWING_LOW, dates[21], 80.0, dates[24])
    recovery = _mark(LandmarkType.SWING_HIGH, dates[34], 96.0, dates[37])

    assert enumerate_open_right_edge_cnh(
        frame,
        [left, trough, recovery],
        asof_date=dates[-1],
    ) == []


def test_enumerator_keeps_trough_open_until_later_high_is_confirmed():
    frame = _frame(45)
    dates = pd.to_datetime(frame["date"]).dt.date.tolist()
    left = _mark(LandmarkType.SWING_HIGH, dates[0], 100.0, dates[2])
    trough = _mark(LandmarkType.SWING_LOW, dates[21], 80.0, dates[24])
    future_confirmed_recovery = _mark(LandmarkType.SWING_HIGH, dates[34], 96.0, dates[-1])
    asof = dates[40]
    truncated = frame.loc[pd.to_datetime(frame["date"]).dt.date <= asof].copy()

    observations = enumerate_open_right_edge_cnh(
        truncated,
        [left, trough, future_confirmed_recovery],
        asof_date=asof,
    )

    assert len(observations) == 1
    assert observations[0].left_rim == left
    assert observations[0].trough == trough
