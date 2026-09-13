# P6 Authoritative Morphology Validation Protocol v0

Date opened: 2026-09-13

Status: **DEVELOPMENT OPEN / VALIDATION LOCKED**

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only. Frozen P3/P4/P5/P8 core detectors are immutable inputs and must not be tuned or reopened by this cycle.

## Standard

P6 now follows the same evidence sequence used by the four core patterns:

1. commit authoritative labels before detector comparison;
2. separate DEVELOPMENT from untouched VALIDATION;
3. run PIT-safe morphology predictions on DEVELOPMENT only;
4. fix only P6-specific assembly/adapter defects exposed by DEVELOPMENT;
5. freeze versions, corpus, evidence commit, workflow run and artifact;
6. execute VALIDATION once after freeze;
7. do not tune after VALIDATION;
8. issue a final verdict with explicit remaining debt.

## Corpus design

Committed corpus: `data/p6/labels_v0.csv`.

DEVELOPMENT:
- 5 `ASCENDING_BASE` authoritative examples;
- 5 `BASE_ON_BASE` authoritative examples.

Locked VALIDATION:
- `p6-label-0011` — STT / `ASCENDING_BASE`;
- `p6-label-0012` — C / `BASE_ON_BASE`.

The DEVELOPMENT runner may reveal VALIDATION example IDs only to prove the split is locked. It must not fetch, score, print, or otherwise inspect VALIDATION source dimensions.

## Authoritative-source rule

Labels are sourced from Investor's Business Daily / MarketSurge statements that explicitly name the advanced pattern. Comparable source dimensions are scored only when published:

- named pattern;
- source start anchor when explicitly described, at its published DAY or MONTH precision;
- buy point / pivot price when explicitly published;
- pivot date or depth only if the source explicitly supplies a detector-comparable value.

No absent dimension may be invented from hindsight.

## Frozen-core boundary

P6 validation may consume:
- frozen P1 confirmed landmarks;
- frozen core morphology predictions as component summaries for Base-on-Base;
- existing R2 -> Yahoo -> Tiingo source routing;
- existing source-dimension evaluator and candidate-identity audit.

P6 validation must not change:
- P3 Flat Base;
- P4 Double Bottom;
- P5 Cup family;
- P8 labels, adapters, thresholds, verdict or production v2.

## P6 validation adapter

Initial adapter: `p6-advanced-prediction-adapter-v0.1`.

Ascending Base:
- enumerates label-agnostic P1 alternating `HIGH-LOW-HIGH-LOW-HIGH-LOW-HIGH` subsequences within the already-frozen maximum duration;
- builds the frozen `ascending-base-v2` geometry;
- uses the third pre-pullback high as the source-comparable pivot;
- preserves detector state/faults separately from source agreement.

Base-on-Base:
- composes only already-`RECOGNIZED` frozen core predictions;
- does not create or tune a second core detector;
- uses the second component's pivot as the source-comparable buy point;
- preserves `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` state separately from source agreement.

## Predeclared scoring

- context lookback: 320 calendar days;
- source start tolerance: 10 calendar days for DAY precision, exact calendar month for MONTH precision;
- pivot-date tolerance: 3 calendar days;
- pivot-price tolerance: 1%;
- source dimensions absent from the article are not scored;
- returns and breakout outcomes are prohibited.

Any change to these rules before DEVELOPMENT freeze must be versioned and justified as a P6 validation-method defect, never from trading performance.
