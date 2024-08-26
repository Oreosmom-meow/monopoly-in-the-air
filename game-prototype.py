# imports
import random

# globals
position = 1
money = 150
jail = False
rounds = 1
counter = 0

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

#functions
def dice_roll():
    die = random.randint(1, 6)
    print('Dice roll:', die)
    return die

#main
while rounds <= 20:
    # Information
    print(f'{bcolors.BOLD}{bcolors.OKGREEN}Round:', rounds, f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.OKCYAN}Money:', money, f'{bcolors.ENDC}')

    # Checks the user's money and declared bankruptcy
    if money <= 0:
        print(f'{bcolors.BOLD}{bcolors.FAIL}You are bankrupt! \nGAME OVER', f'{bcolors.ENDC}')
        break

    # Prompts the user for input before proceeding
    input('Roll the dice')

    # Jail check & roll the dice
    # Add punishment for jail - either have rounds go by while in jail or take money
    if not jail:
        position += dice_roll() + dice_roll()
    elif counter < 3:
        print(f'{bcolors.BOLD}{bcolors.WARNING}You are in jail.', f'{bcolors.ENDC}')
        if dice_roll() != dice_roll():
            counter += 1
        else:
            print(f'{bcolors.BOLD}{bcolors.OKGREEN}{bcolors.UNDERLINE}You have been released.' + f'{bcolors.ENDC}')
            jail = False
    else:
        jail = False
        print(f'{bcolors.BOLD}{bcolors.OKGREEN}{bcolors.UNDERLINE}You have been released.' + f'{bcolors.ENDC}')

    # Position to check for the round and passing go
    if position > 22:
        # round counter
        money += 200
        print(f'{bcolors.BOLD}{bcolors.OKBLUE}Salary time! You have:', money, f'{bcolors.ENDC}')
        rounds += 1
        position = position - 22

    # Printing position for development reasons, take away later, keep after round check to have the right number after passing go
    print('Position:', position)

    # Position checks with negative outcomes, tax & jail
    if position == 3 or position == 9:
        #income tax
        print(f'{bcolors.BOLD}{bcolors.WARNING}Income tax!', f'{bcolors.ENDC}')
        money -= 200
    if position == 6:
        #jail
        position = 17
        jail = True
    if position == 18:
        # luxury tax
        print(f'{bcolors.BOLD}{bcolors.WARNING}Luxury tax!', f'{bcolors.ENDC}')
        money -= 500

# After game is over, if player survived past 20 rounds without going bankrupt, they have won
if rounds > 20:
    print(f'{bcolors.BOLD}{bcolors.HEADER}You have won!', f'{bcolors.ENDC}')
    print(f'{bcolors.BOLD}{bcolors.OKCYAN}You ended the game with:', money, f'{bcolors.ENDC}')

