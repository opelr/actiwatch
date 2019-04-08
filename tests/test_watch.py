# -*- coding: utf-8 -*-

from .context import actiwatch
import unittest


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.path = "tests/data/Example_Data_Bedtime.csv"
        self.watch = actiwatch.Actiwatch(
            path=self.path, start_hour=16, sleep_threshold=40, manually_scored=True
        )

    def test_class_method(self):
        watch_dict = {
            "path": self.path,
            "start_hour": 16,
            "sleep_threshold": 40,
            "manually_scored": True,
        }
        watch_class_method = actiwatch.Actiwatch.from_dict(watch_dict)
        watch_standard = actiwatch.Actiwatch(
            path=self.path, start_hour=16, sleep_threshold=40, manually_scored=True
        )
        assert watch_class_method == watch_standard
