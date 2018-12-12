"""Unittest of actigex.app.rle"""

from .context import actiwatch
import unittest


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.input_string = "aabbabc"
        self.expected_output = [[2, "a"], [2, "b"], [1, "a"], [1, "b"], [1, "c"]]

    def test_encode(self):
        assert self.expected_output == actiwatch.helpers.encode(list(self.input_string))

    def test_decode(self):
        assert list(self.input_string) == actiwatch.helpers.decode(self.expected_output)


if __name__ == "__main__":
    unittest.main()
