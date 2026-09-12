import pytest

from oneil_patterns.morphology.flat_base import FlatBaseState, assess_flat_base
from tests.fixtures.flat_bases import FIXTURES, FlatBaseFixtureLabel


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda x: x.name)
def test_flat_base_fixture_hard_gate_semantics(fixture):
    segment = fixture.segment_factory()
    result = assess_flat_base(fixture.frame_factory(), segment)

    if fixture.name == "too_short":
        assert result.state == FlatBaseState.REJECTED
        assert result.duration_gate is False
        assert result.depth_gate is True
    elif fixture.name == "too_deep":
        assert result.state == FlatBaseState.REJECTED
        assert result.duration_gate is True
        assert result.depth_gate is False
    else:
        assert result.duration_gate is True
        assert result.depth_gate is True
        # v0 deliberately refuses to convert descriptive tightness into a
        # recognition threshold before that threshold is frozen.
        assert result.state == FlatBaseState.AMBIGUOUS


def test_positive_fixture_is_tighter_than_wide_loose_negative():
    by_name = {fixture.name: fixture for fixture in FIXTURES}
    positive = by_name["textbook_tight"]
    loose = by_name["wide_loose"]

    tight_result = assess_flat_base(positive.frame_factory(), positive.segment_factory())
    loose_result = assess_flat_base(loose.frame_factory(), loose.segment_factory())

    assert positive.label == FlatBaseFixtureLabel.POSITIVE
    assert loose.label == FlatBaseFixtureLabel.NEGATIVE
    assert tight_result.close_dispersion_pct < loose_result.close_dispersion_pct
    assert tight_result.normalized_high_low_range < loose_result.normalized_high_low_range
    assert tight_result.upper_band_fraction_5pct > loose_result.upper_band_fraction_5pct


def test_borderline_fixture_sits_between_tight_and_wide_loose_on_dispersion():
    by_name = {fixture.name: fixture for fixture in FIXTURES}
    tight = by_name["textbook_tight"]
    borderline = by_name["borderline_tightness"]
    loose = by_name["wide_loose"]

    tight_result = assess_flat_base(tight.frame_factory(), tight.segment_factory())
    borderline_result = assess_flat_base(
        borderline.frame_factory(), borderline.segment_factory()
    )
    loose_result = assess_flat_base(loose.frame_factory(), loose.segment_factory())

    assert borderline.label == FlatBaseFixtureLabel.AMBIGUOUS
    assert (
        tight_result.close_dispersion_pct
        < borderline_result.close_dispersion_pct
        < loose_result.close_dispersion_pct
    )
