# imports
import random
import json
import os.path

# globals
position = 1
money = 150
jail = False
rounds = 1
counter = 0
doubles = 0

#main
username = input('Enter your name: ')
if username == '':
    username = 'USERNAME'

# colors used for printing, "stolen" from blender
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# temp database
if os.path.exists('newtempdb.json'):
    with open('newtempdb.json') as tempdb:
        db = json.load(tempdb)
        print(f'{bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKGREEN}Config loaded successfully.{bcolors.ENDC}\n')
else:
    print(f'{bcolors.BOLD}{bcolors.WARNING}\n --- \n{bcolors.UNDERLINE}Temporary database file was not found.\n --- \n{bcolors.ENDC}')

# functions
def dice_roll():
    die = random.randint(1, 6)
    return die
# .game events
def income_tax():
    global money
    money_before = money
    money -= 50 + money * 0.25
    print(f'{bcolors.BOLD}{bcolors.WARNING}Income tax!', f'You lost {money_before - money:.0f}', f'{bcolors.ENDC}')
def luxury_tax():
    global money
    money_before = money
    money -= 100 + money * 0.5
    print(f'{bcolors.BOLD}{bcolors.WARNING}Luxury tax!', f'You lost {money_before - money:.0f}', f'{bcolors.ENDC}')
def jail_event():
    global money
    global counter
    global dice_roll_1
    global dice_roll_2
    global jail

    choosing = True
    print(f'{bcolors.BOLD}{bcolors.WARNING}You are in jail.', f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.WARNING}Type "1" to roll the dice and get doubles to get out. You have {3 - counter} rolls left until automatic release.', f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.WARNING}Type "2" to pay a fine of 200 to get out.', f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.WARNING}Type "3" to use a get out of jail free card to get out.', f'{bcolors.ENDC}')
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
            print(f'{bcolors.BOLD}{bcolors.OKGREEN}{bcolors.UNDERLINE}You have been released.' + f'{bcolors.ENDC}')
            jail = False
    elif choice == '2':
        money -= 200
        jail = False
    else:
        print('Cheater option, card doesnt exist yet')
        jail = False
def salary():
    global money
    money_before = money
    # will add in profit from owned properties
    money += 200
    print(f'{bcolors.BOLD}{bcolors.OKBLUE}Salary time!\nYou earned:', f'{money - money_before}','\nYou now have:', money, f'{bcolors.ENDC}')
def get_airport(position):
    global db
    airport_data = db[str(position)][0]
    airport = airport_data['name']
    cost = int(airport_data['cost'])
    group = airport_data['group']
    owner = airport_data['owner']
    return airport, cost, group, owner
def buy_airport(position):
    global db
    global money
    airport_data = db[str(position)][0]
    airport_data['owner'] = username
    cost = int(airport_data['cost'])
    print(airport_data['owner'])
    money -= cost
    print(money)
def airport_event(position):
    global username
    global money
    print('airport', position)
    airport, cost, group, owner = get_airport(position)
    print(airport, cost, group, owner)
    if owner == username:
        print('sell airport?')
        print('upgrade airport?')
        return
    elif owner != '':
        print('rent')
        return
    else:
        if money >= cost:
            buying = input('"1" to buy airport?, ENTER to continue ')
            if buying == '1':
                buy_airport(position)
            else:
                return

print('\n' + f'{bcolors.BOLD}{bcolors.HEADER}━━━━━━━━━━━━━━━━━━━━━{bcolors.ENDC}' + '\n')

while rounds <= 20:
    # Information
    print(f'{bcolors.BOLD}{bcolors.OKGREEN}Round:', rounds, f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.OKCYAN}Money:', f'{money:.0f}', f'{bcolors.ENDC}\n')

    # Checks the user's money and declared bankruptcy
    if money <= 0:
        print(f'{bcolors.BOLD}{bcolors.FAIL}You are bankrupt! \nGAME OVER', f'{bcolors.ENDC}')
        break

    # Dice rolls pre-determined at the start of round
    dice_roll_1 = dice_roll()
    dice_roll_2 = dice_roll()

    # JAIL
    if jail:
        jail_event()

    # PLAYER INPUT TO PROCEED
    input(f'{bcolors.BOLD}Roll the dice to move.{bcolors.ENDC}')
    print(f'{bcolors.OKBLUE}You rolled{bcolors.ENDC}:',f'{dice_roll_1}, {dice_roll_2}')

    # POSITION CHANGE
    # CHECKS FOR DOUBLES
    if dice_roll_1 == dice_roll_2:
        doubles += 1
        if doubles >= 2:
            print(f'{bcolors.BOLD}{bcolors.WARNING}You have been jailed for rolling doubles twice in a row.', f'{bcolors.ENDC}')
            jail = True
            doubles = 0
        else:
            position += dice_roll_1 + dice_roll_2
    else:
        doubles = 0
        position += dice_roll_1 + dice_roll_2

    # ROUND COMPLETED, PASS GO AND COLLECT $200
    if position > 22:
        salary()
        # ROUND COUNTER
        rounds += 1
        position = position - 22

    # Currently prints position as number on the board, when database, turn into airport buying
    print('You are at:', position)


    # Positions with chances : 11, 22

    # Positions with airports: 2,4,5 - 7,8,10 - 13,15,16 - 19,20,21
    # Free parking at 12, nothing happens - jail(location) at 17, nothing happens
    airports = [2,4,5,7,8,10,13,15,16,19,20,21]
    # Position checks with negative outcomes, tax & jail
    if position == 3 or position == 9:
        income_tax()
    elif position == 6:
        #jail
        print(f'{bcolors.BOLD}{bcolors.WARNING}You have been caught trespassing and are sent to jail.', f'{bcolors.ENDC}')
        position = 17
        jail = True
    elif position == 18:
        luxury_tax()
    elif any(airport == position for airport in airports):
        airport_event(position)
    print('\n' + f'{bcolors.BOLD}{bcolors.HEADER}━━━━━━━━━━━━━━━━━━━━━{bcolors.ENDC}' + '\n')

# After game is over, if player survived past 20 rounds without going bankrupt, they have won
if rounds > 20:
    print(f'{bcolors.BOLD}{bcolors.HEADER}You have won!', f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.OKCYAN}You ended the game with:', f'{money:.0f}', f'{bcolors.ENDC}')
    # score calculation
    score = round(money * 0.75 * 10) # + value of owned properties
    print(f'{bcolors.BOLD}{bcolors.OKGREEN}Your score is:', score, f'{bcolors.ENDC}')
    # check if SCORE > HIGHSCORES, if yes ADD USERNAME + SCORE TO SCOREBOARD AND REMOVE LOWEST SCORE
    # if score is new highscore, print(f'{bcolors.BOLD}{bcolors.OKGREEN}{bcolors.UNDERLINE}HIGHSCORE' + f'{bcolors.ENDC}')

