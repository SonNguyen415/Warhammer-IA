from switcher import *
from type import *

def print_intro():
    gameIntro = open('text/intro.txt', 'r')
    introContent = gameIntro.read()
    delay_print(introContent)
    gameIntro.close()


