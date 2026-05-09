import os

from Board import Board
from Player import Player
from Vec4 import Vec4
from typing import Type
from itertools import product
import Util
import time

default_symbols = ['X', 'O', 'Y', 'Z', 'A', 'B', 'C', 'D']
default_colors = ['red', 'blue', 'green', 'yellow', 'magenta', 'cyan', 'orange', 'white']

class GameState:

    WAITING = 0
    PLAYING = 1
    PAUSED = 2
    FINISHED = 3

class Game:

    size: int
    symbols: list[str]
    colors: list[str]
    players: list[Player]
    time_limit_ms: float
    board: Board
    turn: int
    state: int
    history: list[tuple[str, Vec4]]
    scoring_sets: list[tuple[Vec4, ...]]
    consecutive_forfeits: int
    winner_idx: int | None

    def __init__(self, size: int, players: list[Type[Player]], symbols: list[str] = None, colors: list[str] = None, time_limit_ms: float = 0.0) -> None:

        if size < 2:
            raise ValueError('Game size must be at least 2')
        self.size = size
        
        if not symbols:
            if len(players) > len(default_symbols):
                raise ValueError('Not enough default symbols for the number of players. Please provide argument `symbols: list[str]`.')
            symbols = default_symbols
        if len(players) > len(symbols):
            raise ValueError('Not enough symbols for the number of players')
        self.symbols = symbols[:len(players)]

        if not colors:
            if len(players) > len(default_colors):
                raise ValueError('Not enough default colors for the number of players. Please provide argument `colors: list[str]`.')
            colors = default_colors
        if len(players) > len(colors):
            raise ValueError('Not enough colors for the number of players')
        self.colors = colors[:len(players)]

        if len(players) < 2:
            raise ValueError('At least two players are required')
        self.players = [players[i](self.symbols, self.symbols[i], self.size) for i in range(len(players))]

        self.time_limit_ms = time_limit_ms
        self.board = Board(self.size, {self.symbols[i]: self.colors[i] for i in range(len(players))})
        self.turn = 0
        self.state = GameState.WAITING
        self.history = []
        self.scoring_sets = self.getScoringSets()
        self.consecutive_forfeits = 0
    
    def getScoringSets(self) -> list[tuple[Vec4, ...]]:
        step_vectors = []
        for v in product((1, 0, -1), repeat=4):
            vector = Vec4(*v)
            if not vector or -vector in step_vectors:
                continue
            step_vectors.append(vector)
        scoring_sets = []
        for vector in step_vectors:
            origin = Vec4.zero()
            for i in range(4):
                if vector[i] < 0:
                    origin[i] = self.size - 1
            start_points = [origin]
            for i in range(4):
                if vector[i] == 0:
                    step = Vec4(i == 0, i == 1, i == 2, i == 3)
                    new_start_points = []
                    for start_point in start_points:
                        for j in range(self.size):
                            new_start_points.append(start_point + step * j)
                    start_points = new_start_points
            scoring_sets.extend([tuple(start_point + vector * i for i in range(self.size)) for start_point in start_points])
        return scoring_sets
    
    def reset(self) -> None:
        self.board = Board(self.size, {self.symbols[i]: self.colors[i] for i in range(len(self.players))})
        self.turn = 0
        self.state = GameState.WAITING
        self.consecutive_forfeits = 0
    
    def play(self) -> None:
        Util.clearScreen()
        print('Starting new game...\n')
        self.state = GameState.PLAYING
        while self.state == GameState.PLAYING:
            self.board.show()
            self.playTurn()
            if self.consecutive_forfeits >= len(self.players) or self.board.isFull():
                self.board.show()
                self.finish()

    def playTurn(self) -> None:
        player_idx = self.turn % len(self.players)
        player = self.players[player_idx]
        player_char = Util.style(self.symbols[player_idx], self.colors[player_idx], bold=True)
        player_styled = Util.style('Player', self.colors[player_idx])
        print(f'{player_styled} {player_char} ({player})\'s turn...')
        t0 = time.time()
        move = player.query(self.board.copy(), self.time_limit_ms)
        dt = (time.time() - t0) * 1000
        Util.clearScreen()
        if self.validateMove(move, dt):
            human_move = ','.join([str(n + 1) for n in move])
            print(f'{player_styled} {player_char} ({player}) played ({human_move}) in {int(dt)} ms\n')
            self.makeMove(player.symbol, move)
        else:
            print(f'{player_styled} {player_char} ({player}) failed to make a move in {int(dt)} ms\n')
            self.makeMove(player.symbol, None)
    
    def validateMove(self, move: Vec4 | tuple[int, int, int, int], time_ms: float) -> bool:
        if self.time_limit_ms and time_ms > self.time_limit_ms:
            print(f'Invalid move: Exceeded time limit of {self.time_limit_ms} ms')
            return False
        if not isinstance(move, Vec4 | tuple) or (isinstance(move, tuple) and len(move) != 4):
            print('Invalid move: Type must be Vec4 or 4-tuple')
            return False
        if any(not isinstance(n, int) or n < 0 or n >= self.size for n in move):
            print(f'Invalid move: Components must be integers between 0 and {self.size - 1}')
            return False
        if self.board[move]:
            print(f'Invalid move: Cell is already occupied with "{self.board[move]}"')
            return False
        return True

    def makeMove(self, symbol: str, move: Vec4) -> None:
        if move is None:
            self.consecutive_forfeits += 1
        else:
            self.board[move] = symbol
            self.consecutive_forfeits = 0
        self.history.append((symbol, move))
        self.turn += 1
    
    def revertMove(self) -> None:
        if not self.history:
            raise ValueError('No moves to revert')
        move = self.history.pop()[1]
        self.board[move] = ''
        if move is None:
            self.consecutive_forfeits -= 1
        else:
            self.consecutive_forfeits = 0
        self.turn -= 1
    
    def finish(self) -> None:
        self.state = GameState.FINISHED
        Util.clearScreen()
        print('\nGame Finished!\n')
        self.board.show()
        print('Final scores:\n')
        scores = self.countScores()
        for i, score in enumerate(scores):
            if score == max(scores):
                medal = ' 🏆'
            else:
                medal = ''
            player_char = Util.style(self.symbols[i], self.colors[i], bold=True)
            player_styled = Util.style('Player', self.colors[i])
            print(f'{player_styled} {player_char} ({self.players[i]}): {score}{medal}')
        print()
    
    def countScores(self) -> dict[str, int]:
        idx_to_symbol = {symbol: i for i, symbol in enumerate(self.symbols)}
        scores = [0 for _ in self.symbols]
        for scoring_set in self.scoring_sets:
            symbols = [self.board[pos] for pos in scoring_set]
            origin_symbol = symbols[0]
            if origin_symbol and all(symbol == origin_symbol for symbol in symbols):
                scores[idx_to_symbol[origin_symbol]] += 1
        return scores