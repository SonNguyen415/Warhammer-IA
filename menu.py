import time
import sys
from objects import *


# Indent for aesthetic and readability
def indent(space):
    return " " * space


# Print one word at a time per sentence.
def delay_print(text):
    # Code courtesy of stackOverflow
    global TIME_STOP
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(TIME_STOP)


# Skipping lines
def skip_line(line):
    for i in range(0, line):
        print(" ")


# Print the intro and wait 2 seconds
def print_intro():
    # delay_print(introContent)
    print("Yes")
    time.sleep(2)
    intro.close()


def show_character_list():
    charList = get_character_list()
    skip_line(1)
    if charList:
        for char in charList:
            print(indent(2) + 'Name: ' + str(char[0]) + ', ID: ' + str(char[1]) + "\n")
    else:
        new = input("No saves available, type start for new game. Type anything else to return to main menu: ")
        if new.lower() == "start":
            new_game()
            return
        render_menu()
    skip_line(1)


def show_weapon_list(charID):
    wList = get_my_weapons(charID)
    for weapon in wList:
        print(weapon)


def show_weapon_data(weapon):
    wData = get_weapon_data(weapon)
    for attr in wData:
        print(attr)


def customize_character(pt, charID):
    skip_line(1)
    show_character(charID)
    skip_line(1)
    print("You have " + str(pt) + " starting points, spend them wisely. \n")
    weapon = input("You have been provided with a lasgun. Enter w to view your weapon. Any other button to skip: \n")
    if weapon.lower() == "w":
        show_weapon_data("Lasgun")
    print("No additional weapon is available at level 1, you may purchase more upon ascension. \n")
    dist = input("Enter d to distribute points. Enter any other button to skip and save for later: \n")
    print("You may input 0 if you don't wish to add points. Warning, undoing choices is not possible. You have " + str(
        pt) + " points.\n")
    if dist.lower() == "d":
        Player.customize()
    show_character(charID)


# Load new game screen
def new_game():
    skip_line(5)
    global currChar
    global Player
    currChar = get_id()
    if currChar == 0:
        print("You have too many saves. You must delete some.")
        delete_saves()
    name = input("Enter a name: ")
    insert_character(name, currChar)
    Player = Characters(name, 1, BASE_STATS[1][0], BASE_STATS[1][1], BASE_STATS[1][2], BASE_STATS[1][3],
                        BASE_STATS[1][4], BASE_STATS[1][5], START_PTS)
    provide_weapons(1, currChar, "Lasgun")
    customize_character(START_PTS, currChar)


# Allow loading game and change the current characterID
def load_game():
    global currCHAR
    show_character_list()
    while True:
        try:
            currCHAR = int(input("Please type in your character id. If you wish to return to menu, enter e: \n"))
            return
        except ValueError:
            render_menu()


def delete_saves():
    show_character_list()
    error = True
    while error:
        try:
            error = False
            deleteChar = int(input("Please type the id of the character you wish to kill. If you wish to return to "
                                   "menu, enter e: \n"))
            delete_character(deleteChar)
        except ValueError:
            render_menu()
    render_menu()


# Load all the options a player can have in the menu
def load_options():
    userOption = input("Choose your options: ")
    if userOption.lower() == "new game":
        new_game()
    elif userOption.lower() == "load game":
        load_game()
    elif userOption.lower() == "delete saves":
        delete_saves()
    elif userOption.lower() == "exit game":
        sys.exit(0)
    else:
        load_options()


# Create menu and starting screen
def render_menu():
    skip_line(40)
    delay_print("Welcome to Warhammer 40k. The grim dark future of humanity is at hand. \n"
                "Survival is your objective in this bloody galaxy. Please type the following option as given\n")
    print(indent(2) + "New Game \n")
    print(indent(2) + "Load Game \n")
    print(indent(2) + "Delete Saves \n")
    print(indent(2) + "Exit Game \n")
    load_options()
    skip_line(10)
