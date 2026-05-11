"""
gui.py

Pygame GUI for Minesweeper.
"""

import pygame
from board import Board

pygame.init()

WIDTH = 720
HEIGHT = 720

ROWS = 9
COLS = 9
MINES = 10

CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

font = pygame.font.SysFont(None, 36)

game = Board(ROWS, COLS, MINES)

running = True

while running:

    screen.fill((30, 30, 30))

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # LEFT CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            row = y // CELL_SIZE
            col = x // CELL_SIZE

            # LEFT CLICK = reveal
            if event.button == 1:

                alive = game.reveal_cell(row, col)

                if not alive:
                    game.reveal_all_mines()
                    print("GAME OVER")

            # RIGHT CLICK = flag
            elif event.button == 3:

                game.toggle_flag(row, col)

    # DRAW BOARD
    for r in range(ROWS):
        for c in range(COLS):

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Hidden cell
            color = (100, 100, 100)

            # Revealed cell
            if game.visible[r][c]:
                color = (180, 180, 180)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            # FLAG
            if game.flags[r][c]:

                text = font.render("F", True, (255, 0, 0))

                screen.blit(
                    text,
                    (
                        c * CELL_SIZE + CELL_SIZE // 3,
                        r * CELL_SIZE + CELL_SIZE // 4
                    )
                )

            # REVEALED VALUES
            elif game.visible[r][c]:

                value = game.board[r][c]

                if value == -1:
                    display = "*"
                    color = (255, 0, 0)

                elif value == 0:
                    display = ""

                else:
                    display = str(value)

                text = font.render(display, True, (0, 0, 0))

                screen.blit(
                    text,
                    (
                        c * CELL_SIZE + CELL_SIZE // 3,
                        r * CELL_SIZE + CELL_SIZE // 4
                    )
                )

    pygame.display.flip()

pygame.quit()