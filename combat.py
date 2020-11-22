from menu import *
import random


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


# Set the current enemy based on the event id
def set_current_enemy(eventID):
    sql = c.execute(
        'SELECT Enemies.EnemyID, EnemyInitiative, EnemyHealth, EnemyStrength, EnemyEndurance, EnemyDurability, '
        'EnemyAgility, EnemyAccuracy FROM Enemies JOIN Event WHERE Event.EventID = ' + str(eventID) +
        ' AND Enemies.EnemyID = Event.EnemyID ')
    data = c.fetchall()
    CurrEnemy = Enemy(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7])
    return CurrEnemy


# Show Player stats and inventory items
def show_stats(Player):
    wView = input("Enter " + BUTTON + " to view weapon stats, any other button to skip: ")
    if wView.lower() == BUTTON:
        Player.show_inventory()
    skip_line(1)
    cView = input("Enter " + BUTTON + " to view your character stats, any other button to skip: ")
    if cView.lower() == BUTTON:
        Player.show_stats()
    skip_line(1)


# Display the options the player can take in the event and ask for player's choice
def provide_event_option(currState):
    sql = c.execute('SELECT OptionDescription FROM PhaseOption WHERE PhaseID = ' + str(currState))
    data = c.fetchall()
    for option in data:
        delay_print(option[0])
    skip_line(1)
    while True:
        try:
            choice = int(input("Type in the number of your choice: "))
            if choice > len(data):
                print("Please type a valid value")
            return choice
        except ValueError:
            print("Please type a valid value")


# Get all the info of the current phase, including description and options
def get_phase_info(Player, currState):
    delay_print(get_phase_description(currState))
    show_stats(Player)
    choice = provide_event_option(currState)
    skip_line(2)
    return choice


# Enable weapon selection
def weapon_selection(Player, distance):
    print("Select your weapon. Make sure it has enough range.")
    Player.show_inventory()
    error = True
    while error:
        try: 
            currWeapon = int(input("Enter the id of the weapon you would like to use: "))
        except valueError:
            print("Please input an integer value")
        else:
            error = False
    while Player.check_weapon_usability(currWeapon):
        currWeapon = int(input("Your chosen weapon is broken, select another weapon: "))
        Player.show_inventory()
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


# Compare which weapon has higher damage output, used for AI
def weapon_damage_comparison(data):
    largestDamage = 0
    currWeapon = 0
    for weapon in data:
        if weapon[1] >= largestDamage:
            largestDamage = weapon[1]
            currWeapon = weapon[0]
    return currWeapon


# Get the ai weapon based on range and damage output
def get_ai_weapon_id(CurrEnemy, type):
    data = []
    if type == "Range":
        sql = c.execute('SELECT TypeOfWeapon.TypeID,Damage FROM TypeOfWeapon JOIN EnemyWeapons WHERE '
                        'EnemyWeapons.EnemyID = ' + str(CurrEnemy.enemyID) +
                        ' AND TypeOfWeapon.TypeID = EnemyWeapons.TypeID AND TypeOfWeapon.WeaponClass = "Range"')
        data = c.fetchall()
    elif type == "CQC":
        sql = c.execute('SELECT TypeOfWeapon.TypeID,Damage FROM TypeOfWeapon JOIN EnemyWeapons WHERE '
                        'EnemyWeapons.EnemyID = ' + str(CurrEnemy.enemyID) +
                        ' AND TypeOfWeapon.TypeID = EnemyWeapons.TypeID')
        data = c.fetchall()
    if data:
        currWeapon = weapon_damage_comparison(data)
        sql = c.execute('SELECT TypeID FROM TypeOfWeapon WHERE TypeID = ' + str(currWeapon))
        data = c.fetchall()
        return data[0][0]
    return 0


# Get the new distance after the player moved
def get_new_distance(Player, distance):
    maxDisplacement = math.trunc(Player.stats[AGILITY] ^ 2 + Player.stats[ENDURANCE] * 2) * 10
    error = True
    while error:
        try:
            displacement = int(input("Enter your desired movement, you can only move up to " +
                                     str(maxDisplacement) + " m: "))
            if displacement > maxDisplacement:
                displacement = maxDisplacement
            if displacement > distance:
                displacement = distance
                delay_print("You tried to move farther than the actual distance between you and the enemy. "
                            "Unfortunately, your escape attempt did not work and they have blocked your way. \n ")
            distance = distance - displacement
            print("You moved a total of " + str(displacement) + " m")
            error = False
        except ValueError:
            print("Please input an integer value.")
    return distance


# Player movement turn
def player_move(Player, currState, distance):
    delay_print(get_phase_description(currState))
    skip_line(1)
    delay_print("You are at the movement phase, you are " + str(distance) + " m away from the enemy.")
    skip_line(2)
    initiativeCost = get_initiative_cost(currState, 1)
    if Player.currInitiative >= initiativeCost:
        delay_print("You may attempt to move forward. Warning! Movement decreases your initiative and you may "
                    "not be able to shoot first next turn or do anything at all.")
        skip_line(2)
        checkWeapon = input("You currently have " + str(Player.currInitiative) + " initiative points. Enter " + BUTTON +
                            " to check your weapon range, maybe you can shoot next turn without moving: \n")
        if checkWeapon == BUTTON:
            Player.show_inventory()
        skip_line(3)
        delay_print("The maximum distance you can move this turn can be found by adding the square of your agility "
                    "score by twice your endurance score the multiply that by 10.")
        skip_line(2)
        choice = provide_event_option(currState)
        if choice == 1:
            Player.currInitiative -= initiativeCost
            return get_new_distance(Player, distance)
    else:
        delay_print("Unfortunately, you don't have enough initiative points to move this turn. You need " +
                    str(initiativeCost) + " points and you only have " + str(Player.currInitiative))
    return distance


# AI movement phase
def ai_move(CurrEnemy, currState, distance):
    initiativeCost = get_initiative_cost(currState, 1)
    if CurrEnemy.currInitiative >= initiativeCost:
        maxDisplacement = math.trunc(CurrEnemy.stats[AGILITY] ^ 2 + CurrEnemy.stats[ENDURANCE] * 2) * 10
        displacement = random.randint(0, maxDisplacement)
        if displacement > distance:
            displacement = distance
        distance -= displacement
        print("The enemy moved " + str(displacement) + " meters.")
    return distance


# Count the number of shots that are successful
def count_hit(maxNum, minScore):
    totalShots = 0
    for i in range(0, maxNum):
        rand = random.randint(1, 10)
        if rand >= minScore:
            totalShots += 1
    return totalShots


# Calculation the total number of possible hits
def calc_numHits(Attacker, Defender, weaponData, difficulty, distance):
    numShots = math.trunc(weaponData[RATE_OF_FIRE] / 10)
    print("Shot " + str(numShots) + " times")
    attackerAccuracy = Attacker.stats[ACCURACY] - difficulty
    defenderAgility = difficulty + Defender.stats[AGILITY]
    minScore = check_success(attackerAccuracy, defenderAgility) - (weaponData[WEAPON_RANGE] - distance) / 1000
    minScore = math.trunc(minScore)
    numHits = count_hit(numShots, minScore)
    return numHits


# Calculate the shooting damage
def calc_shooting_damage(Attacker, Defender, currWeapon, difficulty, distance, currState, choice):
    weaponData = get_weapon_data(currWeapon)
    numHits = calc_numHits(Attacker, Defender, weaponData, difficulty, distance)
    if numHits > 0:
        print(str(numHits) + " shots have hit their mark.")
        weaponDamage = weaponData[WEAPON_DAMAGE] / 100
        minScore = check_success(weaponDamage, Defender.stats[DURABILITY])
        totalDamage = count_hit(numHits, minScore)
        Defender.stats[HEALTH] = Defender.stats[DURABILITY] - totalDamage
        print("Target HP is now at: " + str(Defender.stats[HEALTH]))
        Attacker.currInitiative -= get_initiative_cost(currState, choice)
    else:
        print("No hit! All shots have missed!")


# Player's turn to shoot
def player_shoot(Player, CurrEnemy, distance, currState, difficulty):
    choice = get_phase_info(Player, currState)
    initiativeCost = get_initiative_cost(currState, choice)
    while Player.currInitiative < initiativeCost:
        delay_print("Unfortunately, you don't have enough initiative points for this action. You need " +
                    str(initiativeCost) + " points and you only have " + str(Player.currInitiative))
        choice = provide_event_option(currState)
        initiativeCost = get_initiative_cost(currState, choice)
    if choice == 1:
        currWeapon = weapon_selection(Player, distance)
        if currWeapon != 0:
            print("Your turn to shoot \n")
            calc_shooting_damage(Player, CurrEnemy, currWeapon, difficulty, distance, currState, 1)
            Player.damage_weapon(currWeapon)
            skip_line(2)


# AI's turn to shoot
def ai_shoot(CurrEnemy, Player, difficulty, distance, currState):
    initiativeCost = get_initiative_cost(currState, 1)
    if CurrEnemy.currInitiative >= initiativeCost:
        currWeapon = get_ai_weapon_id(CurrEnemy, "Range")
        if currWeapon != 0:
            print("Enemy turn to shoot \n")
            calc_shooting_damage(Player, CurrEnemy, currWeapon, difficulty, distance, currState, 1)
        skip_line(2)


# Execute the movement state
def execute_movement(Player, CurrEnemy, distance, currState):
    if Player.currInitiative >= CurrEnemy.currInitiative:
        distance = player_move(Player, currState, distance)
        skip_line(2)
        distance = ai_move(CurrEnemy, currState, distance)
    else:
        distance = ai_move(CurrEnemy, currState, distance)
        skip_line(2)
        distance = player_move(Player, currState, distance)
    return distance


# Execute the shooting state
def execute_shooting(Player, CurrEnemy, distance, difficulty, currState):
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
    time.sleep(WAIT_TIME)


# Set melee up based on the choice of the person
def melee_option(choice, currWeapon, Object):
    if choice == 1:
        if Object.defending:
            Object.disable_guard()
        Object.attack(currWeapon)
    else:
        Object.enable_guard(currWeapon)


# Player's melee turn, get the choice the player wants and set melee phase up
def player_melee(Player, currState, distance):
    choice = get_phase_info(Player, currState)
    currWeapon = weapon_selection(Player, distance)
    melee_option(choice, currWeapon, Player)


# AI's melee turn, randomize the choice and set melee phase up
def ai_melee(CurrEnemy):
    currWeapon = get_ai_weapon_id(CurrEnemy, "CQC")
    choice = random.randint(1, 2)
    melee_option(choice, currWeapon, CurrEnemy)


# Calculate the result of the melee
def melee_result(Player, CurrEnemy):
    diceRoll = random.randint(0, 6)
    skip_line(3)
    print("Your HP is at: " + str(Player.stats[HEALTH]))
    print("Enemy HP is at: " + str(CurrEnemy.stats[HEALTH]))
    skip_line(1)
    print("Your attack output is at: " + str(Player.damage))
    print("Enemy attack output is at: " + str(CurrEnemy.damage))
    skip_line(2)
    if Player.defending and not CurrEnemy.defending:
        print("Enemy decided to attack \n")
        print("You are defending \n")
        Player.durability -= diceRoll
        Player.stats[HEALTH] -= (CurrEnemy.damage - Player.durability)
    elif not Player.defending and CurrEnemy.defending:
        print("You decided to attack \n")
        print("The enemy is defending \n")
        CurrEnemy.durability -= diceRoll
        CurrEnemy.stats[HEALTH] -= (Player.damage - CurrEnemy.durability)
    elif not Player.defending and not CurrEnemy.defending:
        print("Both you and the enemy decided to attack \n")
        if Player.stats[AGILITY] >= CurrEnemy.stats[AGILITY]:
            CurrEnemy.stats[HEALTH] -= (Player.damage - CurrEnemy.durability)
            if not CurrEnemy.check_living():
                return
            Player.stats[HEALTH] -= (CurrEnemy.damage - Player.durability)
        else:
            Player[HEALTH] -= (CurrEnemy.damage - Player.durability)
            if not Player.check_living():
                return
            CurrEnemy.stats[HEALTH] -= (Player.damage - CurrEnemy.durability)
    else:
        print("Both you and the enemy decided to guard. \n")
    skip_line(1)
    print("Your durability is at: " + str(Player.durability))
    print("Enemy durability is at: " + str(CurrEnemy.durability))
    skip_line(3)
    print("Your HP is now at: " + str(Player.stats[HEALTH]))
    print("Enemy HP is now at: " + str(CurrEnemy.stats[HEALTH]))
    time.sleep(WAIT_TIME)


# Execute the melee phase
def execute_melee(Player, CurrEnemy, distance, currState):
    if Player.currInitiative >= CurrEnemy.currInitiative:
        player_melee(Player, currState, distance)
        skip_line(2)
        ai_melee(CurrEnemy)
    else:
        ai_melee(CurrEnemy)
        skip_line(2)
        player_melee(Player, currState, distance)
    melee_result(Player, CurrEnemy)


# Find what the next phase will be
def find_next_state(Player, CurrEnemy, distance, currState):
    if currState == MOVEMENT:
        skip_line(5)
        return SHOOTING
    elif currState == SHOOTING:
        skip_line(5)
        if not Player.check_living() or not CurrEnemy.check_living():
            return EVENT_END
        if distance < MELEE_DISTANCE:
            return MELEE
        return MOVEMENT
    elif currState == MELEE:
        skip_line(5)
        if not Player.check_living() or not CurrEnemy.check_living():
            return EVENT_END
        if distance > MELEE_DISTANCE:
            print("You are too far away for melee actions, proceeding to movement phase")
            return MOVEMENT
        return MELEE
    else:
        return EVENT_END


# Increase initiative after each phase so that game doesn't get stuck
def increase_initiative(Player, CurrEnemy, incr):
    Player.currInitiative += incr
    CurrEnemy.currInitiative += incr
    if Player.currInitiative > Player.stats[0]:
        Player.currInitiative = Player.stats[0]
    if CurrEnemy.currInitiative > CurrEnemy.stats[0]:
        CurrEnemy.currInitiative = CurrEnemy.stats[0]


# Evaluate next phase: increase initiative and find the next state
def evaluate_state(Player, CurrEnemy, distance, currState):
    increase_initiative(Player, CurrEnemy, INITIATIVE_INCREASE)
    currState = find_next_state(Player, CurrEnemy, distance, currState)
    return currState


# Let the player receive exp if they survive the event. If they don't survive, report their death
def receive_exp(Player, CurrEnemy):
    if Player.check_living():
        Player.exp += CurrEnemy.stats[1]
        if Player.exp >= ASC_EXP:
            Player.ascend()
        return ALIVE
    else:
        return DEAD
