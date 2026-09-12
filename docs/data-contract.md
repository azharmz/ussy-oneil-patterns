# Upstream R2 OHLCV Data Contract

Status: frozen for #33 implementation unless upstream `ussy-data` contract changes.

## Source of truth

Upstream repository: `azharmz/ussy-data`.

Consumer pointer:

```text
production/ready/current.json
```

Do not hardcode a run parquet UUID. The pointer resolves the immutable parquet key and supplies checksum / row / security-id integrity metadata.

## Ready dataset schema

Required columns:

```text
date
security_id
ticker
open
high
low
close
adj_close
volume
```

The upstream exporter validates unique `(security_id, date)` rows, minimum/maximum rolling history constraints, and OHLCV QC before publishing the ready dataset.

## Price semantics

Yahoo source history is downloaded upstream with:

```python
auto_adjust=False
```

Therefore:

- `open`, `high`, `low`, `close` are the unadjusted/raw OHLC fields provided by the upstream source;
- `adj_close` is persisted separately;
- #33 must not silently replace raw OHLC with an adjusted series;
- canonical O'Neil morphology / structural pivot geometry uses raw OHLC unless a future specification version explicitly changes this rule;
- `adj_close` may be retained for audit/context but is not a substitute for raw structural prices.

This distinction is important because pattern geometry and canonical pivot levels represent actual historical quoted price levels.

## PIT semantics

For an evaluation as of session `T`:

```text
usable rows satisfy date <= T
```

No feature, landmark or classifier may inspect rows after `T`.

The ready dataset itself is a current rolling export. A historical as-of evaluation must enforce the cutoff in the #33 reader before any downstream transformation.

## Current upstream production policy

The ready export policy is:

```text
active_compliant_and_ready; no independent market-freshness guarantee
```

Upstream minimum-ready history is currently 250 bars and the rolling target is 300 bars. These are upstream consumption constraints, not O'Neil base-duration rules.

## Integrity checks required in #33

Reader must reject:

- unsupported manifest schema version;
- parquet paths outside `production/ready/runs/`;
- SHA-256 mismatch;
- missing required columns;
- duplicate `(security_id, date)` rows;
- malformed/non-monotonic per-security chronology after normalization;
- any request whose `asof_date` would allow future rows through.

## Boundary

`ussy-data` owns source ingestion, provider repair, QC, universe readiness and R2 publication.

`ussy-oneil-patterns` owns only safe consumption and pattern research. It must not repair source bars or reinterpret upstream data quality policy.
