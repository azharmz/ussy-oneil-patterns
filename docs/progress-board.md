# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | IN PROGRESS | repo initialized; package/test/docs skeleton established |
| Parent #32 contract confirmation | COMPLETE | parent specification is frozen and #33 is authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema and raw-vs-adjusted semantics documented |
| PIT-safe data reader | IMPLEMENTED / UNIT-TESTED IN REPO | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| Landmark representation | IMPLEMENTED / EVOLVING | explicit `price_date` vs `confirmed_date`; generic `SWING_HIGH/SWING_LOW` added |
| Swing/extrema research | IN PROGRESS | percentage-excursion and confirmed-window candidates implemented |
| Visual/labelled fixtures | STARTED | deterministic synthetic swing fixture added; richer morphology corpus still required |
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

## P1 swing/extrema candidates

### Candidate A — percentage excursion

- causal alternating swing detector;
- confirms a peak only after a sufficient decline and a trough only after a sufficient advance;
- stores original extremum `price_date` and later `confirmed_date`;
- parameters are research parameters for morphology/stability only, not return optimization.

### Candidate B — confirmed window

- local high/low candidate is emitted only after a fixed number of later sessions have elapsed;
- confirmation date is the end of the required future-confirmation window, never backdated to the extremum date;
- includes a minimum local excursion/prominence requirement to suppress trivial noise.

### PIT tests now encoded

- `confirmed_date >= price_date`;
- percentage-excursion confirmation is not backdated;
- confirmed-window extrema carry the later confirmation date;
- prefix-stability check: already-confirmed landmarks do not change merely because later bars are appended;
- no landmark from a truncated prefix may claim a confirmation date beyond that prefix.

A GitHub Actions pytest workflow is now present so these invariants can be checked on every push/PR.

## Immediate milestone

> Given a daily OHLCV series, produce stable, reproducible, PIT-safe structural landmarks that can later support multiple O'Neil morphologies.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before the shared landmark layer;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Expand deterministic fixtures: V-shape, W-shape, shallow sideways/flat, rounded cup, noisy loose range.
2. Define comparison metrics for landmark stability and landmark-date error without using returns.
3. Add a small evaluation harness that compares extractor outputs against labelled expected swing regions.
4. Only after the landmark method/parameter family is defensible, begin candidate-base segmentation.
