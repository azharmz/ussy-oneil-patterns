from __future__ import annotations

import pytest

from oneil_patterns.landmarks.confirmed_window import ConfirmedWindowParams, extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import ExcursionParams, extract_excursion_landmarks
from oneil_patterns.validation.labelled_eval import RegionLabel, evaluate_regions
from tests.fixtures.expected_landmarks import FIXTURES

# Preregistered morphology-only perturbations around the current research defaults.
# These values must not be selected or revised using return, breakout, or trade outcomes.
EXCURSION_GRID = (
    ExcursionParams(reversal_pct=0.06, min_separation_sessions=2),
    ExcursionParams(reversal_pct=0.08, min_separation_sessions=2),
    ExcursionParams(reversal_pct=0.10, min_separation_sessions=2),
    ExcursionParams(reversal_pct=0.08, min_separation_sessions=3),
)

WINDOW_GRID = (
    ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.010),
    ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.015),
    ConfirmedWindowParams(confirm_sessions=2, min_excursion_pct=0.020),
    ConfirmedWindowParams(confirm_sessions=3, min_excursion_pct=0.015),
)


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


def _score_grid(fixture, extractor, grid):
    frame = fixture.frame_factory()
    labels = _labels(fixture)
    return [evaluate_regions(frame, extractor(frame, params), labels) for params in grid]


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda x: x.name)
def test_excursion_perturbations_remain_well_formed(fixture):
    for result in _score_grid(fixture, extract_excursion_landmarks, EXCURSION_GRID):
        assert result.matched + result.missed == result.expected
        assert result.false_turns >= 0


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda x: x.name)
def test_window_perturbations_remain_well_formed(fixture):
    for result in _score_grid(fixture, extract_confirmed_window_landmarks, WINDOW_GRID):
        assert result.matched + result.missed == result.expected
        assert result.false_turns >= 0


def test_flat_range_does_not_explode_under_small_parameter_changes():
    fixture = next(x for x in FIXTURES if x.name == "flat_sideways")
    excursion = _score_grid(fixture, extract_excursion_landmarks, EXCURSION_GRID)
    window = _score_grid(fixture, extract_confirmed_window_landmarks, WINDOW_GRID)

    # A shallow flat fixture has no labelled structural turns. Small parameter
    # changes must not turn it into a dense swing sequence.
    assert max(r.false_turns for r in excursion) <= 1
    assert max(r.false_turns for r in window) <= 1


def test_w_core_structure_is_not_single_parameter_accident():
    fixture = next(x for x in FIXTURES if x.name == "w_shape")
    excursion = _score_grid(fixture, extract_excursion_landmarks, EXCURSION_GRID)
    window = _score_grid(fixture, extract_confirmed_window_landmarks, WINDOW_GRID)

    # Require the majority of nearby settings to recover at least two of the
    # three labelled W turns. This is a morphology-stability guard, not a
    # detector-selection score.
    assert sum(r.matched >= 2 for r in excursion) >= 3
    assert sum(r.matched >= 2 for r in window) >= 3
