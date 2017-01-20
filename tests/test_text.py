from wordsalad.text import splitWestern
import unittest

class TestTokenisation(unittest.TestCase):

    def test_splitWestern_strips_after_separation(self):
        txt = "\nabc \nde\nf"

        res = list(splitWestern(txt))

        self.assertListEqual(["abc", "def"], res)
    
    def test_splitWestern_punctuation_treated_like_one_word(self):
        txt = "abc. def.,"

        res = list(splitWestern(txt))

        self.assertListEqual(["abc", ".", "def", ".", ","], res)
    
    def test_splitWestern_fails_on_empty_whitespace(self):
        txt = "A high powered mutant"

        with self.assertRaises(ValueError):
            splitWestern(txt, whitespace="")
    
    def test_splitWestern_whitespace_not_a_string(self):
        txt = "ab1c d1ef"

        lst = list(splitWestern(txt, whitespace=1))
        self.assertListEqual(["ab", "c d", "ef"], lst)