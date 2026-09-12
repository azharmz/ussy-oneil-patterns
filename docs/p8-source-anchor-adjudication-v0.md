# P8 Source-Anchor Adjudication v0.1

Status: PREREGISTERED DEVELOPMENT SUPPORT
Date: 2026-09-13

## Purpose

Convert coarse but authoritative source anchors (week/month/date range) into reproducible trading-session dates without consulting detector output or post-pattern returns.

This contract exists because several high-priority P8 candidates have strong authoritative pattern labels but only week-level or month-level timing. They must not be promoted by inventing exact dates ad hoc.

## Guardrails

- Authoritative source semantics come first.
- Detector output must not be inspected before the adjudication rule is chosen.
- A coarse source period is not automatically a base boundary.
- OHLCV may be used only as a trading calendar and to resolve a source-specified structural event.
- A pivot/buy point may be used only when the authoritative source states it.
- If the source does not justify a structural rule, keep the candidate held back or mark it ambiguous.
- No post-pattern return is admissible.

## Frozen rules

`FIRST_SESSION`
: first available trading session inside a source-stated calendar range. Use only when the source semantics state that the event begins in that range and no price extremum is part of the source claim.

`LAST_SESSION`
: last available trading session inside a source-stated range. Use only for an explicitly period-ending source anchor.

`HIGHEST_HIGH`
: session with the highest raw daily high inside a source-stated left-rim/start range. Use only when the source explicitly says the base/cup begins from a peak or reversal in that range.

`LOWEST_LOW`
: session with the lowest raw daily low inside a source-stated bottom/pullback range. Use only when the source explicitly identifies that range as the pattern low/pullback.

`FIRST_PIVOT_CROSS`
: first session whose raw daily high exceeds a source-stated pivot/buy point inside a source-stated breakout date/week range. This resolves a breakout session; it must never discover the pivot itself.

## Fail-closed cases

Do not promote when:

- the source only names a month but gives no semantic clue for start/end selection;
- the cited pivot is absent or cannot be reconciled with the cited breakout range;
- multiple structural interpretations remain plausible;
- the OHLCV source required by the frozen routing policy is unavailable or fails QC;
- resolving a date would require consulting detector landmarks.

## Implementation

- `src/oneil_patterns/validation/adjudication.py`
- `tests/validation/test_p8_adjudication.py`

The helper accepts already-routed OHLCV so provider choice remains governed exclusively by `docs/p8-ohlcv-source-policy.md`.

## Immediate corpus use

This convention unblocks exact calendar adjudication for candidates where authoritative sources already provide enough structure, especially cases with:

- explicit breakout week plus stated pivot;
- explicit start/reversal range plus a named left-rim/peak event;
- explicit pullback ranges for advanced-pattern landmarks.

Candidates with only coarse month labels and no structural source anchor remain held back.
