from datetime import date, timedelta

import pandas as pd
import pytest

from oneil_patterns.validation.canonical_predictions import (
    _candidate_id,
    _right_edge_context_complete,
    extract_core_morphology_predictions,
)


def _frame(days: int = 12) -> pd.DataFrame:
    start = date(2024, 1, 2)
    dates = [start + timedelta(days=i) for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": [100.0 + i for i in range(days)],
            "high": [101.0 + i for i in range(days)],
            "low": [99.0 + i for i in range(days)],
            "close": [100.5 + i for i in range(days)],
            "adj_close": [100.5 + i for i in range(days)],
            "volume": [1_000_000 + i for i in range(days)],
        }
    )


def test_candidate_id_is_deterministic_and_semantic():
    first = _candidate_id("FLAT_BASE", date(2024, 1, 1), date(2024, 2, 1), date(2024, 1, 1))
    second = _candidate_id("FLAT_BASE", date(2024, 1, 1), date(2024, 2, 1), date(2024, 1, 1))
    changed = _candidate_id("DOUBLE_BOTTOM", date(2024, 1, 1), date(2024, 2, 1), date(2024, 1, 1))
    assert first == second
    assert first != changed


def test_cup_no_handle_context_requires_minimum_observed_sessions_after_rim():
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(8)]
    index = {d: i for i, d in enumerate(dates)}
    rim = dates[2]
    assert _right_edge_context_complete(index, right_rim=rim, asof_date=dates[5]) is False
    assert _right_edge_context_complete(index, right_rim=rim, asof_date=dates[6]) is True


def test_extractor_rejects_future_bars():
    frame = _frame()
    with pytest.raises(ValueError, match="future bars"):
        extract_core_morphology_predictions(frame, asof_date=frame.iloc[-2]["date"])


def test_extractor_is_deterministic_on_same_pit_slice():
    frame = _frame()
    asof = frame.iloc[-1]["date"]
    first = extract_core_morphology_predictions(frame, asof_date=asof)
    second = extract_core_morphology_predictions(frame, asof_date=asof)
    assert first == second
