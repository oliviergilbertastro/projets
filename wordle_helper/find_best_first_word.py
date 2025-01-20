from words import get_data
from wordle_solver import WordleSolver
from tqdm import tqdm
N_LETTERS = 5


first_words = get_data(n_letters=N_LETTERS)[0][:]
avg_tries = []
nb_of_games = 100


Wordle = WordleSolver(get_data(n_letters=N_LETTERS))

for first_word in tqdm(first_words):
    total_tries = 0
    for i in range(nb_of_games):
        total_tries += Wordle.play_console(inputs="self", first_word=first_word, verbose=False)
        Wordle.reset()
    avg_tries.append(total_tries/nb_of_games)

print(first_words)
print(avg_tries)


best_words = []
best_tries = []
for i in range(len(first_words)):
    idx = avg_tries.index(min(avg_tries))
    best_tries.append(avg_tries.pop(idx))
    best_words.append(first_words.pop(idx))

import matplotlib.pyplot as plt

plt.bar(best_words, best_tries)
plt.show()