import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


def read_picture(path, show=False):

    img = np.array(imread(path))[:,:,:]
    print(img.shape)
    width, height = img.shape[1], img.shape[0]
    if img.shape[2] == 4:
        black = (0,0,0,1)
    elif img.shape[2] == 3:
        black = (0,0,0)
    else:
        ValueError("That is not a 3-color image")
    #Get inside corners:
    x1, x2, y1, y2 = 0, 0, 0, 0
    for i in range(int(width/2)):
        if (img[int(height/2),i] == black).all():
            x1 = i
            break
    for i in range(int(width/2)):
        if (img[int(height/2),-i] == black).all():
            x2 = i
            break
    for i in range(int(height/2)):
        if (img[i,int(width/2)] == black).all():
            y1 = i
            break
    for i in range(int(height/2)):
        if (img[-i,int(width/2)] == black).all():
            y2 = i
            break
    x2 = 1 if x2 == 0 else x2
    y2 = 1 if y2 == 0 else y2
    print(x1,x2,y1,y2)
    img = img[y1:-(y2+1), x1:-(x2+1)]
    width, height = img.shape[1], img.shape[0]
    if show:
        plt.imshow(img)
        plt.show()

    # Check width of the cells by taking the median distance between vertical black lines in multiple rows
    # We know the cells are all squares, so no need to do this vertically too
    lenghts = []
    for i in range(width):
        for n in range(5):
            img[int(height/(n+1))]
    grid = np.empty((9,9), dtype=str)



if __name__ == "__main__":
    print(read_picture('queens_solver/game2.png', show=True))