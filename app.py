import streamlit as st
import yfinance as yf
import pytz
from datetime import datetime, time

from udts_logic import compute_udts

IST = pytz.timezone("Asia/Kolkata")

st.set_page_config(layout="wide")
st.title("UDTS – Daily Candle Check")

symbol = "INFY.NS"

df = yf.download(
    symbol,
    period="2mo",
    interval="1d",
    auto_adjust=False,
    progress=False
)

df = df.dropna()

now = datetime.now(IST)

# Drop today's candle if market is open
if time(9, 15) <= now.time() <= time(15, 30):
    df = df.iloc[:-1]

udts_result = compute_udts(df["Open"], df["Close"])

st.write(f"UDTS result (last daily candle): {udts_result}")
st.dataframe(df[["Open", "Close"]].tail(10))
