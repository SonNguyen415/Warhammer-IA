import time
import sys
from content import *


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

def welcome():
    delay_print("Welcolme to Warhammer 40k. The grim dark future of humanity is at hand. Survival is your objective. We will begin with character creation.")
    name = input("Enter a name: ")
    
