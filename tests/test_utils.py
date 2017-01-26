from wordsalad.utils import joinGermanic
import unittest

class TestJoinGermanic(unittest.TestCase):

    def test_joinGermanic(self):
        cases = [
            (
                ["abc", "'", "abc", "'"],
                "abc ' abc '",
                {"quoteChars": ""}
            ),
            (
                [1, 2, 3, "\"", "hey", "\""],
                "1 2 3 \"hey\"",
                {"quoteChars": "\""}
            ),
            (
                ["abracadabra", ".", ".", ".", "abracadabra"],
                "abracadabra... Abracadabra",
                {"capitalize": True}
            ),
            (
                ["Whose", "burger", "is", "that", "?", "john", "'", "s", "."],
                "Whose burger is that? john's.",
                {"capitalize": True, "concat":"'"}
            )
        ]

        for input, expected, kwargs in cases:
            actual = joinGermanic(input, **kwargs)
            self.assertEqual(expected, actual)