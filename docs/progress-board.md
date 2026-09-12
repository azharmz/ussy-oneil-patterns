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
| P2 Base Segmentation | COMPLETE | frozen as `p2-segmentation-v1`; structural sequence, stage, geometry, overlap/nesting and PIT validation green |
| P3 Flat Base | COMPLETE | frozen first-pass as `flat-base-v1`; synthetic morphology/PIT validation green; research tightness bands remain subject to P8 labelled validation |
| P4 Double Bottom | COMPLETE | frozen first-pass as `double-bottom-v1`; geometry/state/fault policy + robustness/PIT validation green |
| P5 Cup family | COMPLETE | frozen first-pass as `cup-family-v1`; shared Cup body + Handle + Cup/CWH family classification green |
| P6 Advanced patterns | IN PROGRESS | Ascending Base / Base-on-Base specification next |
| P7 Fault/ambiguity layer | NOT STARTED | cross-pattern wide/loose, V-shape, malformed/incomplete etc. |
| P8 Labelled morphology validation | NOT STARTED | authoritative/human-labelled corpus later required |
| P9 Productionization | NOT STARTED | output schema/versioning/batch runner later |

## Frozen contracts

### P1 — `p1-landmark-v1`
Documented in `docs/p1-landmark-contract-v1.md`.

### P2 — `p2-segmentation-v1`
Documented in `docs/p2-segmentation-contract-v1.md`.

### P3 — `flat-base-v1`
Documented in `docs/p3-flat-base-contract-v1.md`.

### P4 — `double-bottom-v1`
Documented in `docs/p4-double-bottom-contract-v1.md`.

### P5 — `cup-family-v1`
Documented in `docs/p5-cup-family-contract-v1.md`.

Frozen first-pass P5 semantics include:

- shared Cup body before Handle classification;
- Cup body sequence `left_rim -> trough -> right_rim`;
- Cup-without-handle minimum body duration 30 observed sessions;
- normal maximum Cup depth 33%;
- explicit roundedness descriptors and U/V/W/flat/loose synthetic fixtures;
- Handle sequence `right_rim -> handle_low -> handle_recovery`;
- Handle minimum duration 5 sessions;
- Handle must remain in upper half of Cup;
- normal Handle depth up to 12%, deeper cases ambiguous/exceptional;
- no Handle absence inference from a truncated right edge;
- family outputs `CUP_WITH_HANDLE`, `CUP_NO_HANDLE`, `CUP_HANDLE_AMBIGUOUS`, `CUP_FAMILY_INCOMPLETE`, `NOT_A_RECOGNIZED_CUP`.

Research-only roundedness/continuity/recovery bands remain subject to P8 labelled validation and cannot be tuned from returns.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P6 — Advanced patterns active objective

P6 covers the remaining advanced O'Neil base structures required by the parent contract, beginning with:

- Ascending Base
- Base-on-Base

P6 must compose frozen P1/P2/P3/P4/P5 primitives rather than inventing a parallel landmark or base engine.

### P6 checklist

- **6.1 Theory audit + morphology specification for Ascending Base** — NEXT
- 6.2 Ascending Base geometry + fixtures — NOT STARTED
- 6.3 Ascending Base detector/validation — NOT STARTED
- 6.4 Theory audit + morphology specification for Base-on-Base — NOT STARTED
- 6.5 Base-on-Base relation detector + fixtures — NOT STARTED
- 6.6 Advanced patterns first-pass freeze — NOT STARTED

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed duration assumption across pattern families;
- no direct CWH detector before shared Cup body semantics (now enforced by frozen P5 contract);
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Audit O'Neil/IBD guidance for Ascending Base structure and duration/depth semantics.
2. Translate Ascending Base into composition of confirmed P1/P2 turns rather than a new swing detector.
3. Build positive/negative/ambiguous synthetic fixtures before freezing any research-only spacing/slope bands.
4. Then repeat theory-first treatment for Base-on-Base using P2 overlap/nesting relations and frozen lower-level morphology outputs.
