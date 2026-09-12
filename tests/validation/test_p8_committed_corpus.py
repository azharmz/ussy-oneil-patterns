from pathlib import Path

from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.labels import CorpusSplit, LabelProvenance


def test_committed_authoritative_seed_corpus_passes_frozen_schema():
    path = Path("data/p8/labels_v0.csv")
    labels = load_label_corpus_csv(path)

    assert len(labels) >= 2
    assert {item.provenance for item in labels} == {LabelProvenance.AUTHORITATIVE_SOURCE}
    assert {item.split for item in labels} == {CorpusSplit.DEVELOPMENT, CorpusSplit.VALIDATION}


def test_validation_examples_are_frozen_before_detector_comparison():
    labels = load_label_corpus_csv(Path("data/p8/labels_v0.csv"))
    validation = [item for item in labels if item.split == CorpusSplit.VALIDATION]
    assert validation
    assert all(item.label.value == "POSITIVE" for item in validation)
