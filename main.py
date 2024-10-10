import random

import mysql.connector
from mysql.connector import cursor
import time
import threading
import testing
connectionstart = time.time()
# mysql connection
connection = mysql.connector.connect(
    user="yutongd",
    password="12345",
    host="mysql.metropolia.fi",
    port=3306,
    database="yutongd",
    connection_timeout=60,
    autocommit = True
)
connectedtime = time.time()
print(f'Connected to the database in {connectedtime - connectionstart} seconds.')

# classes
class col:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    PURPLE = '\033[100m'

# global variables
rounds = 1
position = 0
doubles = 0
jail_counter = 0
jailed = False
session_id = 0

#sql related functions
#def get_country_from_id
gamestart = time.time()
# set up username
while True:
    username = input('Enter your username: ')
    if username == '':
        print('Username cannot be empty.')
    elif username == 'bank':
        print('Username cannot be "bank"')
    else:
        sql = f"INSERT INTO game_sessions(player_name, money, out_of_jail_card, start_time) VALUES ('{username}', 200, 0, {gamestart});"
        cursor = connection.cursor()
        cursor.execute(sql)
        sql2= f'SELECT MAX(session_id) from game_sessions;'
        cursor = connection.cursor()
        cursor.execute(sql2)
        result = cursor.fetchall()
        session_id = result[0][0]
        break
print(f'Username confirmed as {username}, session id = {session_id}')
# set board airports (˶˃ ᵕ ˂˶) .ᐟ.ᐟ 
def set_board_airports():
    airportnumbers = (2,4,5,7,8,10,13,15,16,19,20,21)
    i = 0
    start = time.time()
    country_sql = f'SELECT DISTINCT iso_country FROM airport GROUP BY iso_country HAVING COUNT(*) >= 3 ORDER BY RAND() LIMIT 4;'
    cursor = connection.cursor()
    cursor.execute(country_sql)
    country_result = cursor.fetchall()
    for row in country_result:
        airport_sql = f'SELECT DISTINCT ident FROM airport WHERE iso_country = "{row[0]}" ORDER BY RAND() LIMIT 3;'
        cursor = connection.cursor()
        cursor.execute(airport_sql)
        airport_result = cursor.fetchall()
        for airport in airport_result:
            sql = f'INSERT INTO session_airp_count (airport_id, country_id, session_id, board_id) VALUES ("{airport[0]}", "{row[0]}", {session_id}, {airportnumbers[i]});'
            cursor = connection.cursor()
            cursor.execute(sql)
            i += 1
    end = time.time()
    print(f"Game database set up in {end - start} seconds.")
    return
set_board_airports()
#insert 12 new rows into player_property table without setting 3 random into bank owned
def set_player_property(session_id):
    airportnumbers = (2, 4, 5, 7, 8, 10, 13, 15, 16, 19, 20, 21)
    i = 0
    for x in airportnumbers:
        insert = f"INSERT INTO player_property (session_id, board_id, ownership, upgrade_status) values ({session_id}, {airportnumbers[i]}, NULL, 0);"
        cursor = connection.cursor()
        cursor.execute(insert)
        i += 1
    random_airport = random.choice(airportnumbers)
    select_country = f"select board_id from session_airp_count where country_id in (select country_id from session_airp_count where board_id = {random_airport}) and session_id = {session_id};"
    cursor = connection.cursor()
    cursor.execute(select_country)
    country_result = cursor.fetchall()
    for row in country_result:
        update_bank = f"update player_property set ownership = 'bank' where board_id = {row[0]} and session_id = {session_id};"
        cursor = connection.cursor()
        cursor.execute(update_bank)
    return
set_player_property(session_id)

def check_owns_all_of_country(position):

    country_id = testing.run(f"SELECT country_id FROM session_airp_count "
                             f"WHERE board_id = {position} "
                             f"AND session_id = {session_id};")[0][0]

    sql = (f"SELECT COUNT(p.board_id) FROM  player_property p "
           f"LEFT JOIN session_airp_count s ON p.board_id = s.board_id "
           f"WHERE s.session_id = {session_id} " 
           f"AND p.ownership = '{username}' "
           f"AND s.country_id = '{country_id}'"
           f"AND p.session_id = {session_id};")
    result = testing.run(sql)
    if result[0][0] == 3:
        return True
    else:
        return False
    print(result[0][0])

#-------- starting of Yutong's code
def clear_tables(session_id):
    sql1 = f"DELETE FROM session_airp_count where session_id = {session_id};"
    sql2 = f"DELETE FROM player_property where session_id = {session_id};"
    cursor = connection.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    print(f"{col.GREEN}Successfully deleted session:{session_id} related redundant tables.{col.END}")

def get_country_name(position):
    sql = f"select name from country join session_airp_count on iso_country = country_id WHERE session_airp_count.session_id = {session_id} and session_airp_count.board_id = {position};"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            country_name = row[0]
    return country_name

def get_all_country_name_and_number(session_id):
    country_names = []
    airport_numbers = []
    tempo_list = []
    sql2 = f"SELECT sa.country_id, COUNT(p.board_id) AS airport_count FROM player_property p JOIN session_airp_count sa ON p.board_id = sa.board_id AND p.session_id = sa.session_id WHERE p.session_id = {session_id}  AND p.ownership = '{username}' GROUP BY sa.country_id;"
    cursor = connection.cursor()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    if cursor.rowcount > 0:
        for key, value in result2:
            tempo_list.append(key)
            airport_numbers.append(value)
    for x in tempo_list:
        sql1 = f"SELECT DISTINCT(name) from country JOIN session_airp_count on iso_country = country_id WHERE session_airp_count.session_id = {session_id} and session_airp_count.country_id = '{x}'; "
        cursor = connection.cursor()
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        if cursor.rowcount > 0:
            for row in result1:
                name = row[0]
                country_names.append(name)
    return (country_names, airport_numbers)

def get_airport_name(position):
    sql = f"select name from airport join session_airp_count on ident = airport_id WHERE session_airp_count.session_id = {session_id} and session_airp_count.board_id = {position};"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airp_name = row[0]
    return airp_name

def get_money(session_id): #Yutong
    sql = f"select money from game_sessions where session_id = {session_id}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            money = row[0]
    return money

def get_airport_price(position):
    sql = f"select price from board where board_id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            price = row[0]
    return price

def get_type_id(position):
    sql = f"select type_id from board where board_id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            type_id = row[0]
    return type_id

def get_all_owned_airport(session_id):
    sql = f"select COUNT(ownership) from player_property where session_id = {session_id} and ownership = '{username}';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_number = row[0]
    return airport_number

def get_upgraded_airport_number(session_id):
    sql = f"select COUNT(ownership) from player_property where session_id = {session_id} and upgrade_status > 0"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_number = row[0]
    return upgrade_number

def get_upgrade_status(position):
    global session_id
    sql = f"select upgrade_status from player_property where session_id = {session_id} and board_id = {position} "
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_status = row[0]
    return upgrade_status

def check_airport_owner(position):
    sql = f"select ownership from player_property where board_id = {position} and session_id = {session_id}"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_owner = row[0]
    return airport_owner

def check_jail_card(session_id):
    sql = f"select out_of_jail_card from game_sessions where session_id = {session_id}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    card_number = result[0][0]
    return card_number

def modify_money(temp_money):
    update = f"update game_sessions set money = {temp_money} where session_id = {session_id}"
    cursor = connection.cursor()
    cursor.execute(update)
    get_money(session_id)

def modify_owner_to_user(position):
    update = (f"update player_property set ownership = '{username}' where board_id = {position} and session_id = {session_id}")
    cursor = connection.cursor()
    cursor.execute(update)

def cheat_owner_to_user(username):
    update = (f"update player_property set ownership = '{username}' where session_id = {session_id}")
    cursor  = connection.cursor()
    cursor.execute(update)

def modify_owner_to_bank(position):
    update = (f"update player_property set ownership = 'bank' where id = {position} and session_id = {session_id}")
    cursor = connection.cursor()
    cursor.execute(update)

def modify_out_of_jail_card(jail_card):
    global username
    sql = f"update game_sessions set out_of_jail_card = '{jail_card}' where session_id = {session_id}"
    cursor = connection.cursor()
    cursor.execute(sql)

def modify_airport_status(position, temp_status):
    global username
    sql = f"update player_property set upgrade_status = {temp_status} where board_id = {position} and session_id = {session_id}"
    cursor = connection.cursor()
    cursor.execute(sql)

def insert_high_score(session_id, score):
    sql = f"INSERT INTO high_score(session_id, score) VALUES ({session_id}, {score});)"
    cursor = connection.cursor()
    cursor.execute(sql)

def get_top_high_score(session_id):
    session_list = []
    player_name = []
    high_score = []
    if not connection.is_connected():
        connection.reconnect(attempts=3, delay=5)
    sql = f'select session_id,score from high_score ORDER by score DESC limit 5'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for id, score in result:
        session_list.append(id)
        high_score.append(score)
    for i in session_list:
        sql2 = f'select player_name from game_sessions where session_id = {i};'
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        for name in result2:
            player_name.append(name[0])
    return(player_name, high_score,session_list)


# functions
def dice_roll(): # iida
    dice = random.randint(1, 6)
    return dice

def income_tax(): # iida
    global username
    money = get_money(session_id)
    temp_money = money
    money -= round(50 + money * 0.25)
    modify_money(money)
    print(f'{col.BOLD}{col.YELLOW}Income tax!', f'You paid {temp_money - money} in taxes.\nYou have ${money} left.', f'{col.END}')

def luxury_tax(): # iida
    global username
    money = get_money(session_id)
    temp_money = money
    money -= round(100 + money * 0.5)
    modify_money(money)
    print(f'{col.BOLD}{col.YELLOW}Luxury tax!', f'You paid ${temp_money - money} in taxes.\n', f'{col.END}')

def jail_event(): # iida
    global jail_counter
    global jailed
    global username
    global rounds
    money = get_money(session_id)

    dice_roll_1 = dice_roll()
    dice_roll_2 = dice_roll()
    jailcard = check_jail_card(session_id)

    choosing = True
    print(f'{col.BOLD}{col.YELLOW}You are in jail.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "1" to roll the dice and get doubles to get out. You have {3 - jail_counter} rolls left until automatic release.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "2" to pay a fine of 200 to get out.', f'{col.END}')
    if money <= 200:
        print(f'{col.BOLD}{col.RED}Paying the fine would lead you to bankruptcy.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "3" to use a get out of jail free card to get out.', f'{col.END}')
    while choosing == True:
        choice = input('Enter your choice: ')
        if choice != '1' and choice != '2' and choice != '3':
            print('Try again, use "1", "2", or "3" to choose.')
        elif 1 > int(choice) < 3:
            print('Try again, use "1", "2", or "3" to choose.')
        else:
            choosing = False
    if choice == '1':
        print(f'Dice result: {dice_roll_1}, {dice_roll_2}')
        if dice_roll_1 != dice_roll_2 and jail_counter < 2:
            jail_counter += 1
            rounds += 1
            print(f'{col.BOLD}{col.RED}Failed to roll a double. Still in jail.', f'{col.END}')
        elif dice_roll_1 != dice_roll_2 and jail_counter >= 2:
            print(f'{col.GREEN}You have been automatically released after 3 attempts. Game continues.{col.END}')
            jailed = False
        elif dice_roll_1 == dice_roll_2:
            print(f'{col.BOLD}{col.GREEN}You have been released.' + f'{col.END}')
            jailed = False
            jail_counter = 0
    elif choice == '2':
        money -= 200
        modify_money(money)
        print(f'{col.BOLD}{col.GREEN} You have spent 200 to be released, you currently have ${money} left.', f'{col.END}')
        jailed = False
        jail_counter = 0
    else:
        if check_jail_card(session_id) > 0:
            print('bee(the insect) free!')
            jailed = False
            jail_counter = 0
            jailcard -= 1
            modify_out_of_jail_card(jailcard)
        else:
            print("nuh uh")

def salary(): # iida
    money = get_money(session_id)
    owned_airport = get_all_owned_airport(session_id)
    upgraded_airport = get_upgraded_airport_number(session_id)
    temp_money = money
    temp_money += 200 + owned_airport * 10 + upgraded_airport * 25
    modify_money(temp_money)
    print(f'{col.BOLD}{col.BLUE}You passed Go cell. Salary time! You earned:', f'{temp_money - money:.0f}. Because you owned {owned_airport} airports and upgraded {upgraded_airport} airports' + f'{col.END}')

def buy_airport(position): #yutong
    temp_price = get_airport_price(position)
    temp_money = get_money(session_id) - temp_price
    modify_money(temp_money)
    modify_owner_to_user(position)



def sell_airport(position): # roberto
    global username
    temp_money = get_money(session_id)
    upgrade_level = get_upgrade_status(position)
    if upgrade_level == 3:
        temp_money = temp_money + (get_airport_price(position) * 0.5 * 0.75)
        modify_money(temp_money)
        temp_level = upgrade_level - 1
        modify_airport_status(position, temp_level)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 2:
        temp_money = temp_money + (get_airport_price(position) * 0.5 * 0.5)
        modify_money(temp_money)
        temp_level = upgrade_level - 1
        modify_airport_status(position, temp_level)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 1:
        temp_money = temp_money + (get_airport_price(position) * 0.5 * 0.25)
        modify_money(temp_money)
        temp_level = upgrade_level - 1
        modify_airport_status(position, temp_level)
        print(f'You have downgraded this airport from {upgrade_level} to {temp_level}')
    elif upgrade_level == 0:
        temp_money = temp_money +  (get_airport_price(position) * 0.5)
        modify_owner_to_bank(position)
        print(f'You have sold this airport to the bank')
    else:
        pass

def get_sell_price(position):
    temp_money = get_money(session_id)
    if upgrade_level == 0:
        temp_money = (get_airport_price(position) * 0.5)
        #print(f'Selling this airport will get you ${temp_money}')
    elif upgrade_level == 1:
        temp_money = (get_airport_price(position) * 0.5 * 0.25)
        #print(f'Selling this level will get you ${temp_money}')
    elif upgrade_level == 2:
        temp_money = (get_airport_price(position) * 0.5 * 0.5)
        #print(f'Selling this level will get you ${temp_money}')
    return(temp_money)

def upgrade_airport(position): # roberto
    #   get_airport_price(position)
    get_upgrade_status(position)
    temp_price = get_airport_price(position)
    if upgrade_level == 0:
        temp_money = get_money(session_id) - 25% temp_price
        modify_money(temp_money)
        temp_level = upgrade_level + 1
        modify_airport_status(position, temp_level)
        print(f'{col.BOLD}{col.GREEN}You have successfully upgraded {airport_name} to level {get_upgrade_status(position)}.{col.END}')
    elif upgrade_level == 1:
        temp_money = get_money(session_id) - 50% temp_price
        modify_money(temp_money)
        temp_level = upgrade_level + 1
        modify_airport_status(position, temp_level)
        print(f'{col.BOLD}{col.GREEN}You have successfully upgraded {airport_name} to level {get_upgrade_status(position)}.{col.END}')
    elif upgrade_level == 2:
        temp_money = get_money(session_id) - 75% temp_price
        modify_money(temp_money)
        temp_level = upgrade_level + 1
        modify_airport_status(position, temp_level)
        print(f'{col.BOLD}{col.GREEN}You have successfully upgraded {airport_name} to level {get_upgrade_status(position)}.{col.END}')


def price_to_upgrade(position):
    get_upgrade_status(position)
    temp_price = get_airport_price(position)
    if upgrade_level == 0:
        temp_money =  25% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    elif upgrade_level == 1:
        temp_money = 50% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    elif upgrade_level == 2:
        temp_money = 75% temp_price
        #print(f'the price to upgrade is ${temp_money}')
    return(temp_money)


def chance_card(position): # yutong
    card_id = random.randint(1, 10)
    temp_money = get_money(session_id)
    if card_id == 1:
        print(f'You picked card: Advance to "Go". You will get $200. Congratulations.')
        salary()
        position = 1
    elif card_id == 2:
        print(f'You picked card: Get out of jail. You can use it for once when you are in jail.')
        jail_card = check_jail_card(session_id)
        jail_card += 1
        modify_out_of_jail_card(jail_card)
    elif card_id == 3:
        print(f'You picked card: Go to jail. You will be moved to jail immediately.')
        jail_event()
    elif card_id == 4:
        temp_money = temp_money + 50
        print(f'You picked card: Bank pays you 50! You will get $50 from the bank.Congratulations.')
        modify_money(temp_money)
    elif card_id == 5:
        punishment = get_all_owned_airport(session_id) * 25 + get_upgraded_airport_number(session_id) * 50
        temp_money = temp_money - punishment
        print(f'You picked card: Pay repair fee for all properties. You need to pay $25 for all airports you own, $50 for all the upgraded airports you own. You need to pay in total ${punishment}.')
        modify_money(temp_money)
    elif card_id == 6:
        temp_money = get_money(session_id) - 50
        print(f'You picked card: Doctor fee. You need to pay $50 to the doctor.')
        modify_money(temp_money)
    elif card_id == 7:
        temp_money = get_money(session_id) + 50
        print(f'You picked card: Grand opening night. You will get $50 from the bank. Congratulations.')
        modify_money(temp_money)
    elif card_id == 8:
        temp_money = get_money(session_id) - 50
        print(f'You picked card: School fee. You need to pay $50 to the school.')
        modify_money(temp_money)
    elif card_id == 9:
        temp_money = get_money(session_id) + 25
        print(f'You picked card: Receive consultancy fee. You will get $25 from the bank. Congratulations.')
        modify_money(temp_money)
    elif card_id == 10:
        temp_money = get_money(session_id) - 50
        print(f'You picked card: Elected as chairman of the board. You need to pay $50 to the bank.')
        modify_money(temp_money)

def board_location(position): # iida
    sql = f'select * from board where id = "{position}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]

# GAME START FUNCTION RUNNING
# MAIN FUNCTION
while rounds <= 20:
    money = get_money(session_id)
    if money <= 0:
        print(f'{col.BOLD}{col.RED}You are bankrupt 💸!  \nGAME OVER' , f'{col.END}☠️')
        clear_tables(session_id)
        break
    if jail_counter >= 3:
        jailed = False
        jail_counter = 0
    if jailed:
        jail_event()
        money = get_money(session_id)
        if money <= 0:
            print(f'{col.BOLD}{col.RED}You are bankrupt 💸!  \nGAME OVER', f'{col.END}')
            break
    print(f'{col.BOLD}{col.PINK}━━━━━━━━━━━━━━━━━━━━━{col.END}' + '\n')
    print(f'{col.BOLD}{col.PINK}Round: {rounds} | Position: {position}{col.END}')
    if not jailed:
        country_list, airport_number = get_all_country_name_and_number(session_id)
        jail_card = check_jail_card(session_id)
        length = len(country_list)
        print(f'{col.CYAN}---------Player Property---------{col.END}')
        print(f'{col.BOLD}💰Money: {col.CYAN}${money}{col.END}')
        print(f'🃏Jail card: {col.CYAN}{jail_card}{col.END}')
        if length == 0:
            print(f"{col.BOLD}🛬Properties:{col.CYAN} 0{col.END} {col.END}")
            print(f'{col.CYAN}--------------------------------{col.END}')
        else:
            print(f'{col.BOLD}🛬Properties: {col.END}')
            print(f'{col.BOLD}Country      | Number of airports 🛬 owned{col.END}')
            for i in range(length):
                print(f'{col.CYAN}{country_list[i]}      | {airport_number[i]}{col.END}')
            print(f'{col.CYAN}--------------------------------{col.END}')
        devcheat = input(f'{col.BOLD}Roll the dice 🎲 to move. Press any key to roll. {col.END}')
        if devcheat == "developer privileges":
            print("Developer mode activated")
            cheating = True
            command = input()
            if command == "rounds":
                roundnumber = int(input())
                rounds = roundnumber
            elif command == "money":
                moneynumber = int(input())
                modify_money(moneynumber)
            elif command == "jail":
                jailed = True
            elif command == "own_all":
                cheat_owner_to_user(session_id)
            elif command == "almighty":
                modify_money(1000000)
                cheat_owner_to_user(session_id)
            elif command == 'end with money':
                temp_money = random.randint(500,50000)
                modify_money(temp_money)
                rounds = 22

        dice_roll_1 = dice_roll()
        dice_roll_2 = dice_roll()
        if dice_roll_1 == dice_roll_2:
            doubles += 1
            if doubles >= 2:
                print(f'You rolled 🎲:', f'{dice_roll_1}, {dice_roll_2}')
                print(f'{col.BOLD}{col.RED}You have been jailed 🧱 for rolling doubles twice.{col.END}')
                jailed = True
                doubles = 0
            else:
                position += dice_roll_1 + dice_roll_2
                print(f'You rolled 🎲:', f'{dice_roll_1}, {dice_roll_2}', f'| You moved to cell number:', f'{position}')
        elif dice_roll_1 != dice_roll_2:
            position += dice_roll_1 + dice_roll_2
            print(f'You rolled 🎲:', f'{dice_roll_1}, {dice_roll_2}', f'| You moved to cell number:', f'{position}')
        else:
            break
        if position > 22:
            salary()
            rounds += 1
            position = position - 21
        temp_type_id = get_type_id(position)
        temp_money = get_money(session_id)
        #Non-airport cells
        if temp_type_id == 0 and jailed == False:
            if position == 1 and rounds != 1:
                print(f'You have landed on Go cell. You will get $200 from the bank.')
            elif position == 1 and round == 1:
                print(f'You have started the game from GO cell.')
            elif position == 12:
                print(f'You have landed on Free Parking cell. You will pass.')
            elif position == 17:
                print(f'You have landed on Jail. You will pass.')
        #airport cell
        elif temp_type_id == 1 and jailed == False:
            airport_price = get_airport_price(position)
            country_name = get_country_name(position)
            airport_name = get_airport_name(position)
            input(f'You have landed on {col.BOLD}{col.CYAN}{airport_name}{col.END} from {col.BOLD}{col.CYAN}{country_name}{col.END}. The airport price is {col.CYAN}${airport_price}{col.END}. Press any key to continue.')
            owner = check_airport_owner(position)
            #first check the owner of the airport
            if owner == username:
                upgrade_level = get_upgrade_status(position)
                upgrade_choice = check_owns_all_of_country(position)
                print(upgrade_choice,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                if upgrade_choice == True:
                    if upgrade_level == 3:
                        print(f'This airport is at level {upgrade_level} - you can not upgrade further ,The price to sell this level is ${get_sell_price(position)}')
                    elif upgrade_level == 2:
                        print(f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(position)} ,The price to sell this level is ${get_sell_price(position)}')
                    elif upgrade_level == 1:
                        print(f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(position)} ,The price to sell this level is ${get_sell_price(position)}')
                    elif upgrade_level == 0:
                        print(f'This airport is at level {upgrade_level}, the price to upgrade is ${price_to_upgrade(position)} ,The price to sell airport is ${get_sell_price(position)}')
                    user_choice = input(f'Enter your choice: "s" for sell, "u" for upgrade, Enter to skip: ')
                    if user_choice.lower() == "u":
                        upgrade_airport(position)
                    elif user_choice.lower() == "s":
                        sell_airport(position)
                elif upgrade_choice == False:
                    print(f'The price to sell this level is ${get_sell_price(position)}')

                    user_choice = input(f'Enter your choice: "s" for sell, Enter to skip: ')
                    if user_choice.lower() == "s":
                        sell_airport(position)
                    else:
                        pass

            elif owner == 'bank':
                rent = airport_price * 0.5
                temp_money = temp_money - rent
                modify_money(temp_money)
                print(f'Bank owns {col.CYAN}{airport_name}{col.END} and you need to pay rent to the bank at price of {col.CYAN}${rent}{col.END}. You currently have {temp_money} after paying the rent.')
            else:
                if temp_money > airport_price:
                    print(f'{airport_name} is available for purchase. Do you want to buy it? (Y/N)')
                    userinput = input().upper()
                    if userinput == 'Y':
                        buy_airport(position)
                        temp_money = get_money(session_id)
                        print(f'You purchased {airport_name} from {country_name} at price of ${airport_price}. Game continues. ')
                    elif userinput == 'N' or 'n':
                        print("You choose to pass this airport without buying. Game continue.")
                    else:
                        print("Invalid input. Game continues.")
                else:
                    print("You can't afford this airport yet. You will continue the game.")

        elif temp_type_id == 2 and jailed == False:
            print(f'You have landed on chance cell. You will randomly select a card from the deck. Press any key to continue.')
            userinput = input()
            if userinput == '':
                chance_card(position)
        elif temp_type_id == 3 and jailed == False:
            print(f'You have landed on Go to Jail cell. You will be sent to jail immediately. :)) Press any key to continue.')
            userinput = input()
            if userinput == '':
                position = 17
                jailed = True
        elif temp_type_id == 4 and jailed == False:
            print(f'You have landed on income tax cell. Press any key to continue. ')
            userinput = input()
            if userinput == '':
                income_tax()
        elif temp_type_id == 5 and jailed == False:
            print(f'You have landed on luxury tax cell. Press any key to continue.')
            userinput = input()
            if userinput == '':
                luxury_tax()



if rounds > 20:
    print(f'{col.BOLD}{col.PINK}You have won!{col.END}')
    print(f'{col.BOLD}{col.CYAN}You ended the game with:', f'${get_money(session_id):.0f}')
    print(f"You finished the game in {round(time.time() - gamestart)} seconds")
    money = get_money(session_id)
    airport = get_all_owned_airport(session_id)
    upgrade_airport = get_upgraded_airport_number(session_id)
    score = round(money + airport * 5 + upgrade_airport * 10)
    insert_high_score(session_id, score)
    print(f'{col.BOLD}{col.GREEN}Your score is:', score, f'{col.END}')
    top_player, top_score, session_list = get_top_high_score(session_id)
    if session_id in session_list:
        rank = session_list.index(session_id) + 1
        print(f'You ranked {rank} in the top 5 high scores.')
    elif session_id not in session_list:
        print(f"You didn't make it to the top 5 high scores.")
    index = 0
    print(f'{col.PINK}USER  | {col.END}', f'{col.PINK}SCORE{col.END}')
    while index < len(top_score):
        print(f'{top_player[index]}    |  {top_score[index]}')
        index += 1
    clear_tables(session_id)