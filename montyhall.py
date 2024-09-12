import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def monty_hall(chosen_door, nb_of_doors=3, switch_door=True):
    assert chosen_door <= nb_of_doors
    # Initialize the doors and put the prize (1) behind one of them
    doors = np.zeros((nb_of_doors,))
    prize_door = np.random.randint(0,nb_of_doors)
    doors[prize_door] = 1

    # host chooses the door(s) to open
    if prize_door == chosen_door:
        host_openable = []
        for i in range(len(doors)):
            if i != prize_door:
                host_openable.append(i)
    else:
        host_openable = []
        for i in range(len(doors)):
            if i != prize_door and i != chosen_door:
                host_openable.append(i)

    #if len(host_openable) > 1:
    #    host_openable = host_openable[np.random.randint(0,len(host_openable))]
    #else:
    #    host_openable = host_openable[0]
    opened_doors = []
    for i in range(nb_of_doors-2):
        opened_doors.append(host_openable.pop(np.random.randint(0,len(host_openable))))
    unopened_doors = []
    for i in range(nb_of_doors):
        if i not in opened_doors:
            unopened_doors.append(i)

    if switch_door:
        chosen_door = unopened_doors[unopened_doors != chosen_door]

    return doors[chosen_door] == 1


sample_size = 100000
wins = 0
for i in tqdm(range(sample_size)):
    if monty_hall(0, nb_of_doors=40, switch_door=True):
        wins += 1
print(wins/sample_size)

    