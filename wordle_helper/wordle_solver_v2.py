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

    def __init__(self, data, L_penalty = 10):
        self.untouched_data = copy.deepcopy(data)
        self.n_letters = len(data[0][0])
        self.L_penalty = L_penalty
        self.reset()

    def letter_info(self, letter, position, good=True):
        """
        letter: letter you have information on
        position: index of the letter
        good: True->letter at this place, False->letter not at this place
        Updates list of words fitting the constraint
        """
        word_bank = self.data[0]
        valid_words = []
        valid_likelihoods = []
        for i in range(len(word_bank)):
            if (word_bank[i][position] == letter) == good:
                valid_words.append(word_bank[i])
                valid_likelihoods.append(self.data[1][i])
        self.data = [valid_words, np.array(valid_likelihoods)/np.sum(valid_likelihoods)]


    def best_word(self, verbose=False):
        if verbose:
            print(np.max(self.data[1]))
        return self.data[0][(list(self.data[1]).index(np.max(self.data[1])))]
    
    def prob_of_word(self, word):
        return self.data[1][self.data[0].index(word)]

    def print_word_bank(self):
        print("---------------")
        for i in range(len(self.data[0])):
            print(f"{self.data[0][i]} : {np.around(self.data[1][i]*100, decimals=3)}%")
        print(f"\nTotal of {len(self.data[0])} words.")

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
        word = word.upper()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        count = []
        # Count the number of each letters in the word you tried
        for i in range(len(alphabet)):
            count.append(sum_letters(alphabet[i], word))
        # Count the min/max of each letters in the word
        min_max = []
        for i in range(len(count)):
            if count[i] != 0:
                cmm = [0,len(word)]
                for k in range(len(word)):
                    if word[k] == alphabet[i]:
                        if word_colors[k] == 2 or word_colors[k] == 1:
                            cmm[0] += 1
                            if cmm[1] != len(word):
                                cmm[1] = cmm[0]
                        else:
                            cmm[1] = cmm[0]
                    else:
                        pass
                min_max.append(cmm)
            else:
                min_max.append([0,len(word)])
        # Shorten word list with info on specific positions:
        for k in range(len(word)):
            if word_colors[k] == 2:
                self.letter_info(word[k], k, good=True)
            else:
                self.letter_info(word[k], k, good=False)
        # Shorten word list with info on number of letters:
        word_bank = self.data[0]
        valid_words = []
        valid_likelihoods = []
        for i in range(len(word_bank)):
            valid = True
            for k in range(len(alphabet)):
                sum = sum_letters(alphabet[k], word_bank[i])
                if sum >= min_max[k][0] and sum <= min_max[k][1]:
                    pass
                else:
                    valid = False
            if valid:
                valid_words.append(word_bank[i])
                valid_likelihoods.append(self.data[1][i])
        self.data = [valid_words, np.array(valid_likelihoods)/np.sum(valid_likelihoods)]


    def reset(self):
        self.tries = []
        self.data = copy.copy(self.untouched_data)
        self.word = self.data[0][random.randint(0, len(self.data[0])-1)]

    def play_console(self, inputs="console", first_word=None, verbose=True):
        solved = False
        while not solved:
            if inputs == "console":
                word = input(f"Enter a {self.n_letters}-letter word:\n").upper()
            else:
                if len(self.tries) == 0 and first_word != None:
                    word = first_word
                else:
                    word = self.best_word()
                letter_dict = {}
                word_colors = [0,0,0,0,0]
                for k, letter in enumerate(word):
                    if letter == self.word[k]:
                        if letter in letter_dict:
                            letter_dict[letter] += 1
                        else:
                            letter_dict[letter] = 1
                        word_colors[k] = 2
                for k, letter in enumerate(word):
                    if letter == self.word[k]:
                        pass
                    elif letter in self.word and letter:
                        if letter in letter_dict:
                            letter_dict[letter] += 1
                        else:
                            letter_dict[letter] = 1
                        if sum_letters(letter, self.word) >= letter_dict[letter]:
                            word_colors[k] = 1
                        else:
                            word_colors[k] = 0
                    else:
                        word_colors[k] = 0
                self.try_word(word=word, word_colors=word_colors)
            if word in self.untouched_data[0]:
                self.tries.append(word)
                solved = word == self.word
                if verbose:
                    print("--------")
                    for i in range(len(self.tries)):
                        letter_dict = {}
                        word_colors = [0,0,0,0,0]
                        for k, letter in enumerate(self.tries[i]):
                            if letter == self.word[k]:
                                if letter in letter_dict:
                                    letter_dict[letter] += 1
                                else:
                                    letter_dict[letter] = 1
                                #print_color(letter, color="green", end="")
                                word_colors[k] = 2
                        for k, letter in enumerate(self.tries[i]):
                            if letter == self.word[k]:
                                pass
                            elif letter in self.word and letter:
                                if letter in letter_dict:
                                    letter_dict[letter] += 1
                                else:
                                    letter_dict[letter] = 1
                                if sum_letters(letter, self.word) >= letter_dict[letter]:
                                    #print_color(letter, color="yellow", end="")
                                    word_colors[k] = 1
                                else:
                                    #print(letter, end="")
                                    word_colors[k] = 0
                            else:
                                #print(letter, end="")
                                word_colors[k] = 0
                        for k, letter in enumerate(self.tries[i]):
                            if word_colors[k] == 2:
                                print_color(letter, color="green", end="")
                            elif word_colors[k] == 1:
                                print_color(letter, color="yellow", end="")
                            else:
                                print(letter, end="")
                        print("")
                    for i in range(len(self.tries), 6):
                        print("_"*self.n_letters)
            else:
                print(f"{word} not in word list!\n")
            if len(self.tries) >= 6 and word != self.word:
                if verbose:
                    if inputs == "console":
                        print(f"You lost :(\nThe word was {self.word}")
                    else:
                        print(f"Failed. The word was {self.word}")
                return self.L_penalty
        if verbose:
            if inputs == "console":
                print(f"You won in {len(self.tries)} tries!")
            else:
                print(f"Succeeded in {len(self.tries)} tries!")
        return len(self.tries)



if __name__ == "__main__":
    Wordle = WordleSolver(get_data())
    # Start reducing sample for example word "DRAFT"
    # Let's say we try STAGE
    Wordle.try_word("STAGE", [0,1,2,0,0])
    Wordle.print_word_bank()