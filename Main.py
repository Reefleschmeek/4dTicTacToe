from Menu import Menu, MenuOptions, MenuInput, MenuCallback, MenuReturn, MenuNavigate
from Game import Game
import PlayerLoader
import readchar

def addPlayer(menu: Menu, player: str):
    menu.data['players'].append(player)

def clearPlayers(menu: Menu):
    menu.data['players'].clear()

def setBoardSize(menu: Menu, str: str):
    if not str.isdigit():
        return
    size = int(str)
    if size >= 2:
        menu.data['board_size'] = size

def setTimeLimit(menu: Menu, str: str):
    time_limit = int(str)
    if time_limit >= 0:
        menu.data['time_limit_ms'] = time_limit

def displayMenu(menu: Menu):
    print('Players:')
    if menu.data['players']:
        for i, player in enumerate(menu.data['players']):
            print(f'  {i + 1}. {player}')
    else:
        print('  None')
    print(f'Board Size: {menu.data['board_size']}')
    print(f'Time Limit: {menu.data['time_limit_ms']} ms')

menu_data = {
    'players': [],
    'board_size': 3,
    'time_limit_ms': 0,
}

menu_tree = MenuOptions(
    title = 'Main Menu',
    children = {
        'Start Game': MenuReturn('start'),
        'Settings': MenuOptions(
            title = 'Settings',
            children = {
                'Edit Players': MenuOptions(
                    title = 'Edit Players',
                    children = {
                        'Add Players': MenuOptions(
                            title = 'Choose Player to Add',
                            children = {
                                **{player: MenuCallback(
                                    lambda menu, player=player: addPlayer(menu, player),
                                ) for player in PlayerLoader.classes},
                                'Back': MenuNavigate('Settings', 'Edit Players')
                            },
                        ),
                        'Clear Players': MenuCallback(clearPlayers),
                        'Back': MenuNavigate('Settings'),
                    }
                ),
                'Set Board Size': MenuInput(
                    title = 'Enter board size (integer >= 2):',
                    handler = setBoardSize,
                ),
                'Set Time Limit': MenuInput(
                    title = 'Enter time limit in milliseconds (integer >= 0):',
                    handler = setTimeLimit,
                ),
                'Back': MenuNavigate(),
            },
        ),
        'Quit': MenuReturn('quit'),
    },
)

if __name__ == '__main__':

    ret = None

    while ret != 'quit':
    
        menu = Menu(menu_tree, menu_data, displayMenu)
        ret = menu.start()

        if ret == 'start':
            game = Game(
                players = [PlayerLoader.classes[player] for player in menu.data['players']],
                size = menu.data['board_size'],
                time_limit_ms = menu.data['time_limit_ms'],
            )
            game.play()
            print('Press any key to continue...')
            readchar.readkey()

