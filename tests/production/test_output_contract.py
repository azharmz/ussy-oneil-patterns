from datetime import date, datetime, timezone

from oneil_patterns.production.output import (
    ENGINE_VERSION,
    LABELLED_VALIDATION_STATUS,
    OUTPUT_SCHEMA_VERSION,
    ProductionAssessmentRecord,
    ProductionRunManifest,
    serialize_jsonl,
)
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction


def _prediction(native_state="FLAT_BASE_RECOGNIZED", *, candidate_id="candidate-a"):
    return MorphologyPrediction(
        candidate_id=candidate_id,
        pattern="FLAT_BASE",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 8, 15),
        pivot_source_date=date(2026, 7, 1),
        pivot_level=100.0,
        depth_pct=0.10,
        detector_status=native_state,
        detector_faults=() if native_state.endswith("RECOGNIZED") else ("WIDE_LOOSE",),
        candidate_semantics="CONFIRMED_STRUCTURE",
        structural_signature=("LEFT_HIGH:2026-07-01", "BASE_LOW:2026-07-20"),
    )


def _record(native_state="FLAT_BASE_RECOGNIZED", *, candidate_id="candidate-a"):
    return ProductionAssessmentRecord.from_prediction(
        security_id="sec-1",
        ticker="TEST",
        asof_date=date(2026, 9, 12),
        prediction=_prediction(native_state, candidate_id=candidate_id),
    )


def test_stable_assessment_id_is_deterministic_for_same_prediction():
    first = _record()
    second = _record()
    assert first.assessment_id == second.assessment_id
    assert len(first.assessment_id) == 64


def test_candidate_id_change_changes_assessment_id_but_structure_has_stable_base_id():
    first = _record(candidate_id="candidate-a")
    second = _record(candidate_id="candidate-b")
    assert first.assessment_id != second.assessment_id
    assert first.base_id == second.base_id
    assert first.lineage_id == second.lineage_id


def test_output_exposes_frozen_p8_status_and_semantics():
    record = _record("FLAT_BASE_AMBIGUOUS")
    assert record.output_schema_version == OUTPUT_SCHEMA_VERSION == "oneil-pattern-output-v2"
    assert record.engine_version == ENGINE_VERSION == "33-core-p8-frozen-v2"
    assert record.labelled_validation_status == LABELLED_VALIDATION_STATUS == "P8_CONDITIONAL_PASS_FROZEN"
    assert record.detector_contract_version == "flat-base-v2"
    assert record.normalized_status == "AMBIGUOUS"
    assert record.candidate_semantics == "CONFIRMED_STRUCTURE"
    assert record.detector_faults == ("WIDE_LOOSE",)
    assert record.pivot_level == 100.0
    assert record.structural_signature == ("LEFT_HIGH:2026-07-01", "BASE_LOW:2026-07-20")


def test_run_manifest_carries_frozen_contract_versions_and_record_count():
    record = _record()
    manifest = ProductionRunManifest.create(
        asof_date=date(2026, 9, 12),
        records=[record],
        source_manifest_sha256="a" * 64,
        generated_at=datetime(2026, 9, 12, 1, 2, 3, tzinfo=timezone.utc),
    )
    assert manifest.record_count == 1
    assert manifest.labelled_validation_status == "P8_CONDITIONAL_PASS_FROZEN"
    assert manifest.contract_versions["flat_base"] == "flat-base-v2"
    assert manifest.contract_versions["double_bottom"] == "double-bottom-v3"
    assert manifest.contract_versions["cup_family"] == "cup-family-v3-cwoh-fragmentation"
    assert manifest.contract_versions["prediction_adapter"] == "p8-canonical-prediction-adapter-v1.2-cwh-measurement"
    assert manifest.generated_at_utc == "2026-09-12T01:02:03+00:00"


def test_jsonl_serialization_is_order_independent_and_deterministic():
    first = _record(candidate_id="candidate-a")
    second = _record("FLAT_BASE_AMBIGUOUS", candidate_id="candidate-b")
    assert serialize_jsonl([first, second]) == serialize_jsonl([second, first])
