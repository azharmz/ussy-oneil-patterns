from datetime import date

import pandas as pd

from oneil_patterns.validation.cup_body_diagnostics import (
    CUP_BODY_DIAGNOSTIC_VERSION,
    extract_cup_body_diagnostics,
)


def _frame() -> pd.DataFrame:
    dates = pd.bdate_range("2024-01-02", periods=70)
    # Deliberately simple series; test is about diagnostic determinism/schema,
    # not whether this fixture is a textbook cup.
    closes = [100.0 - min(i, 20) * 0.8 + max(i - 20, 0) * 0.55 for i in range(70)]
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": closes,
            "high": [x * 1.01 for x in closes],
            "low": [x * 0.99 for x in closes],
            "close": closes,
            "adj_close": closes,
            "volume": [1_000_000] * 70,
        }
    )


def test_cup_body_diagnostic_is_deterministic_and_never_uses_future_rows():
    frame = _frame()
    asof = frame.iloc[-1]["date"]
    first = extract_cup_body_diagnostics(frame, asof_date=asof)
    second = extract_cup_body_diagnostics(frame, asof_date=asof)
    assert first == second
    for item in first:
        assert item["diagnostic_version"] == CUP_BODY_DIAGNOSTIC_VERSION
        assert set(item) >= {
            "left_rim_date",
            "trough_date",
            "right_rim_date",
            "state",
            "faults",
            "decline_sessions",
            "recovery_sessions",
            "left_right_time_ratio",
            "bottom_dwell_5pct_fraction",
            "bottom_dwell_10pct_fraction",
            "lower_third_fraction",
            "bottom_continuity_10pct",
        }
        assert 0.0 <= item["bottom_dwell_5pct_fraction"] <= 1.0
        assert 0.0 <= item["bottom_dwell_10pct_fraction"] <= 1.0
        assert 0.0 <= item["bottom_continuity_10pct"] <= 1.0


def test_cup_body_diagnostic_rejects_future_rows():
    frame = _frame()
    asof = frame.iloc[-2]["date"]
    try:
        extract_cup_body_diagnostics(frame, asof_date=asof)
    except ValueError as exc:
        assert "future bars" in str(exc)
    else:
        raise AssertionError("future rows must be rejected")


def test_cup_body_measurement_extension_does_not_change_state_semantics():
    frame = _frame()
    asof = frame.iloc[-1]["date"]
    records = extract_cup_body_diagnostics(frame, asof_date=asof)
    for item in records:
        # v0.2 fields are observational only: the production assessment remains
        # represented by the existing state/fault pair.
        assert isinstance(item["state"], str)
        assert isinstance(item["faults"], list)
        if item["sessions_within_10pct_of_trough"]:
            expected = item["max_bottom_run_10pct"] / item["sessions_within_10pct_of_trough"]
            assert item["bottom_continuity_10pct"] == expected
