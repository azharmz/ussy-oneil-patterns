# P8 canonical DEVELOPMENT batch 01

Date: 2026-09-13
Status: CANONICAL DEVELOPMENT EVIDENCE — REVISION REQUIRED BEFORE FREEZE

Canonical live run: GitHub Actions run **#175** (`34727720184`), head `551c2bc8a4b1a21bd83bf865a869a0b1a2fa194a`.

Versions:

- prediction adapter: `p8-canonical-prediction-adapter-v0.2`;
- pivot adapter: `p8-pivot-adapter-v0.2`;
- source-dimension evaluator: `p8-source-dimension-eval-v0.2`.

All five rows are DEVELOPMENT. NFLX VALIDATION remained locked and was not inspected by the runner.

## Data source

The canonical repository has no R2 credentials in its Actions runtime. Under the frozen source priority, R2 therefore reported `SourceUnavailable` and every DEVELOPMENT example used Yahoo/yfinance. This is an operational source-routing fact, not a morphology choice.

Missing provider configuration is now distinguished from supplied-but-invalid credentials: only genuine provider unavailability permits fallback; auth/API/schema/QC failures remain terminal.

## Batch result

```text
source-dimension agreement:
  MATCH                  = 1
  BOUNDARY_DISAGREEMENT  = 3
  MISS_PATTERN           = 1
```

| Example | Authoritative pattern | Canonical source agreement | Matched detector state | Key diagnostic |
|---|---|---|---|---|
| SNPS | FLAT_BASE | MATCH | FLAT_BASE_REJECTED | exact start + pivot; emitted segment ends early; `TOO_SHORT`, `WIDE_LOOSE` |
| CTSH | CUP_WITH_HANDLE | BOUNDARY_DISAGREEMENT | CUP_WITH_HANDLE_AMBIGUOUS | only CWH is Dec-2003 to Feb-2004, not source Jan-Jul 2004; `DEEP_HANDLE_EXCEPTIONAL` |
| FOUR | CUP_WITH_HANDLE | BOUNDARY_DISAGREEMENT | CUP_WITH_HANDLE_RECOGNIZED | recognized CWH is Oct-2023 to Jan-2024, not source Feb-Sep 2024 |
| SEI | DOUBLE_BOTTOM | BOUNDARY_DISAGREEMENT | DOUBLE_BOTTOM_REJECTED | nearest selected W starts May rather than July; `NO_SECOND_TROUGH_UNDERCUT` |
| AMZN | CUP_WITHOUT_HANDLE | MISS_PATTERN | no matching pattern | no Cup-no-Handle emitted; 145.86 exists as canonical landmark/pivot in other morphologies |

## Evaluator correction discovered by this batch

The first canonical live run incorrectly scored SNPS as a boundary failure because legacy corpus `window_end=2023-05-18` is a **source breakout anchor**, while canonical `prediction.end_date=2023-04-25` is a **structural segment end**.

Evaluator v0.2 corrects this category error: legacy source-window end is preserved but is not scored against a structural end until the source end role is explicitly versioned. This is evaluator semantics, not detector tuning.

After that correction SNPS is a source-dimension `MATCH`: start `2023-04-04`, pivot date `2023-04-04`, pivot price `392.79` all agree. The detector still independently rejects its emitted Flat Base candidate.

## Morphology diagnosis

### SNPS — pattern-window truncation

The source explicitly describes a roughly six-week Flat Base beginning at the April 4 peak. The canonical structural candidate beginning on April 4 terminates on April 25 and is then rejected as `TOO_SHORT` and `WIDE_LOOSE`.

The current P2/P3 structural window is therefore not representing the authoritative named-base span. Because the assessed region is truncated, this example cannot yet adjudicate Flat Base tightness thresholds themselves.

Verdict:

- current pattern-window assembly: **REVISE**;
- Flat Base tightness bands: **UNRESOLVED** until the source-sized structure can be represented without source leakage.

### CTSH / FOUR — wrong CWH instance

Both authoritative CWH examples cause the canonical engine to emit a CWH, but the emitted CWH is an earlier, different structure:

- CTSH canonical CWH: Dec 3 2003 -> Feb 13 2004; source base begins January and develops through late July 2004;
- FOUR canonical CWH: Oct 20 2023 -> Jan 12 2024; source base begins February 2024 and develops into the September breakout.

This is stronger than a threshold disagreement. The current consecutive-landmark cup/handle assembly is selecting the wrong structural scale / instance.

Verdict:

- current Cup-family candidate assembly: **REVISE**;
- handle-depth research band (`DEEP_HANDLE_EXCEPTIONAL`): **UNRESOLVED**, because CTSH's compared handle belongs to the wrong base instance.

### SEI — DB instance mismatch before undercut adjudication

The selected canonical W starts May 10 and is rejected for `NO_SECOND_TROUGH_UNDERCUT`; the source chronology places formation after the July 12 breakout and subsequent two-week rally.

Because the source and detector are not describing the same structural W, this example cannot yet cleanly answer whether the second trough must strictly undercut the first.

Verdict:

- DB candidate/window assembly: **REVISE**;
- strict second-trough undercut gate: **UNRESOLVED** pending a source-aligned W instance and additional authoritative evidence.

### AMZN — Cup-no-Handle family miss with pivot landmark preserved

No `CUP_WITHOUT_HANDLE` prediction is emitted. The same canonical run nevertheless preserves the authoritative 145.86 level as a structural high used by other emitted morphologies, including a rejected Flat Base and a recognized Double Bottom.

The price landmark is therefore not simply absent. The disagreement lies in named morphology / cup-family structural assembly and hierarchy.

Verdict:

- Cup-no-Handle candidate assembly / family hierarchy: **REVISE / TARGETED DEVELOPMENT REQUIRED**;
- no threshold change is justified from this single example.

## P8.5 morphology-only decisions from batch 01

| Area | Verdict | Reason |
|---|---|---|
| Provider-not-configured routing semantics | REVISE — COMPLETED | runtime provider absence is `SourceUnavailable`; invalid supplied auth remains terminal |
| Source-window end vs structural-end evaluator semantics | REVISE — COMPLETED | different source/detector dimensions were being compared |
| Named-base structural candidate/window assembly | **REVISE REQUIRED** | authoritative spans repeatedly not represented at the correct structural scale |
| Flat Base tightness research bands | UNRESOLVED | SNPS candidate is truncated before threshold meaning can be judged |
| CWH handle-depth research band | UNRESOLVED | CTSH matched CWH is the wrong base instance |
| Double Bottom strict undercut gate | UNRESOLVED | SEI matched W is not source-aligned |
| Cup-no-Handle hierarchy | UNRESOLVED pending assembly revision | AMZN named family is missed although key pivot landmark exists |

## Next engineering slice

Before changing any morphology threshold, preregister and implement a **versioned multi-turn / structural-scale candidate assembly revision** that can represent a named base across intervening minor P1 landmarks while remaining PIT-safe.

Required constraints:

1. P1 landmark extraction remains unchanged initially; the revision is in how confirmed landmarks are assembled into candidate structures.
2. Candidate construction must not use authoritative label dates to choose its landmarks at runtime.
3. Multiple plausible structural scales may coexist and must remain explicit rather than forcing a single winner.
4. Candidate identity must remain deterministic and PIT/prefix stable where applicable.
5. No return, breakout performance, CAGR, PF, FWD1, or entry outcome may participate.
6. Re-run all five DEVELOPMENT examples after the revision; do not open NFLX VALIDATION.

Only after source-aligned structural instances exist can P8 fairly adjudicate tightness, handle, undercut, and Cup-family research bands.
