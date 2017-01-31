from wordsalad.input import split_germanic, group_words
import unittest

class TestTokenisation(unittest.TestCase):
    
    def test_split_germanic_punctuation_treated_like_one_word(self):
        txt = "abc. def.,"

        res = list(split_germanic(txt))

        self.assertListEqual(["abc", ".", "def", ".", ","], res)
    
    def test_split_germanic_fails_on_empty_whitespace(self):
        txt = "A high powered mutant"

        with self.assertRaises(ValueError):
            list(split_germanic(txt, whitespace=""))
    
    def test_split_germanic_whitespace_not_a_string(self):
        txt = "ab1c d1ef"

        lst = list(split_germanic(txt, whitespace=1))
        self.assertListEqual(["ab", "c d", "ef"], lst)

    def test_split_germanic_start_words(self):
        s = "Hello my name is Gary Goat. How very nice to meet you! :) What is your name?"        
        start_words = []
        list(split_germanic(s, start_words=start_words, punctuation=".!", sentence_end=".?!"))

        self.assertEqual(["Hello", "How", ":)"], start_words)
    
    def test_split_germanic(self):
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
            actual = list(split_germanic(s))
            self.assertListEqual(expected, actual)
            
class TestGroupWords(unittest.TestCase):
    
    def test_group_words_words_must_be_iterable(self):
        with self.assertRaises(TypeError):
            group_words(1)
    
    def test_group_words_size_must_be_int(self):
        with self.assertRaises(ValueError):
            group_words([1,2], size="abc")
    
    def test_group_words_fills_with_empty(self):
        words = [1,2,3,4,5,6,7]
        res = group_words(words, size=3, empty="E")
        self.assertIsNotNone(res)

        self.assertEqual(
            res,
            [
                (1,2,3),
                (4,5,6),
                (7,"E", "E")
        ])