# -*- coding: utf-8 -*-

"""
actiwatch.helpers
~~~~~~~~~~~~~~~~~

Helper functions
"""

from itertools import groupby, chain
from datetime import datetime
import pandas as pd
import numpy as np

from astral import Location
from typing import Iterable


def encode(sequence: Iterable):
    """Enumerate continuous observations in a sequence

    Args:
        sequence (Iterable): Sequence to enumerate
    """
    return [[len(list(g)), k] for k, g in groupby(sequence)]


def decode(encode_obj: list):
    """Reconstruct `encoded` sequence

    Args:
        encode_obj (list): Encode object (from `encode`) to stitch together
    """
    nested = [[c] * n for n, c in encode_obj]
    return list(chain(*nested))


def make_sleep_interval(vec):
    """Convert manually-scored sleep data to correct interval

    Args:
        vec ([type]): [description]
    """
    sleep_rle = encode(vec)
    if len(sleep_rle) > 4:
        for i in sleep_rle[1::4]:
            i[1] = "Falling_Asleep"

        for i in sleep_rle[2::4]:
            i[1] = "Rest"

        for i in sleep_rle[3::4]:
            i[1] = "Waking_Up"

    return decode(sleep_rle)


# TODO: Portland should not be default, and this should be an optional function
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

    # Get sunrise/sunset times
    portland = Location(("Portland", "USA", 45.5231, -122.6765, "US/Pacific", 50))
    unique_datetimes = [datetime.strptime(x, "%Y-%m-%d") for x in dates]
    sun_dict = {i: portland.sun(j) for i, j in zip(dates, unique_datetimes)}

    sun_DF = pd.DataFrame.from_dict(sun_dict, orient="index")
    sun_DF["Date"] = sun_DF.index
    sun_DF = sun_DF.reset_index()
    sun_DF = sun_DF[["Date", "sunrise", "sunset"]]
    sun_DF.rename({"Date": date_column}, inplace=True)

    # Merge sun_DF and df
    df_merged = pd.merge(df, sun_DF, on=date_column, how="inner")
    df_merged["DateTime"] = pd.to_datetime(df_merged["DateTime"]).dt.tz_localize(
        "US/Pacific", ambiguous="NaT", nonexistent="NaT"
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


def enum_dates(df):
    """Return enumerated Date column

    Args:
        df (pd.DataFrame): Actiware dataframe with "Date" column
    """

    sorted_dates = sorted(list(set(df["Date"])))
    date_DF = pd.DataFrame(list(enumerate(sorted_dates)))
    date_DF.columns = ["Enum_Day", "Date"]

    df = pd.merge(df, date_DF, on="Date", how="inner")
    if "Day" in df.columns:
        df = df.drop(["Day"], axis=1)
    df = df.rename(columns={"Enum_Day": "Day"})
    return df


def split_days(df, time: int):
    """Cut days at specified time.

    Args:
        df (pd.DataFrame): Actiware dataframe with "Date" column
        time (int): Integer hour to split days at (0-23)
    """

    if not isinstance(time, int):
        raise TypeError("'time' must be of type 'int'")

    time_str = str(time % 24).zfill(2) + ":00:00"

    df["Split_Time"] = pd.to_datetime(
        df["Date"] + " " + time_str, format="%Y-%m-%d %H:%M:%S"
    )

    df["Split_Day"] = df["DateTime"] >= df["Split_Time"]

    encoded_days = list(enumerate(encode(df["Split_Day"])))

    if df["Split_Day"][0]:
        remade_days = [((i - (i % 2)) // 2, x[0]) for i, x in encoded_days]
    else:
        remade_days = [((i + 1) // 2, x[0]) for i, x in encoded_days]

    expanded_days = [[i] * x for i, x in remade_days]
    seq_days = list(chain(*expanded_days))
    df["Split_Day"] = seq_days
    del df["Split_Time"]
    return df
