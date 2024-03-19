import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sudoku_solver import Sudoku
from sudoky_converter import *


grille = Sudoku(read_picture('sudoku_solver/pictures/sudoku7.png', show=True))

grille.show()
grille.show()