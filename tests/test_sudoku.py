


import unittest
from unittest import TestCase
import numpy as np
from sudoku import Sudoku, SudokuCell, SudokuSection, SudokuUnit
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
            self.assertFalse(sudoku[i, j].empty)
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
            self.assertTrue(sudoku[i, j].empty)


    def test_sudoku_get_row(self):
        sudoku = Sudoku()
        for i in range(0, 9):
            self.assertIsInstance(sudoku[i], SudokuSection)
            self.assertEqual(sudoku[i].ndim, 1)
            self.assertEqual(len(sudoku[i]), 9)

            self.assertIsInstance(sudoku.rows[i], SudokuUnit)
            self.assertEqual(sudoku.rows[i].ndim, 1)
            self.assertEqual(sudoku.rows[i].size, 9)



    def test_sudoku_set_row(self):
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
        sudoku = Sudoku()
        for i, num in product(range(0, 9), range(1, 10)):
            sudoku[i] = num
            del sudoku[i]
            self.assertTrue(np.all(sudoku[i] == 0))

            sudoku.rows[i] = num
            del sudoku.rows[i]
            self.assertTrue(np.all(sudoku.rows[i] == 0))


    def test_sudoku_get_column(self):
        sudoku = Sudoku()
        for j in range(0, 9):
            self.assertIsInstance(sudoku[:, j], SudokuSection)
            self.assertEqual(sudoku[:, j].ndim, 1)
            self.assertEqual(len(sudoku[:, j]), 9)

            self.assertIsInstance(sudoku.columns[j], SudokuUnit)
            self.assertEqual(sudoku.columns[j].ndim, 1)
            self.assertEqual(sudoku.columns[j].size, 9)


    def test_sudoku_set_column(self):
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
        sudoku = Sudoku()
        for j, num in product(range(0, 9), range(1, 10)):
            sudoku[:, j] = num
            del sudoku[:, j]
            self.assertTrue(np.all(sudoku[:, j] == 0))

            sudoku.columns[j] = num
            del sudoku.columns[j]
            self.assertTrue(np.all(sudoku.columns[j] == 0))


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
            self.assertIsInstance(square, SudokuUnit)
            self.assertEqual(square.ndim, 2)
            self.assertEqual(len(square.flatten()), 9)

        for y, x in product(range(0, 3), range(0, 3)):
            square = sudoku.squares[y, x]
            self.assertIsInstance(square, SudokuUnit)
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


    def test_sudoku_section_numbers(self):
        sudoku = Sudoku.random()
        for i in range(0, 9):
            row = sudoku[i]
            self.assertTrue(np.all(row[row != 0] == row.numbers))


    def test_sudoku_section_unique_numbers(self):
        sudoku = Sudoku.random()
        for i in range(0, 9):
            self.assertTrue(np.all(np.unique(sudoku[i].numbers) == sudoku[i].unique_numbers))


    def test_sudoku_unit_valid(self):
        sudoku = Sudoku()
        for i in range(0, 9):
            square = sudoku.squares[i]
            square[:] = 1
            self.assertFalse(square.valid)
            square[:] = np.arange(1, 10).reshape([3, 3])
            self.assertTrue(square.valid)


    def test_sudoku_valid(self):
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
        a = Sudoku.random()
        b = Sudoku.fromstring(', '.join(map(str, a.view(type=np.ndarray).flatten())))
        self.assertTrue(np.all(a.view(type=np.ndarray) == b.view(type=np.ndarray)))

if __name__ == '__main__':
    unittest.main()
