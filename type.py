import time
import sys



def delay_print(text):
    # Code courtesy of stackOverflow
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(0.02)

        
def print_intro():
    gameIntro = open('text/intro.txt', 'r')
    introContent = gameIntro.read()
    delay_print(introContent)
    gameIntro.close()

    
def start_menu():
    print(' ')
