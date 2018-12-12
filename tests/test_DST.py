"""Unittest of actigex.app.file_import"""

from .context import actiwatch
import unittest
import pandas as pd


class TZ_Localize_Test(unittest.TestCase):
    def test_dst(self):
        df = pd.DataFrame(
            {
                "DateTime": [
                    "2018-03-11 00:00:00",
                    "2018-03-11 01:00:00",
                    "2018-03-11 02:00:00",
                    "2018-03-11 03:00:00",
                    "2018-03-11 04:00:00",
                ]
            }
        )
        df["DateTime"] = pd.to_datetime(df["DateTime"], format="%Y-%m-%d %H:%M:%S")

        try:
            pd.to_datetime(df["DateTime"]).dt.tz_localize(
                "US/Pacific", ambiguous="NaT", errors="coerce"
            )
        except pytz.exceptions.NonExistentTimeError:
            self.fail("Daylight Savings Time error during localization")


if __name__ == "__main__":
    unittest.main()
