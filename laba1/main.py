import functions

if __name__ == '__main__':
    _text = functions.get_text()

    average = functions.get_average_words(_text)
    print(f"Average words in sentence : {average}")

    median = functions.get_median_words(_text)
    print(f"Median words in sentence : {median}")

    words = functions.get_word_repetition(_text)
    print(f"Word repetitions : \n {words}")

    ngrams = functions.get_ngram(_text)
    print(f"Ngrams:\n{ngrams}")
