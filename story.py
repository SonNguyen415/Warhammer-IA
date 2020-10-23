from menu import *


# Game ending results in either restart or exit
def end_game():
    print("Game Over!")
    time.sleep(1)
    try:
        restart = int(input("Input any integer to restart. Input any letter to exit: "))
        render_menu()
        start_game()
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
def get_event():
    sql = c.execute('SELECT StoryEvent FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data


# Get the difficulty level of the event
def get_difficulty():
    eventID = get_event()
    sql = c.execute('SELECT Difficulty FROM Events WHERE EventID = ' + str(eventID[0][0]))
    difficulty = c.fetchall()
    return difficulty[0][0]


# Get the scene content of the current node
def get_node(nodeID):
    sql = c.execute('SELECT NodeContent FROM EventNode WHERE NodeID = ' + str(nodeID))
    data = c.fetchall()
    return data[0][0]


# Check if the node has children leading from it, if not, then event has ended.
def check_node_child(nodeID):
    sql = c.execute('SELECT Children FROM EventNode WHERE NodeID = ' + str(nodeID))
    data = c.fetchall()
    return data[0][0]


# Get the content of the choices you can make for the event
def get_event_choices(pointer):
    sql = c.execute('SELECT NodeContent FROM EventNode WHERE TextPointer = ' + str(pointer))
    data = c.fetchall()
    return data


# Confirm that the selected choice is correct
def confirm_event_choice(choiceID):
    sql = c.execute('SELECT TextID FROM EventNode WHERE NodePointer  = ' + str(choiceID))
    data = c.fetchall()
    return data


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
def get_chosen_weapon_data():
    wChoice = int(input("Select your weapon: "))
    weaponData = get_weapon_data(wChoice)
    return weaponData


def player_melee(difficulty, survivalChance):
    weaponData = get_chosen_weapon_data()
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


def player_turn(phase, difficulty, survivalChance, distance):
    global Player
    global currEnemy
    if phase == "Movement":
        print("You are at the movement phase, you are " + str(distance) + " away from the enemy. You may attempt to " +
              "move forward. Warning, those who haven't move can shoot first. \n")
        print("The distance you can move this turn can be found by adding twice your agility score "
              "by half your endurance score. \n")
        move = input("Enter m to move forward, you may enter any other letter to skip: ")
        if move == "m":
            displacement = Player.stats[4] * 2 + Player.stats[2] / 2
            if displacement > distance:
                displacement = distance
            distance -= displacement
        return distance
    elif phase == "Range":
        print("You are at the range phase, you can shoot at the enemy. Your accuracy stats and your weapon "
              "stats will determine success. \n")
        show_stats()
        fight = input("You may press s to shoot. Be warned, those who shoot first will not be able to make the first "
                      "blow in melee")
        if fight.lower() == "s":
            Player.show_inventory()
            weaponData = get_chosen_weapon_data()
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
            if numHits > 0:
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
                      "enter combat, no choice here unless you want to die. In that case, press x to do nothing and "
                      "commit sudoku. If you wish to fight, then any other button will do: \n")
        if fight == "x":
            Player.kill()
            print("Game over.")
            render_menu()
        else:
            show_stats()
            Player.show_inventory()
            player_melee(difficulty, survivalChance)
            enemy_turn(phase, difficulty, survivalChance)


def enemy_turn(phase, difficulty, survivalChance):
    player_melee(difficulty, survivalChance)
    return


def manual_fight(difficulty, survivalChance):
    phaseList = ["Movement", "Range"]
    not_in_melee = True
    distance = random.randint(100, 1000)
    while not_in_melee:
        for phase in phaseList:
            distance = player_turn(phase, difficulty, survivalChance, distance)
            enemy_turn(phase, difficulty, survivalChance)
        if distance < 100:
            not_in_melee = False
    while Player.stats[0] > 0 or CurrEnemy.stats[0] > 0:
        player_turn("Melee", difficulty, survivalChance, distance)
    if Player.stats[0] < 0:
        Player.kill()


def combat_calc(choiceID):
    global CurrEnemy
    difficulty = get_difficulty()
    sql = c.execute('SELECT SurvivalChance FROM EventNode WHERE NodeID = ' + str(choiceID))
    survivalChance = c.fetchall()
    sql = c.execute('SELECT EnemyStrength, EnemyEndurance, EnemyDurability, EnemyAgility, EnemyAccuracy FROM Enemies '
                    'JOIN Event WHERE Event.EnemyID = Enemies.EnemyID ')
    data = c.fetchall()
    enemyData = []
    for lst in data:
        enemyData.append(lst[0])
    autoResolve = input("Do you want to auto-resolve this fight (Y/N)?")
    CurrEnemy = Enemy(enemyData[0], enemyData[1], enemyData[2], enemyData[3], enemyData[4], enemyData[5])
    if autoResolve:
        auto_resolve(enemyData, difficulty, survivalChance)
    else:
        manual_fight(difficulty, survivalChance)


def get_next_node(choiceID, currNode):
    return


def play_event(nodeID):
    pause = True
    skip_line(2)
    delay_print(get_node(nodeID))
    if check_node_child(nodeID):
        while pause:
            skip_line(2)
            for choice in get_event_choices(nodeID):
                print(choice[0])
            skip_line(1)
            try:
                choiceID = int(input('Type in the number of your choice to progress, ' +
                                     'type in any letter to open options: '))
                choiceResult = confirm_event_choice(choiceID)
                while not choiceResult:
                    choiceID = int(input('Please type in the correct number, enter any letter to open options: '))

                pause = False
                get_next_node(choiceID, nodeID)
                play_event(nodeID)
            except ValueError:
                render_options()
    else:
        skip_line(5)
        end_game()
    return


def get_scene():
    global currScene
    sql = c.execute('SELECT TextContent FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data[0][0]


def get_story_choices():
    sql = c.execute('SELECT TextContent FROM Storyline WHERE TextPointer = ' + str(currScene))
    data = c.fetchall()
    return data


def confirm_choice(cID):
    sql = c.execute('SELECT TextID FROM Storyline WHERE TextPointer  = ' + str(cID))
    data = c.fetchall()
    return data


def scene_calc(choiceID):
    sql = c.execute('SELECT SceneChance FROM Storyline WHERE TextPointer = ' + str(choiceID))
    data = c.fetchall()
    arr = []
    for lst in data:
        arr.append(lst[0])
    ran = random.randint(0, 100)
    abs_diff = lambda list_value: abs(list_value - ran)
    nextScene = min(arr, key=abs_diff)
    return nextScene


def get_next_scene(cID):
    global currScene
    nextScene = scene_calc(cID)
    sql = c.execute('SELECT TextID FROM Storyline WHERE TextPointer  = ' + str(cID) + ' AND SceneChance = ' +
                    str(nextScene))
    data = c.fetchall()
    currScene = data[0][0]


def check_story_child():
    sql = c.execute('SELECT Children FROM Storyline WHERE TextID = ' + str(currScene))
    data = c.fetchall()
    return data[0][0]


def game_progress():
    global currScene
    pause = True
    if not get_event():
        nodeID = 1
        play_event(nodeID)
    skip_line(4)
    delay_print(get_scene())
    if check_story_child():
        while pause:
            skip_line(2)
            for choice in get_story_choices():
                print(choice[0])
            skip_line(1)
            try:
                choiceID = int(input('Type in the number of your choice to progress, ' +
                                     'type in any letter to open options: '))
                choiceResult = confirm_choice(choiceID)
                while not choiceResult:
                    choiceID = int(input('Please type a correct number, enter in any letter to open options: '))

                pause = False
                get_next_scene(choiceID)
                game_progress()
            except ValueError:
                render_options()
    else:
        skip_line(5)
        end_game()


def start_game():
    while True:
        try:
            start = int(input("Enter any integer to begin: "))
            game_progress()
        except ValueError:
            continue
