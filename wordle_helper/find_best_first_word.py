from words import get_data
from wordle_solver import WordleSolver

N_LETTERS = 5


first_words = get_data(n_letters=N_LETTERS)[0]
avg_tries = []
nb_of_games = 1000


Wordle = WordleSolver(get_data(n_letters=N_LETTERS))

for first_word in first_words:
    total_tries = 0
    for i in range(nb_of_games):
        total_tries += Wordle.play_console(inputs="self", first_word=first_word, verbose=False)
    avg_tries.append(total_tries/nb_of_games)