import sqlite3 as sq
import time
import sys

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()



BUTTON = "x"
STORY = 0
EVENT = 1
LASGUN_ID = 1
MAX_EXP = 100
STOP_TIME = 0
WAIT_TIME = 0
START_PTS = 5
ASC_POINTS = 5

CORRUPTION_INCREASE = 10
CORRUPTION_DIFFERENCE = 5

BASE_STATS = [["Initiative", "Health", "Strength", "Endurance", "Durability", "Agility", "Accuracy", "InventoryCap"],
              [10, 100, 10, 10, 10, 10, 10, 25]]

EVENT_END = 0
MOVEMENT = 1
SHOOTING = 2
MELEE = 3
WEAPON_DAMAGE = 3
WEAPON_RANGE = 4

intro = open('database/intro.txt', 'r')
introContent = intro.read()


# Indent for aesthetic and readability
def indent(space):
    return " " * space


# Print one word at a time per sentence.
def delay_print(text):
    # Code courtesy of stackOverflow
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(STOP_TIME)


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
