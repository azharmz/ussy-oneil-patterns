import hashlib
import io
import json

import pandas as pd
import pytest

from oneil_patterns.data.r2_ready import load_ready_asof


class _Body:
    def __init__(self, payload: bytes):
        self.payload = payload

    def read(self) -> bytes:
        return self.payload


class FakeS3:
    def __init__(self, objects: dict[str, bytes]):
        self.objects = objects

    def get_object(self, Bucket, Key):
        return {"Body": _Body(self.objects[Key])}


def _objects(frame: pd.DataFrame, *, sha_override=None):
    buf = io.BytesIO()
    frame.to_parquet(buf, engine="pyarrow", index=False)
    parquet = buf.getvalue()
    key = "production/ready/runs/test.parquet"
    manifest = {
        "schema_version": 1,
        "parquet_key": key,
        "sha256": sha_override or hashlib.sha256(parquet).hexdigest(),
        "rows": len(frame),
        "security_ids": sorted(frame["security_id"].unique().tolist()),
    }
    return {
        "production/ready/current.json": json.dumps(manifest).encode(),
        key: parquet,
    }


def _frame():
    return pd.DataFrame(
        [
            ["2026-09-08", "s1", "AAA", 10, 11, 9, 10.5, 10.2, 100],
            ["2026-09-09", "s1", "AAA", 10.5, 12, 10, 11.5, 11.1, 110],
            ["2026-09-10", "s1", "AAA", 11.5, 13, 11, 12.5, 12.0, 120],
        ],
        columns=["date", "security_id", "ticker", "open", "high", "low", "close", "adj_close", "volume"],
    )


def test_reader_enforces_asof_cutoff():
    frame = _frame()
    result = load_ready_asof(FakeS3(_objects(frame)), "bucket", "2026-09-09")
    assert result.frame["date"].max() == pd.Timestamp("2026-09-09")
    assert len(result.frame) == 2


def test_reader_preserves_raw_close_and_adj_close_separately():
    frame = _frame()
    result = load_ready_asof(FakeS3(_objects(frame)), "bucket", "2026-09-10")
    assert result.frame.loc[0, "close"] == 10.5
    assert result.frame.loc[0, "adj_close"] == 10.2


def test_reader_rejects_checksum_mismatch():
    with pytest.raises(ValueError, match="checksum"):
        load_ready_asof(FakeS3(_objects(_frame(), sha_override="0" * 64)), "bucket", "2026-09-10")


def test_reader_rejects_duplicate_security_date():
    frame = pd.concat([_frame(), _frame().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate"):
        load_ready_asof(FakeS3(_objects(frame)), "bucket", "2026-09-10")
