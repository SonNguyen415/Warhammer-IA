from menu import *
import random


# Get the event of the current scene
def get_event(choiceID):
    sql = c.execute('SELECT StoryEvent FROM Storyline WHERE TextID = ' + str(choiceID))
    data = c.fetchall()
    return data[0][0]


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


# Get the difficulty level of the event
def get_difficulty(eventID):
    sql = c.execute('SELECT Difficulty FROM Event WHERE EventID = ' + str(eventID))
    difficulty = c.fetchall()
    return difficulty[0][0]


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


def set_current_enemy(eventID):
    global CurrEnemy
    sql = c.execute(
        'SELECT EnemyInitiative, EnemyStrength, EnemyEndurance, EnemyDurability, EnemyAgility, EnemyAccuracy '
        'FROM Enemies JOIN Event WHERE Event.EventID = ' + str(eventID) +
        ' AND Enemies.EnemyID = Event.EnemyID ')
    data = c.fetchall()
    CurrEnemy = Enemy(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6])


def provide_event_option(currState):
    sql = c.execute('SELECT OptionDescription FROM PhaseOption WHERE PhaseID = ' + str(currState))
    data = c.fetchall()
    for option in data:
        print(option[0])
        while True:
            try:
                choice = int(input("Type in the number of your choice: "))
                if choice > len(data):
                    print("Please type a valid value")
                    return choice
            except ValueError:
                print("Please type a valid value")


def get_initiative_cost(currState, choice):
    sql = c.execute('SELECT InitiativeCost FROM PhaseOption WHERE OptionID = ' + str(currState) +
                    ' AND OptionType = ' + str(choice))
    data = c.fetchall
    return data[0][0]


def get_new_distance(distance):
    max_displacement = (Player.stats[4] * 2 + Player.stats[2] / 2) / 10
    displacement = int(input("Enter your desired movement, you can only move up to " + str(max_displacement) + " m: "))
    if displacement > distance:
        displacement = distance
        print("You tried to move farther than the actual distance between you and the enemy. Unfortunately, your escape"
              " attempt did not work and they have blocked your way. Next time just try to flee the other direction. ")
    distance -= displacement
    return distance


def count_hit(maxNum, minScore, x):
    total = 0
    for i in range(0, maxNum):
        rand = random.randint(1, 10)
        if rand >= minScore:
            total += x
    return total


def calc_numHits(difficulty, weaponData, distance):
    numShots = weaponData[2][0] / 10
    currAccuracy = Player.stats[5] - difficulty
    enemyAgility = difficulty + CurrEnemy.data[4]
    minScore = check_success(currAccuracy, enemyAgility) - (weaponData[4] - distance) / 1000
    minScore = math.trunc(minScore)
    numHits = count_hit(numShots, minScore, 1)
    return numHits


def calc_wound(difficulty, weaponData, distance):
    numHits = calc_numHits(difficulty, weaponData, distance)
    if numHits > 0:
        print(str(numHits) + " of your shots hit the targets")
        weaponDamage = weaponData[3] / 10
        minScore = check_success(weaponDamage, CurrEnemy.data[3])
        totalDamage = count_hit(numHits, minScore, weaponDamage)
        if totalDamage > 0:
            CurrEnemy.wound(totalDamage)
            if not CurrEnemy.check_living():
                print("Congratulations on killing this enemy. Good job! Now a few billion more to go..\n")
        else:
            print("You didn't wound the enemy. Maybe get a better weapon next time rather than a flashlight. \n")
    else:
        print("You missed every shot! Improve your accuracy next time! If you manage to survive..\n")


def player_move(currState):
    global distance
    global Player
    choice = provide_event_option(currState)
    if choice == 1:
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
            distance = get_new_distance(distance)
        Player.currInitiative -= get_initiative_cost(currState, choice)


def ai_move():
    return


def player_shoot(currState, difficulty):
    global Player
    show_stats()
    choice = provide_event_option(currState)
    if choice == 1:
        notInRange = True
        weaponData = []
        while notInRange:
            print("Select your weapon. Make sure it has enough range \n")
            Player.show_inventory()
            weaponData = select_weapon()
            if weaponData[WEAPON_RANGE] >= distance:
                print("This weapon has enough range, you may now shoot \n")
                notInRange = False
            else:
                print("Your chosen weapon does not have enough range. Pick another weapon or enter " + BUTTON +
                      " to skip this turn \n")
        fight = input("You may press " + BUTTON + " to shoot. Be warned, shooting will take up initiative")
        if fight.lower() == BUTTON:
            calc_wound(difficulty, weaponData, distance)
        Player.currInitiative -= get_initiative_cost(currState, choice)


def ai_shoot():
    return


def player_first(currState, difficulty):
    if currState == MOVEMENT:
        player_move(currState)
        ai_move()
    elif currState == SHOOTING:
        player_shoot(currState, difficulty)
        ai_shoot()
    elif currState == MELEE:
        print("In Melee")


def ai_first(currState, difficulty):
    if currState == MOVEMENT:
        ai_move()
        player_move(currState)
    elif currState == SHOOTING:
        ai_shoot()
        player_shoot(currState, difficulty)
    elif currState == MELEE:
        print("In Melee")


def execute_state(currState, difficulty):
    global Player
    global CurrEnemy
    if Player.currInitiative >= CurrEnemy.initiative:
        player_first(currState, difficulty)
    else:
        ai_first(currState, difficulty)


def evaluate_state(currState):
    global Player
    global CurrEnemy
    global distance
    if currState == MOVEMENT:
        return SHOOTING
    elif currState == SHOOTING:
        if distance < 100:
            return MELEE
        return SHOOTING
    elif currState == MELEE:
        if not Player.check_living() or not CurrEnemy.check_living():
            return EVENT_END
        return MELEE
    else:
        return EVENT_END
