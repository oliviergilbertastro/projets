from words import get_data
from wordle_solver_v2 import WordleSolver

N_LETTERS = 5
LANGUAGE = "english"
#LANGUAGE = "french"
#LANGUAGE = "german"


Wordle = WordleSolver(get_data(n_letters=N_LETTERS, language=LANGUAGE))
Wordle.play_console(if_plot=True, inputs="console")