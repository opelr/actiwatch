# -*- coding: utf-8 -*-

"""
actiwatch.watch
~~~~~~~~~~~~~~~

Parent class wrapper for Actiware CSVs
"""

from .file_import import get_actigraphy_headers, parse_actigraphy_data
from .helpers import get_sunrise, enum_dates, split_days
from .sleep_processing import windowed_sleep, smooth_sleep
from .analysis import (
    sleep_metrics,
    sleep_latency,
    bedtime,
    relative_amplitude,
    total_values,
)


class Actiwatch:
    """Actigraphy data analysis parent class

    Args:
        path (str): Filepath to a raw, Actiware-exported CSV file
        manually_scored (bool): Is the file of the 'Bedtime' variety?
        sleep_threshold (int): Activity threshold for wake scoring (20 = low, 40 = medium, 80 = high)
    """

    def __init__(self, path, start_time, sleep_threshold, manually_scored):
        self._path = path
        self._start_time = start_time
        self._sleep_threshold = sleep_threshold
        self._manually_scored = manually_scored

        self.header = get_actigraphy_headers(self._path)
        self._recording_interval = self.header.iloc[0]["recording_epoch_length"]
        self.patient_id = self.header["watch_ID"][0]

        self.data = self._generate_data()

    def __repr__(self):
        return f"<Actiwatch [{self.patient_id}]>"

    def _generate_data(self):
        """Aggregate all shaping functions from the module, creating a single
        DataFrame to be passed to `self.data`"""
        dat = parse_actigraphy_data(self._path, self.header, self._manually_scored)
        dat = enum_dates(dat)
        dat = dat.sort_values(by=["Line"])
        dat = split_days(dat, self._start_time)
        dat["Sleep_Acti"] = windowed_sleep(
            dat["Activity"].tolist(), self._sleep_threshold, self._recording_interval
        )
        dat["Sleep_Acti_Smooth"] = smooth_sleep(
            dat["Sleep_Acti"].tolist(), self._recording_interval
        )
        return dat

    @property
    def sleep_metrics(self):
        return sleep_metrics(self.data, self._recording_interval)

    @property
    def sleep_latency(self):
        return sleep_latency(self.data, self._recording_interval)

    @property
    def bedtime(self):
        return bedtime(self.data)

    @property
    def relative_amplitude(self):
        return relative_amplitude(self.data, self._start_time)

    @property
    def total_values(self):
        return total_values(self.data, self._recording_interval)
