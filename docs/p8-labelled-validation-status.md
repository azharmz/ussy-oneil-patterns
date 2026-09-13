# P8 Labelled Morphology Validation — Final Status

Status: **COMPLETE — CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT**

`azharmz/ussy-oneil-patterns` is the canonical source of truth for #33/P8. The former parallel P8 implementation in `azharmz/ussy-canslim-research` is migration evidence only.

## Frozen DEVELOPMENT corpus

Canonical file: `data/p8/labels_v0.csv`.

Authoritative positive DEVELOPMENT coverage:

- FLAT_BASE: 5
- CUP_WITH_HANDLE: 5
- DOUBLE_BOTTOM: 5
- CUP_WITHOUT_HANDLE: 5

Frozen result:

```text
20 / 20 MATCH
0 boundary disagreement
0 landmark disagreement
0 pattern miss
0 identity STATUS_CONFLICT
```

Candidate identity audit:

```text
STABLE                        = 940
MULTI_SEMANTIC_STABLE_STATUS  = 59
LIFECYCLE_TRANSITION          = 9
STATUS_CONFLICT               = 0
```

Freeze evidence commit: `2ed3dadcc354f56f4cb27401248daef60b1627fa`.
Freeze workflow run: `34740880269`.
Freeze decision: `docs/decisions/p8-development-freeze-v1.md`.

## Frozen implementation

- Flat: `flat-base-v2`
- Double Bottom: `double-bottom-v3`
- Cup family: `cup-family-v2`
- prediction adapter: `p8-canonical-prediction-adapter-v1.1`
- pivot adapter: `p8-pivot-adapter-v0.2`
- source evaluator: `p8-source-dimension-eval-v0.5`
- candidate identity audit: `p8-candidate-identity-audit-v0.4`
- source routing: strict R2 -> Yahoo/yfinance -> Tiingo

No return, CAGR, PF, FWD1, breakout outcome or entry optimization was used to tune morphology.

## Independent VALIDATION

NFLX `CUP_WITH_HANDLE` was kept untouched through DEVELOPMENT freeze and then executed once.

Workflow run: `34741079533`.
Artifact id: `10312408925`.
Artifact digest: `sha256:57203f50b3cd9292c81fcb351e5f06ceeb69871cebfd00f1ed47bbfbf6388670`.

Result:

```text
agreement_state         = MATCH
candidate_resolution    = UNIQUE
source start            = 2023-02-03
matched start           = 2023-02-03
start error             = 0 days
matched detector state  = CUP_WITH_HANDLE_AMBIGUOUS
candidate semantics     = OPEN_RIGHT_EDGE_HANDLE:p8-open-right-edge-handle-v0.1
detector fault          = BELOW_CUP_MIDPOINT
```

The one-shot workflow trigger was retired after execution.

## Interpretation

The independent case confirms that the frozen engine can represent the source-authoritative NFLX CWH at the exact published start anchor with a unique source-equivalent candidate.

The detector nevertheless keeps the case `AMBIGUOUS` because of its frozen `BELOW_CUP_MIDPOINT` severity rule. That is retained as validation debt rather than tuned away.

The NFLX row intentionally left pivot and depth unscored before VALIDATION was opened. Those dimensions are not added after seeing the result. Therefore independent evidence covers the preregistered comparable dimensions, not every numeric CWH band.

## Final morphology verdicts

| Area | Final verdict |
|---|---|
| Provider routing semantics | KEEP |
| Optional source dimensions / precision | KEEP |
| Corporate-action comparison | KEEP |
| Right-edge observation semantics | KEEP |
| Flat `WIDE_LOOSE` severity | ambiguity |
| DB second-trough undercut | ambiguity, not absolute rejection |
| DB 35-session threshold | KEEP; boundary/completion semantics revised |
| Cup roundedness proxy severity | ambiguity |
| Candidate identity collision handling | PASS on frozen DEVELOPMENT corpus |
| Independent core structural validation | PASS on frozen NFLX comparable dimensions |
| CWH `BELOW_CUP_MIDPOINT` severity | UNRESOLVED / validation debt |
| Every numeric band independently validated | NO |

## Downstream rule

The four core pattern families may be consumed downstream only with explicit `RECOGNIZED`, `AMBIGUOUS`, `REJECTED`, candidate semantics and detector faults preserved. Advanced families do not automatically inherit this P8 evidence level.

Final decision record: `docs/decisions/p8-final-verdict.md`.
