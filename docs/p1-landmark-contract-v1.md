# P1 Landmark Candidate Contract v1

Status: FROZEN
Date: 2026-09-12
Contract version: `p1-landmark-v1`

## Purpose

This document freezes the handoff from P1 Structural Landmark Engine to P2 Candidate Base Segmentation.

P1 does not classify O'Neil patterns. It produces generic, point-in-time-safe structural-turn candidates with evidence. Pattern-specific meanings such as `LEFT_PEAK`, `TROUGH_1`, `MIDDLE_PEAK`, `RIGHT_PEAK`, `HANDLE_LOW`, or `PIVOT` belong to later morphology layers.

## Data semantics

- Input is daily production-ready OHLCV from `azharmz/ussy-data`.
- Consumers resolve the current dataset through `production/ready/current.json`.
- Structural morphology uses raw OHLC under the current project specification.
- `adj_close` remains a distinct field and is not silently substituted for raw OHLC.
- Historical runs must receive only rows with `date <= asof_date`.

## PIT semantics

Every structural candidate has two distinct dates:

- `price_date`: date on which the structural extremum price occurred;
- `confirmed_date`: earliest date on which the detector could know the turn from data available through that date.

Invariant:

`confirmed_date >= price_date`

A candidate is usable at an as-of date only when:

`confirmed_date <= asof_date`

No downstream P2/P3+ code may reinterpret `price_date` as the date the signal became knowable.

## Candidate vocabulary

P1 output is restricted to:

- `SWING_HIGH`
- `SWING_LOW`

P1 must not emit pattern-specific landmark names.

## Candidate fields

The stable P1 candidate representation is `LandmarkCandidate` with:

- `type`
- `price`
- `price_date`
- `confirmed_date`
- `method`
- `amplitude_pct`
- `prominence_pct`
- `separation_sessions`
- `boundary`
- `evidence`

The evidence mapping is extensible, but downstream code must not require an undocumented key without a contract revision.

## Source policy

The frozen v1 source policy is **primary causal source + auxiliary evidence**, not a naive multi-detector union.

### Primary source

Percentage-excursion provides the candidate structural-turn sequence.

### Auxiliary source

Confirmed-window/local-prominence extrema may corroborate a nearby same-type primary turn and add evidence such as local prominence.

Auxiliary extrema do **not** create a new candidate by themselves in v1.

This preserves diffuse structural turns such as rounded cup troughs while avoiding explosion of local-window extrema into a second independent candidate sequence.

## Fusion semantics

Default v1 fusion policy:

- match only the same landmark type;
- use a bounded session-distance tolerance;
- preserve primary candidate `price_date` and `confirmed_date`;
- auxiliary evidence never backdates primary confirmation;
- preserve detector provenance in `evidence`;
- temporal separation is measured between primary structural turns.

## Boundary semantics

Observed-series boundary proximity is evidence, not deletion.

A turn near the left or right edge is retained with `boundary=True` and distance metadata. P2 may reject, down-weight, or require additional context for such turns, but must not silently treat them as fully interior observations.

## Robustness policy

P1 parameters were checked with a small preregistered morphology-only perturbation grid.

Parameter assessment must not use:

- return;
- CAGR;
- profit factor;
- win rate;
- breakout outcome;
- portfolio result.

Future P1 parameter revisions require morphology/PIT justification and a contract-version change if output semantics materially change.

## P1 validation invariants

The v1 implementation is guarded by tests for:

- no backdated confirmation;
- prefix/no-repaint behavior;
- labelled expected/missed/false structural turns;
- landmark-date error;
- flat-range false-turn control;
- W-structure parameter robustness;
- explicit boundary classification;
- auxiliary-only extrema not creating candidates.

## Versioning rule

`p1-landmark-v1` is frozen for P2 development.

Bug fixes that preserve these semantics may remain v1. Any change to candidate vocabulary, PIT semantics, primary/auxiliary source roles, or mandatory candidate fields requires a new contract version and explicit migration note.

## P2 handoff

P2 may consume only confirmed `LandmarkCandidate` objects under this contract and may assign provisional base roles from their sequence. P2 must not rebuild a separate hidden swing detector.
