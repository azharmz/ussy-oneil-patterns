# P4 Double Bottom Contract v2

Contract id: `double-bottom-v2`

Status: P8 DEVELOPMENT REVISION - NOT FINAL-FROZEN
Date: 2026-09-13

This revision supersedes the first-pass state mapping in `double-bottom-v1` for P8 DEVELOPMENT validation. Geometry, pivot semantics and numerical research bands are unchanged.

## Structural sequence

`left_high -> trough_1 -> middle_peak -> trough_2 -> optional right_recovery_high`

P4 continues to reuse frozen P1/P2 structural evidence and does not create a separate swing detector.

## Hard gates

Unchanged:

- minimum core-W duration: 35 observed sessions measured from `left_high` through `trough_2`;
- maximum depth: 40 percent.

Failure of either gate maps to `DOUBLE_BOTTOM_REJECTED`.

## Undercut semantics revised

P8 DEVELOPMENT now includes three authoritative source-aligned Double Bottom examples. NVDA 2023 has a clear undercut and remains `DOUBLE_BOTTOM_RECOGNIZED`. SPOT 2025 reproduces the published 621.20 pivot but the source-aligned W does not undercut trough 1. SEI 2024 has an undercut but remains slightly short under the unchanged duration gate.

Source theory material describes the second bottom as usually lower than the first. Therefore v2 treats the undercut as a strong morphology characteristic rather than an absolute identity requirement.

State mapping:

- `TOO_SHORT` -> `REJECTED`;
- `TOO_DEEP` -> `REJECTED`;
- `NO_SECOND_TROUGH_UNDERCUT` -> `AMBIGUOUS` with the fault retained;
- `SHALLOW_UNDERCUT` -> `AMBIGUOUS`;
- `WEAK_MIDDLE_REBOUND` -> `AMBIGUOUS`;
- all hard gates pass and no ambiguity fault -> `RECOGNIZED`.

A no-undercut case is never promoted directly to recognized by this revision.

## Research-only bands

Unchanged:

- clear undercut magnitude at least 0.5 percent below trough 1;
- clear middle-peak recovery at least 50 percent of the first decline recovered.

These remain research parameters, not official numerical rules.

## Duration debt

The 35-session operationalization is not changed in v2. SEI shows a possible boundary-semantics issue because the core W can be slightly shorter than the source-described completed base. That question remains `UNRESOLVED` until additional authoritative duration evidence is adjudicated.

## PIT and guardrails

Only evidence confirmed by `asof_date` participates. Optional right recovery cannot backdate recognition or alter core-W duration. No trading-return metrics or VALIDATION data are used. NFLX remains locked.

Decision record: `docs/decisions/2026-09-13-p8-double-bottom-undercut-v0.2.md`.
