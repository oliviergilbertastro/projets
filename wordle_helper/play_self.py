from words import get_data
from wordle_solver_v2 import WordleSolver

N_LETTERS = 5
LANGUAGE = "english"

Wordle = WordleSolver(get_data(n_letters=N_LETTERS, language=LANGUAGE))
#Wordle.print_word_bank()
Wordle.play_console(inputs="self", verbose=True, if_plot=True)