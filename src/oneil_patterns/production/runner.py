from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
from typing import Callable, Iterable

import pandas as pd

from oneil_patterns.data.r2_ready import ReadyDataset, load_ready_asof
from .output import ProductionAssessmentRecord, ProductionRunManifest, serialize_jsonl

SecurityAnalyzer = Callable[[str, str, pd.DataFrame, date], Iterable[ProductionAssessmentRecord]]


@dataclass(frozen=True, slots=True)
class BatchRunResult:
    records: tuple[ProductionAssessmentRecord, ...]
    jsonl: str
    manifest: ProductionRunManifest


def _source_manifest_digest(manifest: dict) -> str:
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_ready_dataset(
    dataset: ReadyDataset,
    *,
    asof_date: date,
    analyze_security: SecurityAnalyzer,
) -> BatchRunResult:
    frame = dataset.frame.copy()
    if frame.empty:
        records: tuple[ProductionAssessmentRecord, ...] = ()
    else:
        dates = pd.to_datetime(frame["date"], errors="raise").dt.date
        if (dates > asof_date).any():
            raise ValueError("batch runner received bars after asof_date")

        collected: list[ProductionAssessmentRecord] = []
        for security_id, security_frame in frame.groupby("security_id", sort=True):
            ordered = security_frame.sort_values("date").reset_index(drop=True)
            tickers = ordered["ticker"].dropna().astype(str).unique().tolist()
            if len(tickers) != 1:
                raise ValueError(f"security_id {security_id} has non-unique ticker within PIT slice")
            ticker = tickers[0]
            collected.extend(analyze_security(str(security_id), ticker, ordered, asof_date))
        records = tuple(sorted(collected, key=lambda item: item.assessment_id))

    jsonl = serialize_jsonl(records)
    manifest = ProductionRunManifest.create(
        asof_date=asof_date,
        records=records,
        source_manifest_sha256=_source_manifest_digest(dataset.manifest),
    )
    return BatchRunResult(records=records, jsonl=jsonl, manifest=manifest)


def run_from_r2(
    s3,
    *,
    bucket: str,
    asof_date: date,
    analyze_security: SecurityAnalyzer,
) -> BatchRunResult:
    """Load the canonical R2 ready pointer with PIT cutoff, then run the batch.

    This wrapper intentionally delegates all source validation/checksum/cutoff
    semantics to ``load_ready_asof`` so production execution cannot bypass the
    frozen R2 consumer contract by supplying a raw parquet key directly.
    """
    dataset = load_ready_asof(s3, bucket, asof_date)
    return run_ready_dataset(dataset, asof_date=asof_date, analyze_security=analyze_security)
