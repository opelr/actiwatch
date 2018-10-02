"""Sunrise and Sunset times"""

from datetime import datetime
import pandas as pd
import numpy as np
from astral import Location


def get_sunrise(df, date_column: str):
    """Calculate sunrise and sunset data from a given long/lat pair

    Args:
        df (pd.DataFrame): Data frame to be processed and returned
        date_column (str): Name of column in `df` that contains dates.

    Returns:
        DataFrame with sunrise and sunset time appended for each observation
    """
    row_verification = len(df.index)
    dates = sorted(list(set(df[date_column])))

    ## Get sunrise/sunset times
    portland = Location(("Portland", "USA", 45.5231, -122.6765, "US/Pacific", 50))
    unique_datetimes = [datetime.strptime(x, "%Y-%m-%d") for x in dates]
    sun_dict = {i: portland.sun(j) for i, j in zip(dates, unique_datetimes)}

    sun_DF = pd.DataFrame.from_dict(sun_dict, orient="index")
    sun_DF["Date"] = sun_DF.index
    sun_DF = sun_DF.reset_index()
    sun_DF = sun_DF[["Date", "sunrise", "sunset"]]
    sun_DF.rename({"Date": date_column}, inplace=True)

    ## Merge sun_DF and df
    df_merged = pd.merge(df, sun_DF, on=date_column, how="inner")
    df_merged["DateTime"] = pd.to_datetime(df_merged["DateTime"]).dt.tz_localize(
        "US/Pacific", ambiguous="NaT", errors="coerce"
    )
    df_merged["SunPeriod"] = np.where(
        (
            (df_merged["DateTime"] > df_merged["sunrise"])
            & (df_merged["DateTime"] < df_merged["sunset"])
        ),
        "Day",
        "Night",
    )
    assert len(df.index) == row_verification

    return df_merged
