from datetime import date

import pandas as pd
import pytest

from oneil_patterns.validation.adjudication import (
    AnchorRule,
    resolve_anchor,
    resolve_first_pivot_cross,
)


def _frame():
    return pd.DataFrame(
        {
            "date": [
                date(2023, 9, 1),
                date(2023, 9, 5),
                date(2023, 9, 6),
                date(2023, 9, 7),
            ],
            "high": [100.0, 104.0, 103.0, 106.0],
            "low": [98.0, 99.0, 97.0, 101.0],
        }
    )


def test_first_and_last_session_use_trading_calendar_not_calendar_edges():
    first = resolve_anchor(
        _frame(),
        source_range_start=date(2023, 9, 2),
        source_range_end=date(2023, 9, 7),
        rule=AnchorRule.FIRST_SESSION,
    )
    last = resolve_anchor(
        _frame(),
        source_range_start=date(2023, 9, 2),
        source_range_end=date(2023, 9, 7),
        rule=AnchorRule.LAST_SESSION,
    )
    assert first.session_date == date(2023, 9, 5)
    assert last.session_date == date(2023, 9, 7)


def test_highest_high_can_resolve_source_stated_left_rim_range():
    result = resolve_anchor(
        _frame(),
        source_range_start=date(2023, 9, 1),
        source_range_end=date(2023, 9, 6),
        rule=AnchorRule.HIGHEST_HIGH,
    )
    assert result.session_date == date(2023, 9, 5)
    assert result.price == 104.0


def test_lowest_low_is_deterministic():
    result = resolve_anchor(
        _frame(),
        source_range_start=date(2023, 9, 1),
        source_range_end=date(2023, 9, 7),
        rule=AnchorRule.LOWEST_LOW,
    )
    assert result.session_date == date(2023, 9, 6)
    assert result.price == 97.0


def test_first_pivot_cross_requires_source_supplied_pivot_and_range():
    result = resolve_first_pivot_cross(
        _frame(),
        source_range_start=date(2023, 9, 5),
        source_range_end=date(2023, 9, 7),
        pivot=103.5,
    )
    assert result.session_date == date(2023, 9, 5)
    assert result.price == 103.5


def test_missing_pivot_cross_fails_closed():
    with pytest.raises(ValueError, match="no pivot cross"):
        resolve_first_pivot_cross(
            _frame(),
            source_range_start=date(2023, 9, 1),
            source_range_end=date(2023, 9, 7),
            pivot=110.0,
        )
