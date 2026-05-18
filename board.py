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
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.first_move = True

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

                if self.board[r][c] != MINE:
                    self.board[r][c] = 0

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

                if self.flags[r][c]:
                    row.append("F")

                elif self.visible[r][c]:

                    if self.board[r][c] == MINE:
                        row.append("*")
                    else:
                        row.append(str(self.board[r][c]))

                else:
                    row.append("#")

            print(" ".join(row))

    def reveal_cell(self, row, col):
        if self.first_move:

            self.first_move = False

            if self.board[row][col] == MINE:
                self.move_mine(row, col)

        if self.flags[row][col]:
            return True
        """
        Reveal a cell on the board.
        """

        if self.board[row][col] == MINE:
            self.visible[row][col] = True
            return False

        self.dfs_reveal(row, col)

        return True

    def dfs_reveal(self, row, col):
        """
        Reveal neighboring empty cells using DFS.
        """

        if row < 0 or row >= self.rows:
            return

        if col < 0 or col >= self.cols:
            return

        if self.visible[row][col]:
            return

        self.visible[row][col] = True

        if self.board[row][col] != 0:
            return

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            self.dfs_reveal(nr, nc)

    def check_win(self):
        """
        Check if the player has won.
        """

        revealed_cells = 0

        for r in range(self.rows):
            for c in range(self.cols):

                if self.visible[r][c]:
                    revealed_cells += 1

        total_safe_cells = (self.rows * self.cols) - self.mines

        return revealed_cells == total_safe_cells

    def toggle_flag(self, row, col):
        """
        Place or remove a flag.
        """

        if not self.visible[row][col]:
            self.flags[row][col] = not self.flags[row][col]

    def move_mine(self, row, col):
        """
        Move a mine to another position.
        """

        for r in range(self.rows):
            for c in range(self.cols):

                if self.board[r][c] != MINE:
                    self.board[r][c] = MINE
                    self.board[row][col] = 0

                    self.calculate_numbers()

                    return

    def reveal_all_mines(self):
        """
        Reveal all mines on the board.
        """

        for r in range(self.rows):
            for c in range(self.cols):

                if self.board[r][c] == MINE:
                    self.visible[r][c] = True
