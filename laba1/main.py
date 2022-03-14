def get_text():
    text = input()
    chars_to_replace = "\\&@:;/*+-1234567890/|#$%()=_"
    for i in chars_to_replace:
        text = text.replace(i, " ")

    text = text.replace("Mr.", "Mr ").replace("Miss.", "Miss ").replace("Ms.", "Ms ")

    return text


def get_average_words(text):
    text = text.replace("?", ".").replace("!", ".").split(".")

    average = 0
    for i in text:
        i = i.split()
        average += len(i)
    average /= len(text)

    print(f"Average words in sentence : {int(average)}")


def get_median_words(text):
    text = text.replace("?", ".").replace("!", ".").split(".")

    for i, j in zip(text, range(len(text))):
        i = i.split()
        text[j] = len(i)
    text.sort()
    print(f"Median words in sentence : {text[int(len(text) / 2)]}")


def replace_end_sentence(text):
    chars = "?!."
    for i in chars:
        text = text.replace(i, " ")

    return text


def get_word_repetition(text):
    words = dict()
    text = replace_end_sentence(text)
    text = text.lower().split()
    print(text)

    for i in text:
        if i in words:
            words[i] += 1
        else:
            words[i] = 1

    print(f"Word repetitions : \n {words}")


def str_to_bool(text):
    return text.lower() in ("yes", "true", "1", "y")


def get_ngram(text):
    n = 4
    k = 10
    key = str_to_bool(input("Change n and k?\n"))
    if key:
        n = int(input("Enter n:\n"))
        k = int(input("Enter k:\n"))

    text = replace_end_sentence(text)
    text = text.replace(" ", "")

    ngrams = dict()

    for start, end in zip(range(0, len(text) + n, n), range(n, len(text) + n, n)):
        if text[start:end] in ngrams:
            ngrams[text[start:end]] += 1
        else:
            ngrams[text[start:end]] = 1

    print(f"Ngrams:\n{ngrams}")


if __name__ == '__main__':
    _text = get_text()
    get_average_words(_text)
    get_median_words(_text)
    get_word_repetition(_text)
    get_ngram(_text)
