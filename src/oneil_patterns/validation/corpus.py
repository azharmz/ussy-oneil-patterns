from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .labels import (
    CorpusSplit,
    LabelEvidence,
    LabelProvenance,
    LabelValue,
    SourcePrecision,
    validate_corpus,
)


def _optional_date(value: str | None) -> date | None:
    text = (value or "").strip()
    return date.fromisoformat(text) if text else None


def _optional_float(value: str | None) -> float | None:
    text = (value or "").strip()
    return float(text) if text else None


def _optional_precision(value: str | None) -> SourcePrecision | None:
    text = (value or "").strip()
    return SourcePrecision(text) if text else None


def load_label_corpus_csv(path: str | Path) -> list[LabelEvidence]:
    """Load committed real-world labels without inventing absent source dimensions."""
    items: list[LabelEvidence] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "example_id",
            "symbol",
            "pattern",
            "label",
            "window_start",
            "window_start_precision",
            "window_end",
            "asof_date",
            "expected_pivot_source_date",
            "expected_pivot_level",
            "pivot_price_adjustment_factor",
            "expected_depth_pct",
            "expected_depth_tolerance_pct_points",
            "provenance",
            "source_name",
            "source_reference",
            "annotator",
            "rationale",
            "split",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"label corpus missing columns: {sorted(missing)}")

        for row in reader:
            items.append(
                LabelEvidence(
                    example_id=row["example_id"].strip(),
                    symbol=row["symbol"].strip(),
                    pattern=row["pattern"].strip(),
                    label=LabelValue(row["label"].strip()),
                    window_start=_optional_date(row.get("window_start")),
                    window_start_precision=_optional_precision(row.get("window_start_precision")),
                    window_end=_optional_date(row.get("window_end")),
                    asof_date=date.fromisoformat(row["asof_date"].strip()),
                    expected_pivot_source_date=_optional_date(row.get("expected_pivot_source_date")),
                    expected_pivot_level=_optional_float(row.get("expected_pivot_level")),
                    pivot_price_adjustment_factor=float((row.get("pivot_price_adjustment_factor") or "1").strip() or "1"),
                    expected_depth_pct=_optional_float(row.get("expected_depth_pct")),
                    expected_depth_tolerance_pct_points=_optional_float(row.get("expected_depth_tolerance_pct_points")),
                    provenance=LabelProvenance(row["provenance"].strip()),
                    source_name=row["source_name"].strip(),
                    source_reference=row["source_reference"].strip(),
                    annotator=row["annotator"].strip() or None,
                    rationale=row["rationale"].strip() or None,
                    split=CorpusSplit(row["split"].strip()),
                    metadata={"corpus_file": Path(path).name},
                )
            )

    validate_corpus(items)
    return items
