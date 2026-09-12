from datetime import date

import pandas as pd

from oneil_patterns.data.r2_ready import ReadyDataset
from oneil_patterns.production import runner


def test_run_from_r2_delegates_to_canonical_loader(monkeypatch):
    calls = {}
    dataset = ReadyDataset(
        frame=pd.DataFrame(columns=[
            "date", "security_id", "ticker", "open", "high", "low", "close", "adj_close", "volume"
        ]),
        manifest={"schema_version": 1, "sha256": "a" * 64},
    )

    def fake_loader(s3, bucket, asof_date):
        calls["s3"] = s3
        calls["bucket"] = bucket
        calls["asof_date"] = asof_date
        return dataset

    monkeypatch.setattr(runner, "load_ready_asof", fake_loader)
    marker_s3 = object()
    result = runner.run_from_r2(
        marker_s3,
        bucket="ussy-data",
        asof_date=date(2026, 9, 12),
        analyze_security=lambda *_: (),
    )

    assert calls == {
        "s3": marker_s3,
        "bucket": "ussy-data",
        "asof_date": date(2026, 9, 12),
    }
    assert result.records == ()
    assert result.manifest.asof_date == "2026-09-12"
    assert result.manifest.labelled_validation_status == "P8_BLOCKED_ON_CORPUS"
