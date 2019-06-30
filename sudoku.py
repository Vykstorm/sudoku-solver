'''
This module creates the helper class Sudoku which can be used to represent any arbitrary sudoku
game configuration
'''



### Import statements
import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from itertools import product
from functools import partial, reduce
import collections.abc
import re
import operator
from visualization import SudokuPlot



### Helper classes
class ListIndexParser:
    def __init__(self, n):
        self.n = n

    def parse(self, index):
        assert hasattr(index, '__int__')

        index = int(index)

        if index < 0:
            index = self.n + index

        if index < 0 or index >= self.n:
            raise IndexError('Index out of bounds')

        return index


class SudokuRowIndexParser(ListIndexParser):
    def __init__(self):
        super().__init__(9)

    def parse(self, index):
        return super().parse(index), slice(None)


class SudokuColumnIndexParser(ListIndexParser):
    def __init__(self):
        super().__init__(9)

    def parse(self, index):
        return slice(None), super().parse(index)


class SudokuSquareIndexParser(ListIndexParser):
    def __init__(self):
        super().__init__(9)

    def parse(self, index):
        assert hasattr(index, '__int__') or (isinstance(index, tuple) and len(index) == 2 and all(map(lambda x: hasattr(x, '__int__'), index)))

        if hasattr(index, '__int__'):
            index = super().parse(index)
            y, x = index // 3, index % 3
        else:
            y, x = map(ListIndexParser(3).parse, index)

        return slice(y*3, (y+1)*3), slice(x*3, (x+1)*3)





class SudokuCell:
    '''
    Instances of this class represents a single cell of an arbitrary sudoku configuration.
    '''
    def __init__(self, sudoku, index):
        self._sudoku, self._index = sudoku, index

    @property
    def value(self):
        return int(self._sudoku.view(type=np.ndarray).flatten().__getitem__(self._index))

    @value.setter
    def value(self, num):
        assert num in range(0, 10)
        self._sudoku.view(type=np.ndarray).put(self._index, num)

    @value.deleter
    def value(self):
        self.value = 0

    def clear(self):
        self.value = 0


    def __int__(self):
        return self.value

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other



    @property
    def empty(self):
        '''
        Returns True if this cell is empty (its the same as comparing its value to zero)
        '''
        return self.value == 0


    @property
    def index(self):
        return self._index


    @property
    def row_index(self):
        '''
        Returns the index of the row where this cell is located inside the sudoku
        '''
        return self._index // 9

    @property
    def column_index(self):
        '''
        Returns the index of the column where this cell is located inside the sudoku
        '''
        return self._index % 9

    col_index = column_index

    @property
    def square_index(self):
        '''
        Returns the index of the square where this cell is located inside the sudoku
        '''
        return (self.row_index // 3) * 3 + self.column_index // 3

    @property
    def row(self):
        '''
        Returns the sudoku row that contains this cell
        '''
        return self._sudoku.rows[self.row_index]

    @property
    def column(self):
        '''
        Returns the sudoku column that contains this cell
        '''
        return self._sudoku.columns[self.column_index]

    col = column

    @property
    def square(self):
        '''
        Returns the sudoku square that contains this cell
        '''
        return self._sudoku.squares[self.square_index]


    @property
    def valid(self):
        '''
        Check if this cell is valid:
        If this is a empty cell, returns True if we can put at least 1 number in this cell
        without repeating it in its row, column or square.
        Otherwise, its valid only if the number written on this cell is not repeated in its row,
        column or square
        '''
        if self == 0:
            return len(self.remaining_numbers) > 0
        return all(map(lambda unit: unit.count(self) == 1, [self.row, self.column, self.square]))


    @property
    def remaining_numbers(self):
        '''
        If this cell is not empty, returns an empty frozenset. Otherwise, it returns all the numbers not
        present in the row, column or square containing this cell as a frozenset instance
        '''
        if self != 0:
            return frozenset()
        return reduce(operator.__and__, map(lambda unit: unit.remaining_numbers, [self.row, self.column, self.square]))


    def __str__(self):
        return '' if self.empty else str(int(self))

    def __repr__(self):
        return str(self)



class SudokuSection(np.ndarray):
    '''
    Objects of this class are subarray of cells of an arbitrary sudoku configuration
    '''
    def __new__(cls, sudoku, indices, values=None):
        if values is None:
            values = sudoku
        return values.view(type=SudokuSection)

    def __init__(self, sudoku, indices, values=None):
        self._sudoku, self._indices = sudoku, indices


    def __getitem__(self, item):
        values = self.view(type=np.ndarray).__getitem__(item)
        indices = self._indices.__getitem__(item)
        if isinstance(indices, np.ndarray):
            return SudokuSection(self._sudoku, indices, values)
        return SudokuCell(self._sudoku, indices)


    def __setitem__(self, item, value):
        if __debug__:
            if isinstance(value, int):
                assert value in range(0, 10)

            value = np.array(value, dtype=np.uint8)
            assert np.all(np.isin(value.flatten(), range(0, 10)))

        super().__setitem__(item, value)


    def __delitem__(self, item):
        super().__setitem__(item, 0)

    def __iter__(self):
        return map(partial(SudokuCell, self._sudoku), self._indices.flatten())


    def clear(self):
        '''
        Clear all the sudoku cells inside this section (set their values to 0)
        '''
        self.fill(0)


    def flatten(self):
        '''
        Returns a flattened version of this sudoku section
        '''
        if self.ndim == 1:
            return self
        return SudokuSection(self._sudoku, self._indices.flatten(), self.view(type=np.ndarray).flatten())


    @property
    def empty_cells_count(self):
        '''
        Returns the number of empty cells on this sudoku section
        '''
        return self.size - self.filled_cells_count


    @property
    def filled_cells_count(self):
        '''
        Return the number of non empty cells on this sudoku section
        '''
        return np.count_nonzero(self)


    @property
    def empty_cells(self):
        '''
        Returns all the empty cells on this section
        '''
        return self[self.view(type=np.ndarray) == 0]


    @property
    def filled_cells(self):
        '''
        Returns all non empty cells on this section
        '''
        return self[self.view(type=np.ndarray) != 0]


    @property
    def empty(self):
        '''
        Returns True if all the cells in this sudoku section are empty
        '''
        return self.filled_cells_count == 0


    @property
    def full(self):
        '''
        Returns True if all the cells in this sudoku section are not empty
        '''
        return self.empty_cells_count == 0


    def count(self, num):
        '''
        Count the number of times the given number appears on this sudoku section
        '''
        return np.count_nonzero(self == num)


    @property
    def numbers(self):
        '''
        Returns all the numbers in this sudoku section
        '''
        cells = self.view(type=np.ndarray).flatten()
        return cells[cells > 0]


    @property
    def unique_numbers(self):
        '''
        Returns all the numbers (removing repetitions) in this sudoku section
        '''
        return frozenset(self.numbers)


    @property
    def remaining_numbers(self):
        '''
        Returns all the numbers that doesnt appear in this sudoku section
        '''
        return frozenset(range(1, 10)) - self.unique_numbers





class Sudoku(SudokuSection):
    '''
    Objects of this class represents a specific configuration for a sudoku grid.
    Its a matrix of size 9x9 of positive integer values in the range [0, 9].
    A zero will indicate that the cell is empty.

    The first dimension of the array are for rows. The second dimension stands for
    columns
    sudoku[i, j] will be the cell at the ith row and jth column
    '''

    class UnitsView:
        def __init__(self, sudoku, index_parser):
            self.sudoku, self.index_parser = sudoku, index_parser

        def __getitem__(self, index):
            index = self.index_parser.parse(index)
            return SudokuSection(
                self.sudoku,
                self.sudoku._indices.__getitem__(index),
                self.sudoku.view(type=np.ndarray).__getitem__(index)
            )

        def __setitem__(self, index, value):
            self.sudoku.__setitem__(self.index_parser.parse(index), value)

        def __delitem__(self, index):
            self.sudoku.__delitem__(self.index_parser.parse(index))

        def __len__(self):
            return 9

        def __iter__(self):
            for i in range(0, len(self)):
                yield self[i]


    SquaresView = partial(UnitsView, index_parser=SudokuSquareIndexParser())
    RowsView = partial(UnitsView, index_parser=SudokuRowIndexParser())
    ColumnsView = partial(UnitsView, index_parser=SudokuColumnIndexParser())



    def __new__(cls, values=None):
        if values is None or not isinstance(values, Sudoku):
            sudoku = np.zeros(shape=(9, 9), dtype=np.uint8).view(type=Sudoku)
            if values is not None:
                np.put(sudoku, np.arange(0, 81), values)
            return sudoku
        return np.array(values, copy=True, subok=True)


    indices = np.arange(0, 81).reshape([9, 9])
    def __init__(self, values=None):
        super().__init__(self, indices=self.indices)
        self.squares = self.SquaresView(self)
        self.rows = self.RowsView(self)
        self.columns = self.cols = self.ColumnsView(self)



    @classmethod
    def random(cls):
        '''
        This method returns a sudoku with some of its cells filled randomly with
        numbers and the rest are left empty (this is used for testing purposes)
        '''
        nums = ((np.random.randint(9, size=81) + 1) * (np.random.random(81) >= 0.4)).reshape([9, 9])
        return Sudoku(nums)


    @classmethod
    def fromstring(cls, s):
        '''
        Creates a sudoku configuration from a string. The string must be a sequence of 81
        integer values separated by spaces, carriage returns tabs or commas.

        '''
        return Sudoku(np.fromstring(re.sub('[\n\t, ]+', '-', s), sep='-', dtype=np.uint8).reshape([9, 9]))


    @classmethod
    def fromfile(cls, path):
        '''
        Its the same as
        with open(path, 'r') as file:
            return Sudoku.fromstring(file.read())
        '''
        with open(path, 'r') as f:
            return cls.fromstring(f.read())


    def copy(self):
        '''
        Make a copy of this sudoku; return another sudoku instance with the same values
        '''
        return Sudoku(self)


    @property
    def valid(self):
        '''
        Returns True if this instance is a valid sudoku configuration. It is valid if
        all its cells are valid (check SudokuCell.valid docs)
        '''
        return all([cell.valid for cell in self])


    @property
    def solved(self):
        '''
        Returns True if the sudoku is solved. It is considered solved if its a valid
        configuration (valid is True) and all its cells are filled
        '''
        return self.full and self.valid


    def __lt__(self, other):
        if not isinstance(other, Sudoku):
            raise ValueError()

        a, b = self.view(type=np.ndarray), other.view(type=np.ndarray)
        return self.empty_cells_count > other.empty_cells_count and\
            np.all(np.logical_or(a == 0, a == b))

    def __gt__(self, other):
        if not isinstance(other, Sudoku):
            raise ValueError()
        return other < self

    def __eq__(self, other):
        return np.all(self.view(type=np.ndarray) == other.view(type=np.ndarray))

    def __ne__(self, other):
        return np.any(self.view(type=np.ndarray) != other.view(type=np.ndarray))


    @property
    def plot(self):
        return SudokuPlot(self)


    def draw(self, *args, **kwargs):
        '''
        Its an alias of plot.draw()
        '''
        return self.plot.draw(*args, **kwargs)


    def show(self, figsize=None):
        '''
        Shows this sudoku on a new matplotlib figure
        '''
        if figsize is None:
            figsize = (5, 5)
        plt.figure(figsize=figsize)
        self.draw()
        plt.show()


    def __str__(self):
        '''
        Returns a string that can be used to print the sudoku on stdout
        '''
        s = ''

        s += '\u23af' * 25 + '\n'
        for i in range(0, 9):
            s += '\uff5c'
            for j in range(0, 9):
                s += (str(self[i, j]) if self[i, j] != 0 else ' ') + ' '
                if (j+1)%3  == 0:
                    s += '\uff5c'
            s += '\n'
            if (i+1)%3 == 0:
                s += '\u23af' * 25 + '\n'
        return s


    def __repr__(self):
        '''
        Same as str
        '''
        return self.__str__()
