from datetime import date

import pytest

from oneil_patterns.morphology.faults import NormalizedStatus
from oneil_patterns.validation.evaluate import LabelPrediction, evaluate_predictions
from oneil_patterns.validation.labels import (
    CorpusSplit,
    LabelEvidence,
    LabelProvenance,
    LabelValue,
    validate_corpus,
)


def _label(example_id, label, *, split=CorpusSplit.VALIDATION):
    return LabelEvidence(
        example_id=example_id,
        symbol="TEST",
        pattern="FLAT_BASE",
        label=label,
        window_start=date(2026, 1, 1),
        window_end=date(2026, 2, 1),
        asof_date=date(2026, 2, 5),
        provenance=LabelProvenance.AUTHORITATIVE_SOURCE,
        source_name="source",
        source_reference=f"ref-{example_id}",
        split=split,
    )


def test_label_schema_requires_independent_evidence_fields():
    item = _label("a", LabelValue.POSITIVE)
    assert item.provenance == LabelProvenance.AUTHORITATIVE_SOURCE
    assert item.source_reference == "ref-a"


def test_human_annotation_requires_annotator():
    with pytest.raises(ValueError, match="annotator"):
        LabelEvidence(
            example_id="x",
            symbol="TEST",
            pattern="CUP_BODY",
            label=LabelValue.AMBIGUOUS,
            window_start=date(2026, 1, 1),
            window_end=date(2026, 2, 1),
            asof_date=date(2026, 2, 2),
            provenance=LabelProvenance.HUMAN_ANNOTATION,
            source_name="manual",
            source_reference="sheet-row-1",
        )


def test_same_window_cannot_leak_across_development_and_validation():
    dev = _label("dev", LabelValue.POSITIVE, split=CorpusSplit.DEVELOPMENT)
    val = _label("val", LabelValue.POSITIVE, split=CorpusSplit.VALIDATION)
    with pytest.raises(ValueError, match="both corpus splits"):
        validate_corpus([dev, val])


def test_metrics_preserve_ambiguity_as_first_class_outcome():
    labels = [
        _label("p", LabelValue.POSITIVE),
        _label("n", LabelValue.NEGATIVE),
        _label("a", LabelValue.AMBIGUOUS),
    ]
    predictions = [
        LabelPrediction("p", NormalizedStatus.RECOGNIZED),
        LabelPrediction("n", NormalizedStatus.AMBIGUOUS),
        LabelPrediction("a", NormalizedStatus.AMBIGUOUS),
    ]

    metrics = evaluate_predictions(labels, predictions)
    assert metrics.total == 3
    assert metrics.exact_agreement == 2
    assert metrics.exact_agreement_rate == pytest.approx(2 / 3)
    assert metrics.decisive_total == 2
    assert metrics.decisive_correct == 1
    assert metrics.decisive_accuracy == pytest.approx(0.5)
    assert metrics.predicted_ambiguous == 2
    assert metrics.labelled_ambiguous == 1
    assert metrics.disagreements == ("n",)


def test_prediction_ids_must_match_label_ids_exactly():
    with pytest.raises(ValueError, match="id mismatch"):
        evaluate_predictions(
            [_label("a", LabelValue.POSITIVE)],
            [LabelPrediction("b", NormalizedStatus.RECOGNIZED)],
        )
