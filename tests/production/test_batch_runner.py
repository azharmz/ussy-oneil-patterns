from datetime import date

import pandas as pd
import pytest

from oneil_patterns.data.r2_ready import ReadyDataset
from oneil_patterns.morphology.faults import normalize_assessment
from oneil_patterns.production.output import ProductionAssessmentRecord
from oneil_patterns.production.runner import run_ready_dataset


def _dataset(*, future=False):
    rows = [
        {"date": "2026-09-10", "security_id": "b", "ticker": "BBB", "open": 1, "high": 2, "low": 1, "close": 2, "adj_close": 2, "volume": 10},
        {"date": "2026-09-09", "security_id": "a", "ticker": "AAA", "open": 1, "high": 2, "low": 1, "close": 2, "adj_close": 2, "volume": 10},
        {"date": "2026-09-10", "security_id": "a", "ticker": "AAA", "open": 2, "high": 3, "low": 2, "close": 3, "adj_close": 3, "volume": 11},
    ]
    if future:
        rows.append({"date": "2026-09-13", "security_id": "a", "ticker": "AAA", "open": 3, "high": 4, "low": 3, "close": 4, "adj_close": 4, "volume": 12})
    return ReadyDataset(frame=pd.DataFrame(rows), manifest={"schema_version": 1, "sha256": "a" * 64})


def _analyzer(security_id, ticker, frame, asof_date):
    assert frame["date"].is_monotonic_increasing
    envelope = normalize_assessment(
        pattern="FLAT_BASE",
        native_state="FLAT_BASE_RECOGNIZED",
        native_faults=(),
        contract_version="flat-base-v1",
    )
    yield ProductionAssessmentRecord.from_envelope(
        security_id=security_id,
        ticker=ticker,
        asof_date=asof_date,
        envelope=envelope,
    )


def test_batch_runner_orders_securities_and_serialization_deterministically():
    result = run_ready_dataset(_dataset(), asof_date=date(2026, 9, 12), analyze_security=_analyzer)
    assert len(result.records) == 2
    assert result.manifest.record_count == 2
    assert result.manifest.labelled_validation_status == "P8_BLOCKED_ON_CORPUS"
    assert result.jsonl.count("\n") == 2
    assert result.records == tuple(sorted(result.records, key=lambda r: r.assessment_id))


def test_batch_runner_rejects_any_future_bar_even_if_reader_should_have_filtered_it():
    with pytest.raises(ValueError, match="after asof_date"):
        run_ready_dataset(_dataset(future=True), asof_date=date(2026, 9, 12), analyze_security=_analyzer)


def test_batch_runner_rejects_ticker_change_inside_security_id():
    dataset = _dataset()
    dataset.frame.loc[dataset.frame["security_id"] == "a", "ticker"] = ["AAA", "AAX"]
    with pytest.raises(ValueError, match="non-unique ticker"):
        run_ready_dataset(dataset, asof_date=date(2026, 9, 12), analyze_security=_analyzer)
