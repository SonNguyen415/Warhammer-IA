import sqlite3 as sq
import time
import sys

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

#
currScene = 1
Player = object

TIME_STOP = 0
START_PTS = 5
ASC_POINTS = 5
BASE_STATS = [["Strength", "Endurance", "Durability", "Agility", "Accuracy", "InventoryCap"],
              [5, 5, 5, 5, 5, 25]]


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