from datetime import datetime, time
import pytz

IST = pytz.timezone("Asia/Kolkata")

def is_weekly_last_candle_in_scope(now=None):
    if not now:
        now = datetime.now(IST)

    weekday = now.weekday()  # Monday = 0
    t = now.time()

    if weekday == 3 and t >= time(15, 30):  # Thursday after 3:30pm
        return True
    if weekday in [4, 5, 6]:  # Fri, Sat, Sun
        return True
    if weekday == 0 and t < time(9, 15):  # Monday before open
        return True

    return False
