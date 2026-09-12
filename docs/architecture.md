# Architecture — #33 O'Neil Pattern Recognition Engine

Status: bootstrap contract
Upstream spec: parent `ussy-canslim-research` #32, frozen v1

## Pipeline

```text
R2 DAILY OHLCV
  -> DATA NORMALIZATION
  -> PRIOR-TREND FEATURES
  -> CANDIDATE-BASE SEGMENTATION
  -> PIT-SAFE LANDMARK EXTRACTION
  -> MORPHOLOGY FEATURES
  -> PATTERN CLASSIFIERS
       - FLAT_BASE
       - DOUBLE_BOTTOM
       - CUP_WITHOUT_HANDLE
       - CUP_WITH_HANDLE
       - ASCENDING_BASE (later)
  -> BASE RELATIONSHIP ENGINE
       - BASE_ON_BASE (later)
  -> FAULT / AMBIGUITY EVIDENCE
  -> CANONICAL STRUCTURAL PIVOT
```

## Boundary

#33 outputs pattern facts. It does not decide full CAN SLIM eligibility and does not perform trading optimization.

Downstream #34 will combine #33 outputs with breakout, volume, C/A/L/M and other CAN SLIM evidence.

## Daily-data contract

Minimum normalized columns:

```text
security_id or symbol
session_date
open
high
low
close
volume
```

The actual upstream R2 contract must be inspected before freezing normalization semantics, especially adjusted-price behavior.

## PIT semantics

Every computation is evaluated with an explicit `asof_date`.

For `asof_date = T`:

```text
max(input.session_date) <= T
```

No landmark may be emitted as known before it was confirmable from available bars.

Landmarks therefore distinguish:

```text
price_date      # where the structural price occurred
confirmed_date  # first date the algorithm could know/confirm it
```

A later-confirmed high/low may retain its original `price_date`, but downstream PIT consumers must use `confirmed_date` for information availability.

## Landmark-first design

Pattern detectors must consume a reusable landmark representation rather than rediscovering extrema independently from raw candles.

This prevents:

- inconsistent extrema across patterns;
- hidden future-aware peaks/troughs;
- duplicated geometry logic;
- detector-specific overfitting.

## Classification philosophy

Do not force a named pattern.

Supported outcomes include valid named morphology, unclassified, ambiguous, and faulty structures.

The classifier must retain interpretable evidence rather than only an opaque score.

## Parameter governance

Landmark/segmentation parameters may be chosen from:

- frozen O'Neil theory;
- morphology-label agreement;
- landmark stability;
- robustness across samples/scales;
- reduction of structural false positives.

They may not be chosen from CAGR, PF, win rate, alpha, or later returns.
