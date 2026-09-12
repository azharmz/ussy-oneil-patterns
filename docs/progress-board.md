# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | IN PROGRESS | repo initialized; package/test/docs skeleton started |
| Parent #32 contract confirmation | COMPLETE | parent specification is frozen and #33 is authorized |
| R2 OHLCV contract inspection | NEXT | inspect actual schema, history, adjusted-price semantics |
| PIT-safe data reader | NOT STARTED | depends on R2 contract inspection |
| Landmark representation | STARTED | explicit `price_date` vs `confirmed_date` model added |
| Swing/extrema research | NOT STARTED | compare PIT-safe approaches without return tuning |
| Visual/labelled fixtures | NOT STARTED | small morphology fixture corpus required |
| Base segmentation | NOT STARTED | follows landmark foundation |
| Flat Base | NOT STARTED | first morphology phase |
| Double Bottom | NOT STARTED | first morphology phase |
| Cup family | NOT STARTED | shared cup morphology before handle classifier |
| Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| Fault/ambiguity layer | NOT STARTED | wide/loose, V-shape, malformed/incomplete etc. |
| Labelled morphology validation | NOT STARTED | precision/recall/confusion + landmark/pivot error |

## Immediate milestone

> Given a daily OHLCV series, produce stable, reproducible, PIT-safe structural landmarks that can later support multiple O'Neil morphologies.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before the shared landmark layer;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Inspect actual upstream R2 OHLCV schema and data contract.
2. Freeze normalization semantics only after inspection.
3. Implement PIT-safe reader with explicit `asof_date`.
4. Prototype multiple swing/extrema extraction methods.
5. Build labelled/visual fixtures for landmark stability comparison.
