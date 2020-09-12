import time
import sys
import sqlite3 as sq

from content import *

# identify location of database, courtesy of Monika Richardson
con = sq.connect("")
c = con.cursor()

def delay_print(text):
    # Code courtesy of stackOverflow
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(0.02)

        
def print_intro():
    delay_print(introContent)
    print(" ")
    time.sleep(0.1)
    gameIntro.close()
    
def insert_character(characterName, Rank, charID):
    """
    Inserting the novel into the database
    """
    insertion = ('INSERT INTO Character (Name, Rank, charID) Values ("' + str(characterName) + '", "' + Rank + '", ' + str(charId) + ', ' + str(aID) + ')');
    sql = c.execute(insertion)
    

def welcome():
    delay_print("Welcolme to Warhammer 40k. The grim dark future of humanity is at hand. Survival is your objective. We will begin with character creation.")
    name = input("Enter a name: ")
 
    
