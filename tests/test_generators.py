import unittest

from wordsalad import WordSaladMatrixBuilder
from wordsalad.generators import draw_follower, chain
from itertools import islice


def _get_static_string_mat():
    builder = WordSaladMatrixBuilder()

    builder.count_follower("cat", "has")
    builder.count_follower("has", "a")
    builder.count_follower("a", "tail")

    return builder.build_matrix()

class TestDrawFollower(unittest.TestCase):

    def test_calls_rng(self):
        class my_rng:
            def __init__(self):
                self.called = False
            
            def __call__(self, a, b):
                self.called = True
                return 1
        rng = my_rng()
        draw_follower(_get_static_string_mat(), "cat", rng=rng)
        self.assertTrue(rng.called, "Our custom rng was not called.")
    
    def test_missing_word_raises_error(self):
        with self.assertRaises(ValueError):
            draw_follower(_get_static_string_mat(), "bahamas")
    
    def test_draws_always_when_only_one_choice(self):
        follower = draw_follower(_get_static_string_mat(), "cat")
        self.assertEqual(follower, "has")
    
    def test_draws_roughly_uniformly(self):
        builder = WordSaladMatrixBuilder()

        builder.count_follower("I", "am")
        builder.count_follower("I", "have")

        mat = builder.build_matrix()

        samples = 100
        ams_count = 0
        have_count = 0
        for i in range(0, samples):
            f = draw_follower(mat, "I")
            if f == "am":
                ams_count += 1
            elif f == "have":
                have_count += 1
            else:
                self.fail("Drew another follower.")
        self.assertGreater(float(ams_count)/samples, 0.40)

class TestChain(unittest.TestCase):

    def test_chain_ends_on_zero_probs(self):
        builder = WordSaladMatrixBuilder()
        builder.count_follower("hey", "man")
        builder.count_follower("man", "end")

        mat = builder.build_matrix()

        lst = list(chain(mat, "hey"))
        self.assertListEqual(["hey", "man", "end"], lst)
    
    def test_chain_never_ends_on_loop(self):
        builder = WordSaladMatrixBuilder()
        builder.count_follower("hey", "man")
        builder.count_follower("man", "hey")

        mat = builder.build_matrix()

        n = 111
        lst = list(islice(chain(mat, "hey"), 2 * n))
        self.assertListEqual(["hey", "man"] * n, lst)
    
    def test_chain_missing_word_yields_exception(self):
        builder = WordSaladMatrixBuilder()
        builder.add_word("goat")
        mat = builder.build_matrix()

        with self.assertRaises(ValueError):
            list(chain(mat, "cow"))