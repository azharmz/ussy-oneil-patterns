# P6 Advanced Patterns — Final Verdict

Date: 2026-09-13

Verdict: **CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT**

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only.

## Why this verdict is defensible

P6 v1 contained two state-driving numerical ideas that were explicitly research-only:

- Ascending Base pullback-depth dispersion threshold `0.05`;
- Base-on-Base close-above-first-high thresholds `0.50` / `0.75`.

Those numbers were not independently labelled and were not stated as universal O'Neil/IBD rules. Leaving them as state gates would create false precision.

P6 v2 removes them from classification and replaces them with conservative source-grounded semantics:

- Ascending Base preserves the three-pullback, higher-high/higher-low and 9–16-week structure, with IBD/MarketSmith's 6%–25% recognition envelope used only as an outer ambiguity guardrail; the familiar 10%–20% textbook band remains evidence, not universal exclusion logic.
- Base-on-Base recognizes the unambiguous case where the entire second base sits above the first base high, rejects a second base that never rises above the first-base high, and preserves partial overlap as ambiguous because published guidance says “entirely or mostly above” without defining a universal numerical “mostly” threshold.

This is intentionally conservative: uncertainty is surfaced rather than filled with a return-tuned or arbitrary number.

## What passed

- theory/source audit completed for both advanced families;
- unsupported v1 numerical state gates removed;
- explicit v2 contracts and versioned adapter output;
- PIT/future-extension invariance retained;
- positive, rejection and ambiguity fixtures retained/strengthened;
- normalized fault taxonomy distinguishes source-grounded P6 ambiguity from research-only core diagnostics;
- full repository regression suite passed: **227 tests** on workflow run `34746587586` at commit `642cfe36aeadf0a488e3478bbfec8cd1e0dfdf07`.

## What remains validation debt

1. No independent human/authoritative labelled OHLCV corpus exists for P6 comparable to the frozen P8 core corpus.
2. Base-on-Base's qualitative “mostly above” region is intentionally unresolved. Partial vertical overlap remains `AMBIGUOUS`; no close-fraction threshold may be invented or tuned from returns.
3. Ascending Base's 45–80 observed-session duration remains an operational translation of 9–16 weeks and has not received independent boundary validation.
4. Prior uptrend, market weakness, moving-average support, Base-on-Base initial breakout gain <20%, stage counting, buy points and breakout execution remain contextual/downstream evidence, not morphology gates silently added to P6.
5. Advanced patterns do not inherit the P8 core evidence level and remain outside frozen production schema `oneil-pattern-output-v2` / engine `33-core-p8-frozen-v1`.

## Freeze rule

P6 v2 is now frozen for the current #33 scope.

Do not:

- tune P6 from CAGR, PF, FWD1, breakout success, trade returns, or a convenient single chart;
- reinterpret P3/P4/P5/P8 thresholds from P6 work;
- add advanced families to frozen production v2 while implying P8-equivalent validation.

A future attempt to reduce P6 validation debt must open a separately versioned P6 validation cycle with independent morphology labels and a predeclared scoring protocol. The current verdict and v2 contracts remain immutable evidence of this cycle.
