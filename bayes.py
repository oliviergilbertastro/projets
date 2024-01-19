import numpy as np
import matplotlib.pyplot as plt
from random import random
from tqdm import tqdm


def bayes(P_EH, P_H, P_E):
    P_HE = (P_EH*P_H)/P_E
    return P_HE

class Population():
    def __init__(self, size, infected_percentage):
        self.size = size
        self.infected_percentage = infected_percentage
        self.pop = []
        self.number_of_infected = 0
        for i in range(size):
            self.pop.append(False if random()>self.infected_percentage else True)
            self.number_of_infected += 1 if self.pop[i] else 0
        
    def test(self, individual, fiability=0.99):
        real = self.pop[individual]
        if real:
            res = True if random()<fiability else False
        else:
            res = False if random()<fiability else True
        return res


population = Population(10000000, 0.001)


print('----------DOING FIRST TESTS----------')
tests1 = []
positive_with_positive_tests1 = []
positive_tests1 = []
for i in tqdm(range(population.size)):
    tests1.append(population.test(i, fiability=0.99))
    if population.pop[i] == tests1[i] and population.pop[i]:
        positive_with_positive_tests1.append(i)
    if tests1[i]:
        positive_tests1.append(i)

print('----------DOING SECOND TESTS----------')
tests2 = []
positive_with_positive_tests1_and_2 = []
positive_tests1_and_2 = []
for i in tqdm(range(population.size)):
    tests2.append(population.test(i, fiability=0.99))
    if population.pop[i] == tests1[i] and population.pop[i] == tests2[i] and population.pop[i]:
        positive_with_positive_tests1_and_2.append(i)
    if tests1[i] and tests2[i]:
        positive_tests1_and_2.append(i)


print(len(positive_with_positive_tests1)/len(positive_tests1))
print(len(positive_with_positive_tests1_and_2)/len(positive_tests1_and_2))