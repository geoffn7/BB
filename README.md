# BB
Implementation of Brian's Brain (cellular automation)

Creates a 300 x 300 grid of cells where each cell can have one of three states - on, off, dying.
The initial states of each cell is set with the following probability weights for each state - 95% off, 4% on, 1% dying.

For each step forward in time, each cell changes states based on the following logic:

- cells that are on become dying
- cells that are dying turn off
- cells that are off turn on if and only if 2 neighbouring cells are on, otherwise they stay off

Running the script will move the grid of cells forward in time incrementally 1000 times, creating an RGB image of the grid for each step in time.
Once all 1000 images have been created the script will string the images together into a viewable gif showing the progression of the grid of cells.
