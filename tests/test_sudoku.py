


import unittest
from unittest import TestCase
import numpy as np
from sudoku import Sudoku, SudokuCell, SudokuSection
from itertools import product




class TestSudoku(TestCase):
    '''
    A bunch of test cases for Sudoku class methods and properties
    '''


    ### SudokuCell test cases

    def test_sudoku_cell_empty(self):
        '''
        The property 'empty' on SudokuCell returns True if the cell is empty and
        False otherwise
        '''
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertFalse((sudoku[i, j] == 0) ^ sudoku[i, j].empty)



    def test_sudoku_get_number(self):
        '''
        Accessing a single cell on the sudoku object via indexation, returns
        a SudokuCell instance
        '''
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertIn(sudoku[i, j], range(0, 10))
            self.assertIsInstance(sudoku[i, j], SudokuCell)


    def test_sudoku_cell_row_index(self):
        '''
        row_index property on SudokuCell returns the index of the sudoku row that contains
        the cell
        '''
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertEqual(i, sudoku[i, j].row_index)


    def test_sudoku_cell_column_index(self):
        '''
        col_index on SudokuCell returns the index of the sudoku column that contains the cell
        '''
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertEqual(j, sudoku[i, j].column_index)


    def test_sudoku_cell_square_index(self):
        '''
        square_index on SudokuCell returns the index of the sudoku square that contains the cell
        '''
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            k = (i // 3) * 3 + j // 3
            self.assertEqual(k, sudoku[i, j].square_index)


    def test_sudoku_set_number(self):
        '''
        We can assign a number to any sudoku cell via indexation, but number must be
        a integer value between 0 and 9 (0 for empty cell)
        '''
        sudoku = Sudoku()
        for i, j, num in product(range(0, 9), range(0, 9), range(1, 10)):
            sudoku[i, j] = num
            self.assertFalse(sudoku[i, j].empty)
            self.assertEqual(sudoku[i, j], num)
            self.assertRaises(Exception, sudoku.__setitem__, (i, j), -1)


    def test_sudoku_remove_number(self):
        '''
        We can use the operator del to remove single sudoku cells (clear them).
        '''
        sudoku = Sudoku()
        for i, j, num in product(range(0, 9), range(0, 9), range(1, 10)):
            sudoku[i, j] = num
            del sudoku[i, j]
            self.assertEqual(sudoku[i, j], 0)
            self.assertTrue(sudoku[i, j].empty)



    def test_sudoku_cell_remaining_numbers(self):
        '''
        'remaining_numbers' property on SudokuCell returns the numbers that we can assign
        to the cell such that any number is not repeated more than one time in its row, column
        or square.
        '''
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            cell = sudoku[i, j]
            if cell != 0:
                self.assertTrue(len(cell.remaining_numbers) == 0)
            else:
                self.assertEqual(
                    cell.row.remaining_numbers & cell.col.remaining_numbers & cell.square.remaining_numbers,
                    cell.remaining_numbers)




    ### SudokuSection test cases

    def test_sudoku_get_row(self):
        '''
        We can access sudoku rows by indexing the first dimension. __getitem__ will
        return an instance of the class SudokuSection. Rows can be also retrieved
        using sudoku.rows attribute.
        All sudoku rows are 1D vectors with 9 items
        '''
        sudoku = Sudoku()
        for i in range(0, 9):
            self.assertIsInstance(sudoku[i], SudokuSection)
            self.assertEqual(sudoku[i].ndim, 1)
            self.assertEqual(len(sudoku[i]), 9)

            self.assertIsInstance(sudoku.rows[i], SudokuSection)
            self.assertEqual(sudoku.rows[i].ndim, 1)
            self.assertEqual(sudoku.rows[i].size, 9)



    def test_sudoku_set_row(self):
        '''
        We can change the numbers of entire row of cells in the sudoku via indexation
        (__setitem__). We can assign a single number or a 1D vector of 9 numbers to any
        row (all numbers must be integers between 0 and 9)
        '''
        sudoku = Sudoku()
        for i, num in product(range(0, 9), range(1, 10)):
            sudoku[i] = num
            self.assertTrue(np.all(sudoku[i] == num))
            sudoku.rows[i] = 9-num
            self.assertTrue(np.all(sudoku.rows[i] == 9-num))

            sudoku[i] = range(1, 10)
            self.assertTrue(np.all(sudoku[i] == range(1, 10)))
            sudoku.rows[i] = range(9, 0, -1)
            self.assertTrue(np.all(sudoku.rows[i] == range(9, 0, -1)))

        for i in range(0, 9):
            for j in range(0, 9):
                self.assertRaises(Exception, sudoku[i].__setitem__, j, -1)
                self.assertRaises(Exception, sudoku.rows[i].__setitem__, j, -1)


    def test_sudoku_del_row(self):
        '''
        Any specific row on the sudoku could be removed: All the cells inside the row
        will be cleared (assigned to 0)
        '''
        sudoku = Sudoku()
        for i, num in product(range(0, 9), range(1, 10)):
            sudoku[i] = num
            del sudoku[i]
            self.assertTrue(np.all(sudoku[i] == 0))

            sudoku.rows[i] = num
            del sudoku.rows[i]
            self.assertTrue(np.all(sudoku.rows[i] == 0))


    def test_sudoku_get_column(self):
        '''
        Same as test_sudoku_get_row but for columns
        '''
        sudoku = Sudoku()
        for j in range(0, 9):
            self.assertIsInstance(sudoku[:, j], SudokuSection)
            self.assertEqual(sudoku[:, j].ndim, 1)
            self.assertEqual(len(sudoku[:, j]), 9)

            self.assertIsInstance(sudoku.columns[j], SudokuSection)
            self.assertEqual(sudoku.columns[j].ndim, 1)
            self.assertEqual(sudoku.columns[j].size, 9)


    def test_sudoku_set_column(self):
        '''
        Same as test_sudoku_set_row but for columns
        '''
        sudoku = Sudoku()
        for j, num in product(range(0, 9), range(1, 10)):
            sudoku[:, j] = num
            self.assertTrue(np.all(sudoku[:, j] == num))
            sudoku.columns[j] = 9-num
            self.assertTrue(np.all(sudoku.columns[j] == 9-num))

            sudoku[:, j] = range(1, 10)
            self.assertTrue(np.all(sudoku[:, j] == range(1, 10)))
            sudoku.columns[j] = range(9, 0, -1)
            self.assertTrue(np.all(sudoku.columns[j] == range(9, 0, -1)))

        for j in range(0, 9):
            for i in range(0, 9):
                self.assertRaises(Exception, sudoku[:, j].__setitem__, i, -1)
                self.assertRaises(Exception, sudoku.columns[j].__setitem__, i, -1)


    def test_sudoku_del_column(self):
        '''
        Same as test_sudoku_del_row but for columns
        '''
        sudoku = Sudoku()
        for j, num in product(range(0, 9), range(1, 10)):
            sudoku[:, j] = num
            del sudoku[:, j]
            self.assertTrue(np.all(sudoku[:, j] == 0))

            sudoku.columns[j] = num
            del sudoku.columns[j]
            self.assertTrue(np.all(sudoku.columns[j] == 0))


    def test_sudoku_get_square(self):
        '''
        Same as test_sudoku_get_row but for squares. The only difference is that
        squares are not 1D vectors. They will be 3x3 arrays
        '''
        sudoku = Sudoku()
        for k in range(0, 9):
            square = sudoku.squares[k]
            self.assertIsInstance(square, SudokuSection)
            self.assertEqual(square.ndim, 2)
            self.assertEqual(len(square.flatten()), 9)

        for y, x in product(range(0, 3), range(0, 3)):
            square = sudoku.squares[y, x]
            self.assertIsInstance(square, SudokuSection)
            self.assertEqual(square.ndim, 2)
            self.assertEqual(len(square.flatten()), 9)


    def test_sudoku_set_square(self):
        '''
        Same as test_sudoku_set_row but for squares
        '''
        sudoku = Sudoku()
        for k, num in product(range(0, 9), range(1, 10)):
            sudoku.squares[k] = num
            self.assertTrue(np.all(sudoku.squares[k].flatten() == num))

        for k in range(0, 9):
            sudoku.squares[k] = np.arange(1, 10).reshape(3, 3)
            self.assertTrue(np.all(sudoku.squares[k].flatten() == np.arange(1, 10)))

        for y, x in product(range(0, 3), range(0, 3)):
            sudoku.squares[y, x] = np.random.randint(9, size=9).reshape([3, 3]) + 1
            self.assertTrue(np.all(sudoku.squares[y, x].flatten() == sudoku.squares[y * 3 + x].flatten()))

        for k in range(0, 9):
            square = sudoku.squares[k]
            for y, x in product(range(0, 3), range(0, 3)):
                self.assertRaises(Exception, square.__setitem__, (y, x), -1)


    def test_sudoku_del_square(self):
        '''
        Same as test_sudoku_del_row but for squares
        '''
        sudoku = Sudoku()
        for k, num in product(range(0, 9), range(1, 10)):
            sudoku.squares[k] = num
            del sudoku.squares[k]
            self.assertTrue(np.all(sudoku.squares[k].flatten() == 0))



    def test_sudoku_section_empty_cells_count(self):
        '''
        'empty_cells_count' returns the number of empty cells in the section
        '''
        sudoku = Sudoku.random()
        for i in range(0, 9):
            row = sudoku[i]
            self.assertEqual(row.empty_cells_count, np.sum(row == 0))


    def test_sudoku_section_filled_cells_count(self):
        '''
        'filled_cells_count' returns the number of non empty cells in the section
        '''
        sudoku = Sudoku.random()
        for j in range(0, 9):
            col = sudoku[:, j]
            self.assertEqual(col.filled_cells_count, np.count_nonzero(col))
            self.assertEqual(col.filled_cells_count + col.empty_cells_count, col.size)


    def test_sudoku_section_empty(self):
        '''
        'empty' property returns True if there are only empty cells in this section
        '''
        sudoku = Sudoku()
        del sudoku.squares[0]
        self.assertTrue(sudoku.squares[0].empty)
        sudoku[0, 0] = 1
        self.assertFalse(sudoku.squares[0].empty)


    def test_sudoku_section_full(self):
        '''
        'full' property returns True if there are only non empty cells in this section
        '''
        sudoku = Sudoku()
        sudoku.squares[0] = (np.random.randint(9, size=9) + 1).reshape([3, 3])
        self.assertTrue(sudoku.squares[0].full)
        del sudoku.squares[0]
        self.assertFalse(sudoku.squares[0].full)


    def test_sudoku_section_clear(self):
        '''
        clear() method clears all the section cells
        '''
        sudoku = Sudoku()

        sudoku.squares[0] = np.arange(1, 10).reshape([3, 3])
        sudoku.squares[0].clear()
        self.assertTrue(sudoku.squares[0].empty)


    def test_sudoku_section_numbers(self):
        '''
        'numbers' property on SudokuSection returns a ndarray with all numbers
        of this sudoku section cells
        '''
        sudoku = Sudoku.random()
        for i in range(0, 9):
            row = sudoku[i]
            self.assertTrue(np.all(row[row != 0] == row.numbers))


    def test_sudoku_iter_row(self):
        '''
        Test we can iterate over the cells on each row using sudoku.rows[i].__iter__ or
        sudoku[i].__iter__
        '''
        sudoku = Sudoku.random()
        for i in range(0, 9):
            self.assertEqual(list(sudoku[i]), list(sudoku[i].view(type=np.ndarray)))
            self.assertEqual(list(sudoku.rows[i]), list(sudoku[i].view(type=np.ndarray)))


        for i, row in zip(range(0, 9), sudoku.rows):
            self.assertEqual(list(sudoku.rows[i]), list(row))


    def test_sudoku_iter_column(self):
        '''
        Same as test_sudoku_iter_row but for columns
        '''
        sudoku = Sudoku.random()
        for j in range(0, 9):
            self.assertEqual(list(sudoku[:, j]), list(sudoku[:, j].view(type=np.ndarray)))
            self.assertEqual(list(sudoku.columns[j]), list(sudoku[:, j].view(type=np.ndarray)))

        for j, col in zip(range(0, 9), sudoku.columns):
            self.assertEqual(list(sudoku.columns[j]), list(col))


    def test_sudoku_iter_square(self):
        '''
        Same as test_sudoku_iter_row but for squares
        '''
        sudoku = Sudoku.random()

        for k, square in zip(range(0, 9), sudoku.squares):
            self.assertEqual(list(square), list(sudoku.squares[k].view(type=np.ndarray).flatten()))





    ### Sudoku class test cases

    def test_sudoku_copy(self):
        '''
        copy() creates a independent copy of the sudoku configuration
        '''
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            sudoku[i, j] = (i * 9 + j) % 9 + 1
        other = sudoku.copy()
        sudoku.clear()
        self.assertTrue(np.all(sudoku != other))


    def test_sudoku_init_values(self):
        '''
        By default, Sudoku() returns a configuration where all the cells are empty
        '''
        sudoku = Sudoku()
        self.assertTrue(np.all(sudoku.flatten() == np.zeros([9, 9]).flatten()))




    def test_sudoku_valid(self):
        '''
        Sudoku.valid property returns True if the sudoku configuration is valid.
        '''
        sudoku = Sudoku()
        sudoku.clear()
        self.assertTrue(sudoku.valid)
        sudoku.rows[0] = 1
        self.assertFalse(sudoku.valid)

        sudoku = Sudoku([
            [7, 9, 2, 5, 1, 8, 3, 4, 6],
            [8, 6, 3, 7, 4, 0, 9, 1, 5],
            [1, 5, 4, 9, 3, 6, 2, 7, 8],
            [9, 8, 6, 3, 5, 7, 1, 2, 4],
            [3, 7, 0, 2, 6, 4, 8, 5, 9],
            [4, 2, 5, 8, 9, 1, 7, 6, 3],
            [6, 3, 9, 1, 2, 5, 0, 8, 7],
            [2, 4, 8, 6, 7, 0, 5, 3, 1],
            [5, 1, 7, 4, 8, 3, 6, 9, 2]
        ])
        self.assertTrue(sudoku.valid)


    def test_sudoku_solved(self):
        '''
        Sudoku.solved property is True when the sudoku configuration represents a valid
        sudoku solution
        '''
        a = Sudoku([
            [7, 9, 2, 5, 1, 8, 3, 4, 6],
            [8, 6, 3, 7, 4, 2, 9, 1, 5],
            [1, 5, 4, 9, 3, 6, 2, 7, 8],
            [9, 8, 6, 3, 5, 7, 1, 2, 4],
            [3, 7, 1, 2, 6, 4, 8, 5, 9],
            [4, 2, 5, 8, 9, 1, 7, 6, 3],
            [6, 3, 9, 1, 2, 5, 4, 8, 7],
            [2, 4, 8, 6, 7, 9, 5, 3, 1],
            [5, 1, 7, 4, 8, 3, 6, 9, 2]
        ])
        self.assertTrue(a.solved)

        b = a.copy()
        del b.squares[1, 1]
        self.assertFalse(b.solved)


    def test_sudoku_fromstring(self):
        '''
        Test we can import a sudoku configuration from a string using class method 'fromstring'
        '''
        a = Sudoku.random()
        b = Sudoku.fromstring(', '.join(map(str, a.view(type=np.ndarray).flatten())))
        self.assertTrue(np.all(a.view(type=np.ndarray) == b.view(type=np.ndarray)))


    def test_sudoku_lower_than(self):
        '''
        Test the operator < and > on Sudoku class.
        '''
        a = Sudoku.random()
        b = a.copy()
        self.assertFalse(b < a)
        self.assertFalse(a < b)
        self.assertFalse(a > b)
        self.assertFalse(b > a)

        for i, j in product(range(0, 9), range(0, 9)):
            if a[i, j].empty:
                b[i, j] = 1
                self.assertTrue(a < b)
                self.assertTrue(b > a)
                del b[i, j]
            else:
                del b[i, j]
                self.assertTrue(b < a)
                self.assertTrue(a > b)
                b[i, j] = a[i, j]
        

if __name__ == '__main__':
    unittest.main()
