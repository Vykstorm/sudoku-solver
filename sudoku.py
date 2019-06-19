

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from itertools import product
import collections.abc


def check_value(value):
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
        raise ValueError('All numbers in a sudoku are between 0 and 9 (0 indicates an empty cell)')




class SudokuSection(np.ndarray):
    def __new__(cls, section):
        return section.view(type=SudokuSection)


    def __getitem__(self, item):
        value = self.view(type=np.ndarray).__getitem__(item)
        if not isinstance(value, np.ndarray):
            return value
        return SudokuSection(value)


    def __setitem__(self, item, value):
        check_value(value)
        super().__setitem__(item, value)


    def __delitem__(self, item):
        super().__setitem__(item, 0)


    def clear(self):
        self.fill(0)



class Sudoku(SudokuSection):
    '''
    Objects of this class represents a specific configuration for a sudoku grid.
    Its a matrix of size 9x9 of positive integer values in the range [0, 9].
    A zero will indicate that the cell is empty.

    The first dimension of the array are for rows. The second dimension stands for
    columns
    sudoku[i, j] will be the cell at the ith row and jth column
    '''

    class SquaresView:
        def __init__(self, sudoku):
            self.sudoku = sudoku


        def _get_indices(self, item):
            try:
                if isinstance(item, tuple):
                    if len(item) != 2:
                        raise IndexError()
                    y, x = item
                else:
                    if not isinstance(item, int):
                        raise IndexError()
                    y, x = item // 3, item % 3

                if y not in range(0, 3) or x not in range(0, 3):
                    raise IndexError()

                return slice(y*3, (y+1)*3), slice(x*3, (x+1)*3)
            except IndexError:
                raise IndexError(
                    'You must pass a number in the range [0, 9) or '+
                    'a pair of numbers in the range [0, 3)')

        def __getitem__(self, item):
            return self.sudoku.__getitem__(self._get_indices(item))

        def __setitem__(self, item, value):
            self.sudoku.__setitem__(self._get_indices(item), value)

        def __delitem__(self, item):
            self.__getitem__(item).fill(0)



    def __new__(cls, values=None):
        return np.zeros(shape=(9, 9), dtype=np.uint8).view(type=Sudoku)

    def __init__(self):
        super().__init__()
        self.squares = self.SquaresView(self)


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
