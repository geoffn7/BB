import random

class Cell:
    def __init__(self):
        #off = 0
        #on = 1
        #dying = 2
        # TODO: Need to set up states of cells that encourage ripple effect, random is hit or miss
        self.state = random.randint(0, 2)

class Grid:
    def __init__(self, grid_length):

        self.grid = self.setup(grid_length)

    def setup(self, grid_length):
        grid = [[Cell = Cell()]*grid_length]*grid_length
        return grid