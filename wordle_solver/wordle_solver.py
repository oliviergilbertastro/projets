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

def unplaced_letter(letter, dictionnary):
    """
    letter: letter you have information on
    dictionnary: list of words currently possible
    Returns updated list of words fitting the constraint
    """
    valid_words = []
    for i in range(len(dictionnary)):
        letter_in_word = False
        for k in range(len(dictionnary[i])):
            if dictionnary[i][k] == letter:
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
    words = get_words()

    # Start reducing sample
    words = unplaced_letter("S", words)
    words = placed_letter("C", 1, words)
    words = bad_letter("I", words)
    words = bad_letter("W", words)
    words = bad_letter("U", words)
    print(words)