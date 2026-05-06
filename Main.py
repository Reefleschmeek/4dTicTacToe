from Game import Game
from RandomPlayer import RandomPlayer

players = [RandomPlayer, RandomPlayer]
game = Game(players=players, size=3, time_limit_ms=10_000)
game.play()