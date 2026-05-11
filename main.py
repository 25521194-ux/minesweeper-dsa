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

    action = input("Reveal or Flag? (r/f): ")

    row = int(input("Enter row: "))
    col = int(input("Enter col: "))

    if action == "f":
        game.toggle_flag(row, col)

    elif action == "r":

        alive = game.reveal_cell(row, col)

        if not alive:
            game.display_board()
            print("BOOM! Game Over")
            break

        if game.check_win():
            game.display_board()
            print("YOU WIN!")
            break