import time
import sys
from dataFetching import *
from content import *

currCHAR = 0


def indent(space):
    return " " * space


def delay_print(text):
    # Code courtesy of stackOverflow
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(0.02)


def skip_line(line):
    print("\n" * line)


def print_intro():
    # delay_print(introContent)
    print("Yes")
    time.sleep(2)
    intro.close()


def new_game():
    skip_line(5)
    name = input("Enter a name: ")
    insert_character(name, 1, get_id() + 1)


def load_game():
    global currCHAR
    get_character_list()
    while True:
        try:
            currCHAR = int(input("Please type in your character id: \n"))
            return
        except ValueError:
            currCHAR = int(input("Please type in your character id properly: \n"))


def load_options():
    user_option = input("Choose your options: ")
    if user_option.lower() == "new game":
        new_game()
    elif user_option.lower() == "load game":
        load_game()
    else:
        load_options()


def render_menu():
    skip_line(40)
    delay_print("Welcome to Warhammer 40k. The grim dark future of humanity is at hand. \n"
                "Survival is your objective in this bloody galaxy. \n")
    print(indent(2) + "New Game \n")
    print(indent(2) + "Load Game \n")
    load_options()
    skip_line(10)
