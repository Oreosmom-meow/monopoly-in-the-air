import random
import SQL_functions
import colors
import connector
import time

def dice_roll(): # iida
    dice = random.randint(1, 6)
    return dice

def income_tax(session_id): # iida
    input(f'You have landed on income tax cell. Press any key to continue. ')
    money = SQL_functions.get_money(session_id)
    temp_money = money
    money -= round(50 + money * 0.25)
    SQL_functions.modify_money(money,session_id)
    print(f'{colors.col.BOLD}{colors.col.YELLOW}Income tax!', f'You paid {temp_money - money} in taxes.\nYou have ${money} left.', f'{colors.col.END}')

def luxury_tax(session_id): # iida
    input(f'You have landed on luxury tax cell. Press any key to continue.')
    money = SQL_functions.get_money(session_id)
    temp_money = money
    money -= round(100 + money * 0.5)
    SQL_functions.modify_money(money,session_id)
    print(f'{colors.col.BOLD}{colors.col.YELLOW}Luxury tax!', f'You paid ${temp_money - money} in taxes.\n', f'{colors.col.END}')


def print_in_jail_message(status):
    money = SQL_functions.get_money(status.session_id)
    print(f'-------------------------------------------------------------------------')
    print(f'{colors.col.BOLD}{colors.col.YELLOW}You are in jail.', f'{colors.col.END}')
    print(
        f'{colors.col.BOLD}{colors.col.YELLOW}Type "1" to roll the dice and get doubles to get out. You have {3 - status.jail_counter} rolls left until automatic release.',
        f'{colors.col.END}')
    print(f'{colors.col.BOLD}{colors.col.YELLOW}Type "2" to pay a fine of 200 to get out.', f'{colors.col.END}')
    if money <= 200:
        print(f'{colors.col.BOLD}{colors.col.RED}Paying the fine would lead you to bankruptcy.', f'{colors.col.END}')
    print(f'{colors.col.BOLD}{colors.col.YELLOW}Type "3" to use a get out of jail free card to get out.',
          f'{colors.col.END}')
    print(f'-------------------------------------------------------------------------')


def check_if_double(dice_roll_1, dice_roll_2, status):
    if dice_roll_1 == dice_roll_2:
        status.double = True
    elif dice_roll_1 != dice_roll_2:
        status.double = False
    return status.double

def release(status):
    status.jailed = False
    status.jail_counter = 0

def jail_event(status): # iida
    jailcard = SQL_functions.check_jail_card(status.session_id)
    print_in_jail_message(status)
    while status.jailed:
        choice = input('Enter your choice: ')
        if choice != '1' and choice != '2' and choice != '3':
            print('Try again, use "1", "2", or "3" to choose.')
        elif 1 > int(choice) < 3:
            print('Try again, use "1", "2", or "3" to choose.')
        else:
            if choice == '1':
                dice_roll_1 = dice_roll()
                dice_roll_2 = dice_roll()
                print(f'You rolled {dice_roll_1} and {dice_roll_2}')
                status.rounds += 1
                if status.jail_counter > 2:
                    print(
                        f'{colors.col.GREEN}You have been automatically released after 3 attempts. Game continues.{colors.col.END}')
                    release(status)
                else:
                    if not check_if_double(dice_roll_1, dice_roll_2, status):
                        status.jail_counter += 1
                        print(f'{colors.col.BOLD}{colors.col.RED}Failed to roll a double. Still in jail.',
                              f'{colors.col.END}')
                    else:
                        print(
                            f'{colors.col.BOLD}{colors.col.GREEN}You have been released for rolling a double.' + f'{colors.col.END}')
                        release(status)
            elif choice == '2':
                money = SQL_functions.get_money(status.session_id)
                money -= 200
                SQL_functions.modify_money(money, status.session_id)
                print(
                    f'{colors.col.BOLD}{colors.col.GREEN} You have spent 200 to be released, you currently have ${money} left.',
                    f'{colors.col.END}')
                release(status)
            else:
                if SQL_functions.check_jail_card(status.session_id) > 0:
                    print('bee(the insect) free!')
                    release(status)
                    status.jailcard -= 1
                    SQL_functions.modify_out_of_jail_card(jailcard, status.session_id)
                else:
                    print("You don't have jailed card to use")

def salary(status): # iida
    money = SQL_functions.get_money(status.session_id)
    owned_airport = SQL_functions.get_all_owned_airport(status.session_id,status.username)
    upgraded_airport = SQL_functions.get_upgraded_airport_number(status.session_id)
    temp_money = money
    temp_money += 200 + owned_airport * 10 + upgraded_airport * 25
    SQL_functions.modify_money(temp_money,status.session_id)
    print(f'{colors.col.BOLD}{colors.col.BLUE}You passed Go cell. Salary time! You earned:', f'{temp_money - money:.0f}. Because you owned {owned_airport} airports and upgraded {upgraded_airport} airports' + f'{colors.col.END}')

def buy_airport(status): #yutong
    temp_price = SQL_functions.get_airport_price(status.position)
    temp_money = SQL_functions.get_money(status.session_id) - temp_price
    SQL_functions.modify_money(temp_money,status.session_id)
    SQL_functions.modify_owner_to_user(status)

def sell_airport(status): # roberto
    temp_money = SQL_functions.get_money(status.session_id)
    upgrade_level = SQL_functions.get_upgrade_status(status)
    if upgrade_level == 3:
        temp_money = temp_money + (SQL_functions.get_airport_price(status.session_idposition) * 0.5 * 0.75)
        SQL_functions.modify_money(temp_money,status.session_idsession_id)
        temp_level = upgrade_level - 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 2:
        temp_money = temp_money + (SQL_functions.get_airport_price(status.position) * 0.5 * 0.5)
        SQL_functions.modify_money(temp_money,status.session_id)
        temp_level = upgrade_level - 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 1:
        temp_money = temp_money + (SQL_functions.get_airport_price(status.position) * 0.5 * 0.25)
        SQL_functions.modify_money(temp_money,status.session_id)
        temp_level = upgrade_level - 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 0:
        temp_money = temp_money +  (SQL_functions.get_airport_price(status.position) * 0.5)
        SQL_functions.modify_money(temp_money,status.session_id)
        SQL_functions.modify_owner_to_bank(status.position,status.session_id)
        print(f'You have sold this airport to the bank')
    else:
        pass

def get_sell_price(status):
    upgrade_level = SQL_functions.get_upgrade_status(status)
    temp_money = SQL_functions.get_money(status.session_id)
    if upgrade_level == 0:
        temp_money = (SQL_functions.get_airport_price(status.position) * 0.5)
        #print(f'Selling this airport will get you ${temp_money}')
    elif upgrade_level == 1:
        temp_money = (SQL_functions.get_airport_price(status.position) * 0.5 * 0.25)
        #print(f'Selling this level will get you ${temp_money}')
    elif upgrade_level == 2:
        temp_money = (SQL_functions.get_airport_price(status.position) * 0.5 * 0.5)
        #print(f'Selling this level will get you ${temp_money}')
    return temp_money

def upgrade_airport(status): # roberto
    #   get_airport_price(position)
    upgrade_level = SQL_functions.get_upgrade_status(status)
    temp_price = SQL_functions.get_airport_price(status.position)
    if upgrade_level == 0:
        temp_money = SQL_functions.get_money(status.session_id) - 25% temp_price
        SQL_functions.modify_money(temp_money,status.session_id)
        temp_level = upgrade_level + 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'{colors.col.BOLD}{colors.col.GREEN}You have successfully upgraded to level {SQL_functions.get_upgrade_status(status)}.{colors.col.END}')
    elif upgrade_level == 1:
        temp_money = SQL_functions.get_money(status.session_id) - 50% temp_price
        SQL_functions.modify_money(temp_money,status.session_id)
        temp_level = upgrade_level + 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'{colors.col.BOLD}{colors.col.GREEN}You have successfully upgraded to level {SQL_functions.get_upgrade_status(status)}.{colors.col.END}')
    elif upgrade_level == 2:
        temp_money = SQL_functions.get_money(status.session_id) - 75% temp_price
        SQL_functions.modify_money(temp_money,status.session_id)
        temp_level = upgrade_level + 1
        SQL_functions.modify_airport_status(status.position, temp_level,status.session_id)
        print(f'{colors.col.BOLD}{colors.col.GREEN}You have successfully upgraded to level {SQL_functions.get_upgrade_status(status)}.{colors.col.END}')


def price_to_upgrade(status):
    upgrade_level = SQL_functions.get_upgrade_status(status)
    temp_price = SQL_functions.get_airport_price(status.position)
    if upgrade_level == 0:
        temp_money =  25% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    elif upgrade_level == 1:
        temp_money = 50% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    elif upgrade_level == 2:
        temp_money = 75% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    return temp_money

def chance_card(status): # yutong
    input(f'You have landed on chance cell. You will randomly select a card from the deck. Press any key to continue.')
    card_id = random.randint(1, 10)
    temp_money = SQL_functions.get_money(status.session_id)
    if card_id == 1:
        print(f'You picked card: Advance to "Go". You will get $200. Congratulations.')
        salary(status)
        status.position = 1
    elif card_id == 2:
        print(f'You picked card: Get out of jail. You can use it for once when you are in jail.')
        jail_card = SQL_functions.check_jail_card(status.session_id)
        jail_card += 1
        SQL_functions.modify_out_of_jail_card(jail_card,status.session_id)
    elif card_id == 3:
        print(f'You picked card: Go to jail. You will be moved to jail immediately.')
        jail_event(status)
        status.position = 17
    elif card_id == 4:
        temp_money = temp_money + 50
        print(f'You picked card: Bank pays you 50! You will get $50 from the bank, congratulations!')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 5:
        punishment = SQL_functions.get_all_owned_airport(status.session_id,status.username) * 25 + SQL_functions.get_upgraded_airport_number(status.session_id) * 50
        temp_money = temp_money - punishment
        print(f'You picked card: Pay repair fee for all properties. You need to pay $25 for all airports you own, $50 for all the upgraded airports you own. You need to pay in total ${punishment}.')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 6:
        temp_money = SQL_functions.get_money(status.session_id) - 50
        print(f'You picked card: Doctor fee. You need to pay $50 to the doctor.')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 7:
        temp_money = SQL_functions.get_money(status.session_id) + 50
        print(f'You picked card: Grand opening night. You will get $50 from the bank. Congratulations.')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 8:
        temp_money = SQL_functions.get_money(status.session_id) - 50
        print(f'You picked card: School fee. You need to pay $50 to the school.')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 9:
        temp_money = SQL_functions.get_money(status.session_id) + 25
        print(f'You picked card: Receive consultancy fee. You will get $25 from the bank. Congratulations.')
        SQL_functions.modify_money(temp_money,status.session_id)
    elif card_id == 10:
        temp_money = SQL_functions.get_money(status.session_id) - 50
        print(f'You picked card: Elected as chairman of the board. You need to pay $50 to the bank.')
        SQL_functions.modify_money(temp_money,status.session_id)
    return status.position

def bankrupt(session_id):
    print(f'😵😵😵😵😵😵😵😵😵😵😵😵😵😵😵😵😵😵😵')
    print(f'{colors.col.BOLD}{colors.col.RED}You are bankrupt 💸!  \nGAME OVER', f'{colors.col.END}')
    SQL_functions.clear_tables(session_id)

def developer_privileges(devcheat,status):
    if devcheat == "developer privileges":
        print("Developer mode activated")
        command = input()
        if command == "rounds":
            roundnumber = int(input())
            status.rounds = roundnumber
        elif command == "money":
            moneynumber = int(input())
            SQL_functions.modify_money(moneynumber, status.session_id)
        elif command == "jail":
            status.jailed = True
        elif command == "own_all":
            SQL_functions.cheat_owner_to_user(status)
        elif command == "almighty":
            SQL_functions.modify_money(1000000, status.session_id)
            SQL_functions.cheat_owner_to_user(status)
        elif command == 'end with money':
            temp_money = random.randint(500, 50000)
            SQL_functions.modify_money(temp_money, status.session_id)
            status.rounds = 22
        elif command == 'position':
            status.position = int(input())

def print_player_property(status):
    print(f'{colors.col.BOLD}{colors.col.PINK}━━━━━━━━━━━━━━━━━━━━━{colors.col.END}' + '\n')
    print(f'{colors.col.BOLD}{colors.col.PINK}Round: {status.rounds} | Position: {status.position}{colors.col.END}')
    country_list, airport_number = SQL_functions.get_all_country_name_and_number(status)
    jail_card = SQL_functions.check_jail_card(status.session_id)
    length = len(country_list)
    money = SQL_functions.get_money(status.session_id)
    print(f'{colors.col.CYAN}---------Player Property---------{colors.col.END}')
    print(f'{colors.col.BOLD}💰Money: {colors.col.CYAN}${money}{colors.col.END}')
    print(f'🃏Jail card: {colors.col.CYAN}{jail_card}{colors.col.END}')
    if length == 0:
        print(f"{colors.col.BOLD}🛬Properties:{colors.col.CYAN} 0{colors.col.END} {colors.col.END}")
        print(f'{colors.col.CYAN}--------------------------------{colors.col.END}')
    else:
        print(f'{colors.col.BOLD}🛬Properties: {colors.col.END}')
        max_country_length = max(len(country) for country in country_list) + 2
        print(f'{colors.col.BOLD}{"Country":<{max_country_length}} | Number of airports 🛬 owned{colors.col.END}')
        for i in range(length):
            print(f'{colors.col.CYAN}{country_list[i]:<{max_country_length}} | {airport_number[i]}{colors.col.END}')
        print(f'{colors.col.CYAN}--------------------------------{colors.col.END}')

def print_won_game(status):
    print(f'👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑')
    print(f'{colors.col.BOLD}{colors.col.PINK}You have won!{colors.col.END}')
    print(f'{colors.col.BOLD}{colors.col.CYAN}You ended the game with:',
          f'${SQL_functions.get_money(status.session_id):.0f}')
    print(f"You finished the game in {round(time.time() - connector.get_start_time())} seconds")
    money = SQL_functions.get_money(status.session_id)
    airport = SQL_functions.get_all_owned_airport(status.session_id, status.username)
    upgrade_airport_number = SQL_functions.get_upgraded_airport_number(status.session_id)
    status.score = round(money + airport * 5 + upgrade_airport_number * 10)
    print(f'{colors.col.BOLD}{colors.col.GREEN}Your score is:', status.score, f'{colors.col.END}')

def print_high_score(status):
    SQL_functions.insert_high_score(status.session_id, status.score)
    top_player, top_score, session_list = SQL_functions.get_top_high_score()
    if status.session_id in session_list:
        rank = session_list.index(status.session_id) + 1
        print(f'You ranked {rank} in the top 5 high scores.')
    elif status.session_id not in session_list:
        print(f"You didn't make it to the top 5 high scores.")
    index = 0
    name_length = max(len(name) for name in top_player) + 2
    print(f'{colors.col.PINK}{"USER":<{name_length}}| {colors.col.END}', f'{colors.col.PINK}SCORE{colors.col.END}')
    while index < len(top_score):
        print(f'{top_player[index]:<{name_length}}|  {top_score[index]}')
        index += 1
    SQL_functions.clear_tables(status.session_id)

def go_to_jail(status):
    input(f'You will be sent to jail immediately. :)) Press any key to continue.')
    status.jailed = True
    status.position = 17

def roll_double(status):
    print(f'{colors.col.BOLD}{colors.col.RED}You have been jailed 🧱 for rolling doubles twice in a row.{colors.col.END}')
    status.jailed = True
    status.doubles = 0

def dice_roll_result(dice_roll_1,dice_roll_2,status):
    print(f'You rolled 🎲:', f'{dice_roll_1}, {dice_roll_2}', f'| {colors.col.PINK}You moved to cell number:',f'{status.position}{colors.col.END}')

def rounds_up(status):
    print(f'You finished one round of the game. Now rounds + 1. Position starts from 0.')
    salary(status)
    status.rounds += 1
    status.position = status.position - 21

def airport_cell(status):
    airport_price = SQL_functions.get_airport_price(status.position)
    country_name = SQL_functions.get_country_name(status)
    airport_name = SQL_functions.get_airport_name(status)
    temp_money = SQL_functions.get_money(status.session_id)
    input(
        f'You have landed on {colors.col.BOLD}{colors.col.CYAN}{airport_name}{colors.col.END} from {colors.col.BOLD}{colors.col.CYAN}{country_name}{colors.col.END}. The airport price is {colors.col.CYAN}${airport_price}{colors.col.END}. Press any key to continue.')
    owner = SQL_functions.check_airport_owner(status)
    # first check the owner of the airport
    if owner == status.username:
        upgrade_level = SQL_functions.get_upgrade_status(status)
        upgrade_choice = SQL_functions.check_owns_all_of_country(status)
        # print(upgrade_choice)
        if upgrade_choice:
            if upgrade_level == 3:
                print(
                    f'This airport is at level {upgrade_level} - you can not upgrade further ,The price to sell this level is ${get_sell_price(status)}')
            elif upgrade_level == 2:
                print(
                    f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(status)} ,The price to sell this level is ${get_sell_price(status)}')
            elif upgrade_level == 1:
                print(
                    f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(status)} ,The price to sell this level is ${get_sell_price(status)}')
            elif upgrade_level == 0:
                print(
                    f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(status)} ,The price to sell airport is ${get_sell_price(status)}')
            user_choice = input(f'Enter your choice: "s" for sell, "u" for upgrade, Enter to skip: ')
            if user_choice.lower() == "u":
                upgrade_airport(status)
            elif user_choice.lower() == "s":
                sell_airport(status)
        elif not upgrade_choice:
            print(f'The price to sell this level is ${get_sell_price(status)}')
            user_choice = input(f'Enter your choice: "s" for sell, Enter to skip: ')
            if user_choice.lower() == "s":
                sell_airport(status)
            else:
                pass
    elif owner == 'bank':
        rent = airport_price * 0.5
        temp_money = temp_money - rent
        SQL_functions.modify_money(temp_money, status.session_id)
        print(
            f'Bank owns {colors.col.CYAN}{airport_name}{colors.col.END} and you need to pay rent to the bank at price of {colors.col.CYAN}${rent}{colors.col.END}. You currently have {temp_money} after paying the rent.')
    else:
        if temp_money > airport_price:
            print(f'{airport_name} is available for purchase. Do you want to buy it? (Y/N)')
            userinput = input().upper()
            if userinput == 'Y':
                buy_airport(status)
                temp_money = SQL_functions.get_money(status.session_id)
                SQL_functions.modify_money(temp_money, status.session_id)
                print(f'You purchased {airport_name} from {country_name} at price of ${airport_price}. Game continues. ')
            elif userinput == 'N':
                print("You choose to pass this airport without buying. Game continue.")
            else:
                print("Invalid input. Game continues.")
        else:
            print("You can't afford this airport yet. You will continue the game.")

def non_functional_cell(status):
    if status.position == 1 and status.rounds != 1:
        print(f'You have landed on Go cell. You will get $200 from the bank.')
    elif status.position == 1 and round == 1:
        print(f'You have started the game from GO cell.')
    elif status.position == 12:
        print(f'You have landed on Free Parking cell. You will pass.')
    elif status.position == 17:
        print(f'You have landed on Jail. You will pass.')

def roll_and_move(status):
    dice_roll_1 = random.randint(1, 6)
    dice_roll_2 = random.randint(1, 6)
    status.position += dice_roll_1 + dice_roll_2
    if status.position > 22:
        rounds_up(status)
    return dice_roll_1,dice_roll_2,status

def check_username(status):
    if status.username == '':
        print('Username cannot be empty.')
    elif status.username == 'bank':
        print('Username cannot be "bank"')
    else:
        SQL_functions.insert_username(status.username, connector.get_start_time())
        status.session_id = SQL_functions.get_session_id()
    print(f'Username confirmed as {status.username}, session id = {status.session_id}')