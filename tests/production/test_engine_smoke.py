from datetime import date, timedelta

import pandas as pd
import pytest

from oneil_patterns.production.engine import analyze_security


def _wave_frame():
    anchors = [
        (100.0, 5),
        (88.0, 8),
        (99.0, 8),
        (87.0, 8),
        (101.0, 8),
        (90.0, 8),
        (103.0, 8),
        (92.0, 8),
        (105.0, 8),
    ]
    closes = []
    previous = anchors[0][0]
    for target, count in anchors:
        step = (target - previous) / count
        segment = [previous + step * (i + 1) for i in range(count)]
        closes.extend(segment)
        previous = target

    start = date(2026, 1, 2)
    return pd.DataFrame({
        "date": [start + timedelta(days=i) for i in range(len(closes))],
        "security_id": ["sec-1"] * len(closes),
        "ticker": ["TEST"] * len(closes),
        "open": closes,
        "high": [x * 1.002 for x in closes],
        "low": [x * 0.998 for x in closes],
        "close": closes,
        "adj_close": closes,
        "volume": [1000] * len(closes),
    })


def test_full_orchestrator_is_deterministic_and_core_only():
    frame = _wave_frame()
    asof = pd.to_datetime(frame["date"].iloc[-1]).date()

    first = analyze_security("sec-1", "TEST", frame, asof)
    second = analyze_security("sec-1", "TEST", frame, asof)

    assert first
    assert [r.assessment_id for r in first] == [r.assessment_id for r in second]
    assert all(r.labelled_validation_status == "P8_CONDITIONAL_PASS_FROZEN" for r in first)
    assert all(r.asof_date == asof.isoformat() for r in first)
    assert {r.pattern for r in first} <= {
        "FLAT_BASE",
        "DOUBLE_BOTTOM",
        "CUP_WITH_HANDLE",
        "CUP_WITHOUT_HANDLE",
    }
    assert all(r.base_id.startswith("base_") for r in first)
    assert all(r.lineage_id.startswith("lineage_") for r in first)
    assert all(r.candidate_semantics for r in first)


def test_orchestrator_rejects_future_rows():
    frame = _wave_frame()
    cutoff = pd.to_datetime(frame["date"].iloc[-2]).date()

    with pytest.raises(ValueError, match="future bars"):
        analyze_security("sec-1", "TEST", frame, cutoff)
