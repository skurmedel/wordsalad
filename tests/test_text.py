from wordsalad.text import splitWestern
import unittest

class TestTokenisation(unittest.TestCase):
    
    def test_splitWestern_punctuation_treated_like_one_word(self):
        txt = "abc. def.,"

        res = list(splitWestern(txt))

        self.assertListEqual(["abc", ".", "def", ".", ","], res)
    
    def test_splitWestern_fails_on_empty_whitespace(self):
        txt = "A high powered mutant"

        with self.assertRaises(ValueError):
            list(splitWestern(txt, whitespace=""))
    
    def test_splitWestern_whitespace_not_a_string(self):
        txt = "ab1c d1ef"

        lst = list(splitWestern(txt, whitespace=1))
        self.assertListEqual(["ab", "c d", "ef"], lst)
    
    def test_splitWestern(self):
        cases = [
            (
                "Swiss cheese is a type of dairy product.[5]", 
                ["Swiss", "cheese", "is", "a", "type", "of", "dairy", "product", ".", "[", "5", "]"]
            ),
            (
                "Who are you... he said.", 
                ["Who", "are", "you", ".", ".", ".", "he", "said", "."]
            ),
            (
                "A list of (approved) items follows:",
                ["A", "list", "of", "(", "approved", ")", "items", "follows", ":"]
            )
        ]

        for s, expected in cases:
            actual = list(splitWestern(s))
            self.assertListEqual(expected, actual)
            