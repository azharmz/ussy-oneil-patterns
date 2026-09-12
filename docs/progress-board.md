# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | IN PROGRESS | repo initialized; package/test/docs skeleton established |
| Parent #32 contract confirmation | COMPLETE | parent specification is frozen and #33 is authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema and raw-vs-adjusted semantics documented |
| PIT-safe data reader | IMPLEMENTED / UNIT-TESTED IN REPO | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| Landmark representation | STARTED | explicit `price_date` vs `confirmed_date` model added |
| Swing/extrema research | NEXT | compare PIT-safe approaches without return tuning |
| Visual/labelled fixtures | NOT STARTED | small morphology fixture corpus required |
| Base segmentation | NOT STARTED | follows landmark foundation |
| Flat Base | NOT STARTED | first morphology phase |
| Double Bottom | NOT STARTED | first morphology phase |
| Cup family | NOT STARTED | shared cup morphology before handle classifier |
| Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| Fault/ambiguity layer | NOT STARTED | wide/loose, V-shape, malformed/incomplete etc. |
| Labelled morphology validation | NOT STARTED | precision/recall/confusion + landmark/pivot error |

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- #33 structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## Immediate milestone

> Given a daily OHLCV series, produce stable, reproducible, PIT-safe structural landmarks that can later support multiple O'Neil morphologies.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before the shared landmark layer;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Implement candidate PIT-safe swing/extrema extractors behind one common interface.
2. Start with simple percentage-excursion and prominence-style candidates.
3. Preserve both `price_date` and `confirmed_date` for every emitted landmark.
4. Build deterministic synthetic fixtures for noise, V-shape, W-shape and shallow sideways action.
5. Compare stability and morphology-label agreement only; do not inspect downstream returns.
