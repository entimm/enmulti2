import unittest

import common
from enmulti2.stats import Stat, get_stats, stat


def apply(key, selections):
    return next(s for s in get_stats() if s.key == key).apply(selections)


class StatsRegistryTest(unittest.TestCase):
    def test_registered_count(self):
        self.assertEqual(len(get_stats()), 3)

    def test_keys_are_unique(self):
        keys = [s.key for s in get_stats()]
        self.assertEqual(len(keys), len(set(keys)))

    def test_duplicate_key_raises(self):
        def dup(selections):
            return ""

        with self.assertRaises(ValueError):
            stat("Dup", "sum")(dup)

    def test_bad_arity_raises(self):
        def one_arg(selections, extra):
            return ""

        with self.assertRaises(ValueError):
            Stat(name="Bad", key="bad", func=one_arg)


class StatsFunctionalTest(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(apply("sum", ["10", "20.5", "-3"]), "27.5")

    def test_sum_raises_without_numbers(self):
        with self.assertRaises(ValueError):
            apply("sum", ["abc", "def"])

    def test_avg(self):
        self.assertEqual(apply("avg", ["10", "20"]), "15")

    def test_avg_raises_without_numbers(self):
        with self.assertRaises(ValueError):
            apply("avg", ["abc"])

    def test_join(self):
        self.assertEqual(apply("join", ["foo", "bar", "baz"]), "foobarbaz")

    def test_join_empty_selections(self):
        self.assertEqual(apply("join", []), "")


if __name__ == "__main__":
    unittest.main()
