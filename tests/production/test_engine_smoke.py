from datetime import date, timedelta

import pandas as pd

from oneil_patterns.production.engine import analyze_security


def _wave_frame():
    # Repeated causal >8% excursions around a broadly stable price level so P1
    # emits multiple alternating turns and downstream morphology code executes.
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
        if count == 1:
            segment = [target]
        else:
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


def test_full_orchestrator_runs_deterministically_over_multi_swing_series():
    frame = _wave_frame()
    asof = pd.to_datetime(frame["date"].iloc[-1]).date()

    first = analyze_security("sec-1", "TEST", frame, asof)
    second = analyze_security("sec-1", "TEST", frame, asof)

    assert first
    assert [r.assessment_id for r in first] == [r.assessment_id for r in second]
    assert all(r.labelled_validation_status == "P8_BLOCKED_ON_CORPUS" for r in first)
    assert all(r.asof_date == asof.isoformat() for r in first)
    assert {r.pattern for r in first} & {"FLAT_BASE", "CUP_BODY", "DOUBLE_BOTTOM", "ASCENDING_BASE"}


def test_orchestrator_rejects_future_rows():
    frame = _wave_frame()
    cutoff = pd.to_datetime(frame["date"].iloc[-2]).date()

    try:
        analyze_security("sec-1", "TEST", frame, cutoff)
    except ValueError as exc:
        assert "future bars" in str(exc)
    else:
        raise AssertionError("expected future-bar guard")
