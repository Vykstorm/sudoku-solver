
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from itertools import product


class SudokuPlot:
    '''
    This class can be used to visualize a sudoku configuration using the matplotlib library
    '''

    def __init__(self, sudoku):
        '''
        Constructor.
        :param sudoku: Must be the sudoku configuration to visualize
        '''
        self.sudoku = sudoku

    @classmethod
    def draw_grid(self):
        '''
        Draws the grid of the sudoku (column, row and square line separators)
        '''
        ax = plt.gca()

        column_separators = LineCollection(
            [[(j, 0), (j, 9)] for j in range(1, 9) if j%3 != 0],
            linewidths=1, colors='black', linestyle='solid')
        ax.add_collection(column_separators)

        row_separators = LineCollection(
            [[(0, i), (9, i)] for i in range(1, 9) if i%3 != 0],
            linewidths=1, colors='black', linestyle='solid')
        ax.add_collection(row_separators)

        vertical_square_separators = LineCollection(
            [[(j, 0), (j, 9)] for j in range(0, 10) if j%3 == 0],
            linewidths=2, colors='black', linestyle='solid')
        ax.add_collection(vertical_square_separators)

        horizontal_square_separators = LineCollection(
            [[(0, i), (9, i)] for i in range(0, 10) if i%3 == 0],
            linewidths=2, colors='black', linestyle='solid')
        ax.add_collection(horizontal_square_separators)

        plt.xlim([0, 9])
        plt.ylim([0, 9])
        plt.xticks([])
        plt.yticks([])



    def draw_numbers(self, highlight_invalid_numbers=True):
        '''
        Draws the numbers of the sudoku
        :param highlight_invalid_numbers: If True, highlight invalid numbers
        :return Return a numpy array of size 8x8 where the element at position (i, j) is a
        matplotlib Text class instance (Artist) used to display the label of the number inside
        the cell at row i and column j
        '''
        labels = np.array([
            plt.text(k % 9 + 0.5, 8 - k // 9 + 0.5, str(cell), horizontalalignment='center', verticalalignment='center',
                fontsize='xx-large', color='red' if highlight_invalid_numbers and not cell.valid else 'black')\
            for k, cell in zip(range(0, 81), self.sudoku.flatten())])

        return labels.reshape([9, 9])


    def draw(self, *args, **kwargs):
        '''
        Draws the sudoku (it draws the grid and the numbers)
        :param args, kwargs: Additional arguments to be passed at draw_numbers() call
        :return Same as draw_numbers() returned
        '''
        self.draw_grid()
        labels = self.draw_numbers(*args, **kwargs)
        return labels


    def __call__(self, *args, **kwargs):
        '''
        Alias of draw()
        '''
        return self.draw(*args, **kwargs)
