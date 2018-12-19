# -*- coding: utf-8 -*-

from .context import actiwatch
import unittest
import numpy as np


class SleepProcessingTest(unittest.TestCase):
    def setUp(self):
        None

    def test_windowed_sleep(self):
        in_15 = [1, 1, 1, 1, 10, 10, 10, 10, 100, 10, 10, 10, 10, 1, 1, 1, 1]
        out_15 = [
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Wake",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
        ]
        assert actiwatch.sleep_processing.windowed_sleep(in_15, 40, 15) == out_15

        in_30 = [1, 1, 10, 10, 100, 10, 10, 1, 1]
        out_30 = [
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
            "Wake",
            "Sleep",
            "Sleep",
            "Sleep",
            "Sleep",
        ]
        assert actiwatch.sleep_processing.windowed_sleep(in_30, 40, 30) == out_30

        in_60 = [1, 10, 100, 10, 1]
        out_60 = ["Sleep", "Sleep", "Wake", "Sleep", "Sleep"]
        assert actiwatch.sleep_processing.windowed_sleep(in_60, 40, 60) == out_60

        in_120 = [10, 100, 10]
        out_120 = ["Sleep", "Wake", "Sleep"]
        assert actiwatch.sleep_processing.windowed_sleep(in_120, 40, 120) == out_120

    def test_cole_post_process(self):
        in_1 = [[10, "Wake"], [1, "Sleep"], [10, "Wake"], [1, "Sleep"], [10, "Wake"]]
        out_1 = [[32, "Wake"]]

        assert actiwatch.sleep_processing.cole_post_process(in_1, 60) == out_1

        in_2 = [[5, "Sleep"], [1, "Wake"]]
        out_2 = [[6, "Sleep"]]

        assert actiwatch.sleep_processing.cole_post_process(in_2, 60) == out_2

    def test_smooth_sleep(self):
        in_1 = ["Sleep", "Sleep", "Sleep", "Sleep", "Sleep", "Wake", "Sleep"]
        out_1 = ["Sleep", "Sleep", "Sleep", "Sleep", "Sleep", "Sleep", "Sleep"]

        assert actiwatch.sleep_processing.smooth_sleep(in_1, 60) == out_1
