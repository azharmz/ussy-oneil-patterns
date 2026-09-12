from datetime import date, datetime, timezone

from oneil_patterns.morphology.faults import normalize_assessment
from oneil_patterns.production.output import (
    LABELLED_VALIDATION_STATUS,
    OUTPUT_SCHEMA_VERSION,
    ProductionAssessmentRecord,
    ProductionRunManifest,
    serialize_jsonl,
)


def _record(native_state="FLAT_BASE_RECOGNIZED"):
    envelope = normalize_assessment(
        pattern="FLAT_BASE",
        native_state=native_state,
        native_faults=(),
        contract_version="flat-base-v1",
    )
    return ProductionAssessmentRecord.from_envelope(
        security_id="sec-1",
        ticker="TEST",
        asof_date=date(2026, 9, 12),
        envelope=envelope,
        structural_start=date(2026, 7, 1),
        structural_end=date(2026, 8, 15),
        confirmed_date=date(2026, 8, 18),
    )


def test_stable_id_is_deterministic_for_same_semantics():
    first = _record()
    second = _record()
    assert first.assessment_id == second.assessment_id
    assert len(first.assessment_id) == 64


def test_semantic_state_change_changes_stable_id():
    recognized = _record("FLAT_BASE_RECOGNIZED")
    ambiguous = _record("FLAT_BASE_AMBIGUOUS")
    assert recognized.assessment_id != ambiguous.assessment_id


def test_output_always_exposes_p8_validation_blocker():
    record = _record()
    assert record.output_schema_version == OUTPUT_SCHEMA_VERSION
    assert record.labelled_validation_status == LABELLED_VALIDATION_STATUS == "P8_BLOCKED_ON_CORPUS"
    assert record.detector_contract_version == "flat-base-v1"


def test_run_manifest_carries_all_contract_versions_and_record_count():
    record = _record()
    manifest = ProductionRunManifest.create(
        asof_date=date(2026, 9, 12),
        records=[record],
        source_manifest_sha256="a" * 64,
        generated_at=datetime(2026, 9, 12, 1, 2, 3, tzinfo=timezone.utc),
    )
    assert manifest.record_count == 1
    assert manifest.labelled_validation_status == "P8_BLOCKED_ON_CORPUS"
    assert manifest.contract_versions["fault_ambiguity"] == "fault-ambiguity-v1"
    assert manifest.generated_at_utc == "2026-09-12T01:02:03+00:00"


def test_jsonl_serialization_is_order_independent_and_deterministic():
    first = _record("FLAT_BASE_RECOGNIZED")
    second = _record("FLAT_BASE_AMBIGUOUS")
    assert serialize_jsonl([first, second]) == serialize_jsonl([second, first])
