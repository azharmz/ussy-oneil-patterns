# P8 Double Bottom undercut semantics v0.2

Date: 2026-09-13

Status: DEVELOPMENT REVISION

## Evidence

The first-pass `double-bottom-v1` contract hard-rejected any W where trough 2 did not undercut trough 1.

P8 now has three authoritative DEVELOPMENT Double Bottom examples:

- SEI 2024 — source-dimension MATCH; source-aligned W undercuts but is slightly short under the current duration gate;
- NVDA 2023 — source-dimension MATCH; canonical 47.61 pivot candidate is `DOUBLE_BOTTOM_RECOGNIZED` with clear undercut;
- SPOT 2025 — IBD/MarketSurge explicitly labels a Double Bottom with 621.20 buy point; canonical candidates reproduce 621.20 exactly but are rejected only because trough 2 does not undercut trough 1.

IBD educational wording states that in a Double Bottom the second bottom **usually** is lower than the first. That supports treating undercut as a strong characteristic rather than an absolute identity requirement.

## Revision

For DEVELOPMENT v0.2:

- `TOO_SHORT` remains a hard rejection pending separate duration adjudication;
- `TOO_DEEP` remains a hard rejection;
- `NO_SECOND_TROUGH_UNDERCUT` becomes an explicit ambiguity fault rather than a hard rejection;
- a candidate with no undercut may therefore be `DOUBLE_BOTTOM_AMBIGUOUS`, never `RECOGNIZED` solely by this revision;
- `SHALLOW_UNDERCUT` and `WEAK_MIDDLE_REBOUND` remain ambiguity faults;
- clear undercut plus all other gates may remain `RECOGNIZED`.

No numerical undercut threshold is changed. `MIN_CLEAR_UNDERCUT_PCT = 0.005` remains research-only.

## Why this is not label overfitting

The revision does not force SPOT to recognized status. It changes an absolute binary rejection into explicit ambiguity because both the authoritative named example and the theory wording contradict an absolute rule. Detector faults remain persisted.

## Deferred duration question

The 35-session / seven-week duration semantics remain unchanged in this slice. SEI shows that the current core-W boundary can be slightly shorter than the source-described completed base, but more evidence is required before changing the duration gate or its boundary semantics.

## Guardrails

No returns, breakout success, CAGR, PF, FWD1, or VALIDATION data are used. NFLX remains locked.
