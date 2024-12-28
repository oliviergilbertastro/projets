import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils import *


def monty_hall(chosen_door, nb_of_doors=3, switch_door=True):
    assert chosen_door <= nb_of_doors
    # Initialize the doors and put the prize (1) behind one of them
    doors = np.zeros((nb_of_doors,))
    prize_door = np.random.randint(0,nb_of_doors)
    doors[prize_door] = 1

    # door(s) that the host can open
    host_openable = []
    for i in range(len(doors)):
        if i != chosen_door:
            host_openable.append(i)

    #host opens doors
    opened_doors = []
    for i in range(nb_of_doors-2):
        opened_doors.append(host_openable.pop(np.random.randint(0,len(host_openable))))

    # check if host opened the winning door:
    for i in range(len(opened_doors)):
        if doors[opened_doors[i]] == 1:
            return 2

    unopened_doors = []
    for i in range(nb_of_doors):
        if i not in opened_doors:
            unopened_doors.append(i)

    if switch_door:
        chosen_door = unopened_doors[unopened_doors != chosen_door]

    valid = 1 if doors[chosen_door] == 1 else 0
    return valid


sample_size = 100000000
wins = 0
results = []
for i in tqdm(range(sample_size)):
    results.append(monty_hall(0, nb_of_doors=3, switch_door=True))
results = np.array(results)
wins = len(results[results == 1])
non_wins = len(results[results == 0])
erreurs = len(results[results == 2])
print("Pourcentage réussite en changeant:", wins/sample_size)
print("Pourcentage réussite sans changer:", non_wins/sample_size)
print("Pourcentage hôte qui ouvre porte gagnante:", erreurs/sample_size)

# Si on renormalise en gardant seulement les cas où l'hôte n'ouvre pas la porte gagnante:
print("On renormalise en gardant seulement les cas où l'hôte n'ouvre pas la porte gagnante")

new_sample_size = wins+non_wins
print_color(f"Pourcentage réussite en changeant: { wins/new_sample_size}", color="yellow")
print_color(f"Pourcentage réussite sans changer: {non_wins/new_sample_size}", color="yellow")

    