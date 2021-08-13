import numpy as np
from numba import njit

""" 
Naive backtracking + a simple heuristics for cells selection. 

The algorithm performs pretty well on 9x9 grids, but scales poorly. For instance, it is in general not suited for 16x16 
grids, since in many cases the completion time becomes enormous.

All the functions are written in a suitable way for numba to just-in-time compile them. It is only required to add the 
@njit decorator after having imported njit from the numba package. 
"""


@njit
def select_heuristics(grid: np.array):
    """ Function to select heuristically the next cell, based on the number of row and column constraints acting
    on each of the cells. The more constraints, the more convenient is the selection since failing fast is crucial
    in keeping the dimensionality of the problem low.

    NOTE: Block-wise constraints are easily computable, but it seems like it's not computationally worthy in most cases
    for 9x9 grids. Further investigation should be carried out to understand the tradeoff.
    """
    max_constr = -1
    optimal_cell = (-1, -1)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            # Cell is not free
            if grid[row, col] != 0:
                continue
            # Number of constraints
            row_constraints = np.count_nonzero(grid[row, :])
            col_constraints = np.count_nonzero(grid[:, col])

            constraints = row_constraints + col_constraints
            if constraints > max_constr:
                max_constr = constraints
                optimal_cell = (row, col)
    return optimal_cell


@njit
def check_cell(grid: np.array, row: int, col: int):
    """ Check if the cell (row, col) in the grid does not lead to constraints violation. """
    # Check row
    if not np.unique(grid[row, :]).sum() == np.sum(grid[row, :]):
        return 0

    # Check col
    if not np.unique(grid[:, col]).sum() == np.sum(grid[:, col]):
        return 0

    # Check block
    block_size = int(np.sqrt(grid.shape[0]))
    row_start = (row // block_size) * block_size
    col_start = (col // block_size) * block_size
    block = grid[row_start:row_start + block_size, col_start:col_start + block_size]
    if not np.unique(block).sum() == np.sum(block):
        return 0

    return 1


@njit
def solve_with_bt(grid):
    """ Solve the grid recursively with backtracking. It uses a simple heuristics to choose the empty cells. """
    row, col = select_heuristics(grid)
    if row == -1 and col == -1:                 # No more empty cells
        return 1

    # Try solutions and go on
    for i in range(1, grid.shape[0] + 1):
        grid[row, col] = i
        if not check_cell(grid, row, col):
            continue
        if solve_with_bt(grid):
            return 1
    grid[row, col] = 0
    return 0
