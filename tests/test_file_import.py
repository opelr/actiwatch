# -*- coding: utf-8 -*-

from .context import actiwatch
import unittest
import pandas as pd


class FileImport_Test(unittest.TestCase):
    def setUp(self):
        self.path = "tests/data/Example_Data_Bedtime.csv"

    def test_import(self):
        headers = actiwatch.file_import.get_actigraphy_headers(self.path)
        assert headers is not None
        assert type(headers) == dict

        data = actiwatch.file_import.parse_actigraphy_data(self.path, headers)
        assert data is not None
        assert type(data) == pd.DataFrame

    def test_actigraphy_class(self):
        watch = actiwatch.Actiwatch(
            path=self.path, start_hour=16, sleep_threshold=40, manually_scored=True
        )
        assert watch is not None
        assert type(watch.data) == pd.DataFrame


if __name__ == "__main__":
    unittest.main()
