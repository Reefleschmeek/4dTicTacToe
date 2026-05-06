from Game import Game
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer

players = [RandomPlayer] * 2
# players[0] = HumanPlayer
game = Game(players=players, size=3)
game.play()