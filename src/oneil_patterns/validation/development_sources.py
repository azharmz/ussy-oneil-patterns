from __future__ import annotations

from datetime import date
import io
import json
import os

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import pandas as pd

from .external_ohlcv import fetch_tiingo, fetch_yfinance, normalize_frame
from .source_router import RoutedOhlcv, SourceUnavailable, route_ohlcv


R2_REQUIRED_ENV = (
    "R2_ENDPOINT",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_BUCKET_NAME",
)


class R2TickerAmbiguous(RuntimeError):
    pass


def _r2_client():
    missing = [name for name in R2_REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        # Configuration/auth absence is operational failure, not data absence.
        # It must not silently permit fallback to a lower-priority provider.
        raise RuntimeError(f"R2 configuration missing: {', '.join(missing)}")
    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
        config=Config(retries={"max_attempts": 5, "mode": "adaptive"}),
    )


def _resolve_r2_security_id(symbol: str) -> str:
    client = _r2_client()
    bucket = os.environ["R2_BUCKET_NAME"]
    pointer = json.loads(client.get_object(Bucket=bucket, Key="universe/current.json")["Body"].read())
    snapshot_date = str(pointer["snapshot_date"])
    payload = json.loads(
        client.get_object(Bucket=bucket, Key=f"universe/membership/{snapshot_date}.json")["Body"].read()
    )
    matches = {
        str(row["security_id"])
        for row in payload.get("records", [])
        if str(row.get("ticker", "")).upper() == symbol.upper()
    }
    if not matches:
        raise SourceUnavailable(f"ticker {symbol} absent from R2 membership snapshot {snapshot_date}")
    if len(matches) != 1:
        raise R2TickerAmbiguous(
            f"ticker {symbol} maps to multiple R2 security_ids in {snapshot_date}: {sorted(matches)}"
        )
    return next(iter(matches))


def r2_ticker_provider(symbol: str, start: date, end: date) -> pd.DataFrame:
    security_id = _resolve_r2_security_id(symbol)
    client = _r2_client()
    bucket = os.environ["R2_BUCKET_NAME"]
    key = f"backtest/ohlcv/{security_id}.parquet"
    try:
        payload = client.get_object(Bucket=bucket, Key=key)["Body"].read()
    except ClientError as exc:
        code = str(exc.response.get("Error", {}).get("Code", ""))
        if code in {"404", "NoSuchKey", "NotFound"}:
            raise SourceUnavailable(f"R2 object absent: {key}") from exc
        raise

    frame = pd.read_parquet(io.BytesIO(payload), engine="pyarrow")
    required = {"date", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"R2 parquet missing columns: {sorted(missing)}")
    work = frame.copy()
    work["date"] = pd.to_datetime(work["date"], errors="raise").dt.date
    work = work.loc[(work["date"] >= start) & (work["date"] <= end)].copy()
    if work.empty:
        raise SourceUnavailable(f"R2 window absent for {symbol} {start}..{end}")
    if "adj_close" not in work.columns:
        raise ValueError("R2 parquet missing adj_close; raw-vs-adjusted contract cannot be verified")
    normalized = normalize_frame(work)
    normalized.attrs["security_id"] = security_id
    normalized.attrs["object_key"] = key
    return normalized


def yahoo_provider(symbol: str, start: date, end: date) -> pd.DataFrame:
    try:
        return fetch_yfinance(symbol, start, end)
    except ValueError as exc:
        if "external OHLCV is empty" in str(exc):
            raise SourceUnavailable(f"Yahoo returned no rows for {symbol} {start}..{end}") from exc
        raise


def tiingo_provider(symbol: str, start: date, end: date) -> pd.DataFrame:
    token = os.environ.get("TIINGO_API_KEY")
    if not token:
        # Missing auth is terminal under the frozen routing contract.
        raise RuntimeError("TIINGO_API_KEY is not configured")
    try:
        return fetch_tiingo(symbol, start, end, token)
    except ValueError as exc:
        if "external OHLCV is empty" in str(exc):
            raise SourceUnavailable(f"Tiingo returned no rows for {symbol} {start}..{end}") from exc
        raise


def route_development_ohlcv(symbol: str, start: date, end: date) -> RoutedOhlcv:
    return route_ohlcv(
        symbol=symbol,
        start=start,
        end=end,
        r2_provider=r2_ticker_provider,
        yahoo_provider=yahoo_provider,
        tiingo_provider=tiingo_provider,
    )
