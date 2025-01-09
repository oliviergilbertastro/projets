"""
Prints possible words based on the user's guesses
"""

from words import get_data
from wordle_solver import WordleSolver

N_LETTERS = 5

Wordle = WordleSolver(get_data(n_letters=N_LETTERS))

solved = False
tries = 0
print("Try a word in WORDLE and answer the following questions:")
while not solved:
    tries += 1
    if tries > 1:
        print(f"Try another word! You could try the word {Wordle.best_word()}.\n")
    nb_of_letters = 0
    bad_letters = input("Which letters in the word you tried are in GREY?\n").upper()
    Wordle.bad_letter(bad_letters)
    nb_of_letters += len(bad_letters)
    if nb_of_letters < 5:
        unplaced_letters = input("Which letters in the word you tried are in \x1b[33mYELLOW\x1b[0m?\n").upper()
        for i in range(len(unplaced_letters)):
            pos = int(input(f"Where in the word was the letter {unplaced_letters[i]}? [1 to {N_LETTERS}]\n"))-1
            Wordle.unplaced_letter(unplaced_letters[i], pos)
        nb_of_letters += len(unplaced_letters)
        if nb_of_letters < 5:
            placed_letters = input("Which letters in the word you tried are in \x1b[32mGREEN\x1b[0m?\n").upper()
            for i in range(len(placed_letters)):
                pos = int(input(f"Where in the word was the letter {placed_letters[i]}? [1 to {N_LETTERS}]\n"))-1
                Wordle.placed_letter(placed_letters[i], pos)
            nb_of_letters += len(placed_letters)
    solved = Wordle.solved()

print(f"Your word is \x1b[32m{Wordle.best_word()}\x1b[0m.")

