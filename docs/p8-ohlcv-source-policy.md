# P8 OHLCV Source Policy

Status: ACTIVE
Date: 2026-09-12

## Principle

P8 validates the frozen morphology detector, not the production universe. An authoritative labelled example remains eligible even when its security is absent from the frozen Musaffa/R2 universe.

The workflow is strictly reference-first:

1. identify an independent authoritative pattern label;
2. freeze the source reference and provisional labelled period;
3. determine whether matching OHLCV exists in canonical R2;
4. if absent, obtain historical OHLCV from an external source using the frozen provider priority below;
5. normalize external OHLCV to the detector's input semantics;
6. freeze the labelled window/split before inspecting detector agreement;
7. run the frozen detector and record agreement/disagreement.

Never search price history for a shape first and then look for an article that appears to confirm it.

## Source routing priority

Provider priority is frozen as:

1. **Canonical R2** — when the referenced security and required historical period exist in `azharmz/ussy-data`.
2. **Yahoo Finance via `yfinance`** — first external route because R2 production ingestion itself uses Yahoo with `auto_adjust=False`; this minimizes source-semantic drift from production.
3. **Tiingo EOD** — fallback and cross-check route. `ussy-data/src/audit_tiingo.py` already maps Tiingo raw `open/high/low/close/volume` plus `adjClose` to the same raw-OHLC + separate `adj_close` contract used for Yahoo comparison.
4. **Other documented provider** — only when the three routes above cannot supply a reliable historical window.

A lower-priority provider must not silently replace an available higher-priority provider merely because its morphology agrees better with the detector.

### R2 route

Use canonical `azharmz/ussy-data` when the referenced security and required historical period are available. Preserve the existing PIT/data contract and raw-OHLC semantics.

### Yahoo/yfinance external route

Use `yfinance` with `auto_adjust=False` so:

- `Open`, `High`, `Low`, `Close` remain raw daily prices;
- `Adj Close` maps to `adj_close` separately;
- `Volume` maps to raw daily volume.

This is the preferred external source because it is semantically closest to R2 production ingestion.

### Tiingo external route

Use Tiingo when Yahoo is unavailable, incomplete, or needs an independent source check. Map:

- Tiingo `open/high/low/close/volume` -> raw detector fields;
- Tiingo `adjClose` -> `adj_close`.

Record the fallback reason. For delisted/historical symbols such as IPHI or legacy MBLY, Tiingo may be especially useful if Yahoo no longer serves the required window.

## External schema

External data must be normalized to:

- `date`;
- stable `security_id` scoped to the validation corpus;
- `ticker` / historical symbol;
- raw `open`, `high`, `low`, `close`;
- `adj_close` retained separately from raw close;
- `volume`.

Do not synthesize missing `adj_close`, split history, or raw OHLC values merely to satisfy the schema. If reliable historical data cannot be obtained, mark the example `OHLCV_UNAVAILABLE` and keep the authoritative reference in the candidate registry without promoting it into executable P8 validation.

## Corporate actions and ticker lineage

For renamed, acquired, or delisted securities:

- preserve the source-era ticker in `LabelEvidence.symbol`;
- store any modern/successor identifier in metadata only;
- document splits and other corporate actions relevant to the labelled window;
- detector morphology continues to use raw OHLC under the frozen #33 contract;
- source adjustments must not silently replace raw prices.

## Required provenance metadata

Every executable P8 label should record at minimum:

- `reference_source` and authoritative URL/document;
- `ohlcv_source` (`R2`, `YAHOO_YFINANCE`, `TIINGO`, or named fallback);
- `ohlcv_source_symbol`;
- `ohlcv_retrieved_at` or dataset version where applicable;
- whether raw/adjusted fields were supplied distinctly;
- fallback reason when a lower-priority provider is used;
- any corporate-action/ticker-lineage note;
- DEVELOPMENT or VALIDATION split.

## Comparability audit

P8 reports should break results down by provider (`R2`, `YAHOO_YFINANCE`, `TIINGO`, other) so a source-specific disagreement pattern cannot be mistaken for a morphology problem.

The production CAN SLIM application remains restricted to its frozen universe. External P8 securities are validation cases only and never alter production-universe membership.
