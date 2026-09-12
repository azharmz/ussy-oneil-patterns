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
| Visual/labelled fixtures | IN PROGRESS | V-shape, W-shape, flat/sideways, rounded cup, noisy loose range + expected regions |
| Landmark evaluation harness | IMPLEMENTED / EVOLVING | repaint/PIT checks + labelled missed/false/date-error metrics |
| Base segmentation | NOT STARTED | blocked until evidence-rich landmark candidate layer is stable |
| Flat Base | NOT STARTED | first morphology phase |
| Double Bottom | NOT STARTED | first morphology phase |
| Cup family | NOT STARTED | shared cup morphology before handle classifier |
| Advanced patterns | NOT STARTED | Ascending Base / Base-on-Base |
| Fault/ambiguity layer | NOT STARTED | wide/loose, V-shape, malformed/incomplete etc. |
| Labelled morphology validation | NOT STARTED | authoritative/human-labelled corpus later required |

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
- parameters are research defaults for morphology/stability only, not frozen detector semantics and not return-optimized.

### Candidate B — confirmed window

- local high/low candidate is emitted only after a fixed number of later sessions have elapsed;
- confirmation date is the end of the required confirmation window, never backdated to the extremum date;
- includes a minimum local excursion/prominence requirement to suppress trivial noise;
- parameters are research defaults only.

## Synthetic labelled morphology corpus

Current deterministic fixtures:

- V-shape rebound;
- W-shape / double-bottom-like structure;
- shallow flat/sideways range;
- rounded cup-like arc;
- noisy wide/loose range.

Expected structural turns are stored as labelled index regions where appropriate rather than forcing one exact bar. These are diagnostic geometry examples, not O'Neil ground truth and not substitutes for later authoritative/human-labelled validation examples.

## Evaluation rules now encoded

- `confirmed_date >= price_date`;
- percentage-excursion confirmation is not backdated;
- confirmed-window extrema carry the later confirmation date;
- prefix repaint test compares contemporaneous prefix output against eventual full-series output restricted to landmarks that should already have been known by that prefix date;
- no landmark from a truncated prefix may claim a confirmation date beyond that prefix;
- labelled evaluation records matched expected turns, missed turns, false structural turns, and landmark-index error;
- cross-extractor agreement is measured only from landmark type/date proximity;
- no return, CAGR, PF, win-rate, or downstream breakout outcome enters P1 selection.

A GitHub Actions pytest workflow is present so these invariants can be checked on every push/PR.

## Current P1 diagnostic verdict

Documented in `docs/p1-landmark-evaluation.md`.

Under the current research defaults:

- confirmed-window is cleaner on V/W/flat/noisy-range fixtures;
- percentage-excursion successfully captures the diffuse rounded-cup trough that the local-prominence method misses;
- percentage-excursion can emit left-boundary extrema that should not automatically be treated as morphology landmarks;
- confirmed-window/local prominence therefore cannot be the sole universal landmark source;
- neither raw extractor is frozen as the universal engine.

Current architectural direction:

> excursion should provide causal structural-turn candidates, while local prominence, separation, amplitude and boundary status should remain independent evidence attached to each candidate.

## Immediate milestone

> Given a daily OHLCV series, produce stable, reproducible, PIT-safe structural landmark candidates with enough evidence for different O'Neil morphologies to interpret them differently.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before the shared landmark layer;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Implement a reusable evidence-rich `LandmarkCandidate` object.
2. Attach excursion amplitude, local prominence, temporal separation, boundary flag and method provenance.
3. Run a small preregistered parameter perturbation grid for morphology/stability robustness only.
4. Confirm that interior expected landmarks remain stable while false structural turns do not explode.
5. Freeze a P1 landmark-candidate contract sufficiently to begin P2 candidate-base segmentation.
