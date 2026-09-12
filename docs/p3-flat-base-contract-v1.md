# P3 Flat Base Contract — `flat-base-v1`

Status: **FROZEN FIRST-PASS CONTRACT**

This contract defines the first defensible Flat Base morphology layer in #33. It is frozen only as a first-pass research contract; later authoritative/human-labelled validation may require a versioned revision.

## Inputs

P3 consumes:

- frozen P1 structural landmarks (`p1-landmark-v1`);
- frozen P2 morphology-neutral base segments (`p2-segmentation-v1`);
- raw OHLC over the structural segment window only.

P3 must not discover hidden extrema or silently redefine the P2 segment boundary.

## Theory-grounded hard gates

The current preregistered hard gates are:

- minimum duration: **25 trading sessions**;
- maximum depth: **15%**.

These are necessary but not sufficient for Flat Base recognition.

## Morphology descriptors

The v1 assessment records:

- normalized high-low range;
- close dispersion relative to mean close;
- fraction of closes within 5% of the region high;
- P2 boundary context.

## Research-only tightness bands

The audited theory sources do not provide one canonical numerical formula for Flat Base tightness. Therefore these values are explicitly research parameters, not official O'Neil/IBD rules:

```text
TIGHT_MAX_NORMALIZED_RANGE = 0.03
TIGHT_MAX_CLOSE_DISPERSION = 0.01
WIDE_LOOSE_MIN_NORMALIZED_RANGE = 0.07
WIDE_LOOSE_MIN_CLOSE_DISPERSION = 0.03
```

They must not be tuned from return, breakout success, CAGR, profit factor, win rate, or portfolio outcomes.

## State semantics

The public morphology states are:

- `FLAT_BASE_RECOGNIZED`
- `FLAT_BASE_REJECTED`
- `FLAT_BASE_AMBIGUOUS`
- `FLAT_BASE_NOT_EVALUABLE`

Decision policy:

- duration/depth hard-gate failure => `REJECTED`;
- `WIDE_LOOSE` morphology => `REJECTED`;
- hard gates pass + tight research band + no boundary fault => `RECOGNIZED`;
- intermediate tightness or boundary context => `AMBIGUOUS`;
- missing/empty required OHLC region => `NOT_EVALUABLE`.

## Fault vocabulary

- `TOO_SHORT`
- `TOO_DEEP`
- `WIDE_LOOSE`
- `BOUNDARY_CONTEXT`

Faults remain evidence; downstream code should not infer additional trading meaning from them.

## PIT / structural-window rule

Flat Base assessment uses only bars from `segment.start_date` through `segment.end_date`. Future rows outside that structural window must not alter an already-known assessment.

No breakout, entry, return, or post-pattern outcome may be used to determine whether the morphology is a Flat Base.

## Validation verdict

Synthetic first-pass validation is green for:

- textbook-tight positive morphology;
- too-short negative;
- too-deep negative;
- wide/loose negative despite duration/depth passing;
- borderline tightness ambiguity;
- small ±0.1% price perturbation stability on clear positive/negative fixtures;
- future-row invariance outside the structural segment window.

This is sufficient to freeze `flat-base-v1` as a reproducible first-pass research contract and proceed to the next morphology family.

It is **not** evidence that the research tightness bands are universally correct. P8 later remains responsible for authoritative/human-labelled morphology validation across real examples.

## Versioning

Any material change to:

- hard-gate semantics;
- research tightness bands;
- state mapping;
- fault vocabulary;
- structural-window/PIT semantics;

must produce a versioned contract revision rather than silently changing `flat-base-v1`.
