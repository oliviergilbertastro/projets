import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from words import get_data
import copy
import random


def sum_letters(letter, word):
    res = 0
    for l in word:
        if l == letter:
            res += 1
    return res

def print_color(message, color="yellow", **kwargs):
    """print(), but with a color option"""
    possible_colors = ["black","red","green","yellow","blue","magenta","cyan","white"]
    if color == None or color == "grey":
        color = "0"
    elif type(color) == str:
        color = color.lower()
        if color in possible_colors:
            color = str(possible_colors.index(color)+30)
        else:
            print(f"Color '{color}' not implemented, defaulting to grey.\nPossible colors are: {['grey']+possible_colors}")
            color = "0"
    else:
        raise ValueError(f"Parameter 'header_color' needs to be a string.")
    print(f"\x1b[{color}m{message}\x1b[0m", **kwargs)

class WordleSolver():

    def __init__(self, data):
        self.untouched_data = copy.deepcopy(data)
        self.n_letters = len(data[0][0])
        self.reset()

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
            if word_bank[i][position] == letter:
                letter_in_word = False
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
    
    def try_word(self, word, word_colors):
        """
        word: "APPLE"
        word colors: [2,1,0,0,1] means the A was green, one P and the E were yellow and the rest was gray

        0: gray
        1: yellow
        2: green
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        count = []
        for i in range(len(alphabet)):
            count.append(sum_letters(alphabet[i], word.upper()))

        print(count)


    def reset(self):
        self.tries = []
        self.data = copy.copy(self.untouched_data)
        self.word = self.data[0][random.randint(0, len(self.data[0])-1)]

    def play_console(self, inputs="console", first_word="CRANE", verbose=True):
        solved = False
        while not solved:
            if inputs == "console":
                word = input(f"Enter a {self.n_letters}-letter word:\n").upper()
            else:
                if len(self.tries) == 0:
                    word = first_word
                else:
                    word = self.best_word()
                self.try_word(word=word)
            self.tries.append(word)
            solved = word == self.word
            if verbose:
                print("--------")
                for i in range(len(self.tries)):
                    for k, letter in enumerate(self.tries[i]):
                        if letter == self.word[k]:
                            print_color(letter, color="green", end="")
                        elif letter in self.word:
                            print_color(letter, color="yellow", end="")
                        else:
                            print(letter, end="")
                    print("")
                for i in range(len(self.tries), 6):
                    print("_"*self.n_letters)
            if len(self.tries) >= 6 and word != self.word:
                if verbose:
                    print(f"You lost :(\nThe word was {self.word}")
                return 10
        if verbose:
            print(f"You won in {len(self.tries)} tries!")
        return len(self.tries)



if __name__ == "__main__":
    Wordle = WordleSolver(get_data())
    Wordle.try_word("apple")