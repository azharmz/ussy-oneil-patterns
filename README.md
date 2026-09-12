# USSY O'Neil Pattern Recognition Engine

Canonical implementation repository for CAN SLIM workstream **#33 — O'Neil Pattern Recognition Engine**.

> ## START HERE — continuation / context recovery
>
> If a prior ChatGPT/work session is unavailable, do **not** reconstruct state from memory or from the CAN SLIM parent branch.
>
> 1. confirm the active branch in this repository;
> 2. read `docs/progress-board.md` on that branch;
> 3. inspect the latest commits;
> 4. read the newest relevant file under `docs/decisions/`;
> 5. continue from the `Next work` section without reopening frozen/locked validation data.
>
> For #33/P8, this repository is the source of truth. The parent `azharmz/ussy-canslim-research` is roadmap/HQ and must not host a parallel pattern engine.
>
> Current guardrails: DEVELOPMENT-only tuning; NFLX VALIDATION remains locked; no return/CAGR/PF/FWD1/entry optimization; source precision must not be invented; ambiguity/fault evidence must remain explicit; #34 stays blocked until P8/#33 is defensible.

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
- morphology / landmark validation;
- canonical #33 production output contracts.

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

## Current phase

**P8 — labelled morphology validation / cross-repo reconciliation.**

P1–P7 and P9 first-pass contracts already exist; P8 remains the blocking validation debt before #33 can be considered final.

The canonical authoritative corpus now carries five DEVELOPMENT examples spanning the four core pattern families plus one locked VALIDATION example. See `data/p8/labels_v0.csv`, `docs/progress-board.md`, and `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

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

## PIT rule

For an evaluation as of date `T`, no feature or landmark may use information after `T`.

If an extremum is economically located at one date but only confirmed later, preserve both concepts:

- `price_date`
- `confirmed_date`

## Research rule

Detector and evaluator semantics may be revised from theory, source-grounded morphology disagreement, landmark stability, and robustness. They may **not** be revised from later trading performance.

See `docs/progress-board.md` and `docs/architecture.md`.
