import streamlit as st
from udts_logic import compute_udts

st.set_page_config(layout="wide")

st.title("UDTS Diagnostic")

result = compute_udts(None, None)

st.success(f"UDTS import worked: {result}")
