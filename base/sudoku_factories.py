import os.path

import numpy as np

from base.sudoku import Sudoku
from generators.naive_generator import generate_solvable

""" Helper functions/factories for valid example grids. Notice that not all of them are proper sudokus, since some 
can be unsolvable and some can have multiple solutions. 
"""


def empty(order: int = 3):
    """ Empty grid of the specified order. """
    grid = np.zeros(shape=(order * order, order * order))
    return Sudoku(grid)


def unsolvable3():
    """ Unsolvable 9x9 "sudoku". """
    grid = np.zeros(shape=(9, 9))
    grid[0, 0] = 2
    grid[0, 3] = 9
    grid[1, 7] = 6
    grid[2, 5] = 1
    grid[3, 0] = 5
    grid[3, 2] = 2
    grid[3, 3] = 6
    grid[3, 6] = 4
    grid[3, 8] = 7
    grid[4, 5] = 4
    grid[4, 6] = 1
    grid[5, 4] = 9
    grid[5, 5] = 8
    grid[5, 7] = 2
    grid[5, 8] = 3
    grid[6, 5] = 3
    grid[6, 7] = 8
    grid[7, 2] = 5
    grid[7, 4] = 1
    grid[8, 2] = 7
    return Sudoku(grid)


def from_file(filename: str):
    """ Sudoku (9x9) or Hexadoku (16x16) grid loaded from the specified file. """
    if not os.path.isfile(filename):
        raise ValueError(f'{filename} is not a valid file path.')

    def conv(n):
        if n == '*':
            return 0
        try:
            nn = int(n)
            if 0 < nn < 17:
                return nn
        except ValueError:
            pass

        raise ValueError(f'Grid contains element {n}, which is not valid. Make sure the loaded grid is either'
                         f'a 9x9 or a 16x16, with valid values in the range 1-9 or 1-G, respectively.')

    with open(filename) as infile:
        rows = []
        for line in infile:
            splitted_line = line.split()
            if len(splitted_line) == 0:
                continue
            col = [conv(n) for n in splitted_line]
            rows.append(col)

    return Sudoku(np.array(rows))


def generated(order: int = 3, hints: int = 17):
    """ An original sudoku (solvable), generated online by the provided algorithm. """
    solvable_sudoku = generate_solvable(order, hints)
    return Sudoku(solvable_sudoku)
