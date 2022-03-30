import constants


def get_text():
    text = input()
    text = text.replace("...", ".")

    for i in constants.CHARS_TO_REPLACE:
        text = text.replace(i, " ")

    text = text.replace(constants.MR, "Mr ").replace(constants.MISS, "Miss ").replace(constants.MS, "Ms ")

    return text


def get_average_words(text):
    text = text.replace("?", ".").replace("!", ".").split(".")

    average = 0
    for i in text:
        i = i.split()
        average += len(i)

    average /= len(text)

    return average


def get_median_words(text):
    text = text.replace("?", ".").replace("!", ".").split(".")

    for i, j in zip(text, range(len(text))):
        i = i.split()
        text[j] = len(i)

    text.sort()

    return text[int(len(text) / 2)]


def replace_end_sentence(text):
    chars = "?!."

    for i in chars:
        text = text.replace(i, " ")

    return text


def get_word_repetition(text):
    words = dict()
    text = replace_end_sentence(text)
    text = text.lower().split()

    for i in text:
        if i in words:
            words[i] += 1
        else:
            words[i] = 1

    return words


def str_to_bool(text):
    return text.lower() in ("yes", "true", "1", "y")


def get_ngram(text):
    key = str_to_bool(input("Change n and k?\n"))

    if key:
        constants.N = int(input("Enter n:\n"))
        constants.K = int(input("Enter k:\n"))

    text = replace_end_sentence(text)
    text = text.replace(" ", "")

    ngrams = dict()

    for start, end, i in zip(range(0, len(text) + constants.N),
                             range(constants.N, len(text) + constants.N), range(constants.K)):

        if text[start:end] in ngrams:
            ngrams[text[start:end]] += 1
        else:
            ngrams[text[start:end]] = 1

    return ngrams
