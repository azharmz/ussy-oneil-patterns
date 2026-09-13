#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
from datetime import timedelta
import json
from pathlib import Path

from oneil_patterns.validation.advanced_predictions import (
    ADVANCED_PREDICTION_ADAPTER_VERSION,
    extract_advanced_morphology_predictions,
)
from oneil_patterns.validation.candidate_identity import (
    CANDIDATE_IDENTITY_AUDIT_VERSION,
    audit_candidate_identities,
)
from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.development_sources import route_development_ohlcv
from oneil_patterns.validation.labels import CorpusSplit
from oneil_patterns.validation.source_dimension_eval import (
    EVALUATOR_VERSION,
    evaluate_positive_development_label,
)

ROOT = Path(__file__).resolve().parents[1]
FREEZE_RECORD_COMMIT = "d47177e5ae4d979f367537a109c4338c7ea71345"
FREEZE_EVIDENCE_COMMIT = "ba13844145095a4bb40f75d9ce477fd61d3aad50"
FREEZE_WORKFLOW_RUN = 34748254127
FREEZE_ARTIFACT_ID = 10315076061
FREEZE_ARTIFACT_DIGEST = "sha256:332f7fc9aab753280b386491cb59d3a48ad4f258374c7e40b804309eb93425e8"
EXPECTED_VERSIONS = {
    "prediction_adapter": "p6-advanced-prediction-adapter-v0.3",
    "evaluator": "p8-source-dimension-eval-v0.5",
    "candidate_identity_audit": "p8-candidate-identity-audit-v0.4",
}
EXPECTED_VALIDATION = {
    "p6-label-0011": "ASCENDING_BASE",
    "p6-label-0012": "BASE_ON_BASE",
}
CONTEXT_CALENDAR_DAYS = 320
BOUNDARY_TOLERANCE_DAYS = 10
PIVOT_DATE_TOLERANCE_DAYS = 3
PIVOT_PRICE_TOLERANCE_PCT = 0.01


def _assert_frozen_versions() -> None:
    actual = {
        "prediction_adapter": ADVANCED_PREDICTION_ADAPTER_VERSION,
        "evaluator": EVALUATOR_VERSION,
        "candidate_identity_audit": CANDIDATE_IDENTITY_AUDIT_VERSION,
    }
    if actual != EXPECTED_VERSIONS:
        raise RuntimeError(f"frozen P6 versions changed before VALIDATION: {actual!r}")


def _run_one(label) -> dict:
    anchor = label.window_start or label.asof_date
    context_start = anchor - timedelta(days=CONTEXT_CALENDAR_DAYS)
    routed = route_development_ohlcv(label.symbol, context_start, label.asof_date)
    predictions = extract_advanced_morphology_predictions(routed.frame, asof_date=label.asof_date)

    # The source-dimension evaluator is intentionally DEVELOPMENT-locked to prevent
    # accidental validation use during tuning. After freeze only the split field is
    # changed on an in-memory copy; every authoritative source dimension is identical.
    scoring_label = replace(label, split=CorpusSplit.DEVELOPMENT)
    agreement = evaluate_positive_development_label(
        scoring_label,
        predictions,
        boundary_tolerance_days=BOUNDARY_TOLERANCE_DAYS,
        pivot_date_tolerance_days=PIVOT_DATE_TOLERANCE_DAYS,
        pivot_price_tolerance_pct=PIVOT_PRICE_TOLERANCE_PCT,
    )
    same_pattern = [item for item in predictions if item.pattern == label.pattern]
    identity_audit = audit_candidate_identities(same_pattern)
    return {
        "example_id": label.example_id,
        "symbol": label.symbol,
        "pattern": label.pattern,
        "original_split": label.split.value,
        "context_start": context_start.isoformat(),
        "asof_date": label.asof_date.isoformat(),
        "selected_source": routed.source.value,
        "fallback_reason": routed.fallback_reason,
        "input_row_count": len(routed.frame),
        "prediction_count": len(predictions),
        "prediction_pattern_counts": dict(sorted(Counter(item.pattern for item in predictions).items())),
        "same_pattern_prediction_count": len(same_pattern),
        "agreement": agreement.to_dict(),
        "same_pattern_predictions": [asdict(item) for item in same_pattern],
        "candidate_identity_state_counts": dict(
            sorted(Counter(item.identity_state for item in identity_audit).items())
        ),
        "candidate_identities": [item.to_dict() for item in identity_audit],
    }


def main() -> int:
    _assert_frozen_versions()
    labels = load_label_corpus_csv(ROOT / "data/p6/labels_v0.csv")
    validation = [item for item in labels if item.split == CorpusSplit.VALIDATION]
    actual = {item.example_id: item.pattern for item in validation}
    if actual != EXPECTED_VALIDATION:
        raise RuntimeError(f"frozen P6 VALIDATION identities changed: {actual!r}")

    results = [_run_one(item) for item in sorted(validation, key=lambda item: item.example_id)]
    identity_counts = Counter()
    for item in results:
        identity_counts.update(item["candidate_identity_state_counts"])

    report = {
        "stage": "P6",
        "scope": "ONE_SHOT_FROZEN_VALIDATION",
        "freeze_record_commit": FREEZE_RECORD_COMMIT,
        "freeze_evidence_commit": FREEZE_EVIDENCE_COMMIT,
        "freeze_workflow_run": FREEZE_WORKFLOW_RUN,
        "freeze_artifact_id": FREEZE_ARTIFACT_ID,
        "freeze_artifact_digest": FREEZE_ARTIFACT_DIGEST,
        "prediction_adapter_version": ADVANCED_PREDICTION_ADAPTER_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "candidate_identity_audit_version": CANDIDATE_IDENTITY_AUDIT_VERSION,
        "context_calendar_days": CONTEXT_CALENDAR_DAYS,
        "boundary_tolerance_days": BOUNDARY_TOLERANCE_DAYS,
        "pivot_date_tolerance_days": PIVOT_DATE_TOLERANCE_DAYS,
        "pivot_price_tolerance_pct": PIVOT_PRICE_TOLERANCE_PCT,
        "result_count": len(results),
        "agreement_counts": dict(sorted(Counter(item["agreement"]["agreement_state"] for item in results).items())),
        "candidate_resolution_counts": dict(sorted(Counter(item["agreement"]["candidate_resolution_state"] for item in results).items())),
        "matched_detector_status_counts": dict(sorted(Counter(item["agreement"].get("matched_detector_status") or "NO_MATCH" for item in results).items())),
        "candidate_identity_state_counts": dict(sorted(identity_counts.items())),
        "candidate_identity_status_conflict_count": identity_counts.get("STATUS_CONFLICT", 0),
        "results": results,
        "guardrails": [
            "This is the single frozen P6 VALIDATION execution after DEVELOPMENT freeze.",
            "No frozen P6 adapter/evaluator/source-routing semantics may be changed in response to this result.",
            "Only the split field is changed on an in-memory scoring copy; authoritative source dimensions remain identical.",
            "Detector state never ranks source agreement.",
            "No return, CAGR, PF, FWD1, breakout outcome, entry optimization, or portfolio outcome is used.",
            "P3/P4/P5/P8 core remains immutable and is not tuned from P6 VALIDATION.",
        ],
    }

    output = ROOT / "results/p6-frozen-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
