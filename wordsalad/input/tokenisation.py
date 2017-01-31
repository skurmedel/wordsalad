import string

def split_germanic(text, strip={"\r"," ", "\n", "\t"}, whitespace=string.whitespace, punctuation=string.punctuation, start_words=[], sentence_end=".?!"):
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
    prevWasSentenceEnd = True
    while i < len(text):
        c = text[i]
        if c in whitespace:
            while i < len(text) and text[i] in whitespace:
                i+=1
        elif c not in punctuation and c not in sentence_end:
            word = ""
            while i < len(text) and text[i] not in nonWordChars:
                word += text[i]
                i+=1
            if word != "":
                yield word
                if prevWasSentenceEnd:
                    start_words.append(word)
                prevWasSentenceEnd = False
        else:
            yield c
            prevWasSentenceEnd = True
            i+=1

def group_words(words, size=2, empty=""):
    """Generates pairs (tuples) of consequtive words.

    Returns a generator object for a sequence of tuples.

    If the length of the input is not divisible by three, the last tuple will 
    have the last len(words) % size spots filled with the value of empty.
    """
    pass