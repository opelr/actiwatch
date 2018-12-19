# -*- coding: utf-8 -*-

"""
actiwatch.watch
~~~~~~~~~~~~~~~

Parent class wrapper for Actiware CSVs
"""

from .file_import import get_actigraphy_headers, parse_actigraphy_data
from .helpers import get_sunrise, enum_dates, split_days
from .sleep_processing import windowed_sleep, smooth_sleep


class Actiwatch:
    """Actigraphy data analysis parent class

    Args:
        path (str): Filepath to a raw, Actiware-exported CSV file
        manually_scored (bool): Is the file of the 'Bedtime' variety?
        sleep_threshold (int): Activity threshold for wake scoring (20 = low, 40 = medium, 80 = high)
    """

    def __init__(self, path, manually_scored, sleep_threshold):
        self._path = path
        self._manually_scored = manually_scored
        self._sleep_threshold = sleep_threshold
        self.header_info = get_actigraphy_headers(self._path)
        self._recording_interval = self.header_info.iloc[0]["recording_epoch_length"]
        self.patient_id = self.header_info["watch_ID"][0]
        self.data = self.generate_data()

    def __repr__(self):
        return f"<Actiwatch [{self.patient_id}]>"

    def generate_data(self):
        """Aggregate all shaping functions from the module, creating a single
        DataFrame to be passed to `self.data`"""
        dat = parse_actigraphy_data(self._path, self.header_info, self._manually_scored)
        # dat = get_sunrise(dat, "Date")
        dat = enum_dates(dat)
        dat = dat.sort_values(by=["Line"])
        dat = split_days(dat, 16)
        dat["Sleep_Acti"] = windowed_sleep(
            dat["Activity"].tolist(), 40, self._recording_interval
        )
        dat["Sleep_Acti_Smooth"] = smooth_sleep(
            dat["Sleep_Acti"].tolist(), self._recording_interval
        )
        return dat
