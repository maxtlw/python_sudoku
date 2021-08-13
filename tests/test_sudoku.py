import numpy as np
import pytest

from base.sudoku import Sudoku  # , flatten, deflatten


def test_invalid_grid():
    # Build an invalid grid
    invalid_grid = np.zeros(shape=(10, 10))
    with pytest.raises(ValueError):
        Sudoku(initial_grid=invalid_grid)

    invalid_grid_2 = np.zeros(shape=(9, 9))
    invalid_grid_2[3, 3] = 10
    with pytest.raises(ValueError):
        Sudoku(initial_grid=invalid_grid_2)


def test_validate_grid():
    zero_grid = np.zeros(shape=(9, 9))
    s = Sudoku(zero_grid)
    s.validate_grid()                                   # Assert that no exception is raised

    # Row-wise
    legal_grid = np.zeros(shape=(9, 9))
    legal_grid[5, 4] = 8
    legal_grid[5, 7] = 5
    s = Sudoku(legal_grid)
    s.validate_grid()                                   # Assert that no exception is raised

    illegal_grid = np.zeros(shape=(9, 9))
    illegal_grid[2, 1] = 1
    illegal_grid[2, 3] = 1
    with pytest.raises(ValueError):
        Sudoku(illegal_grid)

    # Col-wise
    legal_grid = np.zeros(shape=(9, 9))
    legal_grid[1, 4] = 6
    legal_grid[1, 7] = 4
    s = Sudoku(legal_grid)
    s.validate_grid()                                   # Assert that no exception is raised

    illegal_grid = np.zeros(shape=(9, 9))
    illegal_grid[1, 2] = 1
    illegal_grid[3, 2] = 1
    with pytest.raises(ValueError):
        Sudoku(illegal_grid)

    # Block-wise
    legal_grid = np.zeros(shape=(9, 9))
    legal_grid[1, 1] = 4
    legal_grid[1, 2] = 5
    legal_grid[-1, -1] = 4
    s = Sudoku(legal_grid)
    s.validate_grid()                                    # Assert that no exception is raised

    illegal_grid = np.zeros(shape=(9, 9))
    illegal_grid[0, 2] = 1
    illegal_grid[1, 1] = 1
    with pytest.raises(ValueError):
        Sudoku(illegal_grid)


def test_check_solved():
    zero_grid = np.zeros(shape=(9, 9))
    s = Sudoku(zero_grid)
    assert s.solved is False


def test_solve_empty():
    grid = np.zeros(shape=(9, 9))
    s = Sudoku(grid)
    assert s.solve()

    grid = np.zeros(shape=(16, 16))
    s = Sudoku(grid)
    assert s.solve()


def test_solve_9():
    grid = np.zeros(shape=(9, 9))

    grid[8, 8] = 9
    s = Sudoku(grid)
    assert s.solve()

    grid[8, 8] = 1
    s = Sudoku(grid)
    assert s.solve()

    grid[8, 8] = 0
    grid[0, 0] = 5
    s = Sudoku(grid)
    assert s.solve()

    grid[7, 4] = 1
    s = Sudoku(grid)
    assert s.solve()
