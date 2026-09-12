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
| P4 Double Bottom | IN PROGRESS | morphology specification draft opened; theory audit is next |
| P5 Cup family | NOT STARTED | shared cup morphology before handle classifier |
| P6 Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| P7 Fault/ambiguity layer | NOT STARTED | cross-pattern wide/loose, V-shape, malformed/incomplete etc. |
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

### P3 — `flat-base-v1`

Documented in `docs/p3-flat-base-contract-v1.md`.

The first-pass Flat Base contract freezes:

- minimum duration: 25 trading sessions;
- maximum depth: 15%;
- morphology states `RECOGNIZED`, `REJECTED`, `AMBIGUOUS`, `NOT_EVALUABLE`;
- faults `TOO_SHORT`, `TOO_DEEP`, `WIDE_LOOSE`, `BOUNDARY_CONTEXT`;
- structural-window/PIT rule: only bars inside the frozen P2 segment may affect the assessment;
- research-only tightness bands, explicitly not claimed as official O'Neil/IBD numeric rules and not tunable from returns.

Synthetic first-pass validation is green for clear positive/negative/ambiguous fixtures, future-row invariance, and small +/-0.1% perturbation stability on clear examples. P8 remains responsible for authoritative/human-labelled validation of the research tightness bands.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P4 — Double Bottom active objective

P4 is now the active morphology workstream. Draft specification: `docs/p4-double-bottom-spec-draft.md`.

Target structural sequence:

`left-side high -> trough 1 -> middle peak -> trough 2 -> recovery/right-side high`

P4 must interpret existing P1/P2 turns rather than build a separate swing detector.

Geometry dimensions awaiting theory audit and quantification:

- overall duration;
- overall depth;
- two-trough temporal distinctness;
- middle-peak prominence/rebound;
- second-trough relation to first trough;
- right-side recovery completeness;
- asymmetry, wide/loose, boundary and malformed/incomplete evidence.

No numerical Double Bottom threshold is frozen yet.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before shared morphology layers;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. P4.1 audit O'Neil/IBD Double Bottom guidance for duration, depth, middle peak and second-trough semantics.
2. Translate only supported guidance into measurable descriptors/threshold candidates.
3. Build positive/negative/ambiguous synthetic W fixtures.
4. Implement a PIT-safe Double Bottom detector only after the morphology contract is explicit.
