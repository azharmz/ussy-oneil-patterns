from __future__ import annotations

from datetime import date, timedelta
import json
import urllib.parse
import urllib.request

import pandas as pd

REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "adj_close", "volume"]


def normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    missing = set(REQUIRED_COLUMNS) - set(out.columns)
    if missing:
        raise ValueError(f"external OHLCV missing columns: {sorted(missing)}")
    out = out[REQUIRED_COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise").dt.date
    for column in ["open", "high", "low", "close", "adj_close", "volume"]:
        out[column] = pd.to_numeric(out[column], errors="raise")
    if out.empty:
        raise ValueError("external OHLCV is empty")
    if out["date"].duplicated().any():
        raise ValueError("external OHLCV contains duplicate dates")
    if (out[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("external OHLCV contains nonpositive price")
    if (out["volume"] < 0).any():
        raise ValueError("external OHLCV contains negative volume")
    return out.sort_values("date").reset_index(drop=True)


def fetch_yfinance(symbol: str, start: date, end: date) -> pd.DataFrame:
    """Fetch Yahoo daily bars with production-compatible raw OHLC semantics."""
    import yfinance as yf

    # yfinance end is exclusive; include the labelled end date.
    raw = yf.download(
        symbol,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        interval="1d",
        auto_adjust=False,
        actions=False,
        repair=False,
        prepost=False,
        progress=False,
        threads=False,
        timeout=30,
    )
    if isinstance(raw.columns, pd.MultiIndex):
        if symbol in raw.columns.get_level_values(-1):
            raw = raw.xs(symbol, axis=1, level=-1)
        else:
            raw.columns = raw.columns.get_level_values(0)
    frame = pd.DataFrame({
        "date": pd.to_datetime(raw.index).date,
        "open": raw["Open"].to_numpy(),
        "high": raw["High"].to_numpy(),
        "low": raw["Low"].to_numpy(),
        "close": raw["Close"].to_numpy(),
        "adj_close": raw["Adj Close"].to_numpy(),
        "volume": raw["Volume"].to_numpy(),
    })
    return normalize_frame(frame)


def fetch_tiingo(symbol: str, start: date, end: date, token: str) -> pd.DataFrame:
    """Fetch Tiingo EOD bars using the audited ussy-data field mapping."""
    query = urllib.parse.urlencode({
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "token": token,
    })
    request = urllib.request.Request(
        f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?{query}",
        headers={"User-Agent": "ussy-oneil-patterns-p8/1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read())
    if not isinstance(payload, list):
        raise ValueError("Tiingo response is not a price list")
    frame = pd.DataFrame([
        {
            "date": str(row["date"])[:10],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "adj_close": row["adjClose"],
            "volume": row["volume"],
        }
        for row in payload
    ])
    return normalize_frame(frame)
