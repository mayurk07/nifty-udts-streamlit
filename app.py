import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

from udts_logic import compute_udts

st.set_page_config(layout="wide")

st.title("NSE UDTS Screener")
st.caption(f"Last updated: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y %H:%M:%S IST')}")

st.button("Force Refresh")

st.subheader("Step 5: Single Stock – Daily Timeframe")

symbol = "INFY.NS"

@st.cache_data(ttl=900)
def load_daily_data(sym):
    df = yf.download(
        sym,
        period="2mo",
        interval="1d",
        progress=False
    )
    df = df.dropna()
    return df.tail(24)

df = load_daily_data(symbol)

if df.empty:
    st.error("No data received from Yahoo Finance")
    st.stop()

open_series = df["Open"]
close_series = df["Close"]

udts_result = compute_udts(open_series, close_series)

st.write("### Raw OHLC (last 24 daily candles)")
st.dataframe(df[["Open", "Close"]])

st.success(f"UDTS Result for {symbol} (Daily): {udts_result}")
