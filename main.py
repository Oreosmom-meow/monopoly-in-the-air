import random
import mysql.connector

# mysql connection


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

# global
money = 150
rounds = 0
position = 1
doubles = 0
jail_counter = 0
jailed = False

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

# functions
def dice_roll(): # iida
    dice = random.randint(1, 6)
    return dice
def income_tax(): # iida
    money = 1 #sql money
    money_before = money
    money -= 50 + money * 0.25
    print(f'{col.BOLD}{col.YELLOW}Income tax!', f'You paid {money_before - money:.0f} in taxes.', f'{col.END}')
def luxury_tax(): # iida
    money = 1 #sql money
    money_before = money
    money -= 100 + money * 0.5
    print(f'{col.BOLD}{col.YELLOW}Luxury tax!', f'You paid {money_before - money:.0f} in taxes.', f'{col.END}')
def jail_event(): # iida
    money = 1 #sql money
    global jail_counter
    global jailed

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
            counter += 1
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
    money = 1 #sql money
    money_before = money
    money += 200 + 1 #property values
    print(f'{col.BOLD}{col.BLUE}Salary time!\nYou earned:', f'{money - money_before:.0f}','\nYou now have:', f'{money:.0f}', f'{col.END}')
def buy_airport(position): #yutong
    pass 
def sell_airport(position): # roberto
    pass 
def upgrade_airport(position): # roberto
    pass 
def board_location(position): # iida
    sql = f'select * from board where id = "{position}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0]
def chance_card(): # yutong
    pass 

# set board airports
def set_board_airports():
#    sql = f"insert into board (airport_name, country) select name, iso_country from ( with random_countries as ( select distinct c.iso_country from country c where (select count(*) from airport a where a.iso_country = c.iso_country) >= 3 order by rand() limit 4), random_airports as ( select a.name, a.iso_country, row_number() over (partition by a.iso_country order by rand()) as rn from airport a join random_countries rc on a.iso_country = rc.iso_country) select name, iso_country from random_airports where rn <= 3) AS temp_table;"
#    cursor = connection.cursor()
 #   cursor.execute(sql)
  #  result = cursor.fetchall()
   # for row in result:
    #    print(f"{row}")
    return
bank_airports = [] #random.sample(1, 3)
for position in bank_airports:
    pass
    # set board location owner as "bank"
set_board_airports()
while rounds <= 20:
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