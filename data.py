from config import *


# Get the current scene the saved character is at
def get_curr_progress(charID):
    sql = c.execute('SELECT Progress FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0][0]


# Get all weapon id from the Weapons
def get_weapon_id_list():
    sql = c.execute('SELECT WeaponID FROM Weapons')
    data = c.fetchall()
    return data


# Get weapon quality
def get_weapon_quality(wID):
    sql = c.execute('SELECT Quality FROM Weapons WHERE WeaponID = ' + str(wID))
    data = c.fetchall()
    return data[0][0]


# Get my weapons
def get_my_weapons(charID):
    sql = c.execute('SELECT WeaponID, Weapons.TypeID, WeaponType, Quality FROM Weapons JOIN TypeOfWeapon WHERE CharID '
                    '= ' + str(charID) + ' AND Weapons.TypeID = TypeOfWeapon.TypeID')
    data = c.fetchall()
    return data[0]


# Get all the weapons that you can buy
def get_purchasable_weapons(charLevel):
    sql = c.execute(
        'SELECT TypeID, WeaponType, WeaponSize, Cost FROM TypeOfWeapon WHERE WeaponLevel <= ' + str(charLevel))
    data = c.fetchall()
    return data


# Get the stats of a given weapon
def get_weapon_data(typeID):
    sql = c.execute('SELECT * FROM TypeOfWeapon WHERE TypeID = ' + str(typeID))
    data = c.fetchall()
    return data[0]


# Get the id of all the weapons an enemy possesses given their id
def get_ai_weapon(enemyID):
    sql = c.execute('SELECT TypeID FROM EnemyWeapons WHERE EnemyID = ' + str(enemyID))
    data = c.fetchall()
    return data[0]


# Get the info of the characters
def get_character_data(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Change character stats in the database to match the current data of the Player object
def update_character(Player):
    sql = c.execute('UPDATE Characters SET CharLevel = ' + str(Player.level) + ' WHERE CharID = ' + str(Player.charID))
    for i in range(0, len(BASE_STATS[0])):
        sql = c.execute('UPDATE Characters SET ' + BASE_STATS[0][i] + ' = ' + str(Player.data[i]) + ' WHERE CharID = ' +
                        str(Player.charID))
    sql = c.execute('UPDATE Characters SET FreePoints = ' + str(Player.freePoints) + ' WHERE CharID = ' +
                    str(Player.charID))
    sql = c.execute('UPDATE Characters SET Progress = ' + str(Player.progress) + ' WHERE CharID = ' + 
                    str(Player.charID))
    sql = c.execute('UPDATE Characters SET Corruption = ' + str(Player.corruption) + ' WHERE CharID = ' +
                    str(Player.charID))
    sql = c.execute('UPDATE Characters SET CharExp = ' + str(Player.exp) + ' WHERE CharID = ' + str(Player.charID))
    sql = c.execute('UPDATE Characters SET Stress = ' + str(Player.stress) + ' WHERE CharID = ' + str(Player.charID))
    con.commit()


# Create a new character and insert into database
def insert_character(Player):
    insertion = ('INSERT INTO Characters(CharID, CharName, CharLevel, Initiative, Health, Strength, Endurance, '
                 'Durability, Agility, Accuracy, InventoryCap, FreePoints, CharExp, Corruption, Stress, Progress) '
                 'Values (' + str(Player.charID) + ', "' + str(Player.name) + '", ' + str(Player.level) + ', ' +
                 str(Player.data[INITIATIVE]) + ', ' + str(Player.data[HEALTH]) + ', ' + str(Player.data[STRENGTH]) + 
                 ', ' + str(Player.data[ENDURANCE]) + ', ' + str(Player.data[DURABILITY]) + ', ' + 
                 str(Player.data[AGILITY]) + ', ' + str(Player.data[ACCURACY]) + ', ' + str(Player.data[INITIATIVE]) + 
                 ', ' + str(Player.freePoints) + ',' + str(Player.exp) + ',' + str(Player.corruption) + ', ' + 
                 str(Player.stress) + ', ' + str(Player.progress) + ')')
    sql = c.execute(insertion)
    con.commit()


# Insert weapons into database
def update_weapons(wID, quality, charID, typeID):
    insertion = ('INSERT INTO Weapons(WeaponID, Quality, CharID, TypeID) Values (' +
                 str(wID) + ', ' + str(quality) + ', ' + str(charID) + ', ' + str(typeID) + ')')
    sql = c.execute(insertion)
    con.commit()


# Update the weapon quality
def update_quality(quality, wID):
    sql = c.execute('UPDATE Weapons SET Quality = ' + str(quality) + ' WHERE WeaponID = ' + str(wID))
    con.commit()


# Delete a character from database and all associated weapons
def delete_character(charID):
    delete2 = ('DELETE FROM Weapons WHERE CharID = ' + str(charID))
    delete1 = ('DELETE FROM Characters WHERE CharID = ' + str(charID))
    sql = c.execute(delete1)
    sql = c.execute(delete2)
    con.commit()


# Get a new id for a new character
def get_id(obj):
    if obj == 0:
        sql = c.execute('SELECT CharID FROM Characters')
    else:
        sql = c.execute('SELECT WeaponID FROM Weapons')
    data = c.fetchall()
    if data:
        arr = []
        for i in range(0, len(data)):
            arr.append(data[i][0])
        for j in range(1, len(data)):
            if j not in arr:
                return j
        return len(data) + 1
    else:
        return 1


# Get the list of characters
def get_character_list():
    sql = c.execute("SELECT CharName, CharID FROM Characters")
    data = c.fetchall()
    return data


# Check if character is in database
def in_database(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data


# Get column table names and return it
def get_table_data(table):
    sql = c.execute('PRAGMA table_info(' + table + ')')
    data = c.fetchall()
    return data


# Get the corruption value of the choice the user took
def check_corruption(choice):
    sql = c.execute('SELECT CorruptionValue FROM Storyline WHERE TextID = ' + str(choice))
    data = c.fetchall()
    return data[0][0]


# Get the event of the current scene
def get_event(choiceID):
    sql = c.execute('SELECT StoryEvent FROM Storyline WHERE TextID = ' + str(choiceID))
    data = c.fetchall()
    return data[0][0]


# Get the description of the phase you're in
def get_phase_description(currState):
    sql = c.execute('SELECT PhaseDescription FROM EventPhase WHERE PhaseID = ' + str(currState))
    data = c.fetchall()
    return data[0][0]


# Get the difficulty level of the event
def get_difficulty(eventID):
    sql = c.execute('SELECT Difficulty FROM Event WHERE EventID = ' + str(eventID))
    difficulty = c.fetchall()
    return difficulty[0][0]


# Get the initiative cost of an action
def get_initiative_cost(currState, choice):
    sql = c.execute('SELECT InitiativeCost FROM PhaseOption WHERE PhaseID = ' + str(currState) +
                    ' AND OptionType = ' + str(choice))
    data = c.fetchall()
    return data[0][0]
