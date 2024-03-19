import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.image import imread

def pic_to_number(pic, blank):
    """
    As different numbers cover a different percentage, we use the percentage covered to 'guess' the number
    """
    sum = 0
    for i in pic.flatten():
        if i == 0:
            sum += 1
    covered = sum/len(pic.flatten())
    if covered == 0:
        return blank
    elif covered <= 0.11:
        return '1'
    elif covered <= 0.12:
        return '7'
    elif covered <= 0.135:
        return '4'
    elif covered <= 0.1425:
        return '3'
    elif covered <= 0.1475:
        return '5'
    elif covered <= 0.1535:
        return '2'
    elif covered <= 0.1585:
        return '9'
    elif covered <= 0.163:
        return '6'
    else:
        return '8'


def read_picture(path, blank='-'):

    grid = np.empty((9,9), dtype=str)

    pic = np.array(imread(path))[:,:,0]
    width, height = pic.shape
    #Get inside corners:
    x1, x2, y1, y2 = 0, 0, 0, 0
    for i in range(100):
        if pic[int(height/2),i] > 0:
            x1 = i
            break
    for i in range(100):
        if pic[int(height/2),-i] > 0:
            x2 = i
            break
    for i in range(100):
        if pic[i,int(width/2)] > 0:
            y1 = i
            break
    for i in range(100):
        if pic[-i,int(width/2)] > 0:
            y2 = i
            break
    pic = pic[y1:-y2, x1:-x2]
    width, height = pic.shape
    box = int((width+height)/18)
    if width/height > 1.1 or height/width > 1.1:
        raise ValueError('Picture is not a square')
    #plt.imshow(pic)
    #plt.show()

    for y in range(9):
        for x in range(9):
            num_pic = pic[y*box+int(box/6):(y+1)*box-int(box/6),x*box+int(box/6):(x+1)*box-int(box/6)]
            grid[y,x] = pic_to_number(num_pic, blank=blank)
            ##plt.imshow(num_pic)
            plt.show()
            pass
    return grid


if __name__ == "__main__":
    print(read_picture('sudoku_solver/pictures/sudoku1.png'))