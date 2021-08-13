import time
from argparse import ArgumentParser
from pathlib import Path

from base.sudoku_factories import from_file, generated

""" Basic CLI to interact with the program. """

# Arguments
parser = ArgumentParser()
parser.add_argument('--input',
                    type=str,
                    default='gen',
                    help="Input filename: if provided, the program solves the grid represented in the file.")


if __name__ == '__main__':

    args = parser.parse_args()

    if args.input == 'gen':
        s = generated()
        print('Input grid (generated):')
    else:
        s = from_file(str(Path().parent.joinpath(args.input)))
        print(f'Input grid (from file {args.input}):')

    print(s)

    init_time = time.time()
    solved = s.solve()
    final_time = time.time()

    if solved:
        print(f'Solved. Took {final_time - init_time:.5f} seconds.')
        print(s)
    else:
        print(f'Unsolvable. Took {final_time - init_time:.5f} seconds')
