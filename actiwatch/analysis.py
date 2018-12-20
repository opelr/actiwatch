# -*- coding: utf-8 -*-

"""
actiwatch.analysis
~~~~~~~~~~~~~~~~~~

Functions to analyze sleep data
"""

import pandas as pd


def sleep_metrics(df, rec_freq: int):
    """[summary]
    
    Args:
        df ([type]): [description]
        rec_freq (int): [description]
    """
    pivot = pd.pivot_table(
        df,
        values="watch_ID",
        columns=["Sleep_Acti"],
        index=["Split_Day", "Interval"],
        aggfunc="count",
        fill_value=0,
    )
    metrics = pd.DataFrame(pivot.to_records())
    metrics_filter = metrics[metrics.loc[:, "Interval"] == "Rest"]

    metrics_filter.loc[:, "TST_Min"] = metrics_filter.loc[:, "Sleep"] * (rec_freq / 60)
    metrics_filter.loc[:, "WASO_Min"] = metrics_filter.loc[:, "Wake"] * (rec_freq / 60)
    metrics_filter.loc[:, "SE"] = 100 * (
        metrics_filter.loc[:, "Sleep"]
        / (metrics_filter.loc[:, "Sleep"] + metrics_filter.loc[:, "Wake"])
    )
    metrics_filter.loc[:, "watch_ID"] = df.loc[:, "watch_ID"].unique().tolist()[0]

    return metrics_filter


def sleep_latency(df, rec_freq: int):
    """[summary]
    
    Args:
        df ([type]): [description]
        rec_freq (int): [description]
    """
    if not "Falling_Asleep" in df["Interval"].unique():
        return None

    pivot = pd.pivot_table(
        df,
        values="watch_ID",
        columns=["Sleep_Acti"],
        index=["Split_Day", "Interval"],
        aggfunc="count",
        fill_value=0,
    )
    latency = pd.DataFrame(pivot.to_records())
    latency_filter = latency[
        latency.loc[:, "Interval"].isin(["Falling_Asleep", "Waking_Up"])
    ]
    latency_filter.loc[:, "Latency"] = (
        latency_filter.loc[:, "Sleep"] + latency_filter.loc[:, "Wake"]
    ) * (rec_freq / 60)
    latency_filter = latency_filter.drop(columns=["Sleep", "Wake"])
    latency_filter = latency_filter.replace(
        {
            "Interval": {
                "Falling_Asleep": "Sleep_Latency_Min",
                "Waking_Up": "Wake_Latency_Min",
            }
        }
    )

    latency_pivot = latency_filter.pivot(
        index="Split_Day", columns="Interval", values="Latency"
    ).fillna(0)
    return pd.DataFrame(latency_pivot.to_records())


def bedtime(df):
    """[summary]
    
    Args:
        df ([type]): [description]
    """
    if not "Waking_Up" in df["Interval"].unique():
        return None

    bedtime = (
        df[["Split_Day", "DateTime", "Interval"]]
        .groupby(["Split_Day", "Interval"])
        .min()
        .reset_index()
    )
    bedtime_pivot = pd.DataFrame(
        bedtime.pivot(
            index="Split_Day", columns="Interval", values="DateTime"
        ).to_records()
    )
    bedtime_pivot = bedtime_pivot.drop(columns=["Falling_Asleep", "Active"])

    # TODO: Midsleep time
    # bedtime_pivot["Mid_Sleep"] = bedtime_pivot[["Waking_Up","Rest"]]
    bedtime_pivot.loc[:, "Time_Bed"] = bedtime_pivot.loc[:, "Rest"].apply(
        lambda x: x.hour + x.minute / 60
    )
    bedtime_pivot.loc[:, "Time_Wake"] = bedtime_pivot.loc[:, "Waking_Up"].apply(
        lambda x: x.hour + x.minute / 60
    )
    return bedtime_pivot


def rhythm_stability(df, rec_freq: int):
    # TODO:
    raise NotImplementedError


def relative_amplitude(df, start_time: int):
    """[summary]
    
    Args:
        df ([type]): [description]
        start_time (int): [description]
    """
    hours = sorted(df["Hour"].unique())
    hours = hours[start_time::] + hours[:start_time]

    rest_phase = (
        df[["Split_Day", "Hour", "Activity"]]
        .groupby(["Split_Day", "Hour"])
        .sum()
        .reset_index()
    )
    rest_phase["Order"] = rest_phase["Hour"].apply(lambda x: hours.index(x))
    rest_phase = rest_phase.sort_values(by=["Split_Day", "Order"])

    rest_phase["Activity_Sum_10"] = (
        rest_phase.groupby(["Split_Day"])["Activity"].rolling(10).sum().tolist()
    )
    rest_phase["Activity_Sum_5"] = (
        rest_phase.groupby(["Split_Day"])["Activity"].rolling(5).sum().tolist()
    )

    m10 = (
        rest_phase.groupby(["Split_Day"])["Activity_Sum_10"]
        .max()
        .reset_index()
        .rename(columns={"Activity_Sum_10": "M10"})
    )
    l5 = (
        rest_phase.groupby(["Split_Day"])["Activity_Sum_5"]
        .min()
        .reset_index()
        .rename(columns={"Activity_Sum_5": "L5"})
    )

    ra = m10.merge(l5, on="Split_Day")
    ra["RA"] = (ra["M10"] - ra["L5"]) / (ra["M10"] + ra["L5"])
    ra = ra.drop(columns=["M10", "L5"])
    return ra


def total_values(df, rec_freq: int):
    return pd.DataFrame(
        pd.pivot_table(
            df,
            values=["Activity", "Light"],
            index=["Split_Day"],
            aggfunc="sum",
            fill_value=0,
        ).to_records()
    )