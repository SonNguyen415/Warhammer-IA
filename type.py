import time
import sys
from dataFetching import *


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
    print("\n" * line)


# Print the intro and wait 2 seconds
def print_intro():
    # delay_print(introContent)
    print("Yes")
    time.sleep(2)
    intro.close()


def show_character_list():
    charList = get_character_list()
    for char in charList:
        print(indent(2) + 'Name: ' + str(char[0]) + ', ID: ' + str(char[1]) + "\n")
    skip_line(1)


# Load new game screen
def new_game():
    skip_line(5)
    global currChar
    name = input("Enter a name: ")
    insert_character(name)
    currChar = get_id()


# Allow loading game and change the current characterID
def load_game():
    global currCHAR
    show_character_list()
    while True:
        try:
            currCHAR = int(input("Please type in your character id: \n"))
            return
        except ValueError:
            print("Please type in your character id properly: \n")


def delete_saves():
    show_character_list()
    while True:
        try:
            deleteChar = int(input("Please type the id of the character you wish to kill: \n"))
            delete_character(deleteChar)
            break
        except ValueError:
            print("Please input your character id properly \n")


# Load all the options a player can have in the menu
def load_options():
    user_option = input("Choose your options: ")
    if user_option.lower() == "new game":
        new_game()
    elif user_option.lower() == "load game":
        load_game()
    elif user_option.lower() == "delete saves":
        delete_saves()
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
    load_options()
    skip_line(10)
