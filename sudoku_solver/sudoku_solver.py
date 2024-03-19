import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle

def remove_blanks(a, blank='-'):
    x = []
    for i in a:
        if i != blank:
            x.append(i)
    return (x)

class Sudoku():
    def __init__(self, grid, blank='-'):
        self.grid = np.array(grid)
        self.startgrid = self.grid.copy()
        self.blank = blank
        if self.grid.shape != (9,9):
            raise ValueError("Grid is not 9x9")

    def print(self):
        print(self.grid)

    def show(self):
        fig = plt.gcf()
        fig.set_size_inches(6, 6)
        ax1 = plt.subplot(111)
        ticklabels = ax1.get_xticklabels()
        ticklabels.extend( ax1.get_yticklabels() )
        for label in ticklabels:
            label.set_fontsize(0)
        for i in range(10):
            lw = 1
            if i%3 == 0:
                lw = 5
            plt.axvline(i*50, ymin=0, ymax=1, color='black', linewidth=lw)
            plt.axhline(i*50, xmin=0, xmax=1, color='black', linewidth=lw)
        for y in range(9):
            for x in range(9):
                if self.startgrid[y,x] != self.blank:
                    rect = Rectangle((x*50, y*50), 50, 50, color='black', alpha=0.2, fill=True)
                    ax1.add_patch(rect)
                if self.grid[y,x] != self.blank:
                    plt.text((x)*50+12.5, (y)*50+39, self.grid[y,x], fontsize=30)
        plt.xlim(0, 450)
        plt.ylim(450, 0)
        plt.show()

    def get_hline(self, coord):
        y,x = coord
        return  remove_blanks(self.grid[y,:], self.blank)

    def get_vline(self, coord):
        y,x = coord
        return remove_blanks(self.grid[:,x], self.blank)

    def get_box(self, coord):
        y,x = coord
        return remove_blanks(self.grid[((y)//3)*3:((y)//3+1)*3,((x)//3)*3:((x)//3+1)*3].flatten(), self.blank)

    def solve_iteration_guess(self, min=1):
        allpossibilities = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        for y in range(9):
            for x in range(9):
                if self.grid[y,x] == self.blank:
                    interdictions = sorted(set(self.get_hline((y,x))+self.get_vline((y,x))+self.get_box((y,x))))
                    possibilities = list(allpossibilities-set(interdictions))
                    
                    if len(possibilities) == min:
                        self.grid[y,x] = possibilities[int(np.random.random()*min)]
                        min = 1

    def solve_puzzle(self):
        unsolved = True
        iter = 0
        method = 0
        while unsolved:
            thisgrid = self.grid.copy()
            iter += 1
            if int((1-list(thisgrid.flatten()).count(self.blank)/81)) == 1:
                print('Puzzle already solved')
                break
            print(iter, f'{int((1-list(thisgrid.flatten()).count(self.blank)/81)*100)}% solved')
            if method == 0:
                self.solve_iteration_guess(min=1)
                if self.blank not in list(self.grid.flatten()):
                    unsolved = False
                if np.array_equal(self.grid, thisgrid):
                    #This grid cannot be solved using this resolution method.
                    method += 1
            elif method == 1:
                #Guess between 2 possibilities and immediately go back to first method
                self.solve_iteration_guess(min=2)
                if np.array_equal(self.grid, thisgrid):
                    self.grid = self.startgrid.copy()
                method = 0

        return iter

#Example:
if __name__ == '__main__':
    grille = Sudoku(
        [
        ['1', '7', '-', '4', '-', '5', '-', '-', '9'],
        ['-', '-', '-', '-', '2', '-', '4', '-', '-'],
        ['-', '-', '5', '-', '6', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '5', '-', '-', '-', '-'],
        ['-', '-', '7', '3', '-', '1', '6', '-', '-'],
        ['-', '9', '-', '-', '-', '-', '-', '8', '-'],
        ['-', '-', '-', '2', '-', '-', '-', '-', '-'],
        ['3', '-', '-', '-', '-', '-', '-', '-', '6'],
        ['-', '-', '1', '7', '-', '4', '3', '-', '-'],
        ]
        )
    grille.show()
    grille.solve_puzzle()
    grille.show()