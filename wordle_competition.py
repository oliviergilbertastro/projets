import matplotlib.pyplot as plt
import numpy as np


nb_essais_olivier = [
    5,
    4,
    "x",
    4,
    3,
    3,
    3,
    4,
    5,
    4,
    4,
    5,
    3,
    5,
    3,
    3,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    3,
    "x",
    4,
    5,
    3,
    4,
    5,
    4,
    2,
    4, # knead
    4,
    5,
    4,
    5,
    5, # adage
    6,
    5, # thigh
    5, # debut
    3, # crush
    5, # scoff
    3, # canon
    3, # shape
    3, # blare
    5, # gaunt
    5, # cameo
    6, # jiffy
    5, # enact
    5, # video
    4, # swoon
    3, # decoy
    5, # quite
    3, # nerdy
]

nb_essais_marylise = [
    5,
    3,
    5,
    5,
    4,
    4,
    4,
    5,
    6,
    5,
    5,
    5,
    4,
    5,
    4,
    4,
    5,
    5,
    5,
    4,
    5,
    5,
    3,
    3,
    3,
    6,
    5,
    4,
    3,
    4,
    4,
    5,
    3,
    5, # knead
    4,
    3,
    5,
    4,
    4, # adage
    3,
    3, # thigh
    5, # debut
    4, # crush
    4, # scoff
    3, # canon
    4, # shape
    4, # blare
    3, # gaunt
    5, # cameo
    5, # jiffy
    4, # enact
    4, # video
    4, # swoon
    4, # decoy
    3, # quite
    3, # nerdy
]


assert len(nb_essais_olivier) == len(nb_essais_marylise)

nb_parties = len(nb_essais_olivier)

essais_net_olivier = []
essais_net_marylise = []
bar_o = [
    0,  #1
    0,  #2
    0,  #3
    0,  #4
    0,  #5,
    0,  #6,
    0,  #pas réussi
]
bar_m = [
    0,  #1
    0,  #2
    0,  #3
    0,  #4
    0,  #5,
    0,  #6,
    0,  #pas réussi
]
for i in range(nb_parties):
    #Regarde si je l'ai raté (il y a aussi le cas pour Marylise, mais elle rate jamais):
    if nb_essais_olivier[i] == "x":
        essais_net_olivier.append(10)
        bar_o[6] += 1
    else:
        essais_net_olivier.append(nb_essais_olivier[i])
        bar_o[nb_essais_olivier[i]-1] += 1
    if nb_essais_marylise[i] == "x":
        essais_net_marylise.append(10)
        bar_m[6] += 1
    else:
        essais_net_marylise.append(nb_essais_marylise[i])
        bar_m[nb_essais_marylise[i]-1] += 1



victoires = []
for i in range(nb_parties):
    res = "e"
    if essais_net_olivier[i] > essais_net_marylise[i]:
        res = "m"
    elif essais_net_marylise[i] > essais_net_olivier[i]:
        res = "o"
    victoires.append(res)



marylise_victoires = []
olivier_victoires = []

tot_o = 0
tot_m = 0

tot_essais_o = 0
tot_essais_m = 0
tot_essais_o_liste = []
tot_essais_m_liste = []
for i in range(nb_parties):
    tot_essais_o += essais_net_olivier[i]
    tot_essais_o_liste.append(tot_essais_o)
    tot_essais_m += essais_net_marylise[i]
    tot_essais_m_liste.append(tot_essais_m)




print("Moyennes d'essais/partie:")
print(f"Marylise: {tot_essais_m/nb_parties}")
print(f"Olivier: {tot_essais_o/nb_parties}")

parties_jouees =  range(len(victoires))
for i in parties_jouees:
    if victoires[i] == "m":
        tot_m += 1
    elif victoires[i] == "o":
        tot_o += 1
    marylise_victoires.append(tot_m)
    olivier_victoires.append(tot_o)

print("Total victoires:")
print(f"Marylise: {tot_m}")
print(f"Olivier: {tot_o}")



victoires_string = ""
for i in victoires:
    victoires_string += "'"+i+"'" + ","
print(f"var victoires = [{victoires_string}];")
print(f"var tot_essais_M = {tot_essais_m};")
print(f"var tot_essais_O = {tot_essais_o};")

fig = plt.gcf()
ax1 = plt.subplot(121)
ax2 = plt.subplot(122, sharex=ax1)
ax1.plot(parties_jouees, marylise_victoires, "o-", label="Tannante")
ax1.plot(parties_jouees, olivier_victoires, "o-", label="Tannant")
ax1.legend(fontsize=14)
ax1.set_xlabel("Nombre de parties de faites", fontsize=15)
ax1.set_ylabel("Nombre de victoires", fontsize=15)


ax2.plot(parties_jouees, tot_essais_m_liste, "o-", label="Tannante")
ax2.plot(parties_jouees, tot_essais_o_liste, "o-", label="Tannant")
ax2.legend(fontsize="14")
ax2.set_xlabel("Nombre de parties de faites", fontsize=15)
ax2.set_ylabel("Nombre d'essais", fontsize=15)
ax2.legend(fontsize=14)

plt.suptitle("Compétition féroce de Wordle", fontsize=15)
plt.show()


width = 0.35
ax1 = plt.subplot(111)
ax1.bar(["1","2","3","4","5","6","Pas eu"],bar_m, width=-width, align="edge", label="Tannante")
ax1.bar(["1","2","3","4","5","6","Pas eu"], bar_o, width=+width, align="edge", label="Tannant")
ax1.legend(fontsize=14)
ax1.set_xlabel("# d'essais pour réussir", fontsize=15)
ax1.set_ylabel("Nombre de parties", fontsize=15)
plt.show()