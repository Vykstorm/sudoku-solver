


import unittest
from unittest import TestCase
import numpy as np
from sudoku import Sudoku
from itertools import product




class TestSudoku(TestCase):

    def test_sudoku_get_number(self):
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            self.assertIn(sudoku[i, j], range(0, 10))


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
            self.assertIsInstance(sudoku[i], np.ndarray)
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
            self.assertIsInstance(sudoku[:, j], np.ndarray)
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


    def test_sudoku_clear(self):
        sudoku = Sudoku()
        for i, j in product(range(0, 9), range(0, 9)):
            sudoku[i, j] = (i * 9 + j) % 9 + 1
        sudoku.clear()
        self.assertTrue(np.all(sudoku == 0))


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
            self.assertIsInstance(square, np.ndarray)
            self.assertEqual(square.ndim, 2)
            self.assertEqual(len(square.flatten()), 9)

        for y, x in product(range(0, 3), range(0, 3)):
            square = sudoku.squares[y, x]
            self.assertIsInstance(square, np.ndarray)
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


if __name__ == '__main__':
    unittest.main()
