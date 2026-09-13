# #33 Progress Board

Last updated: 2026-09-13

## Source-of-truth boundary

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33 O'Neil Pattern Recognition, including P8 morphology validation. `azharmz/ussy-canslim-research` is the parent/HQ consumer and must not continue a parallel pattern engine.

NFLX VALIDATION remains locked until DEVELOPMENT semantics freeze.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs baseline |
| Parent #32 contract confirmation | COMPLETE | #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | explicit as-of cutoff |
| P1 Structural Landmark Engine | COMPLETE | `p1-landmark-v1` |
| P2 Base Segmentation | FIRST-PASS COMPLETE / RIGHT-EDGE REVISION ACTIVE | confirmed structure plus explicit observation semantics |
| P3 Flat Base | P8 v2 DEVELOPMENT | hard duration/depth unchanged; `WIDE_LOOSE` retained as ambiguity |
| P4 Double Bottom | P8 v3 DEVELOPMENT | no-undercut ambiguity; duration clock supports explicit completion observation without lowering 35-session gate |
| P5 Cup family | P8 v2 DEVELOPMENT | right-edge CWH/CNH active; roundedness research faults map to ambiguity |
| P6 Advanced patterns | COMPLETE | `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | `fault-ambiguity-v1` |
| P8 Labelled morphology validation | COVERAGE_BLOCKED_AFTER_CURRENT_CORPUS_AUDIT | 8 DEVELOPMENT labels; 8/8 source-dimension MATCH; identity STATUS_CONFLICT = 0 |
| P9 Productionization | COMPLETE | `production-v1`; P8 coverage debt remains |

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

DEVELOPMENT:
1. SNPS — FLAT_BASE
2. CTSH — CUP_WITH_HANDLE
3. FOUR — CUP_WITH_HANDLE
4. SEI — DOUBLE_BOTTOM
5. AMZN — CUP_WITHOUT_HANDLE
6. TW — FLAT_BASE
7. NVDA — DOUBLE_BOTTOM
8. SPOT — DOUBLE_BOTTOM

VALIDATION:
- NFLX — CUP_WITH_HANDLE — LOCKED / UNTOUCHED

## Latest canonical DEVELOPMENT result

Latest eight-label live artifact:

```text
MATCH                  = 8
BOUNDARY_DISAGREEMENT  = 0
LANDMARK_DISAGREEMENT  = 0
MISS_PATTERN           = 0
```

Candidate resolution:

```text
SOURCE_EQUIVALENT_MULTIPLE = 5
UNIQUE                     = 3
```

Candidate identity audit:

```text
STABLE                        = 670
MULTI_SEMANTIC_STABLE_STATUS  = 29
LIFECYCLE_TRANSITION          = 4
STATUS_CONFLICT               = 0
```

The four lifecycle transitions are maturity changes of the same anchored structure under explicit right-edge observation semantics; they are not identity collisions.

| Example | Agreement | Matched detector state | Interpretation |
|---|---|---|---|
| SNPS / Flat | MATCH | `FLAT_BASE_REJECTED` selected among source-equivalent candidates | same source dimensions also admit a later maturity candidate; lifecycle remains explicit |
| TW / Flat | MATCH | `FLAT_BASE_AMBIGUOUS` | only research `WIDE_LOOSE` remains |
| CTSH / CWH | MATCH | `CUP_WITH_HANDLE_AMBIGUOUS` | January source anchor and split-normalized pivot represented; Cup ambiguity is retained rather than forced recognized |
| FOUR / CWH | MATCH | `CUP_WITH_HANDLE_AMBIGUOUS` | source pivot represented; deep-handle ambiguity retained |
| SEI / Double Bottom | MATCH | `DOUBLE_BOTTOM_REJECTED` selected among source-equivalent candidates | core W is short, while same anchored structure can mature under right-edge completion; 35-session gate unchanged |
| NVDA / Double Bottom | MATCH | `DOUBLE_BOTTOM_RECOGNIZED` | clean recognized support |
| SPOT / Double Bottom | MATCH | `DOUBLE_BOTTOM_AMBIGUOUS` | exact source pivot; no-undercut remains explicit ambiguity |
| AMZN / Cup-no-Handle | MATCH | `CUP_WITHOUT_HANDLE_AMBIGUOUS` | source depth/scale represented; roundedness research faults retained |

## Current P8 verdicts

| Area | Verdict |
|---|---|
| Missing-provider routing | KEEP |
| Source optional-dimension evaluator | KEEP |
| Corporate-action comparison factor | KEEP |
| Right-edge/open-base representation | KEEP as explicit observation semantics |
| Flat `WIDE_LOOSE` severity | REVISE -> ambiguity |
| Flat numeric tightness bands | UNRESOLVED / coverage-limited |
| CWH right-edge handle / pivot role | KEEP after current audit |
| CWH start / left-rim representation | RESOLVED for current corpus; CTSH now MATCH |
| Double Bottom second-trough undercut | REVISE -> ambiguity |
| Double Bottom duration threshold | KEEP at 35 sessions; boundary semantics revised |
| Cup roundedness proxy severity | REVISE -> ambiguity |
| Candidate identity collisions | RESOLVED for current corpus; STATUS_CONFLICT = 0 |
| BaseIdentity / Lineage final freeze | NOT YET FROZEN; current audit semantics are stable enough for coverage expansion |

## Coverage status

Current positive DEVELOPMENT coverage is still below preregistered comfort for pattern-specific numerical conclusions:

- FLAT_BASE: 2
- CUP_WITH_HANDLE: 2
- DOUBLE_BOTTOM: 3
- CUP_WITHOUT_HANDLE: 1

Target remains approximately >=5 independent authoritative positive examples per major pattern before final pattern-specific numeric-band conclusions. Therefore P8 is now blocked primarily on authoritative corpus coverage, not on implementation correctness.

## Hard constraints

- no future bars or backdated confirmation;
- no return/CAGR/PF/FWD1/breakout-outcome tuning;
- no fabricated authoritative labels;
- source dimensions stay immutable and source-grounded;
- multiple structural scales remain explicit;
- right-edge horizon is observation evidence, never a fabricated P1 landmark;
- NFLX VALIDATION remains untouched until DEVELOPMENT freeze;
- #34 must not start until P8/#33 receives a defensible final verdict.

## Next work

1. expand authoritative DEVELOPMENT corpus, prioritizing under-covered FLAT_BASE, CUP_WITH_HANDLE and CUP_WITHOUT_HANDLE;
2. prefer candidates already present in `data/p8/reference_candidates_v0.csv` and adjudicate exact source-grounded anchors without detector feedback;
3. rerun canonical DEVELOPMENT after each promoted batch;
4. change numeric research bands only if multiple independent authoritative examples contradict them; otherwise keep them unresolved;
5. freeze DEVELOPMENT semantics once coverage is adequate and no unresolved implementation conflict remains;
6. open NFLX VALIDATION exactly once against the frozen DEVELOPMENT version;
7. record final P8/#33 verdict and update the parent #33 pointer before #34 begins.
