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
> 5. read `docs/decisions/p6-development-freeze-v1.md` and `docs/decisions/p6-final-verdict.md` before changing advanced-pattern semantics;
> 6. read `docs/production-output-contract-v2.md` before building a downstream consumer;
> 7. inspect the latest commits only after the frozen records above are understood.
>
> For #33/P8, this repository is the source of truth. The parent `azharmz/ussy-canslim-research` is roadmap/HQ and must not host a parallel pattern engine.
>
> Current state: core #33 is frozen with a **CONDITIONAL PASS** and production schema v2 is aligned to the exact frozen P8 adapter. P6 advanced patterns completed an authoritative DEVELOPMENT freeze plus untouched one-shot VALIDATION and finished **VALIDATION FAIL / FROZEN — NOT PRODUCTION-VALIDATED**. Do not tune from the opened P6 validation rows, NFLX, or trading outcomes.

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

**#33 core morphology and production output are frozen after P8 independent validation. P6 advanced morphology has completed a separate authoritative validation cycle and failed the morphology-recognition bar.**

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

## P6 advanced-pattern verdict

P6 final verdict: **VALIDATION FAIL / FROZEN — NOT PRODUCTION-VALIDATED**.

P6 was held to a separate authoritative DEVELOPMENT + untouched VALIDATION cycle without reopening frozen core morphology.

Frozen DEVELOPMENT:

- 5 authoritative `ASCENDING_BASE` positives;
- 5 authoritative `BASE_ON_BASE` positives;
- 10/10 source-dimension `MATCH`;
- zero candidate identity `STATUS_CONFLICT`;
- detector states nevertheless included 3 rejected Ascending Base examples and 4 ambiguous Base-on-Base examples.

Untouched one-shot VALIDATION:

- STT `ASCENDING_BASE`: source-dimension `MATCH`, candidate `UNIQUE`, detector state `ASCENDING_BASE_REJECTED`;
- C `BASE_ON_BASE`: source-dimension `MATCH`, source-equivalent multiple candidates, matched detector state `BASE_ON_BASE_AMBIGUOUS`;
- validation workflow run `34750413835`, artifact id `10315775412`;
- one-shot workflow path was removed after execution.

Because neither untouched authoritative positive is `RECOGNIZED`, sparse source-dimension agreement is not treated as a morphology pass. The earlier P6 conditional-pass verdict is superseded by the authoritative validation result.

P6 remains outside production schema v2. A future cycle requires new authoritative morphology evidence and a new untouched validation set; STT/C may not be recycled as untouched validation.

See:

- `docs/p6-source-audit-v2.md`
- `docs/p6-advanced-patterns-contract-v2.md`
- `docs/decisions/p6-development-freeze-v1.md`
- `docs/decisions/p6-final-verdict.md`

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

Separately frozen P6 advanced families:

- `ASCENDING_BASE`
- `BASE_ON_BASE`

They failed their separate authoritative validation cycle and are not emitted by frozen production v2.

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

The frozen P8 detector/evaluator semantics must not be revised from NFLX VALIDATION or from later trading performance. The frozen P6 cycle must likewise not be revised from STT/C VALIDATION, trading outcomes, or used as a route to reopen P3/P4/P5/P8.

Any future P6 research requires a new explicitly versioned cycle, new authoritative morphology evidence, and a new untouched validation set. Frozen verdicts remain historical evidence and must not be rewritten by post-hoc tuning.
