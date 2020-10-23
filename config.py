import sqlite3 as sq
import time
import sys
import math
import random
import string


# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

currScene = 1
Player = object
CurrEnemy = object


STORY = 0
EVENT = 1
LASGUN_ID = 1
MAX_EXP = 100
STOP_TIME = 0
WAIT_TIME = 0
START_PTS = 5
ASC_POINTS = 5
BASE_STATS = [["Health", "Strength", "Endurance", "Durability", "Agility", "Accuracy", "InventoryCap"],
              [100, 10, 10, 10, 10, 10, 25]]


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

