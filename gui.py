"""
gui.py

Pygame GUI for Minesweeper.
"""

import pygame
from board import Board

pygame.init()
pygame.mixer.init()

WIDTH = 720
HEIGHT = 720

difficulty = "beginner"

if difficulty == "beginner":
    ROWS = 9
    COLS = 9
    MINES = 10

elif difficulty == "intermediate":
    ROWS = 16
    COLS = 16
    MINES = 40

elif difficulty == "advanced":
    ROWS = 24
    COLS = 24
    MINES = 99

CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)
pygame.display.set_caption("Minesweeper")

FONT_SIZE = max(16, CELL_SIZE // 2)

font = pygame.font.SysFont("Segoe UI Emoji", FONT_SIZE)

# SOUND EFFECTS
click_sound = pygame.mixer.Sound("assets/click.mp3")
boom_sound = pygame.mixer.Sound("assets/boom.mp3")
win_sound = pygame.mixer.Sound("assets/win.mp3")

NUMBER_COLORS = {
    1: (50, 90, 255),
    2: (0, 140, 70),
    3: (220, 50, 50),
    4: (120, 50, 220),
    5: (170, 30, 30),
    6: (0, 170, 170),
    7: (20, 20, 20),
    8: (100, 100, 100)
}

def update_sizes():
    global CELL_SIZE, FONT_SIZE, font

    CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)

    FONT_SIZE = max(16, CELL_SIZE // 2)

    font = pygame.font.SysFont("Segoe UI Emoji", FONT_SIZE)

game = Board(ROWS, COLS, MINES)
update_sizes()

running = True
game_over = False
victory = False


def restart_game():
    """
    Restart the game.
    """

    global game, game_over, victory

    game = Board(ROWS, COLS, MINES)

    game_over = False
    victory = False

while running:

    screen.fill((50, 50, 60))
    board_w = game.cols * CELL_SIZE
    board_h = game.rows * CELL_SIZE
    offset_x = (WIDTH - board_w) // 2
    offset_y = (HEIGHT - board_h) // 2

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            update_sizes()

        # KEYBOARD EVENTS
        if event.type == pygame.KEYDOWN:

            # RESTART
            if event.key == pygame.K_r:
                restart_game()

            # BEGINNER
            elif event.key == pygame.K_1:

                difficulty = "beginner"

                ROWS = 9
                COLS = 9
                MINES = 10

                CELL_SIZE = WIDTH // COLS
                FONT_SIZE = max(16, CELL_SIZE // 2)
                font = pygame.font.SysFont("Segoe UI Emoji", FONT_SIZE)

                update_sizes()
                restart_game()
                continue

            # INTERMEDIATE
            elif event.key == pygame.K_2:

                difficulty = "intermediate"

                ROWS = 16
                COLS = 16
                MINES = 40

                CELL_SIZE = WIDTH // COLS
                FONT_SIZE = max(16, CELL_SIZE // 2)
                font = pygame.font.SysFont("Segoe UI Emoji", FONT_SIZE)

                update_sizes()
                restart_game()
                continue

            # ADVANCED
            elif event.key == pygame.K_3:

                difficulty = "advanced"

                ROWS = 24
                COLS = 24
                MINES = 99

                CELL_SIZE = WIDTH // COLS
                FONT_SIZE = max(16, CELL_SIZE // 2)
                font = pygame.font.SysFont("Segoe UI "
                                           "Emoji", FONT_SIZE)

                update_sizes()
                restart_game()
                continue

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            x, y = pygame.mouse.get_pos()

            row = (y - offset_y) // CELL_SIZE
            col = (x - offset_x) // CELL_SIZE

            # PREVENT OUT OF BOUNDS
            if row < 0 or col < 0 or row >= game.rows or col >= game.cols:
                continue

            # LEFT CLICK = reveal
            if event.button == 1:

                alive = game.reveal_cell(row, col)

                click_sound.play()

                if not alive:

                    boom_sound.play()

                    game.reveal_all_mines()
                    game_over = True

                if game.check_win():

                    win_sound.play()

                    game_over = True
                    victory = True

            # RIGHT CLICK = flag
            elif event.button == 3:

                game.toggle_flag(row, col)

    # DRAW BOARD
    for r in range(game.rows):
        for c in range(game.cols):
            rect = pygame.Rect(
                c * CELL_SIZE + offset_x,
                r * CELL_SIZE + offset_y,
                CELL_SIZE,
                CELL_SIZE
            )

            # Hidden cell
            color = (70, 70, 70)

            # Revealed cell
            if game.visible[r][c]:
                color = (220, 220, 220)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 2)

            # FLAG
            if game.flags[r][c]:

                text = font.render("🚩", True, (255, 60, 60))

                screen.blit(
                    text,
                    (
                            c * CELL_SIZE + offset_x + CELL_SIZE // 3,
                            r * CELL_SIZE + offset_y + CELL_SIZE // 4
                    )
                )

            # REVEALED VALUES
            elif game.visible[r][c]:

                value = game.board[r][c]

                if value == -1:
                    display = "💣"

                elif value == 0:
                    display = ""

                else:
                    display = str(value)

                if value == -1:
                    text_color = (20, 20, 20)
                else:
                    text_color = NUMBER_COLORS.get(value, (0, 0, 0))

                text = font.render(display, True, text_color)

                screen.blit(
                    text,
                    (
                        c * CELL_SIZE + offset_x + CELL_SIZE // 3,
                        r * CELL_SIZE + offset_y + CELL_SIZE // 4
                    )
                )

    # ENDGAME TEXT
    if game_over:

        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        # Fonts
        big_font = pygame.font.SysFont("Arial Black", 72)
        small_font = pygame.font.SysFont(None, 32)

        if victory:

            message = "YOU WIN!"
            color = (0, 255, 120)

            subtext = "Press R to play again"

        else:

            message = "GAME OVER"
            color = (255, 60, 60)

            subtext = "You clicked on a mine"

        # Blinking effect
        blink = (pygame.time.get_ticks() // 500) % 2

        if blink:
            text = big_font.render(message, True, color)

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - 60
                )
            )

        # Glow effect
        glow = big_font.render(message, True, (255, 255, 255))
        glow.set_alpha(40)

        screen.blit(
            glow,
            (
                WIDTH // 2 - glow.get_width() // 2 - 2,
                HEIGHT // 2 - 62
            )
        )

        # Subtext
        info = small_font.render(subtext, True, (220, 220, 220))

        screen.blit(
            info,
            (
                WIDTH // 2 - info.get_width() // 2,
                HEIGHT // 2 + 30
            )
        )

    # INSTRUCTIONS
    small_font = pygame.font.SysFont(None, 28)

    instruction = small_font.render(
        "Left Click: Reveal | Right Click: Flag | 1/2/3: Difficulty | R: Restart",
        True,
        (255, 255, 255)
    )

    screen.blit(instruction, (10, HEIGHT - 40))

    pygame.display.flip()

pygame.quit()
