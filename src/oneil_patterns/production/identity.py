from __future__ import annotations

import hashlib

from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction

CORE_BASE_ID_VERSION = "core-base-id-v1"
CORE_LINEAGE_VERSION = "core-lineage-v1"


def _stable_id(prefix: str, *parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return f"{prefix}_" + hashlib.sha256(payload).hexdigest()[:20]


def base_identity_signature(prediction: MorphologyPrediction) -> tuple[str, ...]:
    """Exact structural identity for one canonical morphology candidate.

    Rolling/right-edge observation horizon and candidate semantics are excluded.
    Different structural landmark sets remain different bases.
    """
    if prediction.structural_signature:
        return tuple(prediction.structural_signature)
    return (
        f"START:{prediction.start_date.isoformat()}",
        f"PIVOT_DATE:{prediction.pivot_source_date.isoformat() if prediction.pivot_source_date else ''}",
        f"PIVOT:{prediction.pivot_level if prediction.pivot_level is not None else ''}",
    )


def stable_base_id(security_id: str, prediction: MorphologyPrediction) -> str:
    if not security_id:
        raise ValueError("security_id is required")
    signature = base_identity_signature(prediction)
    return _stable_id(
        "base",
        CORE_BASE_ID_VERSION,
        security_id,
        prediction.pattern,
        *signature,
    )


def _signature_map(prediction: MorphologyPrediction) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in prediction.structural_signature:
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        out[key] = value
    return out


def lineage_anchor_signature(prediction: MorphologyPrediction) -> tuple[str, ...]:
    """Conservative exact-anchor lineage for evolving observations of one base.

    No fuzzy date/price tolerance is allowed in the frozen v1 lineage. This
    deliberately prefers under-merging to accidental lineage churn.
    """
    values = _signature_map(prediction)
    names_by_pattern = {
        "FLAT_BASE": ("LEFT_HIGH",),
        "DOUBLE_BOTTOM": ("LEFT_HIGH", "TROUGH_1", "MIDDLE_PEAK"),
        "CUP_WITHOUT_HANDLE": ("LEFT_RIM", "CUP_LOW"),
        "CUP_WITH_HANDLE": ("LEFT_RIM", "CUP_LOW"),
    }
    names = names_by_pattern.get(prediction.pattern, ())
    anchor = tuple(f"{name}:{values[name]}" for name in names if values.get(name))
    if anchor:
        return anchor
    return base_identity_signature(prediction)


def stable_lineage_id(security_id: str, prediction: MorphologyPrediction) -> str:
    if not security_id:
        raise ValueError("security_id is required")
    anchor = lineage_anchor_signature(prediction)
    return _stable_id(
        "lineage",
        CORE_LINEAGE_VERSION,
        security_id,
        prediction.pattern,
        *anchor,
    )
