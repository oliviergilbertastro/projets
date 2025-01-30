import numpy as np
import matplotlib.pyplot as plt
import copy
from matplotlib.patches import Rectangle

def count_in_array(a, b):
    """Return the number of instances of b in array a"""
    res = 0
    for i in a:
        if i==b:
            res+=1
    return res

class Solver:
    def __init__(self, grid, colors):
        assert grid.shape[0] == grid.shape[1] == len(colors)
        self.grid = grid # np.array of numbers representing colors
        self.colors = colors
        self.data = np.zeros_like(self.grid) # 0=no info, 1=x, 2=crown
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
                rect = Rectangle((x*50, y*50), 50, 50, color=self.colors[self.grid[y,x]], alpha=1, fill=True)
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

    def get_cells_with_same_color(self, pos):
        return self.color_indices[self.grid[pos[0],pos[1]]]

    def color_array(self, n_color):
        """Returns the array of [0,1,2] representing the info we have on the grid for a specific color"""
        assert n_color in self.grid
        color_a = []
        for c in self.color_indices[self.colors[n_color]]:
            color_a.append(self.data[c[0],c[1]])
        return color_a


    def check_if_possible(self, pos):
        """pos = [y,x]"""
        # Check hline
        if 2 in self.data[pos[0],:]:
            return False
        # Check vline
        elif 2 in self.data[:,pos[1]]:
            return False
        # Check same color
        for c in self.get_cells_with_same_color(pos):
            if 2 == self.data[c[0],c[1]]:
                return False
        # Check 4-diagonal corners
        for x in [-1,1]:
            for y in [-1,1]:
                try:
                    if self.data[pos[0]+y,pos[1]+x] == 2:
                        return False
                except:
                    pass
        
        return True

    def solve_iteration(self):
        # Check all the grid
        # For each spot (if possible), place a crown, check which cells are now Xs
        # If all cells in a row, column, or color are now blocked, block the former cell.
        for y in range(self.n):
            for x in range(self.n):
                if self.data[y,x] == 0: # Only do this if we haven't already placed something
                    original_data = copy.deepcopy(self.data)
                    self.data[y,x] = 2
                    for n in range(self.n):
                        # If >1 Queen in hline
                        if count_in_array(self.data[n,:],2) > 1:
                            original_data[y,x] = 1
                        # If >1 Queen in vline
                        if count_in_array(self.data[:,n],2) > 1:
                            original_data[y,x] = 1

        # Check if only one square is remaining in each row, column, color.
        # If so, place a crown there.


if __name__ == "__main__":
    grid = np.array([[0,0,1,1,1],
                     [0,1,1,1,1],
                     [0,2,2,1,1],
                     [0,3,3,3,3],
                     [0,3,4,4,3],
                     ])
    colors = ["red","blue","green","orange","purple"]
    Queens = Solver(grid, colors)
    Queens.data[4,0] = 2
    print(Queens.colors)
    print(Queens.color_array(0))
    print(Queens.check_if_possible([3,1]))
    Queens.show()
