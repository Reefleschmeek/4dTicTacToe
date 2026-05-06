from Game import Game
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer

players = [HumanPlayer] + [RandomPlayer] * 1
game = Game(players=players, size=3, time_limit_ms=10_000)
game.play()