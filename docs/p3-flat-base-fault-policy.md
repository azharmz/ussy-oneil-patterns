# P3 Flat Base Ambiguity / Fault Policy

Status: RESEARCH POLICY
Date: 2026-09-12
Implementation version: `flat-base-v0.1`

## Purpose

Make Flat Base ambiguity and fault handling explicit before broader labelled validation.

The parent theory contract provides two numeric morphology gates that are treated as theory-grounded in this project:

- minimum duration: 25 trading sessions;
- maximum depth: 15%.

Official guidance also requires a sideways/tight character and warns against wide/loose/erratic action, but the audited sources do not supply one canonical numeric formula for tightness. Therefore the additional numerical bands below are research parameters, not claimed as official O'Neil/IBD rules.

## Research tightness bands

Preregistered for synthetic/labelled morphology validation only:

```text
TIGHT_MAX_NORMALIZED_RANGE = 0.03
TIGHT_MAX_CLOSE_DISPERSION = 0.01
WIDE_LOOSE_MIN_NORMALIZED_RANGE = 0.07
WIDE_LOOSE_MIN_CLOSE_DISPERSION = 0.03
```

These parameters must not be tuned using return, breakout success, CAGR, profit factor, win rate, or portfolio outcome.

## Fault vocabulary

- `TOO_SHORT`: duration < 25 sessions;
- `TOO_DEEP`: depth > 15%;
- `WIDE_LOOSE`: research wide/loose band exceeded;
- `BOUNDARY_CONTEXT`: one or more structural landmarks are boundary-marked by frozen P1 semantics.

Faults are persisted as evidence rather than hidden inside a Boolean.

## State policy

### `FLAT_BASE_REJECTED`

Used when any of the following is true:

- hard duration gate fails;
- hard depth gate fails;
- wide/loose research fault is present.

### `FLAT_BASE_RECOGNIZED`

Used in v0.1 research only when:

- duration/depth gates pass;
- no boundary-context fault is present;
- normalized range <= 3%;
- close dispersion <= 1%.

This is a research recognition state subject to P3.5 labelled validation; it is not yet a frozen production contract.

### `FLAT_BASE_AMBIGUOUS`

Used when hard theory gates pass but:

- tightness sits between the preregistered tight and wide/loose bands; or
- structural boundary context prevents textbook recognition.

### `FLAT_BASE_NOT_EVALUABLE`

Used when the structural region is missing/empty or required price observations are unavailable.

## Why an ambiguity band exists

The detector intentionally leaves a gap between the tight and wide/loose bands. This avoids turning a qualitative theory phrase into an unjustified single knife-edge cutoff. The ambiguous region is expected to be especially useful during labelled validation and future confusion analysis against Double Bottom / Cup-family structures.

## Versioning

`flat-base-v0.1` is research semantics. The 25-session/15%-depth gates are treated separately from the provisional tightness bands. Any production freeze must document which research bands survive labelled morphology validation and why.
