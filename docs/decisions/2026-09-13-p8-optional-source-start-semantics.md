# P8 optional authoritative start semantics

Date: 2026-09-13

Status: PREREGISTERED FOR DEVELOPMENT

## Problem

P8 policy requires source dimensions to be independent and forbids inventing precision that the source does not provide. The canonical evaluator already treats source end and pivot dimensions as optional, but `LabelEvidence.window_start` is still mandatory.

That requirement blocks otherwise strong authoritative examples where the source explicitly provides pattern identity and pivot/breakout evidence but does not publish an exact base-start anchor.

## Decision

Revise the canonical label/evaluator contract so authoritative start is optional.

- `window_start = None` means the source did not provide a detector-comparable start anchor.
- `window_start_precision = None` is required when start is absent.
- start is not scored and does not contribute to candidate ranking when absent.
- detector context retrieval remains independent of source start: the runner uses the configured lookback from `asof_date` when start is absent.
- existing labels with `DAY` or `MONTH` starts remain unchanged.

The evaluator may still select among same-pattern candidates using other published dimensions such as pivot date/price. Detector status/faults remain diagnostic only and do not influence source-match ranking.

## First targeted use

NVDA 2023 Double Bottom is eligible as DEVELOPMENT evidence because IBD explicitly identifies:

- pattern: double-bottom base;
- breakout during the week ended 2023-11-10 / early November 2023;
- entry/pivot: 47.61;
- exact base-start: not published in the source text used by the corpus.

The label therefore must not invent a start date.

## Guardrails

- this revision cannot be used to erase a start anchor that a source actually provides;
- missing start is represented explicitly, not inferred from detector output;
- source-independent context lookback must be fixed before execution;
- no VALIDATION label is changed or executed;
- no return/performance input is used.
