from datetime import date

import pytest

from oneil_patterns.validation.labels import (
    CorpusSplit,
    LabelEvidence,
    LabelProvenance,
    LabelValue,
    SourcePrecision,
)
from oneil_patterns.validation.source_dimension_eval import (
    MorphologyPrediction,
    evaluate_positive_development_label,
)


def _label(**overrides):
    values = dict(
        example_id="dev-1",
        symbol="TEST",
        pattern="CUP_WITH_HANDLE",
        label=LabelValue.POSITIVE,
        window_start=date(2024, 2, 1),
        window_end=None,
        asof_date=date(2024, 9, 20),
        provenance=LabelProvenance.AUTHORITATIVE_SOURCE,
        source_name="IBD",
        source_reference="ref",
        split=CorpusSplit.DEVELOPMENT,
        window_start_precision=SourcePrecision.MONTH,
        expected_pivot_source_date=None,
        expected_pivot_level=84.26,
        pivot_price_adjustment_factor=1.0,
    )
    values.update(overrides)
    return LabelEvidence(**values)


def test_month_precision_partial_boundary_matches_without_inventing_end():
    label = _label()
    prediction = MorphologyPrediction(
        candidate_id="four-cwh",
        pattern="CUP_WITH_HANDLE",
        start_date=date(2024, 2, 16),
        end_date=date(2024, 9, 3),
        pivot_level=84.26,
        detector_status="AMBIGUOUS",
    )

    result = evaluate_positive_development_label(label, [prediction])

    assert result.agreement_state == "MATCH"
    assert result.boundary_validation_state == "START_ONLY_SOURCE_ANCHOR_MONTH_START"
    assert result.matched_detector_status == "AMBIGUOUS"
    assert result.end_error_days is None
    assert result.pivot_price_error_pct == 0.0
    assert result.candidate_resolution_state == "UNIQUE"
    assert result.source_equivalent_candidate_count == 1


def test_source_equivalent_candidates_are_reported_without_detector_status_ranking():
    label = _label(
        pattern="DOUBLE_BOTTOM",
        window_start=date(2024, 7, 1),
        window_start_precision=SourcePrecision.MONTH,
        expected_pivot_level=12.74,
    )
    confirmed = MorphologyPrediction(
        candidate_id="a-confirmed",
        pattern="DOUBLE_BOTTOM",
        start_date=date(2024, 7, 30),
        end_date=date(2024, 9, 12),
        pivot_source_date=date(2024, 8, 30),
        pivot_level=12.74,
        detector_status="DOUBLE_BOTTOM_REJECTED",
        candidate_semantics="CONFIRMED_STRUCTURE",
    )
    right_edge = MorphologyPrediction(
        candidate_id="b-right-edge",
        pattern="DOUBLE_BOTTOM",
        start_date=date(2024, 7, 30),
        end_date=date(2024, 9, 20),
        pivot_source_date=date(2024, 8, 30),
        pivot_level=12.74,
        detector_status="DOUBLE_BOTTOM_RECOGNIZED",
        candidate_semantics="OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:test",
    )

    result = evaluate_positive_development_label(label, [right_edge, confirmed])

    assert result.agreement_state == "MATCH"
    assert result.candidate_resolution_state == "SOURCE_EQUIVALENT_MULTIPLE"
    assert result.source_equivalent_candidate_count == 2
    assert result.source_equivalent_detector_statuses == (
        "DOUBLE_BOTTOM_RECOGNIZED",
        "DOUBLE_BOTTOM_REJECTED",
    )
    assert result.source_equivalent_candidate_semantics == (
        "CONFIRMED_STRUCTURE",
        "OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:test",
    )
    # Deterministic presentation can choose one, but detector status never enters
    # source ranking and the disagreement remains visible in the result.
    assert any("presentation-only" in item for item in result.rationale)
    assert any("disagree on detector state" in item for item in result.rationale)


def test_source_window_end_is_not_assumed_to_be_structural_end():
    label = _label(
        pattern="FLAT_BASE",
        window_start=date(2023, 4, 4),
        window_start_precision=SourcePrecision.DAY,
        window_end=date(2023, 5, 18),
        asof_date=date(2023, 5, 18),
        expected_pivot_source_date=date(2023, 4, 4),
        expected_pivot_level=392.79,
    )
    prediction = MorphologyPrediction(
        candidate_id="snps-flat",
        pattern="FLAT_BASE",
        start_date=date(2023, 4, 4),
        end_date=date(2023, 4, 25),
        pivot_source_date=date(2023, 4, 4),
        pivot_level=392.79,
        detector_status="FLAT_BASE_REJECTED",
    )

    result = evaluate_positive_development_label(label, [prediction])

    assert result.agreement_state == "MATCH"
    assert result.start_error_days == 0
    assert result.end_error_days is None
    assert result.pivot_date_error_days == 0
    assert result.boundary_validation_state == "START_SCORED_SOURCE_END_ROLE_UNSPECIFIED_DAY_START"
    assert any("semantic role" in item for item in result.rationale)


def test_ctsh_split_factor_changes_only_comparison_basis():
    label = _label(
        symbol="CTSH",
        window_start=date(2004, 1, 1),
        asof_date=date(2004, 7, 31),
        expected_pivot_level=26.74,
        pivot_price_adjustment_factor=4.0,
    )
    prediction = MorphologyPrediction(
        candidate_id="ctsh-cwh",
        pattern="CUP_WITH_HANDLE",
        start_date=date(2004, 1, 20),
        pivot_level=6.685,
        detector_status="AMBIGUOUS",
    )

    result = evaluate_positive_development_label(label, [prediction])

    assert label.expected_pivot_level == 26.74
    assert label.comparison_pivot_level == pytest.approx(6.685)
    assert result.agreement_state == "MATCH"
    assert result.pivot_price_error_pct == 0.0


def test_missing_required_detector_pivot_is_landmark_disagreement():
    label = _label(expected_pivot_level=84.26)
    prediction = MorphologyPrediction(
        candidate_id="missing-pivot",
        pattern="CUP_WITH_HANDLE",
        start_date=date(2024, 2, 10),
        pivot_level=None,
    )

    result = evaluate_positive_development_label(label, [prediction])

    assert result.agreement_state == "LANDMARK_DISAGREEMENT"
    assert result.pivot_validation_state == "NOT_EVALUABLE"


def test_validation_label_is_locked():
    label = _label(split=CorpusSplit.VALIDATION)
    with pytest.raises(ValueError, match="DEVELOPMENT"):
        evaluate_positive_development_label(label, [])


def test_wrong_pattern_is_miss_pattern_not_boundary_failure():
    label = _label(pattern="DOUBLE_BOTTOM")
    prediction = MorphologyPrediction(
        candidate_id="flat",
        pattern="FLAT_BASE",
        start_date=date(2024, 2, 1),
    )

    result = evaluate_positive_development_label(label, [prediction])

    assert result.agreement_state == "MISS_PATTERN"
    assert result.matched_candidate_id is None
    assert result.candidate_resolution_state == "NONE"
