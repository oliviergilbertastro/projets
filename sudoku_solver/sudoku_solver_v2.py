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
        self.possibilities_grid = np.empty((9,9), dtype=list)
        self.startgrid = self.grid.copy()
        self.blank = blank
        if self.grid.shape != (9,9):
            raise ValueError("Grid is not 9x9")
        if not self.check_validity():
            raise ValueError("Grid is not valid")

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
                    rect = Rectangle((x*50, y*50), 50, 50, color='black', alpha=0.25, fill=True)
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
    
    def check_validity(self):
        valid = True
        for y in range(9):
            for x in range(9):
                if (
                        len(self.get_hline((y,x))) != len(set(self.get_hline((y,x)))) or
                        len(self.get_vline((y,x))) != len(set(self.get_vline((y,x)))) or
                        len(self.get_box((y,x))) != len(set(self.get_box((y,x))))
                    ):
                    valid = False
        return valid

    def solve_iteration(self, method=0):
        allpossibilities = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

        #First method: if there is only one possibility for the square, place the number
        for y in range(9):
            for x in range(9):
                if self.grid[y,x] == self.blank:
                    interdictions = sorted(set(self.get_hline((y,x))+self.get_vline((y,x))+self.get_box((y,x))))
                    possibilities = list(allpossibilities-set(interdictions))
                    self.possibilities_grid[y,x] = possibilities
                    if len(possibilities) == 1:
                        self.grid[y,x] = possibilities[0]
        #Second method: if no other square in a line/box can hold a number, place it in the one that can
        if method > 0:
            for y in range(9):
                for x in range(9):
                    if self.grid[y,x] == self.blank:
                        #Horizontal line
                        poss_list = []
                        for i in self.possibilities_grid[y,:]:
                            if i is not None:
                                poss_list.extend(i)
                        for i in self.possibilities_grid[y,x]:
                            poss_list.remove(i)
                        poss_list = set(poss_list)
                        for i in self.possibilities_grid[y,x]:
                            if i not in poss_list:
                                self.grid[y,x] = i
                        #Vertical line
                        poss_list = []
                        for i in self.possibilities_grid[:,x]:
                            if i is not None:
                                poss_list.extend(i)
                        for i in self.possibilities_grid[y,x]:
                            poss_list.remove(i)
                        poss_list = set(poss_list)
                        for i in self.possibilities_grid[y,x]:
                            if i not in poss_list:
                                self.grid[y,x] = i
                        #Box
                        poss_list = []
                        for i in self.possibilities_grid[((y)//3)*3:((y)//3+1)*3,((x)//3)*3:((x)//3+1)*3]:
                            if i is not None:
                                poss_list.extend(i)
                        #Why do I need to create another list? I don't know
                        new_poss_list = []
                        for i in poss_list:
                            if i is not None:
                                new_poss_list.extend(i)
                        for i in self.possibilities_grid[y,x]:
                            new_poss_list.remove(i)
                        poss_list = set(new_poss_list)
                        for i in self.possibilities_grid[y,x]:
                            if i not in poss_list:
                                self.grid[y,x] = i
        if method > 1:
            mini = 2
            for y in range(9):
                for x in range(9):
                    if self.grid[y,x] != self.blank:
                        interdictions = sorted(set(self.get_hline((y,x))+self.get_vline((y,x))+self.get_box((y,x))))
                        possibilities = list(allpossibilities-set(interdictions))

                        if len(possibilities) == mini:
                            self.grid[y,x] = possibilities[int(np.random.random()*mini)]
                            mini = 1
            if not self.check_validity():
                self.grid = self.startgrid.copy()
                self.method = 0
                                

        

    def solve_puzzle(self):
        """
        Solves the puzzle using different methods depending on the difficulty of the puzzle
        As the puzzle gets harder to solve, the 'method' int gets bigger, which changes the way
        this function tries to solve the puzzle
        """
        unsolved = True
        iter = 0
        self.method = 0

        #Check if the puzzle is already solved before trying to solve:
        if self.blank not in list(self.grid.flatten()) and self.check_validity():
            print('Puzzle already solved')
            return iter

        #Start solving
        while unsolved:
            #Save a copy of the current grid to check if it changed later
            thisgrid = self.grid.copy()
            iter += 1
            print(iter, f'{int((1-list(thisgrid.flatten()).count(self.blank)/81)*100)}% solved')

            self.solve_iteration(method=self.method)
            if np.array_equal(self.grid, thisgrid):
                #This runs only if the current method didn't change anything to the grid,
                #so we go to the next method
                self.method += 1

            if self.blank not in list(self.grid.flatten()) and self.check_validity():
                    unsolved = False
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