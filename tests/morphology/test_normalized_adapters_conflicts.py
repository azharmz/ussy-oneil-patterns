from oneil_patterns.morphology.conflicts import ConflictResolution, resolve_pattern_conflict
from oneil_patterns.morphology.cup_family import CupFamilyState
from oneil_patterns.morphology.faults import NormalizedStatus, normalize_assessment
from oneil_patterns.morphology.adapters import normalize_cup_family


def _env(pattern, native_state, contract="test-v1"):
    return normalize_assessment(
        pattern=pattern,
        native_state=native_state,
        native_faults=(),
        contract_version=contract,
    )


def test_cup_family_non_recognized_state_maps_to_rejected():
    envelope = normalize_cup_family(CupFamilyState.NOT_A_RECOGNIZED_CUP)
    assert envelope.status == NormalizedStatus.REJECTED


def test_no_recognized_pattern_returns_no_primary():
    result = resolve_pattern_conflict([
        _env("FLAT_BASE", "FLAT_BASE_REJECTED"),
        _env("DOUBLE_BOTTOM", "DOUBLE_BOTTOM_AMBIGUOUS"),
    ])
    assert result.resolution == ConflictResolution.NO_RECOGNIZED_PATTERN
    assert result.primary_pattern is None


def test_single_recognized_pattern_is_clear():
    result = resolve_pattern_conflict([
        _env("FLAT_BASE", "FLAT_BASE_RECOGNIZED"),
        _env("DOUBLE_BOTTOM", "DOUBLE_BOTTOM_REJECTED"),
    ])
    assert result.resolution == ConflictResolution.CLEAR
    assert result.primary_pattern == "FLAT_BASE"


def test_cup_body_plus_completed_family_is_hierarchical_not_conflict():
    result = resolve_pattern_conflict([
        _env("CUP_BODY", "CUP_RECOGNIZED", "cup-family-v1"),
        normalize_cup_family(CupFamilyState.CUP_WITH_HANDLE),
    ])
    assert result.resolution == ConflictResolution.HIERARCHICAL
    assert result.primary_pattern == "CUP_WITH_HANDLE"


def test_unrelated_simultaneous_recognition_remains_ambiguous():
    result = resolve_pattern_conflict([
        _env("FLAT_BASE", "FLAT_BASE_RECOGNIZED"),
        _env("DOUBLE_BOTTOM", "DOUBLE_BOTTOM_RECOGNIZED"),
    ])
    assert result.resolution == ConflictResolution.MULTI_PATTERN_AMBIGUITY
    assert result.primary_pattern is None
    assert set(result.recognized_patterns) == {"FLAT_BASE", "DOUBLE_BOTTOM"}


def test_relation_level_base_on_base_does_not_silently_override_component_pattern():
    result = resolve_pattern_conflict([
        _env("FLAT_BASE", "FLAT_BASE_RECOGNIZED"),
        _env("BASE_ON_BASE", "BASE_ON_BASE_RECOGNIZED", "advanced-patterns-v1"),
    ])
    assert result.resolution == ConflictResolution.MULTI_PATTERN_AMBIGUITY
    assert result.primary_pattern is None
