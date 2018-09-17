"""Determining Day Number by Date"""

import pandas as pd


def enum_dates(df):
    """Return enumerated Date column

    Args:
        df (pd.DataFrame): Actiware dataframe with "Date" column
    """

    sorted_dates = sorted(list(set(df["Date"])))
    date_DF = pd.DataFrame(list(enumerate(sorted_dates)))
    date_DF.columns = ["Enum_Day", "Date"]

    df = pd.merge(df, date_DF, on="Date", how="inner")
    df = df.drop(["Day"], axis=1)
    df = df.rename(columns={"Enum_Day": "Day"})
    return df
