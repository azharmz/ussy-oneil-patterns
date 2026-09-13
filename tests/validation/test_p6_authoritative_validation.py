from datetime import date

import pandas as pd
import pytest

from oneil_patterns.validation.advanced_predictions import (
    ADVANCED_PREDICTION_ADAPTER_VERSION,
    _is_recognized_core,
    extract_advanced_morphology_predictions,
)
from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.labels import CorpusSplit
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction


def test_p6_corpus_has_balanced_development_and_locked_validation():
    labels = load_label_corpus_csv("data/p6/labels_v0.csv")
    development = [item for item in labels if item.split == CorpusSplit.DEVELOPMENT]
    validation = [item for item in labels if item.split == CorpusSplit.VALIDATION]

    assert len(development) == 10
    assert len(validation) == 2
    assert sum(item.pattern == "ASCENDING_BASE" for item in development) == 5
    assert sum(item.pattern == "BASE_ON_BASE" for item in development) == 5
    assert sum(item.pattern == "ASCENDING_BASE" for item in validation) == 1
    assert sum(item.pattern == "BASE_ON_BASE" for item in validation) == 1
    assert {item.example_id for item in validation} == {"p6-label-0011", "p6-label-0012"}


def test_advanced_extractor_rejects_future_bars_before_morphology():
    frame = pd.DataFrame(
        {
            "date": [date(2026, 1, 2), date(2026, 1, 5)],
            "open": [10.0, 10.5],
            "high": [10.5, 11.0],
            "low": [9.5, 10.0],
            "close": [10.2, 10.8],
            "volume": [1000, 1100],
        }
    )
    with pytest.raises(ValueError, match="future bars"):
        extract_advanced_morphology_predictions(frame, asof_date=date(2026, 1, 2))


def test_advanced_extractor_empty_input_is_empty():
    assert extract_advanced_morphology_predictions(pd.DataFrame(), asof_date=date(2026, 1, 2)) == []


def test_base_on_base_components_only_consume_recognized_core_predictions():
    recognized = MorphologyPrediction(
        candidate_id="a",
        pattern="FLAT_BASE",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 2, 1),
        detector_status="FLAT_BASE_RECOGNIZED",
    )
    ambiguous = MorphologyPrediction(
        candidate_id="b",
        pattern="FLAT_BASE",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 2, 1),
        detector_status="FLAT_BASE_AMBIGUOUS",
    )
    advanced = MorphologyPrediction(
        candidate_id="c",
        pattern="ASCENDING_BASE",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 2, 1),
        detector_status="ASCENDING_BASE_RECOGNIZED",
    )

    assert _is_recognized_core(recognized) is True
    assert _is_recognized_core(ambiguous) is False
    assert _is_recognized_core(advanced) is False
    assert ADVANCED_PREDICTION_ADAPTER_VERSION == "p6-advanced-prediction-adapter-v0.1"
