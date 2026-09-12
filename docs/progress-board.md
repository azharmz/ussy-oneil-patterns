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
| P5 Cup family | IN PROGRESS | P5.1 theory audit complete; shared cup geometry formalization next |
| P6 Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
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

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P5 — Cup family active objective

Draft specification: `docs/p5-cup-family-spec-draft.md`.

Shared Cup morphology must be frozen before handle classification. P5 must distinguish a rounded U-like cup from V-shape, W/Double Bottom, Flat Base and wide/loose structures using existing P1/P2 primitives.

### P5.1 audited theory guidance

Official IBD material supports:

- Cup with Handle minimum base duration: **7 weeks**;
- typical cup depth: approximately **12% to 33%**;
- cup visual character: **U-shaped / teacup-like**, not a sharp V;
- Cup without Handle minimum duration: **6 weeks**;
- Cup without Handle normal maximum depth: **33%**;
- handle minimum duration: **5 trading sessions / 1 week**;
- proper handle forms in the **upper half of the cup**;
- normal handle depth commonly **8% to 12%**.

No canonical numeric roundedness threshold was found. Roundedness/V-shape discrimination therefore remains morphology research and must be validated from labelled shape evidence, never returns.

### P5 checklist

- **5.1 Theory audit: cup duration/depth/roundedness + handle guidance** — COMPLETE
- **5.2 Shared cup geometry formalization** — NEXT
- 5.3 U/V/W/flat/loose fixture corpus — NOT STARTED
- 5.4 Cup body detector/state/fault policy — NOT STARTED
- 5.5 Cup body morphology/PIT validation — NOT STARTED
- 5.6 Handle segmentation + family classification — NOT STARTED
- 5.7 Cup family first-pass freeze — NOT STARTED

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed duration assumption across pattern families;
- no direct CWH detector before shared Cup body semantics;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. P5.2 formalize shared Cup body geometry over existing P1/P2 structure.
2. Compute duration, depth, decline/recovery timing, rim relation and bottom-region descriptors.
3. Build synthetic U/V/W/flat/loose fixtures before roundedness thresholding.
4. Freeze shared Cup body semantics before handle classification.
