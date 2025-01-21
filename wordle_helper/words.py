probs = [
    0.078, 0.02, 0.04, 0.038, 0.11, 0.014, 0.03, 0.023, 0.086, 0.0021,
    0.0097, 0.053, 0.027, 0.072, 0.061, 0.028, 0.0019, 0.073, 0.087,
    0.067, 0.033, 0.01, 0.0091, 0.0027, 0.016, 0.0044
]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

import numpy as np
import copy

def sum_letters(letter, word):
    res = 0
    for l in word:
        if l == letter:
            res += 1
    return res

def get_data(n_letters=5, probability=True):
    """
    n_letters: number of letters you want in each word
    probability: return a matched-length list of the probability for each word

    returns a list of two lists [words, probability]
    """
    words_raw = open("wordle_helper/words.txt").readlines()
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
    if not probability:
        return words
    likelihoods = []
    for i in range(len(words)):
        likelihood = 1
        for k in words[i]:
            likelihood = likelihood*probs[alphabet.index(k)]
            likelihood = likelihood*sum_letters(words[i][k], words[i])
        likelihoods.append(likelihood)
    old_likelihoods = copy.deepcopy(likelihoods)
    likelihoods.sort(reverse=True)
    new_words = []
    for i in range(len(words)):
        try:
            if likelihoods[i] != likelihoods[i+1]:
                new_words.append(words[old_likelihoods.index(likelihoods[i])])
        except:
            new_words.append(words[old_likelihoods.index(likelihoods[i])])
    words = new_words
    likelihoods = np.array(likelihoods)/np.sum(likelihoods)
    return [words, likelihoods]

if __name__ == "__main__":
    print(get_data())