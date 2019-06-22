
import numpy as np
from itertools import product
from types import SimpleNamespace


class BacktrackingSudokuSolver:
    def __init__(self):
        # Auxiliar array (to boost performance)
        self.score = np.zeros([9, 9], dtype=np.uint8)


    def solve(self, sudoku):
        if sudoku.full:
            return sudoku

        score = self.score
        # Compute a score value for each cell
        for i, j in product(range(0, 9), range(0, 9)):
            cell = sudoku[i, j]

            # Penality increases as the amout of numbers we can put in the cell increases
            if cell != 0:
                score[i, j] = 0
                continue

            nums = cell.avaliable_numbers
            if len(nums) == 0:
                # The sudoku configuration is not valid (the cell which is empty dont have
                # any avaliable number)
                raise ValueError()

            score[i, j] = 10 - len(nums)


        # Iterate over each cell from maximum to minimum score
        for index in reversed(np.argsort(score.flatten())):
            i, j = index // 9, index % 9
            cell = sudoku[i, j]
            if cell != 0:
                continue

            nums = cell.avaliable_numbers
            if len(nums) == 1:
                # Only 1 possible number can go in this cell. No need to copy sudoku
                # configuration for backtracking
                sudoku[i, j] = next(iter(nums))
                return self.solve(sudoku)

            # More than 1 possible values can go to the current cell...

            # Make a copy of the current sudoku configuration
            other = sudoku.copy()

            # Test each possible value for the cell
            for num in nums:
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

        print("Sudokus solved: {} / {} ({} %), {} msecs solve mean time".format(
            solved_count, count, round((solved_count / count)*100, 1),
            str(round(elapsed_time / solved_count, 3))).rjust(8),
        end='\n')
