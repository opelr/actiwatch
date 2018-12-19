# -*- coding: utf-8 -*-

from .context import actiwatch
import unittest
import pandas as pd


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.input_string = "aabbabc"
        self.expected_output = [[2, "a"], [2, "b"], [1, "a"], [1, "b"], [1, "c"]]

    def test_encode(self):
        assert self.expected_output == actiwatch.helpers.encode(list(self.input_string))

    def test_decode(self):
        assert list(self.input_string) == actiwatch.helpers.decode(self.expected_output)

    def test_make_sleep_interval(self):
        inpt = ["Active", "Active", "Rest", "Active", "Active", "Rest", "Active"]
        outpt = [
            "Active",
            "Active",
            "Falling_Asleep",
            "Rest",
            "Rest",
            "Waking_Up",
            "Active",
        ]
        assert actiwatch.helpers.make_sleep_interval(inpt) == outpt

    def test_enum_dates(self):
        dates = pd.date_range(start="2018-01-01", end="2018-01-31", freq="D")
        df = pd.DataFrame({"Date": dates})
        df2 = actiwatch.helpers.enum_dates(df)
        assert df2["Day"].tolist() == list(range(0, 31))

    def test_split_days(self):
        dates = pd.date_range("2018-01-01 08:00:00", "2018-01-04 22:00:00", freq="H")
        df = pd.DataFrame({"DateTime": dates})
        df["Date"] = df["DateTime"].apply(lambda x: str(x.date()))

        out1 = actiwatch.helpers.split_days(df, 16)
        assert (
            out1["Split_Day"][out1["DateTime"] == "2018-01-01 16:00:00"].values[0] == 1
        )

        out2 = actiwatch.helpers.split_days(df, 7)
        assert (
            out2["Split_Day"][out1["DateTime"] == "2018-01-01 16:00:00"].values[0] == 0
        )


if __name__ == "__main__":
    unittest.main()
