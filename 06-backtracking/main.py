import os

import numpy as np


class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path:str) -> None:

        # list of lists (rows)
        loaded_rows : list[list[int]] = [] 
        # TODO implement loading of the file

        # convert nested list to numpy array
        self.field = np.array(loaded_rows)



    def check_sequence(self, sequence:np.ndarray) -> bool:
        return True


    def check_row(self, row_index:int) -> bool:
        pass

    def check_column(self, column_index:int) -> bool:
        pass 

    def check_block(self, row_index:int, column_index:int) -> bool:
        pass 


    def check_one_cell(self, row_index:int , column_index:int) -> bool:
        return False

    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """
        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """
        return False 





def main() -> None:
    sudoku_solver = SudokuSolver()

if __name__ == "__main__":
    main()

