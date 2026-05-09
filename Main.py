from Menu import Menu
from Game import Game
from Player import Player
from pathlib import Path
import sys
import argparse
import importlib
import importlib.util

def loadSubmission(name: str) -> type[Player]:
    username, botname = name.split('.')
    path = Path('submissions') / username / f'{botname}.py'
    if not path.exists():
        raise ValueError(f'No submission found at {path}')
    spec = importlib.util.spec_from_file_location(botname, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for obj in vars(module).values():
        if isinstance(obj, type) and issubclass(obj, Player) and obj is not Player:
            return obj
    raise ValueError(f'No Player subclass found in {path}')

def loadBuiltin(name: str) -> type[Player]:
    path = Path(f'{name}.py')
    if not path.exists():
        raise ValueError(f'No built-in player named {name}')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for obj in vars(module).values():
        if isinstance(obj, type) and issubclass(obj, Player) and obj is not Player:
            return obj
    raise ValueError(f'No Player subclass found in {path}')

def resolvePlayer(name: str) -> type[Player]:
    if '.' in name:
        return loadSubmission(name)
    return loadBuiltin(name)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('players', nargs='+')
    parser.add_argument('--size', type=int, default=3)
    parser.add_argument('--time', type=int, default=0, help='Time limit per turn in milliseconds')
    args = parser.parse_args()

    if len(args.players) < 2:
        print('At least two players are required')
        sys.exit(1)
    
    menu = Menu()
    choice = menu.prompt('Select an option:', ['Start Game', 'Exit'])
    if choice == 1:
        sys.exit(0)

    players = [resolvePlayer(name) for name in args.players]
    game = Game(players=players, size=args.size, time_limit_ms=args.time)
    game.play()