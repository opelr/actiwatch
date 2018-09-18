"""Unittest of actigex.app.rle"""

import unittest
from actiwatch import rle

class TestRLE(unittest.TestCase):
    def setUp(self):
        self.input_string = 'aabbabc'
        self.expected_output = [[2, 'a'], [2, 'b'], [1, 'a'], [1, 'b'], [1, 'c']]
    
    def test_encode(self):
        self.assertEqual(self.expected_output, rle.encode(list(self.input_string)))
    
    def test_decode(self):
        self.assertEqual(list(self.input_string), rle.decode(self.expected_output))

if __name__ == "__main__":
    unittest.main()