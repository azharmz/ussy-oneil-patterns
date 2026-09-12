from __future__ import annotations

import pytest

from oneil_patterns.landmarks.confirmed_window import ConfirmedWindowParams, extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import ExcursionParams, extract_excursion_landmarks
from oneil_patterns.validation.labelled_eval import RegionLabel, evaluate_regions
from tests.fixtures.expected_landmarks import FIXTURES


def _labels(fixture):
    return [
        RegionLabel(
            type_value=item.type.value,
            start_index=item.start_index,
            end_index=item.end_index,
            label=item.label,
        )
        for item in fixture.expected
    ]


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda x: x.name)
def test_labelled_eval_is_well_formed_for_excursion(fixture):
    frame = fixture.frame_factory()
    marks = extract_excursion_landmarks(
        frame,
        ExcursionParams(reversal_pct=0.08, min_separation_sessions=2),
    )
    result = evaluate_regions(frame, marks, _labels(fixture))
    assert result.matched + result.missed == result.expected
    assert result.false_turns >= 0


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda x: x.name)
def test_labelled_eval_is_well_formed_for_confirmed_window(fixture):
    frame = fixture.frame_factory()
    marks = extract_confirmed_window_landmarks(
        frame,
        ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.015),
    )
    result = evaluate_regions(frame, marks, _labels(fixture))
    assert result.matched + result.missed == result.expected
    assert result.false_turns >= 0


def test_flat_fixture_penalizes_false_structural_turns():
    fixture = next(x for x in FIXTURES if x.name == "flat_sideways")
    frame = fixture.frame_factory()
    labels = _labels(fixture)

    excursion = evaluate_regions(
        frame,
        extract_excursion_landmarks(frame, ExcursionParams(reversal_pct=0.08, min_separation_sessions=2)),
        labels,
    )
    window = evaluate_regions(
        frame,
        extract_confirmed_window_landmarks(frame, ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.015)),
        labels,
    )

    assert excursion.expected == 0
    assert window.expected == 0
    assert excursion.false_turns == excursion.detected
    assert window.false_turns == window.detected


def test_w_fixture_requires_three_core_turns():
    fixture = next(x for x in FIXTURES if x.name == "w_shape")
    frame = fixture.frame_factory()
    labels = _labels(fixture)

    excursion = evaluate_regions(
        frame,
        extract_excursion_landmarks(frame, ExcursionParams(reversal_pct=0.08, min_separation_sessions=2)),
        labels,
    )
    window = evaluate_regions(
        frame,
        extract_confirmed_window_landmarks(frame, ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.015)),
        labels,
    )

    assert excursion.expected == 3
    assert window.expected == 3
