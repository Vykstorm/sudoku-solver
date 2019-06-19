


import unittest
from unittest import TestCase
import numpy as np
from sudoku import Sudoku, SudokuCell, SudokuSection
from itertools import product




class TestSudoku(TestCase):

    def test_sudoku_get_number(self):
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertIn(sudoku[i, j], range(0, 10))
            self.assertIsInstance(sudoku[i, j], SudokuCell)


    def test_sudoku_set_number(self):
        sudoku = Sudoku()
        for i, j, num in product(range(0, 9), range(0, 9), range(1, 10)):
            sudoku[i, j] = num
            self.assertEqual(sudoku[i, j], num)
            self.assertRaises(Exception, sudoku.__setitem__, (i, j), -1)


    def test_sudoku_remove_number(self):
        '''
        Test we can clear a specific sudoku cell using the statement del
        (its the same as assigning the number 0 to the cell)
        '''
        sudoku = Sudoku()
        for i, j, num in product(range(0, 9), range(0, 9), range(1, 10)):
            sudoku[i, j] = num
            del sudoku[i, j]
            self.assertEqual(sudoku[i, j], 0)


    def test_sudoku_get_row(self):
        sudoku = Sudoku()
        for i in range(0, 9):
            self.assertIsInstance(sudoku[i], SudokuSection)
            self.assertEqual(sudoku[i].ndim, 1)
            self.assertEqual(len(sudoku[i]), 9)


    def test_sudoku_set_row(self):
        sudoku = Sudoku()
        for i, num in product(range(0, 9), range(1, 10)):
            sudoku[i] = num
            self.assertTrue(np.all(sudoku[i] == num))

            sudoku[i] = range(1, 10)
            self.assertTrue(np.all(sudoku[i] == range(1, 10)))

        for i in range(0, 9):
            row = sudoku[i]
            for j in range(0, 9):
                self.assertRaises(Exception, row.__setitem__, j, -1)


    def test_sudoku_del_row(self):
        sudoku = Sudoku()
        for i, num in product(range(0, 9), range(1, 10)):
            sudoku[i] = num
            del sudoku[i]
            self.assertTrue(np.all(sudoku[i] == 0))


    def test_sudoku_get_column(self):
        sudoku = Sudoku()
        for j in range(0, 9):
            self.assertIsInstance(sudoku[:, j], SudokuSection)
            self.assertEqual(sudoku[:, j].ndim, 1)
            self.assertEqual(len(sudoku[:, j]), 9)


    def test_sudoku_set_column(self):
        sudoku = Sudoku()
        for j, num in product(range(0, 9), range(1, 10)):
            sudoku[:, j] = num
            self.assertTrue(np.all(sudoku[:, j] == num))

            sudoku[:, j] = range(1, 10)
            self.assertTrue(np.all(sudoku[:, j] == range(1, 10)))

        for j in range(0, 9):
            col = sudoku[:, j]
            for i in range(0, 9):
                self.assertRaises(Exception, col.__setitem__, i, -1)


    def test_sudoku_del_column(self):
        sudoku = Sudoku()
        for j, num in product(range(0, 9), range(1, 10)):
            sudoku[:, j] = num
            del sudoku[:, j]
            self.assertTrue(np.all(sudoku[:, j] == 0))


    def test_sudoku_copy(self):
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            sudoku[i, j] = (i * 9 + j) % 9 + 1
        other = sudoku.copy()
        sudoku.clear()
        self.assertTrue(np.all(sudoku != other))


    def test_sudoku_get_square(self):
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
        sudoku = Sudoku()
        for k, num in product(range(0, 9), range(1, 10)):
            sudoku.squares[k] = num
            del sudoku.squares[k]
            self.assertTrue(np.all(sudoku.squares[k].flatten() == 0))


    def test_sudoku_init_values(self):
        sudoku = Sudoku()
        self.assertTrue(np.all(sudoku.flatten() == np.zeros([9, 9]).flatten()))


    def test_sudoku_cell_empty(self):
        sudoku = Sudoku.random()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertFalse((sudoku[i, j] == 0) ^ sudoku[i, j].empty)


    def test_sudoku_section_empty_cells_count(self):
        sudoku = Sudoku.random()
        for i in range(0, 9):
            row = sudoku[i]
            self.assertEqual(row.empty_cells_count, np.sum(row == 0))


    def test_sudoku_section_filled_cells_count(self):
        sudoku = Sudoku.random()
        for j in range(0, 9):
            col = sudoku[:, j]
            self.assertEqual(col.filled_cells_count, np.count_nonzero(col))
            self.assertEqual(col.filled_cells_count + col.empty_cells_count, col.size)


    def test_sudoku_section_empty(self):
        sudoku = Sudoku()
        del sudoku.squares[0]
        self.assertTrue(sudoku.squares[0].empty)
        sudoku[0, 0] = 1
        self.assertFalse(sudoku.squares[0].empty)


    def test_sudoku_section_full(self):
        sudoku = Sudoku()
        sudoku.squares[0] = (np.random.randint(9, size=9) + 1).reshape([3, 3])
        self.assertTrue(sudoku.squares[0].full)
        del sudoku.squares[0]
        self.assertFalse(sudoku.squares[0].full)


    def test_sudoku_section_clear(self):
        sudoku = Sudoku()

        sudoku.squares[0] = np.arange(1, 10).reshape([3, 3])
        sudoku.squares[0].clear()
        self.assertTrue(sudoku.squares[0].empty)


    def test_sudoku_section_unique_numbers(self):
        sudoku = Sudoku.random()
        for i in range(0, 9):
            row = sudoku[i]
            self.assertTrue(frozenset(row.unique_numbers).issubset(frozenset(row)))
            self.assertFalse(0 in row.unique_numbers)


if __name__ == '__main__':
    unittest.main()
