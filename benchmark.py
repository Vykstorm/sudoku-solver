
from argparse import ArgumentParser
import re
import importlib


def get_solver(name):
    paths = {
        'default': 'solver.BasicSudokuIterativeSolver',
        'basic': 'solver.BasicSudokuIterativeSolver',
        'baseline': 'solver.BasicSudokuIterativeSolver',

        'deepsearch': 'deepsearchsolver.DeepSearchSudokuSolver',
        'deep-search': 'deepsearchsolver.DeepSearchSudokuSolver'
    }

    if name not in paths:
        raise Exception()
    module, cls_name = re.match("^(.+)\.(.+)$", 'solvers.' + paths[name]).groups()
    cls = importlib.import_module(module).__dict__[cls_name]

    solver = cls()
    return solver


if __name__ == '__main__':
    parser = ArgumentParser(description='CLI to benchmark sudoku solver algorithms')
    parser.add_argument('solver', type=str)
    parser.add_argument('--n', '--num-samples', type=int, default=100)

    parsed_args = parser.parse_args()

    n = parsed_args.n
    if n <= 0:
        parser.error('n argument must be a positive number')

    try:
        solver = get_solver(parsed_args.solver)
    except:
        parser.error('"{}" is not a valid sudoku algorithm'.format(parsed_args.solver))

    if __debug__:
        print("Debugging is enabled: Add -O option to get better results")

    # Do benchmark
    solver.benchmark(n)
