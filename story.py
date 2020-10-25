from combat import *
import combat


# Game ending results in either restart or exit
def end_game(currScene):
    print("Game Over!")
    time.sleep(WAIT_TIME)
    try:
        restart = int(input("Input any integer to restart. Input any letter to exit: "))
        return 1
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
def get_scene_content(currScene, sceneType, eventID=0):
    if sceneType == EVENT:
        sql = c.execute('SELECT EventDescription FROM Event WHERE EventID = ' + str(eventID))
    else:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data


# Check if the node has children leading from it, event or game will end if scene has no child
def check_child(currScene, sceneType, nodeID=0):
    if sceneType == EVENT:
        sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodePointer = ' + str(nodeID))
    else:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    data = c.fetchall()
    return data


# Get the content of the choices you can make for the event
def get_choices(currScene, sceneType, pointer=0):
    if sceneType == STORY:
        sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    else:
        sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodePointer = ' + str(pointer))
    data = c.fetchall()
    return data


# Confirm that the choice selected is valid
def confirm_choice(currScene, sceneType, cID):
    if sceneType == STORY:
        sql = c.execute('SELECT TextID FROM Storyline WHERE TextType  = ' + str(cID) +
                        ' AND TextPointer = ' + str(currScene))
    else:
        sql = c.execute('SELECT NodeID FROM EventNode WHERE NodePointer  = ' + str(cID))
    data = c.fetchall()
    return data[0][0]


# Get the list of scenes that can follow due to the choice selected
def get_scene_list(sceneType, choiceID):
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
    sceneList = get_scene_list(sceneType, choiceID)
    nextScene = scene_calc(sceneList)
    if sceneType == STORY:
        sql = c.execute('SELECT TextID FROM Storyline WHERE TextID = ' + str(nextScene))
        data = c.fetchall()
        return data[0][0]
    else:
        print("Stop here for now")
        exit_game()


# Begin the event
def play_event(Player, eventID):
    skip_line(10)
    delay_print(get_scene_content(EVENT, eventID))
    print("You have entered an event, you may not pause until you complete this event")
    CurrEnemy = set_current_enemy(eventID)
    distance = random.randint(100, 1000)
    difficulty = get_difficulty(eventID)
    currState = MOVEMENT
    while currState != EVENT_END:
        skip_line(2)
        if currState == MOVEMENT:
            if Player.currInitiative >= CurrEnemy.currInitiative:
                distance = player_move(Player, distance, currState)
                skip_line(2)
                distance = ai_move(CurrEnemy, distance)
            else:
                distance = ai_move(CurrEnemy, distance)
                skip_line(2)
                distance = player_move(Player, distance, currState)
            skip_line(2)
            print("You are now " + str(distance) + " meters away from the enemy.")
        elif currState == SHOOTING:
            if distance >= 2:
                if Player.currInitiative >= CurrEnemy.currInitiative:
                    player_shoot(Player, CurrEnemy, distance, currState, difficulty)
                    if not Player.check_living() or not CurrEnemy.check_living():
                        return
                    skip_line(2)
                    ai_shoot(CurrEnemy, Player, difficulty, distance, currState)
                else:
                    ai_shoot(CurrEnemy, Player, difficulty, distance, currState)
                    if not Player.check_living() or not CurrEnemy.check_living():
                        return
                    skip_line(2)
                    player_shoot(Player, CurrEnemy, distance, currState, difficulty)
        elif currState == MELEE:
            if Player.currInitiative >= CurrEnemy.currInitiative:
                player_melee(Player, CurrEnemy, distance)
                if not Player.check_living() or not CurrEnemy.check_living():
                    return
                skip_line(2)
                ai_melee(CurrEnemy)
            else:
                ai_melee(CurrEnemy)
                if not Player.check_living() or not CurrEnemy.check_living():
                    return
                skip_line(2)
                player_melee(Player, CurrEnemy, distance)
        currState = evaluate_state(Player, CurrEnemy, distance, currState)


# Progress the game
def game_progress(currScene, Player):
    pause = True
    skip_line(4)
    scene_content = get_scene_content(currScene, STORY)
    delay_print(scene_content[0][0])
    if check_child(currScene, STORY) and Player.check_living():
        while pause:
            skip_line(2)
            for choice in get_choices(currScene, STORY):
                print(choice[0])
            skip_line(1)
            # try:
            choiceID = int(input('Type in the number of your choice to progress, ' +
                                 'type in any letter to open options: '))
            choiceResult = confirm_choice(currScene, STORY, choiceID)
            while not choiceResult:
                choiceID = int(input('Please type a valid number, enter in any letter to open options: '))
                choiceResult = confirm_choice(currScene, STORY, choiceID)
            pause = False
            if event_exists(choiceResult):
                eventID = get_event(choiceResult)
                play_event(Player, eventID)
            Player.reset_initiative()
            Player.corrupt(choiceResult)
            currScene = get_next_scene(STORY, choiceResult)
            game_progress(currScene, Player)
            # except ValueError:
            #     render_options(Player)
    else:
        skip_line(5)
        end_game(currScene)


# Confirmation for game start
def start_game():
    while True:
        start = input("Enter anything to continue, can't back out now: ")
        if start:
            skip_line(10)
            return
