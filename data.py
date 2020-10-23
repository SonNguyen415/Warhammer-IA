from config import *


# Get the current scene the saved character is at
def get_curr_progress(charID):
    sql = c.execute('SELECT Progress FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0][0]


# Get the quality of a given weapon
def get_weapon_quality(typeID):
    sql = c.execute('SELECT Reliability FROM TypeOfWeapon WHERE TypeID = ' + str(typeID))
    data = c.fetchall()
    return data[0][0]


# Get the size of a given weapon
def get_weapon_size(typeID):
    sql = c.execute('SELECT WeaponSize FROM TypeOfWeapon WHERE TypeID = ' + str(typeID))
    data = c.fetchall()
    return data[0][0]


# Get my weapons
def get_my_weapons(charID):
    sql = c.execute('SELECT WeaponID, Quality, WeaponType FROM Weapons JOIN TypeOfWeapon WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Get all the weapons that you can buy
def get_purchasable_weapons(charID):
    sql = c.execute('SELECT WeaponType FROM TypeOfWeapon WHERE WeaponLevel <= ' + str(charID))
    data = c.fetchall()
    return data[0]


# Get the stats of a given weapon
def get_weapon_data(wID):
    sql = c.execute('SELECT * FROM TypeOfWeapon WHERE TypeID = ' + str(wID))
    data = c.fetchall()
    return data[0]


# Get weapon type
def get_weapon_type(wID):
    sql = c.execute('SELECT WeaponType FROM TypeOfWeapon WHERE TypeID = ' + str(wID))
    data = c.fetchall()
    return data[0][0]


# Get the info of the characters
def get_character_data(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Change character stats
def update_character(charID, lvl, val, fP, corruption, exp, stress):
    sql = c.execute('UPDATE Characters SET CharLevel = ' + str(lvl) + ' WHERE CharID = ' + str(charID))
    for i in range(0, len(BASE_STATS[0])):
        sql = c.execute('UPDATE Characters SET ' + BASE_STATS[0][i] + ' = ' + str(val[i]) + ' WHERE CharID = ' +
                        str(charID))
    sql = c.execute('UPDATE Characters SET FreePoints = ' + str(fP) + ' WHERE CharID = ' + str(charID))
    sql = c.execute('UPDATE Characters SET Progress = ' + str(currScene) + ' WHERE CharID = ' + str(charID))
    sql = c.execute('UPDATE Characters SET CharCorruption = ' + str(corruption) + ' WHERE CharID = ' + str(charID))
    sql = c.execute('UPDATE Characters SET CharExp = ' + str(exp) + ' WHERE CharID = ' + str(charID))
    sql = c.execute('UPDATE Characters SET Stress = ' + str(stress) + ' WHERE CharID = ' + str(charID))
    con.commit()


# Create a new character and insert into database
def insert_character(charID, cName, cLevel, cData, cFP, cCorruption, cExp, cStress):
    insertion = ('INSERT INTO Characters(CharID, CharName, CharLevel, Strength, Endurance, Durability, Agility,'
                 'Accuracy, InventoryCap, FreePoints, Progress, CharCorruption, CharExp, Stress, Health) Values (' +
                 str(charID) + ', "' + str(cName) + '", ' + str(cLevel) + ', ' + str(cData[0]) + ', ' +
                 str(cData[1]) + ', ' + str(cData[2]) + ', ' + str(cData[3]) + ', ' + str(cData[4]) + ', ' +
                 str(cData[5]) + ', ' + str(cFP) + ',' + str(currScene) + ',' + str(cCorruption) + ', ' + str(cExp) +
                 ', ' + str(cStress) + ')')
    sql = c.execute(insertion)
    con.commit()


# Insert weapons into database
def update_weapons(wID, quality, charID, typeID):
    insertion = ('INSERT INTO Weapons(WeaponID, Quality, CharID, TypeID) Values (' +
                 str(wID) + ', ' + str(quality) + ', ' + str(charID) + ', ' + str(typeID) + ')')
    sql = c.execute(insertion)
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
            print(j in arr)
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


def check_corruption(charID):
    return 5


# Show data of given weapon
def show_weapon_data(weapon):
    wData = get_weapon_data(weapon)
    for attr in wData:
        print(attr)
