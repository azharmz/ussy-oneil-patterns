# P6 Validation Cycle 2 — Terminal Verdict

Date: 2026-09-13

## Verdict

**DEVELOPMENT STOP / FROZEN — NOT PRODUCTION-VALIDATED; AUTHORITATIVE MORPHOLOGY EVIDENCE INSUFFICIENT FOR A DEFENSIBLE ONE-SHOT VALIDATION.**

This supersedes the idea that P6 should keep iterating merely because more named examples can be found. Cycle 2 deliberately searched for a fresh authoritative corpus and reached the evidence boundary before opening its untouched validation rows.

## What Cycle 2 achieved

A fresh authoritative corpus was locked in `data/p6/labels_cycle2_v0.csv`:

- 5 new DEVELOPMENT `ASCENDING_BASE` positives: AVGO, TME, CCJ, SNOW, NAVN;
- 5 new DEVELOPMENT `BASE_ON_BASE` positives: META, TRV, SE, JLL, SEI;
- untouched VALIDATION reserved before DEVELOPMENT scoring: MRX (`ASCENDING_BASE`) and CAT (`BASE_ON_BASE`).

Cycle 1 validation rows STT/C were not reused.

The final DEVELOPMENT execution was commit `9cab74ace28a55f7715b7bf1bdecddf2cee758e4`, Actions run `34753213531`, artifact digest `sha256:303276ed83abae1f74b83f690d102fdf4c5a6a9c7e2bb1aada8e31d50a93db26`.

Final DEVELOPMENT result:

```text
all DEVELOPMENT                     9 MATCH / 1 MISS_PATTERN
identity STATUS_CONFLICT            0

ASCENDING_BASE                      5/5 MATCH
candidate resolution                5/5 SOURCE_EQUIVALENT_MULTIPLE
presentation detector state         4 RECOGNIZED / 1 REJECTED

BASE_ON_BASE                        4/5 MATCH / 1 MISS_PATTERN
candidate resolution                4 SOURCE_EQUIVALENT_MULTIPLE / 1 NONE
presentation detector state         4 AMBIGUOUS / 1 NO_MATCH
```

AVGO's published pre-split 1151.82 pivot was compared to adjusted OHLCV using the explicit 10-for-1 split factor. The source dimensions then MATCH. The selected presentation candidate is `REJECTED/TOO_LONG`, but the five source-equivalent candidates disagree on detector state; the authoritative article does not publish a detector-comparable start boundary that would identify which candidate is the intended morphology.

META is a genuine `MISS_PATTERN`: IBD/MarketSurge explicitly calls the 602.95 flat base part of a base-on-base formation, while the frozen P6 assembly emits no Base-on-Base candidate at that as-of date.

## Why DEVELOPMENT cannot be defensibly frozen for one-shot validation

The problem is no longer a shortage of named examples. It is missing authoritative **landmark resolution**.

### ASCENDING_BASE

IBD/MarketSurge provides a strong qualitative rule: three moderate pullbacks, successive higher highs and higher lows, roughly 9–16 weeks, and the pattern high as the buy point. Cycle 2 recovered multiple fresh examples with exact pivots.

But most published examples do not provide exact pullback dates/prices or a detector-comparable start boundary. Consequently all five Cycle 2 DEVELOPMENT rows have multiple source-equivalent algorithmic candidates. The evaluator can verify pattern name and pivot, but cannot authoritatively decide which internal landmark sequence is the intended pattern. Selecting the candidate whose detector state looks best would be circular tuning.

### BASE_ON_BASE

Authoritative IBD/O'Neil guidance says:

- the first base breaks out;
- the advance before the next base is less than the normal ~20%–25% profit-taking move;
- the later base forms on top of the prior base and usually finds support around the top of the prior base;
- current wording allows the later base to be `entirely or mostly above` the first base;
- the current/second base supplies the new buy point.

However, the authoritative material does **not** define a universal numeric boundary for `mostly above` or a numeric tolerance for `support around the top of the prior base`. Four fresh positives therefore remain `AMBIGUOUS` under the conservative implementation, and META is missed entirely by composition of the frozen core-base candidates.

Creating a percentage overlap threshold from these ten DEVELOPMENT examples would be research-derived tuning, not an O'Neil/IBD rule. Loosening frozen P3/P4/P5/P8 constituent morphology to make META appear is explicitly outside P6 scope.

## Why MRX and CAT are NOT opened

The user required the same validation discipline as the four core families. Under that discipline, untouched validation is opened only after the DEVELOPMENT morphology contract is defensibly frozen.

Cycle 2 did **not** reach that gate. Opening MRX/CAT now would consume the only fresh untouched rows without resolving the missing authoritative landmark semantics. Therefore:

- MRX remains untouched;
- CAT remains untouched;
- no one-shot Cycle 2 VALIDATION claim is made;
- neither row may be used to choose a threshold or repair DEVELOPMENT.

This is a stronger validation outcome than opening them anyway: it preserves the distinction between a failed model and a model whose authoritative specification is not sufficiently operationalized to justify the test.

## Production consequence

No change to production:

- `ASCENDING_BASE` stays out of `oneil-pattern-output-v2`;
- `BASE_ON_BASE` stays out of `oneil-pattern-output-v2`;
- frozen P3/P4/P5/P8 core remains untouched;
- Cycle 1 remains historical failed validation evidence;
- Cycle 2 is frozen as an evidence-limited DEVELOPMENT stop.

## Reopen condition

P6 should **not** be reopened merely because another IBD article names an Ascending Base or Base-on-Base.

A future cycle is justified only if new authoritative evidence supplies at least one of the missing operational dimensions, for example:

1. labelled charts/data with exact Ascending Base pullback landmarks or an unambiguous detector-comparable start/end boundary; or
2. an authoritative quantitative definition of Base-on-Base `mostly above` / support-at-prior-base-top semantics; or
3. an authoritative machine-readable/labelled MarketSurge corpus that resolves candidate identity independently of this detector.

Without such evidence, another cycle would only repeat sparse pattern-name/pivot matching or tune research thresholds to examples.

## Final interpretation

P6 has now been pursued beyond the first failed validation cycle and through a fresh authoritative Cycle 2 DEVELOPMENT corpus. The remaining blocker is not effort or corpus count. It is the absence of authoritative morphology detail required to distinguish among algorithmic candidates and to quantify Base-on-Base overlap without invention.

Accordingly the defensible terminal state is:

**P6 ADVANCED PATTERNS — DEFERRED / NOT PRODUCTION-VALIDATED / FROZEN UNTIL NEW AUTHORITATIVE MORPHOLOGY EVIDENCE EXISTS.**
