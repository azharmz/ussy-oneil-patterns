# P4.2 Double Bottom Geometry Candidate

Status: IMPLEMENTED / CI PENDING

`DoubleBottomGeometry` is the morphology-neutral measurement layer for a W-like structural sequence.

It consumes existing P1/P2 structural landmarks only:

`left_high -> trough_1 -> middle_peak -> trough_2 -> optional right_recovery_high`

It does not assign `RECOGNIZED`, `REJECTED`, or `AMBIGUOUS` yet.

## Geometry fields

The candidate records:

- `duration_sessions`: inclusive span from left high to trough 2 or optional right recovery;
- `overall_depth_pct`: decline from left high to the deeper trough;
- `trough_spacing_sessions`: observed-session distance between trough 1 and trough 2;
- `trough2_vs_trough1_pct`: signed price difference of trough 2 relative to trough 1;
- `middle_peak_rebound_pct`: rebound from trough 1 to middle peak;
- `middle_peak_recovered_fraction`: fraction of the first decline recovered at the middle peak;
- `right_recovery_pct`: optional rebound from trough 2 to right recovery high;
- `right_recovery_to_left_high_ratio`: optional right recovery high / left high;
- `confirmed_date`: latest confirmation date among the structural landmarks used.

## Sign semantics

`trough2_vs_trough1_pct < 0` means trough 2 undercuts trough 1.

`trough2_vs_trough1_pct > 0` means trough 2 is higher than trough 1.

P4.2 deliberately records both cases. The audited canonical undercut rule belongs to the later detector/state policy, not the raw geometry builder.

## PIT semantics

The geometry cannot be considered known before the latest `confirmed_date` of the landmarks it uses. Adding an optional right recovery moves the candidate's confirmation date forward accordingly.

No future-bar inference or backdating is permitted.

## Theory vs research distinction

Theory-grounded constraints already audited in P4.1:

- minimum Double Bottom duration: 7 weeks / operationalized as 35 observed trading sessions;
- maximum depth: 40%;
- canonical second trough undercuts the first trough.

Still research-only and not yet thresholded:

- minimum trough spacing;
- minimum middle-peak rebound;
- required undercut magnitude;
- recovery completeness/asymmetry tolerances.

These must be tested from morphology fixtures/labels, not trading returns.
