# P2 overlap and nesting semantics

P2 does not suppress provisional base candidates merely because their structural intervals overlap.

Pairwise interval relations are classified as:

- `DISJOINT`: no shared structural interval;
- `TOUCHING`: one candidate ends exactly where another begins;
- `OVERLAP`: intervals intersect but neither fully contains the other;
- `CONTAINS`: the left candidate fully contains the right candidate;
- `WITHIN`: the left candidate is fully contained by the right candidate;
- `IDENTICAL`: both structural intervals have the same start and end dates.

These relations are descriptive evidence only. P2 does not decide that an outer or inner candidate is the correct O'Neil base, and it does not rank, delete, merge, or deduplicate candidates based on morphology assumptions. Later pattern-specific layers may use nesting/overlap evidence when deciding whether a structure is a Flat Base, Double Bottom, Cup family member, Base-on-Base, or an ambiguous/fault case.

The relation is defined from the frozen structural `start_date` and `end_date`, never from the current `asof_date`. Therefore merely advancing the observation horizon cannot change the relation between two already-confirmed segments unless one of those provisional segments legitimately transitions from `DECLINE_CONFIRMED` to `RECOVERY_CONFIRMED` after a new structural recovery landmark becomes PIT-known.
