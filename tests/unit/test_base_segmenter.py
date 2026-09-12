from datetime import date, timedelta

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.segmentation.segmenter import segment_base_candidates


def _frame():
    dates = pd.bdate_range("2026-01-02", periods=12)
    return pd.DataFrame({"date": dates, "close": range(12)})


def _candidate(kind, price, price_date, confirmed_date, *, boundary=False):
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=price_date,
        confirmed_date=confirmed_date,
        method="percentage_excursion",
        boundary=boundary,
    )


def test_segments_high_low_recovery_without_pattern_label():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[3]),
        _candidate(LandmarkType.SWING_LOW, 80.0, d[5], d[7]),
        _candidate(LandmarkType.SWING_HIGH, 96.0, d[9], d[10]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[11])

    assert len(result) == 1
    segment = result[0]
    assert segment.start is marks[0]
    assert segment.trough is marks[1]
    assert segment.recovery is marks[2]
    assert segment.duration_sessions == 9
    assert segment.depth_pct == 0.20
    assert segment.recovery_pct == 0.20
    assert segment.confirmed_date == d[10]
    assert "pattern" not in segment.evidence


def test_future_confirmed_recovery_is_not_used_asof_prefix():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[3]),
        _candidate(LandmarkType.SWING_LOW, 82.0, d[5], d[6]),
        _candidate(LandmarkType.SWING_HIGH, 95.0, d[8], d[10]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[8])

    assert len(result) == 1
    assert result[0].recovery is None
    assert result[0].end_date == d[5]
    assert result[0].confirmed_date == d[6]


def test_boundary_evidence_is_preserved_not_deleted():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[0], d[2], boundary=True),
        _candidate(LandmarkType.SWING_LOW, 85.0, d[4], d[6]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[7])

    assert len(result) == 1
    assert result[0].evidence["start_boundary"] is True
