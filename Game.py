from Board import Board
from Player import Player
from Vec4 import Vec4
from typing import Type
from itertools import product
import time

default_symbols = ['X', 'O', 'Y', 'Z', 'A', 'B', 'C', 'D']

class GameState:

    WAITING = 0
    PLAYING = 1
    PAUSED = 2
    FINISHED = 3

class Game:

    size: int
    time_limit_ms: float
    players: list[Player]
    board: Board
    turn: int
    state: int
    history: list[tuple[str, Vec4]]
    scoring_sets: list[tuple[Vec4, ...]]
    consecutive_forfeits: int

    def __init__(self, size: int, players: list[Type[Player]], symbols: list[str] = None, time_limit_ms: float = 0.0) -> None:
        if size < 2:
            raise ValueError('Game size must be at least 2')
        if len(players) < 2:
            raise ValueError('At least two players are required')
        if not symbols:
            if len(players) > len(default_symbols):
                raise ValueError('Not enough default symbols for the number of players. Please provide argument `symbols: list[str]`.')
            symbols = default_symbols
        if len(players) > len(symbols):
            raise ValueError('Not enough symbols for the number of players')
        self.symbols = symbols[:len(players)]
        self.size = size
        self.time_limit_ms = time_limit_ms
        self.players = [players[i](self.symbols, self.symbols[i]) for i in range(len(players))]
        self.board = Board(self.size)
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
        self.board = Board(self.size)
        self.turn = 0
        self.state = GameState.WAITING
        self.consecutive_forfeits = 0
    
    def play(self) -> None:
        print('\nStarting new game...\n')
        self.state = GameState.PLAYING
        while self.state == GameState.PLAYING:
            self.board.show()
            self.playTurn()
            if self.consecutive_forfeits >= len(self.players) or self.board.isFull():
                self.finish()

    def playTurn(self) -> None:
        player = self.players[self.turn % len(self.players)]
        print(f'Player "{player.symbol}" ({player})\'s turn...')
        t0 = time.time()
        move = player.query(self.board.copy(), self.time_limit_ms)
        dt = (time.time() - t0) * 1000
        if self.validateMove(move, dt):
            human_move = ','.join([str(n + 1) for n in move])
            print(f'Player "{player.symbol}" ({player}) played ({human_move}) in {int(dt)} ms\n')
            self.makeMove(player.symbol, move)
        else:
            print(f'Player "{player.symbol}" ({player}) failed to make a move in {int(dt)} ms\n')
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
        self.board.show()
        scores = self.countScores()
        print('Game finished. Final scores:')
        for i, score in enumerate(scores):
            if score == max(scores):
                medal = ' 🏆'
            else:
                medal = ''
            print(f'Player "{self.symbols[i]}" ({self.players[i]}): {score}{medal}')
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