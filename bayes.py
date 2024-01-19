import numpy as np
import matplotlib.pyplot as plt
from random import random
from tqdm import tqdm


def bayes(P_EH, P_H, P_E):
    P_HE = (P_EH*P_H)/P_E
    return P_HE

class Population():
    def __init__(self, size, infected_percentage, fiability=0.99):
        self.size = size
        self.infected_percentage = infected_percentage
        self.pop = []
        self.number_of_infected = 0
        self.fiability = fiability
        for i in range(size):
            self.pop.append(False if random()>self.infected_percentage else True)
            self.number_of_infected += 1 if self.pop[i] else 0
        
    def test(self, individual):
        real = self.pop[individual]
        if real:
            res = True if random()<self.fiability else False
        else:
            res = False if random()<self.fiability else True
        return res








population = Population(100000, 0.001, fiability=0.95)


print('----------DOING FIRST TESTS----------')
tests1 = []
positive_with_positive_tests1 = []
positive_tests1 = []
for i in tqdm(range(population.size)):
    tests1.append(population.test(i))
    if population.pop[i] == tests1[i] and population.pop[i]:
        positive_with_positive_tests1.append(i)
    if tests1[i]:
        positive_tests1.append(i)

print('----------DOING SECOND TESTS----------')
tests2 = []
positive_with_positive_tests1_and_2 = []
positive_tests1_and_2 = []
for i in tqdm(range(population.size)):
    tests2.append(population.test(i))
    if population.pop[i] == tests1[i] and population.pop[i] == tests2[i] and population.pop[i]:
        positive_with_positive_tests1_and_2.append(i)
    if tests1[i] and tests2[i]:
        positive_tests1_and_2.append(i)


print('----------DOING THIRD TESTS----------')
tests3 = []
positive_with_positive_tests1_to_3 = []
positive_tests1_to_3 = []
for i in tqdm(range(population.size)):
    tests3.append(population.test(i))
    if population.pop[i] == tests1[i] and population.pop[i] == tests2[i]  and population.pop[i] == tests3[i] and population.pop[i]:
        positive_with_positive_tests1_to_3.append(i)
    if tests1[i] and tests2[i] and tests3[i]:
        positive_tests1_to_3.append(i)
print(' ------ ')
print('Experimental:')

print('Test #1: ', len(positive_with_positive_tests1)/len(positive_tests1))
print('Test #2: ', len(positive_with_positive_tests1_and_2)/len(positive_tests1_and_2))
print('Test #3: ', len(positive_with_positive_tests1_to_3)/len(positive_tests1_to_3))

print(' ------ ')
print('Theoretical:')

P_HE = bayes(population.fiability, population.infected_percentage, population.infected_percentage*population.fiability+(1-population.infected_percentage)*(1-population.fiability))
print('Test #1: ', P_HE)
for i in range(2):
    P_HE = bayes(population.fiability, P_HE, P_HE*population.fiability+(1-P_HE)*(1-population.fiability))
    print(f'Test #{i+2}: ', P_HE)


