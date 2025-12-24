def compute_udts(open_series, close_series):
    """
    Placeholder.
    Will implement full G1-R1 / G2-R2 logic next.
    """
    if close_series.iloc[-1] > open_series.iloc[-1]:
        return "UP"
    elif close_series.iloc[-1] < open_series.iloc[-1]:
        return "DOWN"
    return "NEUTRAL"
