# #33 Progress Board

Last updated: 2026-09-12

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline established |
| Parent #32 contract confirmation | COMPLETE | parent specification is frozen and #33 is authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema and raw-vs-adjusted semantics documented |
| PIT-safe data reader | IMPLEMENTED / UNIT-TESTED IN REPO | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| Landmark representation | IMPLEMENTED / EVOLVING | explicit `price_date` vs `confirmed_date`; generic `SWING_HIGH/SWING_LOW` + evidence-rich `LandmarkCandidate` |
| Swing/extrema research | IN PROGRESS | excursion primary source + confirmed-window auxiliary evidence policy implemented |
| Visual/labelled fixtures | IN PROGRESS | V-shape, W-shape, flat/sideways, rounded cup, noisy loose range + expected regions |
| Landmark evaluation harness | IMPLEMENTED / EVOLVING | repaint/PIT checks + labelled missed/false/date-error metrics + perturbation grid |
| Boundary-artifact treatment | COMPLETE | explicit edge classification; preserved as evidence, not silently deleted; CI green |
| Landmark fusion policy | IMPLEMENTED / CI PENDING | primary excursion candidates; confirmed-window corroboration only; no naive union |
| Base segmentation | NOT STARTED | blocked until P1 contract freeze |
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

## P1 structural-turn policy

### Primary source — percentage excursion

- causal alternating swing detector;
- confirms a peak only after a sufficient decline and a trough only after a sufficient advance;
- stores original extremum `price_date` and later `confirmed_date`;
- creates the actual `LandmarkCandidate` structural skeleton.

### Auxiliary source — confirmed window / local prominence

- local high/low candidate is emitted only after a fixed number of later sessions have elapsed;
- confirmation date is never backdated;
- does **not** independently add turns to the structural candidate set;
- when a nearby same-type turn exists, its prominence/local-extremum evidence is attached to the primary candidate.

### Why no naive multi-scale union

Synthetic diagnostics showed complementary behavior: confirmed-window is cleaner on several V/W/flat/noisy cases while excursion preserves diffuse rounded-cup structure. A direct union would increase turn density and ambiguity. P1 therefore freezes a primary causal skeleton plus auxiliary corroboration rather than merging every detected extremum.

The decision is documented in `docs/p1-fusion-decision.md`.

## Evidence-rich candidate contract

`LandmarkCandidate` is restricted to `SWING_HIGH` / `SWING_LOW`; P1 cannot prematurely assign pattern-specific meanings such as `LEFT_PEAK` or `TROUGH_1`.

It can carry:

- original structural price and `price_date`;
- PIT-safe `confirmed_date`;
- detector/method provenance;
- excursion amplitude;
- local prominence/corroboration;
- temporal separation;
- explicit boundary flag and edge distances;
- extensible evidence payload.

This object is the intended handoff from the landmark layer to candidate-base segmentation.

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
- prefix repaint checks compare contemporaneous output to eventual output restricted to information known by that date;
- no truncated prefix may claim a future confirmation date;
- labelled evaluation records matched expected turns, missed turns, false turns, and landmark-index error;
- preregistered nearby-parameter perturbations test morphology stability only;
- shallow flat structure must not explode into dense false swings under small parameter changes;
- boundary candidates remain visible as evidence instead of being silently removed;
- no return, CAGR, PF, win-rate, breakout outcome, or portfolio result enters P1 selection.

## Immediate milestone

> Freeze the P1 landmark-candidate contract and authorize P2 candidate-base segmentation.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before the shared landmark layer;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Verify the fusion-policy tests in CI.
2. Freeze/version the P1 landmark-candidate contract.
3. Mark P1 COMPLETE if the full test suite is green.
4. Begin P2 candidate-base segmentation: structural high → decline/trough → recovery candidate regions.
