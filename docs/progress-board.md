# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline established |
| Parent #32 contract confirmation | COMPLETE | parent specification is frozen and #33 is authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema and raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| P1 Structural Landmark Engine | COMPLETE | frozen as `p1-landmark-v1` |
| Landmark representation | COMPLETE | `LandmarkCandidate` with explicit `price_date` vs `confirmed_date` |
| Swing/extrema research | COMPLETE | percentage-excursion primary source + confirmed-window auxiliary corroboration |
| Visual/labelled fixtures | COMPLETE FOR P1 | V, W, flat, rounded cup, noisy loose range + expected regions |
| Landmark evaluation harness | COMPLETE FOR P1 | repaint/PIT, missed/false/date error, perturbation robustness |
| Boundary-artifact treatment | COMPLETE | explicit edge classification retained as evidence |
| Landmark fusion policy | COMPLETE | primary excursion skeleton; auxiliary corroboration only; no naive union |
| P2 Base segmentation | IN PROGRESS | P2.1 structural sequence green; P2.2 boundary stages green; P2.3 geometry green; P2.4 overlap/nesting implemented |
| Flat Base | NOT STARTED | follows P2 |
| Double Bottom | NOT STARTED | follows P2 |
| Cup family | NOT STARTED | shared cup morphology before handle classifier |
| Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| Fault/ambiguity layer | NOT STARTED | wide/loose, V-shape, malformed/incomplete etc. |
| Labelled morphology validation | NOT STARTED | authoritative/human-labelled corpus later required |
| Productionization | NOT STARTED | output schema/versioning/batch runner later |

## Frozen P1 contract

P1 is frozen under contract version `p1-landmark-v1`, documented in `docs/p1-landmark-contract-v1.md`.

Key rules:

- P1 emits only `SWING_HIGH` / `SWING_LOW` candidates;
- percentage-excursion is the primary structural-turn source;
- confirmed-window/local prominence is auxiliary evidence only;
- auxiliary extrema do not create candidates independently;
- `price_date` and `confirmed_date` remain distinct and PIT-safe;
- boundary turns remain visible with explicit boundary evidence;
- P2 and later layers may not rebuild a hidden independent swing detector;
- no trading outcome or portfolio metric was used to choose P1 semantics.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- #33 structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P2 objective

P2 converts the frozen P1 structural-turn sequence into provisional candidate base regions without assigning a pattern class yet.

Current region vocabulary:

1. structural `SWING_HIGH` = candidate start;
2. subsequent `SWING_LOW` = trough;
3. optional later confirmed `SWING_HIGH` = recovery;
4. explicit segment stage records whether only the decline is known or a recovery turn is also known.

### P2 boundary semantics

Documented in `docs/p2-boundary-semantics.md`.

- `start_date` is always the starting structural high `price_date`;
- `DECLINE_CONFIRMED`: no PIT-known recovery yet, so `end_date = trough.price_date`;
- `RECOVERY_CONFIRMED`: recovery is PIT-known, so `end_date = recovery.price_date`;
- `asof_date` is only an information cutoff and never becomes a structural boundary;
- an incomplete segment does not mechanically grow merely because the observation horizon advances.

### P2 geometry semantics

Documented in `docs/p2-geometry-features.md`.

Current morphology-neutral features:

- `duration_sessions`: inclusive start high → current structural end;
- `decline_sessions`: inclusive start high → trough;
- `recovery_sessions`: inclusive trough → recovery high, when recovery is confirmed;
- `depth_pct = (start_high - trough) / start_high`;
- `recovery_pct = (recovery_high - trough) / trough`;
- `recovery_to_start_ratio = recovery_high / start_high`;
- `recovered_depth_fraction = (recovery_high - trough) / (start_high - trough)`.

A recovered-depth fraction of `1.0` means the original decline distance has been fully recovered; values above `1.0` are allowed and remain descriptive, not breakout/trading semantics.

### P2 overlap / nesting semantics

Documented in `docs/p2-overlap-nesting.md`.

Pairwise provisional segments are classified as `DISJOINT`, `TOUCHING`, `OVERLAP`, `CONTAINS`, `WITHIN`, or `IDENTICAL` using their structural start/end dates. P2 retains all candidates and records the relation as evidence; it does not merge, rank, suppress, or choose a morphology winner.

This is deliberate because nested/overlapping structures may later be interpreted differently by Flat Base, Double Bottom, Cup family, Base-on-Base, or ambiguity/fault layers.

P2 outputs descriptive geometry, overlap/nesting evidence, and PIT-safe confirmation dates. Flat Base, Double Bottom, Cup, etc. are later morphology interpretations of these candidate regions.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before shared segmentation/morphology layers;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Verify P2.4 overlap/nesting tests in CI.
2. Implement P2.5 prefix/PIT segmentation stability validation.
3. Freeze P2 contract if the full suite remains green.
4. Start first morphology detectors only after P2 freeze.
