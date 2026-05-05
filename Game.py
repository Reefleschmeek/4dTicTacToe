from Player import Player

class Game:

    def __init__(self):
        self.x = 0b0101100000010000000011000000000100100010000100010100000100010000000010000001000001
        self.o = 0b0010000000001000000100000000000001000001100000001011100010001100100000000100000000
        self.turn = 1
        self.size = 3
        self.point_masks = self.generatePointMasks()
    
    def coordToBit(self, x, y, z, w):
        return 1 << (x + y * self.size + z * self.size ** 2 + w * self.size ** 3)
    
    def generatePointMasks(self):
        vectors = [
            (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
            (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1),
            (1, 1, 1, 0), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1),
            (1, 1, 1, 1),
        ]
        masks = []
        for vector in vectors:
            for i in range(4):
                if vector[i] == 0:
                    continue

    def displayBoard(self):
        for w in range(self.size - 1, -1, -1):
            for y in range(self.size - 1, -1, -1):
                for z in range(self.size):
                    for x in range(self.size):
                        pos = self.coordToBit(x, y, z, w)
                        if self.x & pos:
                            print('X', end=' ')
                        elif self.o & pos:
                            print('O', end=' ')
                        else:
                            print('.', end=' ')
                    print(' ', end='')
                print()
            print()