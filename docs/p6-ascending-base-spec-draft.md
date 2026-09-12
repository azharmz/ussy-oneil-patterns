# P6 Ascending Base — Morphology Specification Draft

Status: **DRAFT / THEORY-AUDITED FIRST PASS**

## Scope

P6 Ascending Base must compose frozen P1/P2 structural turns. It must not create a separate swing detector.

## Audited IBD guidance

Official IBD educational material describes an Ascending Base as:

- a rare bullish base made of **three pullbacks / retreats**;
- each successive retreat occurs at a **higher price level**, producing higher highs and higher lows;
- the full structure typically develops over approximately **9 to 16 weeks**;
- pullbacks are relatively mild compared with a major base, with official examples/guidance spanning roughly the high-single-digits into the low/mid-20% area depending on the example;
- the pattern often appears while the general market is weak, demonstrating relative strength.

Market weakness and moving-average support are contextual evidence, not morphology gates in #33.

## Structural sequence

First-pass structural representation:

`peak_1 -> trough_1 -> peak_2 -> trough_2 -> peak_3 -> trough_3 -> recovery_peak`

with alternating P1 types:

`HIGH -> LOW -> HIGH -> LOW -> HIGH -> LOW -> HIGH`

The final recovery peak is required for a fully observed first-pass morphology candidate. A candidate missing the final recovery remains incomplete rather than being backfilled from future data.

## Theory-grounded morphology requirements

1. Exactly three structural pullback legs are represented.
2. Troughs are successively higher:
   `trough_1 < trough_2 < trough_3`.
3. Recovery peaks are successively higher:
   `peak_1 < peak_2 < peak_3 < recovery_peak` for a textbook first-pass candidate.
4. Full pattern duration should fall in the broad IBD guidance neighborhood of **9–16 weeks**.

Operationalization for daily observed sessions:

- 9 weeks ~= **45 observed trading sessions**;
- 16 weeks ~= **80 observed trading sessions**.

These duration bounds are first-pass theory translations, not return-optimized parameters.

## Pullback geometry

For each retreat `i`:

`pullback_i_pct = (peak_i - trough_i) / peak_i`

The audited IBD material does not support one single universal hard numerical pullback range across all examples. Therefore P6 will initially measure all three pullback depths and keep any preferred-depth band research-only.

Useful descriptors:

- `pullback_1_pct`, `pullback_2_pct`, `pullback_3_pct`;
- mean/max pullback depth;
- trough step-up percentages;
- peak step-up percentages;
- duration of each retreat/recovery cycle;
- full pattern duration;
- dispersion of pullback depths;
- monotonicity flags for peaks and troughs.

## States planned

- `ASCENDING_BASE_RECOGNIZED`
- `ASCENDING_BASE_REJECTED`
- `ASCENDING_BASE_AMBIGUOUS`
- `ASCENDING_BASE_INCOMPLETE`

## Fault ideas

Theory-grounded:

- `TOO_SHORT`
- `TOO_LONG`
- `NON_ASCENDING_TROUGHS`
- `NON_ASCENDING_PEAKS`
- `MISSING_THIRD_PULLBACK`

Research-only candidates:

- `PULLBACK_TOO_DEEP`
- `PULLBACK_DEPTH_INCONSISTENT`
- `WIDE_LOOSE`

Research-only bands must be validated from morphology labels, never returns.

## PIT semantics

- all turns must already be confirmed by P1;
- candidate confirmation date is the latest required landmark confirmation date;
- later bars may create a later candidate but cannot rewrite/backdate an earlier recognition;
- incomplete structures remain incomplete until the missing required turn becomes confirmed.

## Non-goals

P6 does not implement breakout entry, buy point, market filter, moving-average support rules, returns, position sizing, or CAN SLIM eligibility.

## Next work

1. Formalize `AscendingBaseGeometry` for seven alternating confirmed turns.
2. Build positive, non-ascending-low, non-ascending-high, too-short, too-long and irregular-depth fixtures.
3. Add state/fault policy with only duration + monotonic structure as first-pass hard gates.
4. Validate PIT/prefix stability before freezing the Ascending Base sub-contract.
