from datetime import timedelta

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body_detector import assess_cup_body
from oneil_patterns.morphology.cup_family import (
    CupFamilyState,
    HandleFault,
    HandleState,
    assess_handle,
    build_handle_geometry,
    classify_cup_family,
)
from tests.fixtures.cup_bodies import cup_body_fixtures


def _rounded_u():
    return {f.name: f for f in cup_body_fixtures()}["rounded_u"]


def _mark(kind, price, d):
    return LandmarkCandidate(kind, price, d, d, "fixture")


def _session_index(cup, extra_days=12):
    start = cup.geometry.left_rim.price_date
    end = cup.geometry.right_rim.price_date + timedelta(days=extra_days)
    return {start + timedelta(days=i): i for i in range((end - start).days + 1)}


def test_valid_handle_is_recognized_and_maps_to_cwh():
    cup = _rounded_u()
    right = cup.geometry.right_rim.price_date
    low = _mark(LandmarkType.SWING_LOW, 92.0, right + timedelta(days=2))
    recovery = _mark(LandmarkType.SWING_HIGH, 97.0, right + timedelta(days=5))

    geometry = build_handle_geometry(cup.geometry, _session_index(cup), low, recovery)
    handle = assess_handle(geometry)
    family = classify_cup_family(assess_cup_body(cup.geometry), handle, right_edge_context_complete=True)

    assert geometry.duration_sessions == 6
    assert geometry.low_in_upper_half is True
    assert handle.state == HandleState.RECOGNIZED
    assert family == CupFamilyState.CUP_WITH_HANDLE


def test_too_short_handle_is_rejected():
    cup = _rounded_u()
    right = cup.geometry.right_rim.price_date
    low = _mark(LandmarkType.SWING_LOW, 93.0, right + timedelta(days=1))
    recovery = _mark(LandmarkType.SWING_HIGH, 97.0, right + timedelta(days=3))

    handle = assess_handle(build_handle_geometry(cup.geometry, _session_index(cup), low, recovery))
    assert handle.state == HandleState.REJECTED
    assert HandleFault.TOO_SHORT in handle.faults


def test_handle_below_cup_midpoint_is_rejected():
    cup = _rounded_u()
    right = cup.geometry.right_rim.price_date
    low = _mark(LandmarkType.SWING_LOW, 86.0, right + timedelta(days=2))
    recovery = _mark(LandmarkType.SWING_HIGH, 95.0, right + timedelta(days=6))

    handle = assess_handle(build_handle_geometry(cup.geometry, _session_index(cup), low, recovery))
    assert handle.state == HandleState.REJECTED
    assert HandleFault.BELOW_CUP_MIDPOINT in handle.faults


def test_no_handle_requires_complete_right_edge_context_for_cup_no_handle_label():
    cup_assessment = assess_cup_body(_rounded_u().geometry)
    assert classify_cup_family(cup_assessment, None, right_edge_context_complete=False) == CupFamilyState.CUP_FAMILY_INCOMPLETE
    assert classify_cup_family(cup_assessment, None, right_edge_context_complete=True) == CupFamilyState.CUP_NO_HANDLE


def test_malformed_handle_attempt_is_not_silently_relabelled_no_handle():
    cup = _rounded_u()
    right = cup.geometry.right_rim.price_date
    low = _mark(LandmarkType.SWING_LOW, 93.0, right + timedelta(days=1))
    recovery = _mark(LandmarkType.SWING_HIGH, 97.0, right + timedelta(days=3))
    handle = assess_handle(build_handle_geometry(cup.geometry, _session_index(cup), low, recovery))

    family = classify_cup_family(assess_cup_body(cup.geometry), handle, right_edge_context_complete=True)
    assert family == CupFamilyState.CUP_HANDLE_AMBIGUOUS
