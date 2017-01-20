from .matrix import WordSaladMatrix
import random

def draw_follower(mat, word, rng=random.uniform):
    """Draw a follower for a given word, using the given RNG function. rng 
    should have the same interface as random.uniform. 
    
    A follower is simply another word in the matrix that has a probability of 
    following our given word.
    
    By default rng is random.uniform and thus the distribution is uniform, all 
    words have equal chance of getting picked.
    """
    probs = mat.probabilities(word).tocoo() # Use a COO, lets us iterate better.
    p = rng(0.01, 1.0)
    f = -1
    for i,p1 in zip(probs.col, probs.data):
        if p1 != 0.0:
            p -= p1
            if p <= 0.0:
                f = i
                break
    if f == -1:
        return None
    return mat.wordAt(i)

def chain(mat, start, rng=random.uniform):
    """Evaluates the Markov Chain for the start word. 
    
    The chain will continue until we reach a word which has no follower (no word has a probility of following it.)
    
    This means that the chain can be infinite, as an example:

        With a matrix for ("hey" 1.0 -> "man") ("man" 1.0 -> "hey") chain(matrix, "hey") will generate an endless sequence of:
            
            "hey", "man", "hey", "man", ... 
    """
    w = start
    while w != None:
        yield w
        w = draw_follower(mat, w, rng=rng)