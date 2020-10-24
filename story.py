from menu import *

# Game ending results in either restart or exit
def end_game():
    global currScene
    print("Game Over!")
    time.sleep(1)
    try:
        restart = int(input("Input any integer to restart. Input any letter to exit: "))
        currScene = 1
        return restart
    except ValueError:
        exit_game()


# Check the minimum success based on comparison between attacker and defender score
def check_success(attacker, defender):
    if attacker > 2 * defender:
        return 1
    elif attacker > 1.5 * defender:
        return 2
    elif attacker > defender:
        return 3
    elif attacker == defender:
        return 4
    elif attacker < defender:
        return 5
    elif attacker < 1.5 * defender:
        return 6
    else:
        return 7


# Get the event of the current scene
def get_event(choiceID):
    sql = c.execute('SELECT StoryEvent FROM Storyline WHERE TextID = ' + str(choiceID))
    data = c.fetchall()
    return data[0][0]


# Check you can run an event
def event_exists(choiceID):
    event = get_event(choiceID)
    sql = c.execute('SELECT EventID FROM Event')
    data = c.fetchall()
    for val in data:
        if val[0] == event:
            return True
    return False


# Get the difficulty level of the event
def get_difficulty(choiceID):
    eventID = get_event(choiceID)
    sql = c.execute('SELECT Difficulty FROM Event WHERE EventID = ' + str(eventID))
    difficulty = c.fetchall()
    return difficulty[0][0]


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


# Auto resolving the fight event, randomized and based on stats
def auto_resolve(enemyData, difficulty, survivalChance):
    return


# Show all stats
def show_stats():
    wView = input("Enter w to view weapon stats, any other button to skip: ")
    if wView.lower() == "w":
        Player.show_inventory()
    cView = input("Enter c to view your character stats, any other button to skip: ")
    if cView.lower() == "c":
        Player.show_stats()


# Get the data of the chosen weapons
def select_weapon():
    wChoice = int(input("Select your weapon: "))
    weaponData = get_weapon_data(wChoice)
    return weaponData


# Player in melee
def player_melee(difficulty, survivalChance):
    weaponData = select_weapon()
    currAgility = Player.stats[4] - difficulty
    enemyAgility = difficulty + CurrEnemy.stats[4]
    min_score = check_success(currAgility, enemyAgility) + survivalChance / 100
    rand = random.randint(1, 10)
    if rand > min_score:
        damage = weaponData[3] / 5
        CurrEnemy.wound(damage)
    elif rand > min_score / 2:
        damage = weaponData[3] / 5
        CurrEnemy.reduce_durability(damage)


def get_new_distance(distance):
    max_displacement = (Player.stats[4] * 2 + Player.stats[2] / 2) / 10
    displacement = int(input("Enter your desired movement, you can only move up to " + str(max_displacement) + " m: "))
    if displacement > distance:
        displacement = distance
        print("You tried to move farther than the actual distance between you and the enemy. Unfortunately, your escape"
              " attempt did not work and they have blocked your way. Next time just try to flee the other direction. ")
    distance -= displacement
    return distance


def calc_numHits(difficulty, weaponData, distance):
    currAccuracy = Player.stats[5] - difficulty
    enemyAgility = difficulty + CurrEnemy.stats[4]
    min_score = check_success(currAccuracy, enemyAgility) - (weaponData[4] - distance) / 1000
    min_score = math.trunc(min_score)
    numHits = 0
    numShots = weaponData[2][0] / 10
    for i in range(0, numShots):
        rand = random.randint(1, 10)
        if rand > min_score:
            numHits += 1
    return numHits


# Player turn to fight, what they can do depends on the phase
def player_turn(phase, difficulty, survivalChance, distance):
    global Player
    global currEnemy
    if phase == "Movement":
        distanceInMeters = distance / 10
        checkWeapon = input("You are at the movement phase, you are " + str(distanceInMeters) +
                            " m away from the enemy. You may attempt to move forward. Warning! "
                            "Movement decreases your initiative. Enter " + BUTTON + " to check your weapon range \n")
        if checkWeapon == BUTTON:
            Player.show_inventory()
        print("The maximum distance you can move this turn can be found by adding twice your agility score "
              "by half your endurance score. \n")
        move = input("Enter " + BUTTON + " to move forward, you may enter any other letter to skip: ")
        if move == BUTTON:
            return get_new_distance(distance)
        return distance
    elif phase == "Range":
        print("You are at the range phase, you can shoot at the enemy. Your accuracy stats and your weapon "
              "stats will determine success. \n")
        show_stats()
        notInRange = True
        while notInRange:
            print("Select your weapon. Make sure it has enough range")
            Player.show_inventory()
            weaponData = select_weapon()
            if weaponData[WEAPON_RANGE] >= distance:
                print("This weapon has enough range, you may now shoot")
                notInRange = False
            else:
                print("Your weapon does not have enough range. Pick another one or wait until the ")

        fight = input("You may press " + BUTTON + " to shoot. Be warned, those who shoot first will not be "
                                                  "able to make the first blow in melee")
        if fight.lower() == BUTTON:

            numHits = calc_numHits(difficulty, weaponData, distance)
            if numHits > 0:
                print(str(numHits) + " of your shots hit the targets")
                totalDamage = 0
                weaponDamage = weaponData[3] / 10
                min_score = check_success(weaponDamage, CurrEnemy.stats[3])
                for i in range(0, numHits):
                    rand = random.randint(1, 10)
                    if rand >= min_score:
                        totalDamage += numHits
                if totalDamage > 0:
                    CurrEnemy.wound(totalDamage)
                    if CurrEnemy.check_death():
                        print("Congratulations on killing this enemy. Good job! Now a few billion more to go..")
                else:
                    print("You didn't wound the enemy. Maybe get a better weapon next time rather than a flashlight.")
            else:
                print("You missed every shot! Improve your accuracy next time! If you survive..")
    else:
        fight = input("You are at the melee phase, you may now engage in glorious close quarter combat. You will now "
                      "enter combat, no choice here unless you want to die. In that case, press " + BUTTON +
                      " to do nothing and commit sudoku. If you wish to fight, then any other button will do: \n")
        if fight == BUTTON:
            Player.kill()
            print("Game over.")
            render_menu()
        else:
            show_stats()
            Player.show_inventory()
            player_melee(difficulty, survivalChance)
            enemy_turn(phase, difficulty, survivalChance)


# Enemy turn to fight, what they will do is slightly randomized and based on enemy stats
def enemy_turn(phase, difficulty, survivalChance, distance):
    global Player
    global currEnemy
    if phase == "Movement":
        max_displacement = (currEnemy.stats[4] * 2 + currEnemy.stats[2] / 2) / 10
        displacement = random.randint(0, max_displacement)
        distance -= displacement
        print("The enemy moved " + str(displacement) + " m")
        return distance
    elif phase == "Range":
        return
    return


# Initiating manual combat
def manual_fight(difficulty, survivalChance):
    phaseList = ["Movement", "Range"]
    not_in_melee = True
    distance = random.randint(100, 1000)
    while not_in_melee:
        for phase in phaseList:
            distance = player_turn(phase, difficulty, survivalChance, distance)
            enemy_turn(phase, difficulty, survivalChance, distance)
        if distance < 100:
            print("You are now close enough to engage in melee combat. En garde!")
            not_in_melee = False
    while Player.stats[0] > 0 or CurrEnemy.stats[0] > 0:
        player_turn("Melee", difficulty, survivalChance, distance)
    if Player.stats[0] < 0:
        Player.kill()


# Initial calculation for combat result
def combat_calc(choiceID):
    global CurrEnemy
    difficulty = get_difficulty(choiceID)
    sql = c.execute('SELECT SurvivalChance FROM EventNode WHERE NodeID = ' + str(choiceID))
    survivalChance = c.fetchall()
    sql = c.execute('SELECT EnemyStrength, EnemyEndurance, EnemyDurability, EnemyAgility, EnemyAccuracy FROM Enemies '
                    'JOIN Event WHERE Event.EnemyID = Enemies.EnemyID ')
    data = c.fetchall()
    print(data[0])
    autoResolve = input("Do you want to auto-resolve this fight (Y/N)?")
    CurrEnemy = Enemy(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5])
    if autoResolve:
        auto_resolve(data[0], difficulty, survivalChance)
    else:
        manual_fight(difficulty, survivalChance)


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
    if check_child(STORY):
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
