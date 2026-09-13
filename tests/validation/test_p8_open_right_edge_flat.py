from datetime import date, timedelta

import pandas as pd
import pytest

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.flat_base import FlatBaseFault, FlatBaseState
from oneil_patterns.validation.open_right_edge_flat import observe_open_right_edge_flat


def _frame(days: int = 30) -> pd.DataFrame:
    start = date(2026, 1, 2)
    dates = [start + timedelta(days=i) for i in range(days)]
    closes = [100.0 - min(i, 10) * 0.25 + max(i - 10, 0) * 0.12 for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "high": [x + 0.5 for x in closes],
            "low": [x - 0.5 for x in closes],
            "close": closes,
        }
    )


def _start() -> LandmarkCandidate:
    return LandmarkCandidate(
        type=LandmarkType.SWING_HIGH,
        price=100.5,
        price_date=date(2026, 1, 2),
        confirmed_date=date(2026, 1, 6),
        method="test-confirmed-high",
    )


def test_open_right_edge_requires_start_known_by_asof():
    with pytest.raises(ValueError, match="not known"):
        observe_open_right_edge_flat(_frame(10), _start(), asof_date=date(2026, 1, 5))


def test_open_right_edge_rejects_future_rows_in_input():
    with pytest.raises(ValueError, match="future bars"):
        observe_open_right_edge_flat(_frame(30), _start(), asof_date=date(2026, 1, 20))


def test_prefix_extension_preserves_start_and_only_extends_observation_horizon():
    full = _frame(30)
    t1 = date(2026, 1, 26)
    t2 = date(2026, 1, 31)
    f1 = full.loc[pd.to_datetime(full["date"]).dt.date <= t1].copy()
    f2 = full.loc[pd.to_datetime(full["date"]).dt.date <= t2].copy()

    first = observe_open_right_edge_flat(f1, _start(), asof_date=t1)
    second = observe_open_right_edge_flat(f2, _start(), asof_date=t2)

    assert first.start == second.start
    assert first.asof_date == t1
    assert second.asof_date == t2
    assert second.duration_sessions > first.duration_sessions
    assert first.observed_low_date <= t1
    assert second.observed_low_date <= t2


def test_hard_duration_gate_remains_rejected():
    frame = _frame(20)
    result = observe_open_right_edge_flat(frame, _start(), asof_date=date(2026, 1, 21))
    assert result.state == FlatBaseState.REJECTED
    assert FlatBaseFault.TOO_SHORT in result.faults
