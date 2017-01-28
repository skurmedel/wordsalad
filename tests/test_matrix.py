from wordsalad import WordSaladMatrixBuilder
import unittest

class TestWordSaladMatrixBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = WordSaladMatrixBuilder()

    def test_count_followers_in_sequence_no_endmarker(self):
        seq = [1, 2, 3]
        self.builder.count_followers_in_sequence(seq)
        mat = self.builder.build_matrix()

        self.assertEqual(mat.probability(1, 2), 1)
        self.assertEqual(mat.probability(2, 3), 1)
        
        for w in mat.probabilities(3):
            self.assertEqual(w, 0)
    
    def test_count_followers_in_sequence_endmarker(self):
        marker = "end"
        seq = [1, 2, 3]
        self.builder.count_followers_in_sequence(seq, endmarker=marker)
        mat = self.builder.build_matrix()

        self.assertEqual(mat.probability(1, 2), 1)
        self.assertEqual(mat.probability(2, 3), 1)
        self.assertEqual(mat.probability(3, "end"), 1)
    
    def test_count_followers_in_sequence_throws_on_type(self):
        with self.assertRaises(TypeError):
            self.builder.count_followers_in_sequence(None)