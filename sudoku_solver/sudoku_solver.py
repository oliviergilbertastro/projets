import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Sudoku():
    def __init__(self, grid):
        self.grid = np.array(grid)
        if self.grid.shape != (9,9):
            raise ValueError("Grid is not 9x9")

    def show(self):
        print(self.grid)

    def get_hline(self, coord):
        y,x = coord
        return self.grid[y,:]

    def get_vline(self, coord):
        y,x = coord
        return self.grid[:,x]

    def get_box(self, coord):
        y,x = coord
        return self.grid[((y)//3)*3:((y)//3+1)*3,((x)//3)*3:((x)//3+1)*3].flatten()

    def solve_iteration(self):
        pass


