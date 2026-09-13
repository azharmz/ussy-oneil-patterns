# P8 Final Validation Verdict

Date: 2026-09-13

Status: CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT

Development was frozen before validation. Freeze evidence commit: `2ed3dadcc354f56f4cb27401248daef60b1627fa`.

Development evidence: 20 authoritative examples, five per core family, 20/20 source-dimension MATCH, and zero candidate identity STATUS_CONFLICT.

The locked NFLX CUP_WITH_HANDLE validation case was then evaluated once.

Validation workflow run: `34741079533`.
Validation artifact id: `10312408925`.
Validation artifact digest: `sha256:57203f50b3cd9292c81fcb351e5f06ceeb69871cebfd00f1ed47bbfbf6388670`.

NFLX result:

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

The validation run used the frozen prediction adapter v1.1, pivot adapter v0.2, source evaluator v0.5, and candidate identity audit v0.4. No morphology threshold was changed after the validation result was observed.

Interpretation: the independent case supports structural CWH representation at the authoritative start date, but the frozen detector retains an ambiguity classification because of the BELOW_CUP_MIDPOINT severity rule. That debt remains unresolved rather than being tuned away.

The locked NFLX row had pivot and depth unscored before validation was opened. Those dimensions are not added after the result. Therefore the independent test validates the preregistered comparable dimensions, not every numeric CWH band.

Final P8 verdict for FLAT_BASE, CUP_WITH_HANDLE, CUP_WITHOUT_HANDLE, and DOUBLE_BOTTOM: CONDITIONAL PASS. Downstream use must preserve RECOGNIZED, AMBIGUOUS, REJECTED, candidate semantics, and faults. Advanced families do not inherit this evidence level automatically.
