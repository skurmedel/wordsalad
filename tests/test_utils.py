from wordsalad.utils import joinGermanic
import unittest

class TestJoinGermanic(unittest.TestCase):

    def test_joinGermanic(self):
        cases = [
            (
                # No concat or quoting unless told to.
                ["abc", "'", "abc", "'"],
                "abc ' abc '",
                {"quoteChars": "", "concat": ""}
            ),
            (
                # Test quotes and non-strings.
                [1, 2, 3, "\"", "hey", "\""],
                "1 2 3 \"hey\"",
                {"quoteChars": "\""}
            ),
            (
                # Make sure ellipsis are handled decently.
                ["abracadabra", ".", ".", ".", "abracadabra"],
                "abracadabra... Abracadabra",
                {"capitalize": True}
            ),
            (
                # Todo: We want capitalization to work after "?" too.
                ["Whose", "burger", "is", "that", "?", "john", "'", "s", "."],
                "Whose burger is that? john's.",
                {"capitalize": True, "concat":"'"}
            )
        ]

        for input, expected, kwargs in cases:
            actual = joinGermanic(input, **kwargs)
            self.assertEqual(expected, actual)