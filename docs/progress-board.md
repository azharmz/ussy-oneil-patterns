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
| P3 Flat Base | IN PROGRESS | P3.1 theory morphology defined; P3.2 detector v0 green; P3.3 fixture corpus green; P3.4 ambiguity/fault policy implemented |
| P4 Double Bottom | NOT STARTED | follows Flat Base first pass |
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

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

## P3 — Flat Base active objective

P3 is the first pattern-specific morphology layer. It interprets frozen P1/P2 structure rather than rebuilding extrema or segmentation.

Theory-grounded hard gates currently preregistered:

- minimum duration: 25 trading sessions;
- maximum depth: 15%.

Passing these gates is necessary but not sufficient. Flat Base still requires sideways/tight behavior; `wide/loose/erratic` is contrary evidence.

### Research tightness/fault policy — `flat-base-v0.1`

Documented in `docs/p3-flat-base-fault-policy.md`.

The audited theory sources do not provide one canonical numeric formula for tightness, so the following bands are explicitly research parameters rather than official O'Neil/IBD rules:

```text
TIGHT_MAX_NORMALIZED_RANGE = 0.03
TIGHT_MAX_CLOSE_DISPERSION = 0.01
WIDE_LOOSE_MIN_NORMALIZED_RANGE = 0.07
WIDE_LOOSE_MIN_CLOSE_DISPERSION = 0.03
```

Current fault vocabulary:

- `TOO_SHORT`;
- `TOO_DEEP`;
- `WIDE_LOOSE`;
- `BOUNDARY_CONTEXT`.

Current research state policy:

- hard gate failure or `WIDE_LOOSE` => `FLAT_BASE_REJECTED`;
- hard gates pass + tight research band + no boundary fault => `FLAT_BASE_RECOGNIZED`;
- intermediate tightness or boundary context => `FLAT_BASE_AMBIGUOUS`;
- missing/empty required region => `FLAT_BASE_NOT_EVALUABLE`.

This policy is morphology-only and must not be tuned from return, breakout success, CAGR, profit factor, win rate, or portfolio outcomes.

Current synthetic Flat Base corpus:

- `textbook_tight` — expected research recognition;
- `too_short` — negative by duration gate;
- `too_deep` — negative by depth gate;
- `wide_loose` — negative despite passing hard duration/depth gates;
- `borderline_tightness` — deliberately ambiguous.

No breakout or entry logic belongs in this phase.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no universal fixed 35-session base assumption;
- no direct CWH detector before shared morphology layers;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

1. Verify P3.4 ambiguity/fault policy in CI.
2. P3.5 perform morphology/PIT validation of `flat-base-v0.1`.
3. Add parameter-neighborhood checks around the research tightness bands without using returns.
4. Decide whether the policy is stable enough to freeze as the first Flat Base contract or remains research-only pending authoritative/human-labelled examples.
5. Move to Double Bottom only after the Flat Base first-pass contract has an explicit validation verdict.
