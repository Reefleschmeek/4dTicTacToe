from Player import Player
from Board import Board
from Vec4 import Vec4
import random

class RandomPlayer(Player):

    def query(self, board: Board, time_limit_ms: float) -> Vec4:
        empty_cells = []
        for x in range(board.size):
            for y in range(board.size):
                for z in range(board.size):
                    for w in range(board.size):
                        if not board[x, y, z, w]:
                            empty_cells.append(Vec4(x, y, z, w))
        return random.choice(empty_cells)