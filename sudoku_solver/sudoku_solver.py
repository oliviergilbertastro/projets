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


