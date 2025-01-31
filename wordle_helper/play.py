from words import get_data
from wordle_solver_v2 import WordleSolver

N_LETTERS = 5
LANGUAGE = "english"
#LANGUAGE = "french"
#LANGUAGE = "german"

dic = get_data(n_letters=N_LETTERS, language=LANGUAGE)
print(len(dic[0]))
Wordle = WordleSolver(dic)
good_word = Wordle.word
Wordle.play_console(if_plot=True, inputs="console")


Wordle.reset()
Wordle.word = good_word
Wordle.play_console(if_plot=True, inputs="self")