
import numpy as np
from itertools import product
from types import SimpleNamespace


class BacktrackingSudokuSolver:
    def __init__(self):
        pass

    def solve(self, sudoku):
        if sudoku.full:
            # If the sudoku is full, its already solved
            return sudoku

        scores = np.zeros([9, 9], dtype=np.uint8)

        # Iterate over all the cells in the sudoku
        for i, j in product(range(0, 9), range(0, 9)):
            cell = sudoku[i, j]

            # We dont need to analyze already filled cells
            if cell != 0:
                continue

            # Get all possible numbers can add to the cell
            nums = cell.avaliable_numbers

            if len(nums) == 0:
                # The sudoku configuration is not valid (the cell which is empty dont have
                # any avaliable number)
                raise ValueError()

            if len(nums) == 1:
                # Only 1 possible number. Add the number to the cell and keep solving the sudoku
                sudoku[i, j] = next(iter(nums))
                return self.solve(sudoku)

            # More than 1 possible numbers that can be added to the cell. We can compute a score
            # to later select the cell that has minimum avaliable numbers
            scores[i, j] = 10 - len(nums)


        # Get a cell with maximum score
        scores = scores.flatten()
        index = np.random.choice(np.nonzero(scores == scores.max())[0])
        i, j = index // 9, index % 9
        cell = sudoku[i, j]

        # All possible numbers that can be placed in the selected cell
        nums = cell.avaliable_numbers

        # Make a copy of the current sudoku configuration
        other = sudoku.copy()

        # Test each possible value for the cell
        for num in np.random.permutation(nums):
            try:
                # Set the cell's number
                other[i, j] = num

                # Call this function recursively. If the number we added to the
                # cell is not valid, this will raise an exception
                return self.solve(other)
            except ValueError:
                # Restore old configuration
                del other[i, j]

        # No solutions found
        raise ValueError()



if __name__ == '__main__':
    from dataset import SudokuDataset
    from time import time

    solver = BacktrackingSudokuSolver()
    solved_count = 0
    elapsed_time = 0

    for count, sample in enumerate(SudokuDataset().get_samples(), 1):
        quizz, solution = sample
        try:
            t0 = time()
            solved = solver.solve(quizz)
            t1 = time()
            if not np.all((solved == solution).flatten()):
                raise ValueError()
            solved_count += 1
            elapsed_time += t1 - t0
        except ValueError:
            pass

        print("Sudokus solved: {} / {} ({} %), {} secs solve mean time".format(
            solved_count, count, round((solved_count / count)*100, 1),
            str(round(elapsed_time / solved_count, 3))).rjust(8),
        end='\n')
