import Util
import keyboard

class Menu:

    def __init__(self):
        self.focus_idx = 0

    def prompt(self, prompt: str, options: list[str]) -> int:
        self.focus_idx = 0
        while True:
            Util.clearScreen()
            print(prompt)
            for i, option in enumerate(options):
                focus_symbol = '→' if i == self.focus_idx else ' '
                print(f'{focus_symbol} {i + 1}. {option}')
            keypress = keyboard.read_key()
            print(keypress)
            if keypress.isdigit():
                choice_idx = int(keypress) - 1
                if 0 <= choice_idx < len(options):
                    return choice_idx
            elif keypress in ['up', 'w']:
                self.focus_idx = (self.focus_idx - 1) % len(options)
            elif keypress in ['down', 's']:
                self.focus_idx = (self.focus_idx + 1) % len(options)
            elif keypress in ['enter', 'space']:
                return self.focus_idx