from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from typing import Iterable

from oneil_patterns.production.identity import (
    CORE_BASE_ID_VERSION,
    CORE_LINEAGE_VERSION,
    stable_base_id,
    stable_lineage_id,
)
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction

OUTPUT_SCHEMA_VERSION = "oneil-pattern-output-v2"
ENGINE_VERSION = "33-core-p8-frozen-v2"
LABELLED_VALIDATION_STATUS = "P8_CONDITIONAL_PASS_FROZEN"

CONTRACT_VERSIONS = {
    "landmarks": "p1-landmark-v1",
    "segmentation": "p2-segmentation-v1+explicit-right-edge-observation",
    "flat_base": "flat-base-v2",
    "double_bottom": "double-bottom-v3",
    "cup_family": "cup-family-v3-cwoh-fragmentation",
    "prediction_adapter": "p8-canonical-prediction-adapter-v1.2-cwh-measurement",
    "pivot_adapter": "p8-pivot-adapter-v0.2",
    "candidate_identity_audit": "p8-candidate-identity-audit-v0.4",
    "base_identity": CORE_BASE_ID_VERSION,
    "lineage": CORE_LINEAGE_VERSION,
}

CORE_PATTERNS = {
    "FLAT_BASE",
    "DOUBLE_BOTTOM",
    "CUP_WITHOUT_HANDLE",
    "CUP_WITH_HANDLE",
}


def _iso(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def _normalized_status(native_state: str | None) -> str:
    value = native_state or ""
    if value.endswith("_RECOGNIZED"):
        return "RECOGNIZED"
    if value.endswith("_AMBIGUOUS"):
        return "AMBIGUOUS"
    if value.endswith("_REJECTED"):
        return "REJECTED"
    raise ValueError(f"unsupported frozen core detector state: {native_state!r}")


def stable_assessment_id(
    *,
    security_id: str,
    asof_date: date,
    candidate_id: str,
    engine_version: str = ENGINE_VERSION,
) -> str:
    payload = {
        "security_id": security_id,
        "asof_date": asof_date.isoformat(),
        "candidate_id": candidate_id,
        "engine_version": engine_version,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ProductionAssessmentRecord:
    assessment_id: str
    output_schema_version: str
    engine_version: str
    labelled_validation_status: str
    security_id: str
    ticker: str
    asof_date: str
    candidate_id: str
    base_id: str
    lineage_id: str
    pattern: str
    normalized_status: str
    native_state: str
    candidate_semantics: str
    structural_signature: tuple[str, ...]
    structural_start: str
    structural_end: str | None
    pivot_source_date: str | None
    pivot_level: float | None
    depth_pct: float | None
    detector_faults: tuple[str, ...]
    detector_contract_version: str

    @classmethod
    def from_prediction(
        cls,
        *,
        security_id: str,
        ticker: str,
        asof_date: date,
        prediction: MorphologyPrediction,
    ) -> "ProductionAssessmentRecord":
        if prediction.pattern not in CORE_PATTERNS:
            raise ValueError(f"pattern is outside frozen core P8 scope: {prediction.pattern}")
        native_state = prediction.detector_status
        if not native_state:
            raise ValueError("production prediction must carry detector_status")
        assessment_id = stable_assessment_id(
            security_id=security_id,
            asof_date=asof_date,
            candidate_id=prediction.candidate_id,
        )
        return cls(
            assessment_id=assessment_id,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
            engine_version=ENGINE_VERSION,
            labelled_validation_status=LABELLED_VALIDATION_STATUS,
            security_id=security_id,
            ticker=ticker,
            asof_date=asof_date.isoformat(),
            candidate_id=prediction.candidate_id,
            base_id=stable_base_id(security_id, prediction),
            lineage_id=stable_lineage_id(security_id, prediction),
            pattern=prediction.pattern,
            normalized_status=_normalized_status(native_state),
            native_state=native_state,
            candidate_semantics=prediction.candidate_semantics,
            structural_signature=tuple(prediction.structural_signature),
            structural_start=prediction.start_date.isoformat(),
            structural_end=_iso(prediction.end_date),
            pivot_source_date=_iso(prediction.pivot_source_date),
            pivot_level=round(float(prediction.pivot_level), 8) if prediction.pivot_level is not None else None,
            depth_pct=round(float(prediction.depth_pct), 8) if prediction.depth_pct is not None else None,
            detector_faults=tuple(prediction.detector_faults),
            detector_contract_version=CONTRACT_VERSIONS[
                {
                    "FLAT_BASE": "flat_base",
                    "DOUBLE_BOTTOM": "double_bottom",
                    "CUP_WITHOUT_HANDLE": "cup_family",
                    "CUP_WITH_HANDLE": "cup_family",
                }[prediction.pattern]
            ],
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProductionRunManifest:
    output_schema_version: str
    engine_version: str
    labelled_validation_status: str
    asof_date: str
    source_manifest_sha256: str | None
    contract_versions: dict[str, str]
    record_count: int
    generated_at_utc: str

    @classmethod
    def create(
        cls,
        *,
        asof_date: date,
        records: Iterable[ProductionAssessmentRecord],
        source_manifest_sha256: str | None = None,
        generated_at: datetime | None = None,
    ) -> "ProductionRunManifest":
        record_list = list(records)
        timestamp = generated_at or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return cls(
            output_schema_version=OUTPUT_SCHEMA_VERSION,
            engine_version=ENGINE_VERSION,
            labelled_validation_status=LABELLED_VALIDATION_STATUS,
            asof_date=asof_date.isoformat(),
            source_manifest_sha256=source_manifest_sha256,
            contract_versions=dict(CONTRACT_VERSIONS),
            record_count=len(record_list),
            generated_at_utc=timestamp.astimezone(timezone.utc).isoformat(),
        )


def serialize_jsonl(records: Iterable[ProductionAssessmentRecord]) -> str:
    ordered = sorted(records, key=lambda item: item.assessment_id)
    return "".join(
        json.dumps(item.to_dict(), sort_keys=True, separators=(",", ":")) + "\n"
        for item in ordered
    )
