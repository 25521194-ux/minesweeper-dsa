"""
board.py

Handle board generation and mine placement.
"""

import random

MINE = -1


class Board:
    """
    Represent a Minesweeper board.
    """

    def __init__(self, rows, cols, mines):
        """
        Initialize board size and mine count.
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]

        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        """
        Randomly place mines on the board.
        """
        placed = 0

        while placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if self.board[r][c] != MINE:
                self.board[r][c] = MINE
                placed += 1

    def calculate_numbers(self):
        """
        Calculate numbers around each mine.
        """
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for r in range(self.rows):
            for c in range(self.cols):

                if self.board[r][c] == MINE:
                    continue

                count = 0

                for dr, dc in directions:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.board[nr][nc] == MINE:
                            count += 1

                self.board[r][c] = count

    def display_board(self):
        """
        Display the visible board to the player.
        """

        for r in range(self.rows):
            row = []

            for c in range(self.cols):

                if self.visible[r][c]:

                    if self.board[r][c] == MINE:
                        row.append("*")
                    else:
                        row.append(str(self.board[r][c]))

                else:
                    row.append("#")

            print(" ".join(row))

    def reveal_cell(self, row, col):
        """
        Reveal a cell on the board.
        """

        self.visible[row][col] = True

        if self.board[row][col] == MINE:
            return False

        return True