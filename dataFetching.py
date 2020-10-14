from config import *


def get_curr_progress(charID):
    sql = c.execute('SELECT Progress FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0][0]


def get_weapon_quality(typeID):
    sql = c.execute('SELECT Reliability FROM TypeOfWeapon WHERE TypeID = ' + str(typeID))
    data = c.fetchall()
    return data[0][0]

def get_weapon_size(typeID):
    sql = c.execute('SELECT WeaponSize FROM TypeOfWeapon WHERE TypeID = ' + str(typeID))
    data = c.fetchall()
    return data[0][0]


def get_my_weapons(charID):
    sql = c.execute('SELECT WeaponID, Quality, WeaponType FROM Weapons WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Get all the weapons that you can buy
def get_purchasable_weapons(charID):
    sql = c.execute('SELECT WeaponType FROM TypeOfWeapon WHERE WeaponLevel <= ' + str(charID))
    data = c.fetchall()
    return data[0]


# Get the stats of a given weapon
def get_weapon_data(weapon):
    sql = c.execute('SELECT * FROM TypeOfWeapon WHERE WeaponType = "' + str(weapon) + '"')
    data = c.fetchall()
    return data[0]


# Get the info of the characters
def get_character_data(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Change character stats
def update_character(charID, lvl, val, fP):
    sql = c.execute('UPDATE Characters SET CharLevel = ' + str(lvl) + ' WHERE CharID = ' + str(charID))
    for i in range(0, len(BASE_STATS[0])):
        sql = c.execute('UPDATE Characters SET ' + BASE_STATS[0][i] + ' = ' + str(val[i]) + ' WHERE CharID = ' +
                        str(charID))
    sql = c.execute('UPDATE Characters SET FreePoints = ' + str(fP) + ' WHERE CharID = ' + str(charID))
    sql = c.execute('UPDATE Characters SET Progress = ' + str(currScene) + ' WHERE CharID = ' + str(charID))
    con.commit()


# Create a new character and insert into database
def insert_character(charID, cName, cLevel, cData, cFP):
    insertion = ('INSERT INTO Characters(CharID, CharName, CharLevel, Strength, '
                 'Endurance, Durability, Agility, Accuracy, InventoryCap, FreePoints, Progress) Values (' +
                 str(charID) + ', "' + str(cName) + '", ' + str(cLevel) + ', ' + str(cData[0]) + ', ' +
                 str(cData[1]) + ', ' + str(cData[2]) + ', ' + str(cData[3]) + ', ' + str(cData[4]) + ', ' +
                 str(cData[5]) + ', ' + str(cFP) + ',' + str(currScene) + ')')
    sql = c.execute(insertion)
    con.commit()


# Insert weapons into database
def update_weapons(quantity, charID, wID, ):
    insertion = ('INSERT INTO Ownership(Quantity, CharID, WeaponName) ' +
                 'Values (' + str(quantity) + ',' + str(charID) + ',"' + str(weaponName) + '")')
    sql = c.execute(insertion)
    con.commit()


# Delete a character from database
def delete_character(charID):
    insertion = ('DELETE FROM Characters WHERE CharID = ' + str(charID))
    sql = c.execute(insertion)
    con.commit()


# Get a new id for a new character
def get_id(type):
    if type == 0:
        sql = c.execute('SELECT CharID FROM Characters')
    else:
        sql = c.execute('SELECT WeaponID FROM Weapons')
    data = c.fetchall()
    if data:
        arr = []
        for i in range(0, len(data)):
            arr.append(data[i][0])
        for j in range(1, 20):
            if j not in arr:
                return j
        return 0
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
