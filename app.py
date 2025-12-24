import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

from symbols import NSE_100
from data_fetch import fetch_ohlc
from udts_logic import compute_udts

IST = pytz.timezone("Asia/Kolkata")

st.set_page_config(layout="wide")
st.title("NSE UDTS Screener")

st.caption(f"Last updated: {datetime.now(IST).strftime('%d %b %Y %H:%M:%S IST')}")

if st.button("Force Refresh"):
    st.rerun()

rows = []

for symbol in NSE_100:
    monthly = fetch_ohlc(symbol, "1mo", "6mo")
    weekly = fetch_ohlc(symbol, "1wk", "6mo")
    daily = fetch_ohlc(symbol, "1d", "60d")

    if monthly is None or weekly is None or daily is None:
        continue

    m_trend = compute_udts(monthly["Open"], monthly["Close"])
    w_trend = compute_udts(weekly["Open"], weekly["Close"])
    d_trend = compute_udts(daily["Open"], daily["Close"])

    score = (
        (100 if m_trend == "UP" else -100 if m_trend == "DOWN" else 0) +
        (100 if w_trend == "UP" else -100 if w_trend == "DOWN" else 0) +
        (100 if d_trend == "UP" else -100 if d_trend == "DOWN" else 0)
    )

    rows.append({
        "Stock": symbol.replace(".NS", ""),
        "Monthly": m_trend,
        "Weekly": w_trend,
        "Daily": d_trend,
        "Score": score
    })

df = pd.DataFrame(rows).sort_values("Score", ascending=False)

st.dataframe(df, use_container_width=True)

