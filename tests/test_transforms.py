import string
import time
import unittest
from datetime import datetime

import common
from enmulti2.registry import get_transforms


def by_key(key):
    return next(t for t in get_transforms() if t.key == key)


def apply(key, v, selections=None, index=0):
    return by_key(key).apply(v, index, selections or [v], view=None)


class SimpleTransformsTest(unittest.TestCase):
    def test_md5(self):
        self.assertEqual(apply("md5", "abc"), "900150983cd24fb0d6963f7d28e17f72")

    def test_reverse(self):
        self.assertEqual(apply("reverse", "abc"), "cba")

    def test_base64_roundtrip(self):
        encoded = apply("base64_encode", "hello")
        self.assertEqual(encoded, "aGVsbG8=")
        self.assertEqual(apply("base64_decode", encoded), "hello")

    def test_eval_arithmetic(self):
        self.assertEqual(apply("eval", "2+3*4"), "14")
        self.assertEqual(apply("eval", '"a"*3'), "aaa")
        self.assertEqual(apply("eval", "len('abc')"), "3")

    def test_eval_rejects_unsafe(self):
        for expr in [
            "__import__('os')",
            "__class__",
            "1/0",
            "9**1001",
            "[x for x in range(3)]",
            "globals()",
        ]:
            with self.subTest(expr=expr):
                self.assertTrue(apply("eval", expr).startswith("Error"), expr)

    def test_unicode_roundtrip(self):
        self.assertEqual(apply("utf8_to_unicode", "中文"), "\\u4e2d\\u6587")
        self.assertEqual(apply("unicode_to_utf8", "\\u4e2d\\u6587"), "中文")

    def test_unicode_to_utf8_passthrough(self):
        self.assertEqual(apply("unicode_to_utf8", "no escape here"), "no escape here")


class ComplexTransformsTest(unittest.TestCase):
    def test_time_to_timestamp(self):
        expected = str(int(time.mktime(datetime(2024, 1, 1).timetuple())))
        self.assertEqual(apply("time_timestamp", "2024-01-01 00:00:00"), expected)

    def test_timestamp_to_time(self):
        ts = str(int(time.mktime(datetime(2024, 1, 1).timetuple())))
        self.assertEqual(apply("time_timestamp", ts), "2024-01-01 00:00:00")

    def test_time_empty_returns_now(self):
        result = apply("time_timestamp", "")
        self.assertEqual(len(result), 19)
        datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

    def test_time_invalid(self):
        self.assertEqual(apply("time_timestamp", "not a time"), "")
        self.assertEqual(apply("time_timestamp", "9" * 21), "")

    def test_replace_chars_properties(self):
        sample = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for _ in range(50):
            out = apply("replace_chars", sample)
            self.assertEqual(len(out), len(sample))
            self.assertTrue(out[:26].islower(), out)
            self.assertTrue(out[26:52].isupper(), out)
            self.assertTrue(out[52:].isdigit(), out)
            self.assertEqual(len(set(out[:26])), 26)
            self.assertEqual(len(set(out[26:52])), 26)
            self.assertEqual(len(set(out[52:])), 10)
        self.assertNotEqual(apply("replace_chars", sample)[:26], sample[:26])


if __name__ == "__main__":
    unittest.main()
