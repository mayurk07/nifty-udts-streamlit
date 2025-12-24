import streamlit as st
import yfinance as yf
from udts_logic import compute_udts

st.set_page_config(layout="wide")

st.title("UDTS Step 6 – Candle Color Check")

symbol = "INFY.NS"

df = yf.download(
    symbol,
    period="1mo",
    interval="1d",
    progress=False
)

df = df.dropna()

result = compute_udts(df["Open"], df["Close"])

st.write(f"Last daily candle for {symbol}: {result}")
st.dataframe(df[["Open", "Close"]].tail(10))
