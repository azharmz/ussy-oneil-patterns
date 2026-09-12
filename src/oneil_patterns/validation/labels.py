from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Mapping


class LabelValue(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    AMBIGUOUS = "AMBIGUOUS"


class LabelProvenance(str, Enum):
    AUTHORITATIVE_SOURCE = "AUTHORITATIVE_SOURCE"
    HUMAN_ANNOTATION = "HUMAN_ANNOTATION"
    ADJUDICATED = "ADJUDICATED"


class CorpusSplit(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    VALIDATION = "VALIDATION"


@dataclass(frozen=True, slots=True)
class LabelEvidence:
    example_id: str
    symbol: str
    pattern: str
    label: LabelValue
    window_start: date
    window_end: date
    asof_date: date
    provenance: LabelProvenance
    source_name: str
    source_reference: str
    annotator: str | None = None
    rationale: str | None = None
    split: CorpusSplit = CorpusSplit.VALIDATION
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.example_id.strip():
            raise ValueError("example_id is required")
        if not self.symbol.strip():
            raise ValueError("symbol is required")
        if not self.pattern.strip():
            raise ValueError("pattern is required")
        if self.window_start > self.window_end:
            raise ValueError("window_start cannot be after window_end")
        if self.asof_date < self.window_end:
            raise ValueError("asof_date cannot precede labelled window_end")
        if not self.source_name.strip() or not self.source_reference.strip():
            raise ValueError("source_name and source_reference are required")
        if self.provenance == LabelProvenance.HUMAN_ANNOTATION and not self.annotator:
            raise ValueError("human annotation requires annotator")


def validate_corpus(labels: list[LabelEvidence]) -> None:
    ids = [item.example_id for item in labels]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate example_id in labelled corpus")

    # Avoid hidden tuning leakage: one logical example cannot appear in both
    # development and final validation under the same symbol/pattern/window.
    seen: dict[tuple[str, str, date, date], CorpusSplit] = {}
    for item in labels:
        key = (item.symbol, item.pattern, item.window_start, item.window_end)
        prior = seen.get(key)
        if prior is not None and prior != item.split:
            raise ValueError("same labelled window cannot appear in both corpus splits")
        seen[key] = item.split
