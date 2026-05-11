from Player import Player
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomPlayer
from pathlib import Path
import importlib.util
import inspect

def loadModule(path: Path) -> object:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def getPlayerSubclasses(module: object) -> list[type[Player]]:
    return [
        cls for _, cls in inspect.getmembers(module, inspect.isclass)
        if issubclass(cls, Player) and cls is not Player
    ]

classes: dict[str, type[Player]] = {
    'HumanPlayer': HumanPlayer,
    'RandomPlayer': RandomPlayer,
}

for path in (Path('submissions')).glob('*/*.py'):
    for cls in getPlayerSubclasses(loadModule(path)):
        classes[f'{path.parent.name}.{cls.__name__}'] = cls

if __name__ == '__main__':
    for name, cls in classes.items():
        print(f'{name}: {cls}')