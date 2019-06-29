
import numpy as np
from itertools import product, takewhile, chain
from solver import SudokuSolver





class DeepSearchSudokuSolver(SudokuSolver):

    def solve(self, sudoku):
        def expand_node(cell):
            # Expand a node
            assert cell.empty and cell.valid

            # For each value that we can put in the cell...
            for num in cell.remaining_numbers:
                try:
                    # Set the cell's value
                    cell.value = num

                    # All empty cells in its neightbourhood (row, column or square) still valid?
                    neighbours = chain(cell.row.empty_cells, cell.col.empty_cells, cell.square.empty_cells)
                    if not all(map(lambda neighbour: neighbour.valid, neighbours)):
                        # If not, do backtracking
                        raise ValueError()
                    # Call solve() recursively until complete the sudoku
                    self.solve(sudoku)
                    return
                except ValueError:
                    # Remove node branch (cell cannot have this value because it only leads to
                    # invalid configurations). Test other branches
                    del cell.value

            # All branches lead to invalid configurations. Do backtracking
            raise ValueError()


        def next_node():
            # Find the next node
            assert sudoku.valid and not sudoku.full

            for k in range(1, 10):
                # Search an empty cell where we can put k numbers
                for cell in sudoku.empty_cells:
                     if len(cell.remaining_numbers) == k:
                         return cell

        # Sudoku must be a valid configuration
        assert sudoku.valid

        if sudoku.full:
            # Nothing to be done, already solved
            return
        # Find the next node and expand it
        cell = next_node()
        expand_node(cell)
