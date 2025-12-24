import yfinance as yf
import pandas as pd

def fetch_ohlc(symbol, interval, period):
    """
    interval: '1mo', '1wk', '1d', '1h', '15m'
    period: e.g. '6mo', '60d', '7d'
    """
    try:
        df = yf.download(
            symbol,
            interval=interval,
            period=period,
            progress=False,
            threads=False
        )
        if df.empty:
            return None

        df = df.reset_index()
        df = df[["Open", "Close"]]
        return df.tail(60)  # more than 24 for safety

    except Exception:
        return None
