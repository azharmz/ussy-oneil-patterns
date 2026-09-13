from __future__ import annotations

import pandas as pd

from oneil_patterns.morphology.flat_base import FlatBaseState, assess_flat_base
from tests.fixtures.flat_bases import FIXTURES


def _fixture(name: str):
    return next(item for item in FIXTURES if item.name == name)


def _assessment(name: str):
    fixture = _fixture(name)
    return assess_flat_base(fixture.frame_factory(), fixture.segment_factory())


def test_future_rows_outside_structural_segment_do_not_change_assessment():
    fixture = _fixture("textbook_tight")
    frame = fixture.frame_factory()
    segment = fixture.segment_factory()
    baseline = assess_flat_base(frame, segment)

    last_date = pd.to_datetime(frame["date"]).max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=10, freq="D")
    future = pd.DataFrame(
        {
            "date": future_dates,
            "high": [130.0, 70.0] * 5,
            "low": [120.0, 60.0] * 5,
            "close": [125.0, 65.0] * 5,
        }
    )
    extended = pd.concat([frame, future], ignore_index=True)
    after_future = assess_flat_base(extended, segment)

    assert after_future == baseline


def test_textbook_positive_is_stable_to_small_price_perturbations():
    fixture = _fixture("textbook_tight")
    segment = fixture.segment_factory()
    frame = fixture.frame_factory()

    states = []
    for scale in (0.999, 1.0, 1.001):
        perturbed = frame.copy()
        perturbed[["high", "low", "close"]] = perturbed[["high", "low", "close"]] * scale
        states.append(assess_flat_base(perturbed, segment).state)

    assert states == [FlatBaseState.RECOGNIZED] * 3


def test_wide_loose_ambiguity_is_stable_to_small_price_perturbations():
    fixture = _fixture("wide_loose")
    segment = fixture.segment_factory()
    frame = fixture.frame_factory()

    states = []
    for scale in (0.999, 1.0, 1.001):
        perturbed = frame.copy()
        perturbed[["high", "low", "close"]] = perturbed[["high", "low", "close"]] * scale
        states.append(assess_flat_base(perturbed, segment).state)

    assert states == [FlatBaseState.AMBIGUOUS] * 3


def test_fixture_state_ordering_matches_p8_v2_policy():
    assert _assessment("textbook_tight").state == FlatBaseState.RECOGNIZED
    assert _assessment("too_short").state == FlatBaseState.REJECTED
    assert _assessment("too_deep").state == FlatBaseState.REJECTED
    assert _assessment("wide_loose").state == FlatBaseState.AMBIGUOUS
    assert _assessment("borderline_tightness").state == FlatBaseState.AMBIGUOUS
