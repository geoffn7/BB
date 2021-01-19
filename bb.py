import random
import numpy
from PIL import Image

class Cell:
    def __init__(self):
        #off = 0
        #on = 1
        #dying = 2
        self.state = random.randint(0, 2)

class Grid:
    def __init__(self, grid_length):

        self.grid_length = grid_length
        self.grid = self.setup(grid_length)

    def setup(self, grid_length):

        # TODO: Need to set up states of cells that encourage ripple effect, random is hit or miss 
        row = 0
        grid = []
        while row < grid_length:
            grid_row = []
            col = 0
            while col < grid_length:
                grid_row.append(Cell())
                col+=1
            grid.append(grid_row)
            row+=1
        
        return grid

def neighbours_on(present_grid, row, col):

    X = present_grid.grid_length - 1
    Y = present_grid.grid_length - 1
    neighbours = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
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
            elif present_grid.grid[row][col].state == 1:
                #All cells that were "on" go into the "dying" state
                future_grid.grid[row][col].state = 2
            else:
                #Cells that were in the dying state go into the off state
                future_grid.grid[row][col].state = 0
            col+=1
        row+=1
    return future_grid

def convertToImage(grid, grid_length):
    array = numpy.zeros([grid_length, grid_length, 3], dtype=numpy.uint8)
    row = 0
    while row < len(array):
        col = 0
        while col < len(array):
            cell_val = grid[row][col].state
            if cell_val == 0:
                #cell dead
                array[row][col] = [0, 0, 0] #black
            elif cell_val == 1:
                #cell live
                array[row][col] = [203, 235, 255] #light blue
            else:
                #cell dying
                array[row][col] = [57, 176, 255] #blue
            col+=1
        row+=1
    return array

def test():
    grid_length = 200
    testGrid = Grid(grid_length)

    for x in testGrid.grid:
        grid_string = ""
        for y in x:
            grid_string+= str(y.state) + " "

    iteratedGrid = iterate(testGrid)
    for x in iteratedGrid.grid:
        grid_string = ""
        for y in x:
            grid_string += str(y.state) + " "

    present_img = Image.fromarray(convertToImage(testGrid.grid, grid_length))
    future_img = Image.fromarray(convertToImage(iteratedGrid.grid, grid_length))

    present_img.save('1.png')
    future_img.save('2.png')

if __name__ == "__main__":
    test()