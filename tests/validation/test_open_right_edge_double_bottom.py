from datetime import date, timedelta

import pandas as pd
import pytest

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.double_bottom import build_double_bottom_geometry
from oneil_patterns.morphology.double_bottom_detector import DoubleBottomState
from oneil_patterns.validation.open_right_edge_double_bottom import observe_open_right_edge_double_bottom


def _mark(kind, price, day):
    d = date(2026, 1, 2) + timedelta(days=day)
    return LandmarkCandidate(kind, price, d, d, "fixture")


def _short_core_geometry():
    marks = [
        _mark(LandmarkType.SWING_HIGH, 100.0, 0),
        _mark(LandmarkType.SWING_LOW, 78.0, 8),
        _mark(LandmarkType.SWING_HIGH, 92.0, 16),
        _mark(LandmarkType.SWING_LOW, 76.0, 24),
    ]
    start = marks[0].price_date
    end = start + timedelta(days=40)
    index = {start + timedelta(days=i): i for i in range(41)}
    return build_double_bottom_geometry(index, *marks), index


def _frame(recover=True):
    start = date(2026, 1, 2)
    dates = [start + timedelta(days=i) for i in range(41)]
    highs = [85.0] * 41
    highs[24:] = [93.0 if recover else 90.0] * 17
    return pd.DataFrame({"date": dates, "high": highs})


def test_elapsed_base_duration_can_resolve_short_core_w_after_pivot_recovery():
    geometry, _ = _short_core_geometry()
    assert geometry.duration_sessions == 25
    observation = observe_open_right_edge_double_bottom(
        _frame(recover=True), geometry, asof_date=date(2026, 2, 11)
    )
    assert observation is not None
    assert observation.observed_duration_sessions == 41
    assert observation.state == DoubleBottomState.RECOGNIZED
    assert observation.faults == ()


def test_no_pivot_recovery_emits_no_completion_observation():
    geometry, _ = _short_core_geometry()
    observation = observe_open_right_edge_double_bottom(
        _frame(recover=False), geometry, asof_date=date(2026, 2, 11)
    )
    assert observation is None


def test_future_rows_are_rejected():
    geometry, _ = _short_core_geometry()
    with pytest.raises(ValueError, match="future bars"):
        observe_open_right_edge_double_bottom(
            _frame(recover=True), geometry, asof_date=date(2026, 2, 10)
        )
