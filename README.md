# USSY O'Neil Pattern Recognition Engine

Implementation repository for CAN SLIM workstream **#33 — O'Neil Pattern Recognition Engine**.

## Parent contract

Parent repository: `azharmz/ussy-canslim-research`

Frozen upstream specification: `docs/methodology/theory-faithful-candidate-spec-v1.md` in the parent repository.

This repository owns only:

- candidate-base segmentation;
- PIT-safe swing / landmark extraction;
- morphology features;
- O'Neil base classification;
- fault / ambiguity evidence;
- pattern-specific structural pivots;
- morphology / landmark validation.

This repository does **not** own breakout execution, CAN SLIM C/A/I/M integration, portfolio construction, sell rules, CAGR/PF optimization, FWD1, or EXH2.

## Governing development order

```text
THEORY
  -> FROZEN SPECIFICATION
  -> PATTERN QUANTIFICATION
  -> MORPHOLOGY VALIDATION
  -> CANDIDATE GENERATION
  -> PERFORMANCE RESEARCH
```

#33 occupies only pattern quantification and morphology validation.

## Core pattern scope

Initial core patterns:

- `FLAT_BASE`
- `DOUBLE_BOTTOM`
- `CUP_WITHOUT_HANDLE`
- `CUP_WITH_HANDLE`

Later / secondary:

- `ASCENDING_BASE`
- `BASE_ON_BASE`

Fallback states:

- `UNCLASSIFIED_BASE`
- `AMBIGUOUS`
- `FAULTY_BASE`

## First technical milestone

Given a daily OHLCV series, produce stable, reproducible, **PIT-safe structural landmarks** that can support multiple O'Neil morphologies.

The project must not jump directly to a cup-with-handle detector.

## PIT rule

For an evaluation as of date `T`, no feature or landmark may use information after `T`.

If an extremum is economically located at one date but only confirmed later, preserve both concepts:

- `price_date`
- `confirmed_date`

## Current phase

`P0 — Bootstrap` / `P1 — Landmark research`.

See `docs/progress-board.md` and `docs/architecture.md`.
