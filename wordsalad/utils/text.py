import string
import random

def joinGermanic(iterable, capitalize=True, quoteChars="\"", concat="'"):
    """Like "".join(iterable) but with special handling, making it easier to just concatenate a list of words.

    Tries to join an interable as if it was a sequence of words of a generic western germanic language. Inserts a space between each word.

    If capitalize=True any word following a single period character ("."), will be capitalized.

    quoteChars specifies a string of characters that specifies a quote. It tries to be smart about the quotes and keep track of when they start and end.

    The following conditions yield a space before the current "word":

        -   Current is not "." and the previous was ".".
        -   Previous is not in quoteChars or deemed a start quote.
        -   Current is not in quoteChars and deemed a start quote.
        -   Current is not "!?,:;".
    
    Any word in concat, will never have spaces around it.

    The above rules should ensure that things like [".", ".", "."] yields a "... ", that quotes look reasonably okay ["Hey", "\"", "Friend", "\""] yields "Hey \"Friend\"".

    The function has no concept of semantics, and is thus limited in what it can do.
    
    For example if quoteChars="'", it won't know whether an apostrophe is an apostrophe or a quote.
    """
    def mkcapital(w):
        return w.capitalize()
    
    def nopmkcapital(w):
        return w
        
    capital = mkcapital if capitalize else nopmkcapital

    quoteLevels = {c: 0 for c in quoteChars}
    
    # Check whether c is a quote, and handle it.
    def checkQuote(c):
        if c in quoteChars:
            ql = quoteLevels[c]
            # If we have already seen this quote, decrement, if not we increment.
            # This way we can know how many start quotes we have seen
            if ql > 0:
                ql -= 1
            else:
                ql += 1
            quoteLevels[c] = ql

    s = ""
    last = ""
    for w in iterable:
        w = str(w)
        space = True if last != "" else False
        # Don't add spaces around concat-words.
        if w in concat or last in concat:
            space = False
        # "."" followed by more "."
        elif last.endswith("."):
            w = capital(w)
            if w.startswith("."):
                space = False
        # Remove space after last word in a sentence or certain punctuation.
        elif w in ".!?,;:":
            space = False
        # The last two takes care of end and start quotes.
        elif w in quoteChars:
            ql = quoteLevels[w]
            if ql == 1:
                space = False 
        elif last != "" and last in quoteChars:
            ql = quoteLevels[last]
            if ql == 1:
                space = False
        
        checkQuote(w)
        if space:
            s += " "
        s += w
        last = w
    
    return s

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