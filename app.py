import streamlit as st
import yfinance as yf
import pytz
from datetime import datetime, time

# ----------------------------
# Config
# ----------------------------
st.set_page_config(layout="wide")
st.title("INFY – Daily OHLC Check (Yahoo via Ticker.history)")

IST = pytz.timezone("Asia/Kolkata")
symbol = "INFY.NS"

# ----------------------------
# Fetch data (Yahoo chart API)
# ----------------------------
ticker = yf.Ticker(symbol)

df = ticker.history(
    period="2mo",
    interval="1d",
    auto_adjust=False,
    actions=False
)

df = df.dropna()

# ----------------------------
# Timezone-safe normalization
# ----------------------------
if df.index.tz is None:
    df.index = df.index.tz_localize("UTC").tz_convert(IST)
else:
    df.index = df.index.tz_convert(IST)

df.index = df.index.normalize()

# ----------------------------
# Drop today's candle if market open
# ----------------------------
now = datetime.now(IST)
if time(9, 15) <= now.time() <= time(15, 30):
    df = df.iloc[:-1]

# ----------------------------
# Display
# ----------------------------
st.subheader(f"{symbol} – last 10 daily candles (Open / Close)")
st.dataframe(df[["Open", "Close"]].tail(10))

st.caption(
    "Source: Yahoo Finance chart API (Ticker.history), "
    "unadjusted prices, IST-normalized, only fully closed candles."
)
