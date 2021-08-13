import math

import numpy as np

from solvers.backtracking import solve_with_bt, check_cell


class Sudoku:
    """ Sudoku object. """

    def __init__(self, initial_grid: np.array):

        blocks_size = int(math.sqrt(initial_grid.shape[0]))
        if initial_grid.shape[0] != initial_grid.shape[1] or blocks_size ** 2 != initial_grid.shape[0]:
            raise ValueError('Initial grid must be a compatible (perfect square) sudoku grid.')
        self.__grid = np.array(initial_grid, dtype=np.int32)                          # Deepcopy the grid
        self.__blocks_size = blocks_size                                # Just for the sake of performance

        # Validate the values
        self.validate_grid()

    @property
    def grid(self):                 # Avoid accessing the grid directly, so it is kept always valid
        return self.__grid

    @property
    def solved(self):
        """ Whether the grid is solved. """
        # If not all spots are full, it's surely not solved
        for i in self.__grid.flatten():
            if i == 0:
                return False
        # If it's full and valid, then it's solved
        try:
            self.validate_grid()
        except ValueError:
            return False
        return True

    def validate_grid(self):
        """ Validate the grid. """
        for i in self.__grid.flatten():
            if i > self.grid.shape[0] or i < 0:
                raise ValueError(f'Grid contains value {i}, which is not valid.')

        # Check every cell to validate the whole grid
        for i in range(self.grid.shape[0]):             # It's inefficient but not a problem (called only few times)
            for j in range(self.grid.shape[1]):
                if not check_cell(self.grid, i, j):
                    raise ValueError(f'Cell ({i}, {j}) does not respect constraints.')

    def solve(self, double_check: bool = False):
        """ Solve the grid. It returns True if a valid solution was found, False otherwise.

        :param double_check: Check again if the ultimate grid is solved before returning. Usually not necessary. """
        solved = solve_with_bt(self.grid)
        return bool(solved) if not double_check else self.solved

    def __str__(self):
        # Build rows representations
        rows_str = []
        for row in range(self.grid.shape[0]):
            row_str = '| '
            for col in range(self.grid.shape[1]):
                if self.grid[row, col] != 0:
                    row_str += f'{self.grid[row, col]:2}' + ' '
                else:
                    row_str += '   '

                if (col + 1) % self.__blocks_size == 0 and col < self.grid.shape[1] - 1:
                    row_str += '| '
            row_str += '|'
            rows_str.append(row_str)

        # Find the longest row, for the sake of presentation
        longest_row_len = max([len(r) for r in rows_str])
        line_separator = ''.join(['-'] * longest_row_len)

        # Merge rows, adding --- separators when needed
        to_return = line_separator + '\n'
        for i, r in enumerate(rows_str):
            to_return += r + '\n'
            if (i + 1) % self.__blocks_size == 0:
                to_return += line_separator + '\n'

        return to_return

