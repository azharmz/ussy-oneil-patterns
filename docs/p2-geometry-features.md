# P2 Geometry Feature Semantics

Status: draft contract for P2 base segmentation.

P2 remains morphology-neutral. These features describe the structural region only; they do not classify Flat Base, Double Bottom, Cup, or Cup-with-Handle.

## Session-count semantics

All session counts are inclusive over observed trading sessions in the input frame.

- `duration_sessions`: start structural high through current structural end.
- `decline_sessions`: start structural high through trough.
- `recovery_sessions`: trough through confirmed recovery high; `None` while stage is `DECLINE_CONFIRMED`.

No count is extended to `asof_date` merely because more observation time has elapsed.

## Price geometry

Let:

- `H0` = start structural-high price;
- `L` = trough price;
- `H1` = confirmed recovery-high price, if available.

Then:

- `depth_pct = (H0 - L) / H0`
- `recovery_pct = (H1 - L) / L`
- `recovery_to_start_ratio = H1 / H0`
- `recovered_depth_fraction = (H1 - L) / (H0 - L)`

Interpretation:

- `recovery_to_start_ratio = 1.0` means recovery high returned exactly to the prior structural high.
- `recovered_depth_fraction = 1.0` means the original start-to-trough price distance has been fully recovered.
- `recovered_depth_fraction > 1.0` is permitted; it means the confirmed recovery high moved above the original structural high. P2 records that fact without assigning breakout or trading semantics.

## Stage rules

### `DECLINE_CONFIRMED`

Required:

- start high and trough are known PIT-safe;
- decline features are present;
- all recovery-specific fields are `None`.

### `RECOVERY_CONFIRMED`

Required:

- a later recovery `SWING_HIGH` is known PIT-safe;
- recovery session count and all recovery geometry fields are present.

## Non-goals

P2.3 does not define:

- minimum/maximum acceptable base depth;
- minimum duration for any O'Neil pattern;
- breakout/pivot validity;
- entry or return quality;
- pattern-specific thresholds.

Those belong to later morphology/validation layers and must not be inferred from these descriptive features alone.
