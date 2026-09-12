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
| P3 Flat Base | IN PROGRESS | morphology research/specification is now the active workstream |
| P4 Double Bottom | NOT STARTED | follows Flat Base first pass |
| P5 Cup family | NOT STARTED | shared cup morphology before handle classifier |
| P6 Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| P7 Fault/ambiguity layer | NOT STARTED | wide/loose, V-shape, malformed/incomplete etc. |
| P8 Labelled morphology validation | NOT STARTED | authoritative/human-labelled corpus later required |
| P9 Productionization | NOT STARTED | output schema/versioning/batch runner later |

## Frozen contracts

### P1 — `p1-landmark-v1`

Documented in `docs/p1-landmark-contract-v1.md`.

P1 emits generic PIT-safe `SWING_HIGH` / `SWING_LOW` candidates only. Percentage-excursion is the primary causal source; confirmed-window/local-prominence is auxiliary corroboration. `price_date` and `confirmed_date` remain distinct.

### P2 — `p2-segmentation-v1`

Documented in `docs/p2-segmentation-contract-v1.md`.

P2 converts confirmed P1 turns into provisional morphology-neutral `BaseSegmentCandidate` regions. Frozen semantics include:

- `DECLINE_CONFIRMED` and `RECOVERY_CONFIRMED` stages;
- structural start/end dates that never substitute `asof_date`;
- inclusive duration/decline/recovery session counts;
- depth and recovery geometry;
- pairwise `DISJOINT`, `TOUCHING`, `OVERLAP`, `CONTAINS`, `WITHIN`, `IDENTICAL` relations;
- preservation of all overlapping/nested candidates rather than premature suppression;
- prefix/PIT stability: future data cannot rewrite an already-known segment except for a legitimate stage upgrade once a recovery becomes confirmed.

P2 does not assign Flat Base, Double Bottom, Cup, CWH, pivot, breakout, entry, or performance semantics.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P3 — Flat Base active objective

P3 is the first pattern-specific morphology layer. It must interpret frozen P1/P2 structure rather than rebuilding extrema or segmentation.

The first task is to define a quantitative Flat Base morphology contract from structural geometry and within-region price behaviour. Thresholds must be justified by O'Neil/theory-faithful evidence and morphology validation, not return optimization.

Candidate dimensions to formalize include:

- duration / compactness;
- maximum depth;
- tightness / range compression;
- number and severity of internal structural turns;
- relationship of recovery high to starting high;
- wide-and-loose rejection evidence;
- boundary / incomplete status;
- overlap/nesting context.

No breakout or entry logic belongs in this phase.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before shared morphology layers;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. P3.1 define a theory-faithful quantitative Flat Base morphology specification.
2. Encode positive, negative and ambiguous synthetic Flat Base fixtures.
3. Implement the first Flat Base morphology classifier against frozen P2 segments.
4. Validate morphology/PIT behavior before moving to Double Bottom.
