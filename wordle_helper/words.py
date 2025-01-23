probs = {
    "english": [0.078, 0.02, 0.04, 0.038, 0.11, 0.014, 0.03, 0.023, 0.086, 0.0021,
    0.0097, 0.053, 0.027, 0.072, 0.061, 0.028, 0.0019, 0.073, 0.087,
    0.067, 0.033, 0.01, 0.0091, 0.0027, 0.016, 0.0044],
    "french": [0.07636, 0.00901, 0.0326, 0.03669, 0.14715, 0.01066, 0.00866, 0.00737, 0.07529, 0.00613,
     0.00074, 0.05456, 0.02968, 0.07095, 0.05796, 0.02521, 0.01362, 0.06693, 0.07948, 0.07244,
     0.06311, 0.01838, 0.00049, 0.00427, 0.00128, 0.00326],
    "german": [0.06516, 0.01886, 0.03062, 0.05076, 0.17396, 0.01656, 0.03009, 0.04577, 0.07550, 0.00268,
               0.01217, 0.03437, 0.02534, 0.09776, 0.02514, 0.00790, 0.00018, 0.07003, 0.0727, 0.06154,
               0.04346, 0.00846, 0.01891, 0.00034, 0.00039, 0.01134]
}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

import numpy as np
import copy

def sum_letters(letter, word):
    res = 0
    for l in word:
        if l == letter:
            res += 1
    return res

def get_data(n_letters=5, probability=True, language="english"):
    """
    n_letters: number of letters you want in each word
    probability: return a matched-length list of the probability for each word

    returns a list of two lists [words, probability]
    """
    words_raw = open(f"wordle_helper/{language}.txt").readlines()
    words = []
    for i in range(len(words_raw)):
        curr_word = ""
        valid_word = True
        good_word = True
        while valid_word:
            #print(words_raw[i])
            try:
                if words_raw[i][len(curr_word)].islower() or (words_raw[i][len(curr_word)].isupper() and language == "german"):
                    if (language == "german"):
                        if (words_raw[i][len(curr_word)].upper() not in alphabet):
                            good_word = False
                            #print(words_raw[i][len(curr_word)])
                    curr_word += words_raw[i][len(curr_word)]
                else:
                    valid_word = False
            except:
                print(words_raw[i])
                print(len(curr_word))
        if len(curr_word) == n_letters and good_word:
            words.append(curr_word.upper())
    if not probability:
        return words
    likelihoods = []
    for i in range(len(words)):
        likelihood = 1
        for k in words[i]:
            likelihood = likelihood*probs[language][alphabet.index(k)]
            likelihood = likelihood/sum_letters(k, words[i])
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