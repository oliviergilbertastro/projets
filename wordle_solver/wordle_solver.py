import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from words import get_words




def placed_letter(letter, position, dictionnary):
    """
    letter: letter you have information on
    position: index of the letter
    dictionnary: list of words currently possible
    Returns updated list of words fitting the constraint
    """
    valid_words = []
    for i in range(len(dictionnary)):
        if dictionnary[i][position] == letter:
            valid_words.append(dictionnary[i])
    return valid_words

def unplaced_letter(letter, position, dictionnary):
    """
    letter: letter you have information on
    dictionnary: list of words currently possible
    Returns updated list of words fitting the constraint
    """
    valid_words = []
    for i in range(len(dictionnary)):
        letter_in_word = False
        for k in range(len(dictionnary[i])):
            if dictionnary[i][k] == letter and k != position:
                letter_in_word = True
        if letter_in_word:
            valid_words.append(dictionnary[i])
    return valid_words

def bad_letter(letter, dictionnary):
    """
    letter: letter you have information on
    dictionnary: list of words currently possible
    Returns updated list of words fitting the constraint
    """
    try:
        if len(letter)>1:
            for i in range(len(letter)-1):
                dictionnary = bad_letter(letter[-1], dictionnary)
                letter = letter[:-1]
    except:
        pass
    valid_words = []
    for i in range(len(dictionnary)):
        letter_in_word = False
        for k in range(len(dictionnary[i])):
            if dictionnary[i][k] == letter:
                letter_in_word = True
        if letter_in_word == False:
            valid_words.append(dictionnary[i])
    return valid_words


if __name__ == "__main__":
    words, probs = get_words()

    # Start reducing sample for example word "DRAFT"
    # Let's say we try STAGE
    print(len(words))
    words = placed_letter("A", 2, words)
    print(len(words))
    words = unplaced_letter("T", 1, words)
    print(len(words))
    words = bad_letter("SGE", words)
    print(len(words))
    # Let's try TRACK
    words = unplaced_letter("T", 0, words)
    print(len(words))
    words = placed_letter("R", 1, words)
    print(len(words))
    words = bad_letter("CK", words)
    print(len(words))
    print(words)