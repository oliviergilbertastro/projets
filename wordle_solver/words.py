def get_words(n_letters=5):
    words_raw = open("wordle_solver/words.txt").readlines()
    words = []
    for i in range(len(words_raw)):
        curr_word = ""
        valid_word = True
        while valid_word:
            if words_raw[i][len(curr_word)].islower():
                curr_word += words_raw[i][len(curr_word)]
            else:
                valid_word = False
        if len(curr_word) == n_letters:
            words.append(curr_word.upper())
    return words

if __name__ == "__main__":
    print(get_words())