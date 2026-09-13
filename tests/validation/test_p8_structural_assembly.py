from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.validation.structural_assembly import (
    STRUCTURAL_ASSEMBLY_VERSION,
    assemble_handle_geometries,
    assemble_multiturn_double_bottoms,
    assemble_multiturn_segments,
)


def _frame(days: int = 60) -> pd.DataFrame:
    dates = pd.bdate_range("2024-01-02", periods=days)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": [100.0] * days,
            "high": [101.0] * days,
            "low": [99.0] * days,
            "close": [100.0] * days,
            "adj_close": [100.0] * days,
            "volume": [1_000_000] * days,
        }
    )


def _mark(frame, idx: int, kind: LandmarkType, price: float, *, confirmed_idx: int | None = None):
    confirmed_idx = idx if confirmed_idx is None else confirmed_idx
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=frame.iloc[idx]["date"],
        confirmed_date=frame.iloc[confirmed_idx]["date"],
        method="test",
    )


def test_multiturn_segment_spans_minor_turns_and_uses_deepest_known_low():
    frame = _frame()
    marks = [
        _mark(frame, 0, LandmarkType.SWING_HIGH, 100),
        _mark(frame, 5, LandmarkType.SWING_LOW, 92),
        _mark(frame, 10, LandmarkType.SWING_HIGH, 97),
        _mark(frame, 15, LandmarkType.SWING_LOW, 85),
        _mark(frame, 25, LandmarkType.SWING_HIGH, 98),
    ]

    segments = assemble_multiturn_segments(frame, marks, asof_date=frame.iloc[30]["date"])
    target = next(
        item
        for item in segments
        if item.start.price_date == frame.iloc[0]["date"]
        and item.end_date == frame.iloc[25]["date"]
    )

    assert target.trough.price_date == frame.iloc[15]["date"]
    assert target.evidence["structural_assembly_version"] == STRUCTURAL_ASSEMBLY_VERSION
    # The smaller atomic-scale high-low-high remains representable too.
    assert any(
        item.start.price_date == frame.iloc[0]["date"]
        and item.end_date == frame.iloc[10]["date"]
        for item in segments
    )


def test_multiturn_segment_is_prefix_stable_after_future_extension():
    frame = _frame()
    early_marks = [
        _mark(frame, 0, LandmarkType.SWING_HIGH, 100),
        _mark(frame, 8, LandmarkType.SWING_LOW, 84),
        _mark(frame, 20, LandmarkType.SWING_HIGH, 97),
    ]
    later_marks = early_marks + [
        _mark(frame, 30, LandmarkType.SWING_LOW, 80),
        _mark(frame, 40, LandmarkType.SWING_HIGH, 99),
    ]

    early = assemble_multiturn_segments(frame.iloc[:25], early_marks, asof_date=frame.iloc[24]["date"])
    later = assemble_multiturn_segments(frame, later_marks, asof_date=frame.iloc[50]["date"])

    early_keys = {(x.start_date, x.trough.price_date, x.end_date) for x in early}
    later_keys = {(x.start_date, x.trough.price_date, x.end_date) for x in later}
    assert early_keys <= later_keys


def test_multiturn_double_bottom_uses_highest_middle_peak_and_keeps_multiple_left_scales():
    frame = _frame()
    marks = [
        _mark(frame, 0, LandmarkType.SWING_HIGH, 105),
        _mark(frame, 5, LandmarkType.SWING_HIGH, 101),
        _mark(frame, 10, LandmarkType.SWING_LOW, 80),
        _mark(frame, 16, LandmarkType.SWING_HIGH, 92),
        _mark(frame, 20, LandmarkType.SWING_LOW, 88),
        _mark(frame, 24, LandmarkType.SWING_HIGH, 96),
        _mark(frame, 32, LandmarkType.SWING_LOW, 79),
    ]

    geometries = assemble_multiturn_double_bottoms(frame, marks, asof_date=frame.iloc[40]["date"])
    matches = [
        item
        for item in geometries
        if item.trough_1.price_date == frame.iloc[10]["date"]
        and item.trough_2.price_date == frame.iloc[32]["date"]
    ]

    assert matches
    assert all(item.middle_peak.price_date == frame.iloc[24]["date"] for item in matches)
    assert {item.left_high.price_date for item in matches} >= {
        frame.iloc[0]["date"],
        frame.iloc[5]["date"],
    }


def test_handle_assembly_keeps_multiple_post_rim_attempts():
    frame = _frame()
    left = _mark(frame, 0, LandmarkType.SWING_HIGH, 100)
    trough = _mark(frame, 10, LandmarkType.SWING_LOW, 75)
    right = _mark(frame, 20, LandmarkType.SWING_HIGH, 96)
    cup = build_cup_body_geometry(frame, left, trough, right)
    marks = [
        left,
        trough,
        right,
        _mark(frame, 24, LandmarkType.SWING_LOW, 91),
        _mark(frame, 30, LandmarkType.SWING_HIGH, 95),
        _mark(frame, 35, LandmarkType.SWING_LOW, 90),
        _mark(frame, 42, LandmarkType.SWING_HIGH, 97),
    ]

    handles = assemble_handle_geometries(frame, cup, marks, asof_date=frame.iloc[50]["date"])
    assert [(h.handle_low.price_date, h.handle_recovery.price_date) for h in handles] == [
        (frame.iloc[24]["date"], frame.iloc[30]["date"]),
        (frame.iloc[35]["date"], frame.iloc[42]["date"]),
    ]
