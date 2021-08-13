import random as r

import numpy as np

from base.sudoku import Sudoku
from solvers.backtracking import check_cell

""" Sudoku generator, providing valid grids of the specified order with the specified number of hints.
It uses a very naive (and in general inefficient) approach, although better algorithms could be implemented.
  
NOTE: For 9x9 grids (order 3), the minimum number of hints to make the (eventual) solution unique is 17.
"""


def generate_valid(order: int = 3, hints: int = 17):
    """ Generate a valid sudoku grid.

    WARNING: The generated grids are VALID, not necessarily SOLVABLE. Use the solver directly to assess solvability,
    or use generate_solvable instead (it performs solvability checks automatically).
    """
    if not isinstance(order, int):
        raise ValueError('The specified order must be an integer.')
    cells_per_edge = order * order
    if not isinstance(hints, int) or hints > cells_per_edge * cells_per_edge:
        raise ValueError(f'The specified number of hints must be an integer between '
                         f'0 and {cells_per_edge * cells_per_edge}.')

    grid = np.zeros(shape=(cells_per_edge, cells_per_edge), dtype=np.int32)
    placed_hints = 0
    while placed_hints < hints:
        # Select a random location among the empty ones
        empty_cells = np.argwhere(grid == 0)
        sampled_cell_idx = np.random.randint(0, empty_cells.shape[0], 1)
        sampled_cell = empty_cells[sampled_cell_idx]

        # Place a (valid) number
        possible_numbers = list(range(1, cells_per_edge + 1))
        while True:
            if len(possible_numbers) == 0:
                # Start over with an empty grid
                grid = np.zeros(shape=(cells_per_edge, cells_per_edge), dtype=np.int32)
                placed_hints = 0
                break
            # Sample from possible numbers
            n = r.choice(possible_numbers)
            # Insert
            grid[sampled_cell[0, 0], sampled_cell[0, 1]] = n
            # Check
            if check_cell(grid, sampled_cell[0, 0], sampled_cell[0, 1]):
                break
            # Not valid, remove the value from possible numbers and retry
            possible_numbers.remove(int(n))
        placed_hints += 1

    return grid


def generate_solvable(order: int = 3, hints: int = 17):
    """ Generate a solvable sudoku grid, retrying to generate valid grids until a proper one is found. """
    while True:
        grid = generate_valid(order, hints)
        s = Sudoku(grid)
        if s.solve():
            return grid