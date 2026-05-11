# Minesweeper DSA Project

A Minesweeper game developed in Python using Pygame.

## Features

- GUI using Pygame
- 3 difficulty levels
- Sound effects
- Flag system
- Restart system
- Win/Lose screen
- DFS flood fill reveal algorithm

## Difficulty Levels

| Level | Board Size | Mines |
|---|---|---|
| Beginner | 9x9 | 10 |
| Intermediate | 16x16 | 40 |
| Advanced | 24x24 | 99 |

## Data Structures Used

- 2D Arrays
- Boolean matrices

## Algorithms Used

- Depth First Search (DFS)
- Flood Fill Algorithm
- Random mine placement

## Controls

- Left Click → Reveal cell
- Right Click → Place flag
- R → Restart
- 1 / 2 / 3 → Change difficulty

## Installation

```bash
pip install -r requirements.txt
```

## Run the Game

```bash
python gui.py
```
