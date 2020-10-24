from menu import *


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
def get_difficulty(choiceID):
    eventID = get_event(choiceID)
    sql = c.execute('SELECT Difficulty FROM Event WHERE EventID = ' + str(eventID))
    difficulty = c.fetchall()
    return difficulty[0][0]


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


def movement_phase(distance):
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
    enemyAgility = difficulty + CurrEnemy.stats[4]
    minScore = check_success(currAccuracy, enemyAgility) - (weaponData[4] - distance) / 1000
    minScore = math.trunc(minScore)
    numHits = count_hit(numShots, minScore, 1)
    return numHits


def calc_wound(difficulty, weaponData, distance):
    numHits = calc_numHits(difficulty, weaponData, distance)
    if numHits > 0:
        print(str(numHits) + " of your shots hit the targets")
        weaponDamage = weaponData[3] / 10
        minScore = check_success(weaponDamage, CurrEnemy.stats[3])
        totalDamage = count_hit(numHits, minScore, weaponDamage)
        if totalDamage > 0:
            CurrEnemy.wound(totalDamage)
            if CurrEnemy.check_death():
                print("Congratulations on killing this enemy. Good job! Now a few billion more to go..\n")
        else:
            print("You didn't wound the enemy. Maybe get a better weapon next time rather than a flashlight. \n")
    else:
        print("You missed every shot! Improve your accuracy next time! If you manage to survive..\n")


# Player turn to fight, what they can do depends on the phase
def player_turn(phase, difficulty, survivalChance, distance):
    global Player
    global currEnemy
    if phase == "Movement":
        return movement_phase(distance)
    elif phase == "Range":
        print("You are at the range phase, you can shoot at the enemy. Your accuracy stats and your weapon "
              "stats will determine success. \n")
        show_stats()
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
                print("Your weapon does not have enough range. Pick another weapon or enter " + BUTTON +
                      " to skip this turn \n")

        fight = input("You may press " + BUTTON + " to shoot. Be warned, those who shoot first will not be "
                                                  "able to make the first blow in melee")
        if fight.lower() == BUTTON:
            calc_wound(difficulty, weaponData, distance)
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
    autoResolve = input("Do you want to auto-resolve this fight? Enter " + BUTTON + " to auto-resolve.")
    CurrEnemy = Enemy(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5])
    if autoResolve == BUTTON:
        auto_resolve(data[0], difficulty, survivalChance)
    else:
        manual_fight(difficulty, survivalChance)
