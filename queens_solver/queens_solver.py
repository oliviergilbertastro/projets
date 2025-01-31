import numpy as np
import matplotlib.pyplot as plt
import copy
from matplotlib.patches import Rectangle
import time

def count_in_array(a, b):
    """Return the number of instances of b in array a"""
    if len(np.array(a).shape) > 1:
        a = np.ravel(a)
    res = 0
    for i in a:
        if i==b:
            res+=1
    return res

class Solver:
    def __init__(self, grid, colors):
        assert grid.shape[0] == grid.shape[1] == len(colors)
        self.grid = grid # np.array of numbers representing colors
        self.colors = colors
        self.data = np.zeros_like(self.grid) # 0=no info, 1=x, 2=crown
        self.last_checkpoint = copy.deepcopy(self.data)
        self.n = grid.shape[0]
        self.placed_crowns = [0]
        self.placed_Xs = [0]
        self.color_indices = self.get_color_indices()
        self.solved = False
        assert len(self.color_indices) == self.n

    def get_color_indices(self):
        colors = {}
        for y in range(self.n):
            for x in range(self.n):
                if self.grid[y,x] in colors:
                    colors[self.grid[y,x]].append((y,x))
                else:
                    colors[self.grid[y,x]] = [(y,x)]
        return colors
            
    
    def show(self):
        fig = plt.gcf()
        fig.set_size_inches(6/9*self.n, 6/9*self.n)
        ax1 = plt.subplot(111)
        ticklabels = ax1.get_xticklabels()
        ticklabels.extend( ax1.get_yticklabels() )
        for label in ticklabels:
            label.set_fontsize(0)
        for i in range(self.n+1):
            lw = 2
            plt.axvline(i*50, ymin=0, ymax=1, color='black', linewidth=lw)
            plt.axhline(i*50, xmin=0, xmax=1, color='black', linewidth=lw)
        for y in range(self.n):
            for x in range(self.n):
                rect = Rectangle((x*50, y*50), 50, 50, color=self.colors[self.grid[y,x]], alpha=1, fill=True)
                ax1.add_patch(rect)
                if self.data[y,x] == 1:
                    plt.text((x)*50+13.5, (y)*50+35, r"$\times$", fontsize=20, color="black")
                if self.data[y,x] == 2:
                    plt.text((x)*50+10, (y)*50+39, "Q", fontsize=30, weight="bold", color="black")
                
                #if self.startgrid[y,x] != self.blank:
                #    rect = Rectangle((x*50, y*50), 50, 50, color='black', alpha=0.25, fill=True)
                #    ax1.add_patch(rect)
                #if self.grid[y,x] != self.blank:
                #    plt.text((x)*50+12.5, (y)*50+39, self.grid[y,x], fontsize=30)
                pass
        plt.xlim(0, 50*self.n)
        plt.ylim(50*self.n, 0)
        plt.show()

    def get_cells_with_same_color(self, pos):
        return self.color_indices[self.grid[pos[0],pos[1]]]

    def color_array(self, n_color):
        """Returns the array of [0,1,2] representing the info we have on the grid for a specific color"""
        assert n_color in self.grid
        color_a = []
        for c in self.color_indices[n_color]:
            color_a.append(self.data[c[0],c[1]])
        return color_a


    def check_if_possible(self, pos):
        """pos = [y,x]"""
        # Check hline
        if 2 in self.data[pos[0],:]:
            return False
        # Check vline
        elif 2 in self.data[:,pos[1]]:
            return False
        # Check same color
        for c in self.get_cells_with_same_color(pos):
            if 2 == self.data[c[0],c[1]]:
                return False
        # Check 4-diagonal corners
        for x in [-1,1]:
            for y in [-1,1]:
                try:
                    if self.data[pos[0]+y,pos[1]+x] == 2:
                        return False
                except:
                    pass
        
        return True

    def put_Xs(self):
        # Check all the grid
        # For each spot (if possible), place a crown
        # If rows, columns, or colors now contain >1 crown, cross that cell.
        for y in range(self.n):
            for x in range(self.n):
                if self.data[y,x] == 0: # Only do this if we haven't already placed something
                    original_data = copy.deepcopy(self.data)
                    self.data[y,x] = 2
                    for n in range(self.n):
                        # If >1 Queen in hline
                        if count_in_array(self.data[n,:],2) > 1:
                            original_data[y,x] = 1
                        # If >1 Queen in vline
                        elif count_in_array(self.data[:,n],2) > 1:
                            original_data[y,x] = 1
                    # If >1 Queen in color
                    if count_in_array(self.color_array(self.grid[y,x]),2) > 1:
                        original_data[y,x] = 1
                    # If >1 Queen in corner radius
                    for x1 in [-1,1]:
                        for y1 in [-1,1]:
                            try:
                                if self.data[y+y1,x+x1] == 2 and (x+x1) >= 0 and (x+x1) <= self.n-1 and (y+y1) >= 0 and (y+y1) <= self.n-1:
                                    original_data[y,x] = 1
                            except:
                                pass
                    self.data = original_data
        # Update the data
        try:
            self.data = original_data
        except:
            if not self.solved:
                self.data = copy.deepcopy(self.last_checkpoint)

    def cut_possibilities(self):
        # Check all the grid
        # For each spot (if possible), place a temporary crown, check which cells are now Xs
        # If all cells in a row, column, or color are now blocked, block the former cell.
        for y in range(self.n):
            for x in range(self.n):
                if self.data[y,x] == 0: # Only do this if we haven't already placed something
                    original_data = copy.deepcopy(self.data)
                    self.data[y,x] = 2
                    self.put_Xs()
                    for n in range(self.n):
                        if count_in_array(self.data[n,:],1) == len(self.data[n,:]) or count_in_array(self.data[:,n],1) == len(self.data[:,n]) or count_in_array(self.color_array(n),1)== len(self.color_array(n)):
                            original_data[y,x] = 1
                    self.data = original_data

    def put_crowns(self):
        # Check if only one square is remaining in each row, column, color.
        # If so, place a crown there.
        for n in range(self.n):
            # Place crown in hline
            if count_in_array(self.data[n,:],2) == 0 and count_in_array(self.data[n,:],0) == 1:
                #print("hline", n,list(self.data[n,:]).index(0))
                self.data[n,list(self.data[n,:]).index(0)] = 2
            # Place crown in vline
            if count_in_array(self.data[:,n],2) == 0 and count_in_array(self.data[:,n],0) == 1:
                #print("vline", list(self.data[:,n]).index(0),n)
                self.data[list(self.data[:,n]).index(0),n] = 2
            # Place crown in color
            if count_in_array(self.color_array(n),2) == 0 and count_in_array(self.color_array(n),0) == 1:
                for cell in self.color_indices[n]:
                    if self.data[cell[0], cell[1]] == 0:
                        #print("color", cell[0], cell[1])
                        self.data[cell[0], cell[1]] = 2

    def random_try(self):
        if (self.last_checkpoint == np.zeros_like(self.grid)).all():
            print("Set checkpoint")
            self.last_checkpoint = copy.deepcopy(self.data)
        found = False
        while not found:
            regions_empty_spots = []
            for n in range(self.n):
                regions_empty_spots.append(count_in_array(self.data[n,:],0)) # hline
                regions_empty_spots.append(count_in_array(self.data[:,n],0)) # vline
                regions_empty_spots.append(count_in_array(self.color_array(n),0)) # color
            regions_empty_spots_sorted = copy.deepcopy(regions_empty_spots)
            regions_empty_spots_sorted.sort()
            index_found = False
            k = 0
            while not index_found:
                min_index = regions_empty_spots.index(regions_empty_spots_sorted[k])
                if regions_empty_spots[min_index] == 0:
                    k += 1
                else:
                    index_found = True
            if min_index % 3 == 0: # hline
                x, y = np.random.randint(0,self.n), min_index//3
            elif min_index % 3 == 1: # vline
                x, y = min_index//3, np.random.randint(0,self.n)
            else:
                y, x = self.color_indices[min_index//3][np.random.randint(0,len(self.color_indices[min_index//3]))]

            if self.data[y,x] == 0:
                self.data[y,x] = 2
                found = True


    def solve(self, show_each_iteration=False, verbose=False):
        start_time = time.time()
        tries = 0
        changes = 0
        while not self.solved:
            self.last_data = copy.deepcopy(self.data)
            self.placed_crowns.append(count_in_array(self.data, 2))
            self.placed_Xs.append(count_in_array(self.data, 1))
            if self.placed_crowns[-1] >= self.placed_crowns[-2]:
                self.put_Xs()
            if self.placed_crowns[-1] == self.placed_crowns[-2] and self.placed_Xs[-1] == self.placed_Xs[-2] and tries > 0:
                self.random_try()
            self.cut_possibilities()
            self.put_crowns()
            if (self.data == self.last_data).all():
                changes += 1
            else:
                changes = 0
            if not self.check_valid() or changes >= 2 and not (self.last_checkpoint == np.zeros_like(self.grid)).all():
                self.data = copy.deepcopy(self.last_checkpoint)
            self.solved = self.check_solved()
            #if self.solved:
            #    self.show()
            tries += 1
            if verbose:
                print(tries, changes, self.check_valid(), self.solved)
            if show_each_iteration:
                self.show()
        self.put_Xs()
        print(f"Solved in {np.around(time.time() - start_time, 2)} seconds")

    def check_valid(self):
        for n in range(self.n):
            if count_in_array(self.data[n,:],2) > 1 or count_in_array(self.data[:,n],2) > 1 or count_in_array(self.color_array(n),2) > 1:
                return False
        return True
    
    def check_solved(self):
        for n in range(self.n):
            if count_in_array(self.data[n,:],2) != 1 or count_in_array(self.data[:,n],2) != 1 or count_in_array(self.color_array(n),2) != 1:
                return False
        return self.check_valid()


if __name__ == "__main__":
    grid = np.array([[0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     ])
    grid = np.array([[0,0,1,1,1],
                     [0,1,1,1,1],
                     [0,2,2,1,1],
                     [0,3,3,3,3],
                     [0,3,4,4,3],
                     ])
    grid = np.array([[0,0,1,1],
                     [0,0,1,1],
                     [3,3,2,2],
                     [3,3,2,2],
                     ])
    grid = np.array([[0,0,1,1,1],
                     [0,1,1,1,1],
                     [0,2,2,1,1],
                     [0,3,3,3,3],
                     [0,0,4,4,3],
                     ])
    colors = ["red","blue","green","orange","purple"][:]
    Queens = Solver(grid, colors)
    Queens.show()
    Queens.solve()
    Queens.show()
