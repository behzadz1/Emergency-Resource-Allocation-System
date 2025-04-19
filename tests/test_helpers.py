# tests/test_helpers.py

import unittest
from utils.helpers import calculate_zone_distance, _extract_zone_number


class TestHelpers(unittest.TestCase):

    def test_extract_zone_number_valid(self):
        self.assertEqual(_extract_zone_number("Zone 1"), 1)
        self.assertEqual(_extract_zone_number("Zone 10"), 10)
        self.assertEqual(_extract_zone_number("Z3"), 3)

    def test_extract_zone_number_invalid(self):
        with self.assertRaises(ValueError):
            _extract_zone_number("Unknown")

    def test_calculate_zone_distance(self):
        self.assertEqual(calculate_zone_distance("Zone 1", "Zone 3"), 2)
        self.assertEqual(calculate_zone_distance("Zone 5", "Zone 2"), 3)
        self.assertEqual(calculate_zone_distance("Zone 7", "Zone 7"), 0)

    def test_calculate_zone_distance_with_invalid_input(self):
        # If input format fails, fallback should return large distance
        self.assertEqual(calculate_zone_distance("A", "B"), 99)
        self.assertEqual(calculate_zone_distance("Zone X", "Zone 3"), 99)


if __name__ == '__main__':
    unittest.main()

