def compute_udts(open_series, close_series):
    """
    open_series, close_series:
    pandas Series indexed oldest → newest
    Uses ONLY open & close (no wicks)
    """

    n = len(open_series)
    if n < 2:
        return "UNDECIDED"

    # Step 1: find G1 and its prior R1
    g1_index = None

    for i in range(n - 1, 0, -1):
        if close_series.iloc[i] > open_series.iloc[i]:  # green candle
            # find nearest red before it
            for j in range(i - 1, -1, -1):
                if close_series.iloc[j] < open_series.iloc[j]:  # red candle
                    if close_series.iloc[i] > open_series.iloc[j]:
                        g1_index = i
                        break
            if g1_index is not None:
                break

    if g1_index is None:
        return "UNDECIDED"

    # Step 2: move rightwards from G1 to find R2–G2
    for k in range(g1_index + 1, n):
        if close_series.iloc[k] < open_series.iloc[k]:  # red candle
            # find nearest green to its left
            for m in range(k - 1, g1_index - 1, -1):
                if close_series.iloc[m] > open_series.iloc[m]:
                    if close_series.iloc[k] < open_series.iloc[m]:
                        return "UDTS_DOWN"
                    break

    return "UDTS_UP"
