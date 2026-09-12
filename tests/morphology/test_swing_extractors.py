from datetime import date

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import (
    ConfirmedWindowParams,
    extract_confirmed_window_landmarks,
)
from oneil_patterns.landmarks.excursion import ExcursionParams, extract_excursion_landmarks
from oneil_patterns.landmarks.model import LandmarkType


def fixture_frame() -> pd.DataFrame:
    dates = pd.date_range("2026-01-02", periods=13, freq="D")
    highs = [100, 104, 110, 108, 103, 98, 94, 96, 101, 106, 111, 109, 105]
    lows = [98, 102, 108, 104, 99, 94, 90, 92, 97, 102, 108, 105, 101]
    return pd.DataFrame({"date": dates, "high": highs, "low": lows})


def test_excursion_confirmation_is_not_backdated():
    frame = fixture_frame()
    marks = extract_excursion_landmarks(
        frame,
        ExcursionParams(reversal_pct=0.10, min_separation_sessions=2),
    )
    assert marks
    assert marks[0].type == LandmarkType.SWING_HIGH
    assert marks[0].price_date == date(2026, 1, 4)
    assert marks[0].confirmed_date > marks[0].price_date


def test_confirmed_window_uses_later_confirmation_date():
    frame = fixture_frame()
    marks = extract_confirmed_window_landmarks(
        frame,
        ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.01),
    )
    peak = next(m for m in marks if m.type == LandmarkType.SWING_HIGH and m.price == 110)
    assert peak.price_date == date(2026, 1, 4)
    assert peak.confirmed_date == date(2026, 1, 6)


def test_confirmed_landmarks_are_prefix_stable():
    frame = fixture_frame()
    params = ExcursionParams(reversal_pct=0.10, min_separation_sessions=2)
    prefix = frame.iloc[:9].copy()
    prefix_marks = extract_excursion_landmarks(prefix, params)
    full_marks = extract_excursion_landmarks(frame, params)

    prefix_last_date = pd.Timestamp(prefix["date"].max()).date()
    full_known_by_prefix = [m for m in full_marks if m.confirmed_date <= prefix_last_date]
    assert prefix_marks == full_known_by_prefix


def test_future_window_is_never_required_before_confirmation_date():
    frame = fixture_frame()
    params = ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.01)
    prefix = frame.iloc[:6].copy()
    prefix_marks = extract_confirmed_window_landmarks(prefix, params)
    assert all(m.confirmed_date <= pd.Timestamp(prefix["date"].max()).date() for m in prefix_marks)
