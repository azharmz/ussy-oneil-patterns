# P2 PIT / Prefix-Stability Validation

P2 segmentation consumes only frozen P1 `LandmarkCandidate` objects that are known as of the requested `asof_date`.

## Invariants

1. Future bars alone must not rewrite a segment that was already fully determined by PIT-known landmarks.
2. A recovery landmark whose `confirmed_date` is later than `asof_date` must not affect the segment, even if its `price_date` is already visible in the frame.
3. A provisional segment may upgrade from `DECLINE_CONFIRMED` to `RECOVERY_CONFIRMED` only when the recovery landmark itself becomes PIT-known.
4. Once a completed first segment is known, later landmarks may create additional segments but must not silently rewrite the already-known first segment.
5. `asof_date` remains an information cutoff only. It never substitutes for a structural start/end boundary.

## Validation method

The test suite compares compact segment signatures across:

- truncated prefixes versus the full frame at the same `asof_date`;
- dates immediately before and at a recovery `confirmed_date`;
- earlier output versus later output after additional independent structural turns become known.

The signatures include stage, structural dates, confirmation date, duration geometry, and recovery geometry. Any difference before new PIT information becomes available is treated as repaint/look-ahead failure.

## Scope

This validates P2 segmentation semantics only. It does not validate Flat Base, Double Bottom, Cup, breakout, entry, or trading outcomes.
