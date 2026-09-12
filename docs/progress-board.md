# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline established |
| Parent #32 contract confirmation | COMPLETE | parent specification frozen and #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema, raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| P1 Structural Landmark Engine | COMPLETE | frozen as `p1-landmark-v1` |
| P2 Base Segmentation | COMPLETE | frozen as `p2-segmentation-v1` |
| P3 Flat Base | COMPLETE | frozen first-pass as `flat-base-v1`; research tightness bands remain subject to P8 labelled validation |
| P4 Double Bottom | COMPLETE | frozen first-pass as `double-bottom-v1` |
| P5 Cup family | COMPLETE | frozen first-pass as `cup-family-v1` |
| P6 Advanced patterns | COMPLETE | frozen first-pass as `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | frozen as `fault-ambiguity-v1` |
| P8 Labelled morphology validation | BLOCKED_ON_CORPUS | schema/metrics/anti-leakage infrastructure green; no independent labelled corpus found |
| P9 Productionization | IN PROGRESS | first-pass research-labelled output contract + batch runner next |

## Frozen contracts

- P1 `p1-landmark-v1` — `docs/p1-landmark-contract-v1.md`
- P2 `p2-segmentation-v1` — `docs/p2-segmentation-contract-v1.md`
- P3 `flat-base-v1` — `docs/p3-flat-base-contract-v1.md`
- P4 `double-bottom-v1` — `docs/p4-double-bottom-contract-v1.md`
- P5 `cup-family-v1` — `docs/p5-cup-family-contract-v1.md`
- P6 `advanced-patterns-v1` — `docs/p6-advanced-patterns-contract-v1.md`
- P7 `fault-ambiguity-v1` — `docs/p7-fault-ambiguity-contract-v1.md`

## P8 labelled validation status

Detailed status: `docs/p8-labelled-validation-status.md`.

Complete:

- 8.1 label/evidence/provenance schema;
- 8.2 corpus split/leakage contract;
- 8.3 evaluation metrics + disagreement ids;
- repository audit for existing independent labels.

Blocked:

- 8.4 run frozen detectors against real labelled corpus;
- 8.5 morphology-only threshold verdicts;
- 8.6 final labelled-validation freeze.

Reason: no independent authoritative/human-labelled corpus currently exists in the repository. Synthetic fixtures are intentionally ineligible as P8 evidence.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P9 — Productionization active objective

P9 may productionize the current engine only as **first-pass / research-labelled** while P8 is blocked. Outputs must make validation debt impossible to hide.

### P9 checklist

- **9.1 Versioned output record/schema** — NEXT
- 9.2 Validation-status + contract manifest in every run — NOT STARTED
- 9.3 Batch runner over PIT-safe R2 reader — NOT STARTED
- 9.4 Deterministic serialization / stable ids — NOT STARTED
- 9.5 End-to-end smoke tests — NOT STARTED
- 9.6 Productionization contract + #33 final verdict — NOT STARTED

## P9 output requirements

Every emitted pattern assessment must retain at minimum:

- symbol/security id;
- `asof_date`;
- pattern/family;
- normalized status and native state;
- structural start/end and confirmation date when available;
- normalized faults with severity/provenance;
- detector/source contract versions;
- engine/output schema version;
- explicit labelled-validation state (`P8_BLOCKED_ON_CORPUS` until resolved).

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no fabricated authoritative labels;
- no production output may imply research-only thresholds are P8-validated;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Define stable production record + deterministic id semantics.
2. Define run manifest with contract versions and P8 validation status.
3. Wire a batch/serialization layer without changing detector semantics.
4. Add end-to-end smoke tests against synthetic/regression data and preserve P8 blocker in output metadata.
