from scipy.sparse import csr_matrix, coo_matrix, diags
from scipy.sparse import isspmatrix
import random

class WordSaladMatrixBuilder():
    """Aids in the construction of a WordSaladMatrix. The WordSaladMatrix object
    has some finicky requirements and this object helps construct one in a 
    reasonably efficient manner.
    
    It uses a sparse COO matrix to construct the final sparse matrix which can
    then be used to find word follower probabilities."""
    def __init__(self):
        self.words = dict()
        self.c     = 0
        self.row = []
        self.col = []
        self.data = []
    
    def add_word(self, w):
        if w not in self.words:
            self.words[w] = self.c
            
            #self.row.append(self.c)
            #self.col.append(self.c)
            #self.data.append(0)            
            
            self.c += 1
            return self.c - 1
        else:
            return self.words[w]
    
    def count_follower(self, w, f):
        i = self.add_word(w)
        j = self.add_word(f)
        
        self.row.append(i)
        self.col.append(j)
        self.data.append(1)
    
    def count_followers_in_sequence(self, sequence, endmarker=None):
        """Takes an iterable, and for each two words, calls count_follower.

        If endmarker is not None, the last item will be added with count_follower(last, endmarker).

        For example:

            >>> builder = WordSaladMatrixBuilder()
            >>> builder.count_followers_in_sequence([1, 2, 3], endmarker=None)
        
        Is equivalent to:

            >>> builder = WordSaladMatrixBuilder()
            >>> builder.count_follower(1, 2)
            >>> builder.count_follower(2, 3)
        """
        pass
        
    def build_matrix(self):
        m = coo_matrix((self.data, (self.row, self.col)), shape=(self.c, self.c))
        m.sum_duplicates()
        m = m.tocsr()
        # Get row sums as a row matrix, and convert to float (default is int).        
        sums = m.sum(axis=1).astype("f")
        # Get the reciprocal of each element.
        for i in range(0, sums.shape[0]):
            if sums[i, 0] > 0.0:
               sums[i, 0] = 1.0 / sums[i, 0]
            else:
                sums[i, 0] = 0.0
        # Create a diagonal matrix (scales rows on left-multiply) of sums
        # When we multiply we will normalize each row so it becomes a 
        # weighted sum instead, and in our case a probability vector for a 
        # certain word.
        sums = diags(sums.flat, 0, shape=m.shape)
        return WordSaladMatrix(sums * m, self.words)

class WordSaladMatrix:
    """The WordSaladMatrix is a matrix (and a table) of "words" and their 
    associated "followers", encoding a Markov chain for them.
    
    A word does not have to be an actual english word, it can be anything 
    hashable by Python. This is useful for tracking pairs of words for 
    instance, by inserting tuples instead of single strings. But it can also
    be numbers, letters or anything else that can vaguely be emulated by
    a Markov chain.
    
    A follower is simply another "word" that follows the "word" in question,
    the amount of time a word is followed by another is what is encoded by the 
    matrix.
    
    The underlying matrix is sparse with the motivation that since a structure
    is expected, a great deal of followers will have probability zero.
    """
    def __init__(self, freqmatrix, wordtoindex):
        if not isspmatrix(freqmatrix):
            raise TypeError("freqmatrix must be a scipy sparse matrix, is type {}.".format(type(freqmatrix)))
        self.matrix = freqmatrix
        # Bijection word -> index
        self.wordtoindex = dict(wordtoindex)
        # The inverse of the bijection word -> index
        self.indextoword = {i:w for w,i in self.wordtoindex.items()}
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("Needs a square matrix.")
        if len(self.wordtoindex) != self.matrix.shape[0]:
            raise ValueError("length of wordtoindex does not match dimension of matrix.")
    
    def __contains__(self, w):
        return w in self.wordtoindex
    
    def indexOf(self, w):
        return self.wordtoindex[w]
    
    def wordAt(self, i):
        return self.indextoword[i]
    
    def wordCount(self):
        return len(self.wordtoindex)

    def probability(self, w, f):
        """Returns the probability that a word w is followed by word f."""
        if w not in self.wordtoindex or f not in self.wordtoindex:
            raise ValueError("w or f is not in the matrix.")
        
        i = self.wordtoindex[w]
        j = self.wordtoindex[f]
        return self.matrix[i, j]
    
    def probabilities(self, w):
        """Returns the probability vector for a word. This contains as many 
        elements as there are words encoded in the matrix.
        
        Each index has a bijective relation to a word."""
        if w not in self.wordtoindex:
            raise ValueError("w is not in the matrix.")
        return self.matrix.getrow(self.wordtoindex[w])
    
    def power(self, n):
        """Raises the probability matrix by integer n.
        
        This can be used to find out what the probabilities are after n words.
        
        This is usually pretty CPU-intensive, depending on the size of the 
        matrix.
        """
        n = int(n)
        self.matrix **= n
  
    def __repr__(self):
        return "<WordSaladMatrix with matrix shape {}>".format(self.matrix.shape)

