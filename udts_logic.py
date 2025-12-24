def compute_udts(open_series, close_series):
    """
    SAFE v1:
    - Determines only the LAST candle color
    - Uses ONLY float comparisons
    """

    if open_series is None or close_series is None:
        return "Neutral"

    if len(open_series) == 0:
        return "Neutral"

    # Force scalar extraction
    last_open = float(open_series.iloc[-1])
    last_close = float(close_series.iloc[-1])

    if last_close > last_open:
        return "Green"
    elif last_close < last_open:
        return "Red"
    else:
        return "Neutral"
