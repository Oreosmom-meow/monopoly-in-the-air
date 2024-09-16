import random
import mysql.connector
from mysql.connector import cursor


# mysql connection
connection = mysql.connector.connect(
    user="yutongd",
    password="12345",
    host="mysql.metropolia.fi",
    port=3306,
    database="yutongd"
)

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

# global variables
rounds = 0
position = 1
doubles = 0
jail_counter = 0
jailed = False
username = ''

# username
while True:
    username = input('Enter your username: ')
    if username == '':
        print('Username cannot be empty.')
    elif username == 'bank':
        print('Username cannot be "bank"')
    else:
        #! send username to game table here
        break
print(username)

#sql related functions
def get_owner(position): # Yutong
    sql = f"select owner from board where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            owner = row[0]
    return owner

def get_money(username): #Yutong
    sql = f"select money from game where user_name = ’{username}‘"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            money = row[0]
    return money

def get_all_owned_airport(username):
    sql = f"select COUNT(owner) from board where owner = '{username}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_number = row[0]
    return airport_number

def get_upgrade_status(position):
    sql = f"select upgrade_status from board where id = {position} "
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_status = row[0]
    return upgrade_status

def check_airport_owner(position):
    sql = f"select owner from board where id = {position}"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_owner = row[0]
    return airport_owner

def check_jail_card(username):
    sql = f"select out_jail_card from game where user_name = '{username}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            card_number = row[0]
    return card_number

def get_upgraded_airport_number(username):
    sql = f"SELECT COUNT(owner) from board WHERE owner = '{username}' AND upgrade_status > 0"
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            upgrade_number = row[0]
    return upgrade_number

def modify_money(temp_money):
    global username
    update = f"update game set money = {temp_money} where user_name = '{username}'"
    cursor = connection.cursor()
    cursor.execute(update)

def modify_owner_to_user(position):
    global username
    update = (f"update game set owner = '{username}' where id = position")
    cursor = connection.cursor()
    cursor.execute(update)

def modify_owner_to_bank(position):
    global username
    update = (f"update game set owner = 'bank' where id = position")
    cursor = connection.cursor()
    cursor.execute(update)

def modify_out_of_jail_card(jail_card):
    global username
    sql = f"update game set out_of_jail_card = '{jail_card}' where user_name = '{username}'"
    cursor = connection.cursor()
    cursor.execute(sql)

def modify_airport_status(position, temp_status):
    global username
    sql = f"update board set upgrade_status = temp_status where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)

def board_location(position): # iida
    sql = f'select * from board where id = "{position}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]

# functions
def dice_roll(): # iida
    dice = random.randint(1, 6)
    return dice

def income_tax(): # iida
    global username
    money = get_money(username)
    temp_money = money
    money -= 50 + money * 0.25
    print(f'{col.BOLD}{col.YELLOW}Income tax!', f'You paid {temp_money - money:.0f} in taxes.', f'{col.END}')

def luxury_tax(): # iida
    global username
    money = get_money(username)
    temp_money = money
    money -= 100 + money * 0.5
    print(f'{col.BOLD}{col.YELLOW}Luxury tax!', f'You paid {temp_money - money:.0f} in taxes.', f'{col.END}')

def jail_event(): # iida
    global jail_counter
    global jailed
    global username
    money = get_money(username)

    dice_roll_1 = dice_roll()
    dice_roll_2 = dice_roll()

    choosing = True
    print(f'{col.BOLD}{col.YELLOW}You are in jail.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "1" to roll the dice and get doubles to get out. You have {3 - jail_counter} rolls left until automatic release.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "2" to pay a fine of 200 to get out.', f'{col.END}')
    print(f'{col.BOLD}{col.YELLOW}Type "3" to use a get out of jail free card to get out.', f'{col.END}')
    while choosing == True:
        choice = input('Enter your choice: ')
        if choice == '':
            print('Try again, use "1", "2", or "3" to choose.')
        elif 1 > int(choice) < 3:
            print('Try again, use "1", "2", or "3" to choose.')
        else:
            choosing = False
    if choice == '1':
        print(dice_roll_1, dice_roll_2)
        if dice_roll_1 != dice_roll_2:
            jail_counter += 1
        else:
            print(f'{col.BOLD}{col.GREEN}{col.UNDERLINE}You have been released.' + f'{col.END}')
            jailed = False
    elif choice == '2':
        money -= 200
        jailed = False
    else:
        print('Cheater option, card doesnt exist yet')
        jailed = False

def salary(): # iida
    global username
    money = get_money(username)
    temp_money = money
    temp_money += 200 + 1 #property values
    modify_money(temp_money)
    print(f'{col.BOLD}{col.BLUE}Salary time!\nYou earned:', f'{money - temp_money:.0f}','\nYou now have:', f'{money:.0f}', f'{col.END}')

def buy_airport(position): #yutong
    global username
    temp_money = get_money(username)
    if temp_money >= 200:
        print(f'Do you want to buy the airport you landed in? (Y/n)')
        userinput = input()
        if userinput == 'Y' or userinput == 'y':
            temp_money = temp_money - 200
            print(f'You have purchased 1 airport')
            print(f'Your money now is:' + f'{temp_money}')
            modify_money(temp_money)
            modify_owner_to_user(position)
        elif userinput == 'n' or userinput == 'N':
            print(f'You choose not to buy the airport')
        else:
            print(f'Please input the given options.')
    else:
        print("Your money can't afford to buy the airport. You will pass this airport.")

def sell_airport(position): # roberto
    global username
    temp_money = get_money(username)
    if get_owner(position) == 'username':
        upgrade_level = get_upgrade_status(position)
        print(f'You own this airport, it is upgrade level: {upgrade_level}. Do you want to sell it? (Y/n)')
        userinput = input()
        if userinput == 'Y' or 'y' and upgrade_level > 0:
            temp_money = temp_money + 200
            modify_money(temp_money)
            temp_level = upgrade_level - 1
            modify_airport_status(position, temp_level)
            print(f'You have downgraded this airport from {upgrade_level} to {temp_level} and you currently have ${temp_money}')
        elif userinput == 'Y' or 'y' and upgrade_level == 0:
            temp_money = temp_money + 200
            modify_owner_to_bank(position)
            print(f'You have sold this airport to bank and your current money is {temp_money}')
        elif userinput == 'n' or userinput == 'N':
            print(f'You choose not to sell it. You will continue to play.')
    else:
        pass    


def upgrade_airport(position): # roberto
    money = 1
    price = 100
    if money >= price:
        money = 1
        money -= 50 #25% of original cost would be cool
        price = + 100 #add 50% of org value or same as upgrade cost
    else:
        print('not enough money to perform this task')
    pass

def chance_card(position): # yutong
    global username
    card_id = random.randint(1, 10)
    temp_money = get_money(username)
    if card_id == 1:
        print(f'You picked card: Advance to "Go". You will get $200. Congratulations.')
        temp_money = temp_money + 200
        modify_money(temp_money)
        position = 1
    elif card_id == 2:
        print(f'You picked card: Get out of jail. You can use it for once when you are in jail.')
        jail_card = check_jail_card(username)
        jail_card += 1
        modify_out_of_jail_card(jail_card)
    elif card_id == 3:
        print(f'You picked card: Go to jail. You will be moved to jail immediately.')
        jail_event()
    elif card_id == 4:
        print(f'You picked card: Bank pays you 50! You will get $50 from the bank.Congratulations.')
        temp_money = get_money(username) + 50
        modify_money(temp_money)
    elif card_id == 5:
        print(f'You picked card: Pay repair fee for all properties. You need to pay $25 for all airports you own, $50 for all the upgraded airports you own')
        temp_money = get_money(username)
        temp_money = temp_money - get_all_owned_airport(username) * 25
        temp_money = temp_money - get_upgraded_airport_number(username) * 50
        modify_money(temp_money)
    elif card_id == 6:
        print(f'You picked card: Doctor fee. You need to pay $50 to the doctor.')
        temp_money = get_money(username) - 50
        modify_money(temp_money)
    elif card_id == 7:
        print(f'You picked card: Grand opening night. You will get $50 from the bank. Congratulations.')
        temp_money = get_money(username) + 50
        modify_money(temp_money)
    elif card_id == 8:
        print(f'You picked card: School fee. You need to pay $50 to the school.')
        temp_money = get_money(username) - 50
        modify_money(temp_money)
    elif card_id == 9:
        print(f'You picked card: Receive consultancy fee. You will get $25 from the bank. Congratulations.')
        temp_money = get_money(username) + 25
        modify_money(temp_money)
    elif card_id == 10:
        print(f'You picked card: Elected as chairman of the board. You need to pay $50 to the bank.')
        temp_money = get_money(username) - 50
        modify_money(temp_money)

def board_location(position): # iida
    sql = f'select * from board where id = "{position}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]














# GAME START FUNCTION RUNNING
# set board airports (˶˃ ᵕ ˂˶) .ᐟ.ᐟ working sql when pls
def set_board_airports():
#    sql = f"insert into board (airport_name, country) select name, iso_country from ( with random_countries as ( select distinct c.iso_country from country c where (select count(*) from airport a where a.iso_country = c.iso_country) >= 3 order by rand() limit 4), random_airports as ( select a.name, a.iso_country, row_number() over (partition by a.iso_country order by rand()) as rn from airport a join random_countries rc on a.iso_country = rc.iso_country) select name, iso_country from random_airports where rn <= 3) AS temp_table;"
#    cursor = connection.cursor()
 #   cursor.execute(sql)
  #  result = cursor.fetchall()
   # for row in result:
    #    print(f"{row}")
    return
set_board_airports()
# set starting money
modify_money(150)

















# MAIN FUNCTION
while rounds <= 20:
    money = get_money(username)
    if money <= 0:
        print(f'{col.BOLD}{col.RED}You are bankrupt! \nGAME OVER', f'{col.END}')
        break
    print('\n' + f'{col.BOLD}{col.PINK}━━━━━━━━━━━━━━━━━━━━━{col.END}' + '\n')
    if jail_counter >= 3:
        jailed = False
        counter = 0
    if jailed:
        jail_event()
    if not jailed:
        dice_roll_1 = dice_roll()
        dice_roll_2 = dice_roll()
        input(f'{col.BOLD}Roll the dice to move.{col.END}')
        print(f'{col.BLUE}You rolled{col.END}:',f'{dice_roll_1}, {dice_roll_2}')
        if dice_roll_1 == dice_roll_2:
            doubles += 1
            if doubles >= 2:
                print(f'{col.BOLD}{col.WARNING}You have been jailed for rolling doubles twice.{col.END}')
                jail = True
                doubles = 0
            else:
                position += dice_roll_1 + dice_roll_2
        else:
            position += dice_roll_1 + dice_roll_2
        if position > 22:
            salary()
            rounds += 1
            position = position - 21
        print('You are at:', position)
        locationstuff = board_location()

if rounds > 20:
    print(f'{col.BOLD}{col.PINK}You have won!{col.END}')
    print(f'{col.BOLD}{col.CYAN}You ended the game with:', f'{money:.0f}')
    score = round(money * 0.75 * 10)
    print(f'{col.BOLD}{col.GREEN}Your score is:', score, f'{col.END}')
    # check highest score in table, if score is higher, print
    print(f'{col.BOLD}{col.YELLOW}🜲{col.GREEN}{col.UNDERLINE}HIGHSCORE' + f'{col.ENDC}')
    # print top 5 scores from table