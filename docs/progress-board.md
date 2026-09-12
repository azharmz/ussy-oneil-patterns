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
| P2 Base segmentation | IN PROGRESS | segment model bootstrapped; structural high → trough → recovery logic next |
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

The first region vocabulary is:

1. structural high / candidate base start;
2. subsequent decline / trough;
3. recovery high if confirmed;
4. provisional base end / open-ended status as appropriate.

P2 outputs descriptive geometry such as duration, depth, recovery, overlap/nesting evidence, and PIT-safe confirmation dates. Flat Base, Double Bottom, Cup, etc. are later morphology interpretations of these candidate regions.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before shared segmentation/morphology layers;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Implement P2 structural sequence segmentation from confirmed `LandmarkCandidate` objects.
2. Define candidate start/end and incomplete/open-base semantics.
3. Compute duration, depth, and recovery features.
4. Add nested/overlapping candidate handling.
5. Validate P2 prefix/PIT stability before starting Flat Base / Double Bottom detectors.
