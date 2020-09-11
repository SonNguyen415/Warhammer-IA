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
    gameIntro.close()

    
def start_menu():
    print(' ')
