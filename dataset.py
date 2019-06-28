

import pandas as pd
import numpy as np
from sudoku import Sudoku
from utils.singleton import singleton

# Points to the dataset file (must be a csv).
DATASET_URL = '/home/vykstorm/Datasets/sudoku/sudoku.csv'


@singleton
class SudokuDataset:
    '''
    This class provides a database of sudokus Each entry is a pair of sudoku configurations:
    The sudoku unsolved and solved. It 1M entries
    I got it from kaggle: https://www.kaggle.com/bryanpark/sudoku
    '''
    def __init__(self):
        pass

    def get_samples(self, shuffle=True, return_solutions=True, random_seed=None):
        '''
        Creates an iterator that returns samples from this database

        :param shuffle: When this argument is set to True, the sudokus will be shuffled before
        returned by this method

        :param random_seed: The random seed to be used in order to shuffle the samples

        :param return_solutions: If True the iterator will return a tuple on each epoch
        with two sudoku configurations (the sudoku unsolved and solved). If false, it only
        returns the sudoku unsolved
        '''
        def parse_sudoku(data):
            sudoku = Sudoku(np.array(list(map(int, data)), dtype=np.uint8).reshape([9, 9]))
            if not sudoku.valid:
                raise ValueError('Invalid sudoku configuration found in dataset')
            return sudoku

        np.random.seed(random_seed)
        while True:
            for chunk in pd.read_csv(DATASET_URL, chunksize=50):
                for i in np.random.permutation(chunk.shape[0]):
                    entry = chunk.iloc[i]
                    unsolved = parse_sudoku(entry['quizzes'])

                    if not return_solutions:
                        yield unsolved
                        continue
                    solved = parse_sudoku(entry['solutions'])

                    # The solved configuration is really the solution to the unsolved configuration?
                    if not (unsolved < solved and solved.full):
                        raise ValueError('Invalid sudoku solution found in dataset')

                    yield unsolved, solved


    def get_sample(self, return_solution=True):
        '''
        This method returns only 1 sudoku sample from the dataset.
        :param return_solution: If its True, return also the solution of the sudoku
        '''
        return next(self.get_samples(shuffle=True, return_solutions=return_solution))


if __name__ == '__main__':
    dataset = Dataset()
    quizz, solution = next(dataset.get_samples())
    print("Sudoku:\n")
    print(quizz)
    print('\n\nSolution:\n')
    print(solution)
