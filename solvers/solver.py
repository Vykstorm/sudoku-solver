

from sudoku import Sudoku
from time import time
from itertools import product, islice
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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

        accuracy = 0.0
        solve_time = 0.0


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

            accuracy = solved_count / count
            if solved_count > 0:
                solve_time = elapsed_time / solved_count

            # Print metrics
            info = []
            info.append("{:2.2f}% accuracy".format(100 * accuracy))
            if solved_count > 0:
                info.append("{:.3f} secs/sample".format(solve_time))

            if failures_count > 0:
                info.append("{} failures".format(failures_count))

            info.append("{} / {}".format(count, n))

            print('    '.join([stat.ljust(20) for stat in info]), end='\r')
        print()

        # Return dict with metrics
        return dict(accuracy=accuracy, solve_time=solve_time, failures=failures_count)



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



    def solve_animation(self, sudoku, figsize=None, repeat=True, repeat_delay=3000, interval=500):

        if figsize is None:
            figsize = (5, 5)

        # Create the figure
        fig = plt.figure(figsize=figsize)

        # We solve the sudoku and get a list of steps
        if not sudoku.valid:
            raise ValueError('You must pass a valid sudoku configuration to solve')

        sudoku = sudoku.copy()
        steps = []
        steps.append(sudoku.copy())

        try:
            while not sudoku.full:
                try:
                    self.step(sudoku)
                except ValueError:
                    raise ValueError()

                steps.append(sudoku.copy())
                if not (sudoku.valid and steps[-2] < sudoku and\
                sudoku.empty_cells_count == (steps[-2].empty_cells_count-1)):
                    raise ValueError()
        except ValueError:
            pass


        # First draw the sudoku grid
        Sudoku().draw()

        # Create one label for each sudoku cell
        labels = np.array([
            plt.text(k % 9 + 0.5, 8 - k // 9 + 0.5, '', horizontalalignment='center', verticalalignment='center',
                fontsize='xx-large', color='black')\
            for k, value in zip(range(0, 81), sudoku.flatten())]).reshape([9, 9])


        def init():
            return labels.flatten()

        def update(k):
            # Draw the next frame
            current = steps[k]
            for i, j in product(range(0, 9), range(0, 9)):
                # Update label text
                label = labels[i, j]
                text = '' if current[i, j].empty else str(current[i, j])
                label.set_text(text)
                label.set_color('black')

                # Update label color
                if k == 0:
                    continue
                prev = steps[k-1]

                if not current[i, j].valid:
                    label.set_color('red')
                elif prev[i, j].empty and not current[i, j].empty:
                    label.set_color('#33840E')


            return labels.flatten()


        # Create and return the animation
        anim = FuncAnimation(fig, update, frames=range(0, len(steps)), init_func=init, blit=True,
                            repeat=repeat, repeat_delay=repeat_delay, interval=interval)
        return anim


    def show_solve_animation(self, *args, **kwargs):
        anim = self.solve_animation(*args, **kwargs)
        plt.show()





class BasicSudokuIterativeSolver(SudokuIterativeSolver):
    '''
    Basic sudoku iterative algorithm solver implementation.
    This is the baseline for the rest of the algorithms.
    On each step, it iterates over all cells in the sudoku to find
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
