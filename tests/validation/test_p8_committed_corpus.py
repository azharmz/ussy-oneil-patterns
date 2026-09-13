from pathlib import Path

from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.labels import CorpusSplit, LabelProvenance, SourcePrecision


def test_committed_authoritative_seed_corpus_passes_frozen_schema():
    path = Path("data/p8/labels_v0.csv")
    labels = load_label_corpus_csv(path)

    assert len(labels) == 7
    assert {item.provenance for item in labels} == {LabelProvenance.AUTHORITATIVE_SOURCE}
    assert {item.split for item in labels} == {CorpusSplit.DEVELOPMENT, CorpusSplit.VALIDATION}
    assert len([item for item in labels if item.split == CorpusSplit.DEVELOPMENT]) == 6
    assert len([item for item in labels if item.split == CorpusSplit.VALIDATION]) == 1


def test_validation_examples_are_frozen_before_detector_comparison():
    labels = load_label_corpus_csv(Path("data/p8/labels_v0.csv"))
    validation = [item for item in labels if item.split == CorpusSplit.VALIDATION]
    assert [item.symbol for item in validation] == ["NFLX"]
    assert all(item.label.value == "POSITIVE" for item in validation)


def test_source_precision_and_partial_dimensions_are_preserved():
    labels = {item.symbol: item for item in load_label_corpus_csv(Path("data/p8/labels_v0.csv"))}

    assert labels["SNPS"].window_start_precision == SourcePrecision.DAY
    assert labels["SNPS"].window_end is not None
    assert labels["SNPS"].expected_pivot_level == 392.79

    assert labels["FOUR"].window_start_precision == SourcePrecision.MONTH
    assert labels["FOUR"].window_end is None
    assert labels["FOUR"].expected_pivot_source_date is None
    assert labels["FOUR"].expected_pivot_level == 84.26

    assert labels["TW"].window_start_precision == SourcePrecision.DAY
    assert labels["TW"].window_start.isoformat() == "2024-10-15"
    assert labels["TW"].window_end is None
    assert labels["TW"].expected_pivot_source_date is None
    assert labels["TW"].expected_pivot_level == 136.13


def test_ctsh_source_pivot_is_immutable_but_comparison_basis_is_split_normalized():
    labels = {item.symbol: item for item in load_label_corpus_csv(Path("data/p8/labels_v0.csv"))}
    ctsh = labels["CTSH"]

    assert ctsh.expected_pivot_level == 26.74
    assert ctsh.pivot_price_adjustment_factor == 4.0
    assert ctsh.comparison_pivot_level == 6.685
