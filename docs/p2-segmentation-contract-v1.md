# P2 Candidate Base Segmentation Contract v1

Status: FROZEN
Date: 2026-09-12
Contract version: `p2-segmentation-v1`

## Purpose

This document freezes the handoff from P2 Candidate Base Segmentation to the later morphology layers.

P2 does not classify Flat Base, Double Bottom, Cup, Cup-with-Handle, Ascending Base, or Base-on-Base. It converts frozen P1 structural turns into provisional, morphology-neutral base regions with explicit point-in-time semantics and descriptive geometry.

## Input contract

P2 consumes only P1 `LandmarkCandidate` objects conforming to `p1-landmark-v1`.

P2 may not rebuild or hide an independent swing/extrema detector.

Only candidates with `confirmed_date <= asof_date` may participate in a historical as-of run.

## Structural sequence

The v1 provisional region is built from:

1. `SWING_HIGH` = candidate structural start;
2. subsequent `SWING_LOW` = trough;
3. optional subsequent confirmed `SWING_HIGH` = recovery.

P2 assigns no pattern class to this sequence.

## Stage semantics

Stable v1 stages:

- `DECLINE_CONFIRMED`
- `RECOVERY_CONFIRMED`

For `DECLINE_CONFIRMED`:

- recovery is absent;
- `start_date = start.price_date`;
- `end_date = trough.price_date`;
- all recovery-dependent features are `None`.

For `RECOVERY_CONFIRMED`:

- recovery is present and PIT-known;
- `start_date = start.price_date`;
- `end_date = recovery.price_date`;
- recovery-dependent features are populated.

`asof_date` is an information cutoff only and must never be substituted for a structural boundary.

## Stable output representation

The stable v1 representation is `BaseSegmentCandidate` with:

- `start`
- `trough`
- `recovery`
- `stage`
- `start_date`
- `end_date`
- `confirmed_date`
- `duration_sessions`
- `decline_sessions`
- `recovery_sessions`
- `depth_pct`
- `recovery_pct`
- `recovery_to_start_ratio`
- `recovered_depth_fraction`
- `evidence`

The `evidence` mapping is extensible, but later morphology code must not require undocumented evidence keys without a contract revision.

## Geometry semantics

Session counts are inclusive over structural endpoints.

- `duration_sessions`: start high through current structural end;
- `decline_sessions`: start high through trough;
- `recovery_sessions`: trough through recovery high, when recovery is confirmed;
- `depth_pct = (start_high - trough) / start_high`;
- `recovery_pct = (recovery_high - trough) / trough`;
- `recovery_to_start_ratio = recovery_high / start_high`;
- `recovered_depth_fraction = (recovery_high - trough) / (start_high - trough)`.

`recovered_depth_fraction == 1.0` means the recovery has returned exactly to the starting high. Values above 1.0 remain descriptive geometry and do not imply breakout, entry, or trading eligibility.

## Boundary evidence

P1 boundary evidence remains visible in P2.

P2 does not silently discard a provisional base because its start, trough, or recovery is near the observed-series boundary. Later morphology/fault layers may interpret boundary evidence explicitly.

## Overlap and nesting semantics

Pairwise provisional segment relations are classified as:

- `DISJOINT`
- `TOUCHING`
- `OVERLAP`
- `CONTAINS`
- `WITHIN`
- `IDENTICAL`

P2 retains all provisional candidates. It does not merge, rank, suppress, or choose a winner merely because candidates overlap or nest.

Later morphology layers may interpret these relations differently for Flat Base, Double Bottom, Cup family, Base-on-Base, and ambiguity/fault handling.

## PIT invariants

The v1 implementation is guarded by tests asserting that:

- future bars alone cannot rewrite an already-known segment;
- a future-confirmed recovery cannot leak into an earlier prefix;
- `DECLINE_CONFIRMED` may upgrade to `RECOVERY_CONFIRMED` only when the recovery is PIT-known;
- later structural turns may create additional segments without rewriting an already-completed earlier segment;
- `asof_date` never becomes a structural boundary.

## Out of scope

P2 does not decide:

- whether a segment is a valid O'Neil base;
- Flat Base / Double Bottom / Cup / CWH classification;
- pivot price;
- breakout;
- entry timing;
- CAN SLIM eligibility;
- portfolio construction;
- sell logic;
- return-based quality.

## Versioning rule

`p2-segmentation-v1` is frozen for morphology development.

Bug fixes that preserve the semantics above may remain v1. Any material change to stage vocabulary, boundary semantics, mandatory output fields, geometry definitions, overlap/nesting behavior, or PIT semantics requires a new contract version and migration note.

## Morphology handoff

P3+ morphology layers may consume `BaseSegmentCandidate` and its relation evidence to decide pattern-specific structure. They must not silently redefine P1 landmarks or P2 structural boundaries.
