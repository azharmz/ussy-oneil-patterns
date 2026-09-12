# P8 canonical live DEVELOPMENT execution v0

Date: 2026-09-13

Status: IMPLEMENTED ON DEVELOPMENT BRANCH

## Scope

Run the canonical #33 detector-to-validation path on authoritative `DEVELOPMENT` labels only.

Current examples:

- SNPS — Flat Base;
- CTSH — Cup-with-Handle;
- FOUR — Cup-with-Handle;
- SEI — Double Bottom;
- AMZN — Cup-without-Handle.

NFLX remains `VALIDATION` and is excluded from detector comparison.

## Data routing

Frozen priority remains:

`R2 -> Yahoo/yfinance -> Tiingo`

Fallback is permitted only when a provider raises explicit `SourceUnavailable` for genuine coverage absence. Missing credentials, authentication failure, parse failure, schema failure, or QC failure are terminal and must not silently select a lower-priority source.

R2 ticker resolution uses the current universe membership only to determine R2 availability/security_id. Absence from that membership is `SourceUnavailable`; it does not change the frozen research universe or authoritative pattern label.

## Context

Each DEVELOPMENT case receives 240 calendar days of pre-label warm-up and no bars after its authoritative `asof_date`.

The warm-up is detector context only. It is not a source-label boundary and is not scored as one.

## Evaluation

The run composes:

1. canonical P1-P5 prediction adapter;
2. canonical pattern pivot adapter v0.2;
3. canonical source-dimension evaluator;
4. source precision and corporate-action comparison semantics frozen in the migrated corpus.

`MATCH` continues to mean agreement on source-published dimensions only. Native detector status/ambiguity is reported independently.

## CI/workflow policy

The existing single `tests` workflow remains the only GitHub Actions workflow definition. A `workflow_dispatch` job is added to the same workflow for live P8 DEVELOPMENT execution, preserving the repository's intentionally clean Actions sidebar.

## Guardrails

- no VALIDATION execution;
- no return/CAGR/PF/FWD1/breakout-performance input;
- no label-driven detector changes;
- no fallback on operational/QC errors;
- source prices remain immutable;
- results are evidence for later `KEEP / REVISE / UNRESOLVED`, not automatic threshold changes.
