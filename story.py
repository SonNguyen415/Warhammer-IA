from combat import *


# Game ending results in either restart or exit
def end_game():
    global currScene
    print("Game Over!")
    time.sleep(WAIT_TIME)
    try:
        restart = int(input("Input any integer to restart. Input any letter to exit: "))
        currScene = 1
        return restart
    except ValueError:
        exit_game()


# Check you can run an event
def event_exists(choiceID):
    event = get_event(choiceID)
    sql = c.execute('SELECT EventID FROM Event')
    data = c.fetchall()
    for val in data:
        if val[0] == event:
            return True
    return False


# Get the scene content of the current node
def get_scene_content(sceneType, nodeID=0):
    if sceneType == EVENT:
        sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodeID = ' + str(nodeID))
    else:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data


# Check if the node has children leading from it, event or game will end if scene has no child
def check_child(sceneType, nodeID=0):
    if sceneType == EVENT:
        sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodePointer = ' + str(nodeID))
    else:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    data = c.fetchall()
    return data


# Get the content of the choices you can make for the event
def get_choices(sceneType, pointer=0):
    if sceneType == STORY:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    else:
        sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodePointer = ' + str(pointer))
    data = c.fetchall()
    return data


# Confirm that the choice selected is valid
def confirm_choice(sceneType, cID):
    if sceneType == STORY:
        sql = c.execute('SELECT TextID FROM Storyline WHERE TextType  = ' + str(cID) +
                        ' AND TextPointer = ' + str(currScene))
    else:
        sql = c.execute('SELECT NodeID FROM EventNode WHERE NodePointer  = ' + str(cID))
    data = c.fetchall()
    return data[0][0]


# Get the list of scenes that can follow due to the choice selected
def scene_list(sceneType, choiceID):
    if sceneType == STORY:
        sql = c.execute('SELECT TextID FROM Storyline WHERE TextPointer = ' + str(choiceID))
    else:
        sql = c.execute('SELECT NodeID FROM EventNode WHERE NodePointer = ' + str(choiceID))
    data = c.fetchall()
    return data


# Calculating which scene will follow based on the scene chance
def scene_calc(sceneList):
    arr = []
    for lst in sceneList:
        arr.append(lst[0])
    ran = random.randint(0, 100)
    abs_diff = lambda list_value: abs(list_value - ran)
    nextScene = min(arr, key=abs_diff)
    return nextScene


# Get the next scene
def get_next_scene(sceneType, choiceID):
    global currScene
    sceneList = scene_list(sceneType, choiceID)
    nextScene = scene_calc(sceneList)
    if sceneType == STORY:
        sql = c.execute('SELECT TextID FROM Storyline WHERE TextID = ' + str(nextScene))
        data = c.fetchall()
        currScene = data[0][0]
    else:
        print("Stop here for now")
        exit_game()


# Begin the event
def play_event(nodeID):
    pause = True
    skip_line(2)
    delay_print(get_scene_content(EVENT, nodeID))
    if check_child(EVENT, nodeID):
        while pause:
            skip_line(2)
            for choice in get_choices(EVENT, nodeID):
                print(choice[0])
            skip_line(1)
            try:
                choiceID = int(input('Type in the number of your choice to progress, ' +
                                     'type in any letter to open options: '))
                choiceResult = confirm_choice(EVENT, choiceID)
                while not choiceResult:
                    choiceID = int(input('Please type in the correct number, enter any letter to open options: '))
                    choiceResult = confirm_choice(EVENT, choiceID)
                pause = False
                combat_calc(choiceResult)
                get_next_scene(EVENT, choiceResult)
                play_event(nodeID)
            except ValueError:
                render_options()
    else:
        skip_line(5)
        end_game()
    return


# Progress the game
def game_progress():
    global currScene
    global Player
    pause = True
    skip_line(4)
    scene_content = get_scene_content(STORY)
    delay_print(scene_content[0][0])
    if check_child(STORY) and Player.check_living():
        while pause:
            skip_line(2)
            for choice in get_choices(STORY):
                print(choice[0])
            skip_line(1)
            try:
                choiceID = int(input('Type in the number of your choice to progress, ' +
                                     'type in any letter to open options: '))
                choiceResult = confirm_choice(STORY, choiceID)
                while not choiceResult:
                    choiceID = int(input('Please type a valid number, enter in any letter to open options: '))
                    choiceResult = confirm_choice(STORY, choiceID)
                pause = False
                if event_exists(choiceResult):
                    play_event(1)
                Player.corrupt(choiceResult)
                get_next_scene(STORY, choiceResult)
                game_progress()
            except ValueError:
                render_options()
    else:
        skip_line(5)
        end_game()


# Confirmation for game start
def start_game():
    while True:
        start = input("Enter anything to continue, can't back out now: ")
        if start:
            return
