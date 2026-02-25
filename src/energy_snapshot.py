from __future__ import annotations

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    raise SystemExit(
        "Missing dependency: yfinance. Install it with:\n"
        "  pip install yfinance\n"
        "Then re-run this script."
    )

TICKERS = {
    "Equinor": "EQNR",
    "Aker BP": "AKRBP.OL",
    "ExxonMobil": "XOM",
    "NextEra": "NEE",
    "Tesla": "TSLA",
}

def fetch_prices(ticker: str, period: str = "3mo") -> pd.Series:
    df = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    close = df["Close"]

    # yfinance sometimes returns a DataFrame 
    # so force it into a 1D Series
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return close.dropna()

def pct_return(close: pd.Series, trading_days: int = 30) -> float:
    # 30 trading days is roughly ~6 weeks.
    if len(close) <= trading_days:
        raise ValueError("Not enough data to compute return")
    start = close.iloc[-(trading_days + 1)]
    end = close.iloc[-1]
    return float((end / start - 1) * 100)

def main() -> None:
    rows = []
    for name, ticker in TICKERS.items():
        close = fetch_prices(ticker)
        r_30 = pct_return(close, trading_days=30)
        rows.append({"Company": name, "Ticker": ticker, "Return_30d_%": r_30})

    out = pd.DataFrame(rows).sort_values("Return_30d_%", ascending=False)
    out["Return_30d_%"] = out["Return_30d_%"].map(lambda x: round(x, 2))
    print(out.to_string(index=False))

    # Save output (tangible artifact)
    output_path = "data/energy_snapshot_30d.csv"
    out.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

if __name__ == "__main__":
    main()