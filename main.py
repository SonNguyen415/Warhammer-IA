import time
import sys


def delay_print(text):
    for w in text:
        sys.stdout.write(w)
        sys.stdout.flush()
        time.sleep(0.05)


def print_intro():
    gameIntro = open('intro', 'r')
    introContent = gameIntro.read()
    delay_print(introContent)
    gameIntro.close()


def start_menu():
    print('hi')


print_intro()
start_menu()
exitKey = input('Press any key to exit: ')

