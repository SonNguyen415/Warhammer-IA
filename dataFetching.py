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


def get_my_weapons(charID):
    sql = c.execute('SELECT WeaponName FROM Ownership WHERE CharID = ' + str(charID))
    data = c.fetchall()
    return data[0]


def get_purchable_weapons(charID):
    sql = c.execute('SELECT WeaponName FROM Weapons WHERE WeaponLevel <= ' + str(charID))
    data = c.fetchall()
    return data[0]


def get_weapon_data(weapon):
    sql = c.execute('SELECT * FROM Weapons WHERE WeaponName = "' + str(weapon) + '"')
    data = c.fetchall()
    return data[0]


def show_character(charID):
    for attr in BASE_STATS[0]:
        sql = c.execute('SELECT ' + attr + ' FROM Characters WHERE CharID = ' + str(charID))
        data = c.fetchall()
        print(attr + ": " + str(data[0][0]))


def change_character(charID, val, attr):
    sql = c.execute('SELECT ' + attr + ' FROM Characters WHERE CharID = ' + str(charID))
    data = c.fetchall()
    newVal = val + data[0][0]
    update = ('UPDATE Characters SET ' + attr + ' = ' + str(newVal) + ' WHERE CharID = ' + str(charID))
    sql = c.execute(update)
    con.commit()


def insert_character(charName, charID):
    insertion = ('INSERT INTO Characters(CharID, CharName, CharLevel, Strength, '
                 'Endurance, Durability, Agility, Accuracy, InventoryCap) Values (' + str(charID) + ', "' + str(charName)
                 + '", 1, ' + str(BASE_STATS[1][0]) + ',' + str(BASE_STATS[1][1]) + ',' + str(BASE_STATS[1][2]) + ',' +
                 str(BASE_STATS[1][3]) + ',' + str(BASE_STATS[1][4]) + ',' + str(BASE_STATS[1][5]) + ',' + ')')
    sql = c.execute(insertion)
    con.commit()


def provide_weapons(quantity, charID, weaponName):
    insertion = ('INSERT INTO Ownership(Quantity, CharID, WeaponName) ' +
                 'Values (' + str(quantity) + ',' + str(charID) + ',"' + str(weaponName) + '")')
    sql = c.execute(insertion)
    con.commit()


def delete_character(charID):
    insertion = ('DELETE FROM Characters WHERE CharID = ' + str(charID))
    sql = c.execute(insertion)
    con.commit()


def get_id():
    sql = c.execute('SELECT CharID FROM Characters')
    data = c.fetchall()
    if data:
        for i in range(0, 10):
            if i not in data[0]:
                return i
    else:
        return 1
    return 0


def get_character_list():
    sql = c.execute("SELECT CharName, CharID FROM Characters")
    data = c.fetchall()
    return data
