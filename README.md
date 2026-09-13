# USSY O'Neil Pattern Recognition Engine

Canonical implementation repository for CAN SLIM workstream **#33 — O'Neil Pattern Recognition Engine**.

> ## START HERE — continuation / context recovery
>
> If a prior ChatGPT/work session is unavailable, do **not** reconstruct state from memory or from the CAN SLIM parent repo.
>
> 1. read `docs/progress-board.md`;
> 2. read `docs/decisions/p8-development-freeze-v1.md` and `docs/decisions/p8-final-verdict.md` for the frozen four-core-family track;
> 3. read `docs/decisions/p6-final-verdict.md` and `docs/decisions/p6-cycle2-terminal-verdict.md` before touching advanced patterns;
> 4. read `docs/production-output-contract-v2.md` before building a downstream consumer;
> 5. inspect latest commits only after those frozen records are understood.
>
> This repository is the source of truth for #33. `azharmz/ussy-canslim-research` is the parent/HQ consumer and must not host a parallel pattern engine.

## Current authoritative state

### Four production core families

Frozen production scope:

- `FLAT_BASE`
- `DOUBLE_BOTTOM`
- `CUP_WITHOUT_HANDLE`
- `CUP_WITH_HANDLE`

P8 verdict: **CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT**.

Frozen DEVELOPMENT evidence is 20 authoritative positives, five per core family, with 20/20 source-dimension `MATCH` and zero true candidate identity `STATUS_CONFLICT`. NFLX `CUP_WITH_HANDLE` was then opened once as untouched VALIDATION and structurally matched uniquely at the authoritative start, while retaining frozen `CUP_WITH_HANDLE_AMBIGUOUS / BELOW_CUP_MIDPOINT` debt. No post-validation tuning is allowed.

Production schema remains **`oneil-pattern-output-v2`**, engine **`33-core-p8-frozen-v1`**. Production directly consumes the frozen P8 canonical prediction adapter and preserves candidate/base/lineage identity, explicit detector state, candidate semantics, structural signature, pivot/depth when available, faults, and contract versions.

### P6 advanced families

Advanced scope:

- `ASCENDING_BASE`
- `BASE_ON_BASE`

Terminal verdict:

**DEFERRED / NOT PRODUCTION-VALIDATED / FROZEN UNTIL NEW AUTHORITATIVE MORPHOLOGY EVIDENCE EXISTS**.

P6 is **not** production-equivalent to the four core families and is **not** emitted by `oneil-pattern-output-v2`.

Cycle 1 completed a full DEVELOPMENT → freeze → untouched one-shot VALIDATION discipline. STT (`ASCENDING_BASE`) and C (`BASE_ON_BASE`) were consumed exactly once; both matched sparse source dimensions, but STT was rejected and C ambiguous. Cycle 1 therefore failed morphology validation. STT/C must never be recycled as untouched validation.

Cycle 2 used fresh authoritative DEVELOPMENT evidence:

- Ascending Base: AVGO, TME, CCJ, SNOW, NAVN;
- Base-on-Base: META, TRV, SE, JLL, SEI.

It reserved MRX (`ASCENDING_BASE`) and CAT (`BASE_ON_BASE`) as untouched VALIDATION **before** DEVELOPMENT scoring. Cycle 2 DEVELOPMENT ended at 9/10 source-dimension `MATCH`, zero identity `STATUS_CONFLICT`, but exposed a more fundamental evidence boundary:

- all five Ascending Base examples have multiple source-equivalent internal candidates because authoritative sources do not provide exact pullback landmarks/boundaries;
- Base-on-Base authoritative guidance says the second base is `entirely or mostly above` the first but does not provide a universal quantitative definition of `mostly above`;
- META is a genuine `MISS_PATTERN`, and repairing it by loosening frozen P3/P4/P5/P8 constituent morphology would violate the frozen-core boundary.

Therefore Cycle 2 was **not frozen for one-shot validation**. MRX and CAT remain untouched and must not be used for DEVELOPMENT/tuning while that status is preserved.

Do **not** open Cycle 3 merely because more articles provide pattern names, pivots, or approximate starts. P6 may be reopened only when genuinely new authoritative morphology evidence resolves a missing operational dimension, such as exact Ascending Base pullback landmarks/boundaries, an authoritative quantitative Base-on-Base `mostly above` rule, or an authoritative labelled dataset that independently resolves candidate identity.

## Parent contract and ownership

Parent repository: `azharmz/ussy-canslim-research`.

This repository owns:

- PIT-safe landmarks and base segmentation;
- morphology features and O'Neil pattern classification;
- fault / ambiguity evidence;
- pattern-specific structural pivots;
- morphology validation;
- canonical #33 production output contracts.

This repository does **not** own breakout execution, CAN SLIM C/A/I/M integration, portfolio construction, sell rules, CAGR/PF optimization, FWD1, EXH2, or #34 candidate generation.

The governing order remains:

```text
THEORY
  -> FROZEN SPECIFICATION
  -> PATTERN QUANTIFICATION
  -> MORPHOLOGY VALIDATION
  -> CANDIDATE GENERATION
  -> PERFORMANCE RESEARCH
```

#33 stops at morphology/production-contract governance. #34 belongs to the CAN SLIM parent workstream.

## Governance prohibitions

Do not:

- tune frozen P3/P4/P5/P8 from NFLX, P6, returns, CAGR, PF, FWD1, breakout success, or entry optimization;
- tune P6 from consumed STT/C validation evidence;
- use MRX/CAT as DEVELOPMENT while they remain untouched;
- choose an Ascending Base candidate because its detector state best fits an authoritative label;
- invent a numeric Base-on-Base `mostly above` threshold;
- use P6 as a backdoor to loosen frozen core morphology;
- emit `ASCENDING_BASE` or `BASE_ON_BASE` through `oneil-pattern-output-v2`;
- describe P6 as P8-equivalent or production-validated.

## Canonical records

Core:

- `docs/progress-board.md`
- `docs/decisions/p8-development-freeze-v1.md`
- `docs/decisions/p8-final-verdict.md`
- `docs/production-output-contract-v2.md`

P6:

- `data/p6/labels_cycle2_v0.csv`
- `docs/p6-cycle2-source-audit.md`
- `docs/decisions/p6-cycle2-terminal-verdict.md`
- `docs/decisions/p6-final-verdict.md`

Cycle 1 records/artifacts remain historical evidence and must not be deleted or rewritten.
