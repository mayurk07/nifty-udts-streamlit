import pytz
from datetime import datetime, time

IST = pytz.timezone("Asia/Kolkata")

df = yf.download(
    symbol,
    period="2mo",
    interval="1d",
    auto_adjust=False,
    progress=False
)

df = df.dropna()

now = datetime.now(IST)

# If market is open, drop today's candle
if time(9, 15) <= now.time() <= time(15, 30):
    df = df.iloc[:-1]
