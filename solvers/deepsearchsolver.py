
import numpy as np
from itertools import product, takewhile, chain
from solvers.solver import SudokuSolver
from collections.abc import Sequence
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation




class DeepSearchSudokuSolver(SudokuSolver):

    def expand_node(self, sudoku, cell):
        # Expand a node
        assert cell.empty and cell.valid

        # For each value that we can put in the cell...
        for num in cell.remaining_numbers:
            try:
                # Set the cell's value
                cell.value = num
                yield cell.index, num

                # All empty cells in its neightbourhood (row, column or square) still valid?
                neighbours = chain(cell.row.empty_cells, cell.col.empty_cells, cell.square.empty_cells)
                if not all(map(lambda neighbour: neighbour.valid, neighbours)):
                    # If not, do backtracking
                    raise ValueError()
                # Call solve() recursively until complete the sudoku
                yield from self.solve_iterator(sudoku)
                return
            except ValueError:
                # Remove node branch (cell cannot have this value because it only leads to
                # invalid configurations). Test other branches
                del cell.value
                yield cell.index, 0


        # All branches lead to invalid configurations. Do backtracking
        raise ValueError()


    def next_node(self, sudoku):
        # Find the next node
        assert sudoku.valid and not sudoku.full

        for k in range(1, 10):
            # Search an empty cell where we can put k numbers
            for cell in sudoku.empty_cells:
                 if len(cell.remaining_numbers) == k:
                     return cell


    def solve_iterator(self, sudoku):
        # Sudoku must be a valid configuration
        assert sudoku.valid

        if sudoku.full:
            # Nothing to be done, already solved
            return
        # Find the next node and expand it
        cell = self.next_node(sudoku)
        yield from self.expand_node(sudoku, cell)


    def solve(self, sudoku):
        try:
            it = self.solve_iterator(sudoku)
            while True:
                next(it)
        except StopIteration:
            pass



    def solve_animation(self, sudoku, figsize=None, repeat=True, repeat_delay=3000, interval=500):
        if figsize is None:
            figsize = (5, 5)

        # Create the figure
        fig = plt.figure(figsize=figsize)


        # Solve the sudoku and get a list of steps we've done
        transitions = list(self.solve_iterator(sudoku.copy()))
        class StepsProxy(Sequence):
            def __getitem__(self, item):
                s = sudoku.copy()
                if item == 0:
                    return s

                for transition in transitions[:item]:
                    index, value = transition
                    cell = s.flatten().__getitem__(index)
                    cell.value = value

                return s

            def __len__(self):
                return len(transitions) + 1

        steps = StepsProxy()

        # Draw the sudoku grid and labels
        labels = steps[0].plot()

        def init():
            return labels.flatten()

        def update(k):
            # Draw the next frame
            current = steps[k]
            for i, j in product(range(0, 9), range(0, 9)):
                # Update label text
                label = labels[i, j]
                text = str(current[i, j])
                label.set_text(text)


            return labels.flatten()

        # Create and return the animation
        anim = FuncAnimation(fig, update, frames=range(0, len(steps)), init_func=init, blit=True,
                            repeat=repeat, repeat_delay=repeat_delay, interval=interval)
        return anim


    def show_solve_animation(self, *args, **kwargs):
        anim = self.solve_animation(*args, **kwargs)
        plt.show()
