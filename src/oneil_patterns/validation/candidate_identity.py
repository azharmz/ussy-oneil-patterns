from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from typing import Iterable

from .source_dimension_eval import MorphologyPrediction

CANDIDATE_IDENTITY_AUDIT_VERSION = "p8-candidate-identity-audit-v0.4"


@dataclass(frozen=True, slots=True)
class CandidateIdentityAudit:
    identity_id: str
    pattern: str
    structural_signature: tuple[str, ...]
    start_date: str
    pivot_source_date: str | None
    pivot_level: float | None
    depth_pct: float | None
    member_candidate_ids: tuple[str, ...]
    member_count: int
    end_dates: tuple[str, ...]
    detector_statuses: tuple[str, ...]
    candidate_semantics: tuple[str, ...]
    identity_state: str
    version: str = CANDIDATE_IDENTITY_AUDIT_VERSION

    def to_dict(self) -> dict:
        return asdict(self)


def _rounded(value: float | None, digits: int) -> str:
    return "" if value is None else f"{float(value):.{digits}f}"


def structural_identity_signature(prediction: MorphologyPrediction) -> tuple[str, ...]:
    if prediction.structural_signature:
        return (prediction.pattern, *prediction.structural_signature)
    return (
        prediction.pattern,
        f"START:{prediction.start_date.isoformat()}",
        f"PIVOT_DATE:{prediction.pivot_source_date.isoformat() if prediction.pivot_source_date else ''}",
        f"PIVOT:{_rounded(prediction.pivot_level, 6)}",
        f"DEPTH:{_rounded(prediction.depth_pct, 6)}",
    )


def _stable_identity_id(signature: tuple[str, ...]) -> str:
    digest = hashlib.sha256("|".join(signature).encode("utf-8")).hexdigest()[:16]
    return f"p8ident_{digest}"


def _is_right_edge_semantics(value: str) -> bool:
    return "OPEN_RIGHT_EDGE" in value


def _is_maturity_lifecycle(members: list[MorphologyPrediction]) -> bool:
    """Recognize only explicit TOO_SHORT -> mature right-edge evolution.

    Candidate provenance may prefix the right-edge marker (for example
    `CONFIRMED_STRUCTURE:OPEN_RIGHT_EDGE...` or
    `LOCAL_TURN_AUX:...:OPEN_RIGHT_EDGE...`). The lifecycle decision therefore
    keys on the explicit OPEN_RIGHT_EDGE marker rather than a string prefix.
    """
    core = [item for item in members if not _is_right_edge_semantics(item.candidate_semantics)]
    right_edge = [item for item in members if _is_right_edge_semantics(item.candidate_semantics)]
    if not core or not right_edge:
        return False

    short_core = [
        item
        for item in core
        if item.detector_status
        and item.detector_status.endswith("_REJECTED")
        and "TOO_SHORT" in item.detector_faults
    ]
    mature_right_edge = [
        item
        for item in right_edge
        if item.detector_status and not item.detector_status.endswith("_REJECTED")
    ]
    return bool(short_core and mature_right_edge)


def audit_candidate_identities(predictions: Iterable[MorphologyPrediction]) -> list[CandidateIdentityAudit]:
    grouped: dict[tuple[str, ...], list[MorphologyPrediction]] = {}
    for prediction in predictions:
        grouped.setdefault(structural_identity_signature(prediction), []).append(prediction)

    out: list[CandidateIdentityAudit] = []
    for signature, members in grouped.items():
        first = sorted(members, key=lambda item: item.candidate_id)[0]
        statuses = tuple(sorted({item.detector_status or "NONE" for item in members}))
        semantics = tuple(sorted({item.candidate_semantics for item in members}))
        end_dates = tuple(sorted({item.end_date.isoformat() for item in members if item.end_date is not None}))
        if len(statuses) > 1 and _is_maturity_lifecycle(members):
            identity_state = "LIFECYCLE_TRANSITION"
        elif len(statuses) > 1:
            identity_state = "STATUS_CONFLICT"
        elif len(semantics) > 1:
            identity_state = "MULTI_SEMANTIC_STABLE_STATUS"
        else:
            identity_state = "STABLE"
        out.append(
            CandidateIdentityAudit(
                identity_id=_stable_identity_id(signature),
                pattern=first.pattern,
                structural_signature=signature[1:],
                start_date=first.start_date.isoformat(),
                pivot_source_date=first.pivot_source_date.isoformat() if first.pivot_source_date else None,
                pivot_level=round(float(first.pivot_level), 8) if first.pivot_level is not None else None,
                depth_pct=round(float(first.depth_pct), 8) if first.depth_pct is not None else None,
                member_candidate_ids=tuple(sorted(item.candidate_id for item in members)),
                member_count=len(members),
                end_dates=end_dates,
                detector_statuses=statuses,
                candidate_semantics=semantics,
                identity_state=identity_state,
            )
        )

    return sorted(out, key=lambda item: (item.pattern, item.start_date, item.identity_id))
