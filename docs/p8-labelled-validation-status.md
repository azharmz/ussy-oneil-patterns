# P8 Labelled Morphology Validation — Status

Status: **CANONICAL DEVELOPMENT REVISION IN PROGRESS**

## Canonical boundary

`azharmz/ussy-oneil-patterns` is the source of truth for #33/P8 implementation and validation. The former parallel P8 implementation in `azharmz/ussy-canslim-research` is migration evidence only.

NFLX VALIDATION remains locked and untouched.

## Infrastructure state

P8 now has:

- authoritative machine-readable labels and provenance;
- DEVELOPMENT / VALIDATION split with leakage guardrails;
- optional source dimensions instead of invented boundaries;
- `DAY` / `MONTH` source precision;
- source pivot normalization while preserving source values;
- optional source depth comparison;
- strict OHLCV routing `R2 -> Yahoo/yfinance -> Tiingo`;
- source-dimension evaluator `p8-source-dimension-eval-v0.4`;
- canonical prediction adapter with explicit candidate semantics;
- OPEN_RIGHT_EDGE Flat, Handle and Cup-no-Handle observations;
- live DEVELOPMENT Actions runner/artifact;
- persisted detector state/fault evidence.

## Corpus

Canonical file: `data/p8/labels_v0.csv`.

DEVELOPMENT:

1. SNPS — `FLAT_BASE`
2. CTSH — `CUP_WITH_HANDLE`
3. FOUR — `CUP_WITH_HANDLE`
4. SEI — `DOUBLE_BOTTOM`
5. AMZN — `CUP_WITHOUT_HANDLE`
6. TW — `FLAT_BASE`
7. NVDA — `DOUBLE_BOTTOM`
8. SPOT — `DOUBLE_BOTTOM`

VALIDATION:

- NFLX — `CUP_WITH_HANDLE` — **LOCKED / UNTOUCHED**

## Latest live DEVELOPMENT result

```text
MATCH                  = 7
BOUNDARY_DISAGREEMENT  = 1
LANDMARK_DISAGREEMENT  = 0
MISS_PATTERN           = 0
```

| Example | Agreement | Detector evidence | Diagnosis |
|---|---|---|---|
| SNPS / FLAT_BASE | MATCH | source-aligned right-edge candidate exists; selected candidate still reports `FLAT_BASE_REJECTED` | source dimensions represented; candidate identity/ranking audit still required |
| TW / FLAT_BASE | MATCH | `FLAT_BASE_AMBIGUOUS` | only research `WIDE_LOOSE` remains |
| CTSH / CUP_WITH_HANDLE | BOUNDARY_DISAGREEMENT | `CUP_WITH_HANDLE_RECOGNIZED` | source January start/left-rim remains unresolved |
| FOUR / CUP_WITH_HANDLE | MATCH | `CUP_WITH_HANDLE_AMBIGUOUS` | 84.26 pivot now exact through open-right-edge handle; deep-handle ambiguity retained |
| SEI / DOUBLE_BOTTOM | MATCH | `DOUBLE_BOTTOM_REJECTED` | only unchanged `TOO_SHORT` hard gate remains |
| NVDA / DOUBLE_BOTTOM | MATCH | `DOUBLE_BOTTOM_RECOGNIZED` | clean source-aligned recognized example |
| SPOT / DOUBLE_BOTTOM | MATCH | `DOUBLE_BOTTOM_AMBIGUOUS` | exact 621.20 pivot; no-undercut is now explicit ambiguity |
| AMZN / CUP_WITHOUT_HANDLE | MATCH | `CUP_WITHOUT_HANDLE_AMBIGUOUS` | source depth selects Sep 14 -> Oct 26 scale; roundedness proxies retained as ambiguity |

## Active v2 contracts

- `flat-base-v2` — research `WIDE_LOOSE` no longer hard rejection;
- `double-bottom-v2` — absence of second-trough undercut maps to ambiguity;
- `cup-family-v2` — `SHARP_V` / `FRAGMENTED_BOTTOM` map to ambiguity; explicit right-edge CWH/CNH observations remain separate candidate semantics.

Numeric research bands are unchanged by those revisions.

## Morphology-only verdicts

| Area | Current verdict |
|---|---|
| Missing-provider routing semantics | KEEP |
| Source evaluator optional dimensions | KEEP |
| Source depth dimension | KEEP for candidate-scale adjudication |
| Right-edge representation | REVISE — implemented explicitly |
| Flat `WIDE_LOOSE` severity | REVISE — ambiguity |
| Flat numeric tightness bands | UNRESOLVED |
| CWH pivot role / right-edge handle | REVISE — FOUR now source-aligned |
| CWH start / left-rim semantics | UNRESOLVED — CTSH |
| DB strict second-trough undercut | REVISE — ambiguity |
| DB duration gate / boundary semantics | UNRESOLVED — SEI |
| Cup roundedness proxy severity | REVISE — ambiguity |
| Cup-no-Handle candidate scale | KEEP source-depth selection; identity churn audit pending |
| BaseIdentity / Lineage freeze | NOT READY |

## Current work order

1. CTSH source-start/left-rim audit;
2. additional authoritative DB duration evidence before any duration revision;
3. BaseIdentity / Lineage and candidate-ranking stability audit;
4. targeted extra evidence only where remaining numeric bands are decision-relevant;
5. freeze DEVELOPMENT semantics;
6. open NFLX VALIDATION exactly once;
7. record final P8 verdict and freeze #33 before #34 starts.

## Guardrails

- DEVELOPMENT only during tuning;
- NFLX VALIDATION remains locked;
- no return, CAGR, PF, FWD1, breakout-performance or entry optimization;
- no source dimension invented from detector output;
- authoritative source values remain immutable;
- corporate-action normalization stays explicit;
- multiple plausible structural scales stay visible;
- synthetic fixtures are regression-only;
- contradictory or low-coverage numeric bands remain `UNRESOLVED`.
