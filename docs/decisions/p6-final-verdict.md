# P6 Advanced Patterns — Final Authoritative Validation Verdict

Date: 2026-09-13

Verdict: **VALIDATION FAIL / FROZEN — NOT PRODUCTION-VALIDATED**

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only. Frozen P3/P4/P5/P8 core morphology is unchanged.

## Validation standard

P6 was re-opened only as a separately versioned validation cycle and was held to the same basic evidence discipline as the four core families:

1. authoritative positive DEVELOPMENT corpus;
2. untouched authoritative VALIDATION corpus locked before tuning;
3. PIT-safe morphology extraction and source-dimension scoring;
4. DEVELOPMENT freeze before VALIDATION open;
5. one-shot frozen VALIDATION execution;
6. no tuning from VALIDATION or trading outcomes.

## Frozen DEVELOPMENT

Freeze record: `docs/decisions/p6-development-freeze-v1.md`.

- evidence commit: `ba13844145095a4bb40f75d9ce477fd61d3aad50`
- workflow run: `34748254127`
- artifact id: `10315076061`
- artifact digest: `sha256:332f7fc9aab753280b386491cb59d3a48ad4f258374c7e40b804309eb93425e8`
- regression: **235 tests passed**
- P8 DEVELOPMENT: **skipped**
- corpus: 5 authoritative `ASCENDING_BASE` + 5 authoritative `BASE_ON_BASE` positives
- source-dimension agreement: **10/10 MATCH**
- candidate identity `STATUS_CONFLICT`: **0**

However, detector-state evidence was materially weaker than source-dimension agreement:

- Ascending Base: 1 recognized, 1 ambiguous, 3 rejected;
- Base-on-Base: 1 recognized, 4 ambiguous.

The DEVELOPMENT cycle therefore froze explicit detector-state debt rather than hiding it behind source pivot agreement.

## Untouched one-shot VALIDATION

The locked rows were `p6-label-0011` (State Street, `ASCENDING_BASE`) and `p6-label-0012` (Citigroup, `BASE_ON_BASE`). They were opened exactly once after DEVELOPMENT freeze.

Execution commit: `2c10165e67c1486459ddf191021243ad70e90f7b`.
Workflow: `p6-validation-once`, run `34750413835`.
Artifact: `p6-frozen-validation`, id `10315775412`.
Artifact digest: `sha256:618c72a7accbb9b5434db9040e2bad645bf0435de21b32ffac019bfe4d83ca16`.

Frozen one-shot result:

```text
result_count                    = 2
source-dimension MATCH          = 2
candidate identity conflicts    = 0

STT ASCENDING_BASE:
  candidate resolution          = UNIQUE
  matched detector state        = ASCENDING_BASE_REJECTED

C BASE_ON_BASE:
  candidate resolution          = SOURCE_EQUIVALENT_MULTIPLE
  matched detector state        = BASE_ON_BASE_AMBIGUOUS
```

The one-shot workflow path was removed immediately after execution in commit `da251cee5f8ffbc3038a198950d3b824f4b4d458` so VALIDATION cannot become iterative tuning evidence.

## Interpretation

The two authoritative VALIDATION rows agree with the frozen adapter on the published pattern identity/pivot dimensions, but neither positive untouched example is recognized by the frozen detector state. Under a morphology-validation standard, `MATCH` on sparse source dimensions is not sufficient to override a `REJECTED` or `AMBIGUOUS` morphology state.

Therefore P6 does **not** earn the core patterns' validation status. The defensible verdict for this cycle is **VALIDATION FAIL**, not CONDITIONAL PASS.

This is not evidence that the published patterns are invalid. It is evidence that the current quantitative P6 representation is not sufficiently validated to claim reliable recognition of authoritative examples.

## Why no post-validation fix is allowed

The observed failures cannot be repaired inside this cycle without contaminating the untouched test:

- `ASCENDING_BASE`: the validation example is uniquely resolved but rejected. Weakening higher-low or related morphology after seeing STT would be direct validation-set tuning.
- `BASE_ON_BASE`: authoritative guidance permits the second base to sit “entirely or mostly above” the first, but the available source material does not provide a universal numerical definition of “mostly.” Converting the C result from ambiguous to recognized by inventing an overlap percentage would create unsupported precision.

A new P6 cycle is allowed only with new authoritative DEVELOPMENT evidence and a new untouched VALIDATION set. The failed one-shot rows must never be recycled as untouched validation.

## Frozen consequences

- `ASCENDING_BASE` and `BASE_ON_BASE` remain outside `oneil-pattern-output-v2`.
- No downstream consumer may describe P6 as P8-equivalent or production-validated.
- P3/P4/P5/P8 core remains frozen and unchanged.
- No return, CAGR, PF, FWD1, breakout success, entry optimization, or portfolio outcome may be used to rescue this verdict.
- Existing P6 v2/v3 implementation and artifacts remain historical evidence; this verdict supersedes the earlier `CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT` status.

## What would justify another cycle

A new cycle requires authoritative chart evidence that adds morphology information, not merely another ticker name or buy point. In particular, useful evidence would independently identify the Ascending Base pullback sequence/boundaries and provide enough Base-on-Base geometry to operationalize the qualitative “mostly above” region without fitting it to validation outcomes.

Until such evidence exists, P6 is **FROZEN — VALIDATION FAIL / NOT PRODUCTION-VALIDATED**.
