import string

def splitGermanic(text, strip={"\r"," ", "\n", "\t"}, whitespace=string.whitespace, punctuation=string.punctuation):
    """Tries to split the input text as if it were natural language "germanic" text,
    like english or german.

    whitespace will be used as word separators, characters in strip will be removed
    and punctuation will be treated like single, one character words.

    Returns a generator.
    """
    whitespace = str(whitespace)
    if whitespace == "":
        raise ValueError("whitespace is empty, I have nothing to split on.")
    
    nonWordChars = whitespace + punctuation
    i = 0
    while i < len(text):
        c = text[i]
        if c in whitespace:
            while i < len(text) and text[i] in whitespace:
                i+=1
        elif c not in punctuation:
            word = ""
            while i < len(text) and text[i] not in nonWordChars:
                word += text[i]
                i+=1
            if word != "":
                yield word
        else:
            yield c
            i+=1

            