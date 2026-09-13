# P6 Advanced Patterns — Final Verdict

Date: 2026-09-13

Verdict: **DEFERRED / NOT PRODUCTION-VALIDATED / FROZEN UNTIL NEW AUTHORITATIVE MORPHOLOGY EVIDENCE EXISTS**

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only. Frozen P3/P4/P5/P8 core morphology is unchanged.

## Cycle 1 — completed failed validation

Cycle 1 used 10 authoritative DEVELOPMENT positives and locked STT (`ASCENDING_BASE`) plus C (`BASE_ON_BASE`) as untouched VALIDATION.

DEVELOPMENT achieved 10/10 source-dimension MATCH and zero candidate identity `STATUS_CONFLICT`, but detector-state evidence was weak: Ascending Base 1 recognized / 1 ambiguous / 3 rejected; Base-on-Base 1 recognized / 4 ambiguous.

After freeze, STT/C were opened exactly once. Both source dimensions MATCH, but STT was `ASCENDING_BASE_REJECTED` and C was `BASE_ON_BASE_AMBIGUOUS`. Cycle 1 therefore ended **VALIDATION FAIL / NOT PRODUCTION-VALIDATED**. STT/C are consumed evidence and may never again be treated as untouched validation.

Cycle 1 evidence remains in `docs/decisions/p6-development-freeze-v1.md`; one-shot run `34750413835`, artifact `10315775412`, digest `sha256:618c72a7accbb9b5434db9040e2bad645bf0435de21b32ffac019bfe4d83ca16`.

## Cycle 2 — fresh authoritative evidence search

Cycle 2 was opened because the user required P6 to continue until it either reached a defensible validation verdict or genuinely hit the boundary of available authoritative evidence.

Fresh locked corpus: `data/p6/labels_cycle2_v0.csv`.

DEVELOPMENT:

- Ascending Base: AVGO, TME, CCJ, SNOW, NAVN;
- Base-on-Base: META, TRV, SE, JLL, SEI.

Reserved untouched VALIDATION before DEVELOPMENT scoring:

- MRX — `ASCENDING_BASE`;
- CAT — `BASE_ON_BASE`.

Cycle 2 source audit: `docs/p6-cycle2-source-audit.md`.
Terminal record: `docs/decisions/p6-cycle2-terminal-verdict.md`.

### Final Cycle 2 DEVELOPMENT evidence

Execution commit: `9cab74ace28a55f7715b7bf1bdecddf2cee758e4`.
Workflow run: `34753213531`.
Artifact id: `10316012884`.
Artifact digest: `sha256:303276ed83abae1f74b83f690d102fdf4c5a6a9c7e2bb1aada8e31d50a93db26`.

```text
all DEVELOPMENT                     9 MATCH / 1 MISS_PATTERN
candidate identity STATUS_CONFLICT  0

ASCENDING_BASE                      5/5 MATCH
candidate resolution                5/5 SOURCE_EQUIVALENT_MULTIPLE
presentation detector state         4 RECOGNIZED / 1 REJECTED

BASE_ON_BASE                        4/5 MATCH / 1 MISS_PATTERN
candidate resolution                4 SOURCE_EQUIVALENT_MULTIPLE / 1 NONE
presentation detector state         4 AMBIGUOUS / 1 NO_MATCH
```

AVGO's source pivot is pre-split 1151.82; the explicit 10-for-1 adjustment yields an exact source-dimension match against adjusted OHLCV. Yet five algorithmic candidates remain source-equivalent because the authoritative source does not publish a detector-comparable start/pullback landmark set. Their detector states disagree.

META is a genuine `MISS_PATTERN`: IBD/MarketSurge explicitly identifies the 602.95 flat base as part of a base-on-base formation, but composition of the frozen core candidates emits no Base-on-Base candidate at that as-of date.

## Why Cycle 2 stops before VALIDATION

The four core families were not validated by choosing whichever internal candidate happened to look best. P6 must meet the same discipline.

Cycle 2 found many additional authoritative named examples and exact pivots, so example count is no longer the blocker. The blocker is **authoritative morphology resolution**.

For `ASCENDING_BASE`, IBD/MarketSurge clearly specifies three moderate pullbacks with successively higher highs/lows, generally 9–16 weeks, and the pattern high as buy point. But the published examples usually omit exact pullback dates/prices and detector-comparable boundaries. Every fresh DEVELOPMENT example therefore has multiple source-equivalent internal candidates. Choosing among them from detector state would be circular.

For `BASE_ON_BASE`, IBD/O'Neil clearly specifies a breakout from the first base, less than the normal roughly 20%–25% advance before the next consolidation, and a later base that forms on top of the first and usually finds support around the prior base top. Current wording allows `entirely or mostly above`. The authoritative material does not supply a universal numerical boundary for `mostly above` or a numerical support tolerance. Inventing an overlap percentage from DEVELOPMENT would be research tuning rather than source-grounded quantification. Fixing META by loosening P3/P4/P5/P8 constituent morphology would violate the frozen-core boundary.

Therefore the DEVELOPMENT contract cannot be defensibly frozen for a one-shot Cycle 2 test.

### MRX and CAT remain untouched

MRX and CAT were **not opened**. Consuming them now would not answer the unresolved specification problem and would waste the untouched test set. They remain reserved evidence, not validation results and not tuning targets.

## Production consequence

- `ASCENDING_BASE` remains outside `oneil-pattern-output-v2`.
- `BASE_ON_BASE` remains outside `oneil-pattern-output-v2`.
- P3/P4/P5/P8 core remains frozen and unchanged.
- No downstream consumer may describe P6 as P8-equivalent or production-validated.
- Trading returns, CAGR, PF, FWD1, breakout success, entry optimization and portfolio outcomes remain prohibited rescue evidence.

## Reopen condition

Do not open Cycle 3 merely because another IBD article names an Ascending Base or Base-on-Base or publishes another buy point.

P6 should be reopened only if new authoritative evidence supplies a missing operational dimension, such as:

1. exact labelled Ascending Base pullback landmarks or an unambiguous detector-comparable start/end boundary;
2. an authoritative quantitative definition of Base-on-Base `mostly above` / support-at-prior-base-top geometry; or
3. an authoritative labelled MarketSurge dataset that independently resolves candidate identity.

Until then, additional detector tuning would create unsupported precision rather than improve validation.

## Final interpretation

Cycle 1 proved the then-frozen P6 representation failed untouched morphology validation. Cycle 2 then performed the requested deeper search with a fresh authoritative corpus and demonstrated that the remaining obstacle is not effort or named-example count: it is missing authoritative landmark/overlap semantics required for machine validation at the same standard as the four core patterns.

Accordingly P6 is now terminally frozen as:

**DEFERRED / NOT PRODUCTION-VALIDATED / REOPEN ONLY ON NEW AUTHORITATIVE MORPHOLOGY EVIDENCE.**
