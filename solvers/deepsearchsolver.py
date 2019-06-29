
import numpy as np
from itertools import product, takewhile, chain
from solvers.solver import SudokuSolver
import collections.abc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from operator import itemgetter




class DeepSearchSudokuSolver(SudokuSolver):

    def expand_node(self, sudoku, cell):
        # Expand a node
        assert cell.empty and cell.valid

        # For each value that we can put in the cell.
        for num in cell.remaining_numbers:
            try:
                # Set the cell's value
                cell.value = num
                yield cell

                # All empty cells in its neightbourhood (row, column or square) still valid?
                neighbours = chain(cell.row.empty_cells, cell.col.empty_cells, cell.square.empty_cells)
                if not all(map(lambda neighbour: neighbour.valid, neighbours)):
                    raise ValueError()


                # Call solve() recursively until complete the sudoku
                yield from self.solve_iterator(sudoku)
                return
            except ValueError:
                # Remove node branch (cell cannot have this value because it only leads to
                # invalid configurations). Test other branches
                del cell.value
                yield cell


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
        '''
        This method solves the sudoku. Its like solve() but it returns a iterator
        object. Whenever this algorithm makes a change to any of the sudoku cells,
        it stops until you call its method __next__ again and resume de execution.

        When the sudoku is fully solved, the next call to __next__ raises StopIteration
        exception. If the sudoku couldnt be solved, raises ValueError instead
        '''

        # Sudoku must be a valid configuration
        assert sudoku.valid

        if sudoku.full:
            # Nothing to be done, already solved
            return
        # Find the next node and expand it
        cell = self.next_node(sudoku)
        yield from self.expand_node(sudoku, cell)


    def solve(self, sudoku):
        '''
        Solves the sudoku. If the algorithm couldnt solve it, raise ValueError
        exception
        '''
        try:
            it = self.solve_iterator(sudoku)
            while True:
                next(it)
        except StopIteration:
            pass



    def solve_animation(self, sudoku, figsize=None, repeat=True, repeat_delay=3000, interval=300):
        if figsize is None:
            figsize = (5, 5)

        # Create the figure
        fig = plt.figure(figsize=figsize)

        # Get all the steps we've done to solve the sudoku (instead of storing on each
        # step the current sudoku state, we just save the index of cell changed and its new
        # value)
        transitions = []
        try:
            it = self.solve_iterator(sudoku.copy())
            while True:
                cell = next(it)
                transitions.append((cell.index, cell.value))
        except StopIteration:
            pass

        # Helper class such that we can create the state of the sudoku at the k-th iteration
        class Steps(collections.abc.Sequence):
            def __getitem__(self, k):
                indices = list(map(itemgetter(0), transitions))
                values = list(map(itemgetter(1), transitions))

                step = sudoku.copy()
                cells = list(map(step.flatten().__getitem__, indices))

                n = len(transitions)
                i, j = 0, 0
                while i < n and j < k:
                    cells[i].value = values[i]
                    i += 1
                    j += 1
                    while i < n and values[i] == 0:
                        del cells[i].value
                        i += 1

                return step


            def __len__(self):
                n = 1
                values = np.array(list(map(itemgetter(1), transitions)), dtype=np.uint8)

                n += np.count_nonzero(values != 0)
                n += np.count_nonzero(np.logical_and(values[1:] == 0, values[:-1] != 0))

                return n

        steps = Steps()

        # Draw the sudoku initial grid and generate the text labels
        labels = steps[0].plot()

        def init():
            return labels.flatten()

        def update(k):
            current = steps[k]
            prev = steps[k-1] if k > 0 else None

            # Update animation frame
            for i, j in product(range(0, 9), range(0, 9)):
                label = labels[i, j]
                # Update text label
                label.set_text(str(current[i, j]))

                # Update label color
                if prev is not None and prev[i, j].empty and not current.empty:
                    label.set_color('green')
                else:
                    label.set_color('black')

            return labels.flatten()


        # Create and return the animation
        anim = FuncAnimation(fig, update, frames=range(0, len(steps)), init_func=init, blit=True,
                            repeat=repeat, repeat_delay=repeat_delay, interval=interval)
        return anim


    def show_solve_animation(self, *args, **kwargs):
        anim = self.solve_animation(*args, **kwargs)
        plt.show()
