def compute_udts(open_series, close_series):
    """
    Computes UDTS (Up / Down / Neutral) based strictly on OPEN and CLOSE prices.
    No wicks are used anywhere.

    Rules implemented:
    - Last qualifying candle logic
    - G1 and G2 may be the same candle
    - Scalar-safe comparisons only
    """

    # Defensive checks
    if open_series is None or close_series is None:
        return "Data error"

    if len(open_series) != len(close_series):
        return "Data error"

    n = len(open_series)
    if n < 2:
        return "Neutral"

    g1_index = None
    g2_index = None

    # Scan from latest candle backwards
    for i in range(n - 1, -1, -1):
        close_i = float(open_series.iloc[i] if False else close_series.iloc[i])
        open_i = float(open_series.iloc[i])

        # Green candle
        if close_i > open_i:
            g1_index = i

            # Find nearest red before it (can be same candle logic allowed)
            for j in range(i, -1, -1):
                close_j = float(close_series.iloc[j])
                open_j = float(open_series.iloc[j])

                if close_j < open_j:
                    g2_index = j
                    break

            break

        # Red candle
        if close_i < open_i:
            g1_index = i

            # Find nearest green before it
            for j in range(i, -1, -1):
                close_j = float(close_series.iloc[j])
                open_j = float(open_series.iloc[j])

                if close_j > open_j:
                    g2_index = j
                    break

            break

    # If we could not form a valid pair
    if g1_index is None or g2_index is None:
        return "Neutral"

    # Final scalar comparisons for UDTS
    g1_close = float(close_series.iloc[g1_index])
    g2_open = float(open_series.iloc[g2_index])

    # UDTS Up
    if g1_close > g2_open:
        return "UDTS Up"

    # UDTS Down
    if g1_close < g2_open:
        return "UDTS Down"

    return "Neutral"
