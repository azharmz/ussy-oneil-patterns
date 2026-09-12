from datetime import date, timedelta

import pandas as pd

from oneil_patterns.morphology.base_on_base import (
    BaseOnBaseFault,
    BaseOnBaseState,
    BaseRegionSummary,
    assess_base_on_base,
    build_base_on_base_geometry,
)


def _frame(second_values):
    start = date(2026, 1, 2)
    dates = [start + timedelta(days=i) for i in range(70)]
    closes = [90.0] * 70
    for i, value in enumerate(second_values, start=36):
        closes[i] = value
    return pd.DataFrame({"date": dates, "close": closes})


def _bases(second_low):
    start = date(2026, 1, 2)
    b1 = BaseRegionSummary(
        pattern="CUP_WITH_HANDLE",
        start_date=start,
        end_date=start + timedelta(days=30),
        confirmed_date=start + timedelta(days=30),
        high_price=100.0,
        low_price=75.0,
    )
    b2 = BaseRegionSummary(
        pattern="FLAT_BASE",
        start_date=start + timedelta(days=36),
        end_date=start + timedelta(days=50),
        confirmed_date=start + timedelta(days=50),
        high_price=108.0,
        low_price=second_low,
    )
    return b1, b2


def test_clearly_stacked_second_base_is_recognized():
    frame = _frame([101, 102, 103, 104, 102, 105, 104, 106, 103, 105, 104, 107, 106, 105, 108])
    b1, b2 = _bases(98.0)
    result = assess_base_on_base(build_base_on_base_geometry(frame, b1, b2))
    assert result.state == BaseOnBaseState.RECOGNIZED
    assert result.geometry.second_close_fraction_above_first_high >= 0.75


def test_second_base_mostly_below_first_is_rejected():
    frame = _frame([95, 97, 99, 96, 98, 97, 101, 99, 98, 96, 97, 98, 99, 100, 99])
    b1, b2 = _bases(94.0)
    result = assess_base_on_base(build_base_on_base_geometry(frame, b1, b2))
    assert result.state == BaseOnBaseState.REJECTED
    assert BaseOnBaseFault.SECOND_BASE_NOT_ABOVE_FIRST in result.faults


def test_marginally_above_second_base_remains_ambiguous():
    frame = _frame([101, 102, 99, 100, 101, 98, 102, 100, 101, 99, 102, 101, 99, 100, 102])
    b1, b2 = _bases(97.0)
    result = assess_base_on_base(build_base_on_base_geometry(frame, b1, b2))
    assert result.state == BaseOnBaseState.AMBIGUOUS
    assert BaseOnBaseFault.SECOND_BASE_ONLY_MARGINAL_ABOVE in result.faults


def test_future_rows_after_second_base_do_not_change_geometry():
    core = _frame([101, 102, 103, 104, 102, 105, 104, 106, 103, 105, 104, 107, 106, 105, 108])
    b1, b2 = _bases(98.0)
    baseline = build_base_on_base_geometry(core, b1, b2)

    last = pd.to_datetime(core["date"].iloc[-1])
    future = pd.DataFrame({"date": [last + pd.Timedelta(days=i) for i in range(1, 6)], "close": [50, 150, 40, 160, 30]})
    extended = build_base_on_base_geometry(pd.concat([core, future], ignore_index=True), b1, b2)

    assert extended.second_close_fraction_above_first_high == baseline.second_close_fraction_above_first_high
    assert extended.combined_duration_sessions == baseline.combined_duration_sessions
