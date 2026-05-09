from Vec4 import Vec4
from typing import Self
import Util

class Board:

    size: int
    color_map: dict[str, str]
    cells: list[list[list[list[str]]]]

    def __init__(self, size: int, color_map: dict[str, str] = None) -> None:
        self.size = size
        self.color_map = color_map if color_map is not None else {}
        self.cells = [
            [[['' for w in range(self.size)] for z in range(self.size)] for y in range(self.size)] for x in range(self.size)
        ]
    
    def isFull(self) -> bool:
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    for w in range(self.size):
                        if not self.cells[x][y][z][w]:
                            return False
        return True
    
    def copy(self) -> Self:
        new_board = Board(self.size, self.color_map)
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    for w in range(self.size):
                        new_board.cells[x][y][z][w] = self.cells[x][y][z][w]
        return new_board
    
    def show(self) -> None:
        for y in range(self.size - 1, -1, -1):
            for w in range(self.size - 1, -1, -1):
                if w != self.size - 1:
                    print('  ', end='')
                    grid_str = '╋'.join(['━━━'] * self.size)
                    print('    '.join([grid_str] * self.size))
                print('  ', end='')
                for x in range(self.size):
                    for z in range(self.size):
                        if z != 0:
                            print('┃', end='')
                        symbol = self[Vec4(x, y, z, w)]
                        if symbol:
                            char = Util.style(symbol, self.color_map.get(symbol, 'white'), bold=True)
                            print(' ' + char + ' ', end='')
                        else:
                            print('   ', end='')
                    print('    ', end='')
                print()
            if y != 0:
                print()
            print()

    def __getitem__(self, pos: Vec4 | tuple[int, int, int, int]) -> str:
        if isinstance(pos, Vec4):
            if any(n < 0 or n >= self.size for n in pos):
                raise IndexError('Index out of range')
            return self.cells[pos.x][pos.y][pos.z][pos.w]
        elif isinstance(pos, tuple) and len(pos) == 4:
            if any(n < 0 or n >= self.size for n in pos):
                raise IndexError('Index out of range')
            x, y, z, w = pos
            return self.cells[x][y][z][w]
        else:
            raise IndexError('Index must be a Vec4 or 4-tuple')
    
    def __setitem__(self, pos: Vec4 | tuple[int, int, int, int], value: str) -> None:
        if isinstance(pos, Vec4):
            if any(n < 0 or n >= self.size for n in pos):
                raise IndexError('Index out of range')
            self.cells[pos.x][pos.y][pos.z][pos.w] = value
        elif isinstance(pos, tuple) and len(pos) == 4:
            if any(n < 0 or n >= self.size for n in pos):
                raise IndexError('Index out of range')
            x, y, z, w = pos
            self.cells[x][y][z][w] = value
        else:
            raise IndexError('Index must be a Vec4 or 4-tuple')