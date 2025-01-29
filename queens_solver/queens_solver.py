import numpy as np
import matplotlib.pyplot as plt
import copy
from matplotlib.patches import Rectangle

class Solver:
    def __init__(self, grid, colors):
        assert grid.shape[0] == grid.shape[1] == len(colors)
        self.grid = grid # np.array of numbers representing colors
        self.colors = colors
        self.initial_grid = copy.deepcopy(grid)
        self.n = grid.shape[0]
        self.crowns = []
        self.color_indices = self.get_color_indices()
        assert len(self.color_indices) == self.n

    def get_color_indices(self):
        colors = {}
        for y in range(self.n):
            for x in range(self.n):
                if self.grid[y,x] in colors:
                    colors[self.grid[y,x]].append((y,x))
                else:
                    colors[self.grid[y,x]] = [(y,x)]
        return colors
            
    
    def show(self):
        fig = plt.gcf()
        fig.set_size_inches(6/9*self.n, 6/9*self.n)
        ax1 = plt.subplot(111)
        ticklabels = ax1.get_xticklabels()
        ticklabels.extend( ax1.get_yticklabels() )
        for label in ticklabels:
            label.set_fontsize(0)
        for i in range(self.n+1):
            lw = 2
            plt.axvline(i*50, ymin=0, ymax=1, color='black', linewidth=lw)
            plt.axhline(i*50, xmin=0, xmax=1, color='black', linewidth=lw)
        for y in range(self.n):
            for x in range(self.n):
                rect = Rectangle((x*50, y*50), 50, 50, color=self.colors[self.grid[y,x]], alpha=0.8, fill=True)
                ax1.add_patch(rect)
                
                #if self.startgrid[y,x] != self.blank:
                #    rect = Rectangle((x*50, y*50), 50, 50, color='black', alpha=0.25, fill=True)
                #    ax1.add_patch(rect)
                #if self.grid[y,x] != self.blank:
                #    plt.text((x)*50+12.5, (y)*50+39, self.grid[y,x], fontsize=30)
                pass
        plt.xlim(0, 50*self.n)
        plt.ylim(50*self.n, 0)
        plt.show()

    def solve_iteration(self):
        # Check all the grid
        for y in range(self.n):
            for x in range(self.n):
                pass


if __name__ == "__main__":
    grid = np.array([[0,0,1,1,1],
                     [0,1,1,1,1],
                     [0,2,2,1,1],
                     [0,3,3,3,3],
                     [0,3,4,4,3],
                     ])
    colors = ["red","blue","green","orange","purple"]
    Queens = Solver(grid, colors)
    Queens.show()
