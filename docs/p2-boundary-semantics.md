# P2 Candidate Boundary Semantics

Status: active P2 specification

## Purpose

P2 converts frozen `p1-landmark-v1` structural turns into morphology-neutral provisional base regions. This document defines what the start and end dates mean so later morphology layers do not reinterpret the same segment differently.

## Start semantics

`start_date` is always the `price_date` of the structural `SWING_HIGH` that begins the decline.

It is not:

- the date that swing was later confirmed;
- the first bar of an arbitrary rolling window;
- the current `asof_date`;
- a morphology-specific left rim chosen later.

`confirmed_date` separately records when the segment was first knowable from the available evidence.

## End semantics

P2 has two explicit stages.

### `DECLINE_CONFIRMED`

A `SWING_HIGH -> SWING_LOW` sequence is known but no later recovery `SWING_HIGH` is yet confirmed.

- `recovery = None`
- `end_date = trough.price_date`
- `recovery_pct = None`
- advancing `asof_date` alone does not move `end_date`

This represents a provisional decline/base candidate, not a claim that the base has structurally ended at the trough.

### `RECOVERY_CONFIRMED`

A later `SWING_HIGH` has become PIT-known.

- `recovery` is populated
- `end_date = recovery.price_date`
- `recovery_pct` is populated
- `confirmed_date` is at least the recovery landmark's `confirmed_date`

The segment can now be interpreted by later morphology classifiers, but P2 still does not label it Flat, Double Bottom, Cup, etc.

## `asof_date` rule

`asof_date` is an information cutoff only. It is never substituted for a structural boundary.

Therefore an unchanged `SWING_HIGH -> SWING_LOW` candidate observed on two later `asof_date` values keeps the same `start_date`, `end_date`, duration, and stage until a new frozen-P1 structural landmark becomes confirmed.

## Why this matters

Without this distinction, an incomplete base would appear to grow every day merely because time advanced, mixing observation horizon with morphology. P2 instead changes geometry only when new structural evidence becomes PIT-known.
