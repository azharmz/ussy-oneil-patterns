# #33 Progress Board

Last updated: 2026-09-13

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33 O'Neil Pattern Recognition. `azharmz/ussy-canslim-research` is the parent/HQ consumer and must not host a parallel pattern engine.

NFLX VALIDATION remains locked until DEVELOPMENT semantics freeze.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | baseline complete |
| Parent #32 contract confirmation | COMPLETE | #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | explicit as-of cutoff |
| P1 Structural Landmark Engine | COMPLETE | `p1-landmark-v1` |
| P2 Base Segmentation | FIRST-PASS COMPLETE / RIGHT-EDGE REVISION ACTIVE | explicit observation semantics added |
| P3 Flat Base | P8 v2 DEVELOPMENT | hard gates unchanged; `WIDE_LOOSE` retained as ambiguity |
| P4 Double Bottom | P8 v3 DEVELOPMENT | 35-session threshold retained; duration boundary revised |
| P5 Cup family | P8 v2 DEVELOPMENT | right-edge CWH/CNH active |
| P6 Advanced patterns | COMPLETE | `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | `fault-ambiguity-v1` |
| P8 Labelled morphology validation | EXPANDED_DEVELOPMENT_REVALIDATION | corpus expanded from 8 to 18 DEVELOPMENT examples; live rerun required |
| P9 Productionization | COMPLETE | `production-v1`; P8 debt carried explicitly |

## Current DEVELOPMENT stack

- Flat: `flat-base-v2`
- Double Bottom: `double-bottom-v3`
- Cup family: `cup-family-v2`
- source evaluator: `p8-source-dimension-eval-v0.5`
- canonical prediction adapter: v1.0 with pattern-specific structural signatures
- candidate identity audit: v0.3 with explicit lifecycle transitions
- OHLCV priority: R2 -> Yahoo/yfinance -> Tiingo; fallback only on genuine unavailability

## Authoritative corpus

Canonical file: `data/p8/labels_v0.csv`.

Current DEVELOPMENT positive coverage after source-only promotion:

- FLAT_BASE: 5
- CUP_WITH_HANDLE: 5
- DOUBLE_BOTTOM: 3
- CUP_WITHOUT_HANDLE: 5

New source-grounded examples were promoted without detector inspection: EXEL, TRGP, LLY, APH, NVDA CWH, BAC, INTC, ARW, AMD and SE.

VALIDATION:
- NFLX — CUP_WITH_HANDLE — LOCKED / UNTOUCHED

## Last fully audited live result before expansion

The prior eight-label artifact was:

```text
MATCH                  = 8
BOUNDARY_DISAGREEMENT  = 0
LANDMARK_DISAGREEMENT  = 0
MISS_PATTERN           = 0
STATUS_CONFLICT        = 0
```

Identity states were 670 STABLE, 29 MULTI_SEMANTIC_STABLE_STATUS and 4 LIFECYCLE_TRANSITION. The expanded 18-label corpus must now be rerun before any freeze decision.

## Current verdicts

- provider routing: KEEP
- optional source-dimension evaluator: KEEP
- explicit corporate-action comparison: KEEP
- right-edge/open-base representation: KEEP as explicit observation semantics
- Flat `WIDE_LOOSE`: ambiguity; numeric tightness bands remain evidence-dependent
- CWH start/left-rim representation: resolved for prior corpus
- Double Bottom undercut: ambiguity, not absolute identity gate
- Double Bottom duration threshold: keep 35 sessions; boundary semantics revised
- Cup roundedness research faults: ambiguity
- candidate identity collision: zero conflicts on prior corpus; expanded-corpus audit pending

## Hard constraints

- no future bars or backdated confirmation;
- no return/CAGR/PF/FWD1/breakout-outcome tuning;
- no fabricated authoritative labels;
- source dimensions remain immutable and source-grounded;
- right-edge horizon is observation evidence, never a fabricated P1 landmark;
- NFLX VALIDATION remains untouched until DEVELOPMENT freeze;
- #34 must not start until P8/#33 receives a defensible final verdict.

## Next work

1. run all 18 DEVELOPMENT labels through the canonical stack;
2. classify new source disagreements and identity conflicts without touching VALIDATION;
3. Double Bottom remains below the approximate five-example coverage target, so acquire two more independent authoritative DB examples if needed;
4. freeze numerical-band verdicts only where independent evidence is sufficient; otherwise retain `UNRESOLVED`;
5. freeze DEVELOPMENT semantics only after the expanded run is defensible;
6. open NFLX VALIDATION exactly once against that frozen version;
7. freeze P8/#33 and update the parent pointer before #34.
