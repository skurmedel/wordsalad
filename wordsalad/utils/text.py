import string
import random

def joinGermanic(iterable, capitalize=True, quoteChars="\"", concat="'"):
    """Like "".join(iterable) but with special handling, making it easier to just concatenate a list of words.

    Tries to join an interable as if it was a sequence of words of a generic western germanic language. Inserts a space between each word.

    If capitalize=True any word following a single period character ("."), will be capitalized.

    quoteChars specifies a string of characters that specifies a quote. It tries to be smart about the quotes and keep track of when they start and end.

    The following conditions yield a space before the current "word":

        -   Current is not "." and the previous was ".".
        -   Current is in quoteChars and deemed a start quote.
        -   Current is a word not in quoteChars, and is not ".".
    
    Any word in concat, will never have spaces around it.

    The above rules should ensure that things like [".", ".", "."] yields a "... ", that quotes look reasonably okay ["Hey", "\"", "Friend", "\""] yields "Hey \"Friend\"".

    The function has no concept of semantics, and is thus limited in what it can do.
    
    For example if quoteChars="'", it won't know whether an apostrophe is an apostrophe or a quote.
    """
    pass

def mojibakify(s, bit_rot = True):
	'''Takes an input string, destroys it and returns a byte object.
	'''
	b = s.encode("windows-1252", "ignore")

	def flipper(x):
		if random.randint(0, 25) < 2: 
			n = random.randint(0, 8)
			return x ^ ((3 ** n - 1) % 255)
		return x
	
	if bit_rot:
		b = bytes(map(flipper, b))

	b = b.decode("gbk", "ignore").encode("utf-8", "ignore")

	return b