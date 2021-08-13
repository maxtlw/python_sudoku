from base.sudoku import Sudoku
from generators.naive_generator import generate_solvable


def test_generation():
    solvable_grid = generate_solvable(3, 17)
    s = Sudoku(solvable_grid)
    assert s.solve()

    solvable_grid = generate_solvable(3, 24)
    s = Sudoku(solvable_grid)
    assert s.solve()