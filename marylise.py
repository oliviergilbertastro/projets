import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fractions import Fraction
import datetime

data = pd.read_csv("Mens(2024).csv")

dates = np.array(data["DATE"])
values = np.array(data["Total"])

dates = dates[1:340]
values = values[1:340]
date_debut = np.array(dates[0].split("-"), dtype=int)

for i in range(len(dates)):
    date = np.array(dates[i].split("-"), dtype=int)
    dates[i] = (datetime.date(date[2], date[1], date[0])-datetime.date(date_debut[2], date_debut[1], date_debut[0]))/ datetime.timedelta(days=1)
    values[i] = float(sum(Fraction(s) for s in values[i].split()))


from scipy.signal import find_peaks
def get_peaks_indices(valeurs: np.array,
                                      hauteur_minimum: int = None,
                                      distance_minimum: int = None):
    peaks, _ = find_peaks(valeurs, height=hauteur_minimum, distance=distance_minimum)
    return peaks

peaks = get_peaks_indices(values, hauteur_minimum=1.3)

ecart_entre_chaque = []
duree_chaque = []
for i in range(len(peaks)-1):
    ecart_entre_chaque.append(dates[peaks][i+1]-dates[peaks][i])


values = values*29.5735 # en mL

print(f"Écart entre chaque journée max = {np.mean(ecart_entre_chaque)} +/- {np.std(ecart_entre_chaque)} jours")
print(f"mL moyen par fois: {np.sum(values)/len(peaks)}")
plt.plot(dates, values)
plt.plot(dates[peaks],values[peaks],"o")
plt.xlabel("Jours", fontsize=16)
plt.ylabel("mL", fontsize=16)
plt.show()