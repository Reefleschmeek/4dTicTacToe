
class Player:

    def __init__(self):
        self.next_move: int = None

    def query(self, board):
        pass

    def stop(self):
        pass

class Game:

    def __init__(self):
        self.x = 0b0
        self.o = 0b0
        self.turn = 1
    
    def query(self, player: Player):
        return player.next_move