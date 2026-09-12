# P8 Adjudication Batch 01

Date: 2026-09-12
Status: FIRST REAL LABELS COMMITTED

## Rule applied

Candidate references are promoted to `LabelEvidence` only when the source record provides a sufficiently explicit pattern label and non-detector-derived structural window anchors. No OHLCV/detector output was inspected before assigning the label or DEVELOPMENT/VALIDATION split.

## Promoted

### p8-label-0001 — SNPS — FLAT_BASE — DEVELOPMENT

- source: Investor's Business Daily;
- authoritative label: Flat Base;
- source anchors: April 4, 2023 peak/start and May 18, 2023 breakout;
- committed window: 2023-04-04 through 2023-05-18;
- label: POSITIVE;
- rationale: source explicitly describes a six-week flat base from the April 4 peak and the May 18 breakout.

### p8-label-0002 — NFLX — CUP_WITH_HANDLE — VALIDATION

- source: Investor's Business Daily / MarketSurge example;
- authoritative label: Cup With Handle;
- recorded source anchors: Feb. 3, 2023 cup start and May 18, 2023 breakout at 349.80;
- committed window: 2023-02-03 through 2023-05-18;
- label: POSITIVE;
- split: VALIDATION, frozen before detector comparison.

## Held back

The remaining P0 candidates are not promoted merely because they are plausible. Examples with only breakout week, month-level start, pivot-only evidence, or unresolved component boundaries remain in the adjudication queue until their exact window can be defended from source anchors and/or a frozen calendar convention.

In particular:

- AAPL Flat Base: authoritative label is strong, but start/end are week-level in the source and need an explicit weekly-to-session window convention before promotion;
- OLED CWH: breakout date is explicit, but exact left-rim/start still needs adjudication;
- NVDA Double Bottom / Flat Base / Base-on-Base: pattern labels are explicit, but exact component windows still need structural anchor resolution;
- AMZN Cup No Handle: source gives month-level start and breakout week; exact start requires adjudication;
- STT/NAVN/MRX Ascending Base: source labels are explicit, but exact three-pullback landmark dates still need resolution.

## 2026-09-13 follow-up: calendar convention frozen

`docs/p8-source-anchor-adjudication-v0.md` now freezes how a source-stated week/month/date range may be resolved to a trading session without consulting detector output. The implementation is `src/oneil_patterns/validation/adjudication.py`.

This removes the methodological blocker for candidates whose source supplies enough structural semantics (for example, a named peak/reversal range or a stated pivot plus breakout week). It does **not** automatically promote month-only candidates: where the source still does not justify a structural selection rule, the example remains held back.

Next adjudication batches should apply this convention using OHLCV obtained only through the frozen P8 router and record the rule/range used in label metadata or rationale.

## Scientific status

This batch changes P8 from “no real corpus exists” to “real corpus construction has begun.” It does **not** constitute sufficient sample size for morphology validation, threshold revision, or a P8 freeze. The untouched validation example must not be used for threshold tuning.
