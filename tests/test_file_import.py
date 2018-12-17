"""Unittest of actigex.file_import"""

from .context import actiwatch
import unittest


class FileImport_Test(unittest.TestCase):
    def setUp(self):
        self.path = "tests/data/Example_Data_Bedtime.csv"

    def test_import(self):
        headers = actiwatch.file_import.get_actigraphy_headers(self.path)
        self.assertIsNotNone(headers)
        data = actiwatch.file_import.parse_actigraphy_data(self.path, headers)
        self.assertIsNotNone(data)

    def test_actigraphy_class(self):
        watch = actiwatch.Actiwatch(path=self.path, manually_scored=False, sleep_threshold=40)
        self.assertIsNotNone(watch)


if __name__ == "__main__":
    unittest.main()
