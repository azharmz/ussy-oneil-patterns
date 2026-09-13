# P8 preregistration — open-right-edge Flat Base observation

Date: 2026-09-13
Status: PREREGISTERED DEVELOPMENT experiment

## Problem

Independent DEVELOPMENT evidence now shows the same structural gap in two Flat Base examples:

- SNPS: source start 2023-04-04 is a confirmed P1 SWING_HIGH, but the following low is only confirmed on the source as-of/breakout date and P2 therefore exposes only a 15-session decline span.
- TW: source start 2024-10-15 is a confirmed P1 SWING_HIGH, but there is no confirmed P1 SWING_LOW after it by 2024-11-19; consequently P2 emits no candidate beginning at the source start.

This is not sufficient evidence to alter Flat Base duration/tightness thresholds. It is sufficient evidence that a fully confirmed high-low-high structural segment is not the only representation needed for a base that is still open at the current right edge.

## Contract constraint

`p1-landmark-v1` remains frozen. P2 may consume only confirmed P1 landmarks and must not rebuild a hidden swing detector.

Therefore this experiment MUST NOT fabricate an as-of SWING_LOW/SWING_HIGH or backdate confirmation.

## Experimental structure

Add a DEVELOPMENT-only, label-agnostic `OPEN_RIGHT_EDGE` Flat observation with these semantics:

1. start = any confirmed P1 `SWING_HIGH` known by `asof_date`;
2. observation end = `asof_date` (information horizon, explicitly NOT a structural landmark);
3. observed low/high/close statistics are descriptive facts from raw OHLC inside `[start.price_date, asof_date]`;
4. duration is the inclusive session count across that observed interval;
5. pivot candidate remains the confirmed start-high price/date under the frozen Flat Base pivot contract;
6. the existing Flat Base duration/depth/tightness/wide-loose thresholds are reused unchanged;
7. output must carry an explicit status/evidence marker showing that the candidate is an open-right-edge observation rather than a confirmed P2 segment.

## Enumeration rule

At runtime, enumerate the structure from ALL eligible confirmed P1 SWING_HIGH starts; never select the start from an authoritative label.

Multiple plausible starts may coexist. The evaluator may rank them only after detector output exists, exactly as it does for other candidates.

## PIT / prefix semantics

For an as-of date T:

- only bars `date <= T` are available;
- only P1 highs with `confirmed_date <= T` are eligible starts;
- the observation end is T by definition and is never represented as a confirmed turn;
- extending the prefix from T to T+1 may extend the same open observation, which is expected and must be distinguishable from stable confirmed structural candidates.

## Promotion rule

This remains P8 experimental assembly until DEVELOPMENT evidence shows whether it resolves source-aligned right-edge bases without causing unacceptable structural explosion. It does not revise frozen P2 or production semantics yet.

If supported, a later versioned P2/production contract revision may adopt an explicit open-base state. If unsupported, remove the experiment without changing P1.

## Guardrails

- DEVELOPMENT only;
- NFLX VALIDATION remains locked;
- no threshold changes in this slice;
- no returns/performance inputs;
- no source label consulted at runtime;
- no fabricated structural landmark;
- confirmed and open-right-edge candidate identities remain distinct.
