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
| P3 Flat Base | COMPLETE | frozen first-pass as `flat-base-v1`; research tightness bands remain subject to P8 labelled validation |
| P4 Double Bottom | COMPLETE | frozen first-pass as `double-bottom-v1` |
| P5 Cup family | COMPLETE | frozen first-pass as `cup-family-v1` |
| P6 Advanced patterns | COMPLETE | frozen first-pass as `advanced-patterns-v1`; Ascending Base + Base-on-Base green |
| P7 Fault/ambiguity layer | IN PROGRESS | normalize cross-pattern faults, ambiguity, incomplete and boundary semantics |
| P8 Labelled morphology validation | NOT STARTED | authoritative/human-labelled corpus later required |
| P9 Productionization | NOT STARTED | output schema/versioning/batch runner later |

## Frozen contracts

- P1 `p1-landmark-v1` — `docs/p1-landmark-contract-v1.md`
- P2 `p2-segmentation-v1` — `docs/p2-segmentation-contract-v1.md`
- P3 `flat-base-v1` — `docs/p3-flat-base-contract-v1.md`
- P4 `double-bottom-v1` — `docs/p4-double-bottom-contract-v1.md`
- P5 `cup-family-v1` — `docs/p5-cup-family-contract-v1.md`
- P6 `advanced-patterns-v1` — `docs/p6-advanced-patterns-contract-v1.md`

## P6 frozen summary

### Ascending Base

- three confirmed pullbacks;
- successively higher troughs and peaks;
- 45–80 observed-session first-pass duration neighborhood;
- pullback-depth consistency is research-only;
- synthetic morphology and PIT validation green.

### Base-on-Base

- composes two already-recognized base summaries;
- second base should form entirely or mostly above the first;
- research-only operationalization uses second-base close fraction above first-base high: >=0.75 recognized, <0.50 rejected, middle band ambiguous;
- future rows outside component windows do not change the relation result.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P7 — Fault / ambiguity layer active objective

P7 does not invent new pattern detectors. It normalizes the fault/evidence vocabulary already emitted by P3–P6 so downstream consumers can distinguish:

- hard rejection vs ambiguity;
- incomplete/right-edge context;
- boundary contamination;
- wide/loose morphology;
- V-shape / fragmented bottom;
- excessive depth/duration faults;
- component/relation faults;
- research-only vs theory-grounded rules.

### P7 checklist

- **7.1 Cross-pattern fault taxonomy and severity model** — NEXT
- 7.2 Normalized assessment envelope — NOT STARTED
- 7.3 Mapping adapters for Flat/DB/Cup/Ascending/Base-on-Base — NOT STARTED
- 7.4 Contradiction and multi-pattern ambiguity policy — NOT STARTED
- 7.5 P7 validation + freeze — NOT STARTED

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no pattern family may silently reinterpret another detector's research-only band as a theory rule;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Define shared fault severity and provenance (`THEORY`, `RESEARCH`, `CONTEXT`).
2. Define one normalized assessment envelope preserving native pattern state/faults.
3. Add adapters for all frozen morphology contracts.
4. Define conflict policy when more than one pattern is simultaneously plausible.
