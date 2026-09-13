# P3 Flat Base Contract — `flat-base-v2`

Status: **P8 DEVELOPMENT REVISION — NOT FINAL-FROZEN**
Date: 2026-09-13

This revision supersedes the first-pass state mapping in `flat-base-v1` for P8 DEVELOPMENT validation. Numeric theory gates and research bands are unchanged.

## Inputs

Confirmed-structure assessment continues to consume frozen P1 structural landmarks, P2 morphology-neutral segments, and raw OHLC over the structural segment window.

P8 additionally tests a separately marked `OPEN_RIGHT_EDGE` observation from a confirmed P1 SWING_HIGH through the current as-of horizon. That observation is not a fabricated structural landmark and is not yet promoted into frozen P2 production semantics.

## Theory-grounded hard gates

Unchanged:

- minimum duration: **25 trading sessions**;
- maximum depth: **15%**.

Failure of either gate => `FLAT_BASE_REJECTED`.

## Research-only bands

Unchanged:

```text
TIGHT_MAX_NORMALIZED_RANGE = 0.03
TIGHT_MAX_CLOSE_DISPERSION = 0.01
WIDE_LOOSE_MIN_NORMALIZED_RANGE = 0.07
WIDE_LOOSE_MIN_CLOSE_DISPERSION = 0.03
```

These values are research descriptors, not official O'Neil/IBD numeric rules.

## Revised state mapping

P8 authoritative DEVELOPMENT evidence showed that two independently labelled Flat Bases, SNPS 2023 and TW 2024, can satisfy source start/pivot plus duration/depth gates while tripping only the research-only `WIDE_LOOSE` band.

Therefore v2 maps:

- duration/depth hard-gate failure => `REJECTED`;
- hard gates pass + `WIDE_LOOSE` => `AMBIGUOUS` with `WIDE_LOOSE` fault retained;
- hard gates pass + boundary context => `AMBIGUOUS`;
- hard gates pass + tight research band => `RECOGNIZED`;
- hard gates pass + intermediate tightness => `AMBIGUOUS`;
- missing/empty required OHLC => `NOT_EVALUABLE`.

The numerical wide/loose threshold is **not** moved to fit the labels.

## Right-edge DEVELOPMENT experiment

`p8-open-right-edge-flat-v0.2` enumerates every confirmed P1 SWING_HIGH known as of T as a possible Flat start and observes raw OHLC through T.

- T is an observation boundary, not a structural turn.
- pivot remains the confirmed start-high price/date.
- candidate output carries explicit `OPEN_RIGHT_EDGE` semantics.
- confirmed P2 candidates remain present as a separate candidate class.
- source labels are never consulted during enumeration.

This experiment addresses the inability of a fully confirmed high-low-high segment model to represent a base that is still forming at the right edge.

## Evidence / guardrails

The revision is morphology/source-driven only. No return, CAGR, PF, win rate, FWD1, breakout outcome, entry optimization, or portfolio result was used.

NFLX VALIDATION remains locked until DEVELOPMENT semantics are frozen.

## Freeze status

`flat-base-v2` is not yet final-frozen. P8 must still evaluate additional authoritative Flat examples, candidate explosion/identity effects, and prefix behavior before this revision is promoted into production P2/P3 contracts.
