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
            ),
            (
                # Nested quoting is handled.
                ["\"", "Yo", "man", ",", "you", "'", "chill", "'", "?", "\""],
                "\"Yo man, you 'chill'?\"",
                {"concat": "", "quoteChars": "\"'"}
            ),
            (
                # Nested quoting of the same kind.
                ["\"", "\"", "\"", "Hello", "\"", "\"", "\"","\""],
                "\"\" \"Hello\" \"\" \"",
                {"concat": "", "quoteChars": "\""}
            )
        ]

        for input, expected, kwargs in cases:
            print("Trying {0}".format(expected))
            actual = joinGermanic(input, **kwargs)
            self.assertEqual(expected, actual, "Expected |{0}|".format(expected))