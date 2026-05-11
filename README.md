# 4D Tic-Tac-Toe

A four-dimensional tic-tac-toe engine for running AI competitions. Players compete on a 4D hypercube grid, scoring points for every completed line — across all 40 unique line directions and 272 total lines on a standard 4×4×4×4 board.

## Rules

- The board is an `n × n × n × n` grid (default `n=3`)
- Players take turns placing their symbol on any empty cell
- The game ends when the board is full, or all players forfeit consecutively
- **Scoring**: each player scores 1 point per completed line (all cells owned by that player)
- The player with the most completed lines wins
- Returning an illegal move (out of bounds, occupied cell, wrong type) forfeits that turn
- Exceeding the time limit also forfeits that turn
- Up to 8 players are supported

## Board Layout

The board is displayed as a grid of 2D slices. Coordinates are `(x, y, z, w)` where `x, y` select the slice and `z, w` select the cell within it. Coordinates are **1-indexed** when entering moves as a human player.

```
        z=1         z=2         z=3
w=1     .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
       ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
        .  ┃  .  ┃  .      .  ┃  .  ┃  .      .  ┃  .  ┃  .
       ━━━╋━━━╋━━━    ━━━╋━━━╋━━━    ━━━╋━━━╋━━━
w=2     .  ┃  .  ┃  .      ...
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

## Submitting a Bot

### 1. Folder structure

Place your bot in the `submissions/` folder:

```
submissions/
    yourname/
        MyBot.py
        AnotherBot.py
```

Each file should contain exactly one class that extends `Player`. Multiple bots per contestant are supported — each file is loaded separately.

### 2. Implement the `Player` interface

```python
from Player import Player
from Board import Board
from Vec4 import Vec4

class MyBot(Player):
    def query(self, board: Board, time_limit_ms: float) -> Vec4:
        # return the cell you want to play
        ...
```

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

Your bot receives a **copy** of the board each turn — modifications won't affect the game.

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

A move is invalid if any of the following are true — the turn is forfeited:

- The time limit is exceeded
- The return type is not `Vec4` or a 4-tuple of integers
- Any component is out of range (`< 0` or `>= board_size`)
- The cell is already occupied

### 7. Rules for submissions

- Only Python standard library modules are permitted
- Your bot must return within the time limit or forfeit the turn
- Your file must contain exactly one class extending `Player`

### 8. Sending your submission

Send your bot file(s) directly to the organiser — submissions are kept private and contestants cannot see each other's code.

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
