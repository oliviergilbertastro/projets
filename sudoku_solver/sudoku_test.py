import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sudoku_solver import Sudoku
from sudoky_converter import *


grille = Sudoku([
    ['3','4','-','-','-','-','-','7','-'],
    ['8','-','-','4','-','7','2','5','-'],
    ['7','-','-','8','-','-','3','-','9'],
    ['-','1','3','-','-','6','4','-','-'],
    ['-','-','7','-','-','4','-','1','-'],
    ['-','-','4','-','-','-','6','-','3'],
    ['-','7','9','6','5','-','1','-','2'],
    ['-','-','-','7','-','-','5','9','8'],
    ['-','3','-','2','9','1','7','-','-'],
    ]
)

grille = Sudoku(read_picture('sudoku_solver/pictures/sudoku4.png'))

grille.show()
#print(grille.get_hline((4,3)))
#print(grille.get_vline((4,3)))
print('box:')
print(grille.get_box((6,6)))