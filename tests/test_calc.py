import unittest

import common
from enmulti2.calc import extract_numbers, format_number


class ExtractNumbersTest(unittest.TestCase):
    def test_single_integer(self):
        self.assertEqual(extract_numbers("10"), [10.0])

    def test_negative_and_decimal(self):
        self.assertEqual(extract_numbers("-3.5"), [-3.5])

    def test_thousands_separator(self):
        self.assertEqual(extract_numbers("1,234"), [1234.0])

    def test_mixed_text(self):
        self.assertEqual(extract_numbers("a 1.5 b 2 c"), [1.5, 2.0])

    def test_no_numbers(self):
        self.assertEqual(extract_numbers("hello world"), [])

    def test_empty(self):
        self.assertEqual(extract_numbers(""), [])


class FormatNumberTest(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(format_number(4.0), "4")

    def test_decimal(self):
        self.assertEqual(format_number(4.5), "4.5")

    def test_negative(self):
        self.assertEqual(format_number(-2.5), "-2.5")


if __name__ == "__main__":
    unittest.main()
