from Board import Board
from Vec4 import Vec4
from abc import ABC, abstractmethod

class Player(ABC):

    symbol_list: list[str]
    symbol: str
    board_size: int

    def __init__(self, symbol_list: list[str], symbol: str, board_size: int) -> None:
        self.symbol_list = symbol_list
        self.symbol = symbol
        self.board_size = board_size

    @abstractmethod
    def query(self, board: Board, time_limit_ms: float) -> Vec4 | tuple[int, int, int, int]:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'