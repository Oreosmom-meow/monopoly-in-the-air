import SQL_functions
import Game_functions
import colors
import connector
# class
class GameState:
    def __init__(self):
        self.rounds = 1
        self.doubles = 0
        self.jail_card = 0
        self.jail_counter = 0
        self.jailed = False
        self.username = ''
        self.position = 0
        self.session_id = 0
        self.score = 0
status = GameState()
# get connection time
connector.print_connection_time()
# set up username
status.username = input('Enter your username: ')
Game_functions.check_username(status)
#set up session specific board
SQL_functions.set_board_airports(status.session_id)
SQL_functions.set_player_property(status.session_id)
# position move and rounds up
while status.rounds <= 20:
    money = SQL_functions.get_money(status.session_id)
    if money <= 0:
        Game_functions.bankrupt(status.session_id)
        break
    else:
        if status.jailed:
            Game_functions.jail_event(status)
        else:
            Game_functions.print_player_property(status)
            userinput = input(f'{colors.col.BOLD}Roll the dice 🎲 to move. Press any key to roll. {colors.col.END}')
            Game_functions.developer_privileges(userinput, status)
            dice_roll_1,dice_roll_2,status = Game_functions.roll_and_move(status)
            Game_functions.dice_roll_result(dice_roll_1, dice_roll_2, status)
            if Game_functions.check_if_double(dice_roll_1, dice_roll_2, status):
                status.doubles += 1
            else:
                if status.doubles >= 2:
                    Game_functions.roll_double(status)
                    Game_functions.jail_event(status)
                else:
                    status.doubles = 0
                    temp_type_id = SQL_functions.get_type_id(status.position)
                    # Non-functional cells
                    if temp_type_id == 0:
                        Game_functions.non_functional_cell(status)
                    # airport cell
                    elif temp_type_id == 1:
                        Game_functions.airport_cell(status)
                    # Other cells
                    elif temp_type_id == 2:
                        Game_functions.chance_card(status)
                    elif temp_type_id == 3:
                        Game_functions.go_to_jail(status)
                    elif temp_type_id == 4:
                        Game_functions.income_tax(status.session_id)
                    elif temp_type_id == 5:
                        Game_functions.luxury_tax(status.session_id)
#wininig of game
if  status.rounds > 20:
    Game_functions.print_won_game(status)
    Game_functions.print_high_score(status)