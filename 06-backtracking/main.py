import os

import numpy as np


class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)



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
        for r in range(9):
            for c in range(9):
                if self.field[r, c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """
        return False 


    def check_field(self) -> bool:
        return True



def main() -> None:
    sudoku_solver = SudokuSolver()

if __name__ == "__main__":
    main()

