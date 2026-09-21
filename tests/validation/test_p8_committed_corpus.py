from collections import Counter
from pathlib import Path

from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.labels import CorpusSplit, LabelProvenance, SourcePrecision


def _labels():
    return load_label_corpus_csv(Path("data/p8/labels_v0.csv"))


def _by_example():
    return {item.example_id: item for item in _labels()}


def _by_symbol_pattern():
    return {(item.symbol, item.pattern, item.split): item for item in _labels()}


def test_committed_authoritative_corpus_passes_frozen_schema():
    labels = _labels()

    assert len(labels) == 22
    assert {item.provenance for item in labels} == {LabelProvenance.AUTHORITATIVE_SOURCE}
    assert {item.split for item in labels} == {CorpusSplit.DEVELOPMENT, CorpusSplit.VALIDATION}
    assert len([item for item in labels if item.split == CorpusSplit.DEVELOPMENT]) == 20
    assert len([item for item in labels if item.split == CorpusSplit.VALIDATION]) == 2

    counts = Counter(item.pattern for item in labels if item.split == CorpusSplit.DEVELOPMENT)
    assert counts == {
        "FLAT_BASE": 5,
        "CUP_WITH_HANDLE": 5,
        "DOUBLE_BOTTOM": 5,
        "CUP_WITHOUT_HANDLE": 5,
    }


def test_validation_examples_are_frozen_before_detector_comparison():
    validation = [item for item in _labels() if item.split == CorpusSplit.VALIDATION]
    assert [(item.example_id, item.symbol, item.pattern) for item in validation] == [
        ("p8-label-0002", "NFLX", "CUP_WITH_HANDLE"),
        ("p8-label-0022", "MELI", "DOUBLE_BOTTOM"),
    ]
    assert all(item.label.value == "POSITIVE" for item in validation)


def test_source_precision_and_partial_dimensions_are_preserved():
    labels = _by_example()

    assert labels["p8-label-0001"].window_start_precision == SourcePrecision.DAY
    assert labels["p8-label-0001"].window_end is not None
    assert labels["p8-label-0001"].expected_pivot_level == 392.79

    assert labels["p8-label-0004"].window_start_precision == SourcePrecision.MONTH
    assert labels["p8-label-0004"].window_end is None
    assert labels["p8-label-0004"].expected_pivot_source_date is None
    assert labels["p8-label-0004"].expected_pivot_level == 84.26

    assert labels["p8-label-0006"].window_start_precision == SourcePrecision.MONTH
    assert labels["p8-label-0006"].expected_pivot_level == 145.86
    assert labels["p8-label-0006"].expected_depth_pct == 0.19
    assert labels["p8-label-0006"].expected_depth_tolerance_pct_points == 0.02

    assert labels["p8-label-0007"].window_start_precision == SourcePrecision.DAY
    assert labels["p8-label-0007"].window_start.isoformat() == "2024-10-15"
    assert labels["p8-label-0007"].window_end is None
    assert labels["p8-label-0007"].expected_pivot_source_date is None
    assert labels["p8-label-0007"].expected_pivot_level == 136.13

    for example_id, pivot, end in (
        ("p8-label-0008", 47.61, "2023-11-10"),
        ("p8-label-0009", 621.20, "2025-05-02"),
    ):
        item = labels[example_id]
        assert item.window_start is None
        assert item.window_start_precision is None
        assert item.window_end.isoformat() == end
        assert item.expected_pivot_level == pivot


def test_same_symbol_can_have_independent_pattern_labels_without_collision():
    labels = _by_symbol_pattern()

    nvda_db = labels[("NVDA", "DOUBLE_BOTTOM", CorpusSplit.DEVELOPMENT)]
    nvda_cwh = labels[("NVDA", "CUP_WITH_HANDLE", CorpusSplit.DEVELOPMENT)]

    assert nvda_db.example_id == "p8-label-0008"
    assert nvda_db.expected_pivot_level == 47.61
    assert nvda_cwh.example_id == "p8-label-0014"
    assert nvda_cwh.expected_pivot_level == 227.92


def test_new_corpus_examples_preserve_only_source_grounded_dimensions():
    labels = _by_example()

    assert labels["p8-label-0010"].symbol == "EXEL"
    assert labels["p8-label-0010"].window_start is None
    assert labels["p8-label-0010"].expected_pivot_level == 57.57

    assert labels["p8-label-0013"].symbol == "APH"
    assert labels["p8-label-0013"].window_start is None
    assert labels["p8-label-0013"].expected_pivot_level == 88.17

    amd = labels["p8-label-0018"]
    assert amd.window_start_precision == SourcePrecision.MONTH
    assert amd.expected_pivot_level == 35.55
    assert amd.expected_depth_pct == 0.23
    assert amd.expected_depth_tolerance_pct_points == 0.02

    assert labels["p8-label-0020"].symbol == "WMT"
    assert labels["p8-label-0020"].expected_pivot_level == 60.89
    assert labels["p8-label-0021"].symbol == "EMBJ"
    assert labels["p8-label-0021"].expected_pivot_level == 71.68


def test_ctsh_source_pivot_is_immutable_but_comparison_basis_is_split_normalized():
    ctsh = _by_example()["p8-label-0003"]

    assert ctsh.expected_pivot_level == 26.74
    assert ctsh.pivot_price_adjustment_factor == 4.0
    assert ctsh.comparison_pivot_level == 6.685
