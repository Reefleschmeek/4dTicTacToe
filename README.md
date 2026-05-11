# 4D Tic-Tac-Toe

A four-dimensional tic-tac-toe engine for running bot competitions. Players compete on a 4D hypercube grid, scoring points for every completed line.

## Rules

- The board is an `n x n x n x n` grid (default `n=3`).
- 2 or more players take turns placing their symbol on any empty cell.
- Attempting to play an illegal move (out of bounds, occupied cell, wrong type) forfeits that turn.
- Exceeding the time limit also forfeits that turn.
- The game ends when the board is full, or when all players forfeit their turns consecutively.
- Each player scores 1 point per completed line. The player with the most completed lines wins.
- Games may be played with a handicap, forcing some number of predetermined or random moves to begin the game.

## Board Layout

The board is displayed as a grid of 2D slices of the hypercube, where each slice is a regular 2D tic-tac-toe grid. Coordinates are `(x, y, z, w)` where `x, y` select the slice and `z, w` select the cell within it. The origin is at the bottom left cell of the bottom left slice. Coordinates are **0-indexed** in code and **1-indexed** when displayed for humans.

```
y=3        .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
w=1,2,3   ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
          ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .

y=2        .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
w=1,2,3   ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
          ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .

y=1        .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
w=1,2,3   ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
          ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━    ━━━━╋━━━━━╋━━━━
           .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
           x=1                x=2                x=3
           z=1,2,3            z=1,2,3            z=1,2,3
```
Within each grid, `z` increases left to right and `w` increases bottom to top.

## Scoring

A **line** is a set of `n` cells separated by a constant step vector, where each component of the step is -1, 0, or 1 (and not all zero). This generalises the familiar rows, columns, and diagonals of 2D tic-tac-toe to four dimensions. A standard 3x3x3x3 board has 40 unique step directions and 272 total lines.

A player scores 1 point for each line where all `n` cells contain their symbol.

### Line categories

Each line belongs to one of 15 categories based on how its step vector moves across slices (x,y) and within cells (z,w). The slice and cell components each contribute a row `(±1,0)`, column `(0,±1)`, or diagonal `(±1,±1)` — or neither if all zero.

### Example lines

**Cell-Row** — a row within a single slice:
```
   . ┃ . ┃ .
  ━━━╋━━━╋━━━
   X ┃ X ┃ X
  ━━━╋━━━╋━━━
   . ┃ . ┃ .
step: (x=0, y=0, z=+1, w=0)
```

**Cell-Diagonal** — a diagonal within a single slice:
```
   . ┃ . ┃ X
  ━━━╋━━━╋━━━
   . ┃ X ┃ .
  ━━━╋━━━╋━━━
   X ┃ . ┃ .
step: (x=0, y=0, z=+1, w=+1)
```

**Slice-Row** — the same cell position across slices along x:
```
   . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   . ┃ X ┃ .      . ┃ X ┃ .      . ┃ X ┃ .
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
step: (x=+1, y=0, z=0, w=0)
```

**Slice-Row Cell-Row** — moves across slices along x while stepping along z within each slice:
```
   . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   X ┃ . ┃ .      . ┃ X ┃ .      . ┃ . ┃ X
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
step: (x=+1, y=0, z=+1, w=0)
```

**Slice-Row Cell-Diagonal** — moves across slices along x while stepping diagonally within each slice:
```
   . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ X
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   . ┃ . ┃ .      . ┃ X ┃ .      . ┃ . ┃ .
  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
   X ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
step: (x=+1, y=0, z=+1, w=+1)
```

**Slice-Diagonal** — the same cell position across slices, moving diagonally through x and y:
```
y=3       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ X ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=2       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ X ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=1       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ X ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

         x=1                x=2                x=3
         z=1,2,3            z=1,2,3            z=1,2,3
step: (x=+1, y=+1, z=0, w=0)
```

**Slice-Diagonal Cell-Row** — moves diagonally across slices while stepping along z within each slice:
```
y=3       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ X
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=2       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ X ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=1       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          X ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

         x=1                x=2                x=3
         z=1,2,3            z=1,2,3            z=1,2,3
step: (x=+1, y=+1, z=+1, w=0)
```

**Slice-Diagonal Cell-Diagonal** — all four coordinates change simultaneously, the main hypercube diagonal:
```
y=3       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ X
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=2       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ X ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

y=1       . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
w=1,2,3  ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          . ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .
         ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
          X ┃ . ┃ .      . ┃ . ┃ .      . ┃ . ┃ .

         x=1                x=2                x=3
         z=1,2,3            z=1,2,3            z=1,2,3
step: (x=+1, y=+1, z=+1, w=+1)
```
## Getting Started

### Requirements

```bash
pip install -r requirements.txt
```

### Running

Launch the interactive menu:

```bash
python Main.py
```

The menu lets you add players, set board size, set a time limit, and start a game. Players already in `submissions/` are automatically detected and listed.

## Creating a Bot

### 1. Folder structure

Place your bot in the `submissions/` folder:

```
submissions/
    yourname/
        MyBot.py
        AnotherBot.py
```

Each file should contain exactly one class that extends `Player`. Multiple bots per contestant are supported; each file is loaded separately.

### 2. Implement the `Player` interface

```python
from Player import Player
from Board import Board
from Vec4 import Vec4

class MyBot(Player):
    def query(self, board: Board, time_limit_ms: float) -> Vec4 | tuple[int, int, int, int]:
        # return the cell you want to play
        ...
```

`query` is the only required interface function. Everything else is up to you.

### 3. The `Player` base class

```python
class Player(ABC):
    symbol_list: list[str]   # all player symbols in turn order
    symbol: str              # your symbol
    board_size: int          # n for an n×n×n×n board

    def __init__(self, symbol_list: list[str], symbol: str, board_size: int): ...

    @abstractmethod
    def query(self, board: Board, time_limit_ms: float) -> Vec4 | tuple[int, int, int, int]: ...
```

Your bot receives a **copy** of the board each turn; modifications won't affect the game.

### 4. The `Board` interface

```python
board[Vec4(x, y, z, w)]       # returns symbol string, or '' if empty
board[(x, y, z, w)]           # tuple indexing also works
board.size                    # board dimension n
board.isFull() -> bool        # True if no empty cells remain
board.copy() -> Board         # deep copy
```

Coordinates are **0-indexed** in code (`0` to `board.size - 1`).

### 5. `Vec4`

Coordinates are represented as `Vec4(x, y, z, w)`.

```python
from Vec4 import Vec4

v = Vec4(1, 2, 3, 0)
v[0]              # 1  (integer index)
v['x']            # 1  (named access)
v + Vec4(...)     # component-wise addition
v * scalar        # scalar multiplication
v * Vec4(...)     # dot product
-v                # negation
abs(v)            # magnitude
list(v)           # [x, y, z, w]
x, y, z, w = v    # unpacking
```

### 6. Move validation

A move is invalid and the turn is forfeited if any of the following are true:

- The time limit is exceeded
- The return type is not `Vec4` or a 4-tuple of integers
- Any component is out of range (`< 0` or `>= board_size`)
- The cell is already occupied

### 7. Rules for submissions

- Only Python standard library modules are permitted
- Your file must contain exactly one class extending `Player`

### 8. Sending your submission

Send your bot file(s) directly to the organiser (reefleschmeek@gmail.com). Submissions are kept private and contestants cannot see each other's code.

## Project Structure

```
4dTicTacToe/
├── Main.py             # entry point and interactive menu
├── Menu.py             # menu system
├── Game.py             # game runner and scoring
├── Board.py            # board representation and display
├── Player.py           # abstract base class
├── PlayerLoader.py     # auto-discovers built-ins and submissions
├── Vec4.py             # 4D vector
├── Util.py             # terminal styling helpers
├── HumanPlayer.py      # human input via terminal
├── RandomPlayer.py     # random move bot
├── requirements.txt
└── submissions/
    └── yourname/
        └── MyBot.py
```
