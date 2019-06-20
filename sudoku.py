

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from itertools import product
from functools import partial
import collections.abc




class ListIndexParser:
    def __init__(self, n):
        self.n = n

    def parse(self, index):
        if not isinstance(index, int):
            raise IndexError('Index must be an integer')

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
        if not isinstance(index, int) and (not isinstance(index, tuple) or len(index) != 2 or not all(map(lambda x: isinstance(x, int), index))):
            raise IndexError('Index must be an integer or a tuple of two integers')

        if isinstance(index, int):
            index = super().parse(index)
            y, x = index // 3, index % 3
        else:
            y, x = map(ListIndexParser(3).parse, index)

        return slice(y*3, (y+1)*3), slice(x*3, (x+1)*3)





class SudokuCell(np.uint8):
    '''
    Instances of this class represents a single cell of an arbitrary sudoku configuration
    '''
    def __new__(cls, value):
        return super(SudokuCell, cls).__new__(cls, value)


    @property
    def empty(self):
        '''
        Returns True if this cell is empty (its the same as comparing it to zero)
        '''
        return self == 0




class SudokuSection(np.ndarray):
    '''
    Objects of this class are subarray of cells of an arbitrary sudoku configuration
    '''
    def __new__(cls, values):
        return values.view(type=SudokuSection)


    def __getitem__(self, item):
        value = self.view(type=np.ndarray).__getitem__(item)
        return SudokuSection(value) if isinstance(value, np.ndarray) else SudokuCell(value)


    def __setitem__(self, item, value):
        def _check_value():
            try:
                if isinstance(value, np.ndarray):
                    if not np.all(np.isin(value.flatten(), range(0, 10))):
                        raise ValueError()
                elif isinstance(value, collections.abc.Iterable):
                    if any(map(lambda x: x not in range(0, 10), value)):
                        raise ValueError()
                elif value not in range(0, 10):
                    raise ValueError()
            except ValueError:
                raise ValueError('All numbers in a sudoku must be between 0 and 9 (0 indicates an empty cell)')

        _check_value()
        super().__setitem__(item, value)


    def __delitem__(self, item):
        super().__setitem__(item, 0)


    def clear(self):
        self.fill(0)


    @property
    def empty_cells_count(self):
        return self.size - self.filled_cells_count


    @property
    def filled_cells_count(self):
        return np.count_nonzero(self)


    @property
    def empty(self):
        return self.filled_cells_count == 0


    @property
    def full(self):
        return self.empty_cells_count == 0


    @property
    def numbers(self):
        cells = self.view(type=np.ndarray).flatten()
        return cells[cells > 0]


    @property
    def unique_numbers(self):
        return np.unique(self.numbers)




class SudokuUnit(SudokuSection):
    '''
    An object of this class represent a single row, column or square of an
    arbitrary sudoku configuration (all of them have a fixed size of 9 numbers)
    '''
    def __new__(cls, values):
        return values.view(type=SudokuUnit)


    @property
    def valid(self):
        return len(self.unique_numbers) == 9





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
            return SudokuUnit(self.sudoku.view(type=np.ndarray).__getitem__(self.index_parser.parse(index)))

        def __setitem__(self, index, value):
            self.sudoku.__setitem__(self.index_parser.parse(index), value)

        def __delitem__(self, index):
            self.sudoku.__delitem__(self.index_parser.parse(index))


    SquaresView = partial(UnitsView, index_parser=SudokuSquareIndexParser())
    RowsView = partial(UnitsView, index_parser=SudokuRowIndexParser())
    ColumnsView = partial(UnitsView, index_parser=SudokuColumnIndexParser())



    def __new__(cls, values=None):
        return np.zeros(shape=(9, 9), dtype=np.uint8).view(type=Sudoku)

    def __init__(self):
        super().__init__()
        self.squares = self.SquaresView(self)
        self.rows = self.RowsView(self)
        self.columns = self.cols = self.ColumnsView(self)


    @classmethod
    def random(cls):
        '''
        This method returns a sudoku with some of its cells filled randomly with
        numbers and the rest are left empty (this is used for testing purposes)
        '''
        nums = (np.random.randint(9, size=81) + 1) * (np.random.random(81) >= 0.4)
        sudoku = Sudoku()
        sudoku[:] = nums.reshape([9, 9])
        return sudoku


    def copy(self):
        '''
        Make a copy of this sudoku; return another sudoku instance with the same values
        '''
        return np.copy(self).view(type=Sudoku)




    def show(self):
        '''
        Shows the sudoku on a matplotlib figure
        '''
        plt.figure(figsize=(5, 5))


        column_separators = LineCollection(
            [[(j, 0), (j, 9)] for j in range(1, 9) if j%3 != 0],
            linewidths=1, colors='black', linestyle='solid')

        row_separators = LineCollection(
            [[(0, i), (9, i)] for i in range(1, 9) if i%3 != 0],
            linewidths=1, colors='black', linestyle='solid')

        vertical_square_separators = LineCollection(
            [[(j, 0), (j, 9)] for j in range(0, 10) if j%3 == 0],
            linewidths=2, colors='black', linestyle='solid')

        horizontal_square_separators = LineCollection(
            [[(0, i), (9, i)] for i in range(0, 10) if i%3 == 0],
            linewidths=2, colors='black', linestyle='solid')


        ax = plt.gca()
        for collection in (column_separators, row_separators, vertical_square_separators, horizontal_square_separators):
            ax.add_collection(collection)


        for i, j in product(range(0, 9), range(0, 9)):
            if self[i, j] != 0:
                valid = True

                valid = not((self[i] == self[i, j]).sum() > 1 or (self[:, j] == self[i, j]).sum() > 1 or\
                            (self[(i//3)*3:(i//3+1)*3, (j//3)*3:(j//3+1)*3] == self[i, j]).sum() > 1)

                ax.text(
                    j+0.5, 9-i-1+0.5, str(self[i, j]), horizontalalignment='center', verticalalignment='center',
                    fontsize='xx-large', color='black' if valid else 'red')

        plt.xlim([0, 9])
        plt.ylim([0, 9])
        plt.xticks([])
        plt.yticks([])

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
