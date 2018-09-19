"""Unittest of actigex.app.file_import"""

import unittest
from actiwatch import file_import, actiwatch

class FileImport_Test(unittest.TestCase):
    def setUp(self):
        self.path = 'actiwatch/tests/Example_Data_Bedtime.csv'
    
    def test_import(self):
        headers = file_import.get_actigraphy_headers(self.path)
        self.assertIsNotNone(headers)
        data = file_import.parse_actigraphy_data(self.path, headers)
        self.assertIsNotNone(data)

    def test_actigraphy_class(self):
        watch = actiwatch.Actiwatch(path=self.path, manually_scored=False)
        self.assertIsNotNone(watch)

if __name__ == "__main__":
    unittest.main()