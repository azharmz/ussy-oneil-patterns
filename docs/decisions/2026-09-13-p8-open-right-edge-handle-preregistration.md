# P8 OPEN_RIGHT_EDGE handle preregistration

Date: 2026-09-13

Status: PREREGISTERED FOR DEVELOPMENT

## Problem

Canonical Cup-with-Handle currently requires a completed native handle sequence:

`RIGHT_RIM/HANDLE_HIGH -> HANDLE_LOW -> HANDLE_RECOVERY`

P8 DEVELOPMENT shows a source-grounded case where the cup and handle pullback are already observable at the evaluation horizon, but a later confirmed recovery-high does not yet exist.

FOUR 2024 is the motivating independent case:

- source start precision: February 2024;
- canonical recognized cup: left rim 2024-02-12, trough 2024-04-25, right rim 2024-08-26;
- right rim price: ~84.26, equal to the authoritative pivot;
- confirmed post-rim handle low: 2024-09-10;
- no confirmed post-low swing high exists by the 2024-09-20 as-of horizon.

The current completed-handle representation therefore misses the source-described instance and selects older completed handles instead.

## Revision under test

Add an explicit DEVELOPMENT candidate semantics:

`OPEN_RIGHT_EDGE_HANDLE:p8-open-right-edge-handle-v0.1`

An observation is eligible only when:

1. the underlying cup body is already `CUP_RECOGNIZED` under existing cup-body semantics;
2. cup right rim is a confirmed P1 `SWING_HIGH`;
3. at least one confirmed P1 `SWING_LOW` occurs after that right rim and is known by `asof_date`;
4. no confirmed P1 `SWING_HIGH` occurs after the selected handle low by `asof_date` (otherwise normal completed-handle assembly owns the case);
5. the observation horizon is the explicit `asof_date`, never a fabricated recovery landmark.

Handle geometry uses:

- `handle_high = cup.right_rim`;
- `handle_low = confirmed post-rim low`;
- duration = session count from handle high through the as-of observation horizon;
- depth = `(handle_high - handle_low) / handle_high`;
- upper-half test = existing cup-midpoint rule.

Existing handle thresholds remain unchanged:

- minimum duration: 5 sessions;
- below cup midpoint: hard rejection;
- depth > 12%: `AMBIGUOUS` (`DEEP_HANDLE_EXCEPTIONAL`);
- otherwise: recognized.

The canonical pivot remains the persisted handle-high/right-rim price. No label value is used to choose the candidate or pivot.

## PIT / leakage guardrails

- no bar after `asof_date` may enter the observation;
- `asof_date` is an observation horizon, not a P1 landmark;
- no recovery-high is invented;
- if a confirmed post-low high later becomes available, the completed native handle representation supersedes the open observation for that later horizon;
- NFLX VALIDATION remains locked and must not be executed while this semantics is being tuned.

## Expected diagnostic consequence

FOUR should gain a source-aligned CWH candidate with February start and ~84.26 pivot if the existing cup/handle gates support it.

CTSH is not an acceptance target for this revision. Its January-2004 cup body currently carries independent cup-body morphology faults; those remain a separate P8 question.
