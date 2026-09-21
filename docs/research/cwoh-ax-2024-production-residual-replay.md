# CWOH AX 2024 production residual replay

Date: 2026-09-21
Branch: `research/cwoh-ax-production-replay`
Production baseline: `10668bbe9e27780d0dfe2464b9370e25e996fda5`
Replay commit: `12b4686c15d60f6b6559a7904e0ab629441a9935`
Workflow run: `35582876895`
Artifact: `10631525330`
Artifact digest: `sha256:8e6ceca3c7a51303cdb0db1bcbfbac051a61192ed1ce6905d9cd0d09cc0c646a`

## Purpose

Replay Golden reconstruction case 022 (AX 2024) against the current production CWOH stack without changing production morphology semantics.

Source oracle: IBD/MarketSurge CUP_WITHOUT_HANDLE, pivot 60.00, observed move above the buy point on 2024-05-06. Source start/depth are not scored.

## Result

- Source-dimension agreement: `MATCH`.
- Candidate resolution: `UNIQUE`.
- Pivot: 60.00 exactly; pivot price error 0.0%.
- Matched detector status: `CUP_WITHOUT_HANDLE_AMBIGUOUS`.
- Matched fault: `FRAGMENTED_BOTTOM`.
- Matched structure: left rim 2024-01-31, cup low 2024-04-16, depth 19.20%.
- Candidate semantics: `OPEN_RIGHT_EDGE_CNH:p8-open-right-edge-cnh-v0.3:TROUGH=2024-04-16`.
- Current production emitted four CWOH candidates. A separate 54.64-pivot candidate is RECOGNIZED, but it is not source-equivalent to the 60.00 oracle and must not substitute for it.
- Identity audit: four STABLE identities.

OHLCV source: Yahoo/yfinance because AX was absent from the R2 membership snapshot 2026-08-28. Input was truncated at 2024-05-06.

## Adjudication

The old Golden AX discrepancy remains present on current production. Later Cup-family engineering repaired candidate construction/source matching broadly, but did not resolve AX's source-target `FRAGMENTED_BOTTOM` state mapping.

Therefore AX is a genuine residual CWOH source-fidelity semantics gap. This replay alone does **not** authorize relaxing the `FRAGMENTED_BOTTOM` proxy or any numeric threshold. Any state-semantic change requires independent DEVELOPMENT/source-semantics evidence and subsequent locked validation.

No production engine change is promoted by this replay.
