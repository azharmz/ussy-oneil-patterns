from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from typing import Iterable

from oneil_patterns.morphology.faults import PatternAssessmentEnvelope

OUTPUT_SCHEMA_VERSION = "oneil-pattern-output-v1"
ENGINE_VERSION = "33-first-pass-v1"
LABELLED_VALIDATION_STATUS = "P8_BLOCKED_ON_CORPUS"

CONTRACT_VERSIONS = {
    "landmarks": "p1-landmark-v1",
    "segmentation": "p2-segmentation-v1",
    "flat_base": "flat-base-v1",
    "double_bottom": "double-bottom-v1",
    "cup_family": "cup-family-v1",
    "advanced_patterns": "advanced-patterns-v1",
    "fault_ambiguity": "fault-ambiguity-v1",
}


def _iso(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def stable_assessment_id(
    *,
    security_id: str,
    asof_date: date,
    pattern: str,
    structural_start: date | None,
    structural_end: date | None,
    confirmed_date: date | None,
    native_state: str,
    contract_version: str,
) -> str:
    payload = {
        "security_id": security_id,
        "asof_date": asof_date.isoformat(),
        "pattern": pattern,
        "structural_start": _iso(structural_start),
        "structural_end": _iso(structural_end),
        "confirmed_date": _iso(confirmed_date),
        "native_state": native_state,
        "contract_version": contract_version,
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
    pattern: str
    normalized_status: str
    native_state: str
    structural_start: str | None
    structural_end: str | None
    confirmed_date: str | None
    faults: tuple[dict[str, str], ...]
    detector_contract_version: str

    @classmethod
    def from_envelope(
        cls,
        *,
        security_id: str,
        ticker: str,
        asof_date: date,
        envelope: PatternAssessmentEnvelope,
        structural_start: date | None = None,
        structural_end: date | None = None,
        confirmed_date: date | None = None,
    ) -> "ProductionAssessmentRecord":
        assessment_id = stable_assessment_id(
            security_id=security_id,
            asof_date=asof_date,
            pattern=envelope.pattern,
            structural_start=structural_start,
            structural_end=structural_end,
            confirmed_date=confirmed_date,
            native_state=envelope.native_state,
            contract_version=envelope.contract_version,
        )
        faults = tuple(
            {
                "code": fault.code,
                "native_code": fault.native_code,
                "severity": fault.severity.value,
                "provenance": fault.provenance.value,
            }
            for fault in envelope.faults
        )
        return cls(
            assessment_id=assessment_id,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
            engine_version=ENGINE_VERSION,
            labelled_validation_status=LABELLED_VALIDATION_STATUS,
            security_id=security_id,
            ticker=ticker,
            asof_date=asof_date.isoformat(),
            pattern=envelope.pattern,
            normalized_status=envelope.status.value,
            native_state=envelope.native_state,
            structural_start=_iso(structural_start),
            structural_end=_iso(structural_end),
            confirmed_date=_iso(confirmed_date),
            faults=faults,
            detector_contract_version=envelope.contract_version,
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
