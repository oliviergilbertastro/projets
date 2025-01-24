import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import copy


# Dimensions: 6x12 cm
# Résolution spatiale: 1mm
# Résolution temporelle: 1s

class Plaque:
    def __init__(self, dim=(0.06,0.12), resolution_spatiale=0.001, resolution_temps=1, temperature_ambiante=25, capacite_thermique=0.897):
        """
        dim: tuple de dimension (largeur, hauteur) en mètres
        resolution_spatiale: résolution spatiale en mètres
        resolution_temps: résolution temporelle en secondes
        temperature_ambiante: température ambiante en degrés Celsius
        capacite_thermique: capacité thermique [J/(g.K)] (0.897 pour l'aluminium)
        """
        self.dim = dim
        self.dx = resolution_spatiale
        self.dt = resolution_temps
        self.temperature_ambiante = temperature_ambiante
        self.capacite_thermique = capacite_thermique
        self.data = np.ones((int(dim[0]/self.dx),int(dim[1]/self.dx)))*temperature_ambiante
        self.points_chauffants = []

    def chauffe_point(self, temp=30, indices=(0,0)):
        """
        temp: température constante du point en degrés Celsius
        indices: indices du point à fixer la température en unités de pixel (changent selon la résolution)
        """
        self.points_chauffants.append((indices, temp))
        for pc in self.points_chauffants:
            self.data[pc[0]] = pc[1]
    
    def show(self):
        ax = plt.subplot(111)
        plt.imshow(self.data, cmap="inferno", origin='lower', extent=[0,self.dim[1],0,self.dim[0]])

        ticklabels = ax.get_xticklabels()
        ticklabels.extend( ax.get_yticklabels() )
        for label in ticklabels:
            label.set_fontsize(10)
        plt.show()

    def iteration(self):
        for pc in self.points_chauffants:
            self.data[pc[0]] = pc[1]
        big_data = np.zeros((self.data.shape[0]+2,self.data.shape[1]+2))
        big_data[1:-1, 1:-1] = copy.copy(self.data) # remplace le centre
        alpha = 1
        # On additionne chaque point touchant le point précédent pour faire une moyenne
        new_grid = big_data[1:-1, 1:-1] + ((alpha * self.dt / self.dx**2) * big_data[1:-1, 2:] - 2 * big_data[1:-1, 1:-1] + big_data[1:-1, 0:-2]) + ((alpha * self.dt / self.dx**2) * 
                        (big_data[2:,1: -1] - 2 * big_data[1:-1, 1:-1] + big_data[0:-2, 1:-1]))
        new_grid[0, :] = self.data[0, :]
        new_grid[-1, :] = self.data[-1, :]
        new_grid[:, 0] = self.data[:, 0]
        new_grid[:, -1] = self.data[:, -1]
        self.data = new_grid # moyenne des points environnants
        for pc in self.points_chauffants:
            self.data[pc[0]] = pc[1]

if __name__ == "__main__":
    plaqueChauffante = Plaque(
                            dim=(0.06,0.12),
                            resolution_spatiale=0.001,
                            resolution_temps=0.000000001,
                            temperature_ambiante=25,
                        )
    plaqueChauffante.chauffe_point(50, (30, 40))
    plaqueChauffante.chauffe_point(56, (50, 20))
    plaqueChauffante.show()
    while True:
        for i in range(1):
            plaqueChauffante.iteration()
        plaqueChauffante.show()