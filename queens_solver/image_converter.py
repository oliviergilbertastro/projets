import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


def read_picture(path, show=False, nb_of_checks=5):

    img = np.array(imread(path))[:,:,:]
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
    img = img[y1:-(y2+1), x1:-(x2+1)]
    width, height = img.shape[1], img.shape[0]


    # Check width of the cells by taking the median distance between vertical black lines in multiple rows
    # We know the cells are all squares, so no need to do this vertically too
    lengths_list = []
    already_on_line = [True for i in range(nb_of_checks)]
    lengths = [0 for i in range(nb_of_checks)]
    line_lengths_list = []
    line_lengths = [0 for i in range(nb_of_checks)]
    for i in range(width):
        for n in range(nb_of_checks):
            if (img[int(height/(n+2)), i] == black).all() and not already_on_line[n]:
                lengths_list.append(lengths[n])
                lengths[n] = 0
                line_lengths[n] += 1
                already_on_line[n] = True
            elif (img[int(height/(n+2)), i] == black).all() and already_on_line:
                line_lengths[n] += 1
            elif already_on_line[n]:
                already_on_line[n] = False
                line_lengths_list.append(line_lengths[n])
                line_lengths[n] = 0
                lengths[n] += 1
            else:
                already_on_line[n] = False
                lengths[n] += 1
    length_cell = np.median(lengths_list)+np.quantile(line_lengths_list, 0.1)*2
    n_cells = round(width/length_cell)
    grid = np.empty((n_cells,n_cells), dtype=int)

    # Get the colors
    xs = []
    ys = []
    colors = []
    for y in range(n_cells):
        for x in range(n_cells):
            xs.append(int((x+1/2)*length_cell))
            ys.append(int((y+1/2)*length_cell))
            col = img[int((y+1/2)*length_cell),int((x+1/2)*length_cell)][:3]
            col = (int(col[0]*255), int(col[1]*255), int(col[2]*255))

            try:
                if col in colors:
                    col_int = colors.index(col)
                else:
                    col_int = len(colors)
                    colors.append(col)
            except:
                col_int = len(colors)
                colors.append(col)
            grid[y,x] = col_int
    
    if show:
        plt.imshow(img)
        plt.plot(xs,ys, "o")
        plt.show()
    return grid, colors



if __name__ == "__main__":
    from queens_solver import Solver
    grid, colors = read_picture('queens_solver/game2.png', show=True)
    colors = [[colors[i][k]/255 for k in range(3)] for i in range(len(colors))]
    Queens = Solver(grid, colors)
    Queens.show()