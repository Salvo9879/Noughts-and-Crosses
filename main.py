
# Developed by Salvatore La Paglia
# Copyright (c) 2022 Salvo9879
# See license for more information

# https://github.com/Salvo9879/Noughts-and-Crosses

import random
import math
import os
import re



#* ==================================================================================================================================================


# Configurable settings
DICTATE_HEADER_FROM_TERMINAL = True
HEADER_MAX_LENGTH = 100
DISABLE_COLOR_DATA = False
ALLOW_SCREEN_RESETS = True


if DICTATE_HEADER_FROM_TERMINAL:
    try:
        HEADER_MAX_LENGTH = os.get_terminal_size()[0] 
    except:
        pass

    HEADER_MAX_LENGTH = HEADER_MAX_LENGTH

WINNING_INDEXES = {
    'h': '012345678',
    'v': '036147258',
    'd': '048246'
}


#* ==================================================================================================================================================



class Visuals():
    def __init__(self) -> None:
        self.p1 = '\033[94m' # Blue
        self.p2 = '\033[35m' # Magenta

        self.caution = '\033[93m' # Yellow
        self.success = '\033[92m' # Green

        self.title = '\033[96m' # Cyan
        self.header = '\033[1m' # Bold

        self.important_u = '\033[4m' # Underline
        self.important_b = '\033[1m' # Bold

        self.reset = '\033[0m' # Reset styles

        if DISABLE_COLOR_DATA:
            for attr in self.__dict__:
                setattr(self, attr, '')

    def remove_ansi(self, ansi_value: str):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', ansi_value)

        return result



#* ==================================================================================================================================================



class GameObjects():
    """ Contains any 'game objects' which are used multiple times. """

    def __init__(self) -> None:
        self.visuals = Visuals()

    def header(self, title=None, newlines=True, clear_screen=True):
        newlines_s = ''
        if newlines:
            newlines_s = '\n'

        if ALLOW_SCREEN_RESETS and clear_screen:
            os.system('cls')

        if title is None:
            return f"{self.visuals.header}{newlines_s}{'='*HEADER_MAX_LENGTH}{newlines_s}{self.visuals.reset}"
        
        title_len = len(f" {title} ")
        header_len = HEADER_MAX_LENGTH - title_len
        half_len = math.trunc(header_len / 2)
        
        header = f"{self.visuals.header}{newlines_s}{'='*half_len} {title} {'='*half_len}{newlines_s}{self.visuals.reset}"

        return header

    def yn_choice(self, msg, callback1 = None, callback2 = None, type_='callback'):
        error_occurred = False 
        while True: 
            if error_occurred:
                query = input(msg)
            else:
                query = input(f"{self.visuals.important_u}{msg} (y/n){self.visuals.reset} ")
            if type_ == 'callback':
                if callback1 is None and callback2 is None:
                    raise AttributeError('Attribute \'callback1\' & \'callback2\' are set to None whilst \'type_\' is running in callback.')

                if query == 'y':
                    callback1()
                    break
                elif query == 'n':
                    callback2()
                    break
                else:
                    msg = f"{self.visuals.caution}Please only enter \'y\' or \'n\'. {self.visuals.reset}"
                    error_occurred = True
                    continue
            if type_ == 'boolean':
                if query not in ['y', 'n']:
                    msg = f"{self.visuals.caution}Please only enter \'y\' or \'n\'. {self.visuals.reset}"
                    error_occurred = True
                    continue
                
                return query == 'y'
            raise AttributeError('Attribute \'type_\' must be either \'callback\' or \'boolean\'')
            

    def continue_phase(self, callback):
        if len(input(f"{self.visuals.important_b}\nPress Enter to continue!{self.visuals.reset} "))>=0:
            if callback is None:
                return
            callback()

    def title(self):
        return f"""{self.visuals.title}
         _   _                   _     _                   _____                              
        | \ | |                 | |   | |         ___     / ____|                             
        |  \| | ___  _   _  __ _| |__ | |_ ___   ( _ )   | |     _ __ ___  ___ ___  ___  ___  
        | . ` |/ _ \| | | |/ _` | '_ \| __/ __|  / _ \/\ | |    | '__/ _ \/ __/ __|/ _ \/ __| 
        | |\  | (_) | |_| | (_| | | | | |_\__ \ | (_>  < | |____| | | (_) \__ \__ \  __/\__ \\
        |_| \_|\___/ \__,_|\__, |_| |_|\__|___/  \___/\/  \_____|_|  \___/|___/___/\___||___/ 
                            __/ |                                                             
                           |___/                                                               
        {self.visuals.reset}"""



#* ==================================================================================================================================================



class Board():
    def __init__(game) -> None:
        game.go = GameObjects()
        game.visuals = game.go.visuals

        game.p1 = {'id': 0, 'name': 'Player 1', 'object': 'x', 'color': game.visuals.p1, 'wins': 0}
        game.p2 = {'id': 1, 'name': 'Player 2', 'object': 'o', 'color': game.visuals.p2, 'wins': 0}

        game.current_player = None
        game.running = False
        game.winner = None
        game.display_help = False

        game.metadata = [[' ', ' ', ' ',], [' ', ' ', ' '], [' ', ' ', ' ']]

    def reset_board(game):
        new_md = []
        for row in game.metadata:
            row_md = []
            for i in range(0, 3, 1):
                row_md.append(' ')
            new_md.append(row_md)
        
        game.metadata = new_md
                


    def config_draw(game):
        row_md = ''
        for row in game.metadata:
            for space in row:
                space = game.visuals.remove_ansi(space)
                if space in [game.get_player_by_id(0)['object'], game.get_player_by_id(1)['object']]:
                    row_md += '1'
                    continue
                row_md = '0'
        
        return '111111111' in row_md

    def configure_win(game):
        winning_md = []
        for index in WINNING_INDEXES:
            row_md = ''
            for row in game.metadata:
                for space in row:
                    space = game.visuals.remove_ansi(space)
                    if space == game.current_player['object']:
                        row_md += '1'
                        continue
                    row_md += '0'
                row_md += ' '

            row_md = row_md.replace(' ', '')

            directed_md = ''
            for direction in WINNING_INDEXES[index]:
                directed_md += row_md[int(direction)]

            directed_md = ' '.join(directed_md[i:i+3] for i in range(0, len(directed_md), 3))

            winning_md.append('111' in directed_md)

        return True in winning_md



    def next_player(game):
        if game.current_player is None:
            game.current_player = game.get_player_by_id(random.randint(0,1))
            return
        
        if game.current_player == game.p1:
            game.current_player = game.p2
            return

        game.current_player = game.p1
    
    def get_player_by_id(game, id_):
        if id_ == 0:
            return game.p1
        return game.p2

    def set_settings(game):
        print(game.go.header('What\'s your name?'))
        p1_name = input(f"{game.visuals.important_u}Player 1, what\'s your name?{game.visuals.reset} ").strip()
        if len(p1_name) > 0:
            game.p1['name'] = p1_name
        print(f"Welcome {game.p1['name']}!\n")
        
        p2_name = input(f"{game.visuals.important_u}Player 2, what\'s your name?{game.visuals.reset} ")
        if len(p2_name) > 0:
            game.p2['name'] = p2_name
        print(f"Welcome {game.p2['name']}!\n")

        game.display_help = game.go.yn_choice('Would you like to display help whilst playing?', type_='boolean')
        game.go.continue_phase(game.start_game)
        


    def display_board(game, rules=False, help_=False):
        md = game.metadata
        if rules:
            md = [['1', '2', '3',], ['4', '5', '6',], ['7', '8', '9']]

        if help_:
            h_md = [['1', '2', '3',], ['4', '5', '6',], ['7', '8', '9']]
            print(
                f"         |         |         " +                                ' '*20 + f"         |         |         \n" +f"    {md[0][0]}    |    {md[0][1]}    |    {md[0][2]}    " +     ' '*20 + f"    {h_md[0][0]}    |    {h_md[0][1]}    |    {h_md[0][2]}    \n" +f"         |         |       " +                                  ' '*20 + f"           |         |         \n" +f"---------|---------|---------" +                                ' '*20 + f"---------|---------|---------\n" +f"         |         |       " +                                  ' '*20 + f"           |         |       \n" +f"    {md[1][0]}    |    {md[1][1]}    |    {md[1][2]}    " +     ' '*20 + f"    {h_md[1][0]}    |    {h_md[1][1]}    |    {h_md[1][2]}    \n" +f"         |         |       " +                                  ' '*20 + f"           |         |       \n" +f"---------|---------|---------" +                                ' '*20 + f"---------|---------|---------\n" +f"         |         |       " +                                  ' '*20 + f"           |         |       \n" +f"    {md[2][0]}    |    {md[2][1]}    |    {md[2][2]}    " +     ' '*20 + f"    {h_md[2][0]}    |    {h_md[2][1]}    |    {h_md[2][2]}    \n" +f"         |         |       " +                                  ' '*20 + f"           |         |       \n")
            return
        print(f"         |         |         \n" +                           f"    {md[0][0]}    |    {md[0][1]}    |    {md[0][2]}    \n" +f"         |         |       \n" +                             f"---------|---------|---------\n" +                           f"         |         |       \n" +                             f"    {md[1][0]}    |    {md[1][1]}    |    {md[1][2]}    \n" +f"         |         |       \n" +                             f"---------|---------|---------\n" +                           f"         |         |       \n" +                             f"    {md[2][0]}    |    {md[2][1]}    |    {md[2][2]}    \n" +f"         |         |       \n")                           
        


    def convert_to_pos(game, pos_id):
        data = {
            '1': [0, 0],
            '2': [0, 1],
            '3': [0, 2],

            '4': [1, 0],
            '5': [1, 1],
            '6': [1, 2],

            '7': [2, 0],
            '8': [2, 1],
            '9': [2, 2]
        }

        return data[pos_id]

    def is_pos_empty(game, pos):
        return game.metadata[pos[0]][pos[1]] == ' '
            
    def set_pos(game, pos):
        game.metadata[pos[0]][pos[1]] = f"{game.current_player['color']}{game.current_player['object']}{game.visuals.reset}"


    def clear_screen(game):
        os.system('cls')

    def start_game(game):
        game.reset_board()
        game.running = True
        game.next_player()

        print(game.go.header('Play!'))

        while game.running:
            game.clear_screen()
            game.display_board(help_=game.display_help)
            print(f"{game.current_player['name']} it is your go. (Enter a number between 1-9).")
            pos_id = input('>>>')

            testing = True
            error_occurred = False
            while testing:
                if error_occurred:
                    pos_id = input('>>>')
                
                try:
                    int(pos_id)
                except:
                    print(f"{game.visuals.caution}Please enter a number between 1 & 9.{game.visuals.reset}")
                    error_occurred = True
                    continue

                if int(pos_id) > 9:
                    print(f"{game.visuals.caution}{pos_id} is too big. Choose a number between 1 & 9.{game.visuals.reset}")
                    error_occurred = True
                    continue

                if int(pos_id) < 1:
                    print(f"{game.visuals.caution}{pos_id} is too small. Choose a number between 1 & 9.{game.visuals.reset}")
                    error_occurred = True
                    continue

                pos = game.convert_to_pos(pos_id)

                if not game.is_pos_empty(pos):
                    print(f"{game.visuals.caution}This space is occupied by '{game.metadata[pos[0]][pos[1]]}{game.visuals.caution}'{game.visuals.reset}")
                    error_occurred = True
                    continue

                testing = False

            game.set_pos(pos)
            if game.configure_win():
                game.end_game('win')
            if game.config_draw():
                game.end_game('draw')
            
            game.next_player()

    def display_scoreboard(game):
        print(game.go.header('Scoreboard'))

        print(f"{game.p1['name']} wins: {game.p1['wins']}")
        print(f"{game.p2['name']} wins: {game.p2['wins']}\n")

        if game.p1['wins'] > game.p2['wins']:
            print(f"{game.visuals.success}{game.p1['name']} is in the lead!{game.visuals.reset}")
        elif game.p1['wins'] < game.p2['wins']:
            print(f"{game.visuals.success}{game.p2['name']} is in the lead!{game.visuals.reset}")
        elif game.p1['wins'] == game.p2['wins']:
            print(f"{game.visuals.success}{game.p1['name']} and {game.p2['name']} are drawing!{game.visuals.reset}")

        print(game.go.header(clear_screen=False))

        game.go.continue_phase(game.replay_game)

    def replay_game(game):
        game.go.yn_choice('Would you like to play each other again?', game.start_game, game.exit_game)

    def end_game(game, type_):
        game.running = False
        game.winner = game.current_player

        game.get_player_by_id(game.winner['id'])['wins'] += 1

        header_msg = 'We have a winner!'
        end_msg = f"Congratulations to {game.winner['name']}!"

        if type_ == 'draw':
            header_msg = 'Everyone\'s a winner!'
            end_msg = f"Congratulations to both of you!!"
        
        print(game.go.header(header_msg))
        game.display_board()
        print(f"{game.visuals.success}{end_msg}{game.visuals.reset}")

        game.go.continue_phase(game.display_scoreboard)

    def show_rules(game):
        print(game.go.header('Rules'))
        game.display_board(rules=True)
        print('This is the board, each square is given a number. When playing the game will ask you what letter you want to play your naught or cross. If the space is empty then you can place your object there.')
        game.go.continue_phase(game.set_settings)

    def exit_game(game):
        print(game.go.header('See you later!'))
        print('Thank you very much for playing')
        print('Developed by Salvatore La Paglia')

        print('\nCopyright (c) 2022 Salvo9879')
        print('See \'https://github.com/Salvo9879/Noughts-and-Crosses\'')

        game.go.continue_phase(exit)

    def intro(game):
        os.system('cls')
        print(game.go.title())
        print(game.go.header('Welcome', clear_screen=False))
        print('Welcome to noughts & crosses')
        game.go.yn_choice('Would you like to see the rules?)', game.show_rules, game.set_settings, type_='callback')


b = Board()
if __name__ == '__main__':
    b.intro()
