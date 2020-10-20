from menu import *


def get_event():
    return


def check_event():
    return False


def get_scene():
    sql = c.execute('SELECT TextContent FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data[0][0]


def get_choices():
    sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    data = c.fetchall()
    return data


def scene_calc():
    return 0


def confirm_choice(cID):
    sql = c.execute('SELECT TextID FROM Storyline WHERE TextType = ' + str(cID) + ' and TextPointer = ' + str(currScene))
    data = c.fetchall()
    return data[0][0]


def get_next_scene(cID):
    global currScene
    sql = c.execute('SELECT TextID FROM Storyline WHERE TextPointer = ' + str(confirm_choice(cID)))
    data = c.fetchall()
    currScene = data[0][scene_calc()]


def check_child():
    sql = c.execute('SELECT Children FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data[0][0] > 0


def game_progress():
    global currScene
    if check_event():
        get_event()
    if check_child():
        skip_line(4)
        delay_print(get_scene())
        skip_line(1)
        for i in range(0, len(get_choices())):
            print(get_choices()[i][0])
        skip_line(1)
        try:
            choiceID = delay_print(int(input('Type in the number of your choice to progress, ' +
                                             'type in letters to open options: ')))
            get_next_scene(choiceID)
            game_progress()
        except ValueError:
            render_options()
    else:
        print("Game Over!")
        render_menu()


def start_game():
    skip_line(1)
    while True:
        start = input("Type start to begin: ")
        if start == "start":
            return

