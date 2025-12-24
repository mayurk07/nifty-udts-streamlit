import streamlit as st
import yfinance as yf
import pytz
from datetime import datetime, time

from udts_logic import compute_udts

# -------------------------------------------------
# Config
# -------------------------------------------------
st.set_page_config(layout="wide")
st.title("UDTS – Iteration 1 (Single Stock with Scoring)")

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


def score_from_udts(result):
    if result is None:
        return 0

    r = result.lower()

    if "up" in r:
        return 100
    if "down" in r:
        return -100

    return 0

# -------------------------------------------------
# Fetch data
# -------------------------------------------------
daily_df   = fetch_history(symbol, "1d", "3mo")
weekly_df  = fetch_history(symbol, "1wk", "6mo")
monthly_df = fetch_history(symbol, "1mo", "1y")
hourly_df  = fetch_history(symbol, "60m", "10d")
m15_df     = fetch_history(symbol, "15m", "5d")

# -------------------------------------------------
# Drop forming candles
# -------------------------------------------------
now = datetime.now(IST)

# Daily
if time(9, 15) <= now.time() <= time(15, 30):
    daily_df = daily_df.iloc[:-1]

# Intraday
hourly_df = hourly_df.iloc[:-1]
m15_df = m15_df.iloc[:-1]

# Weekly / Monthly (closed only)
weekly_df = weekly_df.iloc[:-1]
monthly_df = monthly_df.iloc[:-1]

# -------------------------------------------------
# UDTS + scoring
# -------------------------------------------------
rows = []

for tf, df in [
    ("Monthly", monthly_df),
    ("Weekly", weekly_df),
    ("Daily", daily_df),
    ("Hourly", hourly_df),
    ("15 Min", m15_df),
]:
    udts = compute_udts(df["Open"], df["Close"])
    score = score_from_udts(udts)

    rows.append({
        "Timeframe": tf,
        "UDTS": udts,
        "Score": score,
    })

total_score = sum(r["Score"] for r in rows)

# -------------------------------------------------
# Display
# -------------------------------------------------
st.subheader(f"{symbol} – Trend Scores")

st.table(rows)

st.markdown(f"### **Total Trend Score: {total_score}**")

st.caption(
    "Iteration 1 – Step 2: "
    "UDTS-based scoring (+100 / −100 / 0) across 5 timeframes"
)
