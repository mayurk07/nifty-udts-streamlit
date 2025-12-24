def compute_udts(open_series, close_series):
    """
    Returns:
    - "UDTS_UP"
    - "UDTS_DOWN"
    - "NO_UDTS"
    """

    if len(open_series) < 2:
        return "NO_UDTS"

    last_green_idx = None
    last_red_idx = None

    for i in range(len(open_series) - 1, -1, -1):
        o = float(open_series.iloc[i].item())
        c = float(close_series.iloc[i].item())

        if c > o and last_green_idx is None:
            last_green_idx = i

        if c < o and last_red_idx is None:
            last_red_idx = i

        if last_green_idx is not None and last_red_idx is not None:
            break

    if last_green_idx is None or last_red_idx is None:
        return "NO_UDTS"

    # UDTS UP: green close > prior red open
    if last_green_idx > last_red_idx:
        green_close = float(close_series.iloc[last_green_idx].item())
        red_open = float(open_series.iloc[last_red_idx].item())
        if green_close > red_open:
            return "UDTS_UP"

    # UDTS DOWN: red close < prior green open
    if last_red_idx > last_green_idx:
        red_close = float(close_series.iloc[last_red_idx].item())
        green_open = float(open_series.iloc[last_green_idx].item())
        if red_close < green_open:
            return "UDTS_DOWN"

    return "NO_UDTS"
