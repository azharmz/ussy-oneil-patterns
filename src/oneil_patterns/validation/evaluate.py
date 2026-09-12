from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from oneil_patterns.morphology.faults import NormalizedStatus
from .labels import LabelEvidence, LabelValue


@dataclass(frozen=True, slots=True)
class LabelPrediction:
    example_id: str
    predicted_status: NormalizedStatus


@dataclass(frozen=True, slots=True)
class ValidationMetrics:
    total: int
    exact_agreement: int
    exact_agreement_rate: float
    decisive_total: int
    decisive_correct: int
    decisive_accuracy: float | None
    predicted_ambiguous: int
    labelled_ambiguous: int
    disagreements: tuple[str, ...]


def _expected_status(label: LabelValue) -> NormalizedStatus:
    if label == LabelValue.POSITIVE:
        return NormalizedStatus.RECOGNIZED
    if label == LabelValue.NEGATIVE:
        return NormalizedStatus.REJECTED
    return NormalizedStatus.AMBIGUOUS


def evaluate_predictions(
    labels: Iterable[LabelEvidence],
    predictions: Iterable[LabelPrediction],
) -> ValidationMetrics:
    label_map = {item.example_id: item for item in labels}
    pred_map = {item.example_id: item for item in predictions}

    if set(label_map) != set(pred_map):
        missing = sorted(set(label_map) - set(pred_map))
        extra = sorted(set(pred_map) - set(label_map))
        raise ValueError(f"prediction/label id mismatch: missing={missing}, extra={extra}")

    exact = 0
    decisive_total = 0
    decisive_correct = 0
    predicted_ambiguous = 0
    labelled_ambiguous = 0
    disagreements: list[str] = []

    for example_id, label in label_map.items():
        expected = _expected_status(label.label)
        predicted = pred_map[example_id].predicted_status

        if predicted == NormalizedStatus.AMBIGUOUS:
            predicted_ambiguous += 1
        if expected == NormalizedStatus.AMBIGUOUS:
            labelled_ambiguous += 1

        if predicted == expected:
            exact += 1
        else:
            disagreements.append(example_id)

        if expected in {NormalizedStatus.RECOGNIZED, NormalizedStatus.REJECTED}:
            decisive_total += 1
            if predicted == expected:
                decisive_correct += 1

    total = len(label_map)
    return ValidationMetrics(
        total=total,
        exact_agreement=exact,
        exact_agreement_rate=(exact / total if total else 0.0),
        decisive_total=decisive_total,
        decisive_correct=decisive_correct,
        decisive_accuracy=(decisive_correct / decisive_total if decisive_total else None),
        predicted_ambiguous=predicted_ambiguous,
        labelled_ambiguous=labelled_ambiguous,
        disagreements=tuple(disagreements),
    )
