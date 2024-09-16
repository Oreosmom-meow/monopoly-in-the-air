import random
import mysql.connector
from mysql.connector import cursor
from tqdm import tqdm
import time

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
    sql = f"select money from game where user_name = '{username}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][0]

def get_airport_price(position):
    sql = f"select price from board where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            price = row[0]
    return price

def get_airport_name(position):
    sql = f"select airport_name from board where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            airport_name = row[0]
    return airport_name

def get_country_name(position):
    sql = f"select country from board where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            country_name = row[0]
    return country_name

def get_type_id(position):
    sql = f"select type_id from board where id = {position}"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            type_id = row[0]
    return type_id

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
    sql = f"select out_of_jail_card from game where user_name = '{username}'"
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
    get_money(username)

def modify_owner_to_user(position):
    global username
    update = (f"update board set owner = '{username}' where id = {position}")
    cursor = connection.cursor()
    cursor.execute(update)

def modify_owner_to_bank(position):
    global username
    update = (f"update board set owner = 'bank' where id = {position}")
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
    print(f'{col.BOLD}{col.BLUE}Salary time!\nYou earned:', f'{money - temp_money:.0f}','\nYou now have:', f'{temp_money:.0f}', f'{col.END}')

def buy_airport(position): #yutong
    global username
    temp_price = get_airport_price(position)
    temp_money = get_money(username) - temp_price
    modify_money(temp_money)
    modify_owner_to_user(position)

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
        temp_money = temp_money + 50
        print(f'You picked card: Bank pays you 50! You will get $50 from the bank.Congratulations. You now have ${temp_money}.')
        modify_money(temp_money)
    elif card_id == 5:
        punishment = get_all_owned_airport(username) * 25 + get_upgraded_airport_number(username) * 50
        temp_money = temp_money - punishment
        print(f'You picked card: Pay repair fee for all properties. You need to pay $25 for all airports you own, $50 for all the upgraded airports you own. You need to pay in toal ${punishment}. You now have ${temp_money}. ')
        modify_money(temp_money)
    elif card_id == 6:
        temp_money = get_money(username) - 50
        print(f'You picked card: Doctor fee. You need to pay $50 to the doctor.You now have ${temp_money}.')
        modify_money(temp_money)
    elif card_id == 7:
        temp_money = get_money(username) + 50
        print(f'You picked card: Grand opening night. You will get $50 from the bank. Congratulations. You now have ${temp_money}.')
        modify_money(temp_money)
    elif card_id == 8:
        temp_money = get_money(username) - 50
        print(f'You picked card: School fee. You need to pay $50 to the school. You now have ${temp_money}.')
        modify_money(temp_money)
    elif card_id == 9:
        temp_money = get_money(username) + 25
        print(f'You picked card: Receive consultancy fee. You will get $25 from the bank. Congratulations.You now have ${temp_money}.')
        modify_money(temp_money)
    elif card_id == 10:
        temp_money = get_money(username) - 50
        print(f'You picked card: Elected as chairman of the board. You need to pay $50 to the bank.You now have ${temp_money}.')
        modify_money(temp_money)

def board_location(position): # iida
    sql = f'select * from board where id = "{position}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]

#visualization function
def progress_bar():
    for i in tqdm(range(100),
              desc="Game Loading…",
              ascii=False, ncols=100):
        time.sleep(0.09)


# GAME START FUNCTION RUNNING
# set up username
while True:
    username = input('Enter your username: ')
    if username == '':
        print('Username cannot be empty.')
    elif username == 'bank':
        print('Username cannot be "bank"')
    else:
        sql = f"update game set user_name = '{username}';"
        cursor = connection.cursor()
        cursor.execute(sql)
        break
print(f'Username confirmed as {username}')
#progress_bar()

# set board airports (˶˃ ᵕ ˂˶) .ᐟ.ᐟ working sql when pls
def set_board_airports():
    airportnumbers = (2,4,5,7,8,10,11,13,15,16,19,20,21)
    i = 0
    sql = f"with random_countries as ( select distinct c.iso_country from country c where (select count(*) from airport a where a.iso_country = c.iso_country) >= 3 order by rand() limit 4), random_airports as ( select a.name, a.iso_country, row_number() over (partition by a.iso_country order by rand()) as rn from airport a join random_countries rc on a.iso_country = rc.iso_country) select name, iso_country from random_airports where rn <= 3;"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        sql = f'update board set board.airport_name = "{row[0]}", board.country = "{row[1]}" where board.id = "{airportnumbers[i]}";'
        cursor = connection.cursor()
        cursor.execute(sql)
        i += 1
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
        input(f'{col.BOLD}Roll the dice to move.Press any key to roll. {col.END}')
        print(f'{col.BLUE}You rolled{col.END}:',f'{dice_roll_1}, {dice_roll_2}')
        if dice_roll_1 == dice_roll_2:
            doubles += 1
            if doubles >= 2:
                print(f'{col.BOLD}{col.RED}You have been jailed for rolling doubles twice.{col.END}')
                jailed = True
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
        temp_type_id = get_type_id(position)
        temp_money = get_money(username)
        airport_price = get_airport_price(position)
        airport_name = get_airport_name(position)
        country_name = get_country_name(position)
        if temp_type_id == 0:
            if position == 1 and rounds != 1:
                temp_money = temp_money + 200
                print(f'You have landed on Go cell. You will get $200 from the bank. Your money is currently ${temp_money}')
            elif position == 1 and round == 1:
                print(f'You have started the game from GO cell.')
            elif position == 12:
                print(f'You have landed on Free Parking cell. You will pass.')
            elif position == 17:
                #I don't know what to put here
                print(f'You have landed on Jail. You will pass.')
        elif temp_type_id == 1:
            print(f'You have landed on {airport_name} from {country_name}. The airport price is ${airport_price}. Your current money is ${temp_money}. Press any key to continue.')
            userinput = input()
            if userinput == '':
                owner = check_airport_owner(position)
                if owner == username:
                    upgrade_level = get_upgrade_status(position)
                    if temp_money < airport_price:
                        print(f'You own {airport_name}. The level is {upgrade_level}. You have ${temp_money}. You can sell this airport. Do you want to sell? (Y/N)')
                        userinput = input(f'{col.BOLD}{col.YELLOW}').upper()
                        if userinput == 'N':
                            pass
                        elif userinput == 'Y':
                            sell_airport(position)
                        else:
                            print(f'{col.BOLD}{col.RED}Invalid input{col.END}')
                    elif temp_money >= airport_price:
                        print(f'You own {airport_name}. The level is {upgrade_level}. You have ${temp_money}. You can sell or upgrade this airport. Do you want to sell or upgrade? Please enter to skip. (sell/upgrade)')
                        userinput = input().lower()
                        if userinput == 'sell':
                            sell_airport(position)
                            temp_money = get_money(username)
                            print(f'{col.BOLD}{col.GREEN}You have successfully sold {airport_name}. You current money is {temp_money}. {col.END}')
                        elif userinput == 'upgrade':
                            upgrade_airport(position)
                            temp_money = get_money(username)
                            print(f'{col.BOLD}{col.GREEN}You have successfully upgraded {airport_name}. You current money is {temp_money}. {col.END}')
                        else:
                            pass
                elif owner == 'bank':
                    rent = airport_price * 0.5
                    temp_money = temp_money - rent
                    modify_money(temp_money)
                    print(f'Bank owns {airport_name} and you need to pay rent to the bank at price of {rent}. Your current money is {temp_money} after paying the rent. {col.END}')
                else:
                    if temp_money > airport_price:
                        print(f'{airport_name} is available for purchase. The price is ${airport_price}. Do you want to buy it? (Y/N)')
                        userinput = input().upper()
                        if userinput == 'N':
                            print("You choose to pass this airport without buying. Game continue.")
                            pass
                        elif userinput == 'Y':
                            buy_airport(position)
                            temp_money = get_money(username)
                            print(f'You purchased {airport_name} from {country_name} at price of ${airport_price}. Your current money is ${temp_money} after purchase. Game continues. ')
                    else:
                        print("Your money can't afford this airport yet. You will continue the game.")

        elif temp_type_id == 2:
            print(f'You have landed on chance cell. You will randomly select a card from the deck. Press any key to continue.')
            userinput = input()
            if userinput == '':
                chance_card(position)
        elif temp_type_id == 3:
            print(f'You have landed on Go to Jail cell. You will be sent to jail immediately. :)) Press any key to continue.')
            userinput = input()
            if userinput == '':
                position = 17
                #call jail event?
        elif temp_type_id == 4:
            print(f'You have landed on income tax cell. Press any key to continue. ')
            userinput = input()
            if userinput == '':
                income_tax()
                print(f'You now have ${temp_money} money left.')
        elif temp_type_id == 5:
            print(f'You have landed on luxury tax cell. Press any key to continue.')
            userinput = input()
            if userinput == '':
                luxury_tax()
                print(f'You now have ${temp_money} money left.')

if rounds > 20:
    print(f'{col.BOLD}{col.PINK}You have won!{col.END}')
    print(f'{col.BOLD}{col.CYAN}You ended the game with:', f'{money:.0f}')
    score = round(money * 0.75 * 10)
    print(f'{col.BOLD}{col.GREEN}Your score is:', score, f'{col.END}')
    # check highest score in table, if score is higher, print
    print(f'{col.BOLD}{col.YELLOW}🜲{col.GREEN}{col.UNDERLINE}HIGHSCORE' + f'{col.END}')
    # print top 5 scores from table