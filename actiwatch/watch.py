# -*- coding: utf-8 -*-

"""
actiwatch.watch
~~~~~~~~~~~~~~~

Parent class wrapper for Actiware CSVs
"""

from .file_import import get_actigraphy_headers, parse_actigraphy_data
from .helpers import get_sunrise, enum_dates
from .sleep_processing import windowed_sleep, process_sleep


class Actiwatch:
    """Actigraphy data analysis parent class

    Args:
        path (str): Filepath to a raw, Actiware-exported CSV file
        manually_scored (bool): Is the file of the 'Bedtime' variety?
    """

    def __init__(self, path, manually_scored):
        self._path = path
        self._manually_scored = manually_scored
        self.header_info = get_actigraphy_headers(self._path)
        self.patient_ID = self.header_info["watch_ID"][0]
        self.data = self.generate_data()

    def generate_data(self):
        """Aggregate all shaping functions from the module, creating a single
        DataFrame to be passed to `self.data`"""
        dat = parse_actigraphy_data(self._path, self.header_info, self._manually_scored)
        dat = get_sunrise(dat, "Date")
        dat = enum_dates(dat)
        dat["Sleep_Acti"] = windowed_sleep(dat["Activity"].tolist(), 40)
        dat = process_sleep(dat)
        return dat
