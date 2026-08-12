import unittest

import common
from enmulti2.registry import Transform, get_transforms, transformation


class RegistryTest(unittest.TestCase):
    def test_discovery_and_count(self):
        transforms = get_transforms()
        self.assertEqual(len(transforms), 9)

    def test_keys_are_unique(self):
        keys = [t.key for t in get_transforms()]
        self.assertEqual(len(keys), len(set(keys)))

    def test_order_matches_registration(self):
        keys = [t.key for t in get_transforms()]
        self.assertEqual(
            keys,
            [
                "time_timestamp",
                "replace_chars",
                "md5",
                "reverse",
                "base64_encode",
                "base64_decode",
                "eval",
                "unicode_to_utf8",
                "utf8_to_unicode",
            ],
        )

    def test_duplicate_key_raises(self):
        def dup(v, ctx):
            return v

        with self.assertRaises(ValueError):
            transformation("Dup", "md5")(dup)

    def test_empty_name_or_key_raises(self):
        def f(v, ctx):
            return v

        with self.assertRaises(ValueError):
            transformation("", "empty_name")(f)
        with self.assertRaises(ValueError):
            transformation("Empty Key", "")(f)

    def test_legacy_signature_adapter(self):
        calls = {}

        def legacy(v, i, secs):
            calls["v"] = v
            calls["i"] = i
            calls["secs"] = secs
            return v.upper()

        transform = Transform(name="Legacy", key="legacy_test", func=legacy)
        result = transform.apply("abc", 1, ["abc", "def"], view=object())
        self.assertEqual(result, "ABC")
        self.assertEqual(calls, {"v": "abc", "i": 1, "secs": ["abc", "def"]})

    def test_new_signature_adapter(self):
        def new_style(v, ctx):
            return f"{v}:{ctx.index}:{ctx.selections[ctx.index]}:{ctx.view is not None}"

        transform = Transform(name="New", key="new_test", func=new_style)
        result = transform.apply("x", 1, ["a", "x"], view=object())
        self.assertEqual(result, "x:1:x:True")

    def test_bad_arity_raises(self):
        def one_arg(v):
            return v

        with self.assertRaises(ValueError):
            Transform(name="Bad", key="bad", func=one_arg)


if __name__ == "__main__":
    unittest.main()
