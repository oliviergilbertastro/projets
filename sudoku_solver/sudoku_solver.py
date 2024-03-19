import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

    def show(self):
        print(self.grid)

    def get_hline(self, coord):
        y,x = coord
        return  remove_blanks(self.grid[y,:], self.blank)

    def get_vline(self, coord):
        y,x = coord
        return remove_blanks(self.grid[:,x], self.blank)

    def get_box(self, coord):
        y,x = coord
        return remove_blanks(self.grid[((y)//3)*3:((y)//3+1)*3,((x)//3)*3:((x)//3+1)*3].flatten(), self.blank)

    def solve_iteration_basic(self):
        allpossibilities = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        for y in range(9):
            for x in range(9):
                if self.grid[y,x] == self.blank:
                    interdictions = sorted(set(self.get_hline((y,x))+self.get_vline((y,x))+self.get_box((y,x))))
                    possibilities = list(allpossibilities-set(interdictions))
                    #print((x,y), possibilities)
                    if len(possibilities) == 1:
                        self.grid[y,x] = possibilities[0]

    def solve_iteration_guess(self, min=2):
        allpossibilities = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        for y in range(9):
            for x in range(9):
                if self.grid[y,x] == self.blank:
                    interdictions = sorted(set(self.get_hline((y,x))+self.get_vline((y,x))+self.get_box((y,x))))
                    possibilities = list(allpossibilities-set(interdictions))
                    #print((x,y), possibilities)
                    
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
                #Easiest method: check all possibilities
                self.solve_iteration_basic()
                if self.blank not in list(self.grid.flatten()):
                    unsolved = False
                if np.array_equal(self.grid, thisgrid):
                    #print('This grid cannot be solved using this resolution method.')
                    method += 1
            elif method == 1:
                #Dumbest method: guess when 2 possibilities
                self.solve_iteration_guess(min=2)
                if np.array_equal(self.grid, thisgrid):
                    self.grid = self.startgrid.copy()
                method = 0

        return iter


