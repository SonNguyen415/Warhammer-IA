import sqlite3 as sq
import time
import sys

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

STORY = 0
EVENT = 1

BUTTON = "x"
LASGUN_ID = 1
STOP_TIME = 0
WAIT_TIME = 3
START_PTS = 5
ASC_POINTS = 5
ASC_EXP = 100
INITIATIVE_INCREASE = 1
MELEE_DISTANCE = 4
MIN_DISTANCE = 100
MAX_DISTANCE = 1000

DEAD = 1
ALIVE = 0

CORRUPTION_INCREASE = 10
CORRUPTION_DIFFERENCE = 5

BASE_STATS = [["Initiative", "Health", "Strength", "Endurance", "Durability", "Agility", "Accuracy", "InventoryCap"],
              [10, 100, 10, 10, 10, 10, 10, 25]]

EVENT_END = 0
MOVEMENT = 1
SHOOTING = 2
MELEE = 3

INITIATIVE = 0
HEALTH = 1
STRENGTH = 2
ENDURANCE = 3
DURABILITY = 4
AGILITY = 5
ACCURACY = 6

TYPE_ID = 0
TYPE_NAME = 1
RATE_OF_FIRE = 2
WEAPON_DAMAGE = 3
WEAPON_RANGE = 4
WEAPON_SIZE = 5
WEAPON_RELIABILITY = 7
WEAPON_DURABILITY = 8
WEAPON_COST = 10

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
    print(" ")


# Skipping lines
def skip_line(line):
    for i in range(0, line):
        print(" ")


# Print the intro and wait 2 seconds
def print_intro():
    delay_print(introContent)
    time.sleep(STOP_TIME)
    intro.close()
