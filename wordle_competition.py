import matplotlib.pyplot as plt
import numpy as np



victoires = [
    "e",
    "m",
    "m",
    "o",
    "o",
    "o",
    "o",
    "o",
    "o",
    "o",
    "o",
    "e",
    "o",
    "e",
    "o",
    "o",
    "o",
    "o",
    "o",
    "e",
    "e",
    "e",
    "m",
    "m",
    "m",
    "e",
    "m",
    "o",
    "m",
    "e",
    "e",
    "m",

]


marylise_victoires = []
olivier_victoires = []

tot_o = 0
tot_m = 0

parties_jouees =  range(len(victoires))

for i in parties_jouees:
    if victoires[i] == "m":
        tot_m += 1
    elif victoires[i] == "o":
        tot_o += 1
    marylise_victoires.append(tot_m)
    olivier_victoires.append(tot_o)


plt.plot(parties_jouees, marylise_victoires, "o-", label="Tannante")
plt.plot(parties_jouees, olivier_victoires, "o-", label="Tannant")
plt.legend(fontsize="14")
plt.xlabel("Nombre de parties de faites", fontsize=15)
plt.ylabel("Nombre de victoires", fontsize=15)
plt.title("Compétition féroce de Wordle", fontsize=15)
plt.show()