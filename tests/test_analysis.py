# -*- coding: utf-8 -*-

from .context import actiwatch
import unittest
import pandas as pd


class AnalysisTest(unittest.TestCase):
    def setUp(self):
        self.path = "tests/data/Example_Data_Bedtime.csv"
        self.watch = actiwatch.Actiwatch(
            path=self.path, manually_scored=True, sleep_threshold=40
        )

    def test_sleep_metrics(self):
        out = actiwatch.analysis.sleep_metrics(
            self.watch.data, self.watch._recording_interval
        )
        assert type(out) == pd.DataFrame
        assert all(
            [i in out.columns for i in ["Split_Day", "TST_Min", "WASO_Min", "SE"]]
        )

    def test_sleep_latency(self):
        out = actiwatch.analysis.sleep_latency(
            self.watch.data, self.watch._recording_interval
        )
        assert type(out) == pd.DataFrame
        assert all(
            [
                i in out.columns
                for i in ["Split_Day", "Sleep_Latency_Min", "Wake_Latency_Min"]
            ]
        )

    def test_bedtime(self):
        out = actiwatch.analysis.bedtime(self.watch.data)
        assert type(out) == pd.DataFrame
        assert all([i in out.columns for i in ["Split_Day", "Time_Bed", "Time_Wake"]])

    def test_rhythm_stability(self):
        pass

    def test_relative_amplitude(self):
        pass

    def test_total_values(self):
        out = actiwatch.analysis.total_values(
            self.watch.data, self.watch._recording_interval
        )
        assert type(out) == pd.DataFrame
        assert all([i in out.columns for i in ["Split_Day", "Activity", "Light"]])
