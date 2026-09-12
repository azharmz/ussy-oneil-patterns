# P6 Ascending Base Contract v1

Contract id: `ascending-base-v1`

Status: **FROZEN FIRST PASS**

## Structural sequence

`HIGH -> LOW -> HIGH -> LOW -> HIGH -> LOW -> HIGH`

interpreted as three pullbacks followed by the third recovery peak.

## Frozen theory-grounded semantics

- exactly three structural pullbacks;
- successively higher troughs;
- successively higher recovery peaks;
- first-pass duration neighborhood: 45 to 80 observed sessions (9–16 week operationalization);
- market weakness, prior uptrend and moving-average support remain contextual evidence outside the pure morphology gate.

## Geometry

Frozen fields include:

- three pullback depths;
- two trough step-ups;
- three peak step-ups;
- mean/max pullback depth;
- pullback-depth dispersion;
- full duration;
- PIT confirmation date.

## States

- `ASCENDING_BASE_RECOGNIZED`
- `ASCENDING_BASE_REJECTED`
- `ASCENDING_BASE_AMBIGUOUS`

## Faults

Theory-grounded first-pass faults:

- `TOO_SHORT`
- `TOO_LONG`
- `NON_ASCENDING_TROUGHS`
- `NON_ASCENDING_PEAKS`

Research-only ambiguity:

- `PULLBACK_DEPTH_INCONSISTENT`

The current pullback-depth dispersion threshold (0.05) is explicitly research-only and must be validated from labelled morphology in P8, never trading returns.

## PIT semantics

Recognition requires all seven turns to be confirmed. Extending the session index with future dates cannot change geometry or state for an already-complete candidate. Confirmation date equals the latest required landmark confirmation date.

## Validation

Synthetic positive/negative/ambiguous fixtures cover:

- canonical ascending structure;
- nonascending troughs;
- nonascending peaks;
- too-short duration;
- too-long duration;
- irregular pullback depths;
- future-session-index invariance.
