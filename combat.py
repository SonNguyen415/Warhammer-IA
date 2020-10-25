from menu import *
import random
import menu


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
def show_stats(Player):
    wView = input("Enter " + BUTTON + " to view weapon stats, any other button to skip: ")
    if wView.lower() == BUTTON:
        Player.show_inventory()
    skip_line(1)
    cView = input("Enter " + BUTTON + " to view your character stats, any other button to skip: ")
    if cView.lower() == BUTTON:
        Player.show_stats()
    skip_line(1)


def set_current_enemy(eventID):
    sql = c.execute(
        'SELECT Enemies.EnemyID, EnemyInitiative, EnemyHealth, EnemyStrength, EnemyEndurance, EnemyDurability, '
        'EnemyAgility, EnemyAccuracy FROM Enemies JOIN Event WHERE Event.EventID = ' + str(eventID) +
        ' AND Enemies.EnemyID = Event.EnemyID ')
    data = c.fetchall()
    CurrEnemy = Enemy(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7])
    return CurrEnemy


def get_phase_description(currState):
    sql = c.execute('SELECT PhaseDescription FROM EventPhase WHERE PhaseID = ' + str(currState))
    data = c.fetchall()
    return data[0][0]


def provide_event_option(currState):
    sql = c.execute('SELECT OptionDescription FROM PhaseOption WHERE PhaseID = ' + str(currState))
    data = c.fetchall()
    for option in data:
        print(option[0])
    skip_line(1)
    while True:
        try:
            choice = int(input("Type in the number of your choice: "))
            if choice > len(data):
                print("Please type a valid value")
            return choice
        except ValueError:
            print("Please type a valid value")


def get_initiative_cost(currState, choice):
    sql = c.execute('SELECT InitiativeCost FROM PhaseOption WHERE PhaseID = ' + str(currState) +
                    ' AND OptionType = ' + str(choice))
    data = c.fetchall()
    return data[0][0]


def get_phase_info(Player, currState):
    print(get_phase_description(currState))
    show_stats(Player)
    choice = provide_event_option(currState)
    skip_line(2)
    return choice


def weapon_selection(Player, distance):
    print("Select your weapon. Make sure it has enough range.")
    Player.show_inventory()
    currWeapon = int(input("Select your weapon: "))
    while not Player.check_weapon_usability(currWeapon):
        Player.show_inventory()
        currWeapon = int(input("Your chosen weapon is broken, select another weapon: "))
    weaponData = get_weapon_data(currWeapon)
    skip_line(2)
    while weaponData[WEAPON_RANGE] < (distance * 10):
        print("Your chosen weapon does not have enough range. Pick another weapon. You can also press " + BUTTON +
              " to skip if you don't find one with enough range. \n")
        print("Your weapon range in meters can be found by dividing the given range by 10.")
        Player.show_inventory()
        try:
            currWeapon = int(input("Select a new weapon, make sure it has enough range. Enter any letter to skip: "))
            weaponData = get_weapon_data(currWeapon)
        except ValueError:
            return 0
    return currWeapon


def get_ai_weapon_id(weaponList, type):
    for weapon in weaponList:
        sql = c.execute('SELECT TypeID FROM TypeOfWeapon WHERE TypeID = ' + str(weapon) + ' AND WeaponClass = "' +
                        type + '"')
        data = c.fetchall()
        if data:
            return data[0][0]
    return 0


def get_new_distance(Player, distance):
    maxDisplacement = math.trunc(Player.stats[4] ^ 2 + Player.stats[2] * 2) * 10
    displacement = int(input("Enter your desired movement, you can only move up to " + str(maxDisplacement) + " m: "))
    if displacement > distance:
        displacement = distance
        print("You tried to move farther than the actual distance between you and the enemy. Unfortunately, your escape"
              " attempt did not work and they have blocked your way. Next time just try to flee the other direction. ")
    distance = distance - displacement
    return distance


def count_hit(maxNum, minScore, x):
    total = 0
    for i in range(0, maxNum):
        rand = random.randint(1, 10)
        if rand >= minScore:
            total += x
    return total


def calc_numHits(Attacker, Defender, weaponData, difficulty, distance):
    numShots = math.trunc(weaponData[RATE_OF_FIRE] / 10)
    attackerAccuracy = Attacker.stats[5] - difficulty
    defenderAgility = difficulty + Defender.stats[4]
    minScore = check_success(attackerAccuracy, defenderAgility) - (weaponData[4] - distance) / 1000
    minScore = math.trunc(minScore)
    print(minScore)
    numHits = count_hit(numShots, minScore, 1)
    return numHits


def calc_shooting_damage(Attacker, Defender, currWeapon, difficulty, distance, currState, choice):
    weaponData = get_weapon_data(currWeapon)
    numHits = calc_numHits(Attacker, Defender, weaponData, difficulty, distance)
    if numHits > 0:
        print(str(numHits) + " shots have hit their mark.")
        weaponDamage = weaponData[WEAPON_DAMAGE] / 100
        minScore = check_success(weaponDamage, Defender.stats[3])
        totalDamage = count_hit(numHits, minScore, weaponDamage)
        Defender.stats[1] = Defender.stats[1] - totalDamage
        print("HP is now at: " + str(Defender.stats[1]))
        Attacker.currInitiative -= get_initiative_cost(currState, choice)
    else:
        print("No hit! All shots have missed!")
    time.sleep(WAIT_TIME)


def player_move(Player, distance, currState):
    print(get_phase_description(currState))
    skip_line(1)
    print("You are at the movement phase, you are " + str(distance) +
          " m away from the enemy. You may attempt to move forward.")
    checkWeapon = input("Warning! Movement decreases your initiative and you may not be able to shoot first next turn. "
                        "Enter " + BUTTON + " to check your weapon range: \n")
    if checkWeapon == BUTTON:
        Player.show_inventory()
    skip_line(3)
    print("The maximum distance you can move this turn can be found by adding the square of your agility score "
          "by twice your endurance score the multiply that by 10.")
    skip_line(2)
    choice = provide_event_option(currState)
    if choice == 1:
        Player.currInitiative -= get_initiative_cost(currState, choice)
        return get_new_distance(Player, distance)
    else:
        return distance


def ai_move(CurrEnemy, distance):
    maxDisplacement = math.trunc(CurrEnemy.stats[4] ^ 2 + CurrEnemy.stats[2] * 2) * 10
    displacement = random.randint(0, maxDisplacement)
    if displacement > distance:
        displacement = distance
    distance -= displacement
    print("The enemy moved " + str(displacement) + " meters.")
    return distance


def player_shoot(Player, CurrEnemy, distance, currState, difficulty):
    choice = get_phase_info(Player, currState)
    print("")
    if choice == 1:
        currWeapon = weapon_selection(Player, distance)
        if currWeapon != 0:
            calc_shooting_damage(Player, CurrEnemy, currWeapon, difficulty, distance, currState, 1)
            print("You shot the enemy, dealing much damage.")
            Player.damage_weapon(currWeapon)
            skip_line(2)


def ai_shoot(CurrEnemy, Player, difficulty, distance, currState):
    aiWeapon = get_ai_weapon(CurrEnemy.enemyID)
    currWeapon = get_ai_weapon_id(aiWeapon, "Range")
    if currWeapon != 0:
        calc_shooting_damage(Player, CurrEnemy, currWeapon, difficulty, distance, currState, 1)
    skip_line(2)
    return


def melee_option(choice, currWeapon, Object):
    if choice == 1:
        if Object.defending:
            Object.unguard()
        Object.attack(currWeapon)
    else:
        Object.guard(currWeapon)


def player_melee(Player, distance, currState):
    choice = get_phase_info(Player, currState)
    currWeapon = weapon_selection(Player, distance)
    melee_option(choice, currWeapon, Player)


def ai_melee(CurrEnemy):
    aiWeapon = get_ai_weapon(CurrEnemy.enemyID)
    currWeapon = get_ai_weapon_id(aiWeapon, "CQC")
    choice = random.randint(0, 1)
    melee_option(choice, currWeapon, CurrEnemy)


def evaluate_state(Player, CurrEnemy, distance, currState):
    if currState == MOVEMENT:
        skip_line(5)
        return SHOOTING
    elif currState == SHOOTING:
        skip_line(5)
        if not Player.check_living() or not CurrEnemy.check_living():
            return EVENT_END
        if distance < 2:
            return MELEE
        return MOVEMENT
    elif currState == MELEE:
        skip_line(5)
        if not Player.check_living() or not CurrEnemy.check_living():
            return EVENT_END
        if distance > 20:
            print("You are too far away for melee actions, proceeding to shooting phase")
            return SHOOTING
        return MELEE
    else:
        return EVENT_END
