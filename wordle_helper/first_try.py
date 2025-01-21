from words import get_data
from wordle_solver import WordleSolver
from tqdm import tqdm
import numpy as np
import random
N_LETTERS = 5


first_words = np.array(get_data(n_letters=N_LETTERS)[0])
Wordle = WordleSolver(get_data(n_letters=N_LETTERS))



solved = False
total_tries = 0
while not solved:
    first_word = first_words[np.random.randint(len(first_words))]
    total_tries += 1
    solved = Wordle.play_console(inputs="self", first_word=first_word, verbose=False) == 1
    Wordle.reset()
print(total_tries)