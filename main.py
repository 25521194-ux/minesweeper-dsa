"""
main.py

Run the Minesweeper game.
"""

from board import Board

game = Board(8, 8, 10)

for row in game.board:
    print(row)