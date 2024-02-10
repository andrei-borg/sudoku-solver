import unittest
import pprint

SUDOKU_BOARD = [
        [0, 8, 0, 0, 0, 0, 0, 3, 0],
        [2, 0, 0, 6, 0, 7, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0, 2, 0, 1, 0, 7, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 3],
        [9, 0, 0, 7, 0, 5, 0, 0, 8],
        [4, 0, 1, 3, 0, 9, 7, 0, 6],
        [0, 2, 0, 0, 0, 0, 0, 1, 0],
        [8, 0, 3, 1, 0, 6, 5, 0, 9]
    ]

class TestSudokuSolver(unittest.TestCase):

    def test_is_valid(self):
        board = [
            [0, 8, 0, 0, 0, 0, 0, 3, 0],
            [2, 0, 0, 6, 0, 7, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 2, 0, 1, 0, 7, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 3],
            [9, 0, 0, 7, 0, 5, 0, 0, 8],
            [4, 0, 1, 3, 0, 9, 7, 0, 6],
            [0, 2, 0, 0, 0, 0, 0, 1, 0],
            [8, 0, 3, 1, 0, 6, 5, 0, 9]
        ]

        # Test valid placements
        self.assertTrue(is_valid(board, 0, 2, 4))
        self.assertTrue(is_valid(board, 1, 1, 3))
        self.assertTrue(is_valid(board, 4, 4, 9))
        self.assertTrue(is_valid(board, 8, 7, 2))

        # Test invalid placements
        self.assertFalse(is_valid(board, 0, 2, 3))
        self.assertFalse(is_valid(board, 0, 2, 2))
        self.assertFalse(is_valid(board, 2, 5, 6))
        self.assertFalse(is_valid(board, 5, 7, 1))

    def test_find_empty_location(self):
        board = [
            [1, 8, 0, 0, 0, 0, 0, 3, 0],
            [2, 0, 0, 6, 0, 7, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 2, 0, 1, 0, 7, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 3],
            [9, 0, 0, 7, 0, 5, 0, 0, 8],
            [4, 0, 1, 3, 0, 9, 7, 0, 6],
            [0, 2, 0, 0, 0, 0, 0, 1, 0],
            [8, 0, 3, 1, 0, 6, 5, 0, 9]
        ]
    
        empty_location = find_empty_location(board)
        self.assertEqual(empty_location, (0, 2))  # The first empty location is at (0, 2)

    def test_solve_sudoku(self):
        board = [
            [0, 8, 0, 0, 0, 0, 0, 3, 0],
            [2, 0, 0, 6, 0, 7, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 2, 0, 1, 0, 7, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 3],
            [9, 0, 0, 7, 0, 5, 0, 0, 8],
            [4, 0, 1, 3, 0, 9, 7, 0, 6],
            [0, 2, 0, 0, 0, 0, 0, 1, 0],
            [8, 0, 3, 1, 0, 6, 5, 0, 9]
        ]

        solve_sudoku(board)

        # Check if the Sudoku is solved correctly
        self.assertTrue(all(all(cell != 0 for cell in row) for row in board))
        self.assertTrue(all(set(row) == set(range(1, 10)) for row in board))
        self.assertTrue(all(set(board[i][j] for i in range(9)) == set(range(1, 10)) for j in range(9)))
        self.assertTrue(all(set(board[i][j] for i in range(row, row + 3) for j in range(col, col + 3)) == set(range(1, 10))
                            for row in (0, 3, 6) for col in (0, 3, 6)))


# Main function to solve Sudoku using backtracking
def solve_sudoku(board):
    empty_location = find_empty_location(board)

    if empty_location:
        row, col = empty_location
    else:
        return True

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
        
            # Try to solve the rest of the Sudoku recursively
            if solve_sudoku(board):
                return True

            # If the placement doesn't lead to a solution, backtrack
            board[row][col] = 0
    
    # No number valid, trigger backtracking
    return False

# Function to find an empty location in the Sudoku board        
def find_empty_location(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    
    return None

# Function to check if placing 'num' at board[row][col] is valid
def is_valid(board, row, col, num):
    # Check row
    for i in range(len(board)):
        if board[row][i] == num and col != i:
            return False

    # Check column
    for i in range(len(board[0])):
        if board[i][col] == num and row != i:
            return False
    
    # Check 3x3 box
    box_row = col // 3
    box_col = row // 3
    
    for i in range(box_col*3, box_col*3 + 3):
        for j in range(box_row*3, box_row*3 + 3):
            if board[i][j] == num and (row, col) != (i, j):
                return False

    return True

# Function to print the Sudoku board
def print_board(board):
    printer = pprint.PrettyPrinter(width=30, compact=True)
    printer.pprint(board)

def main():
    # Solve and print the Sudoku
    print(f'Solved: {solve_sudoku(SUDOKU_BOARD)}')
    print_board(SUDOKU_BOARD)

if __name__ == "__main__":
    main()

    # Uncomment below to run tests
    # unittest.main()