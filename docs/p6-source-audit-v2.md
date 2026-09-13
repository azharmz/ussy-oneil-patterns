# P6 Advanced Patterns — Source Audit v2

Date: 2026-09-13

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only. This audit does not reopen the frozen P3/P4/P5/P8 core.

## Governing rule

P6 may operationalize published morphology, but a numeric threshold that is not supported by source material must not decide a production-facing morphology state. Trading returns, breakout performance, CAGR, PF, FWD1, or later outcomes are not morphology labels.

## Ascending Base

Primary IBD sources reviewed:

1. Investor's Business Daily, *How To Buy Growth Stocks: Why 3 Mild Retreats May Yield The Bullish Ascending Base* (updated 2024):
   https://www.investors.com/how-to-invest/investors-corner/chart-reading-202-how-3-retreats-may-yield-an-ascending-base/
2. Investor's Business Daily, *These IBD 50 Stocks Form Sneaky But Bullish Chart Pattern* (2026-09-04).
3. IBD Top Stocks 2019, Coupa Software example.

Source-supported morphology:

- three pullbacks / retreats;
- successively higher highs and higher lows;
- usual development window of about 9–16 weeks;
- textbook pullback guidance commonly stated as 10%–20%;
- IBD/MarketSmith programmed recognition has accepted a broader 6%–25% correction envelope;
- market weakness, prior uptrend, moving-average support, buy point and breakout volume are contextual/execution evidence rather than the pure morphology owned by #33.

### v2 decision

The old v1 `0.05` pullback-depth-dispersion threshold is removed from state classification because it was a research-only number with no source basis.

P6 v2 uses:

- 45–80 observed sessions as the existing operational translation of 9–16 weeks;
- strict ascending troughs and peaks as hard morphology gates;
- 6%–25% as a source-grounded outer guardrail: a pullback outside this envelope makes the candidate `AMBIGUOUS`, not automatically a hard rejection;
- 10%–20% is retained as textbook evidence per pullback, not as a hidden hard gate.

This deliberately avoids false precision. Source examples can include pullbacks below 10%, so the textbook band cannot safely be treated as universal exclusion logic.

## Base-on-Base

Primary IBD sources reviewed:

1. Investor's Business Daily, *Stock Market Winners Often Take Flight In The Base-on-Base Pattern* (2026-01-09):
   https://www.investors.com/how-to-invest/investors-corner/stock-market-winners-take-flight-base-on-base-pattern/
2. Investor's Business Daily, *Stock Market Leaders Tend To Do Quite Well From This Technical Setup* (2025-08-08):
   https://www.investors.com/how-to-invest/investors-corner/stock-market-leaders-base-on-base-pattern/

Source-supported concept:

- a stock breaks out from a proper first base but advances less than roughly 20% before forming another base;
- the second base is often a flat base but need not always be;
- the second base should form entirely or mostly above the first base;
- if it sinks too far into the first base it is not a proper Base-on-Base;
- the combined structure counts as one stage until a >20% advance separates a later base.

### v2 decision

IBD does not publish a universal numeric fraction for the phrase “mostly above.” Therefore the old close-fraction thresholds (`>=0.75`, `<0.50`) are removed from state classification.

P6 v2 uses a conservative high-confidence subset:

- if `base_2.low_price >= base_1.high_price`: `RECOGNIZED`;
- if `base_2.high_price <= base_1.high_price`: `REJECTED` with `SECOND_BASE_NOT_ABOVE_FIRST`;
- otherwise the vertical ranges overlap and the candidate is `AMBIGUOUS` with `SECOND_BASE_OVERLAPS_FIRST`.

`second_close_fraction_above_first_high` remains diagnostic evidence only. It cannot resolve “mostly above” without an independently labelled P6 corpus.

The preceding breakout gain (<20%), stage counting, and entry/buy-point logic remain context owned outside this pure morphology gate; they are not silently inferred from the two base summaries.

## Evidence boundary

This audit supports source-faithful quantification and conservative ambiguity handling. It does **not** create an independent labelled validation corpus comparable to P8 core validation.

P6 therefore may receive only a conditional/frozen verdict with explicit validation debt. It must not inherit the P8 evidence level or be added to `oneil-pattern-output-v2` merely because its unit/regression suite is green.
