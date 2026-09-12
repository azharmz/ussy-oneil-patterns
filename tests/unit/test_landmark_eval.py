from __future__ import annotations

from oneil_patterns.landmarks.confirmed_window import (
    ConfirmedWindowParams,
    extract_confirmed_window_landmarks,
)
from oneil_patterns.landmarks.excursion import ExcursionParams, extract_excursion_landmarks
from oneil_patterns.validation.landmark_eval import agreement_by_date, prefix_stability
from tests.fixtures.morphologies import (
    flat_sideways,
    noisy_loose_range,
    rounded_cup,
    v_shape,
    w_shape,
)


def excursion(frame):
    return extract_excursion_landmarks(
        frame,
        ExcursionParams(reversal_pct=0.08, min_separation_sessions=2),
    )


def window(frame):
    return extract_confirmed_window_landmarks(
        frame,
        ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.02),
    )


def test_prefix_stability_on_representative_fixtures():
    for fixture in [v_shape(), w_shape(), flat_sideways(), rounded_cup(), noisy_loose_range()]:
        assert prefix_stability(fixture, excursion, min_prefix=5).stable
        assert prefix_stability(fixture, window, min_prefix=5).stable


def test_flat_sideways_is_not_forced_to_have_many_structural_swings():
    frame = flat_sideways()
    assert len(excursion(frame)) <= 1
    assert len(window(frame)) <= 2


def test_w_shape_exposes_multiple_structural_turns():
    frame = w_shape()
    assert len(excursion(frame)) >= 3
    assert len(window(frame)) >= 3


def test_noisy_loose_range_has_more_turns_than_flat_fixture():
    assert len(excursion(noisy_loose_range())) > len(excursion(flat_sideways()))


def test_agreement_metric_is_return_independent_and_bounded():
    frame = w_shape()
    result = agreement_by_date(excursion(frame), window(frame), tolerance_sessions=1)
    assert 0.0 <= result["precision_like"] <= 1.0
    assert 0.0 <= result["recall_like"] <= 1.0
    assert result["matched"] >= 0.0
