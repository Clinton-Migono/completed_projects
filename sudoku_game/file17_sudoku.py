"""Simple terminal Sudoku game.

The game:
- asks for a difficulty level (`easy` by default)
- generates a full Sudoku solution
- removes some numbers to create a puzzle
- lets the user choose an empty square and enter a value
- shows `CORRECT` when the value matches the solution
- keeps showing the board until the puzzle is complete or the user quits
"""

import random


BOARD_SIZE = 9
BOX_SIZE = 3


def create_empty_board():
    """Return a new 9x9 board filled with zeros."""
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def is_valid(board, num, row, col):
    """Check whether `num` can be placed in `board[row][col]`."""
    for i in range(BOARD_SIZE):
        if board[row][i] == num:
            return False

    for i in range(BOARD_SIZE):
        if board[i][col] == num:
            return False

    box_row_start = (row // BOX_SIZE) * BOX_SIZE
    box_col_start = (col // BOX_SIZE) * BOX_SIZE

    for i in range(box_row_start, box_row_start + BOX_SIZE):
        for j in range(box_col_start, box_col_start + BOX_SIZE):
            if board[i][j] == num:
                return False

    return True


def find_empty(board):
    """Return the next empty position as (row, col), or None if full."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return row, col
    return None


def solve_sudoku(board):
    """Solve the board using backtracking."""
    empty_spot = find_empty(board)
    if empty_spot is None:
        return True

    row, col = empty_spot

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False


def fill_board_randomly(board):
    """Create a complete valid Sudoku board.

    The shuffled candidate list makes each generated solution feel different.
    Without that shuffle, backtracking would keep producing the same pattern.
    """
    empty_spot = find_empty(board)
    if empty_spot is None:
        return True

    row, col = empty_spot
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if is_valid(board, num, row, col):
            board[row][col] = num
            if fill_board_randomly(board):
                return True
            board[row][col] = 0

    return False


def copy_board(board):
    """Create a deep copy of a Sudoku board."""
    return [row[:] for row in board]


def make_puzzle(solution_board, clues_to_keep):
    """Remove numbers from the solved board to create a playable puzzle."""
    puzzle = copy_board(solution_board)
    cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
    random.shuffle(cells)

    cells_to_remove = BOARD_SIZE * BOARD_SIZE - clues_to_keep

    for row, col in cells[:cells_to_remove]:
        puzzle[row][col] = 0

    return puzzle


def print_board(board):
    """Display the Sudoku board with 3x3 box separators."""
    print("\n    1 2 3   4 5 6   7 8 9")
    print("  +-------+-------+-------+")

    for row in range(BOARD_SIZE):
        row_values = []
        for col in range(BOARD_SIZE):
            value = board[row][col]
            row_values.append(str(value) if value != 0 else ".")

        print(
            f"{row + 1} | {' '.join(row_values[0:3])} | "
            f"{' '.join(row_values[3:6])} | {' '.join(row_values[6:9])} |"
        )

        if (row + 1) % BOX_SIZE == 0:
            print("  +-------+-------+-------+")


def choose_difficulty():
    """Ask the player for a difficulty level."""
    levels = {
        "easy": 40,
        "hard": 32,
        "advance": 26,
    }

    user_choice = input(
        "Choose difficulty (easy/hard/advance) [easy]: "
    ).strip().lower()

    if not user_choice:
        user_choice = "easy"

    if user_choice not in levels:
        print("Unknown choice. Starting with easy level.")
        user_choice = "easy"

    return user_choice, levels[user_choice]


def ask_for_number(prompt_text):
    """Read a number from 1 to 9 from the player."""
    while True:
        user_input = input(prompt_text).strip()

        if user_input.isdigit():
            number = int(user_input)
            if 1 <= number <= 9:
                return number

        print("Please enter a number from 1 to 9.")


def play_game():
    """Run the full Sudoku game loop."""
    difficulty_name, clues_to_keep = choose_difficulty()

    solution = create_empty_board()
    fill_board_randomly(solution)

    puzzle = make_puzzle(solution, clues_to_keep)

    # These are the original visible numbers.
    # We keep them separate so the player cannot overwrite the starter clues.
    starter_cells = {
        (row, col)
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
        if puzzle[row][col] != 0
    }

    print(f"\nStarting {difficulty_name} Sudoku.")
    print("Pick an empty square by row and column, then enter the correct value.")
    print("Press Ctrl + C at any time to quit.\n")

    while True:
        print_board(puzzle)

        if find_empty(puzzle) is None:
            print("Congratulations! You completed the Sudoku puzzle.")
            return

        row = ask_for_number("Choose row (1-9): ") - 1
        col = ask_for_number("Choose column (1-9): ") - 1

        if (row, col) in starter_cells:
            print("That square already has a starter number. Choose an empty square.\n")
            continue

        if puzzle[row][col] != 0:
            print("That square is already filled. Choose another empty square.\n")
            continue

        value = ask_for_number("Enter value (1-9): ")

        if solution[row][col] == value:
            puzzle[row][col] = value
            print("CORRECT\n")
        else:
            print("Incorrect. Try another value or another empty square.\n")


def main():
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame ended by user. Goodbye.")


if __name__ == "__main__":
    main()
