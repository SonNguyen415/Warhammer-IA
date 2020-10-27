from config import *


# Get the current scene the saved character is at
def get_curr_progress(charID):
    sql = c.execute('SELECT Progress FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0][0]


# Get all weapon id
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


def get_ai_weapon(enemyID):
    sql = c.execute('SELECT TypeID FROM EnemyWeapons WHERE EnemyID = ' + str(enemyID))
    data = c.fetchall()
    return data[0]


# Get the info of the characters
def get_character_data(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Change character stats
def update_character(Player):
    sql = c.execute('UPDATE Characters SET CharLevel = ' + str(Player.level) + ' WHERE CharID = ' + str(Player.charID))
    for i in range(0, len(BASE_STATS[0])):
        sql = c.execute('UPDATE Characters SET ' + BASE_STATS[0][i] + ' = ' + str(Player.data[i]) + ' WHERE CharID = ' +
                        str(Player.charID))
    sql = c.execute('UPDATE Characters SET FreePoints = ' + str(Player.freePoints) + ' WHERE CharID = ' +
                    str(Player.charID))
    sql = c.execute(
        'UPDATE Characters SET Progress = ' + str(Player.progress) + ' WHERE CharID = ' + str(Player.charID))
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
                 str(Player.data[0]) + ', ' + str(Player.data[1]) + ', ' + str(Player.data[2]) + ', ' +
                 str(Player.data[3]) + ', ' + str(Player.data[4]) + ', ' + str(Player.data[5]) + ', ' +
                 str(Player.data[6]) + ', ' + str(Player.data[7]) + ', ' + str(Player.freePoints) + ',' +
                 str(Player.exp) + ',' + str(Player.corruption) + ', ' + str(Player.stress) + ', ' +
                 str(Player.progress) + ')')
    sql = c.execute(insertion)
    con.commit()


# Insert weapons into database
def update_weapons(wID, quality, charID, typeID):
    insertion = ('INSERT INTO Weapons(WeaponID, Quality, CharID, TypeID) Values (' +
                 str(wID) + ', ' + str(quality) + ', ' + str(charID) + ', ' + str(typeID) + ')')
    sql = c.execute(insertion)
    con.commit()


def update_quality(quality, wID):
    sql = c.execute('UPDATE Weapons SET Quality = ' + str(quality) + ' WHERE WeaponID = ' + str(wID))
    con.commit()


# Delete a character from database and all associated weapons
def delete_character(charID):
    delete1 = ('DELETE FROM Characters WHERE CharID = ' + str(charID))
    # delete2 = ('DELETE FROM Weapons WHERE CharID = ' + str(charID))
    sql = c.execute(delete1)
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
def not_in_database(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return not data


def get_table_data(table):
    sql = c.execute('PRAGMA table_info(' + table + ')')
    data = c.fetchall()
    return data


def check_corruption(choice):
    sql = c.execute('SELECT CorruptionValue FROM Storyline WHERE TextID = ' + str(choice))
    data = c.fetchall()
    return data[0][0]
