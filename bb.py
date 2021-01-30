import random
import numpy
from PIL import Image
import imageio
import time
import datetime

class Cell:

    #off = 0
    #on = 1
    #dying = 2
    population = [0, 1, 2]
    weights = [0.95, 0.04, 0.01]

    def __init__(self):
        self.state = random.choices(self.population, self.weights)[0]

class Grid:
    def __init__(self, grid_length):

        self.grid_length = grid_length
        self.grid = self.setup()
        
    def setup(self):

        row = 0
        grid = []
        while row < self.grid_length:
            grid_row = []
            col = 0
            while col < self.grid_length:
                grid_row.append(Cell())
                col+=1
            grid.append(grid_row)
            row+=1

        return grid

def neighbours_on(present_grid, row, col):

    #Determines for a given cell at [row, col] the number of neighbouring cells that are on

    X = present_grid.grid_length - 1
    Y = present_grid.grid_length - 1
    neighbours = lambda x, y : [(x2, y2) 
                                for x2 in range(x-1, x+2)
                                for y2 in range(y-1, y+2)
                                if (-1 < x <= X and
                                    -1 < y <= Y and
                                    (x != x2 or y != y2) and
                                    (0 <= x2 <= X) and
                                    (0 <= y2 <= Y))]

    all_neighbours = neighbours(row, col)
    num_on = 0
    for neighbour in all_neighbours:
        if present_grid.grid[neighbour[0]][neighbour[1]].state == 1:
            num_on+=1
    return num_on

def iterate(present_grid):

    future_grid = Grid(present_grid.grid_length)
    row = 0
    while row < len(present_grid.grid):
        col = 0
        while col < len(present_grid.grid[0]):
            if present_grid.grid[row][col].state == 0:
                #a cell turns on if it was off but had exactly two neighbours that were on
                num_on = neighbours_on(present_grid, row, col)
                if num_on == 2:
                    future_grid.grid[row][col].state = 1
                else:
                    future_grid.grid[row][col].state = 0
            elif present_grid.grid[row][col].state == 1:
                #All cells that were "on" go into the "dying" state
                future_grid.grid[row][col].state = 2
            else:
                #Cells that were in the dying state go into the off state
                future_grid.grid[row][col].state = 0
            col+=1
        row+=1
    return future_grid

def convertToImage(grid):
    array = numpy.zeros([grid.grid_length, grid.grid_length, 3], dtype=numpy.uint8)
    row = 0
    while row < len(array):
        col = 0
        while col < len(array):
            cell_val = grid.grid[row][col].state
            if cell_val == 0: #cell dead
                array[row][col] = [0, 0, 0] #set block to black
            elif cell_val == 1: #cell live
                array[row][col] = [255, 255, 255] #set block to white
            else: #cell dying
                array[row][col] = [0, 85, 255] #set block to blue
            col+=1
        row+=1
    return array

def produce_bb_gif():
    grid_length = 300
    
    filenames = []
    current_grid = Grid(grid_length)

    image_count = 0
    max_num_images = 1000
    
    while True:
        img = Image.fromarray(convertToImage(current_grid))
        filename = 'images/' + str(image_count) + '.png'
        filenames.append(filename)
        img.save(filename)
        
        print("["+str(datetime.datetime.now()).split(" ")[1]+"] Image "+str(image_count+1)+" created")
        
        image_count+=1

        if image_count < max_num_images:
            current_grid = iterate(current_grid)
        else:
            break

    with imageio.get_writer('gif/bb_sim.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

if __name__ == "__main__":
    start_time = time.time()
    produce_bb_gif()
    end_time = time.time()
    run_time = end_time - start_time

    print("\nStart: "+datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S'))
    print("End: "+datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S'))
    print("Runtime: "+str(round(run_time, 3))+" seconds")