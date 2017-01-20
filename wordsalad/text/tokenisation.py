import string

def splitWestern(text, strip={"\r"," ", "\n", "\t"}, whitespace=string.whitespace, punctuation=string.punctuation):
    """Tries to split the input text as if it were natural language "western" text,
    like english, french or german.

    Whitespace will be used as word separators, characters in strip will be removed
    and punctuation will be treated like single, one character words.

    Returns a generator.
    """
    pass