import streamlit as st
import yfinance as yf
import pytz
from datetime import datetime, time

from udts_logic import compute_udts

# -------------------------------------------------
# Config
# -------------------------------------------------
st.set_page_config(layout="wide")
st.title("UDTS – Iteration 1 (Single Stock, All Timeframes)")

IST = pytz.timezone("Asia/Kolkata")
symbol = "INFY.NS"

# -------------------------------------------------
# Helper: fetch candles safely
# -------------------------------------------------
def fetch_history(symbol, interval, period):
    ticker = yf.Ticker(symbol)
    df = ticker.history(
        interval=interval,
        period=period,
        auto_adjust=False,
        actions=False
    )
    df = df.dropna()

    # Timezone handling
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(IST)
    else:
        df.index = df.index.tz_convert(IST)

    return df


# -------------------------------------------------
# Fetch data
# -------------------------------------------------
daily_df   = fetch_history(symbol, "1d", "3mo")
weekly_df  = fetch_history(symbol, "1wk", "6mo")
monthly_df = fetch_history(symbol, "1mo", "1y")
hourly_df  = fetch_history(symbol, "60m", "10d")
m15_df     = fetch_history(symbol, "15m", "5d")

# -------------------------------------------------
# Drop forming candles where required
# -------------------------------------------------
now = datetime.now(IST)

# Daily – drop today if market open
if time(9, 15) <= now.time() <= time(15, 30):
    daily_df = daily_df.iloc[:-1]

# Hourly & 15m – always drop last candle (forming)
hourly_df = hourly_df.iloc[:-1]
m15_df = m15_df.iloc[:-1]

# Weekly / Monthly – for now, use last closed candle only
weekly_df = weekly_df.iloc[:-1]
monthly_df = monthly_df.iloc[:-1]

# -------------------------------------------------
# Run UDTS
# -------------------------------------------------
results = {
    "Monthly": compute_udts(monthly_df["Open"], monthly_df["Close"]),
    "Weekly":  compute_udts(weekly_df["Open"], weekly_df["Close"]),
    "Daily":   compute_udts(daily_df["Open"], daily_df["Close"]),
    "Hourly":  compute_udts(hourly_df["Open"], hourly_df["Close"]),
    "15 Min":  compute_udts(m15_df["Open"], m15_df["Close"]),
}

# -------------------------------------------------
# Display
# -------------------------------------------------
st.subheader(f"{symbol} – UDTS status")

for tf, res in results.items():
    st.write(f"**{tf}** : {res}")

st.caption("Iteration 1: Yahoo Finance data, open/close only, fully closed candles")
