from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import io
import json
from typing import Any

import pandas as pd


READY_POINTER_KEY = "production/ready/current.json"
REQUIRED_COLUMNS = (
    "date",
    "security_id",
    "ticker",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
)


@dataclass(frozen=True)
class ReadyDataset:
    frame: pd.DataFrame
    manifest: dict[str, Any]


def _parse_asof(asof_date: str | date | datetime | pd.Timestamp) -> pd.Timestamp:
    value = pd.Timestamp(asof_date)
    if value.tzinfo is not None:
        value = value.tz_convert("UTC").tz_localize(None)
    return value.normalize()


def _validate_manifest(manifest: dict[str, Any]) -> str:
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported ready manifest schema_version")
    key = manifest.get("parquet_key")
    if not isinstance(key, str) or not key.startswith("production/ready/runs/") or not key.endswith(".parquet"):
        raise ValueError("Invalid ready parquet_key")
    expected_sha = manifest.get("sha256")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise ValueError("Invalid ready SHA-256")
    return key


def _normalize_and_validate(frame: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Ready dataset missing required columns: {sorted(missing)}")

    result = frame.loc[:, REQUIRED_COLUMNS].copy()
    result["date"] = pd.to_datetime(result["date"], errors="raise")
    if result["date"].dt.tz is not None:
        result["date"] = result["date"].dt.tz_convert("UTC").dt.tz_localize(None)
    result["date"] = result["date"].dt.normalize()

    if result["date"].isna().any():
        raise ValueError("Ready dataset contains null dates")
    if result.duplicated(["security_id", "date"]).any():
        raise ValueError("Ready dataset contains duplicate security/date rows")

    result = result.sort_values(["security_id", "date"]).reset_index(drop=True)
    backwards = result.groupby("security_id", sort=False)["date"].apply(lambda s: not s.is_monotonic_increasing)
    if backwards.any():
        raise ValueError("Non-monotonic per-security chronology")
    return result


def load_ready_asof(s3, bucket: str, asof_date: str | date | datetime | pd.Timestamp) -> ReadyDataset:
    """Load the current upstream ready export, validate it, then enforce `date <= asof_date`.

    The cutoff happens before callers receive the frame, making accidental access to future bars
    harder for segmentation/landmark code.
    """
    pointer = s3.get_object(Bucket=bucket, Key=READY_POINTER_KEY)["Body"].read()
    manifest = json.loads(pointer)
    parquet_key = _validate_manifest(manifest)

    body = s3.get_object(Bucket=bucket, Key=parquet_key)["Body"].read()
    actual_sha = hashlib.sha256(body).hexdigest()
    if actual_sha != manifest["sha256"]:
        raise ValueError("Ready parquet checksum mismatch")

    frame = _normalize_and_validate(pd.read_parquet(io.BytesIO(body)))

    if len(frame) != manifest.get("rows"):
        raise ValueError("Ready manifest row count mismatch")
    expected_ids = set(manifest.get("security_ids", []))
    if set(frame["security_id"]) != expected_ids:
        raise ValueError("Ready manifest security-id mismatch")

    cutoff = _parse_asof(asof_date)
    frame = frame.loc[frame["date"] <= cutoff].copy().reset_index(drop=True)
    if not frame.empty and frame["date"].max() > cutoff:
        raise AssertionError("PIT cutoff failure")

    return ReadyDataset(frame=frame, manifest=manifest)
