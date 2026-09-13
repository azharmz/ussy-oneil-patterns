# USSY O'Neil Pattern Recognition Engine

Canonical implementation repository for CAN SLIM workstream **#33 — O'Neil Pattern Recognition Engine**.

> ## START HERE — continuation / context recovery
>
> If a prior ChatGPT/work session is unavailable, do **not** reconstruct state from memory or from the CAN SLIM parent branch.
>
> 1. confirm the active branch in this repository;
> 2. read `docs/progress-board.md`;
> 3. read `docs/decisions/p8-development-freeze-v1.md`;
> 4. read `docs/decisions/p8-final-verdict.md`;
> 5. read `docs/production-output-contract-v2.md` before building a downstream consumer;
> 6. inspect the latest commits only after the frozen records above are understood.
>
> For #33/P8, this repository is the source of truth. The parent `azharmz/ussy-canslim-research` is roadmap/HQ and must not host a parallel pattern engine.
>
> Current state: core #33 is frozen with a **CONDITIONAL PASS** and production schema v2 is aligned to the exact frozen P8 adapter. Do not reopen morphology tuning from NFLX or from trading outcomes.

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

#33 occupies pattern quantification and morphology validation. Downstream candidate generation belongs to #34.

## Current phase

**#33 core morphology and production output are frozen after P8 independent validation.**

P8 final verdict: **CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT**.

Frozen DEVELOPMENT evidence:

- 20 authoritative positive examples;
- five examples each for `FLAT_BASE`, `CUP_WITH_HANDLE`, `CUP_WITHOUT_HANDLE`, and `DOUBLE_BOTTOM`;
- 20/20 source-dimension `MATCH`;
- zero true candidate identity `STATUS_CONFLICT`.

Independent VALIDATION:

- NFLX `CUP_WITH_HANDLE` was opened once only after DEVELOPMENT freeze;
- source agreement: `MATCH`;
- candidate resolution: `UNIQUE`;
- exact source/matched start: `2023-02-03`;
- frozen detector state: `CUP_WITH_HANDLE_AMBIGUOUS` with `BELOW_CUP_MIDPOINT` retained as validation debt.

The NFLX row had pivot/depth intentionally unscored before opening VALIDATION, so P8 does **not** claim every numeric CWH band has independent validation.

## Frozen production contract

Production schema: `oneil-pattern-output-v2`.
Engine: `33-core-p8-frozen-v1`.
Validation status: `P8_CONDITIONAL_PASS_FROZEN`.

Production directly consumes the canonical frozen P8 predictions instead of rebuilding a separate detector path. Records preserve:

- canonical `candidate_id`;
- stable `base_id` (`core-base-id-v1`);
- conservative exact-anchor `lineage_id` (`core-lineage-v1`);
- `RECOGNIZED` / `AMBIGUOUS` / `REJECTED`;
- candidate semantics;
- structural signature;
- pivot/depth when available;
- detector faults and contract versions.

The frozen v2 stream contains only the four core P8-validated families. Advanced families do not inherit this evidence level.

See:

- `docs/progress-board.md`
- `docs/p8-labelled-validation-status.md`
- `docs/decisions/p8-development-freeze-v1.md`
- `docs/decisions/p8-final-verdict.md`
- `docs/production-output-contract-v2.md`

## Core pattern scope with P8 evidence

Validated core families:

- `FLAT_BASE`
- `DOUBLE_BOTTOM`
- `CUP_WITHOUT_HANDLE`
- `CUP_WITH_HANDLE`

Later / secondary families such as `ASCENDING_BASE` and `BASE_ON_BASE` do not automatically inherit the same P8 evidence level.

Downstream consumers must preserve explicit states such as:

- `RECOGNIZED`
- `AMBIGUOUS`
- `REJECTED`

and must also preserve candidate semantics and detector faults.

## PIT rule

For an evaluation as of date `T`, no feature or landmark may use information after `T`.

If an extremum is economically located at one date but only confirmed later, preserve both concepts:

- `price_date`
- `confirmed_date`

## Research rule

The frozen P8 detector/evaluator semantics must not be revised from NFLX VALIDATION or from later trading performance.

Any future research revision requires a new explicitly versioned research cycle and must not rewrite the frozen P8 verdict.
