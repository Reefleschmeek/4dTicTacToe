from typing import Callable
import Util
import readchar
import time

class MenuAction:

    def __init__(self):
        pass

    def handle(self, menu: 'Menu'):
        pass

class MenuCallback(MenuAction):

    def __init__(self, handler: Callable):
        super().__init__()
        self.handler = handler
    
    def handle(self, menu: 'Menu'):
        self.handler(menu)

class MenuReturn(MenuAction):

    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def handle(self, menu: 'Menu'):
        if callable(self.value):
            return self.value(menu)
        return self.value

class MenuNavigate(MenuAction):

    def __init__(self, *path: str):
        super().__init__()
        self.path = path
    
    def handle(self, menu: 'Menu'):
        screen = menu.screen_tree
        for step in self.path:
            screen = screen.children[step]
        menu.path = list(self.path)
        menu.current_screen = screen

class MenuScreen:

    title: str
    children: dict[str, MenuAction | MenuScreen]

    def __init__(self, title: str, children: dict[str, MenuAction | MenuScreen] = None):
        self.title = title
        self.children = children or {}
    
    def display(self, menu: 'Menu'):
        print(self.title)

    def handle(self, menu: 'Menu'):
        pass

class MenuOptions(MenuScreen):

    def __init__(self, title: str, children: dict[str, MenuAction | MenuScreen]):
        super().__init__(title)
        self.children = children

    def display(self, menu: 'Menu'):
        print(self.title)
        for i, option in enumerate(self.children):
            indicator = '  '
            print(f'{indicator}{i + 1}. {option}')
    
    def handle(self, menu: 'Menu') -> int:
        key = readchar.readkey()
        if key.isdigit():
            n = int(key)
            if 1 <= n <= len(self.children):
                choice = list(self.children.values())[n - 1]
                if isinstance(choice, MenuAction):
                    return choice.handle(menu)
                elif isinstance(choice, MenuScreen):
                    menu.path.append(choice.title)
                    menu.current_screen = choice

class MenuInput(MenuScreen):

    def __init__(self, title: str, children: dict[str, MenuAction | MenuScreen] = None, handler: Callable = None):
        super().__init__(title, children)
        self.handler = handler
    
    def handle(self, menu: 'Menu'):
        input_str = input()
        self.handler(menu, input_str)
        menu.back()

class Menu:

    path: list[str]
    screen_tree: MenuScreen
    current_screen: MenuScreen
    data: dict
    displayFunc: callable

    def __init__(self, screen_tree: MenuScreen, data: dict = None, displayFunc: callable = None):
        self.path = []
        self.screen_tree = screen_tree
        self.current_screen = screen_tree
        self.data = data or {}
        self.displayFunc = displayFunc
    
    def display(self):
        Util.clearScreen()
        if self.displayFunc:
            self.displayFunc(self)
        print()
        self.current_screen.display(self)

    def start(self):
        while True:
            self.display()
            result = self.current_screen.handle(self)
            if result is not None:
                return result
    
    def back(self):
        if self.path:
            self.path.pop()
            self.current_screen = self.screen_tree
            for step in self.path:
                self.current_screen = self.current_screen.children[step]
