

from sudoku import Sudoku
from time import time
from itertools import product, islice
import numpy as np


class SudokuSolver:
    '''
    Its the base class for all sudoku algorithm solvers
    '''
    def solve(self, sudoku: Sudoku):
        '''
        This method must try to solve the given sudoku.
        If the algorithm cant find any solution, must raise ValueError
        '''
        raise NotImplementedError()

    def benchmark(self, n=100, *args, **kwargs):
        '''
        Run this sudoku solver and evaluate performance and accuracy
        :param n: Number of sudokus to be used to evaluate this algorithm (they will be
        fetched from sudoku dataset)
        '''
        assert n > 0

        from dataset import SudokuDataset
        samples = SudokuDataset().get_samples(return_solutions=True, shuffle=True, *args, **kwargs)


        solved_count, count = 0, 0
        elapsed_time = 0.0
        failures_count = 0

        for sample, solution in islice(samples, n):
            count += 1
            try:
                result = sample.copy()
                t0 = time()
                self.solve(result)
                t1 = time()

                if not np.all((result.view(type=np.ndarray) == solution.view(type=np.ndarray))):
                    raise ValueError()

                # Solved sudoku succesfully
                elapsed_time += t1 - t0
                solved_count += 1

            except ValueError:
                pass

            except AssertionError:
                failures_count += 1

            # Print stats
            info = []
            info.append("{:2.2f}% accuracy".format(100 * solved_count / count))
            if solved_count > 0:
                info.append("{:.3f} msecs/sample".format(elapsed_time / solved_count))

            if failures_count > 0:
                info.append("{} failures".format(failures_count))

            info.append("{} / {}".format(count, n))

            print('    '.join([stat.ljust(20) for stat in info]), end='\r')
        print()


class SudokuIterativeSolver(SudokuSolver):
    '''
    Represent any kind of algorithm that can solve a sudoku iteratively: Adding
    one number on each iteration and finish when no empty cells left.
    '''

    def step(self, sudoku: Sudoku):
        raise NotImplementedError()


    def solve(self, sudoku: Sudoku):
        assert sudoku.valid

        while not sudoku.full:
            prev = sudoku.copy() if __debug__ else sudoku
            self.step(sudoku)
            assert sudoku.valid and prev < sudoku and\
                sudoku.empty_cells_count == (prev.empty_cells_count-1)



class BasicSudokuIterativeSolver(SudokuIterativeSolver):
    '''
    Basic sudoku iterative algorithm solver implementation.
    This is the baseline for the rest of the algorithms.
    On each step, it iterates over all cells in the sudoku on each step, to find
    an empty cell that can only have 1 possible value (not present in its row, column or square).
    Then assign that remaining value to the cell.
    '''

    def step(self, sudoku):
        for i, j in product(range(0, 9), range(0, 9)):
            if not sudoku[i, j].empty:
                continue

            nums = sudoku[i, j].remaining_numbers
            if len(nums) == 1:
                sudoku[i, j] = next(iter(nums))
                return

        # Cant put any number
        raise ValueError()
