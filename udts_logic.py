def compute_udts(open_series, close_series):
    """
    UDTS calculation using ONLY open and close prices.
    No wicks. Scalar-safe. Streamlit-safe.
    """

    # Basic safety
    if open_series is None or close_series is None:
        return "Neutral"

    if len(open_series) != len(close_series):
        return "Neutral"

    n = len(open_series)
    if n < 2:
        return "Neutral"

    # Helper functions – ALWAYS return float
    def o(i):
        return float(open_series.iloc[i])

    def c(i):
        return float(close_series.iloc[i])

    g1_index = None
    r1_index = None

    # Step 1: Find G1 and nearest R1 before it
    for i in range(n - 1, -1, -1):
        if c(i) > o(i):  # green candle
            for j in range(i - 1, -1, -1):
                if c(j) < o(j):  # red candle
                    if c(i) > o(j):
                        g1_index = i
                        r1_index = j
                        break
            if g1_index is not None:
                break

    if g1_index is None or r1_index is None:
        return "Neutral"

    # Step 2: Look to the right of G1 for R2–G2
    for k in range(g1_index + 1, n):
        if c(k) < o(k):  # red candle
            for m in range(k - 1, g1_index - 1, -1):
                if c(m) > o(m):  # green candle
                    if c(k) < o(m):
                        return "UDTS Down"
                    break

    return "UDTS Up"
