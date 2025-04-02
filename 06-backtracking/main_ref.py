import os

import numpy as np


class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path:str) -> None:

        # list of lists (rows)
        loaded_rows : list[list[int]] = [] 
        # TODO implement loading of the file 
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                loaded_rows.append([int(cell) for cell in line.split(";")])

        # convert nested list to numpy array
        self.field = np.array(loaded_rows)

    def save(self, file_path:str) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            for row_index in range(9):
                row = self.field[row_index]
                f.write(";".join([str(number) for number in row]) + "\n")


    def check_sequence(self, sequence:np.ndarray) -> bool:
        contains = set()
        for cell in sequence:
            if cell == 0:  # není vyplněno
                continue
            if cell in contains:  # neco vicekrat
                return False
            contains.add(cell)
        return True


    def check_row(self, row_index:int) -> bool:
        row = self.field[row_index, :]
        return self.check_sequence(row)

    def check_column(self, column_index:int) -> bool:
        column = self.field[:, column_index]
        return self.check_sequence(column)

    def check_block(self, row_index:int, column_index:int) -> bool:
        row_start = (row_index // 3) * 3
        column_start = (column_index // 3) * 3
        block = self.field[row_start: row_start + 3, column_start: column_start + 3]
        return self.check_sequence(block.reshape(-1))

    def check_one_cell(self, row_index:int , column_index:int) -> bool:
        return self.check_row(row_index) and self.check_column(column_index) and self.check_block(row_index, column_index):

    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """

        for r in range(9):
            for c in range(9):
                if self.field[r, c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """

        next_field = self.get_empty_cell()

        if not next_field: # celé vyplněno -> dobře!
            return True # jupí

        r, c = next_field

        for v in range(1, 10):
            self.field[r,c] = v

            if not self.check_one_cell(r, c):
                continue

            solved = self.solve()

            if solved:
                return True

        self.field[r,c] = 0
        return False

    def check_field(self) -> bool:
        for r in range(9):
            if not self.check_row(r):
                return False
        for c in range(9):
            if not self.check_column(c):
                return False

        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                if not self.check_block(r, c):
                    return False
        return True

def main() -> None:
    sudoku_solver = SudokuSolver()

    for sudoku_file in os.listdir("data"):
        file = os.path.join("data", sudoku_file)
        print("solving: ", file)
        sudoku_solver.load(file)
        import time; start = time.time()
        print(sudoku_solver.solve())
        print(time.time() - start)
        print(sudoku_solver.field)

if __name__ == "__main__":
    main()

