"""
main.py

Run the Minesweeper game.
"""

from board import Board

print("=== MINESWEEPER ===")
print("1. Beginner")
print("2. Intermediate")
print("3. Advanced")

choice = input("Choose difficulty: ")

if choice == "1":
    rows, cols, mines = 9, 9, 10

elif choice == "2":
    rows, cols, mines = 16, 16, 40

elif choice == "3":
    rows, cols, mines = 24, 24, 99

else:
    print("Invalid choice")
    exit()

game = Board(rows, cols, mines)

while True:

    game.display_board()

    row = int(input("Enter row: "))
    col = int(input("Enter col: "))

    alive = game.reveal_cell(row, col)

    if not alive:
        print("BOOM! Game Over")
        break