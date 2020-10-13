import sqlite3 as sq

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

#
currScene = 1
currChar = 0
Player = object

TIME_STOP = 0
START_PTS = 5
ASC_POINTS = 5
BASE_STATS = [["Strength", "Endurance", "Durability", "Agility", "Accuracy", "InventoryCap"],
              [5, 5, 5, 5, 5, 25]]

intro = open('database/intro.txt', 'r')
introContent = intro.read()


def get_curr_progress(charID):
    sql = c.execute('SELECT Progress FROM Characters WHERE CharID = ' + str(charID))
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
def get_purchable_weapons(charID):
    sql = c.execute('SELECT WeaponType FROM TypeOfWeapon WHERE WeaponLevel <= ' + str(charID))
    data = c.fetchall()
    return data[0]


# Get the stats of a given weapon
def get_weapon_data(weapon):
    sql = c.execute('SELECT * FROM TypeOfWeapon WHERE WeaponType = "' + str(weapon) + '"')
    data = c.fetchall()
    return data[0]


def get_character_data(charID):
    sql = c.execute('SELECT * FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


# Change character stats
def change_character(charID, val, attr):
    sql = c.execute('SELECT ' + attr + ' FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    newVal = val + data[0][0]
    update = ('UPDATE Characters SET ' + attr + ' = ' + str(newVal) + ' WHERE CharID = ' + str(charID))
    sql = c.execute(update)
    con.commit()


# Create a new character and insert into database
def insert_character(cName, cLevel, cData, cFP):
    insertion = ('INSERT INTO Characters(CharID, CharName, CharLevel, Strength, '
                 'Endurance, Durability, Agility, Accuracy, InventoryCap, FreePoints, Progress) Values (' +
                 str(currChar) + ', "' + str(cName) + '", ' + str(cLevel) + ', ' + str(cData[0]) + ', ' +
                 str(cData[1]) + ', ' + str(cData[2]) + ', ' + str(cData[3]) + ', ' + str(cData[4]) + ', ' +
                 str(cData[5]) + ', ' + str(cFP) + ',' + str(currScene) + ')')
    sql = c.execute(insertion)
    con.commit()


# Insert weapons into database
def provide_weapons(quantity, charID, weaponName):
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
def get_id():
    sql = c.execute('SELECT CharID FROM Characters')
    data = c.fetchall()
    if data:
        return len(data) + 1
    else:
        return 1


# Get the list of characters
def get_character_list():
    sql = c.execute("SELECT CharName, CharID FROM Characters")
    data = c.fetchall()
    return data
