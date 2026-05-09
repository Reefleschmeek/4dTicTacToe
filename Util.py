ANSI_COLORS = {
    'red': '31', 'green': '32', 'blue': '34',
    'yellow': '33', 'magenta': '35', 'cyan': '36',
    'orange': '38;5;208', 'white': '37', 'black': '30',
}

def style(text: str, color: str = None, bold: bool = False) -> str:
    color_code = ANSI_COLORS.get(color, '37')
    bold_code = '1' if bold else '0'
    return f'\033[{bold_code};{color_code}m{text}\033[0m'

def clearScreen():
    print('\033[2J\033[H', end='', flush=True)