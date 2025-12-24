import yfinance as yf
import pytz
from datetime import datetime, time

IST = pytz.timezone("Asia/Kolkata")

ticker = yf.Ticker("INFY.NS")

df = ticker.history(
    period="2mo",
    interval="1d",
    auto_adjust=False,
    actions=False
)

df = df.dropna()

# Convert to IST dates
df.index = (
    df.index
    .tz_localize("UTC")
    .tz_convert("Asia/Kolkata")
    .normalize()
)

# Drop today if market is open
now = datetime.now(IST)
if time(9, 15) <= now.time() <= time(15, 30):
    df = df.iloc[:-1]
