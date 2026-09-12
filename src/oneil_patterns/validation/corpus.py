from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .labels import (
    CorpusSplit,
    LabelEvidence,
    LabelProvenance,
    LabelValue,
    validate_corpus,
)


def load_label_corpus_csv(path: str | Path) -> list[LabelEvidence]:
    """Load committed real-world labels into the frozen LabelEvidence schema."""
    items: list[LabelEvidence] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "example_id",
            "symbol",
            "pattern",
            "label",
            "window_start",
            "window_end",
            "asof_date",
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
                    window_start=date.fromisoformat(row["window_start"].strip()),
                    window_end=date.fromisoformat(row["window_end"].strip()),
                    asof_date=date.fromisoformat(row["asof_date"].strip()),
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
