def compute_udts(open_series, close_series):
last_open = float(open_series.values[-1])
last_close = float(close_series.values[-1])

if last_close > last_open:
return "Up"
else:
return "Down"
