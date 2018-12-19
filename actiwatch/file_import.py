# -*- coding: utf-8 -*-

"""
actiwatch.file_import
~~~~~~~~~~~~~~~~~~~~~

Performs basic file I/O and shaping of an Actiwatch CSV file
"""

from datetime import datetime
import pandas as pd
import numpy as np
import re
import calendar

from .helpers import encode, decode, make_sleep_interval


def get_actigraphy_headers(path):
    """Strips header information from exported Actiware CSV file

    Args:
        path (str): Full filepath of an Actiware CSV

    Returns:
        Data frame containing header information from a single file
    """

    # Read CSV to table
    forced_names = ["X" + i for i in list(map(str, list(range(1, 45))))]
    csv = pd.read_csv(path, names=forced_names, low_memory=False)

    # Strip header information to temporary variables
    def strip_csv(string, as_date=False):
        var_out = csv["X2"][csv["X1"] == string]
        var_out = var_out.tolist()[0]

        if as_date:
            var_out = datetime.strptime(var_out, "%Y-%m-%d")
        return var_out

    patient_name = strip_csv("Identity:")
    patient_sex = strip_csv("Gender:")
    patient_DOB = strip_csv("Date of Birth:", True)
    patient_age = int(strip_csv("Age (at start of data collection):"))

    recording_date_start = strip_csv("Data Collection Start Date:", True)
    recording_date_end = strip_csv("Data Collection End Date:", True)
    recording_days_span = float(strip_csv("Number of Days:"))
    recording_epoch_length = int(strip_csv("Epoch Length:"))

    watch_serial_no = strip_csv("Actiwatch Serial Number:")
    calibration_activity = int(strip_csv("Activity Calibration Factor:"))
    calibration_light = int(strip_csv("White Calibration Factor:"))
    threshold_wake = float(strip_csv("Wake Threshold Value:"))
    threshold_light = float(strip_csv("White Light Threshold:"))

    # Create data frame with stripped variables
    header_dict = {
        "watch_ID": re.sub(" ", "_", patient_name),
        "patient_sex": patient_sex,
        "patient_DOB": patient_DOB,
        "patient_age": patient_age,
        "recording_date_start": recording_date_start,
        "recording_date_end": recording_date_end,
        "recording_days_span": recording_days_span,
        "recording_epoch_length": recording_epoch_length,
        "watch_serial_no": watch_serial_no,
        "calibration_activity": calibration_activity,
        "calibration_light": calibration_light,
        "threshold_wake": threshold_wake,
        "threshold_light": threshold_light,
    }
    header_info = pd.DataFrame([header_dict])
    return header_info


def parse_actigraphy_data(path, header_info, manually_scored=False):
    """Strips epoch-by-epoch data from exported Actiware CSV file

    Args:
        path (str): Full filepath of an Actiware CSV
        header_info(DataFrame): Object generated from `get_actigraphy_headers`
                                function.

    Returns:
        Data frame containing epoch-by-epoch data for a single file
    """

    ## Read entire CSV file to a table, force number of columns
    forced_names = ["X" + i for i in list(map(str, list(range(1, 45))))]
    csv = pd.read_csv(
        path, names=forced_names, low_memory=False, skip_blank_lines=False
    )

    ## Find Epoch-by-Epoch data and skip to it
    start_row = csv.index[csv["X1"] == "Line"].tolist()[-1]

    csv = pd.read_csv(path, low_memory=False, skiprows=start_row)
    csv = csv.drop(["S/W Status", "Unnamed: 13"], axis=1)
    csv = csv.rename(
        index=str,
        columns={
            "White Light": "Light",
            "Sleep/Wake": "Sleep_Acti",
            "Interval Status": "Interval",
        },
    )
    csv = csv.replace({"Sleep_Acti": {1.0: "Wake", 0.0: "Sleep"}})
    csv["Interval"] = np.where(csv["Interval"] == "ACTIVE", "Active", "Rest")
    csv["watch_ID"] = header_info.iloc[0]["watch_ID"]

    ## Bed-/wake-time manual scoring
    if manually_scored:
        csv["Interval"] = make_sleep_interval(csv["Interval"].tolist())

    ## Datetime calculations
    csv["DateTime"] = pd.to_datetime(
        csv["Date"] + " " + csv["Time"], format="%Y-%m-%d %I:%M:%S %p"
    )
    # .dt.tz_localize("US/Pacific", ambiguous="NaT", errors="coerce")
    csv = csv[csv["DateTime"].notna()]
    csv["ClockTime"] = pd.to_datetime(csv["Time"], format="%I:%M:%S %p")
    csv["Hour"] = csv["ClockTime"].apply(lambda x: x.hour)
    csv["AM_PM"] = np.floor(csv["Hour"] / 12)
    csv["AM_PM"] = csv.replace({"AM_PM": {1.0: "PM", 0.0: "AM"}})
    csv["Day_of_Week"] = csv["DateTime"].apply(lambda x: calendar.day_name[int(x.weekday())])
    csv["Weekend"] = csv["Day_of_Week"].apply(
        lambda y: any(x in y for x in ["Saturday", "Sunday"])
    )
    csv["DateAbbr"] = csv["DateTime"].dt.strftime("%b %d")
    csv["Month"] = csv["DateTime"].dt.strftime("%B")

    ## Add log-space columns -- adding 1 to avoid div/0 errors
    csv["Activity"] = csv["Activity"] + 1
    csv["Light"] = csv["Light"] + 1
    csv["Log_Activity"] = np.log10(csv["Activity"] + 1)
    csv["Log_Light"] = np.log10(csv["Light"])

    ## Zeitgeber Time bins
    ### ZT6
    zt_6_hours = []
    for hr in [["12AM-6AM"], ["6AM-12PM"], ["12PM-6PM"], ["6PM-12AM"]]:
        zt_6_hours.append(hr * 6)

    ### ZT 12
    zt_12_hours = []
    for hr in [["6PM-6AM"], ["6AM-6PM"], ["6AM-6PM"], ["6PM-6AM"]]:
        zt_12_hours.append(hr * 6)

    zt_6_hours = [i for j in zt_6_hours for i in j]
    zt_12_hours = [i for j in zt_12_hours for i in j]

    zt_bins = pd.DataFrame(
        list(zip(range(24), zt_6_hours, zt_12_hours)), columns=["Hour", "ZT6", "ZT12"]
    )

    ### Merge
    csv = pd.merge(csv, zt_bins, on="Hour", how="inner")
    return csv
