from words import get_data
from wordle_solver_v2 import WordleSolver

N_LETTERS = 5

Wordle = WordleSolver(get_data(n_letters=N_LETTERS))
Wordle.word = "UPPER"
Wordle.play_console(inputs="self", verbose=True)