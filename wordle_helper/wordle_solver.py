import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from words import get_data


class WordleSolver():

    def __init__(self, data):
        self.data = data

    def placed_letter(self, letter, position):
        """
        letter: letter you have information on
        position: index of the letter
        dictionnary: list of words currently possible
        Returns updated list of words fitting the constraint
        """
        word_bank = self.data[0]
        valid_words = []
        valid_likelihoods = []
        for i in range(len(word_bank)):
            if word_bank[i][position] == letter:
                valid_words.append(word_bank[i])
                valid_likelihoods.append(self.data[1][i])
        self.data = [valid_words, np.array(valid_likelihoods)/np.sum(valid_likelihoods)]

    def unplaced_letter(self, letter, position):
        """
        letter: letter you have information on
        dictionnary: list of words currently possible
        Returns updated list of words fitting the constraint
        """
        word_bank = self.data[0]
        valid_words = []
        valid_likelihoods = []
        for i in range(len(word_bank)):
            letter_in_word = False
            for k in range(len(word_bank[i])):
                if word_bank[i][k] == letter and k != position:
                    letter_in_word = True
            if letter_in_word:
                valid_words.append(word_bank[i])
                valid_likelihoods.append(self.data[1][i])
        self.data = [valid_words, np.array(valid_likelihoods)/np.sum(valid_likelihoods)]

    def bad_letter(self, letter):
        """
        letter: letter you have information on
        dictionnary: list of words currently possible
        Returns updated list of words fitting the constraint
        """
        try:
            if len(letter)>1:
                for i in range(len(letter)-1):
                    self.bad_letter(letter[-1])
                    letter = letter[:-1]
        except:
            pass
        word_bank = self.data[0]
        valid_words = []
        valid_likelihoods = []
        for i in range(len(word_bank)):
            letter_in_word = False
            for k in range(len(word_bank[i])):
                if word_bank[i][k] == letter:
                    letter_in_word = True
            if letter_in_word == False:
                valid_words.append(word_bank[i])
                valid_likelihoods.append(self.data[1][i])
        self.data = [valid_words, np.array(valid_likelihoods)/np.sum(valid_likelihoods)]

    def best_word(self):
        return self.data[0][(list(self.data[1]).index(np.max(self.data[1])))]
    
    def prob_of_word(self, word):
        return self.data[1][self.data[0].index(word)]

    def print_word_bank(self):
        print("---------------")
        for i in range(len(self.data[0])):
            print(f"{self.data[0][i]} : {np.around(self.data[1][i]*100, decimals=3)}%")

    def solved(self):
        return len(self.data[0]) == 1



if __name__ == "__main__":
    Wordle = WordleSolver(get_data())

    # Start reducing sample for example word "DRAFT"
    # Let's say we try STAGE
    Wordle.placed_letter("A", 2)
    Wordle.unplaced_letter("T", 1)
    Wordle.bad_letter("SGE")
    # Let's try TRACK
    Wordle.unplaced_letter("T", 0)
    Wordle.placed_letter("R", 1)
    Wordle.bad_letter("CK")
    Wordle.print_word_bank()