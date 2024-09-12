import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def monty_hall(chosen_door, nb_of_doors=3):
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

    if len(host_openable) > 1:
        host_openable = host_openable[np.random.randint(0,len(host_openable))]
    else:
        host_openable = host_openable[0]

    print(doors)
    print(host_openable)

monty_hall(0)
    