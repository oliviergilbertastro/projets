import numpy as np
from time import sleep
from random import random, gauss
import sympy as sp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import os
plt.rcParams['animation.ffmpeg_path']='C:\\Users\\olivi\\Downloads\\ffmpeg\\ffmpeg-6.1.1-essentials_build\\bin\\ffmpeg.exe'

G = 6.6743E-11

def mass_random(width, height, mean_mass, resolution, sigma):
    number_of_squares = (width*height)/(resolution**2)
    value = gauss(mean_mass, sigma)
    return value if value > 0 else 0

def distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2+(y1-y2)**2)



def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "_" + str(counter) + extension
        counter += 1

    return path

#Pendulum
class Universe():
    def __init__(self, width, height, mean_mass, resolution=1, sigma=1, tres=1, add_mass=False, approximate=False):
        '''
        Create a square 2D universe with almost perfectly isotropic mass (energy) distribution
        '''
        self.width = width
        self.height = height
        self.tres = tres
        self.res = resolution
        self.grid = (int(width/resolution),int(height/resolution))
        self.mean_mass = mean_mass
        x, y = np.meshgrid(np.arange(0,width, resolution), np.arange(0,height, resolution))
        #Initialize a randomly distributed spacetime
        self.spacetime = []
        for i in range(int(width/resolution)*int(height/resolution)):
            self.spacetime.append(mass_random(width,height,mean_mass,resolution,sigma))
        self.spacetime = np.array(self.spacetime).reshape(int(width/resolution),int(height/resolution))
        self.inispacetime = self.spacetime.copy()
        #Initialize velocity grids (x and y) - static at t=0
        self.vx = np.zeros(self.grid)
        self.vy = np.zeros(self.grid)
        self.add_mass = add_mass
        self.approximate = approximate

    

    def show(self):
        ax = plt.subplot(111)
        plt.imshow(self.spacetime, cmap="inferno", origin='lower')

        ticklabels = ax.get_xticklabels()
        ticklabels.extend( ax.get_yticklabels() )
        for label in ticklabels:
            label.set_fontsize(10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.streamplot(
                x=np.arange(0, self.spacetime.shape[0]),
                y=np.arange(0, self.spacetime.shape[1]),
                u=self.vy,
                v=self.vx,
                linewidth=1,
                cmap='jet',
                density=3,
                arrowstyle='->',
                arrowsize=1.5
            )
        plt.show()


    def animate(self, frames, fps=30, save=False):
        frame = []
        vector_field_X = []
        vector_field_Y = []
        frame.append(self.spacetime)
        for i in tqdm(range(frames)):
            self.next_time()
            frame.append(self.spacetime)
        fig = plt.figure()
        ax = plt.axes()
        #im=plt.imshow(frame[0],interpolation='none', aspect='equal', cmap='inferno', vmin=np.min(frame[0]), vmax=np.max(frame[0]), origin='lower')
        im=plt.imshow(frame[0],interpolation='none', aspect='equal', cmap='inferno', origin='lower')
        txt=plt.suptitle(f'{self.gini(frame[0])}')
        
        ax.set_xticks([])
        ax.set_yticks([])

        # animation function.  This is called sequentially
        def update(i):
            im.set_array(frame[i])
            im.autoscale()
            txt.set_text(self.gini(frame[i]))
            return [im, txt]

        anim = FuncAnimation(
                            fig, 
                            update, 
                            frames = frames,
                            interval = 1000/fps, # in ms
                            )
        
        print(f'Animating {int(frames)} frames - ({int(frames*self.tres)} seconds)')
        plt.show()

        if save:
            anim.save(uniquify('animations\\animation.mp4'), fps=fps, extra_args=['-vcodec', 'libx264'])

    def next_time(self):
        next_spacetime = self.spacetime.copy()
        next_vx = self.vx.copy()
        next_vy = self.vy.copy()
        for x1 in range(self.grid[0]):
            for y1 in range(self.grid[1]):
                for x2 in range(self.grid[0]):
                    for y2 in range(self.grid[1]):
                        if distance(x1,y1,x2,y2) > 5 and self.approximate:
                            pass
                        else:
                            #print(f'({x1},{y1}) : ({x2},{y2})')
                            if x1 != x2 or y1 != y2:
                                xx1, xx2, yy1, yy2 = x1*self.res, x2*self.res, y1*self.res, y2*self.res
                                angle = np.arctan2((yy2-yy1),(xx2-xx1))
                                acc = G*self.spacetime[x2,y2]/(distance(xx1,yy1,xx2,yy2)**2)
                                self.vx[x1,y1] += np.cos(angle)*acc*self.tres
                                self.vy[x1,y1] += np.sin(angle)*acc*self.tres
                                #if (x1==0 and y1==0):
                                    #print(f'({x2},{y2}):', acc)
                #VX
                if self.vx[x1,y1] > 0:
                    if x1 != self.grid[0]-1:
                        dm = self.spacetime[x1,y1]*np.abs(self.vx[x1,y1])/self.res
                        next_spacetime[x1+1,y1] += dm
                        next_spacetime[x1,y1] -= dm
                        next_vx[x1+1,y1] += (dm*self.vx[x1,y1]+self.spacetime[x1+1,y1]*self.vx[x1+1,y1])/(dm+self.spacetime[x1+1,y1])
                else:
                    if x1 != 0:
                        dm = self.spacetime[x1,y1]*np.abs(self.vx[x1,y1])/self.res
                        next_spacetime[x1-1,y1] += dm
                        next_spacetime[x1,y1] -= dm
                        next_vx[x1-1,y1] += (dm*self.vx[x1,y1]+self.spacetime[x1-1,y1]*self.vx[x1-1,y1])/(dm+self.spacetime[x1-1,y1])
                #VY
                if self.vy[x1,y1] > 0:
                    if y1 != self.grid[1]-1:
                        dm = self.spacetime[x1,y1]*np.abs(self.vy[x1,y1])/self.res
                        next_spacetime[x1,y1+1] += dm
                        next_spacetime[x1,y1] -= dm
                        next_vy[x1,y1+1] += (dm*self.vy[x1,y1]+self.spacetime[x1,y1+1]*self.vy[x1,y1+1])/(dm+self.spacetime[x1,y1+1])
                else:
                    if y1 != 0:
                        dm = self.spacetime[x1,y1]*np.abs(self.vy[x1,y1])/self.res
                        next_spacetime[x1,y1-1] += dm
                        next_spacetime[x1,y1] -= dm
                        next_vx[x1,y1-1] += (dm*self.vy[x1,y1]+self.spacetime[x1,y1-1]*self.vy[x1,y1-1])/(dm+self.spacetime[x1,y1-1])

                if self.add_mass:
                    if x1 == 0 or y1 == 0 or x1 == self.grid[0]-1 or y1 == self.grid[1]-1:
                        next_spacetime[x1, y1] += self.mean_mass/10
                #Make sure the speed does not accumulate towards the outside of our universe
                if x1 == 0 and self.vx[x1,y1] < 0:
                    self.vx[x1,y1] = 0
                if x1 == self.grid[0]-1 and self.vx[x1,y1] > 0:
                    self.vx[x1,y1] = 0
                if y1 == 0 and self.vy[x1,y1] < 0:
                    self.vy[x1,y1] = 0
                if y1 == self.grid[1] and self.vy[x1,y1] > 0:
                    self.vy[x1,y1] = 0
                    
        self.spacetime = next_spacetime

    def total_mass(self, state=None):
        res = np.sum(state)
        return res
    
    def gini(self, state=None):
        if state is None:
            state = self.spacetime
        ordered_mass = np.sort(state.copy().flatten())
        gini = 0
        M = self.total_mass(state)
        n = len(ordered_mass)
        for i in range(1, n+1):
            gini += (2*i-n-1)*np.abs(ordered_mass[i-1])
        return gini/(np.abs(M/n)*n*(n-1))





universe = Universe(20, 20, 1000, 1, sigma=1000, tres=5000, add_mass=False, approximate=True)
#print(universe.gini())
#universe.spacetime = np.zeros(universe.spacetime.shape)
#universe.spacetime[4, 5] += 10000
#universe.spacetime[8, 8] += 10000
universe.next_time()
universe.show()
universe.animate(300, fps=30, save=True)